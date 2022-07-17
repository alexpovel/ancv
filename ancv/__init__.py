from enum import IntEnum
from importlib.metadata import metadata
from pathlib import Path
from typing import Optional

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator

PROJECT_ROOT = Path(__file__).parent
PACKAGE = __package__


class SIPrefix(IntEnum):
    KILO = 1e3
    MEGA = 1e6


class Metadata(BaseModel):
    """Python package metadata.

    Modelled after the Python core metadata specification:
    https://packaging.python.org/en/latest/specifications/core-metadata/ .
    Not all fields were implemented for lack of ability of testing.

    For more context, see:

        - https://docs.python.org/3/library/importlib.metadata.html#metadata
        - https://peps.python.org/pep-0566/
    """

    metadata_version: str = Field(
        description="Version of the metadata format, e.g. '2.1'",
    )
    name: str = Field(
        description="Name of the package, e.g. 'ancv'",
        regex=r"(?i)^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$",
    )
    version: str = Field(
        description="Version of the package, e.g. '0.1.0'",
        # https://peps.python.org/pep-0440/#appendix-b-parsing-version-strings-with-regular-expressions
        regex=r"^([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))?(\.dev(0|[1-9][0-9]*))?$",
    )
    summary: Optional[str] = Field(
        description="One-line summary of the package, e.g. 'Ancv is a package for ...'",
    )
    home_page: Optional[AnyUrl] = Field(
        description="Homepage of the package, e.g. https://ancv.io/'"
    )
    download_url: Optional[AnyUrl] = Field(
        description="URL to download this version of the package"
    )
    license: Optional[str] = Field(description="License of the package, e.g. 'MIT'")
    author: Optional[str] = Field(description="Author of the package, e.g. 'John Doe'")
    author_email: Optional[EmailStr] = Field(
        description="Email of the author, e.g. john@doe.com'"
    )
    requires_python: Optional[str] = Field(
        description="Python version required by the package, e.g. '>=3.6'",
    )
    classifier: Optional[list[str]] = Field(
        description="Classifiers of the package, e.g. 'Programming Language :: Python :: 3.6'",
    )
    requires_dist: Optional[list[str]] = Field(
        description="Distributions required by the package, e.g. 'aiohttp[speedups] (>=3.8.1,<4.0.0)'",
    )
    project_url: Optional[list[str]] = Field(
        description="Project URLs of the package, e.g. 'Repository, https://github.com/namespace/ancv/'",
    )
    description_content_type: Optional[str] = Field(
        description="Content type of the description, e.g. 'text/plain'",
    )
    description: Optional[str] = Field(
        description="Long description of the package, e.g. 'Ancv is a package for ...'",
    )

    @validator("project_url")
    def strip_prefix(cls, v: Optional[list[str]]) -> Optional[list[str]]:
        if v is None:
            return v
        return [url.split()[-1] for url in v]


METADATA = Metadata(**metadata(PACKAGE).json)
