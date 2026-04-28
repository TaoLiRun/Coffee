from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src" / "displacement_effect_estimation"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from control_menu_features import build_and_save_control_menu_introductions
from data import build_estimation_sample, load_config
from menu_features import detect_menu_feature_paths
from report import save_outputs, save_variety_panel_plot
from run import fit_spec_bundle


SELECTED_REGISTRY_REL = "outputs/customer-store/closure_pair_registry_selected.csv"
OUTPUT_ROOT_REL = "outputs/robustness/selected_subset_missing_new_products"
T_HORIZON = 4


def _set_selected_registry_env() -> None:
    os.environ["DISPLACEMENT_EFFECT_CLOSURE_REGISTRY"] = SELECTED_REGISTRY_REL


def _outcome_settings() -> list[dict[str, object]]:
    return [
        {
            "outcome": "n_purchases",
            "output_subdir": "n_purchases",
            "require_balanced_panel": None,
            "variety_seeking_mode": "distinct",
            "drop_period0_purchasers": False,
            "unbalanced_panel": True,
            "use_did": False,
        },
        {
            "outcome": "variety_seeking",
            "output_subdir": "variety_seeking_unbalanced",
            "require_balanced_panel": False,
            "variety_seeking_mode": "distinct",
            "drop_period0_purchasers": False,
            "unbalanced_panel": True,
            "use_did": False,
        },
    ]


def _coerce_term_rows(df: pd.DataFrame, spec: str, term: str) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["spec", "term", "coef", "se", "pvalue", "n", "r2_within"])
    return df[(df["spec"] == spec) & (df["term"] == term)].copy()


def _run_separate_effects(
    *,
    cfg: dict,
    output_dir: Path,
    outcome: str,
    require_balanced_panel: bool | None,
    variety_seeking_mode: str,
    drop_period0_purchasers: bool,
    unbalanced_panel: bool,
    use_did: bool,
) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)

    sample = build_estimation_sample(
        outcome=outcome,
        cfg=cfg,
        t_horizon=T_HORIZON,
        closure_duration_days=False,
        separate_effect=True,
        select_recency_consumers=False,
        require_balanced_panel=require_balanced_panel,
        variety_seeking_mode=variety_seeking_mode,
        drop_period0_purchasers=drop_period0_purchasers,
        unbalanced_panel=unbalanced_panel,
    )

    event_index_rows: list[dict[str, object]] = []
    event_groups = list(
        sample.groupby(["dept_id", "closure_start", "closure_end", "closure_event_id"], sort=False)
    )

    for dept_id, closure_start, closure_end, closure_event_id in (
        group_key for group_key, _ in event_groups
    ):
        event_sample = sample[
            (sample["dept_id"] == dept_id)
            & (sample["closure_start"] == closure_start)
            & (sample["closure_end"] == closure_end)
            & (sample["closure_event_id"] == closure_event_id)
        ].copy()

        results = fit_spec_bundle(
            sample=event_sample,
            outcome=outcome,
            cluster_col="member_id",
            include_length_heterogeneity=False,
            use_did=use_did,
        )

        event_output_dir = output_dir / closure_event_id
        save_outputs(
            output_dir=event_output_dir,
            sample=event_sample,
            binary_terms=results["binary_terms"],
            binary_fit=results["binary_fit"],
            score_terms=results["score_terms"],
            score_fit=results["score_fit"],
            event_terms=results["event_terms"],
            event_fit=results["event_fit"],
            pretrend_tests=results["pretrend_tests"],
            summary_notes=[
                "- Estimation mode: separate_effect=true",
                f"- Closure event: `{closure_event_id}`",
                "- Closure duration filter days: False",
                "- Recency filter days: False",
                f"- Drop period-0 purchasers: {drop_period0_purchasers}",
                "- Length-heterogeneity event-study spec skipped: true",
                f"- Model type: {'DiD' if use_did else 'DDD'}",
            ],
        )
        if outcome == "variety_seeking":
            save_variety_panel_plot(
                output_dir=event_output_dir,
                sample=event_sample,
                cfg=cfg,
                variety_seeking_mode=variety_seeking_mode,
            )

        event_index_rows.append(
            {
                "closure_event_id": closure_event_id,
                "dept_id": int(dept_id),
                "closure_start": closure_start,
                "closure_end": closure_end,
                "closure_duration_days": int(event_sample["closure_duration_days"].iloc[0]),
                "members": int(event_sample["member_id"].nunique()),
                "rows": int(len(event_sample)),
                "treated_members": int(event_sample.loc[event_sample["treated"] == 1, "member_id"].nunique()),
                "control_members": int(event_sample.loc[event_sample["treated"] == 0, "member_id"].nunique()),
                "output_dir": str(event_output_dir.relative_to(PROJECT_ROOT)),
            }
        )

    event_index_df = pd.DataFrame(event_index_rows).sort_values(
        ["closure_start", "dept_id"]
    ).reset_index(drop=True)
    event_index_df.to_csv(output_dir / "event_index.csv", index=False)
    return event_index_df


def _extract_effect_table(
    *,
    event_index_df: pd.DataFrame,
    outcome_dir: Path,
    outcome_label: str,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for record in event_index_df.to_dict(orient="records"):
        event_dir = PROJECT_ROOT / str(record["output_dir"])
        binary_terms = pd.read_csv(event_dir / "ddd_binary_results.csv", encoding="utf-8-sig")
        score_terms = pd.read_csv(event_dir / "ddd_score_results.csv", encoding="utf-8-sig")

        binary_key = _coerce_term_rows(
            binary_terms,
            spec="binary_collapsed",
            term="post_X_treated_X_disp",
        )
        score_key = _coerce_term_rows(
            score_terms,
            spec="score_collapsed",
            term="post_X_treated_X_score",
        )

        row = {
            "outcome": outcome_label,
            "closure_event_id": record["closure_event_id"],
            "dept_id": int(record["dept_id"]),
            "closure_start": record["closure_start"],
            "closure_end": record["closure_end"],
            "closure_duration_days": int(record["closure_duration_days"]),
            "members": int(record["members"]),
            "treated_members": int(record["treated_members"]),
            "control_members": int(record["control_members"]),
        }

        for prefix, coef_df in [("binary", binary_key), ("score", score_key)]:
            if coef_df.empty:
                row[f"{prefix}_coef"] = math.nan
                row[f"{prefix}_se"] = math.nan
                row[f"{prefix}_pvalue"] = math.nan
                row[f"{prefix}_n"] = math.nan
            else:
                coef_row = coef_df.iloc[0]
                row[f"{prefix}_coef"] = float(coef_row["coef"])
                row[f"{prefix}_se"] = float(coef_row["se"])
                row[f"{prefix}_pvalue"] = float(coef_row["pvalue"])
                row[f"{prefix}_n"] = int(coef_row["n"])

        rows.append(row)

    return pd.DataFrame(rows).sort_values(["closure_start", "dept_id"]).reset_index(drop=True)


def _fit_line(x: pd.Series, y: pd.Series) -> tuple[float, float] | None:
    mask = x.notna() & y.notna()
    if mask.sum() < 2:
        return None
    slope, intercept = np.polyfit(x[mask], y[mask], 1)
    return float(slope), float(intercept)


def _corr(x: pd.Series, y: pd.Series) -> float:
    mask = x.notna() & y.notna()
    if mask.sum() < 2:
        return math.nan
    return float(x[mask].corr(y[mask]))


def _plot_effect_vs_introductions(
    *,
    df: pd.DataFrame,
    coef_col: str,
    title: str,
    y_label: str,
    output_path: Path,
) -> None:
    plot_df = df[df[coef_col].notna()].copy()
    if plot_df.empty:
        return

    x = plot_df["avg_n_introduced_during_control"]
    y = plot_df[coef_col]

    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    ax.scatter(x, y, color="#1f5aa6", alpha=0.9)
    for _, row in plot_df.iterrows():
        ax.annotate(
            str(int(row["dept_id"])),
            (row["avg_n_introduced_during_control"], row[coef_col]),
            xytext=(4, 3),
            textcoords="offset points",
            fontsize=8,
        )

    fitted = _fit_line(x, y)
    if fitted is not None:
        slope, intercept = fitted
        x_grid = np.linspace(float(x.min()), float(x.max()), 200)
        ax.plot(x_grid, intercept + slope * x_grid, color="#c44e52", linewidth=2)

    ax.axhline(0.0, color="gray", linestyle="--", linewidth=1)
    ax.set_xlabel("Average number of control-store introductions during closure")
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def _summarize_relationship(
    *,
    df: pd.DataFrame,
    outcome: str,
    coef_col: str,
) -> dict[str, object]:
    work_df = df.copy()
    median_x = float(work_df["avg_n_introduced_during_control"].median())
    work_df["intro_group"] = np.where(
        work_df["avg_n_introduced_during_control"] >= median_x,
        "high",
        "low",
    )

    group_summary = (
        work_df.groupby("intro_group", sort=True)[coef_col]
        .agg(["count", "mean", "median"])
        .reset_index()
        .rename(
            columns={
                "count": "n_closures",
                "mean": "mean_effect",
                "median": "median_effect",
            }
        )
    )

    summary = {
        "outcome": outcome,
        "coef_col": coef_col,
        "n_closures": int(work_df[coef_col].notna().sum()),
        "median_avg_n_introduced_during_control": median_x,
        "corr_avg_intro_vs_effect": _corr(
            work_df["avg_n_introduced_during_control"], work_df[coef_col]
        ),
        "group_summary": group_summary,
    }
    return summary


def _write_effect_summary(
    *,
    output_dir: Path,
    menu_summary_df: pd.DataFrame,
    merged_wide_df: pd.DataFrame,
    relationship_summaries: list[dict[str, object]],
) -> None:
    lines = [
        "# Effect vs. Control-Store Introductions",
        "",
        f"- Selected closures analyzed: {menu_summary_df.shape[0]:,}",
        f"- Mean average control-store introductions during closure: {menu_summary_df['avg_n_introduced_during_control'].mean():.3f}",
        f"- Median average control-store introductions during closure: {menu_summary_df['avg_n_introduced_during_control'].median():.3f}",
        f"- Min / max average control-store introductions during closure: {menu_summary_df['avg_n_introduced_during_control'].min():.3f} / {menu_summary_df['avg_n_introduced_during_control'].max():.3f}",
        "",
        "## Closure-Level Table",
        merged_wide_df.to_markdown(index=False),
    ]

    for summary in relationship_summaries:
        lines.extend(
            [
                "",
                f"## {summary['outcome']}",
                "",
                f"- Closures with non-missing key effect: {summary['n_closures']}",
                (
                    "- Correlation between average control-store introductions and key DDD effect: "
                    f"{summary['corr_avg_intro_vs_effect']:.3f}"
                    if not math.isnan(float(summary["corr_avg_intro_vs_effect"]))
                    else "- Correlation between average control-store introductions and key DDD effect: NA"
                ),
                (
                    "- Median split on average introductions: "
                    f"{summary['median_avg_n_introduced_during_control']:.3f}"
                ),
                "",
                summary["group_summary"].to_markdown(index=False),
            ]
        )

    (output_dir / "summary.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    _set_selected_registry_env()

    cfg = load_config()
    output_root = PROJECT_ROOT / OUTPUT_ROOT_REL
    menu_output_dir = output_root / "menu_features"
    separate_root = output_root / "separate_effects"
    compare_output_dir = output_root / "effect_vs_introductions"

    paths = detect_menu_feature_paths(project_root=PROJECT_ROOT)
    menu_summary_df, menu_detail_df = build_and_save_control_menu_introductions(
        output_dir=menu_output_dir,
        chunksize=1_000_000,
        paths=paths,
    )

    menu_summary_df = menu_summary_df.copy().rename(
        columns={"treatment_dept_id": "dept_id"}
    )
    menu_summary_df["dept_id"] = menu_summary_df["dept_id"].astype(int)
    menu_summary_df.to_csv(menu_output_dir / "control_menu_introductions_during_closure.csv", index=False)
    menu_detail_df.to_csv(
        menu_output_dir / "control_menu_introductions_during_closure_detail.csv", index=False
    )

    effect_tables: list[pd.DataFrame] = []
    merged_tables: list[pd.DataFrame] = []
    relationship_summaries: list[dict[str, object]] = []

    for settings in _outcome_settings():
        outcome_output_dir = separate_root / str(settings["output_subdir"])
        event_index_df = _run_separate_effects(
            cfg=cfg,
            output_dir=outcome_output_dir,
            outcome=str(settings["outcome"]),
            require_balanced_panel=settings["require_balanced_panel"],
            variety_seeking_mode=str(settings["variety_seeking_mode"]),
            drop_period0_purchasers=bool(settings["drop_period0_purchasers"]),
            unbalanced_panel=bool(settings["unbalanced_panel"]),
            use_did=bool(settings["use_did"]),
        )
        effect_df = _extract_effect_table(
            event_index_df=event_index_df,
            outcome_dir=outcome_output_dir,
            outcome_label=str(settings["output_subdir"]),
        )
        effect_tables.append(effect_df)

        merged_df = menu_summary_df.merge(
            effect_df,
            on=["dept_id", "closure_start", "closure_end", "closure_duration_days"],
            how="inner",
            validate="one_to_one",
        )
        merged_tables.append(merged_df.assign(outcome=str(settings["output_subdir"])))

        coef_col = "binary_coef"
        relationship_summaries.append(
            _summarize_relationship(
                df=merged_df,
                outcome=str(settings["output_subdir"]),
                coef_col=coef_col,
            )
        )
        _plot_effect_vs_introductions(
            df=merged_df,
            coef_col=coef_col,
            title=f"{settings['output_subdir']}: key DDD effect vs. control-store introductions",
            y_label="Key DDD effect (binary collapsed triple interaction)",
            output_path=compare_output_dir / f"{settings['output_subdir']}_binary_coef_vs_avg_introductions.png",
        )

    compare_output_dir.mkdir(parents=True, exist_ok=True)
    all_effects_df = pd.concat(effect_tables, ignore_index=True)
    all_effects_df.to_csv(compare_output_dir / "closure_level_key_effects_long.csv", index=False)

    n_purchase_df = next(df for df in merged_tables if df["outcome"].iloc[0] == "n_purchases").copy()
    variety_df = next(
        df for df in merged_tables if df["outcome"].iloc[0] == "variety_seeking_unbalanced"
    ).copy()

    merged_wide_df = n_purchase_df[
        [
            "dept_id",
            "closure_start",
            "closure_end",
            "closure_duration_days",
            "avg_n_introduced_during_control",
            "min_n_introduced_during_control",
            "max_n_introduced_during_control",
            "total_n_introduced_during_control",
            "members",
            "treated_members",
            "control_members",
            "binary_coef",
            "binary_se",
            "binary_pvalue",
            "score_coef",
            "score_pvalue",
        ]
    ].rename(
        columns={
            "members": "n_purchases_members",
            "treated_members": "n_purchases_treated_members",
            "control_members": "n_purchases_control_members",
            "binary_coef": "n_purchases_binary_coef",
            "binary_se": "n_purchases_binary_se",
            "binary_pvalue": "n_purchases_binary_pvalue",
            "score_coef": "n_purchases_score_coef",
            "score_pvalue": "n_purchases_score_pvalue",
        }
    ).merge(
        variety_df[
            [
                "dept_id",
                "closure_start",
                "closure_end",
                "closure_duration_days",
                "members",
                "treated_members",
                "control_members",
                "binary_coef",
                "binary_se",
                "binary_pvalue",
                "score_coef",
                "score_pvalue",
            ]
        ].rename(
            columns={
                "members": "variety_members",
                "treated_members": "variety_treated_members",
                "control_members": "variety_control_members",
                "binary_coef": "variety_binary_coef",
                "binary_se": "variety_binary_se",
                "binary_pvalue": "variety_binary_pvalue",
                "score_coef": "variety_score_coef",
                "score_pvalue": "variety_score_pvalue",
            }
        ),
        on=["dept_id", "closure_start", "closure_end", "closure_duration_days"],
        how="inner",
        validate="one_to_one",
    ).sort_values(["closure_start", "dept_id"]).reset_index(drop=True)

    merged_wide_df.to_csv(
        compare_output_dir / "closure_level_effects_vs_control_introductions.csv",
        index=False,
    )
    _write_effect_summary(
        output_dir=compare_output_dir,
        menu_summary_df=menu_summary_df,
        merged_wide_df=merged_wide_df,
        relationship_summaries=relationship_summaries,
    )

    metadata = {
        "source_registry_path": SELECTED_REGISTRY_REL,
        "menu_feature_output_dir": str(menu_output_dir.relative_to(PROJECT_ROOT)),
        "separate_effect_output_root": str(separate_root.relative_to(PROJECT_ROOT)),
        "comparison_output_dir": str(compare_output_dir.relative_to(PROJECT_ROOT)),
        "t_horizon": T_HORIZON,
        "outcomes": [str(settings["output_subdir"]) for settings in _outcome_settings()],
    }
    (output_root / "run_metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
