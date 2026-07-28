from __future__ import annotations

import argparse
import copy
import json
import logging
import os
import shutil
import subprocess
import sys
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd


DURATION25_KEY = (64, "2021-07-29")
INSUFFICIENT_HISTORY_KEY = (101, "2020-09-12")
LNY_KEYS = {
    (254, "2021-01-30"),
    (228, "2021-02-04"),
    (225, "2021-02-09"),
    (181, "2021-02-11"),
}


def event_keys(df: pd.DataFrame) -> pd.Series:
    return pd.Series(
        list(
            zip(
                df["dept_id"].astype(int),
                pd.to_datetime(df["closure_start"]).dt.strftime("%Y-%m-%d"),
            )
        ),
        index=df.index,
    )


def fit_novelty_ddd(sample: pd.DataFrame, pf) -> dict[str, float]:
    df = sample.copy()
    df["post_X_treated"] = df["post"] * df["treated"]
    df["post_X_disp"] = df["post"] * df["disp_binary"]
    df["post_X_treated_X_disp"] = (
        df["post"] * df["treated"] * df["disp_binary"]
    )
    fit = pf.feols(
        (
            "variety_seeking ~ post_X_treated + post_X_disp + "
            "post_X_treated_X_disp | event_fe_id + rel_t + calendar_month"
        ),
        data=df,
        vcov={"CRV1": "closure_event_id"},
    )
    tidy = fit.tidy()
    ddd = tidy.loc["post_X_treated_X_disp"]
    low = tidy.loc["post_X_treated"]
    return {
        "coef": float(ddd["Estimate"]),
        "se": float(ddd["Std. Error"]),
        "t_stat": float(ddd["t value"]),
        "p_value": float(ddd["Pr(>|t|)"]),
        "ci_low": float(ddd["2.5%"]),
        "ci_high": float(ddd["97.5%"]),
        "low_group_coef": float(low["Estimate"]),
        "n_obs": int(fit._N),
    }


def select_result(
    results: pd.DataFrame,
    *,
    include_lny: bool,
    rate_cutoff: float,
    max_duration: int,
    min_group: int,
) -> pd.Series:
    row = results[
        (results["include_lny"] == include_lny)
        & (results["rate_ratio_cutoff"] == rate_cutoff)
        & (results["max_closure_duration_days"] == max_duration)
        & (results["minimum_members_each_arm"] == min_group)
    ]
    if len(row) != 1:
        raise RuntimeError(f"Could not select one comparison row; found {len(row)}")
    return row.iloc[0]


def configure_imports(project_root: Path):
    dc_dir = project_root / "src/displacement_classification"
    cs_dir = project_root / "src/customer-store"
    effect_dir = project_root / "src/displacement_effect_estimation"
    sys.path.insert(0, str(effect_dir))
    sys.path.insert(0, str(cs_dir))
    sys.path.insert(0, str(dc_dir))

    import data_loading_feature_constructing as dl
    from model import check_gpu, save_model_artifacts

    return dl, check_gpu, save_model_artifacts


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Train the missing duration-25 displacement classifier and build "
            "the 29-closure novelty-seeking sensitivity bundle."
        )
    )
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--candidate-registry", type=Path, required=True)
    parser.add_argument("--added6-dir", type=Path, required=True)
    parser.add_argument("--broad-push-cache", type=Path, required=True)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/06_sample_sensitivity/29_closures"),
    )
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    output_dir = (
        args.output_dir
        if args.output_dir.is_absolute()
        else project_root / args.output_dir
    ).resolve()
    classifier_dir = output_dir / "duration25_classifier"
    cache_dir = output_dir / "feature_cache"
    log_dir = classifier_dir / "logs"
    for path in (output_dir, classifier_dir, cache_dir, log_dir):
        path.mkdir(parents=True, exist_ok=True)

    before_status = subprocess.check_output(
        ["git", "-C", str(project_root), "status", "--short"],
        text=True,
    )
    (output_dir / "git_status_before.txt").write_text(
        before_status, encoding="utf-8"
    )

    dl, check_gpu, save_model_artifacts = configure_imports(project_root)
    dl.PAIR_REGISTRY_CSV = classifier_dir / "closure_registry_duration25.csv"
    dl.OUTPUT_DIR = classifier_dir
    dl.LOG_DIR = log_dir
    dl.LOG_FILE = log_dir / "duration25_training.log"
    dl.DEMO_INTERMEDIATE_DIR = classifier_dir / "demographic_intermediate"
    dl.DEMO_INTERMEDIATE_DIR.mkdir(parents=True, exist_ok=True)
    logger = dl.setup_logging()

    candidates = pd.read_csv(
        args.candidate_registry.resolve(), encoding="utf-8-sig"
    )
    candidates["closure_start"] = pd.to_datetime(
        candidates["closure_start"]
    ).dt.strftime("%Y-%m-%d")
    candidates["event_key"] = event_keys(candidates)
    candidates["rate_ratio"] = (
        candidates["control_purchase_rate_during"]
        / candidates["treatment_purchase_rate_during"]
    )

    scope32 = candidates[
        (candidates["n_treatment"] >= 5)
        & (candidates["n_control"] >= 5)
        & candidates["control_purchase_rate_during"].notna()
        & candidates["treatment_purchase_rate_during"].notna()
    ].copy()
    if len(scope32) != 32:
        raise RuntimeError(f"Expected 32 broad-scope events, got {len(scope32)}")

    duration25_registry = candidates[
        candidates["event_key"] == DURATION25_KEY
    ].copy()
    if len(duration25_registry) != 1:
        raise RuntimeError(
            f"Expected one duration-25 registry row, got {len(duration25_registry)}"
        )
    duration25_registry["status"] = "kept"
    duration25_registry["skip_reason"] = ""
    duration25_registry.drop(columns=["event_key"]).to_csv(
        dl.PAIR_REGISTRY_CSV, index=False
    )

    registry29 = candidates[
        (candidates["n_treatment"] >= 50)
        & (candidates["n_control"] >= 50)
        & candidates["control_purchase_rate_during"].notna()
        & candidates["treatment_purchase_rate_during"].notna()
        & (candidates["event_key"] != INSUFFICIENT_HISTORY_KEY)
    ].copy()
    if len(registry29) != 29:
        raise RuntimeError(f"Expected 29 analysis events, got {len(registry29)}")
    registry29["status"] = "kept"
    registry29["skip_reason"] = ""
    registry29_path = output_dir / "closure_registry_29.csv"
    registry29.drop(columns=["event_key"]).to_csv(registry29_path, index=False)

    closures = pd.read_csv(dl.CLOSURES_CSV, encoding="utf-8-sig")
    closures["closure_start"] = pd.to_datetime(
        closures["closure_start"]
    ).dt.strftime("%Y-%m-%d")
    closures["event_key"] = event_keys(closures)
    closures = closures[
        closures["event_key"].isin(set(scope32["event_key"]))
    ].drop(columns=["event_key"])
    if len(closures) != 32:
        raise RuntimeError(f"Expected 32 closure rows, got {len(closures)}")

    logger.info("Loading source data for duration-25 classifier")
    df_order_full = dl.load_order_result_full(logger)
    no_push_ids = dl.load_no_push_ids()
    member_demographics = dl.load_member_demographics(logger, no_push_ids)
    customer_preference = dl.get_customer_store_preference(
        df_order_full, lowest_purchases=dl.DEFAULT_LOWEST_PURCHASES
    )
    unique_visits = df_order_full[
        ["member_id", "date", "dept_id"]
    ].drop_duplicates()

    training_panel = dl.build_training_panel(
        logger,
        df_order_full,
        closures,
        customer_preference,
        unique_visits,
    )
    t0_panel = dl.build_t0_ex_ante_panel(
        logger,
        df_order_full,
        closures,
        customer_preference,
        unique_visits,
    )
    for name, panel in (
        ("training", training_panel),
        ("t0", t0_panel),
    ):
        keys = set(event_keys(panel))
        if keys != {DURATION25_KEY}:
            raise RuntimeError(
                f"{name} panel has unexpected event keys: {sorted(keys)}"
            )

    members = set(
        pd.concat(
            [training_panel["member_id"], t0_panel["member_id"]],
            ignore_index=True,
        )
        .astype(int)
        .unique()
    )
    df_order_members = df_order_full[
        df_order_full["member_id"].isin(members)
    ].copy()

    filtered_push_path = classifier_dir / "push_events_duration25.parquet"
    if filtered_push_path.exists():
        df_push = pd.read_parquet(filtered_push_path)
        logger.info(
            "Loaded saved duration-25 push cache: %s rows",
            f"{len(df_push):,}",
        )
    else:
        broad_push = pd.read_parquet(args.broad_push_cache.resolve())
        df_push = broad_push[broad_push["member_id"].isin(members)].copy()
        df_push.to_parquet(filtered_push_path, index=False)
        logger.info(
            "Saved duration-25 push cache: %s rows",
            f"{len(df_push):,}",
        )

    training_features = dl.compute_features_for_panel(
        logger,
        training_panel,
        df_order_members,
        member_demographics,
        df_push_events=df_push,
    )
    t0_features = dl.compute_features_for_panel(
        logger,
        t0_panel,
        df_order_members,
        member_demographics,
        df_push_events=df_push,
    )
    training_features.to_parquet(
        classifier_dir / "features_training_25.parquet", index=False
    )
    t0_features.to_parquet(
        classifier_dir / "features_t0_25.parquet", index=False
    )

    push_validation = {
        "training_rows": int(len(training_features)),
        "t0_rows": int(len(t0_features)),
        "training_mean_n_push_28d": float(
            training_features["n_push_28d"].mean()
        ),
        "t0_mean_n_push_28d": float(t0_features["n_push_28d"].mean()),
        "t0_share_positive_n_push_28d": float(
            (t0_features["n_push_28d"] > 0).mean()
        ),
    }
    if (
        push_validation["training_mean_n_push_28d"] <= 0
        or push_validation["t0_mean_n_push_28d"] <= 0
    ):
        raise RuntimeError(f"Push feature validation failed: {push_validation}")
    (classifier_dir / "push_feature_validation.json").write_text(
        json.dumps(push_validation, indent=2) + "\n", encoding="utf-8"
    )

    exclude = {
        "member_id",
        "dept_id",
        "closure_start",
        "closure_end",
        "period",
        "group",
        "label",
        "is_treated",
        "period_start",
        "period_end",
        "closure_length_days",
        "closure_duration_days",
        "closure_start_month",
        "closure_start_weekday",
        "closure_start_season",
        "share_visited_stores_closed",
        "tenure_days",
    }
    feature_cols = [
        c
        for c in training_features.columns
        if c not in exclude
        and pd.api.types.is_numeric_dtype(training_features[c])
    ]

    train_df = training_features[training_features["period"] <= -2].copy()
    eval_pre = training_features[training_features["period"] == -1].copy()
    eval_during = training_features[
        (training_features["period"] == 0)
        & (training_features["group"] == "control")
    ].copy()
    if len(train_df) != 7203:
        raise RuntimeError(
            f"Expected 7,203 duration-25 training rows, got {len(train_df)}"
        )

    import xgboost as xgb

    cfg_model = dl.CONFIG["model"]
    use_gpu = check_gpu()
    params = {
        **cfg_model["xgb_params"],
        "device": "cuda" if use_gpu else "cpu",
        "n_jobs": 1 if use_gpu else -1,
    }
    logger.info(
        "Training duration-25 model: train=%s eval_pre=%s eval_during=%s gpu=%s",
        f"{len(train_df):,}",
        f"{len(eval_pre):,}",
        f"{len(eval_during):,}",
        use_gpu,
    )
    model = xgb.train(
        params,
        xgb.DMatrix(
            train_df[feature_cols].copy(),
            label=train_df["label"].to_numpy(),
            feature_names=feature_cols,
        ),
        num_boost_round=cfg_model["num_boost_round"],
    )

    production_model_dir = (
        project_root / "outputs/displacement_classification"
    )
    save_model_artifacts(
        model=model,
        features_df=training_features,
        feature_cols=feature_cols,
        eval_pre=eval_pre,
        eval_during=eval_during,
        output_dir=production_model_dir,
        logger=logger,
        model_suffix="25",
    )

    t0_pred = model.predict(
        xgb.DMatrix(
            t0_features[feature_cols].copy(),
            feature_names=feature_cols,
        )
    )
    t0_scores25 = t0_features[
        [
            "member_id",
            "dept_id",
            "closure_start",
            "closure_end",
            "closure_duration_days",
            "group",
            "is_treated",
            "score_time",
        ]
    ].copy()
    t0_scores25["displacement_prob_t0_ex_ante"] = t0_pred
    threshold = float(cfg_model.get("decision_threshold", 0.5))
    t0_scores25["predicted_displaced_t0_ex_ante"] = (
        t0_pred >= threshold
    ).astype(int)
    production_t0_path = (
        production_model_dir / "displacement_scores_t0_ex_ante_25.csv"
    )
    t0_scores25.to_csv(production_t0_path, index=False)
    t0_scores25.to_csv(
        classifier_dir / "displacement_scores_t0_ex_ante_25.csv",
        index=False,
    )

    for name in (
        "displacement_model_25.json",
        "variable_importance_25.csv",
        "prediction_accuracy_25.csv",
        "panel_with_scores_25.parquet",
        "displacement_scores_25.csv",
    ):
        shutil.copy2(production_model_dir / name, classifier_dir / name)

    old_scores = pd.read_csv(
        production_model_dir / "displacement_scores_t0_ex_ante.csv",
        encoding="utf-8-sig",
    )
    added6_scores = pd.read_csv(
        args.added6_dir.resolve() / "displacement_scores_added6.csv",
        encoding="utf-8-sig",
    )
    combined_scores = pd.concat(
        [old_scores, added6_scores, t0_scores25],
        ignore_index=True,
    )
    score_keys = ["member_id", "dept_id", "closure_start"]
    if combined_scores.duplicated(score_keys).any():
        raise RuntimeError("Combined 29-event score file has duplicate keys")
    combined_scores_path = output_dir / "displacement_scores_29.csv"
    combined_scores.to_csv(combined_scores_path, index=False)

    effect_dir = project_root / "src/displacement_effect_estimation"
    sys.path.insert(0, str(effect_dir))
    import data as effect_data

    effect_cfg = effect_data.load_config()
    production_feature_dir = (
        project_root / effect_cfg["paths"]["feature_t0_cache_dir"]
    ).resolve()
    production_feature_path = production_feature_dir / (
        f"features_t0_{effect_cfg['paths']['feature_cache_key']}.parquet"
    )
    recency_cols = [
        "member_id",
        "dept_id",
        "closure_start",
        "period",
        "days_since_last_purchase",
    ]
    recency29 = pd.concat(
        [
            pd.read_parquet(production_feature_path, columns=recency_cols),
            pd.read_parquet(
                args.added6_dir.resolve() / "features_t0_added6.parquet",
                columns=recency_cols,
            ),
            t0_features[recency_cols].copy(),
        ],
        ignore_index=True,
    )
    recency_keys = [
        "member_id",
        "dept_id",
        "closure_start",
        "period",
    ]
    if recency29.duplicated(recency_keys).any():
        raise RuntimeError("Combined 29-event recency cache has duplicate keys")
    feature_key = "sample29"
    recency29.to_parquet(
        cache_dir / f"features_t0_{feature_key}.parquet", index=False
    )

    effect_cfg["paths"]["score_file"] = str(combined_scores_path)
    effect_cfg["paths"]["feature_t0_cache_dir"] = str(cache_dir)
    effect_cfg["paths"]["feature_cache_key"] = feature_key
    os.environ["DISPLACEMENT_EFFECT_CLOSURE_REGISTRY"] = str(
        registry29_path
    )
    novelty_sample = effect_data.build_estimation_sample(
        outcome="variety_seeking",
        cfg=effect_cfg,
        t_horizon=4,
        closure_duration_days=False,
        separate_effect=False,
        select_recency_consumers=False,
        require_balanced_panel=False,
        variety_seeking_mode="distinct",
        drop_period0_purchasers=False,
        unbalanced_panel=True,
        variety_pre_novelty_heterogeneity=False,
        customer_median_split=True,
    )
    novelty_sample.to_parquet(
        output_dir / "novelty_estimation_sample_29.parquet",
        index=False,
    )
    novelty_sample["closure_start"] = pd.to_datetime(
        novelty_sample["closure_start"]
    ).dt.strftime("%Y-%m-%d")
    novelty_sample["event_key"] = event_keys(novelty_sample)

    import pyfixest as pf

    rule_rows = []
    membership_rows = []
    result_rows = []
    fit_cache: dict[tuple[tuple[int, str], ...], dict[str, float]] = {}
    for include_lny, rate_cutoff, max_duration, min_group in product(
        [False, True],
        [0.0, 1.5, 2.0],
        [21, 29],
        [50, 100],
    ):
        rule_id = (
            f"lny_{'in' if include_lny else 'out'}"
            f"__rate_ge_{rate_cutoff:g}"
            f"__duration_le_{max_duration}"
            f"__groups_ge_{min_group}"
        )
        eligible = registry29[
            (registry29["closure_duration_days"] <= max_duration)
            & (registry29["n_treatment"] >= min_group)
            & (registry29["n_control"] >= min_group)
        ].copy()
        if rate_cutoff > 0:
            eligible = eligible[
                eligible["rate_ratio"] >= rate_cutoff
            ].copy()
        if not include_lny:
            eligible = eligible[
                ~eligible["event_key"].isin(LNY_KEYS)
            ].copy()
        keys = tuple(sorted(eligible["event_key"].tolist()))
        rule_rows.append(
            {
                "rule_id": rule_id,
                "include_lny": include_lny,
                "rate_ratio_cutoff": rate_cutoff,
                "max_closure_duration_days": max_duration,
                "minimum_members_each_arm": min_group,
                "n_events": len(keys),
            }
        )
        for dept_id, closure_start in keys:
            membership_rows.append(
                {
                    "rule_id": rule_id,
                    "dept_id": dept_id,
                    "closure_start": closure_start,
                }
            )
        if keys not in fit_cache:
            fit_cache[keys] = fit_novelty_ddd(
                novelty_sample[
                    novelty_sample["event_key"].isin(keys)
                ].copy(),
                pf,
            )
        result_rows.append(
            {
                "rule_id": rule_id,
                "n_events": len(keys),
                "status": "fit",
                **fit_cache[keys],
            }
        )

    rules = pd.DataFrame(rule_rows)
    results = pd.DataFrame(result_rows).merge(
        rules.drop(columns=["n_events"]), on="rule_id", how="left"
    )
    results = results.sort_values(["p_value", "n_events"])
    rules.to_csv(output_dir / "rule_definitions_29.csv", index=False)
    pd.DataFrame(membership_rows).to_csv(
        output_dir / "event_membership_29.csv", index=False
    )
    results.to_csv(output_dir / "novelty_results_29_grid.csv", index=False)

    previous_results = pd.read_csv(
        args.added6_dir.resolve().parent / "novelty_results_incremental28.csv"
    )
    comparison_specs = [
        (
            "Current main: ratio >= 2, LNY excluded",
            previous_results,
            False,
            2.0,
        ),
        (
            "Current full: ratio >= 2, LNY included",
            previous_results,
            True,
            2.0,
        ),
        (
            "No rate screen, LNY excluded, duration 25 omitted",
            previous_results,
            False,
            0.0,
        ),
        (
            "No rate screen, LNY included, duration 25 omitted",
            previous_results,
            True,
            0.0,
        ),
        (
            "No rate screen, LNY excluded, duration 25 included",
            results,
            False,
            0.0,
        ),
        (
            "No rate screen, LNY included, duration 25 included",
            results,
            True,
            0.0,
        ),
    ]
    comparison_rows = []
    for label, source, include_lny, rate_cutoff in comparison_specs:
        row = select_result(
            source,
            include_lny=include_lny,
            rate_cutoff=rate_cutoff,
            max_duration=29,
            min_group=50,
        )
        comparison_rows.append(
            {
                "sample": label,
                "n_events": int(row["n_events"]),
                "coef": float(row["coef"]),
                "se": float(row["se"]),
                "p_value": float(row["p_value"]),
                "ci_low": float(row["ci_low"]),
                "ci_high": float(row["ci_high"]),
                "n_obs": int(row["n_obs"]),
            }
        )
    comparison = pd.DataFrame(comparison_rows)
    comparison.to_csv(
        output_dir / "novelty_key_sample_comparison.csv", index=False
    )

    metadata = {
        "duration25_event": list(DURATION25_KEY),
        "analysis_event_count": 29,
        "insufficient_history_event_dropped": list(
            INSUFFICIENT_HISTORY_KEY
        ),
        "cluster": "closure_event_id",
        "fixed_effects": [
            "event_fe_id",
            "rel_t",
            "calendar_month",
        ],
        "classifier_training_rows": int(len(train_df)),
        "classifier_t0_rows": int(len(t0_features)),
        "push_validation": push_validation,
        "git_commit": subprocess.check_output(
            ["git", "-C", str(project_root), "rev-parse", "HEAD"],
            text=True,
        ).strip(),
        "pandas_timestamp_fix": (
            "push_event_cache.py uses Timestamp.value nanoseconds"
        ),
        "production_model_path": str(
            production_model_dir / "displacement_model_25.json"
        ),
    }
    (output_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    (output_dir / "README.md").write_text(
        "# Duration-25 classifier and 29-closure novelty sensitivity\n\n"
        "This bundle trains the missing duration-25 classifier using the "
        "production feature and model specification, combines it with the "
        "unchanged production 22-event scores and six previously scored "
        "low-rate events, and estimates the novelty-seeking DDD with standard "
        "errors clustered by closure event.\n\n"
        "Use `novelty_key_sample_comparison.csv` for the headline comparison "
        "and `novelty_results_29_grid.csv` for the complete rule grid.\n",
        encoding="utf-8",
    )

    after_status = subprocess.check_output(
        ["git", "-C", str(project_root), "status", "--short"],
        text=True,
    )
    (output_dir / "git_status_after.txt").write_text(
        after_status, encoding="utf-8"
    )
    print(comparison.to_string(index=False))
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
