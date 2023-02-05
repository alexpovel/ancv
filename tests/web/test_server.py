from contextlib import nullcontext as does_not_raise
from datetime import timedelta
from http import HTTPStatus
from typing import Any, ContextManager, Optional

import pytest
from aiohttp.client import ClientResponse
from aiohttp.web import Application

from ancv.web.server import (
    _SHOWCASE_RESUME,
    _SHOWCASE_USERNAME,
    is_terminal_client,
    server_timing_header,
)
from tests import gh_rate_limited


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


@pytest.mark.filterwarnings("ignore:Request.message is deprecated")  # No idea...
@pytest.mark.filterwarnings("ignore:Exception ignored in")  # No idea...
@pytest.mark.asyncio
class TestApiHandler:
    @pytest.mark.parametrize(
        ["user_agent", "expected_http_code"],
        [
            ("curl", HTTPStatus.OK),
            ("powershell", HTTPStatus.OK),
            ("wget", HTTPStatus.OK),
            ("Some Browser/1.0", HTTPStatus.FOUND),
            (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
                HTTPStatus.FOUND,
            ),
        ],
    )
    async def test_root_endpoint(
        self,
        user_agent: str,
        expected_http_code: HTTPStatus,
        aiohttp_client: Any,
        api_client_app: Application,
        event_loop: Any,
    ) -> None:
        client = await aiohttp_client(api_client_app)

        resp: ClientResponse = await client.get(
            "/",
            headers={"User-Agent": user_agent},
            allow_redirects=False,  # So we can test the redirect
        )
        assert resp.status == expected_http_code

    @pytest.mark.parametrize(
        ["username", "expected_http_code", "expected_error_message"],
        [
            (
                "alexpovel",
                HTTPStatus.OK,
                None,
            ),
            (
                "thomasdavis",
                HTTPStatus.OK,
                None,
            ),
            (
                "python",  # An organization without any gists...
                HTTPStatus.NOT_FOUND,
                "No 'resume.json' file found in any gist of 'python'.",
            ),
            (  # Let's hope this never turns into a real username...
                "gj5489gujv4398x73x23x892",
                HTTPStatus.NOT_FOUND,
                "User gj5489gujv4398x73x23x892 not found.",
            ),
            (
                "readme",  # GitHub blog of some sort
                HTTPStatus.NOT_FOUND,
                "User readme not found.",
            ),
            (
                "this-user-should-fail-validation-because-its-username-is-way-too-long",
                HTTPStatus.BAD_REQUEST,
                "400: Invalid username: this-user-should-fail-validation-because-its-username-is-way-too-long",
            ),
            (
                "-invalid",
                HTTPStatus.BAD_REQUEST,
                "400: Invalid username: -invalid",
            ),
        ],
    )
    @gh_rate_limited
    async def test_username_endpoint(
        self,
        username: str,
        expected_http_code: HTTPStatus,
        expected_error_message: Optional[str],
        aiohttp_client: Any,
        api_client_app: Application,
        event_loop: Any,
    ) -> None:
        client = await aiohttp_client(api_client_app)

        resp = await client.get(f"/{username}")
        assert resp.status == expected_http_code

        if expected_error_message is not None:
            assert await resp.text() == expected_error_message

    async def test_showcase_endpoint(
        self,
        aiohttp_client: Any,
        api_client_app: Application,
        event_loop: Any,
    ) -> None:
        client = await aiohttp_client(api_client_app)

        resp: ClientResponse = await client.get(f"/{_SHOWCASE_USERNAME}")
        assert resp.status == HTTPStatus.OK
        assert await resp.text() == _SHOWCASE_RESUME

    @pytest.mark.parametrize(
        ["username", "expected_contained_text"],
        [
            ("alexpovel", "Experience"),
        ],
    )
    @gh_rate_limited
    async def test_return_content(
        self,
        username: str,
        expected_contained_text: str,
        aiohttp_client: Any,
        api_client_app: Application,
        event_loop: Any,
    ) -> None:
        client = await aiohttp_client(api_client_app)

        resp = await client.get(f"/{username}")

        text = await resp.text()
        assert expected_contained_text in text


@pytest.mark.filterwarnings("ignore:Request.message is deprecated")  # No idea...
@pytest.mark.filterwarnings("ignore:Exception ignored in")  # No idea...
@pytest.mark.asyncio
class TestFileHandler:
    @pytest.mark.parametrize(
        ["expected_http_code", "expected_str_content"],
        [
            (HTTPStatus.OK, "John Doe"),
            (HTTPStatus.OK, "Experience"),
            (HTTPStatus.OK, "Skills"),
        ],
    )
    async def test_root_endpoint(
        self,
        expected_http_code: HTTPStatus,
        expected_str_content: str,
        aiohttp_client: Any,
        file_handler_app: Application,
        event_loop: Any,
    ) -> None:
        client = await aiohttp_client(file_handler_app)

        resp: ClientResponse = await client.get("/")
        assert resp.status == expected_http_code
        assert expected_str_content in await resp.text()


@pytest.mark.parametrize(
    ["timings", "expected", "expectation"],
    [
        (None, None, pytest.raises(AttributeError)),
        (
            {},
            "",
            does_not_raise(),
        ),
        (
            {
                "Spaces Work As Well": timedelta(seconds=0.1),
            },
            "Spaces-Work-As-Well;dur=100",
            does_not_raise(),
        ),
        (
            {
                "A": timedelta(seconds=0),
            },
            "A;dur=0",
            does_not_raise(),
        ),
        (
            {
                "A": timedelta(seconds=0.1),
            },
            "A;dur=100",
            does_not_raise(),
        ),
        (
            {
                "A": timedelta(seconds=1),
                "B": timedelta(seconds=2),
            },
            "A;dur=1000, B;dur=2000",
            does_not_raise(),
        ),
        (
            {
                "A": timedelta(seconds=1),
                "B": timedelta(seconds=2),
                "C": timedelta(seconds=3),
                "D": timedelta(seconds=4),
                "E": timedelta(seconds=5),
                "F": timedelta(seconds=6),
                "G": timedelta(seconds=7),
                "H": timedelta(seconds=8),
                "I": timedelta(seconds=9),
                "J": timedelta(seconds=10),
                "K": timedelta(seconds=11),
                "L": timedelta(seconds=12),
                "M": timedelta(seconds=13),
                "N": timedelta(seconds=14),
                "O": timedelta(seconds=15),
                "P": timedelta(seconds=16),
                "Q": timedelta(seconds=17),
                "R": timedelta(seconds=18),
                "S": timedelta(seconds=19),
                "T": timedelta(seconds=20),
                "U": timedelta(seconds=21),
                "V": timedelta(seconds=22),
                "W": timedelta(seconds=23),
                "X": timedelta(seconds=24),
                "Y": timedelta(seconds=25),
                "Z": timedelta(seconds=26),
            },
            "A;dur=1000, B;dur=2000, C;dur=3000, D;dur=4000, E;dur=5000, F;dur=6000, G;dur=7000, H;dur=8000, I;dur=9000, J;dur=10000, K;dur=11000, L;dur=12000, M;dur=13000, N;dur=14000, O;dur=15000, P;dur=16000, Q;dur=17000, R;dur=18000, S;dur=19000, T;dur=20000, U;dur=21000, V;dur=22000, W;dur=23000, X;dur=24000, Y;dur=25000, Z;dur=26000",
            does_not_raise(),
        ),
    ],
)
def test_server_timing_header(
    timings: dict[str, timedelta],
    expected: str,
    expectation: ContextManager,
) -> None:
    with expectation:
        assert server_timing_header(timings) == expected


def test_exact_showcase_output(showcase_output: str) -> None:
    assert _SHOWCASE_RESUME == showcase_output
