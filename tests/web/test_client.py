import asyncio
from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import aiohttp
import pytest
from gidgethub.aiohttp import GitHubAPI

from ancv import SIPrefix
from ancv.exceptions import ResumeLookupError
from ancv.reflection import METADATA
from ancv.timing import Stopwatch
from ancv.web.client import get_resume
from tests import GH_TOKEN, gh_rate_limited


@pytest.fixture(scope="function")
def stopwatch():
    return Stopwatch()


@pytest.fixture(scope="function")
async def client_session() -> aiohttp.ClientSession:
    assert (
        asyncio.get_running_loop()
    ), "`aiohttp.ClientSession` constructor will need loop running."

    # The constructor accesses the async event loop, and if none is running errors. So
    # this pytest fixture function needs to be marked `async` for `pytest-asyncio` with
    # the `asyncio_mode = "auto"` option set to pick it up automatically and *provide* a
    # loop.
    return aiohttp.ClientSession()


@pytest.fixture(scope="function")
def gh_api(client_session: aiohttp.ClientSession):
    return GitHubAPI(
        client_session,
        requester=f"{METADATA.name}-PYTEST-REQUESTER",
        oauth_token=GH_TOKEN,
    )


@pytest.mark.parametrize(
    ["username", "size_limit", "filename", "expectation"],
    [
        (
            "alexpovel",
            1 * SIPrefix.MEGA,
            "resume.json",
            does_not_raise(),
        ),
        (
            "alexpovel",
            0,
            "resume.json",
            pytest.raises(
                ResumeLookupError,
                match=r"^Resume file too large \(limit: 0 Bytes, got \d+\.\d+ kB\)\.$",
            ),
        ),
        (
            "alexpovel",
            1 * SIPrefix.MEGA,
            "resume.invalid-json",
            pytest.raises(ResumeLookupError, match=r"^Got malformed JSON\.$"),
        ),
        (
            "alexpovel",
            1 * SIPrefix.MEGA,
            "resume.invalid-schema.json",
            pytest.raises(
                ResumeLookupError,
                match=r"^Got legal JSON but wrong schema \(cf\. https://jsonresume\.org/schema/\)$",
            ),
        ),
    ],
)
@gh_rate_limited
async def test_get_resume_validations(
    username: str,
    size_limit: int,
    filename: str,
    expectation: AbstractContextManager[pytest.ExceptionInfo[BaseException]],  # Unsure
    # Fixtures:
    gh_api: GitHubAPI,
    stopwatch: Stopwatch,
) -> None:
    assert asyncio.get_running_loop()

    with expectation:
        await get_resume(
            user=username,
            github=gh_api,
            stopwatch=stopwatch,
            filename=filename,
            size_limit=size_limit,
        )
