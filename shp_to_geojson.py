"""Convert the KGIS Tumakuru City Corporation shapefile to a web-ready GeoJSON.

The shapefile is in UTM zone 43N (EPSG:32643, metres). Leaflet needs WGS84
longitude/latitude (EPSG:4326), so it is reprojected before export.
"""
from pathlib import Path

import geopandas as gpd

HERE = Path(__file__).resolve().parent
SHP_PATH = HERE.parent / '1810_Tumakuru' / '1810_TUMAKURU.shp'
OUT_PATH = HERE / 'tumakuru_boundary.geojson'

shp = gpd.read_file(SHP_PATH)
print(f'Source CRS: {shp.crs}')

shp = shp.to_crs(epsg=4326)

# RFC7946 = plain lon/lat GeoJSON with no "crs" member, so no tool can
# mistake the coordinates for UTM. 6 decimals is ~0.1 m precision.
shp.to_file(OUT_PATH, driver='GeoJSON', RFC7946='YES', COORDINATE_PRECISION=6)

print(f'Wrote {len(shp)} boundary feature(s), bounds {shp.total_bounds.round(5)} -> {OUT_PATH.name}')
