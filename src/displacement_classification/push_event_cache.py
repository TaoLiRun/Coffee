"""
Load / cache filtered push notification rows and compute push-based features.

Filtered push events (panel members, date range) are written to parquet keyed by
a hash of member set and time bounds so repeated training runs skip CSV ingestion.
"""

from __future__ import annotations

import glob
import hashlib
import json
import logging
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[2]
_data_candidates = [
    PROJECT_ROOT.parent / "data" / "data1031",
    PROJECT_ROOT / "data" / "data1031",
]
DATA_DIR = next(
    (p for p in _data_candidates if (p / "order_result.csv").exists()),
    _data_candidates[0],
)

_NS_PER_DAY = 86400 * 10**9


def _load_config() -> dict:
    with open(SCRIPT_DIR / "config.json", encoding="utf-8") as f:
        return json.load(f)


def _log(logger: logging.Logger, msg: str, level: str = "info") -> None:
    getattr(logger, level)(msg)


def _sanitize_tag_for_column(tag: Any, used: Set[str]) -> str:
    raw = str(tag).strip() if pd.notna(tag) else "na"
    s = re.sub(r"[^a-zA-Z0-9_]+", "_", raw.replace(" ", "_"))
    if not s:
        s = "na"
    if s[0].isdigit():
        s = "t_" + s
    base = s[:100]
    out = base
    k = 1
    while out in used:
        k += 1
        out = f"{base}_{k}"
    used.add(out)
    return out


def _cache_key_parts(
    members_for_push: Set[Any],
    earliest_date: pd.Timestamp,
    t_max: pd.Timestamp,
    source_paths: List[str],
) -> str:
    m_sorted = sorted({int(x) for x in members_for_push})
    payload = json.dumps(
        {
            "members": m_sorted,
            "earliest": str(pd.Timestamp(earliest_date).normalize()),
            "t_max": str(pd.Timestamp(t_max).normalize()),
            "sources": source_paths,
        },
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def _resolve_push_glob(cfg: dict) -> List[str]:
    pf = cfg.get("push_features", {})
    pattern = pf.get("glob_pattern", "sleep_push_result_*.csv")
    return sorted(glob.glob(str(DATA_DIR / pattern)))


def push_cache_parquet_path(cache_key: str, cfg: dict) -> Path:
    pf = cfg.get("push_features", {})
    rel = pf.get("cache_relative_dir", "outputs/displacement_classification/cache")
    out_dir = PROJECT_ROOT / rel
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir / f"push_events_filtered_{cache_key}.parquet"


def load_or_build_push_events_cache(
    logger: logging.Logger,
    members_for_push: Set[Any],
    earliest_date: pd.Timestamp,
    t_max: pd.Timestamp,
    *,
    rebuild: bool = False,
) -> pd.DataFrame:
    """
    Return push rows for members in ``members_for_push`` with
    ``earliest_date <= dt <= t_max``. Load from parquet when the cache file exists
    unless *rebuild* is True.
    """
    cfg = _load_config()
    pf = cfg.get("push_features", {})
    if not pf.get("enabled", False):
        return pd.DataFrame()

    paths = _resolve_push_glob(cfg)
    if not paths:
        _log(
            logger,
            f"  push_features: no files match {DATA_DIR / pf.get('glob_pattern', '*.csv')} — empty frame.",
            level="warning",
        )
        return pd.DataFrame()

    cache_key = _cache_key_parts(
        members_for_push=members_for_push,
        earliest_date=earliest_date,
        t_max=t_max,
        source_paths=paths,
    )
    cache_path = push_cache_parquet_path(cache_key=cache_key, cfg=cfg)

    if cache_path.exists() and not rebuild:
        _log(logger, f"  push_features: loading cached push events → {cache_path}")
        return pd.read_parquet(cache_path)

    _log(logger, f"  push_features: building push event table ({len(paths)} CSV file(s))...")
    cols = ["dt", "member_id", "trigger_tag", "coupon", "discount"]
    parts: List[pd.DataFrame] = []
    for p in paths:
        df = pd.read_csv(p, usecols=lambda c: c in cols, encoding="utf-8-sig")
        parts.append(df)

    all_push = pd.concat(parts, ignore_index=True)
    all_push["dt"] = pd.to_datetime(all_push["dt"], errors="coerce")
    all_push = all_push.dropna(subset=["dt", "member_id"])
    all_push["member_id"] = all_push["member_id"].astype(np.int64)

    ed = pd.Timestamp(earliest_date).normalize()
    tm = pd.Timestamp(t_max).normalize()
    mem = {int(x) for x in members_for_push}
    mask = (
        all_push["member_id"].isin(mem)
        & (all_push["dt"] >= ed)
        & (all_push["dt"] <= tm)
    )
    out = all_push.loc[mask].copy()
    out = out.sort_values(["member_id", "dt"]).reset_index(drop=True)
    out.to_parquet(cache_path, index=False)
    _log(logger, f"  push_features: saved {len(out):,} rows → {cache_path}")
    return out


def build_purchase_day_ordinals_index(df_order_full: pd.DataFrame) -> Dict[int, np.ndarray]:
    """Per member, sorted unique purchase calendar days as int64 nanosecond ordinals."""
    d = df_order_full.copy()
    d["date"] = pd.to_datetime(d["date"]).dt.normalize()
    idx: Dict[int, np.ndarray] = {}
    for mid, g in d.groupby("member_id")["date"]:
        u = np.sort(np.unique(g.values.astype("datetime64[ns]")))
        idx[int(mid)] = u.astype("datetime64[ns]").astype(np.int64)
    return idx


def _next_purchase_ordinal(
    purchase_ordinals: np.ndarray,
    push_day_ord: int,
) -> Optional[int]:
    if purchase_ordinals.size == 0:
        return None
    j = np.searchsorted(purchase_ordinals, push_day_ord, side="left")
    if j >= purchase_ordinals.size:
        return None
    return int(purchase_ordinals[j])


def prepare_push_feature_metadata(df_push: pd.DataFrame) -> Tuple[Dict[str, str], List[str]]:
    used: Set[str] = set()
    tag_to_safe: Dict[str, str] = {}
    for t in df_push["trigger_tag"].dropna().unique():
        ts = str(t)
        if ts not in tag_to_safe:
            tag_to_safe[ts] = _sanitize_tag_for_column(ts, used=used)
    all_safe = sorted(tag_to_safe.values())
    return tag_to_safe, all_safe


def _zero_push_row(
    tag_to_safe: Dict[str, str],
    all_safe_tags: List[str],
    windows_days: List[int],
    response_horizon_days: int,
) -> Dict[str, Any]:
    row: Dict[str, Any] = {}
    for w in windows_days:
        row[f"n_push_{w}d"] = 0
        row[f"n_distinct_trigger_{w}d"] = 0
        for safe in all_safe_tags:
            row[f"ratio_trigger_{safe}_{w}d"] = 0.0
    row["n_push_per_week_28d"] = 0.0
    row["n_push_resolved_pre"] = 0
    row["mean_latency_push_to_purchase_days"] = 0.0
    row["median_latency_push_to_purchase_days"] = 0.0
    row[f"share_push_followed_by_purchase_{response_horizon_days}d"] = 0.0
    row["days_since_last_push"] = 9999
    row["n_push_since_last_purchase"] = 0
    for safe in all_safe_tags:
        row[f"mean_latency_days_trigger_{safe}"] = 0.0
        row[f"p_purchase_within_{response_horizon_days}d_trigger_{safe}"] = 0.0
        row[f"ratio_trigger_{safe}_among_followed_by_purchase_{response_horizon_days}d"] = 0.0
    row["n_push_with_coupon_28d"] = 0
    row["n_push_with_discount_28d"] = 0
    row["mean_coupon_28d"] = 0.0
    row["mean_discount_28d"] = 0.0
    row["share_push_coupon_28d"] = 0.0
    row["share_push_discount_28d"] = 0.0
    return row


def compute_push_features_for_batch(
    member_batch: pd.DataFrame,
    df_push_sorted: pd.DataFrame,
    dt_np: np.ndarray,
    push_end_idx: int,
    history_end: pd.Timestamp,
    purchase_ordinals_index: Dict[int, np.ndarray],
    tag_to_safe: Dict[str, str],
    all_safe_tags: List[str],
    *,
    windows_days: List[int],
    response_horizon_days: int,
) -> pd.DataFrame:
    """
    Add push feature columns to *member_batch* for one ``period_start`` batch.
    ``df_push_sorted`` / ``dt_np`` are sorted by ``dt``; use rows ``0:push_end_idx``.
    """
    he = pd.Timestamp(history_end).normalize()
    he_ord = int(np.int64(he.to_datetime64()))

    sub = df_push_sorted.iloc[:push_end_idx]
    unique_mids = np.unique(member_batch["member_id"].values)

    if sub.empty:
        z = _zero_push_row(
            tag_to_safe=tag_to_safe,
            all_safe_tags=all_safe_tags,
            windows_days=windows_days,
            response_horizon_days=response_horizon_days,
        )
        out = member_batch.copy()
        for k, v in z.items():
            out[k] = v
        return out

    by_m = {int(k): v for k, v in sub.groupby("member_id", sort=False)}

    feat_rows: Dict[int, Dict[str, Any]] = {}
    for mid in unique_mids:
        mid = int(mid)
        g = by_m.get(mid)
        if g is None or g.empty:
            feat_rows[mid] = _zero_push_row(
                tag_to_safe=tag_to_safe,
                all_safe_tags=all_safe_tags,
                windows_days=windows_days,
                response_horizon_days=response_horizon_days,
            )
            continue

        pur = purchase_ordinals_index.get(mid)
        if pur is None:
            pur = np.array([], dtype=np.int64)

        last_purchase_ord: Optional[int] = None
        if pur.size > 0:
            lp = pur[pur <= he_ord]
            if lp.size > 0:
                last_purchase_ord = int(lp.max())

        row: Dict[str, Any] = {}

        for w in windows_days:
            cut = he - pd.Timedelta(days=w)
            mwin = (g["dt"] > cut) & (g["dt"] <= he)
            gw = g.loc[mwin]
            n_w = len(gw)
            row[f"n_push_{w}d"] = int(n_w)
            row[f"n_distinct_trigger_{w}d"] = int(gw["trigger_tag"].nunique()) if n_w else 0
            for safe in all_safe_tags:
                row[f"ratio_trigger_{safe}_{w}d"] = 0.0
            if n_w > 0:
                vc = gw.assign(_tg=gw["trigger_tag"].astype(str)).groupby("_tg").size()
                for tag, safe in tag_to_safe.items():
                    row[f"ratio_trigger_{safe}_{w}d"] = float(vc.get(tag, 0)) / n_w

        row["n_push_per_week_28d"] = float(row.get("n_push_28d", 0)) / 4.0

        cut28 = he - pd.Timedelta(days=28)
        m28 = (g["dt"] > cut28) & (g["dt"] <= he)
        g28 = g.loc[m28]
        if len(g28) == 0:
            row["n_push_with_coupon_28d"] = 0
            row["n_push_with_discount_28d"] = 0
            row["mean_coupon_28d"] = 0.0
            row["mean_discount_28d"] = 0.0
            row["share_push_coupon_28d"] = 0.0
            row["share_push_discount_28d"] = 0.0
        else:
            c = pd.to_numeric(g28["coupon"], errors="coerce").fillna(0)
            d = pd.to_numeric(g28["discount"], errors="coerce").fillna(0)
            row["n_push_with_coupon_28d"] = int((c != 0).sum())
            row["n_push_with_discount_28d"] = int((d != 0).sum())
            row["mean_coupon_28d"] = float(c.mean())
            row["mean_discount_28d"] = float(d.mean())
            row["share_push_coupon_28d"] = float(row["n_push_with_coupon_28d"]) / len(g28)
            row["share_push_discount_28d"] = float(row["n_push_with_discount_28d"]) / len(g28)

        latencies: List[int] = []
        lat_by_tag: Dict[str, List[int]] = {}
        followup_tags: List[str] = []
        for _, r in g.iterrows():
            pdt = pd.Timestamp(r["dt"]).normalize()
            push_day_ord = int(np.int64(pdt.to_datetime64()))
            nxt = _next_purchase_ordinal(pur, push_day_ord)
            if nxt is None or nxt > he_ord:
                continue
            lat = int((np.int64(nxt) - np.int64(push_day_ord)) // _NS_PER_DAY)
            latencies.append(lat)
            tg = str(r["trigger_tag"])
            lat_by_tag.setdefault(tg, []).append(lat)
            if lat <= response_horizon_days:
                followup_tags.append(tg)

        row["n_push_resolved_pre"] = len(latencies)
        if latencies:
            arr = np.array(latencies, dtype=np.float64)
            row["mean_latency_push_to_purchase_days"] = float(arr.mean())
            row["median_latency_push_to_purchase_days"] = float(np.median(arr))
            row[f"share_push_followed_by_purchase_{response_horizon_days}d"] = float(
                (arr <= response_horizon_days).mean()
            )
        else:
            row["mean_latency_push_to_purchase_days"] = 0.0
            row["median_latency_push_to_purchase_days"] = 0.0
            row[f"share_push_followed_by_purchase_{response_horizon_days}d"] = 0.0

        for tag, safe in tag_to_safe.items():
            xs = lat_by_tag.get(tag)
            if xs:
                a = np.array(xs, dtype=np.float64)
                row[f"mean_latency_days_trigger_{safe}"] = float(a.mean())
                row[f"p_purchase_within_{response_horizon_days}d_trigger_{safe}"] = float(
                    (a <= response_horizon_days).mean()
                )
            else:
                row[f"mean_latency_days_trigger_{safe}"] = 0.0
                row[f"p_purchase_within_{response_horizon_days}d_trigger_{safe}"] = 0.0

        if followup_tags:
            cnt = Counter(followup_tags)
            denom = len(followup_tags)
            for tag, safe in tag_to_safe.items():
                row[f"ratio_trigger_{safe}_among_followed_by_purchase_{response_horizon_days}d"] = (
                    float(cnt.get(str(tag), 0)) / denom
                )
        else:
            for safe in all_safe_tags:
                row[f"ratio_trigger_{safe}_among_followed_by_purchase_{response_horizon_days}d"] = 0.0

        ghe = g[g["dt"] <= he]
        if not ghe.empty:
            last_push = ghe["dt"].max()
            row["days_since_last_push"] = int((he - pd.Timestamp(last_push).normalize()).days)
        else:
            row["days_since_last_push"] = 9999

        if last_purchase_ord is not None:
            gdt = g["dt"].values.astype("datetime64[ns]").astype(np.int64)
            m_after = (gdt > last_purchase_ord) & (gdt <= he_ord)
            row["n_push_since_last_purchase"] = int(m_after.sum())
        else:
            row["n_push_since_last_purchase"] = 0

        feat_rows[mid] = row

    out = member_batch.copy()
    for mid, row in feat_rows.items():
        for k, v in row.items():
            out.loc[out["member_id"] == mid, k] = v
    return out


def sort_push_and_dt_array(df_push: pd.DataFrame) -> Tuple[pd.DataFrame, np.ndarray]:
    """Sort push events by dt ascending; return frame and dt values as ns array."""
    s = df_push.sort_values("dt", kind="mergesort").reset_index(drop=True)
    dt_np = s["dt"].values.astype("datetime64[ns]").astype(np.int64)
    return s, dt_np


def push_end_index_for_history_end(dt_np: np.ndarray, history_end: pd.Timestamp) -> int:
    """Row count with dt <= history_end (dt sorted ascending)."""
    he = np.int64(pd.Timestamp(history_end).normalize().to_datetime64())
    return int(np.searchsorted(dt_np, he, side="right"))
