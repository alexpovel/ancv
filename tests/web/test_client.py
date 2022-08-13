from contextlib import nullcontext as does_not_raise
from typing import ContextManager

import aiohttp
import pytest
from gidgethub.aiohttp import GitHubAPI

from ancv import SIPrefix
from ancv.exceptions import ResumeLookupError
from ancv.reflection import METADATA
from ancv.timing import Stopwatch
from ancv.web.client import get_resume
from tests import GH_TOKEN


@pytest.fixture(scope="function")
def stopwatch():
    return Stopwatch()


@pytest.fixture(scope="function")
async def client_session():
    return aiohttp.ClientSession()


@pytest.fixture(scope="function")
async def gh_api(client_session):
    return GitHubAPI(
        await client_session,
        requester=f"{METADATA.name}-PYTEST-REQUESTER",
        oauth_token=GH_TOKEN,
    )


@pytest.mark.parametrize(
    ["username", "size_limit", "expectation"],
    [
        (
            "alexpovel",
            1 * SIPrefix.MEGA,
            does_not_raise(),
        ),
        (
            "alexpovel",
            0,
            pytest.raises(ResumeLookupError),
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_resume_size_limit(
    username: str,
    client_session: aiohttp.ClientSession,
    gh_api: GitHubAPI,
    stopwatch: Stopwatch,
    size_limit: int,
    expectation: ContextManager,
) -> None:
    api = await gh_api
    with expectation:
        await get_resume(username, client_session, api, stopwatch, size_limit)
