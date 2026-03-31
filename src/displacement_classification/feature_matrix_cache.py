"""
Persist full engineered feature matrices so reruns can skip push loading
and ``compute_features_for_panel``.

Cache key includes the push-subset fingerprint (members, dates, CSV paths),
closure list, config slices, and run flags (sample / max-closures / …). It does
not hash order or member source files; after updating those inputs, run with
``--rebuild-feature-cache`` (or delete the parquet for that key).
"""

from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Set, Tuple

import pandas as pd

from push_event_cache import (  # noqa: WPS433 (sibling import)
    PROJECT_ROOT,
    _cache_key_parts,
    _load_config,
    _resolve_push_glob,
)


def feature_matrix_cache_key(
    closures: pd.DataFrame,
    members_for_push: Set[Any],
    earliest_date: pd.Timestamp,
    t_max: pd.Timestamp,
    *,
    run_flags: Dict[str, Any],
    use_set_up_time_matched_control: bool,
) -> str:
    """Stable 16-char key for training + t0 feature matrix parquet files."""
    cfg = _load_config()
    paths = _resolve_push_glob(cfg)
    push_subset_key = _cache_key_parts(
        members_for_push=members_for_push,
        earliest_date=earliest_date,
        t_max=t_max,
        source_paths=paths,
    )
    closure_fp = sorted(
        (
            int(r["dept_id"]),
            pd.to_datetime(r["closure_start"]).strftime("%Y-%m-%d"),
        )
        for _, r in closures.iterrows()
    )
    pf = cfg.get("push_features", {})
    payload = {
        "push_subset_key": push_subset_key,
        "closures": closure_fp,
        "data": cfg.get("data", {}),
        "push_features": {
            "enabled": pf.get("enabled"),
            "windows_days": pf.get("windows_days"),
            "response_horizon_days": pf.get("response_horizon_days"),
        },
        "run": run_flags,
        "use_set_up_time_matched_control": use_set_up_time_matched_control,
    }
    return hashlib.sha256(
        json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    ).hexdigest()[:16]


def _cache_dir(cfg: dict) -> Path:
    fmc = cfg.get("feature_matrix_cache", {})
    rel = fmc.get("cache_relative_dir", "outputs/displacement_classification/cache")
    out = PROJECT_ROOT / rel
    out.mkdir(parents=True, exist_ok=True)
    return out


def training_parquet_path(cache_key: str, cfg: dict) -> Path:
    return _cache_dir(cfg) / f"features_training_{cache_key}.parquet"


def t0_parquet_path(cache_key: str, cfg: dict) -> Path:
    return _cache_dir(cfg) / f"features_t0_{cache_key}.parquet"


def t0_empty_marker_path(cache_key: str, cfg: dict) -> Path:
    return _cache_dir(cfg) / f"features_t0_empty_{cache_key}.marker"


def try_load_feature_matrix_cache(
    logger: logging.Logger,
    cache_key: str,
) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
    """Return (features_df, t0_features_df) if training parquet exists; else None."""
    cfg = _load_config()
    fmc = cfg.get("feature_matrix_cache", {})
    if not fmc.get("enabled", True):
        return None

    train_path = training_parquet_path(cache_key=cache_key, cfg=cfg)
    if not train_path.exists():
        return None

    features_df = pd.read_parquet(train_path)
    t0_path = t0_parquet_path(cache_key=cache_key, cfg=cfg)
    if t0_path.exists():
        t0_features_df = pd.read_parquet(t0_path)
    else:
        t0_features_df = pd.DataFrame()

    logger.info(
        f"  feature_matrix_cache: loaded training {len(features_df):,} rows → {train_path}"
    )
    logger.info(f"  feature_matrix_cache: loaded t0 {len(t0_features_df):,} rows")
    return features_df, t0_features_df


def save_feature_matrix_cache(
    logger: logging.Logger,
    features_df: pd.DataFrame,
    t0_features_df: pd.DataFrame,
    cache_key: str,
) -> None:
    cfg = _load_config()
    fmc = cfg.get("feature_matrix_cache", {})
    if not fmc.get("enabled", True):
        return

    train_path = training_parquet_path(cache_key=cache_key, cfg=cfg)
    t0_path = t0_parquet_path(cache_key=cache_key, cfg=cfg)
    marker = t0_empty_marker_path(cache_key=cache_key, cfg=cfg)

    features_df.to_parquet(train_path, index=False)
    logger.info(
        f"  feature_matrix_cache: saved training {len(features_df):,} rows → {train_path}"
    )

    if t0_features_df.empty:
        if t0_path.exists():
            t0_path.unlink()
        marker.write_text("1", encoding="utf-8")
        logger.info(f"  feature_matrix_cache: t0 empty (marker) → {marker}")
    else:
        if marker.exists():
            marker.unlink()
        t0_features_df.to_parquet(t0_path, index=False)
        logger.info(
            f"  feature_matrix_cache: saved t0 {len(t0_features_df):,} rows → {t0_path}"
        )
