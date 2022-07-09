from datetime import date, datetime, time
from typing import Optional

import pytest


def pytest_make_parametrize_id(
    config: pytest.Config, val: object, argname: str
) -> Optional[str]:
    if isinstance(val, (date, datetime, time)):
        return repr(val)
    return None
