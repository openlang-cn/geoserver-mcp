from geoserver_mcp import main as main_module


def test_main_uses_streamable_http_transport(monkeypatch):
    captured = {}

    class FakeServer:
        def run(self, transport="stdio", mount_path=None):
            captured["transport"] = transport
            captured["mount_path"] = mount_path

    def fake_create_server(**kwargs):
        captured["kwargs"] = kwargs
        return FakeServer()

    monkeypatch.setattr(main_module, "create_mcp_server", fake_create_server)
    monkeypatch.setattr(
        main_module.sys,
        "argv",
        [
            "geoserver-mcp",
            "--transport",
            "streamable-http",
            "--host",
            "0.0.0.0",
            "--port",
            "9000",
            "--streamable-http-path",
            "/remote-mcp",
        ],
    )

    main_module.main()

    assert captured["kwargs"] == {
        "host": "0.0.0.0",
        "port": 9000,
        "mount_path": "/",
        "sse_path": "/sse",
        "message_path": "/messages/",
        "streamable_http_path": "/remote-mcp",
    }
    assert captured["transport"] == "streamable-http"
    assert captured["mount_path"] == "/"
