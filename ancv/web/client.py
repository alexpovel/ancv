import json
from http import HTTPStatus

import aiohttp
import gidgethub
from gidgethub.aiohttp import GitHubAPI
from humanize import naturalsize
from pydantic import ValidationError
from structlog import get_logger

from ancv import SIPrefix
from ancv.data.models.github import Gist
from ancv.data.models.resume import ResumeSchema
from ancv.exceptions import ResumeLookupError
from ancv.timing import Stopwatch

LOGGER = get_logger()


async def get_resume(
    user: str,
    session: aiohttp.ClientSession,
    github: GitHubAPI,
    stopwatch: Stopwatch,
    size_limit: int = 1 * SIPrefix.MEGA,
) -> ResumeSchema:
    log = LOGGER.bind(user=user, session=session)

    stopwatch("Fetching Gists")
    gists = github.getiter(f"/users/{user}/gists")
    while True:
        try:
            raw_gist = await anext(gists)
        except StopAsyncIteration:
            raise ResumeLookupError(
                f"No 'resume.json' file found in any gist of '{user}'."
            )
        except gidgethub.BadRequest as e:
            # `except `RateLimitExceeded` didn't work, it seems it's not correctly
            # raised inside `gidgethub`.
            if e.status_code == HTTPStatus.FORBIDDEN:
                raise ResumeLookupError(
                    "Server exhausted its GitHub API rate limit, terribly sorry!"
                    + " Please try again later."
                )
            if e.status_code == HTTPStatus.NOT_FOUND:
                raise ResumeLookupError(f"User {user} not found.")
            raise e

        log.info("Got raw gist of user.")
        gist = Gist(**raw_gist)
        log = log.bind(gist_url=gist.url)
        log.info("Parsed gist of user.")

        match gist:
            case Gist(files={"resume.json": file}):
                log.info("Gist matched.")
                break
            case _:
                log.info("Gist unsuitable, trying next.")

    if file.size is None or file.size > size_limit:
        size = "unknown" if file.size is None else str(naturalsize(file.size))
        raise ResumeLookupError(
            "Resume file too large" f" (limit: {naturalsize(size_limit)}, got {size})."
        )
    log.info("Fetching resume contents of user.")
    raw_resume: str = await github.getitem(str(file.raw_url))
    log.info("Got raw resume of user.")

    stopwatch("Validation")
    try:
        resume = ResumeSchema(**json.loads(raw_resume))
    except json.decoder.JSONDecodeError:
        raise ResumeLookupError("Got malformed JSON.")
    except ValidationError:
        raise ResumeLookupError(
            "Got legal JSON but wrong schema (cf. https://jsonresume.org/schema/)"
        )

    log.info("Successfully parsed raw resume of user, returning.")
    return resume
