from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyfixest as pf
import statsmodels.formula.api as smf


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
LENGTH_BINS: list[tuple[int, int]] = [(10, 14), (15, 19), (20, 24), (25, 29)]
MECHANISM_ALPHA = 0.05
MECHANISM_PERMUTATIONS = 1000


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


def _assign_length_bin(closure_duration_days: pd.Series) -> pd.Series:
    labels = [f"{start}-{end}" for start, end in LENGTH_BINS]
    bins = [LENGTH_BINS[0][0]] + [end for _, end in LENGTH_BINS]
    return pd.cut(
        closure_duration_days,
        bins=bins,
        labels=labels,
        include_lowest=True,
        right=True,
    )


def _standardize_intro(df: pd.DataFrame, intro_col: str) -> pd.Series:
    values = pd.to_numeric(df[intro_col], errors="coerce")
    std = float(values.std(ddof=0))
    if std == 0.0 or math.isnan(std):
        return values * 0.0
    return (values - float(values.mean())) / std


def _fit_pooled_interaction_test(
    *,
    sample: pd.DataFrame,
    intro_df: pd.DataFrame,
    outcome_col: str,
    cluster_col: str = "member_id",
) -> pd.DataFrame:
    merge_cols = ["dept_id", "closure_start", "closure_end", "closure_duration_days"]
    intro_cols = merge_cols + ["avg_n_introduced_during_control"]
    work_df = sample.merge(
        intro_df[intro_cols],
        on=merge_cols,
        how="left",
        validate="many_to_one",
    ).copy()
    if work_df["avg_n_introduced_during_control"].isna().any():
        raise ValueError("Missing intro intensity after merging pooled sample with closure-level intro table.")

    work_df["intro_z"] = _standardize_intro(work_df, "avg_n_introduced_during_control")
    work_df["post_X_treated"] = work_df["post"] * work_df["treated"]
    work_df["post_X_disp"] = work_df["post"] * work_df["disp_binary"]
    work_df["post_X_treated_X_disp"] = work_df["post"] * work_df["treated"] * work_df["disp_binary"]
    work_df["post_X_intro"] = work_df["post"] * work_df["intro_z"]
    work_df["post_X_treated_X_intro"] = work_df["post"] * work_df["treated"] * work_df["intro_z"]
    work_df["post_X_disp_X_intro"] = work_df["post"] * work_df["disp_binary"] * work_df["intro_z"]
    work_df["post_X_treated_X_disp_X_intro"] = (
        work_df["post"] * work_df["treated"] * work_df["disp_binary"] * work_df["intro_z"]
    )

    formula = (
        f"{outcome_col} ~ post_X_treated + post_X_disp + post_X_treated_X_disp + "
        "post_X_intro + post_X_treated_X_intro + post_X_disp_X_intro + "
        "post_X_treated_X_disp_X_intro | event_fe_id + rel_t + calendar_month"
    )
    fit = pf.feols(
        fml=f"{formula}",
        data=work_df,
        vcov={"CRV1": cluster_col},
    )
    tidy = fit.tidy()
    term = "post_X_treated_X_disp_X_intro"
    if term not in tidy.index:
        raise ValueError(f"Expected pooled interaction term not found in model output: {term}")

    return pd.DataFrame(
        [
            {
                "test_name": "pooled_4way_interaction",
                "term": term,
                "coef": float(tidy.loc[term, "Estimate"]),
                "se": float(tidy.loc[term, "Std. Error"]),
                "pvalue_two_sided": float(tidy.loc[term, "Pr(>|t|)"]),
                "pvalue_one_sided_less": float(tidy.loc[term, "Pr(>|t|)"] / 2.0)
                if float(tidy.loc[term, "Estimate"]) < 0
                else float(1.0 - float(tidy.loc[term, "Pr(>|t|)"] / 2.0)),
                "n": int(fit._N),
                "r2_within": float(fit._r2_within),
            }
        ]
    )


def _fit_closure_level_wls_test(
    *,
    closure_df: pd.DataFrame,
    outcome_label: str,
    coef_col: str,
    se_col: str,
) -> pd.DataFrame:
    work_df = closure_df[
        ["dept_id", "closure_duration_days", "avg_n_introduced_during_control", coef_col, se_col]
    ].copy()
    work_df = work_df.rename(columns={coef_col: "effect", se_col: "effect_se"})
    work_df = work_df.dropna(subset=["effect", "effect_se", "avg_n_introduced_during_control"]).copy()
    work_df["length_bin"] = _assign_length_bin(work_df["closure_duration_days"])
    work_df = work_df[work_df["length_bin"].notna()].copy()
    work_df["intro_z"] = _standardize_intro(work_df, "avg_n_introduced_during_control")
    work_df["weight"] = 1.0 / np.square(work_df["effect_se"])

    fitted = smf.wls(
        formula="effect ~ intro_z + C(length_bin)",
        data=work_df,
        weights=work_df["weight"],
    ).fit()
    if "intro_z" not in fitted.params.index:
        raise ValueError("Expected intro_z coefficient missing from WLS model.")

    return pd.DataFrame(
        [
            {
                "test_name": "closure_level_wls_bin_adjusted",
                "outcome": outcome_label,
                "term": "intro_z",
                "coef": float(fitted.params["intro_z"]),
                "se": float(fitted.bse["intro_z"]),
                "pvalue_two_sided": float(fitted.pvalues["intro_z"]),
                "pvalue_one_sided_less": float(fitted.pvalues["intro_z"] / 2.0)
                if float(fitted.params["intro_z"]) < 0
                else float(1.0 - float(fitted.pvalues["intro_z"] / 2.0)),
                "n_closures": int(work_df.shape[0]),
                "alpha": MECHANISM_ALPHA,
            }
        ]
    )


def _permutation_test_within_bins(
    *,
    closure_df: pd.DataFrame,
    coef_col: str,
    se_col: str,
    n_permutations: int,
    seed: int = 20260506,
) -> pd.DataFrame:
    work_df = closure_df[
        ["closure_duration_days", "avg_n_introduced_during_control", coef_col, se_col]
    ].copy()
    work_df = work_df.rename(columns={coef_col: "effect", se_col: "effect_se"})
    work_df = work_df.dropna(subset=["effect", "effect_se", "avg_n_introduced_during_control"]).copy()
    work_df["length_bin"] = _assign_length_bin(work_df["closure_duration_days"])
    work_df = work_df[work_df["length_bin"].notna()].copy()
    work_df["intro_z"] = _standardize_intro(work_df, "avg_n_introduced_during_control")
    work_df["weight"] = 1.0 / np.square(work_df["effect_se"])

    obs_fit = smf.wls(
        formula="effect ~ intro_z + C(length_bin)",
        data=work_df,
        weights=work_df["weight"],
    ).fit()
    observed_coef = float(obs_fit.params["intro_z"])

    rng = np.random.default_rng(seed=seed)
    perm_coefs: list[float] = []
    for _ in range(n_permutations):
        perm_df = work_df.copy()
        perm_df["intro_perm"] = perm_df["intro_z"]
        for _, idx in perm_df.groupby("length_bin", sort=False).groups.items():
            idx_list = list(idx)
            perm_values = perm_df.loc[idx_list, "intro_perm"].to_numpy(copy=True)
            rng.shuffle(perm_values)
            perm_df.loc[idx_list, "intro_perm"] = perm_values
        perm_fit = smf.wls(
            formula="effect ~ intro_perm + C(length_bin)",
            data=perm_df,
            weights=perm_df["weight"],
        ).fit()
        perm_coefs.append(float(perm_fit.params["intro_perm"]))

    perm_arr = np.asarray(perm_coefs, dtype=float)
    pvalue_one_sided_less = float(np.mean(perm_arr <= observed_coef))
    pvalue_two_sided = float(np.mean(np.abs(perm_arr) >= abs(observed_coef)))
    return pd.DataFrame(
        [
            {
                "test_name": "within_bin_permutation_wls_slope",
                "term": "intro_z",
                "observed_coef": observed_coef,
                "pvalue_one_sided_less": pvalue_one_sided_less,
                "pvalue_two_sided": pvalue_two_sided,
                "n_permutations": int(n_permutations),
                "alpha": MECHANISM_ALPHA,
            }
        ]
    )


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


def _summarize_relationship_by_length_bin(
    *,
    df: pd.DataFrame,
    outcome: str,
    coef_col: str,
) -> tuple[dict[str, object], pd.DataFrame]:
    work_df = df.copy()
    work_df["length_bin"] = _assign_length_bin(work_df["closure_duration_days"])
    work_df = work_df[work_df["length_bin"].notna() & work_df[coef_col].notna()].copy()

    # Pooled within-bin correlation by residualizing both variables on length-bin means.
    work_df["intro_resid"] = (
        work_df["avg_n_introduced_during_control"]
        - work_df.groupby("length_bin")["avg_n_introduced_during_control"].transform("mean")
    )
    work_df["effect_resid"] = (
        work_df[coef_col] - work_df.groupby("length_bin")[coef_col].transform("mean")
    )
    pooled_within_bin_corr = _corr(work_df["intro_resid"], work_df["effect_resid"])

    bin_rows: list[dict[str, object]] = []
    for length_bin, bin_df in work_df.groupby("length_bin", sort=True):
        corr_value = _corr(bin_df["avg_n_introduced_during_control"], bin_df[coef_col])
        within_bin_median_intro = float(bin_df["avg_n_introduced_during_control"].median())
        high_df = bin_df[bin_df["avg_n_introduced_during_control"] >= within_bin_median_intro]
        low_df = bin_df[bin_df["avg_n_introduced_during_control"] < within_bin_median_intro]
        high_low_diff = (
            float(high_df[coef_col].mean() - low_df[coef_col].mean())
            if (not high_df.empty and not low_df.empty)
            else math.nan
        )
        bin_rows.append(
            {
                "outcome": outcome,
                "length_bin": str(length_bin),
                "n_closures": int(bin_df.shape[0]),
                "mean_closure_duration_days": float(bin_df["closure_duration_days"].mean()),
                "mean_avg_n_introduced_during_control": float(
                    bin_df["avg_n_introduced_during_control"].mean()
                ),
                "mean_effect": float(bin_df[coef_col].mean()),
                "corr_intro_vs_effect_within_bin": corr_value,
                "within_bin_median_intro": within_bin_median_intro,
                "high_intro_n_closures": int(high_df.shape[0]),
                "low_intro_n_closures": int(low_df.shape[0]),
                "high_minus_low_mean_effect_within_bin": high_low_diff,
            }
        )

    by_bin_df = pd.DataFrame(bin_rows).sort_values("length_bin").reset_index(drop=True)
    summary = {
        "outcome": outcome,
        "coef_col": coef_col,
        "n_closures": int(work_df.shape[0]),
        "pooled_within_bin_corr": pooled_within_bin_corr,
        "mean_within_bin_high_minus_low_effect": (
            float(by_bin_df["high_minus_low_mean_effect_within_bin"].dropna().mean())
            if "high_minus_low_mean_effect_within_bin" in by_bin_df.columns
            and by_bin_df["high_minus_low_mean_effect_within_bin"].notna().any()
            else math.nan
        ),
    }
    return summary, by_bin_df


def _write_effect_summary(
    *,
    output_dir: Path,
    menu_summary_df: pd.DataFrame,
    merged_wide_df: pd.DataFrame,
    relationship_summaries: list[dict[str, object]],
    relationship_by_bin_summaries: list[dict[str, object]],
    relationship_by_bin_tables: list[pd.DataFrame],
    mechanism_test_tables: list[pd.DataFrame],
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

    lines.extend(
        [
            "",
            "## Matched-Bin Comparison by Closure Length",
            "",
            "- Bins (inclusive): 10-14, 15-19, 20-24, 25-29 days.",
            "- Metric for product changes: `avg_n_introduced_during_control`.",
            "- The pooled within-bin correlation is computed after demeaning introductions and effects within each length bin.",
            "- `high_minus_low_mean_effect_within_bin` compares above-median vs below-median introductions inside each length bin.",
        ]
    )

    for summary, table in zip(relationship_by_bin_summaries, relationship_by_bin_tables):
        lines.extend(
            [
                "",
                f"### {summary['outcome']}",
                "",
                f"- Closures in configured bins with non-missing key effect: {summary['n_closures']}",
                (
                    "- Pooled within-bin correlation between introductions and key DDD effect: "
                    f"{summary['pooled_within_bin_corr']:.3f}"
                    if not math.isnan(float(summary["pooled_within_bin_corr"]))
                    else "- Pooled within-bin correlation between introductions and key DDD effect: NA"
                ),
                (
                    "- Mean within-bin high-minus-low effect gap: "
                    f"{summary['mean_within_bin_high_minus_low_effect']:.4f}"
                    if not math.isnan(float(summary["mean_within_bin_high_minus_low_effect"]))
                    else "- Mean within-bin high-minus-low effect gap: NA"
                ),
                "",
                table.to_markdown(index=False),
            ]
        )

    lines.extend(["", "## Formal Mechanism Tests", ""])
    for table in mechanism_test_tables:
        if table.empty:
            continue
        header = str(table["outcome"].iloc[0]) if "outcome" in table.columns else "global"
        lines.extend([f"### {header}", "", table.to_markdown(index=False), ""])

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
    relationship_by_bin_summaries: list[dict[str, object]] = []
    relationship_by_bin_tables: list[pd.DataFrame] = []
    mechanism_test_tables: list[pd.DataFrame] = []

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

        pooled_sample = build_estimation_sample(
            outcome=str(settings["outcome"]),
            cfg=cfg,
            t_horizon=T_HORIZON,
            closure_duration_days=False,
            separate_effect=False,
            select_recency_consumers=False,
            require_balanced_panel=settings["require_balanced_panel"],
            variety_seeking_mode=str(settings["variety_seeking_mode"]),
            drop_period0_purchasers=bool(settings["drop_period0_purchasers"]),
            unbalanced_panel=bool(settings["unbalanced_panel"]),
        )
        pooled_result = _fit_pooled_interaction_test(
            sample=pooled_sample,
            intro_df=menu_summary_df,
            outcome_col=str(settings["outcome"]),
        ).assign(outcome=str(settings["output_subdir"]))
        wls_result = _fit_closure_level_wls_test(
            closure_df=merged_df,
            outcome_label=str(settings["output_subdir"]),
            coef_col="binary_coef",
            se_col="binary_se",
        )
        perm_result = _permutation_test_within_bins(
            closure_df=merged_df,
            coef_col="binary_coef",
            se_col="binary_se",
            n_permutations=MECHANISM_PERMUTATIONS,
        ).assign(outcome=str(settings["output_subdir"]))
        mechanism_test_tables.append(pd.concat([pooled_result, wls_result, perm_result], ignore_index=True))

        coef_col = "binary_coef"
        relationship_summaries.append(
            _summarize_relationship(
                df=merged_df,
                outcome=str(settings["output_subdir"]),
                coef_col=coef_col,
            )
        )
        by_bin_summary, by_bin_table = _summarize_relationship_by_length_bin(
            df=merged_df,
            outcome=str(settings["output_subdir"]),
            coef_col=coef_col,
        )
        relationship_by_bin_summaries.append(by_bin_summary)
        relationship_by_bin_tables.append(by_bin_table)
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
    pd.concat(relationship_by_bin_tables, ignore_index=True).to_csv(
        compare_output_dir / "closure_level_effects_vs_control_introductions_by_length_bin.csv",
        index=False,
    )
    pd.concat(mechanism_test_tables, ignore_index=True).to_csv(
        compare_output_dir / "mechanism_2_formal_tests.csv",
        index=False,
    )

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
        relationship_by_bin_summaries=relationship_by_bin_summaries,
        relationship_by_bin_tables=relationship_by_bin_tables,
        mechanism_test_tables=mechanism_test_tables,
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
