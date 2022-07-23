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
from ancv.utils.exceptions import ResumeLookupError

LOGGER = get_logger()


async def get_resume(
    user: str, session: aiohttp.ClientSession, github: GitHubAPI
) -> ResumeSchema:
    log = LOGGER.bind(user=user, session=session)

    try:
        # This generates an additional request, counting towards our limit. However,
        # it seems the cleanest way to check for user existence before iterating over
        # the user's gists, since catching exceptions raised in a generator are uglier
        # to deal with.
        await github.getitem(f"/users/{user}")
    except gidgethub.BadRequest as e:
        # Cannot cleanly just catch 404, since e.g. `RateLimitExceeded` inherits from
        # `BadRequest`:
        # https://gidgethub.readthedocs.io/en/latest/__init__.html#gidgethub.RateLimitExceeded
        if e.status_code == HTTPStatus.NOT_FOUND:
            raise ResumeLookupError(f"User {user} not found.")
        raise e

    gists = github.getiter(f"/users/{user}/gists")
    async for raw_gist in gists:
        log.info("Got raw gist of user.")
        gist = Gist(**raw_gist)
        log = log.bind(gist_url=gist.url)
        log.info("Parsed gist of user.")

        file = gist.files.get("resume.json", None)
        if file is not None:
            log.info("Gist matched.")
            break

        log.info("Gist unsuitable, trying next.")
    else:  # nobreak
        raise ResumeLookupError(f"No 'resume.json' file found in any gist of '{user}'.")

    size_limit = SIPrefix.MEGA
    if file.size is None or file.size > size_limit:
        size = "unknown" if file.size is None else str(naturalsize(file.size))
        raise ResumeLookupError(
            "Resume file too large" f" (limit: {naturalsize(size_limit)}, got {size})."
        )
    log.info("Fetching resume contents of user.")
    raw_resume: str = await github.getitem(str(file.raw_url))
    log.info("Got raw resume of user.")

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
