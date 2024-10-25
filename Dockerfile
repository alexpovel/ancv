FROM python:3.12-slim

ARG WORKDIR="/app"
WORKDIR ${WORKDIR}

RUN useradd -u 1000 -d ${WORKDIR} -M app
RUN chown -R app:app ${WORKDIR}
USER 1000

# Cache-friendly dependency installation
COPY pyproject.toml uv.lock ./
# https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/
RUN uv sync --frozen --no-dev

COPY ancv/ ancv/

# Required for Google Cloud Run to auto-detect
EXPOSE 8080

ENTRYPOINT [ "uv", "run", "--frozen", "--module", "ancv" ]
CMD [ "--verbose", "serve", "api", "--port", "8080" ]
