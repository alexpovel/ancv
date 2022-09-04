# Changelog

## [0.15.1](https://github.com/alexpovel/ancv/compare/v0.15.0...v0.15.1) (2022-09-04)


### Bug Fixes

* **build:** Run publish pipeline on tags ([a171597](https://github.com/alexpovel/ancv/commit/a1715970707c754dfabcad7b26e35b2605a18795))

## [0.15.0](https://github.com/alexpovel/ancv/compare/v0.14.1...v0.15.0) (2022-09-04)


### Features

* **build:** Enable Docker image versioning ([8a34b35](https://github.com/alexpovel/ancv/commit/8a34b35de83f8ad8b51325c6152a2aeee83b12c5)), closes [#23](https://github.com/alexpovel/ancv/issues/23)
* **self-hosting:** Add self-hosting instructions and files ([140bbcc](https://github.com/alexpovel/ancv/commit/140bbcc078cfcf6b12eb501dfca654aec5b17560))

## [0.14.1](https://github.com/alexpovel/ancv/compare/v0.14.0...v0.14.1) (2022-09-04)


### Bug Fixes

* **app:** Adjust field name, `language` being much more intuitive ([fd25c0a](https://github.com/alexpovel/ancv/commit/fd25c0a79f80866e62d43b596d004003f605ee28))


### Documentation

* Expand docs, provide flow chart for core functionality ([12346bc](https://github.com/alexpovel/ancv/commit/12346bc3803df883eb4da0211583138f3f6e4752))
* Expand section on creating components ([c0457e4](https://github.com/alexpovel/ancv/commit/c0457e4833f895583bd194ad6e8141bb17ccb86b))
* Polish README, vastly expand the construction flowchart ([56cdc66](https://github.com/alexpovel/ancv/commit/56cdc6676f5222eadcdaf6a02d130f638f61043b))
* Remove illegal JSON ([1729b51](https://github.com/alexpovel/ancv/commit/1729b5169629601023692bc17f4b33571f9076bd))

## [0.14.0](https://github.com/alexpovel/ancv/compare/v0.13.0...v0.14.0) (2022-09-03)


### Features

* **app:** Adjust CV sections order ([ac2ad1f](https://github.com/alexpovel/ancv/commit/ac2ad1f6f1f2b427eb5e1ca3f2f4a4271198f2e3))


### Bug Fixes

* **app:** Adjust defaults handling ([5a11a4c](https://github.com/alexpovel/ancv/commit/5a11a4cff00b5cf050d234accdab4449362d4a65))
* **app:** Adjust rendering for skills to be 'sequential' as well ([bd27a4d](https://github.com/alexpovel/ancv/commit/bd27a4ddee18c76a91e2b75382ca32f619127735))
* **app:** Fix whitespace in language rendering ([43e577a](https://github.com/alexpovel/ancv/commit/43e577af49c7454175105c1823fb9b0af0db729a))
* **templating:** Fix whitespace/newlines around sections ([3e5b5c6](https://github.com/alexpovel/ancv/commit/3e5b5c687720641459cdbdb6cef1b06e5a4f6b86))
* **test:** Expand `full.json` test input, fix/adjust whitespace correspondingly ([cd31537](https://github.com/alexpovel/ancv/commit/cd31537915575e37ff088c11bc0093b6a2f580f7))

## [0.13.0](https://github.com/alexpovel/ancv/compare/v0.12.0...v0.13.0) (2022-09-03)


### Features

* **app:** Make `ancv` available as an installable script ([cabd4ec](https://github.com/alexpovel/ancv/commit/cabd4ece22f651eeb17e662c52ec0f834e2e3fa8))
* **app:** Provide date 'collapsing' for same-month ranges ([5e4cc52](https://github.com/alexpovel/ancv/commit/5e4cc529b2953708ca52757e146ac31f26806c84)), closes [#45](https://github.com/alexpovel/ancv/issues/45)
* **app:** Remove day from date formatting ([08218b0](https://github.com/alexpovel/ancv/commit/08218b0d0d8f2ce0c6a5625115602c61abeb9acc))
* **test:** Mark timings test as flaky, allowing reruns ([5b44cda](https://github.com/alexpovel/ancv/commit/5b44cdad17acc9b045e4a13cfa6f6df9bbc042f9))


### Bug Fixes

* **tests:** Expect tests to fail if GH API limit reached ([b6c97b5](https://github.com/alexpovel/ancv/commit/b6c97b5809d2d34196022949294b9b9446ca945a))


### Documentation

* Simplify README, add LinkedIn link ([a57e8d1](https://github.com/alexpovel/ancv/commit/a57e8d16db1dcdeb257ef409e0ca676d09f00ab3))

## [0.12.0](https://github.com/alexpovel/ancv/compare/v0.11.0...v0.12.0) (2022-08-14)


### Features

* **api:** Forego user existence check, try for gists directly ([9f83798](https://github.com/alexpovel/ancv/commit/9f83798021132a6089193887195a76c568ca9e77)), closes [#41](https://github.com/alexpovel/ancv/issues/41)


### Documentation

* Clean up README, move details to ARCHITECTURE doc ([79c61a8](https://github.com/alexpovel/ancv/commit/79c61a83cd8a2960ba3da893518863f9aef45866))

## [0.11.0](https://github.com/alexpovel/ancv/compare/v0.10.0...v0.11.0) (2022-08-13)


### Features

* **api:** Enable GitHub username validation ([614167b](https://github.com/alexpovel/ancv/commit/614167b8e4c4947b1e9f63a0ddfafbfee785ab85)), closes [#7](https://github.com/alexpovel/ancv/issues/7)
* **api:** Raise 'correct' status code upon lookup error ([8ae751f](https://github.com/alexpovel/ancv/commit/8ae751f6bb5ae29e940ebc816cb1aaf6f2a92dc3))
* **app:** Cover GitHub API rate limit exceeding w/ a server response ([99c6039](https://github.com/alexpovel/ancv/commit/99c60393c44301b6bab6eaedbce10bed1a5db48b))

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
