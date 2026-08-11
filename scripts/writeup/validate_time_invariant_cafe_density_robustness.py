#!/usr/bin/env python3
"""Independently validate the time-invariant cafe-density robustness bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Optional

import matplotlib

matplotlib.use("Agg")
import matplotlib.image as mpimg
import numpy as np
import pandas as pd


RAW_500 = "cafe_count_500m"
RAW_1500 = "cafe_count_1500m"
FIELD_500 = "半径500m内店铺数(咖啡厅)"
FIELD_1500 = "半径1500m内店铺数(咖啡厅)"
CLUSTER = "closure_event_id"
EXPECTED_DENSITY_HASH = "361267209af83070d247aaa4b28d0d97e24654165089332566835673715419de"
EXPECTED_ORDER_HASH = "01eb80ae13cd8e1bb68e6ab3496ee32492795d84b13e0b374bd31c5209dbd74b"
EXPECTED_MEMBER_FIRST_HASH = "2fd0449e995618580a5da0645e68dbc52fedda4471fd9e4aae386083c39580e3"
EXPECTED_MARKET_NEW_HASH = "ce84c6d6a508e9e538d4f84a8cfcd159ac510cd4c08f4d5770226d0ccd3f1ac4"
EXPECTED_DENSITY_TERMS = {
    "post_X_treated",
    "post_X_disp",
    "post_X_treated_X_disp",
    "post_X_density",
    "post_X_treated_X_density",
    "post_X_disp_X_density",
    "post_X_treated_X_disp_X_density",
}


def parse_args() -> argparse.Namespace:
    root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=root)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/05_robustness/time_invariant_cafe_density"),
    )
    parser.add_argument(
        "--density-source",
        type=Path,
        default=Path("../data/data1031/dapt_id_address.csv"),
    )
    parser.add_argument(
        "--order-source",
        type=Path,
        default=Path("../data/data1031/order_result.csv"),
    )
    return parser.parse_args()


def resolve(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


def resolve_input(root: Path, path: Path, verified_local_copy: Path) -> Path:
    candidate = resolve(root, path)
    if candidate.exists():
        return candidate
    if not path.is_absolute() and verified_local_copy.exists():
        return verified_local_copy
    return candidate


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            block = handle.read(1024 * 1024)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def normalized_address(value: Any) -> str:
    text = unicodedata.normalize("NFKC", str(value)).strip()
    if text.startswith("南京市"):
        text = text[3:]
    for token in [" ", "\t", "\r", "\n", ",", "，", "。"]:
        text = text.replace(token, "")
    return text


def main() -> None:
    args = parse_args()
    root = args.project_root.resolve()
    output = resolve(root, args.output_dir)
    density_source = resolve_input(
        root,
        args.density_source,
        Path("/private/tmp/coffee_cafe_density_dapt_id_address.csv"),
    )
    order_source = resolve_input(
        root,
        args.order_source,
        Path("/private/tmp/coffee_cafe_density_order_result.csv"),
    )
    validations: List[Dict[str, Any]] = []

    def check(category: str, name: str, passed: bool, observed: Any, expected: Any) -> None:
        validations.append(
            {
                "category": category,
                "check": name,
                "passed": bool(passed),
                "observed": str(observed),
                "expected": str(expected),
            }
        )

    required_files = [
        "run_metadata.json",
        "validation_checks.csv",
        "summary.md",
        "main_table.csv",
        "main_table.md",
        "member_event_preferred_store_density.csv",
        "member_first_regression_episode_density.csv",
        "market_new_regression_episode_density.csv",
        "design_store_density.csv",
        "store_density_balance.csv",
        "density_common_support.csv",
        "matched_set_density.csv",
        "model_estimands.csv",
        "model_coefficients.csv",
        "model_covariance_long.csv",
        "model_specifications.csv",
        "wild_cluster_bootstrap.csv",
        "leave_one_closure_out.csv",
        "density_interacted_event_study_500m.csv",
        "preferred_store_event_period_fe_event_study.csv",
        "event_study_joint_tests.csv",
        "store_event_period_cell_support.csv",
        "store_event_period_support_summary.csv",
        "low_density_incidence_support.csv",
        "low_density_support.json",
        "stability_benchmark.csv",
        "market_new_outcome_sensitivity.csv",
        "fitted_ddd_curve_500m.csv",
        "fitted_ddd_curve_1500m.csv",
        "store_density_ecdf_500m.png",
        "fitted_ddd_500m.png",
        "fitted_ddd_1500m.png",
        "density_interacted_event_study_500m.png",
    ]
    for filename in required_files:
        path = output / filename
        check("artifact", f"{filename} exists and is nonempty", path.exists() and path.stat().st_size > 0, path.stat().st_size if path.exists() else 0, "> 0 bytes")

    if not all((output / name).exists() for name in required_files):
        report = pd.DataFrame(validations)
        output.mkdir(parents=True, exist_ok=True)
        report.to_csv(output / "validation_results.csv", index=False)
        raise SystemExit("Required output files are missing; see validation_results.csv")

    metadata = json.loads((output / "run_metadata.json").read_text(encoding="utf-8"))
    estimator_checks = pd.read_csv(output / "validation_checks.csv")
    check(
        "upstream",
        "all estimator assertions passed",
        bool(estimator_checks["passed"].astype(bool).all()),
        int(estimator_checks["passed"].astype(bool).sum()),
        len(estimator_checks),
    )

    source_hash = sha256(density_source)
    order_hash = sha256(order_source)
    member_first_sample = root / "outputs/03_main_18_closures/novelty_member_first_ddd_h4/estimation_sample.csv"
    market_new_sample = root / "outputs/03_main_18_closures/novelty_market_new_ddd_h4/estimation_sample.csv"
    check("source", "density SHA-256", source_hash == EXPECTED_DENSITY_HASH, source_hash, EXPECTED_DENSITY_HASH)
    check("source", "order SHA-256", order_hash == EXPECTED_ORDER_HASH, order_hash, EXPECTED_ORDER_HASH)
    check("source", "member-first sample SHA-256", sha256(member_first_sample) == EXPECTED_MEMBER_FIRST_HASH, sha256(member_first_sample), EXPECTED_MEMBER_FIRST_HASH)
    check("source", "market-new sample SHA-256", sha256(market_new_sample) == EXPECTED_MARKET_NEW_HASH, sha256(market_new_sample), EXPECTED_MARKET_NEW_HASH)

    raw = pd.read_csv(density_source, encoding="gb18030").rename(
        columns={FIELD_500: RAW_500, FIELD_1500: RAW_1500}
    )
    raw["dept_id"] = pd.to_numeric(raw["dept_id"], errors="raise").astype(int)
    check("source", "raw source has 260 unique stores", len(raw) == 260 and raw["dept_id"].nunique() == 260, (len(raw), raw["dept_id"].nunique()), (260, 260))
    check("source", "raw counts complete", not raw[[RAW_500, RAW_1500]].isna().any().any(), int(raw[[RAW_500, RAW_1500]].isna().sum().sum()), 0)
    check("source", "raw counts ordered by radius", bool((raw[RAW_500] <= raw[RAW_1500]).all()), int((raw[RAW_500] > raw[RAW_1500]).sum()), 0)
    mirror = pd.read_csv(root / "outputs/nanjing_store_locations/nanjing_stores_geocoded.csv", encoding="utf-8-sig").rename(
        columns={FIELD_500: RAW_500, FIELD_1500: RAW_1500}
    )
    mirror["dept_id"] = pd.to_numeric(mirror["dept_id"], errors="raise").astype(int)
    mirror_check = raw[["dept_id", RAW_500, RAW_1500]].merge(
        mirror[["dept_id", RAW_500, RAW_1500]],
        on="dept_id",
        suffixes=("_raw", "_mirror"),
        validate="one_to_one",
    )
    mirror_equal = bool(
        len(mirror_check) == 260
        and mirror_check[f"{RAW_500}_raw"].eq(mirror_check[f"{RAW_500}_mirror"]).all()
        and mirror_check[f"{RAW_1500}_raw"].eq(mirror_check[f"{RAW_1500}_mirror"]).all()
    )
    check("source", "UTF-8 mirror matches raw counts", mirror_equal, mirror_equal, True)

    design = pd.read_csv(output / "design_store_density.csv")
    check("join", "design has 108 distinct stores", len(design) == 108 and design["dept_id"].nunique() == 108, (len(design), design["dept_id"].nunique()), (108, 108))
    check("join", "design roles are 18 treated and 90 control", design["store_role"].value_counts().to_dict() == {"control": 90, "treated": 18}, design["store_role"].value_counts().to_dict(), {"treated": 18, "control": 90})
    design_raw = design.merge(
        raw[["dept_id", "address", RAW_500, RAW_1500]],
        on="dept_id",
        suffixes=("_output", "_raw"),
        validate="one_to_one",
    )
    count_equal = bool(
        design_raw[f"{RAW_500}_output"].eq(design_raw[f"{RAW_500}_raw"]).all()
        and design_raw[f"{RAW_1500}_output"].eq(design_raw[f"{RAW_1500}_raw"]).all()
    )
    check("join", "design counts match authoritative raw source", count_equal, count_equal, True)

    registry = pd.read_csv(root / "outputs/customer-store/closure_pair_registry.csv", encoding="utf-8-sig")
    registry = registry.loc[registry["status"].eq("kept")].copy()
    expected_addresses: Dict[int, str] = {}
    for row in registry.itertuples(index=False):
        expected_addresses[int(row.dept_id)] = normalized_address(row.treated_store_address)
        controls = [int(value) for value in str(row.control_store_ids).split("|")]
        addresses = str(row.control_store_addresses).split("|")
        for store, address in zip(controls, addresses):
            expected_addresses[store] = normalized_address(address)
    raw_address_map = raw.set_index("dept_id")["address"].map(normalized_address).to_dict()
    bad_addresses = [store for store, address in expected_addresses.items() if raw_address_map.get(store) != address]
    check("join", "normalized design-store addresses match registry", not bad_addresses, bad_addresses[:10], [])

    episodes = pd.read_csv(output / "member_event_preferred_store_density.csv")
    check("preference", "one row per 40,148 member-event", len(episodes) == 40148 and episodes["event_fe_id"].nunique() == 40148, (len(episodes), episodes["event_fe_id"].nunique()), (40148, 40148))
    check("preference", "one event per member", episodes["member_id"].nunique() == 40148, episodes["member_id"].nunique(), 40148)
    check("preference", "five-day eligibility", bool(episodes["total_purchases"].ge(5).all()), episodes["total_purchases"].min(), 5)
    check("preference", "80-percent eligibility", bool(episodes["preferred_ratio"].ge(0.8 - 1e-12).all()), episodes["preferred_ratio"].min(), 0.8)
    treated_ok = episodes.loc[episodes["treated"].eq(1), "preferred_store"].astype(int).eq(
        episodes.loc[episodes["treated"].eq(1), "dept_id"].astype(int)
    )
    check("preference", "treated preferences equal closure store", bool(treated_ok.all()), int((~treated_ok).sum()), 0)
    control_map: Dict[str, set] = {}
    registry["closure_start"] = pd.to_datetime(registry["closure_start"]).dt.strftime("%Y-%m-%d")
    for row in registry.itertuples(index=False):
        key = f"dept_{int(row.dept_id)}_closure_{row.closure_start}"
        control_map[key] = {int(value) for value in str(row.control_store_ids).split("|")}
    controls = episodes.loc[episodes["treated"].eq(0)]
    control_ok = controls.apply(lambda row: int(row.preferred_store) in control_map[row.closure_event_id], axis=1)
    check("preference", "control preferences belong to matched control sets", bool(control_ok.all()), int((~control_ok).sum()), 0)
    wrong_direct_merge_detectable = int((controls["preferred_store"].astype(int) != controls["dept_id"].astype(int)).sum())
    check("preference", "control panel dept_id is not used as preferred store", wrong_direct_merge_detectable > 0, wrong_direct_merge_detectable, "> 0 differing control episodes")
    raw_counts = raw.set_index("dept_id")[[RAW_500, RAW_1500]]
    joined_counts = episodes[["preferred_store", RAW_500, RAW_1500]].join(raw_counts, on="preferred_store", rsuffix="_raw")
    episode_counts_equal = bool(
        joined_counts[RAW_500].eq(joined_counts[f"{RAW_500}_raw"]).all()
        and joined_counts[RAW_1500].eq(joined_counts[f"{RAW_1500}_raw"]).all()
    )
    check("preference", "episode counts match raw source through preferred_store", episode_counts_equal, episode_counts_equal, True)

    primary_panel = pd.read_csv(member_first_sample)
    primary_remerge = primary_panel.merge(
        episodes[["event_fe_id", "preferred_store", RAW_500, RAW_1500]],
        on="event_fe_id",
        how="left",
        validate="many_to_one",
    )
    check("join", "preference merge preserves primary row count", len(primary_remerge) == len(primary_panel), len(primary_remerge), len(primary_panel))
    check("join", "preference merge preserves primary outcome missingness", primary_remerge["variety_seeking"].isna().sum() == primary_panel["variety_seeking"].isna().sum(), primary_remerge["variety_seeking"].isna().sum(), primary_panel["variety_seeking"].isna().sum())
    check("join", "all primary panel rows receive counts", not primary_remerge[[RAW_500, RAW_1500]].isna().any().any(), int(primary_remerge[[RAW_500, RAW_1500]].isna().sum().sum()), 0)

    primary_episode = pd.read_csv(output / "member_first_regression_episode_density.csv")
    check("population", "primary regression population has 23,363 member-events", len(primary_episode) == 23363 and primary_episode["event_fe_id"].nunique() == 23363, (len(primary_episode), primary_episode["event_fe_id"].nunique()), (23363, 23363))
    check("population", "primary population has 18 clusters", primary_episode[CLUSTER].nunique() == 18, primary_episode[CLUSTER].nunique(), 18)
    transforms = metadata["density_standardization"]
    transform_columns = {
        "raw_500m_interaction": (RAW_500, "density_z_raw_500m", False),
        "log_500m_interaction": (RAW_500, "density_z_log_500m", True),
        "raw_1500m_interaction": (RAW_1500, "density_z_raw_1500m", False),
        "log_1500m_interaction": (RAW_1500, "density_z_log_1500m", True),
    }
    for spec, (raw_column, z_column, log_transform) in transform_columns.items():
        values = np.log1p(primary_episode[raw_column]) if log_transform else primary_episode[raw_column].astype(float)
        mean = float(values.mean())
        sd = float(values.std(ddof=0))
        expected_z = (values - mean) / sd
        check("transform", f"{spec} mean metadata", abs(mean - transforms[spec]["mean"]) < 1e-12, mean, transforms[spec]["mean"])
        check("transform", f"{spec} SD metadata", abs(sd - transforms[spec]["sd_population_ddof0"]) < 1e-12, sd, transforms[spec]["sd_population_ddof0"])
        check("transform", f"{spec} standardized values", np.allclose(expected_z, primary_episode[z_column], atol=1e-12), float(np.max(np.abs(expected_z - primary_episode[z_column]))), "<= 1e-12")

    specs = pd.read_csv(output / "model_specifications.csv")
    check("specification", "all regressions are unweighted", specs["weights"].eq("none").all(), specs["weights"].unique().tolist(), ["none"])
    primary_spec = specs.loc[specs["spec"].eq("raw_500m_interaction")].iloc[0]
    primary_terms = set(str(primary_spec["regressors"]).split(" + "))
    check("specification", "primary interaction hierarchy is complete", primary_terms == EXPECTED_DENSITY_TERMS, sorted(primary_terms), sorted(EXPECTED_DENSITY_TERMS))
    check("specification", "primary fixed effects preserved", primary_spec["fixed_effects"] == "event_fe_id + rel_t + calendar_month", primary_spec["fixed_effects"], "event_fe_id + rel_t + calendar_month")
    check("specification", "primary clusters by closure event", primary_spec["cluster"] == CLUSTER, primary_spec["cluster"], CLUSTER)
    store_spec = specs.loc[specs["spec"].eq("preferred_store_event_post_fe")].iloc[0]
    check("specification", "collapsed local-shock FE included", "preferred_store_event_post_fe" in store_spec["fixed_effects"], store_spec["fixed_effects"], "contains preferred_store_event_post_fe")
    check("specification", "treated-post omitted when absorbed", "post_X_treated" not in str(store_spec["regressors"]).split(" + "), store_spec["regressors"], "post_X_treated omitted")

    estimands = pd.read_csv(output / "model_estimands.csv")
    coefficients = pd.read_csv(output / "model_coefficients.csv")
    covariance_long = pd.read_csv(output / "model_covariance_long.csv")
    published_primary = pd.read_csv(root / "outputs/03_main_18_closures/novelty_member_first_ddd_h4/ddd_binary_results.csv")
    published_primary = published_primary.loc[published_primary["estimand"].eq("high_minus_low_ddd")].iloc[0]
    estimated_baseline = estimands.loc[(estimands["spec"].eq("paper_facing_baseline")) & estimands["estimand"].eq("high_minus_low_ddd")].iloc[0]
    check("reproduction", "primary baseline coefficient", abs(estimated_baseline["estimate"] - published_primary["coef"]) < 1e-8, estimated_baseline["estimate"], published_primary["coef"])
    check("reproduction", "primary baseline SE", abs(estimated_baseline["se"] - published_primary["se"]) < 5e-5, estimated_baseline["se"], published_primary["se"])
    published_market = pd.read_csv(root / "outputs/03_main_18_closures/novelty_market_new_ddd_h4/ddd_binary_results.csv")
    published_market = published_market.loc[published_market["estimand"].eq("high_minus_low_ddd")].iloc[0]
    estimated_market = estimands.loc[(estimands["spec"].eq("market_new_baseline")) & estimands["estimand"].eq("high_minus_low_ddd")].iloc[0]
    check("reproduction", "market-new baseline coefficient", abs(estimated_market["estimate"] - published_market["coef"]) < 1e-8, estimated_market["estimate"], published_market["coef"])
    check("reproduction", "market-new baseline SE", abs(estimated_market["se"] - published_market["se"]) < 5e-5, estimated_market["se"], published_market["se"])

    for spec in ["raw_500m_interaction", "log_500m_interaction", "raw_1500m_interaction", "log_1500m_interaction", "market_new_raw_500m_interaction"]:
        coef = coefficients.loc[coefficients["spec"].eq(spec)].set_index("term")
        cov = covariance_long.loc[covariance_long["spec"].eq(spec)].pivot(index="row_term", columns="column_term", values="covariance")
        names = list(coef.index)
        cov = cov.loc[names, names]
        check("covariance", f"{spec} covariance symmetric", np.allclose(cov.to_numpy(), cov.to_numpy().T, atol=1e-12), float(np.max(np.abs(cov.to_numpy() - cov.to_numpy().T))), "<= 1e-12")
        check("covariance", f"{spec} covariance diagonal nonnegative", bool((np.diag(cov.to_numpy()) >= -1e-14).all()), float(np.min(np.diag(cov.to_numpy()))), ">= 0")
        rows = estimands.loc[estimands["spec"].eq(spec) & estimands["estimand"].eq("fitted_ddd")]
        transform = transforms[spec]
        for row in rows.itertuples(index=False):
            raw_value = float(row.raw_count)
            transformed = math.log1p(raw_value) if transform["transformation"] == "log1p" else raw_value
            z = (transformed - transform["mean"]) / transform["sd_population_ddof0"]
            expected_estimate = float(coef.loc["post_X_treated_X_disp", "estimate"] + z * coef.loc["post_X_treated_X_disp_X_density", "estimate"])
            vector = np.zeros(len(names))
            vector[names.index("post_X_treated_X_disp")] = 1.0
            vector[names.index("post_X_treated_X_disp_X_density")] = z
            expected_se = math.sqrt(max(float(vector @ cov.to_numpy() @ vector), 0.0))
            check("marginal", f"{spec} fitted estimate at {raw_value:g}", abs(expected_estimate - row.estimate) < 1e-10, row.estimate, expected_estimate)
            check("marginal", f"{spec} covariance SE at {raw_value:g}", abs(expected_se - row.se) < 1e-10, row.se, expected_se)

    bootstrap = pd.read_csv(output / "wild_cluster_bootstrap.csv")
    check("inference", "wild bootstrap uses 9,999 repetitions", bootstrap["repetitions"].eq(9999).all(), sorted(bootstrap["repetitions"].unique()), [9999])
    check("inference", "wild bootstrap seed locked", bootstrap["seed"].eq(20260811).all(), sorted(bootstrap["seed"].unique()), [20260811])
    check("inference", "wild p-values valid", bootstrap["pvalue_wild_restricted"].between(0, 1).all(), (bootstrap["pvalue_wild_restricted"].min(), bootstrap["pvalue_wild_restricted"].max()), "within [0,1]")
    check("inference", "full-sample wild rows use 18 clusters", bootstrap.loc[~bootstrap["spec"].eq("low_density_le3_descriptive"), "closure_clusters"].eq(18).all(), sorted(bootstrap.loc[~bootstrap["spec"].eq("low_density_le3_descriptive"), "closure_clusters"].unique()), [18])

    loo = pd.read_csv(output / "leave_one_closure_out.csv")
    check("leverage", "18 closures omitted exactly once per estimand", loo["omitted_closure_event_id"].nunique() == 18 and loo.groupby("estimand").size().eq(18).all(), (loo["omitted_closure_event_id"].nunique(), loo.groupby("estimand").size().to_dict()), "18 omissions for each of 4 estimands")
    check("leverage", "LOO models have 17 clusters", loo["closure_clusters"].eq(17).all(), sorted(loo["closure_clusters"].unique()), [17])

    event = pd.read_csv(output / "density_interacted_event_study_500m.csv")
    check("dynamic", "event study has two counts and eight periods", set(event["raw_count_500m"]) == {2.0, 13.0} and set(event["rel_t"]) == {-4, -3, -2, -1, 1, 2, 3, 4}, (sorted(event["raw_count_500m"].unique()), sorted(event["rel_t"].unique())), ([2, 13], [-4, -3, -2, -1, 1, 2, 3, 4]))
    reference = event.loc[event["rel_t"].eq(-1)]
    check("dynamic", "event-study reference period normalized to zero", reference["estimate"].eq(0).all() and reference["ci_low"].eq(0).all() and reference["ci_high"].eq(0).all(), reference[["estimate", "ci_low", "ci_high"]].to_dict("records"), "all zero")
    joint = pd.read_csv(output / "event_study_joint_tests.csv")
    check("dynamic", "two prespecified joint pretests reported", len(joint) == 2 and joint["restrictions"].eq(3).all(), (len(joint), joint["restrictions"].tolist()), (2, [3, 3]))

    low = json.loads((output / "low_density_support.json").read_text(encoding="utf-8"))
    check("restricted sample", "low-density cutoff locked at 3", low["cutoff"] == 3, low["cutoff"], 3)
    check("restricted sample", "low-density design support matches audit", (low["design_stores"], low["design_treated_stores"], low["design_control_stores"]) == (42, 9, 33), (low["design_stores"], low["design_treated_stores"], low["design_control_stores"]), (42, 9, 33))
    check("restricted sample", "eight matched sets have both store roles", low["matched_sets_with_low_density_on_both_treatment_sides"] == 8, low["matched_sets_with_low_density_on_both_treatment_sides"], 8)
    check("restricted sample", "low-density estimate labelled descriptive", estimands.loc[estimands["spec"].eq("low_density_le3_descriptive")].shape[0] == 1 and "descriptive" in specs.loc[specs["spec"].eq("low_density_le3_descriptive"), "sample"].iloc[0], specs.loc[specs["spec"].eq("low_density_le3_descriptive"), "sample"].iloc[0], "contains descriptive")

    balance = pd.read_csv(output / "store_density_balance.csv")
    raw_balance = balance.loc[balance["measure"].eq(RAW_500)]
    check("support", "balance reports 18 treated and 90 controls", raw_balance.set_index("store_role")["stores"].to_dict() == {"treated": 18, "control": 90}, raw_balance.set_index("store_role")["stores"].to_dict(), {"treated": 18, "control": 90})
    common = pd.read_csv(output / "density_common_support.csv")
    support500 = common.loc[common["measure"].eq(RAW_500)].iloc[0]
    check("support", "counts 2,5,13 lie in 500m common support", all(support500["common_support_min"] <= value <= support500["common_support_max"] for value in [2, 5, 13]), (support500["common_support_min"], support500["common_support_max"]), "contains 2,5,13")
    benchmark = pd.read_csv(output / "stability_benchmark.csv")
    check("benchmark", "three locked locations evaluated", set(benchmark["location"]) == {"member_event_mean", "raw_count_2", "raw_count_13"}, sorted(benchmark["location"]), ["member_event_mean", "raw_count_2", "raw_count_13"])

    figure_names = [
        "store_density_ecdf_500m.png",
        "fitted_ddd_500m.png",
        "fitted_ddd_1500m.png",
        "density_interacted_event_study_500m.png",
    ]
    for filename in figure_names:
        image = mpimg.imread(output / filename)
        height, width = image.shape[:2]
        check("figure", f"{filename} readable and sufficiently large", width >= 1000 and height >= 800, (width, height), "width>=1000, height>=800")

    summary = (output / "summary.md").read_text(encoding="utf-8")
    required_phrases = [
        "Evidence classification: Challenging",
        "systematic pre-period warning",
        "do not directly measure other-brand competition",
        "not a measurement date",
        "descriptive",
        "market-new novelty",
        "preferred store",
    ]
    for phrase in required_phrases:
        check("narrative", f"summary contains: {phrase}", phrase in summary, phrase in summary, True)

    try:
        changed_baseline = subprocess.run(
            [
                "git", "diff", "--name-only", "--",
                "outputs/03_main_18_closures/novelty_member_first_ddd_h4",
                "outputs/03_main_18_closures/novelty_market_new_ddd_h4",
            ],
            cwd=str(root),
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except Exception as error:
        changed_baseline = f"git check unavailable: {error}"
    check("isolation", "baseline output bundles were not modified", changed_baseline == "", changed_baseline, "")
    check("isolation", "robustness outputs use separate directory", "outputs/05_robustness/time_invariant_cafe_density" in str(output), str(output), "contains outputs/05_robustness/time_invariant_cafe_density")

    validation_frame = pd.DataFrame(validations)
    validation_frame.to_csv(output / "validation_results.csv", index=False)
    failed = validation_frame.loc[~validation_frame["passed"]]
    category_summary = (
        validation_frame.groupby("category")
        .agg(checks=("check", "size"), passed=("passed", "sum"))
        .reset_index()
    )
    lines = [
        "# Independent validation report",
        "",
        f"**Overall status: {'PASS' if failed.empty else 'FAIL'}.** "
        f"{int(validation_frame['passed'].sum())} of {len(validation_frame)} checks passed.",
        "",
        "## Coverage",
        "",
        markdown_table(category_summary),
        "",
        "## Failed checks",
        "",
    ]
    if failed.empty:
        lines.append("None.")
    else:
        lines.append(markdown_table(failed[["category", "check", "observed", "expected"]]))
    lines.extend(
        [
            "",
            "## Validation scope",
            "",
            "This independent pass re-hashed authoritative inputs; rechecked source grain, design-store joins, preferred-store eligibility and control-set membership; reconstructed the panel merge; verified the complete interaction hierarchy, fixed effects, clustering, and absence of weights; recomputed covariance-based marginal effects; audited bootstrap settings, restricted-sample support, leave-one-closure diagnostics, dynamic tests, figures, narrative caveats, and output isolation.",
            "",
        ]
    )
    (output / "validation_report.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Validation: {'PASS' if failed.empty else 'FAIL'} ({int(validation_frame['passed'].sum())}/{len(validation_frame)})")
    if not failed.empty:
        print(failed[["category", "check", "observed", "expected"]].to_string(index=False))
        raise SystemExit(1)


def markdown_table(frame: pd.DataFrame) -> str:
    columns = [str(column) for column in frame.columns]
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in frame.itertuples(index=False, name=None):
        values = [str(value).replace("|", "\\|").replace("\n", " ") for value in row]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
