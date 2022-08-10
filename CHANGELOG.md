# Changelog

## [0.10.0](https://github.com/alexpovel/ancv/compare/v0.9.0...v0.10.0) (2022-08-10)


### Features

* **web:** Provide `Server-Timing` Header ([a2c2b9e](https://github.com/alexpovel/ancv/commit/a2c2b9eaab58288e0095b467a139b242fa5f8c73))

## [0.9.0](https://github.com/alexpovel/ancv/compare/v0.8.0...v0.9.0) (2022-08-08)


### Features

* **cli:** Add `list` command to display all available components ([eaaa00c](https://github.com/alexpovel/ancv/commit/eaaa00ca89ffb22da79d9e9b49520e2953550389)), closes [#36](https://github.com/alexpovel/ancv/issues/36)
* **cli:** Add `version` CLI command ([8332d84](https://github.com/alexpovel/ancv/commit/8332d84198cfe26b1a106edcbeba90f5cefa1522))
* **tests:** Add new Makefile target + CI job for codecov.io upload ([d451c28](https://github.com/alexpovel/ancv/commit/d451c2840a023478702e7ff5c1738820d83a289f))


### Bug Fixes

* **tests:** Remove unused fixture ([6fd7baa](https://github.com/alexpovel/ancv/commit/6fd7baa8c07f2aef155f4d61437370471060c89d))

## [0.8.0](https://github.com/alexpovel/ancv/compare/v0.7.0...v0.8.0) (2022-07-26)


### Features

* **app:** Add `ascii_only` option ([2efdc09](https://github.com/alexpovel/ancv/commit/2efdc09496a7be679ecb0d938283404850b972a6))

## [0.7.0](https://github.com/alexpovel/ancv/compare/v0.6.1...v0.7.0) (2022-07-24)


### Features

* **ci:** Cache `poetry` dependencies ([23dca4b](https://github.com/alexpovel/ancv/commit/23dca4bb08815c6949df12b777a27d13e2162c3d))
* **cli:** Add command to serve a single file ([6318e96](https://github.com/alexpovel/ancv/commit/6318e96ee8b9070a599e6223b70e9a87b8c875ae))

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
