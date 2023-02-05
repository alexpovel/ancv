class ResumeLookupError(LookupError):
    """Raised when a user's resume cannot be found, is malformed, ..."""

    pass


class ResumeConfigError(ValueError):
    """Raised when a resume config is invalid, e.g. missing required fields."""

    pass
