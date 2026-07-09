from typing import get_type_hints

from geoserver_mcp import resources
from geoserver_mcp.tools import catalog, security, styles, system


def test_tool_return_annotations_match_vendor_contracts():
    assert get_type_hints(security.create_user)["return"] is str
    assert get_type_hints(security.delete_user)["return"] is str
    assert get_type_hints(security.get_all_users)["return"] is dict
    assert get_type_hints(security.modify_user)["return"] is str
    assert get_type_hints(security.create_usergroup)["return"] is str
    assert get_type_hints(security.delete_usergroup)["return"] is str
    assert get_type_hints(security.get_all_usergroups)["return"] is dict

    assert get_type_hints(catalog.delete_coveragestore)["return"] is str
    assert get_type_hints(catalog.create_layergroup)["return"] is str
    assert get_type_hints(catalog.add_layer_to_layergroup)["return"] is type(None)
    assert get_type_hints(catalog.remove_layer_from_layergroup)["return"] is type(None)
    assert get_type_hints(catalog.delete_layergroup)["return"] is str
    assert get_type_hints(catalog.update_layergroup)["return"] is str
    assert get_type_hints(catalog.publish_featurestore)["return"] is int
    assert get_type_hints(catalog.publish_featurestore_sqlview)["return"] is int
    assert get_type_hints(catalog.edit_featuretype)["return"] is int
    assert get_type_hints(catalog.get_featuretypes)["return"] == list[str]
    assert get_type_hints(catalog.get_feature_attribute)["return"] == list[str]

    assert get_type_hints(styles.publish_style)["return"] is int
    assert get_type_hints(styles.create_catagorized_featurestyle)["return"] is int
    assert get_type_hints(styles.create_classified_featurestyle)["return"] is int
    assert get_type_hints(styles.create_coveragestyle)["return"] is int
    assert get_type_hints(styles.create_outline_featurestyle)["return"] is int
    assert get_type_hints(styles.style_coverage_style_colormapentry)["return"] is str
    assert get_type_hints(styles.style_coverage_style_xml)["return"] is str

    assert get_type_hints(system.publish_time_dimension_to_coveragestore)["return"] is dict


def test_resource_registry_exposes_only_supported_capabilities_uris():
    assert [uri for uri, _ in resources.RESOURCE_REGISTRY] == [
        "geoserver://catalog/workspaces",
        "geoserver://catalog/layers/{workspace}/{layer}",
        "geoserver://services/wms/GetCapabilities",
        "geoserver://services/wfs/GetCapabilities",
    ]
