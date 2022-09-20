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
        homepage=os.environ.get("HOMEPAGE", METADATA.home_page or "NO HOMEPAGE SET"),
        # When visiting this endpoint in a browser, we want to redirect to the homepage.
        # That page cannot be this same path under the same hostname again, else we get
        # a loop.
        landing_page=os.environ.get(
            "LANDING_PAGE",
            METADATA.project_url[0] if METADATA.project_url else "https://github.com/",
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


@app.command()
def render(
    path: Path = typer.Argument(
        Path("resume.json"),
        help="File path to the JSON resume file.",
    )
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
    )
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


@app.callback()
def main(
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Turn on verbose logging output."
    )
) -> None:
    """CLI-wide, global options.

    https://typer.tiangolo.com/tutorial/commands/callback/
    """

    import logging
    import os

    import structlog
    from structlog.processors import JSONRenderer, TimeStamper, add_log_level

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
    log.debug(f"Starting up with environment: {os.environ}")


if __name__ == "__main__":
    app()
