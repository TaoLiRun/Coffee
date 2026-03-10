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
    load_order_commodity_data,
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


def load_member_demographics(logger: logging.Logger) -> pd.DataFrame:
    """Load member_result.csv for demographics."""
    log_print(logger, f"Loading member demographics from {MEMBER_RESULT_PATH}")
    df = pd.read_csv(MEMBER_RESULT_PATH, encoding="utf-8-sig")
    want = ["member_id", "gender", "birth_year", "level", "inviter_id", "manufacturer", "callphone", "camera", "location", "network", "push", "sdcard"]
    cols = [c for c in want if c in df.columns]
    df = df[cols]
    log_print(logger, f"  Loaded {len(df):,} members")
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
        - df[[c for c in discount_cols if c in df.columns]].fillna(0).sum(axis=1)
    )
    df["total_discount"] = df[[c for c in discount_cols if c in df.columns]].fillna(0).sum(axis=1)
    df["used_coupon"] = (df["use_coupon_num"] > 0).astype(int) if "use_coupon_num" in df.columns else 0
    log_print(logger, f"  Loaded {len(df):,} orders")
    return df


# ---------------------------------------------------------------------------
# Panel construction
# ---------------------------------------------------------------------------


def build_training_panel(
    logger: logging.Logger,
    df_commodity: pd.DataFrame,
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
    df_com_s = build_date_sorted_index(df_commodity)

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
                        "closure_duration_days": closure_duration,
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
                        "closure_duration_days": closure_duration,
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


def compute_features_for_panel(
    logger: logging.Logger,
    panel: pd.DataFrame,
    df_commodity: pd.DataFrame,
    df_order_full: pd.DataFrame,
    member_demographics: pd.DataFrame,
    no_push_ids: set,
) -> pd.DataFrame:
    """Compute 65+ features for each panel row."""
    log_print(logger, "\nComputing features...")
    df_com_s = build_date_sorted_index(df_commodity)
    df_ord_s = build_date_sorted_index(df_order_full)
    earliest_date = df_commodity["date"].min()

    feature_rows: List[Dict[str, Any]] = []
    n_rows = len(panel)
    for idx, row in panel.iterrows():
        if (idx + 1) % 1000 == 0 or idx == 0:
            log_print(logger, f"  Row {idx + 1}/{n_rows}...")
        mid = row["member_id"]
        period_start = row["period_start"]
        closure_start = pd.to_datetime(row["closure_start"]).date()
        closure_duration = row["closure_duration_days"]
        is_treated = row["is_treated"]

        history_end = (pd.Timestamp(period_start) - pd.Timedelta(days=1)).date()
        if history_end < earliest_date:
            history_end = earliest_date
        hist_com = _slice_by_date(df_com_s, earliest_date, history_end)
        hist_com = hist_com[hist_com["member_id"] == mid]
        hist_ord = _slice_by_date(df_ord_s, earliest_date, history_end)
        hist_ord = hist_ord[hist_ord["member_id"] == mid]

        feats: Dict[str, Any] = {"member_id": mid, "dept_id": row["dept_id"], "closure_start": row["closure_start"], "period": row["period"], "group": row["group"], "label": row["label"], "is_treated": is_treated}

        # Purchase frequency & recency
        purchase_dates = hist_com[["date"]].drop_duplicates()["date"].sort_values()
        n_purchase_days = len(purchase_dates)
        n_weeks_history = max((history_end - earliest_date).days / 7, 0.01)
        feats["purchases_per_week_all_pre"] = n_purchase_days / n_weeks_history

        cutoff_4w = (pd.Timestamp(period_start) - pd.Timedelta(days=28)).date()
        cutoff_2w = (pd.Timestamp(period_start) - pd.Timedelta(days=14)).date()
        cutoff_1w = (pd.Timestamp(period_start) - pd.Timedelta(days=7)).date()
        feats["purchases_per_week_last_4w"] = len(purchase_dates[purchase_dates >= cutoff_4w]) / 4 if len(purchase_dates) else 0
        feats["purchases_per_week_last_2w"] = len(purchase_dates[purchase_dates >= cutoff_2w]) / 2 if len(purchase_dates) else 0
        feats["purchases_per_week_last_1w"] = len(purchase_dates[purchase_dates >= cutoff_1w]) / 1 if len(purchase_dates) else 0

        if len(purchase_dates) > 0:
            last_date = purchase_dates.iloc[-1]
            feats["days_since_last_purchase"] = (period_start - last_date).days
        else:
            feats["days_since_last_purchase"] = 999

        feats["purchased_in_last_7_days"] = 1 if feats["days_since_last_purchase"] <= 7 else 0
        feats["purchased_in_last_14_days"] = 1 if feats["days_since_last_purchase"] <= 14 else 0
        feats["total_purchase_days_pre"] = n_purchase_days
        feats["total_orders_pre"] = hist_ord["order_id"].nunique() if not hist_ord.empty else 0
        feats["total_spend_pre"] = hist_ord["spend"].sum() if not hist_ord.empty else 0
        feats["total_spend_last_4w"] = hist_ord[hist_ord["date"] >= cutoff_4w]["spend"].sum() if not hist_ord.empty else 0
        feats["total_spend_last_2w"] = hist_ord[hist_ord["date"] >= cutoff_2w]["spend"].sum() if not hist_ord.empty else 0

        # Regularity & habit
        if len(purchase_dates) >= 2:
            gaps = purchase_dates.diff().dropna().dt.days
            feats["mean_inter_purchase_interval_days"] = float(gaps.mean())
            feats["std_inter_purchase_interval_days"] = float(gaps.std()) if len(gaps) > 1 else 0
            feats["cv_inter_purchase_interval"] = feats["std_inter_purchase_interval_days"] / feats["mean_inter_purchase_interval_days"] if feats["mean_inter_purchase_interval_days"] > 0 else 0
            feats["max_gap_between_purchases"] = float(gaps.max())
        else:
            feats["mean_inter_purchase_interval_days"] = 0
            feats["std_inter_purchase_interval_days"] = 0
            feats["cv_inter_purchase_interval"] = 0
            feats["max_gap_between_purchases"] = 0

        # Consecutive streak
        if len(purchase_dates) > 0:
            dates_sorted = sorted(purchase_dates.unique())
            streak = 1
            max_streak = 1
            for i in range(1, len(dates_sorted)):
                if (pd.Timestamp(dates_sorted[i]) - pd.Timestamp(dates_sorted[i - 1])).days == 1:
                    streak += 1
                else:
                    max_streak = max(max_streak, streak)
                    streak = 1
            feats["longest_consecutive_streak_days"] = max(max_streak, streak)
        else:
            feats["longest_consecutive_streak_days"] = 0

        n_weeks_in_history = max(int((pd.Timestamp(history_end) - pd.Timestamp(earliest_date)).days / 7), 1)
        week_idx = hist_com["date"].apply(lambda d: (pd.Timestamp(d) - pd.Timestamp(earliest_date)).days // 7)
        n_weeks_with_purchase = week_idx.nunique()
        feats["share_weeks_with_purchase"] = n_weeks_with_purchase / n_weeks_in_history if n_weeks_in_history else 0

        # Temporal (dow)
        if not hist_com.empty:
            hist_com = hist_com.copy()
            hist_com["dow"] = pd.to_datetime(hist_com["date"]).dt.dayofweek
            dow_counts = hist_com.groupby("dow").size()
            total = dow_counts.sum()
            for d in range(7):
                feats[f"share_purchases_dow{d}"] = dow_counts.get(d, 0) / total if total > 0 else 0
            feats["modal_purchase_dow"] = int(dow_counts.idxmax()) if len(dow_counts) else 0
            probs = dow_counts / total if total > 0 else np.ones(7) / 7
            feats["entropy_dow"] = -float((probs * np.log(probs + 1e-10)).sum())
        else:
            for d in range(7):
                feats[f"share_purchases_dow{d}"] = 0
            feats["modal_purchase_dow"] = 0
            feats["entropy_dow"] = 0

        # Temporal (tod)
        if not hist_ord.empty:
            if "hour" not in hist_ord.columns and "dt" in hist_ord.columns:
                hist_ord = hist_ord.copy()
                hist_ord["hour"] = pd.to_datetime(hist_ord["dt"]).dt.hour
            hour_col = hist_ord["hour"] if "hour" in hist_ord.columns else pd.Series([12] * len(hist_ord))
            feats["share_purchases_morning"] = (hour_col.between(6, 11)).mean()
            feats["share_purchases_afternoon"] = (hour_col.between(12, 17)).mean()
            feats["share_purchases_evening"] = (hour_col.between(18, 23)).mean()
            feats["hour_of_day_mean"] = float(hour_col.mean())
            feats["hour_of_day_std"] = float(hour_col.std()) if len(hist_ord) > 1 else 0
        else:
            feats["share_purchases_morning"] = 0
            feats["share_purchases_afternoon"] = 0
            feats["share_purchases_evening"] = 0
            feats["hour_of_day_mean"] = 12
            feats["hour_of_day_std"] = 0

        # Product & basket
        feats["unique_products_pre"] = hist_com["product_name"].nunique() if "product_name" in hist_com.columns and not hist_com.empty else 0
        if not hist_com.empty and "order_id" in hist_com.columns:
            n_items = len(hist_com)
            n_orders = hist_com["order_id"].nunique()
            feats["avg_basket_size"] = n_items / n_orders if n_orders > 0 else 0
        else:
            feats["avg_basket_size"] = 0
        if not hist_ord.empty:
            feats["avg_discount_per_order"] = hist_ord["total_discount"].mean()
            feats["coupon_usage_rate"] = hist_ord["used_coupon"].mean()
            feats["coffee_share_orders"] = (hist_ord["coffee_commodity_num"] > 0).mean() if "coffee_commodity_num" in hist_ord.columns else 0
            feats["avg_coffee_num"] = hist_ord["coffee_commodity_num"].mean() if "coffee_commodity_num" in hist_ord.columns else 0
            feats["avg_food_num"] = hist_ord["food_commodity_num"].mean() if "food_commodity_num" in hist_ord.columns else 0
            feats["avg_use_coffee_wallet"] = hist_ord["use_coffee_wallet_num"].mean() if "use_coffee_wallet_num" in hist_ord.columns else 0
            feats["avg_delivery_pay"] = hist_ord["delivery_pay_money"].mean() if "delivery_pay_money" in hist_ord.columns else 0
            feats["take_address_rate"] = hist_ord["take_address"].notna().astype(int).mean() if "take_address" in hist_ord.columns else 0
        else:
            feats["avg_discount_per_order"] = 0
            feats["coupon_usage_rate"] = 0
            feats["coffee_share_orders"] = 0
            feats["avg_coffee_num"] = 0
            feats["avg_food_num"] = 0
            feats["avg_use_coffee_wallet"] = 0
            feats["avg_delivery_pay"] = 0
            feats["take_address_rate"] = 0

        # New product ratio (simplified)
        feats["new_product_ratio"] = 0  # Placeholder; full computation expensive

        # Store
        feats["unique_stores_pre"] = hist_com["dept_id"].nunique() if not hist_com.empty else 0
        if not hist_com.empty:
            store_counts = hist_com.groupby("dept_id").size()
            total = store_counts.sum()
            sorted_counts = store_counts.sort_values(ascending=False)
            feats["preferred_store_ratio"] = sorted_counts.iloc[0] / total if total > 0 else 0
            feats["second_store_ratio"] = sorted_counts.iloc[1] / total if len(sorted_counts) > 1 else 0
        else:
            feats["preferred_store_ratio"] = 0
            feats["second_store_ratio"] = 0

        # Demographics
        mem = member_demographics[member_demographics["member_id"] == mid]
        if not mem.empty:
            m = mem.iloc[0]
            feats["gender"] = float(m.get("gender", 0)) if "gender" in m.index else 0
            feats["birth_year"] = float(m.get("birth_year", 1990)) if "birth_year" in m.index else 1990
            by = feats["birth_year"]
            feats["age"] = max(0, min(100, 2020 - int(by))) if pd.notna(by) else 30
            feats["level"] = float(m.get("level", 0)) if "level" in m.index else 0
            inv = m.get("inviter_id", None)
            feats["has_inviter"] = 1 if pd.notna(inv) and str(inv).strip() != "" else 0
            feats["callphone"] = float(m.get("callphone", 0)) if "callphone" in m.index else 0
            feats["camera"] = float(m.get("camera", 0)) if "camera" in m.index else 0
            feats["location"] = float(m.get("location", 0)) if "location" in m.index else 0
            feats["network"] = float(m.get("network", 0)) if "network" in m.index else 0
            feats["push"] = 0 if mid in no_push_ids else (float(m.get("push", 1)) if "push" in m.index else 1)
            feats["sdcard"] = float(m.get("sdcard", 0)) if "sdcard" in m.index else 0
        else:
            feats["gender"] = 0
            feats["birth_year"] = 1990
            feats["age"] = 30
            feats["level"] = 0
            feats["has_inviter"] = 0
            feats["callphone"] = 0
            feats["camera"] = 0
            feats["location"] = 0
            feats["network"] = 0
            feats["push"] = 0 if mid in no_push_ids else 1
            feats["sdcard"] = 0

        # Closure-specific
        feats["closure_length_days"] = closure_duration
        feats["closure_start_month"] = closure_start.month
        feats["closure_start_weekday"] = pd.Timestamp(closure_start).dayofweek
        month = closure_start.month
        feats["closure_start_season"] = (month % 12 + 3) // 3  # 1-4
        feats["share_visited_stores_closed"] = 1 if is_treated else 0
        feats["tenure_days"] = (pd.Timestamp(period_start) - pd.Timestamp(earliest_date)).days

        feature_rows.append(feats)

    return pd.DataFrame(feature_rows)


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


def main() -> None:
    logger = setup_logging()
    log_print(logger, "=" * 80)
    log_print(logger, "Displacement Classification Model Training")
    log_print(logger, f"Started at {datetime.now().isoformat()}")
    log_print(logger, "=" * 80)

    # Load data
    df_commodity = load_order_commodity_data()
    df_order_full = load_order_result_full(logger)
    closures = pd.read_csv(CLOSURES_CSV, encoding="utf-8-sig")
    member_demographics = load_member_demographics(logger)
    no_push_ids = load_no_push_ids()
    log_print(logger, f"Loaded {len(no_push_ids):,} no-push members")

    customer_preference = get_customer_store_preference(df_commodity, lowest_purchases=DEFAULT_LOWEST_PURCHASES)
    unique_visits = df_commodity[["member_id", "date", "dept_id"]].drop_duplicates()

    # Build panel
    panel = build_training_panel(
        logger, df_commodity, closures, customer_preference, unique_visits,
    )

    # Compute features
    features_df = compute_features_for_panel(
        logger, panel, df_commodity, df_order_full, member_demographics, no_push_ids,
    )

    # Feature columns (exclude identifiers and label)
    exclude = {"member_id", "dept_id", "closure_start", "period", "group", "label", "is_treated", "manufacturer"}
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
    X_train = train_df[feature_cols].fillna(0)
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
            X = sub[feature_cols].fillna(0)
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
    args = parser.parse_args()
    if args.sample:
        os.environ["DISPLACEMENT_SAMPLE"] = str(args.sample)
    main()
