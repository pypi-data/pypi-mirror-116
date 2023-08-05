from typing import Any

from django.contrib.admin import ModelAdmin as ModelAdmin

spherical_mercator_srid: int

class GeoModelAdmin(ModelAdmin[Any]):
    default_lon: int = ...
    default_lat: int = ...
    default_zoom: int = ...
    display_wkt: bool = ...
    display_srid: bool = ...
    extra_js: Any = ...
    num_zoom: int = ...
    max_zoom: bool = ...
    min_zoom: bool = ...
    units: bool = ...
    max_resolution: bool = ...
    max_extent: bool = ...
    modifiable: bool = ...
    mouse_position: bool = ...
    scale_text: bool = ...
    layerswitcher: bool = ...
    scrollable: bool = ...
    map_width: int = ...
    map_height: int = ...
    map_srid: int = ...
    map_template: str = ...
    openlayers_url: str = ...
    point_zoom: Any = ...
    wms_url: str = ...
    wms_layer: str = ...
    wms_name: str = ...
    wms_options: Any = ...
    debug: bool = ...
    widget: Any = ...
    @property
    def media(self) -> Any: ...
    def formfield_for_dbfield(
        self, db_field: Any, request: Any, **kwargs: Any
    ) -> Any: ...
    def get_map_widget(self, db_field: Any) -> Any: ...

class OSMGeoAdmin(GeoModelAdmin):
    map_template: str = ...
    num_zoom: int = ...
    map_srid: Any = ...
    point_zoom: Any = ...
