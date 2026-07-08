"""GeoServer 连接创建逻辑。"""

from __future__ import annotations

import logging
import os
from typing import Optional

from geo.Geoserver import Geoserver

from .client import GeoServerClient

logger = logging.getLogger("geoserver-mcp")


def get_geoserver() -> Optional[GeoServerClient]:
    """通过环境变量创建 GeoServer 客户端。"""
    url = os.environ.get("GEOSERVER_URL", "http://localhost:8080/geoserver")
    username = os.environ.get("GEOSERVER_USER", "admin")
    password = os.environ.get("GEOSERVER_PASSWORD", "geoserver")

    try:
        geo_client = Geoserver(url, username=username, password=password)
        logger.info("已连接到 GeoServer：%s", url)
        return GeoServerClient(geo_client)
    except Exception as exc:
        logger.error("连接 GeoServer 失败：%s", exc)
        return None
