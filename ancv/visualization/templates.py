import json
from abc import ABC, abstractmethod
from contextlib import redirect_stdout
from datetime import date
from functools import lru_cache, singledispatchmethod
from pathlib import Path
from tempfile import SpooledTemporaryFile
from typing import MutableSequence, NamedTuple, Optional

from babel.core import Locale
from babel.dates import format_date
from rich.align import Align
from rich.console import Console, ConsoleOptions, Group, NewLine, RenderableType, group
from rich.padding import Padding
from rich.rule import Rule
from rich.style import Style
from rich.table import Column, Table
from rich.text import Text

from ancv import SIPrefix
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
    ResumeItem,
    ResumeItemContainer,
    ResumeSchema,
    Skill,
    TemplateConfig,
    VolunteerItem,
    WorkItem,
)
from ancv.exceptions import ResumeConfigError
from ancv.visualization import WIDTH, RenderableGenerator
from ancv.visualization.themes import THEMES, Theme
from ancv.visualization.translations import TRANSLATIONS, Translation


class Template(ABC):
    # This is data:
    def __init__(
        self,
        model: ResumeSchema,
        theme: Theme,
        translation: Translation,
        locale: Locale,
        ascii_only: bool,
    ) -> None:
        self.model = model
        self.theme = theme
        self.translation = translation
        self.locale = locale
        self.ascii_only = ascii_only

    # This is behavior:
    @abstractmethod
    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderableGenerator:
        pass

    def render(self) -> str:
        encoding = "ascii" if self.ascii_only else "utf-8"
        f = SpooledTemporaryFile(max_size=SIPrefix.MEGA, mode="w", encoding=encoding)

        with redirect_stdout(f):
            # `Console` ultimately checks `f.encoding` for its encoding. If we don't
            # specify `file` aka `f`, it will default to `sys.stdout`. Redirecting all
            # of that to a fake, in-memory file with an artificial/controlled encoding
            # will fool `rich` into using its ASCII-only rendering.
            console = Console(
                width=WIDTH,
                color_system="256",
                force_terminal=False,
                force_jupyter=False,
                force_interactive=False,
                no_color=False,
                tab_size=4,
                legacy_windows=False,
            )

            with console.capture() as capture:
                console.print(self)
        return capture.get().strip()

    @lru_cache(maxsize=1_000)
    def format_date(self, date: date) -> str:
        return format_date(date, format=self.theme.datefmt, locale=self.locale)

    @lru_cache(maxsize=1_000)
    def date_range(
        self,
        start: Optional[date],
        end: Optional[date],
        sep: str = "-",
        collapse: bool = True,
    ) -> str:
        if start is None:
            if end is None:
                return ""
            return f"{sep} {self.format_date(end)}"

        if end is None:
            return f"{self.format_date(start)} {sep} {self.translation.present}"

        collapsible = start.month == end.month and start.year == end.year
        if collapsible and collapse:
            return self.format_date(end)

        return f"{self.format_date(start)} {sep} {self.format_date(end)}"

    @classmethod
    # A property would be nicer but it's not supported from Python 3.11 on:
    # https://docs.python.org/3.11/library/functions.html#classmethod
    def subclasses(cls) -> dict[str, type["Template"]]:
        return {cls.__name__: cls for cls in cls.__subclasses__()}

    @classmethod
    def from_model_config(cls, model: ResumeSchema) -> "Template":
        if (config := model.meta.config) is None:
            config = TemplateConfig()

        if (theme_name := config.theme) is None:
            theme_name = "basic"
        try:
            theme = THEMES[theme_name]
        except KeyError as e:
            raise ResumeConfigError(f"Unknown theme: {theme_name}") from e

        if (language := config.language) is None:
            language = "en"
        try:
            translation = TRANSLATIONS[language]
        except KeyError as e:
            raise ResumeConfigError(f"Unknown language: {language}") from e

        if (template_name := config.template) is None:
            template_name = Sequential.__name__
        try:
            template = cls.subclasses()[template_name]
        except KeyError as e:
            raise ResumeConfigError(f"Unknown template: {template_name}") from e

        if (ascii_only := config.ascii_only) is None:
            ascii_only = False

        return template(
            model=model,
            theme=theme,
            translation=translation,
            locale=Locale(language),
            ascii_only=ascii_only,
        )

    @classmethod
    def from_file(cls, file: Path) -> "Template":
        with open(file, "r", encoding="utf8") as f:
            contents = json.loads(f.read())

        return cls.from_model_config(ResumeSchema(**contents))


class PaddingLevels(NamedTuple):
    """Need a `tuple` for `rich` to work with, a `dataclass` is too inconvenient."""

    top: int
    right: int
    bottom: int
    left: int


def indent(renderable: RenderableType, level: int = 4) -> Padding:
    return Padding.indent(renderable, level=level)


def join(*pairs: tuple[Optional[str], Style], separator: str = " - ") -> Optional[Text]:
    out = Text()
    for content, style in pairs:
        if content:
            if out:  # Some content exists already
                out.append(separator)
            out.append(content, style)
    return out or None


def horizontal_fill(left: RenderableType, right: RenderableType) -> RenderableGenerator:
    table = Table.grid(
        Column("left", justify="left"),
        Column("right", justify="right"),
        expand=True,
    )
    table.add_row(left, right)

    if table.rows:
        yield table


def ensure_single_trailing_newline(sequence: MutableSequence[RenderableType]) -> None:
    """Ensure that `sequence` ends w/ exactly one `NewLine`, removing if necessary.

    This has to be done in-place (yuck) because `rich.console.Group.renderables` is a
    read-only property. It can be modified in-place, but not assigned to again.
    """
    while True:
        match sequence:
            case [*_, NewLine(), NewLine()]:
                sequence.pop()
            case [*_, last] if not isinstance(last, NewLine):
                sequence.append(NewLine())
            case []:
                sequence.append(NewLine())
            case _:
                break
    return None


class Sequential(Template):
    def section(self, title: str) -> RenderableGenerator:
        yield NewLine()
        yield Rule(
            Text(title, style=self.theme.headlines[1]),
            align="left",
            characters=self.theme.rulechar,
        )
        yield NewLine()

    @group()
    def format_and_group_all_elements(
        self,
        container: ResumeItemContainer,
    ) -> RenderableGenerator:
        if container is None:
            return
        for item in container:
            yield from self.format(item, self.theme)
            yield NewLine()

    @singledispatchmethod
    def format(self, item: ResumeItem, theme: Theme) -> RenderableGenerator:
        return NotImplemented

    @format.register
    def _(self, item: Basics, theme: Theme) -> RenderableGenerator:
        if name := item.name:
            yield Rule(
                Text(name, style=theme.headlines[0]),
                characters=theme.rulechar,
            )
            yield NewLine()

        if label := item.label:
            yield Align.center(Text(label, style=theme.emphasis[2]))
            yield NewLine()
        contact_items = [item for item in (item.email, item.phone, item.url) if item]
        yield Align.center(Text("  ".join(contact_items)))
        yield NewLine()
        if summary := item.summary:
            yield Text(summary)
            yield NewLine()

    @format.register
    def _(self, item: Location, theme: Theme) -> RenderableGenerator:
        if address := item.address:
            lines = address.split("\n")
            for line in lines:
                yield Align.center(Text(line))

        country_line = [
            item
            for item in (item.postalCode, item.city, item.region, item.countryCode)
            if item
        ]
        yield Align.center(Text(", ".join(country_line)))

    @format.register
    def _(self, item: Profile, theme: Theme) -> RenderableGenerator:
        yield item.network or ""
        yield item.username or ""
        yield f"({item.url})" if item.url else ""

    @format.register
    def _(self, item: WorkItem, theme: Theme) -> RenderableGenerator:
        tagline = Text.assemble(
            (item.name or "", theme.emphasis[0]),
            " ",
            (item.description or "", theme.emphasis[1]),
        )

        yield from horizontal_fill(
            tagline, self.date_range(item.startDate, item.endDate)
        )

        if position := item.position:
            yield NewLine()
            yield indent(Text(position))

        if summary := item.summary:
            yield NewLine()
            yield indent(Text(summary))

        if highlights := item.highlights:
            yield NewLine()
            for highlight in highlights:
                yield indent(indent(Text(f"{theme.bullet} {highlight}")))

        location = item.location
        url = item.url
        if location or url:
            yield NewLine()
            yield indent(
                Text.assemble(
                    location or "",
                    " - " if (location and url) else "",
                    (url or "", theme.emphasis[1]),
                )
            )

    @format.register
    def _(self, item: Skill, theme: Theme) -> RenderableGenerator:
        if name := item.name:
            yield Text.assemble(
                (name, theme.emphasis[0]),
                (f" - {item.level}" if item.level else "", theme.emphasis[0]),
            )
            if keywords := item.keywords:
                yield NewLine()
                yield indent(Text(", ".join(keywords), style=theme.emphasis[1]))
            yield NewLine()

    @format.register
    def _(self, item: VolunteerItem, theme: Theme) -> RenderableGenerator:
        yield from horizontal_fill(
            Text(item.organization or "", style=theme.emphasis[0]),
            self.date_range(item.startDate, item.endDate),
        )

        if position := item.position:
            yield NewLine()
            yield indent(Text(position))

        if summary := item.summary:
            yield NewLine()
            yield indent(Text(summary))

        if highlights := item.highlights:
            yield NewLine()
            for highlight in highlights:
                yield indent(indent(Text(f"{theme.bullet} {highlight}")))

        if url := item.url:
            yield NewLine()
            yield indent(Text(url, theme.emphasis[1]))

    @format.register
    def _(self, item: EducationItem, theme: Theme) -> RenderableGenerator:
        yield from horizontal_fill(
            Text.assemble(
                (item.institution or "", theme.emphasis[0]),
                ": " if item.area else "",
                (item.area or "", theme.emphasis[1]),
                f" ({item.studyType})" if item.studyType else "",
            ),
            self.date_range(item.startDate, item.endDate),
        )

        if score := item.score:
            yield NewLine()
            yield indent(Text(f"{self.translation.score}: {score}"))

        if courses := item.courses:
            yield NewLine()
            for course in courses:
                yield indent(indent(Text(f"{theme.bullet} {course}")))

        if url := item.url:
            yield NewLine()
            yield indent(Text(url, theme.emphasis[1]))

    @format.register
    def _(self, item: Award, theme: Theme) -> RenderableGenerator:
        yield from horizontal_fill(
            Text.assemble(
                (item.title or "", theme.emphasis[0]),
                (f" ({item.awarder})" if item.awarder else "", theme.emphasis[1]),
            ),
            self.format_date(item.date) if item.date else "",
        )

        if summary := item.summary:
            yield NewLine()
            yield indent(Text(summary))

    @format.register
    def _(self, item: Certificate, theme: Theme) -> RenderableGenerator:
        yield from horizontal_fill(
            Text.assemble(
                (item.name or "", theme.emphasis[0]),
                (f" ({item.issuer})" if item.issuer else "", theme.emphasis[1]),
            ),
            self.format_date(item.date) if item.date else "",
        )

        if url := item.url:
            yield NewLine()
            yield indent(Text(url, style=theme.emphasis[1]))

    @format.register
    def _(self, item: Publication, theme: Theme) -> RenderableGenerator:
        yield from horizontal_fill(
            Text.assemble(
                (item.name or "", theme.emphasis[0]),
                (f" ({item.publisher})" if item.publisher else "", theme.emphasis[1]),
            ),
            self.format_date(item.releaseDate) if item.releaseDate else "",
        )

        if summary := item.summary:
            yield NewLine()
            yield indent(Text(summary))

        if url := item.url:
            yield NewLine()
            yield indent(Text(url, style=theme.emphasis[1]))

    @format.register
    def _(self, item: Language, theme: Theme) -> RenderableGenerator:
        if language := item.language:
            yield NewLine()
            yield Text(language, style=theme.emphasis[0])
            if fluency := item.fluency:
                yield NewLine()
                yield indent(Text(fluency, style=theme.emphasis[1]))

    @format.register
    def _(self, item: Reference, theme: Theme) -> RenderableGenerator:
        if reference := item.reference:
            yield NewLine()
            yield indent(Text(reference, style=theme.emphasis[1]))

            if name := item.name:
                yield NewLine()
                yield indent(Text(f" - {name}", style=theme.emphasis[0]))

    @format.register
    def _(self, item: Interest, theme: Theme) -> RenderableGenerator:
        if name := item.name:
            yield Text(name, style=theme.emphasis[0])
            if keywords := item.keywords:
                yield NewLine()
                yield indent(Text(", ".join(keywords), style=theme.emphasis[1]))
            yield NewLine()

    @format.register
    def _(self, item: Project, theme: Theme) -> RenderableGenerator:
        yield from horizontal_fill(
            Text.assemble(
                (item.name or "", theme.emphasis[0]),
                (f" - {item.type}" if item.type else "", theme.emphasis[1]),
            ),
            self.date_range(item.startDate, item.endDate),
        )

        if description := item.description:
            yield indent(Text(description, theme.emphasis[1]))
            yield NewLine()

        if highlights := item.highlights:
            for highlight in highlights:
                yield indent(indent(Text(f"{theme.bullet} {highlight}")))
            yield NewLine()

        if roles := item.roles:
            yield indent(Text(f"{self.translation.roles}:"))
            yield NewLine()
            for role in roles:
                yield indent(
                    indent(Text(f"{theme.bullet} {role}", style=theme.emphasis[1]))
                )
            yield NewLine()

        if keywords := item.keywords:
            yield indent(Text(", ".join(keywords), style=theme.emphasis[1]))
            yield NewLine()

        footer = join((item.url, theme.emphasis[1]), (item.entity, theme.emphasis[0]))
        if footer:
            yield indent(footer)
            yield NewLine()

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderableGenerator:
        if basics := self.model.basics:
            yield from self.format(basics, self.theme)

            if profiles := basics.profiles:
                table = Table.grid(
                    Column("network", style=self.theme.emphasis[0]),
                    Column("username", style=self.theme.emphasis[1]),
                    Column("url"),
                    padding=PaddingLevels(top=0, right=1, bottom=0, left=1),
                )
                for profile in profiles:
                    formatted = self.format(profile, self.theme)
                    table.add_row(*formatted)
                yield Align.center(table)

            if location := basics.location:
                yield NewLine()
                yield from self.format(location, self.theme)

            yield NewLine()

        container: ResumeItemContainer
        title: str
        m = self.model
        t = self.translation
        for container, title in [
            (m.work, t.work),
            (m.education, t.education),
            (m.skills, t.skills),
            (m.awards, t.awards),
            (m.certificates, t.certificates),
            (m.publications, t.publications),
            (m.languages, t.languages),
            (m.references, t.references),
            (m.volunteer, t.volunteer),
            (m.projects, t.projects),
            (m.interests, t.interests),
        ]:
            if container:
                group = Group(
                    *self.section(title),
                    *self.format_and_group_all_elements(container).renderables,
                )
                ensure_single_trailing_newline(group.renderables)
                yield group
