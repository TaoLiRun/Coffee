#!/usr/bin/env python3
"""Generate classifier diagnostics on the exact 18-event estimation cohort.

This script uses saved duration-specific predictions. It does not train or
refit the purchase-incidence classifiers and does not rerun the DDD models.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")
os.environ.setdefault("XDG_CACHE_HOME", "/tmp")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    auc,
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
)


ROOT = Path(__file__).resolve().parents[2]
CLASSIFIER_DIR = ROOT / "outputs" / "displacement_classification"
MAIN_SAMPLE = (
    ROOT
    / "outputs"
    / "03_main_18_closures"
    / "purchase_frequency_ddd_h4"
    / "estimation_sample.csv"
)
OUTPUT_DIR = ROOT / "outputs" / "paper" / "classifier"
FIGURE_DIR = ROOT / "writeup" / "figures"
CONFIG_PATH = ROOT / "src" / "displacement_classification" / "config.json"

KEYS = ["member_id", "dept_id", "closure_start"]
EXPECTED_EPISODES = 40_148
EXPECTED_TREATED = 7_390
EXPECTED_CONTROL = 32_758
EXPECTED_EVENTS = 18
THRESHOLD_GRID = [0.30, 0.40, 0.50, 0.60, 0.70]

SLICE_ORDER = [
    "treated_pre_t-1",
    "control_pre_t-1",
    "control_period_0",
]
SLICE_LABELS = {
    "treated_pre_t-1": "Treated, pre-period -1",
    "control_pre_t-1": "Control, pre-period -1",
    "control_period_0": "Control, period 0",
}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_div(numerator: float, denominator: float) -> float:
    return float(numerator / denominator) if denominator else float("nan")


def _calibration_intercept_slope(y: np.ndarray, prob: np.ndarray) -> tuple[float, float]:
    clipped = np.clip(prob.astype(float), 1e-6, 1 - 1e-6)
    logit = np.log(clipped / (1 - clipped)).reshape(-1, 1)
    model = LogisticRegression(penalty=None, solver="lbfgs", max_iter=2_000)
    model.fit(logit, y.astype(int))
    return float(model.intercept_[0]), float(model.coef_[0, 0])


def _metrics(rows: pd.DataFrame, threshold: float) -> dict[str, float | int]:
    y = rows["label"].to_numpy(dtype=int)
    prob = rows["predicted_probability"].to_numpy(dtype=float)
    pred = (prob >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    precision_curve, recall_curve, _ = precision_recall_curve(y, prob)
    cal_intercept, cal_slope = _calibration_intercept_slope(y, prob)
    prevalence = float(y.mean())
    brier = float(brier_score_loss(y, prob))
    constant_prevalence_brier = prevalence * (1 - prevalence)
    return {
        "n": int(len(rows)),
        "n_positive": int(y.sum()),
        "n_negative": int(len(y) - y.sum()),
        "prevalence": prevalence,
        "mean_predicted_probability": float(prob.mean()),
        "always_negative_accuracy": float(1 - prevalence),
        "threshold": float(threshold),
        "predicted_positive_share": float(pred.mean()),
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
        "accuracy": float(accuracy_score(y, pred)),
        "sensitivity": float(recall_score(y, pred, zero_division=0)),
        "specificity": _safe_div(tn, tn + fp),
        "false_positive_rate": _safe_div(fp, tn + fp),
        "false_negative_rate": _safe_div(fn, fn + tp),
        "positive_predictive_value": float(
            precision_score(y, pred, zero_division=0)
        ),
        "negative_predictive_value": _safe_div(tn, tn + fn),
        "f1": _safe_div(2 * tp, 2 * tp + fp + fn),
        "roc_auc": float(roc_auc_score(y, prob)),
        "pr_auc": float(auc(recall_curve, precision_curve)),
        "average_precision": float(average_precision_score(y, prob)),
        "brier_score": brier,
        "constant_prevalence_brier": constant_prevalence_brier,
        "brier_skill_score": float(1 - brier / constant_prevalence_brier),
        "calibration_intercept": cal_intercept,
        "calibration_slope": cal_slope,
    }


def _load_final_episodes() -> pd.DataFrame:
    usecols = KEYS + [
        "closure_end",
        "closure_duration_days",
        "treated",
        "group",
        "closure_event_id",
        "displacement_prob",
        "disp_binary",
    ]
    rows = pd.read_csv(MAIN_SAMPLE, usecols=usecols)
    for column in ["closure_start", "closure_end"]:
        rows[column] = pd.to_datetime(rows[column]).dt.strftime("%Y-%m-%d")
    episodes = rows.drop_duplicates(KEYS).copy()
    if len(episodes) != EXPECTED_EPISODES:
        raise ValueError(
            f"Expected {EXPECTED_EPISODES:,} final episodes; found {len(episodes):,}."
        )
    if episodes["closure_event_id"].nunique() != EXPECTED_EVENTS:
        raise ValueError(
            f"Expected {EXPECTED_EVENTS} closure events; found "
            f"{episodes['closure_event_id'].nunique()}."
        )
    treated = int(episodes["treated"].sum())
    if treated != EXPECTED_TREATED or len(episodes) - treated != EXPECTED_CONTROL:
        raise ValueError(
            "Final treatment-arm counts do not match the audited cohort: "
            f"treated={treated:,}, control={len(episodes) - treated:,}."
        )
    return episodes


def _load_exact_evaluation_rows(episodes: pd.DataFrame) -> tuple[pd.DataFrame, list[Path]]:
    durations = sorted(episodes["closure_duration_days"].astype(int).unique())
    paths = [CLASSIFIER_DIR / f"panel_with_scores_{duration}.parquet" for duration in durations]
    missing = [path for path in paths if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing production classifier panels: {missing}")

    chunks: list[pd.DataFrame] = []
    columns = KEYS + [
        "closure_end",
        "period",
        "is_treated",
        "label",
        "displacement_prob",
        "closure_length_days",
    ]
    for path in paths:
        panel = pd.read_parquet(path, columns=columns)
        panel = panel.loc[panel["period"].isin([-1, 0])].copy()
        panel["closure_start"] = pd.to_datetime(panel["closure_start"]).dt.strftime("%Y-%m-%d")
        panel["closure_end"] = pd.to_datetime(panel["closure_end"]).dt.strftime("%Y-%m-%d")
        chunks.append(panel)

    predictions = pd.concat(chunks, ignore_index=True)
    episode_fields = episodes[
        KEYS
        + [
            "treated",
            "closure_duration_days",
            "closure_event_id",
            "displacement_prob",
        ]
    ].rename(columns={"displacement_prob": "final_t0_probability"})
    exact = predictions.merge(
        episode_fields,
        on=KEYS,
        how="inner",
        validate="many_to_one",
    )
    if not (exact["is_treated"].astype(int) == exact["treated"].astype(int)).all():
        raise ValueError("Treatment status differs between classifier and final samples.")
    if not (
        exact["closure_length_days"].astype(int)
        == exact["closure_duration_days"].astype(int)
    ).all():
        raise ValueError("Closure duration differs between classifier and final samples.")

    exact["evaluation_slice"] = np.select(
        [
            (exact["period"] == -1) & (exact["treated"] == 1),
            (exact["period"] == -1) & (exact["treated"] == 0),
            (exact["period"] == 0) & (exact["treated"] == 0),
        ],
        SLICE_ORDER,
        default="exclude",
    )
    exact = exact.loc[exact["evaluation_slice"] != "exclude"].copy()
    exact = exact.rename(columns={"displacement_prob": "predicted_probability"})

    expected_counts = {
        "treated_pre_t-1": EXPECTED_TREATED,
        "control_pre_t-1": EXPECTED_CONTROL,
        "control_period_0": EXPECTED_CONTROL,
    }
    counts = exact.groupby("evaluation_slice").size().to_dict()
    if counts != expected_counts:
        raise ValueError(f"Exact-cohort evaluation counts differ: {counts}")
    if exact.duplicated(KEYS + ["evaluation_slice"]).any():
        raise ValueError("Duplicate episode rows found within an evaluation slice.")

    control_t0 = exact.loc[exact["evaluation_slice"] == "control_period_0"]
    max_probability_difference = float(
        np.max(
            np.abs(
                control_t0["predicted_probability"].to_numpy()
                - control_t0["final_t0_probability"].to_numpy()
            )
        )
    )
    if max_probability_difference > 1e-6:
        raise ValueError(
            "Saved period-0 audit scores do not match the final ex-ante scores; "
            f"maximum difference={max_probability_difference}."
        )
    return exact, paths


def _calibration_bins(rows: pd.DataFrame) -> pd.DataFrame:
    pieces: list[pd.DataFrame] = []
    for slice_name in SLICE_ORDER:
        sub = rows.loc[rows["evaluation_slice"] == slice_name].copy()
        sub["score_decile"] = pd.qcut(
            sub["predicted_probability"], q=10, labels=False, duplicates="drop"
        )
        grouped = (
            sub.groupby("score_decile", observed=True)
            .agg(
                n=("label", "size"),
                mean_predicted_probability=("predicted_probability", "mean"),
                observed_purchase_rate=("label", "mean"),
                min_predicted_probability=("predicted_probability", "min"),
                max_predicted_probability=("predicted_probability", "max"),
            )
            .reset_index()
        )
        grouped.insert(0, "evaluation_slice", slice_name)
        pieces.append(grouped)
    return pd.concat(pieces, ignore_index=True)


def _write_calibration_figure(bins: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(11.2, 3.6), sharex=True, sharey=True)
    for ax, slice_name in zip(axes, SLICE_ORDER):
        sub = bins.loc[bins["evaluation_slice"] == slice_name]
        ax.plot([0, 1], [0, 1], linestyle="--", color="0.55", linewidth=1)
        ax.plot(
            sub["mean_predicted_probability"],
            sub["observed_purchase_rate"],
            marker="o",
            color="#1f4e79",
            linewidth=1.6,
            markersize=4.5,
        )
        ax.set_title(SLICE_LABELS[slice_name], fontsize=9)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.grid(alpha=0.2)
    axes[0].set_ylabel("Observed purchase rate")
    for ax in axes:
        ax.set_xlabel("Mean predicted probability")
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "classifier_calibration.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def _score_overlap(episodes: pd.DataFrame, threshold: float) -> pd.DataFrame:
    rows: list[dict[str, float | int | str]] = []
    for treated, label in [(0, "Control"), (1, "Treated")]:
        score = episodes.loc[episodes["treated"] == treated, "displacement_prob"]
        quantiles = score.quantile([0.01, 0.10, 0.25, 0.50, 0.75, 0.90, 0.99])
        rows.append(
            {
                "arm": label,
                "n": int(len(score)),
                "mean": float(score.mean()),
                "sd": float(score.std()),
                "p01": float(quantiles.loc[0.01]),
                "p10": float(quantiles.loc[0.10]),
                "p25": float(quantiles.loc[0.25]),
                "p50": float(quantiles.loc[0.50]),
                "p75": float(quantiles.loc[0.75]),
                "p90": float(quantiles.loc[0.90]),
                "p99": float(quantiles.loc[0.99]),
                "share_at_or_above_threshold": float((score >= threshold).mean()),
            }
        )
    return pd.DataFrame(rows)


def _write_score_overlap_figure(episodes: pd.DataFrame, threshold: float) -> None:
    fig, ax = plt.subplots(figsize=(7.2, 4.1))
    bins = np.linspace(0, 1, 31)
    for treated, label, color in [
        (0, "Control", "#1f4e79"),
        (1, "Treated", "#b44c43"),
    ]:
        score = episodes.loc[episodes["treated"] == treated, "displacement_prob"]
        ax.hist(
            score,
            bins=bins,
            density=True,
            histtype="step",
            linewidth=1.8,
            color=color,
            label=label,
        )
    ax.axvline(threshold, color="0.3", linestyle="--", linewidth=1.2, label="0.5 cutoff")
    ax.set_xlabel("Predicted period-0 purchase probability")
    ax.set_ylabel("Density")
    ax.set_xlim(0, 1)
    ax.legend(frameon=False)
    ax.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "classifier_score_overlap.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    config = json.loads(CONFIG_PATH.read_text())
    threshold = float(config["model"]["decision_threshold"])
    if not 0 < threshold < 1:
        raise ValueError(f"decision_threshold must be in (0, 1); found {threshold}.")

    episodes = _load_final_episodes()
    evaluation_rows, prediction_paths = _load_exact_evaluation_rows(episodes)

    overall_rows = []
    for slice_name in SLICE_ORDER:
        sub = evaluation_rows.loc[evaluation_rows["evaluation_slice"] == slice_name]
        overall_rows.append({"evaluation_slice": slice_name, **_metrics(sub, threshold)})
    overall = pd.DataFrame(overall_rows)

    threshold_rows = []
    for slice_name in SLICE_ORDER:
        sub = evaluation_rows.loc[evaluation_rows["evaluation_slice"] == slice_name]
        for candidate in THRESHOLD_GRID:
            threshold_rows.append(
                {
                    "evaluation_slice": slice_name,
                    **_metrics(sub, candidate),
                }
            )
    threshold_results = pd.DataFrame(threshold_rows)

    duration_rows = []
    for (slice_name, duration), sub in evaluation_rows.groupby(
        ["evaluation_slice", "closure_duration_days"], sort=True
    ):
        duration_rows.append(
            {
                "evaluation_slice": slice_name,
                "closure_duration_days": int(duration),
                **_metrics(sub, threshold),
            }
        )
    by_duration = pd.DataFrame(duration_rows)

    event_rows = []
    for (slice_name, event_id), sub in evaluation_rows.groupby(
        ["evaluation_slice", "closure_event_id"], sort=True
    ):
        if sub["label"].nunique() < 2:
            continue
        event_rows.append(
            {
                "evaluation_slice": slice_name,
                "closure_event_id": event_id,
                "closure_duration_days": int(sub["closure_duration_days"].iloc[0]),
                **_metrics(sub, threshold),
            }
        )
    by_event = pd.DataFrame(event_rows)

    calibration = _calibration_bins(evaluation_rows)
    score_overlap = _score_overlap(episodes, threshold)

    overall.to_csv(OUTPUT_DIR / "classifier_performance_exact_cohort.csv", index=False)
    threshold_results.to_csv(
        OUTPUT_DIR / "classifier_threshold_grid_exact_cohort.csv", index=False
    )
    by_duration.to_csv(
        OUTPUT_DIR / "classifier_performance_by_duration.csv", index=False
    )
    by_event.to_csv(OUTPUT_DIR / "classifier_performance_by_event.csv", index=False)
    calibration.to_csv(OUTPUT_DIR / "classifier_calibration_deciles.csv", index=False)
    score_overlap.to_csv(OUTPUT_DIR / "classifier_score_overlap_summary.csv", index=False)

    _write_calibration_figure(calibration)
    _write_score_overlap_figure(episodes, threshold)

    manifest = {
        "description": "Classifier diagnostics on the exact final 18-event cohort",
        "retrained_classifier": False,
        "main_sample": str(MAIN_SAMPLE.relative_to(ROOT)),
        "main_sample_sha256": _sha256(MAIN_SAMPLE),
        "classifier_config": str(CONFIG_PATH.relative_to(ROOT)),
        "classifier_config_sha256": _sha256(CONFIG_PATH),
        "decision_threshold": threshold,
        "n_events": int(episodes["closure_event_id"].nunique()),
        "n_episodes": int(len(episodes)),
        "n_treated": int(episodes["treated"].sum()),
        "n_control": int((episodes["treated"] == 0).sum()),
        "production_durations": sorted(
            int(value) for value in episodes["closure_duration_days"].unique()
        ),
        "prediction_files": [str(path.relative_to(ROOT)) for path in prediction_paths],
        "prediction_file_sha256": {
            str(path.relative_to(ROOT)): _sha256(path) for path in prediction_paths
        },
        "excluded_sensitivity_duration_25": 25
        not in set(episodes["closure_duration_days"].astype(int)),
    }
    (OUTPUT_DIR / "classifier_diagnostics_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n"
    )

    print("Exact-cohort classifier performance")
    print(overall.to_string(index=False))
    print("\nScore overlap")
    print(score_overlap.to_string(index=False))


if __name__ == "__main__":
    main()
