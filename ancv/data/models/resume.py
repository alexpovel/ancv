"""This module contains models for the JSON Resume standard.

See: https://jsonresume.org/schema/.
"""

import datetime
import typing as t

from pydantic import AnyUrl, BaseModel, ConfigDict, EmailStr, Field


class Location(BaseModel):
    """Modelling a JSON resume location item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L50-L73
    """

    model_config = ConfigDict(extra="allow")

    address: t.Annotated[
        t.Optional[str],
        Field(
            description="To add multiple address lines, use \n. For example, 1234 Glücklichkeit Straße\nHinterhaus 5. Etage li.",
        ),
    ] = None
    postalCode: t.Optional[str] = None
    city: t.Optional[str] = None
    countryCode: t.Annotated[
        t.Optional[str],
        Field(description="code as per ISO-3166-1 ALPHA-2, e.g. US, AU, IN"),
    ] = None
    region: t.Annotated[
        t.Optional[str],
        Field(
            description="The general region where you live. Can be a US state, or a province, for instance.",
        ),
    ] = None


class Profile(BaseModel):
    """Modelling a JSON resume profile item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L74-L99
    """

    model_config = ConfigDict(extra="allow")

    network: t.Annotated[
        t.Optional[str], Field(description="e.g. Facebook or Twitter")
    ] = None
    username: t.Annotated[
        t.Optional[str], Field(description="e.g. neutralthoughts")
    ] = None
    url: t.Annotated[
        t.Optional[AnyUrl],
        Field(description="e.g. http://twitter.example.com/neutralthoughts"),
    ] = None


class Basics(BaseModel):
    """Modelling a JSON resume basics item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L17-L49
    """

    model_config = ConfigDict(extra="allow")

    name: t.Optional[str] = None
    label: t.Annotated[t.Optional[str], Field(description="e.g. Web Developer")] = None
    image: t.Annotated[
        t.Optional[str],
        Field(description="URL (as per RFC 3986) to a image in JPEG or PNG format"),
    ] = None
    email: t.Annotated[
        t.Optional[EmailStr], Field(description="e.g. thomas@gmail.com")
    ] = None
    phone: t.Annotated[
        t.Optional[str],
        Field(
            description="Phone numbers are stored as strings so use any format you like, e.g. 712-117-2923",
        ),
    ] = None
    url: t.Annotated[
        t.Optional[AnyUrl],
        Field(
            description="URL (as per RFC 3986) to your website, e.g. personal homepage",
        ),
    ] = None
    summary: t.Annotated[
        t.Optional[str],
        Field(description="Write a short 2-3 sentence biography about yourself"),
    ] = None
    location: t.Optional[Location] = None
    profiles: t.Annotated[
        t.Optional[list[Profile]],
        Field(
            description="Specify any number of social networks that you participate in",
        ),
    ] = None


class Certificate(BaseModel):
    """Modelling a JSON resume certificate item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L264-L292
    """

    model_config = ConfigDict(extra="allow")

    name: t.Annotated[
        t.Optional[str], Field(description="e.g. Certified Kubernetes Administrator")
    ] = None
    date: t.Annotated[
        t.Optional[datetime.date], Field(description="e.g. 1989-06-12")
    ] = None
    url: t.Annotated[
        t.Optional[AnyUrl], Field(description="e.g. http://example.com")
    ] = None
    issuer: t.Annotated[t.Optional[str], Field(description="e.g. CNCF")] = None


class Skill(BaseModel):
    """Modelling a JSON resume skill item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L324-L351
    """

    model_config = ConfigDict(extra="allow")

    name: t.Annotated[t.Optional[str], Field(description="e.g. Web Development")] = None
    level: t.Annotated[t.Optional[str], Field(description="e.g. Master")] = None
    keywords: t.Annotated[
        t.Optional[list[str]],
        Field(description="List some keywords pertaining to this skill"),
    ] = None


class Language(BaseModel):
    """Modelling a JSON resume language item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L352-L370
    """

    model_config = ConfigDict(extra="allow")

    language: t.Annotated[
        t.Optional[str], Field(description="e.g. English, Spanish")
    ] = None
    fluency: t.Annotated[
        t.Optional[str], Field(description="e.g. Fluent, Beginner")
    ] = None


class Interest(BaseModel):
    """Modelling a JSON resume interest item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L371-L392
    """

    model_config = ConfigDict(extra="allow")

    name: t.Annotated[t.Optional[str], Field(description="e.g. Philosophy")] = None
    keywords: t.Optional[list[str]] = None


class Reference(BaseModel):
    """Modelling a JSON resume reference item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L393-L411
    """

    model_config = ConfigDict(extra="allow")

    name: t.Annotated[t.Optional[str], Field(description="e.g. Timothy Cook")] = None
    reference: t.Annotated[
        t.Optional[str],
        Field(
            description="e.g. Joe blogs was a great employee, who turned up to work at least once a week. He exceeded my expectations when it came to doing nothing.",
        ),
    ] = None


class TemplateConfig(BaseModel):
    """Modelling ancv-specific template configuration.

    This controls ancv-specific settings such as the template and theme to use.
    It occurs as an additional, but optional field in the JSON resume.
    """

    template: t.Optional[str] = None
    theme: t.Optional[str] = None
    language: t.Optional[str] = None
    ascii_only: t.Optional[bool] = None
    dec31_as_year: t.Optional[bool] = None


class Meta(BaseModel):
    """Modelling a JSON resume meta item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L477-L497
    """

    model_config = ConfigDict(extra="allow")

    canonical: t.Annotated[
        t.Optional[AnyUrl],
        Field(description="URL (as per RFC 3986) to latest version of this document"),
    ] = None
    version: t.Annotated[
        t.Optional[str],
        Field(description="A version field which follows semver - e.g. v1.0.0"),
    ] = None
    lastModified: t.Annotated[
        t.Optional[datetime.datetime],
        Field(description="Using ISO 8601 with YYYY-MM-DDThh:mm:ss"),
    ] = None
    config: t.Annotated[
        t.Optional[TemplateConfig],
        Field(
            alias="ancv",
            description="Template configuration to control display",
        ),
    ] = None


class WorkItem(BaseModel):
    """Modelling a JSON resume work item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L100-L149
    """

    model_config = ConfigDict(extra="allow")

    name: t.Annotated[t.Optional[str], Field(description="e.g. Facebook")] = None
    location: t.Annotated[t.Optional[str], Field(description="e.g. Menlo Park, CA")] = (
        None
    )
    description: t.Annotated[
        t.Optional[str], Field(description="e.g. Social Media Company")
    ] = None
    position: t.Annotated[
        t.Optional[str], Field(description="e.g. Software Engineer")
    ] = None
    url: t.Annotated[
        t.Optional[AnyUrl], Field(description="e.g. http://facebook.example.com")
    ] = None
    startDate: t.Optional[datetime.date] = None
    endDate: t.Optional[datetime.date] = None
    summary: t.Annotated[
        t.Optional[str],
        Field(description="Give an overview of your responsibilities at the company"),
    ] = None
    highlights: t.Annotated[
        t.Optional[list[str]], Field(description="Specify multiple accomplishments")
    ] = None


class VolunteerItem(BaseModel):
    """Modelling a JSON resume volunteer item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L150-L191
    """

    model_config = ConfigDict(extra="allow")

    organization: t.Annotated[t.Optional[str], Field(description="e.g. Facebook")] = (
        None
    )
    position: t.Annotated[
        t.Optional[str], Field(description="e.g. Software Engineer")
    ] = None
    url: t.Annotated[
        t.Optional[AnyUrl], Field(description="e.g. http://facebook.example.com")
    ] = None
    startDate: t.Optional[datetime.date] = None
    endDate: t.Optional[datetime.date] = None
    summary: t.Annotated[
        t.Optional[str],
        Field(description="Give an overview of your responsibilities at the company"),
    ] = None
    highlights: t.Annotated[
        t.Optional[list[str]],
        Field(description="Specify accomplishments and achievements"),
    ] = None


class EducationItem(BaseModel):
    """Modelling a JSON resume education item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L192-L237
    """

    model_config = ConfigDict(extra="allow")

    institution: t.Annotated[
        t.Optional[str], Field(description="e.g. Massachusetts Institute of Technology")
    ] = None
    url: t.Annotated[
        t.Optional[AnyUrl], Field(description="e.g. http://facebook.example.com")
    ] = None
    area: t.Annotated[t.Optional[str], Field(description="e.g. Arts")] = None
    studyType: t.Annotated[t.Optional[str], Field(description="e.g. Bachelor")] = None
    startDate: t.Optional[datetime.date] = None
    endDate: t.Optional[datetime.date] = None
    score: t.Annotated[
        t.Optional[str], Field(description="grade point average, e.g. 3.67/4.0")
    ] = None
    courses: t.Annotated[
        t.Optional[list[str]], Field(description="List notable courses/subjects")
    ] = None


class Award(BaseModel):
    """Modelling a JSON resume award item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L238-L263
    """

    model_config = ConfigDict(extra="allow")

    title: t.Annotated[
        t.Optional[str],
        Field(description="e.g. One of the 100 greatest minds of the century"),
    ] = None
    date: datetime.date | None = None
    awarder: t.Annotated[t.Optional[str], Field(description="e.g. Time Magazine")] = (
        None
    )
    summary: t.Annotated[
        t.Optional[str],
        Field(description="e.g. Received for my work with Quantum Physics"),
    ] = None


class Publication(BaseModel):
    """Modelling a JSON resume publication item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L293-L323
    """

    model_config = ConfigDict(extra="allow")

    name: t.Annotated[t.Optional[str], Field(description="e.g. The World Wide Web")] = (
        None
    )
    publisher: t.Annotated[
        t.Optional[str], Field(description="e.g. IEEE, Computer Magazine")
    ] = None
    releaseDate: t.Optional[datetime.date] = None
    url: t.Annotated[
        t.Optional[AnyUrl],
        Field(
            description="e.g. http://www.computer.org.example.com/csdl/mags/co/1996/10/rx069-abs.html",
        ),
    ] = None
    summary: t.Annotated[
        t.Optional[str],
        Field(
            description="Short summary of publication. e.g. Discussion of the World Wide Web, HTTP, HTML.",
        ),
    ] = None


class Project(BaseModel):
    """Modelling a JSON resume project item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L412-L476
    """

    model_config = ConfigDict(extra="allow")

    name: t.Annotated[t.Optional[str], Field(description="e.g. The World Wide Web")] = (
        None
    )
    description: t.Annotated[
        t.Optional[str],
        Field(description="Short summary of project. e.g. Collated works of 2017."),
    ] = None
    highlights: t.Annotated[
        t.Optional[list[str]], Field(description="Specify multiple features")
    ] = None
    keywords: t.Annotated[
        t.Optional[list[str]], Field(description="Specify special elements involved")
    ] = None
    startDate: t.Optional[datetime.date] = None
    endDate: t.Optional[datetime.date] = None
    url: t.Annotated[
        t.Optional[AnyUrl],
        Field(
            description="e.g. http://www.computer.org/csdl/mags/co/1996/10/rx069-abs.html",
        ),
    ] = None
    roles: t.Annotated[
        t.Optional[list[str]],
        Field(description="Specify your role on this project or in company"),
    ] = None
    entity: t.Annotated[
        t.Optional[str],
        Field(
            description="Specify the relevant company/entity affiliations e.g. 'greenpeace', 'corporationXYZ'",
        ),
    ] = None
    type: t.Annotated[
        t.Optional[str],
        Field(
            description=" e.g. 'volunteering', 'presentation', 'talk', 'application', 'conference'",
        ),
    ] = None


class ResumeSchema(BaseModel):
    """Modelling a complete JSON resume schema.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json
    """

    model_config = ConfigDict(extra="forbid")

    schema_: t.Annotated[
        t.Optional[AnyUrl],
        Field(
            alias="$schema",
            description="link to the version of the schema that can validate the resume",
        ),
    ] = None
    basics: t.Optional[Basics] = None
    work: t.Optional[list[WorkItem]] = None
    volunteer: t.Optional[list[VolunteerItem]] = None
    education: t.Optional[list[EducationItem]] = None
    awards: t.Annotated[
        t.Optional[list[Award]],
        Field(
            description="Specify any awards you have received throughout your professional career",
        ),
    ] = None
    certificates: t.Annotated[
        t.Optional[list[Certificate]],
        Field(
            description="Specify any certificates you have received throughout your professional career",
        ),
    ] = None
    publications: t.Annotated[
        t.Optional[list[Publication]],
        Field(description="Specify your publications through your career"),
    ] = None
    skills: t.Annotated[
        t.Optional[list[Skill]],
        Field(description="List out your professional skill-set"),
    ] = None
    languages: t.Annotated[
        t.Optional[list[Language]],
        Field(description="List any other languages you speak"),
    ] = None
    interests: t.Optional[list[Interest]] = None
    references: t.Annotated[
        t.Optional[list[Reference]],
        Field(description="List references you have received"),
    ] = None
    projects: t.Annotated[
        t.Optional[list[Project]], Field(description="Specify career projects")
    ] = None
    meta: t.Annotated[
        Meta,
        Field(
            description="The schema version and any other tooling configuration lives here",
        ),
    ] = Meta()


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
