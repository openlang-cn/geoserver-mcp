FROM python:3.10-slim

LABEL org.opencontainers.image.title="open-geoserver-mcp" \
      org.opencontainers.image.description="GeoServer MCP server packaged for container deployment" \
      org.opencontainers.image.licenses="MIT"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    GEOSERVER_URL="http://localhost:8080/geoserver" \
    GEOSERVER_USER="admin" \
    GEOSERVER_PASSWORD="geoserver" \
    GEOSERVER_STORAGE_PATH="/data" \
    MCP_TRANSPORT="streamable-http" \
    MCP_HOST="0.0.0.0" \
    MCP_PORT="8000" \
    MCP_MOUNT_PATH="/" \
    MCP_SSE_PATH="/sse" \
    MCP_MESSAGE_PATH="/messages/" \
    MCP_STREAMABLE_HTTP_PATH="/mcp"

WORKDIR /app

RUN useradd --create-home --uid 10001 appuser

COPY LICENSE README.md pyproject.toml ./
COPY src ./src

RUN python -m pip install --upgrade pip \
    && python -m pip install .

USER appuser

EXPOSE 8000

CMD ["sh", "-c", "geoserver-mcp --transport \"${MCP_TRANSPORT}\" --host \"${MCP_HOST}\" --port \"${MCP_PORT}\" --mount-path \"${MCP_MOUNT_PATH}\" --sse-path \"${MCP_SSE_PATH}\" --message-path \"${MCP_MESSAGE_PATH}\" --streamable-http-path \"${MCP_STREAMABLE_HTTP_PATH}\""]

