"""
Analyze customer-store relationships and the impact of store closures on customers.

This script analyzes:
1. Justification for DEFAULT_LOWEST_PURCHASES and DEFAULT_LOWEST_RATIO thresholds
2. Histogram of unique stores visited per customer
3. Staggered Difference-in-Difference closure impact analysis with
   pre/during/post behavior comparison (purchases, product variety,
   product lifetime, discount & coupon usage)
4. Visualizations of treatment vs control behavior across periods
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from scipy import stats


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # model-free directory
DATA_DIR = PROJECT_ROOT.parent / "data" / "data1031"
ORDER_COMMODITY_PATH = DATA_DIR / "order_commodity_result.csv"
ORDER_RESULT_PATH = DATA_DIR / "order_result.csv"
CLOSURES_CSV = PROJECT_ROOT / "outputs" / "store" / "non_uni_store_closures.csv"
OUTPUT_DIR = PROJECT_ROOT / "plots" / "customer_store_analysis"
OUTPUT_CUSTOMER_STORE_DIR = PROJECT_ROOT / "outputs" / "customer-store"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Default config values
DEFAULT_LOWEST_PURCHASES = 5
DEFAULT_LOWEST_RATIO = 0.8
DEFAULT_WINDOW_DAYS = 14   # pre/post window in days
ROBUSTNESS_WINDOW_DAYS = 28
DEFAULT_CLOSURE_TWO_GROUP_THRESHOLD = 30  # days: short vs long closure split
NO_PUSH_MEMBERS_PATH = PROJECT_ROOT / "data" / "processed" / "no_push_members.csv"

# Set-up-time-matched control (Option A): True = match control stores by set_up_time, one-time use, pre-closure preference
USE_SET_UP_TIME_MATCHED_CONTROL = True
DEPT_STATIC_PATH = DATA_DIR / "dept_result_static.csv"
SET_UP_TIME_NEAREST_N = 5
MIN_GROUP_SIZE = 50  # skip closure if #treatment or #control < this
MIN_CTRL_TREAT_RATIO = 2.0  # skip closure if ctrl_rate < this * treat_rate


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_order_commodity_data() -> pd.DataFrame:
    """
    Load order-commodity data, parse datetime, and unify product names.

    Each row is one item in an order.  The product name is spread across
    four mutually-exclusive commodity columns; we consolidate them into a
    single 'product_name' column.
    """
    print(f"Loading order commodity data from: {ORDER_COMMODITY_PATH}")
    df = pd.read_csv(ORDER_COMMODITY_PATH, encoding="utf-8-sig")

    df["dt"] = pd.to_datetime(df["create_hour"], errors="coerce")
    df = df.dropna(subset=["dt"])
    df["date"] = df["dt"].dt.date

    # Unified product name: exactly one name column is non-null per row
    product_cols = [
        "coffee_commodity_name",
        "food_commodity_name",
        "drink_not_coffee_commodity_name",
        "other_not_coffee_commodity_name",
    ]
    df["product_name"] = df[product_cols].apply(
        lambda row: next((v for v in row if pd.notna(v) and v != ""), np.nan), axis=1
    )

    print(f"  Total records: {len(df):,}")
    print(f"  Unique customers: {df['member_id'].nunique():,}")
    print(f"  Unique stores: {df['dept_id'].nunique():,}")
    print(f"  Date range: {df['dt'].min().date()} to {df['dt'].max().date()}")
    return df


def load_order_result_data() -> pd.DataFrame:
    """
    Load order-level data (one row per order) with discount and coupon columns.

    Aggregates category-level discounts into a single 'total_discount' column
    and derives a binary 'used_coupon' flag.
    """
    print(f"Loading order result data from: {ORDER_RESULT_PATH}")
    df = pd.read_csv(ORDER_RESULT_PATH, encoding="utf-8-sig")
    df["dt"] = pd.to_datetime(df["create_hour"], errors="coerce")
    df = df.dropna(subset=["dt"])
    df["date"] = df["dt"].dt.date

    discount_cols = [
        "coffee_discount",
        "drink_not_coffee_discount",
        "food_discount",
        "other_discount",
    ]
    existing_discount = [c for c in discount_cols if c in df.columns]
    df["total_discount"] = df[existing_discount].sum(axis=1, min_count=1)

    df["used_coupon"] = (df["use_coupon_num"] > 0).astype(int) if "use_coupon_num" in df.columns else 0

    print(f"  Total orders: {len(df):,}")
    return df[["member_id", "order_id", "dt", "date", "dept_id",
               "total_discount", "used_coupon", "disount_tag"]]


def load_store_set_up_times(path: Path) -> pd.DataFrame:
    """
    Load store static table and return dept_id (int) and set_up_time (date).
    Raises FileNotFoundError if path missing; raises ValueError if required cols or set_up_time missing.
    """
    if not path.exists():
        raise FileNotFoundError(f"Store static file not found: {path}")
    df = pd.read_csv(path, encoding="utf-8-sig")
    if "dept_id" not in df.columns or "set_up_time" not in df.columns:
        raise ValueError(f"Store static must have columns dept_id and set_up_time; got {list(df.columns)}")
    df["dept_id"] = df["dept_id"].astype(str).str.strip().replace(r"^0+", "", regex=True)
    df = df[df["dept_id"] != ""]
    df["dept_id"] = df["dept_id"].astype(int)
    df["set_up_time"] = pd.to_datetime(df["set_up_time"], errors="coerce")
    if df["set_up_time"].isna().any():
        bad = df[df["set_up_time"].isna()]["dept_id"].tolist()
        raise ValueError(f"Store static has missing or invalid set_up_time for dept_id: {bad[:10]}{'...' if len(bad) > 10 else ''}")
    df["set_up_time"] = df["set_up_time"].dt.date
    return df[["dept_id", "set_up_time"]].drop_duplicates(subset=["dept_id"])


# ---------------------------------------------------------------------------
# Threshold justification
# ---------------------------------------------------------------------------

def analyze_threshold_justification(
    df: pd.DataFrame,
    lowest_purchases: int = DEFAULT_LOWEST_PURCHASES,
    lowest_ratio: float = DEFAULT_LOWEST_RATIO,
) -> None:
    """
    Justify the choice of DEFAULT_LOWEST_PURCHASES and DEFAULT_LOWEST_RATIO.

    Prints:
    - Population-level distribution of per-customer purchase counts
    - Fraction of customers qualifying at various purchase thresholds
    - Distribution of preferred-store loyalty ratio at various ratio thresholds
    """
    print("\n" + "=" * 70)
    print("Threshold Justification Analysis")
    print("=" * 70)

    # --- Purchase count distribution ---
    unique_visits = df[["member_id", "date", "dept_id"]].drop_duplicates()
    purchase_counts = unique_visits.groupby("member_id").size().reset_index(name="purchase_count")
    pc = purchase_counts["purchase_count"]

    print("\n[1] Population-level purchase count statistics (unique purchase days per customer):")
    print(f"    Total customers : {len(pc):,}")
    print(f"    Min             : {pc.min()}")
    print(f"    Max             : {pc.max()}")
    print(f"    Mean            : {pc.mean():.2f}")
    print(f"    Median          : {pc.median():.0f}")
    print(f"    Std             : {pc.std():.2f}")
    print(f"    25th pct        : {pc.quantile(0.25):.0f}")
    print(f"    75th pct        : {pc.quantile(0.75):.0f}")

    print("\n[2] Coverage at different purchase thresholds:")
    total_customers = len(pc)
    for threshold in [1, 2, 3, 5, 7, 10, 15, 20]:
        n_q = (pc >= threshold).sum()
        print(f"    >= {threshold:2d} purchases : {n_q:7,} customers ({n_q/total_customers*100:.1f}%)")
    n_chosen = (pc >= lowest_purchases).sum()
    print(f"    --> Chosen threshold = {lowest_purchases}: "
          f"{n_chosen:,} customers ({n_chosen/total_customers*100:.1f}%) qualify")

    # --- Preferred-store ratio distribution among qualified customers ---
    qualified_ids = purchase_counts[purchase_counts["purchase_count"] >= lowest_purchases]["member_id"]
    qual_visits = unique_visits[unique_visits["member_id"].isin(qualified_ids)]

    cust_store = qual_visits.groupby(["member_id", "dept_id"]).size().reset_index(name="n")
    cust_total = qual_visits.groupby("member_id").size().reset_index(name="total")
    max_idx = cust_store.groupby("member_id")["n"].idxmax()
    top_store = cust_store.loc[max_idx].merge(cust_total, on="member_id")
    top_store["ratio"] = top_store["n"] / top_store["total"]
    r = top_store["ratio"]

    print("\n[3] Preferred-store ratio (max single-store share) among qualified customers:")
    print(f"    Count   : {len(r):,}")
    print(f"    Min     : {r.min():.3f}")
    print(f"    Max     : {r.max():.3f}")
    print(f"    Mean    : {r.mean():.3f}")
    print(f"    Median  : {r.median():.3f}")
    print(f"    Std     : {r.std():.3f}")
    print(f"    50th pct: {r.quantile(0.50):.3f}")
    print(f"    75th pct: {r.quantile(0.75):.3f}")
    print(f"    90th pct: {r.quantile(0.90):.3f}")

    print("\n[4] Coverage at different ratio thresholds (among qualified customers):")
    n_qual = len(r)
    for threshold in [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
        n = (r >= threshold).sum()
        print(f"    ratio >= {threshold:.1f} : {n:7,} customers ({n/n_qual*100:.1f}%)")
    n_loyal = (r >= lowest_ratio).sum()
    print(f"    --> Chosen ratio = {lowest_ratio}: "
          f"{n_loyal:,} customers ({n_loyal/n_qual*100:.1f}%) are store-loyal")


# ---------------------------------------------------------------------------
# Unique stores histogram
# ---------------------------------------------------------------------------

def get_customer_unique_stores(
    df: pd.DataFrame, lowest_purchases: int = DEFAULT_LOWEST_PURCHASES
) -> pd.DataFrame:
    """
    Calculate the number of unique stores each customer visited.

    Only considers customers with at least lowest_purchases orders on different days.
    Returns DataFrame with columns: member_id, unique_stores, purchase_count.
    """
    print(f"\nCalculating unique stores per customer (min {lowest_purchases} purchases)...")
    unique_visits = df[["member_id", "date", "dept_id"]].drop_duplicates()
    purchase_counts = unique_visits.groupby("member_id").size().reset_index(name="purchase_count")
    qualified = purchase_counts[purchase_counts["purchase_count"] >= lowest_purchases]["member_id"]

    unique_stores = (
        unique_visits[unique_visits["member_id"].isin(qualified)]
        .groupby("member_id")["dept_id"]
        .nunique()
        .reset_index(name="unique_stores")
    )
    result = unique_stores.merge(purchase_counts, on="member_id")

    print(f"  Qualified customers: {len(result):,}")
    print(f"  Unique stores - Min: {result['unique_stores'].min()}, "
          f"Max: {result['unique_stores'].max()}, "
          f"Mean: {result['unique_stores'].mean():.2f}, "
          f"Median: {result['unique_stores'].median():.0f}")
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


# ---------------------------------------------------------------------------
# Customer store preference
# ---------------------------------------------------------------------------

def get_customer_store_preference(
    df: pd.DataFrame, lowest_purchases: int = DEFAULT_LOWEST_PURCHASES
) -> pd.DataFrame:
    """
    Calculate each qualified customer's preferred store and loyalty ratio.

    Returns DataFrame with columns:
      member_id, preferred_store, preferred_store_purchases,
      total_purchases, preferred_ratio
    """
    print(f"\nCalculating customer store preferences (min {lowest_purchases} purchases)...")
    unique_visits = df[["member_id", "date", "dept_id"]].drop_duplicates()
    customer_store_counts = (
        unique_visits.groupby(["member_id", "dept_id"]).size().reset_index(name="store_purchases")
    )
    customer_totals = unique_visits.groupby("member_id").size().reset_index(name="total_purchases")
    qualified = customer_totals[customer_totals["total_purchases"] >= lowest_purchases]["member_id"]
    customer_store_counts = customer_store_counts[customer_store_counts["member_id"].isin(qualified)]
    max_idx = customer_store_counts.groupby("member_id")["store_purchases"].idxmax()
    preferred_stores = customer_store_counts.loc[max_idx].copy()
    preferred_stores = preferred_stores.merge(customer_totals, on="member_id")
    preferred_stores["preferred_ratio"] = (
        preferred_stores["store_purchases"] / preferred_stores["total_purchases"]
    )
    preferred_stores = preferred_stores.rename(
        columns={"dept_id": "preferred_store", "store_purchases": "preferred_store_purchases"}
    )
    print(f"  Qualified customers: {len(preferred_stores):,}")
    print(f"  Preferred store ratio - Mean: {preferred_stores['preferred_ratio'].mean():.3f}, "
          f"Median: {preferred_stores['preferred_ratio'].median():.3f}")
    return preferred_stores


# ---------------------------------------------------------------------------
# Product feature helpers
# ---------------------------------------------------------------------------

def compute_product_first_appearance(df: pd.DataFrame) -> pd.Series:
    """
    Compute the first calendar date each product name appeared in the full dataset.

    Returns a Series indexed by product_name with date (datetime.date) values.
    Product lifetime for an item = date_of_purchase - first_appearance_date (in days).
    """
    first_app = (
        df.dropna(subset=["product_name"])
        .groupby("product_name")["date"]
        .min()
    )
    print(f"\nComputed first-appearance date for {len(first_app):,} unique products.")
    return first_app


# ---------------------------------------------------------------------------
# Per-customer period behavior extraction
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Fast date-range pre-index (call once after loading data)
# ---------------------------------------------------------------------------

def build_date_sorted_index(df: pd.DataFrame, date_col: str = "date") -> pd.DataFrame:
    """
    Sort a DataFrame by date column and reset index for O(log n) date range slicing
    via numpy searchsorted.  Attach `_dates_np` attribute for reuse.
    """
    df_sorted = df.sort_values(date_col).reset_index(drop=True)
    return df_sorted


def _slice_by_date(df_sorted: pd.DataFrame, start_date, end_date) -> pd.DataFrame:
    """
    Extract rows where date is in [start_date, end_date] using binary search.
    Requires df_sorted to have been produced by build_date_sorted_index().
    """
    dates = df_sorted["date"].values          # numpy array of date objects
    lo = int(np.searchsorted(dates, start_date, side="left"))
    hi = int(np.searchsorted(dates, end_date,   side="right"))
    return df_sorted.iloc[lo:hi]




def _compute_customer_behavior(
    df_commodity: pd.DataFrame,   # must be date-sorted (via build_date_sorted_index)
    df_order: pd.DataFrame,       # must be date-sorted
    member_ids: List,
    start_date,
    end_date,
    period_length_days: int,      # number of calendar days in this period (for normalisation)
) -> pd.DataFrame:
    """
    Compute per-customer behaviour metrics over [start_date, end_date].

    Returns a DataFrame with one row per member (all members in member_ids),
    with columns:
      member_id, n_purchases (per day), new_product_ratio,
      total_discount, coupon_usage_rate.

    Metrics:
      - n_purchases        : purchase days in period / period_length_days
      - new_product_ratio  : distinct new products (never tried before start_date)
                             divided by total distinct products in period
      - total_discount     : mean per-order discount (NaN if no orders)
      - coupon_usage_rate  : fraction of orders that used a coupon (NaN if no orders)
    """
    if not member_ids:
        return pd.DataFrame()

    id_set = set(member_ids)
    result = pd.DataFrame({"member_id": member_ids})

    # --- fast date-range slice for the current period, then member filter ---
    pc_date = _slice_by_date(df_commodity, start_date, end_date)
    pc = pc_date[pc_date["member_id"].isin(id_set)] if not pc_date.empty else pc_date

    po_date = _slice_by_date(df_order, start_date, end_date)
    po = po_date[po_date["member_id"].isin(id_set)] if not po_date.empty else po_date

    # per-customer purchase days (normalised by period length)
    result["n_purchases"] = (
        pc[["member_id", "date"]].drop_duplicates()
        .groupby("member_id").size()
        .reindex(member_ids, fill_value=0)
        .astype(float) / period_length_days
    ).values

    # per-customer new-product ratio
    # "new" = product the customer had never purchased before start_date
    if not pc.empty:
        pcom_period = pc.dropna(subset=["product_name"])[["member_id", "product_name"]].drop_duplicates()
        if not pcom_period.empty:
            earliest_date = df_commodity["date"].iloc[0]  # df is sorted
            history_end = (pd.Timestamp(start_date) - pd.Timedelta(days=1)).date()
            if history_end >= earliest_date:
                pc_hist = _slice_by_date(df_commodity, earliest_date, history_end)
                pc_hist_filt = (
                    pc_hist[pc_hist["member_id"].isin(id_set)]
                    .dropna(subset=["product_name"])[["member_id", "product_name"]]
                    .drop_duplicates()
                )
            else:
                pc_hist_filt = pd.DataFrame(columns=["member_id", "product_name"])

            merged = pcom_period.merge(
                pc_hist_filt.assign(_seen=True),
                on=["member_id", "product_name"],
                how="left",
            )
            merged["_is_new"] = merged["_seen"].isna()
            per_cust_new = merged.groupby("member_id").agg(
                _total=("product_name", "count"),
                _new=("_is_new", "sum"),
            )
            per_cust_new["new_product_ratio"] = per_cust_new["_new"] / per_cust_new["_total"]
            result["new_product_ratio"] = (
                per_cust_new["new_product_ratio"].reindex(member_ids).values
            )
        else:
            result["new_product_ratio"] = np.nan
    else:
        result["new_product_ratio"] = np.nan

    if not po.empty:
        result["total_discount"]   = po.groupby("member_id")["total_discount"].mean().reindex(member_ids).values
        result["coupon_usage_rate"] = po.groupby("member_id")["used_coupon"].mean().reindex(member_ids).values
    else:
        result["total_discount"]   = np.nan
        result["coupon_usage_rate"] = np.nan

    return result


# ---------------------------------------------------------------------------
# Staggered DiD treatment / control selection
# ---------------------------------------------------------------------------

def _get_treated_members_for_store(
    customer_preference: pd.DataFrame,
    dept_id: int,
    lowest_ratio: float,
) -> List:
    """Return member IDs loyal (>= lowest_ratio) to a specific store."""
    return (
        customer_preference[
            (customer_preference["preferred_store"] == dept_id) &
            (customer_preference["preferred_ratio"] >= lowest_ratio)
        ]["member_id"].tolist()
    )


def get_never_treated_members(
    closures: pd.DataFrame,
    customer_preference: pd.DataFrame,
    lowest_purchases: int,
    lowest_ratio: float,
) -> List:
    """
    Return member IDs that are qualified (>= lowest_purchases) but whose
    preferred store never appears in the closures list with loyalty >=
    lowest_ratio.  These customers serve as the "clean" control group
    for all closure analyses.
    """
    all_treated: set = set()
    for _, closure in closures.iterrows():
        all_treated.update(
            _get_treated_members_for_store(
                customer_preference, int(closure["dept_id"]), lowest_ratio
            )
        )
    qualified = set(
        customer_preference[
            (customer_preference["total_purchases"] >= lowest_purchases) &
            (customer_preference["preferred_ratio"] >= lowest_ratio)
        ]["member_id"].tolist()
    )
    never_treated = sorted(qualified - all_treated)
    print(f"  Never-treated control pool: {len(never_treated):,} customers")
    return never_treated


def get_closure_specific_control_members(
    unique_visits: pd.DataFrame,
    control_pool: List,
    closure_start_date,
    lowest_purchases: int,
    lowest_ratio: float,
) -> List:
    """
    For a given closure, return never-treated consumers who were qualified
    *at the time of the closure*: >= lowest_purchases purchases before
    closure_start, with >= lowest_ratio of those at a single store.

    unique_visits: DataFrame with columns member_id, date, dept_id
    control_pool: list of member_ids (never-treated)
    closure_start_date: date object (exclusive: purchases must be before this)
    """
    if not control_pool:
        return []

    pool_set = set(control_pool)
    pre = unique_visits[
        (unique_visits["member_id"].isin(pool_set)) &
        (unique_visits["date"] < closure_start_date)
    ]
    if pre.empty:
        return []

    pre_counts = pre.groupby("member_id").size()
    qualified = pre_counts[pre_counts >= lowest_purchases].index.tolist()
    if not qualified:
        return []

    pre_qual = pre[pre["member_id"].isin(qualified)]
    cust_store = pre_qual.groupby(["member_id", "dept_id"]).size().reset_index(name="store_purchases")
    cust_total = pre_qual.groupby("member_id").size().reset_index(name="total_purchases")
    cust_store = cust_store.merge(cust_total, on="member_id")
    cust_store["ratio"] = cust_store["store_purchases"] / cust_store["total_purchases"]
    max_ratio = cust_store.groupby("member_id")["ratio"].max()
    qualified_loyal = max_ratio[max_ratio >= lowest_ratio].index.tolist()
    return sorted(qualified_loyal)


# ---------------------------------------------------------------------------
# Set-up-time-matched control (one-time use per store, pre-closure preference)
# ---------------------------------------------------------------------------

def get_control_stores_per_closure(
    closures_df: pd.DataFrame,
    store_df: pd.DataFrame,
    n_nearest: int,
    treated_store_ids: set,
) -> Dict[Tuple[int, Any], List[int]]:
    """
    Assign up to n_nearest control stores per closure by set_up_time similarity.
    Each store is used as control at most once (closure_start_asc order).
    Raises if closed store not in store_df or no candidates for a closure.
    Returns dict mapping (dept_id, closure_start) -> list of control store dept_ids.
    """
    store_df = store_df.dropna(subset=["set_up_time"]).copy()
    closures_sorted = closures_df.sort_values("closure_start").reset_index(drop=True)
    used_control_store_ids: set = set()
    result: Dict[Tuple[int, Any], List[int]] = {}

    for _, closure in closures_sorted.iterrows():
        closed_dept_id = int(closure["dept_id"])
        closure_start = closure["closure_start"]
        closure_key = (closed_dept_id, closure_start)

        if closed_dept_id not in store_df["dept_id"].values:
            raise ValueError(
                f"Closed store dept_id={closed_dept_id} (closure_start={closure_start}) "
                f"not found in store static. Cannot get set_up_time."
            )

        t0 = store_df.loc[store_df["dept_id"] == closed_dept_id, "set_up_time"].iloc[0]

        candidates = store_df[
            (~store_df["dept_id"].isin(treated_store_ids))
            & (~store_df["dept_id"].isin(used_control_store_ids))
        ].copy()
        if candidates.empty:
            raise ValueError(
                f"No eligible control store candidates for closure {closure_key}. "
                "All similar stores may be treated or already used."
            )

        candidates["_diff"] = candidates["set_up_time"].apply(
            lambda d: abs((d - t0).days) if hasattr(d - t0, "days") else float("inf")
        )
        candidates = candidates.sort_values("_diff")
        chosen = candidates.head(n_nearest)["dept_id"].tolist()
        used_control_store_ids.update(chosen)
        result[closure_key] = chosen

    return result


def get_preference_before_date(
    unique_visits: pd.DataFrame,
    cutoff_date: Any,
) -> pd.DataFrame:
    """
    Compute preferred store and ratio using only visits with date < cutoff_date.
    Returns DataFrame with member_id, preferred_store, preferred_ratio, total_purchases.
    """
    pre = unique_visits[unique_visits["date"] < pd.Timestamp(cutoff_date).date()]
    if pre.empty:
        return pd.DataFrame(columns=["member_id", "preferred_store", "preferred_ratio", "total_purchases"])

    cust_store = pre.groupby(["member_id", "dept_id"]).size().reset_index(name="store_purchases")
    cust_total = pre.groupby("member_id").size().reset_index(name="total_purchases")
    cust_store = cust_store.merge(cust_total, on="member_id")
    cust_store["ratio"] = cust_store["store_purchases"] / cust_store["total_purchases"]
    idx_max = cust_store.groupby("member_id")["ratio"].idxmax()
    preferred = cust_store.loc[idx_max].rename(
        columns={"dept_id": "preferred_store", "ratio": "preferred_ratio", "total_purchases": "total_purchases"}
    )[["member_id", "preferred_store", "preferred_ratio", "total_purchases"]]
    preferred["preferred_store"] = preferred["preferred_store"].astype(int)
    return preferred


def get_closure_control_members_set_up_matched(
    unique_visits: pd.DataFrame,
    closure_start_date: Any,
    control_store_ids: List[int],
    lowest_purchases: int,
    lowest_ratio: float,
    closure_key: Tuple[int, Any],
) -> List[int]:
    """
    Return control member IDs: qualified (pre-closure) and preferred_store in control_store_ids.
    Returns empty list if no qualified members (caller should skip and log).
    """
    if not control_store_ids:
        return []

    pref = get_preference_before_date(unique_visits, closure_start_date)
    control_set = set(control_store_ids)
    out = pref[
        (pref["preferred_store"].isin(control_set))
        & (pref["total_purchases"] >= lowest_purchases)
        & (pref["preferred_ratio"] >= lowest_ratio)
    ]["member_id"].tolist()

    return sorted(out) if out else []


# ---------------------------------------------------------------------------
# Staggered DiD closure impact analysis
# ---------------------------------------------------------------------------

def analyze_closure_impact(
    df_commodity: pd.DataFrame,
    df_order: pd.DataFrame,
    closures: pd.DataFrame,
    customer_preference: pd.DataFrame,
    lowest_purchases: int = DEFAULT_LOWEST_PURCHASES,
    lowest_ratio: float = DEFAULT_LOWEST_RATIO,
    window_days: int = DEFAULT_WINDOW_DAYS,
    use_set_up_time_matched_control: bool = False,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Staggered Difference-in-Difference closure impact analysis.

    If use_set_up_time_matched_control is False (default):
      - Treatment: customers whose preferred store is the closed store (global preference).
      - Control: never-treated pool, qualified at closure time.

    If use_set_up_time_matched_control is True:
      - Treatment: pre-closure preference, preferred_store = closed store, qualified.
      - Control: pre-closure preference, preferred_store in nearest-N set_up_time–matched stores (each store used once).

    period_df has one row per (closure, group, period, customer).

    Returns:
      summary_df : one row per closure with group sizes and purchase rates
      period_df  : one row per (closure, group, period, member_id) with metrics
    """
    print(f"\nAnalyzing closure impact (staggered DiD, window={window_days} days)...")
    print(f"  Config: lowest_purchases={lowest_purchases}, lowest_ratio={lowest_ratio}")
    print(f"  Control: use_set_up_time_matched_control={use_set_up_time_matched_control}")

    # Pre-sort once so _slice_by_date (binary search) works correctly
    print("  Pre-sorting data by date for fast period slicing...")
    df_com_s = build_date_sorted_index(df_commodity)
    df_ord_s = build_date_sorted_index(df_order)
    print("  Pre-sorting done.")

    unique_visits = df_commodity[["member_id", "date", "dept_id"]].drop_duplicates()

    if use_set_up_time_matched_control:
        store_df = load_store_set_up_times(DEPT_STATIC_PATH)
        treated_store_ids = set(closures["dept_id"].astype(int).unique())
        control_stores_by_closure = get_control_stores_per_closure(
            closures, store_df, n_nearest=SET_UP_TIME_NEAREST_N, treated_store_ids=treated_store_ids
        )
        print(f"  Set-up-time-matched control: {len(control_stores_by_closure)} closures with control stores assigned.")
        control_pool = None
    else:
        control_pool = get_never_treated_members(
            closures, customer_preference, lowest_purchases, lowest_ratio
        )
        control_stores_by_closure = None

    summary_rows: List[Dict] = []
    period_frames: List[pd.DataFrame] = []

    for _, closure in closures.iterrows():
        dept_id = int(closure["dept_id"])
        closure_start = pd.to_datetime(closure["closure_start"])
        closure_end = pd.to_datetime(closure["closure_end"])

        pre_start  = (closure_start - pd.Timedelta(days=window_days)).date()
        pre_end    = (closure_start - pd.Timedelta(days=1)).date()
        dur_start  = closure_start.date()
        dur_end    = closure_end.date()
        post_start = (closure_end + pd.Timedelta(days=1)).date()
        post_end   = (closure_end + pd.Timedelta(days=window_days)).date()

        if use_set_up_time_matched_control:
            closure_key = (dept_id, closure["closure_start"])
            pref = get_preference_before_date(unique_visits, closure_start.date())
            treatment = pref[
                (pref["preferred_store"] == dept_id)
                & (pref["preferred_ratio"] >= lowest_ratio)
                & (pref["total_purchases"] >= lowest_purchases)
            ]["member_id"].tolist()
            control_store_ids = control_stores_by_closure[closure_key]
            closure_control = get_closure_control_members_set_up_matched(
                unique_visits, closure_start.date(), control_store_ids,
                lowest_purchases, lowest_ratio, closure_key,
            )
        else:
            treatment = _get_treated_members_for_store(
                customer_preference, dept_id, lowest_ratio
            )
            closure_control = get_closure_specific_control_members(
                unique_visits, control_pool, closure_start.date(),
                lowest_purchases, lowest_ratio,
            )

        if not treatment:
            print(f"  Skipping closure (dept_id={dept_id}, closure_start={closure['closure_start']}): no qualified treatment members.")
            continue

        if not closure_control:
            msg = f"  Skipping closure (dept_id={dept_id}, closure_start={closure['closure_start']}): no qualified control members."
            if use_set_up_time_matched_control:
                msg += f" (control_stores={control_store_ids})"
            print(msg)
            continue

        if len(treatment) < MIN_GROUP_SIZE or len(closure_control) < MIN_GROUP_SIZE:
            print(f"  Skipping closure (dept_id={dept_id}, closure_start={closure['closure_start']}): #treatment={len(treatment)} or #control={len(closure_control)} < {MIN_GROUP_SIZE}.")
            continue

        # Compute during-period purchase rates for filter
        during_slice = _slice_by_date(df_com_s, dur_start, dur_end)
        during_purch = during_slice[["member_id"]].drop_duplicates()
        t_rate = during_purch["member_id"].isin(treatment).sum() / len(treatment)
        c_rate = during_purch["member_id"].isin(closure_control).sum() / len(closure_control)

        if c_rate < MIN_CTRL_TREAT_RATIO * t_rate:
            print(f"  Skipping closure (dept_id={dept_id}, closure_start={closure['closure_start']}): ctrl_rate={c_rate:.3f} < {MIN_CTRL_TREAT_RATIO}*treat_rate={t_rate:.3f}.")
            continue

        # Period lengths for normalisation
        closure_duration = int(closure["closure_duration_days"])
        period_lengths = {
            "pre":    window_days,
            "during": max(closure_duration, 1),
            "post":   window_days,
        }

        # Customer-level behavior for all six (group × period) combinations
        for group_label, members in [("treatment", treatment), ("control", closure_control)]:
            for period_label, s, e in [
                ("pre",    pre_start,  pre_end),
                ("during", dur_start,  dur_end),
                ("post",   post_start, post_end),
            ]:
                cust_df = _compute_customer_behavior(
                    df_com_s, df_ord_s,
                    members, s, e,
                    period_length_days=period_lengths[period_label],
                )
                if not cust_df.empty:
                    cust_df["dept_id"]                = dept_id
                    cust_df["closure_start"]           = closure["closure_start"]
                    cust_df["window_days"]             = window_days
                    cust_df["closure_duration_days"]   = closure["closure_duration_days"]
                    cust_df["group"]                   = group_label
                    cust_df["period"]                  = period_label
                    period_frames.append(cust_df)

        summary_rows.append({
            "dept_id":                        dept_id,
            "closure_start":                  closure["closure_start"],
            "closure_end":                    closure["closure_end"],
            "closure_duration_days":          closure["closure_duration_days"],
            "window_days":                    window_days,
            "#treatment":                     len(treatment),
            "#control":                       len(closure_control),
            "treatment_purchase_rate_during": t_rate,
            "control_purchase_rate_during":   c_rate,
            "selectivity_ratio":              t_rate / c_rate if c_rate and c_rate > 0 else np.nan,
        })
        print(
            f"  Closure dept={dept_id} "
            f"({closure['closure_start']} – {closure['closure_end']}): "
            f"treated={len(treatment)}, control={len(closure_control)}, "
            f"treat_rate={t_rate:.3f}, ctrl_rate={c_rate:.3f}"
        )

    summary_df = pd.DataFrame(summary_rows).sort_values("closure_start").reset_index(drop=True)
    period_df_out = (
        pd.concat(period_frames, ignore_index=True) if period_frames else pd.DataFrame()
    )
    print(f"\n  Analyzed {len(summary_df)} closures.")

    # Save the subset of closures that were not skipped (same schema as non_uni_store_closures.csv)
    if not summary_df.empty:
        kept = closures.merge(
            summary_df[["dept_id", "closure_start"]],
            on=["dept_id", "closure_start"],
            how="inner",
        )
        OUTPUT_CUSTOMER_STORE_DIR.mkdir(parents=True, exist_ok=True)
        closures_used_path = OUTPUT_CUSTOMER_STORE_DIR / "closures_used.csv"
        kept.to_csv(closures_used_path, index=False, encoding="utf-8-sig")
        print(f"  Closures used in analysis (not skipped) saved to: {closures_used_path} ({len(kept)} rows)")

    return summary_df, period_df_out


# ---------------------------------------------------------------------------
# Visualization
# ---------------------------------------------------------------------------

BEHAVIOR_METRICS = [
    ("n_purchases",        "Purchase Days per Day"),
    ("new_product_ratio",  "New Product Ratio"),
    ("total_discount",     "Mean Total Discount"),
    ("coupon_usage_rate",  "Coupon Usage Rate"),
]
PERIOD_ORDER = ["pre", "during", "post"]


# ---------------------------------------------------------------------------
# Statistical tests
# ---------------------------------------------------------------------------

def _sig_stars(pvalue: float) -> str:
    """Return significance stars for a p-value."""
    if np.isnan(pvalue):  return "n/a"
    if pvalue < 0.001:    return "***"
    if pvalue < 0.01:     return "**"
    if pvalue < 0.05:     return "*"
    return "ns"


def _cust_vals(
    df: pd.DataFrame,
    group: str,
    period: str,
    metric: str,
    deduplicate: bool = False,
) -> pd.Series:
    """
    Extract customer-level metric values for a (group, period) slice.

    If deduplicate=True, average each customer across closures first
    (used for never-treated control customers who appear in every closure).
    """
    sub = df[(df["group"] == group) & (df["period"] == period)][["member_id", metric]].dropna()
    if deduplicate:
        return sub.groupby("member_id")[metric].mean()
    return sub.groupby("member_id")[metric].mean()   # harmless dedup for treatment too


def _paired_ttest(
    df: pd.DataFrame,
    group: str,
    period_a: str,
    period_b: str,
    metric: str,
) -> Tuple[float, int]:
    """
    Paired t-test by customer: group[period_a] vs group[period_b].

    For treatment, each customer appears in exactly one closure.
    For control (never-treated), customers are deduplicated (averaged across
    closures) before pairing.
    Returns (pvalue, n_pairs).
    """
    a = _cust_vals(df, group, period_a, metric, deduplicate=True)
    b = _cust_vals(df, group, period_b, metric, deduplicate=True)
    common = a.index.intersection(b.index)
    if len(common) < 2:
        return np.nan, len(common)
    return float(stats.ttest_rel(a[common], b[common]).pvalue), len(common)


def _between_group_ttest(
    df: pd.DataFrame,
    period: str,
    metric: str,
) -> Tuple[float, int, int]:
    """
    Independent-samples t-test: treatment vs control customer values in period.

    Treatment customers each appear in exactly one closure (one value each).
    Control customers are deduplicated (averaged across closures).
    Returns (pvalue, n_treatment, n_control).
    """
    t_vals = _cust_vals(df, "treatment", period, metric, deduplicate=False)
    c_vals = _cust_vals(df, "control",   period, metric, deduplicate=True)
    if len(t_vals) < 2 or len(c_vals) < 2:
        return np.nan, len(t_vals), len(c_vals)
    return float(stats.ttest_ind(t_vals, c_vals, equal_var=False).pvalue), len(t_vals), len(c_vals)


def run_statistical_tests(
    period_df: pd.DataFrame,
    window_days: int = DEFAULT_WINDOW_DAYS,
) -> pd.DataFrame:
    """
    Run statistical tests for four comparisons per metric:
      1. Treatment Pre vs Post  — paired t-test by customer
      2. Control   Pre vs Post  — paired t-test by customer (deduplicated)
      3. T vs C in Pre period   — independent-samples Welch t-test
      4. T vs C in Post period  — independent-samples Welch t-test

    Prints a formatted table and returns a DataFrame with columns:
      metric, comparison, n, pvalue, stars
    """
    df = period_df[period_df["window_days"] == window_days].copy()
    if df.empty:
        print(f"No data for window_days={window_days} — skipping tests.")
        return pd.DataFrame()

    print("\n" + "=" * 70)
    print(f"Statistical Tests (customer-level, window={window_days} days)")
    print("=" * 70)

    rows: List[Dict] = []

    for metric, metric_label in BEHAVIOR_METRICS:
        print(f"\n  Metric: {metric_label}")

        # 1. Treatment Pre vs Post (paired by customer)
        p, n = _paired_ttest(df, "treatment", "pre", "post", metric)
        s = _sig_stars(p)
        p_str = f"{p:.4f}" if not np.isnan(p) else "n/a   "
        print(f"    treat_pre_vs_post          : p={p_str}  {s}  (n={n} customers)")
        rows.append({"metric": metric, "comparison": "treat_pre_vs_post",
                     "n": n, "pvalue": p, "stars": s})

        # 2. Control Pre vs Post (paired by customer, deduplicated)
        p, n = _paired_ttest(df, "control", "pre", "post", metric)
        s = _sig_stars(p)
        p_str = f"{p:.4f}" if not np.isnan(p) else "n/a   "
        print(f"    ctrl_pre_vs_post           : p={p_str}  {s}  (n={n} customers)")
        rows.append({"metric": metric, "comparison": "ctrl_pre_vs_post",
                     "n": n, "pvalue": p, "stars": s})

        # 3. T vs C in Pre (independent Welch t-test)
        p, nt, nc = _between_group_ttest(df, "pre", metric)
        s = _sig_stars(p)
        p_str = f"{p:.4f}" if not np.isnan(p) else "n/a   "
        print(f"    T_vs_C_in_pre              : p={p_str}  {s}  (nT={nt}, nC={nc})")
        rows.append({"metric": metric, "comparison": "T_vs_C_in_pre",
                     "n": nt + nc, "pvalue": p, "stars": s})

        # 4. T vs C in Post (independent Welch t-test)
        p, nt, nc = _between_group_ttest(df, "post", metric)
        s = _sig_stars(p)
        p_str = f"{p:.4f}" if not np.isnan(p) else "n/a   "
        print(f"    T_vs_C_in_post             : p={p_str}  {s}  (nT={nt}, nC={nc})")
        rows.append({"metric": metric, "comparison": "T_vs_C_in_post",
                     "n": nt + nc, "pvalue": p, "stars": s})

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Significance bracket helper
# ---------------------------------------------------------------------------

def _add_bracket(
    ax,
    x1: float,
    x2: float,
    y: float,
    text: str,
    tick: float = 0.0,
    fontsize: int = 8,
    color: str = "black",
) -> None:
    """
    Draw a significance bracket between x1 and x2 at height y.
    tick controls the vertical tick mark size at each end.
    """
    ax.plot([x1, x1, x2, x2],
            [y, y + tick, y + tick, y],
            lw=0.9, c=color, clip_on=False)
    ax.text((x1 + x2) / 2, y + tick, text,
            ha="center", va="bottom", fontsize=fontsize, color=color)


def visualize_behavior_comparison(
    period_df: pd.DataFrame,
    window_days: int = DEFAULT_WINDOW_DAYS,
    tag: str = "",
    test_results: Optional[pd.DataFrame] = None,
) -> None:
    """
    Plot mean ± std of treatment vs control across pre / during / post periods.

    Significance brackets are drawn for four paired t-test comparisons per metric:
      - Treatment Pre vs Post  (red bracket, upper level)
      - Control Pre vs Post    (blue bracket, upper level)
      - T vs C in Pre          (grey bracket, lower level)
      - T vs C in Post         (grey bracket, lower level)

    `test_results` is the DataFrame returned by run_statistical_tests().
    If None, tests are computed internally.

    Saves:
      - One combined PDF with all metrics side by side
      - One individual PDF per metric
    Both written to OUTPUT_DIR.
    """
    if period_df is None or period_df.empty:
        print("No period data to visualize.")
        return

    df = period_df[period_df["window_days"] == window_days].copy()
    if df.empty:
        print(f"No data for window_days={window_days}.")
        return

    # Compute tests if not supplied
    if test_results is None or test_results.empty:
        test_results = run_statistical_tests(period_df, window_days)

    def _get_sig(metric: str, comparison: str) -> str:
        if test_results is None or test_results.empty:
            return ""
        row = test_results[(test_results["metric"] == metric) &
                           (test_results["comparison"] == comparison)]
        return row["stars"].values[0] if len(row) else ""

    print(f"\nCreating behavior comparison plots (window={window_days} days)...")

    n_metrics = len(BEHAVIOR_METRICS)
    x = np.arange(len(PERIOD_ORDER))
    width = 0.35
    colors = {"treatment": "#d62728", "control": "#1f77b4"}
    suffix = f"_w{window_days}" + (f"_{tag}" if tag else "")

    def _get_mean_std(grp_df: pd.DataFrame, metric: str) -> Tuple[List, List]:
        """
        Compute mean ± std per period from customer-level rows.
        Deduplicate by customer first (average across closures) so that
        never-treated control customers are not counted multiple times.
        """
        means, stds = [], []
        for period in PERIOD_ORDER:
            sub = grp_df[grp_df["period"] == period][["member_id", metric]].dropna()
            per_cust = sub.groupby("member_id")[metric].mean()
            means.append(float(per_cust.mean()) if len(per_cust) else np.nan)
            stds.append(float(per_cust.std()) if len(per_cust) > 1 else 0.0)
        return means, stds

    def _annotate_ax(ax, metric: str) -> None:
        """Draw significance brackets on ax for the given metric."""
        # bar x-centres: treat offset=-width/2, ctrl offset=+width/2
        half = width / 2
        # (period_index, group_offset) → bar x centre
        x_tp = x[0] - half  # treat-pre
        x_cp = x[0] + half  # ctrl-pre
        x_tpo = x[2] - half  # treat-post
        x_cpo = x[2] + half  # ctrl-post

        # compute top of each bar (mean + std, ignoring NaN)
        all_means_stds: List[float] = []
        for i, group in enumerate(["treatment", "control"]):
            grp = df[df["group"] == group]
            means, stds = _get_mean_std(grp, metric)
            for m, s in zip(means, stds):
                if not np.isnan(m):
                    all_means_stds.append(m + (s if not np.isnan(s) else 0))
        y_data_top = max(all_means_stds) if all_means_stds else 0.0
        step = max(abs(y_data_top) * 0.08, 1e-6)
        tick = step * 0.25

        # Level 1 (lower): T vs C within Pre and within Post
        h1 = y_data_top + step
        s_tcp = _get_sig(metric, "T_vs_C_in_pre")
        s_tcpo = _get_sig(metric, "T_vs_C_in_post")
        if s_tcp:
            _add_bracket(ax, x_tp, x_cp, h1, s_tcp, tick=tick, fontsize=7, color="#444444")
        if s_tcpo:
            _add_bracket(ax, x_tpo, x_cpo, h1, s_tcpo, tick=tick, fontsize=7, color="#444444")

        # Level 2 (higher): within-group Pre vs Post
        h2 = h1 + step * 2.2
        s_treat = _get_sig(metric, "treat_pre_vs_post")
        s_ctrl  = _get_sig(metric, "ctrl_pre_vs_post")
        if s_treat:
            _add_bracket(ax, x_tp, x_tpo, h2, s_treat, tick=tick, fontsize=7,
                         color=colors["treatment"])
        if s_ctrl:
            _add_bracket(ax, x_cp, x_cpo, h2 + step * 0.9, s_ctrl, tick=tick, fontsize=7,
                         color=colors["control"])

        # Expand y-axis to accommodate brackets
        new_top = h2 + step * 2.5
        ylo, _ = ax.get_ylim()
        ax.set_ylim(ylo, new_top)

    # ------------------------------------------------------------------ #
    # Combined figure
    # ------------------------------------------------------------------ #
    fig, axes = plt.subplots(1, n_metrics, figsize=(5 * n_metrics, 6))
    if n_metrics == 1:
        axes = [axes]

    for ax, (metric, metric_label) in zip(axes, BEHAVIOR_METRICS):
        for i, group in enumerate(["treatment", "control"]):
            grp = df[df["group"] == group]
            means, stds = _get_mean_std(grp, metric)
            offset = (i - 0.5) * width
            ax.bar(
                x + offset, means, width,
                label=group.capitalize(), color=colors[group], alpha=0.75,
                yerr=stds, capsize=4,
                error_kw={"elinewidth": 1, "ecolor": "black"},
            )
        ax.set_xticks(x)
        ax.set_xticklabels(["Pre", "During", "Post"], fontsize=11)
        ax.set_ylabel(metric_label, fontsize=10)
        ax.set_title(metric_label, fontsize=11, fontweight="bold")
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3, axis="y")
        ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.2f"))
        _annotate_ax(ax, metric)

    fig.suptitle(
        f"Treatment vs Control: Behavior Across Closure Periods\n"
        f"(window = {window_days} days, mean \u00b1 std across closures)\n"
        f"Brackets: *** p<0.001  ** p<0.01  * p<0.05  ns = not significant",
        fontsize=11, fontweight="bold",
    )
    plt.tight_layout(rect=[0, 0, 1, 0.90])
    combined_path = OUTPUT_DIR / f"behavior_comparison{suffix}.pdf"
    plt.savefig(combined_path, dpi=300, bbox_inches="tight")
    print(f"  Combined plot saved: {combined_path}")
    plt.close()

    # ------------------------------------------------------------------ #
    # Individual metric plots
    # ------------------------------------------------------------------ #
    '''
    for metric, metric_label in BEHAVIOR_METRICS:
        fig2, ax2 = plt.subplots(figsize=(6, 5))
        for i, group in enumerate(["treatment", "control"]):
            grp = df[df["group"] == group]
            means, stds = _get_mean_std(grp, metric)
            offset = (i - 0.5) * width
            ax2.bar(
                x + offset, means, width,
                label=group.capitalize(), color=colors[group], alpha=0.75,
                yerr=stds, capsize=4,
                error_kw={"elinewidth": 1, "ecolor": "black"},
            )
        ax2.set_xticks(x)
        ax2.set_xticklabels(["Pre", "During", "Post"], fontsize=11)
        ax2.set_ylabel(metric_label, fontsize=11)
        ax2.set_title(
            f"{metric_label}\n(window = {window_days} days)",
            fontsize=11, fontweight="bold",
        )
        ax2.legend(fontsize=9)
        ax2.grid(True, alpha=0.3, axis="y")
        _annotate_ax(ax2, metric)
        ax2.annotate(
            "Brackets: *** p<0.001  ** p<0.01  * p<0.05  ns = not significant",
            xy=(0.5, -0.12), xycoords="axes fraction",
            ha="center", fontsize=7, color="#555555",
        )
        plt.tight_layout()
        safe_metric = metric.replace("_", "-")
        out2 = OUTPUT_DIR / f"behavior_{safe_metric}{suffix}.pdf"
        plt.savefig(out2, dpi=300, bbox_inches="tight")
        plt.close()
    print(f"  Individual metric plots saved to: {OUTPUT_DIR}")
    '''


# ---------------------------------------------------------------------------
# Duration-split combined plots
# ---------------------------------------------------------------------------

def visualize_behavior_comparison_by_duration_split(
    period_df: pd.DataFrame,
    window_days: int = DEFAULT_WINDOW_DAYS,
    threshold_days: int = DEFAULT_CLOSURE_TWO_GROUP_THRESHOLD,
    tag: str = "",
) -> None:
    """
    Generate two Combined plots split by closure duration:
      - Short closures  : closure_duration_days <  threshold_days
      - Long closures   : closure_duration_days >= threshold_days

    Each subset is passed to visualize_behavior_comparison with an appropriate tag.
    """
    if period_df is None or period_df.empty:
        print("No period data for duration-split plots.")
        return

    if "closure_duration_days" not in period_df.columns:
        print("  closure_duration_days column missing — cannot split by duration.")
        return

    df_w = period_df[period_df["window_days"] == window_days]
    short = df_w[df_w["closure_duration_days"] < threshold_days]
    long_ = df_w[df_w["closure_duration_days"] >= threshold_days]

    base_tag = (f"_{tag}" if tag else "")
    print(f"\nDuration-split plots (threshold={threshold_days} days):")
    print(f"  Short closures (< {threshold_days} days): "
          f"{short['dept_id'].nunique()} closures, {len(short):,} rows")
    print(f"  Long  closures (>= {threshold_days} days): "
          f"{long_['dept_id'].nunique()} closures, {len(long_):,} rows")

    if not short.empty:
        visualize_behavior_comparison(
            short, window_days=window_days,
            tag=f"short_lt{threshold_days}{base_tag}",
        )
    else:
        print(f"  No short closures (<{threshold_days} days) found.")

    if not long_.empty:
        visualize_behavior_comparison(
            long_, window_days=window_days,
            tag=f"long_ge{threshold_days}{base_tag}",
        )
    else:
        print(f"  No long closures (>={threshold_days} days) found.")


# ---------------------------------------------------------------------------
# Push-split treatment combined plot
# ---------------------------------------------------------------------------

def load_no_push_member_ids() -> set:
    """Load the set of member IDs who opted out of push notifications."""
    if not NO_PUSH_MEMBERS_PATH.exists():
        print(f"  Warning: no_push_members file not found at {NO_PUSH_MEMBERS_PATH}. "
              f"Push-split plot will be skipped.")
        return set()
    df = pd.read_csv(NO_PUSH_MEMBERS_PATH, encoding="utf-8-sig")
    ids = set(df["member_id"].unique())
    print(f"  Loaded {len(ids):,} no-push member IDs.")
    return ids


def visualize_behavior_comparison_push_split(
    period_df: pd.DataFrame,
    no_push_ids: set,
    window_days: int = DEFAULT_WINDOW_DAYS,
    tag: str = "",
) -> None:
    """
    Generate a Combined plot where the treatment group is split by push opt-in:
      - treatment_no_push   : treatment customers in no_push_ids
      - treatment_with_push : treatment customers NOT in no_push_ids
      - control             : unchanged control group

    Significance brackets are drawn only for within-subgroup Pre vs Post
    paired t-tests (no between-subgroup or T-vs-C tests).
    """
    if period_df is None or period_df.empty:
        print("No period data for push-split plot.")
        return
    if not no_push_ids:
        print("  No push-member IDs available — skipping push-split plot.")
        return

    df = period_df[period_df["window_days"] == window_days].copy()
    if df.empty:
        print(f"No data for window_days={window_days} — skipping push-split plot.")
        return

    # Re-label treatment rows based on push membership
    treat_mask = df["group"] == "treatment"
    df.loc[treat_mask & df["member_id"].isin(no_push_ids),  "group"] = "treatment_no_push"
    df.loc[treat_mask & ~df["member_id"].isin(no_push_ids), "group"] = "treatment_with_push"

    n_no_push   = df[df["group"] == "treatment_no_push"]["member_id"].nunique()
    n_with_push = df[df["group"] == "treatment_with_push"]["member_id"].nunique()
    print(f"\nPush-split treatment plot (window={window_days} days):")
    print(f"  treatment_no_push   : {n_no_push:,} unique members")
    print(f"  treatment_with_push : {n_with_push:,} unique members")

    groups_to_plot = ["treatment_no_push", "treatment_with_push", "control"]
    colors = {
        "treatment_no_push":   "#ff7f0e",
        "treatment_with_push": "#d62728",
        "control":             "#1f77b4",
    }
    labels = {
        "treatment_no_push":   "Treat (no push)",
        "treatment_with_push": "Treat (with push)",
        "control":             "Control",
    }

    suffix = f"_w{window_days}_push_split" + (f"_{tag}" if tag else "")

    # Compute per-group pre-vs-post paired t-test for each metric
    push_tests: Dict[Tuple[str, str], Tuple[float, int]] = {}
    for grp in ["treatment_no_push", "treatment_with_push"]:
        for metric, _ in BEHAVIOR_METRICS:
            a = _cust_vals(df, grp, "pre",  metric, deduplicate=True)
            b = _cust_vals(df, grp, "post", metric, deduplicate=True)
            common = a.index.intersection(b.index)
            if len(common) >= 2:
                p = float(stats.ttest_rel(a[common], b[common]).pvalue)
                push_tests[(grp, metric)] = (p, len(common))
            else:
                push_tests[(grp, metric)] = (np.nan, len(common))

    def _get_mean_std_push(grp: str, metric: str) -> Tuple[List, List]:
        means, stds = [], []
        for period in PERIOD_ORDER:
            sub = df[(df["group"] == grp) & (df["period"] == period)][
                ["member_id", metric]
            ].dropna()
            per_cust = sub.groupby("member_id")[metric].mean()
            means.append(float(per_cust.mean()) if len(per_cust) else np.nan)
            stds.append(float(per_cust.std()) if len(per_cust) > 1 else 0.0)
        return means, stds

    n_metrics = len(BEHAVIOR_METRICS)
    x = np.arange(len(PERIOD_ORDER))
    n_groups = len(groups_to_plot)
    width = 0.25
    print(f"\nCreating push-split behavior comparison plot (window={window_days} days)...")

    fig, axes = plt.subplots(1, n_metrics, figsize=(5 * n_metrics, 6))
    if n_metrics == 1:
        axes = [axes]

    for ax, (metric, metric_label) in zip(axes, BEHAVIOR_METRICS):
        all_tops: List[float] = []
        bar_centres: Dict[str, List[float]] = {}

        for i, grp in enumerate(groups_to_plot):
            means, stds = _get_mean_std_push(grp, metric)
            offset = (i - (n_groups - 1) / 2) * width
            centres = x + offset
            bar_centres[grp] = list(centres)
            ax.bar(
                centres, means, width,
                label=labels[grp], color=colors[grp], alpha=0.75,
                yerr=stds, capsize=3,
                error_kw={"elinewidth": 1, "ecolor": "black"},
            )
            for m, s in zip(means, stds):
                if not np.isnan(m):
                    all_tops.append(m + (s if not np.isnan(s) else 0))

        y_top = max(all_tops) if all_tops else 0.0
        step  = max(abs(y_top) * 0.09, 1e-6)
        tick  = step * 0.25

        # Draw pre-vs-post brackets for each treatment subgroup
        for level_idx, grp in enumerate(["treatment_no_push", "treatment_with_push"]):
            p_val, n_pairs = push_tests.get((grp, metric), (np.nan, 0))
            stars = _sig_stars(p_val)
            if stars and grp in bar_centres:
                x_pre  = bar_centres[grp][0]  # period index 0 = pre
                x_post = bar_centres[grp][2]  # period index 2 = post
                h = y_top + step * (2.5 + level_idx * 2.2)
                _add_bracket(ax, x_pre, x_post, h, stars, tick=tick,
                             fontsize=7, color=colors[grp])

        new_top = y_top + step * 7.5
        ylo, _ = ax.get_ylim()
        ax.set_ylim(ylo, new_top)

        ax.set_xticks(x)
        ax.set_xticklabels(["Pre", "During", "Post"], fontsize=11)
        ax.set_ylabel(metric_label, fontsize=10)
        ax.set_title(metric_label, fontsize=11, fontweight="bold")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3, axis="y")
        ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.2f"))

    fig.suptitle(
        f"Treatment (Push Split) vs Control: Behavior Across Closure Periods\n"
        f"(window = {window_days} days, mean \u00b1 std)\n"
        f"Brackets (pre vs post within subgroup): *** p<0.001  ** p<0.01  * p<0.05  ns",
        fontsize=11, fontweight="bold",
    )
    plt.tight_layout(rect=[0, 0, 1, 0.90])
    out_path = OUTPUT_DIR / f"behavior_comparison{suffix}.pdf"
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    print(f"  Push-split combined plot saved: {out_path}")
    plt.close()


# ---------------------------------------------------------------------------
# Merge helper
# ---------------------------------------------------------------------------

def merge_with_closures(impact_df: pd.DataFrame, closures: pd.DataFrame) -> pd.DataFrame:
    """Merge impact summary with original closure metadata."""
    closure_cols = [
        "dept_id", "closure_start", "closure_end", "closure_duration_days",
        "latitude", "longitude", "address",
    ]
    available = [c for c in closure_cols if c in closures.columns]
    join_keys = [c for c in ["dept_id", "closure_start", "closure_end", "closure_duration_days"]
                 if c in available and c in impact_df.columns]
    result = impact_df.merge(closures[available], on=join_keys, how="left")
    return result.loc[:, ~result.columns.duplicated()]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(
    lowest_purchases: int = DEFAULT_LOWEST_PURCHASES,
    lowest_ratio: float = DEFAULT_LOWEST_RATIO,
    window_days: int = DEFAULT_WINDOW_DAYS,
    closure_two_group_threshold: int = DEFAULT_CLOSURE_TWO_GROUP_THRESHOLD,
    use_set_up_time_matched_control: bool = USE_SET_UP_TIME_MATCHED_CONTROL,
):
    """Main analysis function. Run with: python analyze_closure_impact.py > analyze_closure_impact.log 2>&1"""
    print("=" * 70)
    print("Customer-Store Closure Impact Analysis")
    print("=" * 70)

    # Load data
    df = load_order_commodity_data()
    df_order = load_order_result_data()
    closures = pd.read_csv(CLOSURES_CSV, encoding="utf-8-sig")
    print(f"\nLoaded {len(closures)} store closures.")

    # Task 0: Threshold justification
    analyze_threshold_justification(
        df, lowest_purchases=lowest_purchases, lowest_ratio=lowest_ratio
    )

    # Task 1: Histogram of unique stores per customer
    print("\n" + "=" * 70)
    print("Task 1: Distribution of Unique Stores per Customer")
    print("=" * 70)
    customer_stores = get_customer_unique_stores(df, lowest_purchases=lowest_purchases)
    plot_unique_stores_histogram(customer_stores, lowest_purchases=lowest_purchases)

    # Shared inputs for Tasks 2 & 3
    customer_preference = get_customer_store_preference(df, lowest_purchases=lowest_purchases)

    # Task 2a: Staggered DiD — primary window
    print("\n" + "=" * 70)
    print(f"Task 2: Staggered DiD Closure Impact (window={window_days} days)")
    print("=" * 70)
    summary_df, period_df = analyze_closure_impact(
        df, df_order, closures, customer_preference,
        lowest_purchases=lowest_purchases,
        lowest_ratio=lowest_ratio,
        window_days=window_days,
        use_set_up_time_matched_control=use_set_up_time_matched_control,
    )

    # Task 2b: Robustness check — 28-day window
    print("\n" + "=" * 70)
    print(f"Task 2 (robustness): Staggered DiD Closure Impact "
          f"(window={ROBUSTNESS_WINDOW_DAYS} days)")
    print("=" * 70)
    summary_df_rob, period_df_rob = analyze_closure_impact(
        df, df_order, closures, customer_preference,
        lowest_purchases=lowest_purchases,
        lowest_ratio=lowest_ratio,
        window_days=ROBUSTNESS_WINDOW_DAYS,
        use_set_up_time_matched_control=use_set_up_time_matched_control,
    )

    # Merge with closure metadata and save
    final_df     = merge_with_closures(summary_df,     closures)
    final_df_rob = merge_with_closures(summary_df_rob, closures)

    out_csv = (
        OUTPUT_DIR /
        f"closure_impact_did_p{lowest_purchases}_r{int(lowest_ratio*100)}_w{window_days}.csv"
    )
    out_csv_rob = (
        OUTPUT_DIR /
        f"closure_impact_did_p{lowest_purchases}_r{int(lowest_ratio*100)}"
        f"_w{ROBUSTNESS_WINDOW_DAYS}.csv"
    )
    final_df.to_csv(out_csv,     index=False, encoding="utf-8-sig")
    final_df_rob.to_csv(out_csv_rob, index=False, encoding="utf-8-sig")
    print(f"\nSummary saved to: {out_csv}")
    print(f"Robustness summary saved to: {out_csv_rob}")

    # Save period behavior tables
    if not period_df.empty:
        out_period = (
            OUTPUT_DIR /
            f"period_behavior_p{lowest_purchases}_r{int(lowest_ratio*100)}_w{window_days}.csv"
        )
        period_df.to_csv(out_period, index=False, encoding="utf-8-sig")
        print(f"Period behavior saved to: {out_period}")
    if not period_df_rob.empty:
        out_period_rob = (
            OUTPUT_DIR /
            f"period_behavior_p{lowest_purchases}_r{int(lowest_ratio*100)}"
            f"_w{ROBUSTNESS_WINDOW_DAYS}.csv"
        )
        period_df_rob.to_csv(out_period_rob, index=False, encoding="utf-8-sig")
        print(f"Robustness period behavior saved to: {out_period_rob}")

    # Print summary statistics
    print("\n" + "=" * 70)
    print("Summary Statistics (primary window)")
    print("=" * 70)
    for col in [
        "#treatment", "#control",
        "treatment_purchase_rate_during",
        "control_purchase_rate_during",
        "selectivity_ratio",
    ]:
        if col in final_df.columns:
            s = final_df[col]
            print(f"\n{col}:")
            print(f"  Mean   : {s.mean():.3f}")
            print(f"  Median : {s.median():.3f}")
            print(f"  Min    : {s.min():.3f}")
            print(f"  Max    : {s.max():.3f}")

    # Task 3: Statistical tests
    print("\n" + "=" * 70)
    print("Task 3: Statistical Tests")
    print("=" * 70)
    tests_primary  = run_statistical_tests(period_df,     window_days=window_days)
    tests_robust   = run_statistical_tests(period_df_rob, window_days=ROBUSTNESS_WINDOW_DAYS)

    # Save test results
    if not tests_primary.empty:
        out_tests = (
            OUTPUT_DIR /
            f"stat_tests_p{lowest_purchases}_r{int(lowest_ratio*100)}_w{window_days}.csv"
        )
        tests_primary.to_csv(out_tests, index=False, encoding="utf-8-sig")
        print(f"  Test results saved to: {out_tests}")
    if not tests_robust.empty:
        out_tests_rob = (
            OUTPUT_DIR /
            f"stat_tests_p{lowest_purchases}_r{int(lowest_ratio*100)}"
            f"_w{ROBUSTNESS_WINDOW_DAYS}.csv"
        )
        tests_robust.to_csv(out_tests_rob, index=False, encoding="utf-8-sig")
        print(f"  Robustness test results saved to: {out_tests_rob}")

    # Task 4: Visualize behavior comparison with significance annotations
    print("\n" + "=" * 70)
    print("Task 4: Visualize Behavior Comparison")
    print("=" * 70)
    visualize_behavior_comparison(period_df,     window_days=window_days,
                                  test_results=tests_primary)
    visualize_behavior_comparison(period_df_rob, window_days=ROBUSTNESS_WINDOW_DAYS,
                                  tag="robustness", test_results=tests_robust)

    # Task 5: Duration-split combined plots
    print("\n" + "=" * 70)
    print("Task 5: Duration-Split Behavior Comparison")
    print("=" * 70)
    visualize_behavior_comparison_by_duration_split(
        period_df, window_days=window_days,
        threshold_days=closure_two_group_threshold,
    )
    visualize_behavior_comparison_by_duration_split(
        period_df_rob, window_days=ROBUSTNESS_WINDOW_DAYS,
        threshold_days=closure_two_group_threshold,
        tag="robustness",
    )

    # Task 6: Push-split treatment combined plot
    print("\n" + "=" * 70)
    print("Task 6: Push-Split Treatment Behavior Comparison")
    print("=" * 70)
    no_push_ids = load_no_push_member_ids()
    visualize_behavior_comparison_push_split(
        period_df, no_push_ids=no_push_ids, window_days=window_days,
    )
    visualize_behavior_comparison_push_split(
        period_df_rob, no_push_ids=no_push_ids, window_days=ROBUSTNESS_WINDOW_DAYS,
        tag="robustness",
    )

    print("\n" + "=" * 70)
    print("Analysis Complete!")
    print("=" * 70)


if __name__ == "__main__":
    main(
        lowest_purchases=DEFAULT_LOWEST_PURCHASES,
        lowest_ratio=DEFAULT_LOWEST_RATIO,
        window_days=DEFAULT_WINDOW_DAYS,
        closure_two_group_threshold=DEFAULT_CLOSURE_TWO_GROUP_THRESHOLD,
    )
