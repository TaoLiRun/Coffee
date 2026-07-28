from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pyfixest as pf


ROOT = Path(__file__).resolve().parents[2]
SAMPLE_PATH = (
    ROOT
    / "outputs"
    / "04_diagnostics_18_closures"
    / "novelty_pre_heterogeneity_median"
    / "estimation_sample.csv"
)
COUNT_PATH = (
    ROOT
    / "outputs"
    / "paper"
    / "heterogeneity_audit"
    / "pre_novelty_purchase_count_episode_diagnostic.csv"
)
OUTPUT_PATH = (
    ROOT
    / "outputs"
    / "paper"
    / "heterogeneity_audit"
    / "pre_novelty_minimum_pre_order_sensitivity.csv"
)
OUTCOME = "variety_seeking"
FE = "event_fe_id + rel_t + calendar_month"
CLUSTER = "closure_event_id"


def _prepare(sample: pd.DataFrame, counts: pd.DataFrame) -> pd.DataFrame:
    frame = sample.merge(
        counts[["event_fe_id", "pre_orders", "pre_product_window_choices"]],
        on="event_fe_id",
        how="left",
        validate="many_to_one",
    )
    if frame[["pre_orders", "pre_product_window_choices"]].isna().any().any():
        raise ValueError("Purchase-count diagnostic does not cover the estimation sample.")
    for column in ["post", "treated", "disp_binary", "novelty_pre_high"]:
        frame[column] = frame[column].astype(int)
    p = frame["post"]
    t = frame["treated"]
    d = frame["disp_binary"]
    h = frame["novelty_pre_high"]
    low = 1 - h

    frame["post_X_treated"] = p * t
    frame["post_X_disp"] = p * d
    frame["post_X_treated_X_disp"] = p * t * d
    frame["post_X_pre_high"] = p * h
    frame["post_X_treated_X_pre_high"] = p * t * h
    frame["post_X_disp_X_pre_high"] = p * d * h
    frame["post_X_treated_X_disp_X_pre_high"] = p * t * d * h

    frame["post_X_disp_X_pre_low"] = p * d * low
    frame["post_X_disp_X_pre_high_direct"] = p * d * h
    frame["post_X_treated_X_pre_low"] = p * t * low
    frame["post_X_treated_X_disp_X_pre_low"] = p * t * d * low
    frame["post_X_treated_X_pre_high_direct"] = p * t * h
    frame["post_X_treated_X_disp_X_pre_high_direct"] = p * t * d * h
    return frame


def _result_row(
    fit,
    *,
    term: str,
    estimand: str,
    minimum_pre_orders: int,
    episodes: pd.DataFrame,
) -> dict:
    row = fit.tidy().loc[term]
    return {
        "minimum_pre_orders": minimum_pre_orders,
        "estimand": estimand,
        "term": term,
        "coef": float(row["Estimate"]),
        "se": float(row["Std. Error"]),
        "pvalue": float(row["Pr(>|t|)"]),
        "ci_low": float(row["2.5%"]),
        "ci_high": float(row["97.5%"]),
        "regression_observations": int(fit._N),
        "eligible_episodes": len(episodes),
        "low_pre_novelty_episodes": int((episodes["novelty_pre_high"] == 0).sum()),
        "high_pre_novelty_episodes": int((episodes["novelty_pre_high"] == 1).sum()),
        "mean_pre_orders": float(episodes["pre_orders"].mean()),
        "n_closure_clusters": int(episodes[CLUSTER].nunique()),
        "cluster": CLUSTER,
    }


def main() -> None:
    sample = pd.read_csv(SAMPLE_PATH)
    counts = pd.read_csv(COUNT_PATH)
    frame = _prepare(sample, counts)
    rows: list[dict] = []

    increment_formula = (
        f"{OUTCOME} ~ post_X_treated + post_X_disp + post_X_treated_X_disp + "
        "post_X_pre_high + post_X_treated_X_pre_high + "
        "post_X_disp_X_pre_high + post_X_treated_X_disp_X_pre_high "
        f"| {FE}"
    )
    direct_formula = (
        f"{OUTCOME} ~ post_X_pre_high + post_X_disp_X_pre_low + "
        "post_X_disp_X_pre_high_direct + post_X_treated_X_pre_low + "
        "post_X_treated_X_disp_X_pre_low + post_X_treated_X_pre_high_direct + "
        f"post_X_treated_X_disp_X_pre_high_direct | {FE}"
    )

    for minimum in [1, 2, 3, 4, 5, 7, 11]:
        work = frame.loc[frame["pre_orders"] >= minimum].copy()
        episodes = work.drop_duplicates("event_fe_id")
        if episodes[CLUSTER].nunique() != 18:
            raise ValueError(f"Threshold {minimum} loses closure-event support.")
        increment = pf.feols(
            increment_formula, data=work, vcov={"CRV1": CLUSTER}
        )
        direct = pf.feols(direct_formula, data=work, vcov={"CRV1": CLUSTER})

        increment_tidy = increment.tidy()
        direct_tidy = direct.tidy()
        low = direct_tidy.loc["post_X_treated_X_disp_X_pre_low", "Estimate"]
        high = direct_tidy.loc[
            "post_X_treated_X_disp_X_pre_high_direct", "Estimate"
        ]
        difference = increment_tidy.loc[
            "post_X_treated_X_disp_X_pre_high", "Estimate"
        ]
        if not np.isclose(high - low, difference, atol=1e-10):
            raise AssertionError(f"Parameterizations disagree at threshold {minimum}.")

        for fit, term, estimand in [
            (
                increment,
                "post_X_pre_high",
                "general_post_shift_high_minus_low_pre_novelty",
            ),
            (
                direct,
                "post_X_treated_X_disp_X_pre_low",
                "low_pre_novelty_ddd",
            ),
            (
                direct,
                "post_X_treated_X_disp_X_pre_high_direct",
                "high_pre_novelty_ddd",
            ),
            (
                increment,
                "post_X_treated_X_disp_X_pre_high",
                "high_minus_low_pre_novelty_ddd_difference",
            ),
        ]:
            rows.append(
                _result_row(
                    fit,
                    term=term,
                    estimand=estimand,
                    minimum_pre_orders=minimum,
                    episodes=episodes,
                )
            )

    result = pd.DataFrame(rows)
    result.to_csv(OUTPUT_PATH, index=False)
    display = result.pivot(
        index="minimum_pre_orders", columns="estimand", values=["coef", "se", "pvalue"]
    )
    print(display.to_string())


if __name__ == "__main__":
    main()
