# Global ARG, available to all stages (if renewed)
ARG WORKDIR="/app"

FROM python:3.11 AS builder

# Renew (https://stackoverflow.com/a/53682110):
ARG WORKDIR

# Don't buffer `stdout`:
ENV PYTHONUNBUFFERED=1
# Don't create `.pyc` files:
ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install poetry && poetry config virtualenvs.in-project true

WORKDIR ${WORKDIR}
COPY . .

RUN poetry install --only main

FROM python:3.11-alpine

ARG WORKDIR

WORKDIR ${WORKDIR}

COPY --from=builder ${WORKDIR} .

# For options, see https://boxmatrix.info/wiki/Property:adduser
RUN adduser app -DHh ${WORKDIR} -u 1000
USER 1000

# App-specific settings:
EXPOSE 8080
ENTRYPOINT [ "./.venv/bin/python", "-m", "ancv" ]
CMD [ "serve", "api", "--port", "8080" ]
