import os

from geoserver_mcp.tools import catalog


class FakeCatalogClient:
    def __init__(self):
        self.calls = []

    def get_workspaces(self):
        self.calls.append(("get_workspaces",))
        return {"workspaces": {"workspace": [{"name": "fire_monitor"}, {"name": "demo"}]}}

    def get_workspace(self, workspace):
        self.calls.append(("get_workspace", workspace))
        return {"workspace": workspace}

    def get_default_workspace(self):
        self.calls.append(("get_default_workspace",))
        return {"workspace": {"name": "demo"}}

    def set_default_workspace(self, workspace):
        self.calls.append(("set_default_workspace", workspace))
        return "ok"

    def get_featurestore(self, store_name, workspace):
        self.calls.append(("get_featurestore", store_name, workspace))
        return {"store": store_name, "workspace": workspace}

    def delete_featurestore(self, name, workspace):
        self.calls.append(("delete_featurestore", name, workspace))
        return "deleted"

    def create_datastore(self, name, workspace, **params):
        self.calls.append(("create_datastore", name, workspace, params))
        return {"ok": True}


def test_workspace_tools_delegate(monkeypatch):
    fake = FakeCatalogClient()
    monkeypatch.setattr(catalog, "require_geoserver", lambda: fake)

    assert catalog.list_workspaces() == ["fire_monitor", "demo"]
    assert catalog.get_workspace("demo") == {"workspace": "demo"}
    assert catalog.get_default_workspace() == {"workspace": {"name": "demo"}}
    assert catalog.set_default_workspace("demo") == "ok"
    assert fake.calls == [
        ("get_workspaces",),
        ("get_workspace", "demo"),
        ("get_default_workspace",),
        ("set_default_workspace", "demo"),
    ]


def test_featurestore_tools_delegate(monkeypatch):
    fake = FakeCatalogClient()
    monkeypatch.setattr(catalog, "require_geoserver", lambda: fake)

    assert catalog.get_featurestore("demo", "pg") == {"store": "pg", "workspace": "demo"}
    assert catalog.delete_featurestore("demo", "pg") == "deleted"

    assert fake.calls == [
        ("get_featurestore", "pg", "demo"),
        ("delete_featurestore", "pg", "demo"),
    ]


def test_create_datastore_resolves_relative_storage_path(monkeypatch):
    fake = FakeCatalogClient()
    monkeypatch.setattr(catalog, "require_geoserver", lambda: fake)
    monkeypatch.setenv("GEOSERVER_STORAGE_PATH", "D:/data")

    catalog.create_datastore("demo", "roads", {"path": "roads"})

    assert fake.calls == [
        ("create_datastore", "roads", "demo", {"path": os.path.join("D:/data", "roads")})
    ]
