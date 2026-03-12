"""
Identify store closures using consecutive zero-demand days as a proxy.

This script analyzes order data to find stores that experienced consecutive
periods of zero demand (10+ days) with non-zero demand before AND after,
which may indicate Covid-19 related closures.
"""

import os
from pathlib import Path
from typing import List, Tuple

import pandas as pd
import numpy as np


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "order_commodity_result_processed.csv"
GEOCODED_STORES_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "nanjing_store_locations"
    / "nanjing_stores_geocoded.csv"
)
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "store"
OUTPUT_CSV = OUTPUT_DIR / "store_closures.csv"


def load_order_data() -> pd.DataFrame:
    """Load order data and convert dt to datetime."""
    print(f"Loading order data from: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    df["dt"] = pd.to_datetime(df["dt"])

    # Get date range and store count
    print(f"  Date range: {df['dt'].min().date()} to {df['dt'].max().date()}")
    print(f"  Total records: {len(df):,}")
    print(f"  Unique stores: {df['dept_id'].nunique()}")

    return df


def create_zero_demand_grid(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a complete grid of all date × store combinations and mark zero-demand days.

    Returns a DataFrame with columns: dept_id, dt, has_demand (0/1)
    """
    print("\nCreating zero-demand grid...")

    # Get all unique dates and store IDs
    all_dates = sorted(df["dt"].unique())
    all_dept_ids = sorted(df["dept_id"].unique())

    print(f"  Total unique dates: {len(all_dates)}")
    print(f"  Total unique stores: {len(all_dept_ids)}")

    # Create complete grid of all date × store combinations
    complete_grid = pd.MultiIndex.from_product(
        [all_dates, all_dept_ids], names=["dt", "dept_id"]
    ).to_frame(index=False)

    # Get actual records (store-date combinations that have demand)
    actual_records = (
        df.groupby(["dt", "dept_id"]).size().reset_index(name="count")
    )
    actual_records = actual_records[["dt", "dept_id"]]

    # Merge to identify which combinations have no records (zero demand)
    merged = complete_grid.merge(
        actual_records, on=["dt", "dept_id"], how="left", indicator=True
    )

    # Mark has_demand: 1 if record exists, 0 if zero demand
    merged["has_demand"] = (merged["_merge"] == "both").astype(int)

    result = merged[["dept_id", "dt", "has_demand"]].sort_values(["dept_id", "dt"])

    zero_demand_count = (result["has_demand"] == 0).sum()
    total_count = len(result)
    print(f"  Zero-demand cells: {zero_demand_count:,} ({zero_demand_count/total_count*100:.2f}%)")

    return result


def find_consecutive_zero_periods(
    demand_df: pd.DataFrame, min_days: int = 10
) -> List[Tuple[int, pd.Timestamp, pd.Timestamp, int]]:
    """
    Find consecutive zero-demand periods for each store.

    Args:
        demand_df: DataFrame with columns dept_id, dt, has_demand
        min_days: Minimum consecutive days to consider as a closure

    Returns:
        List of tuples: (dept_id, closure_start, closure_end, duration_days)
    """
    print(f"\nFinding consecutive zero-demand periods (minimum {min_days} days)...")

    closures = []

    for dept_id in sorted(demand_df["dept_id"].unique()):
        store_data = demand_df[demand_df["dept_id"] == dept_id].copy()
        store_data = store_data.sort_values("dt").reset_index(drop=True)

        # Find consecutive zero-demand periods
        zero_mask = store_data["has_demand"] == 0

        # Identify groups of consecutive zeros
        # Create a group identifier that increments when has_demand changes
        store_data["group"] = (zero_mask != zero_mask.shift()).cumsum()

        # Filter to only zero-demand groups
        zero_groups = store_data[zero_mask].groupby("group")

        for _, group in zero_groups:
            duration = len(group)

            if duration >= min_days:
                closure_start = group["dt"].min()
                closure_end = group["dt"].max()

                # Check if there's demand before AND after this closure
                has_demand_before = store_data[
                    store_data["dt"] < closure_start
                ]["has_demand"].max() == 1

                has_demand_after = store_data[
                    store_data["dt"] > closure_end
                ]["has_demand"].max() == 1

                if has_demand_before and has_demand_after:
                    closures.append(
                        (dept_id, closure_start, closure_end, duration)
                    )

    print(f"  Found {len(closures)} closures meeting criteria")
    return closures


def create_closures_table(
    closures: List[Tuple[int, pd.Timestamp, pd.Timestamp, int]], geocoded_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Create a DataFrame of closures with store coordinates.

    Args:
        closures: List of tuples from find_consecutive_zero_periods
        geocoded_df: DataFrame with store coordinates

    Returns:
        DataFrame with closure information
    """
    print("\nCreating closures table...")

    # Convert closures list to DataFrame
    closures_df = pd.DataFrame(
        closures, columns=["dept_id", "closure_start", "closure_end", "closure_duration_days"]
    )

    # Merge with geocoded store data
    # Only keep successfully geocoded stores with coordinates
    geocoded_valid = geocoded_df[
        (geocoded_df["geocode_status"] == "ok") &
        (geocoded_df["within_nanjing_bounds"] == True)
    ][["dept_id", "latitude", "longitude", "address"]]

    closures_df = closures_df.merge(geocoded_valid, on="dept_id", how="left")

    # Sort by closure start date
    closures_df = closures_df.sort_values("closure_start").reset_index(drop=True)

    # Convert dates to string format for CSV
    closures_df["closure_start"] = closures_df["closure_start"].dt.strftime("%Y-%m-%d")
    closures_df["closure_end"] = closures_df["closure_end"].dt.strftime("%Y-%m-%d")

    print(f"  Total closures with coordinates: {len(closures_df)}")

    # Summary statistics
    if len(closures_df) > 0:
        print(f"\nClosure duration statistics:")
        print(f"  Min: {closures_df['closure_duration_days'].min()} days")
        print(f"  Max: {closures_df['closure_duration_days'].max()} days")
        print(f"  Mean: {closures_df['closure_duration_days'].mean():.1f} days")
        print(f"  Median: {closures_df['closure_duration_days'].median():.0f} days")

        print(f"\nUnique stores affected: {closures_df['dept_id'].nunique()}")

        # Count closures per store
        closures_per_store = closures_df.groupby("dept_id").size()
        print(f"\nClosures per store:")
        print(f"  Stores with 1 closure: {(closures_per_store == 1).sum()}")
        print(f"  Stores with 2+ closures: {(closures_per_store >= 2).sum()}")

    return closures_df


def main(min_closure_days: int = 10):
    """
    Main function to identify store closures.

    Args:
        min_closure_days: Minimum consecutive zero-demand days to consider as closure
    """
    print("=" * 60)
    print("Store Closure Identification")
    print("=" * 60)

    # Load data
    df = load_order_data()

    # Create zero-demand grid
    demand_df = create_zero_demand_grid(df)

    # Find consecutive zero periods
    closures = find_consecutive_zero_periods(demand_df, min_days=min_closure_days)

    # Load geocoded stores
    print(f"\nLoading geocoded stores from: {GEOCODED_STORES_PATH}")
    geocoded_df = pd.read_csv(GEOCODED_STORES_PATH, encoding="utf-8-sig")

    # Create closures table
    closures_df = create_closures_table(closures, geocoded_df)

    # Save to CSV
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    closures_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    print(f"\nClosures table saved to: {OUTPUT_CSV}")

    # Display first few rows
    if len(closures_df) > 0:
        print("\n" + "=" * 60)
        print("Sample closures (first 5):")
        print("=" * 60)
        print(closures_df[["dept_id", "closure_start", "closure_end", "closure_duration_days"]].head(5).to_string(index=False))

    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)


if __name__ == "__main__":
    # You can customize the minimum closure days here
    main(min_closure_days=10)
