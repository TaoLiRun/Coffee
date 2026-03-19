"""
Data loading, panel construction, and feature engineering for the
displacement classification pipeline.

Exports
-------
Constants : DATA_DIR, CLOSURES_CSV, OUTPUT_DIR, LOG_DIR, LOG_FILE,
            NUM_PRE_PERIODS, DEMO_INTERMEDIATE_DIR
Functions : setup_logging, log_print,
            load_no_push_ids, load_member_demographics, load_order_result_full,
            build_training_panel, compute_features_for_panel
Re-exports (from analyze_closure_impact):
            DEFAULT_LOWEST_PURCHASES, DEFAULT_LOWEST_RATIO,
            get_customer_store_preference
"""

from __future__ import annotations

import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR   = Path(__file__).resolve().parent
# parents[0]=displacement_classification, parents[1]=src, parents[2]=model-free
PROJECT_ROOT = SCRIPT_DIR.parents[2]          # model-free/

# Data dir: prefer location where order_result.csv exists (works with either repo layout)
_data_candidates = [
    PROJECT_ROOT.parent / "data" / "data1031",
    PROJECT_ROOT / "data" / "data1031",
]
DATA_DIR = next(
    (p for p in _data_candidates if (p / "order_result.csv").exists()),
    _data_candidates[0],
)

# Outputs/closures: prefer PROJECT_ROOT; if not found, try model-free subdir (when PROJECT_ROOT is parent repo)
_outputs_root = PROJECT_ROOT
if not (PROJECT_ROOT / "outputs" / "store").exists() and (PROJECT_ROOT / "model-free" / "outputs" / "store").exists():
    _outputs_root = PROJECT_ROOT / "model-free"

CLOSURES_CSV        = _outputs_root / "outputs" / "store" / "non_uni_store_closures.csv"
PAIR_REGISTRY_CSV   = _outputs_root / "outputs" / "customer-store" / "closure_pair_registry.csv"
MEMBER_RESULT_PATH  = DATA_DIR / "member_result.csv"
NO_PUSH_MEMBERS_PATH = _outputs_root / "data" / "processed" / "no_push_members.csv"
DEMO_INTERMEDIATE_DIR = _outputs_root / "data" / "intermediate"

OUTPUT_DIR = _outputs_root / "outputs" / "displacement_classification"
LOG_DIR    = OUTPUT_DIR / "logs"
LOG_FILE   = LOG_DIR / "train_displacement_model.log"

# Create directories eagerly so log handlers don't fail on first use
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)
DEMO_INTERMEDIATE_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
CONFIG_PATH = SCRIPT_DIR / "config.json"


def load_config() -> dict:
    """Load configuration from config.json located next to this file."""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


CONFIG = load_config()

NUM_PRE_PERIODS = CONFIG["data"]["num_pre_periods"]

# ---------------------------------------------------------------------------
# Imports from customer-store analysis module
# ---------------------------------------------------------------------------
sys.path.insert(0, str(PROJECT_ROOT / "src" / "customer-store"))

from data_processing import (           # noqa: E402
    DEFAULT_LOWEST_PURCHASES,
    DEFAULT_LOWEST_RATIO,
    MIN_CTRL_TREAT_RATIO,
    MIN_GROUP_SIZE,
    USE_SET_UP_TIME_MATCHED_CONTROL,
    build_date_sorted_index,
    get_closure_specific_control_members,
    get_closure_control_members_set_up_matched,
    get_customer_store_preference,
    get_preference_before_date,
    get_treatment_and_control_members_for_closure,
    get_never_treated_members,
)
from data_processing import (           # noqa: E402
    _get_treated_members_for_store,
    _slice_by_date,
)

# Override analyze_closure_impact defaults with config-driven values
# (edit config.json to change these thresholds without touching code)
DEFAULT_LOWEST_PURCHASES = CONFIG["data"]["min_purchases_threshold"]
DEFAULT_LOWEST_RATIO     = CONFIG["data"]["min_store_ratio"]

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------


def setup_logging() -> logging.Logger:
    """Configure logging to file (LOG_FILE) and console (stdout)."""
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
    """Log at *level* and echo to the attached stream handlers."""
    getattr(logger, level)(msg)


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------


def load_no_push_ids() -> set:
    """Return the set of member IDs for whom push notifications are suppressed."""
    if not NO_PUSH_MEMBERS_PATH.exists():
        return set()
    df = pd.read_csv(NO_PUSH_MEMBERS_PATH, encoding="utf-8-sig")
    return set(df["member_id"].unique())


def load_member_demographics(logger: logging.Logger, no_push_ids: set) -> pd.DataFrame:
    """
    Load member_result.csv and integer-encode categorical demographics.

    Excluded columns: birth_year, camera, location, network, sdcard.
    Encoding rule: NaN → 1; sorted unique non-NaN values → 2, 3, 4, …
    The mapping is saved to DEMO_INTERMEDIATE_DIR/demo_encoding_map.csv.

    ``no_push_ids`` members: push value is overridden to 0 before encoding.
    """
    log_print(logger, f"Loading member demographics from {MEMBER_RESULT_PATH}")
    df = pd.read_csv(MEMBER_RESULT_PATH, encoding="utf-8-sig")
    want = ["member_id", "gender", "level", "inviter_id", "manufacturer", "callphone", "push"]
    cols = [c for c in want if c in df.columns]
    df = df[cols].copy()
    log_print(logger, f"  Loaded {len(df):,} members")

    # Derive binary has_inviter before encoding
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

    mapping_path = DEMO_INTERMEDIATE_DIR / "demo_encoding_map.csv"
    pd.DataFrame(mapping_records).to_csv(mapping_path, index=False)
    log_print(logger, f"  Saved encoding map ({len(mapping_records)} entries) → {mapping_path}")
    return df


def load_order_result_full(logger: logging.Logger) -> pd.DataFrame:
    """Load full order_result.csv and compute derived spend / discount columns."""
    path = DATA_DIR / "order_result.csv"
    log_print(logger, f"Loading order result from {path}")
    df = pd.read_csv(path, encoding="utf-8-sig")
    df["dt"] = pd.to_datetime(df["create_hour"], errors="coerce")
    df = df.dropna(subset=["dt"])
    df["date"] = df["dt"].dt.date
    df["hour"] = df["dt"].dt.hour
    spend_cols    = ["coffee_origin_money", "drink_not_coffee_origin_money",
                     "food_origin_money", "other_origin_money"]
    discount_cols = ["coffee_discount", "drink_not_coffee_discount",
                     "food_discount", "other_discount"]
    df["spend"] = (
        df[[c for c in spend_cols    if c in df.columns]].fillna(0).sum(axis=1)
        * df[[c for c in discount_cols if c in df.columns]].fillna(1).sum(axis=1)
    )
    df["total_discount"] = df[[c for c in discount_cols if c in df.columns]].fillna(1).sum(axis=1)
    df["used_coupon"]    = (df["use_coupon_num"] > 0).astype(int) if "use_coupon_num" in df.columns else 0
    log_print(logger, f"  Loaded {len(df):,} orders")
    return df


def _closure_key(dept_id: Any, closure_start: Any) -> tuple[int, str]:
    return int(dept_id), pd.to_datetime(closure_start).strftime("%Y-%m-%d")


def parse_control_store_ids(serialized: Any) -> List[int]:
    if serialized is None or (isinstance(serialized, float) and np.isnan(serialized)):
        return []
    s = str(serialized).strip()
    if not s:
        return []
    return [int(x) for x in s.split("|") if x != ""]


def load_or_build_closure_pair_registry(
    logger: logging.Logger,
    df_orders: pd.DataFrame,
    closures: pd.DataFrame,
    customer_preference: pd.DataFrame,
    unique_visits: pd.DataFrame,
) -> pd.DataFrame:
    """
    Load closure_pair_registry from existing CSV.

    This pipeline requires the registry to be pre-built by
    analyze_closure_impact.py. If the CSV is missing, raise an error to
    remind users to run that script first.
    """
    if not PAIR_REGISTRY_CSV.exists():
        raise FileNotFoundError(
            f"Required closure pair registry not found: {PAIR_REGISTRY_CSV}. "
            "Please run analyze_closure_impact.py first to generate this file."
        )

    reg = pd.read_csv(PAIR_REGISTRY_CSV, encoding="utf-8-sig")
    if "status" not in reg.columns:
        raise ValueError(
            f"closure_pair_registry.csv is missing required column 'status': {PAIR_REGISTRY_CSV}"
        )

    n_total = len(reg)
    reg = reg[reg["status"] == "kept"].copy()
    log_print(
        logger,
        f"Loaded closure pair registry from CSV: {PAIR_REGISTRY_CSV} "
        f"(kept rows: {len(reg):,}/{n_total:,})",
    )
    return reg


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

    Each period has length D = closure_duration_days for that closure.
    period: −num_pre_periods … −1 (pre-closure spans of D days each);
    0 for control during closure (evaluation only — excluded from training in main.py).
    Closures are skipped if there is insufficient history for 4 pre-periods of length D.
    """
    log_print(logger, f"\nBuilding training panel ({NUM_PRE_PERIODS} pre-periods of length D=closure_duration_days)...")
    pair_registry = load_or_build_closure_pair_registry(
        logger, df_orders, closures, customer_preference, unique_visits
    )
    reg_map: Dict[tuple[int, str], pd.Series] = {
        _closure_key(r["dept_id"], r["closure_start"]): r
        for _, r in pair_registry.iterrows()
    }

    control_pool = get_never_treated_members(
        closures, customer_preference, DEFAULT_LOWEST_PURCHASES, DEFAULT_LOWEST_RATIO
    )
    df_com_s = build_date_sorted_index(df_orders)
    log_print(logger, f"  Never-treated control pool: {len(control_pool):,} customers")

    df_orders_ts = df_orders.copy()
    df_orders_ts["date"] = pd.to_datetime(df_orders_ts["date"])
    member_first_purchase = df_orders_ts.groupby("member_id")["date"].min()
    earliest_order_date = df_orders_ts["date"].min()
    log_print(logger, f"  Earliest order date in data: {earliest_order_date.date()}")

    rows: List[Dict[str, Any]] = []
    n_closures = len(closures)
    skipped_history = 0
    for idx, (_, closure) in enumerate(closures.iterrows()):
        if (idx + 1) % 25 == 0 or idx == 0:
            log_print(logger, f"  Closure {idx + 1}/{n_closures}...")
        dept_id = int(closure["dept_id"])
        closure_start = pd.to_datetime(closure["closure_start"])
        closure_end = pd.to_datetime(closure["closure_end"])
        D = max(int(closure["closure_duration_days"]), 1)

        # Skip closure if not enough calendar history for 4 pre-periods of length D
        # (need at least 7 days before period -4 start for feature computation)
        min_closure_start = earliest_order_date + pd.Timedelta(days=NUM_PRE_PERIODS * D + 8)
        if closure_start < min_closure_start:
            skipped_history += 1
            continue

        key = _closure_key(dept_id, closure["closure_start"])
        reg_row = reg_map.get(key)
        if reg_row is None or reg_row.get("status") != "kept":
            continue

        if USE_SET_UP_TIME_MATCHED_CONTROL:
            control_store_ids = parse_control_store_ids(reg_row.get("control_store_ids", ""))
            if not control_store_ids:
                continue
            treatment, closure_control, _ = get_treatment_and_control_members_for_closure(
                unique_visits=unique_visits,
                customer_preference=customer_preference,
                closure=closure,
                lowest_purchases=DEFAULT_LOWEST_PURCHASES,
                lowest_ratio=DEFAULT_LOWEST_RATIO,
                use_set_up_time_matched_control=True,
                control_pool=None,
                control_stores_by_closure={(dept_id, closure["closure_start"]): control_store_ids},
            )
        else:
            treatment, closure_control, _ = get_treatment_and_control_members_for_closure(
                unique_visits=unique_visits,
                customer_preference=customer_preference,
                closure=closure,
                lowest_purchases=DEFAULT_LOWEST_PURCHASES,
                lowest_ratio=DEFAULT_LOWEST_RATIO,
                use_set_up_time_matched_control=False,
                control_pool=control_pool,
                control_stores_by_closure=None,
            )

        if not treatment or not closure_control:
            continue

        earliest_preperiod = closure_start - pd.Timedelta(days=NUM_PRE_PERIODS * D)

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
            for w in range(-NUM_PRE_PERIODS, 0):  # periods −4, −3, −2, −1 (each of length D days)
                period_start = (closure_start + pd.Timedelta(days=w * D)).date()
                period_end = (closure_start + pd.Timedelta(days=(w + 1) * D - 1)).date()
                pc = _slice_by_date(df_com_s, period_start, period_end)
                pc = pc[pc["member_id"].isin(members)]
                purchasers = set(pc["member_id"].unique()) if not pc.empty else set()
                for mid in members:
                    rows.append({
                        "member_id": mid,
                        "dept_id": dept_id,
                        "closure_start": closure["closure_start"],
                        "closure_end": closure["closure_end"],
                        "closure_length_days": D,
                        "closure_duration_days": D,
                        "group": group_label,
                        "period": w,
                        "period_start": period_start,
                        "period_end": period_end,
                        "label": 1 if mid in purchasers else 0,
                        "is_treated": 1 if group_label == "treatment" else 0,
                    })
            # Control: add period 0 (during closure) for evaluation only
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
                        "closure_length_days": D,
                        "closure_duration_days": D,
                        "group": group_label,
                        "period": 0,
                        "period_start": dur_start,
                        "period_end": dur_end,
                        "label": 1 if mid in purchasers else 0,
                        "is_treated": 0,
                    })

    if skipped_history > 0:
        log_print(logger, f"  Skipped {skipped_history} closure(s) for insufficient history.")
    panel = pd.DataFrame(rows)
    sample = os.environ.get("DISPLACEMENT_SAMPLE")
    if sample:
        n = int(sample)
        panel = panel.sample(n=min(n, len(panel)), random_state=42)
        log_print(logger, f"  Sampled to {len(panel):,} rows (--sample={n})")
    log_print(logger, f"  Panel: {len(panel):,} rows, {panel['member_id'].nunique():,} unique members")
    log_print(logger, f"  Label distribution: {panel['label'].value_counts().to_dict()}")
    return panel


def build_t0_ex_ante_panel(
    logger: logging.Logger,
    df_orders: pd.DataFrame,
    closures: pd.DataFrame,
    customer_preference: pd.DataFrame,
    unique_visits: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build ex-ante t0 scoring panel for both treatment and control groups.

    One row per (member_id, dept_id, closure_start, group) with:
    - period_start = closure_start (features use history up to closure_start - 1)
    - score_time = "t0_ex_ante"

    This panel is for post-training scoring only (not for model training).
    """
    log_print(logger, "\nBuilding ex-ante t0 scoring panel (both groups)...")

    pair_registry = load_or_build_closure_pair_registry(
        logger, df_orders, closures, customer_preference, unique_visits
    )
    reg_map: Dict[tuple[int, str], pd.Series] = {
        _closure_key(r["dept_id"], r["closure_start"]): r
        for _, r in pair_registry.iterrows()
    }

    control_pool = get_never_treated_members(
        closures, customer_preference, DEFAULT_LOWEST_PURCHASES, DEFAULT_LOWEST_RATIO
    )
    log_print(logger, f"  Never-treated control pool: {len(control_pool):,} customers")

    df_orders_ts = df_orders.copy()
    df_orders_ts["date"] = pd.to_datetime(df_orders_ts["date"])
    member_first_purchase = df_orders_ts.groupby("member_id")["date"].min()
    earliest_order_date = df_orders_ts["date"].min()

    rows: List[Dict[str, Any]] = []
    skipped_history = 0
    for _, closure in closures.iterrows():
        dept_id = int(closure["dept_id"])
        closure_start = pd.to_datetime(closure["closure_start"])
        closure_end = pd.to_datetime(closure["closure_end"])
        D = max(int(closure["closure_duration_days"]), 1)

        min_closure_start = earliest_order_date + pd.Timedelta(days=NUM_PRE_PERIODS * D + 8)
        if closure_start < min_closure_start:
            skipped_history += 1
            continue

        key = _closure_key(dept_id, closure["closure_start"])
        reg_row = reg_map.get(key)
        if reg_row is None or reg_row.get("status") != "kept":
            continue

        if USE_SET_UP_TIME_MATCHED_CONTROL:
            control_store_ids = parse_control_store_ids(reg_row.get("control_store_ids", ""))
            if not control_store_ids:
                continue
            treatment, closure_control, _ = get_treatment_and_control_members_for_closure(
                unique_visits=unique_visits,
                customer_preference=customer_preference,
                closure=closure,
                lowest_purchases=DEFAULT_LOWEST_PURCHASES,
                lowest_ratio=DEFAULT_LOWEST_RATIO,
                use_set_up_time_matched_control=True,
                control_pool=None,
                control_stores_by_closure={(dept_id, closure["closure_start"]): control_store_ids},
            )
        else:
            treatment, closure_control, _ = get_treatment_and_control_members_for_closure(
                unique_visits=unique_visits,
                customer_preference=customer_preference,
                closure=closure,
                lowest_purchases=DEFAULT_LOWEST_PURCHASES,
                lowest_ratio=DEFAULT_LOWEST_RATIO,
                use_set_up_time_matched_control=False,
                control_pool=control_pool,
                control_stores_by_closure=None,
            )

        if not treatment or not closure_control:
            continue

        earliest_preperiod = closure_start - pd.Timedelta(days=NUM_PRE_PERIODS * D)

        def _has_pre_window_history(members: list) -> list:
            return [
                m for m in members
                if m in member_first_purchase.index and member_first_purchase[m] < earliest_preperiod
            ]

        treatment = _has_pre_window_history(treatment)
        closure_control = _has_pre_window_history(closure_control)
        if not treatment or not closure_control:
            continue

        period_start = closure_start.date()
        period_end = closure_end.date()

        for group_label, members in [("treatment", treatment), ("control", closure_control)]:
            is_treated = 1 if group_label == "treatment" else 0
            for mid in members:
                rows.append(
                    {
                        "member_id": mid,
                        "dept_id": dept_id,
                        "closure_start": closure["closure_start"],
                        "closure_end": closure["closure_end"],
                        "closure_length_days": D,
                        "closure_duration_days": D,
                        "group": group_label,
                        "period": 0,
                        "period_start": period_start,
                        "period_end": period_end,
                        "label": 0,
                        "is_treated": is_treated,
                        "score_time": "t0_ex_ante",
                    }
                )

    panel = pd.DataFrame(rows)
    if skipped_history > 0:
        log_print(logger, f"  Skipped {skipped_history} closure(s) for insufficient history.")
    log_print(
        logger,
        f"  Ex-ante panel: {len(panel):,} rows, {panel['member_id'].nunique() if not panel.empty else 0:,} unique members",
    )
    return panel


# ---------------------------------------------------------------------------
# Feature construction
# ---------------------------------------------------------------------------


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

    Iterates once per unique period_start date (instead of once per
    closure × period group) to amortise the cost of large groupby aggregations
    across all closures that share the same history cutoff date.
    """
    log_print(logger, "\nComputing features (vectorized)...")

    # ------------------------------------------------------------------
    # 0. Canonicalize types
    # ------------------------------------------------------------------
    df_order_full["date"] = pd.to_datetime(df_order_full["date"])
    panel["period_start"]    = pd.to_datetime(panel["period_start"])
    panel["_closure_start_dt"] = pd.to_datetime(panel["closure_start"])

    earliest_date = df_order_full["date"].min()   # Timestamp

    df_ord_sorted  = df_order_full.sort_values("date").reset_index(drop=True)
    ord_dates_np   = df_ord_sorted["date"].values

    # ------------------------------------------------------------------
    # 1. Closure-specific features
    # ------------------------------------------------------------------
    panel["closure_start_month"]    = panel["_closure_start_dt"].dt.month
    panel["closure_start_weekday"]  = panel["_closure_start_dt"].dt.dayofweek
    panel["closure_start_season"]   = (panel["_closure_start_dt"].dt.month % 12 + 3) // 3
    panel["share_visited_stores_closed"] = panel["is_treated"].astype(float)
    panel["tenure_days"]            = (panel["period_start"] - earliest_date).dt.days

    # ------------------------------------------------------------------
    # 2. Demographic features – merged once
    # ------------------------------------------------------------------
    required_demo_cols = ["gender", "level", "has_inviter", "manufacturer", "callphone", "push"]
    missing_demo_src   = [c for c in required_demo_cols if c not in member_demographics.columns]
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
    # 3. Behavioral features — one pass per unique period_start date
    # ------------------------------------------------------------------
    # KEY INSIGHT: all behavioral features are a function of
    # (member_id, history_cutoff = period_start − 1 day).  Many
    # (closure × period) groups share the same period_start, so iterating
    # over unique dates avoids redundant groupby work.
    unique_period_starts = sorted(panel["period_start"].unique())
    n_unique_ps = len(unique_period_starts)
    n_groups    = panel[["dept_id", "closure_start", "period_start"]].drop_duplicates().shape[0]
    log_print(
        logger,
        f"  {n_groups} (closure × period) groups across "
        f"{panel['member_id'].nunique():,} unique members — "
        f"iterating over {n_unique_ps} unique period_start dates...",
    )

    # df_ord_sorted is already filtered to panel members (done in main).
    # No per-iteration isin() filter needed — we compute features for all
    # panel members at each cutoff and rely on the fan-out join to discard
    # rows that don't belong to the current (closure × period) context.
    all_panel_members = panel["member_id"].unique()
    behavioral_parts: List[pd.DataFrame] = []

    for ps_idx, ps in enumerate(unique_period_starts):
        if (ps_idx + 1) % 10 == 0 or ps_idx == 0:
            log_print(
                logger,
                f"  period_start {ps_idx + 1}/{n_unique_ps}  date={pd.Timestamp(ps).date()}",
            )

        ps = pd.Timestamp(ps)
        panel_at_ps  = panel[panel["period_start"] == ps]
        members_at_ps = panel_at_ps["member_id"].unique()

        history_end            = ps - pd.Timedelta(days=1)
        history_days_available = (history_end - earliest_date).days

        if history_days_available < 7:
            raise ValueError(
                f"[period_start={ps.date()}] Only {history_days_available}d of history "
                f"available before {ps.date()}. The Aug-2020 closure filter should have "
                "prevented this. Check that closures were filtered to closure_start >= 2020-09-01."
            )

        n_weeks_history    = max(history_days_available / 7, 0.01)
        n_weeks_in_history = max(int(history_days_available / 7), 1)

        hi_ord   = int(np.searchsorted(ord_dates_np, history_end.to_datetime64(), side="right"))
        hist_ord = df_ord_sorted.iloc[:hi_ord]

        cutoff_4w = history_end - pd.Timedelta(days=28)
        cutoff_2w = history_end - pd.Timedelta(days=14)
        cutoff_1w = history_end - pd.Timedelta(days=7)

        if hist_ord.empty:
            raise ValueError(
                f"[period_start={ps.date()}] No order history found for any of "
                f"{len(members_at_ps)} panel members before {history_end.date()}. "
                "Check that treatment/control members satisfy the pre-closure "
                f"purchase requirement (≥{DEFAULT_LOWEST_PURCHASES} purchases)."
            )

        member_batch = pd.DataFrame({"member_id": all_panel_members})

        # ---- Purchase frequency & recency --------------------------------
        pur_days = hist_ord.drop_duplicates(["member_id", "date"])
        pur_all  = pur_days.groupby("member_id").size().rename("total_purchase_days_pre")
        last_pur = pur_days.groupby("member_id")["date"].max().rename("_last_purchase")
        pur_4w   = pur_days[pur_days["date"] >= cutoff_4w].groupby("member_id").size().rename("_pur4w")
        pur_2w   = pur_days[pur_days["date"] >= cutoff_2w].groupby("member_id").size().rename("_pur2w")
        pur_1w   = pur_days[pur_days["date"] >= cutoff_1w].groupby("member_id").size().rename("_pur1w")

        member_batch = member_batch.merge(pur_all,  on="member_id", how="left")
        member_batch = member_batch.merge(last_pur, on="member_id", how="left")
        member_batch = member_batch.merge(pur_4w,   on="member_id", how="left")
        member_batch = member_batch.merge(pur_2w,   on="member_id", how="left")
        member_batch = member_batch.merge(pur_1w,   on="member_id", how="left")

        # Validate only members that actually need features at this period_start
        at_ps_mask  = member_batch["member_id"].isin(members_at_ps)
        missing_hist = member_batch[at_ps_mask & member_batch["total_purchase_days_pre"].isna()]["member_id"].tolist()
        if missing_hist:
            raise ValueError(
                f"[period_start={ps.date()}] {len(missing_hist)} members have no purchase "
                f"history before {history_end.date()} but appear in panel. "
                f"First 10: {missing_hist[:10]}. "
                "All panel members must have purchase records dating from before the "
                "closure's earliest pre-period. Check that the Aug-2020 closure filter "
                "and the treatment/control eligibility criteria are enforced."
            )
        member_batch["total_purchase_days_pre"] = member_batch["total_purchase_days_pre"].fillna(0).astype(int)

        missing_lp = member_batch[at_ps_mask & member_batch["_last_purchase"].isna()]["member_id"].tolist()
        if missing_lp:
            raise ValueError(
                f"[period_start={ps.date()}] {len(missing_lp)} members have NaT last_purchase. "
                f"First 10: {missing_lp[:10]}"
            )

        for col in ["_pur4w", "_pur2w", "_pur1w"]:
            member_batch[col] = member_batch[col].fillna(0).astype(int)

        member_batch["purchases_per_week_all_pre"]  = member_batch["total_purchase_days_pre"] / n_weeks_history
        member_batch["purchases_per_week_last_4w"]  = member_batch["_pur4w"] / 4.0
        member_batch["purchases_per_week_last_2w"]  = member_batch["_pur2w"] / 2.0
        member_batch["purchases_per_week_last_1w"]  = member_batch["_pur1w"] / 1.0
        member_batch["days_since_last_purchase"]    = (ps - member_batch["_last_purchase"]).dt.days.fillna(9999).astype(int)
        member_batch["purchased_in_last_7_days"]    = (member_batch["days_since_last_purchase"] <= 7).astype(int)
        member_batch["purchased_in_last_14_days"]   = (member_batch["days_since_last_purchase"] <= 14).astype(int)

        # ---- Order counts & spend ----------------------------------------
        for req_col in ["order_id", "spend"]:
            if req_col not in hist_ord.columns:
                raise ValueError(
                    f"order_result.csv is missing required column '{req_col}'. "
                    "Cannot compute order-level features."
                )
        ord_g      = hist_ord.groupby("member_id")
        ord_counts = ord_g["order_id"].nunique().rename("total_orders_pre")
        spend_all  = ord_g["spend"].sum().rename("total_spend_pre")
        spend_4w   = hist_ord[hist_ord["date"] >= cutoff_4w].groupby("member_id")["spend"].sum().rename("total_spend_last_4w")
        spend_2w   = hist_ord[hist_ord["date"] >= cutoff_2w].groupby("member_id")["spend"].sum().rename("total_spend_last_2w")
        member_batch = member_batch.merge(ord_counts, on="member_id", how="left")
        member_batch = member_batch.merge(spend_all,  on="member_id", how="left")
        member_batch = member_batch.merge(spend_4w,   on="member_id", how="left")
        member_batch = member_batch.merge(spend_2w,   on="member_id", how="left")

        missing_ord = member_batch[at_ps_mask & member_batch["total_orders_pre"].isna()]["member_id"].tolist()
        if missing_ord:
            raise ValueError(
                f"[period_start={ps.date()}] {len(missing_ord)} members have purchase history "
                f"in commodity data but no records in order_result.csv. "
                f"First 10: {missing_ord[:10]}. "
                "Check join key consistency between order_commodity and order_result."
            )
        member_batch["total_orders_pre"]    = member_batch["total_orders_pre"].fillna(0).astype(int)
        member_batch["total_spend_pre"]     = member_batch["total_spend_pre"].astype(float)
        member_batch["total_spend_last_4w"] = member_batch["total_spend_last_4w"].fillna(0.0)
        member_batch["total_spend_last_2w"] = member_batch["total_spend_last_2w"].fillna(0.0)

        # ---- Habit / regularity (vectorized) --------------------------------
        pur_sorted = (
            hist_ord.drop_duplicates(["member_id", "date"])
            .sort_values(["member_id", "date"])
            .copy()
        )
        pur_sorted["_gap"] = pur_sorted.groupby("member_id")["date"].diff().dt.days
        gap_stats = (
            pur_sorted.groupby("member_id")["_gap"]
            .agg(
                mean_inter_purchase_interval_days="mean",
                std_inter_purchase_interval_days="std",
                max_gap_between_purchases="max",
            )
            .reset_index()
        )
        gap_stats["mean_inter_purchase_interval_days"] = gap_stats["mean_inter_purchase_interval_days"].fillna(0.0)
        gap_stats["std_inter_purchase_interval_days"]  = gap_stats["std_inter_purchase_interval_days"].fillna(0.0)
        gap_stats["max_gap_between_purchases"]          = gap_stats["max_gap_between_purchases"].fillna(0.0)
        gap_stats["cv_inter_purchase_interval"] = (
            gap_stats["std_inter_purchase_interval_days"]
            / gap_stats["mean_inter_purchase_interval_days"].replace(0.0, np.nan)
        ).fillna(0.0)

        pur_sorted["_new_streak"] = (pur_sorted["_gap"] != 1) | pur_sorted["_gap"].isna()
        pur_sorted["_streak_id"]  = pur_sorted.groupby("member_id")["_new_streak"].cumsum()
        streak_len = pur_sorted.groupby(["member_id", "_streak_id"]).size()
        max_streak = (
            streak_len.groupby("member_id").max()
            .rename("longest_consecutive_streak_days")
            .reset_index()
        )
        habit_feats  = gap_stats.merge(max_streak, on="member_id", how="left")
        week_idx_s   = (hist_ord["date"] - earliest_date).dt.days // 7
        weeks_with_pur = week_idx_s.groupby(hist_ord["member_id"]).nunique().rename("_n_weeks_pur")

        member_batch = member_batch.merge(habit_feats,  on="member_id", how="left")
        member_batch = member_batch.merge(weeks_with_pur, on="member_id", how="left")

        missing_habit = member_batch[at_ps_mask & member_batch["mean_inter_purchase_interval_days"].isna()]["member_id"].tolist()
        if missing_habit:
            raise ValueError(
                f"[period_start={ps.date()}] {len(missing_habit)} members are missing habit "
                f"features after vectorized gap computation. "
                f"First 10: {missing_habit[:10]}. "
                "Check that hist_ord contains these members."
            )
        member_batch["longest_consecutive_streak_days"] = member_batch["longest_consecutive_streak_days"].fillna(0).astype(int)

        missing_nwp = member_batch[at_ps_mask & member_batch["_n_weeks_pur"].isna()]["member_id"].tolist()
        if missing_nwp:
            raise ValueError(
                f"[period_start={ps.date()}] {len(missing_nwp)} members missing weeks_with_purchase. "
                f"First 10: {missing_nwp[:10]}"
            )
        member_batch["_n_weeks_pur"]             = member_batch["_n_weeks_pur"].fillna(0)
        member_batch["share_weeks_with_purchase"] = member_batch["_n_weeks_pur"] / n_weeks_in_history

        # ---- Day-of-week -----------------------------------------------
        dow_s     = hist_ord["date"].dt.dayofweek.rename("_dow")
        dow_total = hist_ord.groupby("member_id").size().rename("_dow_total")
        dow_size  = (
            hist_ord.groupby(["member_id", dow_s])
            .size()
            .unstack(fill_value=0)
            .reindex(columns=range(7), fill_value=0)
        )
        dow_modal = dow_size.idxmax(axis=1).rename("modal_purchase_dow")
        dow_pivot = dow_size.copy()
        dow_pivot.columns = [f"_dow_cnt_{d}" for d in range(7)]
        member_batch = member_batch.merge(dow_total, on="member_id", how="left")
        member_batch = member_batch.merge(dow_pivot, on="member_id", how="left")
        member_batch = member_batch.merge(dow_modal, on="member_id", how="left")

        missing_dow = member_batch[at_ps_mask & member_batch["_dow_total"].isna()]["member_id"].tolist()
        if missing_dow:
            raise ValueError(
                f"[period_start={ps.date()}] {len(missing_dow)} members missing DoW totals. "
                f"First 10: {missing_dow[:10]}"
            )
        member_batch["_dow_total"] = member_batch["_dow_total"].fillna(1)   # avoid ÷0 for non-at_ps
        for d in range(7):
            member_batch[f"share_purchases_dow{d}"] = (
                member_batch[f"_dow_cnt_{d}"].fillna(0) / member_batch["_dow_total"]
            )
        member_batch["modal_purchase_dow"] = member_batch["modal_purchase_dow"].fillna(0).astype(int)
        dow_share_cols  = [f"share_purchases_dow{d}" for d in range(7)]
        probs_matrix    = member_batch[dow_share_cols].values.clip(0)
        member_batch["entropy_dow"] = -(probs_matrix * np.log(probs_matrix + 1e-10)).sum(axis=1)

        # ---- Basket size & category breadth ----------------------------
        basket_num_cols = [c for c in [
            "coffee_commodity_num", "not_coffee_commodity_num",
            "food_commodity_num", "other_not_coffee_commodity_num",
        ] if c in hist_ord.columns]
        if not basket_num_cols:
            raise ValueError(
                "order_result.csv is missing all commodity count columns "
                "(coffee_commodity_num, not_coffee_commodity_num, etc.)."
            )
        basket_vals    = hist_ord[basket_num_cols].fillna(0)
        total_items_s  = basket_vals.sum(axis=1)
        n_categories_s = (basket_vals > 0).sum(axis=1)
        com_orders     = hist_ord.groupby("member_id").size().rename("_com_orders")
        avg_basket     = total_items_s.groupby(hist_ord["member_id"]).mean().rename("avg_basket_size")
        avg_categories = n_categories_s.groupby(hist_ord["member_id"]).mean().rename("n_order_categories_avg")
        member_batch = member_batch.merge(com_orders,     on="member_id", how="left")
        member_batch = member_batch.merge(avg_basket,     on="member_id", how="left")
        member_batch = member_batch.merge(avg_categories, on="member_id", how="left")

        missing_basket = member_batch[at_ps_mask & member_batch["avg_basket_size"].isna()]["member_id"].tolist()
        if missing_basket:
            raise ValueError(
                f"[period_start={ps.date()}] {len(missing_basket)} members missing basket features. "
                f"First 10: {missing_basket[:10]}"
            )

        # ---- Store loyalty -----------------------------------------------
        hist_ord_visits = hist_ord.drop_duplicates(["member_id", "date", "dept_id"])
        store_counts    = (
            hist_ord_visits.groupby(["member_id", "dept_id"])
            .size()
            .unstack(fill_value=0)
        )
        uniq_stores   = (store_counts > 0).sum(axis=1).rename("unique_stores_pre")
        sc_vals       = store_counts.values.astype(float)
        sc_sorted     = -np.sort(-sc_vals, axis=1)
        row_totals    = sc_sorted.sum(axis=1)
        safe_totals   = np.where(row_totals > 0, row_totals, 1.0)
        pref_ratio    = pd.Series(sc_sorted[:, 0] / safe_totals,
                                  index=store_counts.index, name="preferred_store_ratio")
        sec_vals_col  = sc_sorted[:, 1] if sc_sorted.shape[1] > 1 else np.zeros(len(store_counts))
        sec_ratio     = pd.Series(sec_vals_col / safe_totals,
                                  index=store_counts.index, name="second_store_ratio")
        member_batch = member_batch.merge(uniq_stores, on="member_id", how="left")
        member_batch = member_batch.merge(pref_ratio,  on="member_id", how="left")
        member_batch = member_batch.merge(sec_ratio,   on="member_id", how="left")

        missing_store = member_batch[at_ps_mask & member_batch["unique_stores_pre"].isna()]["member_id"].tolist()
        if missing_store:
            raise ValueError(
                f"[period_start={ps.date()}] {len(missing_store)} members missing store features. "
                f"First 10: {missing_store[:10]}"
            )
        member_batch["unique_stores_pre"] = member_batch["unique_stores_pre"].fillna(0).astype(int)

        # ---- Order-level aggregates ------------------------------------
        ord_scalar_cols = {
            "avg_discount_per_order":  ("total_discount",        "mean"),
            "coupon_usage_rate":        ("used_coupon",           "mean"),
            "avg_coffee_num":           ("coffee_commodity_num",  "mean"),
            "avg_food_num":             ("food_commodity_num",    "mean"),
            "avg_use_coffee_wallet":    ("use_coffee_wallet_num", "mean"),
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
        member_batch = member_batch.merge(ord_agg, on="member_id", how="left")

        if "delivery_pay_money" not in hist_ord.columns:
            raise ValueError("order_result.csv is missing required column 'delivery_pay_money'.")
        avg_delivery = (
            hist_ord["delivery_pay_money"].fillna(0)
            .groupby(hist_ord["member_id"]).mean()
            .rename("avg_delivery_pay")
        )
        member_batch = member_batch.merge(avg_delivery, on="member_id", how="left")

        missing_ord_agg = member_batch[at_ps_mask & member_batch["avg_discount_per_order"].isna()]["member_id"].tolist()
        if missing_ord_agg:
            raise ValueError(
                f"[period_start={ps.date()}] {len(missing_ord_agg)} members missing order aggregates. "
                f"First 10: {missing_ord_agg[:10]}"
            )

        cof_share = (
            hist_ord["coffee_commodity_num"].gt(0)
            .groupby(hist_ord["member_id"]).mean()
            .rename("coffee_share_orders")
        )
        member_batch = member_batch.merge(cof_share, on="member_id", how="left")

        if "take_address" not in hist_ord.columns:
            raise ValueError("order_result.csv is missing required column 'take_address'.")
        ta_rate = (
            hist_ord["take_address"].notna().astype(int)
            .groupby(hist_ord["member_id"]).mean()
            .rename("take_address_rate")
        )
        member_batch = member_batch.merge(ta_rate, on="member_id", how="left")

        # Drop internal helper columns
        member_batch.drop(
            columns=[c for c in member_batch.columns if c.startswith("_")],
            inplace=True, errors="ignore",
        )

        # Fan out: for each (dept_id, closure_start) that shares this period_start,
        # join member-level features to produce one row per
        # (member_id, dept_id, closure_start, period_start).
        closure_keys = (
            panel_at_ps[["member_id", "dept_id", "closure_start"]]
            .drop_duplicates()
        )
        batch = closure_keys.merge(member_batch, on="member_id", how="left")
        batch["period_start"] = ps
        behavioral_parts.append(batch)

    # ------------------------------------------------------------------
    # Merge behavioral features back onto panel
    # ------------------------------------------------------------------
    log_print(logger, "  Merging behavioral features back onto panel...")
    if not behavioral_parts:
        raise ValueError(
            "No closure-period groups produced features. Check that closures are "
            "filtered to closure_start >= 2020-09-01."
        )
    behavioral_df = pd.concat(behavioral_parts, ignore_index=True)
    merge_keys    = ["member_id", "dept_id", "closure_start", "period_start"]
    result        = panel.merge(behavioral_df, on=merge_keys, how="left")
    n_unmatched   = result[result["total_purchase_days_pre"].isna()].shape[0]
    if n_unmatched > 0:
        raise ValueError(
            f"{n_unmatched:,} panel rows could not be matched to behavioral features "
            "after merge. Check that all (dept_id, closure_start, period_start) groups "
            "were processed without gaps."
        )
    result = result.merge(demo_df, on="member_id", how="left")
    result.drop(columns=["_closure_start_dt"], inplace=True, errors="ignore")

    # Final NaN validation
    _exclude = {"member_id", "dept_id", "closure_start", "closure_end",
                "period", "group", "label", "is_treated", "period_end"}
    feature_cols_final = [c for c in result.columns if c not in _exclude]
    nan_summary = result[feature_cols_final].isna().sum()
    nan_cols    = nan_summary[nan_summary > 0]
    if not nan_cols.empty:
        details = "\n".join(f"  {col}: {count} NaN" for col, count in nan_cols.items())
        raise ValueError(
            f"NaN values found in feature matrix after all joins — indicates a data "
            f"processing bug. Affected columns:\n{details}\n"
            "Fix the upstream data issue; do not paper over with fillna."
        )

    log_print(logger, f"  Done. Feature matrix: {result.shape[0]:,} rows × {result.shape[1]:,} columns")
    return result
