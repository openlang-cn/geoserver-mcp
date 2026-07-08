# Repository Guidelines

## 项目结构与模块组织
本仓库是一个基于 Python 的 GeoServer MCP 服务，整体结构较小，核心逻辑集中。

- `src/geoserver_mcp/main.py`：服务入口，定义绝大多数 MCP 工具。
- `src/geoserver_mcp/__init__.py`：包初始化文件。
- `examples/client.py`：最小客户端调用示例。
- `docs/`：README 使用的图片与演示资源。
- `README.md`：安装、配置、工具说明的主文档。

当前没有独立的 `tests/` 目录；新增非 trivial 功能时，应补充 `tests/` 下的测试文件。

## 构建、测试与开发命令
- `uv venv --python=3.10`：创建推荐的 Python 虚拟环境。
- `uv pip install -e .`：以可编辑模式安装，便于本地开发。
- `geoserver-mcp --url http://localhost:8080/geoserver --user admin --password geoserver --debug`：通过 CLI 启动服务。
- `python -m geoserver_mcp.main --storage D:/data`：直接运行模块，并指定文件存储根目录。
- `docker build -t geoserver-mcp .`：构建 Docker 镜像。
- `pytest`：运行测试；如仅验证局部变更，可用 `pytest tests/test_xxx.py`。

## 代码风格与命名规范
遵循 Python 常规风格：4 空格缩进、函数和变量使用 `snake_case`、类名使用 `PascalCase`。新增 MCP 工具时，名称应与功能直接对应，避免缩写与含糊命名。优先提取小型辅助函数，避免在 `main.py` 中复制环境变量、路径解析或请求处理逻辑。除非必要，不添加单字母变量和多余的行内注释。

## 测试规范
新增功能、缺陷修复或参数处理逻辑时，应补充 `pytest` 测试。测试文件命名为 `test_*.py`，放在 `tests/` 目录下。优先覆盖参数解析、路径处理、异常分支和 GeoServer 调用边界；涉及外部服务时尽量使用 mock，避免依赖真实 GeoServer 实例。

## 提交与合并请求规范
提交信息沿用简短、祈使句风格，例如 `Fix HTML entities in README.md`、`Storage can be configured now`。建议使用“动词 + 具体改动”的格式，例如 `Add workspace validation for style tools`。

PR 至少应包含：变更摘要、关联 Issue（如有）、本地验证步骤、对 README 或示例的同步更新。仅当文档图片或演示资源变更时再附截图。

## 分支与发布规范
功能开发建议使用 `feature/<topic>`，缺陷修复使用 `fix/<topic>`，文档调整使用 `docs/<topic>`。发布版本前同步更新 `pyproject.toml` 中的版本号，并检查 `README.md` 中示例命令、安装说明和工具清单是否仍然准确。

## MCP 工具变更要求
新增、删除或修改 MCP 工具时，必须同步更新 `README.md` 中的工具说明、参数示例和相关用法。如果工具涉及文件读写、认证或破坏性操作，应同时补充限制条件、默认行为和风险提示。

## 安全与配置建议
不要提交真实的 GeoServer 地址、用户名或密码。优先通过运行时参数 `--url`、`--user`、`--password` 或环境变量注入配置。使用 `--storage` 时，应将目录限制在受控路径下，避免访问无关文件。
