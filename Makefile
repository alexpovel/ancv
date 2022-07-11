typecheck:
	mypy -p ancv

depgraph.svg:
	@command -v dot > /dev/null || (echo "Please install graphviz for its 'dot' command." && exit 1)
	@pydeps --max-bacon=4 --cluster -T svg -o "$@" ancv

resume.py:
	datamodel-codegen \
		--url "https://raw.githubusercontent.com/jsonresume/resume-schema/master/schema.json" \
		--input-file-type jsonschema \
		--target-python-version 3.10 \
		--output "$@"

github.py:
	datamodel-codegen \
		--url "https://raw.githubusercontent.com/github/rest-api-description/main/descriptions-next/api.github.com/dereferenced/api.github.com.deref.json" \
		--input-file-type openapi \
		--target-python-version 3.10 \
		--openapi-scopes paths \
		--output "$@"
