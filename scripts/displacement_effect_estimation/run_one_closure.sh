#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SRC_DIR="$PROJECT_ROOT/src/displacement_effect_estimation"
OUT_ROOT="$PROJECT_ROOT/outputs/displacement_effect_estimation"

WINDOW_DAYS="${WINDOW_DAYS:-28}"
T_HORIZON="${T_HORIZON:-4}"
OUTCOME="${OUTCOME:-n_purchases}"
THRESHOLDS="${THRESHOLDS:-0.5}"
CLUSTER_COL="${CLUSTER_COL:-member_id}"
CLOSURE_IDX="${CLOSURE_IDX:-0}"
OUTPUT_SUBDIR="${OUTPUT_SUBDIR:-one_closure_test}"

PYTHON_BIN="${PYTHON_BIN:-/home/litao/anaconda3/bin/python}"

mkdir -p "$OUT_ROOT/logs"

cd "$SRC_DIR"

"$PYTHON_BIN" -u - <<'PY'
from pathlib import Path
import os
import pandas as pd

from data import load_config, load_displacement_scores, load_orders_for_behavior, _window_bounds, _slice_by_date
from report import save_outputs
from specs import fit_threshold_specs, fit_score_spec, fit_event_study_specs


def parse_thresholds(text: str) -> list[float]:
    vals = [x.strip() for x in text.split(",") if x.strip()]
    if not vals:
        raise ValueError("threshold list is empty")
    return [float(v) for v in vals]


cfg = load_config()
project_root = Path(__file__).resolve().parents[2]

window_days = int(os.environ.get("WINDOW_DAYS", "28"))
t_horizon = int(os.environ.get("T_HORIZON", "4"))
outcome = os.environ.get("OUTCOME", "n_purchases")
thresholds = parse_thresholds(os.environ.get("THRESHOLDS", "0.5"))
cluster_col = os.environ.get("CLUSTER_COL", "member_id")
closure_idx = int(os.environ.get("CLOSURE_IDX", "0"))
output_subdir = os.environ.get("OUTPUT_SUBDIR", "one_closure_test")

if outcome != "n_purchases":
    raise ValueError("This script currently supports OUTCOME=n_purchases only.")
if t_horizon < 1:
    raise ValueError("T_HORIZON must be >= 1")

scores = load_displacement_scores(cfg=cfg)
orders = load_orders_for_behavior(cfg=cfg)

closures = (
    scores[["dept_id", "closure_start", "closure_end"]]
    .drop_duplicates()
    .sort_values(["closure_start", "dept_id"])
    .reset_index(drop=True)
)
if closures.empty:
    raise ValueError("No closures available in displacement_scores_t0_ex_ante.csv")
if closure_idx < 0 or closure_idx >= len(closures):
    raise ValueError(f"CLOSURE_IDX out of range: {closure_idx}. Valid range: 0..{len(closures)-1}")

pick = closures.iloc[closure_idx]
dept_id = int(pick["dept_id"])
closure_start = str(pick["closure_start"])
closure_end = str(pick["closure_end"])

cohort = scores[
    (scores["dept_id"] == dept_id)
    & (scores["closure_start"] == closure_start)
    & (scores["closure_end"] == closure_end)
].copy()
if cohort.empty:
    raise ValueError("Selected closure has no cohort rows.")

member_frame = cohort[
    [
        "member_id",
        "dept_id",
        "closure_start",
        "closure_end",
        "closure_duration_days",
        "group",
        "treated",
        "displacement_prob",
    ]
].drop_duplicates()
members = set(member_frame["member_id"].tolist())

rel_t_values = list(range(-t_horizon, 0)) + list(range(1, t_horizon + 1))
closure_start_dt = pd.to_datetime(closure_start)
closure_end_dt = pd.to_datetime(closure_end)

parts = []
for rel_t in rel_t_values:
    start_dt, end_dt = _window_bounds(closure_start_dt, closure_end_dt, rel_t, window_days)
    win = _slice_by_date(orders, start_dt, end_dt)
    if not win.empty:
        win = win[win["member_id"].isin(members)]
        counts = win.groupby("member_id")["date"].nunique().rename("_purchase_days").reset_index()
    else:
        counts = pd.DataFrame(columns=["member_id", "_purchase_days"])

    block = member_frame.merge(counts, on="member_id", how="left")
    block["_purchase_days"] = block["_purchase_days"].fillna(0)
    block["n_purchases"] = block["_purchase_days"] / float(window_days)
    block["rel_t"] = int(rel_t)
    block["post"] = (block["rel_t"] > 0).astype(int)
    parts.append(
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
                "rel_t",
                "post",
                "n_purchases",
            ]
        ]
    )

sample = pd.concat(parts, ignore_index=True)
sample["event_fe_id"] = (
    sample["member_id"].astype(str)
    + "|"
    + sample["dept_id"].astype(str)
    + "|"
    + sample["closure_start"].astype(str)
)

for tau in thresholds:
    tag = str(tau).replace(".", "")
    sample[f"disp_{tag}"] = (sample["displacement_prob"] >= tau).astype(int)

threshold_terms, threshold_fit = fit_threshold_specs(sample, outcome=outcome, thresholds=thresholds, cluster_col=cluster_col)
score_terms, score_fit = fit_score_spec(sample, outcome=outcome, cluster_col=cluster_col)
event_terms, event_fit = fit_event_study_specs(sample, outcome=outcome, thresholds=thresholds, cluster_col=cluster_col)

out_dir = project_root / cfg["paths"]["output_dir"] / output_subdir / f"dept_{dept_id}_start_{closure_start}"
save_outputs(
    output_dir=out_dir,
    sample=sample,
    threshold_terms=threshold_terms,
    threshold_fit=threshold_fit,
    score_terms=score_terms,
    score_fit=score_fit,
    event_terms=event_terms,
    event_fit=event_fit,
)

print("One-closure workflow finished")
print(f"  Closure: dept_id={dept_id}, closure_start={closure_start}, closure_end={closure_end}")
print(f"  Rows: {len(sample):,}")
print(f"  Members: {sample['member_id'].nunique():,}")
print(f"  Relative periods: {sorted(sample['rel_t'].unique().tolist())}")
print(f"  Output dir: {out_dir}")
PY
