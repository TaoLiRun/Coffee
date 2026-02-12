"""
Analyze customer-store relationships and the impact of store closures on customers.

This script analyzes:
1. Histogram of unique stores visited per customer
2. For each closure, identify affected customers and their purchase behavior during closure
"""

import os
from pathlib import Path
from typing import List, Tuple, Dict, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # Coffee directory
# PROJECT_ROOT.parents[0] is Coffee_code (where data1031 is located)
DATA_DIR = PROJECT_ROOT.parents[0] / "data1031"
ORDER_DATA_PATH = DATA_DIR / "order_commodity_result.csv"
CLOSURES_CSV = PROJECT_ROOT / "plots" / "nanjing_store_locations" / "store_closures.csv"
OUTPUT_DIR = PROJECT_ROOT / "plots" / "customer_store_analysis"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# Default config values
DEFAULT_LOWEST_PURCHASES = 5
DEFAULT_LOWEST_RATIO = 0.8


def load_order_data() -> pd.DataFrame:
    """Load order data and prepare for analysis."""
    print(f"Loading order data from: {ORDER_DATA_PATH}")
    df = pd.read_csv(ORDER_DATA_PATH, encoding="utf-8-sig")

    # Select relevant columns
    cols = ["member_id", "create_hour", "dept_id"]
    df = df[cols].copy()

    # Parse datetime and extract date
    df["dt"] = pd.to_datetime(df["create_hour"], errors="coerce")
    df = df.dropna(subset=["dt"])
    df["date"] = df["dt"].dt.date

    print(f"  Total records: {len(df):,}")
    print(f"  Unique customers: {df['member_id'].nunique():,}")
    print(f"  Unique stores: {df['dept_id'].nunique():,}")
    print(f"  Date range: {df['dt'].min().date()} to {df['dt'].max().date()}")

    return df


def get_customer_unique_stores(
    df: pd.DataFrame, lowest_purchases: int = DEFAULT_LOWEST_PURCHASES
) -> pd.DataFrame:
    """
    Calculate the number of unique stores each customer visited.

    Only considers customers with at least lowest_purchases orders on different days.

    Returns DataFrame with columns: member_id, unique_stores, purchase_count
    """
    print(f"\nCalculating unique stores per customer (min {lowest_purchases} purchases)...")

    # Get unique member-date-store combinations (one purchase per day per store max)
    unique_visits = df[["member_id", "date", "dept_id"]].drop_duplicates()

    # Count purchases per customer (unique days)
    purchase_counts = unique_visits.groupby("member_id").size().reset_index(name="purchase_count")

    # Filter customers with enough purchases
    qualified_customers = purchase_counts[purchase_counts["purchase_count"] >= lowest_purchases]["member_id"]

    # Count unique stores per qualified customer
    unique_stores = (
        unique_visits[unique_visits["member_id"].isin(qualified_customers)]
        .groupby("member_id")["dept_id"]
        .nunique()
        .reset_index(name="unique_stores")
    )

    # Merge with purchase counts
    result = unique_stores.merge(purchase_counts, on="member_id")

    print(f"  Qualified customers: {len(result):,}")
    print(f"  Unique stores per customer:")
    print(f"    Min: {result['unique_stores'].min()}")
    print(f"    Max: {result['unique_stores'].max()}")
    print(f"    Mean: {result['unique_stores'].mean():.2f}")
    print(f"    Median: {result['unique_stores'].median():.0f}")

    return result


def plot_unique_stores_histogram(
    customer_stores: pd.DataFrame, lowest_purchases: int = DEFAULT_LOWEST_PURCHASES
) -> Path:
    """Create and save histogram of unique stores visited per customer."""
    print(f"\nCreating histogram of unique stores per customer...")

    fig, ax = plt.subplots(figsize=(10, 6))

    # Create histogram
    data = customer_stores["unique_stores"].values
    bins = np.arange(0.5, data.max() + 1.5, 1)

    ax.hist(data, bins=bins, edgecolor="black", alpha=0.7, color="steelblue")

    ax.set_xlabel("Number of Unique Stores Visited", fontsize=12, fontweight="bold")
    ax.set_ylabel("Number of Customers", fontsize=12, fontweight="bold")
    ax.set_title(
        f"Distribution of Unique Stores per Customer\n(Only customers with ≥{lowest_purchases} purchases on different days)",
        fontsize=14,
        fontweight="bold",
    )

    # Add statistics text
    stats_text = f"n={len(data):,} customers\nMean={data.mean():.2f} stores\nMedian={np.median(data):.0f} stores"
    ax.text(0.95, 0.95, stats_text, transform=ax.transAxes, fontsize=10,
            verticalalignment="top", horizontalalignment="right",
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))

    ax.grid(True, alpha=0.3, axis="y")

    plt.tight_layout()

    output_path = OUTPUT_DIR / f"unique_stores_histogram_p{lowest_purchases}.pdf"
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"  Histogram saved to: {output_path}")
    plt.close()

    return output_path


def get_customer_store_preference(
    df: pd.DataFrame, lowest_purchases: int = DEFAULT_LOWEST_PURCHASES
) -> pd.DataFrame:
    """
    Calculate for each customer their preferred store (most visited).

    Returns DataFrame with columns: member_id, preferred_store, total_purchases, preferred_ratio
    """
    print(f"\nCalculating customer store preferences (min {lowest_purchases} purchases)...")

    # Get unique member-date-store combinations
    unique_visits = df[["member_id", "date", "dept_id"]].drop_duplicates()

    # Count purchases per customer per store
    customer_store_counts = (
        unique_visits.groupby(["member_id", "dept_id"]).size().reset_index(name="store_purchases")
    )

    # Count total purchases per customer
    customer_totals = unique_visits.groupby("member_id").size().reset_index(name="total_purchases")

    # Filter customers with enough purchases
    qualified_customers = customer_totals[customer_totals["total_purchases"] >= lowest_purchases]["member_id"]

    # For each customer, find their most visited store and ratio
    customer_store_counts = customer_store_counts[
        customer_store_counts["member_id"].isin(qualified_customers)
    ]

    # Find max store purchases per customer
    max_idx = customer_store_counts.groupby("member_id")["store_purchases"].idxmax()
    preferred_stores = customer_store_counts.loc[max_idx].copy()

    # Calculate ratio
    preferred_stores = preferred_stores.merge(customer_totals, on="member_id")
    preferred_stores["preferred_ratio"] = (
        preferred_stores["store_purchases"] / preferred_stores["total_purchases"]
    )

    preferred_stores = preferred_stores.rename(
        columns={"dept_id": "preferred_store", "store_purchases": "preferred_store_purchases"}
    )

    print(f"  Qualified customers: {len(preferred_stores):,}")
    print(f"  Preferred store ratio:")
    print(f"    Min: {preferred_stores['preferred_ratio'].min():.3f}")
    print(f"    Max: {preferred_stores['preferred_ratio'].max():.3f}")
    print(f"    Mean: {preferred_stores['preferred_ratio'].mean():.3f}")
    print(f"    Median: {preferred_stores['preferred_ratio'].median():.3f}")

    return preferred_stores


def analyze_closure_impact(
    df: pd.DataFrame,
    closures: pd.DataFrame,
    customer_preference: pd.DataFrame,
    lowest_purchases: int = DEFAULT_LOWEST_PURCHASES,
    lowest_ratio: float = DEFAULT_LOWEST_RATIO,
) -> pd.DataFrame:
    """
    Analyze the impact of each closure on customers.

    For each closure, identify:
    - Customers who meet lowest_purchases AND lowest_ratio for the closed store (affected)
    - Customers who meet lowest_purchases but NOT lowest_ratio (control)
    - Ratio of each group that made a purchase during the closure period
    """
    print(f"\nAnalyzing closure impact...")
    print(f"  Config: lowest_purchases={lowest_purchases}, lowest_ratio={lowest_ratio}")

    results = []

    for idx, closure in closures.iterrows():
        dept_id = closure["dept_id"]
        closure_start = pd.to_datetime(closure["closure_start"])
        closure_end = pd.to_datetime(closure["closure_end"])

        # Find customers who prefer this store (meet lowest_ratio)
        store_affected = customer_preference[
            (customer_preference["preferred_store"] == dept_id) &
            (customer_preference["preferred_ratio"] >= lowest_ratio)
        ]["member_id"].tolist()

        # Find customers who qualify but don't prefer this store (control)
        # Use customers with similar total purchase count distribution for fair comparison
        all_qualified = customer_preference[
            customer_preference["total_purchases"] >= lowest_purchases
        ]

        # For control, select customers whose preferred store is NOT dept_id
        # and whose preferred_ratio is < lowest_ratio
        store_control = all_qualified[
            (all_qualified["preferred_store"] != dept_id) &
            (all_qualified["preferred_ratio"] < lowest_ratio)
        ]["member_id"].tolist()

        # Get all customer purchases
        all_purchases = df[["member_id", "dt"]].drop_duplicates()

        # Purchases during closure period
        closure_purchases = all_purchases[
            (all_purchases["dt"] >= closure_start) & (all_purchases["dt"] <= closure_end)
        ]

        # Calculate ratios
        affected_purchased = closure_purchases[closure_purchases["member_id"].isin(store_affected)]
        control_purchased = closure_purchases[closure_purchases["member_id"].isin(store_control)]

        affected_count = len(store_affected)
        affected_purchased_count = affected_purchased["member_id"].nunique()
        affected_ratio = affected_purchased_count / affected_count if affected_count > 0 else 0

        control_count = len(store_control)
        control_purchased_count = control_purchased["member_id"].nunique()
        control_ratio = control_purchased_count / control_count if control_count > 0 else 0

        results.append({
            "dept_id": dept_id,
            "closure_start": closure["closure_start"],
            "closure_end": closure["closure_end"],
            "closure_duration_days": closure["closure_duration_days"],
            "#customers_lowest_purchases_lowest_ratio": affected_count,
            "affected_purchased_during_closure_ratio": affected_ratio,
            "#customers_lowest_purchases_only": control_count,
            "control_purchased_during_closure_ratio": control_ratio,
            "selectivity_ratio": affected_ratio / control_ratio if control_ratio > 0 else np.nan,
        })

    result_df = pd.DataFrame(results)

    print(f"  Analyzed {len(result_df)} closures")

    return result_df


def merge_with_closures(
    impact_df: pd.DataFrame, closures: pd.DataFrame
) -> pd.DataFrame:
    """Merge impact analysis with original closure data."""
    # Select key columns from closures
    closure_cols = ["dept_id", "closure_start", "closure_end", "closure_duration_days",
                    "latitude", "longitude", "address"]

    result = impact_df.merge(
        closures[closure_cols],
        on=["dept_id", "closure_start", "closure_end", "closure_duration_days"],
        how="left",
        suffixes=("", "_original")
    )

    # Remove duplicate columns if any
    result = result.loc[:, ~result.columns.duplicated()]

    return result


def main(
    lowest_purchases: int = DEFAULT_LOWEST_PURCHASES,
    lowest_ratio: float = DEFAULT_LOWEST_RATIO,
):
    """Main analysis function."""
    print("=" * 70)
    print("Customer-Store Closure Impact Analysis")
    print("=" * 70)

    # Load data
    df = load_order_data()
    closures = pd.read_csv(CLOSURES_CSV, encoding="utf-8-sig")

    # Task 1: Histogram of unique stores per customer
    print("\n" + "=" * 70)
    print("Task 1: Distribution of Unique Stores per Customer")
    print("=" * 70)

    customer_stores = get_customer_unique_stores(df, lowest_purchases=lowest_purchases)
    plot_unique_stores_histogram(customer_stores, lowest_purchases=lowest_purchases)

    # Task 2: Closure impact analysis
    print("\n" + "=" * 70)
    print("Task 2: Closure Impact on Customers")
    print("=" * 70)

    customer_preference = get_customer_store_preference(df, lowest_purchases=lowest_purchases)
    impact_df = analyze_closure_impact(
        df, closures, customer_preference,
        lowest_purchases=lowest_purchases,
        lowest_ratio=lowest_ratio
    )

    # Merge with original closure data
    final_df = merge_with_closures(impact_df, closures)

    # Reorder columns for readability
    cols_order = [
        "dept_id", "closure_start", "closure_end", "closure_duration_days",
        "#customers_lowest_purchases_lowest_ratio",
        "affected_purchased_during_closure_ratio",
        "#customers_lowest_purchases_only",
        "control_purchased_during_closure_ratio",
        "selectivity_ratio",
        "latitude", "longitude", "address"
    ]

    # Only include columns that exist
    cols_order = [c for c in cols_order if c in final_df.columns]
    final_df = final_df[cols_order]

    # Sort by closure start date
    final_df = final_df.sort_values("closure_start").reset_index(drop=True)

    # Save results
    output_csv = OUTPUT_DIR / f"closure_impact_analysis_p{lowest_purchases}_r{int(lowest_ratio*100)}.csv"
    final_df.to_csv(output_csv, index=False, encoding="utf-8-sig")

    print(f"\nResults saved to: {output_csv}")

    # Print summary statistics
    print("\n" + "=" * 70)
    print("Summary Statistics")
    print("=" * 70)

    print(f"\nAffected customers per closure:")
    print(f"  Mean: {final_df['#customers_lowest_purchases_lowest_ratio'].mean():.1f}")
    print(f"  Median: {final_df['#customers_lowest_purchases_lowest_ratio'].median():.0f}")
    print(f"  Min: {final_df['#customers_lowest_purchases_lowest_ratio'].min()}")
    print(f"  Max: {final_df['#customers_lowest_purchases_lowest_ratio'].max()}")

    print(f"\nAffected purchase ratio during closure:")
    print(f"  Mean: {final_df['affected_purchased_during_closure_ratio'].mean():.3f}")
    print(f"  Median: {final_df['affected_purchased_during_closure_ratio'].median():.3f}")

    print(f"\nControl purchase ratio during closure:")
    print(f"  Mean: {final_df['control_purchased_during_closure_ratio'].mean():.3f}")
    print(f"  Median: {final_df['control_purchased_during_closure_ratio'].median():.3f}")

    print(f"\nSelectivity ratio (affected/control):")
    print(f"  Mean: {final_df['selectivity_ratio'].mean():.3f}")
    print(f"  Median: {final_df['selectivity_ratio'].median():.3f}")

    # Display first few rows
    print("\n" + "=" * 70)
    print("Sample Results (first 5 rows):")
    print("=" * 70)
    display_cols = [
        "dept_id", "closure_start", "closure_end", "closure_duration_days",
        "#customers_lowest_purchases_lowest_ratio",
        "affected_purchased_during_closure_ratio",
        "#customers_lowest_purchases_only",
        "control_purchased_during_closure_ratio",
        "selectivity_ratio"
    ]
    print(final_df[display_cols].head().to_string(index=False))

    print("\n" + "=" * 70)
    print("Analysis Complete!")
    print("=" * 70)


if __name__ == "__main__":
    main(
        lowest_purchases=DEFAULT_LOWEST_PURCHASES,
        lowest_ratio=DEFAULT_LOWEST_RATIO
    )
