"""安全相关工具。"""

from __future__ import annotations

from ..utils import parse_mapping, require_geoserver


def create_user(username: str, password: str, enabled: bool = True, properties: dict | None = None) -> dict:
    """创建用户。"""
    return require_geoserver().create_user(username, password, enabled, properties or {})


def delete_user(username: str) -> dict:
    """删除用户。"""
    return require_geoserver().delete_user(username)


def get_all_users() -> list:
    """列出所有用户。"""
    return require_geoserver().get_all_users()


def modify_user(username: str, kwargs: str) -> dict:
    """修改用户属性。"""
    return require_geoserver().modify_user(username, **parse_mapping(kwargs))


def create_usergroup(name: str, users: list | None = None) -> dict:
    """创建用户组。"""
    return require_geoserver().create_usergroup(name, users or [])


def delete_usergroup(name: str) -> dict:
    """删除用户组。"""
    return require_geoserver().delete_usergroup(name)


def get_all_usergroups() -> list:
    """列出所有用户组。"""
    return require_geoserver().get_all_usergroups()


TOOLS = [
    create_user,
    delete_user,
    get_all_users,
    modify_user,
    create_usergroup,
    delete_usergroup,
    get_all_usergroups,
]


def register_tools(mcp) -> None:
    """注册安全相关工具。"""
    for tool in TOOLS:
        mcp.tool()(tool)
