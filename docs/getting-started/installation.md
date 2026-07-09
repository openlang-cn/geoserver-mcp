# Installation and Startup

## Requirements

- Python `3.10+`
- A reachable GeoServer instance
- GeoServer REST API enabled

Recommended dependency versions:

- `mcp==1.28.1`
- `geoserver-rest==2.10.0`

## Package Naming

- PyPI package name: `open-geoserver-mcp`
- CLI command: `geoserver-mcp`

## Installation Options

- Local development: use `uv`
- Temporary launch or no local install: use `uvx --from open-geoserver-mcp geoserver-mcp`
- Long-running remote service: use Docker
- 1Panel-managed deployment: use `deploy/docker-compose.yml` or imported MCP config

### Local development

```bash
uv venv --python=3.10
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux or macOS:

```bash
source .venv/bin/activate
```

Install the project:

```bash
uv pip install -e .
```

Install development dependencies:

```bash
uv pip install -e ".[dev]"
```

### Run from PyPI with `uvx`

```bash
uvx --from open-geoserver-mcp geoserver-mcp --help
```

With GeoServer connection:

```bash
uvx --from open-geoserver-mcp geoserver-mcp \
  --url http://localhost:8080/geoserver \
  --user admin \
  --password geoserver
```

Install from PyPI:

```bash
pip install open-geoserver-mcp
```

The installed CLI command remains:

```bash
geoserver-mcp --help
```

## Startup Modes

### Local `stdio` mode

```bash
geoserver-mcp --url http://localhost:8080/geoserver --user admin --password geoserver
```

Or:

```bash
python -m geoserver_mcp.main --url http://localhost:8080/geoserver --user admin --password geoserver
```

### Remote `streamable-http` mode

```bash
geoserver-mcp \
  --transport streamable-http \
  --host 0.0.0.0 \
  --port 8000
```

Default endpoint:

```text
http://<host>:8000/mcp
```

### Remote `sse` mode

```bash
geoserver-mcp \
  --transport sse \
  --host 0.0.0.0 \
  --port 8000
```

Default paths:

- SSE: `/sse`
- Message: `/messages/`

## Common CLI Arguments

- `--url`: GeoServer URL
- `--user`: GeoServer username
- `--password`: GeoServer password
- `--storage`: file storage root
- `--transport`: `stdio` / `sse` / `streamable-http`
- `--host`: bind host
- `--port`: bind port
- `--mount-path`: HTTP mount root
- `--sse-path`: SSE path
- `--message-path`: SSE message path
- `--streamable-http-path`: Streamable HTTP path

## File Storage and `--storage`

If MCP tools need to read local files such as Shapefiles, GeoPackages, or SLD files, configure a storage root:

```bash
python -m geoserver_mcp.main --storage D:/data
```

Relative paths are resolved under that root.

Examples:

```text
roads.zip -> D:/data/roads.zip
style/demo.sld -> D:/data/style/demo.sld
```

For Docker or 1Panel:

- `GEOSERVER_STORAGE_PATH` should point to the container path
- the matching host directory must be mounted into the container
