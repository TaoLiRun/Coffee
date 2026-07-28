from __future__ import annotations

from pathlib import Path

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
TRAIT_PATH = (
    ROOT
    / "outputs"
    / "paper"
    / "heterogeneity_audit"
    / "long_pre_window"
    / "episode_long_pre_novelty_traits.csv"
)
OUTPUT_DIR = TRAIT_PATH.parent
OUTCOME = "variety_seeking"
FE = "event_fe_id + rel_t + calendar_month"
CLUSTER = "closure_event_id"
VARIANTS = ["overlap_4", "overlap_8", "overlap_12", "separate_4", "separate_8"]
MINIMUM_ORDERS = [1, 3, 5, 10, 15, 20]


def _coef(fit, term: str) -> dict:
    row = fit.tidy().loc[term]
    return {
        "coef": float(row["Estimate"]),
        "se": float(row["Std. Error"]),
        "pvalue": float(row["Pr(>|t|)"]),
        "ci_low": float(row["2.5%"]),
        "ci_high": float(row["97.5%"]),
    }


def _holm(pvalues: pd.Series) -> pd.Series:
    order = pvalues.sort_values().index
    m = len(order)
    running = 0.0
    adjusted: dict[int, float] = {}
    for rank, index in enumerate(order):
        running = max(running, min(1.0, (m - rank) * float(pvalues.loc[index])))
        adjusted[index] = running
    return pd.Series(adjusted).reindex(pvalues.index)


def _prepare_work(
    sample: pd.DataFrame,
    traits: pd.DataFrame,
    *,
    variant: str,
    minimum_orders: int,
    threshold: float,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    trait_col = f"{variant}_novelty_mean"
    order_col = f"{variant}_orders"
    episode = traits.loc[
        traits[trait_col].notna() & (traits[order_col] >= minimum_orders),
        ["event_fe_id", trait_col, order_col],
    ].copy()
    episode = episode.rename(columns={trait_col: "type_value", order_col: "type_orders"})
    episode["type_high"] = (episode["type_value"] > threshold).astype(int)
    work = sample.merge(
        episode, on="event_fe_id", how="inner", validate="many_to_one"
    )
    for column in ["post", "treated", "disp_binary", "type_high"]:
        work[column] = work[column].astype(int)
    p = work["post"]
    t = work["treated"]
    d = work["disp_binary"]
    h = work["type_high"]
    low = 1 - h

    work["post_X_treated"] = p * t
    work["post_X_disp"] = p * d
    work["post_X_treated_X_disp"] = p * t * d
    work["post_X_type_high"] = p * h
    work["post_X_treated_X_type_high"] = p * t * h
    work["post_X_disp_X_type_high"] = p * d * h
    work["post_X_treated_X_disp_X_type_high"] = p * t * d * h

    work["post_X_disp_X_type_low"] = p * d * low
    work["post_X_disp_X_type_high_direct"] = p * d * h
    work["post_X_treated_X_type_low"] = p * t * low
    work["post_X_treated_X_disp_X_type_low"] = p * t * d * low
    work["post_X_treated_X_type_high_direct"] = p * t * h
    work["post_X_treated_X_disp_X_type_high_direct"] = p * t * d * h

    center = float(episode["type_value"].mean())
    work["type_centered"] = work["type_value"] - center
    z = work["type_centered"]
    work["post_X_type_cont"] = p * z
    work["post_X_treated_X_type_cont"] = p * t * z
    work["post_X_disp_X_type_cont"] = p * d * z
    work["post_X_treated_X_disp_X_type_cont"] = p * t * d * z
    return work, episode


def _fit_cell(
    sample: pd.DataFrame,
    traits: pd.DataFrame,
    *,
    variant: str,
    minimum_orders: int,
    threshold: float,
) -> list[dict]:
    work, episode = _prepare_work(
        sample,
        traits,
        variant=variant,
        minimum_orders=minimum_orders,
        threshold=threshold,
    )
    if episode["type_high"].nunique() != 2 or work[CLUSTER].nunique() != 18:
        raise ValueError(f"Insufficient support for {variant}, min orders {minimum_orders}.")

    increment_formula = (
        f"{OUTCOME} ~ post_X_treated + post_X_disp + post_X_treated_X_disp + "
        "post_X_type_high + post_X_treated_X_type_high + "
        "post_X_disp_X_type_high + post_X_treated_X_disp_X_type_high "
        f"| {FE}"
    )
    direct_formula = (
        f"{OUTCOME} ~ post_X_type_high + post_X_disp_X_type_low + "
        "post_X_disp_X_type_high_direct + post_X_treated_X_type_low + "
        "post_X_treated_X_disp_X_type_low + post_X_treated_X_type_high_direct + "
        f"post_X_treated_X_disp_X_type_high_direct | {FE}"
    )
    continuous_formula = (
        f"{OUTCOME} ~ post_X_treated + post_X_disp + post_X_treated_X_disp + "
        "post_X_type_cont + post_X_treated_X_type_cont + "
        "post_X_disp_X_type_cont + post_X_treated_X_disp_X_type_cont "
        f"| {FE}"
    )
    increment = pf.feols(increment_formula, data=work, vcov={"CRV1": CLUSTER})
    direct = pf.feols(direct_formula, data=work, vcov={"CRV1": CLUSTER})
    continuous = pf.feols(
        continuous_formula, data=work, vcov={"CRV1": CLUSTER}
    )

    inc = increment.tidy()
    direct_tidy = direct.tidy()
    low = direct_tidy.loc["post_X_treated_X_disp_X_type_low", "Estimate"]
    high = direct_tidy.loc[
        "post_X_treated_X_disp_X_type_high_direct", "Estimate"
    ]
    difference = inc.loc["post_X_treated_X_disp_X_type_high", "Estimate"]
    if not np.isclose(high - low, difference, atol=1e-10):
        raise AssertionError(f"Binary parameterizations disagree for {variant}.")
    if increment._N != direct._N or not np.isclose(increment._r2, direct._r2):
        raise AssertionError(f"Binary fits disagree for {variant}.")

    base = {
        "variant": variant,
        "minimum_pre_orders": minimum_orders,
        "type_threshold": threshold,
        "type_mean_in_screened_sample": float(episode["type_value"].mean()),
        "type_sd_in_screened_sample": float(episode["type_value"].std()),
        "eligible_episodes": len(episode),
        "low_type_episodes": int((episode["type_high"] == 0).sum()),
        "high_type_episodes": int((episode["type_high"] == 1).sum()),
        "mean_type_orders": float(episode["type_orders"].mean()),
        "closure_clusters": 18,
        "cluster": CLUSTER,
    }
    rows: list[dict] = []
    for model, fit, term, estimand in [
        (
            "binary_saturated_increment",
            increment,
            "post_X_type_high",
            "general_post_shift_high_minus_low_type",
        ),
        (
            "binary_saturated_direct",
            direct,
            "post_X_treated_X_disp_X_type_low",
            "low_type_ddd",
        ),
        (
            "binary_saturated_direct",
            direct,
            "post_X_treated_X_disp_X_type_high_direct",
            "high_type_ddd",
        ),
        (
            "binary_saturated_increment",
            increment,
            "post_X_treated_X_disp_X_type_high",
            "high_minus_low_type_ddd_difference",
        ),
        (
            "continuous_saturated",
            continuous,
            "post_X_treated_X_disp",
            "ddd_at_mean_type",
        ),
        (
            "continuous_saturated",
            continuous,
            "post_X_treated_X_disp_X_type_cont",
            "ddd_slope_per_unit_type",
        ),
    ]:
        rows.append(
            {
                **base,
                "model": model,
                "estimand": estimand,
                "term": term,
                **_coef(fit, term),
                "regression_observations": int(fit._N),
                "r2": float(fit._r2),
                "r2_within": float(fit._r2_within),
            }
        )
    return rows


def main() -> None:
    sample = pd.read_csv(SAMPLE_PATH)
    traits = pd.read_csv(TRAIT_PATH)
    rows: list[dict] = []
    skipped: list[dict] = []
    thresholds: dict[str, float] = {}
    for variant in VARIANTS:
        trait_col = f"{variant}_novelty_mean"
        thresholds[variant] = float(traits.loc[traits[trait_col].notna(), trait_col].median())
        for minimum in MINIMUM_ORDERS:
            try:
                rows.extend(
                    _fit_cell(
                        sample,
                        traits,
                        variant=variant,
                        minimum_orders=minimum,
                        threshold=thresholds[variant],
                    )
                )
            except (KeyError, ValueError) as error:
                skipped.append(
                    {
                        "variant": variant,
                        "minimum_pre_orders": minimum,
                        "type_threshold": thresholds[variant],
                        "status": "not_identified",
                        "reason": str(error),
                    }
                )
    result = pd.DataFrame(rows)
    test_mask = result["estimand"].isin(
        ["high_minus_low_type_ddd_difference", "ddd_slope_per_unit_type"]
    )
    result["holm_adjusted_pvalue_across_all_type_tests"] = np.nan
    result.loc[test_mask, "holm_adjusted_pvalue_across_all_type_tests"] = _holm(
        result.loc[test_mask, "pvalue"]
    )
    result.to_csv(OUTPUT_DIR / "long_pre_window_heterogeneity_results.csv", index=False)
    pd.DataFrame(skipped).to_csv(
        OUTPUT_DIR / "long_pre_window_unidentified_cells.csv", index=False
    )

    tests = result.loc[test_mask].sort_values("pvalue")
    print(
        tests[
            [
                "variant",
                "minimum_pre_orders",
                "estimand",
                "eligible_episodes",
                "coef",
                "se",
                "pvalue",
                "holm_adjusted_pvalue_across_all_type_tests",
            ]
        ].to_string(index=False)
    )
    if skipped:
        print("\nUnidentified cells")
        print(pd.DataFrame(skipped).to_string(index=False))


if __name__ == "__main__":
    main()
