"""Refit the current novelty DDD on a saved estimation sample.

This is useful for closure-registry sensitivity checks when the expensive
feature-construction cache is unavailable.  The saved sample fixes the outcome
and covariates; the supplied registry selects closure events, and the current
estimation code recomputes coefficients and inference.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODULE_DIR = PROJECT_ROOT / "src" / "displacement_effect_estimation"
sys.path.insert(0, str(MODULE_DIR))

from specs import fit_collapsed_specs, fit_event_study_specs  # noqa: E402


def _event_keys(frame: pd.DataFrame) -> pd.DataFrame:
    keys = frame.loc[:, ["dept_id", "closure_start"]].copy()
    keys["dept_id"] = keys["dept_id"].astype(str).str.strip()
    keys["closure_start"] = pd.to_datetime(
        keys["closure_start"], errors="raise"
    ).dt.strftime("%Y-%m-%d")
    return keys.drop_duplicates()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Refit the current novelty DDD on selected closure events."
    )
    parser.add_argument("--sample", required=True, type=Path)
    parser.add_argument("--registry", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--cluster-col", default="closure_event_id")
    args = parser.parse_args()

    sample_path = (PROJECT_ROOT / args.sample).resolve()
    registry_path = (PROJECT_ROOT / args.registry).resolve()
    output_dir = (PROJECT_ROOT / args.output_dir).resolve()

    sample = pd.read_csv(sample_path, encoding="utf-8-sig")
    registry = pd.read_csv(registry_path, encoding="utf-8-sig")
    registry_keys = _event_keys(registry)

    sample["dept_id"] = sample["dept_id"].astype(str).str.strip()
    sample["closure_start"] = pd.to_datetime(
        sample["closure_start"], errors="raise"
    ).dt.strftime("%Y-%m-%d")
    selected = sample.merge(
        registry_keys.assign(_selected_registry=1),
        on=["dept_id", "closure_start"],
        how="inner",
        validate="many_to_one",
    ).drop(columns="_selected_registry")

    selected_keys = _event_keys(selected)
    if len(selected_keys) != len(registry_keys):
        missing = registry_keys.merge(
            selected_keys,
            on=["dept_id", "closure_start"],
            how="left",
            indicator=True,
        ).loc[lambda x: x["_merge"] == "left_only", ["dept_id", "closure_start"]]
        raise ValueError(f"Saved sample is missing registry events:\n{missing}")

    binary_terms, binary_fit = fit_collapsed_specs(
        df=selected,
        outcome="variety_seeking",
        cluster_col=args.cluster_col,
        use_did=False,
    )
    event_terms, event_fit, pretrend_tests = fit_event_study_specs(
        df=selected,
        outcome="variety_seeking",
        cluster_col=args.cluster_col,
        include_length_heterogeneity=True,
        use_did=False,
        ref_period=-1,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    binary_terms.to_csv(output_dir / "ddd_binary_results.csv", index=False)
    binary_fit.to_csv(output_dir / "ddd_binary_fit.csv", index=False)
    event_terms.to_csv(output_dir / "event_study_results.csv", index=False)
    event_fit.to_csv(output_dir / "event_study_fit.csv", index=False)
    pretrend_tests.to_csv(output_dir / "pretrend_joint_tests.csv", index=False)

    support = (
        selected.groupby(["dept_id", "closure_start", "closure_event_id"], as_index=False)
        .agg(rows=("member_id", "size"), members=("member_id", "nunique"))
        .sort_values(["closure_start", "dept_id"])
    )
    support.to_csv(output_dir / "event_support.csv", index=False)

    metadata = {
        "source_sample": str(args.sample),
        "closure_registry": str(args.registry),
        "cluster_col": args.cluster_col,
        "outcome": "variety_seeking",
        "event_study_reference_period": -1,
        "closure_events": int(len(selected_keys)),
        "sample_rows_before_outcome_na_drop": int(len(selected)),
    }
    (output_dir / "refit_metadata.json").write_text(
        json.dumps(metadata, indent=2), encoding="utf-8"
    )

    ddd = binary_terms.loc[
        (binary_terms["spec"] == "binary_collapsed")
        & (binary_terms["term"] == "post_X_treated_X_disp")
    ].iloc[0]
    pretrend = pretrend_tests.loc[
        (pretrend_tests["spec"] == "event_binary_B")
        & (pretrend_tests["test"] == "pretrend_displacement_joint_zero")
    ].iloc[0]
    print(
        json.dumps(
            {
                "events": int(len(selected_keys)),
                "ddd_coef": float(ddd["coef"]),
                "ddd_se": float(ddd["se"]),
                "ddd_pvalue": float(ddd["pvalue"]),
                "ddd_n": int(ddd["n"]),
                "pretrend_pvalue": float(pretrend["pvalue"]),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
