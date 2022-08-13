from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import timedelta
from http import HTTPStatus
from pathlib import Path
from typing import AsyncGenerator, Optional

from aiohttp import ClientSession, web
from cachetools import TTLCache
from gidgethub.aiohttp import GitHubAPI
from structlog import get_logger

from ancv.data.validation import is_valid_github_username
from ancv.exceptions import ResumeConfigError, ResumeLookupError
from ancv.timing import Stopwatch
from ancv.visualization.templates import Template
from ancv.web import is_terminal_client
from ancv.web.client import get_resume

LOGGER = get_logger()


@dataclass
class ServerContext:
    host: Optional[str]
    port: Optional[int]
    path: Optional[str]


class Runnable(ABC):
    @abstractmethod
    def run(self, context: ServerContext) -> None:
        ...


class APIHandler(Runnable):
    def __init__(
        self,
        requester: str,
        token: Optional[str],
        homepage: str,
        landing_page: str,
    ) -> None:
        self.requester = requester
        self.token = token
        self.homepage = homepage
        self.landing_page = landing_page

        LOGGER.debug("Instantiating web application.")
        self.app = web.Application()

        LOGGER.debug("Adding routes.")
        self.app.add_routes(
            [
                web.get("/", self.root),
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
        user_agent = request.headers.get("User-Agent", "")

        if is_terminal_client(user_agent):
            return web.Response(text=f"Visit {self.homepage} to get started.\n")

        raise web.HTTPFound(self.landing_page)  # Redirect

    async def username(self, request: web.Request) -> web.Response:
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
        session: ClientSession = request.app["client_session"]
        github: GitHubAPI = request.app["github"]

        log = log.bind(user=user)

        stopwatch.stop()
        try:
            resume = await get_resume(
                user=user, session=session, github=github, stopwatch=stopwatch
            )
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
    def __init__(self, file: Path) -> None:
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
        LOGGER.debug("Serving rendered template.", request=request)
        return web.Response(text=self.rendered)


def server_timing_header(timings: dict[str, timedelta]) -> str:
    """https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Server-Timing"""

    # For controlling `timedelta` conversion precision, see:
    # https://docs.python.org/3/library/datetime.html#datetime.timedelta.total_seconds
    # E.g., `td.microseconds` will return `0` for `timedelta(seconds=1)`, not 1e6.

    return ", ".join(
        f"{name.replace(' ', '-')};dur={duration // timedelta(milliseconds=1)}"
        for name, duration in timings.items()
    )
