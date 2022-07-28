import pytest
from typer.testing import CliRunner

from ancv.__main__ import app
from tests import RESUMES

RUNNER = CliRunner()


def test_help_exists():
    result = RUNNER.invoke(app, ["--help"])
    assert result.exit_code == 0


def test_serve_exists():
    result = RUNNER.invoke(app, ["serve"])
    assert result.exit_code == 0


def test_serve_file_exists():
    result = RUNNER.invoke(app, ["serve", "file", "--help"])
    assert result.exit_code == 0


def test_serve_api_exists():
    result = RUNNER.invoke(app, ["serve", "api", "--help"])
    assert result.exit_code == 0


def test_version_exists():
    result = RUNNER.invoke(app, ["version"])
    assert result.exit_code == 0


@pytest.mark.parametrize("filename", RESUMES)
# All resumes as a single fixture wouldn't be too bad either but doesn't work:
# https://stackoverflow.com/q/56672179/11477374
class TestCli:
    def test_validate(self, filename):
        result = RUNNER.invoke(app, ["validate", str(filename)])
        assert result.exit_code == 0

    def test_render(self, filename):
        result = RUNNER.invoke(app, ["render", str(filename)])
        assert result.exit_code == 0
