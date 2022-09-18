import sys
from enum import IntEnum
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
PACKAGE = __package__

# See also https://github.com/python/typeshed/issues/3049
sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]


class SIPrefix(IntEnum):
    KILO = 1e3
    MEGA = 1e6
