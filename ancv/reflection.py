import typing as t
from importlib.metadata import metadata

from pydantic import AnyUrl, BaseModel, EmailStr, Field, field_validator

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
        str | None,
        Field(
            description="One-line summary of the package, e.g. 'Ancv is a package for ...'",
        ),
    ]
    home_page: t.Annotated[
        AnyUrl | None,
        Field(description="Homepage of the package, e.g. https://ancv.io/'"),
    ] = None
    download_url: t.Annotated[AnyUrl | None, Field(description="URL to download this version of the package")] = None
    license: t.Annotated[str | None, Field(description="License of the package, e.g. 'MIT'")] = None
    author: t.Annotated[str | None, Field(description="Author of the package, e.g. 'John Doe'")] = None
    author_email: t.Annotated[EmailStr | None, Field(description="Email of the author, e.g. john@doe.com'")] = None
    requires_python: t.Annotated[
        str | None,
        Field(
            description="Python version required by the package, e.g. '>=3.6'",
        ),
    ] = None
    classifier: t.Annotated[
        list[str] | None,
        Field(
            description="Classifiers of the package, e.g. 'Programming Language :: Python :: 3.6'",
        ),
    ] = None
    requires_dist: t.Annotated[
        list[str] | None,
        Field(
            description="Distributions required by the package, e.g. 'aiohttp[speedups] (>=3.8.1,<4.0.0)'",
        ),
    ] = None
    project_url: t.Annotated[
        list[str] | None,
        Field(
            description="Project URLs of the package, e.g. 'Repository, https://github.com/namespace/ancv/'",
        ),
    ] = None
    description_content_type: t.Annotated[
        str | None,
        Field(
            description="Content type of the description, e.g. 'text/plain'",
        ),
    ] = None
    description: t.Annotated[
        str | None,
        Field(
            description="Long description of the package, e.g. 'Ancv is a package for ...'",
        ),
    ] = None

    @field_validator("project_url")
    def strip_prefix(cls, v: list[str] | None) -> list[str] | None:
        """Strips the prefixes 'Name, ' from the URLs.

        For example, extracts just the URL from:
        'Repository, https://github.com/namespace/ancv/'.
        """
        if v is None:
            return v
        return [url.split()[-1] for url in v]


METADATA = Metadata(**metadata(PACKAGE).json)
