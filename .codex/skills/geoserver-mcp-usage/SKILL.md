---
name: geoserver-mcp-usage
description: "Use GeoServer MCP tools to manage workspaces, stores, layers, styles, users, and system operations. Use when the user asks to manage GeoServer, create/publish layers, configure styles, manage users, query features, generate maps, or any GeoServer administration task via MCP tools. Also use when the user needs help installing or configuring GeoServer MCP itself."
---

# GeoServer MCP Usage

## Overview

This skill provides domain knowledge and workflow patterns for using GeoServer MCP tools. When the user connects to a GeoServer MCP server, the available MCP tools expose raw GeoServer REST API operations. This skill teaches how to compose them into correct, safe sequences for common administration tasks.

If the GeoServer MCP tools are not available in the current session, guide the user to install and configure them first.

## Prerequisites Check

Before executing any GeoServer task, verify whether the GeoServer MCP tools are available in the current session:

1. Check if any tool starting with `list_workspaces`, `create_workspace`, `get_version`, `get_styles`, `create_style`, etc. is available.
2. If none of these tools are available, the GeoServer MCP server is not connected. **Do not attempt to use GeoServer REST API directly** -- guide the user to set up the MCP server instead.

### Setting Up GeoServer MCP (when tools are missing)

When the GeoServer MCP tools are not available, first ask the user: **"Do you already have a GeoServer MCP server running?"**

**If the user provides a Streamable HTTP or SSE URL:**

The user already has a running server. Just add their MCP server to the agent's `mcpServers` configuration. Do NOT install anything.

Streamable HTTP:
```json
{
  "mcpServers": {
    "geoserver": {
      "url": "<USER_PROVIDED_URL>"
    }
  }
}
```

SSE:
```json
{
  "mcpServers": {
    "geoserver": {
      "url": "<USER_PROVIDED_SSE_URL>"
    }
  }
}
```

**If the user does NOT have a running MCP server:**

Ask for the GeoServer connection details:

- GeoServer URL (e.g., `http://localhost:8080/geoserver`)
- Username
- Password

Then ask: **"Do you want me to install geoserver-mcp locally?"**

If the user confirms, install and configure:

1. Install via uvx:
   ```bash
   uvx --from open-geoserver-mcp geoserver-mcp --url <PROVIDED_URL> --user <PROVIDED_USER> --password <PROVIDED_PASSWORD> --transport streamable-http --host 127.0.0.1 --port 8000
   ```

2. Add the agent's `mcpServers` configuration:
   ```json
   {
     "mcpServers": {
       "geoserver": {
         "url": "http://127.0.0.1:8000/mcp"
       }
     }
   }
   ```

If the user declines local installation, provide the installation options for reference:

- uvx: `uvx --from open-geoserver-mcp geoserver-mcp --url ... --user ... --password ...`
- pip: `pip install open-geoserver-mcp` then `geoserver-mcp --url ... --user ... --password ...`
- Docker: `docker run -e GEOSERVER_URL=... -e GEOSERVER_USER=... -e GEOSERVER_PASSWORD=... open-geoserver-mcp`

Once their server is running, ask for the connection details and configure the agent's `mcpServers` as above.

ps, or any GeoServer administration task via MCP tools. Also use when the user needs help installing or configuring GeoServer MCP itself."
---

# GeoServer MCP Usage

## Overview

This skill provides domain knowledge and workflow patterns for using GeoServer MCP tools. When the user connects to a GeoServer MCP server, the available MCP tools expose raw GeoServer REST API operations. This skill teaches how to compose them into correct, safe sequences for common administration tasks.

If the GeoServer MCP tools are not available in the current session, guide the user to install and configure them first.

## Prerequisites Check

Before executing any GeoServer task, verify whether the GeoServer MCP tools are available in the current session:

1. Check if any tool starting with `list_workspaces`, `create_workspace`, `get_version`, `get_styles`, `create_style`, etc. is available.
2. If none of these tools are available, the GeoServer MCP server is not connected. **Do not attempt to use GeoServer REST API directly** -- guide the user to set up the MCP server instead.

## Domain Model

GeoServer resources form a strict hierarchy. Read `references/domain-model.md` for the full entity model, naming constraints, and lifecycle rules. Key relationships:

- **Workspace** -- contains stores, layers, styles. Create first.
- **Store** (DataStore/FeatureStore/CoverageStore) -- connects to data. Create inside a workspace.
- **Layer** -- published from a store. Often auto-published.
- **Style** -- SLD XML. Global or workspace-scoped. Bind to layer with `publish_style`.
- **LayerGroup** -- ordered stack of layers rendered together.

## Tool Categories

### Catalog Tools (workspaces, stores, layers, layer groups)

| Task | Primary Tool | Notes |
|------|-------------|-------|
| List workspaces | `list_workspaces` | Always start here to discover existing state |
| Create workspace | `create_workspace` | Name must be unique; returns info if already exists |
| Set default workspace | `set_default_workspace` | Convenience for subsequent operations |
| Create Shapefile store | `create_shp_datastore` | `file_path` resolves from `--storage` root |
| Create GeoPackage store | `create_gpkg_datastore` | Same `file_path` resolution |
| Create generic DataStore | `create_datastore` | Pass `params` with `path` and store type keys |
| Create FeatureStore | `create_featurestore` | Database connection; pass `params` with host/db/user/password |
| Create CoverageStore | `create_coveragestore` | Raster data; `params` must include `path` or `url` |
| List layers | `list_layers` | Filter by `workspace` (optional) |
| Publish layer | `create_layer` | Requires workspace, layer name, store name, source name |
| Publish FeatureStore | `publish_featurestore` | Publish a database table/view as layer |
| Publish SQL view | `publish_featurestore_sqlview` | Custom SQL query as layer |
| Get feature types | `get_featuretypes` | List tables/views in a store |
| Get feature attributes | `get_feature_attribute` | Column names and types |
| Edit feature type | `edit_featuretype` | Update metadata; `kwargs` as key=value pairs |
| Query features | `query_features` | WFS query with optional CQL filter |
| Generate map | `generate_map` | WMS map with bbox, layers, styles, format |
| Create layer group | `create_layergroup` | Stack multiple layers with metadata |
| Manage layer groups | `add_layer_to_layergroup`, `remove_layer_from_layergroup`, `update_layergroup`, `delete_layergroup` | |
| Delete any resource | `delete_resource` | Unified: workspace/layer/datastore/style/coverage/featurestore |

### Style Tools

| Task | Primary Tool | Notes |
|------|-------------|-------|
| Create from SLD | `create_style` | Pass SLD XML string directly |
| Upload from file | `upload_style` | `path` resolves from `--storage` root |
| List styles | `get_styles` | Optional `workspace` filter |
| Get style detail | `get_style` | Returns the SLD body |
| Bind style to layer | `publish_style` | Layer must already exist |
| Categorized vector style | `create_catagorized_featurestyle` | Color by distinct column values |
| Classified vector style | `create_classified_featurestyle` | Ranges by column values |
| Outline-only style | `create_outline_featurestyle` | Border only, no fill |
| Raster coverage style | `create_coveragestyle` | Requires `raster_path` in params |
| Generate SLD XML | `style_catagorize_xml`, `style_classified_xml`, `style_coverage_style_xml`, `style_outline_only_xml` | Preview XML before creating |
| Generate colormap | `style_coverage_style_colormapentry` | Color ramp entries for raster |

### Security Tools

| Task | Tool | Notes |
|------|------|-------|
| List users | `get_all_users` | Optional `service` filter |
| Create user | `create_user` | Requires username, password; enabled defaults to True |
| Modify user | `modify_user` | Rename, change password, enable/disable |
| Delete user | `delete_user` | |
| List groups | `get_all_usergroups` | |
| Create group | `create_usergroup` | |
| Delete group | `delete_usergroup` | |

### System Tools

| Task | Tool | Notes |
|------|------|-------|
| Version | `get_version` | GeoServer version info |
| Status | `get_status`, `get_system_status` | Runtime health |
| Manifest | `get_manifest` | Component list and versions |
| Reload config | `reload_geoserver` | Apply config changes without restart |
| Reset | `reset_geoserver` | Clear caches and connection pools |
| Update OGC service | `update_service` | Configure WMS/WFS/WCS settings |
| Time dimension | `publish_time_dimension_to_coveragestore` | Enable time on raster stores |

## Common Workflows

### Publish a Shapefile as a Styled Layer

```
1. list_workspaces() -- discover or plan workspace name
2. create_workspace("myworkspace") -- idempotent, safe to call
3. create_shp_datastore("myworkspace", "mystore", "data/roads.shp") -- store the shapefile
4. get_featuretypes("myworkspace", "mystore") -- find the auto-published layer name
5. get_feature_attribute("myworkspace", "mystore", "roads") -- inspect columns for styling
6. create_outline_featurestyle("roads_style", "#FF0000", "myworkspace", width="2") -- or use other style helpers
7. publish_style("roads", "roads_style", "myworkspace") -- bind style to layer
```

### Publish a PostGIS Table

```
1. create_workspace("myworkspace")
2. create_featurestore("myworkspace", "pgstore", {
     "host": "localhost", "port": "5432", "database": "gis",
     "user": "postgres", "password": "***", "dbtype": "postgis"
   })
3. publish_featurestore("myworkspace", "pgstore", {
     "nativeName": "cities", "title": "Cities"
   })
4. get_feature_attribute("myworkspace", "pgstore", "cities")
5. create_classified_featurestyle("cities_style", "population", "0,100000,500000,1000000", "myworkspace", color_ramp="YlOrRd")
6. publish_style("cities", "cities_style", "myworkspace")
```

### Publish a GeoTIFF as a Raster Layer

```
1. create_workspace("raster")
2. create_coveragestore("raster", "dem", {"path": "data/elevation.tif", "type": "GeoTIFF"})
3. create_coveragestyle("dem_style", {
     "raster_path": "data/elevation.tif",
     "style_name": "dem_style",
     "color_ramp": "terrain",
     "number_of_classes": 10,
     "min_value": 0, "max_value": 3000,
     "cmap_type": "ramp", "opacity": 1.0
   })
   -- or use style_coverage_style_xml() + style_coverage_style_colormapentry() + create_style() for more control
4. publish_style("dem", "dem_style", "raster")
```

### Query and Map Generation

```
1. query_features("myworkspace", "cities", filter="population > 1000000", max_features=50)
2. generate_map(["myworkspace:cities"], styles=["cities_style"], bbox=[-180,-90,180,90], format="image/png")
```

### User Management

```
1. get_all_users() -- check existing users
2. create_user("viewer", "securepass", enabled=True)
3. create_usergroup("viewers")
4. modify_user("viewer", new_password="newpass") -- rotate credentials
5. delete_user("viewer") -- remove when done
```

### System Maintenance

```
1. get_version() -- check GeoServer version
2. get_system_status() -- check health
3. reload_geoserver() -- apply config changes
4. reset_geoserver() -- clear caches if layers not appearing
```

## Safety Rules

### Destructive Operations Require Confirmation

**Before executing any delete or update operation, you MUST ask the user for explicit confirmation.** This applies to all tools that modify or destroy existing resources:

- `delete_resource` -- any resource type
- `delete_user`, `delete_usergroup`, `delete_layergroup`, `delete_coveragestore`, `delete_featurestore`
- `modify_user`, `update_service`, `update_layergroup`, `edit_featuretype`

When confirmation is required:

1. Show the user exactly what will be modified or deleted (resource type, name, workspace).
2. Explain the consequences briefly (e.g., deleting a workspace will fail if child resources still exist).
3. Wait for explicit approval before proceeding.

**Exception**: `create_*` tools and `publish_*` tools are idempotent or additive and do not require confirmation. `reload_geoserver` and `reset_geoserver` do not require confirmation unless the user asks for a safety check.

## Best Practices

- **Always check existing state first**: call `list_workspaces`, `get_datastores`, `get_layers` before creating.
- **Idempotent creation**: `create_workspace` returns an info message if the workspace already exists; it is safe to call speculatively.
- **Workspace scoping**: pass `workspace` parameter whenever available to avoid ambiguity. Use `set_default_workspace` for convenience.
- **Style creation order**: styles can be created independently of layers, but must be bound with `publish_style` after the layer exists.
- **Store creation auto-publishes**: many store types auto-publish layers. Use `get_featuretypes` or `get_layers` to discover them rather than calling `create_layer` unnecessarily.
- **File paths**: all file path parameters (`file_path`, `path`, `raster_path`) resolve relative to the `--storage` directory configured at server startup. The server enforces this sandbox; you cannot reference arbitrary filesystem paths.
- **Error handling**: when a tool returns an error, read the message carefully. Common issues: workspace not found, store name conflict, layer already exists, style not found.
- **After store/config changes**: call `reload_geoserver` or `reset_geoserver` if new layers or styles are not immediately visible.
- **Style helpers vs raw SLD**: use the style helper tools (`create_catagorized_featurestyle`, etc.) for common cases; fall back to `create_style` with raw SLD XML only when custom styling is needed.
- **Delete with care**: `delete_resource` is destructive. Verify the resource name and type before deleting. For workspaces, all child resources must be deleted first.