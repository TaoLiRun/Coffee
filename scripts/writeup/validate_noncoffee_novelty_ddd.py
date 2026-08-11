from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pyfixest as pf


SCOPES = ["all_noncoffee", "noncoffee_consumables", "noncoffee_drinks"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def add_check(checks: list[dict], name: str, passed: bool, detail: str) -> None:
    checks.append({"check": name, "passed": bool(passed), "detail": detail})


def refit_ddd(panel: pd.DataFrame, outcome: str) -> tuple[float, int]:
    work = panel.copy()
    work["post_X_treated"] = work["post"] * work["treated"]
    work["post_X_disp"] = work["post"] * work["disp_binary"]
    work["post_X_treated_X_disp"] = (
        work["post"] * work["treated"] * work["disp_binary"]
    )
    fit = pf.feols(
        f"{outcome} ~ post_X_treated + post_X_disp + post_X_treated_X_disp"
        " | event_fe_id + rel_t + calendar_month",
        data=work,
        vcov={"CRV1": "closure_event_id"},
    )
    return float(fit.tidy().loc["post_X_treated_X_disp", "Estimate"]), int(fit._N)


def main() -> None:
    args = parse_args()
    root = args.project_root.resolve()
    out = args.output_dir.resolve()
    panel = pd.read_parquet(out / "noncoffee_novelty_panel.parquet")
    crosswalk = pd.read_csv(out / "product_classification.csv")
    ddd = pd.read_csv(out / "ddd_results.csv")
    events = pd.read_csv(out / "event_study_results.csv")
    pretrends = pd.read_csv(out / "pretrend_tests.csv")
    support = pd.read_csv(out / "sample_support.csv")
    benchmark = pd.read_csv(out / "headline_reproduction.csv").iloc[0]
    audit = json.loads((out / "classification_audit.json").read_text(encoding="utf-8"))

    checks: list[dict] = []
    add_check(
        checks,
        "raw row count",
        audit["raw_rows"] == 10_631_943,
        f"raw_rows={audit['raw_rows']:,}",
    )
    expected_category_rows = {
        "coffee": 7_651_380,
        "food": 1_010_912,
        "noncoffee_drink": 1_947_508,
        "other_noncoffee": 22_143,
    }
    add_check(
        checks,
        "source category reconciliation",
        audit["global_category_rows"] == expected_category_rows,
        str(audit["global_category_rows"]),
    )
    exclusivity = audit["nonempty_category_fields_per_row"]
    add_check(
        checks,
        "exactly one category field per source row",
        exclusivity == {"1": 10_631_943},
        str(exclusivity),
    )
    category_pair_counts = crosswalk.groupby("category").size().to_dict()
    add_check(
        checks,
        "complete non-coffee classification crosswalk",
        category_pair_counts
        == {"food": 103, "noncoffee_drink": 168, "other_noncoffee": 81}
        and crosswalk["product_key"].nunique() == 352,
        f"category-name pairs={category_pair_counts}; unique keys={crosswalk['product_key'].nunique()}",
    )

    key_cols = ["event_fe_id", "rel_t"]
    panel_shape_ok = (
        len(panel) == 321_184
        and not panel.duplicated(key_cols).any()
        and panel["event_fe_id"].nunique() == 40_148
        and panel.groupby("event_fe_id")["rel_t"].nunique().eq(8).all()
    )
    add_check(
        checks,
        "headline grid retained",
        panel_shape_ok,
        f"rows={len(panel):,}; episodes={panel['event_fe_id'].nunique():,}",
    )

    metric_ok = True
    for scope in SCOPES:
        n_col = f"n_products_{scope}"
        new_col = f"n_new_products_{scope}"
        any_col = f"any_purchase_{scope}"
        outcome = f"novelty_{scope}"
        metric_ok &= panel[new_col].le(panel[n_col]).all()
        metric_ok &= panel[any_col].eq(panel[n_col].gt(0).astype(int)).all()
        observed = panel.loc[panel[outcome].notna(), outcome]
        metric_ok &= observed.between(0, 1).all()
        metric_ok &= panel[outcome].notna().eq(panel[any_col].eq(1)).all()
    add_check(checks, "novelty metric bounds and denominators", metric_ok, "all scopes checked")

    nesting_ok = (
        panel["n_products_all_noncoffee"]
        .ge(panel["n_products_noncoffee_consumables"])
        .all()
        and panel["n_products_noncoffee_consumables"]
        .ge(panel["n_products_noncoffee_drinks"])
        .all()
    )
    add_check(checks, "scope nesting", nesting_ok, "all >= consumables >= drinks")

    algebra_ok = True
    for (scope, outcome_type), group in ddd.groupby(["scope", "outcome_type"]):
        if scope == "headline_all_products" and outcome_type != "conditional_novelty":
            continue
        values = group.set_index("estimand")["coef"]
        algebra_ok &= np.isclose(
            values["high_predicted_incidence_effect"],
            values["low_predicted_incidence_effect"] + values["high_minus_low_ddd"],
            atol=1e-10,
        )
    add_check(checks, "DDD group-effect algebra", algebra_ok, "high = low + DDD")

    reproduction_ok = (
        abs(float(benchmark.coef_difference)) < 1e-10
        and abs(float(benchmark.se_difference)) < 1e-10
        and int(benchmark.saved_n) == int(benchmark.temporary_n)
    )
    add_check(
        checks,
        "headline estimator reproduction",
        reproduction_ok,
        f"coef diff={benchmark.coef_difference:.3g}; se diff={benchmark.se_difference:.3g}; N={int(benchmark.temporary_n):,}",
    )

    refit_ok = True
    refit_details = []
    for scope in SCOPES:
        outcome = f"novelty_{scope}"
        coefficient, n = refit_ddd(panel, outcome)
        saved = ddd[
            ddd["scope"].eq(scope)
            & ddd["outcome_type"].eq("conditional_novelty")
            & ddd["estimand"].eq("high_minus_low_ddd")
        ].iloc[0]
        refit_ok &= np.isclose(coefficient, saved.coef, atol=1e-10) and n == saved.n
        refit_details.append(f"{scope}: coef={coefficient:.6f}, N={n:,}")
    add_check(checks, "independent DDD refits", refit_ok, "; ".join(refit_details))

    pretrend_ok = True
    for scope in ["headline_all_products", *SCOPES]:
        rows = pretrends[
            pretrends["scope"].eq(scope)
            & pretrends["test"].eq("pretrend_ddd_joint_zero")
        ]
        pretrend_ok &= len(rows) == 1 and int(rows.iloc[0].n_restrictions) == 3
    add_check(checks, "DDD pretrend coverage", pretrend_ok, "three leads for every novelty scope")

    event_ok = True
    for scope in ["headline_all_products", *SCOPES]:
        periods = set(
            events[
                events["scope"].eq(scope)
                & events["component"].eq("high_minus_low_ddd")
            ]["rel_t"].astype(int)
        )
        event_ok &= periods == {-4, -3, -2, 1, 2, 3, 4}
    add_check(checks, "event-study period coverage", event_ok, "reference period -1 omitted")

    support_ok = len(support) == 3 * 4 * 8 and support["purchase_entry_rate"].between(0, 1).all()
    add_check(
        checks,
        "sample-entry support table",
        support_ok,
        f"rows={len(support)}; expected=96",
    )

    checks_df = pd.DataFrame(checks)
    checks_df.to_csv(out / "validation_checks.csv", index=False)
    overall = "Ready to share with caveats" if checks_df["passed"].all() else "Needs revision"
    primary = ddd[
        ddd["scope"].eq("all_noncoffee")
        & ddd["outcome_type"].eq("conditional_novelty")
        & ddd["estimand"].eq("high_minus_low_ddd")
    ].iloc[0]
    primary_pretrend = pretrends[
        pretrends["scope"].eq("all_noncoffee")
        & pretrends["test"].eq("pretrend_ddd_joint_zero")
    ].iloc[0]
    failed = checks_df.loc[~checks_df["passed"], "check"].tolist()
    report = f"""# Validation report: non-coffee novelty DDD

## Overall assessment: {overall}

The primary all-non-coffee DDD is **{primary.coef:+.4f}** (SE {primary.se:.4f}; 95% CI [{primary.ci_low:.4f}, {primary.ci_high:.4f}]; CRV1 p={primary.pvalue:.4f}; restricted wild-cluster p={primary.pvalue_wild_restricted:.4f}). The differential-pretrend test has p={primary_pretrend.pvalue:.4f}.

## Validation checks

{checks_df.to_markdown(index=False)}

## Required caveat

The novelty ratio is defined only in member-periods containing at least one product in the selected non-coffee scope. The saved any-purchase DDD and cell-specific entry rates must accompany interpretation of the conditional result.

## Incomplete blockers

{('None.' if not failed else ', '.join(failed))}
"""
    (out / "VALIDATION_REPORT.md").write_text(report, encoding="utf-8")
    print(checks_df.to_string(index=False))
    print("\n" + report)
    if not checks_df["passed"].all():
        raise SystemExit(1)


if __name__ == "__main__":
    main()
