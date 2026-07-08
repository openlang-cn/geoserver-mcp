"""GeoServer MCP 服务启动入口。"""

from __future__ import annotations

import argparse
import logging
import os
import sys

from .server import mcp

logger = logging.getLogger("geoserver-mcp")


def main() -> None:
    """GeoServer MCP 服务主入口。"""
    parser = argparse.ArgumentParser(description="GeoServer MCP Server")
    parser.add_argument("--url", help="GeoServer URL，例如 http://localhost:8080/geoserver")
    parser.add_argument("--user", help="GeoServer 用户名")
    parser.add_argument("--password", help="GeoServer 密码")
    parser.add_argument("--debug", action="store_true", help="启用调试日志")
    parser.add_argument("--storage", help="文件读写根目录，例如 D:/data 或 /srv/geoserver-mcp/files")
    args = parser.parse_args()

    if args.url:
        os.environ["GEOSERVER_URL"] = args.url
    if args.user:
        os.environ["GEOSERVER_USER"] = args.user
    if args.password:
        os.environ["GEOSERVER_PASSWORD"] = args.password
    if args.storage:
        os.environ["GEOSERVER_STORAGE_PATH"] = args.storage

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("已启用调试日志。")

    try:
        print("正在启动 GeoServer MCP 服务...")
        print(f"目标 GeoServer：{os.environ.get('GEOSERVER_URL', 'http://localhost:8080/geoserver')}")
        mcp.run()
    except KeyboardInterrupt:
        logger.info("用户已停止服务。")
    except Exception as exc:
        logger.error("服务启动失败：%s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
