.PHONY: sync lint format format-check typecheck test check build build-image make-github.py make-resume.py

IMAGE ?= ancv/ancv:dev

sync:
	uv sync --frozen

lint:
	uv run --frozen ruff check --verbose .

format:
	uv run --frozen ruff format .

format-check:
	uv run --frozen ruff format --check --diff

typecheck:
	uv run --frozen mypy -v -p ancv

test:
	uv run --frozen pytest -vv --cov=ancv --cov-report=html --cov-report=term --cov-report=xml

check: lint format-check typecheck test

build:
	uv build

build-image:
	docker build --progress=plain --tag $(IMAGE) .

make-github.py:
	uv run --frozen datamodel-codegen --url "https://raw.githubusercontent.com/github/rest-api-description/main/descriptions-next/api.github.com/dereferenced/api.github.com.deref.json" --encoding utf-8 --input-file-type openapi --openapi-scopes paths --output ancv/data/models/github.py

make-resume.py:
	uv run --frozen datamodel-codegen --url "https://raw.githubusercontent.com/jsonresume/resume-schema/master/schema.json" --encoding utf-8 --input-file-type jsonschema --output ancv/data/models/resume.py
