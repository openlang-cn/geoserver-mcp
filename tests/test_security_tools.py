from geoserver_mcp.tools import security


class FakeSecurityClient:
    def __init__(self):
        self.calls = []

    def create_user(self, username, password, enabled=True, service=None):
        self.calls.append(("create_user", username, password, enabled, service))
        return "created"

    def delete_user(self, username, service=None):
        self.calls.append(("delete_user", username, service))
        return "deleted"

    def get_all_users(self, service=None):
        self.calls.append(("get_all_users", service))
        return {"users": []}

    def modify_user(self, username, new_name=None, new_password=None, enable=None, service=None):
        self.calls.append(("modify_user", username, new_name, new_password, enable, service))
        return "modified"

    def create_usergroup(self, name, service=None):
        self.calls.append(("create_usergroup", name, service))
        return "group-created"

    def delete_usergroup(self, name, service=None):
        self.calls.append(("delete_usergroup", name, service))
        return "group-deleted"

    def get_all_usergroups(self, service=None):
        self.calls.append(("get_all_usergroups", service))
        return {"groups": []}


def test_security_tools_delegate_supported_geo_service_parameters(monkeypatch):
    fake = FakeSecurityClient()
    monkeypatch.setattr(security, "require_geoserver", lambda: fake)

    assert security.create_user("alice", "secret", enabled=False, service="default") == "created"
    assert security.delete_user("alice", service="default") == "deleted"
    assert security.get_all_users(service="default") == {"users": []}
    assert (
        security.modify_user(
            "alice",
            new_name="alice2",
            new_password="new-secret",
            enable=True,
            service="default",
        )
        == "modified"
    )
    assert security.create_usergroup("admins", service="default") == "group-created"
    assert security.delete_usergroup("admins", service="default") == "group-deleted"
    assert security.get_all_usergroups(service="default") == {"groups": []}
    assert fake.calls == [
        ("create_user", "alice", "secret", False, "default"),
        ("delete_user", "alice", "default"),
        ("get_all_users", "default"),
        ("modify_user", "alice", "alice2", "new-secret", True, "default"),
        ("create_usergroup", "admins", "default"),
        ("delete_usergroup", "admins", "default"),
        ("get_all_usergroups", "default"),
    ]
