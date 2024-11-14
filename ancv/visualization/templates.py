import json
from abc import ABC, abstractmethod
from contextlib import redirect_stdout
from datetime import date
from functools import lru_cache, singledispatchmethod
from pathlib import Path
from tempfile import SpooledTemporaryFile
from typing import Iterable, Literal, MutableSequence, NamedTuple, Optional

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
    ResumeSchema,
    Skill,
    TemplateConfig,
    VolunteerItem,
    WorkItem,
)
from ancv.exceptions import ResumeConfigError
from ancv.visualization import OUTPUT_COLUMN_WIDTH, RenderableGenerator
from ancv.visualization.themes import THEMES, Theme
from ancv.visualization.translations import TRANSLATIONS, Translation


class Template(ABC):
    """Base class for all templates.

    Templates are the top-level abstraction for rendering a resume. They hold all data
    as well as all styling information, combining them into a printable version.

    The ABC provides a common interface for all templates. Most importantly, it provides
    a common constructor, ensuring all necessary data is present.
    """

    def __init__(
        self,
        model: ResumeSchema,
        theme: Theme,
        translation: Translation,
        locale: Locale,
        ascii_only: bool,
        dec31_as_year: bool,
    ) -> None:
        self.model = model
        self.theme = theme
        self.translation = translation
        self.locale = locale
        self.ascii_only = ascii_only
        self.dec31_as_year = dec31_as_year

    @abstractmethod
    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderableGenerator:
        """Generates renderable elements from the template instance for `rich`.

        This method is called by `rich` for custom rendering of objects it doesn't
        natively know about:
        https://rich.readthedocs.io/en/stable/protocol.html#console-render

        Args:
            console: The `rich.Console` instance that is rendering the template.
            options: The `rich.ConsoleOptions` instance that contains information about.

        Yields:
            Renderable elements for `rich` to work with.
        """

        return NotImplemented

    def render(self) -> str:
        """Renders the template to a console-printable string.

        Using `self` and the data as well as styling information contained therein, uses
        a `rich.Console` to render the template to a string. The string contains ANSI
        escape codes for styling and formatting.

        Returns:
            A console-printable string representation of the template.
        """

        encoding = "ascii" if self.ascii_only else "utf-8"
        f = SpooledTemporaryFile(max_size=SIPrefix.MEGA, mode="w", encoding=encoding)

        with redirect_stdout(f):
            # `Console` ultimately checks `f.encoding` for its encoding, if no file is
            # passed explicitly:
            # https://github.com/Textualize/rich/blob/b89d0362e8ebcb18902f0f0a206879f1829b5c0b/rich/console.py#L933
            #
            # If we don't specify `file` aka `f`, it will default to `sys.stdout`.
            # Redirecting all of that to a fake, in-memory file with an
            # artificial/controlled encoding will fool `rich` into using its ASCII-only
            # rendering.
            console = Console(
                width=OUTPUT_COLUMN_WIDTH,
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
    def _format_date(self, date: date) -> str:
        """Formats a date according to the current theme.

        Args:
            date: The date to format.

        Returns:
            A string representation of the date, respecting the current theme (with its
            locale and possibly year-only only setting.)
        """

        format = self.theme.datefmt.full

        is_last_doy = date.month == date.max.month and date.day == date.max.day
        if is_last_doy and self.dec31_as_year:
            format = self.theme.datefmt.year_only

        # Code-wise, `format_date` could accept `DateTimePattern` as its `format`
        # directly (version 2.10.3):
        # https://github.com/python-babel/babel/blob/25e436016970443226d0ec19cf74ac8476369b33/babel/dates.py#L683
        # However, the type annotation is wrong/more restrictive, and it only accepts
        # `str`. The original stringly-typed date pattern hides in the `pattern`
        # attribute:
        pattern = format.pattern

        return format_date(date, format=pattern, locale=self.locale)

    @lru_cache(maxsize=1_000)
    def _format_date_range(
        self,
        start: Optional[date],
        end: Optional[date],
        collapse: bool = True,
    ) -> str:
        """Formats a date range according to the current theme.

        Both `start` and `end` are optional, and all four combinations are allowed,
        yielding different results. If no `end` is given, the range is considered
        "ongoing".

        Args:
            start: The start date of the range.
            end: The end date of the range.
            collapse: Whether to collapse the range to a single date if it is in the
                same month and year, e.g. "Jan 2021 - Jan 2021" -> "Jan 2021".

        Returns:
            A (possibly empty) string representation of the date range.
        """

        if start is None:
            if end is None:
                return ""
            return f"{self.theme.range_sep} {self._format_date(end)}"

        if end is None:
            return f"{self._format_date(start)} {self.theme.range_sep} {self.translation.present}"

        collapsible = start.month == end.month and start.year == end.year
        if collapsible and collapse:
            return self._format_date(end)

        return f"{self._format_date(start)} {self.theme.range_sep} {self._format_date(end)}"

    # A property would be nicer but it's not supported from Python 3.11 on:
    # https://docs.python.org/3.11/library/functions.html#classmethod
    @classmethod
    def subclasses(cls) -> dict[str, type["Template"]]:
        """Returns a dictionary of all subclasses of `Template`."""

        return {cls.__name__: cls for cls in cls.__subclasses__()}

    @classmethod
    def from_model_config(cls, model: ResumeSchema) -> "Template":
        """Creates a template instance from a resume model.

        Certain defaults are hard-coded *here* instead of in the `TemplateConfig` class
        (where it would be much cleaner using pydantic's field default syntax) such that
        `TemplateConfig` doesn't have to know about the available options.

        Args:
            model: The pydantic resume model to create the template from.

        Returns:
            A template instance.
        """

        if (config := model.meta.config) is None:
            config = TemplateConfig(
                template=None,
                theme=None,
                language=None,
                ascii_only=None,
                dec31_as_year=None,
            )

        if (theme_name := config.theme) is None:
            theme_name = "lollipop"
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

        if (dec31_as_year := config.dec31_as_year) is None:
            dec31_as_year = False

        return template(
            model=model,
            theme=theme,
            translation=translation,
            locale=Locale(language),
            ascii_only=ascii_only,
            dec31_as_year=dec31_as_year,
        )

    @classmethod
    def from_file(cls, file: Path) -> "Template":
        """Creates a template instance from a JSON resume file.

        The JSON file is validated against the `ResumeSchema` model, aka it has to
        possess this schema:
        https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json

        Args:
            file: The path to the JSON resume file.

        Returns:
            A template instance.
        """

        with open(file, "r", encoding="utf8") as f:
            contents = json.loads(f.read())

        return cls.from_model_config(ResumeSchema(**contents))


class PaddingLevels(NamedTuple):
    """Padding levels for `rich` objects.

    `rich` expects a `tuple`, so `dataclass` is not an option here:
    https://github.com/Textualize/rich/blob/b89d0362e8ebcb18902f0f0a206879f1829b5c0b/rich/table.py#L195
    Anonymous tuples aren't typing-friendly enough, so use a `NamedTuple` subclass.

    For more context, see https://rich.readthedocs.io/en/stable/padding.html.
    """

    top: int
    right: int
    bottom: int
    left: int


def indent(renderable: RenderableType, level: int = 4) -> Padding:
    """Indents a `rich` renderable by `level` spaces."""

    return Padding.indent(renderable, level=level)


def join(*pairs: tuple[Optional[str], Style], separator: str) -> Optional[Text]:
    """Joins a sequence of styled strings with a separator into a single `rich` `Text`.

    Args:
        pairs: A sequence of tuples of plain strings with corresponding styles.
        separator: The separator to use.

    Returns:
        A `rich` `Text` object or `None` if no content was provided.
    """

    out = Text()
    for content, style in pairs:
        if content:
            if out:  # Some content exists already
                out.append(separator)
            out.append(content, style)
    return out or None


def horizontal_fill(left: RenderableType, right: RenderableType) -> RenderableGenerator:
    """Yields a renderable with `left` and `right` maximally horizontally separated.

    For example:

    ```text
    +------------------------+------------------------+
    | left                   |                  right |
    +------------------------+------------------------+
    ```

    The functionality is implemented using `rich`'s `Table`, but since it's a normal
    renderable, a user usually needn't worry about it.

    Args:
        left: The left item. right: The right item.

    Yields:
        A single renderable objects, or nothing if no content was provided.
    """

    table = Table.grid(
        Column("left", justify="left"),
        Column("right", justify="right"),
        expand=True,
    )
    table.add_row(left, right)

    if table.rows:
        yield table


def ensure_single_trailing_newline(sequence: MutableSequence[RenderableType]) -> None:
    """Ensures that `sequence` ends w/ exactly one `NewLine`, removing any if necessary.

    This has to be done in-place (yuck) because `rich.console.Group.renderables` is a
    read-only property. It can be modified in-place, but not assigned to again.

    This function is idempotent.

    Args:
        sequence: The sequence to modify and ensure ends w/ exactly one `NewLine`.

    Returns:
        `None`: This is a side-effecting function.
    """

    while True:
        # Pattern matching prevents this function from being more generalizable: we
        # cannot pass `NewLine` or whatever type should be 'single trailing' as an
        # argument (forming a function like `ensure_single_trailing(seq, obj)`), since
        # pattern matching works primarily with literals.
        match sequence:  # noqa: E999
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
    """A sequential template.

    This template renders the resume sequentially, i.e. all sections are rendered one
    after another, linearly until all sections are exhausted. This is in contrast to
    other thinkable templates, like multi-column ones.
    """

    def _section(
        self, title: str, align: Literal["left", "center", "right"] = "center"
    ) -> RenderableGenerator:
        """Renders a section title.

        Args:
            title: The title to render. align: The alignment of the title.

        Yields:
            A `rich` renderable. Ensure to exhaust the generator to receive all relevant
            and intended items.
        """

        yield NewLine()
        yield Rule(
            Text(title, style=self.theme.emphasis.maximum),
            align=align,
            characters=self.theme.rulechar,
            style=self.theme.emphasis.maximum,
        )
        yield NewLine()

    def _format_all(
        self,
        items: Optional[Iterable[ResumeItem]],
    ) -> RenderableGenerator:
        """Formats aka renders all items in an iterable.

        Through method overloading, `self` will (need to) know how to render each item
        automatically.

        Args:
            items: The items to render.

        Yields:
            A `rich` renderable. Ensure to exhaust the generator to receive all relevant
            and intended items.
        """

        if items is None:
            return

        for item in items:
            yield from self.format(item)
            yield NewLine()

    # In some scenarios, we need an iterable of renderables in a `rich.Group`:
    _format_all_and_group = group(fit=True)(_format_all)

    @singledispatchmethod
    def format(self, item: ResumeItem) -> RenderableGenerator:
        """Formats aka renders a resume item. Base case for method overloading."""
        return NotImplemented

    @format.register
    def _(self, item: Basics) -> RenderableGenerator:
        """Formats aka renders a `Basics` item."""

        if name := item.name:
            yield from self._section(name)

        if label := item.label:
            yield Align.center(Text(label, style=self.theme.emphasis.strong))
            yield NewLine()

        contact_items = [
            str(item) for item in (item.email, item.phone, item.url) if item
        ]
        if contact_items:
            yield Align.center(
                Text(
                    f" {self.theme.sep} ".join(contact_items),
                    style=self.theme.emphasis.weak,
                )
            )
            yield NewLine()

        if summary := item.summary:
            yield Text(summary, style=self.theme.emphasis.medium)
            yield NewLine()

    @format.register
    def _(self, item: Location) -> RenderableGenerator:
        """Formats aka renders a `Location` item."""

        if address := item.address:
            lines = address.split("\n")
            for line in lines:
                yield Align.center(Text(line, style=self.theme.emphasis.weak))

        country_line = [
            item
            for item in (item.postalCode, item.city, item.region, item.countryCode)
            if item
        ]
        yield Align.center(
            Text(", ".join(country_line), style=self.theme.emphasis.weak)
        )

    @format.register
    def _(self, item: Profile) -> RenderableGenerator:
        """Formats aka renders a `Profile` item."""

        yield item.network or ""
        yield item.username or ""
        yield f"({item.url})" if item.url else ""

    @format.register
    def _(self, item: WorkItem) -> RenderableGenerator:
        """Formats aka renders a `WorkItem` item."""

        tagline = Text.assemble(
            (item.name or "", self.theme.emphasis.maximum),
            " ",
            (item.description or "", self.theme.emphasis.weak),
        )

        yield from horizontal_fill(
            tagline,
            Text(
                self._format_date_range(item.startDate, item.endDate),
                style=self.theme.emphasis.weak,
            ),
        )

        if position := item.position:
            yield NewLine()
            yield indent(Text(position, style=self.theme.emphasis.strong))

        if summary := item.summary:
            yield NewLine()
            yield indent(Text(summary, style=self.theme.emphasis.medium))

        if highlights := item.highlights:
            yield NewLine()
            for highlight in highlights:
                yield indent(
                    indent(
                        Text(
                            f"{self.theme.bullet} {highlight}",
                            style=self.theme.emphasis.medium,
                        )
                    )
                )

        location = item.location
        url = item.url
        if location or url:
            yield NewLine()
            yield indent(
                Text.assemble(
                    (location or "", self.theme.emphasis.weak),
                    (
                        f" {self.theme.sep} " if (location and url) else "",
                        self.theme.emphasis.weak,
                    ),
                    ("" if url is None else str(url), self.theme.emphasis.weak),
                )
            )

    @format.register
    def _(self, item: Skill) -> RenderableGenerator:
        """Formats aka renders a `Skill` item."""

        if name := item.name:
            yield Text.assemble(
                (name, self.theme.emphasis.maximum),
                (" " if item.level else ""),
                (self.theme.sep if item.level else "", self.theme.emphasis.maximum),
                (" " if item.level else ""),
                (f"{item.level}" if item.level else "", self.theme.emphasis.strong),
            )
            if keywords := item.keywords:
                yield NewLine()
                yield indent(
                    Text(", ".join(keywords), style=self.theme.emphasis.medium)
                )
            yield NewLine()

    @format.register
    def _(self, item: VolunteerItem) -> RenderableGenerator:
        """Formats aka renders a `VolunteerItem` item."""

        yield from horizontal_fill(
            Text(item.organization or "", style=self.theme.emphasis.maximum),
            Text(
                self._format_date_range(item.startDate, item.endDate),
                style=self.theme.emphasis.weak,
            ),
        )

        if position := item.position:
            yield NewLine()
            yield indent(Text(position, style=self.theme.emphasis.strong))

        if summary := item.summary:
            yield NewLine()
            yield indent(Text(summary, style=self.theme.emphasis.medium))

        if highlights := item.highlights:
            yield NewLine()
            for highlight in highlights:
                yield indent(
                    indent(
                        Text(
                            f"{self.theme.bullet} {highlight}",
                            style=self.theme.emphasis.medium,
                        )
                    )
                )

        if url := item.url:
            yield NewLine()
            yield indent(Text(str(url), self.theme.emphasis.weak))

    @format.register
    def _(self, item: EducationItem) -> RenderableGenerator:
        """Formats aka renders a `EducationItem` item."""

        yield from horizontal_fill(
            Text.assemble(
                (item.institution or "", self.theme.emphasis.maximum),
                (":" if item.area else "", self.theme.emphasis.maximum),
                " " if item.area else "",
                (item.area or "", self.theme.emphasis.strong),
                " " if item.studyType else "",
                (
                    f"({item.studyType})" if item.studyType else "",
                    self.theme.emphasis.medium,
                ),
            ),
            Text(
                self._format_date_range(item.startDate, item.endDate),
                style=self.theme.emphasis.weak,
            ),
        )

        if score := item.score:
            yield NewLine()
            yield indent(
                Text(
                    f"{self.translation.grade}: {score}",
                    style=self.theme.emphasis.medium,
                )
            )

        if courses := item.courses:
            yield NewLine()
            for course in courses:
                yield indent(
                    indent(
                        Text(
                            f"{self.theme.bullet} {course}",
                            style=self.theme.emphasis.weak,
                        )
                    )
                )

        if url := item.url:
            yield NewLine()
            yield indent(Text(str(url), style=self.theme.emphasis.weak))

    @format.register
    def _(self, item: Award) -> RenderableGenerator:
        """Formats aka renders a `Award` item."""

        yield from horizontal_fill(
            Text.assemble(
                (item.title or "", self.theme.emphasis.maximum),
                " " if item.awarder else "",
                (f"({item.awarder})" if item.awarder else "", self.theme.emphasis.weak),
            ),
            Text(
                self._format_date(item.date) if item.date else "",
                style=self.theme.emphasis.weak,
            ),
        )

        if summary := item.summary:
            yield NewLine()
            yield indent(Text(summary, style=self.theme.emphasis.medium))

    @format.register
    def _(self, item: Certificate) -> RenderableGenerator:
        """Formats aka renders a `Certificate` item."""

        yield from horizontal_fill(
            Text.assemble(
                (item.name or "", self.theme.emphasis.maximum),
                " " if item.issuer else "",
                (f"({item.issuer})" if item.issuer else "", self.theme.emphasis.weak),
            ),
            Text(
                self._format_date(item.date) if item.date else "",
                style=self.theme.emphasis.weak,
            ),
        )

        if url := item.url:
            yield NewLine()
            yield indent(Text(str(url), style=self.theme.emphasis.weak))

    @format.register
    def _(self, item: Publication) -> RenderableGenerator:
        """Formats aka renders a `Publication` item."""

        yield from horizontal_fill(
            Text.assemble(
                (item.name or "", self.theme.emphasis.maximum),
                (" " if item.publisher else ""),
                (
                    f"({item.publisher})" if item.publisher else "",
                    self.theme.emphasis.weak,
                ),
            ),
            Text(
                self._format_date(item.releaseDate) if item.releaseDate else "",
                style=self.theme.emphasis.weak,
            ),
        )

        if summary := item.summary:
            yield NewLine()
            yield indent(Text(summary, style=self.theme.emphasis.medium))

        if url := item.url:
            yield NewLine()
            yield indent(Text(str(url), style=self.theme.emphasis.weak))

    @format.register
    def _(self, item: Language) -> RenderableGenerator:
        """Formats aka renders a `Language` item."""

        if language := item.language:
            yield NewLine()
            yield Text(language, style=self.theme.emphasis.maximum)
            if fluency := item.fluency:
                yield NewLine()
                yield indent(Text(fluency, style=self.theme.emphasis.strong))

    @format.register
    def _(self, item: Reference) -> RenderableGenerator:
        """Formats aka renders a `Reference` item."""

        if reference := item.reference:
            yield NewLine()
            yield indent(Text(reference, style=self.theme.emphasis.strong))

            if name := item.name:
                yield NewLine()
                yield indent(
                    Text(f" {self.theme.bullet} {name}", style=self.theme.emphasis.weak)
                )

    @format.register
    def _(self, item: Interest) -> RenderableGenerator:
        """Formats aka renders a `Interest` item."""

        if name := item.name:
            yield Text(name, style=self.theme.emphasis.maximum)
            if keywords := item.keywords:
                yield NewLine()
                yield indent(
                    Text(", ".join(keywords), style=self.theme.emphasis.strong)
                )
            yield NewLine()

    @format.register
    def _(self, item: Project) -> RenderableGenerator:
        """Formats aka renders a `Project` item."""

        yield from horizontal_fill(
            Text.assemble(
                (item.name or "", self.theme.emphasis.maximum),
                (" " if item.type else ""),
                (self.theme.sep if item.type else "", self.theme.emphasis.maximum),
                (" " if item.type else ""),
                (item.type if item.type else "", self.theme.emphasis.weak),
            ),
            Text(
                self._format_date_range(item.startDate, item.endDate),
                style=self.theme.emphasis.weak,
            ),
        )

        if description := item.description:
            yield NewLine()
            yield indent(Text(description, self.theme.emphasis.strong))
            yield NewLine()

        if highlights := item.highlights:
            for highlight in highlights:
                yield indent(
                    indent(
                        Text(
                            f"{self.theme.bullet} {highlight}",
                            style=self.theme.emphasis.medium,
                        )
                    )
                )
            yield NewLine()

        if roles := item.roles:
            yield indent(
                Text(f"{self.translation.roles}:", style=self.theme.emphasis.strong)
            )
            yield NewLine()
            for role in roles:
                yield indent(
                    indent(
                        Text(
                            f"{self.theme.bullet} {role}",
                            style=self.theme.emphasis.medium,
                        )
                    )
                )
            yield NewLine()

        if keywords := item.keywords:
            yield indent(Text(", ".join(keywords), style=self.theme.emphasis.medium))
            yield NewLine()

        footer = join(
            ("" if item.url is None else str(item.url), Style()),
            (item.entity, Style()),
            separator=self.theme.sep,
        )
        if footer:
            footer.style = self.theme.emphasis.weak
            yield indent(footer)
            yield NewLine()

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderableGenerator:
        """Renders the resume."""

        # While all other parts of the resume are sequential and trivially rendered and
        # composed, the basics section has some special, center-aligned formatting
        # logic. As such, it is treated as a special case and rendered separately, not
        # in the main loop below.
        if basics := self.model.basics:
            yield from self.format(basics)

            if profiles := basics.profiles:
                table = Table.grid(
                    Column("network", style=self.theme.emphasis.strong),
                    Column("username", style=self.theme.emphasis.medium),
                    Column("url", style=self.theme.emphasis.weak),
                    padding=PaddingLevels(top=0, right=1, bottom=0, left=1),
                )
                for profile in profiles:
                    formatted = self.format(profile)
                    table.add_row(*formatted)
                yield Align.center(table)

            if location := basics.location:
                yield NewLine()
                yield from self.format(location)

            yield NewLine()

        # Shortcut names
        m = self.model
        t = self.translation

        items_with_title: list[tuple[Optional[Iterable[ResumeItem]], str]] = [
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
        ]

        # The 'main loop'. All items are rendered through `singledispatch`. This is
        # somewhat elegant, but has limitations: all elements can only easily be
        # rendered on their own, forcing sequential flow. Multi-column outputs are not
        # possible, for example.
        for items, title in items_with_title:
            # Key aka section might be missing entirely (`None`) *or* be empty (`[]`),
            # the latter of which type checking cannot protect against. In either case,
            # skip the section.
            if not items:
                continue

            group = Group(
                *self._section(title),
                *self._format_all_and_group(items).renderables,
            )
            ensure_single_trailing_newline(group.renderables)
            yield group
