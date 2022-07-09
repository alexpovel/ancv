from abc import ABC, abstractmethod
from functools import singledispatchmethod
from typing import Final, Generator, Optional

from ancv.data.models.resume import (
    Award,
    Basics,
    Certificate,
    EducationItem,
    Interest,
    Language,
    Location,
    Profile,
    Project,
    Publication,
    Reference,
    ResumeSchema,
    Skill,
    VolunteerItem,
    WorkItem,
)
from ancv.visualization.themes import Theme
from rich.console import Console, ConsoleOptions, RenderableType

RenderableGenerator = Generator[RenderableType, None, None]


ResumeItem = (
    Award
    | Basics
    | Certificate
    | EducationItem
    | Interest
    | Language
    | Location
    | Profile
    | Project
    | Publication
    | Reference
    | Skill
    | VolunteerItem
    | WorkItem
)

ResumeItemContainer = Optional[
    list[Award]
    | list[Certificate]
    | list[EducationItem]
    | list[Interest]
    | list[Language]
    | list[Project]
    | list[Publication]
    | list[Reference]
    | list[Skill]
    | list[VolunteerItem]
    | list[WorkItem]
]


WIDTH: Final = 120


class Template(ABC):
    def __init__(self, model: ResumeSchema) -> None:
        self.model = model

    @abstractmethod
    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderableGenerator:
        pass

    @property
    @abstractmethod
    def theme(self) -> Theme:
        pass

    @singledispatchmethod
    @staticmethod
    @abstractmethod
    def format(item: ResumeItem, theme: Theme) -> RenderableGenerator:
        raise NotImplementedError(f"Formatting not implemented for type: {type(item)}")
