"""REST API 适配器——geoserver-rest 库不支持的方法。"""

from __future__ import annotations

from typing import Any


class GeoServerRESTAdapter:
    """直接 REST API 调用适配器。

    所有 geoserver-rest 库不支持的方法集中在此，通过 self.request 直接组装
    GeoServer REST API 请求。新增时只需在此类添加方法。
    """

    def __init__(self, client: Any) -> None:
        self._client = client

    def get_featuretype(self, workspace: str, store_name: str, featuretype: str) -> dict[str, Any]:
        """获取要素类型完整元数据，包括 SQL 视图定义。"""
        response = self._client.request(
            "get",
            f"/rest/workspaces/{workspace}/datastores/{store_name}/featuretypes/{featuretype}.json",
        )
        response.raise_for_status()
        return response.json()

    def recalculate_featuretype_bbox(
        self, workspace: str, store_name: str, featuretype: str
    ) -> dict[str, Any]:
        """重新计算要素类型的原生和经纬度边界框。"""
        response = self._client.request(
            "put",
            f"/rest/workspaces/{workspace}/datastores/{store_name}/featuretypes/{featuretype}.json"
            "?recalculate=nativebbox,latlonbbox",
        )
        response.raise_for_status()
        return {
            "status": "success",
            "featuretype": featuretype,
            "message": "Bounding boxes recalculated.",
        }
