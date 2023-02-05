from pydantic import BaseModel


class Translation(BaseModel):
    """Modelling a translation for a resume section or field.

    These are simple, hard-coded translations. Special grammatical cases, singular vs.
    plural, etc. are not handled and need to be handled identically across all languages
    (which might end up not working...).
    """

    grade: str
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
    present: str


TRANSLATIONS = {
    "en": Translation(
        grade="Grade",
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
        present="present",
    ),
    "de": Translation(
        grade="Note",
        awarded_by="verliehen von",
        issued_by="ausgestellt von",
        roles="Rollen",
        skills="Fähigkeiten",
        work="Erfahrung",
        volunteer="Ehrenamtliche Arbeit",
        education="Ausbildung",
        awards="Auszeichnungen",
        certificates="Zertifikate",
        publications="Publikationen",
        languages="Sprachen",
        references="Referenzen",
        interests="Interessen",
        projects="Projekte",
        present="heute",
    ),
    "es": Translation(
        grade="Nota",
        awarded_by="otorgado por",
        issued_by="emitido por",
        roles="Funciones",
        skills="Conocimientos y aptitudes",
        work="Experiencia",
        volunteer="Voluntariado",
        education="Educación",
        awards="Premios",
        certificates="Certificaciones",
        publications="Publicaciones",
        languages="Idiomas",
        references="Referencias",
        interests="Intereses",
        projects="Proyectos",
        present="actualidad",
    ),
    "fr": Translation(
        grade="Note",
        awarded_by="décerné par",
        issued_by="délivré par",
        roles="Rôles",
        skills="Compétences",
        work="Expérience",
        volunteer="Bénévolat",
        education="Formation",
        awards="Distinctions",
        certificates="Certifications",
        publications="Publications",
        languages="Langues",
        references="Références",
        interests="Intérêts",
        projects="Projets",
        present="aujourd'hui",
    ),
}
