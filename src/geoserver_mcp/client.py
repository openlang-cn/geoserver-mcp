"""GeoServer 兼容客户端封装。"""

from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING, Any
from xml.sax.saxutils import escape as _xml_escape

from .adapters.rest import GeoServerRESTAdapter

if TYPE_CHECKING:
    from geo.Geoserver import Geoserver


class GeoServerClient:
    """对第三方 ``geo.Geoserver`` 做轻量兼容封装。"""

    def __init__(self, geo_client: Geoserver):
        self._geo = geo_client
    @property
    def rest(self) -> GeoServerRESTAdapter:
        """直接 REST API 适配器（库不支持的方法）。"""
        return GeoServerRESTAdapter(self)


    def __getattr__(self, item: str) -> Any:
        return getattr(self._geo, item)

    @property
    def service_url(self) -> str:
        return self._geo.service_url

    def request(self, method: str, path: str, **kwargs: Any):
        """使用 GeoServer 已配置的认证信息发起原始请求。"""
        url = f"{self.service_url}{path}"
        return self._geo._requests(method=method, url=url, **kwargs)

    def get_wms_capabilities(self) -> dict[str, Any]:
        response = self.request(
            "get",
            "/ows",
            params={"service": "WMS", "request": "GetCapabilities"},
        )
        return {"content": response.text, "status_code": response.status_code}

    def get_wfs_capabilities(self) -> dict[str, Any]:
        response = self.request(
            "get",
            "/ows",
            params={"service": "WFS", "request": "GetCapabilities"},
        )
        return {"content": response.text, "status_code": response.status_code}

    def create_style(self, name: str, sld: str, workspace: str | None = None) -> int:
        return self._geo.upload_style(path=sld, name=name, workspace=workspace)

    def create_datastore(self, name: str, workspace: str, **params: Any):
        path = params.pop("path", None) or params.pop("url", None)
        if not path:
            raise ValueError("params.path 或 params.url 为必填项。")
        overwrite = params.pop("overwrite", False)
        return self._geo.create_datastore(name, path, workspace=workspace, overwrite=overwrite)

    def create_coveragestore(self, workspace: str, name: str, **params: Any):
        path = params.pop("path", None) or params.pop("url", None)
        if not path:
            raise ValueError("params.path 或 params.url 为必填项。")
        file_type = params.pop("type", params.pop("file_type", "GeoTIFF"))
        content_type = params.pop("content_type", "image/tiff")
        layer_name = params.pop("layer_name", name)
        return self._geo.create_coveragestore(
            path,
            workspace=workspace,
            layer_name=layer_name,
            file_type=file_type,
            content_type=content_type,
        )

    def create_gpkg_datastore(self, workspace: str, name: str, file_path: str):
        return self._geo.create_gpkg_datastore(file_path, store_name=name, workspace=workspace)

    def create_shp_datastore(self, workspace: str, name: str, file_path: str):
        return self._geo.create_shp_datastore(file_path, store_name=name, workspace=workspace)

    def delete_datastore(self, name: str, workspace: str | None = None):
        if not workspace:
            raise ValueError("删除 datastore 时必须提供 workspace。")
        return self.request(
            "delete",
            f"/rest/workspaces/{workspace}/datastores/{name}",
            params={"recurse": "true"},
        )

    def delete_coverage(self, name: str, workspace: str | None = None):
        return self._geo.delete_coveragestore(name, workspace=workspace)

    def delete_featurestore(self, name: str, workspace: str | None = None):
        return self._geo.delete_featurestore(name, workspace=workspace)

    def create_layer(self, workspace: str, data_store: str, layer: str, source: str):
        return self._geo.publish_featurestore(
            store_name=data_store,
            pg_table=source,
            workspace=workspace,
            title=layer,
        )

    def get_workspace(self, workspace: str):
        return self._geo.get_workspace(workspace)

    def get_default_workspace(self):
        return self._geo.get_default_workspace()

    def set_default_workspace(self, workspace: str):
        return self._geo.set_default_workspace(workspace)

    def get_featurestore(self, store_name: str, workspace: str):
        return self._geo.get_featurestore(store_name, workspace)

    def get_style(self, style_name: str, workspace: str | None = None):
        return self._geo.get_style(style_name, workspace=workspace)

    def get_styles(self, workspace: str | None = None):
        return self._geo.get_styles(workspace=workspace)

    def upload_style(
        self,
        path: str,
        name: str | None = None,
        workspace: str | None = None,
        sld_version: str = "1.0.0",
    ):
        return self._geo.upload_style(
            path=path,
            name=name,
            workspace=workspace,
            sld_version=sld_version,
        )

    def query_features(
        self,
        workspace: str,
        layer: str,
        filter: str | None = None,
        properties: list[str] | None = None,
        max_features: int | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {
            "service": "WFS",
            "version": "1.0.0",
            "request": "GetFeature",
            "typeName": f"{workspace}:{layer}",
            "outputFormat": "application/json",
        }
        if filter:
            params["CQL_FILTER"] = filter
        if properties:
            params["propertyName"] = ",".join(properties)
        if max_features:
            params["maxFeatures"] = max_features

        response = self.request("get", "/ows", params=params)
        response.raise_for_status()
        return response.json()


    def generate_map(
        self,
        layers: list[str],
        styles: list[str] | None = None,
        bbox: list[float] | None = None,
        width: int = 1024,
        height: int = 768,
        format: str = "image/png",
    ) -> dict[str, Any]:
        if bbox is None:
            bbox = [-180, -90, 180, 90]

        params = {
            "service": "WMS",
            "version": "1.1.0",
            "request": "GetMap",
            "layers": ",".join(layers),
            "bbox": ",".join(str(value) for value in bbox),
            "width": width,
            "height": height,
            "srs": "EPSG:4326",
            "format": format,
        }
        if styles:
            params["styles"] = ",".join(styles)

        query_string = "&".join(f"{key}={value}" for key, value in params.items())
        url = f"{self.service_url}/wms?{query_string}"
        return {"url": url, "params": params}

    def edit_featuretype(
        self,
        store_name: str,
        workspace: str | None,
        pg_table: str,
        **kwargs: Any,
    ):
        return self._geo.edit_featuretype(
            store_name=store_name,
            workspace=workspace,
            pg_table=pg_table,
            name=_xml_escape(kwargs.get("name", pg_table)),
            title=_xml_escape(kwargs.get("title", pg_table)),
            abstract=_xml_escape(kwargs["abstract"]) if kwargs.get("abstract") else None,
            keywords=[_xml_escape(k) for k in kwargs["keywords"]]
            if kwargs.get("keywords")
            else None,
            recalculate=kwargs.get("recalculate"),
        )

    def publish_featurestore_sqlview(
        self,
        store_name: str,
        params: dict[str, Any],
        sqlview_params: Iterable[dict[str, Any]],
        workspace: str,
    ):
        return self._geo.publish_featurestore_sqlview(
            name=_xml_escape(params["name"]),
            store_name=store_name,
            sql=_xml_escape(params["sql"]),
            parameters=list(sqlview_params),
            key_column=params.get("key_column"),
            geom_name=params.get("geom_name", "geom"),
            geom_type=params.get("geom_type", "Geometry"),
            srid=params.get("srid", 4326),
            workspace=workspace,
        )

    def publish_featurestore(self, store_name: str, params: dict[str, Any], workspace: str):
        keywords = params.get("keywords")
        if keywords:
            keywords = [_xml_escape(k) for k in keywords]
        cqlfilter = params.get("cqlfilter")
        if cqlfilter:
            cqlfilter = _xml_escape(cqlfilter)
        return self._geo.publish_featurestore(
            store_name=store_name,
            pg_table=_xml_escape(params["table"]),
            workspace=workspace,
            title=_xml_escape(params.get("title", "")) if params.get("title") else None,
            advertised=params.get("advertised", True),
            abstract=_xml_escape(params["abstract"]) if params.get("abstract") else None,
            keywords=keywords,
            cqlfilter=cqlfilter,
        )

    def update_service(self, service: str, options: dict[str, Any]):
        return self._geo.update_service(service, **options)

    def publish_time_dimension_to_coveragestore(
        self,
        store_name: str | None = None,
        workspace: str | None = None,
        presentation: str = "LIST",
        units: str = "ISO8601",
        default_value: str = "MINIMUM",
        content_type: str = "application/xml; charset=UTF-8",
    ):
        return self._geo.publish_time_dimension_to_coveragestore(
            store_name,
            workspace,
            presentation,
            units,
            default_value,
            content_type,
        )

