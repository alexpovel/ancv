import os
from pathlib import Path

import pytest
import requests

TESTS_DIR = Path(__file__).parent
DATA_DIR = TESTS_DIR / "test_data"
RESUMES_DIR = DATA_DIR / "resumes"

EXPECTED_OUTPUTS_DIR = DATA_DIR / "expected-outputs"
ACTUAL_OUTPUTS_DIR = EXPECTED_OUTPUTS_DIR.parent / "actual-outputs"
Path.mkdir(ACTUAL_OUTPUTS_DIR, exist_ok=True)

RESUMES = {p.name: p for p in RESUMES_DIR.iterdir()}

# Map empty string to `None` as well: for pull requests from forked repos, the env var
# is/might be defined but *empty*; if we use it, we get Bad Credentials errors:
# https://web.archive.org/web/20241118204412/https://github.com/alexpovel/ancv/actions/runs/11881484194/job/33160883626
# 🤷
GH_TOKEN = os.environ.get("GH_TOKEN", None) or None

# Probably a terrible idea to do IO using the GH API in unit tests, but it does test the
# full thing instead of just some mock.
headers = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "ancv-pytest",
}
if GH_TOKEN is not None:
    # Just guessing at this point (GitHub Actions CI from PRs from forks is confusing):
    assert GH_TOKEN != "", "GitHub token is empty"

    headers["Authorization"] = f"Bearer {GH_TOKEN}"

resp = requests.get(
    "https://api.github.com/rate_limit",
    headers=headers,
)

try:
    remaining = resp.json()["resources"]["core"]["remaining"]
except KeyError as e:
    try:
        if resp.json()["message"] == "Bad credentials":
            raise KeyError("Bad credentials for GH_TOKEN") from e
        raise
    except KeyError:
        raise

gh_rate_limited = pytest.mark.xfail(
    condition=remaining == 0,
    reason="GitHub API rate limit reached. If you haven't already, set the 'GH_TOKEN' env var to a PAT.",
)
