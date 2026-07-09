"""
GeoServer MCP Client Example

This example demonstrates how to use the MCP client to connect to the GeoServer
MCP server and interact with GeoServer through the Model Context Protocol.
"""

import asyncio
import argparse
import json
import os
from typing import Any

# 按最新 MCP SDK 规范导入模块
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="GeoServer MCP Client Example")
    parser.add_argument("--url", help="GeoServer URL (e.g., http://localhost:8080/geoserver)")
    parser.add_argument("--user", help="GeoServer username")
    parser.add_argument("--password", help="GeoServer password")
    parser.add_argument("--server-url", help="Server URL argument to pass to the MCP server")
    parser.add_argument("--server-user", help="Server username argument to pass to the MCP server")
    parser.add_argument("--server-password", help="Server password argument to pass to the MCP server")
    return parser


def build_server_params(args: argparse.Namespace) -> StdioServerParameters:
    geoserver_url = args.url or os.environ.get("GEOSERVER_URL", "http://localhost:8080/geoserver")
    geoserver_user = args.user or os.environ.get("GEOSERVER_USER", "admin")
    geoserver_password = args.password or os.environ.get("GEOSERVER_PASSWORD", "geoserver")

    server_args = ["--from", "open-geoserver-mcp", "geoserver-mcp"]
    if args.server_url:
        server_args.extend(["--url", args.server_url])
    if args.server_user:
        server_args.extend(["--user", args.server_user])
    if args.server_password:
        server_args.extend(["--password", args.server_password])

    return StdioServerParameters(
        command="uvx",
        args=server_args,
        env={
            "GEOSERVER_URL": geoserver_url,
            "GEOSERVER_USER": geoserver_user,
            "GEOSERVER_PASSWORD": geoserver_password,
        },
    )

def print_json(obj: Any) -> None:
    """格式化打印 JSON 对象。"""
    print(json.dumps(obj, indent=2))

async def run(server_params: StdioServerParameters):
    """运行 GeoServer MCP 客户端示例。"""
    print("\n🌍 Starting GeoServer MCP Client Example\n")
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化连接
            print("Initializing connection to GeoServer MCP server...")
            await session.initialize()
            print("✅ Connection initialized\n")

            # 列出可用资源
            print("📚 Listing available resources...")
            resources = await session.list_resources()
            print(f"Found {len(resources.resources)} resources:")
            for resource in resources.resources:
                print(f"  - {resource.uri}")
            print()

            # 列出可用工具
            print("🔧 Listing available tools...")
            tools = await session.list_tools()
            print(f"Found {len(tools.tools)} tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            print()

            # 示例 1：列出工作区
            print("🗂️  Example 1: Listing workspaces")
            print("--------------------------------")
            try:
                workspaces_result = await session.call_tool("list_workspaces", {})
                if workspaces_result.isError:
                    print(f"❌ Error: {workspaces_result.content[0].text}")
                else:
                    # list_workspaces 工具直接返回列表，而不是 JSON 字符串
                    workspaces = workspaces_result.content[0].text
                    if isinstance(workspaces, str):
                        try:
                            workspaces = json.loads(workspaces)
                        except json.JSONDecodeError:
                            # 如果不是 JSON，可能是逗号分隔的列表
                            workspaces = [w.strip() for w in workspaces.strip('[]').split(',')]
                    
                    print(f"Found {len(workspaces)} workspaces:")
                    for workspace in workspaces:
                        print(f"  - {workspace}")
                print()
            except Exception as e:
                print(f"❌ Error listing workspaces: {e}")
                print()

            # 示例 2：获取图层信息
            print("🗃️  Example 2: Getting layer information")
            print("-------------------------------------")
            try:
                layer_info_result = await session.call_tool(
                    "get_layer_info", 
                    {"workspace": "topp", "layer": "states"}
                )
                if layer_info_result.isError:
                    print(f"❌ Error: {layer_info_result.content[0].text}")
                else:
                    print("Layer information:")
                    print_json(json.loads(layer_info_result.content[0].text))
                print()
            except Exception as e:
                print(f"❌ Error getting layer info: {e}")
                print()

            # 示例 3：查询要素
            print("🔍 Example 3: Querying features")
            print("-----------------------------")
            try:
                query_result = await session.call_tool(
                    "query_features",
                    {
                        "workspace": "topp",
                        "layer": "states",
                        "filter": "PERSONS > 10000000",
                        "properties": ["STATE_NAME", "PERSONS"],
                        "max_features": 3
                    }
                )
                if query_result.isError:
                    print(f"❌ Error: {query_result.content[0].text}")
                else:
                    features_data = json.loads(query_result.content[0].text)
                    features = features_data.get('features', [])
                    print(f"Found {len(features)} features:")
                    print_json(features_data)
                print()
            except Exception as e:
                print(f"❌ Error querying features: {e}")
                print()

            # 示例 4：生成地图
            print("🗺️  Example 4: Generating a map")
            print("-----------------------------")
            try:
                map_result = await session.call_tool(
                    "generate_map",
                    {
                        "layers": ["topp:states"],
                        "styles": ["population"],
                        "bbox": [-124.73, 24.96, -66.97, 49.37],
                        "width": 800,
                        "height": 600,
                        "format": "png"
                    }
                )
                if map_result.isError:
                    print(f"❌ Error: {map_result.content[0].text}")
                else:
                    map_data = json.loads(map_result.content[0].text)
                    print("Map generated successfully:")
                    print_json(map_data)
                    print(f"\nMap URL: {map_data.get('url')}")
                print()
            except Exception as e:
                print(f"❌ Error generating map: {e}")
                print()
                
            # 示例 5：创建工作区
            print("📁 Example 5: Creating a workspace")
            print("--------------------------------")
            try:
                create_result = await session.call_tool(
                    "create_workspace",
                    {"workspace": "demo-workspace"}
                )
                if create_result.isError:
                    print(f"❌ Error: {create_result.content[0].text}")
                else:
                    print("Workspace creation result:")
                    print_json(json.loads(create_result.content[0].text))
                print()
            except Exception as e:
                print(f"❌ Error creating workspace: {e}")
                print()
                
            # 示例 6：访问目录资源
            print("📋 Example 6: Accessing a catalog resource")
            print("----------------------------------------")
            try:
                resource_content, mime_type = await session.read_resource(
                    "geoserver://catalog/workspaces"
                )
                print(f"Resource content (mime-type: {mime_type}):")
                if isinstance(resource_content, list):
                    for content in resource_content:
                        if hasattr(content, 'text'):
                            if mime_type == "application/json":
                                try:
                                    data = json.loads(content.text)
                                    print_json(data)
                                except json.JSONDecodeError:
                                    print(content.text)
                            else:
                                print(content.text)
                else:
                    print(resource_content)
                print()
            except Exception as e:
                print(f"❌ Error accessing resource: {e}")
                print()

            print("🏁 GeoServer MCP Client Example completed!")


def main() -> None:
    args = build_parser().parse_args()
    asyncio.run(run(build_server_params(args)))

if __name__ == "__main__":
    main()
