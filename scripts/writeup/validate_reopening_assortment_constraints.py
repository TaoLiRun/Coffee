"""Validate paper-facing reopening-assortment outputs against source results."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


OUTCOMES = ("core_coverage", "rarefied_products_50", "menu_jaccard_pre")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
    )
    return parser.parse_args()


def check_close(
    checks: list[dict],
    label: str,
    observed: float,
    expected: float,
    tolerance: float = 5e-5,
) -> None:
    checks.append(
        {
            "check": label,
            "passed": bool(np.isclose(observed, expected, atol=tolerance, rtol=0)),
            "observed": float(observed),
            "expected": float(expected),
        }
    )


def main() -> None:
    root = parse_args().project_root.resolve()
    output_dir = root / "outputs/05_robustness/reopening_assortment_constraints"
    manuscript = (root / "writeup/main.tex").read_text(encoding="utf-8")
    results = pd.read_csv(output_dir / "treated_post_path_results.csv")
    joint = pd.read_csv(output_dir / "treated_post_path_joint_tests.csv")
    support = pd.read_csv(output_dir / "treated_post_path_support.csv")
    returns = pd.read_csv(output_dir / "treated_first_return_exposure_results.csv")
    opportunity = pd.read_csv(
        output_dir / "treated_return_week_novel_opportunity_results.csv"
    )
    timing_distribution = pd.read_csv(
        output_dir / "treated_return_timing_distribution.csv"
    )
    internal_checks = pd.read_csv(output_dir / "validation_checks.csv")

    checks: list[dict] = []
    primary = results[results["sample"].eq("complete_4_post_weeks")]
    primary_joint = joint[joint["sample"].eq("complete_4_post_weeks")]
    primary_support = support[support["sample"].eq("complete_4_post_weeks")]
    for outcome in OUTCOMES:
        outcome_rows = primary[primary["outcome"].eq(outcome)].set_index(
            "relative_week"
        )
        for week in (2, 3, 4):
            coefficient = float(outcome_rows.loc[week, "coef"])
            checks.append(
                {
                    "check": f"manuscript includes {outcome} week {week} coefficient",
                    "passed": f"${coefficient:.4f}$" in manuscript,
                    "observed": f"{coefficient:.4f}",
                    "expected": "exact four-decimal manuscript cell",
                }
            )
        pvalue = float(
            primary_joint.loc[
                primary_joint["outcome"].eq(outcome), "pvalue_wild_restricted"
            ].iloc[0]
        )
        checks.append(
            {
                "check": f"manuscript includes {outcome} wild-cluster joint p-value",
                "passed": f"${pvalue:.4f}$" in manuscript,
                "observed": f"{pvalue:.4f}",
                "expected": "exact four-decimal manuscript cell",
            }
        )

    expected_support = {
        "core_coverage": (72, 18, 0.7687),
        "rarefied_products_50": (64, 16, 29.2581),
        "menu_jaccard_pre": (72, 18, 0.6120),
    }
    for outcome, (observations, stores, week_one_mean) in expected_support.items():
        row = primary_support[primary_support["outcome"].eq(outcome)].iloc[0]
        check_close(
            checks,
            f"{outcome} week-one mean",
            float(row["week_1_mean"]),
            week_one_mean,
        )
        check_close(
            checks,
            f"{outcome} observation count",
            float(row["observations"]),
            observations,
            tolerance=0,
        )
        check_close(
            checks,
            f"{outcome} treated-store count",
            float(row["treated_stores"]),
            stores,
            tolerance=0,
        )

    return_effect = returns[returns["outcome"].eq("days_after_reopening")].iloc[0]
    check_close(checks, "days-to-return coefficient", return_effect["coef"], -2.8724)
    check_close(checks, "days-to-return standard error", return_effect["se_crv1"], 0.2936)
    expected_opportunity = {
        "timing_deviation_novel_opportunity_share_leave_one_out": (
            -0.0010,
            0.0006,
            0.0930,
            2325,
            17,
        ),
        "timing_deviation_novel_products_leave_one_out": (
            -0.2756,
            0.3848,
            0.4836,
            2402,
            18,
        ),
    }
    for outcome, expected in expected_opportunity.items():
        row = opportunity[opportunity["outcome"].eq(outcome)].iloc[0]
        for column, value in zip(
            ("coef", "se_crv1", "pvalue_crv1", "n", "n_clusters"), expected
        ):
            tolerance = 5e-5 if column not in {"n", "n_clusters"} else 0
            check_close(
                checks,
                f"{outcome} {column}",
                float(row[column]),
                value,
                tolerance=tolerance,
            )
        expected_ci = {
            "timing_deviation_novel_opportunity_share_leave_one_out": (
                -0.0021886,
                0.0001867,
            ),
            "timing_deviation_novel_products_leave_one_out": (-1.0874, 0.5363),
        }[outcome]
        for column, value in zip(("ci_low", "ci_high"), expected_ci):
            check_close(
                checks,
                f"{outcome} {column}",
                float(row[column]),
                value,
                tolerance=5e-5,
            )

    expected_distribution = {
        0: (5349, 1134, 0.2120, 12.1570, 11, 0.3695),
        1: (2041, 1268, 0.6213, 9.0331, 7, 0.5363),
    }
    for high, expected in expected_distribution.items():
        row = timing_distribution[timing_distribution["disp_binary"].eq(high)].iloc[0]
        for column, value in zip(
            (
                "eligible_members",
                "returned_within_28_days",
                "share_returned_within_28_days",
                "mean_days_after_reopening",
                "median_days_after_reopening",
                "share_returning_week_1",
            ),
            expected,
        ):
            tolerance = 5e-5 if isinstance(value, float) else 0
            check_close(
                checks,
                f"return distribution group {high}: {column}",
                float(row[column]),
                value,
                tolerance=tolerance,
            )

    checks.append(
        {
            "check": "all runner-internal validation checks pass",
            "passed": bool(internal_checks["passed"].all()),
            "observed": int(internal_checks["passed"].sum()),
            "expected": int(len(internal_checks)),
        }
    )
    report = pd.DataFrame(checks)
    report.to_csv(output_dir / "paper_validation_checks.csv", index=False)
    payload = {
        "checks": int(len(report)),
        "passed": int(report["passed"].sum()),
        "failed": int((~report["passed"]).sum()),
    }
    (output_dir / "paper_validation_summary.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )
    if not report["passed"].all():
        failed = report.loc[~report["passed"], "check"].tolist()
        raise RuntimeError(f"Paper validation failed: {failed}")
    print(json.dumps(payload))


if __name__ == "__main__":
    main()
