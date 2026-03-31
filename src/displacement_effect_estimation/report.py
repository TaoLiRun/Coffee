from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from data import build_variety_period0_rows


def _table_to_markdown(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows produced._"
    return df.to_markdown(index=False)


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
    summary_title: str = "# Displacement Effect Estimation Summary",
    summary_notes: list[str] | None = None,
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
        summary_title,
        "",
        f"- Sample rows: {len(sample):,}",
        f"- Unique members: {sample['member_id'].nunique():,}",
        f"- Unique closures: {sample[['dept_id', 'closure_start']].drop_duplicates().shape[0]:,}",
        f"- Event FE units: {sample['event_fe_id'].nunique():,}",
        f"- Relative periods: {sorted(sample['rel_t'].unique().tolist())}",
        "",
        "## Binary Specs",
        _table_to_markdown(binary_terms),
        "",
        "## Score Spec",
        _table_to_markdown(score_terms),
        "",
        "## Event-study Specs",
        _table_to_markdown(event_terms),
        "",
        "## Pre-trend Joint Tests",
        _table_to_markdown(pretrend_tests),
    ]
    if summary_notes:
        lines[7:7] = [*summary_notes, ""]
    (output_dir / "summary.md").write_text("\n".join(lines), encoding="utf-8")


def save_variety_panel_plot(
    *,
    output_dir: Path,
    sample: pd.DataFrame,
    cfg: dict,
    variety_seeking_mode: str,
) -> None:
    """Save mean ± SD trend plot of variety_seeking for rel_t in [-k..-1,0,1..k]."""
    required = {"member_id", "dept_id", "closure_start", "closure_end", "group", "treated", "rel_t", "variety_seeking"}
    missing = required - set(sample.columns)
    if missing:
        raise ValueError(f"sample missing required columns for variety plot: {sorted(missing)}")

    base = sample[
        ["member_id", "dept_id", "closure_start", "closure_end", "group", "treated", "rel_t", "variety_seeking"]
    ].copy()
    period0 = build_variety_period0_rows(
        sample=sample,
        cfg=cfg,
        variety_seeking_mode=variety_seeking_mode,
    )
    if not period0.empty:
        period0 = period0[
            ["member_id", "dept_id", "closure_start", "closure_end", "group", "treated", "rel_t", "variety_seeking"]
        ].copy()
        period0["variety_seeking"] = period0["variety_seeking"].fillna(0.0)

    panel_for_plot = pd.concat([base, period0], ignore_index=True)

    agg = (
        panel_for_plot.groupby(["group", "rel_t"], sort=True)["variety_seeking"]
        .agg(["mean", "std"])
        .reset_index()
    )

    x_vals = sorted(agg["rel_t"].unique().tolist())
    colors = {"treatment": "#d62728", "control": "#1f77b4"}

    fig, ax = plt.subplots(figsize=(8, 5))
    for group in ["treatment", "control"]:
        sub = agg[agg["group"] == group].sort_values("rel_t")
        if sub.empty:
            continue
        x = sub["rel_t"].values
        y = sub["mean"].values
        std = np.where(np.isnan(sub["std"].values), 0, sub["std"].values)
        ax.plot(x, y, "o-", color=colors.get(group, "#2f2f2f"), linewidth=2, markersize=5, label=group.capitalize())
        ax.fill_between(x, y - std, y + std, color=colors.get(group, "#2f2f2f"), alpha=0.2)

    ax.axvline(x=0, color="gray", linestyle="--", alpha=0.7)
    ax.set_xlabel("Relative period t (0 = closure window)")
    ax.set_ylabel("Variety seeking")
    ax.set_title("Variety seeking by period (mean ± SD)")
    ax.set_xticks(x_vals)
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()

    output_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_dir / "variety_panel_trend_mean_sd.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    agg.to_csv(output_dir / "variety_panel_trend_stats.csv", index=False)
