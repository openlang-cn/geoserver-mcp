# Client Configuration

## Local command mode

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

## Remote `streamable-http` mode

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

## Remote `sse` mode

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
