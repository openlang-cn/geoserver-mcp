# Contributing

Thanks for considering a contribution to `open-geoserver-mcp`.

## Development setup

1. Create a virtual environment:

```bash
uv venv --python=3.10
```

2. Activate it.

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux / macOS:

```bash
source .venv/bin/activate
```

3. Install the project and development dependencies:

```bash
uv pip install -e ".[dev]"
```

## Local checks

Run the same baseline checks expected in CI before opening a pull request:

```bash
ruff check src tests examples
mypy src/geoserver_mcp
pytest tests -q
pytest tests -q --cov=geoserver_mcp --cov-report=term-missing
python -m compileall src examples tests
```

## Coding guidelines

- Follow the existing Python style in `src/`: 4 spaces, `snake_case`, small focused functions.
- Keep MCP tool names descriptive and aligned with their GeoServer behavior.
- When changing MCP tools, resources, arguments, or behavior, update `README.md` and related examples in the same pull request.
- Prefer tests that mock GeoServer interactions instead of depending on a real GeoServer instance.

## Pull requests

- Use a focused branch and keep each pull request scoped to one topic.
- Include a short summary, local verification steps, and any documentation updates.
- Add or update tests for bug fixes, parameter handling, path handling, and integration boundaries.
- If you change public installation, release, or deployment behavior, update `README.md`.

## Releases

- Version numbers are managed in `pyproject.toml` and `src/geoserver_mcp/__init__.py`.
- Update `CHANGELOG.md` when shipping user-visible changes.
- PyPI publishing is handled through GitHub Actions after a GitHub Release is published.
