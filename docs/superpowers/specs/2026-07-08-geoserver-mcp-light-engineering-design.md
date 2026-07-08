# GeoServer MCP 轻量工程化设计

## 目标
- 补齐 `geo.Geoserver` 中当前项目缺失的高频 MCP 能力。
- 将单文件实现拆分为轻量模块结构，降低维护成本。
- 为新增与关键包装逻辑补充基础自动化测试。

## 范围
本次优先补充以下工具：
- `get_workspace`
- `get_default_workspace`
- `set_default_workspace`
- `get_featurestore`
- `delete_featurestore`
- `get_style`
- `get_styles`
- `upload_style`

同时修正一批现有高风险错配：
- `create_style` 改为通过底层 `upload_style` 实现。
- `create_datastore`、`create_coveragestore`、`create_gpkg_datastore`、`create_shp_datastore` 统一做参数适配。
- `delete_resource` 统一走兼容层，避免调用底层不存在的方法名。

## 架构
- `src/geoserver_mcp/main.py`：仅保留 CLI 入口。
- `src/geoserver_mcp/server.py`：创建 `FastMCP` 并注册资源和工具。
- `src/geoserver_mcp/connection.py`：读取环境变量并创建连接。
- `src/geoserver_mcp/client.py`：对 `geo.Geoserver` 做兼容封装，补齐缺失方法并统一参数格式。
- `src/geoserver_mcp/utils.py`：通用辅助方法。
- `src/geoserver_mcp/tools/`：按目录、样式、安全、系统拆分工具定义。
- `src/geoserver_mcp/resources.py`：资源端点定义。

## 测试策略
- 使用 `pytest`。
- 以 mock 为主，不依赖真实 GeoServer。
- 优先覆盖：
  - 新增 8 个工具的参数转发；
  - 兼容层中关键适配逻辑；
  - 存储路径解析与连接缺失处理。

## 风险与约束
- 不做重型框架化改造。
- 保持现有 CLI 入口和已有 MCP 工具名兼容。
- 对底层 `geoserver-rest` 不存在的公开方法，通过兼容层封装补齐，而不是直接修改第三方依赖。
