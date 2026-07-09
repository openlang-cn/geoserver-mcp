# Local Development

## Project Structure

```text
src/geoserver_mcp/
├─ main.py          # CLI entrypoint
├─ server.py        # FastMCP server factory and registration
├─ connection.py    # GeoServer connection creation
├─ client.py        # Compatibility wrapper for geoserver-rest
├─ resources.py     # MCP resource endpoints
├─ utils.py         # Shared utility functions
└─ tools/
   ├─ catalog.py    # workspaces, layers, stores, layer groups, feature types
   ├─ styles.py     # styles and SLD XML helpers
   ├─ security.py   # users and groups
   └─ system.py     # status, version, service config
```

Other important files:

- `examples/client.py`: example client
- `tests/`: test suite
- `deploy/Dockerfile`: container image
- `deploy/docker-compose.yml`: Compose example
- `deploy/.env.example`: environment template

## Local Commands

```bash
pytest tests -q
ruff check src tests examples
mypy src/geoserver_mcp
pytest tests -q --cov=geoserver_mcp --cov-report=term-missing
python -m compileall src examples tests
```

## Contribution Workflow

- Read `CONTRIBUTING.md` before opening a pull request.
- Keep changes focused and include local verification steps.
- Update `README.md`, `docs/`, examples, and `CHANGELOG.md` when user-facing behavior changes.

## Continuous Integration

GitHub Actions runs these baseline checks on pull requests and supported branches:

- `ruff check src tests examples`
- `mypy src/geoserver_mcp`
- `pytest tests -q --cov=geoserver_mcp --cov-report=term-missing --cov-fail-under=75`
- `python -m compileall src examples tests`

## Governance

- Contribution guide: `CONTRIBUTING.md`
- Code of conduct: `CODE_OF_CONDUCT.md`
- Security policy: `SECURITY.md`
- Release notes: `CHANGELOG.md`
