"""CLI tests for `validate` with a corrupt resume file.

A resume file containing malformed JSON must be rejected with a clean
error message and exit code 1, not an unhandled `json.JSONDecodeError`
traceback.
"""

import json
from pathlib import Path

from typer.testing import CliRunner

from ancv.__main__ import app
from tests import RESUMES

RUNNER = CliRunner()


def test_validate_malformed_json_is_clean_error(tmp_path: Path) -> None:
    bad = tmp_path / "resume.json"
    bad.write_text("{not valid json", encoding="utf-8")

    result = RUNNER.invoke(app, ["validate", str(bad)])

    assert result.exit_code == 1
    assert not isinstance(result.exception, json.JSONDecodeError)
    assert "Traceback" not in result.output


def test_validate_valid_resume_still_passes() -> None:
    result = RUNNER.invoke(app, ["validate", str(RESUMES["full.resume.json"])])

    assert result.exit_code == 0
    assert "Pass!" in result.output
