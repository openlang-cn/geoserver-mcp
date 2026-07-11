# Release and Versioning

## Project Version

- Current project version: `1.0.7`
- PyPI package name: `open-geoserver-mcp`
- CLI command: `geoserver-mcp`

## Dependency Baseline

- `mcp==1.28.1`
- `geoserver-rest==2.10.0`

## Versioning Rules

- The project version is independent from dependency versions.
- Every formal release must update:
  - `pyproject.toml`
  - `src/geoserver_mcp/__init__.py`
  - `CHANGELOG.md`
- Use semantic versioning:
  - `PATCH` for internal fixes or compatibility-only changes
  - `MINOR` for backward-compatible new tools, resources, or parameters
  - `MAJOR` for breaking changes

## Release Traceability

- Create a Git tag in the format `vX.Y.Z`.
- Keep GitHub Release and PyPI version aligned.
- Do not rewrite or delete historical tags, releases, or published versions unless there is a serious operational reason.
- If a published version should no longer be recommended, prefer yanking the package instead of removing history.

## Before Releasing

```bash
ruff check src tests examples
mypy src/geoserver_mcp
pytest tests -q --cov=geoserver_mcp --cov-report=term-missing
python -m compileall src examples tests
uv build
```

## When Dependencies Change

When upgrading `mcp`, `geoserver-rest`, or another key dependency:

- update dependency declarations in `pyproject.toml`
- update installation, compatibility, or usage notes in `README.md` and `docs/`
- add upgrade notes and migration impact to `CHANGELOG.md`
- verify CI still reflects the real local validation commands
