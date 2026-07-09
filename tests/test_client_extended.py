from geoserver_mcp.client import GeoServerClient


class FakeResponse:
    def __init__(self, status_code=200, text="", payload=None):
        self.status_code = status_code
        self.text = text
        self._payload = payload or {}

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError("request failed")


class FakeGeo:
    def __init__(self):
        self.calls = []
        self.service_url = "http://example.com/geoserver"

    def __getattr__(self, item):
        def recorder(*args, **kwargs):
            self.calls.append((item, args, kwargs))
            return {"method": item, "args": args, "kwargs": kwargs}

        return recorder

    def _requests(self, **kwargs):
        self.calls.append(("request", kwargs))
        params = kwargs.get("params", {})
        if params.get("service") == "WFS" and params.get("request") == "GetFeature":
            return FakeResponse(payload={"features": [{"id": 1}]})
        if params.get("service") == "WMS":
            return FakeResponse(status_code=200, text="<wms />")
        if params.get("service") == "WFS":
            return FakeResponse(status_code=200, text="<wfs />")
        return FakeResponse(payload={"ok": True})

    def upload_style(self, **kwargs):
        self.calls.append(("upload_style", kwargs))
        return 200

    def create_datastore(self, *args, **kwargs):
        self.calls.append(("create_datastore", args, kwargs))
        return {"ok": True}

    def create_coveragestore(self, *args, **kwargs):
        self.calls.append(("create_coveragestore", args, kwargs))
        return {"ok": True}

    def create_gpkg_datastore(self, *args, **kwargs):
        self.calls.append(("create_gpkg_datastore", args, kwargs))
        return {"ok": True}

    def create_shp_datastore(self, *args, **kwargs):
        self.calls.append(("create_shp_datastore", args, kwargs))
        return {"ok": True}

    def publish_featurestore(self, **kwargs):
        self.calls.append(("publish_featurestore", kwargs))
        return 201

    def publish_featurestore_sqlview(
        self,
        *,
        name,
        store_name,
        sql,
        parameters,
        key_column,
        geom_name,
        geom_type,
        srid,
        workspace,
    ):
        self.calls.append(
            (
                "publish_featurestore_sqlview",
                {
                    "name": name,
                    "store_name": store_name,
                    "sql": sql,
                    "parameters": parameters,
                    "key_column": key_column,
                    "geom_name": geom_name,
                    "geom_type": geom_type,
                    "srid": srid,
                    "workspace": workspace,
                },
            )
        )
        return {"sqlview": True}


def test_client_request_and_capabilities_methods():
    geo = FakeGeo()
    client = GeoServerClient(geo)

    response = client.request("get", "/rest/about/version")
    wms = client.get_wms_capabilities()
    wfs = client.get_wfs_capabilities()

    assert response.json() == {"ok": True}
    assert wms == {"content": "<wms />", "status_code": 200}
    assert wfs == {"content": "<wfs />", "status_code": 200}


def test_client_passthrough_methods_delegate_to_underlying_geo():
    geo = FakeGeo()
    client = GeoServerClient(geo)

    assert client.service_url == "http://example.com/geoserver"
    assert client.some_missing_method("arg") == {
        "method": "some_missing_method",
        "args": ("arg",),
        "kwargs": {},
    }
    assert client.get_workspace("demo")["method"] == "get_workspace"
    assert client.get_default_workspace()["method"] == "get_default_workspace"
    assert client.set_default_workspace("demo")["method"] == "set_default_workspace"
    assert client.get_featurestore("pg", "demo")["method"] == "get_featurestore"
    assert client.get_style("roads", workspace="demo")["method"] == "get_style"
    assert client.get_styles(workspace="demo")["method"] == "get_styles"
    assert client.delete_coverage("cov", workspace="demo")["method"] == "delete_coveragestore"
    assert client.delete_featurestore("pg", workspace="demo")["method"] == "delete_featurestore"


def test_client_store_methods_handle_success_and_required_path():
    geo = FakeGeo()
    client = GeoServerClient(geo)

    gpkg = client.create_gpkg_datastore("demo", "roads", "/tmp/roads.gpkg")
    shp = client.create_shp_datastore("demo", "roads", "/tmp/roads.zip")
    uploaded = client.upload_style("/tmp/roads.sld", name="roads", workspace="demo")

    assert gpkg == {"ok": True}
    assert shp == {"ok": True}
    assert uploaded == 200

    try:
        client.create_datastore("roads", "demo")
    except ValueError as exc:
        assert "必填项" in str(exc)
    else:
        raise AssertionError("expected create_datastore to require path")

    try:
        client.create_coveragestore("demo", "landsat")
    except ValueError as exc:
        assert "必填项" in str(exc)
    else:
        raise AssertionError("expected create_coveragestore to require path")


def test_client_delete_datastore_requires_workspace():
    client = GeoServerClient(FakeGeo())

    try:
        client.delete_datastore("roads")
    except ValueError as exc:
        assert "workspace" in str(exc)
    else:
        raise AssertionError("expected delete_datastore to require workspace")


def test_client_query_features_and_generate_map():
    geo = FakeGeo()
    client = GeoServerClient(geo)

    features = client.query_features(
        "demo",
        "roads",
        filter="PERSONS > 1",
        properties=["name", "persons"],
        max_features=10,
    )
    generated = client.generate_map(
        ["demo:roads"],
        styles=["roads-style"],
        bbox=[1.0, 2.0, 3.0, 4.0],
        width=512,
        height=256,
        format="image/png",
    )
    default_map = client.generate_map(["demo:roads"])

    assert features == {"features": [{"id": 1}]}
    assert generated["params"]["styles"] == "roads-style"
    assert generated["params"]["bbox"] == "1.0,2.0,3.0,4.0"
    assert generated["url"].startswith("http://example.com/geoserver/wms?")
    assert default_map["params"]["bbox"] == "-180,-90,180,90"


def test_client_publish_and_service_update_helpers():
    geo = FakeGeo()
    client = GeoServerClient(geo)

    sqlview = client.publish_featurestore_sqlview(
        "pg",
        {
            "name": "roads_view",
            "sql": "select * from roads",
            "key_column": "id",
        },
        [{"name": "limit", "default_value": "10"}],
        "demo",
    )
    published = client.publish_featurestore(
        "pg",
        {
            "table": "roads",
            "title": "Roads",
            "advertised": False,
            "abstract": "demo",
            "keywords": ["roads"],
            "cqlfilter": "INCLUDE",
        },
        "demo",
    )
    service = client.update_service("wms", {"enabled": True})
    timed = client.publish_time_dimension_to_coveragestore("landsat", "demo")

    assert sqlview == {"sqlview": True}
    assert published == 201
    assert service["method"] == "update_service"
    assert timed["method"] == "publish_time_dimension_to_coveragestore"
