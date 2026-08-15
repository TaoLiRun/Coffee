#!/usr/bin/env python3
"""Re-estimate customer-level manuscript inference with consumer clusters.

This runner is intentionally separate from the production output generators.
It reads their locked samples or saved analysis panels, changes only the CRV1
cluster to ``member_id``, and writes small sensitivity artifacts under
``outputs/06_inference_sensitivity/consumer_cluster``. Closure-event inference
remains the production specification.
"""

from __future__ import annotations

import argparse
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pyfixest as pf
from scipy import stats


CLUSTER = "member_id"
EVENT = "closure_event_id"
BASE_FE = ["event_fe_id", "rel_t", "calendar_month"]
FAMILIES = (
    "core",
    "baseline_heterogeneity",
    "notifications",
    "return_timing",
    "noncoffee",
    "cafe_density",
    "raw_paths",
)


def parse_args() -> argparse.Namespace:
    script_path = Path(__file__).resolve()
    root = script_path.parents[2] if len(script_path.parents) > 2 else Path.cwd()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=root)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/06_inference_sensitivity/consumer_cluster"),
    )
    parser.add_argument(
        "--families",
        nargs="+",
        choices=FAMILIES,
        default=list(FAMILIES),
    )
    parser.add_argument(
        "--return-input-dir",
        type=Path,
        default=Path("outputs/05_robustness/reopening_assortment_constraints"),
    )
    parser.add_argument("--chunksize", type=int, default=2_000_000)
    return parser.parse_args()


def resolve(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


def save_metadata(
    output_dir: Path,
    family: str,
    inputs: list[str],
    details: dict | None = None,
) -> None:
    metadata = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "family": family,
        "variance_estimator": "CRV1",
        "cluster": CLUSTER,
        "inference_role": "sensitivity; closure_event_id remains primary",
        "inputs": inputs,
        "python": platform.python_version(),
        "pyfixest": pf.__version__,
    }
    if details:
        metadata.update(details)
    (output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2, default=str) + "\n", encoding="utf-8"
    )


def actual_cluster_count(fit) -> int:
    return int(round(float(fit._df_t))) + 1


def run_core(root: Path, output_root: Path) -> None:
    from src.displacement_effect_estimation.specs import (
        fit_collapsed_specs,
        fit_event_study_specs,
    )

    specifications = {
        "purchase_frequency": (
            "outputs/03_main_18_closures/purchase_frequency_ddd_h4/estimation_sample.csv",
            "n_purchases",
        ),
        "purchase_incidence": (
            "outputs/03_main_18_closures/purchase_incidence_ddd_h4/estimation_sample.csv",
            "purchase_incidence_binary",
        ),
        "novelty_member_first": (
            "outputs/03_main_18_closures/novelty_member_first_ddd_h4/estimation_sample.csv",
            "variety_seeking",
        ),
        "novelty_market_new": (
            "outputs/03_main_18_closures/novelty_market_new_ddd_h4/estimation_sample.csv",
            "variety_seeking",
        ),
    }
    for label, (relative_path, outcome) in specifications.items():
        print(f"[core] {label}", flush=True)
        path = root / relative_path
        frame = pd.read_csv(path, encoding="utf-8-sig")
        frame = frame.loc[frame[outcome].notna() & frame["rel_t"].ne(0)].copy()
        collapsed, collapsed_fit = fit_collapsed_specs(
            frame, outcome, cluster_col=CLUSTER
        )
        events, event_fit, pretrends = fit_event_study_specs(
            frame, outcome, cluster_col=CLUSTER
        )
        out = output_root / "core" / label
        out.mkdir(parents=True, exist_ok=True)
        collapsed.to_csv(out / "collapsed_results.csv", index=False)
        collapsed_fit.to_csv(out / "collapsed_fit.csv", index=False)
        events.to_csv(out / "event_study_results.csv", index=False)
        event_fit.to_csv(out / "event_study_fit.csv", index=False)
        pretrends.to_csv(out / "pretrend_tests.csv", index=False)
        save_metadata(
            out,
            "core",
            [relative_path],
            {
                "label": label,
                "outcome": outcome,
                "observations": int(len(frame)),
                "consumer_clusters_before_estimator_singleton_handling": int(
                    frame[CLUSTER].nunique()
                ),
            },
        )


def load_baseline_frame(module) -> tuple[pd.DataFrame, pd.DataFrame]:
    traits = module._load_baseline_traits()
    sample = pd.read_csv(module.SAMPLE_PATH)
    sample = sample.loc[sample[module.OUTCOME].notna()].copy()
    frame = sample.merge(
        traits, on="event_fe_id", how="inner", validate="many_to_one"
    )
    for column in ["rel_t", "post", "treated", "disp_binary", CLUSTER]:
        frame[column] = pd.to_numeric(frame[column], errors="raise").astype(int)
    episode = frame.drop_duplicates("event_fe_id")
    if episode[CLUSTER].duplicated().any():
        raise AssertionError("A customer appears in more than one closure event")
    if episode[EVENT].nunique() != 18:
        raise AssertionError("Expected the 18-event cohort")
    return frame, traits


def run_baseline_heterogeneity(root: Path, output_root: Path) -> None:
    from scripts.writeup import estimate_baseline_novelty_mechanism as module

    print("[baseline heterogeneity]", flush=True)
    module.CLUSTER = CLUSTER
    frame, traits = load_baseline_frame(module)
    out = output_root / "baseline_novelty_heterogeneity"
    out.mkdir(parents=True, exist_ok=True)
    summary_rows = []
    for adjusted, label in [(True, "with_order_adjustment"), (False, "without_order_adjustment")]:
        collapsed_frame, formula = module._add_collapsed_interactions(
            frame.copy(), include_order_adjustment=adjusted
        )
        fit = module._fit(formula, collapsed_frame)
        coefficients = module._coefficient_output(fit)
        n_clusters = actual_cluster_count(fit)
        coefficients["cluster"] = CLUSTER
        coefficients["n_clusters"] = n_clusters
        events, pretrend = module._event_study(
            frame.copy(), include_order_adjustment=adjusted
        )
        events["cluster"] = CLUSTER
        events["n_clusters"] = n_clusters
        pretrend["cluster"] = CLUSTER
        pretrend["n_clusters"] = n_clusters
        coefficients.to_csv(out / f"collapsed_{label}.csv", index=False)
        events.to_csv(out / f"event_study_{label}.csv", index=False)
        pretrend.to_csv(out / f"pretrend_{label}.csv", index=False)
        theta = coefficients.loc[coefficients["term"].eq(module.THETA_TERM)].iloc[0]
        summary_rows.append(
            {
                "specification": label,
                "term": module.THETA_TERM,
                "estimate": float(theta["estimate"]),
                "se": float(theta["se"]),
                "pvalue_two_sided": float(theta["pvalue_two_sided"]),
                "pvalue_one_sided_positive": float(
                    theta["pvalue_one_sided_positive"]
                ),
                "pretrend_pvalue": float(pretrend.iloc[0]["pvalue"]),
                "n": int(theta["n"]),
                "n_clusters": n_clusters,
            }
        )
    pd.DataFrame(summary_rows).to_csv(out / "headline_comparison.csv", index=False)
    save_metadata(
        out,
        "baseline_heterogeneity",
        [
            str(module.SAMPLE_PATH.relative_to(root)),
            str(module.NOVELTY_COMPONENTS.relative_to(root)),
            str(module.ORDER_COMPONENTS.relative_to(root)),
        ],
        {
            "eligible_traits": int(len(traits)),
            "regression_rows_before_estimator_singleton_handling": int(len(frame)),
        },
    )


def notification_fit_ddd(module, data: pd.DataFrame, outcome: str, comparison: str) -> dict:
    if comparison == "post_vs_pre":
        work = data.loc[data["rel_t"].ne(0)].copy()
        work["after"] = work["rel_t"].gt(0).astype(int)
    elif comparison == "during_vs_all_pre":
        work = data.loc[data["rel_t"].le(0)].copy()
        work["after"] = work["rel_t"].eq(0).astype(int)
    elif comparison == "during_vs_last_pre":
        work = data.loc[data["rel_t"].isin([-1, 0])].copy()
        work["after"] = work["rel_t"].eq(0).astype(int)
    else:
        raise ValueError(comparison)
    work["after_X_treated"] = work["after"] * work["treated"]
    work["after_X_high"] = work["after"] * work["disp_binary"]
    term = "after_X_treated_X_high"
    work[term] = work["after"] * work["treated"] * work["disp_binary"]
    regressors = ["after_X_treated", "after_X_high", term]
    fit = module.fit_fe_ols(work, outcome, regressors, BASE_FE, CLUSTER)
    index = regressors.index(term)
    return {
        "comparison": comparison,
        "outcome": outcome,
        "term": term,
        "coef": float(fit["beta"][index]),
        "se_crv1": float(fit["standard_errors"][index]),
        "pvalue_crv1": float(fit["pvalues"][index]),
        "ci_low": float(fit["ci_low"][index]),
        "ci_high": float(fit["ci_high"][index]),
        "n": int(fit["n"]),
        "clusters": int(len(fit["cluster_labels"])),
        "singleton_drops": int(fit["singleton_drops"]),
        "cluster": CLUSTER,
    }


def notification_event_study(module, data: pd.DataFrame, outcome: str):
    work = data.copy()
    regressors = []
    triple_terms = []
    term_to_period = {}
    for period in module.REL_PERIODS:
        if period == -1:
            continue
        suffix = f"m{abs(period)}" if period < 0 else f"p{period}"
        indicator = work["rel_t"].eq(period).astype(int)
        treated_term = f"rt_{suffix}_X_treated"
        high_term = f"rt_{suffix}_X_high"
        triple_term = f"rt_{suffix}_X_treated_X_high"
        work[treated_term] = indicator * work["treated"]
        work[high_term] = indicator * work["disp_binary"]
        work[triple_term] = indicator * work["treated"] * work["disp_binary"]
        regressors.extend([treated_term, high_term, triple_term])
        triple_terms.append(triple_term)
        term_to_period[triple_term] = period
    fit = module.fit_fe_ols(work, outcome, regressors, BASE_FE, CLUSTER)
    rows = []
    for term in triple_terms:
        index = regressors.index(term)
        rows.append(
            {
                "outcome": outcome,
                "term": term,
                "rel_t": term_to_period[term],
                "coef": float(fit["beta"][index]),
                "se_crv1": float(fit["standard_errors"][index]),
                "pvalue_crv1": float(fit["pvalues"][index]),
                "ci_low": float(fit["ci_low"][index]),
                "ci_high": float(fit["ci_high"][index]),
                "cluster": CLUSTER,
                "clusters": int(len(fit["cluster_labels"])),
            }
        )
    pre_terms = [term for term in triple_terms if term_to_period[term] < -1]
    indices = [regressors.index(term) for term in pre_terms]
    beta = fit["beta"][indices]
    covariance = fit["covariance"][np.ix_(indices, indices)]
    wald = float(beta.T @ np.linalg.pinv(covariance) @ beta)
    f_statistic = wald / len(indices)
    df_denom = len(fit["cluster_labels"]) - 1
    pretrend = {
        "outcome": outcome,
        "wald_chi2": wald,
        "pvalue_chi2": float(stats.chi2.sf(wald, len(indices))),
        "f_statistic": f_statistic,
        "df_num": len(indices),
        "df_denom": df_denom,
        "pvalue_f_cluster_df": float(stats.f.sf(f_statistic, len(indices), df_denom)),
        "cluster": CLUSTER,
        "clusters": int(len(fit["cluster_labels"])),
    }
    return pd.DataFrame(rows).sort_values("rel_t"), pretrend


def run_notifications(root: Path, output_root: Path) -> None:
    from scripts.writeup import estimate_new_product_notification_exposure as module

    print("[notifications]", flush=True)
    input_path = (
        root
        / "outputs/05_robustness/new_product_notification_exposure/"
        "new_product_push_panel.parquet"
    )
    panel = pd.read_parquet(input_path)
    outcomes = [
        "new_campaigns_per_day",
        "new_records_per_day",
        "any_new_push",
        "new_push_days_per_day",
        "campaigns_per_day",
        "push_records_per_day",
        "new_campaign_share",
    ]
    comparisons = ["post_vs_pre", "during_vs_all_pre", "during_vs_last_pre"]
    ddd = pd.DataFrame(
        [
            notification_fit_ddd(module, panel, outcome, comparison)
            for outcome in outcomes
            for comparison in comparisons
        ]
    )
    events, pretrend = notification_event_study(
        module, panel, "new_campaigns_per_day"
    )
    out = output_root / "new_product_notification_exposure"
    out.mkdir(parents=True, exist_ok=True)
    ddd.to_csv(out / "ddd_results.csv", index=False)
    events.to_csv(out / "event_study_results.csv", index=False)
    pd.DataFrame([pretrend]).to_csv(out / "pretrend_test.csv", index=False)
    save_metadata(
        out,
        "notifications",
        [str(input_path.relative_to(root))],
        {"panel_rows": int(len(panel)), "members": int(panel[CLUSTER].nunique())},
    )


def fit_return_outcomes(module, data: pd.DataFrame, outcomes: list[str]) -> pd.DataFrame:
    rows = []
    for outcome in outcomes:
        work = data.copy()
        if "novel_opportunity_share" in outcome:
            work = work.loc[
                work["complete_4_week_novel_opportunity_share_leave_one_out"].eq(1)
            ].copy()
        fit = module.fit_fe_ols(
            work, outcome, ["disp_binary"], [EVENT], CLUSTER
        )
        row = module.extract_term(fit, "disp_binary")
        row.update(
            {
                "outcome": outcome,
                "estimand": "high_minus_low_among_treated_first_returners",
                "cluster": CLUSTER,
            }
        )
        rows.append(row)
    return pd.DataFrame(rows)


def run_return_timing(
    root: Path, output_root: Path, return_input_dir: Path
) -> None:
    from scripts.writeup import estimate_reopening_assortment_constraints as module

    print("[return timing]", flush=True)
    input_dir = resolve(root, return_input_dir)
    first_path = input_dir / "treated_first_return_exposure.csv"
    opportunity_path = input_dir / "treated_return_week_novel_opportunity.csv"
    first = pd.read_csv(first_path)
    opportunity = pd.read_csv(opportunity_path)
    actual = opportunity.loc[opportunity["is_actual_return_week"].eq(1)].copy()
    actual["event_store_fe"] = actual[EVENT]
    first_results = fit_return_outcomes(
        module,
        first,
        ["days_after_reopening", *module.OUTCOMES],
    )
    opportunity_results = fit_return_outcomes(
        module,
        actual,
        [
            "novel_opportunity_share_leave_one_out",
            "timing_deviation_novel_opportunity_share_leave_one_out",
            "novel_products_leave_one_out",
            "timing_deviation_novel_products_leave_one_out",
        ],
    )
    out = output_root / "return_timing_novel_opportunity"
    out.mkdir(parents=True, exist_ok=True)
    first_results.to_csv(out / "first_return_results.csv", index=False)
    opportunity_results.to_csv(out / "novel_opportunity_results.csv", index=False)
    save_metadata(
        out,
        "return_timing",
        [str(first_path), str(opportunity_path)],
        {
            "first_return_rows": int(len(first)),
            "actual_opportunity_rows": int(len(actual)),
        },
    )


def run_noncoffee(root: Path, output_root: Path, chunksize: int) -> None:
    from scripts.writeup import estimate_noncoffee_novelty_ddd as module

    print("[noncoffee: reconstructing outcomes from authoritative transactions]", flush=True)
    module.CLUSTER = CLUSTER
    panel, headline_path = module.load_headline_grid(root)
    member_ids = set(panel[CLUSTER].dropna().astype(int).unique())
    raw_path = root.parent / "data/data1031/order_commodity_result.csv"
    transactions, _, audit = module.load_and_classify_transactions(
        raw_path, member_ids, chunksize
    )
    panel = module.construct_outcomes(panel, transactions)

    def contributing_clusters(outcome: str) -> int:
        observed = panel.loc[panel[outcome].notna(), ["event_fe_id", CLUSTER]]
        counts = observed.groupby("event_fe_id", observed=True).size()
        retained = set(counts.loc[counts.gt(1)].index)
        return int(
            observed.loc[observed["event_fe_id"].isin(retained), CLUSTER].nunique()
        )

    cluster_counts = {"variety_seeking": contributing_clusters("variety_seeking")}
    for scope in module.SCOPES:
        cluster_counts[f"novelty_{scope}"] = contributing_clusters(
            f"novelty_{scope}"
        )
        cluster_counts[f"any_purchase_{scope}"] = contributing_clusters(
            f"any_purchase_{scope}"
        )
    ddd_rows = []
    event_frames = []
    pretrend_frames = []
    entry_event_frames = []
    entry_pretrend_frames = []
    headline_rows, _ = module.fit_collapsed(
        panel,
        "variety_seeking",
        "headline_all_products",
        "conditional_novelty",
        0,
        module.SEED,
    )
    ddd_rows.extend(headline_rows)
    headline_event, headline_pretrend = module.fit_event_study(
        panel, "variety_seeking", "headline_all_products"
    )
    event_frames.append(headline_event)
    pretrend_frames.append(headline_pretrend)
    for index, scope in enumerate(module.SCOPES, start=1):
        novelty_outcome = f"novelty_{scope}"
        rows, _ = module.fit_collapsed(
            panel,
            novelty_outcome,
            scope,
            "conditional_novelty",
            0,
            module.SEED + index,
        )
        ddd_rows.extend(rows)
        event, pretrend = module.fit_event_study(panel, novelty_outcome, scope)
        event_frames.append(event)
        pretrend_frames.append(pretrend)
        entry_outcome = f"any_purchase_{scope}"
        entry_rows, _ = module.fit_collapsed(
            panel,
            entry_outcome,
            scope,
            "purchase_entry",
            0,
            module.SEED + 100 + index,
        )
        ddd_rows.extend(entry_rows)
        entry_event, entry_pretrend = module.fit_event_study(
            panel, entry_outcome, scope
        )
        entry_event_frames.append(entry_event)
        entry_pretrend_frames.append(entry_pretrend)
    out = output_root / "noncoffee_novelty"
    out.mkdir(parents=True, exist_ok=True)
    ddd = pd.DataFrame(ddd_rows)
    ddd["clusters"] = ddd["outcome"].map(cluster_counts)
    ddd["cluster"] = CLUSTER
    events = pd.concat(event_frames, ignore_index=True)
    events["clusters"] = events["outcome"].map(cluster_counts)
    events["cluster"] = CLUSTER
    pretrends = pd.concat(pretrend_frames, ignore_index=True)
    pretrends["clusters"] = pretrends["outcome"].map(cluster_counts)
    pretrends["cluster"] = CLUSTER
    entry_events = pd.concat(entry_event_frames, ignore_index=True)
    entry_events["clusters"] = entry_events["outcome"].map(cluster_counts)
    entry_events["cluster"] = CLUSTER
    entry_pretrends = pd.concat(entry_pretrend_frames, ignore_index=True)
    entry_pretrends["clusters"] = entry_pretrends["outcome"].map(cluster_counts)
    entry_pretrends["cluster"] = CLUSTER
    ddd.to_csv(out / "ddd_results.csv", index=False)
    events.to_csv(
        out / "event_study_results.csv", index=False
    )
    pretrends.to_csv(
        out / "pretrend_tests.csv", index=False
    )
    entry_events.to_csv(
        out / "entry_event_study_results.csv", index=False
    )
    entry_pretrends.to_csv(
        out / "entry_pretrend_tests.csv", index=False
    )
    save_metadata(
        out,
        "noncoffee",
        [str(headline_path.relative_to(root)), str(raw_path)],
        {
            "raw_audit": audit,
            "panel_rows": int(len(panel)),
            "members": int(panel[CLUSTER].nunique()),
            "contributing_consumer_clusters_by_outcome": cluster_counts,
        },
    )


def cafe_model_row(
    module,
    spec: str,
    estimand: str,
    result: dict,
    model: dict,
    raw_count: float | None = None,
    standardized_density: float | None = None,
    measure: str | None = None,
) -> dict:
    return {
        "spec": spec,
        "measure": measure,
        "estimand": estimand,
        "raw_count": raw_count,
        "standardized_density": standardized_density,
        **result,
        "observations": int(model["n"]),
        "member_events": int(model["work"]["event_fe_id"].nunique()),
        "consumer_clusters": int(len(model["cluster_labels"])),
        "fixed_effects": " + ".join(model["fixed_effects"]),
        "cluster": CLUSTER,
    }


def load_cafe_frame(
    root: Path, sample_relative: str, episode_relative: str
) -> pd.DataFrame:
    sample = pd.read_csv(root / sample_relative, encoding="utf-8-sig")
    episode = pd.read_csv(root / episode_relative, encoding="utf-8-sig")
    density_columns = [
        "event_fe_id",
        "preferred_store",
        "cafe_count_500m",
        "cafe_count_1500m",
    ]
    frame = sample.merge(
        episode[density_columns],
        on="event_fe_id",
        how="inner",
        validate="many_to_one",
    )
    return frame.loc[frame["variety_seeking"].notna()].copy()


def run_cafe_density(root: Path, output_root: Path) -> None:
    from scripts.writeup import estimate_time_invariant_cafe_density_robustness as module

    print("[cafe density]", flush=True)
    member_sample = (
        "outputs/03_main_18_closures/novelty_member_first_ddd_h4/estimation_sample.csv"
    )
    market_sample = (
        "outputs/03_main_18_closures/novelty_market_new_ddd_h4/estimation_sample.csv"
    )
    member_episode = (
        "outputs/05_robustness/time_invariant_cafe_density/"
        "member_first_regression_episode_density.csv"
    )
    market_episode = (
        "outputs/05_robustness/time_invariant_cafe_density/"
        "market_new_regression_episode_density.csv"
    )
    frame = load_cafe_frame(root, member_sample, member_episode)
    market_frame = load_cafe_frame(root, market_sample, market_episode)
    frame, initial_drops = module.drop_singletons(frame, BASE_FE)
    market_frame, market_drops = module.drop_singletons(market_frame, BASE_FE)

    transform_configs = {
        "raw_500m_interaction": (module.RAW_500, False, "density_z_raw_500m"),
        "log_500m_interaction": (module.RAW_500, True, "density_z_log_500m"),
        "raw_1500m_interaction": (module.RAW_1500, False, "density_z_raw_1500m"),
        "log_1500m_interaction": (module.RAW_1500, True, "density_z_log_1500m"),
    }
    transforms = {}
    for spec, (raw_column, log_transform, z_column) in transform_configs.items():
        z, transform = module.standardized_episode_measure(
            frame, raw_column, log_transform
        )
        frame[z_column] = z.to_numpy()
        transforms[spec] = transform
    market_z, market_transform = module.standardized_episode_measure(
        market_frame, module.RAW_500, False
    )
    market_frame["density_z_raw_500m"] = market_z.to_numpy()

    baseline_work, baseline_terms = module.add_collapsed_terms(frame)
    baseline_model = module.fit_fe_ols(
        baseline_work,
        module.OUTCOME,
        baseline_terms,
        BASE_FE,
        CLUSTER,
        drop_fe_singletons=False,
    )
    rows = [
        cafe_model_row(
            module,
            "paper_facing_baseline",
            "high_minus_low_ddd",
            module.linear_combination(
                baseline_model, {"post_X_treated_X_disp": 1.0}
            ),
            baseline_model,
        )
    ]
    models = {}
    for spec, (raw_column, _, z_column) in transform_configs.items():
        work, terms = module.add_collapsed_terms(frame, z_column)
        model = module.fit_fe_ols(
            work,
            module.OUTCOME,
            terms,
            BASE_FE,
            CLUSTER,
            drop_fe_singletons=False,
        )
        models[spec] = (model, work)
        gradient = "post_X_treated_X_disp_X_density"
        rows.append(
            cafe_model_row(
                module,
                spec,
                "ddd_at_member_event_mean",
                module.linear_combination(model, {"post_X_treated_X_disp": 1.0}),
                model,
                standardized_density=0.0,
                measure=raw_column,
            )
        )
        rows.append(
            cafe_model_row(
                module,
                spec,
                "density_gradient_per_sd",
                module.linear_combination(model, {gradient: 1.0}),
                model,
                measure=raw_column,
            )
        )
        if raw_column == module.RAW_500:
            counts = module.PRIMARY_COUNTS
        else:
            episode_values = frame.drop_duplicates("event_fe_id")[raw_column]
            counts = (0.0, *[float(episode_values.quantile(q)) for q in (0.25, 0.5, 0.75)])
        for count in counts:
            z_value = module.standardize_raw_value(float(count), transforms[spec])
            rows.append(
                cafe_model_row(
                    module,
                    spec,
                    "fitted_ddd",
                    module.linear_combination(
                        model,
                        {
                            "post_X_treated_X_disp": 1.0,
                            gradient: z_value,
                        },
                    ),
                    model,
                    raw_count=float(count),
                    standardized_density=z_value,
                    measure=raw_column,
                )
            )

    low = frame.loc[frame[module.RAW_500].le(module.LOW_DENSITY_CUTOFF)].copy()
    low_work, low_terms = module.add_collapsed_terms(low)
    low_model = module.fit_fe_ols(
        low_work, module.OUTCOME, low_terms, BASE_FE, CLUSTER
    )
    rows.append(
        cafe_model_row(
            module,
            "low_density_le3_descriptive",
            "high_minus_low_ddd",
            module.linear_combination(low_model, {"post_X_treated_X_disp": 1.0}),
            low_model,
        )
    )

    store_frame = frame.copy()
    store_frame["preferred_store_event_post_fe"] = (
        store_frame[EVENT].astype(str)
        + "|store_"
        + store_frame["preferred_store"].astype(str)
        + "|post_"
        + store_frame["post"].astype(str)
    )
    store_work, _ = module.add_collapsed_terms(store_frame)
    store_terms = ["post_X_disp", "post_X_treated_X_disp"]
    store_fes = [*BASE_FE, "preferred_store_event_post_fe"]
    store_model = module.fit_fe_ols(
        store_work,
        module.OUTCOME,
        store_terms,
        store_fes,
        CLUSTER,
        drop_fe_singletons=False,
    )
    rows.append(
        cafe_model_row(
            module,
            "preferred_store_event_post_fe",
            "high_minus_low_ddd",
            module.linear_combination(store_model, {"post_X_treated_X_disp": 1.0}),
            store_model,
        )
    )

    market_base_work, market_base_terms = module.add_collapsed_terms(market_frame)
    market_base_model = module.fit_fe_ols(
        market_base_work,
        module.OUTCOME,
        market_base_terms,
        BASE_FE,
        CLUSTER,
        drop_fe_singletons=False,
    )
    rows.append(
        cafe_model_row(
            module,
            "market_new_baseline",
            "high_minus_low_ddd",
            module.linear_combination(
                market_base_model, {"post_X_treated_X_disp": 1.0}
            ),
            market_base_model,
            measure="market-new outcome",
        )
    )
    market_work, market_terms = module.add_collapsed_terms(
        market_frame, "density_z_raw_500m"
    )
    market_model = module.fit_fe_ols(
        market_work,
        module.OUTCOME,
        market_terms,
        BASE_FE,
        CLUSTER,
        drop_fe_singletons=False,
    )
    gradient = "post_X_treated_X_disp_X_density"
    for estimand, weights, count in [
        ("ddd_at_member_event_mean", {"post_X_treated_X_disp": 1.0}, None),
        ("density_gradient_per_sd", {gradient: 1.0}, None),
    ]:
        rows.append(
            cafe_model_row(
                module,
                "market_new_raw_500m_interaction",
                estimand,
                module.linear_combination(market_model, weights),
                market_model,
                raw_count=count,
                measure=module.RAW_500,
            )
        )
    for count in module.PRIMARY_COUNTS:
        z_value = module.standardize_raw_value(float(count), market_transform)
        rows.append(
            cafe_model_row(
                module,
                "market_new_raw_500m_interaction",
                "fitted_ddd",
                module.linear_combination(
                    market_model,
                    {"post_X_treated_X_disp": 1.0, gradient: z_value},
                ),
                market_model,
                raw_count=float(count),
                standardized_density=z_value,
                measure=module.RAW_500,
            )
        )

    primary_model, _ = models["raw_500m_interaction"]
    event_work, event_terms, term_map = module.add_event_study_terms(
        frame, "density_z_raw_500m"
    )
    event_model = module.fit_fe_ols(
        event_work,
        module.OUTCOME,
        event_terms,
        BASE_FE,
        CLUSTER,
        drop_fe_singletons=False,
    )
    event_results = module.event_study_results(
        event_model, term_map, transforms["raw_500m_interaction"], [2.0, 13.0]
    )
    event_results["cluster"] = CLUSTER
    pre_terms = [
        term_map[period]["treated_X_disp_X_density"]
        for period in [-4, -3, -2]
    ]
    pretrend = module.joint_zero_test(
        event_model, pre_terms, "density-gradient leads jointly zero"
    )
    pretrend["cluster"] = CLUSTER
    pretrend["consumer_clusters"] = len(event_model["cluster_labels"])

    store_event_frame = frame.copy()
    store_event_frame["preferred_store_event_period_fe"] = (
        store_event_frame[EVENT].astype(str)
        + "|store_"
        + store_event_frame["preferred_store"].astype(str)
        + "|rel_"
        + store_event_frame["rel_t"].astype(str)
    )
    store_event_work, store_event_terms, store_map = (
        module.add_store_fe_event_study_terms(store_event_frame)
    )
    store_event_fes = [*BASE_FE, "preferred_store_event_period_fe"]
    store_event_model = module.fit_fe_ols(
        store_event_work,
        module.OUTCOME,
        store_event_terms,
        store_event_fes,
        CLUSTER,
        drop_fe_singletons=False,
    )
    store_event_results = module.store_fe_event_study_results(
        store_event_model, store_map
    )
    store_event_results["cluster"] = CLUSTER
    store_pretrend = module.joint_zero_test(
        store_event_model,
        [store_map[period] for period in [-4, -3, -2]],
        "preferred-store-event-period-FE DDD leads jointly zero",
    )
    store_pretrend["cluster"] = CLUSTER
    store_pretrend["consumer_clusters"] = len(store_event_model["cluster_labels"])

    out = output_root / "cafe_density"
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out / "model_estimands.csv", index=False)
    event_results.to_csv(out / "density_event_study.csv", index=False)
    store_event_results.to_csv(out / "preferred_store_fe_event_study.csv", index=False)
    pd.DataFrame([pretrend, store_pretrend]).to_csv(
        out / "pretrend_tests.csv", index=False
    )
    save_metadata(
        out,
        "cafe_density",
        [member_sample, market_sample, member_episode, market_episode],
        {
            "member_first_rows": int(len(frame)),
            "market_new_rows": int(len(market_frame)),
            "initial_singleton_drops": int(initial_drops),
            "market_singleton_drops": int(market_drops),
            "wild_cluster_pvalues": "not computed for consumer clusters",
            "unused_primary_model_consumer_clusters": int(
                len(primary_model["cluster_labels"])
            ),
        },
    )


def consumer_mean_summary(
    frame: pd.DataFrame, value: str, by: list[str]
) -> pd.DataFrame:
    rows = []
    for keys, group in frame.groupby(by, sort=True, observed=True):
        if not isinstance(keys, tuple):
            keys = (keys,)
        values = group[value].dropna().astype(float)
        aligned = group.loc[values.index]
        mean = float(values.mean())
        scores = (values - mean).groupby(aligned[CLUSTER]).sum()
        clusters = int(scores.size)
        variance = (clusters / (clusters - 1)) * float((scores**2).sum()) / (
            len(values) ** 2
        )
        se = float(np.sqrt(max(variance, 0.0)))
        critical = float(stats.t.ppf(0.975, clusters - 1))
        rows.append(
            {
                **dict(zip(by, keys)),
                "mean": mean,
                "se_cluster": se,
                "ci_low": mean - critical * se,
                "ci_high": mean + critical * se,
                "observations": int(len(values)),
                "n_clusters": clusters,
                "cluster": CLUSTER,
            }
        )
    return pd.DataFrame(rows)


def build_purchase_period_zero(root: Path, base: pd.DataFrame) -> pd.DataFrame:
    from scripts.writeup import generate_paper_exhibits as exhibits

    keys = ["member_id", "dept_id", "closure_start", "closure_end"]
    members = (
        base[
            keys
            + [
                "closure_duration_days",
                "closure_event_id",
                "group",
                "treated",
            ]
        ]
        .drop_duplicates(keys)
        .copy()
    )
    member_ids = set(members[CLUSTER].dropna().astype(int))
    orders = exhibits.load_orders_for_behavior_members(member_ids=member_ids)
    orders = orders.sort_values("date").reset_index(drop=True)
    parts = []
    for _, cohort in members.groupby(
        ["dept_id", "closure_start", "closure_end"], sort=False
    ):
        start = pd.to_datetime(cohort["closure_start"].iloc[0])
        end = pd.to_datetime(cohort["closure_end"].iloc[0])
        duration = float(cohort["closure_duration_days"].iloc[0])
        window_orders = exhibits._slice_by_date(orders, start, end)
        window_orders = window_orders.loc[
            window_orders[CLUSTER].isin(cohort[CLUSTER])
        ]
        counts = (
            window_orders.groupby(CLUSTER)["date"]
            .nunique()
            .rename("_purchase_days")
            .reset_index()
            if not window_orders.empty
            else pd.DataFrame(columns=[CLUSTER, "_purchase_days"])
        )
        block = cohort.merge(counts, on=CLUSTER, how="left")
        block["_purchase_days"] = block["_purchase_days"].fillna(0.0)
        block["mean_source"] = block["_purchase_days"] / duration
        block["rel_t"] = 0
        parts.append(block[[CLUSTER, EVENT, "group", "rel_t", "mean_source"]])
    return pd.concat(parts, ignore_index=True)


def run_raw_paths(root: Path, output_root: Path) -> None:
    print("[raw paths]", flush=True)
    purchase_path = (
        root
        / "outputs/03_main_18_closures/purchase_frequency_ddd_h4/estimation_sample.csv"
    )
    novelty_path = (
        root
        / "outputs/03_main_18_closures/novelty_member_first_ddd_h4/estimation_sample.csv"
    )
    purchase = pd.read_csv(purchase_path, encoding="utf-8-sig")
    purchase["mean_source"] = purchase["purchase_frequency"]
    purchase_base = purchase[[CLUSTER, EVENT, "group", "rel_t", "mean_source"]]
    period_zero = build_purchase_period_zero(root, purchase)
    purchase_panel = pd.concat([purchase_base, period_zero], ignore_index=True)
    purchase_summary = consumer_mean_summary(
        purchase_panel, "mean_source", ["group", "rel_t"]
    )

    novelty = pd.read_csv(novelty_path, encoding="utf-8-sig")
    novelty = novelty.loc[novelty["rel_t"].ne(0)].copy()
    novelty_summary = consumer_mean_summary(
        novelty,
        "variety_seeking",
        ["disp_binary", "treated", "rel_t"],
    )
    novelty["novelty_observed"] = novelty["variety_seeking"].notna().astype(float)
    probability_summary = consumer_mean_summary(
        novelty,
        "novelty_observed",
        ["disp_binary", "treated", "rel_t"],
    ).rename(columns={"mean": "purchase_probability"})

    out = output_root / "raw_paths"
    out.mkdir(parents=True, exist_ok=True)
    purchase_summary.to_csv(out / "raw_purchase_paths.csv", index=False)
    novelty_summary.to_csv(out / "raw_novelty_paths.csv", index=False)
    probability_summary.to_csv(out / "purchase_probability_paths.csv", index=False)
    save_metadata(
        out,
        "raw_paths",
        [str(purchase_path.relative_to(root)), str(novelty_path.relative_to(root))],
        {"purchase_period_zero_reconstructed_from_orders": True},
    )


def main() -> None:
    args = parse_args()
    root = args.project_root.resolve()
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    output_root = resolve(root, args.output_dir)
    output_root.mkdir(parents=True, exist_ok=True)
    for family in args.families:
        if family == "core":
            run_core(root, output_root)
        elif family == "baseline_heterogeneity":
            run_baseline_heterogeneity(root, output_root)
        elif family == "notifications":
            run_notifications(root, output_root)
        elif family == "return_timing":
            run_return_timing(root, output_root, args.return_input_dir)
        elif family == "noncoffee":
            run_noncoffee(root, output_root, args.chunksize)
        elif family == "cafe_density":
            run_cafe_density(root, output_root)
        elif family == "raw_paths":
            run_raw_paths(root, output_root)
        else:
            raise ValueError(family)
    print(f"Saved consumer-cluster sensitivity outputs to {output_root}", flush=True)


if __name__ == "__main__":
    main()
