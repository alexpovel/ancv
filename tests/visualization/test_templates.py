import pytest
from rich.console import NewLine, RenderableType

from ancv.visualization.templates import ensure_single_trailing_newline


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
