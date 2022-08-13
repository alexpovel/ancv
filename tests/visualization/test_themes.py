from datetime import date
from typing import Optional

import pytest

from ancv.visualization.themes import Theme


@pytest.mark.parametrize(
    ["start", "end", "fmt", "sep", "ongoing", "expected"],
    [
        (
            None,
            None,
            "",
            "",
            "",
            "",
        ),
        (
            None,
            None,
            "%Y-%m-%d",
            "",
            "",
            "",
        ),
        (
            None,
            None,
            "%Y-%m-%d",
            "-",
            "",
            "",
        ),
        (
            None,
            None,
            "%Y-%m-%d",
            "-",
            "present",
            "",
        ),
        (
            date(2020, 1, 1),
            None,
            "%Y-%m-%d",
            "",
            "",
            "2020-01-01  ",
        ),
        (
            date(2020, 1, 10),
            None,
            "%Y-%m-%d",
            "",
            "",
            "2020-01-10  ",
        ),
        (
            date(2020, 1, 1),
            None,
            "%Y-%m-%d",
            "-",
            "",
            "2020-01-01 - ",
        ),
        (
            date(2020, 1, 1),
            None,
            "%Y-%m-%d",
            "-",
            "present",
            "2020-01-01 - present",
        ),
        (
            date(2020, 1, 1),
            None,
            "%Y-%m-%d",
            "...",
            "present",
            "2020-01-01 ... present",
        ),
        (
            date(2020, 1, 1),
            date(2020, 1, 2),
            "%Y-%m-%d",
            "",
            "",
            "2020-01-01  2020-01-02",
        ),
        (
            date(2020, 1, 1),
            date(2020, 1, 2),
            "%Y-%m-%d",
            "-",
            "",
            "2020-01-01 - 2020-01-02",
        ),
        (
            None,
            date(2020, 1, 2),
            "%Y-%m-%d",
            "",
            "",
            " 2020-01-02",
        ),
        (
            None,
            date(2020, 1, 2),
            "%Y-%m-%d",
            "-",
            "",
            "- 2020-01-02",
        ),
        (
            None,
            date(2020, 1, 2),
            "%Y-%m-%d",
            "-",
            "present",
            "- 2020-01-02",
        ),
    ],
)
def test_default_date_range(
    start: Optional[date],
    end: Optional[date],
    fmt: str,
    sep: str,
    ongoing: str,
    expected: str,
) -> None:
    assert Theme.date_range(start, end, fmt, sep, ongoing) == expected
