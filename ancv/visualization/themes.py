from abc import ABC, abstractmethod
from datetime import date
from typing import Optional

from rich.style import Style


class Theme(ABC):
    @property
    @abstractmethod
    def emphasis(self) -> list[Style]:
        pass

    @property
    @abstractmethod
    def headlines(self) -> list[Style]:
        pass

    @property
    @abstractmethod
    def bullet(self) -> str:
        pass

    @property
    @abstractmethod
    def rulechar(self) -> str:
        pass

    @property
    @abstractmethod
    def datefmt(self) -> str:
        pass

    @staticmethod
    def date_range(
        start: Optional[date],
        end: Optional[date],
        fmt: str,
        sep: str = "-",
        ongoing: str = "present",
    ) -> str:
        match (start, end):
            case (None, None):
                return ""
            # https://github.com/python/mypy/issues/12364#issuecomment-1179683164:
            case (None, date() as end):
                return f"{sep} {end.strftime(fmt)}"
            case (date() as start, None):
                return f"{start.strftime(fmt)} {sep} {ongoing}"
            case (date() as start, date() as end):
                return f"{start.strftime(fmt)} {sep} {end.strftime(fmt)}"
            case _:
                raise TypeError(f"Invalid date range: {start} - {end}")


class Plain(Theme):
    @property
    def emphasis(self) -> list[Style]:
        return [Style(), Style(), Style(), Style()]

    @property
    def headlines(self) -> list[Style]:
        return [Style(), Style(), Style(), Style()]

    @property
    def bullet(self) -> str:
        return "*"

    @property
    def rulechar(self) -> str:
        return "─"

    @property
    def datefmt(self) -> str:
        return "%Y-%m-%d"


class Basic(Theme):
    @property
    def emphasis(self) -> list[Style]:
        return [Style(bold=True), Style(italic=True), Style(underline=True), Style()]

    @property
    def headlines(self) -> list[Style]:
        return [Style(bold=True), Style(italic=True), Style(underline=True), Style()]

    @property
    def bullet(self) -> str:
        return "*"

    @property
    def rulechar(self) -> str:
        return "─"

    @property
    def datefmt(self) -> str:
        return "%B %d, %Y"
