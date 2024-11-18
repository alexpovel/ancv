"""Render JSON resumes to rich ANSI text for terminal output.

Comes with a server serving either an API or a single file, and a CLI to render files
locally.
"""

from pathlib import Path
from typing import Optional

import typer

app = typer.Typer(no_args_is_help=True, help=__doc__)
server_app = typer.Typer(no_args_is_help=True, help="Interacts with the web server.")

app.add_typer(server_app, name="serve")


@server_app.command()
def api(
    host: str = typer.Option("0.0.0.0", help="Hostname to bind to."),
    port: int = typer.Option(8080, help="Port to bind to."),
    path: Optional[str] = typer.Option(
        None, help="File system path for an HTTP server UNIX domain socket."
    ),
) -> None:
    """Starts the web server and serves the API."""

    import os

    from ancv.reflection import METADATA
    from ancv.web.server import APIHandler, ServerContext

    context = ServerContext(host=host, port=port, path=path)
    api = APIHandler(
        # https://docs.github.com/en/rest/overview/resources-in-the-rest-api#user-agent-required :
        requester=os.environ.get("GH_REQUESTER", METADATA.name),
        # Not specifying a token works just as well, but has a much lower request
        # ceiling:
        token=os.environ.get("GH_TOKEN"),
        terminal_landing_page=os.environ.get(
            "HOMEPAGE",
            str(METADATA.project_urls.get("Homepage", "No homepage set")),
        ),
        # When visiting this endpoint in a browser, we want to redirect to the homepage.
        # That page cannot be this same path under the same hostname again, else we get
        # a loop.
        browser_landing_page=os.environ.get(
            "LANDING_PAGE",
            str(METADATA.project_urls.get("Homepage", "https://github.com/")),
        ),
    )
    api.run(context)


@server_app.command()
def file(
    file: Path = typer.Argument(Path("resume.json")),
    host: str = typer.Option("0.0.0.0", help="Hostname to bind to."),
    port: int = typer.Option(8080, help="Port to bind to."),
    path: Optional[str] = typer.Option(
        None, help="File system path for an HTTP server UNIX domain socket."
    ),
) -> None:
    """Starts the web server and serves a single, rendered resume file."""

    from ancv.web.server import FileHandler, ServerContext

    context = ServerContext(host=host, port=port, path=path)
    FileHandler(file).run(context)


@server_app.command(no_args_is_help=True)
def web(
    destination: str = typer.Argument(
        ..., help="HTTP/HTTPS URL of the JSON resume file to serve."
    ),
    refresh: int = typer.Option(
        3600, help="Refresh interval in seconds for fetching updates from the URL."
    ),
    port: int = typer.Option(8080, help="Port to bind to."),
    host: str = typer.Option("0.0.0.0", help="Hostname to bind to."),
    path: Optional[str] = typer.Option(
        None, help="File system path for an HTTP server UNIX domain socket."
    ),
) -> None:
    """Starts a web server that serves a JSON resume from a URL with periodic refresh.

    The server will fetch and render the resume from the provided URL, caching it for the specified
    refresh interval. This is useful for serving resumes hosted on external services.
    """

    from ancv.web.server import WebHandler, ServerContext
    from datetime import timedelta

    context = ServerContext(host=host, port=port, path=path)
    WebHandler(destination, refresh_interval=timedelta(seconds=refresh)).run(context)


@app.command()
def render(
    path: Path = typer.Argument(
        Path("resume.json"),
        help="File path to the JSON resume file.",
    ),
) -> None:
    """Locally renders the JSON resume at the given file path."""

    from ancv.visualization.templates import Template

    template = Template.from_file(path)
    output = template.render()
    print(output)
    return None


@app.command()
def validate(
    path: Path = typer.Argument(
        Path("resume.json"),
        help="File path to the JSON resume file.",
    ),
) -> None:
    """Checks the validity of the given JSON resume without rendering."""

    from pydantic import ValidationError

    from ancv.exceptions import ResumeConfigError
    from ancv.visualization.templates import Template

    try:
        Template.from_file(path)
    except (ValidationError, ResumeConfigError) as e:
        print(str(e))
        raise typer.Exit(code=1)
    else:
        print("Pass!")


@app.command()
def version() -> None:
    """Prints the application version."""

    from ancv.reflection import METADATA

    print(f"ancv {METADATA.version}")


@app.command()
def list() -> None:
    """Lists all available components (templates, themes and translations)."""

    # This is pretty raw, but it works. Could make it prettier using more of `rich`.
    from rich import print
    from rich.tree import Tree

    from ancv.visualization.templates import Template
    from ancv.visualization.themes import THEMES
    from ancv.visualization.translations import TRANSLATIONS

    tree = Tree("Components")

    template_tree = Tree("Templates")
    for template in Template.subclasses().keys():
        template_tree.add(template)
    tree.add(template_tree)

    theme_tree = Tree("Themes")
    for theme in THEMES:
        theme_tree.add(theme)
    tree.add(theme_tree)

    translation_tree = Tree("Translations")
    for translation in TRANSLATIONS:
        translation_tree.add(translation)
    tree.add(translation_tree)

    print(tree)


@app.command()
def generate_schema() -> None:
    """Generates and prints the current JSON schema.

    ATTENTION: This schema is defined manually, independently of the actual models
    contained within this package. As such, the two *might* end up out of sync. This
    approach was chosen as a temporary solution, since syncing the JSON Schema and the
    pydantic models is a lot of work with a lot of tiny blockers.
    """

    import json
    import typing as t

    from ancv.reflection import METADATA
    from ancv.visualization.templates import Template
    from ancv.visualization.themes import THEMES
    from ancv.visualization.translations import TRANSLATIONS

    schema: dict[str, t.Any] = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "allOf": [
            {
                "$ref": "https://raw.githubusercontent.com/jsonresume/resume-schema/v1.0.0/schema.json"
            },
            {
                "type": "object",
                "properties": {
                    "meta": {
                        "allOf": [
                            {
                                "$ref": "https://raw.githubusercontent.com/jsonresume/resume-schema/v1.0.0/schema.json#/properties/meta"
                            }
                        ],
                        "properties": {
                            METADATA.name: {
                                "type": "object",
                                "description": f"{METADATA.name}-specific ({METADATA.project_urls.get("Homepage")}) properties",
                                "properties": {
                                    "template": {
                                        "type": "string",
                                        "description": "The template (ordering, alignment, positioning, ...) to use",
                                        "enum": sorted(Template.subclasses().keys()),
                                    },
                                    "theme": {
                                        "type": "string",
                                        "description": "The theme (colors, emphasis, ...) to use",
                                        "enum": sorted(THEMES.keys()),
                                    },
                                    "language": {
                                        "type": "string",
                                        "description": "The language aka translation (for section titles like 'Education' etc.) to use",
                                        "enum": sorted(TRANSLATIONS.keys()),
                                    },
                                    "ascii_only": {
                                        "type": "boolean",
                                        "description": "Whether to only use ASCII characters in the template (you are responsible for not using non-ASCII characters in your resume)",
                                    },
                                    "dec31_as_year": {
                                        "type": "boolean",
                                        "description": "Whether to display dates of 'December 31st of some year' as that year only, without month or day info",
                                    },
                                },
                            }
                        },
                    }
                },
            },
        ],
    }

    print(json.dumps(schema, indent=4))


@app.callback()
def main(
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Turn on verbose logging output."
    ),
) -> None:
    """CLI-wide, global options.

    https://typer.tiangolo.com/tutorial/commands/callback/
    """

    import logging

    import structlog
    from structlog.processors import JSONRenderer, TimeStamper, add_log_level

    from ancv.reflection import METADATA

    structlog.configure(  # This is global state
        processors=[  # https://www.structlog.org/en/stable/api.html#procs
            TimeStamper(fmt="iso", utc=True, key="ts"),
            add_log_level,
            JSONRenderer(sort_keys=True),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.DEBUG if verbose else logging.INFO
        ),
    )

    log = structlog.get_logger()
    log.debug("Got app metadata.", metadata=METADATA.model_dump())


if __name__ == "__main__":
    app()
