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

    def _requests(self, **kwargs):
        self.calls.append(("request", kwargs))
        return FakeResponse(payload={"type": "FeatureCollection"})


def test_create_style_uses_upload_style():
    geo = FakeGeo()
    client = GeoServerClient(geo)

    result = client.create_style("demo", "<StyledLayerDescriptor/>", workspace="ws")

    assert result == 200
    assert geo.calls[0] == (
        "upload_style",
        {"path": "<StyledLayerDescriptor/>", "name": "demo", "workspace": "ws"},
    )


def test_create_datastore_adapts_path_and_workspace():
    geo = FakeGeo()
    client = GeoServerClient(geo)

    client.create_datastore("roads", "demo", path="/tmp/roads", overwrite=True)

    assert geo.calls[0] == (
        "create_datastore",
        ("roads", "/tmp/roads"),
        {"workspace": "demo", "overwrite": True},
    )


def test_create_coveragestore_maps_common_params():
    geo = FakeGeo()
    client = GeoServerClient(geo)

    client.create_coveragestore("demo", "landsat", path="/tmp/a.tif", type="GeoTIFF")

    assert geo.calls[0] == (
        "create_coveragestore",
        ("/tmp/a.tif",),
        {
            "workspace": "demo",
            "layer_name": "landsat",
            "file_type": "GeoTIFF",
            "content_type": "image/tiff",
        },
    )


def test_create_layer_uses_publish_featurestore():
    geo = FakeGeo()
    client = GeoServerClient(geo)

    client.create_layer("demo", "postgis", "roads_layer", "roads")

    assert geo.calls[0] == (
        "publish_featurestore",
        {
            "store_name": "postgis",
            "pg_table": "roads",
            "workspace": "demo",
            "title": "roads_layer",
        },
    )
