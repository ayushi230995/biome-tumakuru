# BIOME Work at Tumakuru: map

Live site: https://ayushi230995.github.io/biome-tumakuru/

The site is rebuilt from BIOME's SharePoint workbook ("BIOME Work at Tumkur Locations")
by [`.github/workflows/refresh-from-sharepoint.yml`](.github/workflows/refresh-from-sharepoint.yml):

- every hour, on every push to `main`, and on demand (Actions tab > Refresh map from SharePoint > Run workflow);
- the workbook's share link is stored as the repo secret `SHAREPOINT_XLSX_URL`, never in the code;
- if the download or build fails (e.g. the link was revoked or a column was renamed), nothing is
  deployed and the last good version stays live. GitHub emails the repo owner about failed runs.

GitHub pauses scheduled workflows in public repos after 60 days without commits. If the map stops
refreshing, re-enable the workflow from the Actions tab.

## Build locally

Needs Python 3 with `openpyxl` (and `geopandas` only to rebuild the boundary). Run from this folder:

```
curl -sL -c cookies.txt -b cookies.txt -o workbook.xlsx "<share link>&download=1"
python create_geojson_from_excel.py workbook.xlsx   # -> biome_work_tumkur.geojson
python build_index_html.py                          # template.html + both GeoJSON files -> index.html
```

`index.html` is self-contained, so it also works when opened straight from disk.
The city boundary rarely changes; to rebuild it from the KGIS shapefile in the parent folder,
run `python shp_to_geojson.py` and commit `tumakuru_boundary.geojson`.

Make layout or style changes in `template.html`; `index.html` is overwritten on every build.

## Workbook format

- Sheet "BIOME Work Details" holds two tables (schools/hostels, then open wells), each with its own
  header row. The script looks columns up by name; a trailing unit such as "(Feet)" is ignored and
  extra columns are fine. Renaming or removing a column the script uses will fail the refresh.
- Each school's locality comes from the "Summary" sheet, matched on Sl.No.
- "View site photos" opens the hyperlink behind the `Link - Pictures` / `Link` cell (BIOME's shared
  SharePoint folders). SharePoint doesn't allow those folders to be embedded in other sites.
- Students and staff are counted once where two buildings of one school share a location.
