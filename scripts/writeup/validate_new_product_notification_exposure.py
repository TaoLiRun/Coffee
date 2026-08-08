from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd


OUT = Path(".")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the saved new-product-notification exposure analysis."
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/05_robustness/new_product_notification_exposure"),
    )
    return parser.parse_args()


def phase_mean(cells: pd.DataFrame, treated: int, high: int, phase: str, metric: str) -> float:
    row = cells[
        cells["treated"].eq(treated)
        & cells["disp_binary"].eq(high)
        & cells["phase"].eq(phase)
    ]
    if len(row) != 1:
        raise AssertionError((treated, high, phase, len(row)))
    return float(row.iloc[0][metric])


def main() -> None:
    global OUT
    args = parse_args()
    project_root = args.project_root.resolve()
    OUT = args.output_dir if args.output_dir.is_absolute() else project_root / args.output_dir
    panel = pd.read_parquet(OUT / "new_product_push_panel.parquet")
    estimates = pd.read_csv(OUT / "new_product_push_ddd.csv")
    event_study = pd.read_csv(OUT / "new_product_push_event_study.csv")
    cells = pd.read_csv(OUT / "cell_phase_descriptives.csv")
    audit = json.loads((OUT / "audit.json").read_text(encoding="utf-8"))

    checks = []

    def check(name: str, condition: bool, detail: str) -> None:
        checks.append({"check": name, "passed": bool(condition), "detail": detail})
        if not condition:
            raise AssertionError(f"{name}: {detail}")

    check(
        "panel grain",
        not panel.duplicated(["member_id", "closure_event_id", "rel_t"]).any(),
        f"{len(panel):,} unique member-event-period rows",
    )
    check(
        "balanced nine-period panel",
        len(panel) == 40148 * 9 and panel.groupby("member_id")["rel_t"].nunique().eq(9).all(),
        f"{panel.member_id.nunique():,} members x 9 periods = {len(panel):,} rows",
    )
    check(
        "raw push count reconciliation",
        int(panel["n_push_records"].sum())
        == audit["raw_push"]["rows_mapped_to_analysis_periods"],
        f"panel={int(panel['n_push_records'].sum()):,}; audit={audit['raw_push']['rows_mapped_to_analysis_periods']:,}",
    )
    check(
        "new-product count reconciliation",
        int(panel["n_new_push_records"].sum())
        == audit["raw_push"]["new_product_raw_rows"],
        f"panel={int(panel['n_new_push_records'].sum()):,}; audit={audit['raw_push']['new_product_raw_rows']:,}",
    )
    check(
        "new-product records are unique campaign-days",
        audit["raw_push"]["new_product_raw_rows"]
        == audit["raw_push"]["new_product_unique_campaign_day_rows"],
        "raw and deduplicated new-product counts are identical",
    )
    check(
        "no missing policy ids",
        audit["raw_push"]["missing_policy_share"] == 0,
        f"missing share={audit['raw_push']['missing_policy_share']}",
    )
    primary = estimates[estimates["outcome"].eq("new_campaigns_per_day")].copy()
    check(
        "all primary estimates oppose the proposed mechanism",
        primary["coef"].gt(0).all(),
        ", ".join(f"{row.comparison}={row.coef:.6f}" for row in primary.itertuples()),
    )
    check(
        "campaign and raw-record estimates coincide",
        np.allclose(
            primary.sort_values("comparison")["coef"],
            estimates[estimates["outcome"].eq("new_records_per_day")]
            .sort_values("comparison")["coef"],
        ),
        "new-product notification records contain no duplicate member-policy-date exposures",
    )
    check(
        "primary pretrend does not reject",
        audit["primary_pretrend"]["pvalue"] > 0.10,
        f"joint p={audit['primary_pretrend']['pvalue']:.4f}",
    )

    metric = "new_campaigns_per_day_mean"
    decomposition = []
    for comparison, after_phase in [
        ("during_vs_pre", "during"),
        ("post_vs_pre", "post"),
    ]:
        changes = {}
        for treated in [0, 1]:
            low_change = phase_mean(cells, treated, 0, after_phase, metric) - phase_mean(
                cells, treated, 0, "pre", metric
            )
            high_change = phase_mean(cells, treated, 1, after_phase, metric) - phase_mean(
                cells, treated, 1, "pre", metric
            )
            changes[treated] = high_change - low_change
            decomposition.append(
                {
                    "comparison": comparison,
                    "treated": treated,
                    "low_pre": phase_mean(cells, treated, 0, "pre", metric),
                    "low_after": phase_mean(cells, treated, 0, after_phase, metric),
                    "low_change": low_change,
                    "high_pre": phase_mean(cells, treated, 1, "pre", metric),
                    "high_after": phase_mean(cells, treated, 1, after_phase, metric),
                    "high_change": high_change,
                    "high_minus_low_change": changes[treated],
                }
            )
        for row in decomposition:
            if row["comparison"] == comparison:
                row["raw_ddd"] = changes[1] - changes[0]
    decomposition_frame = pd.DataFrame(decomposition)
    decomposition_frame.to_csv(OUT / "directional_decomposition.csv", index=False)
    pd.DataFrame(checks).to_csv(OUT / "validation_checks.csv", index=False)

    post = primary[primary["comparison"].eq("post_vs_pre")].iloc[0]
    during = primary[primary["comparison"].eq("during_vs_all_pre")].iloc[0]
    report = f"""# Validation report: new-product notification mechanism

## Overall assessment: Ready to share with caveats

The required first-stage has the wrong sign for the alternative explanation. The high-minus-low treated-control change in unique new-product notification campaigns is **+{during.coef:.4f} per consumer-day during closure** (95% CI {during.ci_low:.4f} to {during.ci_high:.4f}; restricted wild-cluster p={during.pvalue_wild_restricted:.4f}) and **+{post.coef:.4f} after reopening** (95% CI {post.ci_low:.4f} to {post.ci_high:.4f}; restricted wild-cluster p={post.pvalue_wild_restricted:.4f}). A negative coefficient is required for differential new-product notification exposure to explain the negative novelty DDD.

## What the levels show

Low-intention treated consumers receive more new-product notifications in absolute terms in every phase, as expected from inactivity-triggered targeting. During closure, the rates are 0.0307 per day for low-intention and 0.0115 for high-intention consumers; after reopening, they are 0.0250 and 0.0113. But the pre-period rates are already 0.0247 and 0.0058. The high group therefore experiences the larger relative increase after accounting for pre-period levels and the matched controls.

## Validation checks

All {len(checks)} programmed checks pass. The analysis uses {panel.member_id.nunique():,} consumers, {panel.closure_event_id.nunique()} closures and {len(panel):,} member-period observations including the closure period. The raw scan covers {audit['raw_push']['rows_scanned']:,} records and maps {audit['raw_push']['rows_mapped_to_analysis_periods']:,} to the analysis windows. All {audit['raw_push']['new_product_raw_rows']:,} trigger-tag-3 records are unique at the member-policy-date level, so raw and deduplicated estimates coincide. The primary event-study leads do not reject a joint pretrend (p={audit['primary_pretrend']['pvalue']:.3f}).

## Caveats

- The records establish targeting entries, not verified delivery, impression, opening or reading.
- The interpretation assumes that new-product notifications weakly increase awareness or exploration. If they reduce novelty, the sign argument reverses, but that would conflict with the proposed notification mechanism.
- The test rules out differential recorded new-product notifications as an explanation; it does not cover familiar-product messages or unobserved in-app rankings.
- With 18 closure clusters, the primary inference uses both CRV1 intervals and restricted wild-cluster p-values.
"""
    (OUT / "VALIDATION_REPORT.md").write_text(report, encoding="utf-8")
    print(pd.DataFrame(checks).to_string(index=False))
    print("\nDIRECTIONAL DECOMPOSITION")
    print(decomposition_frame.to_string(index=False))
    print("\n", report)


if __name__ == "__main__":
    main()
