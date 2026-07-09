# Repository Guidelines

## 项目结构与模块组织
本仓库是一个基于 Python 的 GeoServer MCP 服务，整体结构较小，核心逻辑集中。

- `src/geoserver_mcp/main.py`：服务入口，定义绝大多数 MCP 工具。
- `src/geoserver_mcp/__init__.py`：包初始化文件。
- `examples/client.py`：最小客户端调用示例。
- `docs/`：详细文档目录，按 `getting-started/`、`deployment/`、`mcp/`、`development/`、`maintainers/`、`internal/` 分类存放；图片与演示资源也保留在此目录。
- `deploy/`：部署资产目录，包含 `Dockerfile`、`docker-compose.yml`、`.env.example` 等容器与托管部署文件。
- `README.md`：项目入口文档，只保留概览、快速开始与文档导航。
- `tests/`：`pytest` 测试目录，覆盖工具封装、参数处理与示例行为。

## 构建、测试与开发命令
- `uv venv --python=3.10`：创建推荐的 Python 虚拟环境。
- `uv pip install -e .`：以可编辑模式安装，便于本地开发。
- `geoserver-mcp --url http://localhost:8080/geoserver --user admin --password geoserver --debug`：通过 CLI 启动服务。
- `python -m geoserver_mcp.main --storage D:/data`：直接运行模块，并指定文件存储根目录。
- `docker build -f deploy/Dockerfile -t geoserver-mcp .`：构建 Docker 镜像。
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

## 版本、依赖与发布策略
本仓库作为公开发布的开源项目，后续 AI 或维护者在处理版本、依赖和发版时必须遵循以下规则：

- 项目版本独立于依赖版本管理；`open-geoserver-mcp` 的版本号不能简单跟随 `mcp` 或 `geoserver-rest` 的版本号。
- 每次正式发版都必须同步维护三处：`pyproject.toml` 中的项目版本、`src/geoserver_mcp/__init__.py` 中的 `__version__`、`CHANGELOG.md` 中对应版本条目。
- 每次正式发布都应保留完整发布痕迹：Git tag 使用 `vX.Y.Z` 格式，GitHub Release 与 PyPI 版本保持一致；历史 tag、Release、PyPI 版本不得覆盖、重写或删除。
- 旧版本默认保留且可回溯；除非出现严重发布错误或安全问题，不对既有版本做删除操作。如确需处理，应优先考虑 PyPI yank，而不是移除历史版本。
- 依赖升级时必须先评估兼容性，再决定项目版本号：
  - 仅修复兼容性或内部实现、不改变公开接口时，优先发 `PATCH`。
  - 新增 MCP tool/resource/参数且保持向后兼容时，发 `MINOR`。
  - 删除、重命名、改变默认行为、提高最低支持版本或破坏现有调用时，发 `MAJOR`。
- 升级 `mcp`、`geoserver-rest` 或其他关键依赖时，必须同步更新：
  - `pyproject.toml` 中的依赖声明；
  - `README.md` 中的兼容性、安装或使用说明；
  - `CHANGELOG.md` 中的升级说明、影响范围和迁移提示（如有）。
- 在项目早期可继续使用精确依赖版本（如 `==`）保证可重复性；如果后续改为区间版本（如 `>=,<`），必须先补充 CI 验证矩阵，再放宽依赖范围。
- 发版前至少完成以下验证：`pytest tests -q`、语法/编译检查、构建分发包；若仓库已配置 CI，则确保 CI 配置与本地验证命令保持一致。
- 后续新增维护分支时，默认采用 `release/<major>.x` 命名；未明确建立维护分支前，默认只维护主分支上的最新稳定版本。
- 如果依赖升级导致旧版本不再兼容，必须通过 `CHANGELOG.md`、README 或 Release Notes 明确说明，不得让用户通过提交记录自行推断。

## MCP 工具变更要求
新增、删除或修改 MCP 工具时，必须同步更新 `README.md` 中的概览导航，以及 `docs/mcp/`、`docs/getting-started/`、`docs/deployment/` 下相关工具说明、参数示例和相关用法。如果工具涉及文件读写、认证或破坏性操作，应同时补充限制条件、默认行为和风险提示。

## 安全与配置建议
不要提交真实的 GeoServer 地址、用户名或密码。优先通过运行时参数 `--url`、`--user`、`--password` 或环境变量注入配置。使用 `--storage` 时，应将目录限制在受控路径下，避免访问无关文件。
