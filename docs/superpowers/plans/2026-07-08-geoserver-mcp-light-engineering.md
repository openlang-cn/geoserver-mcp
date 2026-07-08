# GeoServer MCP Light Engineering Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 补齐常用 GeoServer MCP 工具覆盖，并将项目拆分为轻量可维护结构。

**Architecture:** 引入一个 `GeoServerClient` 兼容层统一封装第三方 `geo.Geoserver`，让工具模块只处理 MCP 参数与响应。将工具按目录、样式、安全、系统拆分，`main.py` 仅保留启动逻辑。

**Tech Stack:** Python 3.10+, FastMCP, geoserver-rest, pytest

---

### Task 1: 建立模块骨架

**Files:**
- Create: `src/geoserver_mcp/client.py`
- Create: `src/geoserver_mcp/connection.py`
- Create: `src/geoserver_mcp/utils.py`
- Create: `src/geoserver_mcp/server.py`
- Create: `src/geoserver_mcp/resources.py`
- Create: `src/geoserver_mcp/tools/__init__.py`

- [ ] 抽出连接、兼容层与注册入口。
- [ ] 保持 `geoserver-mcp` CLI 入口不变。

### Task 2: 拆分并补齐目录/样式工具

**Files:**
- Create: `src/geoserver_mcp/tools/catalog.py`
- Create: `src/geoserver_mcp/tools/styles.py`
- Modify: `src/geoserver_mcp/main.py`

- [ ] 迁移现有工作区、图层、数据源、图层组、要素类型工具。
- [ ] 增加缺失的工作区、featurestore、样式查询/上传工具。
- [ ] 修复与底层 `geo` 方法签名不一致的包装逻辑。

### Task 3: 拆分安全与系统工具

**Files:**
- Create: `src/geoserver_mcp/tools/security.py`
- Create: `src/geoserver_mcp/tools/system.py`

- [ ] 迁移用户/用户组、状态、版本、重载等工具。
- [ ] 保证所有工具注册仍由统一 `server.py` 负责。

### Task 4: 编写测试

**Files:**
- Create: `tests/test_client.py`
- Create: `tests/test_catalog_tools.py`
- Create: `tests/test_style_tools.py`
- Modify: `pyproject.toml`

- [ ] 增加 `pytest` 开发依赖。
- [ ] 为兼容层和新增工具编写 mock 测试。
- [ ] 验证关键包装逻辑与参数适配。

### Task 5: 更新文档与验证

**Files:**
- Modify: `README.md`

- [ ] 更新 README 工具清单。
- [ ] 运行 `pytest` 与 `python -m py_compile`。
- [ ] 确认 CLI 入口仍可导入启动。
