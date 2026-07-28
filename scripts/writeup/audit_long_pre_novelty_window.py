from __future__ import annotations

from pathlib import Path
import re

import numpy as np
import pandas as pd
import pyfixest as pf


ROOT = Path(__file__).resolve().parents[2]
SAMPLE_PATH = (
    ROOT
    / "outputs"
    / "03_main_18_closures"
    / "novelty_member_first_ddd_h4"
    / "estimation_sample.csv"
)
OUTPUT_DIR = ROOT / "outputs" / "paper" / "heterogeneity_audit" / "long_pre_window"
TRAIT_PATH = OUTPUT_DIR / "episode_long_pre_novelty_traits.csv"
COMPONENT_PATH = OUTPUT_DIR / "episode_window_novelty_components.csv"
RESULT_PATH = OUTPUT_DIR / "long_pre_window_heterogeneity_results.csv"
OUTCOME = "variety_seeking"
FE = "event_fe_id + rel_t + calendar_month"
CLUSTER = "closure_event_id"
BEST_VARIANT = "separate_4"
BEST_MINIMUM_ORDERS = 15


def _coef(fit, term: str) -> dict:
    row = fit.tidy().loc[term]
    return {
        "coef": float(row["Estimate"]),
        "se": float(row["Std. Error"]),
        "pvalue": float(row["Pr(>|t|)"]),
        "ci_low": float(row["2.5%"]),
        "ci_high": float(row["97.5%"]),
        "n": int(fit._N),
        "r2": float(fit._r2),
        "r2_within": float(fit._r2_within),
    }


def _prepare(
    sample: pd.DataFrame,
    traits: pd.DataFrame,
    *,
    variant: str,
    minimum_orders: int,
    threshold: float,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    novelty = f"{variant}_novelty_mean"
    orders = f"{variant}_orders"
    episode = traits.loc[
        traits[novelty].notna() & (traits[orders] >= minimum_orders),
        ["event_fe_id", novelty, orders],
    ].copy()
    episode = episode.rename(columns={novelty: "type_value", orders: "type_orders"})
    episode["type_high"] = (episode["type_value"] > threshold).astype(int)
    frame = sample.merge(episode, on="event_fe_id", how="inner", validate="many_to_one")
    for column in ["rel_t", "post", "treated", "disp_binary", "type_high"]:
        frame[column] = pd.to_numeric(frame[column], errors="raise").astype(int)
    p = frame["post"]
    t = frame["treated"]
    d = frame["disp_binary"]
    h = frame["type_high"]
    low = 1 - h
    frame["post_X_treated"] = p * t
    frame["post_X_disp"] = p * d
    frame["post_X_treated_X_disp"] = p * t * d
    frame["post_X_type_high"] = p * h
    frame["post_X_treated_X_type_high"] = p * t * h
    frame["post_X_disp_X_type_high"] = p * d * h
    frame["post_X_treated_X_disp_X_type_high"] = p * t * d * h
    frame["disp_X_type_low"] = d * low
    frame["disp_X_type_high"] = d * h
    frame["treated_X_type_low"] = t * low
    frame["treated_X_disp_X_type_low"] = t * d * low
    frame["treated_X_type_high"] = t * h
    frame["treated_X_disp_X_type_high"] = t * d * h
    frame["treated_X_disp"] = t * d
    frame["treated_X_type_high_increment"] = t * h
    frame["disp_X_type_high_increment"] = d * h
    frame["treated_X_disp_X_type_high_increment"] = t * d * h
    center = float(episode["type_value"].mean())
    z = frame["type_value"] - center
    frame["post_X_type_cont"] = p * z
    frame["post_X_treated_X_type_cont"] = p * t * z
    frame["post_X_disp_X_type_cont"] = p * d * z
    frame["post_X_treated_X_disp_X_type_cont"] = p * t * d * z
    return frame, episode


def _binary_formula() -> str:
    return (
        f"{OUTCOME} ~ post_X_treated + post_X_disp + post_X_treated_X_disp + "
        "post_X_type_high + post_X_treated_X_type_high + "
        "post_X_disp_X_type_high + post_X_treated_X_disp_X_type_high "
        f"| {FE}"
    )


def _continuous_formula() -> str:
    return (
        f"{OUTCOME} ~ post_X_treated + post_X_disp + post_X_treated_X_disp + "
        "post_X_type_cont + post_X_treated_X_type_cont + "
        "post_X_disp_X_type_cont + post_X_treated_X_disp_X_type_cont "
        f"| {FE}"
    )


def _history_average(
    components: pd.DataFrame, periods: range, label: str
) -> pd.DataFrame:
    selected = components.loc[components["rel_t_history"].isin(periods)]
    return (
        selected.groupby("event_fe_id", sort=False)["window_novelty"]
        .mean()
        .rename(label)
        .reset_index()
    )


def _split_history_reliability(
    traits: pd.DataFrame, components: pd.DataFrame
) -> pd.DataFrame:
    definitions = [
        ("adjacent_4_week_blocks", range(-8, -4), range(-4, 0)),
        ("separate_8_split_into_4_week_blocks", range(-12, -8), range(-8, -4)),
        ("overlap_12_split_into_6_week_blocks", range(-12, -6), range(-6, 0)),
    ]
    rows: list[dict] = []
    order_lookup = traits.set_index("event_fe_id")
    for name, early_periods, late_periods in definitions:
        early = _history_average(components, early_periods, "early")
        late = _history_average(components, late_periods, "late")
        paired = early.merge(late, on="event_fe_id", validate="one_to_one")
        early_first = min(early_periods)
        late_last = max(late_periods)
        span_name = {
            (-8, -1): "overlap_8",
            (-12, -5): "separate_8",
            (-12, -1): "overlap_12",
        }[(early_first, late_last)]
        paired = paired.merge(
            order_lookup[[f"{span_name}_orders"]],
            left_on="event_fe_id",
            right_index=True,
            validate="one_to_one",
        )
        for minimum_orders in [1, 3, 5, 10]:
            subset = paired.loc[paired[f"{span_name}_orders"] >= minimum_orders]
            rows.append(
                {
                    "comparison": name,
                    "early_periods": f"{min(early_periods)} to {max(early_periods)}",
                    "late_periods": f"{min(late_periods)} to {max(late_periods)}",
                    "minimum_orders_across_full_span": minimum_orders,
                    "paired_episodes": len(subset),
                    "pearson_correlation": subset["early"].corr(subset["late"]),
                    "spearman_correlation": subset["early"].rank().corr(
                        subset["late"].rank()
                    ),
                    "mean_early_novelty": subset["early"].mean(),
                    "mean_late_novelty": subset["late"].mean(),
                }
            )
    return pd.DataFrame(rows)


def _trait_diagnostics(traits: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict] = []
    for variant in ["overlap_4", "overlap_8", "overlap_12", "separate_4", "separate_8"]:
        novelty = f"{variant}_novelty_mean"
        orders = f"{variant}_orders"
        eligible = traits.loc[traits[novelty].notna(), [novelty, orders]].copy()
        threshold = float(eligible[novelty].median())
        eligible["type_high"] = (eligible[novelty] > threshold).astype(int)
        rows.append(
            {
                "variant": variant,
                "eligible_episodes": len(eligible),
                "median_threshold": threshold,
                "pearson_novelty_order_correlation": eligible[novelty].corr(
                    eligible[orders]
                ),
                "spearman_novelty_order_correlation": eligible[novelty].rank().corr(
                    eligible[orders].rank()
                ),
                "mean_orders_low_type": eligible.loc[
                    eligible["type_high"] == 0, orders
                ].mean(),
                "mean_orders_high_type": eligible.loc[
                    eligible["type_high"] == 1, orders
                ].mean(),
                "share_high_type": eligible["type_high"].mean(),
            }
        )
    return pd.DataFrame(rows)


def _threshold_sensitivity(
    sample: pd.DataFrame, traits: pd.DataFrame
) -> pd.DataFrame:
    novelty = f"{BEST_VARIANT}_novelty_mean"
    orders = f"{BEST_VARIANT}_orders"
    eligible = traits.loc[traits[novelty].notna() & (traits[orders] >= BEST_MINIMUM_ORDERS)]
    all_eligible = traits.loc[traits[novelty].notna(), novelty]
    thresholds = {
        "full_eligible_median": float(all_eligible.median()),
        "screened_q33": float(eligible[novelty].quantile(1 / 3)),
        "screened_median": float(eligible[novelty].median()),
        "screened_q67": float(eligible[novelty].quantile(2 / 3)),
    }
    rows: list[dict] = []
    for name, threshold in thresholds.items():
        frame, episode = _prepare(
            sample,
            traits,
            variant=BEST_VARIANT,
            minimum_orders=BEST_MINIMUM_ORDERS,
            threshold=threshold,
        )
        fit = pf.feols(_binary_formula(), data=frame, vcov={"CRV1": CLUSTER})
        rows.append(
            {
                "threshold_rule": name,
                "threshold": threshold,
                "low_type_episodes": int((episode["type_high"] == 0).sum()),
                "high_type_episodes": int((episode["type_high"] == 1).sum()),
                **_coef(fit, "post_X_treated_X_disp_X_type_high"),
            }
        )
    return pd.DataFrame(rows)


def _leave_one_event_out(
    sample: pd.DataFrame, traits: pd.DataFrame, threshold: float
) -> pd.DataFrame:
    frame, _ = _prepare(
        sample,
        traits,
        variant=BEST_VARIANT,
        minimum_orders=BEST_MINIMUM_ORDERS,
        threshold=threshold,
    )
    rows: list[dict] = []
    for omitted in sorted(frame[CLUSTER].unique(), key=str):
        subset = frame.loc[frame[CLUSTER] != omitted]
        binary = pf.feols(_binary_formula(), data=subset, vcov={"CRV1": CLUSTER})
        continuous = pf.feols(
            _continuous_formula(), data=subset, vcov={"CRV1": CLUSTER}
        )
        for model, fit, term in [
            (
                "binary",
                binary,
                "post_X_treated_X_disp_X_type_high",
            ),
            (
                "continuous",
                continuous,
                "post_X_treated_X_disp_X_type_cont",
            ),
        ]:
            rows.append(
                {
                    "omitted_event": omitted,
                    "remaining_clusters": 17,
                    "model": model,
                    **_coef(fit, term),
                }
            )
    return pd.DataFrame(rows)


def _extract_rel_t(term: str) -> int | None:
    match = re.search(r"\[(-?\d+)\]", term)
    if match:
        return int(match.group(1))
    match = re.search(r"rel_t::(-?\d+):", term)
    return int(match.group(1)) if match else None


def _event_rows(fit, suffix: str, estimand: str) -> pd.DataFrame:
    rows: list[dict] = []
    for term, result in fit.tidy().iterrows():
        if not str(term).endswith(f":{suffix}"):
            continue
        rel_t = _extract_rel_t(str(term))
        if rel_t is None:
            continue
        rows.append(
            {
                "estimand": estimand,
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
    terms = [
        str(term)
        for term in fit.tidy().index
        if str(term).endswith(f":{suffix}") and _extract_rel_t(str(term)) in {-4, -3, -2}
    ]
    if len(terms) != 3:
        raise ValueError(f"Expected three pretrend terms for {suffix}; found {terms}")
    names = [str(term) for term in fit.tidy().index]
    position = {name: index for index, name in enumerate(names)}
    restrictions = np.zeros((3, len(names)))
    for row, term in enumerate(terms):
        restrictions[row, position[term]] = 1
    result = fit.wald_test(R=restrictions)
    return {
        "test": test,
        "n_restrictions": 3,
        "statistic": float(result.iloc[0]),
        "pvalue": float(result.iloc[1]),
        "n": int(fit._N),
        "n_clusters": 18,
    }


def _event_study(
    sample: pd.DataFrame, traits: pd.DataFrame, threshold: float
) -> tuple[pd.DataFrame, pd.DataFrame]:
    frame, _ = _prepare(
        sample,
        traits,
        variant=BEST_VARIANT,
        minimum_orders=BEST_MINIMUM_ORDERS,
        threshold=threshold,
    )
    direct_formula = (
        f"{OUTCOME} ~ i(rel_t, type_high, ref=-1) + "
        "i(rel_t, disp_X_type_low, ref=-1) + "
        "i(rel_t, disp_X_type_high, ref=-1) + "
        "i(rel_t, treated_X_type_low, ref=-1) + "
        "i(rel_t, treated_X_disp_X_type_low, ref=-1) + "
        "i(rel_t, treated_X_type_high, ref=-1) + "
        f"i(rel_t, treated_X_disp_X_type_high, ref=-1) | {FE}"
    )
    increment_formula = (
        f"{OUTCOME} ~ i(rel_t, treated, ref=-1) + "
        "i(rel_t, treated_X_disp, ref=-1) + "
        "i(rel_t, disp_binary, ref=-1) + "
        "i(rel_t, type_high, ref=-1) + "
        "i(rel_t, treated_X_type_high_increment, ref=-1) + "
        "i(rel_t, disp_X_type_high_increment, ref=-1) + "
        f"i(rel_t, treated_X_disp_X_type_high_increment, ref=-1) | {FE}"
    )
    direct = pf.feols(direct_formula, data=frame, vcov={"CRV1": CLUSTER})
    increment = pf.feols(increment_formula, data=frame, vcov={"CRV1": CLUSTER})
    paths = pd.concat(
        [
            _event_rows(
                direct, "treated_X_disp_X_type_low", "low_type_ddd"
            ),
            _event_rows(
                direct, "treated_X_disp_X_type_high", "high_type_ddd"
            ),
            _event_rows(
                increment,
                "treated_X_disp_X_type_high_increment",
                "high_minus_low_type_ddd_difference",
            ),
        ],
        ignore_index=True,
    )
    tests = pd.DataFrame(
        [
            _joint_pretrend(
                direct, "treated_X_disp_X_type_low", "low_type_ddd_pretrend"
            ),
            _joint_pretrend(
                direct, "treated_X_disp_X_type_high", "high_type_ddd_pretrend"
            ),
            _joint_pretrend(
                increment,
                "treated_X_disp_X_type_high_increment",
                "difference_in_ddd_pretrend",
            ),
        ]
    )
    return paths, tests


def _cell_support(
    sample: pd.DataFrame, traits: pd.DataFrame, threshold: float
) -> pd.DataFrame:
    frame, episode = _prepare(
        sample,
        traits,
        variant=BEST_VARIANT,
        minimum_orders=BEST_MINIMUM_ORDERS,
        threshold=threshold,
    )
    episode_info = frame.drop_duplicates("event_fe_id")[[
        "event_fe_id", CLUSTER, "treated", "disp_binary", "type_high", "type_orders"
    ]]
    return (
        episode_info.groupby(["type_high", "treated", "disp_binary"], sort=True)
        .agg(
            episodes=("event_fe_id", "size"),
            closures=(CLUSTER, "nunique"),
            mean_pre_orders=("type_orders", "mean"),
        )
        .reset_index()
    )


def _write_report(
    results: pd.DataFrame,
    reliability: pd.DataFrame,
    traits: pd.DataFrame,
    thresholds: pd.DataFrame,
    leave_out: pd.DataFrame,
    pretrends: pd.DataFrame,
) -> None:
    tests = results.loc[
        results["estimand"].isin(
            ["high_minus_low_type_ddd_difference", "ddd_slope_per_unit_type"]
        )
    ].sort_values("pvalue")
    best = tests.iloc[0]
    preferred = results.loc[
        (results["variant"] == "separate_8")
        & (results["minimum_pre_orders"] == 1)
        & (results["estimand"] == "high_minus_low_type_ddd_difference")
    ].iloc[0]
    loo_binary = leave_out.loc[leave_out["model"] == "binary"]
    loo_cont = leave_out.loc[leave_out["model"] == "continuous"]
    adjacent = reliability.loc[
        (reliability["comparison"] == "adjacent_4_week_blocks")
        & (reliability["minimum_orders_across_full_span"] == 1)
    ].iloc[0]
    trait_best = traits.loc[traits["variant"] == BEST_VARIANT].iloc[0]
    pre_diff = pretrends.loc[
        pretrends["test"] == "difference_in_ddd_pretrend"
    ].iloc[0]
    fixed_threshold_row = thresholds.loc[
        thresholds["threshold_rule"] == "full_eligible_median"
    ].iloc[0]
    screened_median_row = thresholds.loc[
        thresholds["threshold_rule"] == "screened_median"
    ].iloc[0]
    report = f"""# Longer pre-window heterogeneity audit

## Question and design

This audit asks whether measuring baseline novelty over a longer history, optionally requiring more baseline purchases, produces credible heterogeneity in the novelty-seeking DDD. It does not change the manuscript or its main estimation code. All models use the exact 18-closure main cohort, the corrected fully saturated interaction hierarchy, and closure-event clustered standard errors.

Five histories are compared: the existing weeks -4 to -1 (`overlap_4`); overlapping extensions through weeks -8 and -12; and two histories that end before the outcome regression's pre-period, weeks -8 to -5 (`separate_4`) and -12 to -5 (`separate_8`). The non-overlapping histories are preferable because the baseline trait and regression outcome do not reuse the same customer-period observations. Minimum-order screens of 1, 3, 5, 10, 15, and 20 are crossed with each history. Both a fixed median split and a continuous trait are estimated.

## Main result

Longer histories do **not** provide stable evidence of heterogeneity. The smallest raw p-value among the {len(tests)} binary and continuous type-difference tests is {best.pvalue:.3f}: {best.variant}, at least {int(best.minimum_pre_orders)} orders, {best.estimand}, coefficient {best.coef:.3f} (SE {best.se:.3f}). Its Holm-adjusted p-value across the specification grid is {best.holm_adjusted_pvalue_across_all_type_tests:.3f}.

The most defensible longer definition before looking at results is the non-overlapping eight-period history (`separate_8`) without an extra activity screen. Its binary high-minus-low DDD difference is {preferred.coef:.3f} (SE {preferred.se:.3f}, p = {preferred.pvalue:.3f}). Thus the preferred design is null.

The isolated raw-significant result occurs for weeks -8 to -5 with at least {BEST_MINIMUM_ORDERS} orders. Under the median threshold fixed using all customers eligible for that window, the binary difference is {fixed_threshold_row.coef:.3f} (SE {fixed_threshold_row.se:.3f}, p = {fixed_threshold_row.pvalue:.3f}). This split is highly unbalanced after screening ({int(fixed_threshold_row.low_type_episodes)} low versus {int(fixed_threshold_row.high_type_episodes)} high). Re-splitting at the screened-sample median gives {screened_median_row.coef:.3f} (SE {screened_median_row.se:.3f}, p = {screened_median_row.pvalue:.3f}). The original-threshold estimate is not dominated by one closure: leave-one-closure estimates range from {loo_binary.coef.min():.3f} to {loo_binary.coef.max():.3f}, and {int((loo_binary.pvalue < .05).sum())} of 18 remain significant at 5%. The continuous leave-one-out slopes range from {loo_cont.coef.min():.3f} to {loo_cont.coef.max():.3f}; {int((loo_cont.pvalue < .05).sum())} of 18 remain significant at 5%.

The event-study joint pretrend test for the high-minus-low DDD path has p = {pre_diff.pvalue:.3f}. This diagnostic is informative but does not rescue the post-hoc cell if it passes, nor is it the sole reason to reject it if it fails.

## Measurement diagnostics

Longer histories improve coverage and order counts, but baseline novelty remains negatively related to exposure. For `separate_4`, the Pearson correlation between novelty and order count is {trait_best.pearson_novelty_order_correlation:.3f}; low- and high-type customers average {trait_best.mean_orders_low_type:.2f} and {trait_best.mean_orders_high_type:.2f} orders, respectively. Adjacent four-period novelty measures correlate only {adjacent.pearson_correlation:.3f} (Pearson; {adjacent.spearman_correlation:.3f} Spearman), indicating substantial within-customer instability/noise in the short trait.

## Interpretation

This exploration does not identify a defensible way to restore the earlier heterogeneity claim. A minimum-purchase rule improves measurement precision in principle, but selecting a particular window and cutoff because it yields significance is outcome-driven specification search. The favorable cell is reasonably stable to closure deletion and has no rejected joint pretrend, but is sensitive to the type threshold, has thin high-type support, and is one result from a large grid. The appropriate record is therefore: longer histories increase trait availability, yet the corrected heterogeneity result remains generally null; the isolated cell should be treated as exploratory rather than confirmatory evidence.

## Files

- `long_pre_window_heterogeneity_results.csv`: complete specification grid and Holm correction.
- `long_pre_window_trait_diagnostics.csv`: dependence of the trait on purchase exposure.
- `long_pre_window_split_history_reliability.csv`: stability across adjacent history blocks.
- `long_pre_window_threshold_sensitivity.csv`: threshold sensitivity of the isolated cell.
- `long_pre_window_best_cell_leave_one_event_out.csv`: closure influence.
- `long_pre_window_best_cell_event_study.csv` and `long_pre_window_best_cell_pretrend_tests.csv`: dynamic path and joint pretrend tests.
- `long_pre_window_best_cell_support.csv`: cell counts and closure support.
"""
    (OUTPUT_DIR / "LONG_PRE_WINDOW_AUDIT.md").write_text(report, encoding="utf-8")


def main() -> None:
    sample = pd.read_csv(SAMPLE_PATH)
    traits = pd.read_csv(TRAIT_PATH)
    components = pd.read_csv(COMPONENT_PATH)
    results = pd.read_csv(RESULT_PATH)

    reliability = _split_history_reliability(traits, components)
    diagnostics = _trait_diagnostics(traits)
    thresholds = _threshold_sensitivity(sample, traits)
    fixed_threshold = float(
        traits.loc[traits[f"{BEST_VARIANT}_novelty_mean"].notna(), f"{BEST_VARIANT}_novelty_mean"].median()
    )
    leave_out = _leave_one_event_out(sample, traits, fixed_threshold)
    paths, pretrends = _event_study(sample, traits, fixed_threshold)
    support = _cell_support(sample, traits, fixed_threshold)

    reliability.to_csv(OUTPUT_DIR / "long_pre_window_split_history_reliability.csv", index=False)
    diagnostics.to_csv(OUTPUT_DIR / "long_pre_window_trait_diagnostics.csv", index=False)
    thresholds.to_csv(OUTPUT_DIR / "long_pre_window_threshold_sensitivity.csv", index=False)
    leave_out.to_csv(OUTPUT_DIR / "long_pre_window_best_cell_leave_one_event_out.csv", index=False)
    paths.to_csv(OUTPUT_DIR / "long_pre_window_best_cell_event_study.csv", index=False)
    pretrends.to_csv(OUTPUT_DIR / "long_pre_window_best_cell_pretrend_tests.csv", index=False)
    support.to_csv(OUTPUT_DIR / "long_pre_window_best_cell_support.csv", index=False)
    _write_report(results, reliability, diagnostics, thresholds, leave_out, pretrends)

    print("\nThreshold sensitivity")
    print(thresholds.to_string(index=False))
    print("\nSplit-history reliability")
    print(reliability.to_string(index=False))
    print("\nPretrend tests")
    print(pretrends.to_string(index=False))
    print("\nLeave-one-out summaries")
    print(leave_out.groupby("model")["coef"].agg(["min", "max", "mean"]).to_string())


if __name__ == "__main__":
    main()
