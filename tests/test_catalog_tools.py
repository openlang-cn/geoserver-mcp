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

    def create_workspace(self, workspace):
        self.calls.append(("create_workspace", workspace))
        return "created"

    def edit_featuretype(self, store_name, workspace, featuretype, **kwargs):
        self.calls.append(("edit_featuretype", store_name, workspace, featuretype, kwargs))
        return {"ok": True}

    def get_featuretypes(self, workspace, store_name):
        self.calls.append(("get_featuretypes", workspace, store_name))
        return ["roads"]

    def get_feature_attribute(self, featuretype, workspace, store_name):
        self.calls.append(("get_feature_attribute", featuretype, workspace, store_name))
        return ["id", "name"]

    def create_layergroup(
        self,
        name="group",
        mode="single",
        title="group",
        abstract_text="group",
        layers=None,
        workspace=None,
        formats="html",
        metadata=None,
        keywords=None,
    ):
        self.calls.append(
            (
                "create_layergroup",
                {
                    "name": name,
                    "mode": mode,
                    "title": title,
                    "abstract_text": abstract_text,
                    "layers": layers or [],
                    "workspace": workspace,
                    "formats": formats,
                    "metadata": metadata or [],
                    "keywords": keywords or [],
                },
            )
        )
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


def test_create_workspace_detects_existing_workspace_from_normalized_names(monkeypatch):
    fake = FakeCatalogClient()
    monkeypatch.setattr(catalog, "require_geoserver", lambda: fake)

    result = catalog.create_workspace("demo")

    assert result == {"status": "info", "workspace": "demo", "message": "工作区‘demo’已存在。"}
    assert fake.calls == [("get_workspaces",)]


def test_featuretype_tools_delegate_in_geo_parameter_order(monkeypatch):
    fake = FakeCatalogClient()
    monkeypatch.setattr(catalog, "require_geoserver", lambda: fake)

    result = catalog.edit_featuretype("demo", "pg", "roads", "{'name': 'roads', 'title': 'Roads'}")

    assert result == {"ok": True}
    assert catalog.get_featuretypes("demo", "pg") == ["roads"]
    assert catalog.get_feature_attribute("demo", "pg", "roads") == ["id", "name"]
    assert fake.calls == [
        ("edit_featuretype", "pg", "demo", "roads", {"name": "roads", "title": "Roads"}),
        ("get_featuretypes", "demo", "pg"),
        ("get_feature_attribute", "roads", "demo", "pg"),
    ]


def test_create_layergroup_passes_geo_supported_metadata_and_keywords(monkeypatch):
    fake = FakeCatalogClient()
    monkeypatch.setattr(catalog, "require_geoserver", lambda: fake)

    result = catalog.create_layergroup(
        "demo",
        "transport",
        ["roads"],
        metadata=[{"about": "meta", "content_url": "https://example.com/meta.xml"}],
        keywords=["roads", "transport"],
        mode="named",
    )

    assert result == {"ok": True}
    assert fake.calls == [
        (
            "create_layergroup",
            {
                "name": "transport",
                "mode": "named",
                "title": "transport",
                "abstract_text": "transport",
                "layers": ["roads"],
                "workspace": "demo",
                "formats": "html",
                "metadata": [{"about": "meta", "content_url": "https://example.com/meta.xml"}],
                "keywords": ["roads", "transport"],
            },
        )
    ]
