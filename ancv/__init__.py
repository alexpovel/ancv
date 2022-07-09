import os
from enum import IntEnum
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
PACKAGE = __package__

GH_TOKEN = os.environ["GH_TOKEN"]
GH_REQUESTER = os.environ["GH_REQUESTER"]


class SIPrefix(IntEnum):
    KILO = 1e3
    MEGA = 1e6
