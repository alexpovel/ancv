"""This module contains models for the JSON Resume standard.

See: https://jsonresume.org/schema/.
"""

from __future__ import annotations

import typing as t
from datetime import date, datetime

from pydantic import AnyUrl, BaseModel, ConfigDict, EmailStr, Field


class Location(BaseModel):
    """Modelling a JSON resume location item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L50-L73
    """

    model_config = ConfigDict(extra="allow")

    address: t.Annotated[
        str,
        Field(
            description="To add multiple address lines, use \n. For example, 1234 Glücklichkeit Straße\nHinterhaus 5. Etage li.",
        ),
    ]
    postalCode: str | None = None
    city: str | None = None
    countryCode: t.Annotated[
        str,
        Field(description="code as per ISO-3166-1 ALPHA-2, e.g. US, AU, IN"),
    ] = None
    region: t.Annotated[
        str,
        Field(
            description="The general region where you live. Can be a US state, or a province, for instance.",
        ),
    ] = None


class Profile(BaseModel):
    """Modelling a JSON resume profile item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L74-L99
    """

    model_config = ConfigDict(extra="allow")

    network: t.Annotated[str | None, Field(description="e.g. Facebook or Twitter")] = None
    username: t.Annotated[str | None, Field(description="e.g. neutralthoughts")] = None
    url: t.Annotated[AnyUrl | None, Field(description="e.g. http://twitter.example.com/neutralthoughts")] = None


class Basics(BaseModel):
    """Modelling a JSON resume basics item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L17-L49
    """

    model_config = ConfigDict(extra="allow")

    name: str | None = None
    label: t.Annotated[str | None, Field(description="e.g. Web Developer")] = None
    image: t.Annotated[str | None, Field(description="URL (as per RFC 3986) to a image in JPEG or PNG format")] = None
    email: t.Annotated[EmailStr | None, Field(description="e.g. thomas@gmail.com")] = None
    phone: t.Annotated[str | None, Field(description="Phone numbers are stored as strings so use any format you like, e.g. 712-117-2923")] = None
    url: t.Annotated[AnyUrl | None, Field(description="URL (as per RFC 3986) to your website, e.g. personal homepage")] = None
    summary: t.Annotated[str | None, Field(description="Write a short 2-3 sentence biography about yourself")] = None
    location: Location | None = None
    profiles: t.Annotated[list[Profile] | None, Field(description="Specify any number of social networks that you participate in")] = None


class Certificate(BaseModel):
    """Modelling a JSON resume certificate item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L264-L292
    """

    model_config = ConfigDict(extra="allow")

    name: t.Annotated[str | None, Field(description="e.g. Certified Kubernetes Administrator")] = None
    date: t.Annotated[date | None, Field(description="e.g. 1989-06-12")] = None
    url: t.Annotated[AnyUrl | None, Field(description="e.g. http://example.com")] = None
    issuer: t.Annotated[str | None, Field(description="e.g. CNCF")] = None


class Skill(BaseModel):
    """Modelling a JSON resume skill item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L324-L351
    """

    model_config = ConfigDict(extra="allow")

    name: t.Annotated[str | None, Field(description="e.g. Web Development")] = None
    level: t.Annotated[str | None, Field(description="e.g. Master")] = None
    keywords: t.Annotated[list[str] | None, Field(description="List some keywords pertaining to this skill")] = None


class Language(BaseModel):
    """Modelling a JSON resume language item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L352-L370
    """

    model_config = ConfigDict(extra="allow")

    language: t.Annotated[str | None, Field(description="e.g. English, Spanish")] = None
    fluency: t.Annotated[str | None, Field(description="e.g. Fluent, Beginner")] = None


class Interest(BaseModel):
    """Modelling a JSON resume interest item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L371-L392
    """

    model_config = ConfigDict(extra="allow")

    name: t.Annotated[str | None, Field(description="e.g. Philosophy")] = None
    keywords: list[str] | None = None


class Reference(BaseModel):
    """Modelling a JSON resume reference item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L393-L411
    """

    model_config = ConfigDict(extra="allow")

    name: t.Annotated[str | None, Field(description="e.g. Timothy Cook")] = None
    reference: t.Annotated[
        str | None, Field(description="e.g. Joe blogs was a great employee, who turned up to work at least once a week. He exceeded my expectations when it came to doing nothing.")
    ] = None


class TemplateConfig(BaseModel):
    """Modelling ancv-specific template configuration.

    This controls ancv-specific settings such as the template and theme to use.
    It occurs as an additional, but optional field in the JSON resume.
    """

    template: str | None = None
    theme: str | None = None
    language: str | None = None
    ascii_only: bool | None = None
    dec31_as_year: bool | None = None


class Meta(BaseModel):
    """Modelling a JSON resume meta item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L477-L497
    """

    model_config = ConfigDict(extra="allow")

    canonical: t.Annotated[AnyUrl | None, Field(description="URL (as per RFC 3986) to latest version of this document")] = None
    version: t.Annotated[str | None, Field(description="A version field which follows semver - e.g. v1.0.0")] = None
    lastModified: t.Annotated[datetime | None, Field(description="Using ISO 8601 with YYYY-MM-DDThh:mm:ss")] = None
    config: t.Annotated[TemplateConfig | None, Field(alias="ancv", description="Template configuration to control display")] = None


class WorkItem(BaseModel):
    """Modelling a JSON resume work item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L100-L149
    """

    model_config = ConfigDict(extra="allow")

    name: t.Annotated[str | None, Field(description="e.g. Facebook")] = None
    location: t.Annotated[str | None, Field(description="e.g. Menlo Park, CA")] = None
    description: t.Annotated[str | None, Field(description="e.g. Social Media Company")] = None
    position: t.Annotated[str | None, Field(description="e.g. Software Engineer")] = None
    url: t.Annotated[AnyUrl | None, Field(description="e.g. http://facebook.example.com")] = None
    startDate: date | None = None
    endDate: date | None = None
    summary: t.Annotated[str | None, Field(description="Give an overview of your responsibilities at the company")] = None
    highlights: t.Annotated[list[str], Field(description="Specify multiple accomplishments")] = None


class VolunteerItem(BaseModel):
    """Modelling a JSON resume volunteer item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L150-L191
    """

    model_config = ConfigDict(extra="allow")

    organization: t.Annotated[str | None, Field(description="e.g. Facebook")] = None
    position: t.Annotated[str | None, Field(description="e.g. Software Engineer")] = None
    url: t.Annotated[AnyUrl | None, Field(description="e.g. http://facebook.example.com")] = None
    startDate: date | None = None
    endDate: date | None = None
    summary: t.Annotated[str, Field(description="Give an overview of your responsibilities at the company")] = None
    highlights: t.Annotated[list[str] | None, Field(description="Specify accomplishments and achievements")] = None


class EducationItem(BaseModel):
    """Modelling a JSON resume education item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L192-L237
    """

    model_config = ConfigDict(extra="allow")

    institution: t.Annotated[str | None, Field(description="e.g. Massachusetts Institute of Technology")] = None
    url: t.Annotated[AnyUrl | None, Field(description="e.g. http://facebook.example.com")] = None
    area: t.Annotated[str | None, Field(description="e.g. Arts")] = None
    studyType: t.Annotated[str | None, Field(description="e.g. Bachelor")] = None
    startDate: date | None = None
    endDate: date | None = None
    score: t.Annotated[str | None, Field(description="grade point average, e.g. 3.67/4.0")] = None
    courses: t.Annotated[list[str] | None, Field(description="List notable courses/subjects")] = None


class Award(BaseModel):
    """Modelling a JSON resume award item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L238-L263
    """

    model_config = ConfigDict(extra="allow")

    title: t.Annotated[str | None, Field(description="e.g. One of the 100 greatest minds of the century")] = None
    date: date | None = None
    awarder: t.Annotated[str | None, Field(description="e.g. Time Magazine")] = None
    summary: t.Annotated[str | None, Field(description="e.g. Received for my work with Quantum Physics")] = None


class Publication(BaseModel):
    """Modelling a JSON resume publication item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L293-L323
    """

    model_config = ConfigDict(extra="allow")

    name: t.Annotated[str | None, Field(description="e.g. The World Wide Web")] = None
    publisher: t.Annotated[str | None, Field(description="e.g. IEEE, Computer Magazine")] = None
    releaseDate: date | None = None
    url: t.Annotated[AnyUrl | None, Field(description="e.g. http://www.computer.org.example.com/csdl/mags/co/1996/10/rx069-abs.html")] = None
    summary: t.Annotated[str | None, Field(description="Short summary of publication. e.g. Discussion of the World Wide Web, HTTP, HTML.")] = None


class Project(BaseModel):
    """Modelling a JSON resume project item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L412-L476
    """

    model_config = ConfigDict(extra="allow")

    name: t.Annotated[str | None, Field(description="e.g. The World Wide Web")] = None
    description: t.Annotated[str | None, Field(description="Short summary of project. e.g. Collated works of 2017.")] = None
    highlights: t.Annotated[list[str] | None, Field(description="Specify multiple features")] = None
    keywords: t.Annotated[list[str] | None, Field(description="Specify special elements involved")] = None
    startDate: date | None = None
    endDate: date | None = None
    url: t.Annotated[AnyUrl | None, Field(description="e.g. http://www.computer.org/csdl/mags/co/1996/10/rx069-abs.html")] = None
    roles: t.Annotated[list[str] | None, Field(description="Specify your role on this project or in company")] = None
    entity: t.Annotated[str | None, Field(description="Specify the relevant company/entity affiliations e.g. 'greenpeace', 'corporationXYZ'")] = None
    type: t.Annotated[str | None, Field(description=" e.g. 'volunteering', 'presentation', 'talk', 'application', 'conference'")] = None


class ResumeSchema(BaseModel):
    """Modelling a complete JSON resume schema.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json
    """

    model_config = ConfigDict(extra="forbid")

    schema_: t.Annotated[AnyUrl | None, Field(alias="$schema", description="link to the version of the schema that can validate the resume")] = None
    basics: Basics | None = None
    work: list[WorkItem] | None = None
    volunteer: list[VolunteerItem] | None = None
    education: list[EducationItem] | None = None
    awards: t.Annotated[list[Award] | None, Field(description="Specify any awards you have received throughout your professional career")] = None
    certificates: t.Annotated[list[Certificate] | None, Field(description="Specify any certificates you have received throughout your professional career")] = None
    publications: t.Annotated[list[Publication] | None, Field(description="Specify your publications through your career")] = None
    skills: t.Annotated[list[Skill] | None, Field(description="List out your professional skill-set")] = None
    languages: t.Annotated[list[Language] | None, Field(description="List any other languages you speak")] = None
    interests: list[Interest] | None = None
    references: t.Annotated[list[Reference] | None, Field(description="List references you have received")] = None
    projects: t.Annotated[list[Project] | None, Field(description="Specify career projects")] = None
    meta: t.Annotated[Meta, Field(description="The schema version and any other tooling configuration lives here")] = Meta()


ResumeItem = t.Union[
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
]
