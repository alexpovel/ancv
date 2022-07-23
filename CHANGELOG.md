# Changelog

## [0.6.1](https://github.com/alexpovel/ancv/compare/v0.6.0...v0.6.1) (2022-07-23)


### Bug Fixes

* **build:** Fixed Dockerfile using old CLI syntax ([39fa5c8](https://github.com/alexpovel/ancv/commit/39fa5c8227c1ca47d3531e384c0ace46762b9ec9))
* **cli:** Turn 'Arguments' into 'Options' ([756b681](https://github.com/alexpovel/ancv/commit/756b6818403052b6bd1588c72dab7065f5e45e9b))

## [0.6.0](https://github.com/alexpovel/ancv/compare/v0.5.2...v0.6.0) (2022-07-23)


### Features

* **cli:** Add `--verbose` CLI option ([0c22e8c](https://github.com/alexpovel/ancv/commit/0c22e8cc92edf1b8ba7ac532b4b30d352183416c))
* **cli:** Replace `click` with `typer` ([a50d347](https://github.com/alexpovel/ancv/commit/a50d347a0829c305578f308dd0a2c375c1098a3f))

## [0.5.2](https://github.com/alexpovel/ancv/compare/v0.5.1...v0.5.2) (2022-07-19)


### Bug Fixes

* **build:** Allow cached Docker builds ([4edb27b](https://github.com/alexpovel/ancv/commit/4edb27b2de0d650a4c3837b9415d12f34318a386))
* **build:** Reorder jobs and steps ([de7b891](https://github.com/alexpovel/ancv/commit/de7b891f8aefb4aff3cd5b70fb997af6a67d003d))
* **build:** Use `main` branch ([2888677](https://github.com/alexpovel/ancv/commit/2888677faff53472e133baa6fbfe419e3e88c15a))
* **git:** Only run Python tasks on Python files ([cfd0fdb](https://github.com/alexpovel/ancv/commit/cfd0fdbb0e3937f0eed9c27161cfa1c8225be793))
* **web:** Use new env var, redirect properly for browsers ([c887388](https://github.com/alexpovel/ancv/commit/c8873882eeb396eeefb948eb7bf4fd947c0a32ee))

## [0.5.1](https://github.com/alexpovel/ancv/compare/v0.5.0...v0.5.1) (2022-07-19)


### Bug Fixes

* **build:** Move Docker image creation to 'publish' pipeline ([b43039f](https://github.com/alexpovel/ancv/commit/b43039f19d38390fff6eb20b6b6423dd0770e3e3))

## [0.5.0](https://github.com/alexpovel/ancv/compare/v0.4.0...v0.5.0) (2022-07-19)


### Features

* **build:** Add GitHub Actions job to upload Docker image ([b2e54f2](https://github.com/alexpovel/ancv/commit/b2e54f2593de4b1db3be12e35f4f94ec5fd73a9e))

## [0.4.0](https://github.com/alexpovel/ancv/compare/v0.3.0...v0.4.0) (2022-07-18)


### Features

* **ci:** Add `release-please` config ([01093ae](https://github.com/alexpovel/ancv/commit/01093aeec6c8fb104d558b25298a96f77feffa4a))
* **git:** Add `commitizen` commit lint for Conventional Commits ([a8c5937](https://github.com/alexpovel/ancv/commit/a8c5937de590476d2324f2b790ae834bbd47962c))


### Bug Fixes

* **deps:** Reorder metadata ([c679d48](https://github.com/alexpovel/ancv/commit/c679d4885b1ff40e71ca89b6529ad3501bdccc64))
