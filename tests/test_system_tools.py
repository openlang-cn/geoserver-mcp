from geoserver_mcp.tools import system


class FakeSystemClient:
    def __init__(self):
        self.calls = []

    def get_manifest(self):
        self.calls.append(("get_manifest",))
        return {"manifest": True}

    def get_status(self):
        self.calls.append(("get_status",))
        return {"status": "ok"}

    def get_system_status(self):
        self.calls.append(("get_system_status",))
        return {"system": "ok"}

    def get_version(self):
        self.calls.append(("get_version",))
        return {"about": {"resource": [{"@name": "GeoServer", "Version": "2.26.0"}]}}

    def reload(self):
        self.calls.append(("reload",))
        return "reloaded"

    def reset(self):
        self.calls.append(("reset",))
        return "reset"

    def update_service(self, service, options):
        self.calls.append(("update_service", service, options))
        return "updated"

    def publish_time_dimension_to_coveragestore(
        self,
        store_name,
        workspace,
        presentation,
        units,
        default_value,
        content_type,
    ):
        self.calls.append(
            (
                "publish_time_dimension_to_coveragestore",
                store_name,
                workspace,
                presentation,
                units,
                default_value,
                content_type,
            )
        )
        return {"timed": True}


class FakeMCP:
    def __init__(self):
        self.registered = []

    def tool(self):
        def decorator(fn):
            self.registered.append(fn.__name__)
            return fn

        return decorator


def test_system_tools_delegate_and_register(monkeypatch):
    fake = FakeSystemClient()
    monkeypatch.setattr(system, "require_geoserver", lambda: fake)

    assert system.get_manifest() == {"manifest": True}
    assert system.get_status() == {"status": "ok"}
    assert system.get_system_status() == {"system": "ok"}
    assert system.get_version() == {
        "about": {"resource": [{"@name": "GeoServer", "Version": "2.26.0"}]}
    }
    assert system.reload_geoserver() == "reloaded"
    assert system.reset_geoserver() == "reset"
    assert system.update_service("wms", {"enabled": True}) == "updated"
    assert (
        system.publish_time_dimension_to_coveragestore("landsat", "demo") == {"timed": True}
    )

    mcp = FakeMCP()
    system.register_tools(mcp)

    assert mcp.registered == [
        "get_manifest",
        "get_status",
        "get_system_status",
        "get_version",
        "reload_geoserver",
        "reset_geoserver",
        "update_service",
        "publish_time_dimension_to_coveragestore",
    ]
