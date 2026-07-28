from __future__ import annotations

import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import pyfixest as pf
from scipy.stats import t as student_t


ROOT = Path(__file__).resolve().parents[2]
SAMPLE_PATH = (
    ROOT
    / "outputs"
    / "03_main_18_closures"
    / "novelty_member_first_ddd_h4"
    / "estimation_sample.csv"
)
OUTPUT_DIR = ROOT / "outputs" / "paper" / "mechanism_baseline_novelty"
COMPONENT_DIR = OUTPUT_DIR / "inputs"
NOVELTY_COMPONENTS = COMPONENT_DIR / "episode_window_novelty_components.csv"
ORDER_COMPONENTS = COMPONENT_DIR / "episode_window_order_counts.csv"

OUTCOME = "variety_seeking"
CLUSTER = "closure_event_id"
FIXED_EFFECTS = "event_fe_id + rel_t + calendar_month"
BASELINE_PERIODS = tuple(range(-8, 0))
MINIMUM_BASELINE_ORDERS = 5
THETA_TERM = "post_X_treated_X_incidence_X_baseline_novelty"


def _load_baseline_traits() -> pd.DataFrame:
    novelty = pd.read_csv(NOVELTY_COMPONENTS)
    orders = pd.read_csv(ORDER_COMPONENTS)
    novelty = novelty.loc[novelty["rel_t_history"].isin(BASELINE_PERIODS)]
    novelty = (
        novelty.groupby("event_fe_id", sort=False)
        .agg(
            baseline_novelty=("window_novelty", "mean"),
            baseline_purchasing_periods=("rel_t_history", "nunique"),
            baseline_distinct_choices=("product_window_choices", "sum"),
        )
        .reset_index()
    )
    orders = orders.loc[orders["rel_t_history"].isin(BASELINE_PERIODS)]
    orders = (
        orders.groupby("event_fe_id", sort=False)
        .agg(baseline_orders=("orders", "sum"))
        .reset_index()
    )
    traits = novelty.merge(orders, on="event_fe_id", how="outer", validate="one_to_one")
    traits = traits.loc[
        traits["baseline_novelty"].notna()
        & traits["baseline_orders"].notna()
        & (traits["baseline_orders"] >= MINIMUM_BASELINE_ORDERS)
    ].copy()
    novelty_mean = float(traits["baseline_novelty"].mean())
    novelty_sd = float(traits["baseline_novelty"].std(ddof=0))
    traits["baseline_novelty_z"] = (
        traits["baseline_novelty"] - novelty_mean
    ) / novelty_sd
    traits["baseline_log_orders"] = np.log1p(traits["baseline_orders"])
    order_mean = float(traits["baseline_log_orders"].mean())
    order_sd = float(traits["baseline_log_orders"].std(ddof=0))
    traits["baseline_log_orders_z"] = (
        traits["baseline_log_orders"] - order_mean
    ) / order_sd
    traits.attrs.update(
        baseline_novelty_mean=novelty_mean,
        baseline_novelty_sd=novelty_sd,
        baseline_log_orders_mean=order_mean,
        baseline_log_orders_sd=order_sd,
    )
    return traits


def _load_frame(traits: pd.DataFrame) -> pd.DataFrame:
    sample = pd.read_csv(SAMPLE_PATH)
    sample = sample.loc[sample[OUTCOME].notna()].copy()
    frame = sample.merge(
        traits,
        on="event_fe_id",
        how="inner",
        validate="many_to_one",
    )
    for column in ["rel_t", "post", "treated", "disp_binary"]:
        frame[column] = pd.to_numeric(frame[column], errors="raise").astype(int)
    episode = frame.drop_duplicates("event_fe_id")
    if episode["member_id"].duplicated().any():
        raise AssertionError("A customer appears in more than one closure event")
    if episode[CLUSTER].nunique() != 18:
        raise AssertionError("Expected the 18-closure main cohort")
    return frame


def _add_collapsed_interactions(
    frame: pd.DataFrame,
    include_order_adjustment: bool = True,
) -> tuple[pd.DataFrame, str]:
    p = frame["post"]
    t = frame["treated"]
    h = frame["disp_binary"]
    n = frame["baseline_novelty_z"]
    o = frame["baseline_log_orders_z"]
    interactions: dict[str, pd.Series] = {
        "post_X_treated": p * t,
        "post_X_incidence": p * h,
        "post_X_treated_X_incidence": p * t * h,
        "post_X_baseline_novelty": p * n,
        "post_X_treated_X_baseline_novelty": p * t * n,
        "post_X_incidence_X_baseline_novelty": p * h * n,
        THETA_TERM: p * t * h * n,
    }
    if include_order_adjustment:
        interactions.update(
            {
                "post_X_baseline_log_orders": p * o,
                "post_X_treated_X_baseline_log_orders": p * t * o,
                "post_X_incidence_X_baseline_log_orders": p * h * o,
                "post_X_treated_X_incidence_X_baseline_log_orders": p * t * h * o,
            }
        )
    for name, value in interactions.items():
        frame[name] = value
    formula = f"{OUTCOME} ~ {' + '.join(interactions)} | {FIXED_EFFECTS}"
    return frame, formula


def _fit(formula: str, frame: pd.DataFrame):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return pf.feols(formula, data=frame, vcov={"CRV1": CLUSTER})


def _coefficient_output(fit) -> pd.DataFrame:
    output = fit.tidy().reset_index().rename(
        columns={
            "Coefficient": "term",
            "Estimate": "estimate",
            "Std. Error": "se",
            "t value": "tvalue",
            "Pr(>|t|)": "pvalue_two_sided",
            "2.5%": "ci_low",
            "97.5%": "ci_high",
        }
    )
    if "term" not in output.columns:
        output = output.rename(columns={output.columns[0]: "term"})
    output["pvalue_one_sided_positive"] = np.where(
        output["estimate"] >= 0,
        output["pvalue_two_sided"] / 2,
        1 - output["pvalue_two_sided"] / 2,
    )
    output["n"] = int(fit._N)
    output["reference_df"] = float(fit._df_t)
    output["cluster"] = CLUSTER
    output["n_clusters"] = 18
    return output


def _event_study(
    frame: pd.DataFrame,
    include_order_adjustment: bool = True,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    work = frame.copy()
    t = work["treated"]
    h = work["disp_binary"]
    n = work["baseline_novelty_z"]
    o = work["baseline_log_orders_z"]
    components: dict[str, pd.Series] = {
        "treated": t,
        "incidence": h,
        "treated_X_incidence": t * h,
        "baseline_novelty": n,
        "treated_X_baseline_novelty": t * n,
        "incidence_X_baseline_novelty": h * n,
        "treated_X_incidence_X_baseline_novelty": t * h * n,
    }
    if include_order_adjustment:
        components.update(
            {
                "baseline_log_orders": o,
                "treated_X_baseline_log_orders": t * o,
                "incidence_X_baseline_log_orders": h * o,
                "treated_X_incidence_X_baseline_log_orders": t * h * o,
            }
        )
    rhs: list[str] = []
    theta_terms: dict[int, str] = {}
    for rel_t in sorted(work["rel_t"].unique()):
        rel_t = int(rel_t)
        if rel_t == -1:
            continue
        tag = f"m{abs(rel_t)}" if rel_t < 0 else f"p{rel_t}"
        indicator = (work["rel_t"] == rel_t).astype(int)
        for name, value in components.items():
            column = f"rel_{tag}_X_{name}"
            work[column] = indicator * value
            rhs.append(column)
            if name == "treated_X_incidence_X_baseline_novelty":
                theta_terms[rel_t] = column
    formula = f"{OUTCOME} ~ {' + '.join(rhs)} | {FIXED_EFFECTS}"
    fit = _fit(formula, work)
    tidy = fit.tidy()
    rows: list[dict] = []
    for rel_t, term in theta_terms.items():
        result = tidy.loc[term]
        estimate = float(result["Estimate"])
        pvalue = float(result["Pr(>|t|)"])
        rows.append(
            {
                "rel_t": rel_t,
                "term": term,
                "estimate": estimate,
                "se": float(result["Std. Error"]),
                "pvalue_two_sided": pvalue,
                "pvalue_one_sided_positive": pvalue / 2 if estimate >= 0 else 1 - pvalue / 2,
                "ci_low": float(result["2.5%"]),
                "ci_high": float(result["97.5%"]),
                "n": int(fit._N),
            }
        )
    names = list(map(str, tidy.index))
    pre_terms = [theta_terms[value] for value in [-4, -3, -2]]
    positions = {name: index for index, name in enumerate(names)}
    restrictions = np.zeros((len(pre_terms), len(names)))
    for row, term in enumerate(pre_terms):
        restrictions[row, positions[term]] = 1
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        test = fit.wald_test(R=restrictions)
    pretrend = pd.DataFrame(
        [
            {
                "null_hypothesis": "theta_-4 = theta_-3 = theta_-2 = 0",
                "terms": ",".join(pre_terms),
                "restrictions": len(pre_terms),
                "wald_statistic": float(test.iloc[0]),
                "pvalue": float(test.iloc[1]),
                "cluster": CLUSTER,
                "n_clusters": 18,
            }
        ]
    )
    return pd.DataFrame(rows).sort_values("rel_t"), pretrend


def _support(frame: pd.DataFrame) -> pd.DataFrame:
    episode = frame.drop_duplicates("event_fe_id")
    return (
        episode.groupby(["treated", "disp_binary"], sort=True)
        .agg(
            episodes=("event_fe_id", "size"),
            closures=(CLUSTER, "nunique"),
            mean_baseline_novelty=("baseline_novelty", "mean"),
            sd_baseline_novelty=("baseline_novelty", "std"),
            mean_baseline_orders=("baseline_orders", "mean"),
        )
        .reset_index()
        .rename(columns={"disp_binary": "high_predicted_incidence"})
    )


def _distribution(traits: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    values = traits["baseline_novelty"].astype(float)
    quantiles = values.quantile([0.10, 0.25, 0.50, 0.75, 0.90])
    summary = pd.DataFrame(
        [
            ("eligible_episodes", float(len(values))),
            ("mean", float(values.mean())),
            ("sd", float(values.std(ddof=0))),
            ("minimum", float(values.min())),
            ("p10", float(quantiles.loc[0.10])),
            ("p25", float(quantiles.loc[0.25])),
            ("median", float(quantiles.loc[0.50])),
            ("p75", float(quantiles.loc[0.75])),
            ("p90", float(quantiles.loc[0.90])),
            ("maximum", float(values.max())),
            ("share_at_zero", float((values == 0).mean())),
            ("share_at_one", float((values == 1).mean())),
            ("mean_baseline_orders", float(traits["baseline_orders"].mean())),
            ("median_baseline_orders", float(traits["baseline_orders"].median())),
        ],
        columns=["statistic", "value"],
    )

    edges = np.linspace(0.0, 1.0, 11)
    counts, _ = np.histogram(values, bins=edges)
    bins = pd.DataFrame(
        {
            "bin_left": edges[:-1],
            "bin_right": edges[1:],
            "bin_midpoint": (edges[:-1] + edges[1:]) / 2,
            "episodes": counts.astype(int),
            "share": counts / len(values),
        }
    )
    if int(bins["episodes"].sum()) != len(values):
        raise AssertionError("Baseline-novelty histogram does not cover all episodes")
    return summary, bins


def _baseline_order_diagnostic(
    traits: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Describe the model-free relation between trait values and history length."""

    work = traits[
        ["event_fe_id", "baseline_novelty", "baseline_orders", "baseline_log_orders"]
    ].copy()
    summary = pd.DataFrame(
        [
            (
                "pearson_novelty_raw_orders",
                float(work["baseline_novelty"].corr(work["baseline_orders"])),
            ),
            (
                "spearman_novelty_raw_orders",
                float(
                    work["baseline_novelty"].corr(
                        work["baseline_orders"], method="spearman"
                    )
                ),
            ),
            (
                "pearson_novelty_log_orders",
                float(work["baseline_novelty"].corr(work["baseline_log_orders"])),
            ),
            (
                "spearman_novelty_log_orders",
                float(
                    work["baseline_novelty"].corr(
                        work["baseline_log_orders"], method="spearman"
                    )
                ),
            ),
            ("eligible_episodes", float(len(work))),
        ],
        columns=["statistic", "value"],
    )
    work["baseline_order_group"] = pd.cut(
        work["baseline_orders"],
        bins=[4, 5, 9, 19, np.inf],
        labels=["5", "6--9", "10--19", "20+"],
        right=True,
    )
    grouped = (
        work.groupby("baseline_order_group", observed=True, sort=False)
        .agg(
            episodes=("event_fe_id", "size"),
            minimum_orders=("baseline_orders", "min"),
            maximum_orders=("baseline_orders", "max"),
            mean_orders=("baseline_orders", "mean"),
            mean_baseline_novelty=("baseline_novelty", "mean"),
            sd_baseline_novelty=("baseline_novelty", "std"),
            share_novelty_zero=(
                "baseline_novelty",
                lambda values: np.isclose(values, 0).mean(),
            ),
            share_novelty_one=(
                "baseline_novelty",
                lambda values: np.isclose(values, 1).mean(),
            ),
        )
        .reset_index()
    )
    if int(grouped["episodes"].sum()) != len(work):
        raise AssertionError("Baseline-order diagnostic groups do not cover the sample")
    return summary, grouped


def _headline_results(coefficients: pd.DataFrame, fit) -> pd.DataFrame:
    terms = ["post_X_treated_X_incidence", THETA_TERM]
    labels = [
        "DDD at mean baseline novelty and order history",
        "Change in DDD per SD of baseline novelty",
    ]
    output = coefficients.set_index("term").loc[terms].reset_index()
    output.insert(1, "label", labels)
    output["estimate_percentage_points"] = 100 * output["estimate"]
    output["se_percentage_points"] = 100 * output["se"]
    output["r2"] = float(fit._r2)
    output["within_r2"] = float(fit._r2_within)
    return output


def _specification_comparison(
    current_coefficients: pd.DataFrame,
    current_fit,
    no_order_coefficients: pd.DataFrame,
    no_order_fit,
) -> pd.DataFrame:
    parts = []
    for specification, coefficients, fit in [
        ("with_baseline_order_adjustment", current_coefficients, current_fit),
        ("without_baseline_order_adjustment", no_order_coefficients, no_order_fit),
    ]:
        part = _headline_results(coefficients, fit)
        if specification == "without_baseline_order_adjustment":
            part.loc[
                part["term"] == "post_X_treated_X_incidence", "label"
            ] = "DDD at mean baseline novelty"
        part.insert(0, "specification", specification)
        parts.append(part)
    return pd.concat(parts, ignore_index=True)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    traits = _load_baseline_traits()
    frame = _load_frame(traits)
    work, formula = _add_collapsed_interactions(frame.copy())
    fit = _fit(formula, work)
    coefficients = _coefficient_output(fit)
    theta = coefficients.loc[coefficients["term"] == THETA_TERM].iloc[0]
    event_study, pretrend = _event_study(frame)
    no_order_work, no_order_formula = _add_collapsed_interactions(
        frame.copy(), include_order_adjustment=False
    )
    no_order_fit = _fit(no_order_formula, no_order_work)
    no_order_coefficients = _coefficient_output(no_order_fit)
    no_order_theta = no_order_coefficients.loc[
        no_order_coefficients["term"] == THETA_TERM
    ].iloc[0]
    no_order_event_study, no_order_pretrend = _event_study(
        frame, include_order_adjustment=False
    )
    support = _support(frame)
    distribution_summary, distribution_bins = _distribution(traits)
    order_diagnostic_summary, order_diagnostic_groups = _baseline_order_diagnostic(
        traits
    )
    headline = _headline_results(coefficients, fit)
    specification_comparison = _specification_comparison(
        coefficients, fit, no_order_coefficients, no_order_fit
    )
    eligible_episodes = len(traits)
    outcome_observed_episodes = frame["event_fe_id"].nunique()
    if (
        eligible_episodes != 18_525
        or outcome_observed_episodes != 17_866
        or int(fit._N) != 79_578
    ):
        raise AssertionError(
            "Unexpected accepted-specification sample: "
            f"eligible_episodes={eligible_episodes}, "
            f"outcome_observed_episodes={outcome_observed_episodes}, n={fit._N}"
        )
    if not np.isclose(float(theta["estimate"]), 0.029394, atol=5e-7):
        raise AssertionError(f"Accepted theta drifted: {theta['estimate']}")
    if not np.isclose(float(pretrend.iloc[0]["pvalue"]), 0.561121, atol=5e-6):
        raise AssertionError(f"Accepted pretrend drifted: {pretrend.iloc[0]['pvalue']}")
    if not np.isclose(float(no_order_theta["estimate"]), 0.022927, atol=5e-7):
        raise AssertionError(
            f"No-order-adjustment theta drifted: {no_order_theta['estimate']}"
        )
    if not np.isclose(
        float(no_order_theta["pvalue_one_sided_positive"]), 0.063633, atol=5e-6
    ):
        raise AssertionError(
            "No-order-adjustment one-sided p-value drifted: "
            f"{no_order_theta['pvalue_one_sided_positive']}"
        )
    if not np.isclose(
        float(no_order_pretrend.iloc[0]["pvalue"]), 0.409413, atol=5e-6
    ):
        raise AssertionError(
            "No-order-adjustment pretrend drifted: "
            f"{no_order_pretrend.iloc[0]['pvalue']}"
        )

    coefficients.to_csv(OUTPUT_DIR / "baseline_novelty_results.csv", index=False)
    event_study.to_csv(OUTPUT_DIR / "baseline_novelty_event_study.csv", index=False)
    pretrend.to_csv(OUTPUT_DIR / "baseline_novelty_pretrend_test.csv", index=False)
    no_order_coefficients.to_csv(
        OUTPUT_DIR / "baseline_novelty_results_without_order_adjustment.csv",
        index=False,
    )
    no_order_event_study.to_csv(
        OUTPUT_DIR / "baseline_novelty_event_study_without_order_adjustment.csv",
        index=False,
    )
    no_order_pretrend.to_csv(
        OUTPUT_DIR / "baseline_novelty_pretrend_without_order_adjustment.csv",
        index=False,
    )
    support.to_csv(OUTPUT_DIR / "baseline_novelty_support.csv", index=False)
    distribution_summary.to_csv(
        OUTPUT_DIR / "baseline_novelty_distribution_summary.csv", index=False
    )
    distribution_bins.to_csv(
        OUTPUT_DIR / "baseline_novelty_distribution_bins.csv", index=False
    )
    order_diagnostic_summary.to_csv(
        OUTPUT_DIR / "baseline_order_diagnostic_summary.csv", index=False
    )
    order_diagnostic_groups.to_csv(
        OUTPUT_DIR / "baseline_order_diagnostic_groups.csv", index=False
    )
    headline.to_csv(OUTPUT_DIR / "baseline_novelty_headline_results.csv", index=False)
    specification_comparison.to_csv(
        OUTPUT_DIR / "baseline_novelty_order_adjustment_comparison.csv", index=False
    )
    manifest = {
        "sample_path": str(SAMPLE_PATH.relative_to(ROOT)),
        "novelty_components": str(NOVELTY_COMPONENTS.relative_to(ROOT)),
        "order_components": str(ORDER_COMPONENTS.relative_to(ROOT)),
        "outcome": OUTCOME,
        "baseline_relative_periods": list(BASELINE_PERIODS),
        "minimum_baseline_orders": MINIMUM_BASELINE_ORDERS,
        "baseline_novelty_definition": "mean of within-period novelty-seeking over purchasing periods",
        "baseline_novelty_standardization_mean": traits.attrs["baseline_novelty_mean"],
        "baseline_novelty_standardization_sd": traits.attrs["baseline_novelty_sd"],
        "baseline_order_adjustment": "standardized log(1 + baseline orders), fully interacted with post, treatment, and predicted incidence",
        "formula": formula,
        "formula_without_baseline_order_adjustment": no_order_formula,
        "fixed_effects": FIXED_EFFECTS,
        "variance_estimator": "CRV1",
        "cluster": CLUSTER,
        "n_clusters": 18,
        "eligible_episodes": eligible_episodes,
        "outcome_observed_episodes_before_singleton_removal": outcome_observed_episodes,
        "regression_observations": int(fit._N),
        "r2": float(fit._r2),
        "within_r2": float(fit._r2_within),
        "theta_term": THETA_TERM,
        "theta": float(theta["estimate"]),
        "theta_se": float(theta["se"]),
        "theta_pvalue_one_sided_positive": float(theta["pvalue_one_sided_positive"]),
        "theta_pvalue_two_sided": float(theta["pvalue_two_sided"]),
        "pretrend_pvalue": float(pretrend.iloc[0]["pvalue"]),
        "theta_without_baseline_order_adjustment": float(no_order_theta["estimate"]),
        "theta_se_without_baseline_order_adjustment": float(no_order_theta["se"]),
        "theta_pvalue_one_sided_positive_without_baseline_order_adjustment": float(
            no_order_theta["pvalue_one_sided_positive"]
        ),
        "theta_pvalue_two_sided_without_baseline_order_adjustment": float(
            no_order_theta["pvalue_two_sided"]
        ),
        "pretrend_pvalue_without_baseline_order_adjustment": float(
            no_order_pretrend.iloc[0]["pvalue"]
        ),
        "pearson_baseline_novelty_log_orders": float(
            order_diagnostic_summary.set_index("statistic").loc[
                "pearson_novelty_log_orders", "value"
            ]
        ),
    }
    (OUTPUT_DIR / "baseline_novelty_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
