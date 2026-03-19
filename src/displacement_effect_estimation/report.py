from __future__ import annotations

from pathlib import Path

import pandas as pd


def save_outputs(
    output_dir: Path,
    sample: pd.DataFrame,
    binary_terms: pd.DataFrame,
    binary_fit: pd.DataFrame,
    score_terms: pd.DataFrame,
    score_fit: pd.DataFrame,
    event_terms: pd.DataFrame,
    event_fit: pd.DataFrame,
    pretrend_tests: pd.DataFrame,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    sample.to_csv(output_dir / "estimation_sample.csv", index=False)
    binary_terms.to_csv(output_dir / "ddd_binary_results.csv", index=False)
    binary_fit.to_csv(output_dir / "ddd_binary_fit.csv", index=False)
    score_terms.to_csv(output_dir / "ddd_score_results.csv", index=False)
    score_fit.to_csv(output_dir / "ddd_score_fit.csv", index=False)
    event_terms.to_csv(output_dir / "event_study_results.csv", index=False)
    event_fit.to_csv(output_dir / "event_study_fit.csv", index=False)
    pretrend_tests.to_csv(output_dir / "pretrend_joint_tests.csv", index=False)

    comparison = pd.concat(
        [
            binary_terms.assign(group="binary"),
            score_terms.assign(group="score"),
            event_terms.assign(group="event_study"),
        ],
        ignore_index=True,
    )
    comparison.to_csv(output_dir / "spec_comparison.csv", index=False)

    lines = [
        "# Displacement Effect Estimation Summary",
        "",
        f"- Sample rows: {len(sample):,}",
        f"- Unique members: {sample['member_id'].nunique():,}",
        f"- Unique closures: {sample[['dept_id', 'closure_start']].drop_duplicates().shape[0]:,}",
        f"- Event FE units: {sample['event_fe_id'].nunique():,}",
        f"- Relative periods: {sorted(sample['rel_t'].unique().tolist())}",
        "",
        "## Binary Specs",
        binary_terms.to_markdown(index=False),
        "",
        "## Score Spec",
        score_terms.to_markdown(index=False),
        "",
        "## Event-study Specs",
        event_terms.to_markdown(index=False),
        "",
        "## Pre-trend Joint Tests",
        pretrend_tests.to_markdown(index=False),
    ]
    (output_dir / "summary.md").write_text("\n".join(lines), encoding="utf-8")
