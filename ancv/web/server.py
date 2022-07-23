import os
from typing import AsyncGenerator, Optional

from aiohttp import ClientSession, web
from cachetools import TTLCache
from gidgethub.aiohttp import GitHubAPI
from structlog import get_logger

from ancv import METADATA
from ancv.utils.exceptions import ResumeConfigError, ResumeLookupError
from ancv.visualization.templates import Template
from ancv.web.client import get_resume

LOGGER = get_logger()

_ROUTES = web.RouteTableDef()


def run(host: Optional[str], port: Optional[int], path: Optional[str]) -> None:
    LOGGER.debug("Instantiating web application.")
    app = web.Application()
    LOGGER.debug("Adding routes.")
    app.add_routes(_ROUTES)
    app.cleanup_ctx.append(app_context)
    LOGGER.info("Loaded, starting server...")
    web.run_app(app, host=host, port=port, path=path)


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


def is_terminal_client(user_agent: str) -> bool:
    user_agent = user_agent.lower()
    return any(
        client in user_agent
        for client in [
            "curl",
            "wget",
            "powershell",
        ]
    )


@_ROUTES.get("/")
async def root(request: web.Request) -> web.Response:
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


@_ROUTES.get("/{username}")
async def username(request: web.Request) -> web.Response:
    log = LOGGER
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
        return web.Response(text=template.render())
