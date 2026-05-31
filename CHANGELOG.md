# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Test suite: offline unit tests over saved per-endpoint fixtures, plus live contract
  tests (`-m live`) that flag when upstream BSE/Screener markup or schemas drift.
- GitHub Actions CI (lint, type-check, and a Python 3.9–3.13 test matrix) and Dependabot.
- Type hints across the public API, shipped to consumers via a `py.typed` marker.
- `pyproject.toml` (PEP 621) packaging managed by uv, with a `uv.lock` lockfile.
- Ruff (lint + format), mypy, and pre-commit configuration.
- `CHANGELOG.md`, `SECURITY.md`, and `DESIGN_DECISIONS.md`.

### Changed

- Migrated to a `src/` layout.
- `requires-python` is now `>=3.9` (dropped dead 2.7/3.5–3.8 classifiers).
- Tightened dependency pins (`beautifulsoup4`, `requests`, `pandas`, `lxml`, `html5lib`).
- `analysis()` now returns pros/cons as `list[str]` (previously a single string).
- Replaced bare `except:` blocks with `except Exception:`.

### Fixed

- Repaired scrapers against current upstream markup: BSE API now requires Origin/Referer
  headers; `script()` needed a browser User-Agent; Screener moved its annual/credit-report
  and pros/cons containers; `comp_profile` re-sourced from Screener after Yahoo removed its
  profile page; corrected `quote` change/percent-change sign handling.

## [0.0.5] — 2023

- Initial published feature set: live quotes, search, gainers/losers, statements, ratios,
  corporate actions, holdings, news, analysis and report links.

[Unreleased]: https://github.com/Sachin-Kahandal/bselib/compare/v0.0.5...HEAD
[0.0.5]: https://github.com/Sachin-Kahandal/bselib/releases/tag/v0.0.5
