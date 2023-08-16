from datetime import date
from pathlib import Path
from typing import Optional

import pytest
from babel.core import Locale
from babel.dates import parse_pattern
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
from tests import ACTUAL_OUTPUTS_DIR, EXPECTED_OUTPUTS_DIR, RESUMES_DIR


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
        "dec31_as_year",
        "expected",
    ],
    [
        (
            None,
            None,
            DateFormat(
                full=parse_pattern("MMMM yyyy"), year_only=parse_pattern("yyyy")
            ),
            Locale("en"),
            "-",
            "present",
            False,
            False,
            "",
        ),
        (
            None,
            date(2900, 3, 1),
            DateFormat(
                full=parse_pattern("MMMM yyyy"), year_only=parse_pattern("yyyy")
            ),
            Locale("en"),
            "-",
            "present",
            False,
            False,
            "- March 2900",
        ),
        (
            date(163, 12, 1),
            None,
            DateFormat(
                full=parse_pattern("MMMM yyyy"), year_only=parse_pattern("yyyy")
            ),
            Locale("en"),
            "-",
            "present",
            False,
            False,
            "December 0163 - present",
        ),
        (
            date(2021, 1, 1),
            None,
            DateFormat(
                full=parse_pattern("MMMM yyyy"), year_only=parse_pattern("yyyy")
            ),
            Locale("en"),
            "-",
            "today",
            False,
            False,
            "January 2021 - today",
        ),
        (
            date(2021, 1, 1),
            date(2021, 2, 1),
            DateFormat(
                full=parse_pattern("MMMM yyyy"), year_only=parse_pattern("yyyy")
            ),
            Locale("en"),
            "-",
            "present",
            False,
            False,
            "January 2021 - February 2021",
        ),
        (
            date(1999, 4, 1),
            date(2018, 9, 1),
            DateFormat(full=parse_pattern("yyyy-MM"), year_only=parse_pattern("yyyy")),
            Locale("en"),
            "-",
            "present",
            False,
            False,
            "1999-04 - 2018-09",
        ),
        (
            date(1999, 4, 1),
            date(2018, 9, 1),
            DateFormat(full=parse_pattern("yyyy-MM"), year_only=parse_pattern("yyyy")),
            Locale("en"),
            "***",
            "present",
            False,
            False,
            "1999-04 *** 2018-09",
        ),
        (
            date(1999, 3, 1),
            date(2018, 10, 1),
            DateFormat(
                full=parse_pattern("MMMM yyyy"), year_only=parse_pattern("yyyy")
            ),
            Locale("de"),
            "***",
            "heute",
            False,
            False,
            "März 1999 *** Oktober 2018",
        ),
        (
            date(1999, 3, 1),
            date(2018, 10, 1),
            DateFormat(
                full=parse_pattern("MMMM yyyy"), year_only=parse_pattern("yyyy")
            ),
            Locale("es"),
            "***",
            "heute",
            False,
            False,
            "marzo 1999 *** octubre 2018",
        ),
        (
            date(2018, 3, 1),
            date(2018, 4, 1),
            DateFormat(
                full=parse_pattern("MMMM yyyy"), year_only=parse_pattern("yyyy")
            ),
            Locale("en"),
            "***",
            "present",
            True,
            False,
            "March 2018 *** April 2018",
        ),
        (
            date(2018, 4, 1),
            date(2018, 4, 1),
            DateFormat(
                full=parse_pattern("MMMM yyyy"), year_only=parse_pattern("yyyy")
            ),
            Locale("en"),
            "***",
            "present",
            True,
            False,
            "April 2018",
        ),
        (
            None,
            date(2000, 12, 31),
            DateFormat(
                full=parse_pattern("MMMM yyyy"), year_only=parse_pattern("yyyy")
            ),
            Locale("en"),
            "---",
            "present",
            True,
            True,
            "--- 2000",
        ),
        (
            date(2000, 12, 31),
            date(2000, 12, 31),
            DateFormat(
                full=parse_pattern("MMMM yyyy"), year_only=parse_pattern("yyyy")
            ),
            Locale("en"),
            "---",
            "present",
            True,
            True,
            "2000",
        ),
        (
            date(2000, 12, 31),
            None,
            DateFormat(
                full=parse_pattern("MMMM yyyy"), year_only=parse_pattern("yyyy")
            ),
            Locale("en"),
            "---",
            "present",
            True,
            True,
            "2000 --- present",
        ),
        (
            date(2000, 12, 31),
            date(2002, 12, 31),
            DateFormat(
                full=parse_pattern("MMMM yyyy"), year_only=parse_pattern("yyyy")
            ),
            Locale("en"),
            "---",
            "present",
            True,
            True,
            "2000 --- 2002",
        ),
        (
            date(2000, 12, 30),
            date(2002, 12, 30),
            DateFormat(
                full=parse_pattern("MMMM yyyy"), year_only=parse_pattern("yyyy")
            ),
            Locale("en"),
            "---",
            "present",
            True,
            True,
            "December 2000 --- December 2002",
        ),
        (
            date(2000, 12, 31),
            date(2002, 12, 31),
            DateFormat(
                full=parse_pattern("MMMM yyyy"), year_only=parse_pattern("yyyy")
            ),
            Locale("en"),
            "---",
            "present",
            True,
            False,
            "December 2000 --- December 2002",
        ),
        (
            date(1995, 12, 31),
            date(1999, 12, 31),
            DateFormat(
                full=parse_pattern("MMMM yyyy"), year_only=parse_pattern("''yy")
            ),
            Locale("en"),
            "---",
            "present",
            True,
            True,
            "'95 --- '99",
        ),
        (
            date(1995, 12, 31),
            date(1999, 12, 31),
            DateFormat(
                full=parse_pattern("MMMM yyyy"), year_only=parse_pattern("'Anno' yy")
            ),
            Locale("en"),
            "to",
            "present",
            True,
            True,
            "Anno 95 to Anno 99",
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
    dec31_as_year: bool,
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
        dec31_as_year=dec31_as_year,
    )
    assert template._format_date_range(start, end, collapse) == expected


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


@pytest.mark.parametrize(
    ["path"], [(file,) for file in sorted(Path(RESUMES_DIR).glob("*.resume.json"))]
)
def test_expected_outputs(path: Path) -> None:
    """For each resume, compare with expected rendered output in sibling directory."""
    rendered_resume = Template.from_model_config(ResumeSchema.parse_file(path)).render()

    while path.suffix:
        path = path.with_suffix("")

    expected_output = EXPECTED_OUTPUTS_DIR / f"{path.name}.resume.output.txt"

    is_equal = rendered_resume == expected_output.read_text(encoding="utf-8")

    # Provide a mechanism for debugging tests easier: write out to a file. The diff
    # printed by `pytest -vv` is not very helpful, as the ANSI escape codes are rendered
    # and cannot be inspected 'raw'. Open the below file in a text editor to see raw
    # bytes and compare.
    with open(
        ACTUAL_OUTPUTS_DIR
        / f"{'OK' if is_equal else 'FAIL'}-{path.name}.resume.output.txt",
        "w",
        encoding="utf8",
    ) as f:
        f.write(rendered_resume)

    assert is_equal
