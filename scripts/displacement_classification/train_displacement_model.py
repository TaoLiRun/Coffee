"""
Train Displacement Classification Model for store closure impact analysis.

Uses 4-week pre-closure window. Builds (consumer, closure, period) panel with
65+ features, trains XGBoost (GPU if available), and outputs:
- Variable importance ranking
- Prediction accuracy: Treatment Pre, Control Pre, Control During

All output is logged to train_displacement_model.log in this directory.
"""

from __future__ import annotations

import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

# Add parent to path for customer-store imports
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]  # model-free
sys.path.insert(0, str(PROJECT_ROOT / "scripts" / "customer-store"))

from analyze_closure_impact import (
    DEFAULT_LOWEST_PURCHASES,
    DEFAULT_LOWEST_RATIO,
    build_date_sorted_index,
    get_closure_specific_control_members,
    get_customer_store_preference,
    get_never_treated_members,
)
from analyze_closure_impact import _get_treated_members_for_store, _slice_by_date

# Paths
DATA_DIR = PROJECT_ROOT.parent / "data" / "data1031"
CLOSURES_CSV = PROJECT_ROOT / "plots" / "nanjing_store_locations" / "store_closures.csv"
MEMBER_RESULT_PATH = DATA_DIR / "member_result.csv"
NO_PUSH_MEMBERS_PATH = PROJECT_ROOT / "data" / "processed" / "no_push_members.csv"

WINDOW_WEEKS = 4
LOG_FILE = SCRIPT_DIR / "train_displacement_model.log"
OUTPUT_DIR = SCRIPT_DIR
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DEMO_INTERMEDIATE_DIR = PROJECT_ROOT / "data" / "intermediate"


def setup_logging() -> logging.Logger:
    """Configure logging to file and console."""
    logger = logging.getLogger("displacement")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    fh = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("%(message)s"))

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


def log_print(logger: logging.Logger, msg: str, level: str = "info") -> None:
    """Log and optionally print."""
    getattr(logger, level)(msg)


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------


def load_member_demographics(logger: logging.Logger, no_push_ids: set) -> pd.DataFrame:
    """
    Load member_result.csv and integer-encode categorical demographics.

    Excluded columns: birth_year, camera, location, network, sdcard.
    Encoding rule: NaN → 1; sorted unique non-NaN values → 2, 3, 4, …
    The mapping is saved to DEMO_INTERMEDIATE_DIR/demo_encoding_map.csv.

    no_push_ids: members whose push value is overridden to 0 before encoding.
    """
    log_print(logger, f"Loading member demographics from {MEMBER_RESULT_PATH}")
    df = pd.read_csv(MEMBER_RESULT_PATH, encoding="utf-8-sig")
    want = ["member_id", "gender", "level", "inviter_id", "manufacturer", "callphone", "push"]
    cols = [c for c in want if c in df.columns]
    df = df[cols].copy()
    log_print(logger, f"  Loaded {len(df):,} members")

    # Derive has_inviter (binary, no NaN) before encoding
    if "inviter_id" in df.columns:
        df["has_inviter"] = (
            df["inviter_id"].notna() & (df["inviter_id"] != "")
        ).astype(int)
        df.drop(columns=["inviter_id"], inplace=True)

    # Apply no_push_ids override BEFORE encoding so push=0 is encoded consistently
    if no_push_ids and "push" in df.columns:
        df.loc[df["member_id"].isin(no_push_ids), "push"] = 0

    # Integer-encode: NaN → 1; sorted unique non-NaN values → 2, 3, 4, …
    encode_cols = [c for c in ["gender", "level", "manufacturer", "callphone", "push", "has_inviter"]
                   if c in df.columns]
    mapping_records: List[Dict[str, Any]] = []
    for col in encode_cols:
        unique_vals = sorted(
            df[col].dropna().unique(),
            key=lambda x: (type(x).__name__, str(x)),
        )
        val_to_int = {v: i + 2 for i, v in enumerate(unique_vals)}
        for orig, enc in val_to_int.items():
            mapping_records.append({"column": col, "original_value": orig, "encoded_value": enc})
        mapping_records.append({"column": col, "original_value": float("nan"), "encoded_value": 1})
        df[col] = df[col].map(val_to_int).fillna(1).astype(int)

    DEMO_INTERMEDIATE_DIR.mkdir(parents=True, exist_ok=True)
    mapping_path = DEMO_INTERMEDIATE_DIR / "demo_encoding_map.csv"
    pd.DataFrame(mapping_records).to_csv(mapping_path, index=False)
    log_print(logger, f"  Saved encoding map ({len(mapping_records)} entries) → {mapping_path}")
    return df


def load_no_push_ids() -> set:
    """Load no-push member IDs."""
    if not NO_PUSH_MEMBERS_PATH.exists():
        return set()
    df = pd.read_csv(NO_PUSH_MEMBERS_PATH, encoding="utf-8-sig")
    return set(df["member_id"].unique())


def load_order_result_full(logger: logging.Logger) -> pd.DataFrame:
    """Load full order_result for spend and order-level features."""
    path = DATA_DIR / "order_result.csv"
    log_print(logger, f"Loading order result from {path}")
    df = pd.read_csv(path, encoding="utf-8-sig")
    df["dt"] = pd.to_datetime(df["create_hour"], errors="coerce")
    df = df.dropna(subset=["dt"])
    df["date"] = df["dt"].dt.date
    df["hour"] = df["dt"].dt.hour
    # Spend = origin - discount
    spend_cols = ["coffee_origin_money", "drink_not_coffee_origin_money", "food_origin_money", "other_origin_money"]
    discount_cols = ["coffee_discount", "drink_not_coffee_discount", "food_discount", "other_discount"]
    df["spend"] = (
        df[[c for c in spend_cols if c in df.columns]].fillna(0).sum(axis=1)
        * df[[c for c in discount_cols if c in df.columns]].fillna(1).sum(axis=1)
    )
    df["total_discount"] = df[[c for c in discount_cols if c in df.columns]].fillna(1).sum(axis=1)
    df["used_coupon"] = (df["use_coupon_num"] > 0).astype(int) if "use_coupon_num" in df.columns else 0
    log_print(logger, f"  Loaded {len(df):,} orders")
    return df


# ---------------------------------------------------------------------------
# Panel construction
# ---------------------------------------------------------------------------


def build_training_panel(
    logger: logging.Logger,
    df_orders: pd.DataFrame,
    closures: pd.DataFrame,
    customer_preference: pd.DataFrame,
    unique_visits: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build (member_id, dept_id, closure_start, period, label) panel.
    period: -4, -3, -2, -1 (pre-closure weeks); 0 for control (evaluation only).
    """
    log_print(logger, "\nBuilding training panel (4-week window)...")
    control_pool = get_never_treated_members(
        closures, customer_preference, DEFAULT_LOWEST_PURCHASES, DEFAULT_LOWEST_RATIO
    )
    df_com_s = build_date_sorted_index(df_orders)
    log_print(logger, f"  Earliest order date in data: {df_orders['date'].min()}")

    # Build a lookup: member_id -> earliest purchase date.
    # Used to enforce that members have purchase history before the earliest
    # pre-closure window (closure_start - 28 days).
    # Ensure dates are converted to pd.Timestamp for uniform comparison.
    df_orders_ts = df_orders.copy()
    df_orders_ts["date"] = pd.to_datetime(df_orders_ts["date"])
    member_first_purchase = df_orders_ts.groupby("member_id")["date"].min()

    rows: List[Dict[str, Any]] = []
    n_closures = len(closures)
    for idx, (_, closure) in enumerate(closures.iterrows()):
        if (idx + 1) % 25 == 0 or idx == 0:
            log_print(logger, f"  Closure {idx + 1}/{n_closures}...")
        dept_id = int(closure["dept_id"])
        closure_start = pd.to_datetime(closure["closure_start"])
        closure_end = pd.to_datetime(closure["closure_end"])
        closure_duration = max(int(closure["closure_duration_days"]), 1)

        treatment = _get_treated_members_for_store(customer_preference, dept_id, DEFAULT_LOWEST_RATIO)
        if not treatment:
            continue
        closure_control = get_closure_specific_control_members(
            unique_visits, control_pool, closure_start.date(), DEFAULT_LOWEST_PURCHASES, DEFAULT_LOWEST_RATIO
        )
        if not closure_control:
            continue

        # Require members to have purchase history before the earliest pre-closure
        # period (closure_start - 28 days).  Members who only started ordering après
        # that cutoff cannot have features computed for period -4.
        earliest_preperiod = closure_start - pd.Timedelta(days=WINDOW_WEEKS * 7)
        def _has_pre_window_history(members: list) -> list:
            return [
                m for m in members
                if m in member_first_purchase.index
                and member_first_purchase[m] < earliest_preperiod
            ]
        treatment = _has_pre_window_history(treatment)
        closure_control = _has_pre_window_history(closure_control)
        if not treatment or not closure_control:
            continue

        for group_label, members in [("treatment", treatment), ("control", closure_control)]:
            for w in range(-WINDOW_WEEKS, 0):  # periods -4, -3, -2, -1
                period_start = (closure_start + pd.Timedelta(days=7 * w)).date()
                period_end = (closure_start + pd.Timedelta(days=7 * w + 6)).date()
                # Label: any purchase in this week?
                pc = _slice_by_date(df_com_s, period_start, period_end)
                pc = pc[pc["member_id"].isin(members)]
                purchasers = set(pc["member_id"].unique()) if not pc.empty else set()
                for mid in members:
                    rows.append({
                        "member_id": mid,
                        "dept_id": dept_id,
                        "closure_start": closure["closure_start"],
                        "closure_end": closure["closure_end"],
                        "closure_length_days": closure_duration,
                        "group": group_label,
                        "period": w,
                        "period_start": period_start,
                        "period_end": period_end,
                        "label": 1 if mid in purchasers else 0,
                        "is_treated": 1 if group_label == "treatment" else 0,
                    })
            # Control: add period 0 for evaluation
            if group_label == "control":
                dur_start = closure_start.date()
                dur_end = closure_end.date()
                pc = _slice_by_date(df_com_s, dur_start, dur_end)
                pc = pc[pc["member_id"].isin(members)]
                purchasers = set(pc["member_id"].unique()) if not pc.empty else set()
                for mid in members:
                    rows.append({
                        "member_id": mid,
                        "dept_id": dept_id,
                        "closure_start": closure["closure_start"],
                        "closure_end": closure["closure_end"],
                        "closure_length_days": closure_duration,
                        "group": group_label,
                        "period": 0,
                        "period_start": dur_start,
                        "period_end": dur_end,
                        "label": 1 if mid in purchasers else 0,
                        "is_treated": 0,
                    })

    panel = pd.DataFrame(rows)
    sample = os.environ.get("DISPLACEMENT_SAMPLE")
    if sample:
        n = int(sample)
        panel = panel.sample(n=min(n, len(panel)), random_state=42)
        log_print(logger, f"  Sampled to {len(panel):,} rows (--sample={n})")
    log_print(logger, f"  Panel: {len(panel):,} rows, {panel['member_id'].nunique():,} unique members")
    log_print(logger, f"  Label distribution: {panel['label'].value_counts().to_dict()}")
    return panel


# ---------------------------------------------------------------------------
# Feature construction
# ---------------------------------------------------------------------------


def _compute_habit_features(dates: pd.Series) -> pd.Series:
    """
    Compute inter-purchase interval and streak features for one member's
    purchase dates.  Called via groupby.apply on deduplicated purchase days.
    """
    dates_sorted = sorted(dates.unique())
    n = len(dates_sorted)
    if n == 0:
        return pd.Series({
            "mean_inter_purchase_interval_days": 0.0,
            "std_inter_purchase_interval_days": 0.0,
            "cv_inter_purchase_interval": 0.0,
            "max_gap_between_purchases": 0.0,
            "longest_consecutive_streak_days": 0,
        })
    if n == 1:
        return pd.Series({
            "mean_inter_purchase_interval_days": 0.0,
            "std_inter_purchase_interval_days": 0.0,
            "cv_inter_purchase_interval": 0.0,
            "max_gap_between_purchases": 0.0,
            "longest_consecutive_streak_days": 1,
        })
    dates_ts = [pd.Timestamp(d) for d in dates_sorted]
    gaps = np.array([(dates_ts[i] - dates_ts[i - 1]).days for i in range(1, n)], dtype=float)
    mean_g = float(gaps.mean())
    std_g = float(gaps.std()) if len(gaps) > 1 else 0.0
    cv_g = std_g / mean_g if mean_g > 0 else 0.0
    max_g = float(gaps.max())
    streak = max_streak = 1
    for g in gaps:
        if g == 1:
            streak += 1
        else:
            max_streak = max(max_streak, streak)
            streak = 1
    max_streak = max(max_streak, streak)
    return pd.Series({
        "mean_inter_purchase_interval_days": mean_g,
        "std_inter_purchase_interval_days": std_g,
        "cv_inter_purchase_interval": cv_g,
        "max_gap_between_purchases": max_g,
        "longest_consecutive_streak_days": max_streak,
    })


def compute_features_for_panel(
    logger: logging.Logger,
    panel: pd.DataFrame,
    df_order_full: pd.DataFrame,
    member_demographics: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compute behavioral and closure-specific features for each panel row.

    Uses a single order-level DataFrame (df_order_full from order_result.csv).
    Demographics (member_demographics) are pre-encoded integers from
    load_member_demographics().  Hour-level and product-name features are
    intentionally excluded.

    Iterates over unique (closure, period) groups for vectorized groupby
    aggregations, then merges the feature table back onto the panel.
    """
    log_print(logger, "\nComputing features (vectorized)...")

    # ------------------------------------------------------------------
    # 0. Canonicalize types
    # ------------------------------------------------------------------
    df_order_full["date"] = pd.to_datetime(df_order_full["date"])

    panel["period_start"] = pd.to_datetime(panel["period_start"])
    panel["_closure_start_dt"] = pd.to_datetime(panel["closure_start"])

    earliest_date = df_order_full["date"].min()  # Timestamp

    # Pre-sort by date for efficient slicing
    df_ord_sorted = df_order_full.sort_values("date").reset_index(drop=True)
    ord_dates_np = df_ord_sorted["date"].values

    # ------------------------------------------------------------------
    # 1. Closure-specific features (straight from panel columns)
    # ------------------------------------------------------------------
    panel["closure_start_month"] = panel["_closure_start_dt"].dt.month
    panel["closure_start_weekday"] = panel["_closure_start_dt"].dt.dayofweek
    panel["closure_start_season"] = (panel["_closure_start_dt"].dt.month % 12 + 3) // 3
    panel["share_visited_stores_closed"] = panel["is_treated"].astype(float)
    panel["tenure_days"] = (panel["period_start"] - earliest_date).dt.days

    # ------------------------------------------------------------------
    # 2. Demographic features – one merge (pre-encoded by load_member_demographics)
    # ------------------------------------------------------------------
    required_demo_cols = ["gender", "level", "has_inviter", "manufacturer", "callphone", "push"]
    missing_demo_src = [c for c in required_demo_cols if c not in member_demographics.columns]
    if missing_demo_src:
        raise ValueError(
            f"member_demographics is missing required columns: {missing_demo_src}. "
            "Ensure load_member_demographics() was called before compute_features_for_panel()."
        )
    demo_cols = ["member_id"] + required_demo_cols

    all_members = panel["member_id"].unique()
    demo_df = (
        pd.DataFrame({"member_id": all_members})
        .merge(member_demographics[demo_cols], on="member_id", how="left")
    )
    missing_members = demo_df[demo_df["gender"].isna()]["member_id"].tolist()
    if missing_members:
        raise ValueError(
            f"{len(missing_members)} panel members are missing from member_result.csv. "
            f"All treatment/control members must have demographic records. "
            f"First 10 missing: {missing_members[:10]}"
        )

    # ------------------------------------------------------------------
    # 3. Behavioral features — one iteration per (closure × period)
    # ------------------------------------------------------------------
    # Group by (dept_id, closure_start, period_start) so each iteration
    # processes the exact treatment/control members for one closure event.
    # No deduplication needed: each group produces one batch row per member
    # uniquely identified by (member_id, dept_id, closure_start, period_start).
    unique_closure_periods = (
        panel[["dept_id", "closure_start", "period_start"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    n_groups = len(unique_closure_periods)
    log_print(
        logger,
        f"  {n_groups} unique (closure, period) groups across "
        f"{panel['member_id'].nunique():,} unique members — iterating by closure × period...",
    )

    behavioral_parts: List[pd.DataFrame] = []

    for i, (_, grp_key) in enumerate(unique_closure_periods.iterrows()):
        if (i + 1) % 50 == 0 or i == 0:
            log_print(
                logger,
                f"  Group {i + 1}/{n_groups}  dept={grp_key['dept_id']}  "
                f"closure={grp_key['closure_start']}  period_start={pd.Timestamp(grp_key['period_start']).date()}",
            )

        ps = pd.Timestamp(grp_key["period_start"])
        members_at_ps = panel.loc[
            (panel["dept_id"] == grp_key["dept_id"])
            & (panel["closure_start"] == grp_key["closure_start"])
            & (panel["period_start"] == ps),
            "member_id",
        ].values
        members_set = set(members_at_ps)

        history_end = ps - pd.Timedelta(days=1)
        history_days_available = (history_end - earliest_date).days

        if history_days_available < 7:
            raise ValueError(
                f"[period_start={ps.date()}] Only {history_days_available}d of history "
                f"available before {ps.date()}. The Aug-2020 closure filter should have "
                "prevented this. Check that closures were filtered to closure_start >= 2020-09-01."
            )

        n_weeks_history = max(history_days_available / 7, 0.01)
        n_weeks_in_history = max(int(history_days_available / 7), 1)

        # Efficient binary-search slice (no Python loop over rows)
        hi_ord = int(np.searchsorted(ord_dates_np, history_end.to_datetime64(), side="right"))
        hist_ord = df_ord_sorted.iloc[:hi_ord]
        hist_ord = hist_ord[hist_ord["member_id"].isin(members_set)]

        # Cutoffs for rolling windows (defined regardless of empty frames)
        cutoff_4w = history_end - pd.Timedelta(days=28)
        cutoff_2w = history_end - pd.Timedelta(days=14)
        cutoff_1w = history_end - pd.Timedelta(days=7)

        # ---- Structural invariant check ----------------------------------
        # All panel members must have order history before period_start.
        # If hist_ord is empty, the treatment/control filter has a bug.
        if hist_ord.empty:
            raise ValueError(
                f"[period_start={ps.date()}] No order history found for any of "
                f"{len(members_at_ps)} panel members before {history_end.date()}. "
                "Check that treatment/control members satisfy the pre-closure "
                f"purchase requirement (≥{DEFAULT_LOWEST_PURCHASES} purchases)."
            )

        # Start with a DataFrame keyed by (member_id, closure context)
        batch = pd.DataFrame({
            "member_id": members_at_ps,
            "dept_id": grp_key["dept_id"],
            "closure_start": grp_key["closure_start"],
            "period_start": ps,
        })

        # ---- Purchase frequency & recency --------------------------------
        pur_days = hist_ord.drop_duplicates(["member_id", "date"])

        pur_all = pur_days.groupby("member_id").size().rename("total_purchase_days_pre")
        last_pur = pur_days.groupby("member_id")["date"].max().rename("_last_purchase")
        pur_4w = pur_days[pur_days["date"] >= cutoff_4w].groupby("member_id").size().rename("_pur4w")
        pur_2w = pur_days[pur_days["date"] >= cutoff_2w].groupby("member_id").size().rename("_pur2w")
        pur_1w = pur_days[pur_days["date"] >= cutoff_1w].groupby("member_id").size().rename("_pur1w")

        batch = batch.merge(pur_all, on="member_id", how="left")
        batch = batch.merge(last_pur, on="member_id", how="left")
        batch = batch.merge(pur_4w, on="member_id", how="left")
        batch = batch.merge(pur_2w, on="member_id", how="left")
        batch = batch.merge(pur_1w, on="member_id", how="left")

        # Structural check: every member must appear in purchase history.
        missing_hist = batch[batch["total_purchase_days_pre"].isna()]["member_id"].tolist()
        if missing_hist:
            raise ValueError(
                f"[period_start={ps.date()}] {len(missing_hist)} members have no purchase "
                f"history before {history_end.date()} but appear in panel. "
                f"First 10: {missing_hist[:10]}. "
                "All panel members must have purchase records dating from before the "
                "closure's earliest pre-period. Check that the Aug-2020 closure filter "
                "and the treatment/control eligibility criteria are enforced."
            )
        batch["total_purchase_days_pre"] = batch["total_purchase_days_pre"].astype(int)

        # Structural check: last purchase must be computable
        missing_lp = batch[batch["_last_purchase"].isna()]["member_id"].tolist()
        if missing_lp:
            raise ValueError(
                f"[period_start={ps.date()}] {len(missing_lp)} members have NaT last_purchase. "
                f"First 10: {missing_lp[:10]}"
            )

        # Rolling window counts: fillna(0) is correct — member has all-time history
        # but may have zero purchases within the rolling window.
        for col in ["_pur4w", "_pur2w", "_pur1w"]:
            batch[col] = batch[col].fillna(0).astype(int)

        batch["purchases_per_week_all_pre"] = batch["total_purchase_days_pre"] / n_weeks_history
        batch["purchases_per_week_last_4w"] = batch["_pur4w"] / 4.0
        batch["purchases_per_week_last_2w"] = batch["_pur2w"] / 2.0
        batch["purchases_per_week_last_1w"] = batch["_pur1w"] / 1.0

        batch["days_since_last_purchase"] = (ps - batch["_last_purchase"]).dt.days.astype(int)
        batch["purchased_in_last_7_days"] = (batch["days_since_last_purchase"] <= 7).astype(int)
        batch["purchased_in_last_14_days"] = (batch["days_since_last_purchase"] <= 14).astype(int)

        # ---- Order counts & spend ----------------------------------------
        # order_id and spend are required columns in order_result
        for req_col in ["order_id", "spend"]:
            if req_col not in hist_ord.columns:
                raise ValueError(
                    f"order_result.csv is missing required column '{req_col}'. "
                    "Cannot compute order-level features."
                )
        if hist_ord.empty:
            raise ValueError(
                f"[period_start={ps.date()}] No order history found for any of "
                f"{len(members_at_ps)} panel members before {history_end.date()}. "
                "All panel members must have order records matching their commodity purchases."
            )
        ord_g = hist_ord.groupby("member_id")
        ord_counts = ord_g["order_id"].nunique().rename("total_orders_pre")
        spend_all = ord_g["spend"].sum().rename("total_spend_pre")
        # Rolling window spend: fillna(0) is correct (no orders in window = 0 spend)
        spend_4w = hist_ord[hist_ord["date"] >= cutoff_4w].groupby("member_id")["spend"].sum().rename("total_spend_last_4w")
        spend_2w = hist_ord[hist_ord["date"] >= cutoff_2w].groupby("member_id")["spend"].sum().rename("total_spend_last_2w")
        batch = batch.merge(ord_counts, on="member_id", how="left")
        batch = batch.merge(spend_all, on="member_id", how="left")
        batch = batch.merge(spend_4w, on="member_id", how="left")
        batch = batch.merge(spend_2w, on="member_id", how="left")
        # Structural check: every member must have at least one order record
        missing_ord = batch[batch["total_orders_pre"].isna()]["member_id"].tolist()
        if missing_ord:
            raise ValueError(
                f"[period_start={ps.date()}] {len(missing_ord)} members have purchase history "
                f"in commodity data but no records in order_result.csv. "
                f"First 10: {missing_ord[:10]}. "
                "Check join key consistency between order_commodity and order_result."
            )
        batch["total_orders_pre"] = batch["total_orders_pre"].astype(int)
        batch["total_spend_pre"] = batch["total_spend_pre"].astype(float)
        # Rolling window spend: 0 is correct when no orders fall in the window
        batch["total_spend_last_4w"] = batch["total_spend_last_4w"].fillna(0.0)
        batch["total_spend_last_2w"] = batch["total_spend_last_2w"].fillna(0.0)

        # ---- Habit / regularity ------------------------------------------
        pur_days_for_habit = hist_ord.drop_duplicates(["member_id", "date"])
        habit_feats = (
            pur_days_for_habit
            .groupby("member_id")["date"]
            .apply(_compute_habit_features)
            .unstack(level=1)   # pandas 2.x returns MultiIndex Series; unstack → DataFrame
            .reset_index()      # member_id becomes a regular column for merging
        )
        # week participation
        hc2 = hist_ord.copy()
        hc2["_week_idx"] = ((hc2["date"] - earliest_date).dt.days // 7)
        weeks_with_pur = hc2.groupby("member_id")["_week_idx"].nunique().rename("_n_weeks_pur")

        batch = batch.merge(habit_feats, on="member_id", how="left")
        batch = batch.merge(weeks_with_pur, on="member_id", how="left")

        # Structural check: habit features must be present for all members in hist_ord
        missing_habit = batch[batch["mean_inter_purchase_interval_days"].isna()]["member_id"].tolist()
        if missing_habit:
            raise ValueError(
                f"[period_start={ps.date()}] {len(missing_habit)} members are missing habit "
                f"features after groupby.apply(_compute_habit_features). "
                f"First 10: {missing_habit[:10]}. "
                "Check that hist_ord contains these members."
            )
        batch["longest_consecutive_streak_days"] = batch["longest_consecutive_streak_days"].astype(int)
        missing_nwp = batch[batch["_n_weeks_pur"].isna()]["member_id"].tolist()
        if missing_nwp:
            raise ValueError(
                f"[period_start={ps.date()}] {len(missing_nwp)} members missing weeks_with_purchase. "
                f"First 10: {missing_nwp[:10]}"
            )
        batch["share_weeks_with_purchase"] = batch["_n_weeks_pur"] / n_weeks_in_history

        # ---- Day-of-week --------------------------------------------------
        hc_dow = hist_ord.copy()
        hc_dow["_dow"] = hc_dow["date"].dt.dayofweek
        dow_total = hc_dow.groupby("member_id").size().rename("_dow_total")
        dow_pivot = (
            hc_dow.groupby(["member_id", "_dow"])
            .size()
            .unstack(fill_value=0)
            .reindex(columns=range(7), fill_value=0)
        )
        dow_pivot.columns = [f"_dow_cnt_{d}" for d in range(7)]
        dow_modal = (
            hc_dow.groupby(["member_id", "_dow"])
            .size()
            .groupby(level=0)
            .idxmax()
            .apply(lambda x: x[1])
            .rename("modal_purchase_dow")
        )
        batch = batch.merge(dow_total, on="member_id", how="left")
        batch = batch.merge(dow_pivot, on="member_id", how="left")
        batch = batch.merge(dow_modal, on="member_id", how="left")
        # Structural check: all members must have DoW data (hist_ord is non-empty)
        missing_dow = batch[batch["_dow_total"].isna()]["member_id"].tolist()
        if missing_dow:
            raise ValueError(
                f"[period_start={ps.date()}] {len(missing_dow)} members missing DoW totals. "
                f"First 10: {missing_dow[:10]}"
            )
        for d in range(7):
            batch[f"share_purchases_dow{d}"] = (
                batch[f"_dow_cnt_{d}"] / batch["_dow_total"]
            )
        batch["modal_purchase_dow"] = batch["modal_purchase_dow"].astype(int)
        # entropy
        dow_share_cols = [f"share_purchases_dow{d}" for d in range(7)]
        probs_matrix = batch[dow_share_cols].values.clip(0)
        batch["entropy_dow"] = -(probs_matrix * np.log(probs_matrix + 1e-10)).sum(axis=1)

        # ---- Basket size & category breadth -----------------------------
        basket_num_cols = [c for c in [
            "coffee_commodity_num", "not_coffee_commodity_num",
            "food_commodity_num", "other_not_coffee_commodity_num",
        ] if c in hist_ord.columns]
        if not basket_num_cols:
            raise ValueError(
                "order_result.csv is missing all commodity count columns "
                "(coffee_commodity_num, not_coffee_commodity_num, etc.)."
            )
        for req_col in ["order_id", "dept_id"]:
            if req_col not in hist_ord.columns:
                raise ValueError(
                    f"order_result.csv is missing required column '{req_col}'."
                )

        hist_ord_basket = hist_ord.copy()
        # Total items per order (sum of category item counts)
        hist_ord_basket["_total_items"] = hist_ord_basket[basket_num_cols].fillna(0).sum(axis=1)
        # Number of distinct product categories ordered (> 0) per order
        hist_ord_basket["_n_categories"] = (hist_ord_basket[basket_num_cols].fillna(0) > 0).sum(axis=1)

        com_orders = hist_ord.groupby("member_id").size().rename("_com_orders")
        avg_basket = hist_ord_basket.groupby("member_id")["_total_items"].mean().rename("avg_basket_size")
        avg_categories = hist_ord_basket.groupby("member_id")["_n_categories"].mean().rename("n_order_categories_avg")
        batch = batch.merge(com_orders, on="member_id", how="left")
        batch = batch.merge(avg_basket, on="member_id", how="left")
        batch = batch.merge(avg_categories, on="member_id", how="left")

        missing_basket = batch[batch["avg_basket_size"].isna()]["member_id"].tolist()
        if missing_basket:
            raise ValueError(
                f"[period_start={ps.date()}] {len(missing_basket)} members missing basket features. "
                f"First 10: {missing_basket[:10]}"
            )

        # Use visit-level deduplication (one row per member-date-store combination)
        hist_ord_visits = hist_ord.drop_duplicates(["member_id", "date", "dept_id"])
        store_counts = (
            hist_ord_visits.groupby(["member_id", "dept_id"])
            .size()
            .unstack(fill_value=0)
        )
        uniq_stores = (store_counts > 0).sum(axis=1).rename("unique_stores_pre")
        pref_ratio = store_counts.apply(
            lambda r: r.sort_values(ascending=False).iloc[0] / r.sum(), axis=1
        ).rename("preferred_store_ratio")
        # sec_store_ratio is 0 when member uses only one store (legitimate 0, not missing)
        sec_ratio = store_counts.apply(
            lambda r: r.sort_values(ascending=False).iloc[1] / r.sum()
            if (r > 0).sum() > 1 else 0.0,
            axis=1,
        ).rename("second_store_ratio")
        batch = batch.merge(uniq_stores, on="member_id", how="left")
        batch = batch.merge(pref_ratio, on="member_id", how="left")
        batch = batch.merge(sec_ratio, on="member_id", how="left")

        missing_store = batch[batch["unique_stores_pre"].isna()]["member_id"].tolist()
        if missing_store:
            raise ValueError(
                f"[period_start={ps.date()}] {len(missing_store)} members missing store features. "
                f"First 10: {missing_store[:10]}"
            )
        batch["unique_stores_pre"] = batch["unique_stores_pre"].astype(int)

        # ---- Order-level aggregates --------------------------------------
        ord_scalar_cols = {
            "avg_discount_per_order": ("total_discount", "mean"),
            "coupon_usage_rate": ("used_coupon", "mean"),
            "avg_coffee_num": ("coffee_commodity_num", "mean"),
            "avg_food_num": ("food_commodity_num", "mean"),
            "avg_use_coffee_wallet": ("use_coffee_wallet_num", "mean"),
        }
        for feat, (src_col, _) in ord_scalar_cols.items():
            if src_col not in hist_ord.columns:
                raise ValueError(
                    f"order_result.csv is missing required column '{src_col}' "
                    f"needed to compute feature '{feat}'."
                )
        agg_spec = {
            feat: pd.NamedAgg(column=src_col, aggfunc=agg_fn)
            for feat, (src_col, agg_fn) in ord_scalar_cols.items()
        }
        ord_agg = hist_ord.groupby("member_id").agg(**agg_spec)
        batch = batch.merge(ord_agg, on="member_id", how="left")

        # avg_delivery_pay: NaN means the member ordered only via pickup / in-store,
        # i.e., no delivery fee charged. This is a legitimate 0, not missing data.
        if "delivery_pay_money" not in hist_ord.columns:
            raise ValueError("order_result.csv is missing required column 'delivery_pay_money'.")
        avg_delivery = (
            hist_ord["delivery_pay_money"]
            .fillna(0)                          # NaN = no delivery fee
            .groupby(hist_ord["member_id"])
            .mean()
            .rename("avg_delivery_pay")
        )
        batch = batch.merge(avg_delivery, on="member_id", how="left")
        missing_ord_agg = batch[batch["avg_discount_per_order"].isna()]["member_id"].tolist()
        if missing_ord_agg:
            raise ValueError(
                f"[period_start={ps.date()}] {len(missing_ord_agg)} members missing order aggregates. "
                f"First 10: {missing_ord_agg[:10]}"
            )

        if "coffee_commodity_num" not in hist_ord.columns:
            raise ValueError("order_result.csv is missing required column 'coffee_commodity_num'.")
        cof_share = (
            hist_ord["coffee_commodity_num"]
            .gt(0)
            .groupby(hist_ord["member_id"])
            .mean()
            .rename("coffee_share_orders")
        )
        batch = batch.merge(cof_share, on="member_id", how="left")

        if "take_address" not in hist_ord.columns:
            raise ValueError("order_result.csv is missing required column 'take_address'.")
        ta_rate = (
            hist_ord["take_address"]
            .notna()
            .astype(int)
            .groupby(hist_ord["member_id"])
            .mean()
            .rename("take_address_rate")
        )
        batch = batch.merge(ta_rate, on="member_id", how="left")

        # Drop internal helper columns
        batch.drop(
            columns=[c for c in batch.columns if c.startswith("_")],
            inplace=True, errors="ignore",
        )
        behavioral_parts.append(batch)

    log_print(logger, "  Merging behavioral features back onto panel...")
    if not behavioral_parts:
        raise ValueError(
            "No closure-period groups produced features. Check that closures are "
            "filtered to closure_start >= 2020-09-01."
        )
    behavioral_df = pd.concat(behavioral_parts, ignore_index=True)

    # Merge on full closure context.
    merge_keys = ["member_id", "dept_id", "closure_start", "period_start"]
    result = panel.merge(behavioral_df, on=merge_keys, how="left")
    n_unmatched = result[result["total_purchase_days_pre"].isna()].shape[0]
    if n_unmatched > 0:
        raise ValueError(
            f"{n_unmatched:,} panel rows could not be matched to behavioral features "
            "after merge. Check that all (dept_id, closure_start, period_start) groups "
            "were processed without gaps."
        )
    result = result.merge(demo_df, on="member_id", how="left")
    result.drop(columns=["_closure_start_dt"], inplace=True, errors="ignore")

    # ------------------------------------------------------------------
    # Final validation: no NaN allowed in any feature column
    # ------------------------------------------------------------------
    exclude = {"member_id", "dept_id", "closure_start", "closure_end",
               "period", "group", "label", "is_treated", "period_end"}
    feature_cols_final = [c for c in result.columns if c not in exclude]
    nan_summary = result[feature_cols_final].isna().sum()
    nan_cols = nan_summary[nan_summary > 0]
    if not nan_cols.empty:
        details = "\n".join(f"  {col}: {count} NaN" for col, count in nan_cols.items())
        raise ValueError(
            f"NaN values found in feature matrix after all joins — indicates a data "
            f"processing bug. Affected columns:\n{details}\n"
            "Fix the upstream data issue; do not paper over with fillna."
        )

    log_print(logger, f"  Done. Feature matrix: {result.shape[0]:,} rows × {result.shape[1]:,} columns")
    return result

# ---------------------------------------------------------------------------
# Statistics and training
# ---------------------------------------------------------------------------


def print_variable_statistics(logger: logging.Logger, df: pd.DataFrame, feature_cols: List[str]) -> None:
    """Print mean, min, max for each variable."""
    log_print(logger, "\n" + "=" * 80)
    log_print(logger, "Variable Statistics (mean, min, max)")
    log_print(logger, "=" * 80)
    for col in feature_cols:
        if col not in df.columns:
            continue
        s = df[col]
        if pd.api.types.is_numeric_dtype(s):
            valid = s.dropna()
            if len(valid) > 0:
                log_print(logger, f"  {col}: mean={valid.mean():.4f}, min={valid.min():.4f}, max={valid.max():.4f}")
            else:
                log_print(logger, f"  {col}: (all NaN)")
        else:
            log_print(logger, f"  {col}: categorical, n_unique={s.nunique()}")


def check_gpu() -> bool:
    """Check if GPU is available for XGBoost."""
    try:
        import xgboost as xgb
        # Try to create a small GPU model
        dtrain = xgb.DMatrix(np.array([[1, 2], [3, 4]]), label=[0, 1])
        params = {"tree_method": "hist", "device": "cuda"}
        xgb.train(params, dtrain, num_boost_round=1)
        return True
    except Exception:
        return False


def main(max_closures: Optional[int] = None, tail_closures: Optional[int] = None) -> None:
    logger = setup_logging()
    log_print(logger, "=" * 80)
    log_print(logger, "Displacement Classification Model Training")
    log_print(logger, f"Started at {datetime.now().isoformat()}")
    log_print(logger, "=" * 80)

    # Load data
    df_order_full = load_order_result_full(logger)
    closures = pd.read_csv(CLOSURES_CSV, encoding="utf-8-sig")
    # Retain only closures where all 4 pre-closure weeks fall after the earliest
    # order date (2020-06-01).  Period -4 starts at closure_start - 28 days,
    # so we require closure_start >= 2020-09-01 (ensuring >=4 weeks of Aug data).
    closures["closure_start_dt"] = pd.to_datetime(closures["closure_start"])
    closures = (
        closures[closures["closure_start_dt"] >= pd.Timestamp("2020-09-01")]
        .drop(columns=["closure_start_dt"])
        .reset_index(drop=True)
    )
    log_print(logger, f"  Closures after Aug-2020 filter: {len(closures)}")
    if closures.empty:
        raise ValueError("No closures remain after Aug-2020 filter.")
    if tail_closures is not None:
        closures = closures.tail(tail_closures).reset_index(drop=True)
        log_print(logger, f"  [DEBUG] Using last {len(closures)} closure(s) (tail)")
    elif max_closures is not None:
        closures = closures.head(max_closures).reset_index(drop=True)
        log_print(logger, f"  [DEBUG] Limiting to {len(closures)} closure(s) for testing")
    no_push_ids = load_no_push_ids()
    log_print(logger, f"Loaded {len(no_push_ids):,} no-push members")
    member_demographics = load_member_demographics(logger, no_push_ids)

    customer_preference = get_customer_store_preference(df_order_full, lowest_purchases=DEFAULT_LOWEST_PURCHASES)

    # unique_visits must be built from the FULL df_order_full here so that
    # get_closure_specific_control_members can correctly assess pre-closure
    # visit counts for control candidates before any filtering takes place.
    unique_visits = df_order_full[["member_id", "date", "dept_id"]].drop_duplicates()

    # --- Pre-filter: retain only members who actually appear in treatment or
    # control for at least one closure event (exact membership, not the full pool).
    log_print(logger, "\nPre-filtering data to exact panel members across all closures...")
    all_treated_members: set = set()
    all_control_members: set = set()
    never_treated_pool = get_never_treated_members(
        closures, customer_preference, DEFAULT_LOWEST_PURCHASES, DEFAULT_LOWEST_RATIO
    )
    for _, closure in closures.iterrows():
        treated = _get_treated_members_for_store(
            customer_preference, int(closure["dept_id"]), DEFAULT_LOWEST_RATIO
        )
        all_treated_members.update(treated)
        ctrl = get_closure_specific_control_members(
            unique_visits, never_treated_pool,
            pd.to_datetime(closure["closure_start"]).date(),
            DEFAULT_LOWEST_PURCHASES, DEFAULT_LOWEST_RATIO,
        )
        all_control_members.update(ctrl)

    panel_members = all_treated_members | all_control_members
    log_print(logger, f"  Treatment members (union):  {len(all_treated_members):,}")
    log_print(logger, f"  Control members (union):    {len(all_control_members):,}")
    log_print(logger, f"  Total panel members:        {len(panel_members):,}")

    n_ord_before = len(df_order_full)
    df_order_full = df_order_full[df_order_full["member_id"].isin(panel_members)].copy()
    log_print(logger, f"  df_order_full: {n_ord_before:,} → {len(df_order_full):,} rows")

    # Build panel
    panel = build_training_panel(
        logger, df_order_full, closures, customer_preference, unique_visits,
    )

    # Compute features
    features_df = compute_features_for_panel(
        logger, panel, df_order_full, member_demographics,
    )

    # Feature columns: exclude identifiers, label, and all closure-specific columns.
    # Closure-specific features (closure_length_days, closure_start_month, etc.) describe
    # the closure event, not the consumer's pre-closure behaviour. Consumers cannot
    # anticipate an upcoming closure, so these features carry no causal information
    # about the consumer's purchase propensity before the closure.  They belong in the
    # DiD regression (Step 4), not in the displacement classifier.
    exclude = {
        # --- identifiers / bookkeeping ---
        "member_id", "dept_id", "closure_start", "closure_end",
        "period", "group", "label", "is_treated", "period_start", "period_end",
        # --- closure-event features (not available to consumers pre-closure) ---
        "closure_length_days", "closure_start_month", "closure_start_weekday",
        "closure_start_season", "share_visited_stores_closed", "tenure_days",
    }
    feature_cols = [c for c in features_df.columns if c not in exclude and pd.api.types.is_numeric_dtype(features_df[c])]

    # Print variable statistics
    print_variable_statistics(logger, features_df, feature_cols)

    # Dataset statistics
    log_print(logger, "\n" + "=" * 80)
    log_print(logger, "Selected Data Statistics")
    log_print(logger, "=" * 80)
    train_df = features_df[features_df["period"] != 0]  # Exclude control period 0 from training
    eval_pre = features_df[(features_df["period"] == -1)]
    eval_during = features_df[(features_df["period"] == 0) & (features_df["group"] == "control")]

    log_print(logger, f"  Training observations: {len(train_df):,}")
    log_print(logger, f"  Treatment Pre (t=-1) eval: {len(eval_pre[eval_pre['group']=='treatment']):,}")
    log_print(logger, f"  Control Pre (t=-1) eval: {len(eval_pre[eval_pre['group']=='control']):,}")
    log_print(logger, f"  Control During (t=0) eval: {len(eval_during):,}")
    log_print(logger, f"  Label rate (train): {train_df['label'].mean():.4f}")

    # Prepare X, y
    # Note: no fillna() here — compute_features_for_panel raises on any NaN,
    # so the feature matrix is guaranteed to be NaN-free at this point.
    X_train = train_df[feature_cols].copy()
    y_train = train_df["label"].values

    # Encode manufacturer if present
    if "manufacturer" in features_df.columns and "manufacturer" not in exclude:
        # Add manufacturer as one-hot if needed
        pass  # Simplified: skip for now

    # Check GPU and train
    use_gpu = check_gpu()
    log_print(logger, f"\nGPU available: {use_gpu}")

    try:
        import xgboost as xgb
        params = {
            "max_depth": 6,
            "eta": 0.1,
            "objective": "binary:logistic",
            "eval_metric": "auc",
            "tree_method": "hist",
            "device": "cuda" if use_gpu else "cpu",
            "n_jobs": -1 if not use_gpu else 1,
        }
        dtrain = xgb.DMatrix(X_train, label=y_train, feature_names=feature_cols)
        model = xgb.train(params, dtrain, num_boost_round=500)

        # Variable importance
        imp = model.get_score(importance_type="gain")
        imp_df = pd.DataFrame([{"feature": k, "importance": v} for k, v in imp.items()])
        imp_df = imp_df.sort_values("importance", ascending=False).reset_index(drop=True)
        imp_df["rank"] = imp_df.index + 1

        log_print(logger, "\n" + "=" * 80)
        log_print(logger, "Variable Importance Ranking (top 30)")
        log_print(logger, "=" * 80)
        for _, r in imp_df.head(30).iterrows():
            log_print(logger, f"  {r['rank']:3d}. {r['feature']}: {r['importance']:.2f}")

        imp_df.to_csv(OUTPUT_DIR / "variable_importance.csv", index=False)
        log_print(logger, f"\nSaved variable_importance.csv to {OUTPUT_DIR}")

        # Evaluation
        def eval_metrics(y_true, y_pred_proba, threshold=0.5):
            y_pred = (y_pred_proba >= threshold).astype(int)
            tp = ((y_true == 1) & (y_pred == 1)).sum()
            tn = ((y_true == 0) & (y_pred == 0)).sum()
            fp = ((y_true == 0) & (y_pred == 1)).sum()
            fn = ((y_true == 1) & (y_pred == 0)).sum()
            acc = (tp + tn) / len(y_true) if len(y_true) > 0 else 0
            prec = tp / (tp + fp) if (tp + fp) > 0 else 0
            rec = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0
            fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
            fnr = fn / (fn + tp) if (fn + tp) > 0 else 0
            return {"accuracy": acc, "precision": prec, "recall": rec, "f1": f1, "fpr": fpr, "fnr": fnr, "n": len(y_true)}

        results = []
        for name, sub in [
            ("Treatment_Pre_t-1", eval_pre[eval_pre["group"] == "treatment"]),
            ("Control_Pre_t-1", eval_pre[eval_pre["group"] == "control"]),
            ("Control_During_t0", eval_during),
        ]:
            if sub.empty:
                continue
            X = sub[feature_cols].copy()
            d = xgb.DMatrix(X, feature_names=feature_cols)
            pred = model.predict(d)
            m = eval_metrics(sub["label"].values, pred)
            m["group"] = name
            results.append(m)

        log_print(logger, "\n" + "=" * 80)
        log_print(logger, "Prediction Accuracy Table")
        log_print(logger, "=" * 80)
        res_df = pd.DataFrame(results)
        log_print(logger, res_df.to_string(index=False))
        res_df.to_csv(OUTPUT_DIR / "prediction_accuracy.csv", index=False)
        log_print(logger, f"\nSaved prediction_accuracy.csv to {OUTPUT_DIR}")

    except ImportError:
        log_print(logger, "XGBoost not installed. Install with: pip install xgboost")
    except Exception as e:
        log_print(logger, f"Training error: {e}", level="error")
        raise

    log_print(logger, "\n" + "=" * 80)
    log_print(logger, f"Completed at {datetime.now().isoformat()}")
    log_print(logger, "=" * 80)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", type=int, default=None, help="Limit panel rows for quick test (e.g. 10000)")
    parser.add_argument("--max-closures", type=int, default=None, help="Limit number of closures processed (e.g. 1 for quick test)")
    parser.add_argument("--tail-closures", type=int, default=None, help="Use last N closures from store_closures.csv (e.g. 20)")
    args = parser.parse_args()
    if args.sample:
        os.environ["DISPLACEMENT_SAMPLE"] = str(args.sample)
    main(max_closures=args.max_closures, tail_closures=args.tail_closures)
