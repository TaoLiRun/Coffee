#!/usr/bin/env python3
"""Estimate the prespecified time-invariant local cafe-density robustness check.

The authoritative density fields live in the GB18030/GBK-encoded
``dapt_id_address.csv`` on mktserver.  This script deliberately joins those
fields through each member-event's pre-closure preferred store, not through
the treated closure-store identifier carried by the estimation panel.

The regression code is a small, auditable Frisch-Waugh-Lovell implementation
of the paper-facing specification.  It is used here because the server was
out of disk space when this robustness check was run and the local interpreter
does not provide pyfixest.  The script refuses to proceed unless its collapsed
baseline reproduces the coefficient and CRV1 standard error previously saved
by ``fit_collapsed_specs`` within explicit tolerances.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import warnings
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


OUTCOME = "variety_seeking"
CLUSTER = "closure_event_id"
BASE_FIXED_EFFECTS = ["event_fe_id", "rel_t", "calendar_month"]
RAW_500 = "cafe_count_500m"
RAW_1500 = "cafe_count_1500m"
RAW_FIELD_500 = "半径500m内店铺数(咖啡厅)"
RAW_FIELD_1500 = "半径1500m内店铺数(咖啡厅)"
EXPECTED_DENSITY_SHA256 = (
    "361267209af83070d247aaa4b28d0d97e24654165089332566835673715419de"
)
EXPECTED_SAMPLE_SHA256 = (
    "2fd0449e995618580a5da0645e68dbc52fedda4471fd9e4aae386083c39580e3"
)
EXPECTED_MARKET_NEW_SAMPLE_SHA256 = (
    "ce84c6d6a508e9e538d4f84a8cfcd159ac510cd4c08f4d5770226d0ccd3f1ac4"
)
EXPECTED_ORDER_SHA256 = (
    "01eb80ae13cd8e1bb68e6ab3496ee32492795d84b13e0b374bd31c5209dbd74b"
)
AUTHORITATIVE_DENSITY_PATH = "/home/litao/Coffee/data/data1031/dapt_id_address.csv"
AUTHORITATIVE_ORDER_PATH = "/home/litao/Coffee/data/data1031/order_result.csv"
SERVER_WORKING_DIR = "/home/litao/Coffee/model-free"
PRIMARY_COUNTS = (0.0, 2.0, 5.0, 13.0)
LOW_DENSITY_CUTOFF = 3
SEED = 20260811


def parse_args() -> argparse.Namespace:
    root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=root)
    parser.add_argument(
        "--density-source",
        type=Path,
        default=Path("../data/data1031/dapt_id_address.csv"),
        help="Authoritative mktserver GB18030 CSV (a verified /private/tmp copy is auto-detected locally).",
    )
    parser.add_argument(
        "--order-source",
        type=Path,
        default=Path("../data/data1031/order_result.csv"),
        help="Baseline transaction source (a verified /private/tmp copy is auto-detected locally).",
    )
    parser.add_argument(
        "--sample-path",
        type=Path,
        default=Path(
            "outputs/03_main_18_closures/novelty_member_first_ddd_h4/"
            "estimation_sample.csv"
        ),
    )
    parser.add_argument(
        "--registry-path",
        type=Path,
        default=Path("outputs/customer-store/closure_pair_registry.csv"),
    )
    parser.add_argument(
        "--published-baseline-path",
        type=Path,
        default=Path(
            "outputs/03_main_18_closures/novelty_member_first_ddd_h4/"
            "ddd_binary_results.csv"
        ),
    )
    parser.add_argument(
        "--market-new-sample-path",
        type=Path,
        default=Path(
            "outputs/03_main_18_closures/novelty_market_new_ddd_h4/"
            "estimation_sample.csv"
        ),
    )
    parser.add_argument(
        "--market-new-baseline-path",
        type=Path,
        default=Path(
            "outputs/03_main_18_closures/novelty_market_new_ddd_h4/"
            "ddd_binary_results.csv"
        ),
    )
    parser.add_argument(
        "--utf8-mirror-path",
        type=Path,
        default=Path("outputs/nanjing_store_locations/nanjing_stores_geocoded.csv"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/05_robustness/time_invariant_cafe_density"),
    )
    parser.add_argument("--bootstrap-reps", type=int, default=9999)
    parser.add_argument("--chunksize", type=int, default=750_000)
    return parser.parse_args()


def resolve(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


def resolve_input(root: Path, path: Path, verified_local_copy: Path) -> Path:
    candidate = resolve(root, path)
    if candidate.exists():
        return candidate
    if not path.is_absolute() and verified_local_copy.exists():
        return verified_local_copy
    return candidate


def sha256(path: Path, block_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            block = handle.read(block_size)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def git_commit(root: Path) -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(root),
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except Exception:
        return "unavailable"


def record_check(
    checks: List[Dict[str, Any]],
    check: str,
    passed: bool,
    observed: Any,
    expected: Any,
) -> None:
    checks.append(
        {
            "check": check,
            "passed": bool(passed),
            "observed": str(observed),
            "expected": str(expected),
        }
    )
    if not passed:
        raise AssertionError(f"{check}: observed={observed!r}, expected={expected!r}")


def load_density_source(
    path: Path,
    mirror_path: Path,
    checks: List[Dict[str, Any]],
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(path)
    source_hash = sha256(path)
    record_check(
        checks,
        "authoritative density SHA-256",
        source_hash == EXPECTED_DENSITY_SHA256,
        source_hash,
        EXPECTED_DENSITY_SHA256,
    )
    raw = pd.read_csv(path, encoding="gb18030")
    required = {"dept_id", "address", RAW_FIELD_500, RAW_FIELD_1500}
    record_check(
        checks,
        "density source required fields",
        required.issubset(raw.columns),
        sorted(raw.columns),
        sorted(required),
    )
    density = raw.rename(
        columns={RAW_FIELD_500: RAW_500, RAW_FIELD_1500: RAW_1500}
    )[["dept_id", "address", RAW_500, RAW_1500]].copy()
    for column in ["dept_id", RAW_500, RAW_1500]:
        density[column] = pd.to_numeric(density[column], errors="raise")
    record_check(checks, "density source rows", len(density) == 260, len(density), 260)
    record_check(
        checks,
        "density source unique stores",
        density["dept_id"].nunique() == 260 and not density["dept_id"].duplicated().any(),
        density["dept_id"].nunique(),
        260,
    )
    record_check(
        checks,
        "density source complete key/address/counts",
        not density[["dept_id", "address", RAW_500, RAW_1500]].isna().any().any(),
        int(density[["dept_id", "address", RAW_500, RAW_1500]].isna().sum().sum()),
        0,
    )
    for column in ["dept_id", RAW_500, RAW_1500]:
        integer = np.allclose(density[column], np.round(density[column]))
        record_check(checks, f"{column} integer-valued", integer, integer, True)
        density[column] = density[column].astype(int)
    record_check(
        checks,
        "density counts nonnegative",
        bool((density[[RAW_500, RAW_1500]] >= 0).all().all()),
        density[[RAW_500, RAW_1500]].min().to_dict(),
        "both >= 0",
    )
    record_check(
        checks,
        "500m count does not exceed 1500m count",
        bool((density[RAW_500] <= density[RAW_1500]).all()),
        int((density[RAW_500] > density[RAW_1500]).sum()),
        0,
    )

    mirror_match = None
    if mirror_path.exists():
        mirror = pd.read_csv(mirror_path, encoding="utf-8-sig")
        mirror = mirror[["dept_id", RAW_FIELD_500, RAW_FIELD_1500]].rename(
            columns={RAW_FIELD_500: RAW_500, RAW_FIELD_1500: RAW_1500}
        )
        mirror["dept_id"] = pd.to_numeric(mirror["dept_id"], errors="raise").astype(int)
        joined = density[["dept_id", RAW_500, RAW_1500]].merge(
            mirror,
            on="dept_id",
            how="outer",
            suffixes=("_raw", "_mirror"),
            indicator=True,
            validate="one_to_one",
        )
        mirror_match = bool(
            joined["_merge"].eq("both").all()
            and joined[f"{RAW_500}_raw"].eq(joined[f"{RAW_500}_mirror"]).all()
            and joined[f"{RAW_1500}_raw"].eq(joined[f"{RAW_1500}_mirror"]).all()
        )
        record_check(checks, "UTF-8 mirror exactly matches raw counts", mirror_match, mirror_match, True)

    stat = path.stat()
    metadata = {
        "authoritative_server_working_directory": SERVER_WORKING_DIR,
        "authoritative_raw_path": AUTHORITATIVE_DENSITY_PATH,
        "authoritative_source_archive": "/home/litao/Coffee/data/data1031.zip",
        "authoritative_csv_file_mtime": "2022-11-07 11:19:18 +0800",
        "execution_copy_path": str(path),
        "encoding": "GB18030 (GBK-compatible)",
        "sha256": source_hash,
        "rows": int(len(density)),
        "unique_dept_id": int(density["dept_id"].nunique()),
        "raw_field_500m": RAW_FIELD_500,
        "raw_field_1500m": RAW_FIELD_1500,
        "execution_copy_file_mtime": datetime.fromtimestamp(stat.st_mtime).astimezone().isoformat(),
        "file_timestamp_interpretation": (
            "The authoritative CSV mtime and execution-copy mtime are file metadata only; neither is the POI measurement or pre-treatment date."
        ),
        "utf8_mirror_match": mirror_match,
        "measurement_limitations": [
            "The labels identify cafes, not brands or other-brand competitors.",
            "The source does not document operating status, provider, counting procedure, or POI snapshot date.",
            "The fixed value is an observed store-level density proxy and is not evidence that market structure was constant over time.",
        ],
    }
    return density.sort_values("dept_id").reset_index(drop=True), metadata


def load_registry(path: Path, density: pd.DataFrame, checks: List[Dict[str, Any]]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    registry = pd.read_csv(path, encoding="utf-8-sig")
    registry = registry.loc[registry["status"].eq("kept")].copy()
    registry["dept_id"] = pd.to_numeric(registry["dept_id"], errors="raise").astype(int)
    registry["closure_start"] = pd.to_datetime(registry["closure_start"], errors="raise").dt.normalize()
    record_check(checks, "kept closure events", len(registry) == 18, len(registry), 18)
    design_rows: List[Dict[str, Any]] = []
    for row in registry.itertuples(index=False):
        event_id = f"dept_{int(row.dept_id)}_closure_{row.closure_start:%Y-%m-%d}"
        design_rows.append(
            {
                CLUSTER: event_id,
                "closure_start": row.closure_start,
                "treated_store": int(row.dept_id),
                "dept_id": int(row.dept_id),
                "store_role": "treated",
            }
        )
        controls = [int(value) for value in str(row.control_store_ids).split("|")]
        if len(controls) != 5:
            raise AssertionError(f"{event_id} does not have five controls: {controls}")
        for control in controls:
            design_rows.append(
                {
                    CLUSTER: event_id,
                    "closure_start": row.closure_start,
                    "treated_store": int(row.dept_id),
                    "dept_id": control,
                    "store_role": "control",
                }
            )
    design = pd.DataFrame(design_rows)
    record_check(checks, "design store-event rows", len(design) == 108, len(design), 108)
    record_check(
        checks,
        "design stores are distinct",
        design["dept_id"].nunique() == 108,
        design["dept_id"].nunique(),
        108,
    )
    design = design.merge(density, on="dept_id", how="left", validate="one_to_one")
    record_check(
        checks,
        "all design stores match density source",
        not design[[RAW_500, RAW_1500]].isna().any().any(),
        int(design[[RAW_500, RAW_1500]].isna().sum().sum()),
        0,
    )
    registry[CLUSTER] = registry.apply(
        lambda row: f"dept_{int(row['dept_id'])}_closure_{row['closure_start']:%Y-%m-%d}",
        axis=1,
    )
    return registry, design


def load_sample(
    path: Path,
    checks: List[Dict[str, Any]],
    expected_hash: str,
    label: str,
) -> pd.DataFrame:
    sample_hash = sha256(path)
    record_check(
        checks,
        f"{label} estimation sample SHA-256",
        sample_hash == expected_hash,
        sample_hash,
        expected_hash,
    )
    sample = pd.read_csv(path, encoding="utf-8-sig")
    required = {
        "member_id", "dept_id", "closure_start", "treated", "disp_binary",
        CLUSTER, "rel_t", "post", "period_start", "calendar_month",
        "event_fe_id", OUTCOME,
    }
    record_check(
        checks,
        f"{label} sample fields",
        required.issubset(sample.columns),
        sorted(sample.columns),
        sorted(required),
    )
    sample["member_id"] = pd.to_numeric(sample["member_id"], errors="raise").astype(int)
    sample["dept_id"] = pd.to_numeric(sample["dept_id"], errors="raise").astype(int)
    sample["closure_start"] = pd.to_datetime(sample["closure_start"], errors="raise").dt.normalize()
    for column in ["treated", "disp_binary", "rel_t", "post"]:
        sample[column] = pd.to_numeric(sample[column], errors="raise").astype(int)
    record_check(
        checks,
        f"{label} member-event-period uniqueness",
        not sample.duplicated(["event_fe_id", "rel_t"]).any(),
        int(sample.duplicated(["event_fe_id", "rel_t"]).sum()),
        0,
    )
    record_check(
        checks,
        f"{label} expected event window",
        set(sample["rel_t"].unique()) == {-4, -3, -2, -1, 1, 2, 3, 4},
        sorted(sample["rel_t"].unique()),
        [-4, -3, -2, -1, 1, 2, 3, 4],
    )
    record_check(checks, f"{label} closure clusters", sample[CLUSTER].nunique() == 18, sample[CLUSTER].nunique(), 18)
    return sample


def scan_unique_visits(
    order_path: Path,
    member_ids: set,
    chunksize: int,
    checks: List[Dict[str, Any]],
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    if not order_path.exists():
        raise FileNotFoundError(order_path)
    order_hash = sha256(order_path)
    record_check(
        checks,
        "order source SHA-256",
        order_hash == EXPECTED_ORDER_SHA256,
        order_hash,
        EXPECTED_ORDER_SHA256,
    )
    frames: List[pd.DataFrame] = []
    raw_rows = 0
    selected_rows = 0
    for chunk in pd.read_csv(
        order_path,
        encoding="utf-8-sig",
        usecols=["member_id", "dept_id", "create_hour"],
        chunksize=chunksize,
    ):
        raw_rows += len(chunk)
        chunk["member_id"] = pd.to_numeric(chunk["member_id"], errors="coerce")
        chunk = chunk.loc[chunk["member_id"].isin(member_ids)].copy()
        if chunk.empty:
            continue
        selected_rows += len(chunk)
        chunk["member_id"] = chunk["member_id"].astype(int)
        chunk["dept_id"] = pd.to_numeric(chunk["dept_id"], errors="coerce")
        chunk["date"] = pd.to_datetime(chunk["create_hour"], errors="coerce").dt.normalize()
        chunk = chunk.dropna(subset=["dept_id", "date"])
        chunk["dept_id"] = chunk["dept_id"].astype(int)
        frames.append(chunk[["member_id", "date", "dept_id"]])
    if not frames:
        raise AssertionError("No order rows found for the main-panel members")
    visits = pd.concat(frames, ignore_index=True).drop_duplicates(
        ["member_id", "date", "dept_id"]
    )
    metadata = {
        "authoritative_raw_path": AUTHORITATIVE_ORDER_PATH,
        "execution_copy_path": str(order_path),
        "sha256": order_hash,
        "raw_order_rows_scanned": int(raw_rows),
        "selected_order_rows_before_visit_deduplication": int(selected_rows),
        "unique_member_date_store_visits": int(len(visits)),
    }
    return visits.sort_values(["member_id", "date", "dept_id"]).reset_index(drop=True), metadata


def recover_preferred_stores(
    sample: pd.DataFrame,
    visits: pd.DataFrame,
    registry: pd.DataFrame,
    density: pd.DataFrame,
    checks: List[Dict[str, Any]],
) -> pd.DataFrame:
    episode_cols = [
        "event_fe_id", "member_id", CLUSTER, "dept_id", "closure_start",
        "treated", "disp_binary",
    ]
    episodes = sample[episode_cols].drop_duplicates().copy()
    record_check(
        checks,
        "one row per event_fe_id before preference merge",
        not episodes["event_fe_id"].duplicated().any(),
        int(episodes["event_fe_id"].duplicated().sum()),
        0,
    )
    record_check(
        checks,
        "members belong to one closure event",
        not episodes["member_id"].duplicated().any(),
        int(episodes["member_id"].duplicated().sum()),
        0,
    )

    preference_frames: List[pd.DataFrame] = []
    for event_id, event in episodes.groupby(CLUSTER, sort=True):
        cutoffs = event["closure_start"].drop_duplicates()
        if len(cutoffs) != 1:
            raise AssertionError(f"Multiple closure dates within {event_id}")
        cutoff = cutoffs.iloc[0]
        event_members = set(event["member_id"])
        pre = visits.loc[
            visits["member_id"].isin(event_members) & visits["date"].lt(cutoff)
        ].copy()
        cust_store = (
            pre.groupby(["member_id", "dept_id"]).size().reset_index(name="store_purchases")
        )
        cust_total = pre.groupby("member_id").size().reset_index(name="total_purchases")
        cust_store = cust_store.merge(cust_total, on="member_id", validate="many_to_one")
        cust_store["preferred_ratio"] = (
            cust_store["store_purchases"] / cust_store["total_purchases"]
        )
        idx_max = cust_store.groupby("member_id")["preferred_ratio"].idxmax()
        preferred = cust_store.loc[
            idx_max,
            ["member_id", "dept_id", "preferred_ratio", "total_purchases"],
        ].rename(columns={"dept_id": "preferred_store"})
        preferred[CLUSTER] = event_id
        preference_frames.append(preferred)
    preference = pd.concat(preference_frames, ignore_index=True)
    episodes = episodes.merge(
        preference,
        on=["member_id", CLUSTER],
        how="left",
        validate="one_to_one",
    )
    record_check(
        checks,
        "all member-events recover a preferred store",
        not episodes["preferred_store"].isna().any(),
        int(episodes["preferred_store"].isna().sum()),
        0,
    )
    episodes["preferred_store"] = episodes["preferred_store"].astype(int)
    record_check(
        checks,
        "all reconstructed episodes meet five-day rule",
        bool(episodes["total_purchases"].ge(5).all()),
        float(episodes["total_purchases"].min()),
        ">= 5",
    )
    record_check(
        checks,
        "all reconstructed episodes meet 80-percent rule",
        bool(episodes["preferred_ratio"].ge(0.8 - 1e-12).all()),
        float(episodes["preferred_ratio"].min()),
        ">= 0.8",
    )
    treated_ok = episodes.loc[episodes["treated"].eq(1), "preferred_store"].eq(
        episodes.loc[episodes["treated"].eq(1), "dept_id"]
    )
    record_check(
        checks,
        "treated preferred store equals closing store",
        bool(treated_ok.all()),
        int((~treated_ok).sum()),
        0,
    )
    control_map = registry.set_index(CLUSTER)["control_store_ids"].apply(
        lambda value: {int(item) for item in str(value).split("|")}
    )
    controls = episodes.loc[episodes["treated"].eq(0)]
    control_ok = controls.apply(
        lambda row: int(row["preferred_store"]) in control_map.loc[row[CLUSTER]],
        axis=1,
    )
    record_check(
        checks,
        "control preferred store belongs to event control set",
        bool(control_ok.all()),
        int((~control_ok).sum()),
        0,
    )
    episodes = episodes.merge(
        density[["dept_id", RAW_500, RAW_1500]].rename(columns={"dept_id": "preferred_store"}),
        on="preferred_store",
        how="left",
        validate="many_to_one",
    )
    record_check(
        checks,
        "all member-events match both density measures",
        not episodes[[RAW_500, RAW_1500]].isna().any().any(),
        int(episodes[[RAW_500, RAW_1500]].isna().sum().sum()),
        0,
    )
    store_constancy = episodes.groupby("preferred_store")[[RAW_500, RAW_1500]].nunique()
    record_check(
        checks,
        "counts constant within preferred store",
        bool(store_constancy.le(1).all().all()),
        int(store_constancy.gt(1).sum().sum()),
        0,
    )
    return episodes.sort_values([CLUSTER, "member_id"]).reset_index(drop=True)


def merge_density_to_panel(
    sample: pd.DataFrame,
    episodes: pd.DataFrame,
    checks: List[Dict[str, Any]],
    label: str,
) -> pd.DataFrame:
    before_rows = len(sample)
    before_missing = int(sample[OUTCOME].isna().sum())
    merge_cols = [
        "event_fe_id", "preferred_store", "preferred_ratio", "total_purchases",
        RAW_500, RAW_1500,
    ]
    merged = sample.merge(
        episodes[merge_cols], on="event_fe_id", how="left", validate="many_to_one"
    )
    record_check(checks, f"{label} density merge preserves panel rows", len(merged) == before_rows, len(merged), before_rows)
    record_check(
        checks,
        f"{label} density merge preserves outcome missingness",
        int(merged[OUTCOME].isna().sum()) == before_missing,
        int(merged[OUTCOME].isna().sum()),
        before_missing,
    )
    record_check(
        checks,
        f"{label} density merge covers all panel rows",
        not merged[["preferred_store", RAW_500, RAW_1500]].isna().any().any(),
        int(merged[["preferred_store", RAW_500, RAW_1500]].isna().sum().sum()),
        0,
    )
    within = merged.groupby("event_fe_id")[["preferred_store", RAW_500, RAW_1500]].nunique()
    record_check(
        checks,
        f"{label} store and counts constant within member-event",
        bool(within.le(1).all().all()),
        int(within.gt(1).sum().sum()),
        0,
    )
    return merged


def drop_singletons(data: pd.DataFrame, fixed_effects: Sequence[str]) -> Tuple[pd.DataFrame, int]:
    work = data.copy()
    initial = len(work)
    while True:
        keep = np.ones(len(work), dtype=bool)
        for column in fixed_effects:
            counts = work.groupby(column, observed=True)[column].transform("size").to_numpy()
            keep &= counts > 1
        if keep.all():
            return work.reset_index(drop=True), initial - len(work)
        work = work.loc[keep].copy()


def residualize(
    values: np.ndarray,
    fixed_effect_codes: Sequence[np.ndarray],
    tolerance: float = 1e-11,
    max_iterations: int = 2000,
) -> Tuple[np.ndarray, int, float]:
    residual = np.asarray(values, dtype=np.float64).copy()
    if residual.ndim == 1:
        residual = residual[:, None]
    for iteration in range(1, max_iterations + 1):
        previous = residual.copy()
        for codes in fixed_effect_codes:
            group_count = int(codes.max()) + 1
            counts = np.bincount(codes, minlength=group_count).astype(float)
            for column in range(residual.shape[1]):
                sums = np.bincount(codes, weights=residual[:, column], minlength=group_count)
                residual[:, column] -= (sums / counts)[codes]
        error = float(np.max(np.abs(residual - previous)))
        if error < tolerance:
            return residual, iteration, error
    raise RuntimeError(f"Fixed-effect absorption did not converge; last error={error}")


def fit_fe_ols(
    data: pd.DataFrame,
    outcome: str,
    regressors: Sequence[str],
    fixed_effects: Sequence[str],
    cluster: str,
    drop_fe_singletons: bool = True,
) -> Dict[str, Any]:
    required = [outcome, *regressors, *fixed_effects, cluster]
    work = data.dropna(subset=required).copy()
    if drop_fe_singletons:
        work, singleton_drops = drop_singletons(work, fixed_effects)
    else:
        singleton_drops = 0
    codes = [pd.factorize(work[column], sort=False)[0] for column in fixed_effects]
    matrix = work[[outcome, *regressors]].to_numpy(dtype=float)
    residualized, iterations, absorption_error = residualize(matrix, codes)
    y = residualized[:, 0]
    X = residualized[:, 1:]
    xtx = X.T @ X
    rank = int(np.linalg.matrix_rank(xtx))
    if rank < len(regressors):
        raise ValueError(
            f"Rank deficiency: rank={rank}, regressors={len(regressors)}, names={list(regressors)}"
        )
    bread = np.linalg.inv(xtx)
    beta = bread @ (X.T @ y)
    residuals = y - X @ beta
    cluster_codes, cluster_labels = pd.factorize(work[cluster], sort=False)
    group_count = len(cluster_labels)
    if group_count < 2:
        raise ValueError("Cluster-robust inference needs at least two clusters")
    scores = np.zeros((group_count, len(regressors)), dtype=float)
    np.add.at(scores, cluster_codes, X * residuals[:, None])
    correction = (group_count / (group_count - 1)) * (
        (len(work) - 1) / (len(work) - len(regressors))
    )
    covariance = correction * bread @ (scores.T @ scores) @ bread
    standard_errors = np.sqrt(np.maximum(np.diag(covariance), 0.0))
    reference_df = group_count - 1
    tvalues = np.divide(
        beta,
        standard_errors,
        out=np.full_like(beta, np.nan),
        where=standard_errors > 0,
    )
    pvalues = 2 * stats.t.sf(np.abs(tvalues), reference_df)
    critical = stats.t.ppf(0.975, reference_df)
    return {
        "work": work,
        "X": X,
        "y": y,
        "beta": beta,
        "bread": bread,
        "covariance": covariance,
        "standard_errors": standard_errors,
        "pvalues": pvalues,
        "ci_low": beta - critical * standard_errors,
        "ci_high": beta + critical * standard_errors,
        "names": list(regressors),
        "fixed_effects": list(fixed_effects),
        "cluster": cluster,
        "cluster_codes": cluster_codes,
        "cluster_labels": np.asarray(cluster_labels),
        "correction": correction,
        "reference_df": reference_df,
        "n": len(work),
        "rank": rank,
        "singleton_drops": singleton_drops,
        "iterations": iterations,
        "absorption_error": absorption_error,
    }


def linear_combination(model: Dict[str, Any], weights: Dict[str, float]) -> Dict[str, float]:
    vector = np.zeros(len(model["names"]), dtype=float)
    positions = {name: index for index, name in enumerate(model["names"])}
    for term, value in weights.items():
        if term not in positions:
            raise KeyError(f"{term} absent from model terms {model['names']}")
        vector[positions[term]] = float(value)
    estimate = float(vector @ model["beta"])
    variance = float(vector @ model["covariance"] @ vector)
    se = math.sqrt(max(variance, 0.0))
    tvalue = estimate / se if se > 0 else float("nan")
    pvalue = float(2 * stats.t.sf(abs(tvalue), model["reference_df"])) if se > 0 else float("nan")
    critical = float(stats.t.ppf(0.975, model["reference_df"]))
    return {
        "estimate": estimate,
        "se": se,
        "tvalue": tvalue,
        "pvalue": pvalue,
        "ci_low": estimate - critical * se,
        "ci_high": estimate + critical * se,
        "reference_df": float(model["reference_df"]),
    }


def restricted_wild_cluster_pvalue(
    model: Dict[str, Any],
    weights: Dict[str, float],
    repetitions: int,
    seed: int = SEED,
) -> float:
    if repetitions <= 0:
        return float("nan")
    restriction = np.zeros(len(model["names"]), dtype=float)
    positions = {name: index for index, name in enumerate(model["names"])}
    for term, value in weights.items():
        restriction[positions[term]] = float(value)
    bread = model["bread"]
    beta = model["beta"]
    denominator = float(restriction @ bread @ restriction)
    if denominator <= 0:
        raise ValueError("Invalid restriction variance in restricted bootstrap")
    beta_restricted = beta - (
        bread @ restriction * (float(restriction @ beta) / denominator)
    )
    X = model["X"]
    y = model["y"]
    cluster_codes = model["cluster_codes"]
    group_count = len(model["cluster_labels"])
    residual_null = y - X @ beta_restricted
    score_null = np.zeros((group_count, X.shape[1]), dtype=float)
    np.add.at(score_null, cluster_codes, X * residual_null[:, None])
    xtx_by_cluster = np.zeros((group_count, X.shape[1], X.shape[1]), dtype=float)
    for group in range(group_count):
        X_group = X[cluster_codes == group]
        xtx_by_cluster[group] = X_group.T @ X_group
    observed = linear_combination(model, weights)
    observed_t = observed["tvalue"]
    rng = np.random.default_rng(seed)
    exceedances = 0
    valid = 0
    for _ in range(repetitions):
        wild_weights = rng.choice(np.array([-1.0, 1.0]), size=group_count)
        beta_star = beta_restricted + bread @ (score_null.T @ wild_weights)
        delta = beta_star - beta_restricted
        bootstrap_scores = wild_weights[:, None] * score_null - np.einsum(
            "gij,j->gi", xtx_by_cluster, delta
        )
        covariance_star = (
            model["correction"]
            * bread
            @ (bootstrap_scores.T @ bootstrap_scores)
            @ bread
        )
        variance_star = float(restriction @ covariance_star @ restriction)
        if variance_star <= 0:
            continue
        t_star = float(restriction @ beta_star) / math.sqrt(variance_star)
        exceedances += int(abs(t_star) >= abs(observed_t))
        valid += 1
    if valid == 0:
        return float("nan")
    return float((exceedances + 1) / (valid + 1))


def standardized_episode_measure(
    regression_frame: pd.DataFrame,
    raw_column: str,
    log_transform: bool,
) -> Tuple[pd.Series, Dict[str, float]]:
    episodes = regression_frame.drop_duplicates("event_fe_id")[["event_fe_id", raw_column]].copy()
    transformed = np.log1p(episodes[raw_column].astype(float)) if log_transform else episodes[raw_column].astype(float)
    mean = float(transformed.mean())
    sd = float(transformed.std(ddof=0))
    if sd <= 0:
        raise AssertionError(f"Zero SD for {raw_column}")
    episodes["density_z"] = (transformed - mean) / sd
    mapping = episodes.set_index("event_fe_id")["density_z"]
    z = regression_frame["event_fe_id"].map(mapping)
    metadata = {
        "mean": mean,
        "sd_population_ddof0": sd,
        "member_events": int(len(episodes)),
        "raw_column": raw_column,
        "transformation": "log1p" if log_transform else "raw",
    }
    return z.astype(float), metadata


def standardize_raw_value(raw_value: float, transform: Dict[str, float]) -> float:
    value = math.log1p(raw_value) if transform["transformation"] == "log1p" else raw_value
    return (value - transform["mean"]) / transform["sd_population_ddof0"]


def add_collapsed_terms(frame: pd.DataFrame, density_column: Optional[str] = None) -> Tuple[pd.DataFrame, List[str]]:
    work = frame.copy()
    p = work["post"].astype(float)
    t = work["treated"].astype(float)
    h = work["disp_binary"].astype(float)
    work["post_X_treated"] = p * t
    work["post_X_disp"] = p * h
    work["post_X_treated_X_disp"] = p * t * h
    terms = ["post_X_treated", "post_X_disp", "post_X_treated_X_disp"]
    if density_column is not None:
        c = work[density_column].astype(float)
        interactions = {
            "post_X_density": p * c,
            "post_X_treated_X_density": p * t * c,
            "post_X_disp_X_density": p * h * c,
            "post_X_treated_X_disp_X_density": p * t * h * c,
        }
        for name, values in interactions.items():
            work[name] = values
        terms.extend(interactions.keys())
    return work, terms


def model_summary_row(
    spec: str,
    estimand: str,
    result: Dict[str, float],
    model: Dict[str, Any],
    frame: pd.DataFrame,
    raw_count: Optional[float] = None,
    standardized_density: Optional[float] = None,
    measure: Optional[str] = None,
) -> Dict[str, Any]:
    episodes = frame.drop_duplicates("event_fe_id")
    return {
        "spec": spec,
        "measure": measure,
        "estimand": estimand,
        "raw_count": raw_count,
        "standardized_density": standardized_density,
        **result,
        "observations": int(model["n"]),
        "member_events": int(model["work"]["event_fe_id"].nunique()),
        "preferred_stores": int(model["work"]["preferred_store"].nunique()),
        "treated_stores": int(model["work"].loc[model["work"]["treated"].eq(1), "preferred_store"].nunique()),
        "closure_clusters": int(len(model["cluster_labels"])),
        "fixed_effects": " + ".join(model["fixed_effects"]),
        "cluster": model["cluster"],
        "weighted": False,
        "singleton_drops_within_call": int(model["singleton_drops"]),
        "absorption_iterations": int(model["iterations"]),
        "absorption_error": float(model["absorption_error"]),
        "input_member_events": int(episodes["event_fe_id"].nunique()),
    }


def pooled_smd(treated: pd.Series, control: pd.Series) -> float:
    treated = treated.astype(float)
    control = control.astype(float)
    numerator = float(treated.mean() - control.mean())
    denominator = math.sqrt(
        ((len(treated) - 1) * treated.var(ddof=1) + (len(control) - 1) * control.var(ddof=1))
        / (len(treated) + len(control) - 2)
    )
    return numerator / denominator if denominator > 0 else float("nan")


def build_balance_outputs(design: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    work = design.copy()
    work["log1p_cafe_count_500m"] = np.log1p(work[RAW_500])
    work["log1p_cafe_count_1500m"] = np.log1p(work[RAW_1500])
    measures = [RAW_500, "log1p_cafe_count_500m", RAW_1500, "log1p_cafe_count_1500m"]
    rows: List[Dict[str, Any]] = []
    for measure in measures:
        treated = work.loc[work["store_role"].eq("treated"), measure]
        control = work.loc[work["store_role"].eq("control"), measure]
        smd = pooled_smd(treated, control)
        for role, values in [("treated", treated), ("control", control)]:
            rows.append(
                {
                    "measure": measure,
                    "store_role": role,
                    "stores": int(len(values)),
                    "mean": float(values.mean()),
                    "sd": float(values.std(ddof=1)),
                    "median": float(values.median()),
                    "q25": float(values.quantile(0.25)),
                    "q75": float(values.quantile(0.75)),
                    "min": float(values.min()),
                    "max": float(values.max()),
                    "zero_count": int(values.eq(0).sum()),
                    "zero_share": float(values.eq(0).mean()),
                    "standardized_mean_difference_treated_minus_control": smd,
                }
            )
    balance = pd.DataFrame(rows)
    common_rows: List[Dict[str, Any]] = []
    for radius in [RAW_500, RAW_1500]:
        treated = work.loc[work["store_role"].eq("treated"), radius]
        control = work.loc[work["store_role"].eq("control"), radius]
        lower = float(max(treated.min(), control.min()))
        upper = float(min(treated.max(), control.max()))
        common_rows.append(
            {
                "measure": radius,
                "treated_min": float(treated.min()),
                "treated_max": float(treated.max()),
                "control_min": float(control.min()),
                "control_max": float(control.max()),
                "common_support_min": lower,
                "common_support_max": upper,
                "common_support_width": upper - lower,
                "treated_within_common_support": int(treated.between(lower, upper).sum()),
                "control_within_common_support": int(control.between(lower, upper).sum()),
            }
        )
    common = pd.DataFrame(common_rows)
    matched = work[
        [CLUSTER, "closure_start", "treated_store", "dept_id", "store_role", RAW_500, RAW_1500]
    ].sort_values(["closure_start", CLUSTER, "store_role", "dept_id"])
    return balance, common, matched


def add_event_study_terms(
    frame: pd.DataFrame,
    density_column: str,
    reference_period: int = -1,
) -> Tuple[pd.DataFrame, List[str], Dict[int, Dict[str, str]]]:
    work = frame.copy()
    components = {
        "treated": work["treated"].astype(float),
        "disp": work["disp_binary"].astype(float),
        "treated_X_disp": work["treated"].astype(float) * work["disp_binary"].astype(float),
        "density": work[density_column].astype(float),
        "treated_X_density": work["treated"].astype(float) * work[density_column].astype(float),
        "disp_X_density": work["disp_binary"].astype(float) * work[density_column].astype(float),
        "treated_X_disp_X_density": (
            work["treated"].astype(float)
            * work["disp_binary"].astype(float)
            * work[density_column].astype(float)
        ),
    }
    terms: List[str] = []
    term_map: Dict[int, Dict[str, str]] = {}
    for period in sorted(int(value) for value in work["rel_t"].unique()):
        if period == reference_period:
            continue
        tag = f"m{abs(period)}" if period < 0 else f"p{period}"
        indicator = work["rel_t"].eq(period).astype(float)
        term_map[period] = {}
        for component, values in components.items():
            name = f"rel_{tag}_X_{component}"
            work[name] = indicator * values
            terms.append(name)
            term_map[period][component] = name
    return work, terms, term_map


def add_store_fe_event_study_terms(
    frame: pd.DataFrame,
    reference_period: int = -1,
) -> Tuple[pd.DataFrame, List[str], Dict[int, str]]:
    work = frame.copy()
    terms: List[str] = []
    ddd_terms: Dict[int, str] = {}
    for period in sorted(int(value) for value in work["rel_t"].unique()):
        if period == reference_period:
            continue
        tag = f"m{abs(period)}" if period < 0 else f"p{period}"
        indicator = work["rel_t"].eq(period).astype(float)
        common_high = f"rel_{tag}_X_disp_store_fe"
        ddd = f"rel_{tag}_X_treated_X_disp_store_fe"
        work[common_high] = indicator * work["disp_binary"].astype(float)
        work[ddd] = indicator * work["treated"].astype(float) * work["disp_binary"].astype(float)
        terms.extend([common_high, ddd])
        ddd_terms[period] = ddd
    return work, terms, ddd_terms


def joint_zero_test(model: Dict[str, Any], terms: Sequence[str], label: str) -> Dict[str, Any]:
    positions = {name: index for index, name in enumerate(model["names"])}
    indices = [positions[name] for name in terms]
    beta = model["beta"][indices]
    covariance = model["covariance"][np.ix_(indices, indices)]
    statistic = float(beta.T @ np.linalg.pinv(covariance) @ beta)
    q = len(indices)
    # A cluster-df F reference is more conservative and transparent with 18 clusters.
    f_statistic = statistic / q
    pvalue_f = float(stats.f.sf(f_statistic, q, model["reference_df"]))
    pvalue_chi2 = float(stats.chi2.sf(statistic, q))
    return {
        "test": label,
        "terms": "|".join(terms),
        "restrictions": q,
        "wald_chi2": statistic,
        "f_statistic": f_statistic,
        "pvalue_f_cluster_df": pvalue_f,
        "pvalue_chi2_asymptotic": pvalue_chi2,
        "reference_df": model["reference_df"],
        "closure_clusters": len(model["cluster_labels"]),
        "observations": model["n"],
    }


def event_study_results(
    model: Dict[str, Any],
    term_map: Dict[int, Dict[str, str]],
    transform: Dict[str, float],
    raw_counts: Sequence[float],
    reference_period: int = -1,
) -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []
    periods = sorted(set(term_map) | {reference_period})
    for period in periods:
        for raw_count in raw_counts:
            z = standardize_raw_value(float(raw_count), transform)
            if period == reference_period:
                result = {
                    "estimate": 0.0,
                    "se": 0.0,
                    "tvalue": float("nan"),
                    "pvalue": float("nan"),
                    "ci_low": 0.0,
                    "ci_high": 0.0,
                    "reference_df": float(model["reference_df"]),
                }
            else:
                result = linear_combination(
                    model,
                    {
                        term_map[period]["treated_X_disp"]: 1.0,
                        term_map[period]["treated_X_disp_X_density"]: z,
                    },
                )
            rows.append(
                {
                    "rel_t": period,
                    "raw_count_500m": float(raw_count),
                    "standardized_density": z,
                    "reference_period": period == reference_period,
                    **result,
                }
            )
    return pd.DataFrame(rows).sort_values(["raw_count_500m", "rel_t"])


def store_fe_event_study_results(
    model: Dict[str, Any],
    term_map: Dict[int, str],
    reference_period: int = -1,
) -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []
    for period in sorted(set(term_map) | {reference_period}):
        if period == reference_period:
            result = {
                "estimate": 0.0,
                "se": 0.0,
                "tvalue": float("nan"),
                "pvalue": float("nan"),
                "ci_low": 0.0,
                "ci_high": 0.0,
                "reference_df": float(model["reference_df"]),
            }
        else:
            result = linear_combination(model, {term_map[period]: 1.0})
        rows.append({"rel_t": period, "reference_period": period == reference_period, **result})
    return pd.DataFrame(rows).sort_values("rel_t")


def empirical_cdf(values: pd.Series) -> Tuple[np.ndarray, np.ndarray]:
    ordered = np.sort(values.to_numpy(dtype=float))
    probabilities = np.arange(1, len(ordered) + 1, dtype=float) / len(ordered)
    return ordered, probabilities


def plot_density_ecdf(design: pd.DataFrame, common: pd.DataFrame, output: Path) -> None:
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    colors = {"control": "#3B6FB6", "treated": "#C6533D"}
    for role in ["control", "treated"]:
        values = design.loc[design["store_role"].eq(role), RAW_500]
        x, y = empirical_cdf(values)
        ax.step(x, y, where="post", color=colors[role], linewidth=2.2, label=f"{role.title()} stores (n={len(values)})")
    support = common.loc[common["measure"].eq(RAW_500)].iloc[0]
    ax.axvspan(
        support["common_support_min"],
        support["common_support_max"],
        color="#8FB996",
        alpha=0.16,
        label="Treated-control common-support range",
    )
    ax.set_xlabel("Locations classified as cafes within 500 meters (count)")
    ax.set_ylabel("Empirical cumulative distribution")
    ax.set_ylim(0, 1.02)
    ax.set_title(
        "Observed local cafe density by matched-store role\n"
        "Each step is one of 18 treated or 90 prespecified control stores"
    )
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(output, dpi=300, bbox_inches="tight")
    plt.close(fig)


def fitted_curve_data(
    model: Dict[str, Any],
    transform: Dict[str, float],
    raw_min: float,
    raw_max: float,
    base_term: str = "post_X_treated_X_disp",
    gradient_term: str = "post_X_treated_X_disp_X_density",
    points: int = 300,
) -> pd.DataFrame:
    grid = np.linspace(raw_min, raw_max, points)
    rows: List[Dict[str, Any]] = []
    for raw_count in grid:
        z = standardize_raw_value(float(raw_count), transform)
        result = linear_combination(model, {base_term: 1.0, gradient_term: z})
        rows.append({"raw_count": raw_count, "standardized_density": z, **result})
    return pd.DataFrame(rows)


def plot_fitted_curve(
    curve: pd.DataFrame,
    marker_rows: pd.DataFrame,
    support_min: float,
    support_max: float,
    radius: int,
    output: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    ax.fill_between(
        curve["raw_count"].to_numpy(),
        curve["ci_low"].to_numpy(),
        curve["ci_high"].to_numpy(),
        color="#3B6FB6",
        alpha=0.18,
        label="95% CRV1 confidence band",
    )
    ax.plot(curve["raw_count"], curve["estimate"], color="#244D7C", linewidth=2.3, label="Fitted DDD")
    ax.axvspan(support_min, support_max, color="#8FB996", alpha=0.14, label="Treated-control common support")
    ax.axhline(0, color="#333333", linewidth=1, linestyle="--")
    ax.errorbar(
        marker_rows["raw_count"],
        marker_rows["estimate"],
        yerr=np.vstack(
            [
                marker_rows["estimate"] - marker_rows["ci_low"],
                marker_rows["ci_high"] - marker_rows["estimate"],
            ]
        ),
        fmt="o",
        color="#C6533D",
        ecolor="#C6533D",
        capsize=3,
        label="Prespecified density points",
        zorder=5,
    )
    ax.set_xlabel(f"Locations classified as cafes within {radius:,} meters (count)")
    ax.set_ylabel("Fitted novelty-seeking DDD")
    ax.set_title(
        f"Novelty-seeking DDD across observed {radius:,}-meter cafe density\n"
        "Bands use closure-level CRV1 covariance; shaded x-range marks overlap"
    )
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False, fontsize=8.5)
    fig.tight_layout()
    fig.savefig(output, dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_density_event_study(
    results: pd.DataFrame,
    output: Path,
    common_support_min: float,
    common_support_max: float,
) -> None:
    fig, ax = plt.subplots(figsize=(8.4, 5.4))
    styles = {
        2.0: ("#3B6FB6", "Count 2 (design-store Q1)"),
        13.0: ("#C6533D", "Count 13 (design-store Q3)"),
    }
    offsets = {2.0: -0.05, 13.0: 0.05}
    for raw_count, (color, label) in styles.items():
        subset = results.loc[results["raw_count_500m"].eq(raw_count)].sort_values("rel_t")
        x = subset["rel_t"].to_numpy(dtype=float) + offsets[raw_count]
        ax.errorbar(
            x,
            subset["estimate"],
            yerr=np.vstack(
                [
                    subset["estimate"] - subset["ci_low"],
                    subset["ci_high"] - subset["estimate"],
                ]
            ),
            marker="o",
            linewidth=1.8,
            capsize=3,
            color=color,
            label=label,
        )
    ax.axhline(0, color="#333333", linestyle="--", linewidth=1)
    ax.axvline(-1, color="#777777", linestyle=":", linewidth=1)
    ax.set_xticks([-4, -3, -2, -1, 1, 2, 3, 4])
    ax.set_xlabel("Relative period (period -1 is the reference)")
    ax.set_ylabel("Fitted novelty-seeking DDD relative to period -1")
    ax.set_title(
        "Density-interacted novelty-seeking event study\n"
        f"Both plotted counts are within treated-control overlap [{common_support_min:.0f}, {common_support_max:.0f}]"
    )
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(output, dpi=300, bbox_inches="tight")
    plt.close(fig)


def coefficient_rows(spec: str, model: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for index, term in enumerate(model["names"]):
        rows.append(
            {
                "spec": spec,
                "term": term,
                "estimate": float(model["beta"][index]),
                "se": float(model["standard_errors"][index]),
                "pvalue": float(model["pvalues"][index]),
                "ci_low": float(model["ci_low"][index]),
                "ci_high": float(model["ci_high"][index]),
                "observations": int(model["n"]),
                "closure_clusters": int(len(model["cluster_labels"])),
                "reference_df": int(model["reference_df"]),
            }
        )
    return rows


def covariance_rows(spec: str, model: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for i, row_term in enumerate(model["names"]):
        for j, column_term in enumerate(model["names"]):
            rows.append(
                {
                    "spec": spec,
                    "row_term": row_term,
                    "column_term": column_term,
                    "covariance": float(model["covariance"][i, j]),
                }
            )
    return rows


def markdown_table(frame: pd.DataFrame) -> str:
    columns = [str(column) for column in frame.columns]
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join(["---"] * len(columns)) + " |"
    lines = [header, divider]
    for row in frame.itertuples(index=False, name=None):
        values = [str(value).replace("|", "\\|").replace("\n", " ") for value in row]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def format_number(value: Any, digits: int = 4) -> str:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return "—"
    return f"{float(value):.{digits}f}"


def find_result(results: pd.DataFrame, spec: str, estimand: str, raw_count: Optional[float] = None) -> pd.Series:
    subset = results.loc[results["spec"].eq(spec) & results["estimand"].eq(estimand)]
    if raw_count is not None:
        subset = subset.loc[np.isclose(subset["raw_count"].astype(float), raw_count, equal_nan=False)]
    if len(subset) != 1:
        raise AssertionError(
            f"Expected one result for spec={spec}, estimand={estimand}, raw_count={raw_count}; got {len(subset)}"
        )
    return subset.iloc[0]


def build_main_table(
    results: pd.DataFrame,
    bootstrap: pd.DataFrame,
    model_specs: pd.DataFrame,
    transforms: Dict[str, Dict[str, float]],
    design: pd.DataFrame,
) -> pd.DataFrame:
    specs = [
        "paper_facing_baseline",
        "raw_500m_interaction",
        "log_500m_interaction",
        "raw_1500m_interaction",
        "low_density_le3_descriptive",
        "preferred_store_event_post_fe",
    ]
    labels = {
        "paper_facing_baseline": "Paper-facing baseline",
        "raw_500m_interaction": "Raw 500m interaction",
        "log_500m_interaction": "Log(1+) 500m interaction",
        "raw_1500m_interaction": "Raw 1,500m interaction",
        "low_density_le3_descriptive": "Density <=3 (descriptive)",
        "preferred_store_event_post_fe": "Preferred-store x event x post FE",
    }
    main: Dict[str, Dict[str, str]] = {}
    q1500 = [float(design[RAW_1500].quantile(value)) for value in (0.25, 0.5, 0.75)]
    for spec in specs:
        focal_name = "high_minus_low_ddd" if spec in {
            "paper_facing_baseline", "low_density_le3_descriptive", "preferred_store_event_post_fe"
        } else "ddd_at_member_event_mean"
        focal = find_result(results, spec, focal_name)
        wild = bootstrap.loc[
            bootstrap["spec"].eq(spec) & bootstrap["estimand"].eq(focal_name),
            "pvalue_wild_restricted",
        ]
        row: Dict[str, str] = {
            "Focal DDD": format_number(focal["estimate"]),
            "CRV1 SE": format_number(focal["se"]),
            "95% CI": f"[{format_number(focal['ci_low'])}, {format_number(focal['ci_high'])}]",
            "Restricted wild p": format_number(wild.iloc[0], 3) if len(wild) == 1 else "—",
            "Density gradient": "—",
            "Fitted DDD: low": "—",
            "Fitted DDD: middle": "—",
            "Fitted DDD: high": "—",
            "Observations": f"{int(focal['observations']):,}",
            "Member-events": f"{int(focal['member_events']):,}",
            "Preferred stores": f"{int(focal['preferred_stores']):,}",
            "Treated stores": f"{int(focal['treated_stores']):,}",
            "Closure clusters": f"{int(focal['closure_clusters'])}",
            "Fixed effects": str(focal["fixed_effects"]),
            "Sample restriction": "None",
        }
        if "interaction" in spec:
            gradient = find_result(results, spec, "density_gradient_per_sd")
            row["Density gradient"] = (
                f"{format_number(gradient['estimate'])} "
                f"[{format_number(gradient['ci_low'])}, {format_number(gradient['ci_high'])}]"
            )
            if "1500m" in spec:
                points = q1500
            else:
                points = [2.0, 5.0, 13.0]
            point_labels = ["low", "middle", "high"]
            for point_label, point in zip(point_labels, points):
                fitted = find_result(results, spec, "fitted_ddd", point)
                row[f"Fitted DDD: {point_label}"] = (
                    f"{format_number(fitted['estimate'])} at count {format_number(point, 1)}"
                )
        if spec == "low_density_le3_descriptive":
            row["Sample restriction"] = "Preferred-store raw 500m cafe count <= 3; descriptive"
        if spec == "preferred_store_event_post_fe":
            row["Sample restriction"] = "Full baseline population; treated x post absorbed"
        main[labels[spec]] = row
    metrics = list(next(iter(main.values())).keys())
    table = pd.DataFrame({"Statistic": metrics})
    for label, values in main.items():
        table[label] = [values[metric] for metric in metrics]
    return table


def support_for_low_density(frame: pd.DataFrame, design: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    episodes = frame.drop_duplicates("event_fe_id")
    support = (
        episodes.groupby(["treated", "disp_binary"], observed=True)
        .agg(
            member_events=("event_fe_id", "size"),
            preferred_stores=("preferred_store", "nunique"),
            closure_clusters=(CLUSTER, "nunique"),
        )
        .reset_index()
    )
    event_treatment = (
        episodes.groupby([CLUSTER, "treated"], observed=True)
        .agg(
            member_events=("event_fe_id", "size"),
            incidence_groups=("disp_binary", "nunique"),
            preferred_stores=("preferred_store", "nunique"),
        )
        .reset_index()
    )
    event_pivot = event_treatment.pivot(index=CLUSTER, columns="treated", values="member_events")
    both_sides = set(event_pivot.dropna().index)
    incidence_pivot = event_treatment.pivot(index=CLUSTER, columns="treated", values="incidence_groups")
    both_incidence_both_sides = int(
        ((incidence_pivot.get(0, 0) >= 2) & (incidence_pivot.get(1, 0) >= 2)).sum()
    )
    design_low = design.loc[design[RAW_500].le(LOW_DENSITY_CUTOFF)].copy()
    design_event_roles = design_low.groupby([CLUSTER, "store_role"]).size().unstack()
    matched_both = int(design_event_roles.dropna().shape[0])
    metadata = {
        "cutoff": LOW_DENSITY_CUTOFF,
        "cutoff_basis": "Observed 33rd percentile among 108 design stores; fixed before outcome estimation.",
        "design_stores": int(len(design_low)),
        "design_treated_stores": int(design_low["store_role"].eq("treated").sum()),
        "design_control_stores": int(design_low["store_role"].eq("control").sum()),
        "matched_sets_with_low_density_on_both_treatment_sides": matched_both,
        "member_events": int(episodes["event_fe_id"].nunique()),
        "outcome_observations": int(len(frame)),
        "closure_clusters": int(episodes[CLUSTER].nunique()),
        "treated_closure_events_retained": int(episodes.loc[episodes["treated"].eq(1), CLUSTER].nunique()),
        "events_with_member_support_on_both_treatment_sides": len(both_sides),
        "events_with_high_and_low_incidence_support_on_both_treatment_sides": both_incidence_both_sides,
    }
    support["sample"] = "cafe_count_500m <= 3"
    return support, metadata


def write_summary(
    output: Path,
    classification: str,
    baseline: pd.Series,
    primary_mean: pd.Series,
    primary_zero: pd.Series,
    primary_low: pd.Series,
    primary_middle: pd.Series,
    primary_high: pd.Series,
    primary_gradient: pd.Series,
    low_result: pd.Series,
    store_fe_result: pd.Series,
    market_baseline: pd.Series,
    market_mean: pd.Series,
    market_low: pd.Series,
    market_middle: pd.Series,
    market_high: pd.Series,
    market_gradient: pd.Series,
    wild: pd.DataFrame,
    balance: pd.DataFrame,
    common: pd.DataFrame,
    pretrend: pd.Series,
    store_pretrend: pd.Series,
    pre_gradient_values: Sequence[float],
    benchmark: pd.DataFrame,
    low_metadata: Dict[str, Any],
    loo: pd.DataFrame,
    bootstrap_reps: int,
) -> None:
    balance_500 = balance.loc[
        (balance["measure"].eq(RAW_500)) & balance["store_role"].eq("treated")
    ].iloc[0]
    support = common.loc[common["measure"].eq(RAW_500)].iloc[0]
    primary_wild = wild.loc[
        wild["spec"].eq("raw_500m_interaction")
        & wild["estimand"].eq("ddd_at_member_event_mean"),
        "pvalue_wild_restricted",
    ].iloc[0]
    benchmark_text = "; ".join(
        f"{row.location}: {'within' if row.within_25pct_benchmark else 'outside'} benchmark"
        for row in benchmark.itertuples(index=False)
    )
    loo_count2 = loo.loc[loo["estimand"].eq("fitted_ddd_count_2"), "estimate"]
    loo_count13 = loo.loc[loo["estimand"].eq("fitted_ddd_count_13"), "estimate"]
    absolute_change = abs(float(primary_mean["estimate"]) - float(baseline["estimate"]))
    percentage_change = 100 * absolute_change / abs(float(baseline["estimate"]))
    gradient_path = ", ".join(f"{value:.4f}" for value in pre_gradient_values)
    text = f"""# Time-invariant local café-density robustness

## Bottom line

**Evidence classification: {classification}.** The collapsed estimates remain directionally similar, but the density-interacted event study displays a systematic pre-period warning. The three pre-period density-gradient coefficients (periods -4, -3, and -2 relative to -1) are {gradient_path}; their joint cluster-df F test has p={pretrend['pvalue_f_cluster_df']:.3f}. Because all three estimates point in the same direction and the joint test rejects, the interacted dynamic design does not provide a clean robustness result, even though the stronger additive local-shock fixed effects are stable.

The paper-facing member-first novelty-seeking DDD is {baseline['estimate']:.4f} (95% CI [{baseline['ci_low']:.4f}, {baseline['ci_high']:.4f}]). Allowing the complete post-period interaction hierarchy with the fixed raw 500-meter café count gives a fitted DDD of {primary_mean['estimate']:.4f} at the member-event mean (95% CI [{primary_mean['ci_low']:.4f}, {primary_mean['ci_high']:.4f}]; restricted wild-cluster p={primary_wild:.3f}, {bootstrap_reps:,} repetitions). This is an absolute change of {absolute_change:.4f}, or {percentage_change:.1f}% of the absolute baseline magnitude. The density gradient is {primary_gradient['estimate']:.4f} per one-SD increase (95% CI [{primary_gradient['ci_low']:.4f}, {primary_gradient['ci_high']:.4f}]).

At raw 500-meter counts 2, 5, and 13, the fitted DDDs are {primary_low['estimate']:.4f}, {primary_middle['estimate']:.4f}, and {primary_high['estimate']:.4f}, respectively. Their 95% intervals are [{primary_low['ci_low']:.4f}, {primary_low['ci_high']:.4f}], [{primary_middle['ci_low']:.4f}, {primary_middle['ci_high']:.4f}], and [{primary_high['ci_low']:.4f}, {primary_high['ci_high']:.4f}]. The locked 25% magnitude benchmark reads: {benchmark_text}.

At a raw count of zero, the continuous model predicts {primary_zero['estimate']:.4f} (95% CI [{primary_zero['ci_low']:.4f}, {primary_zero['ci_high']:.4f}]). Only three treated design stores have zero observed 500-meter counts, so this is a sparse-support model prediction rather than a separate confirmatory estimate.

## Support and leverage

The raw 500-meter treated-minus-control standardized mean difference is {balance_500['standardized_mean_difference_treated_minus_control']:.3f}. Treated and control design stores overlap from counts {support['common_support_min']:.0f} through {support['common_support_max']:.0f}; the fitted figures mark this range explicitly. Leaving out one closure and its five matched controls at a time gives count-2 fitted DDDs from {loo_count2.min():.4f} to {loo_count2.max():.4f} and count-13 fitted DDDs from {loo_count13.min():.4f} to {loo_count13.max():.4f}.

The density-gradient pre-period test uses {int(pretrend['restrictions'])} restrictions and 18 closure clusters. Its rejection is substantively relevant because the coefficients are directionally aligned, but it does not identify the source of the differential pattern. By comparison, the preferred-store-by-event-by-period-FE event-study pretest has p={store_pretrend['pvalue_f_cluster_df']:.3f}. The collapsed preferred-store-by-event-by-post-FE DDD is {store_fe_result['estimate']:.4f} (95% CI [{store_fe_result['ci_low']:.4f}, {store_fe_result['ci_high']:.4f}]). These fixed effects absorb arbitrary additive store-level local shocks, but not shocks that affect high- and low-predicted-incidence members differently within a store.

## Low-density descriptive check

The locked rule `cafe_count_500m <= 3` retains {low_metadata['design_stores']} design stores ({low_metadata['design_treated_stores']} treated and {low_metadata['design_control_stores']} controls), {low_metadata['member_events']:,} member-events, {low_metadata['outcome_observations']:,} outcome observations, and {low_metadata['closure_clusters']} contributing closure clusters. Its DDD is {low_result['estimate']:.4f} (95% CI [{low_result['ci_low']:.4f}, {low_result['ci_high']:.4f}]). Only {low_metadata['matched_sets_with_low_density_on_both_treatment_sides']} matched sets contain low-density stores on both treatment sides. This estimate is descriptive and its wide interval is limited information, not affirmative evidence for or against the baseline.

## Outcome-definition sensitivity

Using market-new novelty, the unchanged baseline DDD is {market_baseline['estimate']:.4f} (95% CI [{market_baseline['ci_low']:.4f}, {market_baseline['ci_high']:.4f}]). With the raw 500-meter interaction, the fitted DDD at the member-event mean is {market_mean['estimate']:.4f}, and the density gradient is {market_gradient['estimate']:.4f} per SD. Fitted DDDs at counts 2, 5, and 13 are {market_low['estimate']:.4f}, {market_middle['estimate']:.4f}, and {market_high['estimate']:.4f}. This is an outcome-definition sensitivity; member-first novelty remains primary.

## Interpretation boundary

The source counts locations classified as cafés. It does not identify brands, operating status, the POI provider, the counting procedure, or the snapshot date. The CSV file timestamp postdates the 2020-2021 treatment period and is not a measurement date. These results therefore test whether the novelty DDD is concentrated in locations with high observed café density. They do not directly measure other-brand competition, competitor closures, or a pre-treatment covariate, and the counts were not used to rematch, reweight, trim, or select specifications.

## Reproducibility

The analysis joins density through the pre-closure preferred store reconstructed from unique member-date-store visits using the original five-day and 80% rules. It reproduces the published baseline before fitting any density interaction, retains the unweighted `event_fe_id + rel_t + calendar_month` fixed effects, and clusters CRV1 inference by the 18 closure events. See `run_metadata.json`, `validation_checks.csv`, `model_specifications.csv`, and `validation_report.md` for provenance and QA.
"""
    output.write_text(text, encoding="utf-8")


def main() -> None:
    args = parse_args()
    root = args.project_root.resolve()
    density_path = resolve_input(
        root,
        args.density_source,
        Path("/private/tmp/coffee_cafe_density_dapt_id_address.csv"),
    )
    order_path = resolve_input(
        root,
        args.order_source,
        Path("/private/tmp/coffee_cafe_density_order_result.csv"),
    )
    sample_path = resolve(root, args.sample_path)
    registry_path = resolve(root, args.registry_path)
    baseline_path = resolve(root, args.published_baseline_path)
    market_new_sample_path = resolve(root, args.market_new_sample_path)
    market_new_baseline_path = resolve(root, args.market_new_baseline_path)
    mirror_path = resolve(root, args.utf8_mirror_path)
    output_dir = resolve(root, args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    checks: List[Dict[str, Any]] = []
    print("[1/9] Loading and validating authoritative sources", flush=True)
    density, density_metadata = load_density_source(density_path, mirror_path, checks)
    registry, design = load_registry(registry_path, density, checks)
    sample = load_sample(
        sample_path, checks, EXPECTED_SAMPLE_SHA256, "member-first novelty"
    )
    market_new_sample = load_sample(
        market_new_sample_path,
        checks,
        EXPECTED_MARKET_NEW_SAMPLE_SHA256,
        "market-new novelty",
    )

    print("[2/9] Reconstructing pre-closure preferred stores", flush=True)
    member_ids = set(sample["member_id"].unique())
    visits, order_metadata = scan_unique_visits(order_path, member_ids, args.chunksize, checks)
    episodes = recover_preferred_stores(sample, visits, registry, density, checks)
    primary_episode_ids = set(sample["event_fe_id"])
    market_episode_ids = set(market_new_sample["event_fe_id"])
    record_check(
        checks,
        "market-new and member-first episode keys agree",
        primary_episode_ids == market_episode_ids,
        len(primary_episode_ids.symmetric_difference(market_episode_ids)),
        0,
    )
    merged = merge_density_to_panel(sample, episodes, checks, "member-first novelty")
    market_new_merged = merge_density_to_panel(
        market_new_sample, episodes, checks, "market-new novelty"
    )
    episodes.to_csv(output_dir / "member_event_preferred_store_density.csv", index=False)

    print("[3/9] Locking exact baseline regression population and reproducing baseline", flush=True)
    outcome_rows = merged.loc[merged[OUTCOME].notna()].copy()
    regression_frame, initial_singleton_drops = drop_singletons(outcome_rows, BASE_FIXED_EFFECTS)
    baseline_work, baseline_terms = add_collapsed_terms(regression_frame)
    baseline_model = fit_fe_ols(
        baseline_work,
        OUTCOME,
        baseline_terms,
        BASE_FIXED_EFFECTS,
        CLUSTER,
        drop_fe_singletons=False,
    )
    published = pd.read_csv(baseline_path)
    published = published.loc[
        published["spec"].eq("binary_collapsed")
        & published["estimand"].eq("high_minus_low_ddd")
    ].iloc[0]
    baseline_result = linear_combination(
        baseline_model, {"post_X_treated_X_disp": 1.0}
    )
    record_check(
        checks,
        "baseline estimation observations reproduce",
        baseline_model["n"] == int(published["n"]),
        baseline_model["n"],
        int(published["n"]),
    )
    record_check(
        checks,
        "baseline coefficient reproduces fit_collapsed_specs",
        abs(baseline_result["estimate"] - float(published["coef"])) <= 1e-8,
        baseline_result["estimate"],
        published["coef"],
    )
    record_check(
        checks,
        "baseline CRV1 SE reproduces fit_collapsed_specs",
        abs(baseline_result["se"] - float(published["se"])) <= 5e-5,
        baseline_result["se"],
        published["se"],
    )

    market_outcome_rows = market_new_merged.loc[market_new_merged[OUTCOME].notna()].copy()
    market_regression_frame, market_singleton_drops = drop_singletons(
        market_outcome_rows, BASE_FIXED_EFFECTS
    )
    market_baseline_work, market_baseline_terms = add_collapsed_terms(
        market_regression_frame
    )
    market_baseline_model = fit_fe_ols(
        market_baseline_work,
        OUTCOME,
        market_baseline_terms,
        BASE_FIXED_EFFECTS,
        CLUSTER,
        drop_fe_singletons=False,
    )
    market_published = pd.read_csv(market_new_baseline_path)
    market_published = market_published.loc[
        market_published["spec"].eq("binary_collapsed")
        & market_published["estimand"].eq("high_minus_low_ddd")
    ].iloc[0]
    market_baseline_result = linear_combination(
        market_baseline_model, {"post_X_treated_X_disp": 1.0}
    )
    record_check(
        checks,
        "market-new baseline estimation observations reproduce",
        market_baseline_model["n"] == int(market_published["n"]),
        market_baseline_model["n"],
        int(market_published["n"]),
    )
    record_check(
        checks,
        "market-new baseline coefficient reproduces fit_collapsed_specs",
        abs(market_baseline_result["estimate"] - float(market_published["coef"])) <= 1e-8,
        market_baseline_result["estimate"],
        market_published["coef"],
    )
    record_check(
        checks,
        "market-new baseline CRV1 SE reproduces fit_collapsed_specs",
        abs(market_baseline_result["se"] - float(market_published["se"])) <= 5e-5,
        market_baseline_result["se"],
        market_published["se"],
    )

    transform_configs = {
        "raw_500m_interaction": (RAW_500, False, "density_z_raw_500m"),
        "log_500m_interaction": (RAW_500, True, "density_z_log_500m"),
        "raw_1500m_interaction": (RAW_1500, False, "density_z_raw_1500m"),
        "log_1500m_interaction": (RAW_1500, True, "density_z_log_1500m"),
    }
    transforms: Dict[str, Dict[str, float]] = {}
    for spec, (raw_column, log_transform, z_column) in transform_configs.items():
        z, transform = standardized_episode_measure(regression_frame, raw_column, log_transform)
        regression_frame[z_column] = z.to_numpy()
        transforms[spec] = transform
    market_z, market_transform = standardized_episode_measure(
        market_regression_frame, RAW_500, False
    )
    market_regression_frame["density_z_raw_500m"] = market_z.to_numpy()
    transforms["market_new_raw_500m_interaction"] = market_transform

    print("[4/9] Estimating collapsed density interactions and supporting specifications", flush=True)
    models: Dict[str, Dict[str, Any]] = {"paper_facing_baseline": baseline_model}
    model_frames: Dict[str, pd.DataFrame] = {"paper_facing_baseline": baseline_work}
    model_specs_rows: List[Dict[str, Any]] = [
        {
            "spec": "paper_facing_baseline",
            "outcome": OUTCOME,
            "regressors": " + ".join(baseline_terms),
            "fixed_effects": " + ".join(BASE_FIXED_EFFECTS),
            "cluster": CLUSTER,
            "weights": "none",
            "sample": "paper-facing nonmissing outcome rows after FE singleton removal",
        }
    ]
    for spec, (_, _, z_column) in transform_configs.items():
        work, terms = add_collapsed_terms(regression_frame, z_column)
        model = fit_fe_ols(
            work, OUTCOME, terms, BASE_FIXED_EFFECTS, CLUSTER, drop_fe_singletons=False
        )
        models[spec] = model
        model_frames[spec] = work
        model_specs_rows.append(
            {
                "spec": spec,
                "outcome": OUTCOME,
                "regressors": " + ".join(terms),
                "fixed_effects": " + ".join(BASE_FIXED_EFFECTS),
                "cluster": CLUSTER,
                "weights": "none",
                "sample": "same exact population as paper-facing baseline",
            }
        )

    models["market_new_baseline"] = market_baseline_model
    model_frames["market_new_baseline"] = market_baseline_work
    model_specs_rows.append(
        {
            "spec": "market_new_baseline",
            "outcome": "market-new variety_seeking",
            "regressors": " + ".join(market_baseline_terms),
            "fixed_effects": " + ".join(BASE_FIXED_EFFECTS),
            "cluster": CLUSTER,
            "weights": "none",
            "sample": "market-new outcome-definition sensitivity",
        }
    )
    market_density_work, market_density_terms = add_collapsed_terms(
        market_regression_frame, "density_z_raw_500m"
    )
    market_density_model = fit_fe_ols(
        market_density_work,
        OUTCOME,
        market_density_terms,
        BASE_FIXED_EFFECTS,
        CLUSTER,
        drop_fe_singletons=False,
    )
    models["market_new_raw_500m_interaction"] = market_density_model
    model_frames["market_new_raw_500m_interaction"] = market_density_work
    model_specs_rows.append(
        {
            "spec": "market_new_raw_500m_interaction",
            "outcome": "market-new variety_seeking",
            "regressors": " + ".join(market_density_terms),
            "fixed_effects": " + ".join(BASE_FIXED_EFFECTS),
            "cluster": CLUSTER,
            "weights": "none",
            "sample": "market-new outcome-definition sensitivity",
        }
    )

    low_frame = regression_frame.loc[regression_frame[RAW_500].le(LOW_DENSITY_CUTOFF)].copy()
    low_work, low_terms = add_collapsed_terms(low_frame)
    low_model = fit_fe_ols(low_work, OUTCOME, low_terms, BASE_FIXED_EFFECTS, CLUSTER)
    models["low_density_le3_descriptive"] = low_model
    model_frames["low_density_le3_descriptive"] = low_work
    model_specs_rows.append(
        {
            "spec": "low_density_le3_descriptive",
            "outcome": OUTCOME,
            "regressors": " + ".join(low_terms),
            "fixed_effects": " + ".join(BASE_FIXED_EFFECTS),
            "cluster": CLUSTER,
            "weights": "none",
            "sample": "preferred-store cafe_count_500m <= 3; descriptive",
        }
    )

    store_fe_frame = regression_frame.copy()
    store_fe_frame["preferred_store_event_post_fe"] = (
        store_fe_frame[CLUSTER].astype(str)
        + "|store_"
        + store_fe_frame["preferred_store"].astype(str)
        + "|post_"
        + store_fe_frame["post"].astype(str)
    )
    store_fe_work, _ = add_collapsed_terms(store_fe_frame)
    store_fe_terms = ["post_X_disp", "post_X_treated_X_disp"]
    store_fe_fixed_effects = [*BASE_FIXED_EFFECTS, "preferred_store_event_post_fe"]
    store_fe_model = fit_fe_ols(
        store_fe_work,
        OUTCOME,
        store_fe_terms,
        store_fe_fixed_effects,
        CLUSTER,
        drop_fe_singletons=False,
    )
    models["preferred_store_event_post_fe"] = store_fe_model
    model_frames["preferred_store_event_post_fe"] = store_fe_work
    model_specs_rows.append(
        {
            "spec": "preferred_store_event_post_fe",
            "outcome": OUTCOME,
            "regressors": " + ".join(store_fe_terms),
            "fixed_effects": " + ".join(store_fe_fixed_effects),
            "cluster": CLUSTER,
            "weights": "none",
            "sample": "full baseline population; post x treated absorbed by store-event-post FE",
        }
    )

    model_results_rows: List[Dict[str, Any]] = []
    model_results_rows.append(
        model_summary_row(
            "paper_facing_baseline",
            "high_minus_low_ddd",
            baseline_result,
            baseline_model,
            baseline_work,
        )
    )
    q1500 = [float(design[RAW_1500].quantile(value)) for value in (0.25, 0.5, 0.75)]
    for spec, (raw_column, _, _) in transform_configs.items():
        model = models[spec]
        frame = model_frames[spec]
        gradient_term = "post_X_treated_X_disp_X_density"
        mean_result = linear_combination(model, {"post_X_treated_X_disp": 1.0})
        model_results_rows.append(
            model_summary_row(
                spec,
                "ddd_at_member_event_mean",
                mean_result,
                model,
                frame,
                standardized_density=0.0,
                measure=raw_column,
            )
        )
        gradient_result = linear_combination(model, {gradient_term: 1.0})
        model_results_rows.append(
            model_summary_row(
                spec,
                "density_gradient_per_sd",
                gradient_result,
                model,
                frame,
                measure=raw_column,
            )
        )
        evaluation_counts = PRIMARY_COUNTS if raw_column == RAW_500 else (0.0, *q1500)
        for raw_count in evaluation_counts:
            z_value = standardize_raw_value(float(raw_count), transforms[spec])
            result = linear_combination(
                model,
                {"post_X_treated_X_disp": 1.0, gradient_term: z_value},
            )
            model_results_rows.append(
                model_summary_row(
                    spec,
                    "fitted_ddd",
                    result,
                    model,
                    frame,
                    raw_count=float(raw_count),
                    standardized_density=z_value,
                    measure=raw_column,
                )
            )
    model_results_rows.append(
        model_summary_row(
            "market_new_baseline",
            "high_minus_low_ddd",
            market_baseline_result,
            market_baseline_model,
            market_baseline_work,
            measure="market-new outcome",
        )
    )
    market_gradient_term = "post_X_treated_X_disp_X_density"
    market_mean_result = linear_combination(
        market_density_model, {"post_X_treated_X_disp": 1.0}
    )
    model_results_rows.append(
        model_summary_row(
            "market_new_raw_500m_interaction",
            "ddd_at_member_event_mean",
            market_mean_result,
            market_density_model,
            market_density_work,
            standardized_density=0.0,
            measure=RAW_500,
        )
    )
    market_gradient_result = linear_combination(
        market_density_model, {market_gradient_term: 1.0}
    )
    model_results_rows.append(
        model_summary_row(
            "market_new_raw_500m_interaction",
            "density_gradient_per_sd",
            market_gradient_result,
            market_density_model,
            market_density_work,
            measure=RAW_500,
        )
    )
    for raw_count in PRIMARY_COUNTS:
        z_value = standardize_raw_value(float(raw_count), market_transform)
        result = linear_combination(
            market_density_model,
            {"post_X_treated_X_disp": 1.0, market_gradient_term: z_value},
        )
        model_results_rows.append(
            model_summary_row(
                "market_new_raw_500m_interaction",
                "fitted_ddd",
                result,
                market_density_model,
                market_density_work,
                raw_count=float(raw_count),
                standardized_density=z_value,
                measure=RAW_500,
            )
        )
    for spec, model, frame in [
        ("low_density_le3_descriptive", low_model, low_work),
        ("preferred_store_event_post_fe", store_fe_model, store_fe_work),
    ]:
        result = linear_combination(model, {"post_X_treated_X_disp": 1.0})
        model_results_rows.append(
            model_summary_row(spec, "high_minus_low_ddd", result, model, frame)
        )
    model_results = pd.DataFrame(model_results_rows)

    print(f"[5/9] Running restricted wild-cluster bootstrap ({args.bootstrap_reps:,} repetitions per test)", flush=True)
    bootstrap_rows: List[Dict[str, Any]] = []
    focal_specs = [
        "paper_facing_baseline",
        "raw_500m_interaction",
        "log_500m_interaction",
        "raw_1500m_interaction",
        "log_1500m_interaction",
        "market_new_baseline",
        "market_new_raw_500m_interaction",
        "low_density_le3_descriptive",
        "preferred_store_event_post_fe",
    ]
    for spec in focal_specs:
        estimand = (
            "ddd_at_member_event_mean" if "interaction" in spec else "high_minus_low_ddd"
        )
        weights = {"post_X_treated_X_disp": 1.0}
        pvalue = restricted_wild_cluster_pvalue(
            models[spec], weights, args.bootstrap_reps, SEED
        )
        bootstrap_rows.append(
            {
                "spec": spec,
                "estimand": estimand,
                "raw_count": np.nan,
                "pvalue_wild_restricted": pvalue,
                "repetitions": args.bootstrap_reps,
                "seed": SEED,
                "weight_distribution": "Rademacher",
                "bootstrap_type": "restricted cluster bootstrap-t",
                "cluster": CLUSTER,
                "closure_clusters": len(models[spec]["cluster_labels"]),
            }
        )
    primary_model = models["raw_500m_interaction"]
    primary_transform = transforms["raw_500m_interaction"]
    for estimand, weights, raw_count in [
        ("density_gradient_per_sd", {"post_X_treated_X_disp_X_density": 1.0}, np.nan),
        *[
            (
                "fitted_ddd",
                {
                    "post_X_treated_X_disp": 1.0,
                    "post_X_treated_X_disp_X_density": standardize_raw_value(count, primary_transform),
                },
                count,
            )
            for count in PRIMARY_COUNTS
        ],
    ]:
        bootstrap_rows.append(
            {
                "spec": "raw_500m_interaction",
                "estimand": estimand,
                "raw_count": raw_count,
                "pvalue_wild_restricted": restricted_wild_cluster_pvalue(
                    primary_model, weights, args.bootstrap_reps, SEED
                ),
                "repetitions": args.bootstrap_reps,
                "seed": SEED,
                "weight_distribution": "Rademacher",
                "bootstrap_type": "restricted cluster bootstrap-t",
                "cluster": CLUSTER,
                "closure_clusters": len(primary_model["cluster_labels"]),
            }
        )
    bootstrap = pd.DataFrame(bootstrap_rows)

    print("[6/9] Estimating leave-one-closure-out and dynamic diagnostics", flush=True)
    loo_rows: List[Dict[str, Any]] = []
    primary_work = model_frames["raw_500m_interaction"]
    primary_terms = models["raw_500m_interaction"]["names"]
    for omitted in sorted(primary_work[CLUSTER].unique()):
        subset = primary_work.loc[primary_work[CLUSTER].ne(omitted)].copy()
        loo_model = fit_fe_ols(
            subset, OUTCOME, primary_terms, BASE_FIXED_EFFECTS, CLUSTER
        )
        loo_estimands = {
            "ddd_at_full_sample_mean": {"post_X_treated_X_disp": 1.0},
            "density_gradient_per_sd": {"post_X_treated_X_disp_X_density": 1.0},
            "fitted_ddd_count_2": {
                "post_X_treated_X_disp": 1.0,
                "post_X_treated_X_disp_X_density": standardize_raw_value(2, primary_transform),
            },
            "fitted_ddd_count_13": {
                "post_X_treated_X_disp": 1.0,
                "post_X_treated_X_disp_X_density": standardize_raw_value(13, primary_transform),
            },
        }
        for estimand, weights in loo_estimands.items():
            result = linear_combination(loo_model, weights)
            loo_rows.append(
                {
                    "omitted_closure_event_id": omitted,
                    "estimand": estimand,
                    **result,
                    "observations": loo_model["n"],
                    "closure_clusters": len(loo_model["cluster_labels"]),
                }
            )
    loo = pd.DataFrame(loo_rows)

    event_work, event_terms, event_term_map = add_event_study_terms(
        regression_frame, "density_z_raw_500m"
    )
    event_model = fit_fe_ols(
        event_work,
        OUTCOME,
        event_terms,
        BASE_FIXED_EFFECTS,
        CLUSTER,
        drop_fe_singletons=False,
    )
    event_results = event_study_results(
        event_model, event_term_map, primary_transform, [2.0, 13.0]
    )
    pre_gradient_terms = [
        event_term_map[period]["treated_X_disp_X_density"]
        for period in [-4, -3, -2]
    ]
    pretrend_rows = [
        joint_zero_test(
            event_model,
            pre_gradient_terms,
            "density-gradient event-study coefficients jointly zero in periods -4,-3,-2",
        )
    ]
    model_specs_rows.append(
        {
            "spec": "raw_500m_density_interacted_event_study",
            "outcome": OUTCOME,
            "regressors": " + ".join(event_terms),
            "fixed_effects": " + ".join(BASE_FIXED_EFFECTS),
            "cluster": CLUSTER,
            "weights": "none",
            "sample": "same exact population as paper-facing baseline; period -1 reference",
        }
    )

    store_event_frame = regression_frame.copy()
    store_event_frame["preferred_store_event_period_fe"] = (
        store_event_frame[CLUSTER].astype(str)
        + "|store_"
        + store_event_frame["preferred_store"].astype(str)
        + "|rel_"
        + store_event_frame["rel_t"].astype(str)
    )
    store_event_work, store_event_terms, store_event_map = add_store_fe_event_study_terms(
        store_event_frame
    )
    store_event_fixed_effects = [*BASE_FIXED_EFFECTS, "preferred_store_event_period_fe"]
    store_event_model = fit_fe_ols(
        store_event_work,
        OUTCOME,
        store_event_terms,
        store_event_fixed_effects,
        CLUSTER,
        drop_fe_singletons=False,
    )
    store_event_results = store_fe_event_study_results(store_event_model, store_event_map)
    pretrend_rows.append(
        joint_zero_test(
            store_event_model,
            [store_event_map[period] for period in [-4, -3, -2]],
            "preferred-store-event-period-FE DDD coefficients jointly zero in periods -4,-3,-2",
        )
    )
    model_specs_rows.append(
        {
            "spec": "preferred_store_event_period_fe_event_study",
            "outcome": OUTCOME,
            "regressors": " + ".join(store_event_terms),
            "fixed_effects": " + ".join(store_event_fixed_effects),
            "cluster": CLUSTER,
            "weights": "none",
            "sample": "full baseline population; treatment-by-period terms absorbed; period -1 reference",
        }
    )
    pretrend = pd.DataFrame(pretrend_rows)

    cell_level = (
        regression_frame.groupby([CLUSTER, "preferred_store", "treated", "rel_t"], observed=True)
        .agg(
            observations=(OUTCOME, "size"),
            incidence_groups=("disp_binary", "nunique"),
            low_incidence_observations=("disp_binary", lambda values: int(values.eq(0).sum())),
            high_incidence_observations=("disp_binary", lambda values: int(values.eq(1).sum())),
        )
        .reset_index()
    )
    cell_level["contains_both_incidence_groups"] = cell_level["incidence_groups"].eq(2)
    cell_summary = (
        cell_level.groupby(["treated", "rel_t"], observed=True)
        .agg(
            store_event_period_cells=("preferred_store", "size"),
            cells_with_both_incidence_groups=("contains_both_incidence_groups", "sum"),
            observations=("observations", "sum"),
        )
        .reset_index()
    )
    cell_summary["share_cells_with_both_incidence_groups"] = (
        cell_summary["cells_with_both_incidence_groups"]
        / cell_summary["store_event_period_cells"]
    )

    print("[7/9] Building balance, support, benchmark, and figures", flush=True)
    balance, common, matched = build_balance_outputs(design)
    low_support, low_metadata = support_for_low_density(low_model["work"], design)
    baseline_row = find_result(model_results, "paper_facing_baseline", "high_minus_low_ddd")
    primary_mean = find_result(model_results, "raw_500m_interaction", "ddd_at_member_event_mean")
    primary_zero = find_result(model_results, "raw_500m_interaction", "fitted_ddd", 0.0)
    primary_low = find_result(model_results, "raw_500m_interaction", "fitted_ddd", 2.0)
    primary_middle = find_result(model_results, "raw_500m_interaction", "fitted_ddd", 5.0)
    primary_high = find_result(model_results, "raw_500m_interaction", "fitted_ddd", 13.0)
    primary_gradient = find_result(model_results, "raw_500m_interaction", "density_gradient_per_sd")
    low_result = find_result(
        model_results, "low_density_le3_descriptive", "high_minus_low_ddd"
    )
    store_fe_result = find_result(
        model_results, "preferred_store_event_post_fe", "high_minus_low_ddd"
    )
    market_baseline_row = find_result(
        model_results, "market_new_baseline", "high_minus_low_ddd"
    )
    market_mean_row = find_result(
        model_results, "market_new_raw_500m_interaction", "ddd_at_member_event_mean"
    )
    market_gradient_row = find_result(
        model_results, "market_new_raw_500m_interaction", "density_gradient_per_sd"
    )
    market_low_row = find_result(
        model_results, "market_new_raw_500m_interaction", "fitted_ddd", 2.0
    )
    market_middle_row = find_result(
        model_results, "market_new_raw_500m_interaction", "fitted_ddd", 5.0
    )
    market_high_row = find_result(
        model_results, "market_new_raw_500m_interaction", "fitted_ddd", 13.0
    )
    threshold = 0.25 * abs(float(baseline_row["estimate"]))
    benchmark_rows = []
    for location, result in [
        ("member_event_mean", primary_mean),
        ("raw_count_2", primary_low),
        ("raw_count_13", primary_high),
    ]:
        difference = abs(float(result["estimate"]) - float(baseline_row["estimate"]))
        benchmark_rows.append(
            {
                "location": location,
                "baseline_estimate": float(baseline_row["estimate"]),
                "fitted_estimate": float(result["estimate"]),
                "absolute_difference": difference,
                "percentage_change_relative_to_absolute_baseline": (
                    100 * difference / abs(float(baseline_row["estimate"]))
                ),
                "threshold_25pct_baseline_magnitude": threshold,
                "within_25pct_benchmark": difference <= threshold,
            }
        )
    benchmark = pd.DataFrame(benchmark_rows)

    support_500 = common.loc[common["measure"].eq(RAW_500)].iloc[0]
    curve_500 = fitted_curve_data(
        primary_model,
        primary_transform,
        float(design[RAW_500].min()),
        float(design[RAW_500].max()),
    )
    marker_500 = model_results.loc[
        model_results["spec"].eq("raw_500m_interaction")
        & model_results["estimand"].eq("fitted_ddd")
        & model_results["raw_count"].isin([2.0, 5.0, 13.0])
    ].copy()
    curve_500.to_csv(output_dir / "fitted_ddd_curve_500m.csv", index=False)
    plot_density_ecdf(design, common, output_dir / "store_density_ecdf_500m.png")
    plot_fitted_curve(
        curve_500,
        marker_500,
        float(support_500["common_support_min"]),
        float(support_500["common_support_max"]),
        500,
        output_dir / "fitted_ddd_500m.png",
    )

    raw1500_model = models["raw_1500m_interaction"]
    raw1500_transform = transforms["raw_1500m_interaction"]
    support_1500 = common.loc[common["measure"].eq(RAW_1500)].iloc[0]
    curve_1500 = fitted_curve_data(
        raw1500_model,
        raw1500_transform,
        float(design[RAW_1500].min()),
        float(design[RAW_1500].max()),
    )
    marker_1500 = model_results.loc[
        model_results["spec"].eq("raw_1500m_interaction")
        & model_results["estimand"].eq("fitted_ddd")
        & model_results["raw_count"].isin(q1500)
    ].copy()
    curve_1500.to_csv(output_dir / "fitted_ddd_curve_1500m.csv", index=False)
    plot_fitted_curve(
        curve_1500,
        marker_1500,
        float(support_1500["common_support_min"]),
        float(support_1500["common_support_max"]),
        1500,
        output_dir / "fitted_ddd_1500m.png",
    )
    plot_density_event_study(
        event_results,
        output_dir / "density_interacted_event_study_500m.png",
        float(support_500["common_support_min"]),
        float(support_500["common_support_max"]),
    )

    baseline_sign = np.sign(float(baseline_row["estimate"]))
    common_curve = curve_500.loc[
        curve_500["raw_count"].between(
            float(support_500["common_support_min"]),
            float(support_500["common_support_max"]),
        )
    ]
    reversal_in_common_support = bool(
        (np.sign(common_curve["estimate"].replace(0, np.nan).dropna()) != baseline_sign).any()
    )
    key_primary = [primary_low, primary_middle, primary_high]
    point_stable = bool(benchmark["within_25pct_benchmark"].all())
    key_same_sign = all(np.sign(float(row["estimate"])) == baseline_sign for row in key_primary)
    intervals_exclude_zero = all(
        float(row["ci_low"]) * float(row["ci_high"]) > 0 for row in key_primary
    )
    alt_rows = []
    for spec in ["log_500m_interaction", "raw_1500m_interaction", "log_1500m_interaction"]:
        alt_rows.extend(
            model_results.loc[
                model_results["spec"].eq(spec) & model_results["estimand"].eq("fitted_ddd")
            ].iloc[-3:].to_dict("records")
        )
    alternative_same_sign = all(
        np.sign(float(row["estimate"])) == baseline_sign for row in alt_rows
    )
    market_key_rows = [
        find_result(model_results, "market_new_raw_500m_interaction", "fitted_ddd", count)
        for count in [2.0, 5.0, 13.0]
    ]
    market_same_sign = all(
        np.sign(float(row["estimate"])) == baseline_sign for row in market_key_rows
    )
    pre_gradient_values = [
        linear_combination(event_model, {term: 1.0})["estimate"]
        for term in pre_gradient_terms
    ]
    nonzero_pre_signs = [np.sign(value) for value in pre_gradient_values if value != 0]
    systematic_pre_gradient = bool(
        float(pretrend.iloc[0]["pvalue_f_cluster_df"]) < 0.05
        and len(nonzero_pre_signs) == len(pre_gradient_values)
        and len(set(nonzero_pre_signs)) == 1
    )
    if reversal_in_common_support or not key_same_sign or systematic_pre_gradient:
        classification = "Challenging"
    elif point_stable and alternative_same_sign and market_same_sign and intervals_exclude_zero:
        classification = "Supportive"
    else:
        classification = "Mixed"

    print("[8/9] Saving tables, metadata, and paper-ready summary", flush=True)
    model_specs = pd.DataFrame(model_specs_rows)
    coefficient_output: List[Dict[str, Any]] = []
    covariance_output: List[Dict[str, Any]] = []
    for spec, model in models.items():
        coefficient_output.extend(coefficient_rows(spec, model))
        covariance_output.extend(covariance_rows(spec, model))
    coefficient_output.extend(coefficient_rows("raw_500m_density_interacted_event_study", event_model))
    coefficient_output.extend(coefficient_rows("preferred_store_event_period_fe_event_study", store_event_model))
    covariance_output.extend(covariance_rows("raw_500m_density_interacted_event_study", event_model))
    covariance_output.extend(covariance_rows("preferred_store_event_period_fe_event_study", store_event_model))

    main_table = build_main_table(model_results, bootstrap, model_specs, transforms, design)
    main_table.to_csv(output_dir / "main_table.csv", index=False)
    (output_dir / "main_table.md").write_text(
        "# Main cafe-density robustness table\n\n" + markdown_table(main_table) + "\n",
        encoding="utf-8",
    )
    design.to_csv(output_dir / "design_store_density.csv", index=False)
    regression_frame.drop_duplicates("event_fe_id")[
        [
            "event_fe_id", "member_id", CLUSTER, "treated", "disp_binary",
            "preferred_store", RAW_500, RAW_1500,
            "density_z_raw_500m", "density_z_log_500m",
            "density_z_raw_1500m", "density_z_log_1500m",
        ]
    ].to_csv(output_dir / "member_first_regression_episode_density.csv", index=False)
    market_regression_frame.drop_duplicates("event_fe_id")[
        [
            "event_fe_id", "member_id", CLUSTER, "treated", "disp_binary",
            "preferred_store", RAW_500, RAW_1500, "density_z_raw_500m",
        ]
    ].to_csv(output_dir / "market_new_regression_episode_density.csv", index=False)
    balance.to_csv(output_dir / "store_density_balance.csv", index=False)
    common.to_csv(output_dir / "density_common_support.csv", index=False)
    matched.to_csv(output_dir / "matched_set_density.csv", index=False)
    model_results.to_csv(output_dir / "model_estimands.csv", index=False)
    model_results.loc[
        model_results["spec"].isin(
            ["market_new_baseline", "market_new_raw_500m_interaction"]
        )
    ].to_csv(output_dir / "market_new_outcome_sensitivity.csv", index=False)
    pd.DataFrame(coefficient_output).to_csv(output_dir / "model_coefficients.csv", index=False)
    pd.DataFrame(covariance_output).to_csv(output_dir / "model_covariance_long.csv", index=False)
    model_specs.to_csv(output_dir / "model_specifications.csv", index=False)
    bootstrap.to_csv(output_dir / "wild_cluster_bootstrap.csv", index=False)
    loo.to_csv(output_dir / "leave_one_closure_out.csv", index=False)
    event_results.to_csv(output_dir / "density_interacted_event_study_500m.csv", index=False)
    store_event_results.to_csv(output_dir / "preferred_store_event_period_fe_event_study.csv", index=False)
    pretrend.to_csv(output_dir / "event_study_joint_tests.csv", index=False)
    cell_level.to_csv(output_dir / "store_event_period_cell_support.csv", index=False)
    cell_summary.to_csv(output_dir / "store_event_period_support_summary.csv", index=False)
    low_support.to_csv(output_dir / "low_density_incidence_support.csv", index=False)
    (output_dir / "low_density_support.json").write_text(
        json.dumps(low_metadata, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    benchmark.to_csv(output_dir / "stability_benchmark.csv", index=False)

    metadata = {
        "run_timestamp": datetime.now().astimezone().isoformat(),
        "git_commit": git_commit(root),
        "project_root": str(root),
        "goal_file": "README/2026_08_11_time_invariant_competition_robustness_goal.md",
        "evidence_classification": classification,
        "source": density_metadata,
        "orders": order_metadata,
        "paper_facing_sample": {
            "path": str(sample_path),
            "sha256": EXPECTED_SAMPLE_SHA256,
            "panel_rows": int(len(sample)),
            "outcome_nonmissing_rows": int(sample[OUTCOME].notna().sum()),
            "fe_singleton_rows_removed": int(initial_singleton_drops),
            "regression_rows": int(len(regression_frame)),
            "member_events": int(regression_frame["event_fe_id"].nunique()),
            "closure_clusters": int(regression_frame[CLUSTER].nunique()),
        },
        "market_new_outcome_sensitivity_sample": {
            "path": str(market_new_sample_path),
            "sha256": EXPECTED_MARKET_NEW_SAMPLE_SHA256,
            "panel_rows": int(len(market_new_sample)),
            "outcome_nonmissing_rows": int(market_new_sample[OUTCOME].notna().sum()),
            "fe_singleton_rows_removed": int(market_singleton_drops),
            "regression_rows": int(len(market_regression_frame)),
            "member_events": int(market_regression_frame["event_fe_id"].nunique()),
            "closure_clusters": int(market_regression_frame[CLUSTER].nunique()),
            "published_baseline_coefficient": float(market_published["coef"]),
            "published_baseline_se": float(market_published["se"]),
            "baseline_coefficient_difference": float(
                market_baseline_result["estimate"] - market_published["coef"]
            ),
            "baseline_se_difference": float(
                market_baseline_result["se"] - market_published["se"]
            ),
        },
        "published_baseline": {
            "coefficient": float(published["coef"]),
            "se": float(published["se"]),
            "n": int(published["n"]),
            "source": str(baseline_path),
        },
        "independent_estimator": {
            "method": "Frisch-Waugh-Lovell alternating fixed-effect absorption and OLS",
            "crv1_correction": "G/(G-1) * (N-1)/(N-K_slope)",
            "reference_df": "G-1",
            "baseline_coefficient_difference": float(baseline_result["estimate"] - published["coef"]),
            "baseline_se_difference": float(baseline_result["se"] - published["se"]),
            "reason": "mktserver filesystem was 100% full and local Python lacked pyfixest; acceptance is conditional on baseline reproduction.",
        },
        "density_standardization": transforms,
        "standardization_population": (
            "One unweighted row per member-event in the exact nonmissing, post-singleton-removal baseline outcome population; population SD (ddof=0)."
        ),
        "primary_raw_counts": list(PRIMARY_COUNTS),
        "alternative_1500m_design_store_quantiles": {
            "q25": q1500[0], "median": q1500[1], "q75": q1500[2]
        },
        "low_density_cutoff": LOW_DENSITY_CUTOFF,
        "wild_cluster_bootstrap": {
            "repetitions": args.bootstrap_reps,
            "seed": SEED,
            "weights": "Rademacher",
            "method": "restricted cluster bootstrap-t",
        },
        "stability_benchmark": {
            "definition": "Absolute difference from baseline <=25% of absolute baseline magnitude",
            "threshold": threshold,
        },
        "classification_diagnostics": {
            "reversal_in_common_support": reversal_in_common_support,
            "primary_counts_same_baseline_sign": key_same_sign,
            "measurement_sensitivities_same_baseline_sign": alternative_same_sign,
            "market_new_counts_same_baseline_sign": market_same_sign,
            "all_primary_count_intervals_exclude_zero": intervals_exclude_zero,
            "systematic_pre_period_density_gradient": systematic_pre_gradient,
            "pre_period_density_gradient_estimates": pre_gradient_values,
            "pre_period_joint_f_pvalue": float(
                pretrend.iloc[0]["pvalue_f_cluster_df"]
            ),
        },
        "no_rematching": True,
        "no_reweighting": True,
        "no_trimming_or_winsorization": True,
        "regression_weights": "none",
    }
    (output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    pd.DataFrame(checks).to_csv(output_dir / "validation_checks.csv", index=False)

    write_summary(
        output_dir / "summary.md",
        classification,
        baseline_row,
        primary_mean,
        primary_zero,
        primary_low,
        primary_middle,
        primary_high,
        primary_gradient,
        low_result,
        store_fe_result,
        market_baseline_row,
        market_mean_row,
        market_low_row,
        market_middle_row,
        market_high_row,
        market_gradient_row,
        bootstrap,
        balance,
        common,
        pretrend.iloc[0],
        pretrend.iloc[1],
        pre_gradient_values,
        benchmark,
        low_metadata,
        loo,
        args.bootstrap_reps,
    )
    print("[9/9] Estimation complete", flush=True)
    print(f"Outputs: {output_dir}", flush=True)
    print(f"Evidence classification: {classification}", flush=True)
    print(
        f"Baseline DDD {baseline_row['estimate']:.6f}; primary mean-density DDD {primary_mean['estimate']:.6f}; "
        f"gradient {primary_gradient['estimate']:.6f}",
        flush=True,
    )


if __name__ == "__main__":
    main()
