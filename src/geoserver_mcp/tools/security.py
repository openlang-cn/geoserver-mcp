"""安全相关工具。"""

from __future__ import annotations

from ..utils import require_geoserver


def create_user(
    username: str,
    password: str,
    enabled: bool = True,
    service: str | None = None,
) -> dict:
    """创建用户。"""
    return require_geoserver().create_user(username, password, enabled, service)


def delete_user(username: str, service: str | None = None) -> dict:
    """删除用户。"""
    return require_geoserver().delete_user(username, service)


def get_all_users(service: str | None = None) -> list:
    """列出所有用户。"""
    return require_geoserver().get_all_users(service)


def modify_user(
    username: str,
    new_name: str | None = None,
    new_password: str | None = None,
    enable: bool | None = None,
    service: str | None = None,
) -> dict:
    """修改用户属性。"""
    return require_geoserver().modify_user(
        username,
        new_name=new_name,
        new_password=new_password,
        enable=enable,
        service=service,
    )


def create_usergroup(name: str, service: str | None = None) -> dict:
    """创建用户组。"""
    return require_geoserver().create_usergroup(name, service)


def delete_usergroup(name: str, service: str | None = None) -> dict:
    """删除用户组。"""
    return require_geoserver().delete_usergroup(name, service)


def get_all_usergroups(service: str | None = None) -> list:
    """列出所有用户组。"""
    return require_geoserver().get_all_usergroups(service)


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
