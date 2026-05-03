# Contributing

## Environment setup

Use the project Python version from [`.python-version`](./.python-version) and
[`uv`](https://docs.astral.sh/uv/) directly:

```bash
make sync
```

Common targets:

```bash
make lint
make format-check
make typecheck
make test
make check
make build
make build-image
```

Schema/model regeneration:

```bash
make make-github.py
make make-resume.py
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
