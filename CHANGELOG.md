# Changelog

## [1.5.3](https://github.com/alexpovel/ancv/compare/v1.5.2...v1.5.3) (2025-01-05)


### Bug Fixes

* Move `ancv.io` -&gt; `ancv.povel.dev` ([3e45365](https://github.com/alexpovel/ancv/commit/3e4536508039214e5f0c649bba571440a6ee9dc7))

## [1.5.2](https://github.com/alexpovel/ancv/compare/v1.5.1...v1.5.2) (2024-11-18)


### Bug Fixes

* **build:** Docker ARM build (try 2) ([7e2d595](https://github.com/alexpovel/ancv/commit/7e2d595d6b31dbe83425e5e715aea042bd716e31))

## [1.5.1](https://github.com/alexpovel/ancv/compare/v1.5.0...v1.5.1) (2024-11-18)


### Bug Fixes

* **build:** Docker ARM build ([8216ac8](https://github.com/alexpovel/ancv/commit/8216ac8bff3bc328369e6fdc211c9610cda517c2))


### Documentation

* Add port mapping for docker command ([3c1d404](https://github.com/alexpovel/ancv/commit/3c1d404804e9c609cf280543d7babf7859818757))

## [1.5.0](https://github.com/alexpovel/ancv/compare/v1.4.5...v1.5.0) (2024-11-18)


### Features

* **web:** Add web server command to serve JSON resume from URL with periodic refresh ([#241](https://github.com/alexpovel/ancv/issues/241)) ([51e1640](https://github.com/alexpovel/ancv/commit/51e1640d4629342ecf279530b5f4400f5c13d0e7))

## [1.4.5](https://github.com/alexpovel/ancv/compare/v1.4.4...v1.4.5) (2024-10-25)


### Bug Fixes

* Release process ([dc64e98](https://github.com/alexpovel/ancv/commit/dc64e98d27b9ba95a9ac8d271036b5aafb4a8b9c))

## [1.4.4](https://github.com/alexpovel/ancv/compare/v1.4.3...v1.4.4) (2024-10-25)


### Bug Fixes

* **metadata:** Fix URL metadata fetching & printing ([3c4bbb5](https://github.com/alexpovel/ancv/commit/3c4bbb5751cc73e793051192d6e75d284bf6da54))

## [1.4.3](https://github.com/alexpovel/ancv/compare/v1.4.2...v1.4.3) (2024-10-24)


### Bug Fixes

* **ci:** Empty fix to trigger CI ([60736c4](https://github.com/alexpovel/ancv/commit/60736c4a884c9bb9f59fc5dc338f5c09236c8b80))
* **docker:** `error: failed to write to file `/app/uv.lock` ([a12a2d5](https://github.com/alexpovel/ancv/commit/a12a2d5cabc6e1ad1f19582a805b8d2a7d29ad92))

## [1.4.2](https://github.com/alexpovel/ancv/compare/v1.4.1...v1.4.2) (2024-10-23)


### Bug Fixes

* `remaining` variable possibly unbound ([ea03173](https://github.com/alexpovel/ancv/commit/ea03173d92943797c5d0a16ebdadb993b3ba4c47))
* **project-setup:** Switch from `poetry` to `uv`, bump all dependency versions to latest ([4983dee](https://github.com/alexpovel/ancv/commit/4983dee25ab3d23781ab2b7bd59077e00a9d3e99))

## [1.4.1](https://github.com/alexpovel/ancv/compare/v1.4.0...v1.4.1) (2024-05-01)


### Bug Fixes

* Provide libc for pydantic ([49a91f9](https://github.com/alexpovel/ancv/commit/49a91f98f9764d5f67ee53b0de54e53d0b759eff))

## [1.4.0](https://github.com/alexpovel/ancv/compare/v1.3.1...v1.4.0) (2024-05-01)


### Features

* Set up devbox ([b1156f6](https://github.com/alexpovel/ancv/commit/b1156f650380079d87f0062aa9d4e6e481ae0225))


### Bug Fixes

* **ci:** Allow release-please to run as full bot account ([2fcafa2](https://github.com/alexpovel/ancv/commit/2fcafa28f5ef8f35930c0c329ebace1bb11cc21b))
* **ci:** Bootstrap release-please ([bd5cb39](https://github.com/alexpovel/ancv/commit/bd5cb39c69b02cbcdb30c0f934309e37aecc219e))
* **ci:** Bootstrap release-please after its v4 release ([926edc6](https://github.com/alexpovel/ancv/commit/926edc645b59d477ae88d2e968a55f11c37fa278))
* **ci:** Package manifest path ([d6c914d](https://github.com/alexpovel/ancv/commit/d6c914d4df8f56856feb1122fcb2ad013dd6fb6c))
* **ci:** Roll back to normal PAT ([5a84fc4](https://github.com/alexpovel/ancv/commit/5a84fc4432e1f53f5dbf077906873e4ac01c13c6))
* **tests:** URL str output changed subtly ([bfc8632](https://github.com/alexpovel/ancv/commit/bfc8632a3648122e1c858a817666beff77e1ffbc))
* Type errors after mypy version bump ([dcc813d](https://github.com/alexpovel/ancv/commit/dcc813d3ad8ab9984e3edfae0eac5cd730ea87a0))
* **typing:** Allow `Any` until `mypy`/`pydantic` play well together again ([22dff21](https://github.com/alexpovel/ancv/commit/22dff2144aff6fb19097c0080d3a5369cea7b15e))


### Documentation

* Suggest a gpt prompt for generating resumes in JSON Resume Schema format ([321c438](https://github.com/alexpovel/ancv/commit/321c438601b1257f6b32e39be726cb0c006297d3))

## [1.3.1](https://github.com/alexpovel/ancv/compare/v1.3.0...v1.3.1) (2023-04-21)


### Bug Fixes

* Protect container image release via environment ([aa93136](https://github.com/alexpovel/ancv/commit/aa93136fdf71683da2790312fa4f9577b8da09ee))

## [1.3.0](https://github.com/alexpovel/ancv/compare/v1.2.3...v1.3.0) (2023-04-21)


### Features

* Harden PyPI deployment via OIDC ([9fec4ed](https://github.com/alexpovel/ancv/commit/9fec4edb75c39aba52a913b3e7d7b9f62c155022))

## [1.2.3](https://github.com/alexpovel/ancv/compare/v1.2.2...v1.2.3) (2023-02-05)


### Bug Fixes

* Skip empty but specified (`[]`) sections ([ed5d20f](https://github.com/alexpovel/ancv/commit/ed5d20f9a0e68311e1266acbfccd5249df2131c5))

## [1.2.2](https://github.com/alexpovel/ancv/compare/v1.2.1...v1.2.2) (2023-02-05)


### Documentation

* Document and clear up templating code ([920a759](https://github.com/alexpovel/ancv/commit/920a75968cde31d97f38db01f50a328e4d50d76b))
* Document and clear up theme code ([5229102](https://github.com/alexpovel/ancv/commit/5229102e7b818d617550b181ec3a2372c7d7a6bf))
* Document and clear up web {client,server} and other code ([7690b08](https://github.com/alexpovel/ancv/commit/7690b089906746e6607bbe8bebed086aa7d3c9c9))
* Document pydantic models and their original counterpart ([8365454](https://github.com/alexpovel/ancv/commit/836545490dcf3d82a90ca253a8be5ab07f30ba89))

## [1.2.1](https://github.com/alexpovel/ancv/compare/v1.2.0...v1.2.1) (2022-11-10)


### Bug Fixes

* Incorporate updated dependencies into deployed version ([cac2373](https://github.com/alexpovel/ancv/commit/cac2373687a24163f9b2c65f42f5ef7112c21173))

## [1.2.0](https://github.com/alexpovel/ancv/compare/v1.1.0...v1.2.0) (2022-09-20)


### Features

* Add command to generate JSON schema for the package ([ea26b22](https://github.com/alexpovel/ancv/commit/ea26b2286b78977c389fb79805a9d589c13ad16b))


### Bug Fixes

* Only run imports for actually used command ([432311a](https://github.com/alexpovel/ancv/commit/432311ac3c488218e4dcadc23fadc2ed3273c62b))
* Use correct encoding when exporting Python models ([ab7ca67](https://github.com/alexpovel/ancv/commit/ab7ca6739e39afbdd9a6e70bde154fb79d7d482a))


### Documentation

* Update to reflect new JSON Schema provision ([2cc9e87](https://github.com/alexpovel/ancv/commit/2cc9e872fde4970ba6843bff1a1746d82c0d23b4))

## [1.1.0](https://github.com/alexpovel/ancv/compare/v1.0.2...v1.1.0) (2022-09-18)


### Features

* Add toggle to display 'Dec. 31st' dates as year-only ([26d46cb](https://github.com/alexpovel/ancv/commit/26d46cb94eb45ae5df526bf785a7eb299008e201)), closes [#65](https://github.com/alexpovel/ancv/issues/65)


### Bug Fixes

* Please the Windows overlords ([fb58c58](https://github.com/alexpovel/ancv/commit/fb58c583234dd8fb77e1a96ab8371033a15e3cc7))

## [1.0.2](https://github.com/alexpovel/ancv/compare/v1.0.1...v1.0.2) (2022-09-11)


### Documentation

* Add caveats concerning the LinkedIn Exporter approach ([87db22d](https://github.com/alexpovel/ancv/commit/87db22d447ac0be9ce21cec44c6feb6728240dbb))

## [1.0.1](https://github.com/alexpovel/ancv/compare/v1.0.0...v1.0.1) (2022-09-08)


### Bug Fixes

* **i18n:** `score` -> `grade` ([17389b6](https://github.com/alexpovel/ancv/commit/17389b6c462914d2b6d9f24f2d13d99c0cf6ed62))

## [1.0.0](https://github.com/alexpovel/ancv/compare/v0.20.0...v1.0.0) (2022-09-06)


### ⚠ BREAKING CHANGES

* Trigger initial major bump aka release

### Documentation

* Explain all the different components ([6baf1d2](https://github.com/alexpovel/ancv/commit/6baf1d28b1f01c134bce9bbee3dae0bdc1edbe22))


### bump

* Trigger initial major bump aka release ([543f5e7](https://github.com/alexpovel/ancv/commit/543f5e7bff09046bf3a7a8193f09174c0b4deed4))

## [0.20.0](https://github.com/alexpovel/ancv/compare/v0.19.1...v0.20.0) (2022-09-06)


### Features

* **i18n:** Add Spanish and French translations ([df98c24](https://github.com/alexpovel/ancv/commit/df98c2413d40180fef5029499543f6121e85fe74))


### Documentation

* Add showcase 'hero image' ([2e8de72](https://github.com/alexpovel/ancv/commit/2e8de72a7dc43e1fc0147b07fefb0bd757233205))
* Update available components ([76c83a0](https://github.com/alexpovel/ancv/commit/76c83a0182b0d9c286017528dca17e7d3e8668a6))

## [0.19.1](https://github.com/alexpovel/ancv/compare/v0.19.0...v0.19.1) (2022-09-06)


### Documentation

* Give `rich` a shout-out ([3ad55ca](https://github.com/alexpovel/ancv/commit/3ad55ca87bbd6a4a9aa18b1bb9d9d4db3fbad8a5))
* Improve README, add YouTube timestamp ([615d883](https://github.com/alexpovel/ancv/commit/615d88306bfb4ebce2b527f0ae6caca8571e0522))
* Specify `-UseBasicParsing` for PowerShell 5 ([38566d1](https://github.com/alexpovel/ancv/commit/38566d122e39b6e13f699b215a746bdfefa89196))

## [0.19.0](https://github.com/alexpovel/ancv/compare/v0.18.0...v0.19.0) (2022-09-05)


### Features

* **app:** Refactor and improve theming ([e35b703](https://github.com/alexpovel/ancv/commit/e35b703283f1e58e97a7856dfbfaef52699a3854))

## [0.18.0](https://github.com/alexpovel/ancv/compare/v0.17.0...v0.18.0) (2022-09-05)


### Features

* **app:** Add special `heyho` endpoint for showcasing ([79f20b8](https://github.com/alexpovel/ancv/commit/79f20b8b622108a626996989e3243c583357805b))

## [0.17.0](https://github.com/alexpovel/ancv/compare/v0.16.0...v0.17.0) (2022-09-04)


### Features

* **i18n:** Employ `babel`, add proper internationalization to dates ([492ee55](https://github.com/alexpovel/ancv/commit/492ee5579d0475eca20fbe747b39994e53996ff6))


### Bug Fixes

* **app:** Get rid of last remaining hard-coded strings ([ad58a6e](https://github.com/alexpovel/ancv/commit/ad58a6ed001a142aff82b8b16cc0bc323b4f34b5))
* **test:** Remove explicit `null` fields ([823d932](https://github.com/alexpovel/ancv/commit/823d932551fcc408d19728008a2deaad58b354be))


### Documentation

* Add `less` usage hint ([0bd5ca3](https://github.com/alexpovel/ancv/commit/0bd5ca32c9915d3a58506c3d9b4dee2f9ae61fc1))
* Add local usage examples ([e66a9b1](https://github.com/alexpovel/ancv/commit/e66a9b193ff1b84f3726512f66eb8e5460a0387f))
* Fix arrowheads (draw them manually) ([8a1dce3](https://github.com/alexpovel/ancv/commit/8a1dce396caf8347dabb050452a32bb2b74a4c36))

## [0.16.0](https://github.com/alexpovel/ancv/compare/v0.15.2...v0.16.0) (2022-09-04)


### Features

* **build:** Halve the Docker image size ([4d9fa53](https://github.com/alexpovel/ancv/commit/4d9fa5357c733a720a10a7f3c1575bdb237b296e))

## [0.15.2](https://github.com/alexpovel/ancv/compare/v0.15.1...v0.15.2) (2022-09-04)


### Bug Fixes

* **build:** Use `release-please` output as tag value input for Docker tagging ([4b05181](https://github.com/alexpovel/ancv/commit/4b05181303274d4034a2c10c75a174fa07b6f2d6))

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
