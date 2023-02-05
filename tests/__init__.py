import os
from pathlib import Path

import pytest
import requests

TESTS_DIR = Path(__file__).parent
DATA_DIR = TESTS_DIR / "test_data"
RESUMES_DIR = DATA_DIR / "resumes"
EXPECTED_OUTPUTS_DIR = DATA_DIR / "expected-outputs"
RESUMES = {p.name: p for p in RESUMES_DIR.iterdir()}

GH_TOKEN = os.environ.get("GH_TOKEN", None)

# Probably a terrible idea to do IO using the GH API in unit tests, but it does test the
# full thing instead of just some mock.
headers = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "ancv-pytest",
}
if GH_TOKEN is not None:
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
    except KeyError:
        raise

gh_rate_limited = pytest.mark.xfail(
    condition=remaining == 0,
    reason="GitHub API rate limit reached. If you haven't already, set the 'GH_TOKEN' env var to a PAT.",
)
