FROM python:3.10-slim

ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    GEOSERVER_URL="http://localhost:8080/geoserver" \
    GEOSERVER_USER="admin" \
    GEOSERVER_PASSWORD="geoserver" \
    MCP_TRANSPORT="streamable-http" \
    MCP_HOST="0.0.0.0" \
    MCP_PORT="8000" \
    MCP_MOUNT_PATH="/" \
    MCP_SSE_PATH="/sse" \
    MCP_MESSAGE_PATH="/messages/" \
    MCP_STREAMABLE_HTTP_PATH="/mcp"

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl gcc build-essential \
    && python -m venv "$VIRTUAL_ENV" \
    && "$VIRTUAL_ENV/bin/pip" install --no-cache-dir geoserver-mcp \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

ENTRYPOINT ["sh", "-c", "geoserver-mcp --transport \"$MCP_TRANSPORT\" --host \"$MCP_HOST\" --port \"$MCP_PORT\" --mount-path \"$MCP_MOUNT_PATH\" --sse-path \"$MCP_SSE_PATH\" --message-path \"$MCP_MESSAGE_PATH\" --streamable-http-path \"$MCP_STREAMABLE_HTTP_PATH\" \"$@\"", "--"]
