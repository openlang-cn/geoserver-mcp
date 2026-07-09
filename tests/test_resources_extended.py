from geoserver_mcp import resources


class FakeResourceClient:
    def __init__(self, fail=None):
        self.fail = fail

    def get_workspaces(self):
        if self.fail == "workspaces":
            raise RuntimeError("workspaces failed")
        return {"workspaces": {"workspace": [{"name": "fire_monitor"}, {"name": "demo"}]}}

    def get_layer(self, layer, workspace):
        if self.fail == "layer":
            raise RuntimeError("layer failed")
        return {"layer": layer, "workspace": workspace}

    def get_wms_capabilities(self):
        if self.fail == "wms":
            raise RuntimeError("wms failed")
        return {"content": "<wms />"}

    def get_wfs_capabilities(self):
        if self.fail == "wfs":
            raise RuntimeError("wfs failed")
        return {"content": "<wfs />"}


class FakeMCP:
    def __init__(self):
        self.registered = []

    def resource(self, uri):
        def decorator(fn):
            self.registered.append((uri, fn))
            return fn

        return decorator


def test_resources_cover_success_no_connection_and_error_paths(monkeypatch):
    monkeypatch.setattr(resources, "get_geoserver", lambda: FakeResourceClient())
    assert resources.get_workspaces_resource() == {"workspaces": ["fire_monitor", "demo"]}
    assert resources.get_layer_resource("demo", "roads") == {"layer": "roads", "workspace": "demo"}
    assert resources.get_wms_resource("GetCapabilities") == {
        "service": "WMS",
        "request": "GetCapabilities",
        "capabilities": {"content": "<wms />"},
    }
    assert resources.get_wfs_resource("GetCapabilities") == {
        "service": "WFS",
        "request": "GetCapabilities",
        "capabilities": {"content": "<wfs />"},
    }

    monkeypatch.setattr(resources, "get_geoserver", lambda: None)
    assert resources.get_workspaces_resource() == {"error": "未连接到 GeoServer。"}
    assert resources.get_layer_resource("demo", "roads") == {"error": "未连接到 GeoServer。"}

    monkeypatch.setattr(resources, "get_geoserver", lambda: FakeResourceClient(fail="wms"))
    assert resources.get_wms_resource("GetCapabilities") == {"error": "wms failed"}

    monkeypatch.setattr(resources, "get_geoserver", lambda: FakeResourceClient(fail="wfs"))
    assert resources.get_wfs_resource("GetCapabilities") == {"error": "wfs failed"}

    monkeypatch.setattr(resources, "get_geoserver", lambda: FakeResourceClient(fail="layer"))
    assert resources.get_layer_resource("demo", "roads") == {"error": "layer failed"}


def test_register_resources_registers_every_registry_entry():
    mcp = FakeMCP()

    resources.register_resources(mcp)

    assert [uri for uri, _ in mcp.registered] == [
        "geoserver://catalog/workspaces",
        "geoserver://catalog/layers/{workspace}/{layer}",
        "geoserver://services/wms/{request}",
        "geoserver://services/wfs/{request}",
    ]
