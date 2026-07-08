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

mcp = FastMCP("GeoServer MCP")

register_resources(mcp)
catalog.register_tools(mcp)
styles.register_tools(mcp)
security.register_tools(mcp)
system.register_tools(mcp)
