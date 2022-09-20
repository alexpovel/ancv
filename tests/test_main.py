from pathlib import Path

import pytest
from typer.testing import CliRunner

from ancv import PROJECT_ROOT
from ancv.__main__ import app
from tests import RESUMES

RUNNER = CliRunner()


def test_help_exists() -> None:
    result = RUNNER.invoke(app, ["--help"])
    assert result.exit_code == 0


def test_serve_exists() -> None:
    result = RUNNER.invoke(app, ["serve"])
    assert result.exit_code == 0


def test_serve_file_exists() -> None:
    result = RUNNER.invoke(app, ["serve", "file", "--help"])
    assert result.exit_code == 0


def test_serve_api_exists() -> None:
    result = RUNNER.invoke(app, ["serve", "api", "--help"])
    assert result.exit_code == 0


def test_version_exists() -> None:
    result = RUNNER.invoke(app, ["version"])
    assert result.exit_code == 0


def test_list_exists() -> None:
    result = RUNNER.invoke(app, ["list"])
    assert result.exit_code == 0


def test_generate_schema_exists() -> None:
    result = RUNNER.invoke(app, ["generate-schema"])
    assert result.exit_code == 0


def test_generate_schema_is_current() -> None:
    result = RUNNER.invoke(app, ["generate-schema"])
    assert result.exit_code == 0
    assert result.stdout == Path(PROJECT_ROOT, "..", "schema.json").read_text(
        encoding="utf-8"
    )


@pytest.mark.parametrize("filename", RESUMES.values())
# All resumes as a single fixture wouldn't be too bad either but doesn't work:
# https://stackoverflow.com/q/56672179/11477374
class TestCli:
    def test_validate(self, filename: Path) -> None:
        result = RUNNER.invoke(app, ["validate", str(filename)])
        assert result.exit_code == 0

    def test_render(self, filename: Path) -> None:
        result = RUNNER.invoke(app, ["render", str(filename)])
        assert result.exit_code == 0
