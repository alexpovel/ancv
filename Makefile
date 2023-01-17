.PHONY: tests test typecheck formatcheck lint image

RUN = poetry run
LIBRARY = ancv

tests: test typecheck formatcheck lint

# Ensure the Docker image also builds properly
alltests: tests image

test:
	${RUN} pytest \
		--cov=${LIBRARY} \
		--cov-report=html \
		--cov-report=term \
		--cov-report=xml

typecheck:
	${RUN} mypy -p ${LIBRARY}

formatcheck:
	${RUN} black --check --diff ${LIBRARY}

lint:
	${RUN} ruff .

image:
	@docker build --progress=plain --tag ${LIBRARY}/${LIBRARY} .

# Hooks need to be added here manually if other 'types' are later added:
hooks:
	@pre-commit install --hook-type pre-push --hook-type pre-commit --hook-type commit-msg

requirements.txt:
	poetry export --with=dev --output=requirements.txt

depgraph.svg:
	@command -v dot > /dev/null || (echo "Please install graphviz for its 'dot' command." && exit 1)
	@${RUN} pydeps --max-bacon=4 --cluster -T svg -o "$@" ${LIBRARY}

schema.json:
	${RUN} python -m ${LIBRARY} generate-schema > "$@"

resume.py:
	${RUN} datamodel-codegen \
		--url "https://raw.githubusercontent.com/jsonresume/resume-schema/master/schema.json" \
		--encoding utf-8 \
		--input-file-type jsonschema \
		--output "$@"

github.py:
	${RUN} datamodel-codegen \
		--url "https://raw.githubusercontent.com/github/rest-api-description/main/descriptions-next/api.github.com/dereferenced/api.github.com.deref.json" \
		--encoding utf-8 \
		--input-file-type openapi \
		--openapi-scopes paths \
		--output "$@"
