import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import AsyncGenerator, Optional

from aiohttp import ClientSession, web
from cachetools import TTLCache
from gidgethub.aiohttp import GitHubAPI
from structlog import get_logger

from ancv.exceptions import ResumeConfigError, ResumeLookupError
from ancv.reflection import METADATA
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
    def run(self, context: ServerContext) -> None:
        LOGGER.debug("Instantiating web application.")
        app = web.Application()

        LOGGER.debug("Adding routes.")
        app.add_routes(
            [
                web.get("/", self.root),
                web.get("/{username}", self.username),
            ]
        )

        app.cleanup_ctx.append(self.app_context)

        LOGGER.info("Loaded, starting server...")
        web.run_app(app, host=context.host, port=context.port, path=context.path)

    @staticmethod
    async def app_context(app: web.Application) -> AsyncGenerator[None, None]:
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
            requester=os.environ.get("GH_REQUESTER", METADATA.name),
            oauth_token=os.environ.get("GH_TOKEN", None),
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

        HOMEPAGE = os.environ.get("HOMEPAGE", METADATA.home_page or "")

        if is_terminal_client(user_agent):
            return web.Response(text=f"Visit {HOMEPAGE} to get started.\n")

        # When visiting this endpoint in a browser, we want to redirect to the homepage.
        # That page cannot be this same path under the same hostname again, else we get a
        # loop.
        browser_page = os.environ.get(
            "LANDING_PAGE",
            METADATA.project_url[0] if METADATA.project_url else "https://github.com/",
        )

        raise web.HTTPFound(browser_page)  # Redirect

    async def username(self, request: web.Request) -> web.Response:
        log = LOGGER.bind(request=request)
        log.info(request.message.headers)

        user = request.match_info["username"]

        # Implicit 'downcasting' from `Any` doesn't require an explicit `cast` call, just
        # regular type hints:
        # https://adamj.eu/tech/2021/07/06/python-type-hints-how-to-use-typing-cast/
        session: ClientSession = request.app["client_session"]
        github: GitHubAPI = request.app["github"]

        log = log.bind(user=user)

        try:
            resume = await get_resume(user=user, session=session, github=github)
        except ResumeLookupError as e:
            log.warning(str(e))
            return web.Response(text=str(e))
        else:
            try:
                template = Template.from_model_config(resume)
            except ResumeConfigError as e:
                log.warning(str(e))
                return web.Response(text=str(e))
            log.debug("Serving rendered template.")
            return web.Response(text=template.render())


class FileHandler(Runnable):
    def __init__(self, file: Path) -> None:
        self.template = Template.from_file(file)
        self.rendered = self.template.render()

    def run(self, context: ServerContext) -> None:
        LOGGER.debug("Instantiating web application.")
        app = web.Application()

        LOGGER.debug("Adding routes.")
        app.add_routes([web.get("/", self.root)])

        LOGGER.info("Loaded, starting server...")
        web.run_app(app, host=context.host, port=context.port, path=context.path)

    async def root(self, request: web.Request) -> web.Response:
        LOGGER.debug("Serving rendered template.", request=request)
        return web.Response(text=self.rendered)
