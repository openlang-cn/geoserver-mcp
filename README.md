[简体中文文档](./docs/README.zh-CN.md)

# GeoServer MCP Server

An MCP (Model Context Protocol) server for GeoServer.  
It wraps the `GeoServer REST API` into MCP tools that can be used by MCP-compatible clients such as Codex, Cursor, and Claude Desktop.

---

## Overview

- Manage workspaces, datastores, featurestores, coveragestores, layers, and layer groups
- Query layer details, query features, and generate map access parameters
- Manage styles, upload SLD files, and generate style XML
- Read GeoServer status, version, and manifest information
- Support local `stdio` mode
- Support remote `streamable-http` / `sse`
- Support launch via `uvx --from git+...`
- Support Docker and 1Panel deployment

---

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
- `tests/`: basic tests
- `Dockerfile`: container image
- `docker-compose.yml`: remote deployment / 1Panel Compose example
- `.env.example`: environment template

---

## Requirements

- Python `3.10+`
- A reachable GeoServer instance
- GeoServer REST API enabled

Recommended dependency versions:

- `mcp==1.28.1`
- `geoserver-rest==2.10.0`

---

## Installation

### Which option should I use?

Choose by scenario:

- **Local development / debugging**: use `uv`, no Docker required
- **Temporary usage / no local install**: use `uvx --from git+...`
- **Long-running server / remote MCP endpoint**: use Docker
- **1Panel managed remote deployment**: use `docker-compose.yml`
- **1Panel imported MCP configuration**: use `uvx` import mode

In short:

- **Local development**: `uv`
- **Temporary launch**: `uvx`
- **Remote deployment**: Docker
- **Panel management**: 1Panel

### Option 1: Local development / local run

```bash
uv venv --python=3.10
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux / macOS:

```bash
source .venv/bin/activate
```

Install the project:

```bash
uv pip install -e .
```

Install dev dependencies:

```bash
uv pip install -e ".[dev]"
```

### Option 2: Run directly from GitHub with uvx

```bash
uvx --from git+https://github.com/openlang-cn/geoserver-mcp.git geoserver-mcp --help
```

With GeoServer connection:

```bash
uvx --from git+https://github.com/openlang-cn/geoserver-mcp.git geoserver-mcp \
  --url http://localhost:8080/geoserver \
  --user admin \
  --password geoserver
```

### Option 3: Docker

Docker is mainly for:

- server deployment
- remote MCP services
- 1Panel / Compose management
- avoiding manual Python runtime setup

Docker is **not required** for local development or local debugging.

Build the image:

```bash
docker build -t geoserver-mcp .
```

Run the container:

```bash
docker run --rm -p 8000:8000 \
  -e GEOSERVER_URL=http://host.docker.internal:8080/geoserver \
  -e GEOSERVER_USER=admin \
  -e GEOSERVER_PASSWORD=geoserver \
  geoserver-mcp
```

---

## Startup Modes

### 1) Local stdio mode

```bash
geoserver-mcp --url http://localhost:8080/geoserver --user admin --password geoserver
```

Or:

```bash
python -m geoserver_mcp.main --url http://localhost:8080/geoserver --user admin --password geoserver
```

### 2) Remote Streamable HTTP mode

```bash
geoserver-mcp \
  --transport streamable-http \
  --host 0.0.0.0 \
  --port 8000
```

Default remote endpoint:

```text
http://<host>:8000/mcp
```

### 3) Remote SSE mode

```bash
geoserver-mcp \
  --transport sse \
  --host 0.0.0.0 \
  --port 8000
```

Default paths:

- SSE: `/sse`
- Message: `/messages/`

### Common CLI arguments

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

---

## Client Configuration Examples

### Local command mode

```json
{
  "mcpServers": {
    "geoserver-mcp": {
      "command": "geoserver-mcp",
      "args": [
        "--url",
        "http://localhost:8080/geoserver",
        "--user",
        "admin",
        "--password",
        "geoserver"
      ]
    }
  }
}
```

### Remote Streamable HTTP mode

```json
{
  "mcpServers": {
    "geoserver-mcp": {
      "type": "streamable-http",
      "url": "https://your-domain.com/mcp"
    }
  }
}
```

### Remote SSE mode

```json
{
  "mcpServers": {
    "geoserver-mcp": {
      "type": "sse",
      "url": "https://your-domain.com/geoserver-mcp"
    }
  }
}
```

---

## 1Panel Usage

Two recommended approaches:

1. **Remote deployment mode**: deploy this project as a remote MCP service and connect directly by URL
2. **Imported MCP config mode**: let 1Panel launch the project with `uvx`, then expose `sse` or `streamableHttp`

### Option A: 1Panel remote deployment

Use the repository `docker-compose.yml`.

1. Copy the template:

```bash
cp .env.example .env
```

2. Edit `.env`:

```env
GEOSERVER_URL=http://your-geoserver:8080/geoserver
GEOSERVER_USER=admin
GEOSERVER_PASSWORD=geoserver
MCP_TRANSPORT=streamable-http
MCP_PORT=8000
MCP_STREAMABLE_HTTP_PATH=/mcp
```

3. Import `docker-compose.yml` into 1Panel
4. Start the service
5. Add a website / reverse proxy in 1Panel:

```text
https://your-domain.com/mcp -> http://127.0.0.1:8000/mcp
```

Codex config:

```json
{
  "mcpServers": {
    "geoserver-mcp-remote": {
      "type": "streamable-http",
      "url": "https://your-domain.com/mcp"
    }
  }
}
```

### Option B: 1Panel imported configuration

If your 1Panel supports importing standard `mcpServers` JSON, use this template.

#### Import JSON template

```json
{
  "mcpServers": {
    "geoserver-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/openlang-cn/geoserver-mcp.git",
        "geoserver-mcp"
      ],
      "env": {
        "GEOSERVER_URL": "http://your-geoserver:8080/geoserver",
        "GEOSERVER_USER": "admin",
        "GEOSERVER_PASSWORD": "geoserver"
      }
    }
  }
}
```

#### Automatically filled by import

- `command`
- `args`
- `env`

#### Still needs manual input in 1Panel

- external access path
- output type
- SSE path
- image
- container name
- port
- mounts

#### Notes

- Keep the launcher in default `stdio` mode
- Do not add `--transport streamable-http` to the imported command
- Let 1Panel handle the conversion to `sse` or `streamableHttp`

---

## Complete 1Panel Templates

### Template 1: `uvx + sse`

#### Import JSON

```json
{
  "mcpServers": {
    "geoserver-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/openlang-cn/geoserver-mcp.git",
        "geoserver-mcp"
      ],
      "env": {
        "GEOSERVER_URL": "http://your-geoserver:8080/geoserver",
        "GEOSERVER_USER": "admin",
        "GEOSERVER_PASSWORD": "geoserver"
      }
    }
  }
}
```

#### Manual 1Panel fields

- Name: `geoserver-mcp`
- Type: `适合 uvx 启动的 mcp`
- Start command: `uvx --from git+https://github.com/openlang-cn/geoserver-mcp.git geoserver-mcp`
- External access path: `http://<your-server-ip>:8084`
- Output type: `sse`
- SSE path: `/geoserver-mcp`
- Image: `supercorp/supergateway:uvx`
- Container name: `geoserver-mcp`
- Port: `8084`

#### Environment variables

```text
GEOSERVER_URL=http://your-geoserver:8080/geoserver
GEOSERVER_USER=admin
GEOSERVER_PASSWORD=geoserver
GEOSERVER_STORAGE_PATH=/data
```

#### Optional mount

```text
Host path: /your/local/data
Container path: /data
```

#### Codex config

```json
{
  "mcpServers": {
    "geoserver-mcp": {
      "type": "sse",
      "url": "http://<your-server-ip>:8084/geoserver-mcp"
    }
  }
}
```

### Template 2: `uvx + streamableHttp`

#### Import JSON

```json
{
  "mcpServers": {
    "geoserver-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/openlang-cn/geoserver-mcp.git",
        "geoserver-mcp"
      ],
      "env": {
        "GEOSERVER_URL": "http://your-geoserver:8080/geoserver",
        "GEOSERVER_USER": "admin",
        "GEOSERVER_PASSWORD": "geoserver"
      }
    }
  }
}
```

#### Manual 1Panel fields

- Name: `geoserver-mcp`
- Type: `适合 uvx 启动的 mcp`
- Start command: `uvx --from git+https://github.com/openlang-cn/geoserver-mcp.git geoserver-mcp`
- External access path: `http://<your-server-ip>:8084`
- Output type: `streamableHttp`
- SSE path: `/geoserver-mcp`
- Image: `supercorp/supergateway:uvx`
- Container name: `geoserver-mcp`
- Port: `8084`

#### Environment variables

```text
GEOSERVER_URL=http://your-geoserver:8080/geoserver
GEOSERVER_USER=admin
GEOSERVER_PASSWORD=geoserver
GEOSERVER_STORAGE_PATH=/data
```

#### Optional mount

```text
Host path: /your/local/data
Container path: /data
```

#### Codex config

```json
{
  "mcpServers": {
    "geoserver-mcp": {
      "type": "streamable-http",
      "url": "http://<your-server-ip>:8084/geoserver-mcp"
    }
  }
}
```

### Which one should I choose?

- Try `uvx + streamableHttp` first
- If your 1Panel build does not behave well with `streamableHttp`, fall back to `uvx + sse`

---

## File Storage and `--storage`

If you want MCP tools to read local files such as Shapefiles, GeoPackages, or SLD files, use a storage root:

```bash
python -m geoserver_mcp.main --storage D:/data
```

Relative paths will be resolved under that root.

Examples:

```text
roads.zip -> D:/data/roads.zip
style/demo.sld -> D:/data/style/demo.sld
```

For Docker / 1Panel:

- `GEOSERVER_STORAGE_PATH` should point to the container path
- the matching host directory must be mounted into the container

---

## Available Tools

### Resource Endpoints

- `geoserver://catalog/workspaces`
- `geoserver://catalog/layers/{workspace}/{layer}`
- `geoserver://services/wms/{request}`
- `geoserver://services/wfs/{request}`

### Workspaces / Layers / Stores

- `list_workspaces`
- `create_workspace`
- `get_workspace`
- `get_default_workspace`
- `set_default_workspace`
- `get_layer_info`
- `list_layers`
- `create_layer`
- `delete_resource`
- `query_features`
- `generate_map`
- `create_datastore`
- `create_featurestore`
- `create_gpkg_datastore`
- `create_shp_datastore`
- `create_coveragestore`
- `delete_coveragestore`
- `get_coveragestore`
- `get_coveragestores`
- `get_datastore`
- `get_datastores`
- `get_featurestore`
- `delete_featurestore`

### Layer Groups

- `create_layergroup`
- `get_layergroup`
- `get_layergroups`
- `add_layer_to_layergroup`
- `remove_layer_from_layergroup`
- `delete_layergroup`
- `update_layergroup`

### Feature Types

- `publish_featurestore`
- `publish_featurestore_sqlview`
- `edit_featuretype`
- `get_featuretypes`
- `get_feature_attribute`

### Styles

- `create_style`
- `upload_style`
- `get_style`
- `get_styles`
- `publish_style`
- `create_catagorized_featurestyle`
- `create_classified_featurestyle`
- `create_coveragestyle`
- `create_outline_featurestyle`

### Style XML Helpers

- `style_catagorize_xml`
- `style_classified_xml`
- `style_coverage_style_colormapentry`
- `style_coverage_style_xml`
- `style_outline_only_xml`

### Security

- `create_user`
- `delete_user`
- `get_all_users`
- `modify_user`
- `create_usergroup`
- `delete_usergroup`
- `get_all_usergroups`

### System

- `get_manifest`
- `get_status`
- `get_system_status`
- `get_version`
- `reload_geoserver`
- `reset_geoserver`
- `update_service`
- `publish_time_dimension_to_coveragestore`

---

## Development

### Run tests

```bash
pytest tests -q
```

### Syntax check

```bash
python -m py_compile src/geoserver_mcp/main.py
```

### Use a specific branch with uvx

```bash
uvx --from git+https://github.com/openlang-cn/geoserver-mcp.git@codex/geoserver-mcp-light-engineering geoserver-mcp
```

---

## License

MIT
