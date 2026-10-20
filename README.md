# BIOME Work at Tumakuru: map

`index.html` is self-contained (both GeoJSON layers are embedded), so it works when opened
straight from disk and needs no other files when published, e.g. on GitHub Pages.

## Rebuild after the CSV or shapefile changes

The source CSV and the KGIS shapefile are kept in the parent folder, outside this repo.
Needs Python 3 with `pandas` and `geopandas` (`pip install pandas geopandas`). Run from this folder:

```
python create_geojson_from_csv.py   # ../BIOME Work at Tumkur Locations(...).csv -> biome_work_tumkur.geojson
python shp_to_geojson.py            # ../1810_Tumakuru/1810_TUMAKURU.shp      -> tumakuru_boundary.geojson
python build_index_html.py          # template.html + both GeoJSON files      -> index.html
```

Make layout or style changes in `template.html`; `index.html` is overwritten on every build.

## Data notes

- The CSV holds two tables (schools/hostels, then open wells), each with its own header row.
  The script expects that layout and those column names.
- Well diameter and depth have no units in the sheet. The page shows them as feet, which
  matches the recorded volumes (9 ft x 45 ft -> 81,000 L).
- Students and staff are counted once where two buildings of one school share a location.
- A `Link - Pictures` / `Link` cell that holds a URL shows as a "Photos" link in the popup.
