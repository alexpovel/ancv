import pytest

from ancv.web import is_terminal_client


@pytest.mark.parametrize(
    ["user_agent", "expected"],
    [
        ("curl", True),
        ("curl/7.83.1", True),
        ("wget", True),
        ("Wget/1.21", True),
        ("Wget/1.21 (cygwin)", True),
        ("powershell", True),
        ("powershell/5.1.1", True),
        (
            "Mozilla/5.0 (Windows NT; Windows NT 10.0; en-US) WindowsPowerShell/5.1.19041.1682",
            True,
        ),
        ("PowerShell/7.2.5", True),
        (
            "Mozilla/5.0 (Windows NT 10.0; Microsoft Windows 10.0.19044; en-US) PowerShell/7.2.5",
            True,
        ),
        (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            False,
        ),
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            False,
        ),
        (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            False,
        ),
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36 Edge/18.18362",
            False,
        ),
    ],
)
def test_is_terminal_client(user_agent: str, expected: bool) -> None:
    assert is_terminal_client(user_agent) == expected
