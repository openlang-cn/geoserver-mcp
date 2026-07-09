from types import SimpleNamespace

from geoserver_mcp import connection


def test_get_geoserver_class_suppresses_vendor_syntax_warning(monkeypatch):
    calls = []

    def fake_filterwarnings(action, message=None, category=None, module=None):
        calls.append((action, message, category, module))

    def fake_import_module(name):
        assert name == "geo.Geoserver"
        return SimpleNamespace(Geoserver="FakeGeoserver")

    monkeypatch.setattr(connection.warnings, "filterwarnings", fake_filterwarnings)
    monkeypatch.setattr(connection.importlib, "import_module", fake_import_module)

    assert connection.get_geoserver_class() == "FakeGeoserver"
    assert calls == [
        (
            "ignore",
            r"invalid escape sequence '\\w'",
            SyntaxWarning,
            r"geo\.Geoserver",
        )
    ]
