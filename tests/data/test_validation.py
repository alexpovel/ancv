import pytest

from ancv.data.validation import is_valid_github_username


@pytest.mark.parametrize(
    ["name", "valid"],
    [
        ("j", True),
        ("johndoe", True),
        ("john-doe", True),
        ("johndoe-johndoe", True),
        ("johndoe0-johndoe1", True),
        ("john-john-doe-doe", True),
        ("johndoe1970", True),
        ("1970johndoe", True),
        ("j" * 30, True),
        ("j" * 37, True),
        ("j" * 38, True),
        ("j" * 39, True),
        #
        ("", False),
        ("-johndoe", False),
        ("johndoe-", False),
        ("-johndoe-", False),
        ("johndoe--johndoe", False),
        ("j" * 40, False),
        ("j" * 100, False),
        #
        ("🚧", False),
        ("🚧" * 100, False),
        ("ö", False),
        ("äääääääääääää", False),
        ("}", False),
        ("[", False),
        ("hello; world", False),
        ("exec('evil')", False),
        ("TIMMY; DROP TABLES :-)", False),
    ],
)
def test_is_valid_github_name(name: str, valid: bool) -> None:
    assert is_valid_github_username(name) == valid
