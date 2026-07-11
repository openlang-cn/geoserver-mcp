"""目录、图层、存储与要素相关工具。"""

from __future__ import annotations

from typing import Annotated, Any

from pydantic import Field

from ..utils import (
    normalize_workspace_names,
    parse_mapping,
    require_geoserver,
    resolve_storage_path,
)


def list_workspaces() -> list[str]:
    """列出 GeoServer 中可用的工作区。"""
    return normalize_workspace_names(require_geoserver().get_workspaces())


def create_workspace(
    workspace: Annotated[
        str,
        Field(description="要创建的工作区名称")
    ],
) -> dict[str, Any]:
    """在 GeoServer 中创建新的工作区。"""
    geo = require_geoserver()
    if not workspace:
        raise ValueError("工作区名称不能为空。")
    existing = normalize_workspace_names(geo.get_workspaces())
    if workspace in existing:
        return {"status": "info", "workspace": workspace, "message": f"工作区‘{workspace}’已存在。"}
    geo.create_workspace(workspace)
    return {"status": "success", "workspace": workspace, "message": f"工作区‘{workspace}’已创建。"}


def get_workspace(
    workspace: Annotated[
        str,
        Field(description="工作区名称")
    ],
) -> dict:
    """获取指定工作区详情。"""
    return require_geoserver().get_workspace(workspace)


def get_default_workspace() -> dict:
    """获取当前默认工作区。"""
    return require_geoserver().get_default_workspace()


def set_default_workspace(
    workspace: Annotated[
        str,
        Field(description="要设为默认的工作区名称")
    ],
) -> str:
    """设置默认工作区。"""
    return require_geoserver().set_default_workspace(workspace)


def get_layer_info(
    workspace: Annotated[
        str,
        Field(description="图层所在工作区名称")
    ],
    layer: Annotated[
        str,
        Field(description="图层名称")
    ],
) -> dict[str, Any]:
    """获取图层详情。"""
    return require_geoserver().get_layer(layer, workspace)


def list_layers(
    workspace: Annotated[
        str | None,
        Field(description="工作区名称，不填则列出所有工作区的图层")
    ] = None,
) -> Any:
    """列出图层，可按工作区过滤。"""
    return require_geoserver().get_layers(workspace)


def create_layer(
    workspace: Annotated[
        str,
        Field(description="目标工作区名称")
    ],
    layer: Annotated[
        str,
        Field(description="发布后的图层名称（标题）")
    ],
    data_store: Annotated[
        str,
        Field(description="数据存储名称")
    ],
    source: Annotated[
        str,
        Field(description="数据源名称，如 PostGIS 表名")
    ],
) -> dict[str, Any]:
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


def delete_resource(
    resource_type: Annotated[str, Field(description="资源类型：workspace、layer、datastore、style、"
    "coverage、featurestore")],
    workspace: Annotated[
        str,
        Field(description="资源所在工作区名称")
    ],
    name: Annotated[
        str,
        Field(description="要删除的资源名称")
    ],
) -> dict[str, Any]:
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
    workspace: Annotated[
        str,
        Field(description="图层所在工作区名称")
    ],
    layer: Annotated[
        str,
        Field(description="图层名称")
    ],
    filter: Annotated[
        str | None,
        Field(description='CQL 过滤器，如 "population > 10000"')
    ] = None,
    properties: Annotated[
        list[str] | None,
        Field(description='要返回的属性列表，如 ["name", "population"]')
    ] = None,
    max_features: Annotated[
        int | None,
        Field(description="最大返回要素数")
    ] = None,
) -> dict:
    """查询矢量图层要素。"""
    return require_geoserver().query_features(workspace, layer, filter, properties, max_features)


def generate_map(
    layers: Annotated[
        list[str],
        Field(description='图层名称列表，如 ["demo:roads"]')
    ],
    styles: Annotated[
        list[str] | None,
        Field(description="样式名称列表，与 layers 一一对应")
    ] = None,
    bbox: Annotated[list[float] | None, Field(description="边界框 [minx, miny, maxx, maxy]，"
    "默认 [-180, -90, 180, 90]")] = None,
    width: Annotated[
        int,
        Field(description="地图宽度(像素)，默认 1024")
    ] = 1024,
    height: Annotated[
        int,
        Field(description="地图高度(像素)，默认 768")
    ] = 768,
    format: Annotated[str, Field(description="输出格式，如 image/png、image/jpeg，"
    "默认 image/png")] = "image/png",
) -> dict:
    """生成 WMS 地图访问参数。"""
    return require_geoserver().generate_map(layers, styles, bbox, width, height, format)


def create_datastore(
    workspace: Annotated[
        str,
        Field(description="工作区名称")
    ],
    name: Annotated[
        str,
        Field(description="数据存储名称")
    ],
    params: Annotated[
        dict,
        Field(
            description="存储参数，必须包含 path(文件路径)或 url(WFS URL)；"
            "可选 overwrite(是否覆盖，默认 False)"
        )
    ],
) -> dict:
    """创建文件型数据存储。"""
    params = dict(params)
    if "path" in params:
        params["path"] = resolve_storage_path(params["path"])
    return require_geoserver().create_datastore(name, workspace, **params)


def create_featurestore(
    workspace: Annotated[
        str,
        Field(description="工作区名称")
    ],
    name: Annotated[
        str,
        Field(description="要素存储名称")
    ],
    params: Annotated[
        dict,
        Field(
            description="数据库连接参数，可用键：host(默认 localhost)、"
            "port(默认 5432)、db(默认 postgres)、"
            "pg_user(默认 postgres)、pg_password(默认 admin)、"
            "schema(默认 public)"
        )
    ],
) -> dict:
    """创建数据库要素存储。"""
    return require_geoserver().create_featurestore(name, workspace=workspace, **params)


def create_gpkg_datastore(
    workspace: Annotated[
        str,
        Field(description="工作区名称")
    ],
    name: Annotated[
        str,
        Field(description="数据存储名称")
    ],
    file_path: Annotated[
        str,
        Field(description="GeoPackage 文件路径（相对于 storage 目录或绝对路径）")
    ],
) -> dict:
    """创建 GeoPackage 数据存储。"""
    resolved_path = resolve_storage_path(file_path)
    return require_geoserver().create_gpkg_datastore(workspace, name, resolved_path)


def create_shp_datastore(
    workspace: Annotated[
        str,
        Field(description="工作区名称")
    ],
    name: Annotated[
        str,
        Field(description="数据存储名称")
    ],
    file_path: Annotated[
        str,
        Field(description="Shapefile 文件路径（相对于 storage 目录或绝对路径）")
    ],
) -> dict:
    """创建 Shapefile 数据存储。"""
    resolved_path = resolve_storage_path(file_path)
    return require_geoserver().create_shp_datastore(workspace, name, resolved_path)


def create_coveragestore(
    workspace: Annotated[
        str,
        Field(description="工作区名称")
    ],
    name: Annotated[
        str,
        Field(description="栅格存储名称")
    ],
    params: Annotated[
        dict,
        Field(description="栅格参数，需包含 path(文件路径)；可选 file_type(默认 GeoTIFF)、layer_name")
    ],
) -> dict:
    """创建栅格存储。"""
    params = dict(params)
    if "path" in params:
        params["path"] = resolve_storage_path(params["path"])
    return require_geoserver().create_coveragestore(workspace, name, **params)


def delete_coveragestore(
    workspace: Annotated[
        str,
        Field(description="工作区名称")
    ],
    name: Annotated[
        str,
        Field(description="要删除的栅格存储名称")
    ],
) -> str:
    """删除栅格存储。"""
    return require_geoserver().delete_coveragestore(name, workspace)


def get_coveragestore(
    workspace: Annotated[
        str,
        Field(description="工作区名称")
    ],
    name: Annotated[
        str,
        Field(description="栅格存储名称")
    ],
) -> dict:
    """获取单个栅格存储详情。"""
    return require_geoserver().get_coveragestore(name, workspace)


def get_coveragestores(
    workspace: Annotated[
        str,
        Field(description="工作区名称")
    ],
) -> dict:
    """列出工作区下的栅格存储。"""
    return require_geoserver().get_coveragestores(workspace)


def get_datastore(
    workspace: Annotated[
        str,
        Field(description="工作区名称")
    ],
    name: Annotated[
        str,
        Field(description="数据存储名称")
    ],
) -> dict:
    """获取单个数据存储详情。"""
    return require_geoserver().get_datastore(name, workspace)


def get_datastores(
    workspace: Annotated[
        str,
        Field(description="工作区名称")
    ],
) -> dict:
    """列出工作区下的数据存储。"""
    return require_geoserver().get_datastores(workspace)


def get_featurestore(
    workspace: Annotated[
        str,
        Field(description="工作区名称")
    ],
    store_name: Annotated[
        str,
        Field(description="要素存储名称")
    ],
) -> dict:
    """获取单个要素存储详情。"""
    return require_geoserver().get_featurestore(store_name, workspace)


def delete_featurestore(
    workspace: Annotated[
        str,
        Field(description="工作区名称")
    ],
    name: Annotated[
        str,
        Field(description="要删除的要素存储名称")
    ],
) -> str:
    """删除要素存储。"""
    return require_geoserver().delete_featurestore(name, workspace)


def create_layergroup(
    workspace: Annotated[
        str,
        Field(description="工作区名称")
    ],
    name: Annotated[
        str,
        Field(description="图层组名称")
    ],
    layers: Annotated[
        list,
        Field(description='图层列表，每个元素为 {"name": "图层名", "workspace": "工作区"}')
    ],
    metadata: Annotated[
        list[dict] | None,
        Field(description='元数据列表，如 [{"key": "k", "value": "v"}]')
    ] = None,
    keywords: Annotated[
        list[str] | None,
        Field(description="关键词列表")
    ] = None,
    mode: Annotated[
        str,
        Field(description="图层组模式：single(单一)、opaque(不透明)、tree(树形)，默认 single")
    ] = "single",
    title: Annotated[
        str | None,
        Field(description="标题，默认使用 name")
    ] = None,
    abstract_text: Annotated[
        str | None,
        Field(description="摘要描述")
    ] = None,
    formats: Annotated[
        str,
        Field(description='输出格式列表，逗号分隔，如 "html,png"，默认 html')
    ] = "html",
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


def get_layergroup(
    workspace: Annotated[
        str,
        Field(description="工作区名称")
    ],
    name: Annotated[
        str,
        Field(description="图层组名称")
    ],
) -> dict:
    """获取图层组详情。"""
    return require_geoserver().get_layergroup(name, workspace)


def get_layergroups(
    workspace: Annotated[
        str,
        Field(description="工作区名称")
    ],
) -> dict:
    """列出图层组。"""
    return require_geoserver().get_layergroups(workspace)


def add_layer_to_layergroup(
    layer_name: Annotated[
        str,
        Field(description="要添加的图层名称")
    ],
    layer_workspace: Annotated[
        str,
        Field(description="要添加的图层所在工作区")
    ],
    layergroup_name: Annotated[
        str,
        Field(description="目标图层组名称")
    ],
    layergroup_workspace: Annotated[str | None, Field(description="目标图层组所在工作区，默认与 "
    "layer_workspace 相同")] = None,
) -> None:
    """向图层组添加图层。"""
    return require_geoserver().add_layer_to_layergroup(
        layer_name,
        layer_workspace,
        layergroup_name,
        layergroup_workspace,
    )


def remove_layer_from_layergroup(
    layer_name: Annotated[
        str,
        Field(description="要移除的图层名称")
    ],
    layer_workspace: Annotated[
        str,
        Field(description="要移除的图层所在工作区")
    ],
    layergroup_name: Annotated[
        str,
        Field(description="目标图层组名称")
    ],
    layergroup_workspace: Annotated[str | None, Field(description="目标图层组所在工作区，默认与 "
    "layer_workspace 相同")] = None,
) -> None:
    """从图层组移除图层。"""
    return require_geoserver().remove_layer_from_layergroup(
        layer_name,
        layer_workspace,
        layergroup_name,
        layergroup_workspace,
    )


def delete_layergroup(
    workspace: Annotated[
        str,
        Field(description="工作区名称")
    ],
    name: Annotated[
        str,
        Field(description="要删除的图层组名称")
    ],
) -> str:
    """删除图层组。"""
    return require_geoserver().delete_layergroup(name, workspace)


def update_layergroup(
    layergroup_name: Annotated[
        str,
        Field(description="图层组名称")
    ],
    title: Annotated[
        str | None,
        Field(description="新标题")
    ] = None,
    abstract_text: Annotated[
        str | None,
        Field(description="新摘要")
    ] = None,
    formats: Annotated[
        str,
        Field(description="输出格式列表，逗号分隔，默认 html")
    ] = "html",
    metadata: Annotated[
        list | None,
        Field(description="元数据列表")
    ] = None,
    keywords: Annotated[
        list | None,
        Field(description="关键词列表")
    ] = None,
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


def publish_featurestore(
    workspace: Annotated[
        str,
        Field(description="工作区名称")
    ],
    store_name: Annotated[
        str,
        Field(description="要素存储名称")
    ],
    params: Annotated[
        dict,
        Field(description="图层元数据，必须包含 table(表名)；可选 title、advertised、abstract、keywords、cqlfilter")
    ],
) -> int:
    """将要素存储发布为图层。"""
    return require_geoserver().publish_featurestore(store_name, params, workspace)


def publish_featurestore_sqlview(
    workspace: Annotated[
        str,
        Field(description="工作区名称")
    ],
    store_name: Annotated[
        str,
        Field(description="要素存储名称")
    ],
    params: Annotated[
        dict,
        Field(
            description="SQL 视图元数据，必须包含 name(视图名)、sql(SQL 查询)；"
            "可选 key_column、geom_name(默认 geom)、"
            "geom_type(默认 Geometry)、srid(默认 4326)"
        )
    ],
    sqlview_params: Annotated[
        list,
        Field(
            description="SQL 视图参数列表，每个元素为 "
            "{\"name\":\"参数名\",\"defaultValue\":\"默认值\","
            "\"regexpValidator\":\"正则校验\"}"
        )
    ],
) -> int:
    """通过 SQL 视图发布图层。"""
    return require_geoserver().publish_featurestore_sqlview(
        store_name,
        params,
        sqlview_params,
        workspace,
    )


def edit_featuretype(
    workspace: Annotated[
        str,
        Field(description="工作区名称")
    ],
    store_name: Annotated[
        str,
        Field(description="要素存储名称")
    ],
    featuretype: Annotated[
        str,
        Field(description="要素类型名称（表名）")
    ],
    kwargs: Annotated[
        str,
        Field(
            description="要更新的键值对 JSON 字符串，"
            "如 {\"title\":\"新标题\",\"abstract\":\"新摘要\"}"
        )
    ],
) -> int:
    """更新要素类型配置。"""
    return require_geoserver().edit_featuretype(
        store_name,
        workspace,
        featuretype,
        **parse_mapping(kwargs),
    )


def recalculate_featuretype_bbox(
    workspace: Annotated[
        str,
        Field(description="工作区名称")
    ],
    store_name: Annotated[
        str,
        Field(description="要素存储名称")
    ],
    featuretype: Annotated[
        str,
        Field(description="要素类型名称")
    ],
) -> dict[str, Any]:
    """"重新计算要素类型的原生和经纬度边界框。"""
    return require_geoserver().rest.recalculate_featuretype_bbox(workspace, store_name, featuretype)


def get_featuretype(
    workspace: Annotated[
        str,
        Field(description="工作区名称")
    ],
    store_name: Annotated[
        str,
        Field(description="要素存储名称")
    ],
    featuretype: Annotated[
        str,
        Field(description="要素类型名称")
    ],
) -> dict[str, Any]:
    """获取要素类型完整元数据，包括 SQL 视图定义。"""
    return require_geoserver().rest.get_featuretype(workspace, store_name, featuretype)


def get_featuretypes(
    workspace: Annotated[
        str,
        Field(description="工作区名称")
    ],
    store_name: Annotated[
        str,
        Field(description="要素存储名称")
    ],
) -> list[str]:
    """列出要素类型。"""
    return require_geoserver().get_featuretypes(workspace, store_name)


def get_feature_attribute(
    workspace: Annotated[
        str,
        Field(description="工作区名称")
    ],
    store_name: Annotated[
        str,
        Field(description="要素存储名称")
    ],
    featuretype: Annotated[
        str,
        Field(description="要素类型名称")
    ],
) -> list[str]:
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
    recalculate_featuretype_bbox,
    get_featuretype,
    get_featuretypes,
    get_feature_attribute,
]


def register_tools(mcp) -> None:
    """注册目录类工具。"""
    for tool in TOOLS:
        mcp.tool()(tool)
