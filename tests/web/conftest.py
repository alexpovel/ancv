import pytest
from aiohttp.web import Application

from ancv.reflection import METADATA
from ancv.web.server import APIHandler, FileHandler
from tests import DATA_DIR, GH_TOKEN, RESUMES


@pytest.fixture(scope="function")
def api_client_app() -> Application:
    return APIHandler(
        requester=f"{METADATA.name}-PYTEST-REQUESTER",
        token=GH_TOKEN,
        terminal_landing_page=f"{METADATA.name}-PYTEST-HOMEPAGE",
        browser_landing_page=f"{METADATA.name}-PYTEST-LANDING_PAGE",
    ).app


@pytest.fixture(scope="function")
def file_handler_app() -> Application:
    return FileHandler(
        file=RESUMES["full.json"],
    ).app


@pytest.fixture(scope="function")
def showcase_output() -> str:
    with open(DATA_DIR / "showcase-output.txt", encoding="utf8") as f:
        return f.read()
