from pydantic import BaseModel
from rich.style import Style


class Emphasis(BaseModel):
    maximum: Style
    strong: Style
    medium: Style
    weak: Style

    class Config:
        arbitrary_types_allowed = True  # No validator for `Style` available


class DateFormat(BaseModel):
    full: str
    year_only: str


class Theme(BaseModel):
    emphasis: Emphasis
    bullet: str
    rulechar: str
    sep: str
    range_sep: str
    datefmt: DateFormat


# See here for available colors:
# https://rich.readthedocs.io/en/stable/appendix/colors.html#appendix-colors

THEMES = {
    "plain": Theme(
        emphasis=Emphasis(
            maximum=Style(),
            strong=Style(),
            medium=Style(),
            weak=Style(),
        ),
        bullet="•",
        sep="•",
        range_sep="–",
        rulechar="─",
        datefmt=DateFormat(full="yyyy-MM", year_only="yyyy-MM"),
    ),
    "grayscale": Theme(
        emphasis=Emphasis(
            maximum=Style(color="grey93"),
            strong=Style(color="grey74"),
            medium=Style(color="grey58"),
            weak=Style(color="grey42"),
        ),
        bullet="*",
        sep="*",
        range_sep="–",
        rulechar="─",
        datefmt=DateFormat(full="MMMM yyyy", year_only="MMMM yyyy"),
    ),
    "basic": Theme(
        emphasis=Emphasis(
            maximum=Style(bold=True),
            strong=Style(italic=True),
            medium=Style(),
            weak=Style(dim=True),
        ),
        bullet="•",
        sep="•",
        range_sep="–",
        rulechar="─",
        datefmt=DateFormat(full="MMMM yyyy", year_only="MMMM yyyy"),
    ),
    "lollipop": Theme(
        emphasis=Emphasis(
            maximum=Style(bold=True, color="sandy_brown"),
            strong=Style(italic=True, color="pale_green3"),
            medium=Style(color="sky_blue1"),
            weak=Style(color="thistle3"),
        ),
        bullet="➔",
        sep="•",
        range_sep="➔",
        rulechar="─",
        datefmt=DateFormat(full="MMMM yyyy", year_only="MMMM yyyy"),
    ),
    "hendrix": Theme(
        emphasis=Emphasis(
            maximum=Style(blink=True, bold=True, color="sandy_brown"),
            strong=Style(blink=True, italic=True, color="pale_green3"),
            medium=Style(blink=True, color="sky_blue1"),
            weak=Style(blink=True, color="thistle3"),
        ),
        bullet="➔",
        sep="•",
        range_sep="➔",
        rulechar="─",
        datefmt=DateFormat(full="MMMM yyyy", year_only="MMMM yyyy"),
    ),
}
