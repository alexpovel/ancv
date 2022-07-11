import json
import sys
from typing import TextIO

import click
from pydantic import ValidationError

import ancv.web.server
from ancv.data.models.resume import ResumeSchema
from ancv.visualization.templates import Template


@click.group(context_settings={"show_default": True})
def cli() -> None:
    pass


@cli.command(help="Starts the web server.")
@click.option("--host", default="0.0.0.0", help="The hostname to bind to.")
@click.option("--port", default=8080, help="The port to bind to.")
@click.option(
    "--path",
    help="File system path for an HTTP server Unix domain socket.",
)
def serve(host: str, port: int, path: str) -> None:
    ancv.web.server.run(host=host, port=port, path=path)


@cli.command(help="Locally renders the JSON resume at the given file path.")
@click.argument("file", type=click.File())
def render(file: TextIO) -> None:
    contents = json.loads(file.read())
    resume = ResumeSchema(**contents)
    template = Template.from_model_config(resume)
    output = template.render()
    print(output)
    return None


@cli.command(help="Checks the validity of the given JSON resume without rendering.")
@click.argument("file", type=click.File())
def validate(file: TextIO) -> None:
    contents = json.loads(file.read())
    ec = 0
    try:
        ResumeSchema(**contents)
    except ValidationError as e:
        print(str(e))
        ec = 1
    else:
        print("Pass!")
    sys.exit(ec)


if __name__ == "__main__":
    cli()
