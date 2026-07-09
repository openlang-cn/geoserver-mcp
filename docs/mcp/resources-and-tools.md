# MCP Resources and Tools

## Resource Endpoints

- `geoserver://catalog/workspaces`
- `geoserver://catalog/layers/{workspace}/{layer}`
- `geoserver://services/wms/{request}`
- `geoserver://services/wfs/{request}`

## Workspaces, Layers, and Stores

- `list_workspaces`
- `create_workspace`
- `get_workspace`
- `get_default_workspace`
- `set_default_workspace`
- `get_layer_info`
- `list_layers`
- `create_layer`
- `delete_resource`
- `query_features`
- `generate_map`
- `create_datastore`
- `create_featurestore`
- `create_gpkg_datastore`
- `create_shp_datastore`
- `create_coveragestore`
- `delete_coveragestore`
- `get_coveragestore`
- `get_coveragestores`
- `get_datastore`
- `get_datastores`
- `get_featurestore`
- `delete_featurestore`

## Layer Groups

- `create_layergroup`
- `get_layergroup`
- `get_layergroups`
- `add_layer_to_layergroup`
- `remove_layer_from_layergroup`
- `delete_layergroup`
- `update_layergroup`

## Feature Types

- `publish_featurestore`
- `publish_featurestore_sqlview`
- `edit_featuretype`
- `get_featuretypes`
- `get_feature_attribute`

## Styles

- `create_style`
- `upload_style`
- `get_style`
- `get_styles`
- `publish_style`
- `create_catagorized_featurestyle`
- `create_classified_featurestyle`
- `create_coveragestyle`
- `create_outline_featurestyle`

## Style XML Helpers

- `style_catagorize_xml`
- `style_classified_xml`
- `style_coverage_style_colormapentry`
- `style_coverage_style_xml`
- `style_outline_only_xml`

## Security

- `create_user`
- `delete_user`
- `get_all_users`
- `modify_user`
- `create_usergroup`
- `delete_usergroup`
- `get_all_usergroups`

## System

- `get_manifest`
- `get_status`
- `get_system_status`
- `get_version`
- `reload_geoserver`
- `reset_geoserver`
- `update_service`
- `publish_time_dimension_to_coveragestore`
