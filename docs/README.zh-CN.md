[English README](../README.md)

# GeoServer MCP Server

一个面向 GeoServer 的 MCP（Model Context Protocol）服务。  
它把 `GeoServer REST API` 封装为一组 MCP 工具，供 Codex、Cursor、Claude Desktop 等支持 MCP 的客户端调用。

---

## 功能概览

- 管理工作区、数据存储、要素存储、栅格存储、图层、图层组
- 查询图层详情、查询要素、生成地图访问参数
- 管理样式、上传 SLD、生成样式 XML
- 查询系统状态、版本信息、重载和重置 GeoServer
- 支持本地 `stdio` 启动
- 支持远程 `streamable-http` / `sse` 启动
- 支持通过 `uvx --from git+...` 直接从 GitHub 拉起

---

## 项目结构

```text
src/geoserver_mcp/
├─ main.py          # CLI 入口
├─ server.py        # FastMCP 服务工厂与注册
├─ connection.py    # GeoServer 连接创建
├─ client.py        # geoserver-rest 兼容封装
├─ resources.py     # MCP 资源端点
├─ utils.py         # 通用工具函数
└─ tools/
   ├─ catalog.py    # 工作区、图层、存储、图层组、要素类型
   ├─ styles.py     # 样式与 SLD XML
   ├─ security.py   # 用户与用户组
   └─ system.py     # 状态、版本、服务配置
```

其他重要文件：

- `examples/client.py`：示例客户端
- `tests/`：基础测试
- `Dockerfile`：容器镜像构建
- `docker-compose.yml`：远程部署 / 1Panel Compose 示例
- `.env.example`：环境变量模板

---

## 环境要求

- Python `3.10+`
- 可访问的 GeoServer 实例
- GeoServer 开启 REST API

推荐依赖版本：

- `mcp==1.28.1`
- `geoserver-rest==2.10.0`

## 包名说明

- PyPI 包名：`open-geoserver-mcp`
- CLI 命令名：`geoserver-mcp`
- 从 GitHub 直接启动的方式仍然是：`uvx --from git+https://github.com/openlang-cn/geoserver-mcp.git geoserver-mcp`

---

## 安装方式

### 我该用哪种方式？

可以按下面的场景来选：

- **本地开发 / 本地调试**：用 `uv` 本地安装运行，不需要 Docker
- **临时使用 / 不想安装项目**：用 `uvx --from git+...`
- **已发布到 PyPI / 不想依赖 Git**：发布后用 `uvx open-geoserver-mcp`
- **服务器长期运行 / 提供远程 MCP URL**：用 Docker
- **1Panel 托管远程服务**：优先用 `docker-compose.yml`
- **1Panel 导入 MCP 配置**：用 `uvx` 导入模式

一句话理解：

- **本地开发**：`uv`
- **临时启动**：`uvx`
- **PyPI 启动**：`uvx open-geoserver-mcp`
- **远程部署**：Docker
- **面板管理**：1Panel

### 方式一：本地开发 / 本地运行

```bash
uv venv --python=3.10
```

Windows PowerShell：

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux / macOS：

```bash
source .venv/bin/activate
```

安装项目：

```bash
uv pip install -e .
```

安装开发依赖：

```bash
uv pip install -e ".[dev]"
```

### 方式二：通过 GitHub + uvx 直接运行

如果你不想先安装项目，可以直接从公开 GitHub 仓库启动：

```bash
uvx --from git+https://github.com/openlang-cn/geoserver-mcp.git geoserver-mcp --help
```

连接 GeoServer：

```bash
uvx --from git+https://github.com/openlang-cn/geoserver-mcp.git geoserver-mcp \
  --url http://localhost:8080/geoserver \
  --user admin \
  --password geoserver
```

### 方式二补充：发布到 PyPI 后通过 uvx 运行

```bash
uvx open-geoserver-mcp --help
```

连接 GeoServer：

```bash
uvx open-geoserver-mcp \
  --url http://localhost:8080/geoserver \
  --user admin \
  --password geoserver
```

从 PyPI 安装：

```bash
pip install open-geoserver-mcp
```

安装后的 CLI 命令仍然是：

```bash
geoserver-mcp --help
```

### 方式三：Docker

Docker 主要用于：

- 服务器部署
- 远程 MCP 服务
- 1Panel / Compose 管理
- 不想手动维护 Python 运行环境

本地开发和本地调试 **不要求** 使用 Docker。

如果你的容器镜像里没有 `git`，发布到 PyPI 后应优先改用：

```bash
uvx open-geoserver-mcp
```

构建镜像：

```bash
docker build -t geoserver-mcp .
```

容器默认以远程 `streamable-http` 模式运行，可通过环境变量控制：

```bash
docker run --rm -p 8000:8000 \
  -e GEOSERVER_URL=http://host.docker.internal:8080/geoserver \
  -e GEOSERVER_USER=admin \
  -e GEOSERVER_PASSWORD=geoserver \
  geoserver-mcp
```

---

## 启动方式

### 1）本地 stdio 模式

适合 Claude Desktop、Cursor 本地命令启动型配置。

```bash
geoserver-mcp --url http://localhost:8080/geoserver --user admin --password geoserver
```

或者：

```bash
python -m geoserver_mcp.main --url http://localhost:8080/geoserver --user admin --password geoserver
```

### 2）远程 Streamable HTTP 模式

适合公网 / 局域网部署，由客户端直接连接 MCP URL。

```bash
geoserver-mcp \
  --transport streamable-http \
  --host 0.0.0.0 \
  --port 8000
```

默认远程地址：

```text
http://<host>:8000/mcp
```

### 3）远程 SSE 模式

适合需要兼容旧客户端时使用。

```bash
geoserver-mcp \
  --transport sse \
  --host 0.0.0.0 \
  --port 8000
```

默认路径：

- SSE：`/sse`
- Message：`/messages/`

### 常用参数

- `--url`：GeoServer 地址
- `--user`：GeoServer 用户名
- `--password`：GeoServer 密码
- `--storage`：文件读写根目录
- `--transport`：`stdio` / `sse` / `streamable-http`
- `--host`：监听地址
- `--port`：监听端口
- `--mount-path`：HTTP 根路径
- `--sse-path`：SSE 路径
- `--message-path`：SSE 消息路径
- `--streamable-http-path`：Streamable HTTP 路径

---

## 客户端配置示例

### 本地命令模式

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

### 远程 Streamable HTTP 模式

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

### 远程 SSE 模式

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

## 1Panel 使用方式

当前推荐两种方式：

1. **远程部署模式**：1Panel 部署本项目为远程 MCP 服务，客户端直接连 URL
2. **导入配置模式**：1Panel 通过 `uvx` 启动本项目，再由平台输出 `sse` 或 `streamableHttp`

### 方案 A：1Panel 远程部署

推荐使用仓库内的 `docker-compose.yml`。

1. 复制环境变量模板：

```bash
cp .env.example .env
```

2. 修改 `.env`：

```env
GEOSERVER_URL=http://your-geoserver:8080/geoserver
GEOSERVER_USER=admin
GEOSERVER_PASSWORD=geoserver
MCP_TRANSPORT=streamable-http
MCP_PORT=8000
MCP_STREAMABLE_HTTP_PATH=/mcp
```

3. 在 1Panel 中导入 `docker-compose.yml`
4. 启动服务
5. 通过 1Panel 网站 / 反向代理暴露：

```text
https://your-domain.com/mcp -> http://127.0.0.1:8000/mcp
```

Codex 配置：

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

### 方案 B：1Panel 导入配置

如果你的 1Panel 支持导入标准 `mcpServers` JSON，可使用下面的导入模板。

#### 导入 JSON 模板

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

#### 导入 JSON 能自动填充的内容

- `command`
- `args`
- `env`

#### 导入后仍需手动填写的 1Panel 字段

- 外部访问路径
- 输出类型
- SSE 路径
- 镜像
- 容器名称
- 端口
- 挂载

#### 注意

- 这里推荐保持默认 `stdio` 启动
- 不要在导入 JSON 的命令里额外添加 `--transport streamable-http`
- 让 1Panel 平台负责把进程包装成 `sse` 或 `streamableHttp`

---

## 1Panel 完整可复制模板

### 模板一：`uvx + sse`

#### 导入 JSON

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

#### 1Panel 手填字段

- 名称：`geoserver-mcp`
- 类型：`适合 uvx 启动的 mcp`
- 启动命令：`uvx --from git+https://github.com/openlang-cn/geoserver-mcp.git geoserver-mcp`
- 外部访问路径：`http://<your-server-ip>:8084`
- 输出类型：`sse`
- SSE 路径：`/geoserver-mcp`
- 镜像：`supercorp/supergateway:uvx`
- 容器名称：`geoserver-mcp`
- 端口：`8084`

#### 环境变量

```text
GEOSERVER_URL=http://your-geoserver:8080/geoserver
GEOSERVER_USER=admin
GEOSERVER_PASSWORD=geoserver
GEOSERVER_STORAGE_PATH=/data
```

#### 可选挂载

```text
Host path: /your/local/data
Container path: /data
```

#### Codex 配置

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

### 模板二：`uvx + streamableHttp`

#### 导入 JSON

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

#### 1Panel 手填字段

- 名称：`geoserver-mcp`
- 类型：`适合 uvx 启动的 mcp`
- 启动命令：`uvx --from git+https://github.com/openlang-cn/geoserver-mcp.git geoserver-mcp`
- 外部访问路径：`http://<your-server-ip>:8084`
- 输出类型：`streamableHttp`
- SSE 路径：`/geoserver-mcp`
- 镜像：`supercorp/supergateway:uvx`
- 容器名称：`geoserver-mcp`
- 端口：`8084`

#### 环境变量

```text
GEOSERVER_URL=http://your-geoserver:8080/geoserver
GEOSERVER_USER=admin
GEOSERVER_PASSWORD=geoserver
GEOSERVER_STORAGE_PATH=/data
```

#### 可选挂载

```text
Host path: /your/local/data
Container path: /data
```

#### Codex 配置

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

### 怎么选

- 优先尝试：`uvx + streamableHttp`
- 如果你的 1Panel 对 `streamableHttp` 支持不稳定：退回 `uvx + sse`

---

## 文件存储与 `--storage`

如果你需要让 MCP 工具读取本地文件（例如 Shapefile、GeoPackage、SLD 文件），可以指定存储根目录：

```bash
python -m geoserver_mcp.main --storage D:/data
```

这样相对路径会被解析到该根目录下。

示例：

```text
roads.zip -> D:/data/roads.zip
style/demo.sld -> D:/data/style/demo.sld
```

Docker / 1Panel 中使用时，要同时确保：

- `GEOSERVER_STORAGE_PATH` 指向容器内路径
- 对应宿主机目录已经挂载到容器

---

## 可用工具

### 资源端点

- `geoserver://catalog/workspaces`
- `geoserver://catalog/layers/{workspace}/{layer}`
- `geoserver://services/wms/{request}`
- `geoserver://services/wfs/{request}`

### 工作区 / 图层 / 存储

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

### 图层组

- `create_layergroup`
- `get_layergroup`
- `get_layergroups`
- `add_layer_to_layergroup`
- `remove_layer_from_layergroup`
- `delete_layergroup`
- `update_layergroup`

### 要素类型

- `publish_featurestore`
- `publish_featurestore_sqlview`
- `edit_featuretype`
- `get_featuretypes`
- `get_feature_attribute`

### 样式

- `create_style`
- `upload_style`
- `get_style`
- `get_styles`
- `publish_style`
- `create_catagorized_featurestyle`
- `create_classified_featurestyle`
- `create_coveragestyle`
- `create_outline_featurestyle`

### 样式 XML 辅助

- `style_catagorize_xml`
- `style_classified_xml`
- `style_coverage_style_colormapentry`
- `style_coverage_style_xml`
- `style_outline_only_xml`

### 安全

- `create_user`
- `delete_user`
- `get_all_users`
- `modify_user`
- `create_usergroup`
- `delete_usergroup`
- `get_all_usergroups`

### 系统

- `get_manifest`
- `get_status`
- `get_system_status`
- `get_version`
- `reload_geoserver`
- `reset_geoserver`
- `update_service`
- `publish_time_dimension_to_coveragestore`

---

## 开发说明

### 运行测试

```bash
pytest tests -q
```

### 语法检查

```bash
python -m py_compile src/geoserver_mcp/main.py
```

### 当前分支开发

如果你想让 1Panel / uvx 固定拉某个分支，可以这样：

```bash
uvx --from git+https://github.com/openlang-cn/geoserver-mcp.git@codex/geoserver-mcp-light-engineering geoserver-mcp
```

---

## License

MIT
