from functools import partial, singledispatchmethod
from typing import NamedTuple, Optional

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
    Skill,
    VolunteerItem,
    WorkItem,
)
from ancv.visualization import (
    RenderableGenerator,
    ResumeItem,
    ResumeItemContainer,
    Template,
)
from ancv.visualization.themes import Theme
from rich import box
from rich.align import Align
from rich.console import Console, ConsoleOptions, Group, NewLine, RenderableType, group
from rich.padding import Padding
from rich.panel import Panel
from rich.rule import Rule
from rich.style import Style
from rich.table import Column, Table
from rich.text import Text


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
        yield NewLine()


class BerlinSkeleton(Template):
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

    @singledispatchmethod
    @staticmethod
    def format(item: ResumeItem, theme: Theme) -> RenderableGenerator:
        return Template.format(item, theme)

    @format.register
    @staticmethod
    def _(item: Basics, theme: Theme) -> RenderableGenerator:
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
    @staticmethod
    def _(item: Location, theme: Theme) -> RenderableGenerator:
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
    @staticmethod
    def _(item: Profile, theme: Theme) -> RenderableGenerator:
        yield item.network or ""
        yield item.username or ""
        yield f"({item.url})" if item.url else ""

    @format.register
    @staticmethod
    def _(item: WorkItem, theme: Theme) -> RenderableGenerator:
        tagline = Text.assemble(
            (item.name or "", theme.emphasis[0]),
            " ",
            (item.description or "", theme.emphasis[1]),
        )

        yield from horizontal_fill(
            tagline, theme.date_range(item.startDate, item.endDate, theme.datefmt)
        )

        if position := item.position:
            yield indent(Text(position))
            yield NewLine()

        if summary := item.summary:
            yield indent(Text(summary))
            yield NewLine()

        if highlights := item.highlights:
            for highlight in highlights:
                yield indent(indent(Text(f"{theme.bullet} {highlight}")))
            yield NewLine()

        yield indent(
            Text.assemble(
                item.location or "",
                " - " if (item.location and item.url) else "",
                (item.url or "", theme.emphasis[1]),
            )
        )
        yield NewLine()

    @format.register
    @staticmethod
    def _(item: VolunteerItem, theme: Theme) -> RenderableGenerator:
        yield from horizontal_fill(
            Text(item.organization or "", style=theme.emphasis[0]),
            theme.date_range(item.startDate, item.endDate, theme.datefmt),
        )

        if position := item.position:
            yield indent(Text(position))
            yield NewLine()

        if summary := item.summary:
            yield indent(Text(summary))
            yield NewLine()

        if highlights := item.highlights:
            for highlight in highlights:
                yield indent(indent(Text(f"{theme.bullet} {highlight}")))
            yield NewLine()

        yield indent(Text(item.url or "", theme.emphasis[1]))
        yield NewLine()

    @format.register
    @staticmethod
    def _(item: EducationItem, theme: Theme) -> RenderableGenerator:
        yield from horizontal_fill(
            Text.assemble(
                (item.institution or "", theme.emphasis[0]),
                ": " if item.institution else "",
                (item.area or "", theme.emphasis[1]),
                f" ({item.studyType})" if item.studyType else "",
            ),
            theme.date_range(item.startDate, item.endDate, theme.datefmt),
        )

        if score := item.score:
            yield indent(Text(f"Score: {score}"))
            yield NewLine()

        if courses := item.courses:
            for course in courses:
                yield indent(indent(Text(f"{theme.bullet} {course}")))
            yield NewLine()

        if url := item.url:
            yield indent(Text(url, theme.emphasis[1]))
            yield NewLine()

    @format.register
    @staticmethod
    def _(item: Award, theme: Theme) -> RenderableGenerator:
        yield from horizontal_fill(
            Text.assemble(
                (item.title or "", theme.emphasis[0]),
                " awarded by " if item.awarder else "",
                (item.awarder or "", theme.emphasis[1]),
            ),
            item.date.strftime(theme.datefmt) if item.date else "",
        )

        if summary := item.summary:
            yield indent(Text(summary))
            yield NewLine()

    @format.register
    @staticmethod
    def _(item: Certificate, theme: Theme) -> RenderableGenerator:
        yield from horizontal_fill(
            Text.assemble(
                (item.name or "", theme.emphasis[0]),
                " issued by " if item.issuer else "",
                (item.issuer or "", theme.emphasis[1]),
            ),
            item.date.strftime(theme.datefmt) if item.date else "",
        )

        if url := item.url:
            yield indent(Text(url, style=theme.emphasis[1]))
            yield NewLine()

    @format.register
    @staticmethod
    def _(item: Publication, theme: Theme) -> RenderableGenerator:
        yield from horizontal_fill(
            Text.assemble(
                (item.name or "", theme.emphasis[0]),
                " ",
                (item.publisher or "", theme.emphasis[1]),
            ),
            item.releaseDate.strftime(theme.datefmt) if item.releaseDate else "",
        )

        if summary := item.summary:
            yield indent(Text(summary))
            yield NewLine()

        if url := item.url:
            yield indent(Text(url, style=theme.emphasis[1]))
            yield NewLine()

    @format.register
    @staticmethod
    def _(item: Language, theme: Theme) -> RenderableGenerator:
        match item:
            # Not sure this is the best way; very verbose since every possible
            # combination needs to be handled.
            case Language(language=str() as name, fluency=None):
                yield Text(name)
            case Language(language=None, fluency=str() as level):
                yield Text(level)
            case Language(language=str() as name, fluency=str() as level):
                yield Text.assemble(
                    (name, theme.emphasis[0]), " ", (level, theme.emphasis[1])
                )

    @format.register
    @staticmethod
    def _(item: Reference, theme: Theme) -> RenderableGenerator:
        if reference := item.reference:
            yield indent(Text(reference, style=theme.emphasis[1]))
            yield NewLine()

            if name := item.name:
                yield indent(Text(f" - {name}", style=theme.emphasis[0]))
                yield NewLine()

    @format.register
    @staticmethod
    def _(item: Interest, theme: Theme) -> RenderableGenerator:
        if name := item.name:
            yield Text(name, style=theme.emphasis[0])
            if keywords := item.keywords:
                yield indent(Text(", ".join(keywords), style=theme.emphasis[1]))
            yield NewLine()

    @format.register
    @staticmethod
    def _(item: Project, theme: Theme) -> RenderableGenerator:
        yield from horizontal_fill(
            Text.assemble(
                (item.name or "", theme.emphasis[0]),
                (f" - {item.type}" if item.type else "", theme.emphasis[1]),
            ),
            theme.date_range(item.startDate, item.endDate, theme.datefmt),
        )

        if description := item.description:
            yield indent(Text(description, theme.emphasis[1]))
            yield NewLine()

        if highlights := item.highlights:
            for highlight in highlights:
                yield indent(indent(Text(f"{theme.bullet} {highlight}")))
            yield NewLine()

        if roles := item.roles:
            yield indent(Text("Roles:"))
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
        panel = partial(
            Panel,
            box=box.SIMPLE,
            padding=PaddingLevels(top=0, right=0, bottom=0, left=0),
        )

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

        if skills := self.model.skills:
            yield from self.section("Skills")
            table = Table.grid(
                Column("name", style=self.theme.emphasis[0]),
                Column("level"),
                Column("keywords", style=self.theme.emphasis[1]),
                padding=PaddingLevels(top=0, right=1, bottom=0, left=1),
            )
            for skill in skills:
                if name := skill.name:
                    keywords = ", ".join(skill.keywords) if skill.keywords else ""
                    level = skill.level or ""
                    table.add_row(name, level, keywords)
            yield panel(table)

        container: ResumeItemContainer
        title: str
        for container, title in [
            (self.model.work, "Experience"),
            (self.model.volunteer, "Volunteering"),
            (self.model.education, "Education"),
            (self.model.awards, "Awards"),
            (self.model.certificates, "Certificates"),
            (self.model.publications, "Publications"),
            (self.model.languages, "Languages"),
            (self.model.references, "References"),
            (self.model.interests, "Interests"),
            (self.model.projects, "Projects"),
        ]:
            if container:
                group = Group(
                    *self.section(title),
                    self.format_and_group_all_elements(container),
                )
                yield panel(group)
