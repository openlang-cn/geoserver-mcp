from geoserver_mcp import resources


class FakeResourceClient:
    def get_workspaces(self):
        return {"workspaces": {"workspace": [{"name": "fire_monitor"}, {"name": "demo"}]}}


def test_get_workspaces_resource_normalizes_names(monkeypatch):
    monkeypatch.setattr(resources, "get_geoserver", lambda: FakeResourceClient())

    assert resources.get_workspaces_resource() == {
        "workspaces": ["fire_monitor", "demo"]
    }
