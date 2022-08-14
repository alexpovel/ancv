# Architecture

[![codecov](https://codecov.io/gh/alexpovel/ancv/branch/main/graph/badge.svg?token=I5XFLBHRCH)](https://codecov.io/gh/alexpovel/ancv)

This document is less about software architecture per-se, but rather about technical details deemed out-of-scope for the [README](./README.md).

## Features

- fully async using [`aiohttp`](https://docs.aiohttp.org/en/stable/) and [gidgethub](https://gidgethub.readthedocs.io/en/latest/index.html)
- [structural pattern matching](https://peps.python.org/pep-0634/), introduced in Python 3.10:
  - initially used for fun, but not because any use cases were substantially easier using it,
  - then dropped on 2022-07-16 since Python 3.10 is [unsupported by AWS lambda](https://github.com/aws/aws-lambda-base-images/issues/31),
  - but since switched to [Google Cloud Run](https://cloud.google.com/run), which is based on regular OCI containers (see [Dockerfile](./Dockerfile)), hence resolving the hell that is dependency management in serverless environments.

  Fully serverless is still interesting since it's such a fitting use-case.
  The best solution seems to [vendor all dependencies](https://www.serverless.com/plugins/serverless-python-requirements), instead of trying our luck with the serverless provider reading and correctly installing the dependencies for us (which often requires a `requirements.txt` instead of a [`poetry.lock`](./poetry.lock) or similar).

  However, since this project treats self-hosting as a first-class citizen, going full serverless and abandoning providing Docker images entirely isn't an option anyway.
  Hosting serverlessly would be a split, required maintenance of two hosting options instead of just building one image and calling it a day.
- [fully typed](https://mypy.readthedocs.io/en/stable/index.html) using Python type hints, verified through `mypy --strict` (with additional, [even stricter settings](pyproject.toml))
- [structural logging](https://github.com/hynek/structlog) with a JSON event stream output
- [`pydantic`](https://pydantic-docs.helpmanual.io/) for fully typed data validation (e.g., for APIs), facilitated by [automatic `pydantic` model generation](https://koxudaxi.github.io/datamodel-code-generator/) from e.g. OpenAPI specs like [GitHub's](https://github.com/github/rest-api-description/tree/main/descriptions/api.github.com) or [JSON Resume's](https://github.com/jsonresume/resume-schema/blob/master/schema.json), allowing full support from `mypy` and the IDE when using said validated data
- [12 Factor App](https://12factor.net/) conformance:
  1. [Codebase](https://12factor.net/codebase): [GitHub-hosted repo](https://github.com/alexpovel/ancv/)
  2. [Dependencies](https://12factor.net/dependencies): taken care of by [poetry](https://python-poetry.org/) and its standardized ([PEP 621](https://peps.python.org/pep-0621/)) [config](pyproject.toml) and [lock](poetry.lock) files, pinning all transient dependencies and providing virtual environments
  3. [Config](https://12factor.net/config): the app is configured using environment variables.
     Although [problematic](https://news.ycombinator.com/item?id=31200132), this approach was chosen for its simplicity
  4. [Backing Services](https://12factor.net/backing-services): not applicable for this very simple app
  5. [Build, release, run](https://12factor.net/build-release-run): handled through GitHub releases via git tags and [release-please](https://github.com/marketplace/actions/release-please-action)
  6. [Processes](https://12factor.net/processes): this simple app is stateless in and of itself
  7. [Port binding](https://12factor.net/port-binding): the `aiohttp` [server](ancv/web/server.py) part of the app acts as a [standalone web server](https://docs.aiohttp.org/en/stable/deployment.html#standalone), exposing a port.
     That port can then be serviced by any arbitrary reverse proxy
  8. [Concurrency](https://12factor.net/concurrency): covered by async functionality (in a single process and thread).
     This being a stateless app, horizontal scaling through additional processes is trivial (e.g. via serverless hosting), although vertical scaling will likely suffice indefinitely
  9. [Disposability](https://12factor.net/disposability): `aiohttp` handles `SIGTERM` gracefully
  10. [Dev/prod parity](https://12factor.net/dev-prod-parity): trivial to do for this simple app.
       If running on Windows, mind [this issue](https://stackoverflow.com/q/45600579/11477374).
       If running on Linux, no special precautions are necessary
  11. [Logs](https://12factor.net/logs): structured JSON logs are written directly to `stdout`
  12. [Admin processes](https://12factor.net/admin-processes): not applicable either

## Similar solutions

Very hard to find any, and even hard to google.
For example, `bash curl curriculum vitae` will prompt Google to interpret `curriculum vitae == resume`, which isn't wrong but `curl resume` is an entirely unrelated query (concerned with resuming halted downloads and such).

Similar projects:

- <https://github.com/soulshake/cv.soulshake.net>

Related, but 'fake' hits:

- <https://ostechnix.com/create-beautiful-resumes-commandline-linux/>
