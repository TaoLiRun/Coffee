from __future__ import annotations

import json
import logging
import time
from pathlib import Path
import numpy as np
import pandas as pd


LOGGER = logging.getLogger("displacement_effect_estimation")


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


def load_displacement_scores(cfg: dict | None = None) -> pd.DataFrame:
    cfg = cfg or load_config()
    project_root = get_project_root()
    score_path = project_root / cfg["paths"]["score_file"]
    closure_registry_path = project_root / "outputs" / "customer-store" / "closure_pair_registry.csv"
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

    score_df["treated"] = score_df["is_treated"].astype(int)
    score_df["closure_duration_days"] = score_df["closure_duration_days"].astype(int)
    score_df["disp_binary"] = score_df["predicted_displaced_t0_ex_ante"].astype(int)
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

    df = pd.concat(frames, ignore_index=True)
    df = df.drop_duplicates()
    return df.sort_values("date").reset_index(drop=True)


def _slice_by_date(sorted_df: pd.DataFrame, start_date: pd.Timestamp, end_date: pd.Timestamp) -> pd.DataFrame:
    if end_date < start_date:
        return sorted_df.iloc[0:0]
    date_arr = sorted_df["date"].values
    left = np.searchsorted(date_arr, start_date.to_datetime64(), side="left")
    right = np.searchsorted(date_arr, end_date.to_datetime64(), side="right")
    return sorted_df.iloc[left:right]


def _window_bounds(closure_start: pd.Timestamp, closure_end: pd.Timestamp, rel_t: int, bin_days: int) -> tuple[pd.Timestamp, pd.Timestamp]:
    if rel_t < 0:
        start = closure_start + pd.Timedelta(days=rel_t * bin_days)
        end = start + pd.Timedelta(days=bin_days - 1)
        return start, end

    post_anchor = closure_end + pd.Timedelta(days=1)
    start = post_anchor + pd.Timedelta(days=(rel_t - 1) * bin_days)
    end = start + pd.Timedelta(days=bin_days - 1)
    return start, end


def build_estimation_sample(
    outcome: str,
    cfg: dict | None = None,
    t_horizon: int | None = None,
) -> pd.DataFrame:
    cfg = cfg or load_config()
    if outcome != "n_purchases":
        raise ValueError(
            f"Only outcome='n_purchases' is currently supported for event-time construction; got '{outcome}'."
        )

    scores = load_displacement_scores(cfg=cfg)
    scoped_member_ids = set(scores["member_id"].dropna().tolist())
    orders = load_orders_for_behavior_members(member_ids=scoped_member_ids, cfg=cfg)

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
    LOGGER.info("Starting closure loop: total_closures=%s", total_closures)

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
            ]
        ].drop_duplicates()
        members = set(member_frame["member_id"].tolist())
        closure_rows = 0

        for rel_t in rel_t_values:
            start_dt, end_dt = _window_bounds(closure_start_dt, closure_end_dt, rel_t, closure_bin_days)
            win_orders = _slice_by_date(orders, start_dt, end_dt)
            if not win_orders.empty:
                win_orders = win_orders[win_orders["member_id"].isin(members)]
                counts = (
                    win_orders.groupby("member_id")["date"].nunique().rename("_purchase_days").reset_index()
                )
            else:
                counts = pd.DataFrame(columns=["member_id", "_purchase_days"])

            block = member_frame.merge(counts, on="member_id", how="left")
            block["_purchase_days"] = block["_purchase_days"].fillna(0)
            block["n_purchases"] = block["_purchase_days"] / float(closure_bin_days)
            block["rel_t"] = int(rel_t)
            block["post"] = (block["rel_t"] > 0).astype(int)
            block["period_start"] = start_dt
            block["calendar_month"] = start_dt.strftime("%Y-%m")
            out_parts.append(
                block[
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
                        "period_start",
                        "calendar_month",
                        "rel_t",
                        "post",
                        "n_purchases",
                    ]
                ]
            )
            closure_rows += len(block)

        LOGGER.info(
            "Closure %s/%s done: dept_id=%s closure_start=%s members=%s rows=%s duration_days=%s elapsed=%.2fs",
            closure_idx,
            total_closures,
            dept_id,
            closure_start,
            len(members),
            closure_rows,
            closure_bin_days,
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

    return merged
