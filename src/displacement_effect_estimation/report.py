from __future__ import annotations

from pathlib import Path
import re

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


def _extract_rel_t(term: str) -> int | None:
    match = re.search(r"C\(rel_t, contr\.treatment\(base=-?\d+\)\)\[(-?\d+)\]", term)
    if match:
        return int(match.group(1))

    match = re.search(r"rel_t::(-?\d+):", term)
    if match:
        return int(match.group(1))

    return None


def _classify_event_term(term: str) -> str | None:
    suffix_map = [
        (":treated_X_disp", "displacement"),
        (":treated_X_score", "score_slope"),
        (":treated_X_len", "length_baseline"),
        (":disp_X_len", "length_lower_order"),
        (":tXdXlen", "length_displacement"),
        (":disp_binary", "blocked_control_gap"),
        (":treated", "att_or_baseline"),
    ]
    for suffix, label in suffix_map:
        if term.endswith(suffix):
            return label
    return None


def _event_study_plot_specs(event_terms: pd.DataFrame) -> list[dict]:
    plot_specs: list[dict] = []

    if ((event_terms["spec"] == "event_att") & (event_terms["effect"] == "att_or_baseline")).any():
        plot_specs.append(
            {
                "spec": "event_att",
                "effect": "att_or_baseline",
                "filename": "event_study_att.png",
                "title": "Event-study ATT",
                "ylabel": "Coefficient",
            }
        )

    if ((event_terms["spec"] == "event_binary_B") & (event_terms["effect"] == "displacement")).any():
        plot_specs.append(
            {
                "spec": "event_binary_B",
                "effect": "displacement",
                "filename": "event_study_displacement.png",
                "title": "Event-study displacement effect",
                "ylabel": "Triple-difference coefficient",
            }
        )

    if ((event_terms["spec"] == "event_binary_B") & (event_terms["effect"] == "att_or_baseline")).any():
        plot_specs.append(
            {
                "spec": "event_binary_B",
                "effect": "att_or_baseline",
                "filename": "event_study_baseline.png",
                "title": "Event-study baseline treatment effect",
                "ylabel": "Difference-in-differences coefficient",
            }
        )

    return plot_specs


def save_event_study_plots(
    *,
    output_dir: Path,
    event_terms: pd.DataFrame,
) -> None:
    """Save coefficient plots for the main event-study effects."""
    required = {"spec", "term", "coef", "se"}
    missing = required - set(event_terms.columns)
    if missing:
        raise ValueError(f"event_terms missing required columns for event-study plots: {sorted(missing)}")

    plot_df = event_terms.copy()
    plot_df["term"] = plot_df["term"].astype(str)
    plot_df["rel_t"] = plot_df["term"].map(_extract_rel_t)
    plot_df["effect"] = plot_df["term"].map(_classify_event_term)
    plot_df = plot_df.loc[plot_df["rel_t"].notna() & plot_df["effect"].notna()].copy()
    if plot_df.empty:
        return

    plot_df["rel_t"] = plot_df["rel_t"].astype(int)
    plot_df["ci_low"] = plot_df["coef"] - 1.96 * plot_df["se"]
    plot_df["ci_high"] = plot_df["coef"] + 1.96 * plot_df["se"]
    plot_df.to_csv(output_dir / "event_study_plot_data.csv", index=False)

    output_dir.mkdir(parents=True, exist_ok=True)
    for plot_spec in _event_study_plot_specs(plot_df):
        sub = plot_df[
            (plot_df["spec"] == plot_spec["spec"])
            & (plot_df["effect"] == plot_spec["effect"])
        ].sort_values("rel_t")
        if sub.empty:
            continue

        fig, ax = plt.subplots(figsize=(8, 5))
        x = sub["rel_t"].to_numpy()
        y = sub["coef"].to_numpy()
        ci_low = sub["ci_low"].to_numpy()
        ci_high = sub["ci_high"].to_numpy()

        ax.axhline(y=0, color="black", linewidth=1, alpha=0.8)
        ax.axvline(x=0, color="gray", linestyle="--", linewidth=1.2, alpha=0.8)
        ax.plot(x, y, "o-", color="#1f4e79", linewidth=2, markersize=5)
        ax.fill_between(x, ci_low, ci_high, color="#6baed6", alpha=0.25)

        ax.set_xticks(sorted(sub["rel_t"].unique().tolist()))
        ax.set_xlabel("Relative period t")
        ax.set_ylabel(plot_spec["ylabel"])
        ax.set_title(plot_spec["title"])
        ax.grid(True, axis="y", alpha=0.25)
        fig.tight_layout()
        fig.savefig(output_dir / plot_spec["filename"], dpi=300, bbox_inches="tight")
        plt.close(fig)


def save_lower_group_displacement_event_study_plot(
    *,
    output_dir: Path,
    event_terms: pd.DataFrame,
    split_label: str,
) -> None:
    """
    Save the blocked-buyer displacement event-study path for the lower/baseline
    pre-novelty group only. This uses the filtered sample produced by the
    heterogeneity pipeline, where `novelty_pre_high == 0` identifies the lower
    group under either the full-sample median split or the quartile-tail split.
    """
    required_event = {"spec", "term", "coef", "se"}
    missing_event = required_event - set(event_terms.columns)
    if missing_event:
        raise ValueError(
            f"event_terms missing required columns for lower-group event-study plot: {sorted(missing_event)}"
        )

    plot_df = event_terms.copy()
    plot_df["term"] = plot_df["term"].astype(str)
    plot_df["rel_t"] = plot_df["term"].map(_extract_rel_t)
    plot_df["effect"] = plot_df["term"].map(_classify_event_term)
    plot_df = plot_df.loc[
        (plot_df["spec"] == "event_binary_B_pre_novelty_split")
        & (plot_df["effect"] == "displacement")
        & plot_df["rel_t"].notna()
    ].copy()
    if plot_df.empty:
        return

    plot_df["rel_t"] = plot_df["rel_t"].astype(int)
    plot_df["ci_low"] = plot_df["coef"] - 1.96 * plot_df["se"]
    plot_df["ci_high"] = plot_df["coef"] + 1.96 * plot_df["se"]

    fig, ax = plt.subplots(figsize=(8, 5))
    x = plot_df["rel_t"].to_numpy()
    y = plot_df["coef"].to_numpy()
    ci_low = plot_df["ci_low"].to_numpy()
    ci_high = plot_df["ci_high"].to_numpy()

    ax.axhline(y=0, color="black", linewidth=1, alpha=0.8)
    ax.axvline(x=0, color="gray", linestyle="--", linewidth=1.2, alpha=0.8)
    ax.plot(x, y, "o-", color="#8c2d04", linewidth=2, markersize=5)
    ax.fill_between(x, ci_low, ci_high, color="#fdbb84", alpha=0.3)
    ax.set_xticks(sorted(plot_df["rel_t"].unique().tolist()))
    ax.set_xlabel("Relative period t")
    ax.set_ylabel("Triple-difference coefficient")
    ax.set_title(f"Lower-group displacement event study ({split_label})")
    ax.grid(True, axis="y", alpha=0.25)
    fig.tight_layout()

    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"event_study_displacement_lower_group_{split_label}.png"
    fig.savefig(output_dir / filename, dpi=300, bbox_inches="tight")
    plt.close(fig)


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


def save_pre_novelty_histogram(
    *,
    output_dir: Path,
    sample: pd.DataFrame,
) -> None:
    """Save the episode-level pre-period novelty distribution and histogram."""
    stored_distribution = sample.attrs.get("pre_novelty_distribution")
    if stored_distribution is not None:
        episode_df = stored_distribution.copy()
    else:
        required = {
            "member_id",
            "dept_id",
            "closure_start",
            "novelty_pre_mean",
            "novelty_pre_split_rule",
            "novelty_pre_threshold_low",
            "novelty_pre_threshold_high",
        }
        missing = required - set(sample.columns)
        if missing:
            raise ValueError(f"sample missing required columns for pre-novelty histogram: {sorted(missing)}")

        key_cols = ["member_id", "dept_id", "closure_start"]
        episode_df = (
            sample.loc[
                sample["novelty_pre_mean"].notna(),
                key_cols
                + [
                    "novelty_pre_mean",
                    "novelty_pre_high",
                    "novelty_pre_group",
                    "novelty_pre_split_rule",
                    "novelty_pre_threshold_low",
                    "novelty_pre_threshold_high",
                ],
            ]
            .drop_duplicates(subset=key_cols)
            .copy()
        )
    if episode_df.empty:
        raise ValueError("No non-missing novelty_pre_mean values available for histogram.")

    episode_df["novelty_pre_mean"] = episode_df["novelty_pre_mean"].astype(float)
    split_rule = str(episode_df["novelty_pre_split_rule"].iloc[0])
    threshold_low = float(episode_df["novelty_pre_threshold_low"].iloc[0])
    threshold_high = float(episode_df["novelty_pre_threshold_high"].iloc[0])

    output_dir.mkdir(parents=True, exist_ok=True)
    episode_df.to_csv(output_dir / "pre_period_novelty_episode_means.csv", index=False)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(
        episode_df["novelty_pre_mean"].values,
        bins=np.linspace(0.0, 1.0, 31),
        color="#1f77b4",
        edgecolor="white",
        alpha=0.85,
    )
    ax.axvline(
        threshold_low,
        color="#d62728",
        linestyle="--",
        linewidth=2,
        label=f"low threshold = {threshold_low:.3f}",
    )
    if not np.isclose(threshold_high, threshold_low):
        ax.axvline(
            threshold_high,
            color="#2ca02c",
            linestyle="--",
            linewidth=2,
            label=f"high threshold = {threshold_high:.3f}",
        )
    ax.set_xlim(0.0, 1.0)
    ax.set_xlabel("Pre-period novelty share")
    ax.set_ylabel("Episodes")
    ax.set_title(f"Distribution of pre-period novelty ({split_rule})")
    ax.legend()
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(output_dir / "pre_period_novelty_histogram.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
