"""This module contains models for the JSON Resume standard.

See: https://jsonresume.org/schema/.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional, Union

from pydantic import AnyUrl, BaseModel, EmailStr, Extra, Field


class Location(BaseModel):
    """Modelling a JSON resume location item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L50-L73"""

    class Config:
        extra = Extra.allow

    address: Optional[str] = Field(
        None,
        description="To add multiple address lines, use \n. For example, 1234 Glücklichkeit Straße\nHinterhaus 5. Etage li.",
    )
    postalCode: Optional[str] = None
    city: Optional[str] = None
    countryCode: Optional[str] = Field(
        None, description="code as per ISO-3166-1 ALPHA-2, e.g. US, AU, IN"
    )
    region: Optional[str] = Field(
        None,
        description="The general region where you live. Can be a US state, or a province, for instance.",
    )


class Profile(BaseModel):
    """Modelling a JSON resume profile item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L74-L99"""

    class Config:
        extra = Extra.allow

    network: Optional[str] = Field(None, description="e.g. Facebook or Twitter")
    username: Optional[str] = Field(None, description="e.g. neutralthoughts")
    url: Optional[AnyUrl] = Field(
        None, description="e.g. http://twitter.example.com/neutralthoughts"
    )


class Basics(BaseModel):
    """Modelling a JSON resume basics item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L17-L49"""

    class Config:
        extra = Extra.allow

    name: Optional[str] = None
    label: Optional[str] = Field(None, description="e.g. Web Developer")
    image: Optional[str] = Field(
        None, description="URL (as per RFC 3986) to a image in JPEG or PNG format"
    )
    email: Optional[EmailStr] = Field(None, description="e.g. thomas@gmail.com")
    phone: Optional[str] = Field(
        None,
        description="Phone numbers are stored as strings so use any format you like, e.g. 712-117-2923",
    )
    url: Optional[AnyUrl] = Field(
        None,
        description="URL (as per RFC 3986) to your website, e.g. personal homepage",
    )
    summary: Optional[str] = Field(
        None, description="Write a short 2-3 sentence biography about yourself"
    )
    location: Optional[Location] = None
    profiles: Optional[list[Profile]] = Field(
        None,
        description="Specify any number of social networks that you participate in",
    )


class Certificate(BaseModel):
    """Modelling a JSON resume certificate item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L264-L292"""

    class Config:
        extra = Extra.allow

    name: Optional[str] = Field(
        None, description="e.g. Certified Kubernetes Administrator"
    )
    date: Optional[date] = Field(None, description="e.g. 1989-06-12")
    url: Optional[AnyUrl] = Field(None, description="e.g. http://example.com")
    issuer: Optional[str] = Field(None, description="e.g. CNCF")


class Skill(BaseModel):
    """Modelling a JSON resume skill item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L324-L351"""

    class Config:
        extra = Extra.allow

    name: Optional[str] = Field(None, description="e.g. Web Development")
    level: Optional[str] = Field(None, description="e.g. Master")
    keywords: Optional[list[str]] = Field(
        None, description="List some keywords pertaining to this skill"
    )


class Language(BaseModel):
    """Modelling a JSON resume language item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L352-L370"""

    class Config:
        extra = Extra.allow

    language: Optional[str] = Field(None, description="e.g. English, Spanish")
    fluency: Optional[str] = Field(None, description="e.g. Fluent, Beginner")


class Interest(BaseModel):
    """Modelling a JSON resume interest item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L371-L392"""

    class Config:
        extra = Extra.allow

    name: Optional[str] = Field(None, description="e.g. Philosophy")
    keywords: Optional[list[str]] = None


class Reference(BaseModel):
    """Modelling a JSON resume reference item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L393-L411"""

    class Config:
        extra = Extra.allow

    name: Optional[str] = Field(None, description="e.g. Timothy Cook")
    reference: Optional[str] = Field(
        None,
        description="e.g. Joe blogs was a great employee, who turned up to work at least once a week. He exceeded my expectations when it came to doing nothing.",
    )


class TemplateConfig(BaseModel):
    """Modelling ancv-specific template configuration.

    This controls ancv-specific settings such as the template and theme to use.
    It occurs as an additional, but optional field in the JSON resume.
    """

    template: Optional[str]
    theme: Optional[str]
    language: Optional[str]
    ascii_only: Optional[bool]
    dec31_as_year: Optional[bool]


class Meta(BaseModel):
    """Modelling a JSON resume meta item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L477-L497"""

    class Config:
        extra = Extra.allow

    canonical: Optional[AnyUrl] = Field(
        None, description="URL (as per RFC 3986) to latest version of this document"
    )
    version: Optional[str] = Field(
        None, description="A version field which follows semver - e.g. v1.0.0"
    )
    lastModified: Optional[datetime] = Field(
        None, description="Using ISO 8601 with YYYY-MM-DDThh:mm:ss"
    )
    config: Optional[TemplateConfig] = Field(
        None,
        alias="ancv",
        description="Template configuration to control display",
    )


class WorkItem(BaseModel):
    """Modelling a JSON resume work item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L100-L149"""

    class Config:
        extra = Extra.allow

    name: Optional[str] = Field(None, description="e.g. Facebook")
    location: Optional[str] = Field(None, description="e.g. Menlo Park, CA")
    description: Optional[str] = Field(None, description="e.g. Social Media Company")
    position: Optional[str] = Field(None, description="e.g. Software Engineer")
    url: Optional[AnyUrl] = Field(None, description="e.g. http://facebook.example.com")
    startDate: Optional[date] = None
    endDate: Optional[date] = None
    summary: Optional[str] = Field(
        None, description="Give an overview of your responsibilities at the company"
    )
    highlights: Optional[list[str]] = Field(
        None, description="Specify multiple accomplishments"
    )


class VolunteerItem(BaseModel):
    """Modelling a JSON resume volunteer item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L150-L191"""

    class Config:
        extra = Extra.allow

    organization: Optional[str] = Field(None, description="e.g. Facebook")
    position: Optional[str] = Field(None, description="e.g. Software Engineer")
    url: Optional[AnyUrl] = Field(None, description="e.g. http://facebook.example.com")
    startDate: Optional[date] = None
    endDate: Optional[date] = None
    summary: Optional[str] = Field(
        None, description="Give an overview of your responsibilities at the company"
    )
    highlights: Optional[list[str]] = Field(
        None, description="Specify accomplishments and achievements"
    )


class EducationItem(BaseModel):
    """Modelling a JSON resume education item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L192-L237"""

    class Config:
        extra = Extra.allow

    institution: Optional[str] = Field(
        None, description="e.g. Massachusetts Institute of Technology"
    )
    url: Optional[AnyUrl] = Field(None, description="e.g. http://facebook.example.com")
    area: Optional[str] = Field(None, description="e.g. Arts")
    studyType: Optional[str] = Field(None, description="e.g. Bachelor")
    startDate: Optional[date] = None
    endDate: Optional[date] = None
    score: Optional[str] = Field(None, description="grade point average, e.g. 3.67/4.0")
    courses: Optional[list[str]] = Field(
        None, description="List notable courses/subjects"
    )


class Award(BaseModel):
    """Modelling a JSON resume award item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L238-L263"""

    class Config:
        extra = Extra.allow

    title: Optional[str] = Field(
        None, description="e.g. One of the 100 greatest minds of the century"
    )
    date: Optional[date] = None
    awarder: Optional[str] = Field(None, description="e.g. Time Magazine")
    summary: Optional[str] = Field(
        None, description="e.g. Received for my work with Quantum Physics"
    )


class Publication(BaseModel):
    """Modelling a JSON resume publication item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L293-L323"""

    class Config:
        extra = Extra.allow

    name: Optional[str] = Field(None, description="e.g. The World Wide Web")
    publisher: Optional[str] = Field(None, description="e.g. IEEE, Computer Magazine")
    releaseDate: Optional[date] = None
    url: Optional[AnyUrl] = Field(
        None,
        description="e.g. http://www.computer.org.example.com/csdl/mags/co/1996/10/rx069-abs.html",
    )
    summary: Optional[str] = Field(
        None,
        description="Short summary of publication. e.g. Discussion of the World Wide Web, HTTP, HTML.",
    )


class Project(BaseModel):
    """Modelling a JSON resume project item.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json#L412-L476"""

    class Config:
        extra = Extra.allow

    name: Optional[str] = Field(None, description="e.g. The World Wide Web")
    description: Optional[str] = Field(
        None, description="Short summary of project. e.g. Collated works of 2017."
    )
    highlights: Optional[list[str]] = Field(
        None, description="Specify multiple features"
    )
    keywords: Optional[list[str]] = Field(
        None, description="Specify special elements involved"
    )
    startDate: Optional[date] = None
    endDate: Optional[date] = None
    url: Optional[AnyUrl] = Field(
        None,
        description="e.g. http://www.computer.org/csdl/mags/co/1996/10/rx069-abs.html",
    )
    roles: Optional[list[str]] = Field(
        None, description="Specify your role on this project or in company"
    )
    entity: Optional[str] = Field(
        None,
        description="Specify the relevant company/entity affiliations e.g. 'greenpeace', 'corporationXYZ'",
    )
    type: Optional[str] = Field(
        None,
        description=" e.g. 'volunteering', 'presentation', 'talk', 'application', 'conference'",
    )


class ResumeSchema(BaseModel):
    """Modelling a complete JSON resume schema.

    See: https://github.com/alexpovel/resume-schema/blob/6e3244639cebfa89e66ee60d47c665a96e01a811/schema.json"""

    class Config:
        extra = Extra.forbid

    schema_: Optional[AnyUrl] = Field(
        None,
        alias="$schema",
        description="link to the version of the schema that can validate the resume",
    )
    basics: Optional[Basics] = None
    work: Optional[list[WorkItem]] = None
    volunteer: Optional[list[VolunteerItem]] = None
    education: Optional[list[EducationItem]] = None
    awards: Optional[list[Award]] = Field(
        None,
        description="Specify any awards you have received throughout your professional career",
    )
    certificates: Optional[list[Certificate]] = Field(
        None,
        description="Specify any certificates you have received throughout your professional career",
    )
    publications: Optional[list[Publication]] = Field(
        None, description="Specify your publications through your career"
    )
    skills: Optional[list[Skill]] = Field(
        None, description="List out your professional skill-set"
    )
    languages: Optional[list[Language]] = Field(
        None, description="List any other languages you speak"
    )
    interests: Optional[list[Interest]] = None
    references: Optional[list[Reference]] = Field(
        None, description="List references you have received"
    )
    projects: Optional[list[Project]] = Field(
        None, description="Specify career projects"
    )
    meta: Meta = Field(
        Meta(),
        description="The schema version and any other tooling configuration lives here",
    )


ResumeItem = Union[
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
