"""
Visualize store closures on an interactive map using folium.

This script creates an interactive map showing store closures with dual encoding:
- Marker SIZE represents closure duration (larger = longer closure)
- Marker COLOR represents chronological order (red=early, green=late)
"""

import os
from pathlib import Path
from typing import Tuple, List

import folium
import numpy as np
import pandas as pd
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CLOSURES_CSV = PROJECT_ROOT / "plots" / "nanjing_store_locations" / "store_closures.csv"
OUTPUT_DIR = Path(__file__).resolve().parent
OUTPUT_HTML = OUTPUT_DIR / "store_closures_map.html"


# Nanjing city center (fallback)
NANJING_CENTER = (32.0603, 118.7969)


def load_closures_data() -> pd.DataFrame:
    """Load store closures data from CSV."""
    print(f"Loading closures data from: {CLOSURES_CSV}")
    df = pd.read_csv(CLOSURES_CSV, encoding="utf-8-sig")

    # Convert date columns back to datetime for processing
    df["closure_start"] = pd.to_datetime(df["closure_start"])
    df["closure_end"] = pd.to_datetime(df["closure_end"])

    # Filter to only rows with valid coordinates
    df = df[df["latitude"].notna() & df["longitude"].notna()].copy()

    print(f"  Total closures with valid coordinates: {len(df)}")
    print(f"  Date range: {df['closure_start'].min().date()} to {df['closure_end'].max().date()}")
    print(f"  Unique stores: {df['dept_id'].nunique()}")

    return df


def get_color_by_date(closure_start: pd.Timestamp, min_date: pd.Timestamp, max_date: pd.Timestamp) -> str:
    """
    Get color based on closure start date using RdYlGn colormap.

    Earlier closures = Red
    Later closures = Green
    """
    # Normalize date to 0-1 range
    if max_date > min_date:
        normalized = (closure_start - min_date) / (max_date - min_date)
    else:
        normalized = 0.5

    # Use matplotlib's RdYlGn colormap - red to green
    cmap = plt.get_cmap('RdYlGn')
    rgba = cmap(normalized)
    # Convert to hex color
    color = mcolors.to_hex(rgba)
    return color


def get_marker_size(duration_days: int, min_duration: int, max_duration: int) -> float:
    """
    Get marker radius based on closure duration.

    Formula: base_radius + scale_factor * normalized_duration
    """
    base_radius = 6
    max_added_radius = 20

    if max_duration > min_duration:
        normalized = (duration_days - min_duration) / (max_duration - min_duration)
    else:
        normalized = 0.5

    radius = base_radius + max_added_radius * normalized
    return radius


def create_closure_popup(row: pd.Series) -> str:
    """Create HTML popup content for a closure marker."""
    popup_html = f"""
    <div style="font-family: Arial, sans-serif; width: 250px;">
        <h4 style="margin: 0 0 8px 0; color: #333;">Store {row['dept_id']}</h4>
        <p style="margin: 4px 0;"><strong>Closure Start:</strong> {row['closure_start'].strftime('%Y-%m-%d')}</p>
        <p style="margin: 4px 0;"><strong>Closure End:</strong> {row['closure_end'].strftime('%Y-%m-%d')}</p>
        <p style="margin: 4px 0;"><strong>Duration:</strong> {row['closure_duration_days']} days</p>
        <p style="margin: 4px 0; font-size: 11px; color: #666;">{row.get('address', '')[:60]}...</p>
    </div>
    """
    return popup_html


def create_legend(
    min_date: pd.Timestamp,
    max_date: pd.Timestamp,
    min_duration: int,
    max_duration: int,
    total_closures: int,
) -> folium.Element:
    """Create a legend showing both color (time) and size (duration) scales."""

    legend_html = f"""
    <div style="
        position: fixed;
        bottom: 30px;
        left: 30px;
        width: 320px;
        background: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        z-index: 1000;
        font-family: Arial, sans-serif;
        font-size: 12px;
    ">
        <h4 style="margin: 0 0 10px 0; color: #333;">Store Closures Legend</h4>

        <div style="margin-bottom: 12px;">
            <strong style="color: #555;">Color (Time):</strong><br>
            <div style="display: flex; align-items: center; margin-top: 5px;">
                <span style="margin-right: 5px;">Early</span>
                <div style="flex: 1; height: 12px; background: linear-gradient(to right, #d73027, #f46d43, #fdae61, #fee08b, #d9ef8b, #a6d96a, #66bd63, #1a9850); border-radius: 2px;"></div>
                <span style="margin-left: 5px;">Late</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 3px; color: #666; font-size: 11px;">
                <span>{min_date.strftime('%Y-%m')}</span>
                <span>{max_date.strftime('%Y-%m')}</span>
            </div>
        </div>

        <div>
            <strong style="color: #555;">Size (Duration):</strong><br>
            <div style="margin-top: 8px;">
                <div style="display: flex; align-items: center; margin-bottom: 4px;">
                    <div style="width: 12px; height: 12px; background: #d73027; border-radius: 50%; margin-right: 8px;"></div>
                    <span>{min_duration} days</span>
                </div>
                <div style="display: flex; align-items: center; margin-bottom: 4px;">
                    <div style="width: 20px; height: 20px; background: #fdae61; border-radius: 50%; margin-right: 4px;"></div>
                    <span>~{(min_duration + max_duration) // 2} days</span>
                </div>
                <div style="display: flex; align-items: center;">
                    <div style="width: 26px; height: 26px; background: #1a9850; border-radius: 50%;"></div>
                    <span style="margin-left: 2px;">{max_duration} days</span>
                </div>
            </div>
        </div>

        <div style="margin-top: 10px; padding-top: 8px; border-top: 1px solid #eee; color: #666; font-size: 11px;">
            Total closures: {total_closures}
        </div>
    </div>
    """

    return folium.Element(legend_html)


def create_closure_map(df: pd.DataFrame) -> folium.Map:
    """
    Create an interactive map showing store closures.

    Markers use dual encoding:
    - Color: Chronological order (red=early, green=late)
    - Size: Closure duration (larger=longer)
    """
    print("\nCreating closure map...")

    # Get date and duration ranges for normalization
    min_date = df["closure_start"].min()
    max_date = df["closure_start"].max()
    min_duration = df["closure_duration_days"].min()
    max_duration = df["closure_duration_days"].max()

    print(f"  Date range: {min_date.date()} to {max_date.date()}")
    print(f"  Duration range: {min_duration} to {max_duration} days")

    # Calculate map center from data
    center_lat = df["latitude"].mean()
    center_lon = df["longitude"].mean()

    # Create base map
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
        tiles="OpenStreetMap"
    )

    # Add markers for each closure
    for idx, row in df.iterrows():
        color = get_color_by_date(row["closure_start"], min_date, max_date)
        radius = get_marker_size(row["closure_duration_days"], min_duration, max_duration)

        popup_html = create_closure_popup(row)

        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=radius,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"Store {row['dept_id']}: {row['closure_duration_days']} days"
        ).add_to(m)

    # Add legend
    legend = create_legend(min_date, max_date, min_duration, max_duration, len(df))
    m.get_root().add_child(legend)

    print(f"  Added {len(df)} closure markers")

    return m


def main():
    """Main function to create and save the closure map."""
    print("=" * 60)
    print("Store Closure Map Visualization")
    print("=" * 60)

    # Load data
    df = load_closures_data()

    if len(df) == 0:
        print("\nNo closures with valid coordinates found!")
        return

    # Create map
    m = create_closure_map(df)

    # Save map
    m.save(str(OUTPUT_HTML))
    print(f"\nMap saved to: {OUTPUT_HTML}")

    print("\n" + "=" * 60)
    print("Done! Open the HTML file in your browser to view the map.")
    print("=" * 60)


if __name__ == "__main__":
    main()
