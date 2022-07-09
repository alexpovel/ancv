import re
from functools import cache
from string import ascii_letters, digits


@cache
def is_valid_github_username(name: str) -> bool:
    """Checks whether a name is a valid GitHub username.

    From trying to register, we can gather:

        - "Username is too long (maximum is 39 characters)."
        - "Username may only contain alphanumeric characters or single hyphens, and
            cannot begin or end with a hyphen."

    Decided to do this vanilla, since the corresponding regex is (un)surprisingly
    unreadable.
    """
    hyphen = "-"

    if not name or len(name) > 39:
        return False

    alphanumeric = ascii_letters + digits
    legal = set(alphanumeric + hyphen)

    illegal_characters = set(name) - legal
    if illegal_characters:
        return False

    if name[0] == hyphen or name[-1] == hyphen:
        return False

    if re.search("[-]{2,}", name):
        return False

    return True
