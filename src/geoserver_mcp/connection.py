"""GeoServer 连接创建逻辑。"""

from __future__ import annotations

import importlib
import logging
import os
import warnings

from .client import GeoServerClient

logger = logging.getLogger("geoserver-mcp")


def get_geoserver_class():
    """延迟导入第三方 Geoserver 类，并抑制其已知的语法告警。"""
    warnings.filterwarnings(
        "ignore",
        message=r"invalid escape sequence '\\w'",
        category=SyntaxWarning,
        module=r"geo\.Geoserver",
    )
    return importlib.import_module("geo.Geoserver").Geoserver


def get_geoserver() -> GeoServerClient | None:
    """通过环境变量创建 GeoServer 客户端。"""
    url = os.environ.get("GEOSERVER_URL", "http://localhost:8080/geoserver")
    username = os.environ.get("GEOSERVER_USER", "admin")
    password = os.environ.get("GEOSERVER_PASSWORD", "geoserver")

    try:
        geoserver_class = get_geoserver_class()
        geo_client = geoserver_class(url, username=username, password=password)
        logger.info("已连接到 GeoServer：%s", url)
        return GeoServerClient(geo_client)
    except Exception as exc:
        logger.error("连接 GeoServer 失败：%s", exc)
        return None
