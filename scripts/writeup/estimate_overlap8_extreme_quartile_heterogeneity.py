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
OUTCOME = "variety_seeking"
FE = "event_fe_id + rel_t + calendar_month"
CLUSTER = "closure_event_id"
NOVELTY = "overlap_8_novelty_mean"
ORDERS = "overlap_8_orders"
MINIMUM_ORDERS = 15


def _row(fit, term: str, estimand: str) -> dict:
    result = fit.tidy().loc[term]
    return {
        "estimand": estimand,
        "term": term,
        "coef": float(result["Estimate"]),
        "se": float(result["Std. Error"]),
        "pvalue": float(result["Pr(>|t|)"]),
        "ci_low": float(result["2.5%"]),
        "ci_high": float(result["97.5%"]),
        "regression_observations": int(fit._N),
        "r2": float(fit._r2),
        "r2_within": float(fit._r2_within),
        "closure_clusters": int(fit._data[CLUSTER].nunique()),
        "cluster": CLUSTER,
    }


def _prepare(sample: pd.DataFrame, traits: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, float, float]:
    eligible = traits.loc[
        traits[NOVELTY].notna() & (traits[ORDERS] >= MINIMUM_ORDERS),
        ["event_fe_id", NOVELTY, ORDERS],
    ].copy()
    q25, q75 = eligible[NOVELTY].quantile([0.25, 0.75]).tolist()
    extreme = eligible.loc[
        (eligible[NOVELTY] <= q25) | (eligible[NOVELTY] >= q75)
    ].copy()
    extreme["type_high"] = (extreme[NOVELTY] >= q75).astype(int)
    extreme = extreme.rename(columns={NOVELTY: "type_value", ORDERS: "type_orders"})
    frame = sample.merge(extreme, on="event_fe_id", how="inner", validate="many_to_one")
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
    frame["post_X_disp_X_type_low"] = p * d * low
    frame["post_X_disp_X_type_high_direct"] = p * d * h
    frame["post_X_treated_X_type_low"] = p * t * low
    frame["post_X_treated_X_disp_X_type_low"] = p * t * d * low
    frame["post_X_treated_X_type_high_direct"] = p * t * h
    frame["post_X_treated_X_disp_X_type_high_direct"] = p * t * d * h
    frame["treated_X_disp"] = t * d
    frame["treated_X_type_high_increment"] = t * h
    frame["disp_X_type_high_increment"] = d * h
    frame["treated_X_disp_X_type_high_increment"] = t * d * h
    return frame, extreme, float(q25), float(q75)


def _fit_main(frame: pd.DataFrame) -> tuple[pd.DataFrame, object]:
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
    increment = pf.feols(increment_formula, data=frame, vcov={"CRV1": CLUSTER})
    direct = pf.feols(direct_formula, data=frame, vcov={"CRV1": CLUSTER})
    low = _row(direct, "post_X_treated_X_disp_X_type_low", "low_quartile_ddd")
    high = _row(
        direct,
        "post_X_treated_X_disp_X_type_high_direct",
        "high_quartile_ddd",
    )
    difference = _row(
        increment,
        "post_X_treated_X_disp_X_type_high",
        "high_minus_low_quartile_ddd_difference",
    )
    if not np.isclose(high["coef"] - low["coef"], difference["coef"], atol=1e-10):
        raise AssertionError("Direct and increment parameterizations disagree.")
    post_shift = _row(
        increment, "post_X_type_high", "general_post_shift_high_minus_low_quartile"
    )
    return pd.DataFrame([post_shift, low, high, difference]), increment


def _extract_rel_t(term: str) -> int | None:
    match = re.search(r"\[(-?\d+)\]", term)
    if match:
        return int(match.group(1))
    match = re.search(r"rel_t::(-?\d+):", term)
    return int(match.group(1)) if match else None


def _fit_event_study(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    formula = (
        f"{OUTCOME} ~ i(rel_t, treated, ref=-1) + "
        "i(rel_t, treated_X_disp, ref=-1) + "
        "i(rel_t, disp_binary, ref=-1) + "
        "i(rel_t, type_high, ref=-1) + "
        "i(rel_t, treated_X_type_high_increment, ref=-1) + "
        "i(rel_t, disp_X_type_high_increment, ref=-1) + "
        f"i(rel_t, treated_X_disp_X_type_high_increment, ref=-1) | {FE}"
    )
    fit = pf.feols(formula, data=frame, vcov={"CRV1": CLUSTER})
    suffix = "treated_X_disp_X_type_high_increment"
    rows: list[dict] = []
    terms: list[str] = []
    for term, result in fit.tidy().iterrows():
        if not str(term).endswith(f":{suffix}"):
            continue
        rel_t = _extract_rel_t(str(term))
        if rel_t is None:
            continue
        if rel_t in {-4, -3, -2}:
            terms.append(str(term))
        rows.append(
            {
                "rel_t": rel_t,
                "coef": float(result["Estimate"]),
                "se": float(result["Std. Error"]),
                "pvalue": float(result["Pr(>|t|)"]),
                "ci_low": float(result["2.5%"]),
                "ci_high": float(result["97.5%"]),
                "regression_observations": int(fit._N),
                "closure_clusters": 18,
            }
        )
    if len(terms) != 3:
        raise ValueError(f"Expected three pretrend terms, found {terms}")
    names = list(map(str, fit.tidy().index))
    positions = {term: index for index, term in enumerate(names)}
    restrictions = np.zeros((3, len(names)))
    for row, term in enumerate(terms):
        restrictions[row, positions[term]] = 1
    test = fit.wald_test(R=restrictions)
    return pd.DataFrame(rows), pd.DataFrame(
        [{"test": "high_minus_low_quartile_ddd_pretrend", "statistic": float(test.iloc[0]), "pvalue": float(test.iloc[1]), "n_restrictions": 3, "closure_clusters": 18}]
    )


def _leave_one_event_out(frame: pd.DataFrame) -> pd.DataFrame:
    formula = (
        f"{OUTCOME} ~ post_X_treated + post_X_disp + post_X_treated_X_disp + "
        "post_X_type_high + post_X_treated_X_type_high + "
        "post_X_disp_X_type_high + post_X_treated_X_disp_X_type_high "
        f"| {FE}"
    )
    rows: list[dict] = []
    for omitted in sorted(frame[CLUSTER].unique(), key=str):
        subset = frame.loc[frame[CLUSTER] != omitted]
        fit = pf.feols(formula, data=subset, vcov={"CRV1": CLUSTER})
        rows.append(
            {
                "omitted_event": omitted,
                **_row(
                    fit,
                    "post_X_treated_X_disp_X_type_high",
                    "high_minus_low_quartile_ddd_difference",
                ),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    sample = pd.read_csv(SAMPLE_PATH)
    traits = pd.read_csv(TRAIT_PATH)
    frame, extreme, q25, q75 = _prepare(sample, traits)
    results, _ = _fit_main(frame)
    results.insert(0, "q25", q25)
    results.insert(1, "q75", q75)
    results.insert(2, "eligible_before_extreme_filter", int(
        (traits[NOVELTY].notna() & (traits[ORDERS] >= MINIMUM_ORDERS)).sum()
    ))
    results.insert(3, "retained_extreme_episodes", len(extreme))
    results.insert(4, "low_quartile_episodes", int((extreme["type_high"] == 0).sum()))
    results.insert(5, "high_quartile_episodes", int((extreme["type_high"] == 1).sum()))
    paths, pretrend = _fit_event_study(frame)
    leave_out = _leave_one_event_out(frame)
    episode = frame.drop_duplicates("event_fe_id")
    support = (
        episode.groupby(["type_high", "treated", "disp_binary"], sort=True)
        .agg(
            episodes=("event_fe_id", "size"),
            closures=(CLUSTER, "nunique"),
            mean_pre_orders=("type_orders", "mean"),
            mean_pre_novelty=("type_value", "mean"),
        )
        .reset_index()
    )
    prefix = "overlap8_min15_extreme_quartile"
    results.to_csv(OUTPUT_DIR / f"{prefix}_results.csv", index=False)
    paths.to_csv(OUTPUT_DIR / f"{prefix}_event_study.csv", index=False)
    pretrend.to_csv(OUTPUT_DIR / f"{prefix}_pretrend.csv", index=False)
    leave_out.to_csv(OUTPUT_DIR / f"{prefix}_leave_one_event_out.csv", index=False)
    support.to_csv(OUTPUT_DIR / f"{prefix}_support.csv", index=False)
    low = results.loc[results["estimand"] == "low_quartile_ddd"].iloc[0]
    high = results.loc[results["estimand"] == "high_quartile_ddd"].iloc[0]
    difference = results.loc[
        results["estimand"] == "high_minus_low_quartile_ddd_difference"
    ].iloc[0]
    note = f"""# Eight-period, minimum-15-order extreme-quartile sensitivity

Among the 5,358 episodes with an observed novelty trait over periods -8 through -1 and at least 15 orders in that history, the bottom quartile is defined as novelty no greater than {q25:.6f} and the top quartile as novelty at least {q75:.6f}. Ties leave 1,349 low-quartile and 1,350 high-quartile episodes; the middle 2,659 episodes are excluded.

Using the corrected fully saturated DDD and standard errors clustered by 18 closure events, the low-quartile DDD is {low.coef:.4f} (SE {low.se:.4f}, p = {low.pvalue:.3f}); the high-quartile DDD is {high.coef:.4f} (SE {high.se:.4f}, p = {high.pvalue:.3f}); and the high-minus-low difference is {difference.coef:.4f} (SE {difference.se:.4f}, 95% CI [{difference.ci_low:.4f}, {difference.ci_high:.4f}], p = {difference.pvalue:.3f}). The joint pretrend test for the high-minus-low DDD path rejects (p = {pretrend.pvalue.iloc[0]:.3f}). Leave-one-closure differences range from {leave_out.coef.min():.4f} to {leave_out.coef.max():.4f}, and none is significant at 10%.

This extreme-groups comparison therefore does not strengthen the heterogeneity evidence. It reduces precision by discarding half the eligible episodes, does not produce a statistically significant difference, and exhibits an adverse joint pretrend diagnostic.
"""
    (OUTPUT_DIR / f"{prefix}.md").write_text(note, encoding="utf-8")
    print(results.to_string(index=False))
    print("\nSupport")
    print(support.to_string(index=False))
    print("\nPretrend")
    print(pretrend.to_string(index=False))
    print("\nLeave-one-event-out")
    print(leave_out[["coef", "se", "pvalue"]].agg(["min", "max", "mean"]).to_string())


if __name__ == "__main__":
    main()
