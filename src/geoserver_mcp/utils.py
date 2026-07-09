"""通用辅助方法。"""

from __future__ import annotations

import ast
import os

from typing import Any

from .connection import get_geoserver


def resolve_storage_path(path: str | None) -> str | None:
    """在设置存储根目录时返回对应的绝对路径。"""
    base = os.environ.get("GEOSERVER_STORAGE_PATH", "")
    if not path:
        return path
    if os.path.isabs(path) or not base:
        return path
    return os.path.join(base, path)


def require_geoserver():
    """获取客户端；如未连接则抛出错误。"""
    geo = get_geoserver()
    if geo is None:
        raise ValueError("未连接到 GeoServer。")
    return geo


def parse_mapping(value: str) -> dict:
    """将 JSON/Python 字面量字符串解析为字典。"""
    parsed = ast.literal_eval(value)
    if not isinstance(parsed, dict):
        raise ValueError("参数必须能解析为字典。")
    return parsed


def normalize_workspace_names(workspaces: Any) -> list[str]:
    """将 GeoServer 工作区返回结果规范为名称列表。"""
    if isinstance(workspaces, list):
        return [item["name"] if isinstance(item, dict) else str(item) for item in workspaces]

    if not isinstance(workspaces, dict):
        return [str(workspaces)]

    workspace_items = workspaces.get("workspaces", {}).get("workspace", [])
    if isinstance(workspace_items, dict):
        workspace_items = [workspace_items]

    return [
        item["name"] if isinstance(item, dict) and "name" in item else str(item)
        for item in workspace_items
    ]
