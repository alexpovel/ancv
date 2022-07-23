FROM python:3.10

ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

# Don't buffer `stdout`:
ENV PYTHONUNBUFFERED=1
# Don't create `.pyc` files:
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update \
    && apt-get install --no-install-recommends --yes \
    curl

RUN curl -sSL https://install.python-poetry.org | python - --version 1.2.0b3

# README.md is junk but poetry requests it and fails otherwise.
COPY pyproject.toml poetry.lock README.md ./
COPY ancv/ ./ancv/

# Since this is an isolated image *just* for this project, we can install everything
# globally, killing one virtual environment a time... See also:
# https://python-poetry.org/docs/configuration/#virtualenvscreate .
RUN poetry config virtualenvs.create false && poetry install --no-dev

EXPOSE 8080
CMD [ "python", "-m", "ancv", "serve", "api", "--port", "8080" ]
