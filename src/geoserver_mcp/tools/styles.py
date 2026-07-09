"""样式相关工具。"""

from __future__ import annotations

from typing import Optional

from geo import Style

from ..utils import require_geoserver, resolve_storage_path


def create_style(name: str, sld: str, workspace: Optional[str] = None) -> dict:
    """创建样式。"""
    result = require_geoserver().create_style(name, sld, workspace)
    return {"status": "success", "name": name, "workspace": workspace or "global", "result": result}


def upload_style(
    path: str,
    name: Optional[str] = None,
    workspace: Optional[str] = None,
    sld_version: str = "1.0.0",
) -> dict:
    """上传样式文件或 SLD XML。"""
    resolved = resolve_storage_path(path)
    result = require_geoserver().upload_style(
        resolved,
        name=name,
        workspace=workspace,
        sld_version=sld_version,
    )
    return {"status": "success", "name": name, "workspace": workspace or "global", "result": result}


def get_style(name: str, workspace: Optional[str] = None) -> dict:
    """获取单个样式详情。"""
    return require_geoserver().get_style(name, workspace)


def get_styles(workspace: Optional[str] = None) -> dict:
    """列出样式。"""
    return require_geoserver().get_styles(workspace)


def publish_style(layer_name: str, style_name: str, workspace: str) -> dict:
    """给图层绑定样式。"""
    return require_geoserver().publish_style(layer_name, style_name, workspace)


def create_catagorized_featurestyle(
    style_name: str,
    column_name: str,
    column_distinct_values: str,
    workspace: Optional[str] = None,
    color_ramp: Optional[str] = None,
    geom_type: Optional[str] = None,
) -> dict:
    """创建分类矢量样式。"""
    return require_geoserver().create_catagorized_featurestyle(
        style_name,
        column_name,
        column_distinct_values,
        workspace,
        color_ramp,
        geom_type,
    )


def create_classified_featurestyle(
    style_name: str,
    column_name: str,
    column_distinct_values: str,
    workspace: Optional[str] = None,
    color_ramp: Optional[str] = None,
    geom_type: Optional[str] = None,
) -> dict:
    """创建分级矢量样式。"""
    return require_geoserver().create_classified_featurestyle(
        style_name,
        column_name,
        column_distinct_values,
        workspace,
        color_ramp,
        geom_type,
    )


def create_coveragestyle(style_name: str, params: dict) -> dict:
    """创建栅格样式。"""
    params = dict(params)
    raster_path = params.pop("raster_path", None) or params.pop("path", None)
    if not raster_path:
        raise ValueError("params.raster_path 或 params.path 为必填项。")
    return require_geoserver().create_coveragestyle(
        resolve_storage_path(raster_path),
        style_name=style_name,
        **params,
    )


def create_outline_featurestyle(
    style_name: str,
    outline_color: str,
    workspace: Optional[str] = None,
    width: str = "2",
    geom_type: str = "polygon",
) -> dict:
    """创建仅轮廓样式。"""
    return require_geoserver().create_outline_featurestyle(
        style_name,
        color=outline_color,
        width=width,
        geom_type=geom_type,
        workspace=workspace,
    )


def style_catagorize_xml(
    column_name: str,
    values: list,
    color_ramp: Optional[str] = None,
    geom_type: str = "polygon",
) -> str:
    """生成分类样式 SLD XML。"""
    return Style.catagorize_xml(column_name, values, color_ramp, geom_type)


def style_classified_xml(
    style_name: str,
    column_name: str,
    values: list,
    color_ramp: Optional[str] = None,
    geom_type: str = "polygon",
) -> str:
    """生成分级样式 SLD XML。"""
    return Style.classified_xml(style_name, column_name, values, color_ramp, geom_type)


def style_coverage_style_colormapentry(
    color_ramp,
    min_value: float,
    max_value: float,
    number_of_classes: Optional[int] = None,
):
    """生成栅格色带条目。"""
    return Style.coverage_style_colormapentry(color_ramp, min_value, max_value, number_of_classes)


def style_coverage_style_xml(
    color_ramp,
    style_name,
    cmap_type,
    min_value,
    max_value,
    number_of_classes,
    opacity,
):
    """生成栅格样式 XML。"""
    return Style.coverage_style_xml(
        color_ramp,
        style_name,
        cmap_type,
        min_value,
        max_value,
        number_of_classes,
        opacity,
    )


def style_outline_only_xml(color: str, width: float, geom_type: str = "polygon") -> str:
    """生成轮廓样式 XML。"""
    return Style.outline_only_xml(color, width, geom_type)


TOOLS = [
    create_style,
    upload_style,
    get_style,
    get_styles,
    publish_style,
    create_catagorized_featurestyle,
    create_classified_featurestyle,
    create_coveragestyle,
    create_outline_featurestyle,
    style_catagorize_xml,
    style_classified_xml,
    style_coverage_style_colormapentry,
    style_coverage_style_xml,
    style_outline_only_xml,
]


def register_tools(mcp) -> None:
    """注册样式相关工具。"""
    for tool in TOOLS:
        mcp.tool()(tool)
