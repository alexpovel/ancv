# Contributing

## Environment setup

[![Built with Devbox](https://jetpack.io/img/devbox/shield_moon.svg)](https://jetpack.io/devbox/docs/contributor-quickstart/)

Use devbox to set up a development environment.
Refer to [the available `script`s](devbox.json) to see what's possible.
Generally, even when running in a `devbox shell`, running `uv` is necessary:

- devbox sets up what used to be system-wide packages (Python, uv, ...) deterministically and automatically
- within the devbox virtual environment, we still manage and use a Python virtual environment through `uv` commands

That way, we get the normal Python package management for normal Python packages (`ruff`, `pytest`, ...), and devbox for the overarching rest.

Lastly, for bonus points, set up pre-commit hooks:

```bash
devbox run install-hooks
```

## Creating components

### Templates

To create a new template, inherit from [`Template`](./ancv/visualization/templates.py) and simply fulfills its interface:
It needs a [`__rich_console__`](https://rich.readthedocs.io/en/stable/protocol.html#console-render) method yielding all elements that will eventually make up the output document.
That's it!
The implementation is entirely up to you.
You can use [tables](https://rich.readthedocs.io/en/stable/tables.html), [panels](https://rich.readthedocs.io/en/stable/panel.html), [columns](https://rich.readthedocs.io/en/stable/columns.html) and most else [`rich`](https://github.com/Textualize/rich) has on offer.

`mypy` checks (`make typecheck`) will help getting the implementation right.
However, note that this method cannot (currently) check whether *all sections* were implemented: for example, *Volunteering* could simply have been forgotten, but the code would run all checks would pass.
Further, lots of manual and visual testing will be necessary.

### Translations

Simply add your translation [here](./ancv/visualization/translations.py).

### Themes

Simply add your theme [here](./ancv/visualization/themes.py).
