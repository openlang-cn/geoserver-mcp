# GeoServer MCP 提交到 mcp.so 的文案草稿

## 名称

`GeoServer MCP`

## 仓库地址

`https://github.com/openlang-cn/geoserver-mcp`

## 简短描述

一个面向 GeoServer 的 MCP 服务，通过 GeoServer REST API 暴露工作区、数据源、图层、样式、查询和系统管理能力。

## 详细描述

GeoServer MCP 是一个面向 Codex、Cursor、Claude Desktop 等 MCP 客户端的 Model Context Protocol 服务。

它将 GeoServer REST API 封装为一组 MCP 工具，覆盖：

- 工作区管理
- 数据存储 / 要素存储 / 栅格存储管理
- 图层与图层组管理
- 样式创建与上传
- 要素查询
- 地图访问参数生成
- GeoServer 状态与服务管理

支持的使用方式：

- 本地 `stdio`
- 通过 `uvx --from git+...` 从 GitHub 直接启动
- Docker 部署
- 远程 `streamable-http`
- 远程 `sse`
- 1Panel 部署

## 启动方式

### 通过 GitHub + uvx 启动

```bash
uvx --from git+https://github.com/openlang-cn/geoserver-mcp.git geoserver-mcp
```

### 带 GeoServer 参数启动

```bash
uvx --from git+https://github.com/openlang-cn/geoserver-mcp.git geoserver-mcp \
  --url http://localhost:8080/geoserver \
  --user admin \
  --password geoserver
```

### 远程 Streamable HTTP 模式

```bash
geoserver-mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

默认访问地址：

```text
http://<host>:8000/mcp
```

## 必需环境变量

- `GEOSERVER_URL`
- `GEOSERVER_USER`
- `GEOSERVER_PASSWORD`

可选：

- `GEOSERVER_STORAGE_PATH`

## MCP 客户端示例配置

### 命令模式

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

### 远程 streamable-http

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

## 建议标签

`geoserver`、`gis`、`geospatial`、`maps`、`wms`、`wfs`、`ogc`、`mcp`
