from typing import Final, Generator

from rich.console import RenderableType

RenderableGenerator = Generator[RenderableType, None, None]

WIDTH: Final = 120
