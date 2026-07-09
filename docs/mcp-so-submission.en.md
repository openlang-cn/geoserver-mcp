# GeoServer MCP Submission Draft for mcp.so

## Name

`GeoServer MCP`

## Repository

`https://github.com/openlang-cn/geoserver-mcp`

## Short Description

An MCP server for GeoServer that exposes workspace, datastore, layer, style, query, and system management capabilities through the GeoServer REST API.

## Long Description

GeoServer MCP is a Model Context Protocol server for MCP-compatible clients such as Codex, Cursor, and Claude Desktop.

It wraps the GeoServer REST API into MCP tools for:

- workspace management
- datastore / featurestore / coveragestore management
- layer and layer group management
- style creation and upload
- feature querying
- map URL generation
- GeoServer status and service operations

It supports:

- local stdio mode
- `uvx --from git+...` launch from GitHub
- `uvx open-geoserver-mcp` launch after PyPI publication
- Docker deployment
- remote `streamable-http`
- remote `sse`
- 1Panel deployment

## Launch Options

### Run from GitHub with uvx

```bash
uvx --from git+https://github.com/openlang-cn/geoserver-mcp.git geoserver-mcp
```

### Run from PyPI with uvx (after publishing)

```bash
uvx open-geoserver-mcp
```

### Run with GeoServer parameters

```bash
uvx --from git+https://github.com/openlang-cn/geoserver-mcp.git geoserver-mcp \
  --url http://localhost:8080/geoserver \
  --user admin \
  --password geoserver
```

### Remote streamable-http

```bash
geoserver-mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

Default endpoint:

```text
http://<host>:8000/mcp
```

## Required Environment Variables

- `GEOSERVER_URL`
- `GEOSERVER_USER`
- `GEOSERVER_PASSWORD`

Optional:

- `GEOSERVER_STORAGE_PATH`

## Package Naming

- PyPI package: `open-geoserver-mcp`
- CLI command: `geoserver-mcp`

## Example MCP Client Config

### Command-based

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
        "GEOSERVER_URL": "http://localhost:8080/geoserver",
        "GEOSERVER_USER": "admin",
        "GEOSERVER_PASSWORD": "geoserver"
      }
    }
  }
}
```

### Remote streamable-http

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

## Suggested Tags

`geoserver`, `gis`, `geospatial`, `maps`, `wms`, `wfs`, `ogc`, `mcp`
