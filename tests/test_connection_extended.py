from geoserver_mcp import connection


class FakeGeoBase:
    def __init__(self, url, username=None, password=None):
        self.url = url
        self.username = username
        self.password = password


def test_get_geoserver_builds_wrapped_client_from_environment(monkeypatch):
    created = {}

    class FakeGeo(FakeGeoBase):
        def __init__(self, url, username=None, password=None):
            super().__init__(url, username=username, password=password)
            created["url"] = url
            created["username"] = username
            created["password"] = password

    monkeypatch.setenv("GEOSERVER_URL", "http://example.com/geoserver")
    monkeypatch.setenv("GEOSERVER_USER", "alice")
    monkeypatch.setenv("GEOSERVER_PASSWORD", "secret")
    monkeypatch.setattr(connection, "get_geoserver_class", lambda: FakeGeo)

    wrapped = connection.get_geoserver()

    assert created == {
        "url": "http://example.com/geoserver",
        "username": "alice",
        "password": "secret",
    }
    assert isinstance(wrapped, connection.GeoServerClient)


def test_get_geoserver_returns_none_when_vendor_client_fails(monkeypatch):
    class BrokenGeo(FakeGeoBase):
        def __init__(self, url, username=None, password=None):
            raise RuntimeError("boom")

    monkeypatch.setattr(connection, "get_geoserver_class", lambda: BrokenGeo)

    assert connection.get_geoserver() is None
