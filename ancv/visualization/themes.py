from babel.dates import DateTimePattern, parse_pattern
from pydantic import ConfigDict, BaseModel
from rich.style import Style


class Emphasis(BaseModel):
    """Emphasis styles for different levels of importance.

    Using `rich.Style`, each can be styled arbitrarily.
    """

    maximum: Style
    strong: Style
    medium: Style
    weak: Style
    model_config = ConfigDict(arbitrary_types_allowed=True)


class DateFormat(BaseModel):
    """Date formats for different levels of detail.

    The `full` format is as detailed as possible, while `year_only` should only contain
    the year. Formats may otherwise be in whatever format you desire (ISO8601,
    localized, months spelled out etc.). For more context, see:
    https://babel.pocoo.org/en/latest/dates.html

    Using `babel.dates.DateTimePattern` and forcing it here over `str` allows for
    considerably better type safety (`str` is the worst offender in terms of typing) and
    fast failure: at application startup, when a theme is loaded but `parse_pattern` (or
    similar) fails, the program won't launch altogether, instead of failing at runtime.
    """

    full: DateTimePattern
    year_only: DateTimePattern
    model_config = ConfigDict(arbitrary_types_allowed=True)


class Theme(BaseModel):
    """A theme, containing styles and other formatting options."""

    emphasis: Emphasis  # styles for different levels of importance
    bullet: str  # bullet character to use in (unordered) lists
    rulechar: str  # character for *horizontal* rules
    sep: str  # separator character for joined-together strings (e.g. "•" for "foo•bar")
    range_sep: str  # separator character for ranges (e.g. "..." for "2010...2020")
    datefmt: DateFormat  # date formats in different levels of detail


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
        datefmt=DateFormat(
            full=parse_pattern("yyyy-MM"), year_only=parse_pattern("yyyy")
        ),
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
        datefmt=DateFormat(
            full=parse_pattern("MMMM yyyy"), year_only=parse_pattern("yyyy")
        ),
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
        datefmt=DateFormat(
            full=parse_pattern("MMMM yyyy"), year_only=parse_pattern("yyyy")
        ),
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
        datefmt=DateFormat(
            full=parse_pattern("MMMM yyyy"), year_only=parse_pattern("yyyy")
        ),
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
        datefmt=DateFormat(
            full=parse_pattern("MMMM yyyy"), year_only=parse_pattern("yyyy")
        ),
    ),
}
