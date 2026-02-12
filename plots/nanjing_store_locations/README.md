Nanjing Store Geocoding & Mapping
=================================

This folder contains scripts and outputs for geocoding store locations in Nanjing
and visualizing them on an interactive map.

Source data
-----------

- Input CSV: `data/data1031/dapt_id_address.csv` (relative to the project root
  `/home/litao/Coffee`).
- Important columns:
  - `dept_id`: Store identifier.
  - `address`: Store address in Chinese within Nanjing.
  - Two numeric columns describing counts within 500m and 1500m (kept and
    visualised in the outputs).

Workflow
--------

1. Load the CSV and normalise addresses.
2. Geocode each unique address using the OpenStreetMap Nominatim service
   (WGS84 coordinates).
3. Cache geocoding responses locally to avoid repeated API calls.
4. Save a geocoded CSV with latitude/longitude and status/quality flags.
5. Build an interactive Folium map of all successfully geocoded stores.

Outputs
-------

- `nanjing_stores_geocoded.csv` – enriched table with latitude/longitude and
  basic quality flags.
- `nanjing_store_map.html` – interactive map of stores in Nanjing.

Dependencies
------------

The scripts assume the following Python packages are available:

- `pandas`
- `requests`
- `folium`

You can install them, for example, with:

```bash
pip install pandas requests folium
```


