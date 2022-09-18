from datetime import date
from typing import Optional

import pytest
from babel.core import Locale
from rich.console import NewLine, RenderableType
from rich.style import Style

from ancv.data.models.resume import Meta, ResumeSchema, TemplateConfig
from ancv.exceptions import ResumeConfigError
from ancv.visualization.templates import (
    Sequential,
    Template,
    ensure_single_trailing_newline,
)
from ancv.visualization.themes import DateFormat, Emphasis, Theme
from ancv.visualization.translations import Translation


@pytest.mark.parametrize(
    ["input_sequence", "expected_sequence"],
    [
        ([], [NewLine()]),
        ([1], [1, NewLine()]),
        ([1, 2], [1, 2, NewLine()]),
        ([1, 2, NewLine()], [1, 2, NewLine()]),
        ([1, 2, NewLine(), NewLine()], [1, 2, NewLine()]),
        ([1, NewLine(), NewLine(), NewLine(), NewLine()], [1, NewLine()]),
        ([NewLine(), NewLine(), NewLine(), NewLine()], [NewLine()]),
    ],
)
def test_ensure_single_trailing_newline(
    input_sequence: list[RenderableType], expected_sequence: list[RenderableType]
) -> None:
    ensure_single_trailing_newline(input_sequence)

    for result, expected in zip(input_sequence, expected_sequence, strict=True):
        if isinstance(result, NewLine):  # Cannot compare for equality
            assert isinstance(expected, NewLine)
        else:
            assert result == expected


@pytest.mark.parametrize(
    [
        "start",
        "end",
        "datefmt",
        "locale",
        "range_sep",
        "present",
        "collapse",
        "expected",
    ],
    [
        (
            None,
            None,
            DateFormat(full="MMMM yyyy", year_only="yyyy"),
            Locale("en"),
            "-",
            "present",
            False,
            "",
        ),
        (
            None,
            date(2900, 3, 1),
            DateFormat(full="MMMM yyyy", year_only="yyyy"),
            Locale("en"),
            "-",
            "present",
            False,
            "- March 2900",
        ),
        (
            date(163, 12, 1),
            None,
            DateFormat(full="MMMM yyyy", year_only="yyyy"),
            Locale("en"),
            "-",
            "present",
            False,
            "December 0163 - present",
        ),
        (
            date(2021, 1, 1),
            None,
            DateFormat(full="MMMM yyyy", year_only="yyyy"),
            Locale("en"),
            "-",
            "today",
            False,
            "January 2021 - today",
        ),
        (
            date(2021, 1, 1),
            date(2021, 2, 1),
            DateFormat(full="MMMM yyyy", year_only="yyyy"),
            Locale("en"),
            "-",
            "present",
            False,
            "January 2021 - February 2021",
        ),
        (
            date(1999, 4, 1),
            date(2018, 9, 1),
            DateFormat(full="yyyy-MM", year_only="yyyy"),
            Locale("en"),
            "-",
            "present",
            False,
            "1999-04 - 2018-09",
        ),
        (
            date(1999, 4, 1),
            date(2018, 9, 1),
            DateFormat(full="yyyy-MM", year_only="yyyy"),
            Locale("en"),
            "***",
            "present",
            False,
            "1999-04 *** 2018-09",
        ),
        (
            date(1999, 3, 1),
            date(2018, 10, 1),
            DateFormat(full="MMMM yyyy", year_only="yyyy"),
            Locale("de"),
            "***",
            "heute",
            False,
            "März 1999 *** Oktober 2018",
        ),
        (
            date(1999, 3, 1),
            date(2018, 10, 1),
            DateFormat(full="MMMM yyyy", year_only="yyyy"),
            Locale("es"),
            "***",
            "heute",
            False,
            "marzo 1999 *** octubre 2018",
        ),
        (
            date(2018, 3, 1),
            date(2018, 4, 1),
            DateFormat(full="MMMM yyyy", year_only="yyyy"),
            Locale("en"),
            "***",
            "present",
            True,
            "March 2018 *** April 2018",
        ),
        (
            date(2018, 4, 1),
            date(2018, 4, 1),
            DateFormat(full="MMMM yyyy", year_only="yyyy"),
            Locale("en"),
            "***",
            "present",
            True,
            "April 2018",
        ),
    ],
)
def test_default_date_range(
    start: Optional[date],
    end: Optional[date],
    datefmt: DateFormat,
    locale: Locale,
    range_sep: str,
    present: str,
    collapse: bool,
    expected: str,
) -> None:
    irrelevant = "."
    template = Sequential(
        ResumeSchema(),
        Theme(
            bullet=irrelevant,
            emphasis=Emphasis(
                maximum=Style(),
                strong=Style(),
                medium=Style(),
                weak=Style(),
            ),
            sep=irrelevant,
            range_sep=range_sep,
            rulechar=irrelevant,
            datefmt=datefmt,
        ),
        Translation(
            grade=irrelevant,
            awarded_by=irrelevant,
            issued_by=irrelevant,
            roles=irrelevant,
            skills=irrelevant,
            work=irrelevant,
            volunteer=irrelevant,
            education=irrelevant,
            awards=irrelevant,
            certificates=irrelevant,
            publications=irrelevant,
            languages=irrelevant,
            references=irrelevant,
            interests=irrelevant,
            projects=irrelevant,
            present=present,
        ),
        locale=locale,
        ascii_only=False,
    )
    assert template.format_date_range(start, end, collapse) == expected


@pytest.mark.parametrize(
    ["model", "expectation"],
    [
        (
            ResumeSchema(meta=Meta(ancv=TemplateConfig(template="DOESNT_EXIST"))),
            pytest.raises(ResumeConfigError, match="^Unknown template: DOESNT_EXIST$"),
        ),
        (
            ResumeSchema(meta=Meta(ancv=TemplateConfig(theme="DOESNT_EXIST"))),
            pytest.raises(ResumeConfigError, match="^Unknown theme: DOESNT_EXIST$"),
        ),
        (
            ResumeSchema(meta=Meta(ancv=TemplateConfig(language="zz"))),
            pytest.raises(ResumeConfigError, match="^Unknown language: zz$"),
        ),
    ],
)
def test_rejects_unknown_configs(model, expectation) -> None:
    with expectation:
        Template.from_model_config(model)
