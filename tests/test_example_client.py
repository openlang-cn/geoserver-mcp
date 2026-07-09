import argparse
import importlib.util
import sys
from pathlib import Path


def load_example_module():
    module_path = Path(__file__).resolve().parents[1] / "examples" / "client.py"
    spec = importlib.util.spec_from_file_location("example_client", module_path)
    module = importlib.util.module_from_spec(spec)
    original_argv = sys.argv[:]
    try:
        sys.argv = [str(module_path)]
        spec.loader.exec_module(module)
    finally:
        sys.argv = original_argv
    return module


def test_build_server_params_uses_pypi_uvx_launcher(monkeypatch):
    monkeypatch.setenv("GEOSERVER_URL", "http://env.example/geoserver")
    monkeypatch.setenv("GEOSERVER_USER", "env-user")
    monkeypatch.setenv("GEOSERVER_PASSWORD", "env-pass")
    module = load_example_module()
    args = argparse.Namespace(
        url=None,
        user=None,
        password=None,
        server_url="http://server.example/geoserver",
        server_user="server-user",
        server_password="server-pass",
    )

    params = module.build_server_params(args)

    assert params.command == "uvx"
    assert params.args == [
        "--from",
        "open-geoserver-mcp",
        "geoserver-mcp",
        "--url",
        "http://server.example/geoserver",
        "--user",
        "server-user",
        "--password",
        "server-pass",
    ]
    assert params.env == {
        "GEOSERVER_URL": "http://env.example/geoserver",
        "GEOSERVER_USER": "env-user",
        "GEOSERVER_PASSWORD": "env-pass",
    }
