"""Build a self-contained index.html by inlining both GeoJSON files into template.html.

Inlining (instead of fetch()) means the page works when opened straight from
disk as well as on GitHub Pages: browsers block fetch() on file:// pages.
"""
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
IST = timezone(timedelta(hours=5, minutes=30))


def inline(filename):
    data = json.loads((HERE / filename).read_text(encoding='utf-8'))
    # "</" inside a <script> block would end the script early.
    return json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')


html = (HERE / 'template.html').read_text(encoding='utf-8')
html = (html
        .replace('__SITES_GEOJSON__', inline('biome_work_tumkur.geojson'))
        .replace('__BOUNDARY_GEOJSON__', inline('tumakuru_boundary.geojson'))
        .replace('__BUILD_TIME__', datetime.now(IST).strftime('%Y-%m-%d %H:%M IST')))
(HERE / 'index.html').write_text(html, encoding='utf-8')

print(f'Wrote index.html ({len(html) / 1024:.0f} KB)')
