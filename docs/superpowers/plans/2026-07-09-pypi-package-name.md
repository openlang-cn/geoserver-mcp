# PyPI Package Name Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将公开发布包名调整为 `open-geoserver-mcp`，同时保持 `geoserver-mcp` CLI 兼容，并同步文档与发布流程。

**Architecture:** 仅修改打包元数据、发布工作流和文档，不改动 Python 包路径与 CLI 入口。这样影响面最小，也不会破坏现有本地调用方式。

**Tech Stack:** Python packaging (`pyproject.toml`, `hatchling`), GitHub Actions, Markdown documentation

---

### Task 1: 更新包元数据

**Files:**
- Modify: `pyproject.toml`

- [ ] **Step 1: 修改 PyPI 包名**

将：

```toml
name = "geoserver-mcp"
```

改为：

```toml
name = "open-geoserver-mcp"
```

- [ ] **Step 2: 保持 CLI 入口不变**

确认保留：

```toml
[project.scripts]
geoserver-mcp = "geoserver_mcp.main:main"
```

### Task 2: 同步 README 与发布说明

**Files:**
- Modify: `README.md`
- Modify: `docs/README.zh-CN.md`
- Modify: `docs/mcp-so-submission.en.md`
- Modify: `docs/mcp-so-submission.zh.md`

- [ ] **Step 1: 增加包名说明**

在文档中明确：

```text
PyPI package: open-geoserver-mcp
CLI command: geoserver-mcp
```

- [ ] **Step 2: 增加 PyPI 安装与 uvx 示例**

加入：

```bash
uvx open-geoserver-mcp --help
pip install open-geoserver-mcp
```

- [ ] **Step 3: 说明容器无 git 时优先用 PyPI 包**

增加说明：

```text
If your container image does not include git, prefer uvx open-geoserver-mcp after publication.
```

### Task 3: 增加发布工作流

**Files:**
- Create: `.github/workflows/publish-pypi.yml`

- [ ] **Step 1: 新增 GitHub Actions 工作流**

工作流应包含：

```yaml
on:
  release:
    types: [published]
  workflow_dispatch:
```

- [ ] **Step 2: 构建并发布**

工作流分为：

```yaml
- build
- publish
```

其中 `publish` 使用：

```yaml
uses: pypa/gh-action-pypi-publish@release/v1
```

### Task 4: 验证

**Files:**
- Test: `pyproject.toml`
- Test: `README.md`

- [ ] **Step 1: 运行构建验证**

Run: `python -m build`

Expected: 成功生成 `dist/` 下的 wheel 和 sdist

- [ ] **Step 2: 运行测试**

Run: `pytest tests -q`

Expected: 现有测试继续通过
