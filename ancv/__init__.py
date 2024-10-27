from enum import IntEnum
from pathlib import Path

from ancv.typehelp import unwrap

PROJECT_ROOT = Path(__file__).parent
PACKAGE = unwrap(__package__)


class SIPrefix(IntEnum):
    KILO = int(1e3)
    MEGA = int(1e6)
