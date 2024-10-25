import typing as t
from importlib.metadata import metadata

from pydantic import (
    AnyUrl,
    BaseModel,
    EmailStr,
    Field,
    computed_field,
)

from ancv import PACKAGE


class Metadata(BaseModel):
    """Modeling Python package metadata.

    Modelled after the Python core metadata specification:
    https://packaging.python.org/en/latest/specifications/core-metadata/ .
    Not all fields were implemented for lack of ability of testing.

    For more context, see:

        - https://docs.python.org/3/library/importlib.metadata.html#metadata
        - https://peps.python.org/pep-0566/
    """

    metadata_version: t.Annotated[
        str,
        Field(
            description="Version of the metadata format, e.g. '2.1'",
        ),
    ]
    name: t.Annotated[
        str,
        Field(
            description="Name of the package, e.g. 'ancv'",
            pattern=r"(?i)^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$",
        ),
    ]
    version: t.Annotated[
        str,
        Field(
            description="Version of the package, e.g. '0.1.0'",
            # https://peps.python.org/pep-0440/#appendix-b-parsing-version-strings-with-regular-expressions
            pattern=r"^([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))?(\.dev(0|[1-9][0-9]*))?$",
        ),
    ]
    summary: t.Annotated[
        t.Optional[str],
        Field(
            description="One-line summary of the package, e.g. 'Ancv is a package for ...'",
        ),
    ] = None
    download_url: t.Annotated[
        t.Optional[AnyUrl],
        Field(description="URL to download this version of the package"),
    ] = None
    license: t.Annotated[
        t.Optional[str], Field(description="License of the package, e.g. 'MIT'")
    ] = None
    author: t.Annotated[
        t.Optional[str],
        Field(description="Author of the package, e.g. 'John Doe'"),
    ] = None
    author_email: t.Annotated[
        t.Optional[EmailStr],
        Field(description="Email of the author, e.g. john@doe.com'"),
    ] = None
    requires_python: t.Annotated[
        t.Optional[str],
        Field(
            description="Python version required by the package, e.g. '>=3.6'",
        ),
    ] = None
    classifier: t.Annotated[
        t.Optional[list[str]],
        Field(
            description="Classifiers of the package, e.g. 'Programming Language :: Python :: 3.6'",
        ),
    ] = None
    requires_dist: t.Annotated[
        t.Optional[list[str]],
        Field(
            description="Distributions required by the package, e.g. 'aiohttp[speedups] (>=3.8.1,<4.0.0)'",
        ),
    ] = None
    project_url: t.Annotated[
        t.Optional[list[str]],
        Field(
            description="Project URLs of the package, e.g. 'Repository, https://github.com/namespace/ancv/'",
        ),
    ] = None
    description_content_type: t.Annotated[
        t.Optional[str],
        Field(
            description="Content type of the description, e.g. 'text/plain'",
        ),
    ] = None
    description: t.Annotated[
        t.Optional[str],
        Field(
            description="Long description of the package, e.g. 'Ancv is a package for ...'",
        ),
    ] = None

    @computed_field  # type: ignore[prop-decorator]
    @property
    def project_urls(
        self,
    ) -> t.Annotated[
        dict[str, str],
        Field(description="Map of project URLs, e.g. {'Homepage': 'https://ancv.io/'}"),
    ]:
        """Converts the 'Name, https://example.com' array of project URLs to a dict.

        https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#urls
        """

        urls: dict[str, str] = dict()

        if self.project_url is None:
            return urls

        for url in self.project_url:
            name, url = url.split(",")
            urls[name.strip()] = url.strip()

        return urls


METADATA = Metadata.model_validate(metadata(PACKAGE).json)
