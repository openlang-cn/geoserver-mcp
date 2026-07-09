[简体中文文档](./docs/README.zh-CN.md)

# GeoServer MCP Server

GeoServer MCP is an MCP (Model Context Protocol) server for GeoServer. It wraps the GeoServer REST API into MCP tools for MCP-compatible clients such as Codex, Cursor, and Claude Desktop.

![GeoServer MCP](./docs/geoserver-mcp.png)

## Overview

- Manage workspaces, stores, layers, layer groups, feature types, styles, users, and system operations.
- Expose MCP resources and tools over `stdio`, `streamable-http`, and `sse`.
- Support local development, `uvx` launch from PyPI, Docker deployment, and 1Panel deployment.

## Quick Start

Requirements:

- Python `3.10+`
- A reachable GeoServer instance with REST API enabled

Run directly from PyPI:

```bash
uvx --from open-geoserver-mcp geoserver-mcp \
  --url http://localhost:8080/geoserver \
  --user admin \
  --password geoserver
```

Package naming:

- PyPI package: `open-geoserver-mcp`
- CLI command: `geoserver-mcp`

## Documentation

- [Documentation Index](./docs/README.md)
- [Installation and Startup](./docs/getting-started/installation.md)
- [Client Configuration](./docs/getting-started/client-configuration.md)
- [MCP Resources and Tools](./docs/mcp/resources-and-tools.md)
- [Docker and 1Panel Deployment](./docs/deployment/docker-and-1panel.md)
- [Local Development](./docs/development/local-development.md)
- [Release and Versioning](./docs/maintainers/release-and-versioning.md)

## Open Source Project Files

- [CONTRIBUTING.md](./CONTRIBUTING.md)
- [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)
- [SECURITY.md](./SECURITY.md)
- [CHANGELOG.md](./CHANGELOG.md)
- [LICENSE](./LICENSE)
- [Deployment Assets](./deploy/README.md)

## Development

```bash
uv venv --python=3.10
uv pip install -e ".[dev]"
ruff check src tests examples
mypy src/geoserver_mcp
pytest tests -q --cov=geoserver_mcp --cov-report=term-missing
python -m compileall src examples tests
```

## License

MIT
