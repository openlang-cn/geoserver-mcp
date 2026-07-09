"""目录、图层、存储与要素相关工具。"""

from __future__ import annotations

from typing import Any, Dict, Optional

from ..utils import (
    normalize_workspace_names,
    parse_mapping,
    require_geoserver,
    resolve_storage_path,
)


def list_workspaces() -> list[str]:
    """列出 GeoServer 中可用的工作区。"""
    return normalize_workspace_names(require_geoserver().get_workspaces())


def create_workspace(workspace: str) -> Dict[str, Any]:
    """在 GeoServer 中创建新的工作区。"""
    geo = require_geoserver()
    if not workspace:
        raise ValueError("工作区名称不能为空。")
    existing = normalize_workspace_names(geo.get_workspaces())
    if workspace in existing:
        return {"status": "info", "workspace": workspace, "message": f"工作区“{workspace}”已存在。"}
    geo.create_workspace(workspace)
    return {"status": "success", "workspace": workspace, "message": f"工作区“{workspace}”已创建。"}


def get_workspace(workspace: str) -> dict:
    """获取指定工作区详情。"""
    return require_geoserver().get_workspace(workspace)


def get_default_workspace() -> dict:
    """获取当前默认工作区。"""
    return require_geoserver().get_default_workspace()


def set_default_workspace(workspace: str) -> str:
    """设置默认工作区。"""
    return require_geoserver().set_default_workspace(workspace)


def get_layer_info(workspace: str, layer: str) -> Dict[str, Any]:
    """获取图层详情。"""
    return require_geoserver().get_layer(layer, workspace)


def list_layers(workspace: Optional[str] = None) -> Any:
    """列出图层，可按工作区过滤。"""
    return require_geoserver().get_layers(workspace)


def create_layer(workspace: str, layer: str, data_store: str, source: str) -> Dict[str, Any]:
    """基于已有数据存储发布图层。"""
    geo = require_geoserver()
    if not workspace or not layer or not data_store or not source:
        raise ValueError("workspace、layer、data_store、source 均为必填。")
    result = geo.create_layer(workspace, data_store, layer, source)
    return {
        "status": "success",
        "layer": layer,
        "workspace": workspace,
        "data_store": data_store,
        "source": source,
        "result": result,
    }


def delete_resource(resource_type: str, workspace: str, name: str) -> Dict[str, Any]:
    """按资源类型删除 GeoServer 资源。"""
    geo = require_geoserver()
    valid_types = {"workspace", "layer", "datastore", "style", "coverage", "featurestore"}
    if resource_type not in valid_types:
        raise ValueError(f"resource_type 必须是：{', '.join(sorted(valid_types))}")

    if resource_type == "workspace":
        result = geo.delete_workspace(name)
    elif resource_type == "layer":
        result = geo.delete_layer(name, workspace)
    elif resource_type == "datastore":
        result = geo.delete_datastore(name, workspace)
    elif resource_type == "style":
        result = geo.delete_style(name, workspace)
    elif resource_type == "featurestore":
        result = geo.delete_featurestore(name, workspace)
    else:
        result = geo.delete_coverage(name, workspace)

    return {
        "status": "success",
        "type": resource_type,
        "name": name,
        "workspace": workspace,
        "result": str(result),
    }


def query_features(
    workspace: str,
    layer: str,
    filter: Optional[str] = None,
    properties: Optional[list[str]] = None,
    max_features: Optional[int] = None,
) -> dict:
    """查询矢量图层要素。"""
    return require_geoserver().query_features(workspace, layer, filter, properties, max_features)


def generate_map(
    layers: list[str],
    styles: Optional[list[str]] = None,
    bbox: Optional[list[float]] = None,
    width: int = 1024,
    height: int = 768,
    format: str = "image/png",
) -> dict:
    """生成 WMS 地图访问参数。"""
    return require_geoserver().generate_map(layers, styles, bbox, width, height, format)


def create_datastore(workspace: str, name: str, params: dict) -> dict:
    """创建文件型数据存储。"""
    params = dict(params)
    if "path" in params:
        params["path"] = resolve_storage_path(params["path"])
    return require_geoserver().create_datastore(name, workspace, **params)


def create_featurestore(workspace: str, name: str, params: dict) -> dict:
    """创建数据库要素存储。"""
    return require_geoserver().create_featurestore(name, workspace=workspace, **params)


def create_gpkg_datastore(workspace: str, name: str, file_path: str) -> dict:
    """创建 GeoPackage 数据存储。"""
    resolved_path = resolve_storage_path(file_path)
    return require_geoserver().create_gpkg_datastore(workspace, name, resolved_path)


def create_shp_datastore(workspace: str, name: str, file_path: str) -> dict:
    """创建 Shapefile 数据存储。"""
    resolved_path = resolve_storage_path(file_path)
    return require_geoserver().create_shp_datastore(workspace, name, resolved_path)


def create_coveragestore(workspace: str, name: str, params: dict) -> dict:
    """创建栅格存储。"""
    params = dict(params)
    if "path" in params:
        params["path"] = resolve_storage_path(params["path"])
    return require_geoserver().create_coveragestore(workspace, name, **params)


def delete_coveragestore(workspace: str, name: str) -> str:
    """删除栅格存储。"""
    return require_geoserver().delete_coveragestore(name, workspace)


def get_coveragestore(workspace: str, name: str) -> dict:
    """获取单个栅格存储详情。"""
    return require_geoserver().get_coveragestore(name, workspace)


def get_coveragestores(workspace: str) -> dict:
    """列出工作区下的栅格存储。"""
    return require_geoserver().get_coveragestores(workspace)


def get_datastore(workspace: str, name: str) -> dict:
    """获取单个数据存储详情。"""
    return require_geoserver().get_datastore(name, workspace)


def get_datastores(workspace: str) -> dict:
    """列出工作区下的数据存储。"""
    return require_geoserver().get_datastores(workspace)


def get_featurestore(workspace: str, store_name: str) -> dict:
    """获取单个要素存储详情。"""
    return require_geoserver().get_featurestore(store_name, workspace)


def delete_featurestore(workspace: str, name: str) -> str:
    """删除要素存储。"""
    return require_geoserver().delete_featurestore(name, workspace)


def create_layergroup(
    workspace: str,
    name: str,
    layers: list,
    metadata: Optional[list[dict]] = None,
    keywords: Optional[list[str]] = None,
    mode: str = "single",
    title: Optional[str] = None,
    abstract_text: Optional[str] = None,
    formats: str = "html",
) -> str:
    """创建图层组。"""
    geo = require_geoserver()
    return geo.create_layergroup(
        name=name,
        mode=mode,
        title=title or name,
        abstract_text=abstract_text or name,
        layers=layers,
        workspace=workspace,
        formats=formats,
        metadata=metadata or [],
        keywords=keywords or [],
    )


def get_layergroup(workspace: str, name: str) -> dict:
    """获取图层组详情。"""
    return require_geoserver().get_layergroup(name, workspace)


def get_layergroups(workspace: str) -> dict:
    """列出图层组。"""
    return require_geoserver().get_layergroups(workspace)


def add_layer_to_layergroup(
    layer_name: str,
    layer_workspace: str,
    layergroup_name: str,
    layergroup_workspace: Optional[str] = None,
) -> None:
    """向图层组添加图层。"""
    return require_geoserver().add_layer_to_layergroup(
        layer_name,
        layer_workspace,
        layergroup_name,
        layergroup_workspace,
    )


def remove_layer_from_layergroup(
    layer_name: str,
    layer_workspace: str,
    layergroup_name: str,
    layergroup_workspace: Optional[str] = None,
) -> None:
    """从图层组移除图层。"""
    return require_geoserver().remove_layer_from_layergroup(
        layer_name,
        layer_workspace,
        layergroup_name,
        layergroup_workspace,
    )


def delete_layergroup(workspace: str, name: str) -> str:
    """删除图层组。"""
    return require_geoserver().delete_layergroup(name, workspace)


def update_layergroup(
    layergroup_name: str,
    title: Optional[str] = None,
    abstract_text: Optional[str] = None,
    formats: str = "html",
    metadata: Optional[list] = None,
    keywords: Optional[list] = None,
) -> str:
    """更新图层组元数据。"""
    return require_geoserver().update_layergroup(
        layergroup_name=layergroup_name,
        title=title,
        abstract_text=abstract_text,
        formats=formats,
        metadata=metadata or [],
        keywords=keywords or [],
    )


def publish_featurestore(workspace: str, store_name: str, params: dict) -> int:
    """将要素存储发布为图层。"""
    return require_geoserver().publish_featurestore(store_name, params, workspace)


def publish_featurestore_sqlview(
    workspace: str,
    store_name: str,
    params: dict,
    sqlview_params: list,
) -> int:
    """通过 SQL 视图发布图层。"""
    return require_geoserver().publish_featurestore_sqlview(
        store_name,
        params,
        sqlview_params,
        workspace,
    )


def edit_featuretype(workspace: str, store_name: str, featuretype: str, kwargs: str) -> int:
    """更新要素类型配置。"""
    return require_geoserver().edit_featuretype(
        store_name,
        workspace,
        featuretype,
        **parse_mapping(kwargs),
    )


def get_featuretypes(workspace: str, store_name: str) -> list[str]:
    """列出要素类型。"""
    return require_geoserver().get_featuretypes(workspace, store_name)


def get_feature_attribute(workspace: str, store_name: str, featuretype: str) -> list[str]:
    """获取要素属性定义。"""
    return require_geoserver().get_feature_attribute(featuretype, workspace, store_name)


TOOLS = [
    list_workspaces,
    create_workspace,
    get_workspace,
    get_default_workspace,
    set_default_workspace,
    get_layer_info,
    list_layers,
    create_layer,
    delete_resource,
    query_features,
    generate_map,
    create_datastore,
    create_featurestore,
    create_gpkg_datastore,
    create_shp_datastore,
    create_coveragestore,
    delete_coveragestore,
    get_coveragestore,
    get_coveragestores,
    get_datastore,
    get_datastores,
    get_featurestore,
    delete_featurestore,
    create_layergroup,
    get_layergroup,
    get_layergroups,
    add_layer_to_layergroup,
    remove_layer_from_layergroup,
    delete_layergroup,
    update_layergroup,
    publish_featurestore,
    publish_featurestore_sqlview,
    edit_featuretype,
    get_featuretypes,
    get_feature_attribute,
]


def register_tools(mcp) -> None:
    """注册目录类工具。"""
    for tool in TOOLS:
        mcp.tool()(tool)
