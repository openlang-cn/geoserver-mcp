"""样式相关工具。"""

from __future__ import annotations

import importlib
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Annotated, Any

from pydantic import Field

from ..utils import require_geoserver, resolve_storage_path


def get_style_module() -> Any:
    """延迟加载 geo.Style，避免模块导入阶段绑定运行环境。"""
    return importlib.import_module("geo.Style")


def _normalize_color_ramp(color_ramp, number_of_classes: int | None = None):
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


def create_style(
    name: Annotated[
        str,
        Field(description="样式名称")
    ],
    sld: Annotated[
        str,
        Field(description="SLD 样式 XML 字符串")
    ],
    workspace: Annotated[
        str | None,
        Field(description="工作区名称，不填则为全局样式")
    ] = None,
) -> dict:
    """创建样式。"""
    result = require_geoserver().create_style(name, sld, workspace)
    return {"status": "success", "name": name, "workspace": workspace or "global", "result": result}


def upload_style(
    path: Annotated[
        str,
        Field(description="样式文件路径（.sld 或 .xml，相对于 storage 目录或绝对路径）")
    ],
    name: Annotated[
        str | None,
        Field(description="样式名称，默认使用文件名")
    ] = None,
    workspace: Annotated[
        str | None,
        Field(description="工作区名称，不填则为全局样式")
    ] = None,
    sld_version: Annotated[
        str,
        Field(description="SLD 版本，如 1.0.0、1.1.0，默认 1.0.0")
    ] = "1.0.0",
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


def get_style(
    name: Annotated[
        str,
        Field(description="样式名称")
    ],
    workspace: Annotated[
        str | None,
        Field(description="工作区名称，不填则查找全局样式")
    ] = None,
) -> dict:
    """获取单个样式详情。"""
    return require_geoserver().get_style(name, workspace)


def get_styles(
    workspace: Annotated[
        str | None,
        Field(description="工作区名称，不填则列出所有样式")
    ] = None,
) -> dict:
    """列出样式。"""
    return require_geoserver().get_styles(workspace)


def publish_style(
    layer_name: Annotated[
        str,
        Field(description="图层名称")
    ],
    style_name: Annotated[
        str,
        Field(description="样式名称")
    ],
    workspace: Annotated[
        str,
        Field(description="工作区名称")
    ],
) -> int:
    """给图层绑定样式。"""
    return require_geoserver().publish_style(layer_name, style_name, workspace)


def create_catagorized_featurestyle(
    style_name: Annotated[
        str,
        Field(description="样式名称")
    ],
    column_name: Annotated[
        str,
        Field(description="用于分类的属性列名")
    ],
    column_distinct_values: Annotated[
        str,
        Field(description="属性列的 distinct 值列表，逗号分隔")
    ],
    workspace: Annotated[
        str | None,
        Field(description="工作区名称")
    ] = None,
    color_ramp: Annotated[
        str | None,
        Field(description="色带名称，如 viridis、plasma、Reds，或颜色列表")
    ] = None,
    geom_type: Annotated[
        str | None,
        Field(description="几何类型：polygon、line、point")
    ] = None,
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
    style_name: Annotated[
        str,
        Field(description="样式名称")
    ],
    column_name: Annotated[
        str,
        Field(description="用于分级的数值属性列名")
    ],
    column_distinct_values: Annotated[
        str,
        Field(description="属性列的 distinct 值列表，逗号分隔")
    ],
    workspace: Annotated[
        str | None,
        Field(description="工作区名称")
    ] = None,
    color_ramp: Annotated[
        str | None,
        Field(description="色带名称，如 viridis、plasma、Reds，或颜色列表")
    ] = None,
    geom_type: Annotated[
        str | None,
        Field(description="几何类型：polygon、line、point")
    ] = None,
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


def create_coveragestyle(
    style_name: Annotated[
        str,
        Field(description="样式名称")
    ],
    params: Annotated[
        dict,
        Field(
            description="栅格样式参数，必须包含 raster_path(栅格文件路径)；"
            "可选 color_ramp(默认 RdYlGn_r)、cmap_type(默认 ramp)、"
            "number_of_classes(默认 5)、opacity(默认 1)"
        )
    ],
) -> int:
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
    style_name: Annotated[
        str,
        Field(description="样式名称")
    ],
    outline_color: Annotated[
        str,
        Field(description="轮廓颜色，如 #FF0000、red")
    ],
    workspace: Annotated[
        str | None,
        Field(description="工作区名称")
    ] = None,
    width: Annotated[
        str,
        Field(description="轮廓线宽，默认 2")
    ] = "2",
    geom_type: Annotated[
        str,
        Field(description="几何类型：polygon、line、point，默认 polygon")
    ] = "polygon",
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
    column_name: Annotated[
        str,
        Field(description="用于分类的属性列名")
    ],
    values: Annotated[
        list,
        Field(description="分类值列表，如 [\"urban\", \"rural\", \"water\"]")
    ],
    color_ramp: Annotated[
        str | None,
        Field(description="色带名称，如 viridis、plasma、Reds，或颜色列表")
    ] = None,
    geom_type: Annotated[
        str,
        Field(description="几何类型：polygon、line、point，默认 polygon")
    ] = "polygon",
) -> str:
    """生成分类样式 SLD XML。"""
    style_module = get_style_module()
    return _capture_style_xml(
        lambda: style_module.catagorize_xml(column_name, values, color_ramp, geom_type)
    )


def style_classified_xml(
    style_name: Annotated[
        str,
        Field(description="样式名称")
    ],
    column_name: Annotated[
        str,
        Field(description="用于分级的数值属性列名")
    ],
    values: Annotated[
        list,
        Field(description="分级区间值列表，如 [0, 100, 500, 1000]")
    ],
    color_ramp: Annotated[
        str | None,
        Field(description="色带名称，如 viridis、plasma、Reds，或颜色列表")
    ] = None,
    geom_type: Annotated[
        str,
        Field(description="几何类型：polygon、line、point，默认 polygon")
    ] = "polygon",
) -> str:
    """生成分级样式 SLD XML。"""
    style_module = get_style_module()
    return _capture_style_xml(
        lambda: style_module.classified_xml(style_name, column_name, values, color_ramp, geom_type)
    )


def style_coverage_style_colormapentry(
    color_ramp: Annotated[
        Any,
        Field(description="色带名称或颜色列表")
    ],
    min_value: Annotated[
        float,
        Field(description="最小值")
    ],
    max_value: Annotated[
        float,
        Field(description="最大值")
    ],
    number_of_classes: Annotated[
        int | None,
        Field(description="分级数，默认 5")
    ] = None,
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
    color_ramp: Annotated[
        Any,
        Field(description="色带名称或颜色列表")
    ],
    style_name: Annotated[
        str,
        Field(description="样式名称")
    ],
    cmap_type: Annotated[
        str,
        Field(description="色带类型：ramp(渐变)、intervals(分段)")
    ],
    min_value: Annotated[
        str,
        Field(description="最小值")
    ],
    max_value: Annotated[
        str,
        Field(description="最大值")
    ],
    number_of_classes: Annotated[
        str,
        Field(description="分级数")
    ],
    opacity: Annotated[
        str,
        Field(description="不透明度，0.0-1.0")
    ],
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


def style_outline_only_xml(
    color: Annotated[
        str,
        Field(description="轮廓颜色，如 #FF0000、red")
    ],
    width: Annotated[
        float,
        Field(description="轮廓线宽")
    ],
    geom_type: Annotated[
        str,
        Field(description="几何类型：polygon、line、point，默认 polygon")
    ] = "polygon",
) -> str:
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
