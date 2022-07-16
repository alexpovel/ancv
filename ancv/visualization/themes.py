from datetime import date
from typing import Optional

from pydantic import BaseModel
from rich.style import Style


class Theme(BaseModel):
    emphasis: list[Style]
    headlines: list[Style]
    bullet: str
    rulechar: str
    datefmt: str

    class Config:
        arbitrary_types_allowed = True  # No validator for `Style` available

    @staticmethod
    def date_range(
        start: Optional[date],
        end: Optional[date],
        fmt: str,
        sep: str = "-",
        ongoing: str = "present",
    ) -> str:
        if start is None:
            if end is None:
                return ""
            return f"{sep} {end.strftime(fmt)}"

        if end is None:
            return f"{start.strftime(fmt)} {sep} {ongoing}"

        return f"{start.strftime(fmt)} {sep} {end.strftime(fmt)}"


THEMES = {
    "plain": Theme(
        emphasis=[Style(), Style(), Style(), Style()],
        headlines=[Style(), Style(), Style(), Style()],
        bullet="*",
        rulechar="─",
        datefmt="%Y-%m-%d",
    ),
    "basic": Theme(
        emphasis=[
            Style(bold=True),
            Style(italic=True),
            Style(underline=True),
            Style(),
        ],
        headlines=[
            Style(bold=True),
            Style(italic=True),
            Style(underline=True),
            Style(),
        ],
        bullet="*",
        rulechar="─",
        datefmt="%B %d, %Y",
    ),
}
