# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project uses semantic versioning for published releases.

## [Unreleased]
## [1.0.10] - 2026-07-12

### Added
- 为所有 MCP 工具参数添加 `Annotated[type, Field(description="...")]` 类型注解和中文描述

### Changed
- 将 `Annotated` 类型注解改为多行格式以符合 ruff E501 行长度限制

### Fixed
- 修复 `publish_featurestore` 中 `title`/`abstract` 空字符串被错误转为 `None` 的问题
- 修复 `create_featurestore`/`create_datastore`/`create_coveragestyle` 参数描述与官方库不一致

## [1.0.9] - 2026-07-11

### Fixed

- Fix XML escaping: `publish_featurestore_sqlview`, `publish_featurestore`, and `edit_featuretype` now escape user-provided values (SQL, abstract, keywords, CQL filter, etc.) before building XML, preventing XStream parsing errors when values contain `<`, `>`, `&`.


## [1.0.8] - 2026-07-11

### Fixed

- Fix feature type update request for data stores via direct REST API.


## [1.0.7] - 2026-07-11

### Added

- New `recalculate_featuretype_bbox` tool: recalculates native and lat/lon bounding boxes for a feature type via direct REST API call (library does not support this).


## [1.0.6] - 2026-07-11

### Added

- New `get_featuretype` tool: returns full feature type metadata including SQL view definitions, CRS, bounding box, and attributes.

### Fixed

- Fix empty wheel build: sdist was missing source files. Added `force-include` to sdist and wheel hatch configs to properly include Python source files.


## [1.0.7] - 2026-07-11

### Fixed

- Fix wheel build: sdist was missing `src/geoserver_mcp/`. Added `force-include` to sdist preserving the path, and to wheel mapping to the package directory.


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
