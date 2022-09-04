# Contributing

## Environment setup

Sadly, the setup cannot be automated arbitrarily (say, using a `make init` target).
Installing `poetry` requires system packages (`python3`, `pip`, `curl`) that cannot be easily installed on the user's behalf in a distribution-independent way.
Further, inserting `poetry` in one's `$PATH` is best done manually and consciously (environments, user desires etc. differ too much).

1. [Install `poetry`](https://python-poetry.org/docs/master/#installing-with-the-official-installer).

   If you're having trouble with version mismatch, check which version the `poetry` installation currently uses in the [CI](https://github.com/alexpovel/ancv/actions).
2. Run `poetry install` in the root directly (where the [`pyproject.toml`](./pyproject.toml) is located).

   `poetry` will throw an error here if your Python version isn't supported by the project.
   If that is the case, look into using [`pyenv`](https://github.com/pyenv/pyenv), which will use the version specified in [`.python-version`](.python-version), guaranteeing a version match.
3. Enter into the created environment with `poetry shell`.

   *Alternatively*, prepend all commands pertaining to the repository with `poetry run`, like `poetry run python -m ancv`.
4. Set up `git` hooks provided by [`pre-commit`](https://pre-commit.com/#intro) (already installed through `poetry`): `make hooks`.

   For this to work, you will have to have `make` installed (Windows alternatives exist).

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
