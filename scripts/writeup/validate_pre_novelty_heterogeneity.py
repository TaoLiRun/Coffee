from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")
os.environ.setdefault("XDG_CACHE_HOME", "/tmp")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyfixest as pf


ROOT = Path(__file__).resolve().parents[2]
INPUT_DIR = (
    ROOT
    / "outputs"
    / "04_diagnostics_18_closures"
    / "novelty_pre_heterogeneity_median"
)
PURCHASE_SAMPLE = (
    ROOT
    / "outputs"
    / "03_main_18_closures"
    / "purchase_frequency_ddd_h4"
    / "estimation_sample.csv"
)
OUTPUT_DIR = ROOT / "outputs" / "paper" / "heterogeneity_audit"
FIG_DIR = ROOT / "writeup" / "figures"
OUTCOME = "variety_seeking"
CLUSTER = "closure_event_id"
FE = "event_fe_id + rel_t + calendar_month"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _fit(formula: str, data: pd.DataFrame):
    return pf.feols(formula, data=data, vcov={"CRV1": CLUSTER})


def _row(fit, term: str, estimand: str, specification: str) -> dict:
    tidy = fit.tidy()
    if term not in tidy.index:
        raise KeyError(f"Term {term!r} not found in {specification}: {list(tidy.index)}")
    result = tidy.loc[term]
    return {
        "specification": specification,
        "estimand": estimand,
        "term": term,
        "coef": float(result["Estimate"]),
        "se": float(result["Std. Error"]),
        "pvalue": float(result["Pr(>|t|)"]),
        "ci_low": float(result["2.5%"]),
        "ci_high": float(result["97.5%"]),
        "n": int(fit._N),
        "r2": float(fit._r2),
        "r2_within": float(fit._r2_within),
        "n_clusters": 18,
        "cluster": CLUSTER,
    }


def _prepare_columns(data: pd.DataFrame) -> pd.DataFrame:
    frame = data.copy()
    for col in ["post", "treated", "disp_binary", "novelty_pre_high", "rel_t"]:
        frame[col] = pd.to_numeric(frame[col], errors="raise").astype(int)
    frame["pre_low"] = 1 - frame["novelty_pre_high"]
    frame["pred_low"] = 1 - frame["disp_binary"]

    p = frame["post"]
    t = frame["treated"]
    d = frame["disp_binary"]
    h = frame["novelty_pre_high"]
    l = frame["pre_low"]

    # Fully saturated polynomial parameterization. The four-way coefficient is
    # the difference between the high- and low-pre-novelty DDDs.
    frame["post_X_treated"] = p * t
    frame["post_X_disp"] = p * d
    frame["post_X_treated_X_disp"] = p * t * d
    frame["post_X_pre_high"] = p * h
    frame["post_X_treated_X_pre_high"] = p * t * h
    frame["post_X_disp_X_pre_high"] = p * d * h
    frame["post_X_treated_X_disp_X_pre_high"] = p * t * d * h

    # Equivalent parameterization estimating each pre-novelty subgroup DDD
    # directly with its own covariance-aware standard error.
    frame["post_X_disp_X_pre_low"] = p * d * l
    frame["post_X_disp_X_pre_high_direct"] = p * d * h
    frame["post_X_treated_X_pre_low"] = p * t * l
    frame["post_X_treated_X_disp_X_pre_low"] = p * t * d * l
    frame["post_X_treated_X_pre_high_direct"] = p * t * h
    frame["post_X_treated_X_disp_X_pre_high_direct"] = p * t * d * h

    # Equivalent parameterization estimating all four treated-control effects
    # directly, before differencing high versus low predicted incidence.
    frame["post_X_treated_X_pred_low_X_pre_low"] = p * t * (1 - d) * l
    frame["post_X_treated_X_pred_high_X_pre_low"] = p * t * d * l
    frame["post_X_treated_X_pred_low_X_pre_high"] = p * t * (1 - d) * h
    frame["post_X_treated_X_pred_high_X_pre_high"] = p * t * d * h

    # Event-study versions of the same saturated interactions.
    frame["disp_X_pre_low"] = d * l
    frame["disp_X_pre_high"] = d * h
    frame["treated_X_pre_low"] = t * l
    frame["treated_X_disp_X_pre_low"] = t * d * l
    frame["treated_X_pre_high"] = t * h
    frame["treated_X_disp_X_pre_high"] = t * d * h
    frame["treated_X_disp"] = t * d
    frame["treated_X_pre_high_increment"] = t * h
    frame["disp_X_pre_high_increment"] = d * h
    frame["treated_X_disp_X_pre_high_increment"] = t * d * h
    return frame


def _fit_binary_models(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    legacy_formula = (
        f"{OUTCOME} ~ post_X_treated + post_X_disp + post_X_treated_X_disp + "
        "post_X_treated_X_pre_high + post_X_disp_X_pre_high + "
        f"post_X_treated_X_disp_X_pre_high | {FE}"
    )
    legacy = _fit(legacy_formula, frame)

    increment_formula = (
        f"{OUTCOME} ~ post_X_treated + post_X_disp + post_X_treated_X_disp + "
        "post_X_pre_high + post_X_treated_X_pre_high + "
        "post_X_disp_X_pre_high + post_X_treated_X_disp_X_pre_high "
        f"| {FE}"
    )
    increment = _fit(increment_formula, frame)

    direct_formula = (
        f"{OUTCOME} ~ post_X_pre_high + post_X_disp_X_pre_low + "
        "post_X_disp_X_pre_high_direct + post_X_treated_X_pre_low + "
        "post_X_treated_X_disp_X_pre_low + post_X_treated_X_pre_high_direct + "
        f"post_X_treated_X_disp_X_pre_high_direct | {FE}"
    )
    direct = _fit(direct_formula, frame)

    group_formula = (
        f"{OUTCOME} ~ post_X_pre_high + post_X_disp_X_pre_low + "
        "post_X_disp_X_pre_high_direct + "
        "post_X_treated_X_pred_low_X_pre_low + "
        "post_X_treated_X_pred_high_X_pre_low + "
        "post_X_treated_X_pred_low_X_pre_high + "
        f"post_X_treated_X_pred_high_X_pre_high | {FE}"
    )
    group = _fit(group_formula, frame)

    effects = [
        _row(
            legacy,
            "post_X_treated_X_disp",
            "legacy_low_pre_novelty_ddd_omitting_post_by_type",
            "legacy_unsaturated",
        ),
        _row(
            legacy,
            "post_X_treated_X_disp_X_pre_high",
            "legacy_high_minus_low_pre_novelty_ddd_increment",
            "legacy_unsaturated",
        ),
        _row(
            direct,
            "post_X_treated_X_pre_low",
            "low_pre_novelty_low_predicted_incidence_effect",
            "binary_saturated_group_ddd_direct",
        ),
        _row(
            group,
            "post_X_treated_X_pred_high_X_pre_low",
            "low_pre_novelty_high_predicted_incidence_effect",
            "binary_saturated_group_effects_direct",
        ),
        _row(
            direct,
            "post_X_treated_X_disp_X_pre_low",
            "low_pre_novelty_ddd",
            "binary_saturated_group_ddd_direct",
        ),
        _row(
            direct,
            "post_X_treated_X_pre_high_direct",
            "high_pre_novelty_low_predicted_incidence_effect",
            "binary_saturated_group_ddd_direct",
        ),
        _row(
            group,
            "post_X_treated_X_pred_high_X_pre_high",
            "high_pre_novelty_high_predicted_incidence_effect",
            "binary_saturated_group_effects_direct",
        ),
        _row(
            direct,
            "post_X_treated_X_disp_X_pre_high_direct",
            "high_pre_novelty_ddd",
            "binary_saturated_group_ddd_direct",
        ),
        _row(
            increment,
            "post_X_treated_X_disp_X_pre_high",
            "high_minus_low_pre_novelty_ddd_difference",
            "binary_saturated_increment",
        ),
        _row(
            increment,
            "post_X_pre_high",
            "post_by_pre_novelty_type_lower_order_term",
            "binary_saturated_increment",
        ),
    ]
    effects_df = pd.DataFrame(effects)

    direct_tidy = direct.tidy()
    group_tidy = group.tidy()
    increment_tidy = increment.tidy()
    checks = {
        "same_estimation_n": len({legacy._N, increment._N, direct._N, group._N}) == 1,
        "same_saturated_r2": np.allclose(
            [increment._r2, direct._r2, group._r2], increment._r2, atol=1e-10
        ),
        "low_ddd_parameterizations_match": np.isclose(
            direct_tidy.loc["post_X_treated_X_disp_X_pre_low", "Estimate"],
            increment_tidy.loc["post_X_treated_X_disp", "Estimate"],
            atol=1e-10,
        ),
        "high_ddd_parameterizations_match": np.isclose(
            direct_tidy.loc["post_X_treated_X_disp_X_pre_high_direct", "Estimate"],
            increment_tidy.loc["post_X_treated_X_disp", "Estimate"]
            + increment_tidy.loc[
                "post_X_treated_X_disp_X_pre_high", "Estimate"
            ],
            atol=1e-10,
        ),
        "low_group_effects_match": np.isclose(
            direct_tidy.loc["post_X_treated_X_pre_low", "Estimate"],
            group_tidy.loc[
                "post_X_treated_X_pred_low_X_pre_low", "Estimate"
            ],
            atol=1e-10,
        ),
        "high_group_effects_match": np.isclose(
            direct_tidy.loc["post_X_treated_X_pre_high_direct", "Estimate"],
            group_tidy.loc[
                "post_X_treated_X_pred_low_X_pre_high", "Estimate"
            ],
            atol=1e-10,
        ),
    }
    if not all(checks.values()):
        raise AssertionError(f"Binary parameterization checks failed: {checks}")

    fits = pd.DataFrame(
        [
            {
                "specification": name,
                "formula": formula,
                "n": int(fit._N),
                "r2": float(fit._r2),
                "r2_within": float(fit._r2_within),
                "cluster": CLUSTER,
                "n_clusters": 18,
            }
            for name, formula, fit in [
                ("legacy_unsaturated", legacy_formula, legacy),
                ("binary_saturated_increment", increment_formula, increment),
                ("binary_saturated_group_ddd_direct", direct_formula, direct),
                ("binary_saturated_group_effects_direct", group_formula, group),
            ]
        ]
    )
    fitted = {"legacy": legacy, "increment": increment, "direct": direct, "group": group}
    return effects_df, fits, {"checks": checks, "fits": fitted}


def _fit_continuous_models(frame: pd.DataFrame) -> pd.DataFrame:
    episodes = frame.drop_duplicates("event_fe_id")
    centers = {
        "episode_mean": float(episodes["novelty_pre_mean"].mean()),
        "p25": float(episodes["novelty_pre_mean"].quantile(0.25)),
        "median": float(episodes["novelty_pre_mean"].median()),
        "p75": float(episodes["novelty_pre_mean"].quantile(0.75)),
    }
    rows: list[dict] = []
    for center_name, center in centers.items():
        work = frame.copy()
        work["pre_novelty_centered"] = work["novelty_pre_mean"] - center
        p = work["post"]
        t = work["treated"]
        d = work["disp_binary"]
        z = work["pre_novelty_centered"]
        work["post_X_pre_novelty"] = p * z
        work["post_X_disp_cont"] = p * d
        work["post_X_disp_X_pre_novelty"] = p * d * z
        work["post_X_treated_cont"] = p * t
        work["post_X_treated_X_disp_cont"] = p * t * d
        work["post_X_treated_X_pre_novelty"] = p * t * z
        work["post_X_treated_X_disp_X_pre_novelty"] = p * t * d * z
        formula = (
            f"{OUTCOME} ~ post_X_pre_novelty + post_X_disp_cont + "
            "post_X_disp_X_pre_novelty + post_X_treated_cont + "
            "post_X_treated_X_disp_cont + post_X_treated_X_pre_novelty + "
            f"post_X_treated_X_disp_X_pre_novelty | {FE}"
        )
        fit = _fit(formula, work)
        level = _row(
            fit,
            "post_X_treated_X_disp_cont",
            "ddd_at_pre_novelty_value",
            f"continuous_saturated_centered_{center_name}",
        )
        level["pre_novelty_value"] = center
        level["center_name"] = center_name
        rows.append(level)
        slope = _row(
            fit,
            "post_X_treated_X_disp_X_pre_novelty",
            "ddd_slope_per_unit_pre_novelty",
            f"continuous_saturated_centered_{center_name}",
        )
        slope["pre_novelty_value"] = center
        slope["center_name"] = center_name
        rows.append(slope)

    result = pd.DataFrame(rows)
    slopes = result[result["estimand"] == "ddd_slope_per_unit_pre_novelty"]["coef"]
    if not np.allclose(slopes, slopes.iloc[0], atol=1e-9):
        raise AssertionError("Continuous heterogeneity slope changes across recenterings.")
    return result


def _extract_rel_t(term: str) -> int | None:
    bracket = re.search(r"\[(-?\d+)\]", term)
    if bracket:
        return int(bracket.group(1))
    colon = re.search(r"rel_t::(-?\d+):", term)
    if colon:
        return int(colon.group(1))
    return None


def _event_rows(fit, suffix: str, subgroup: str, specification: str) -> pd.DataFrame:
    tidy = fit.tidy()
    rows = []
    for term in tidy.index:
        if not str(term).endswith(f":{suffix}"):
            continue
        rel_t = _extract_rel_t(str(term))
        if rel_t is None:
            continue
        result = tidy.loc[term]
        rows.append(
            {
                "specification": specification,
                "subgroup": subgroup,
                "rel_t": rel_t,
                "term": str(term),
                "coef": float(result["Estimate"]),
                "se": float(result["Std. Error"]),
                "pvalue": float(result["Pr(>|t|)"]),
                "ci_low": float(result["2.5%"]),
                "ci_high": float(result["97.5%"]),
                "n": int(fit._N),
                "n_clusters": 18,
            }
        )
    return pd.DataFrame(rows)


def _joint_pretrend(fit, suffix: str, test: str) -> dict:
    tidy = fit.tidy()
    terms = [
        str(term)
        for term in tidy.index
        if str(term).endswith(f":{suffix}") and _extract_rel_t(str(term)) in {-4, -3, -2}
    ]
    if len(terms) != 3:
        raise ValueError(f"Expected three pretrend terms for {suffix}; found {terms}")
    names = [str(term) for term in tidy.index]
    index = {name: position for position, name in enumerate(names)}
    restrictions = np.zeros((len(terms), len(names)))
    for row_index, term in enumerate(terms):
        restrictions[row_index, index[term]] = 1.0
    result = fit.wald_test(R=restrictions)
    return {
        "test": test,
        "n_restrictions": 3,
        "statistic": float(result.iloc[0]),
        "pvalue": float(result.iloc[1]),
        "n": int(fit._N),
        "n_clusters": 18,
        "cluster": CLUSTER,
    }


def _fit_event_study(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    direct_formula = (
        f"{OUTCOME} ~ i(rel_t, novelty_pre_high, ref=-1) + "
        "i(rel_t, disp_X_pre_low, ref=-1) + "
        "i(rel_t, disp_X_pre_high, ref=-1) + "
        "i(rel_t, treated_X_pre_low, ref=-1) + "
        "i(rel_t, treated_X_disp_X_pre_low, ref=-1) + "
        "i(rel_t, treated_X_pre_high, ref=-1) + "
        f"i(rel_t, treated_X_disp_X_pre_high, ref=-1) | {FE}"
    )
    direct = _fit(direct_formula, frame)
    low = _event_rows(
        direct,
        "treated_X_disp_X_pre_low",
        "low_pre_novelty",
        "event_saturated_group_ddd_direct",
    )
    high = _event_rows(
        direct,
        "treated_X_disp_X_pre_high",
        "high_pre_novelty",
        "event_saturated_group_ddd_direct",
    )

    increment_formula = (
        f"{OUTCOME} ~ i(rel_t, treated, ref=-1) + "
        "i(rel_t, treated_X_disp, ref=-1) + "
        "i(rel_t, disp_binary, ref=-1) + "
        "i(rel_t, novelty_pre_high, ref=-1) + "
        "i(rel_t, treated_X_pre_high_increment, ref=-1) + "
        "i(rel_t, disp_X_pre_high_increment, ref=-1) + "
        f"i(rel_t, treated_X_disp_X_pre_high_increment, ref=-1) | {FE}"
    )
    increment = _fit(increment_formula, frame)
    difference = _event_rows(
        increment,
        "treated_X_disp_X_pre_high_increment",
        "high_minus_low_pre_novelty",
        "event_saturated_increment",
    )

    event_rows = pd.concat([low, high, difference], ignore_index=True)
    tests = pd.DataFrame(
        [
            _joint_pretrend(
                direct,
                "treated_X_disp_X_pre_low",
                "low_pre_novelty_ddd_pretrend_joint_zero",
            ),
            _joint_pretrend(
                direct,
                "treated_X_disp_X_pre_high",
                "high_pre_novelty_ddd_pretrend_joint_zero",
            ),
            _joint_pretrend(
                increment,
                "treated_X_disp_X_pre_high_increment",
                "difference_in_ddd_pretrend_joint_zero",
            ),
        ]
    )
    return event_rows, tests


def _leave_one_event_out(frame: pd.DataFrame) -> pd.DataFrame:
    rows = []
    formula = (
        f"{OUTCOME} ~ post_X_pre_high + post_X_disp_X_pre_low + "
        "post_X_disp_X_pre_high_direct + post_X_treated_X_pre_low + "
        "post_X_treated_X_disp_X_pre_low + post_X_treated_X_pre_high_direct + "
        f"post_X_treated_X_disp_X_pre_high_direct | {FE}"
    )
    events = sorted(frame[CLUSTER].dropna().unique().tolist(), key=str)
    for omitted in events:
        subset = frame.loc[frame[CLUSTER] != omitted]
        fit = _fit(formula, subset)
        low = _row(
            fit,
            "post_X_treated_X_disp_X_pre_low",
            "low_pre_novelty_ddd",
            "leave_one_event_out",
        )
        high = _row(
            fit,
            "post_X_treated_X_disp_X_pre_high_direct",
            "high_pre_novelty_ddd",
            "leave_one_event_out",
        )
        for result in [low, high]:
            result["omitted_event"] = omitted
            result["remaining_clusters"] = 17
            result["n_clusters"] = 17
            rows.append(result)
    return pd.DataFrame(rows)


def _support_summary(frame: pd.DataFrame) -> pd.DataFrame:
    episode_cols = [
        "event_fe_id",
        CLUSTER,
        "novelty_pre_high",
        "disp_binary",
        "treated",
        "novelty_pre_mean",
    ]
    episodes = frame[episode_cols].drop_duplicates("event_fe_id")
    purchase = pd.read_csv(PURCHASE_SAMPLE)
    purchase = purchase.loc[purchase["event_fe_id"].isin(episodes["event_fe_id"])].copy()
    purchase = purchase.merge(
        episodes[["event_fe_id", "novelty_pre_high", "disp_binary", "treated"]],
        on="event_fe_id",
        how="inner",
        suffixes=("_purchase", ""),
        validate="many_to_one",
    )
    purchase["purchased"] = (purchase["n_purchases"] > 0).astype(float)
    group_cols = ["novelty_pre_high", "disp_binary", "treated"]
    episode_summary = (
        episodes.groupby(group_cols, sort=True)
        .agg(
            n_episodes=("event_fe_id", "size"),
            n_events=(CLUSTER, "nunique"),
            mean_pre_novelty=("novelty_pre_mean", "mean"),
            median_pre_novelty=("novelty_pre_mean", "median"),
        )
        .reset_index()
    )
    purchase_summary = (
        purchase.groupby(group_cols, sort=True)
        .apply(
            lambda block: pd.Series(
                {
                    "pre_purchase_frequency": block.loc[
                        block["rel_t"] < 0, "n_purchases"
                    ].mean(),
                    "post_purchase_frequency": block.loc[
                        block["rel_t"] > 0, "n_purchases"
                    ].mean(),
                    "pre_purchase_probability": block.loc[
                        block["rel_t"] < 0, "purchased"
                    ].mean(),
                    "post_purchase_probability": block.loc[
                        block["rel_t"] > 0, "purchased"
                    ].mean(),
                }
            )
        )
        .reset_index()
    )
    outcome_summary = (
        frame.groupby(group_cols, sort=True)
        .apply(
            lambda block: pd.Series(
                {
                    "panel_rows": len(block),
                    "novelty_rows": block[OUTCOME].notna().sum(),
                    "novelty_observed_share": block[OUTCOME].notna().mean(),
                    "pre_novelty_outcome_mean": block.loc[
                        (block["rel_t"] < 0) & block[OUTCOME].notna(), OUTCOME
                    ].mean(),
                    "post_novelty_outcome_mean": block.loc[
                        (block["rel_t"] > 0) & block[OUTCOME].notna(), OUTCOME
                    ].mean(),
                }
            )
        )
        .reset_index()
    )
    return episode_summary.merge(purchase_summary, on=group_cols).merge(
        outcome_summary, on=group_cols
    )


def _plot_effects(binary: pd.DataFrame, continuous: pd.DataFrame) -> None:
    binary_rows = binary.loc[
        binary["estimand"].isin(["low_pre_novelty_ddd", "high_pre_novelty_ddd"])
    ].copy()
    binary_rows["label"] = binary_rows["estimand"].map(
        {
            "low_pre_novelty_ddd": "Low pre-novelty",
            "high_pre_novelty_ddd": "High pre-novelty",
        }
    )
    continuous_rows = continuous.loc[
        (continuous["estimand"] == "ddd_at_pre_novelty_value")
        & continuous["center_name"].isin(["p25", "median", "p75"])
    ].copy()
    continuous_rows["label"] = continuous_rows.apply(
        lambda row: f"{row['center_name']} ({row['pre_novelty_value']:.2f})", axis=1
    )

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2), sharey=True)
    for ax, data, title in [
        (axes[0], binary_rows, "Median split"),
        (axes[1], continuous_rows, "Continuous pre-novelty"),
    ]:
        positions = np.arange(len(data))
        ax.axhline(0, color="0.4", linewidth=1)
        ax.errorbar(
            positions,
            100 * data["coef"],
            yerr=[
                100 * (data["coef"] - data["ci_low"]),
                100 * (data["ci_high"] - data["coef"]),
            ],
            fmt="o",
            color="#1f4e79",
            capsize=4,
            markersize=6,
        )
        ax.set_xticks(positions)
        ax.set_xticklabels(data["label"].tolist())
        ax.set_title(title)
        ax.grid(axis="y", alpha=0.25)
    axes[0].set_ylabel("High-minus-low DDD (percentage points)")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "heterogeneity_corrected_effects.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def _plot_leave_one_out(leave_out: pd.DataFrame, binary: pd.DataFrame) -> None:
    baseline = binary.set_index("estimand")["coef"].to_dict()
    labels = {
        "low_pre_novelty_ddd": "Low pre-novelty",
        "high_pre_novelty_ddd": "High pre-novelty",
    }
    fig, axes = plt.subplots(2, 1, figsize=(9.2, 6.5), sharex=True)
    events = sorted(leave_out["omitted_event"].unique().tolist(), key=str)
    positions = np.arange(len(events))
    for ax, estimand in zip(axes, labels):
        sub = leave_out.loc[leave_out["estimand"] == estimand].set_index(
            "omitted_event"
        ).loc[events]
        ax.axhline(0, color="0.45", linewidth=1)
        ax.axhline(
            100 * baseline[estimand], color="#1f4e79", linestyle="--", linewidth=1.5
        )
        ax.plot(positions, 100 * sub["coef"], "o", color="#d62728", markersize=4.5)
        ax.set_ylabel("DDD (pp)")
        ax.set_title(labels[estimand])
        ax.grid(axis="y", alpha=0.25)
    axes[-1].set_xticks(positions)
    axes[-1].set_xticklabels([str(event) for event in events], rotation=60, ha="right")
    axes[-1].set_xlabel("Omitted closure event")
    fig.tight_layout()
    fig.savefig(
        FIG_DIR / "heterogeneity_leave_one_event_out.png", dpi=300, bbox_inches="tight"
    )
    plt.close(fig)


def _multiple_testing_adjustment(
    binary: pd.DataFrame, continuous: pd.DataFrame
) -> pd.DataFrame:
    """Holm-adjust the two alternative tests of differential heterogeneity."""
    binary_test = binary.loc[
        binary["estimand"] == "high_minus_low_pre_novelty_ddd_difference"
    ].iloc[0]
    continuous_test = continuous.loc[
        (continuous["estimand"] == "ddd_slope_per_unit_pre_novelty")
        & (continuous["center_name"] == "episode_mean")
    ].iloc[0]
    tests = pd.DataFrame(
        [
            {
                "test": "median_split_high_minus_low_pre_novelty_ddd",
                "raw_pvalue": float(binary_test["pvalue"]),
            },
            {
                "test": "continuous_pre_novelty_ddd_slope",
                "raw_pvalue": float(continuous_test["pvalue"]),
            },
        ]
    )
    ordered = tests.sort_values("raw_pvalue").copy()
    m = len(ordered)
    running_max = 0.0
    adjusted: list[float] = []
    for rank, pvalue in enumerate(ordered["raw_pvalue"]):
        running_max = max(running_max, min(1.0, (m - rank) * float(pvalue)))
        adjusted.append(running_max)
    ordered["holm_adjusted_pvalue"] = adjusted
    return tests.merge(
        ordered[["test", "holm_adjusted_pvalue"]], on="test", validate="one_to_one"
    )


def _write_report(
    binary: pd.DataFrame,
    continuous: pd.DataFrame,
    pretrends: pd.DataFrame,
    leave_out: pd.DataFrame,
    support: pd.DataFrame,
    multiple_tests: pd.DataFrame,
    checks: dict,
) -> None:
    effects = binary.set_index("estimand")
    low = effects.loc["low_pre_novelty_ddd"]
    high = effects.loc["high_pre_novelty_ddd"]
    difference = effects.loc["high_minus_low_pre_novelty_ddd_difference"]
    lower_order = effects.loc["post_by_pre_novelty_type_lower_order_term"]
    legacy_low = effects.loc["legacy_low_pre_novelty_ddd_omitting_post_by_type"]
    legacy_inc = effects.loc["legacy_high_minus_low_pre_novelty_ddd_increment"]
    cont_slope = continuous.loc[
        (continuous["estimand"] == "ddd_slope_per_unit_pre_novelty")
        & (continuous["center_name"] == "episode_mean")
    ].iloc[0]
    low_loo = leave_out.loc[leave_out["estimand"] == "low_pre_novelty_ddd", "coef"]
    high_loo = leave_out.loc[leave_out["estimand"] == "high_pre_novelty_ddd", "coef"]
    lines = [
        "# Corrected pre-novelty heterogeneity audit",
        "",
        "## Scope",
        "",
        "This diagnostic uses the saved final 18-event heterogeneity sample. It does not rebuild the sample, retrain the classifier, or alter the main DDD estimates. All reported standard errors are clustered by closure event.",
        "",
        "## Specification correction",
        "",
        "The legacy model omitted `Post × pre-novelty type`. The corrected binary model includes every post interaction implied by `Post × Treated × predicted incidence × pre-novelty type`. Algebraically equivalent parameterizations were fitted to estimate subgroup DDDs and all four treated-control effects directly.",
        "",
        f"- Legacy low-pre-novelty DDD: {legacy_low.coef:.4f} (SE {legacy_low.se:.4f}).",
        f"- Legacy high-minus-low-pre increment: {legacy_inc.coef:.4f} (SE {legacy_inc.se:.4f}).",
        f"- Corrected omitted lower-order `Post × type` coefficient: {lower_order.coef:.4f} (SE {lower_order.se:.4f}, p={lower_order.pvalue:.3f}).",
        f"- Corrected low-pre-novelty DDD: {low.coef:.4f} (SE {low.se:.4f}, 95% CI [{low.ci_low:.4f}, {low.ci_high:.4f}], p={low.pvalue:.3f}).",
        f"- Corrected high-pre-novelty DDD: {high.coef:.4f} (SE {high.se:.4f}, 95% CI [{high.ci_low:.4f}, {high.ci_high:.4f}], p={high.pvalue:.3f}).",
        f"- Difference between subgroup DDDs: {difference.coef:.4f} (SE {difference.se:.4f}, 95% CI [{difference.ci_low:.4f}, {difference.ci_high:.4f}], p={difference.pvalue:.3f}).",
        "",
        "## Continuous interaction",
        "",
        f"The DDD slope with respect to the episode-level pre-period novelty mean is {cont_slope.coef:.4f} per unit (SE {cont_slope.se:.4f}, p={cont_slope.pvalue:.3f}), or {0.1 * cont_slope.coef:.4f} per 0.1 increase.",
        f"Treating the median-split difference and continuous slope as a family of two alternative heterogeneity tests, both Holm-adjusted p-values equal {multiple_tests['holm_adjusted_pvalue'].min():.3f}.",
        "",
        "## Event sensitivity",
        "",
        f"- Low-pre-novelty leave-one-event-out range: [{low_loo.min():.4f}, {low_loo.max():.4f}].",
        f"- High-pre-novelty leave-one-event-out range: [{high_loo.min():.4f}, {high_loo.max():.4f}].",
        f"- Low-pre-novelty sign agreement: {(np.sign(low_loo) == np.sign(low.coef)).mean():.1%}.",
        f"- High-pre-novelty sign agreement: {(np.sign(high_loo) == np.sign(high.coef)).mean():.1%}.",
        "",
        "## Validation checks",
        "",
        *[f"- {name}: {value}" for name, value in checks.items()],
        "",
        "## Interpretation limit",
        "",
        "Pre-novelty type is constructed from the same outcome in the four pre-periods and is available only for episodes with a pre-period purchase. Saturation fixes the omitted-interaction error but does not remove regression-to-the-mean or selected-type concerns. The heterogeneity remains exploratory unless it survives a type measure constructed in a separate initialization window.",
        "",
        "## Output inventory",
        "",
        "- `binary_saturated_effects.csv`",
        "- `binary_saturated_fits.csv`",
        "- `continuous_saturated_effects.csv`",
        "- `heterogeneity_event_study.csv`",
        "- `heterogeneity_pretrend_tests.csv`",
        "- `leave_one_event_out.csv`",
        "- `multiple_testing_adjustment.csv`",
        "- `subgroup_support.csv`",
        "- `heterogeneity_manifest.json`",
    ]
    (OUTPUT_DIR / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    input_path = INPUT_DIR / "estimation_sample.csv"
    raw = pd.read_csv(input_path)
    required = {
        OUTCOME,
        "post",
        "treated",
        "disp_binary",
        "novelty_pre_high",
        "novelty_pre_mean",
        "event_fe_id",
        "rel_t",
        "calendar_month",
        CLUSTER,
    }
    missing = sorted(required.difference(raw.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    if len(raw) != 207_152 or raw[CLUSTER].nunique() != 18:
        raise ValueError(
            f"Unexpected cohort: rows={len(raw):,}, events={raw[CLUSTER].nunique()}"
        )
    if raw["event_fe_id"].nunique() != 25_894:
        raise ValueError("Unexpected episode count in heterogeneity cohort.")
    if raw[OUTCOME].notna().sum() != 100_012:
        raise ValueError("Unexpected number of nonmissing novelty rows.")

    frame = _prepare_columns(raw)
    binary, fits, binary_payload = _fit_binary_models(frame)
    continuous = _fit_continuous_models(frame)
    event_rows, pretrends = _fit_event_study(frame)
    leave_out = _leave_one_event_out(frame)
    support = _support_summary(frame)
    multiple_tests = _multiple_testing_adjustment(binary, continuous)

    binary.to_csv(OUTPUT_DIR / "binary_saturated_effects.csv", index=False)
    fits.to_csv(OUTPUT_DIR / "binary_saturated_fits.csv", index=False)
    continuous.to_csv(OUTPUT_DIR / "continuous_saturated_effects.csv", index=False)
    event_rows.to_csv(OUTPUT_DIR / "heterogeneity_event_study.csv", index=False)
    pretrends.to_csv(OUTPUT_DIR / "heterogeneity_pretrend_tests.csv", index=False)
    leave_out.to_csv(OUTPUT_DIR / "leave_one_event_out.csv", index=False)
    multiple_tests.to_csv(
        OUTPUT_DIR / "multiple_testing_adjustment.csv", index=False
    )
    support.to_csv(OUTPUT_DIR / "subgroup_support.csv", index=False)

    _plot_effects(binary, continuous)
    _plot_leave_one_out(leave_out, binary)
    checks = {name: bool(value) for name, value in binary_payload["checks"].items()}
    _write_report(
        binary,
        continuous,
        pretrends,
        leave_out,
        support,
        multiple_tests,
        checks,
    )

    manifest = {
        "analysis": "corrected_pre_novelty_heterogeneity",
        "input": str(input_path.relative_to(ROOT)),
        "input_sha256": _sha256(input_path),
        "purchase_sample": str(PURCHASE_SAMPLE.relative_to(ROOT)),
        "purchase_sample_sha256": _sha256(PURCHASE_SAMPLE),
        "script": str(Path(__file__).resolve().relative_to(ROOT)),
        "script_sha256": _sha256(Path(__file__).resolve()),
        "sample_checks": {
            "rows": len(raw),
            "nonmissing_novelty_rows_before_fixed_effect_singletons": int(
                raw[OUTCOME].notna().sum()
            ),
            "episodes": int(raw["event_fe_id"].nunique()),
            "closure_events": int(raw[CLUSTER].nunique()),
            "relative_periods": sorted(raw["rel_t"].unique().tolist()),
            "median_split_threshold": float(raw["novelty_pre_threshold_low"].iloc[0]),
        },
        "parameterization_checks": checks,
        "inference": {"vcov": "CRV1", "cluster": CLUSTER, "clusters": 18},
        "notes": [
            "No sample reconstruction.",
            "No classifier retraining.",
            "No main DDD estimates changed.",
            "Pre-novelty type remains outcome-derived and exploratory.",
        ],
    }
    (OUTPUT_DIR / "heterogeneity_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print((OUTPUT_DIR / "README.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
