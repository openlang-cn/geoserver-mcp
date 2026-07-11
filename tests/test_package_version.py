from geoserver_mcp import __version__


def test_package_version_matches_project_release():
    assert __version__ == "1.0.9"
