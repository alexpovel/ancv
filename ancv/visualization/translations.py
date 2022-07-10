from pydantic import BaseModel


class Translation(BaseModel):
    score: str
    awarded_by: str
    issued_by: str
    roles: str
    skills: str
    work: str
    volunteer: str
    education: str
    awards: str
    certificates: str
    publications: str
    languages: str
    references: str
    interests: str
    projects: str


TRANSLATIONS = {
    "en": Translation(
        score="Score",
        awarded_by="awarded by",
        issued_by="issued by",
        roles="Roles",
        skills="Skills",
        work="Experience",
        volunteer="Volunteer",
        education="Education",
        awards="Awards",
        certificates="Certificates",
        publications="Publications",
        languages="Languages",
        references="References",
        interests="Interests",
        projects="Projects",
    ),
    "de": Translation(
        score="Note",
        awarded_by="verliehen von",
        issued_by="ausgestellt von",
        roles="Rollen",
        skills="Fähigkeiten",
        work="Erfahrung",
        volunteer="Ehrenamtliche Arbeit",
        education="Bildung",
        awards="Auszeichnungen",
        certificates="Zertifikate",
        publications="Publikationen",
        languages="Sprachen",
        references="Referenzen",
        interests="Interessen",
        projects="Projekte",
    ),
}
