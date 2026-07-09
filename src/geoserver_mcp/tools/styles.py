"""样式相关工具。"""

from __future__ import annotations

import importlib
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Optional

from ..utils import require_geoserver, resolve_storage_path


def get_style_module() -> Any:
    """延迟加载 geo.Style，避免模块导入阶段绑定运行环境。"""
    return importlib.import_module("geo.Style")


def _normalize_color_ramp(color_ramp, number_of_classes: Optional[int] = None):
    if isinstance(color_ramp, str):
        sns = importlib.import_module("seaborn")
        rgb2hex = importlib.import_module("matplotlib.colors").rgb2hex
        palette = sns.color_palette(color_ramp, int(number_of_classes or 5))
        return [rgb2hex(color) for color in palette]
    return color_ramp


def _capture_style_xml(factory) -> str:
    with TemporaryDirectory() as temp_dir:
        previous_cwd = os.getcwd()
        os.chdir(temp_dir)
        try:
            result = factory()
            if isinstance(result, str):
                return result

            style_file = Path("style.sld")
            if style_file.exists():
                return style_file.read_text(encoding="utf-8")

            raise ValueError("Style helper did not return XML or write style.sld.")
        finally:
            os.chdir(previous_cwd)


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


def publish_style(layer_name: str, style_name: str, workspace: str) -> int:
    """给图层绑定样式。"""
    return require_geoserver().publish_style(layer_name, style_name, workspace)


def create_catagorized_featurestyle(
    style_name: str,
    column_name: str,
    column_distinct_values: str,
    workspace: Optional[str] = None,
    color_ramp: Optional[str] = None,
    geom_type: Optional[str] = None,
) -> int:
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
) -> int:
    """创建分级矢量样式。"""
    return require_geoserver().create_classified_featurestyle(
        style_name,
        column_name,
        column_distinct_values,
        workspace,
        color_ramp,
        geom_type,
    )


def create_coveragestyle(style_name: str, params: dict) -> int:
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
) -> int:
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
    style_module = get_style_module()
    return _capture_style_xml(
        lambda: style_module.catagorize_xml(column_name, values, color_ramp, geom_type)
    )


def style_classified_xml(
    style_name: str,
    column_name: str,
    values: list,
    color_ramp: Optional[str] = None,
    geom_type: str = "polygon",
) -> str:
    """生成分级样式 SLD XML。"""
    style_module = get_style_module()
    return _capture_style_xml(
        lambda: style_module.classified_xml(style_name, column_name, values, color_ramp, geom_type)
    )


def style_coverage_style_colormapentry(
    color_ramp,
    min_value: float,
    max_value: float,
    number_of_classes: Optional[int] = None,
) -> str:
    """生成栅格色带条目。"""
    style_module = get_style_module()
    normalized_ramp = _normalize_color_ramp(color_ramp, number_of_classes)
    return style_module.coverage_style_colormapentry(
        normalized_ramp,
        min_value,
        max_value,
        number_of_classes,
    )


def style_coverage_style_xml(
    color_ramp,
    style_name,
    cmap_type,
    min_value,
    max_value,
    number_of_classes,
    opacity,
) -> str:
    """生成栅格样式 XML。"""
    style_module = get_style_module()
    normalized_ramp = _normalize_color_ramp(color_ramp, number_of_classes)
    return _capture_style_xml(
        lambda: style_module.coverage_style_xml(
            normalized_ramp,
            style_name,
            cmap_type,
            min_value,
            max_value,
            number_of_classes,
            opacity,
        )
    )


def style_outline_only_xml(color: str, width: float, geom_type: str = "polygon") -> str:
    """生成轮廓样式 XML。"""
    style_module = get_style_module()
    return _capture_style_xml(lambda: style_module.outline_only_xml(color, width, geom_type))


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
