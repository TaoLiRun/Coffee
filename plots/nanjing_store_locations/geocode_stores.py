import json
import time
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import pandas as pd
import requests


PROJECT_ROOT = Path(__file__).resolve().parents[3]
# The raw data for Nanjing store addresses lives directly under the top-level
# `data1031` directory in this project (see workspace structure).
DATA_CSV = PROJECT_ROOT / "data1031" / "dapt_id_address.csv"

# Save all outputs (CSV, cache, map) in the same directory as this script.
OUTPUT_DIR = Path(__file__).resolve().parent
# Use a Baidu-specific cache file so we do not mix with any previous Nominatim cache.
GEOCODE_CACHE_PATH = OUTPUT_DIR / "geocode_cache_baidu.json"
GEOCODED_CSV_PATH = OUTPUT_DIR / "nanjing_stores_geocoded.csv"


BAIDU_AK = "nBfqPNjaoGXK4pkUmeJXful3x8zG8kVT"
BAIDU_GEOCODER_URL = "https://api.map.baidu.com/geocoding/v3/"


def load_address_data() -> pd.DataFrame:
    """Load the source CSV with dept_id and address columns."""
    # Try UTF-8 first, fall back to GBK (common for Chinese CSVs)
    encodings = ["utf-8", "gbk"]
    last_error: Optional[Exception] = None
    for enc in encodings:
        try:
            df = pd.read_csv(DATA_CSV, encoding=enc)
            break
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            df = None  # type: ignore[assignment]
    if df is None:
        raise RuntimeError(f"Failed to read CSV {DATA_CSV} with encodings {encodings}") from last_error

    # Basic sanity checks
    expected_cols = {"dept_id", "address"}
    missing = expected_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing expected columns {missing} in {DATA_CSV}. Got: {list(df.columns)}")

    # Ensure types
    df["dept_id"] = df["dept_id"].astype(str)
    df["address"] = df["address"].astype(str).str.strip()

    # Drop rows with empty address
    df = df[df["address"].str.len() > 0].copy()
    return df


def normalize_address(raw_address: str) -> str:
    """Normalise address string for Baidu geocoding by ensuring the city prefix."""
    addr = raw_address.strip()
    if not addr:
        return addr
    # If city name is already present, keep as is; otherwise prefix with 南京市.
    if "南京" not in addr:
        addr = f"南京市{addr}"
    return addr


def load_cache() -> Dict[str, Any]:
    if GEOCODE_CACHE_PATH.exists():
        try:
            with GEOCODE_CACHE_PATH.open("r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}


def save_cache(cache: Dict[str, Any]) -> None:
    # Ensure the output directory exists before writing the cache file.
    GEOCODE_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with GEOCODE_CACHE_PATH.open("w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def geocode_address(
    address: str,
    session: Optional[requests.Session] = None,
    delay_seconds: float = 0.2,
) -> Tuple[Optional[float], Optional[float], Dict[str, Any]]:
    """Call Baidu Map geocoding API to geocode a single address.

    Returns BD-09 coordinates (Baidu's coordinate system), which are close to
    standard lat/lon and suitable for visualisation on the map.
    """
    sess = session or requests.Session()
    params = {
        "address": address,
        "city": "南京市",
        "output": "json",
        "ak": BAIDU_AK,
    }
    # Be polite with a small delay between requests.
    time.sleep(delay_seconds)
    resp = sess.get(BAIDU_GEOCODER_URL, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    # Baidu returns status 0 on success.
    if data.get("status") != 0:
        return None, None, {
            "status": "error",
            "baidu_status": data.get("status"),
            "message": data.get("msg") or data.get("message"),
        }

    result = data.get("result") or {}
    loc = result.get("location") or {}
    try:
        lat = float(loc.get("lat"))
        lon = float(loc.get("lng"))
    except (TypeError, ValueError):
        return None, None, {"status": "invalid_coords", "raw": data}

    meta: Dict[str, Any] = {
        "status": "ok",
        "level": result.get("level"),
        "precise": result.get("precise"),
        "confidence": result.get("confidence"),
    }
    return lat, lon, meta


def is_within_nanjing_bounds(lat: Optional[float], lon: Optional[float]) -> bool:
    """Simple bounding-box check around Nanjing city."""
    if lat is None or lon is None:
        return False
    return 31.5 <= lat <= 32.5 and 118.0 <= lon <= 119.5


def build_geocoded_table(limit_rows: Optional[int] = None, output_path: Optional[Path] = None) -> pd.DataFrame:
    df = load_address_data()

    # Optionally restrict to the first N rows for quick testing.
    if limit_rows is not None:
        df = df.iloc[:limit_rows].copy()

    # Prepare unique addresses with normalisation
    df["normalized_address"] = df["address"].apply(normalize_address)
    unique_addresses = df["normalized_address"].drop_duplicates().tolist()

    cache = load_cache()
    session = requests.Session()

    results: Dict[str, Dict[str, Any]] = {}
    for addr in unique_addresses:
        if addr in cache:
            info = cache[addr]
        else:
            try:
                lat, lon, meta = geocode_address(addr, session=session)
            except Exception as exc:  # noqa: BLE001
                lat, lon, meta = None, None, {"status": "error", "error": str(exc)}
            info = {
                "latitude": lat,
                "longitude": lon,
                "meta": meta,
            }
            cache[addr] = info
            save_cache(cache)
        results[addr] = info

    # Map back to original rows
    df["latitude"] = df["normalized_address"].map(lambda a: results.get(a, {}).get("latitude"))
    df["longitude"] = df["normalized_address"].map(lambda a: results.get(a, {}).get("longitude"))
    df["geocode_status"] = df["normalized_address"].map(
        lambda a: results.get(a, {}).get("meta", {}).get("status", "unknown"),
    )
    df["within_nanjing_bounds"] = df.apply(
        lambda row: is_within_nanjing_bounds(row["latitude"], row["longitude"]),
        axis=1,
    )

    # Reorder columns: keep original plus new ones
    # Preserve all original columns
    orig_cols = [c for c in df.columns if c not in {"normalized_address", "latitude", "longitude", "geocode_status", "within_nanjing_bounds"}]
    ordered_cols = orig_cols + [
        "latitude",
        "longitude",
        "geocode_status",
        "within_nanjing_bounds",
        "normalized_address",
    ]
    df_out = df[ordered_cols].copy()

    # Decide where to save the geocoded results.
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if output_path is None:
        if limit_rows is None:
            # Full dataset: use the default path.
            csv_path = GEOCODED_CSV_PATH
        else:
            # Limited run: save to a separate sample file so we don't overwrite the full results.
            csv_path = OUTPUT_DIR / f"nanjing_stores_geocoded_first_{limit_rows}.csv"
    else:
        csv_path = output_path

    df_out.to_csv(csv_path, index=False, encoding="utf-8-sig")
    return df_out


def build_map(df: Optional[pd.DataFrame] = None) -> Path:
    import folium

    if df is None:
        if not GEOCODED_CSV_PATH.exists():
            df = build_geocoded_table()
        else:
            df = pd.read_csv(GEOCODED_CSV_PATH)

    # Filter successful points within Nanjing bounds
    mask_ok = (df["geocode_status"] == "ok") & (df["within_nanjing_bounds"])
    df_map = df[mask_ok].copy()

    # Fallback center: Nanjing city center
    center_lat, center_lon = 32.0603, 118.7969
    if not df_map.empty:
        center_lat = df_map["latitude"].mean()
        center_lon = df_map["longitude"].mean()

    m = folium.Map(location=[center_lat, center_lon], zoom_start=12, tiles="OpenStreetMap")

    # Identify the original count columns (3rd and 4th columns of original CSV)
    # They should still be present; we avoid hardcoding names in case of encoding issues.
    orig_df = load_address_data()
    orig_cols = list(orig_df.columns)
    count_cols = orig_cols[2:4] if len(orig_cols) >= 4 else []

    for _, row in df_map.iterrows():
        popup_lines = [f"dept_id: {row.get('dept_id', '')}", f"address: {row.get('address', '')}"]
        for col in count_cols:
            if col in row:
                popup_lines.append(f"{col}: {row[col]}")
        popup_text = "<br>".join(popup_lines)

        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=4,
            color="blue",
            fill=True,
            fill_opacity=0.7,
            popup=folium.Popup(popup_text, max_width=300),
        ).add_to(m)

    map_path = OUTPUT_DIR / "nanjing_store_map.html"
    m.save(str(map_path))
    return map_path


def main() -> None:
    df = build_geocoded_table()
    build_map(df)


if __name__ == "__main__":
    main()


