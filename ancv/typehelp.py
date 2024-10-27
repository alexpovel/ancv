import typing as t

T = t.TypeVar("T")


def unwrap(value: None | T) -> T:
    """Like Rust."""

    if value is None:
        raise ValueError("Provided value is `None`")

    return value
