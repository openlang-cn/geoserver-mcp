import io
from contextlib import redirect_stdout

import pytest

from geoserver_mcp import main as main_module


class FakeServer:
    def __init__(self, captured, should_fail=False):
        self.captured = captured
        self.should_fail = should_fail

    def run(self, transport="stdio", mount_path=None):
        self.captured["transport"] = transport
        self.captured["mount_path"] = mount_path
        if self.should_fail:
            raise RuntimeError("server failed")


def test_main_sets_env_and_prints_remote_endpoints(monkeypatch):
    captured = {}

    def fake_create_server(**kwargs):
        captured["kwargs"] = kwargs
        return FakeServer(captured)

    monkeypatch.setattr(main_module, "create_mcp_server", fake_create_server)
    monkeypatch.setattr(
        main_module.sys,
        "argv",
        [
            "geoserver-mcp",
            "--url",
            "http://demo/geoserver",
            "--user",
            "alice",
            "--password",
            "secret",
            "--storage",
            "/tmp/data",
            "--transport",
            "sse",
            "--host",
            "0.0.0.0",
            "--port",
            "9001",
            "--mount-path",
            "/root",
            "--sse-path",
            "/events",
            "--message-path",
            "/messages-custom/",
        ],
    )

    stream = io.StringIO()
    with redirect_stdout(stream):
        main_module.main()

    output = stream.getvalue()
    assert "SSE 地址：http://0.0.0.0:9001/events" in output
    assert main_module.os.environ["GEOSERVER_URL"] == "http://demo/geoserver"
    assert main_module.os.environ["GEOSERVER_USER"] == "alice"
    assert main_module.os.environ["GEOSERVER_PASSWORD"] == "secret"
    assert main_module.os.environ["GEOSERVER_STORAGE_PATH"] == "/tmp/data"
    assert captured["kwargs"] == {
        "host": "0.0.0.0",
        "port": 9001,
        "mount_path": "/root",
        "sse_path": "/events",
        "message_path": "/messages-custom/",
        "streamable_http_path": "/mcp",
    }


def test_main_exits_with_error_when_server_run_fails(monkeypatch):
    captured = {}

    def fake_create_server(**kwargs):
        captured["kwargs"] = kwargs
        return FakeServer(captured, should_fail=True)

    monkeypatch.setattr(main_module, "create_mcp_server", fake_create_server)
    monkeypatch.setattr(main_module.sys, "argv", ["geoserver-mcp"])

    with pytest.raises(SystemExit) as exc:
        main_module.main()

    assert exc.value.code == 1
