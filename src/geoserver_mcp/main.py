"""GeoServer MCP 服务启动入口。"""

from __future__ import annotations

import argparse
import logging
import os
import sys

from .server import create_mcp_server

logger = logging.getLogger("geoserver-mcp")


def main() -> None:
    """GeoServer MCP 服务主入口。"""
    parser = argparse.ArgumentParser(description="GeoServer MCP Server")
    parser.add_argument("--url", help="GeoServer URL，例如 http://localhost:8080/geoserver")
    parser.add_argument("--user", help="GeoServer 用户名")
    parser.add_argument("--password", help="GeoServer 密码")
    parser.add_argument("--debug", action="store_true", help="启用调试日志")
    parser.add_argument("--storage", help="文件读写根目录，例如 D:/data 或 /srv/geoserver-mcp/files")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default="stdio",
        help="MCP 传输方式，默认使用 stdio。",
    )
    parser.add_argument("--host", default="127.0.0.1", help="远程传输监听地址。")
    parser.add_argument("--port", type=int, default=8000, help="远程传输监听端口。")
    parser.add_argument("--mount-path", default="/", help="HTTP 服务挂载根路径。")
    parser.add_argument("--sse-path", default="/sse", help="SSE 模式下的事件路径。")
    parser.add_argument("--message-path", default="/messages/", help="SSE 模式下的消息路径。")
    parser.add_argument("--streamable-http-path", default="/mcp", help="Streamable HTTP 模式下的 MCP 路径。")
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

    mcp = create_mcp_server(
        host=args.host,
        port=args.port,
        mount_path=args.mount_path,
        sse_path=args.sse_path,
        message_path=args.message_path,
        streamable_http_path=args.streamable_http_path,
    )

    try:
        print("正在启动 GeoServer MCP 服务...")
        print(f"目标 GeoServer：{os.environ.get('GEOSERVER_URL', 'http://localhost:8080/geoserver')}")
        print(f"传输方式：{args.transport}")
        if args.transport != "stdio":
            if args.transport == "streamable-http":
                print(f"MCP 地址：http://{args.host}:{args.port}{args.streamable_http_path}")
            elif args.transport == "sse":
                print(f"SSE 地址：http://{args.host}:{args.port}{args.sse_path}")
        mcp.run(transport=args.transport, mount_path=args.mount_path)
    except KeyboardInterrupt:
        logger.info("用户已停止服务。")
    except Exception as exc:
        logger.error("服务启动失败：%s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
