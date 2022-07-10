import os
from enum import IntEnum
from pathlib import Path
from typing import Final

PROJECT_ROOT = Path(__file__).parent
PACKAGE = __package__

GH_TOKEN: Final = os.environ["GH_TOKEN"]
GH_REQUESTER: Final = os.environ["GH_REQUESTER"]
REPO_URL: Final = os.environ["REPO_URL"]


class SIPrefix(IntEnum):
    KILO = 1e3
    MEGA = 1e6
