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
from tests import GH_TOKEN, gh_rate_limited


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
@pytest.mark.asyncio
@gh_rate_limited
async def test_get_resume_validations(
    username: str,
    client_session: aiohttp.ClientSession,
    gh_api: GitHubAPI,
    stopwatch: Stopwatch,
    size_limit: int,
    filename: str,
    expectation: ContextManager,
) -> None:
    api = await gh_api
    with expectation:
        await get_resume(
            user=username,
            session=client_session,
            github=api,
            stopwatch=stopwatch,
            filename=filename,
            size_limit=size_limit,
        )
