FROM python:3.12-slim

ARG WORKDIR="/app"
WORKDIR ${WORKDIR}

RUN useradd -u 1000 -d ${WORKDIR} -M app
RUN chown -R app:app ${WORKDIR}
USER 1000

# https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# This just works... splitting this up for better caching is a pain with Python.
COPY . .
RUN uv sync --frozen

EXPOSE 8080

ENTRYPOINT [ "uv", "run", "ancv" ]
CMD [ "serve", "api", "--port", "8080" ]
