# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project uses semantic versioning for published releases.

## [Unreleased]
## [1.0.6] - 2026-07-11

### Fixed

- Fix wheel build: `force-include` on sdist caused duplicate file paths, breaking wheel build from sdist. Removed `force-include` from sdist, kept only for wheel.


## [1.0.5] - 2026-07-11

### Fixed

- Fix empty wheel build (second attempt): replaced `packages` with `force-include` in hatch config to properly include Python source files in the wheel.


## [1.0.4] - 2026-07-11

### Fixed

- Fix empty wheel build: `packages = ["src/geoserver_mcp"]` in hatch config caused empty wheel on PyPI. Changed to `sources = ["src"]` so hatch correctly discovers and includes the `geoserver_mcp` package.


## [1.0.3] - 2026-07-11

### Added

- New `get_featuretype` tool returns full feature type metadata including SQL view definitions, CRS, bounding box, and attributes.

### Changed

- Enable automatic MCP tool discovery for `get_featuretype` in the catalog module.



### Added

- Open-source project governance files and contribution guidance.
- GitHub Actions CI for pull requests and pushes.
- Trusted Publishing with API token fallback for PyPI releases.

### Changed

- MCP tool wrappers were aligned with the installed `geo` library signatures for feature types, styles, security, and workspace checks.
- Documentation was reorganized under `docs/`, and deployment assets were grouped under `deploy/`.
- CI now runs on Python 3.12 only, and coverage gates were aligned with the expanded test suite.

## [1.0.2] - 2026-07-09

### Fixed

- MCP tool return annotations corrected to match `geo` library contracts (security, catalog, styles, system).
- `get_version()` now returns `dict` instead of `str`, matching the underlying `geo.Geoserver` API.
- Style XML tools (`style_outline_only_xml`, `style_catagorize_xml`, `style_classified_xml`, `style_coverage_style_xml`) capture generated `style.sld` content instead of returning `None`.
- Named color ramp strings (e.g. `"viridis"`) in `style_coverage_style_colormapentry` and `style_coverage_style_xml` are expanded to real hex colors via seaborn.
- `geo.Style` / `seaborn` / `matplotlib` imports deferred to lazy loading to avoid blocking module import.
- WMS/WFS resource URIs tightened from `{request}` templates to static `GetCapabilities` resources.

### Changed

- Bumped from `1.0.1`; `1.0.0` PyPI filename could no longer be reused.
- Documentation: added `uvx --refresh` / `--no-cache` usage to installation guide.
- Tests: added `test_tool_contracts.py` to lock return annotations against `geo` library contracts.

## [1.0.0] - 2026-07-09

### Added

- Initial PyPI release as `open-geoserver-mcp`.
- MCP server entrypoint, resources, tools, Docker deployment, and example client.
