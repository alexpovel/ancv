# Contributing

## Environment setup

1. [Install `poetry`](https://python-poetry.org/docs/master/#installing-with-the-official-installer).

   If you're having trouble with version mismatch, check which version the `poetry` installation currently uses in the [CI](https://github.com/alexpovel/ancv/actions).
2. Run `poetry install` in the root directly (where the `pyproject.toml` is located).
3. Enter into the created environment with `poetry shell`, alternatively prepend all commands pertaining to the repository with `poetry run`, like `poetry run python -m ancv`.
4. Set up `git` hooks provided by [`pre-commit`](https://pre-commit.com/#intro) (already installed through `poetry`): `make hooks`.

   For this to work, you will have to have `make` installed (Windows alternatives exist).
