"""MCP 资源端点。"""

from __future__ import annotations

from typing import Any, TypeAlias

from .connection import get_geoserver
from .utils import normalize_workspace_names

ResourceResult: TypeAlias = dict[str, Any]


def get_workspaces_resource() -> ResourceResult:
    """返回工作区资源列表。"""
    geo = get_geoserver()
    if geo is None:
        return {"error": "未连接到 GeoServer。"}
    try:
        return {"workspaces": normalize_workspace_names(geo.get_workspaces())}
    except Exception as exc:
        return {"error": str(exc)}


def get_layer_resource(workspace: str, layer: str) -> ResourceResult:
    """返回指定图层资源信息。"""
    geo = get_geoserver()
    if geo is None:
        return {"error": "未连接到 GeoServer。"}
    try:
        return geo.get_layer(layer, workspace)
    except Exception as exc:
        return {"error": str(exc)}


def get_wms_resource() -> ResourceResult:
    """返回 WMS 资源响应。"""
    geo = get_geoserver()
    if geo is None:
        return {"error": "未连接到 GeoServer。"}
    try:
        return {
            "service": "WMS",
            "request": "GetCapabilities",
            "capabilities": geo.get_wms_capabilities(),
        }
    except Exception as exc:
        return {"error": str(exc)}


def get_wfs_resource() -> ResourceResult:
    """返回 WFS 资源响应。"""
    geo = get_geoserver()
    if geo is None:
        return {"error": "未连接到 GeoServer。"}
    try:
        return {
            "service": "WFS",
            "request": "GetCapabilities",
            "capabilities": geo.get_wfs_capabilities(),
        }
    except Exception as exc:
        return {"error": str(exc)}


RESOURCE_REGISTRY = [
    ("geoserver://catalog/workspaces", get_workspaces_resource),
    ("geoserver://catalog/layers/{workspace}/{layer}", get_layer_resource),
    ("geoserver://services/wms/GetCapabilities", get_wms_resource),
    ("geoserver://services/wfs/GetCapabilities", get_wfs_resource),
]


def register_resources(mcp) -> None:
    """将资源端点注册到 MCP 服务。"""
    for uri, fn in RESOURCE_REGISTRY:
        mcp.resource(uri)(fn)
