# BIOME Work at Tumakuru: map

`index.html` is self-contained (both GeoJSON layers are embedded), so it works when opened
straight from disk and needs no other files when published, e.g. on GitHub Pages.

## Rebuild after the Excel or shapefile changes

The source Excel and the KGIS shapefile are kept in the parent folder, outside this repo.
Needs Python 3 with `openpyxl` and `geopandas` (`pip install openpyxl geopandas`). Run from this folder:

```
python create_geojson_from_excel.py   # ../BIOME Work at Tumkur Locations.xlsx -> biome_work_tumkur.geojson
python shp_to_geojson.py              # ../1810_Tumakuru/1810_TUMAKURU.shp     -> tumakuru_boundary.geojson
python build_index_html.py            # template.html + both GeoJSON files     -> index.html
```

Make layout or style changes in `template.html`; `index.html` is overwritten on every build.

## Data notes

- Sheet "BIOME Work Details" holds two tables (schools/hostels, then open wells), each with its
  own header row. The script expects that layout and those column names. Extra columns are ignored.
- Each school's locality comes from the "Summary" sheet, matched on Sl.No.
- "View site photos" opens the hyperlink behind the `Link - Pictures` / `Link` cell (BIOME's shared
  SharePoint folders). SharePoint doesn't allow those folders to be embedded in other sites.
- Well diameter and depth have no units in the sheet. The page shows them as feet, which
  matches the recorded volumes (9 ft x 45 ft -> 81,000 L).
- Students and staff are counted once where two buildings of one school share a location.
