from __future__ import annotations

import json
import logging
import os
import time
from pathlib import Path

import numpy as np
import pandas as pd


LOGGER = logging.getLogger("displacement_effect_estimation")

_VARIETY_SEEKING_MODES = frozenset({"distinct", "instance", "distinct-only-new"})

_BASE_OUTPUT_COLS = [
    "member_id",
    "dept_id",
    "closure_start",
    "closure_end",
    "closure_duration_days",
    "group",
    "treated",
    "displacement_prob",
    "disp_binary",
    "closure_event_id",
    "period_start",
    "calendar_month",
    "rel_t",
    "post",
]


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_config() -> dict:
    cfg_path = Path(__file__).resolve().parent / "config.json"
    with open(cfg_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _normalize_closure_start(s: pd.Series) -> pd.Series:
    return pd.to_datetime(s, errors="coerce").dt.strftime("%Y-%m-%d")


def _detect_data_dir(project_root: Path) -> Path:
    candidates = [
        project_root.parent / "data" / "data1031",
        project_root / "data" / "data1031",
    ]
    for p in candidates:
        if (p / "order_result.csv").exists():
            return p
    return candidates[0]


def load_t0_feature_recency(cfg: dict | None = None) -> pd.DataFrame:
    cfg = cfg or load_config()
    project_root = get_project_root()
    paths_cfg = cfg["paths"]
    cache_dir = project_root / paths_cfg["feature_t0_cache_dir"]
    cache_key = paths_cfg["feature_cache_key"]
    cache_path = cache_dir / f"features_t0_{cache_key}.parquet"
    if not cache_path.exists():
        raise FileNotFoundError(
            f"T0 feature cache not found: {cache_path}. "
            "Update paths.feature_cache_key in displacement_effect_estimation/config.json."
        )

    recency_df = pd.read_parquet(
        cache_path,
        columns=["member_id", "dept_id", "closure_start", "period", "days_since_last_purchase"],
    )
    required = {"member_id", "dept_id", "closure_start", "period", "days_since_last_purchase"}
    missing = required - set(recency_df.columns)
    if missing:
        raise ValueError(
            f"Missing required columns in {cache_path.name}: {sorted(missing)}"
        )

    recency_df = recency_df[recency_df["period"] == 0].copy()
    if recency_df.empty:
        raise ValueError(
            f"No period=0 rows found in {cache_path.name}. "
            "Expected ex-ante t0 feature cache rows."
        )

    key_cols = ["member_id", "dept_id", "closure_start"]
    recency_df = (
        recency_df.assign(
            closure_start=_normalize_closure_start(recency_df["closure_start"]),
            days_since_last_purchase=recency_df["days_since_last_purchase"].astype(int),
        )
        .sort_values(key_cols)
        .drop_duplicates(subset=key_cols, keep="first")
        .loc[:, key_cols + ["days_since_last_purchase"]]
    )
    return recency_df


def load_displacement_scores(cfg: dict | None = None) -> pd.DataFrame:
    cfg = cfg or load_config()
    project_root = get_project_root()
    score_path = project_root / cfg["paths"]["score_file"]
    closure_registry_rel = os.environ.get(
        "DISPLACEMENT_EFFECT_CLOSURE_REGISTRY",
        cfg["paths"].get("closure_registry_file", "outputs/customer-store/closure_pair_registry.csv"),
    )
    closure_registry_path = project_root / closure_registry_rel
    if not score_path.exists():
        raise FileNotFoundError(
            f"Ex-ante score file not found: {score_path}. "
            "Run displacement_classification/main.py first to generate displacement_scores_t0_ex_ante.csv."
        )
    if not closure_registry_path.exists():
        raise FileNotFoundError(
            f"Closure registry not found: {closure_registry_path}. "
            "Run customer-store/main_customer_store.py first to generate closure_pair_registry.csv."
        )

    score_df = pd.read_csv(score_path, encoding="utf-8-sig")
    required = {
        "member_id",
        "dept_id",
        "closure_start",
        "closure_end",
        "closure_duration_days",
        "group",
        "is_treated",
        "displacement_prob_t0_ex_ante",
        "predicted_displaced_t0_ex_ante",
    }
    missing = required - set(score_df.columns)
    if missing:
        raise ValueError(f"Missing required columns in {score_path.name}: {sorted(missing)}")

    key_cols = ["member_id", "dept_id", "closure_start"]
    score_df = (
        score_df.assign(
            displacement_prob=score_df["displacement_prob_t0_ex_ante"].astype(float),
            closure_start=_normalize_closure_start(score_df["closure_start"]),
            closure_end=pd.to_datetime(score_df["closure_end"], errors="coerce").dt.strftime("%Y-%m-%d"),
        )
        .sort_values(key_cols)
        .drop_duplicates(subset=key_cols, keep="first")
        .loc[
            :,
            key_cols
            + [
                "closure_end",
                "closure_duration_days",
                "group",
                "is_treated",
                "displacement_prob",
                "predicted_displaced_t0_ex_ante",
            ],
        ]
    )

    registry_df = pd.read_csv(closure_registry_path, encoding="utf-8-sig")
    registry_required = {"dept_id", "closure_start", "closure_end"}
    registry_missing = registry_required - set(registry_df.columns)
    if registry_missing:
        raise ValueError(
            f"Missing required columns in {closure_registry_path.name}: {sorted(registry_missing)}"
        )

    closure_scope = (
        registry_df.assign(
            closure_start=_normalize_closure_start(registry_df["closure_start"]),
            closure_end=pd.to_datetime(registry_df["closure_end"], errors="coerce").dt.strftime("%Y-%m-%d"),
            _dept_key=registry_df["dept_id"].astype(str),
        )[["_dept_key", "closure_start", "closure_end"]]
        .dropna(subset=["_dept_key", "closure_start", "closure_end"])
        .drop_duplicates()
    )

    closure_count_before = score_df[["dept_id", "closure_start", "closure_end"]].drop_duplicates().shape[0]
    score_df = score_df.assign(_dept_key=score_df["dept_id"].astype(str)).merge(
        closure_scope,
        on=["_dept_key", "closure_start", "closure_end"],
        how="inner",
    )
    score_df = score_df.drop(columns=["_dept_key"])
    closure_count_after = score_df[["dept_id", "closure_start", "closure_end"]].drop_duplicates().shape[0]
    LOGGER.info(
        "Applied closure registry filter using %s: closures %s -> %s (dropped=%s)",
        closure_registry_path,
        closure_count_before,
        closure_count_after,
        closure_count_before - closure_count_after,
    )
    if closure_count_after == 0:
        raise ValueError(
            "Closure registry filter removed all displacement score closures. "
            "Check key consistency between displacement scores and closure_pair_registry.csv."
        )

    recency_df = load_t0_feature_recency(cfg=cfg)
    score_df = score_df.merge(recency_df, on=key_cols, how="left", validate="one_to_one")
    missing_recency = score_df[score_df["days_since_last_purchase"].isna()]
    if not missing_recency.empty:
        raise ValueError(
            f"Missing days_since_last_purchase for {len(missing_recency)} scored rows after "
            f"merging feature cache {cfg['paths']['feature_cache_key']}. "
            "Check that the score file and feature cache come from the same classification run."
        )

    score_df["treated"] = score_df["is_treated"].astype(int)
    score_df["closure_duration_days"] = score_df["closure_duration_days"].astype(int)
    score_df["disp_binary"] = score_df["predicted_displaced_t0_ex_ante"].astype(int)
    score_df["days_since_last_purchase"] = score_df["days_since_last_purchase"].astype(int)
    return score_df


def load_orders_for_behavior(cfg: dict | None = None) -> pd.DataFrame:
    cfg = cfg or load_config()
    project_root = get_project_root()
    data_dir = _detect_data_dir(project_root)
    path = data_dir / "order_result.csv"
    if not path.exists():
        raise FileNotFoundError(f"order_result.csv not found: {path}")

    df = pd.read_csv(path, encoding="utf-8-sig", usecols=["member_id", "create_hour"])
    df["dt"] = pd.to_datetime(df["create_hour"], errors="coerce")
    df = df.dropna(subset=["dt"]).copy()
    df["date"] = df["dt"].dt.normalize()
    df = df[["member_id", "date"]].drop_duplicates()
    return df.sort_values("date").reset_index(drop=True)


def load_orders_for_behavior_members(
    member_ids: set,
    cfg: dict | None = None,
    chunksize: int = 1_000_000,
) -> pd.DataFrame:
    cfg = cfg or load_config()
    project_root = get_project_root()
    data_dir = _detect_data_dir(project_root)
    path = data_dir / "order_result.csv"
    if not path.exists():
        raise FileNotFoundError(f"order_result.csv not found: {path}")

    if not member_ids:
        return pd.DataFrame(columns=["member_id", "date"])

    frames: list[pd.DataFrame] = []
    for chunk in pd.read_csv(
        path,
        encoding="utf-8-sig",
        usecols=["member_id", "create_hour"],
        chunksize=chunksize,
    ):
        chunk = chunk[chunk["member_id"].isin(member_ids)]
        if chunk.empty:
            continue
        chunk["dt"] = pd.to_datetime(chunk["create_hour"], errors="coerce")
        chunk = chunk.dropna(subset=["dt"])
        if chunk.empty:
            continue
        chunk["date"] = chunk["dt"].dt.normalize()
        frames.append(chunk[["member_id", "date"]])

    if not frames:
        return pd.DataFrame(columns=["member_id", "date"])

    df = pd.concat(frames, ignore_index=True)
    df = df.drop_duplicates()
    return df.sort_values("date").reset_index(drop=True)


def load_commodity_orders_for_members(
    member_ids: set,
    cfg: dict | None = None,
    chunksize: int = 1_000_000,
) -> pd.DataFrame:
    """Load order_commodity_result_processed.csv for the given member IDs.

    Returns a DataFrame with columns [member_id, date, product_id], sorted by date.
    Covers the full date range in the file (all historical purchases).
    """
    cfg = cfg or load_config()
    project_root = get_project_root()
    rel_path = cfg.get("paths", {}).get(
        "commodity_processed_file",
        "data/processed/order_commodity_result_processed.csv",
    )
    path = project_root / rel_path
    if not path.exists():
        raise FileNotFoundError(
            f"Processed commodity file not found: {path}. "
            "Expected columns: member_id, dt, product_id."
        )
    if not member_ids:
        return pd.DataFrame(columns=["member_id", "date", "product_id"])

    frames: list[pd.DataFrame] = []
    for chunk in pd.read_csv(
        path,
        encoding="utf-8-sig",
        usecols=["member_id", "dt", "product_id"],
        chunksize=chunksize,
    ):
        chunk = chunk[chunk["member_id"].isin(member_ids)]
        if chunk.empty:
            continue
        chunk["date"] = pd.to_datetime(chunk["dt"], errors="coerce").dt.normalize()
        chunk = chunk.dropna(subset=["date"])
        if chunk.empty:
            continue
        frames.append(chunk[["member_id", "date", "product_id"]].dropna())

    if not frames:
        return pd.DataFrame(columns=["member_id", "date", "product_id"])

    df = pd.concat(frames, ignore_index=True)
    df["product_id"] = df["product_id"].astype(int)
    return df.sort_values("date").reset_index(drop=True)


def load_product_first_seen_dates(
    cfg: dict | None = None,
    chunksize: int = 1_000_000,
) -> pd.DataFrame:
    """Load earliest observed purchase date per product from the full commodity file."""
    cfg = cfg or load_config()
    project_root = get_project_root()
    rel_path = cfg.get("paths", {}).get(
        "commodity_processed_file",
        "data/processed/order_commodity_result_processed.csv",
    )
    path = project_root / rel_path
    if not path.exists():
        raise FileNotFoundError(
            f"Processed commodity file not found: {path}. "
            "Expected columns: dt, product_id."
        )

    first_seen_by_product: dict[int, pd.Timestamp] = {}
    for chunk in pd.read_csv(
        path,
        encoding="utf-8-sig",
        usecols=["dt", "product_id"],
        chunksize=chunksize,
    ):
        chunk["date"] = pd.to_datetime(chunk["dt"], errors="coerce").dt.normalize()
        chunk = chunk.dropna(subset=["date", "product_id"])
        if chunk.empty:
            continue
        chunk["product_id"] = chunk["product_id"].astype(int)
        chunk_min = chunk.groupby("product_id", sort=False)["date"].min()
        for product_id, first_seen in chunk_min.items():
            previous = first_seen_by_product.get(product_id)
            if previous is None or first_seen < previous:
                first_seen_by_product[product_id] = first_seen

    if not first_seen_by_product:
        return pd.DataFrame(columns=["product_id", "product_first_date"])

    return pd.DataFrame(
        {
            "product_id": list(first_seen_by_product.keys()),
            "product_first_date": list(first_seen_by_product.values()),
        }
    )


def _compute_first_purchase_dates(commodity_df: pd.DataFrame) -> pd.DataFrame:
    """Return (member_id, product_id, first_date): the earliest purchase date per member-product pair."""
    return (
        commodity_df.groupby(["member_id", "product_id"], sort=False)["date"]
        .min()
        .reset_index()
        .rename(columns={"date": "first_date"})
    )


def _compute_product_first_seen_dates(commodity_df: pd.DataFrame) -> pd.DataFrame:
    """Return (product_id, product_first_date): earliest observed purchase date per product."""
    return (
        commodity_df.groupby("product_id", sort=False)["date"]
        .min()
        .reset_index()
        .rename(columns={"date": "product_first_date"})
    )


def _compute_variety_seeking_for_window(
    commodity_df: pd.DataFrame,
    first_purchase_df: pd.DataFrame,
    members: set,
    start_dt: pd.Timestamp,
    end_dt: pd.Timestamp,
    mode: str = "distinct",
    product_first_seen_df: pd.DataFrame | None = None,
    prev_window_start: pd.Timestamp | None = None,
    prev_window_end: pd.Timestamp | None = None,
) -> pd.DataFrame:
    """Compute variety_seeking for all members in one period window.

    variety_seeking = |new products in window| / |products in window|,
    where a product is "new" if the member's first-ever purchase of it is on or
    after start_dt (i.e., never seen before this period).

    mode="distinct" (default):
        Both numerator and denominator use set cardinality — each product_id
        counted once per member per window regardless of purchase frequency.
    mode="instance":
        Both numerator and denominator count individual purchase rows — buying
        the same product k times contributes k to both numerator and denominator.
    mode="distinct-only-new":
        Among distinct product_ids purchased in [start_dt, end_dt], share whose
        global first-sale date lies in that same window or, when provided, in the
        adjacent previous panel window [prev_window_start, prev_window_end]. When
        no previous window is passed (leftmost pre bin), only the current window
        is used.

    Returns DataFrame[member_id, variety_seeking].
    Members with no purchases in the window receive NaN.
    """
    if mode not in _VARIETY_SEEKING_MODES:
        raise ValueError(
            f"variety_seeking_mode must be one of {sorted(_VARIETY_SEEKING_MODES)}; got '{mode}'."
        )

    win = _slice_by_date(commodity_df, start_dt, end_dt)
    if not win.empty:
        win = win[win["member_id"].isin(members)]

    all_members = pd.DataFrame({"member_id": list(members)})

    if win.empty:
        all_members["variety_seeking"] = np.nan
        return all_members

    if mode == "distinct-only-new":
        if product_first_seen_df is None:
            raise ValueError("distinct-only-new mode requires product_first_seen_df.")
        win_prods = win[["member_id", "product_id"]].drop_duplicates()
        win_prods = win_prods.merge(product_first_seen_df, on="product_id", how="left")
        pdt = pd.to_datetime(win_prods["product_first_date"], errors="coerce")
        in_curr = (pdt >= start_dt) & (pdt <= end_dt)
        if prev_window_start is not None and prev_window_end is not None:
            in_prev = (pdt >= prev_window_start) & (pdt <= prev_window_end)
            is_new = (in_curr | in_prev).fillna(False).astype(int)
        else:
            is_new = in_curr.fillna(False).astype(int)
        win_prods["is_new"] = is_new
        agg = (
            win_prods.groupby("member_id", sort=False)
            .agg(total_prods=("product_id", "count"), new_prods=("is_new", "sum"))
            .reset_index()
        )
        agg["variety_seeking"] = agg["new_prods"] / agg["total_prods"]
        return all_members.merge(agg[["member_id", "variety_seeking"]], on="member_id", how="left")

    win_prods = win[["member_id", "product_id"]].copy()
    if mode == "distinct":
        # Each product counted once per member — set cardinality
        win_prods = win_prods.drop_duplicates()

    # Join with global first-purchase dates; flag as new when first_date >= start_dt
    win_prods = win_prods.merge(first_purchase_df, on=["member_id", "product_id"], how="left")
    win_prods["is_new"] = (win_prods["first_date"] >= start_dt).astype(int)

    agg = (
        win_prods.groupby("member_id", sort=False)
        .agg(total_prods=("product_id", "count"), new_prods=("is_new", "sum"))
        .reset_index()
    )
    agg["variety_seeking"] = agg["new_prods"] / agg["total_prods"]

    return all_members.merge(agg[["member_id", "variety_seeking"]], on="member_id", how="left")


def _slice_by_date(sorted_df: pd.DataFrame, start_date: pd.Timestamp, end_date: pd.Timestamp) -> pd.DataFrame:
    if end_date < start_date:
        return sorted_df.iloc[0:0]
    date_arr = sorted_df["date"].values
    left = np.searchsorted(date_arr, start_date.to_datetime64(), side="left")
    right = np.searchsorted(date_arr, end_date.to_datetime64(), side="right")
    return sorted_df.iloc[left:right]


def _previous_rel_t_in_variety_panel(rel_t: int, *, t_horizon: int) -> int | None:
    """Chronological predecessor in [-K..-1] + [1..K] (no rel_t=0 in the panel)."""
    if t_horizon < 1:
        raise ValueError("t_horizon must be >= 1.")
    seq = list(range(-t_horizon, 0)) + list(range(1, t_horizon + 1))
    if rel_t not in seq:
        raise ValueError(f"rel_t={rel_t} not in panel sequence for t_horizon={t_horizon}.")
    idx = seq.index(rel_t)
    if idx == 0:
        return None
    return int(seq[idx - 1])


def _window_bounds(closure_start: pd.Timestamp, closure_end: pd.Timestamp, rel_t: int, bin_days: int) -> tuple[pd.Timestamp, pd.Timestamp]:
    if rel_t < 0:
        start = closure_start + pd.Timedelta(days=rel_t * bin_days)
        end = start + pd.Timedelta(days=bin_days - 1)
        return start, end

    post_anchor = closure_end + pd.Timedelta(days=1)
    start = post_anchor + pd.Timedelta(days=(rel_t - 1) * bin_days)
    end = start + pd.Timedelta(days=bin_days - 1)
    return start, end


def _resolve_recency_days(
    *,
    separate_effect: bool,
    select_recency_consumers: bool | int,
) -> int | None:
    if isinstance(select_recency_consumers, bool):
        if select_recency_consumers:
            raise ValueError("select_recency_consumers must be a positive integer or false.")
        return None

    recency_days = int(select_recency_consumers)
    if recency_days < 1:
        raise ValueError("select_recency_consumers must be >= 1 when provided.")
    if not separate_effect:
        raise ValueError("select_recency_consumers can only be set when separate_effect=true.")
    return recency_days


def _resolve_closure_duration_days(
    *,
    closure_duration_days: bool | int,
) -> int | None:
    if isinstance(closure_duration_days, bool):
        if closure_duration_days:
            raise ValueError("closure_duration_days must be a positive integer or false.")
        return None

    duration_days = int(closure_duration_days)
    if duration_days < 1:
        raise ValueError("closure_duration_days must be >= 1 when provided.")
    return duration_days


def _filter_members_by_recency(
    *,
    member_frame: pd.DataFrame,
    recency_days: int | None,
) -> pd.DataFrame:
    if recency_days is None:
        return member_frame

    if "days_since_last_purchase" not in member_frame.columns:
        raise ValueError(
            "member_frame is missing days_since_last_purchase. "
            "Merge t0 feature-cache recency fields before applying recency filtering."
        )
    return member_frame[member_frame["days_since_last_purchase"] < recency_days].copy()


def _filter_members_with_period0_purchases(
    *,
    member_frame: pd.DataFrame,
    commodity_df: pd.DataFrame,
    closure_start_dt: pd.Timestamp,
    closure_end_dt: pd.Timestamp,
) -> tuple[pd.DataFrame, int, int]:
    """Apply period-0 selection for clean treatment contrast.

    - Treated members: drop if they purchased during period 0.
    - Control members: keep only if they purchased during period 0.
    """
    period0_orders = _slice_by_date(
        sorted_df=commodity_df,
        start_date=closure_start_dt,
        end_date=closure_end_dt,
    )
    if period0_orders.empty:
        is_control = member_frame["treated"] == 0
        dropped_control_no_p0 = int(is_control.sum())
        filtered = member_frame[~is_control].copy()
        return filtered, 0, dropped_control_no_p0

    period0_member_ids = set(period0_orders["member_id"].dropna().tolist())
    if not period0_member_ids:
        is_control = member_frame["treated"] == 0
        dropped_control_no_p0 = int(is_control.sum())
        filtered = member_frame[~is_control].copy()
        return filtered, 0, dropped_control_no_p0

    is_period0_member = member_frame["member_id"].isin(period0_member_ids)
    is_treated = member_frame["treated"] == 1
    is_control = ~is_treated

    drop_treated_p0 = is_treated & is_period0_member
    drop_control_no_p0 = is_control & ~is_period0_member

    dropped_treated_p0 = int(drop_treated_p0.sum())
    dropped_control_no_p0 = int(drop_control_no_p0.sum())
    keep_mask = ~(drop_treated_p0 | drop_control_no_p0)
    return member_frame[keep_mask].copy(), dropped_treated_p0, dropped_control_no_p0


def _build_closure_event_id(*, dept_id: object, closure_start: object) -> str:
    return f"dept_{dept_id}_closure_{closure_start}"


def build_variety_period0_rows(
    *,
    sample: pd.DataFrame,
    cfg: dict | None = None,
    variety_seeking_mode: str = "distinct",
) -> pd.DataFrame:
    """Compute variety_seeking at rel_t=0 for sample member-closure pairs.

    The estimation panel excludes rel_t=0 by design. This helper reconstructs
    the period-0 (closure-window) variety outcome for visualization.
    """
    cfg = cfg or load_config()
    required = {
        "member_id",
        "dept_id",
        "closure_start",
        "closure_end",
        "closure_duration_days",
        "group",
        "treated",
    }
    missing = required - set(sample.columns)
    if missing:
        raise ValueError(f"sample is missing required columns for period-0 build: {sorted(missing)}")

    event_members = sample[
        ["member_id", "dept_id", "closure_start", "closure_end", "closure_duration_days", "group", "treated"]
    ].drop_duplicates()
    if event_members.empty:
        return pd.DataFrame(columns=["member_id", "dept_id", "closure_start", "closure_end", "group", "treated", "rel_t", "variety_seeking"])

    scoped_member_ids = set(event_members["member_id"].dropna().tolist())
    commodity_df = load_commodity_orders_for_members(member_ids=scoped_member_ids, cfg=cfg)
    first_purchase_df = _compute_first_purchase_dates(commodity_df)
    product_first_seen_df = (
        load_product_first_seen_dates(cfg=cfg)
        if variety_seeking_mode == "distinct-only-new"
        else _compute_product_first_seen_dates(commodity_df)
    )

    out_parts: list[pd.DataFrame] = []
    for (dept_id, closure_start, closure_end), frame in event_members.groupby(
        ["dept_id", "closure_start", "closure_end"],
        sort=False,
    ):
        closure_start_dt = pd.to_datetime(closure_start)
        closure_end_dt = pd.to_datetime(closure_end)
        closure_bin_days = int(frame["closure_duration_days"].iloc[0])
        if variety_seeking_mode == "distinct-only-new":
            prev_start, prev_end = _window_bounds(
                closure_start=closure_start_dt,
                closure_end=closure_end_dt,
                rel_t=-1,
                bin_days=closure_bin_days,
            )
        else:
            prev_start, prev_end = None, None
        members = set(frame["member_id"].tolist())
        vs_result = _compute_variety_seeking_for_window(
            commodity_df=commodity_df,
            first_purchase_df=first_purchase_df,
            members=members,
            start_dt=closure_start_dt,
            end_dt=closure_end_dt,
            mode=variety_seeking_mode,
            product_first_seen_df=product_first_seen_df,
            prev_window_start=prev_start,
            prev_window_end=prev_end,
        )
        part = frame.merge(vs_result, on="member_id", how="left")
        part["rel_t"] = 0
        out_parts.append(part)

    if not out_parts:
        return pd.DataFrame(columns=["member_id", "dept_id", "closure_start", "closure_end", "group", "treated", "rel_t", "variety_seeking"])

    return pd.concat(out_parts, ignore_index=True)


def _attach_novelty_pre_heterogeneity_cols(
    *,
    merged: pd.DataFrame,
    outcome_col: str,
    split_method: str,
    customer_median_split: bool,
) -> pd.DataFrame:
    """Episode-level pre mean of outcome, split vs cross-sectional median or mode; inner-merge drops episodes with no valid pre mean."""
    key_cols = ["member_id", "dept_id", "closure_start"]
    sm = str(split_method).lower().strip()
    if sm not in {"median", "mode"}:
        raise ValueError(
            "variety_pre_novelty_split_method in config must be 'median' or 'mode'; "
            f"got {split_method!r}."
        )
    pre = merged.loc[merged["rel_t"] < 0, key_cols + [outcome_col]].copy()
    pre = pre[pre[outcome_col].notna()]
    if pre.empty:
        raise ValueError(
            "No pre-period rows with non-missing outcome; cannot compute pre-novelty heterogeneity split."
        )
    episode_means = (
        pre.groupby(key_cols, sort=False)[outcome_col].mean().rename("novelty_pre_mean")
    )
    valid_means = episode_means.dropna()
    if valid_means.empty:
        raise ValueError("Episode pre-novelty means are all missing.")

    ep_df_full = episode_means.reset_index()
    if customer_median_split:
        if sm == "median":
            thresh = float(valid_means.median())
        else:
            rounded = valid_means.round(decimals=10)
            modes = rounded.mode(dropna=True)
            thresh = float(modes.iloc[0]) if len(modes) > 0 else float(valid_means.median())
        ep_df_full["novelty_pre_selected_for_heterogeneity"] = 1
        ep_df_full["novelty_pre_high"] = (ep_df_full["novelty_pre_mean"] > thresh).astype(int)
        ep_df_full["novelty_pre_group"] = np.where(ep_df_full["novelty_pre_high"] == 1, "high", "baseline")
        ep_df_full["novelty_pre_split_rule"] = f"{sm}_full_sample"
        ep_df_full["novelty_pre_threshold_low"] = thresh
        ep_df_full["novelty_pre_threshold_high"] = thresh
        ep_df = ep_df_full.copy()
        dropped_middle = 0
    else:
        thresh_low = float(valid_means.quantile(0.25))
        thresh_high = float(valid_means.quantile(0.75))
        lower_mask = ep_df_full["novelty_pre_mean"] <= thresh_low
        upper_mask = ep_df_full["novelty_pre_mean"] >= thresh_high
        keep_mask = lower_mask | upper_mask
        dropped_middle = int((~keep_mask).sum())
        ep_df_full["novelty_pre_selected_for_heterogeneity"] = keep_mask.astype(int)
        ep_df_full["novelty_pre_group"] = np.where(
            lower_mask,
            "baseline",
            np.where(upper_mask, "high", "middle"),
        )
        ep_df_full["novelty_pre_split_rule"] = "quartile_tails"
        ep_df_full["novelty_pre_threshold_low"] = thresh_low
        ep_df_full["novelty_pre_threshold_high"] = thresh_high
        ep_df = ep_df_full.loc[keep_mask].copy()
        ep_df["novelty_pre_high"] = upper_mask.loc[ep_df.index].astype(int)

    n_ep = int(ep_df["novelty_pre_mean"].notna().sum())
    n_hi = int((ep_df["novelty_pre_high"] == 1).sum())
    n_baseline = int((ep_df["novelty_pre_high"] == 0).sum())
    out = merged.merge(ep_df, on=key_cols, how="inner")
    out.attrs["pre_novelty_distribution"] = ep_df_full.copy()
    LOGGER.info(
        "Pre-novelty heterogeneity: customer_median_split=%s split_method=%s threshold_low=%s "
        "threshold_high=%s episode_rows=%s n_baseline_episodes=%s n_high_episodes=%s "
        "dropped_middle_episodes=%s panel_rows_before=%s panel_rows_after=%s",
        customer_median_split,
        sm,
        repr(float(ep_df["novelty_pre_threshold_low"].iloc[0])),
        repr(float(ep_df["novelty_pre_threshold_high"].iloc[0])),
        f"{n_ep:,}",
        f"{n_baseline:,}",
        f"{n_hi:,}",
        f"{dropped_middle:,}",
        f"{len(merged):,}",
        f"{len(out):,}",
    )
    if out.empty:
        raise ValueError("Sample empty after merging pre-novelty heterogeneity columns.")
    return out


def build_estimation_sample(
    outcome: str,
    cfg: dict | None = None,
    t_horizon: int | None = None,
    closure_duration_days: bool | int | None = None,
    separate_effect: bool | None = None,
    select_recency_consumers: bool | int | None = None,
    require_balanced_panel: bool | None = None,
    variety_seeking_mode: str = "distinct",
    drop_period0_purchasers: bool | None = None,
    unbalanced_panel: bool | None = None,
    variety_pre_novelty_heterogeneity: bool = False,
    customer_median_split: bool = True,
) -> pd.DataFrame:
    cfg = cfg or load_config()
    _SUPPORTED_OUTCOMES = frozenset({"n_purchases", "purchase_incidence_binary", "variety_seeking"})
    if outcome not in _SUPPORTED_OUTCOMES:
        raise ValueError(
            f"Unsupported outcome '{outcome}'. Must be one of {sorted(_SUPPORTED_OUTCOMES)}."
        )
    # For variety_seeking, default is unbalanced (DDD): keep member-period rows even when
    # variety_seeking is missing in some periods. Pass require_balanced_panel=True for DiD.
    if require_balanced_panel is None:
        _require_balanced_panel = False
    else:
        _require_balanced_panel = bool(require_balanced_panel)

    if drop_period0_purchasers is None:
        _drop_period0_purchasers = outcome == "variety_seeking" and _require_balanced_panel
    else:
        _drop_period0_purchasers = bool(drop_period0_purchasers)

    # unbalanced_panel controls the n_purchases panel structure.
    # Default True (unbalanced) keeps all members; False restricts to
    # members who purchased in every pre-period (balanced).
    if unbalanced_panel is None:
        _unbalanced_panel = True
    else:
        _unbalanced_panel = bool(unbalanced_panel)

    spec_cfg = cfg.get("spec", {})
    if closure_duration_days is None:
        closure_duration_days = spec_cfg.get("closure_duration_days", False)
    if separate_effect is None:
        separate_effect = bool(spec_cfg.get("separate_effect", False))
    if select_recency_consumers is None:
        select_recency_consumers = spec_cfg.get("select_recency_consumers", False)
    duration_days_filter = _resolve_closure_duration_days(
        closure_duration_days=closure_duration_days,
    )
    recency_days = _resolve_recency_days(
        separate_effect=separate_effect,
        select_recency_consumers=select_recency_consumers,
    )

    scores = load_displacement_scores(cfg=cfg)
    if duration_days_filter is not None:
        scores = scores[scores["closure_duration_days"] == duration_days_filter].copy()
        if scores.empty:
            raise ValueError(
                f"No scored rows remain after filtering closure_duration_days == {duration_days_filter}."
            )
    if recency_days is None:
        scoped_member_ids = set(scores["member_id"].dropna().tolist())
    else:
        scoped_member_ids = set(
            scores.loc[scores["days_since_last_purchase"] < recency_days, "member_id"].dropna().tolist()
        )
    if outcome in {"n_purchases", "purchase_incidence_binary"}:
        orders = load_orders_for_behavior_members(member_ids=scoped_member_ids, cfg=cfg)
        commodity_df: pd.DataFrame | None = None
        first_purchase_df: pd.DataFrame | None = None
    else:  # variety_seeking
        orders = None
        commodity_df = load_commodity_orders_for_members(member_ids=scoped_member_ids, cfg=cfg)
        first_purchase_df = _compute_first_purchase_dates(commodity_df)
        product_first_seen_df = (
            load_product_first_seen_dates(cfg=cfg)
        if variety_seeking_mode == "distinct-only-new"
        else _compute_product_first_seen_dates(commodity_df)
        )
        if variety_seeking_mode not in _VARIETY_SEEKING_MODES:
            raise ValueError(
                f"variety_seeking_mode must be one of {sorted(_VARIETY_SEEKING_MODES)}; got '{variety_seeking_mode}'."
            )
        LOGGER.info(
            "Loaded commodity orders: %s rows, %s member-product pairs, %s products, variety_seeking_mode=%s",
            f"{len(commodity_df):,}",
            f"{len(first_purchase_df):,}",
            f"{len(product_first_seen_df):,}",
            variety_seeking_mode,
        )

    if t_horizon is None:
        t_horizon = int(cfg.get("spec", {}).get("t_horizon", 4))
    if t_horizon < 1:
        raise ValueError("t_horizon must be >= 1")

    rel_t_values = list(range(-t_horizon, 0)) + list(range(1, t_horizon + 1))

    scores = scores.copy()
    scores["closure_start_dt"] = pd.to_datetime(scores["closure_start"])
    scores["closure_end_dt"] = pd.to_datetime(scores["closure_end"])

    out_parts: list[pd.DataFrame] = []
    group_cols = ["dept_id", "closure_start", "closure_end"]
    grouped_closures = list(scores.groupby(group_cols, sort=False))
    total_closures = len(grouped_closures)
    loop_start = time.perf_counter()
    LOGGER.info(
        "Starting closure loop: total_closures=%s closure_duration_days=%s",
        total_closures,
        duration_days_filter if duration_days_filter is not None else "all",
    )

    for closure_idx, ((dept_id, closure_start, closure_end), closure_cohort) in enumerate(grouped_closures, start=1):
        closure_start_time = time.perf_counter()
        closure_start_dt = pd.to_datetime(closure_start)
        closure_end_dt = pd.to_datetime(closure_end)
        closure_bin_days = int(closure_cohort["closure_duration_days"].iloc[0])
        if closure_bin_days < 1:
            LOGGER.info(
                "Closure %s/%s skipped: dept_id=%s closure_start=%s invalid_duration=%s",
                closure_idx,
                total_closures,
                dept_id,
                closure_start,
                closure_bin_days,
            )
            continue

        member_frame = closure_cohort[
            [
                "member_id",
                "dept_id",
                "closure_start",
                "closure_end",
                "closure_duration_days",
                "group",
                "treated",
                "displacement_prob",
                "disp_binary",
                "days_since_last_purchase",
            ]
        ].drop_duplicates()
        member_frame = _filter_members_by_recency(
            member_frame=member_frame,
            recency_days=recency_days,
        )
        period0_treated_dropped = 0
        period0_control_no_purchase_dropped = 0
        if outcome == "variety_seeking" and _drop_period0_purchasers:
            member_frame, period0_treated_dropped, period0_control_no_purchase_dropped = _filter_members_with_period0_purchases(
                member_frame=member_frame,
                commodity_df=commodity_df,
                closure_start_dt=closure_start_dt,
                closure_end_dt=closure_end_dt,
            )
        if member_frame.empty:
            LOGGER.info(
                "Closure %s/%s skipped: dept_id=%s closure_start=%s recency_days=%s "
                "period0_treated_dropped=%s period0_control_no_purchase_dropped=%s selected_members=%s",
                closure_idx,
                total_closures,
                dept_id,
                closure_start,
                recency_days,
                period0_treated_dropped,
                period0_control_no_purchase_dropped,
                0,
            )
            continue

        member_frame = member_frame.assign(
            closure_event_id=_build_closure_event_id(dept_id=dept_id, closure_start=closure_start)
        )
        members = set(member_frame["member_id"].tolist())
        closure_parts: list[pd.DataFrame] = []

        for rel_t in rel_t_values:
            start_dt, end_dt = _window_bounds(
                closure_start=closure_start_dt,
                closure_end=closure_end_dt,
                rel_t=rel_t,
                bin_days=closure_bin_days,
            )

            prev_start: pd.Timestamp | None = None
            prev_end: pd.Timestamp | None = None
            if outcome == "variety_seeking" and variety_seeking_mode == "distinct-only-new":
                prev_rel = _previous_rel_t_in_variety_panel(rel_t, t_horizon=t_horizon)
                if prev_rel is not None:
                    prev_start, prev_end = _window_bounds(
                        closure_start=closure_start_dt,
                        closure_end=closure_end_dt,
                        rel_t=prev_rel,
                        bin_days=closure_bin_days,
                    )

            if outcome in {"n_purchases", "purchase_incidence_binary"}:
                win_orders = _slice_by_date(sorted_df=orders, start_date=start_dt, end_date=end_dt)
                if not win_orders.empty:
                    win_orders = win_orders[win_orders["member_id"].isin(members)]
                    counts = (
                        win_orders.groupby("member_id")["date"].nunique().rename("_purchase_days").reset_index()
                    )
                else:
                    counts = pd.DataFrame(columns=["member_id", "_purchase_days"])
                block = member_frame.merge(counts, on="member_id", how="left")
                block["_purchase_days"] = block["_purchase_days"].fillna(0)
                if outcome == "n_purchases":
                    block["n_purchases"] = block["_purchase_days"] / float(closure_bin_days)
                else:
                    block["purchase_incidence_binary"] = (block["_purchase_days"] > 0).astype(int)
            else:  # variety_seeking
                vs_result = _compute_variety_seeking_for_window(
                    commodity_df=commodity_df,
                    first_purchase_df=first_purchase_df,
                    members=members,
                    start_dt=start_dt,
                    end_dt=end_dt,
                    mode=variety_seeking_mode,
                    product_first_seen_df=product_first_seen_df,
                    prev_window_start=prev_start,
                    prev_window_end=prev_end,
                )
                block = member_frame.merge(vs_result, on="member_id", how="left")

            block["rel_t"] = int(rel_t)
            block["post"] = (block["rel_t"] > 0).astype(int)
            block["period_start"] = start_dt
            block["calendar_month"] = start_dt.strftime("%Y-%m")
            closure_parts.append(block[_BASE_OUTPUT_COLS + [outcome]])

        # Balanced-panel filter.
        # variety_seeking + balanced: drop members missing any period (NaN check).
        # n_purchases + balanced: keep only members with purchases in every pre-period.
        _apply_filter = False
        if outcome == "variety_seeking" and _require_balanced_panel and closure_parts:
            _apply_filter = True
            _filter_kind = "variety_nan"
        elif outcome == "n_purchases" and not _unbalanced_panel and closure_parts:
            _apply_filter = True
            _filter_kind = "purchases_pre"

        if _apply_filter:
            closure_df = pd.concat(closure_parts, ignore_index=True)
            if _filter_kind == "variety_nan":
                has_all_periods = closure_df.groupby("member_id")[outcome].transform(
                    lambda x: x.notna().all()
                )
                closure_df = closure_df[has_all_periods]
            else:  # purchases_pre: keep members with n_purchases > 0 in every pre-period
                pre_mask = closure_df["rel_t"] < 0
                pre_df = closure_df[pre_mask]
                if not pre_df.empty:
                    member_valid = pre_df.groupby("member_id")[outcome].apply(
                        lambda x: (x > 0).all()
                    )
                    valid_members = set(member_valid[member_valid].index)
                    closure_df = closure_df[closure_df["member_id"].isin(valid_members)]
            closure_rows = len(closure_df)
            if not closure_df.empty:
                out_parts.append(closure_df)
        else:
            out_parts.extend(closure_parts)
            closure_rows = sum(len(p) for p in closure_parts)

        LOGGER.info(
            "Closure %s/%s done: dept_id=%s closure_start=%s members=%s rows=%s duration_days=%s "
            "period0_treated_dropped=%s period0_control_no_purchase_dropped=%s elapsed=%.2fs",
            closure_idx,
            total_closures,
            dept_id,
            closure_start,
            len(members),
            closure_rows,
            closure_bin_days,
            period0_treated_dropped,
            period0_control_no_purchase_dropped,
            time.perf_counter() - closure_start_time,
        )

    LOGGER.info("Closure loop completed in %.2fs", time.perf_counter() - loop_start)

    if not out_parts:
        raise ValueError("No estimation rows were constructed from score cohort and orders.")

    merged = pd.concat(out_parts, ignore_index=True)
    merged["event_fe_id"] = (
        merged["member_id"].astype(str)
        + "|"
        + merged["dept_id"].astype(str)
        + "|"
        + merged["closure_start"].astype(str)
    )
    merged["treated"] = merged["treated"].astype(int)
    merged["disp_binary"] = merged["disp_binary"].astype(int)
    merged["closure_duration_days"] = merged["closure_duration_days"].astype(int)
    merged["displacement_prob_centered"] = merged["displacement_prob"] - float(merged["displacement_prob"].mean())

    len_mean = float(merged["closure_duration_days"].mean())
    len_std = float(merged["closure_duration_days"].std(ddof=0))
    if len_std == 0.0:
        merged["closure_length_std"] = 0.0
    else:
        merged["closure_length_std"] = (merged["closure_duration_days"] - len_mean) / len_std

    if variety_pre_novelty_heterogeneity:
        if outcome != "variety_seeking" or variety_seeking_mode != "distinct":
            raise ValueError(
                "variety_pre_novelty_heterogeneity requires outcome='variety_seeking' and "
                "variety_seeking_mode='distinct'."
            )
        split_raw = str(
            cfg.get("spec", {}).get("variety_pre_novelty_split_method", "median")
        )
        merged = _attach_novelty_pre_heterogeneity_cols(
            merged=merged,
            outcome_col=outcome,
            split_method=split_raw,
            customer_median_split=customer_median_split,
        )

    return merged
