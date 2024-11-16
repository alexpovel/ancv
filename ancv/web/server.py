import json
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import timedelta
from http import HTTPStatus
from pathlib import Path
from pydantic import ValidationError
from typing import AsyncGenerator, Optional

from aiohttp import ClientSession, ClientError, web
from cachetools import TTLCache
from gidgethub.aiohttp import GitHubAPI
from structlog import get_logger

from ancv import PROJECT_ROOT
from ancv.data.models.resume import ResumeSchema
from ancv.data.validation import is_valid_github_username
from ancv.exceptions import ResumeConfigError, ResumeLookupError
from ancv.timing import Stopwatch
from ancv.visualization.templates import Template
from ancv.web.client import get_resume

LOGGER = get_logger()

SHOWCASE_RESUME = Template.from_file(
    PROJECT_ROOT / "data" / "showcase.resume.json"
).render()

SHOWCASE_USERNAME = "heyho"


def is_terminal_client(user_agent: str) -> bool:
    """Determines if a user agent string indicates a terminal client."""

    terminal_clients = [
        "curl",
        "wget",
        "powershell",
    ]

    for client in terminal_clients:
        if client.lower() in user_agent.lower():
            return True
    return False


@dataclass
class ServerContext:
    """Context for the server."""

    host: Optional[str]
    port: Optional[int]
    path: Optional[str]


class Runnable(ABC):
    """A server object that can be `run`, enabling different server implementations."""

    @abstractmethod
    def run(self, context: ServerContext) -> None: ...


class APIHandler(Runnable):
    """A runnable server for handling dynamic API requests.

    This is the core application server powering the API. It is responsible for handling
    requests for the resume of a given user, and returning the appropriate response. It
    queries the live GitHub API.
    """

    def __init__(
        self,
        requester: str,
        token: Optional[str],
        terminal_landing_page: str,
        browser_landing_page: str,
    ) -> None:
        """Initializes the handler.

        Args:
            requester: The user agent to use for the GitHub API requests.
            token: The token to use for the GitHub API requests.
            terminal_landing_page: URL to "redirect" to for requests to the root from a
                *terminal* client.
            browser_landing_page: URL to redirect to for requests to the root from a
                *browser* client.
        """

        self.requester = requester
        self.token = token
        self.terminal_landing_page = terminal_landing_page
        self.browser_landing_page = browser_landing_page

        LOGGER.debug("Instantiating web application.")
        self.app = web.Application()

        LOGGER.debug("Adding routes.")
        self.app.add_routes(
            [
                # Order matters, see also https://www.grandmetric.com/2020/07/08/routing-order-in-aiohttp-library-in-python/
                web.get("/", self.root),
                web.get(f"/{SHOWCASE_USERNAME}", self.showcase),
                web.get("/{username}", self.username),
            ]
        )

        self.app.cleanup_ctx.append(self.app_context)

    def run(self, context: ServerContext) -> None:
        LOGGER.info("Loaded, starting server...")
        web.run_app(self.app, host=context.host, port=context.port, path=context.path)

    async def app_context(self, app: web.Application) -> AsyncGenerator[None, None]:
        """For an `aiohttp.web.Application`, provides statefulness by attaching objects.

        See also:
            - https://docs.aiohttp.org/en/stable/web_advanced.html#data-sharing-aka-no-singletons-please
            - https://docs.aiohttp.org/en/stable/web_advanced.html#cleanup-context

        Args:
            app: The app instance to attach our state to. It can later be retrieved,
                such that all app components use the same session etc.
        """
        log = LOGGER.bind(app=app)
        log.debug("App context initialization starting.")

        log.debug("Starting client session.")
        session = ClientSession()
        log = log.bind(session=session)
        log.debug("Started client session.")

        log.debug("Creating GitHub API instance.")
        github = GitHubAPI(
            session,
            requester=self.requester,
            oauth_token=self.token,
            cache=TTLCache(maxsize=1e2, ttl=60),
        )
        log = log.bind(github=github)
        log.debug("Created GitHub API instance.")

        app["client_session"] = session
        app["github"] = github

        log.debug("App context initialization done, yielding.")

        yield

        log.debug("App context teardown starting.")

        log.debug("Closing client session.")
        await app["client_session"].close()
        log.debug("Closed client session.")

        log.info("App context teardown done.")

    async def root(self, request: web.Request) -> web.Response:
        """The root endpoint, redirecting to the landing page."""

        user_agent = request.headers.get("User-Agent", "")

        if is_terminal_client(user_agent):
            return web.Response(
                text=f"Visit {self.terminal_landing_page} to get started.\n"
            )

        raise web.HTTPFound(self.browser_landing_page)  # Redirect

    async def showcase(self, request: web.Request) -> web.Response:
        """The showcase endpoint, returning a static resume."""

        return web.Response(text=SHOWCASE_RESUME)

    async def username(self, request: web.Request) -> web.Response:
        """The username endpoint, returning a dynamic resume from a user's gists."""

        stopwatch = Stopwatch()
        stopwatch(segment="Initialize Request")

        log = LOGGER.bind(request=request)
        log.info(request.message.headers)

        user = request.match_info["username"]

        if not is_valid_github_username(user):
            raise web.HTTPBadRequest(reason=f"Invalid username: {user}")

        # Implicit 'downcasting' from `Any` doesn't require an explicit `cast` call, just
        # regular type hints:
        # https://adamj.eu/tech/2021/07/06/python-type-hints-how-to-use-typing-cast/
        github: GitHubAPI = request.app["github"]

        log = log.bind(user=user)

        stopwatch.stop()
        try:
            resume = await get_resume(user=user, github=github, stopwatch=stopwatch)
        except ResumeLookupError as e:
            stopwatch.stop()
            log.warning(str(e))
            return web.Response(text=str(e), status=HTTPStatus.NOT_FOUND)
        else:
            stopwatch(segment="Templating")
            try:
                template = Template.from_model_config(resume)
            except ResumeConfigError as e:
                log.warning(str(e))
                return web.Response(text=str(e))

            stopwatch(segment="Rendering")
            resp = web.Response(text=template.render())
            stopwatch.stop()

            resp.headers["Server-Timing"] = server_timing_header(stopwatch.timings)

            log.debug("Serving rendered template.")
            return resp


class FileHandler(Runnable):
    """A handler serving a rendered, static template loaded from a file at startup."""

    def __init__(self, file: Path) -> None:
        """Initializes the handler.

        Args:
            file: The (JSON Resume) file to load the template from.
        """

        self.template = Template.from_file(file)
        self.rendered = self.template.render()

        LOGGER.debug("Instantiating web application.")
        self.app = web.Application()

        LOGGER.debug("Adding routes.")
        self.app.add_routes([web.get("/", self.root)])

    def run(self, context: ServerContext) -> None:
        LOGGER.info("Loaded, starting server...")
        web.run_app(self.app, host=context.host, port=context.port, path=context.path)

    async def root(self, request: web.Request) -> web.Response:
        """The root and *only* endpoint, returning the rendered template."""

        LOGGER.debug("Serving rendered template.", request=request)
        return web.Response(text=self.rendered)


def server_timing_header(timings: dict[str, timedelta]) -> str:
    """From a mapping of names to `timedelta`s, return a `Server-Timing` header value.

    See also: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Server-Timing
    """

    # For controlling `timedelta` conversion precision, see:
    # https://docs.python.org/3/library/datetime.html#datetime.timedelta.total_seconds
    # E.g., `td.microseconds` will return `0` for `timedelta(seconds=1)`, not 1e6.

    return ", ".join(
        f"{name.replace(' ', '-')};dur={duration // timedelta(milliseconds=1)}"
        for name, duration in timings.items()
    )


class RenderError(Exception):
    """Base exception for resume rendering failures"""

    pass


class TemplateRenderError(RenderError):
    """Raised when template rendering fails"""

    pass


class InvalidResumeDataError(RenderError):
    """Raised when resume data is invalid"""

    pass


class WebHandler(Runnable):
    """A handler serving a rendered template loaded from a URL with periodic refresh."""

    def __init__(
        self, destination: str, refresh_interval: timedelta = timedelta(seconds=300)
    ) -> None:
        """Initializes the handler.

        Args:
            destination: The URL to load the JSON Resume from.
            refresh_interval: How often to refresh the resume.
        """
        self.destination = destination
        self.refresh_interval = refresh_interval
        self.cache: str = ""
        self.last_fetch: float = 0
        self._last_valid_render: str = ""

        LOGGER.debug("Instantiating web application.")
        self.app = web.Application()
        LOGGER.debug("Adding routes.")
        self.app.add_routes([web.get("/", self.root)])
        self.app.cleanup_ctx.append(self.app_context)

    def run(self, context: ServerContext) -> None:
        LOGGER.info("Loaded, starting server...")
        web.run_app(self.app, host=context.host, port=context.port, path=context.path)

    async def app_context(self, app: web.Application) -> AsyncGenerator[None, None]:
        """Sets up the application context with required clients.

        Args:
            app: The app instance to attach our state to.
        """
        log = LOGGER.bind(app=app)
        log.debug("App context initialization starting.")
        log.debug("Starting client session.")
        session = ClientSession()
        app["client_session"] = session
        log.debug("Started client session.")
        log.debug("App context initialization done, yielding.")
        yield
        log.debug("App context teardown starting.")
        await session.close()
        log.debug("App context teardown done.")

    async def fetch(self, session: ClientSession) -> ResumeSchema:
        """Fetches and validates resume JSON from the destination URL.

        Args:
            session: The aiohttp client session to use for requests.

        Returns:
            ResumeSchema: The validated resume data
            web.Response: Error response when:
                - Resume cannot be fetched from destination (NOT_FOUND)
                - Response is not valid JSON (BAD_REQUEST)
                - JSON data doesn't match resume schema
        """
        async with session.get(self.destination) as response:
            if response.status != HTTPStatus.OK:
                raise RenderError(f"Failed to fetch resume from {self.destination}")
            content = await response.text()
            try:
                resume_data = json.loads(content)
                return ResumeSchema(**resume_data)
            except json.JSONDecodeError:
                raise InvalidResumeDataError("Invalid JSON format in resume data")

    def render(self, resume_data: ResumeSchema) -> str:
        """Renders resume data into a formatted template string.

        Args:
            resume_data: The resume data dictionary to render

        Returns:
            str: The successfully rendered resume template
            web.Response: Error response when:
                - Resume data doesn't match expected schema
                - Template rendering fails
        """
        try:
            template = Template.from_model_config(resume_data)
            rendered = template.render()
            if not rendered:
                raise TemplateRenderError("Template rendering failed")
            return rendered
        except ResumeConfigError:
            raise InvalidResumeDataError("Resume configuration error")

    async def root(self, request: web.Request) -> web.Response:
        """The root endpoint, returning the rendered template with periodic refresh.

        Implements a caching mechanism that refreshes the resume data at configured intervals.
        Uses monotonic time to ensure reliable cache invalidation. Falls back to cached version
        if refresh fails.

        Args:
            request: The incoming web request containing the client session

        Returns:
            web.Response: Contains either:
                - Fresh or cached rendered template as text
                - Error message with SERVICE_UNAVAILABLE status when no cache exists

        Note:
            Cache refresh occurs when:
            - No cache exists
            - No previous fetch timestamp exists
            - Refresh interval has elapsed since last fetch
        """
        log = LOGGER.bind(request=request)
        session: ClientSession = request.app["client_session"]

        current_time = time.monotonic()
        should_refresh = (
            not self.cache
            or (current_time - self.last_fetch) > self.refresh_interval.total_seconds()
        )

        if should_refresh:
            log.debug("Fetching fresh resume data.")
            try:
                resume_data = await self.fetch(session)
                rendered = self.render(resume_data)
                self._last_valid_render = rendered
                self.cache = rendered
                self.last_fetch = current_time
            except (ClientError, ValidationError) as exc:
                log.error("Network or validation error", error=str(exc))
                if self._last_valid_render:
                    self.cache = self._last_valid_render
                    log.warning("Using last valid render as fallback")
                else:
                    return web.Response(
                        text="No cache available", status=HTTPStatus.SERVICE_UNAVAILABLE
                    )
            except (RenderError, InvalidResumeDataError) as exc:
                log.error("Resume rendering error", error=str(exc))
                if self._last_valid_render:
                    self.cache = self._last_valid_render
                    log.warning("Using last valid render as fallback")
                else:
                    return web.Response(
                        text="Unable to render resume",
                        status=HTTPStatus.INTERNAL_SERVER_ERROR,
                    )

        log.debug("Serving rendered template.")
        return web.Response(text=self.cache)
