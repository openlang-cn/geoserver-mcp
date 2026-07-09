import os
from pathlib import Path

from geoserver_mcp.tools import styles


class FakeStyleClient:
    def __init__(self):
        self.calls = []

    def create_style(self, name, sld, workspace=None):
        self.calls.append(("create_style", name, sld, workspace))
        return 200

    def upload_style(self, path, name=None, workspace=None, sld_version="1.0.0"):
        self.calls.append(("upload_style", path, name, workspace, sld_version))
        return 201

    def get_style(self, name, workspace=None):
        self.calls.append(("get_style", name, workspace))
        return {"style": name}

    def get_styles(self, workspace=None):
        self.calls.append(("get_styles", workspace))
        return {"styles": []}

    def create_coveragestyle(self, raster_path, **params):
        self.calls.append(("create_coveragestyle", raster_path, params))
        return 201

    def create_outline_featurestyle(
        self,
        style_name,
        color="#3579b1",
        width="2",
        geom_type="polygon",
        workspace=None,
    ):
        self.calls.append(
            ("create_outline_featurestyle", style_name, color, width, geom_type, workspace)
        )
        return 201


def test_create_style_returns_normalized_response(monkeypatch):
    fake = FakeStyleClient()
    monkeypatch.setattr(styles, "require_geoserver", lambda: fake)

    result = styles.create_style("demo", "<sld/>", workspace="ws")

    assert result == {"status": "success", "name": "demo", "workspace": "ws", "result": 200}
    assert fake.calls == [("create_style", "demo", "<sld/>", "ws")]


def test_upload_style_resolves_storage_path(monkeypatch):
    fake = FakeStyleClient()
    monkeypatch.setattr(styles, "require_geoserver", lambda: fake)
    monkeypatch.setenv("GEOSERVER_STORAGE_PATH", "D:/styles")

    result = styles.upload_style("demo.sld", name="demo")

    assert result == {"status": "success", "name": "demo", "workspace": "global", "result": 201}
    assert fake.calls == [
        ("upload_style", os.path.join("D:/styles", "demo.sld"), "demo", None, "1.0.0")
    ]


def test_get_style_tools_delegate(monkeypatch):
    fake = FakeStyleClient()
    monkeypatch.setattr(styles, "require_geoserver", lambda: fake)

    assert styles.get_style("demo") == {"style": "demo"}
    assert styles.get_styles("ws") == {"styles": []}
    assert fake.calls == [("get_style", "demo", None), ("get_styles", "ws")]


def test_create_coveragestyle_extracts_raster_path_from_params(monkeypatch):
    fake = FakeStyleClient()
    monkeypatch.setattr(styles, "require_geoserver", lambda: fake)
    monkeypatch.setenv("GEOSERVER_STORAGE_PATH", "D:/rasters")

    result = styles.create_coveragestyle(
        "landsat",
        {"raster_path": "landsat.tif", "workspace": "demo"},
    )

    assert result == 201
    assert fake.calls == [
        (
            "create_coveragestyle",
            os.path.join("D:/rasters", "landsat.tif"),
            {"style_name": "landsat", "workspace": "demo"},
        )
    ]


def test_create_outline_featurestyle_passes_color_width_geom_type_and_workspace(monkeypatch):
    fake = FakeStyleClient()
    monkeypatch.setattr(styles, "require_geoserver", lambda: fake)

    result = styles.create_outline_featurestyle(
        "roads-outline",
        "#ff0000",
        workspace="demo",
        width="4",
        geom_type="line",
    )

    assert result == 201
    assert fake.calls == [
        ("create_outline_featurestyle", "roads-outline", "#ff0000", "4", "line", "demo")
    ]


def test_style_xml_helpers_capture_written_sld_file(monkeypatch, tmp_path):
    class FakeStyleModule:
        @staticmethod
        def outline_only_xml(color, width, geom_type="polygon"):
            Path("style.sld").write_text(
                f"outline:{color}:{width}:{geom_type}",
                encoding="utf-8",
            )

        @staticmethod
        def catagorize_xml(column_name, values, color_ramp=None, geom_type="polygon"):
            Path("style.sld").write_text(
                f"categorize:{column_name}:{values}:{color_ramp}:{geom_type}",
                encoding="utf-8",
            )

        @staticmethod
        def classified_xml(
            style_name,
            column_name,
            values,
            color_ramp=None,
            geom_type="polygon",
        ):
            Path("style.sld").write_text(
                f"classified:{style_name}:{column_name}:{values}:{color_ramp}:{geom_type}",
                encoding="utf-8",
            )

        @staticmethod
        def coverage_style_xml(
            color_ramp,
            style_name,
            cmap_type,
            min_value,
            max_value,
            number_of_classes,
            opacity,
        ):
            Path("style.sld").write_text(
                (
                    f"coverage:{style_name}:{cmap_type}:{min_value}:"
                    f"{max_value}:{number_of_classes}:{opacity}"
                ),
                encoding="utf-8",
            )

    monkeypatch.setattr(styles, "get_style_module", lambda: FakeStyleModule)

    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        assert (
            styles.style_outline_only_xml("#ff0000", 2.0, "polygon")
            == "outline:#ff0000:2.0:polygon"
        )
        assert (
            styles.style_catagorize_xml("level", [1, 2], "viridis", "polygon")
            == "categorize:level:[1, 2]:viridis:polygon"
        )
        assert (
            styles.style_classified_xml("demo", "level", [1, 2], "viridis", "polygon")
            == "classified:demo:level:[1, 2]:viridis:polygon"
        )
        assert (
            styles.style_coverage_style_xml("viridis", "demo", "ramp", 0, 10, 3, 1.0)
            == "coverage:demo:ramp:0:10:3:1.0"
        )
    finally:
        os.chdir(cwd)


def test_style_coverage_style_colormapentry_supports_named_palette():
    xml = styles.style_coverage_style_colormapentry("viridis", 0, 10, 3)

    assert 'color="#' in xml
    assert 'color="v"' not in xml
