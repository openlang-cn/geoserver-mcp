"""系统与服务类工具。"""

from __future__ import annotations

from ..utils import require_geoserver


def get_manifest() -> dict:
    """获取 GeoServer 清单信息。"""
    return require_geoserver().get_manifest()


def get_status() -> dict:
    """获取服务状态。"""
    return require_geoserver().get_status()


def get_system_status() -> dict:
    """获取系统状态。"""
    return require_geoserver().get_system_status()


def get_version() -> dict:
    """获取 GeoServer 版本。"""
    return require_geoserver().get_version()


def reload_geoserver() -> str:
    """重新加载 GeoServer 配置。"""
    return require_geoserver().reload()


def reset_geoserver() -> str:
    """重置 GeoServer 缓存和连接。"""
    return require_geoserver().reset()


def update_service(service: str, options: dict) -> str:
    """更新 OGC 服务配置。"""
    return require_geoserver().update_service(service, options)


def publish_time_dimension_to_coveragestore(
        store_name: str | None = None,
        workspace: str | None = None,
        presentation: str = "LIST",
        units: str = "ISO8601",
        default_value: str = "MINIMUM",
        content_type: str = "application/xml; charset=UTF-8",
) -> dict:
    """为栅格存储发布或更新时间维度。"""
    return require_geoserver().publish_time_dimension_to_coveragestore(
        store_name,
        workspace,
        presentation,
        units,
        default_value,
        content_type,
    )


TOOLS = [
    get_manifest,
    get_status,
    get_system_status,
    get_version,
    reload_geoserver,
    reset_geoserver,
    update_service,
    publish_time_dimension_to_coveragestore,
]


def register_tools(mcp) -> None:
    """注册系统相关工具。"""
    for tool in TOOLS:
        mcp.tool()(tool)
