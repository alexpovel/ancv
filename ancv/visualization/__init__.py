from typing import Final, Generator

from rich.console import RenderableType

RenderableGenerator = Generator[RenderableType, None, None]

OUTPUT_COLUMN_WIDTH: Final = 120
