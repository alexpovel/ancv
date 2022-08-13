from contextlib import nullcontext as does_not_raise
from datetime import timedelta

import pytest

from ancv.web.server import server_timing_header


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
def test_server_timing_header(timings, expected, expectation):
    with expectation:
        assert server_timing_header(timings) == expected
