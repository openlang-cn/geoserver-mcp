# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project uses semantic versioning for published releases.

## [Unreleased]

### Added

- Open-source project governance files and contribution guidance.
- GitHub Actions CI for pull requests and pushes.
- Trusted Publishing with API token fallback for PyPI releases.

### Changed

- MCP tool wrappers were aligned with the installed `geo` library signatures for feature types, styles, security, and workspace checks.
- Documentation was reorganized under `docs/`, and deployment assets were grouped under `deploy/`.
- CI now runs on Python 3.12 only, and coverage gates were aligned with the expanded test suite.

## [1.0.1] - 2026-07-09

### Changed

- Republished release metadata after the original `1.0.0` PyPI filename could no longer be reused.

## [1.0.0] - 2026-07-09

### Added

- Initial PyPI release as `open-geoserver-mcp`.
- MCP server entrypoint, resources, tools, Docker deployment, and example client.
