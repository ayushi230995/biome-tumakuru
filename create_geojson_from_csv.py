"""Build biome_work_tumkur.geojson from the BIOME work CSV.

The CSV holds two tables one after the other, each with its own header row
starting with "Date,Sl.No":
  1. Schools / hostels  -> rooftop rainwater harvesting (RWH)
  2. Open wells         -> open well rejuvenation
"""
import json
import re
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
CSV_PATH = HERE.parent / 'BIOME Work at Tumkur Locations(BIOME Work Details).csv'
OUT_PATH = HERE / 'biome_work_tumkur.geojson'

RWH = 'Rooftop rainwater harvesting'
WELL = 'Open well rejuvenation'


def number(value):
    """'400 SQM' -> 400, '11000 Ltr' -> 11000, 'No' / 'Nil' / '' / '0' -> None."""
    nums = re.findall(r'\d+(?:\.\d+)?', str(value).replace(',', ''))
    if len(nums) != 1 or float(nums[0]) == 0:
        return None
    n = float(nums[0])
    return int(n) if n.is_integer() else n


def litres_range(value):
    """'2800 Ltr' -> 2800, '20000 to 25000 Ltr' -> [20000, 25000]."""
    nums = [int(n) for n in re.findall(r'\d+', str(value).replace(',', ''))]
    return nums[0] if len(nums) == 1 else nums or None


def year(value):
    """'2023 - 2024' / '2023-2024' -> '2023-24'."""
    start, end = re.findall(r'\d{4}', value)
    return f'{start}-{end[2:]}'


def interventions(value):
    """'Roof top RWH, Recharge well, Storage stump' -> ['Roof top RWH', 'Recharge well', 'Storage sump']."""
    value = re.sub(r'^Open well rejuvenation\s*-\s*', '', value.strip())
    value = re.sub(r'\bstump\b', 'sump', value)  # typo in source sheet
    return [part.strip()[:1].upper() + part.strip()[1:] for part in value.split(',') if part.strip()]


def link(value):
    return value.strip() if str(value).strip().startswith('http') else None


def split_tables(raw):
    """Yield one list of row dicts per table in the CSV."""
    header, rows = None, []
    for values in raw.itertuples(index=False):
        values = [v.strip() for v in values]
        if values[0] == 'Date':
            if rows:
                yield rows
            header, rows = values, []
        elif header and any(values):
            rows.append(dict(zip(header, values)))
    if rows:
        yield rows


def rwh_properties(row):
    name = row['School Name']
    return {
        'category': RWH,
        'institution': 'Hostel' if 'hostel' in name.lower() else 'School',
        'name': name,
        'year': year(row['Date']),
        'funder': row['Funded By'],
        'interventions': interventions(row['What we did']),
        'roof_area_m2': number(row['Building Roof Area covered']),
        'sump_l': number(row['RWH Sump Size']),
        'rain_barrel_l': number(row['Rain Barrel Ltr']),
        'students': number(row['Students']),
        'teaching_staff': number(row['Teaching Staff']),
        'daily_water_demand_l': litres_range(row['Daily Water Demand']),
        'potential_harvest_l': number(row['Potential Rainwater harvested']),
        'maps_url': link(row['Locations']),
        'photos_url': link(row['Link - Pictures']),
    }


def well_properties(row):
    return {
        'category': WELL,
        'institution': 'Open well',
        'name': row['Well Name'],
        'year': year(row['Date']),
        'funder': row['Funded By'],
        'interventions': interventions(row['What we did']),
        # Source columns carry no units; feet fits the recorded volumes
        # (e.g. 9 x 45 -> pi * (9 ft / 2)^2 * 45 ft = 81,000 L).
        'well_diameter_ft': number(row['Well dimentions']),
        'well_depth_ft': number(row['Well Depth']),
        'well_volume_l': number(row['Well Volume (Litres)']),
        'households': number(row['Households using the well']),
        'maps_url': link(row['Locations']),
        'photos_url': link(row['Link']),
    }


raw = pd.read_csv(CSV_PATH, header=None, dtype=str, keep_default_na=False, encoding='utf-8-sig')
rwh_rows, well_rows = split_tables(raw)

features = []
for prefix, rows, to_properties in [('rwh', rwh_rows, rwh_properties), ('well', well_rows, well_properties)]:
    for row in rows:
        lat, lon = float(row['Latitude']), float(row['Longitude'])
        features.append({
            'type': 'Feature',
            'geometry': {'type': 'Point', 'coordinates': [lon, lat]},
            'properties': {'id': f"{prefix}-{int(row['Sl.No']):02d}", **to_properties(row)},
        })

with open(OUT_PATH, 'w', encoding='utf-8') as f:
    json.dump({'type': 'FeatureCollection', 'features': features}, f, ensure_ascii=False, indent=1)

print(f'Wrote {len(features)} sites ({len(rwh_rows)} RWH, {len(well_rows)} wells) -> {OUT_PATH.name}')
