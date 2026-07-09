# PyPI Package Name Design

## 背景

当前仓库的 CLI 命令为 `geoserver-mcp`，但 PyPI 上同名项目已存在，不适合作为新的公开发布包名。

## 目标

- 将 PyPI 包名调整为 `open-geoserver-mcp`
- 保持 CLI 命令 `geoserver-mcp` 不变
- 同步更新中英文文档中的安装与发布说明
- 增加 GitHub Actions 发布工作流，便于后续接入 PyPI Trusted Publishing

## 设计决策

### 包名与命令分离

- 包名：`open-geoserver-mcp`
- 命令名：`geoserver-mcp`

这样可以避免 PyPI 名称冲突，同时不破坏现有命令行和 MCP 客户端配置习惯。

### 文档策略

- 保留从 GitHub 直接运行的示例
- 增加“发布到 PyPI 后”的安装和 `uvx` 启动示例
- 明确说明在 1Panel / 容器缺少 `git` 时，应优先使用 PyPI 包方式

### 发布策略

- 仓库中增加 GitHub Actions 工作流
- 工作流负责构建发行包并发布到 PyPI
- 实际发布前仍需在 PyPI 后台配置 Trusted Publisher
