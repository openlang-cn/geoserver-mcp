# Docker and 1Panel Deployment

## Repository Layout

The Docker deployment assets are grouped under `deploy/`:

- `deploy/Dockerfile`
- `deploy/docker-compose.yml`
- `deploy/.env.example`

This keeps the repository root cleaner while preserving a single deployment entrypoint folder.

## When to Use Docker

Docker is recommended for:

- remote MCP service deployment
- long-running server processes
- 1Panel or Compose-based hosting
- environments where you do not want to manage Python directly

For local one-off usage, prefer:

```bash
uvx --from open-geoserver-mcp geoserver-mcp
```

## Quick Start with Docker Compose

1. Copy the environment template:

```bash
cp deploy/.env.example deploy/.env
```

2. Edit `.env` and set at least:

```env
GEOSERVER_URL=http://your-geoserver:8080/geoserver
GEOSERVER_USER=admin
GEOSERVER_PASSWORD=geoserver
```

3. Start the service:

```bash
docker compose --env-file deploy/.env -f deploy/docker-compose.yml up --build -d
```

4. Check logs:

```bash
docker compose --env-file deploy/.env -f deploy/docker-compose.yml logs -f geoserver-mcp
```

Default remote endpoint in `streamable-http` mode:

```text
http://127.0.0.1:8000/mcp
```

## Build and Run with Docker

Build the image from the current source tree:

```bash
docker build -f deploy/Dockerfile -t open-geoserver-mcp:local .
```

Run the container:

```bash
docker run --rm -p 8000:8000 \
  -e GEOSERVER_URL=http://host.docker.internal:8080/geoserver \
  -e GEOSERVER_USER=admin \
  -e GEOSERVER_PASSWORD=geoserver \
  -e GEOSERVER_STORAGE_PATH=/data \
  -v ./data:/data \
  open-geoserver-mcp:local
```

## Environment Variables

Required:

- `GEOSERVER_URL`
- `GEOSERVER_USER`
- `GEOSERVER_PASSWORD`

Storage:

- `GEOSERVER_STORAGE_HOST_PATH`: host path mounted into the container in Compose
- `GEOSERVER_STORAGE_PATH`: in-container storage root, default `/data`

MCP transport:

- `MCP_TRANSPORT`: `streamable-http` or `sse`
- `MCP_HOST`: bind host, default `0.0.0.0`
- `MCP_PORT`: bind port, default `8000`
- `MCP_MOUNT_PATH`: HTTP mount root, default `/`
- `MCP_SSE_PATH`: SSE path, default `/sse`
- `MCP_MESSAGE_PATH`: SSE message path, default `/messages/`
- `MCP_STREAMABLE_HTTP_PATH`: Streamable HTTP path, default `/mcp`

## Storage and Volume Mapping

The default Compose setup binds:

```text
../data -> /data
```

This keeps file-based operations predictable for shapefiles, GeoPackages, and SLD files. If you change the container path, keep `GEOSERVER_STORAGE_PATH` and the Compose volume target aligned.

## 1Panel Usage

Two recommended approaches:

1. Remote deployment mode: deploy this project as a remote MCP service and connect directly by URL.
2. Imported MCP config mode: let 1Panel launch the project with `uvx`, then expose `sse` or `streamableHttp`.

### Option A: 1Panel remote deployment

Use `deploy/docker-compose.yml`.

Recommended `.env` values:

```env
GEOSERVER_URL=http://your-geoserver:8080/geoserver
GEOSERVER_USER=admin
GEOSERVER_PASSWORD=geoserver
GEOSERVER_STORAGE_HOST_PATH=../data
GEOSERVER_STORAGE_PATH=/data
MCP_TRANSPORT=streamable-http
MCP_PORT=8000
MCP_STREAMABLE_HTTP_PATH=/mcp
```

Then:

1. Import `deploy/docker-compose.yml` into 1Panel.
2. Start the service.
3. Add a website or reverse proxy in 1Panel:

```text
https://your-domain.com/mcp -> http://127.0.0.1:8000/mcp
```

Client config:

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

If 1Panel supports importing standard `mcpServers` JSON, use this template:

```json
{
  "mcpServers": {
    "geoserver-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "open-geoserver-mcp",
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

Still requires manual input in 1Panel:

- external access path
- output type
- SSE path
- image
- container name
- port
- mounts

Notes:

- Keep the launcher in default `stdio` mode.
- Do not add `--transport streamable-http` to the imported command.
- Let 1Panel handle the conversion to `sse` or `streamableHttp`.

## Choosing `streamable-http` or `sse`

- Prefer `streamable-http` first.
- Fall back to `sse` when an older client or gateway handles it more reliably.
