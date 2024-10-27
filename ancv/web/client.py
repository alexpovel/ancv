import json
from http import HTTPStatus
from types import SimpleNamespace

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
    github: GitHubAPI,
    stopwatch: Stopwatch,
    filename: str = "resume.json",
    size_limit: int = 1 * SIPrefix.MEGA,
) -> ResumeSchema:
    """Fetch a user's resume from their GitHub gists.

    Searches through all of the user's gists for a file with a given name. Checks for
    various bad states:

    - User...
        - doesn't exist.
        - has no gists.
        - has no gists with the given filename.
    - File...
        - is too large.
        - is not valid JSON.
        - is not valid against the resume schema.

    There are others that are probably not covered (hard to test).

    Sections of the code are timed for performance analysis.

    Args:
        user: The GitHub username to fetch the resume from.
        github: The API object to use for the request.
        stopwatch: The `Stopwatch` to use for timing.
        filename: The name of the file to look for in the user's gists.
        size_limit: The maximum size of the file to look for in the user's gists.

    Returns:
        The parsed resume.
    """

    log = LOGGER.bind(user=user)

    stopwatch("Fetching Gists")
    gists = github.getiter(f"/users/{user}/gists")
    while True:
        try:
            raw_gist = await anext(gists)
        except StopAsyncIteration:
            raise ResumeLookupError(
                f"No '{filename}' file found in any gist of '{user}'."
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

        # https://peps.python.org/pep-0636/#matching-against-constants-and-enums :
        obj = SimpleNamespace()  # Direct kwargs passing isn't mypy-friendly.
        obj.filename = filename

        match gist:  # noqa: E999
            case Gist(files={obj.filename: file}):
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
