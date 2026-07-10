## GeoServer Domain Model

### Entity Hierarchy

```
Workspace
├── Namespace (URI prefix for layer names)
├── DataStore | FeatureStore | CoverageStore
│   └── FeatureType | Coverage (auto-published layers)
├── Layer (published from a store resource)
├── LayerGroup (ordered collection of layers)
└── Style (SLD XML, can be global or workspace-scoped)
```

### Key Concepts

**Workspace** -- A logical container grouping related stores, layers, and styles. Every resource belongs to a workspace. Workspace names must be unique across the GeoServer instance. Use `list_workspaces` to discover existing ones, then `create_workspace` to add new ones.

**Store** -- A connection to a data source. Three types:
- **DataStore** (`create_datastore`, `create_shp_datastore`, `create_gpkg_datastore`): Vector data from files (Shapefile, GeoPackage) or directories.
- **FeatureStore** (`create_featurestore`): Vector data from databases (PostGIS, Oracle, SQL Server, etc.). Requires connection parameters: host, port, database, user, password, dbtype.
- **CoverageStore** (`create_coveragestore`): Raster data (GeoTIFF, ImageMosaic, WorldImage, etc.). Requires a `path` to the raster file or directory.

**Layer** -- A published resource from a store, accessible via WMS/WFS. A store may auto-publish layers when created; check with `get_layers` or `get_featuretypes`. Explicitly publish via `create_layer` or `publish_featurestore`.

**LayerGroup** -- An ordered stack of layers rendered together as a single map. Created via `create_layergroup`. Layers can be added/removed with `add_layer_to_layergroup` and `remove_layer_from_layergroup`. Supports modes: `single` (one tile request), `opaque` (no transparency), `named tree`, `container tree`, `eo`.

**Style** -- SLD (Styled Layer Descriptor) XML defining visual rendering. Global styles are available to all workspaces; workspace-scoped styles only apply within that workspace. Created via `create_style` (inline SLD), `upload_style` (file), or helper functions. Bind to a layer with `publish_style`.

**FeatureType** -- The schema/metadata of a vector layer (attribute names, types, projections, bounding box). Manage via `get_featuretypes`, `get_feature_attribute`, `edit_featuretype`.

### Naming Constraints

- Workspace names: unique across the instance, no spaces, lowercase preferred.
- Store names: unique within a workspace.
- Style names: unique within a workspace (or globally if no workspace specified).
- Layer names: derived from the source (e.g., table name, file name). The auto-published name matches the source name.
- LayerGroup names: unique within a workspace.

### Resource Lifecycle

Resources are created in dependency order:

1. **Workspace** -- container for everything below.
2. **Store** -- depends on workspace. Connects to data.
3. **Layer** -- depends on store. Often auto-published when store is created.
4. **Style** -- independent of the above, but bound to a layer later.
5. **publish_style** -- binds an existing style to an existing layer.

Deletion is reverse: remove style bindings, delete layers, then stores, then workspace. Use `delete_resource` for a unified deletion interface supporting types: workspace, layer, datastore, style, coverage, featurestore.

### File Path Resolution

All file path parameters (`file_path`, `path`, `raster_path`) resolve relative to the `--storage` directory configured at server startup. The server enforces this sandbox: paths outside the storage root are rejected. Typical layout:

```
--storage /data/
├── shapefiles/
│   └── roads.shp (and .dbf, .shx, .prj)
├── geopackages/
│   └── buildings.gpkg
├── rasters/
│   └── elevation.tif
└── styles/
    └── custom.sld
```

Tool parameters use the relative path: `"data/shapefiles/roads.shp"` resolves to `{storage}/data/shapefiles/roads.shp`.