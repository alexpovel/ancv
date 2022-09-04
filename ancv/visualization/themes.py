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


THEMES = {
    "plain": Theme(
        emphasis=[Style(), Style(), Style(), Style()],
        headlines=[Style(), Style(), Style(), Style()],
        bullet="*",
        rulechar="─",
        datefmt="yyyy-MM",
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
        datefmt="MMMM yyyy",
    ),
}
