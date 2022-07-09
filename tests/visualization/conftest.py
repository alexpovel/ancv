import json
import pytest

from tests import DATA_DIR


@pytest.fixture(params=["full"])
def resume(request):
    with open(DATA_DIR / "resumes" / request.param + ".json") as f:
        return json.load(f)
