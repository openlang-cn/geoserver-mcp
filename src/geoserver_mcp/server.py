"""FastMCP 服务创建与注册。"""

from __future__ import annotations

import logging

from mcp.server.fastmcp import FastMCP

from .resources import register_resources
from .tools import catalog, security, styles, system

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def create_mcp_server(
    *,
    host: str = "127.0.0.1",
    port: int = 8000,
    mount_path: str = "/",
    sse_path: str = "/sse",
    message_path: str = "/messages/",
    streamable_http_path: str = "/mcp",
) -> FastMCP:
    """创建并注册 GeoServer MCP 服务。"""
    mcp = FastMCP(
        "GeoServer MCP",
        host=host,
        port=port,
        mount_path=mount_path,
        sse_path=sse_path,
        message_path=message_path,
        streamable_http_path=streamable_http_path,
    )

    register_resources(mcp)
    catalog.register_tools(mcp)
    styles.register_tools(mcp)
    security.register_tools(mcp)
    system.register_tools(mcp)
    return mcp


mcp = create_mcp_server()
