from __future__ import annotations

import math
import os
from pathlib import Path
import sys

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")
os.environ.setdefault("XDG_CACHE_HOME", "/tmp")

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.displacement_effect_estimation.data import (
    _slice_by_date,
    load_orders_for_behavior_members,
)


MAIN_DIR = ROOT / "outputs" / "03_main_18_closures"
DIAG_DIR = ROOT / "outputs" / "04_diagnostics_18_closures"
FIG_DIR = ROOT / "writeup" / "figures"

PURCHASE_DIR = MAIN_DIR / "purchase_frequency_ddd_h4"
NOVELTY_DIR = MAIN_DIR / "novelty_member_first_ddd_h4"
MARKET_NEW_DIR = MAIN_DIR / "novelty_market_new_ddd_h4"
HET_DIR = DIAG_DIR / "novelty_pre_heterogeneity_median"


def _fmt(x: float, digits: int = 3) -> str:
    if pd.isna(x):
        return ""
    return f"{x:.{digits}f}"


def _fmt_pp(x: float, digits: int = 1) -> str:
    if pd.isna(x):
        return ""
    return f"{100 * x:.{digits}f}"


def _stars(pvalue: float) -> str:
    if pd.isna(pvalue):
        return ""
    if pvalue < 0.01:
        return "***"
    if pvalue < 0.05:
        return "**"
    if pvalue < 0.10:
        return "*"
    return ""


def _load_sample(path: Path, outcome: str) -> pd.DataFrame:
    df = pd.read_csv(path / "estimation_sample.csv")
    df["closure_start"] = pd.to_datetime(df["closure_start"]).dt.strftime("%Y-%m-%d")
    df["closure_end"] = pd.to_datetime(df["closure_end"]).dt.strftime("%Y-%m-%d")
    df["treated"] = df["treated"].astype(int)
    df["disp_binary"] = df["disp_binary"].astype(int)
    df["rel_t"] = df["rel_t"].astype(int)
    return df.dropna(subset=[outcome]).copy()


def _print_snippet(name: str, lines: list[str]) -> None:
    print(f"\n% --- {name} ---")
    print("\n".join(lines).rstrip())


def _coef_rows(path: Path) -> pd.DataFrame:
    return pd.read_csv(path / "ddd_binary_results.csv")


def _fit_row(path: Path, spec: str, filename: str = "ddd_binary_fit.csv") -> pd.Series:
    rows = pd.read_csv(path / filename)
    matches = rows.loc[rows["spec"] == spec]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one fit row for spec={spec!r}; found {len(matches)}.")
    return matches.iloc[0]


def _estimand_row(rows: pd.DataFrame, estimand: str) -> pd.Series:
    matches = rows.loc[rows["estimand"] == estimand]
    if len(matches) != 1:
        raise ValueError(
            f"Expected exactly one row for estimand={estimand!r}; found {len(matches)}."
        )
    return matches.iloc[0]


def _coef_cell(row: pd.Series) -> str:
    return f"{_fmt(float(row['coef']), 4)}{_stars(float(row['pvalue']))}"


def _se_cell(row: pd.Series) -> str:
    return f"({_fmt(float(row['se']), 4)})"


def _term_row(path: Path, filename: str, spec: str, term: str) -> pd.Series:
    rows = pd.read_csv(path / filename)
    matches = rows.loc[(rows["spec"] == spec) & (rows["term"] == term)]
    if len(matches) != 1:
        raise ValueError(
            f"Expected exactly one row for spec={spec!r}, term={term!r}; "
            f"found {len(matches)} in {path / filename}."
        )
    return matches.iloc[0]


def _pre_mean(path: Path, outcome: str) -> float:
    sample = pd.read_csv(path / "estimation_sample.csv", usecols=["rel_t", outcome])
    return float(sample.loc[(sample["rel_t"] < 0) & sample[outcome].notna(), outcome].mean())


def write_main_results_decomposition_table() -> None:
    purchase = _coef_rows(PURCHASE_DIR)
    novelty = _coef_rows(NOVELTY_DIR)
    purchase_fit = _fit_row(PURCHASE_DIR, "binary_collapsed")
    novelty_fit = _fit_row(NOVELTY_DIR, "binary_collapsed")
    purchase_low = _estimand_row(purchase, "low_predicted_incidence_effect")
    purchase_high = _estimand_row(purchase, "high_predicted_incidence_effect")
    purchase_ddd = _estimand_row(purchase, "high_minus_low_ddd")
    novelty_low = _estimand_row(novelty, "low_predicted_incidence_effect")
    novelty_high = _estimand_row(novelty, "high_predicted_incidence_effect")
    novelty_ddd = _estimand_row(novelty, "high_minus_low_ddd")

    lines = [
        r"\begin{table}[h!]",
        r"\centering",
        r"\caption{Decomposition of the main triple-differences results}",
        r"\label{tab:main_results_decomposition}",
        r"\small",
        r"\begin{tabularx}{\textwidth}{Xcc}",
        r"\toprule",
        r"Effect & Purchase frequency & Novelty-seeking \\",
        r"\midrule",
        r"\multicolumn{3}{l}{\textit{Panel A. Closure effects within predicted-incidence group}} \\",
        rf"Low predicted purchase incidence ($\delta^B$) & {_coef_cell(purchase_low)} & {_coef_cell(novelty_low)} \\",
        rf" & {_se_cell(purchase_low)} & {_se_cell(novelty_low)} \\",
        rf"High predicted purchase incidence ($\delta^B + \delta^D$) & {_coef_cell(purchase_high)} & {_coef_cell(novelty_high)} \\",
        rf" & {_se_cell(purchase_high)} & {_se_cell(novelty_high)} \\",
        r"\addlinespace",
        r"\multicolumn{3}{l}{\textit{Panel B. Incremental interruption contrast}} \\",
        rf"High minus low ($\delta^D$) & {_coef_cell(purchase_ddd)} & {_coef_cell(novelty_ddd)} \\",
        rf" & {_se_cell(purchase_ddd)} & {_se_cell(novelty_ddd)} \\",
        r"\addlinespace",
        rf"Pre-period outcome mean & {_fmt(_pre_mean(PURCHASE_DIR, 'n_purchases'), 4)} & {_fmt(_pre_mean(NOVELTY_DIR, 'variety_seeking'), 4)} \\",
        rf"Observations & {int(purchase_low['n']):,} & {int(novelty_low['n']):,} \\",
        rf"$R^2$ & {_fmt(float(purchase_fit['r2']), 3)} & {_fmt(float(novelty_fit['r2']), 3)} \\",
        rf"Within $R^2$ & {_fmt(float(purchase_low['r2_within']), 3)} & {_fmt(float(novelty_low['r2_within']), 3)} \\",
        r"\bottomrule",
        r"\end{tabularx}",
        r"\vspace{1mm}",
        r"\fnote{Notes: Panel A reports treated-control post contrasts within low- and high-predicted-incidence episodes. Panel B reports their difference, the triple-differences coefficient. Purchase frequency is purchase days per calendar day. Novelty-seeking is the share of distinct products purchased in a window that the consumer had not purchased before that window and is defined only for windows with a purchase. The high-group effects are estimated in algebraically equivalent parameterizations and have their own cluster-robust standard errors. Standard errors, clustered at the member level, are in parentheses. All regressions include member-closure, relative-period and calendar-month fixed effects and omit the closure window. $R^2$ includes the absorbed fixed effects; within $R^2$ is calculated after absorbing them. *** $p<0.01$, ** $p<0.05$, * $p<0.1$.}",
        r"\end{table}",
        "",
    ]
    _print_snippet("main_results_decomposition", lines)


def write_appendix_main_specification_tables() -> None:
    outcomes = [
        ("Purchase frequency", PURCHASE_DIR),
        ("Novelty-seeking", NOVELTY_DIR),
    ]

    binary_rows = [
        (r"Post $\times$ Treated ($\delta^B$)", "post_X_treated"),
        (r"Post $\times$ High predicted incidence ($\beta$)", "post_X_disp"),
        (
            r"Post $\times$ Treated $\times$ High predicted incidence ($\delta^D$)",
            "post_X_treated_X_disp",
        ),
    ]
    binary_results = {
        label: {
            term: _term_row(path, "ddd_binary_results.csv", "binary_collapsed", term)
            for _, term in binary_rows
        }
        for label, path in outcomes
    }
    binary_fits = {
        label: _fit_row(path, "binary_collapsed")
        for label, path in outcomes
    }
    binary_lines = [
        r"\begin{table}[H]",
        r"\centering",
        r"\caption{Complete binary predicted-incidence specifications}",
        r"\label{tab:appendix_binary_main_results}",
        r"\small",
        r"\begin{tabularx}{\textwidth}{Xcc}",
        r"\toprule",
        r" & Purchase frequency & Novelty-seeking \\",
        r" & (1) & (2) \\",
        r"\midrule",
    ]
    for row_label, term in binary_rows:
        binary_lines.append(
            f"{row_label} & "
            + " & ".join(_coef_cell(binary_results[label][term]) for label, _ in outcomes)
            + r" \\"
        )
        binary_lines.append(
            " & "
            + " & ".join(_se_cell(binary_results[label][term]) for label, _ in outcomes)
            + r" \\"
        )
    binary_lines.extend(
        [
            r"\addlinespace",
            "Pre-period outcome mean & "
            + " & ".join(
                [
                    _fmt(_pre_mean(PURCHASE_DIR, "n_purchases"), 4),
                    _fmt(_pre_mean(NOVELTY_DIR, "variety_seeking"), 4),
                ]
            )
            + r" \\",
            "Observations & "
            + " & ".join(f"{int(binary_fits[label]['n']):,}" for label, _ in outcomes)
            + r" \\",
            "$R^2$ & "
            + " & ".join(_fmt(float(binary_fits[label]["r2"]), 3) for label, _ in outcomes)
            + r" \\",
            "Within $R^2$ & "
            + " & ".join(
                _fmt(float(binary_fits[label]["r2_within"]), 3) for label, _ in outcomes
            )
            + r" \\",
            r"Member-closure fixed effects & Yes & Yes \\",
            r"Relative-period fixed effects & Yes & Yes \\",
            r"Calendar-month fixed effects & Yes & Yes \\",
            r"\bottomrule",
            r"\end{tabularx}",
            r"\vspace{1mm}",
            r"\fnote{Notes: This table reports every coefficient from equation~\eqref{eq:main_ddd}. Post $\times$ Treated is the low-predicted-incidence treated-control post contrast. Post $\times$ High captures the high-minus-low post shift common to treated and control episodes and is not a treatment effect. The triple interaction is the high-minus-low DDD. The closure window is omitted. Novelty-seeking is conditional on a purchase in the window. Standard errors, clustered at the member level, are in parentheses. See Table~\ref{tab:main_results_decomposition} for the directly estimated high-group effects and detailed outcome definitions. *** $p<0.01$, ** $p<0.05$, * $p<0.1$.}",
            r"\end{table}",
            "",
        ]
    )
    _print_snippet("appendix_binary_main_results", binary_lines)

    score_rows = [
        (r"Post $\times$ Treated", "post_X_treated"),
        (r"Post $\times$ Centered predicted-incidence score", "post_X_score"),
        (
            r"Post $\times$ Treated $\times$ Centered predicted-incidence score",
            "post_X_treated_X_score",
        ),
    ]
    score_results = {
        label: {
            term: _term_row(path, "ddd_score_results.csv", "score_collapsed", term)
            for _, term in score_rows
        }
        for label, path in outcomes
    }
    score_fits = {
        label: _fit_row(path, "score_collapsed", "ddd_score_fit.csv")
        for label, path in outcomes
    }
    score_lines = [
        r"\begin{table}[H]",
        r"\centering",
        r"\caption{Complete continuous predicted-incidence specifications}",
        r"\label{tab:appendix_score_main_results}",
        r"\small",
        r"\begin{tabularx}{\textwidth}{Xcc}",
        r"\toprule",
        r" & Purchase frequency & Novelty-seeking \\",
        r" & (1) & (2) \\",
        r"\midrule",
    ]
    for row_label, term in score_rows:
        score_lines.append(
            f"{row_label} & "
            + " & ".join(_coef_cell(score_results[label][term]) for label, _ in outcomes)
            + r" \\"
        )
        score_lines.append(
            " & "
            + " & ".join(_se_cell(score_results[label][term]) for label, _ in outcomes)
            + r" \\"
        )
    score_lines.extend(
        [
            r"\addlinespace",
            "Observations & "
            + " & ".join(f"{int(score_fits[label]['n']):,}" for label, _ in outcomes)
            + r" \\",
            "$R^2$ & "
            + " & ".join(_fmt(float(score_fits[label]["r2"]), 3) for label, _ in outcomes)
            + r" \\",
            "Within $R^2$ & "
            + " & ".join(
                _fmt(float(score_fits[label]["r2_within"]), 3) for label, _ in outcomes
            )
            + r" \\",
            r"Member-closure fixed effects & Yes & Yes \\",
            r"Relative-period fixed effects & Yes & Yes \\",
            r"Calendar-month fixed effects & Yes & Yes \\",
            r"\bottomrule",
            r"\end{tabularx}",
            r"\vspace{1mm}",
            r"\fnote{Notes: The predicted-incidence score is centered at its estimation-sample mean. Post $\times$ Treated therefore gives the treated-control post contrast at the mean score. The score coefficient is the post-period score gradient common to treated and control episodes. The triple interaction shows how the treated-control post contrast changes with the predicted-incidence score. All remaining conventions and outcome definitions follow Table~\ref{tab:appendix_binary_main_results}. Standard errors, clustered at the member level, are in parentheses. *** $p<0.01$, ** $p<0.05$, * $p<0.1$.}",
            r"\end{table}",
            "",
        ]
    )
    _print_snippet("appendix_score_main_results", score_lines)


def write_new_product_seeking_table() -> None:
    binary = _coef_rows(MARKET_NEW_DIR)
    binary_fit = _fit_row(MARKET_NEW_DIR, "binary_collapsed")
    score_fit = _fit_row(MARKET_NEW_DIR, "score_collapsed", "ddd_score_fit.csv")

    low = _estimand_row(binary, "low_predicted_incidence_effect")
    high = _estimand_row(binary, "high_predicted_incidence_effect")
    ddd = _estimand_row(binary, "high_minus_low_ddd")
    binary_common = _term_row(
        MARKET_NEW_DIR, "ddd_binary_results.csv", "binary_collapsed", "post_X_disp"
    )
    score_treated = _term_row(
        MARKET_NEW_DIR, "ddd_score_results.csv", "score_collapsed", "post_X_treated"
    )
    score_common = _term_row(
        MARKET_NEW_DIR, "ddd_score_results.csv", "score_collapsed", "post_X_score"
    )
    score_ddd = _term_row(
        MARKET_NEW_DIR,
        "ddd_score_results.csv",
        "score_collapsed",
        "post_X_treated_X_score",
    )
    pre_mean = _pre_mean(MARKET_NEW_DIR, "variety_seeking")

    lines = [
        r"\begin{table}[H]",
        r"\centering",
        r"\caption{Robustness to using new-product-seeking}",
        r"\label{tab:appendix_new_product_seeking}",
        r"\small",
        r"\begin{tabularx}{\textwidth}{Xcc}",
        r"\toprule",
        r" & Binary high-incidence & Continuous incidence score \\",
        r" & (1) & (2) \\",
        r"\midrule",
        r"\multicolumn{3}{l}{\textit{Panel A. Group effects and incremental interruption contrast}} \\",
        rf"Low predicted purchase incidence & {_coef_cell(low)} & -- \\",
        rf" & {_se_cell(low)} & \\",
        rf"High predicted purchase incidence & {_coef_cell(high)} & -- \\",
        rf" & {_se_cell(high)} & \\",
        rf"High minus low DDD & {_coef_cell(ddd)} & -- \\",
        rf" & {_se_cell(ddd)} & \\",
        r"\addlinespace",
        r"\multicolumn{3}{l}{\textit{Panel B. Complete regression coefficients}} \\",
        rf"Post $\times$ Treated & {_coef_cell(low)} & {_coef_cell(score_treated)} \\",
        rf" & {_se_cell(low)} & {_se_cell(score_treated)} \\",
        rf"Post $\times$ Predicted incidence & {_coef_cell(binary_common)} & {_coef_cell(score_common)} \\",
        rf" & {_se_cell(binary_common)} & {_se_cell(score_common)} \\",
        rf"Post $\times$ Treated $\times$ Predicted incidence & {_coef_cell(ddd)} & {_coef_cell(score_ddd)} \\",
        rf" & {_se_cell(ddd)} & {_se_cell(score_ddd)} \\",
        r"\addlinespace",
        rf"Pre-period outcome mean & {_fmt(pre_mean, 4)} & {_fmt(pre_mean, 4)} \\",
        rf"Observations & {int(binary_fit['n']):,} & {int(score_fit['n']):,} \\",
        rf"$R^2$ & {_fmt(float(binary_fit['r2']), 3)} & {_fmt(float(score_fit['r2']), 3)} \\",
        rf"Within $R^2$ & {_fmt(float(binary_fit['r2_within']), 4)} & {_fmt(float(score_fit['r2_within']), 4)} \\",
        r"Member-closure fixed effects & Yes & Yes \\",
        r"Relative-period fixed effects & Yes & Yes \\",
        r"Calendar-month fixed effects & Yes & Yes \\",
        r"\bottomrule",
        r"\end{tabularx}",
        r"\vspace{1mm}",
        r"\fnote{Notes: Column (1) uses the binary high-predicted-incidence indicator; column (2) uses the mean-centered predicted-incidence score. In Panel A, the low- and high-incidence rows are directly estimated treated-control post contrasts, and the high-minus-low row is their DDD. These discrete group effects are not defined for column (2). In Panel B, Post $\times$ Predicted incidence is the common post shift across treated and control episodes; it is not a treatment effect. In column (2), a one-unit change corresponds to moving across the full predicted-incidence scale. Standard errors, clustered at the member level, are in parentheses. All regressions omit the closure window. *** $p<0.01$, ** $p<0.05$, * $p<0.1$.}",
        r"\end{table}",
        "",
    ]
    _print_snippet("appendix_new_product_seeking", lines)


def _episode_panel() -> pd.DataFrame:
    purchase = _load_sample(PURCHASE_DIR, "n_purchases")
    novelty_raw = pd.read_csv(NOVELTY_DIR / "estimation_sample.csv")
    novelty_raw["rel_t"] = novelty_raw["rel_t"].astype(int)

    keys = ["member_id", "dept_id", "closure_start", "event_fe_id"]
    base = (
        purchase[keys + ["treated", "disp_binary", "displacement_prob", "closure_duration_days"]]
        .drop_duplicates(subset=keys)
        .copy()
    )
    pre_purchase = (
        purchase[purchase["rel_t"] < 0]
        .groupby(keys, sort=False)["n_purchases"]
        .mean()
        .rename("pre_purchase_frequency")
        .reset_index()
    )
    pre_novelty = (
        novelty_raw[(novelty_raw["rel_t"] < 0) & novelty_raw["variety_seeking"].notna()]
        .groupby(keys, sort=False)["variety_seeking"]
        .mean()
        .rename("pre_novelty_seeking")
        .reset_index()
    )
    return base.merge(pre_purchase, on=keys, how="left").merge(pre_novelty, on=keys, how="left")


def _diff_se(control: pd.Series, treated: pd.Series) -> tuple[float, float, float]:
    c = control.dropna()
    t = treated.dropna()
    diff = float(t.mean() - c.mean())
    se = math.sqrt(float(t.var(ddof=1) / len(t) + c.var(ddof=1) / len(c)))
    pvalue = math.erfc(abs(diff / se) / math.sqrt(2)) if se > 0 else float("nan")
    return diff, se, pvalue


def write_balance_table() -> None:
    episode = _episode_panel()
    control = episode[episode["treated"] == 0]
    treated = episode[episode["treated"] == 1]
    variables = [
        ("Predicted blocked-purchase probability", "displacement_prob", 3),
        ("Blocked-buyer share", "disp_binary", 3),
        ("Pre-period purchase frequency", "pre_purchase_frequency", 3),
        ("Pre-period novelty-seeking", "pre_novelty_seeking", 3),
        ("Closure duration in days", "closure_duration_days", 1),
    ]
    lines = [
        r"\begin{table}[h!]",
        r"\centering",
        r"\caption{Treatment-control balance before closure}",
        r"\label{tab:treatment_control_balance}",
        r"\small",
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        r"Variable & Control mean & Treated mean & Difference & SE \\",
        r"\midrule",
        rf"Member-events & {len(control):,} & {len(treated):,} & & \\",
        rf"Unique members & {control['member_id'].nunique():,} & {treated['member_id'].nunique():,} & & \\",
    ]
    for label, col, digits in variables:
        diff, se, pvalue = _diff_se(control[col], treated[col])
        lines.append(
            f"{label} & {_fmt(control[col].mean(), digits)} & {_fmt(treated[col].mean(), digits)} & "
            f"{_fmt(diff, digits)}{_stars(pvalue)} & {_fmt(se, digits)} \\\\"
        )
    lines.extend(
        [
            r"\bottomrule",
            r"\end{tabular}",
            r"\vspace{1mm}",
            r"\fnote{Notes: The unit is a member-closure event. Pre-period purchase frequency is averaged over relative periods -4 to -1. Pre-period novelty-seeking is averaged over pre-period windows in which the member purchased at least one product. Difference is treatment minus control. Standard errors are heteroskedasticity-robust difference-in-means standard errors at the member-event level. *** $p<0.01$, ** $p<0.05$, * $p<0.1$.}",
            r"\end{table}",
            "",
        ]
    )
    _print_snippet("treatment_control_balance", lines)


def _purchase_trend_with_period0() -> pd.DataFrame:
    sample = _load_sample(PURCHASE_DIR, "n_purchases")
    base = sample[["group", "rel_t", "n_purchases"]].copy()
    base = base.rename(columns={"n_purchases": "mean_source"})

    keys = ["member_id", "dept_id", "closure_start"]
    members = (
        sample[
            keys
            + [
                "closure_end",
                "closure_duration_days",
                "group",
                "treated",
            ]
        ]
        .drop_duplicates(subset=keys)
        .copy()
    )
    member_ids = set(members["member_id"].dropna().astype(int).tolist())
    orders = load_orders_for_behavior_members(member_ids=member_ids)
    orders = orders.sort_values("date").reset_index(drop=True)

    parts: list[pd.DataFrame] = []
    for _, cohort in members.groupby(["dept_id", "closure_start", "closure_end"], sort=False):
        start = pd.to_datetime(cohort["closure_start"].iloc[0])
        end = pd.to_datetime(cohort["closure_end"].iloc[0])
        duration = float(cohort["closure_duration_days"].iloc[0])
        window_orders = _slice_by_date(orders, start, end)
        window_orders = window_orders[window_orders["member_id"].isin(cohort["member_id"])]
        counts = (
            window_orders.groupby("member_id")["date"].nunique().rename("_purchase_days").reset_index()
            if not window_orders.empty
            else pd.DataFrame(columns=["member_id", "_purchase_days"])
        )
        block = cohort.merge(counts, on="member_id", how="left")
        block["_purchase_days"] = block["_purchase_days"].fillna(0.0)
        block["mean_source"] = block["_purchase_days"] / duration
        block["rel_t"] = 0
        parts.append(block[["group", "rel_t", "mean_source"]])

    panel = pd.concat([base, *parts], ignore_index=True)
    return (
        panel.groupby(["group", "rel_t"], sort=True)["mean_source"]
        .mean()
        .reset_index()
        .rename(columns={"mean_source": "mean"})
    )


def write_closure_shock_figure() -> None:
    purchase_trend = _purchase_trend_with_period0()

    fig, ax = plt.subplots(figsize=(7.2, 4.3))
    colors = {"control": "#1f77b4", "treatment": "#d62728"}
    labels = {"control": "Control", "treatment": "Treated"}
    marker_faces = {"control": "white", "treatment": colors["treatment"]}
    line_styles = {"control": "--", "treatment": "-"}

    for group in ["control", "treatment"]:
        sub = purchase_trend[purchase_trend["group"] == group].sort_values("rel_t")
        ax.plot(
            sub["rel_t"],
            sub["mean"],
            marker="o",
            linewidth=2,
            linestyle=line_styles[group],
            color=colors[group],
            markerfacecolor=marker_faces[group],
            markeredgecolor=colors[group],
            markeredgewidth=1.6,
            label=labels[group],
        )
    ax.axvline(0, color="0.45", linestyle="--", linewidth=1)
    ax.set_title("Purchase frequency")
    ax.set_xlabel("Relative period")
    ax.set_ylabel("Purchase days per calendar day")
    ax.set_xticks([-4, -3, -2, -1, 0, 1, 2, 3, 4])
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False, loc="best")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "closure_shock_purchase_frequency.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def write_novelty_intention_paths_figure() -> None:
    novelty = _load_sample(NOVELTY_DIR, "variety_seeking")
    novelty = novelty[novelty["rel_t"] != 0].copy()
    trend = (
        novelty.groupby(["disp_binary", "treated", "rel_t"], sort=True)["variety_seeking"]
        .agg(mean="mean", n="size")
        .reset_index()
    )

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.3), sharex=True, sharey=True)
    colors = {0: "#1f77b4", 1: "#d62728"}
    labels = {0: "Control", 1: "Treated"}
    marker_faces = {0: "white", 1: colors[1]}
    line_styles = {0: "--", 1: "-"}
    panel_titles = {0: "Low intention", 1: "High intention"}

    for disp_binary, ax in zip([0, 1], axes):
        panel = trend[trend["disp_binary"] == disp_binary]
        for treated in [0, 1]:
            sub = panel[panel["treated"] == treated].sort_values("rel_t")
            ax.plot(
                sub["rel_t"],
                sub["mean"],
                marker="o",
                linewidth=2,
                linestyle=line_styles[treated],
                color=colors[treated],
                markerfacecolor=marker_faces[treated],
                markeredgecolor=colors[treated],
                markeredgewidth=1.6,
                label=labels[treated],
            )
        ax.axvspan(-0.5, 0.5, color="0.90", zorder=0)
        ax.text(
            0,
            0.98,
            "Closure\nwindow",
            transform=ax.get_xaxis_transform(),
            ha="center",
            va="top",
            fontsize=8,
            color="0.35",
        )
        ax.set_title(panel_titles[disp_binary])
        ax.set_xlabel("Relative period")
        ax.set_xticks([-4, -3, -2, -1, 1, 2, 3, 4])
        ax.grid(axis="y", alpha=0.25)

    axes[0].set_ylabel("Share of distinct products new to consumer")
    axes[0].legend(frameon=False, loc="best")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "novelty_intention_paths.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def _read_coef(path: Path, spec: str, term: str) -> tuple[float, float, float]:
    df = pd.read_csv(path)
    row = df[(df["spec"] == spec) & (df["term"] == term)].iloc[0]
    return float(row["coef"]), float(row["se"]), float(row["pvalue"])


def write_heterogeneity_table() -> None:
    df = pd.read_csv(HET_DIR / "ddd_binary_results.csv")
    sub = df[df["spec"] == "binary_collapsed_pre_novelty_split"].copy()
    base = sub[sub["term"] == "post_X_treated_X_disp"].iloc[0]
    inc = sub[sub["term"] == "post_X_treated_X_disp_X_novelty_pre_high"].iloc[0]
    high_effect = float(base["coef"] + inc["coef"])
    rows = [
        (r"Low pre-novelty effect ($\delta_L^D$)", float(base["coef"]), float(base["se"]), float(base["pvalue"])),
        (r"High pre-novelty increment ($\theta^D$)", float(inc["coef"]), float(inc["se"]), float(inc["pvalue"])),
        (r"High pre-novelty effect ($\delta_L^D+\theta^D$)", high_effect, float("nan"), float("nan")),
    ]
    lines = [
        r"\begin{table}[h!]",
        r"\centering",
        r"\caption{Heterogeneity by pre-period novelty-seeking}",
        r"\label{tab:pre_novelty_heterogeneity}",
        r"\small",
        r"\begin{tabular}{lcc}",
        r"\toprule",
        r"Parameter or effect & Estimate & SE \\",
        r"\midrule",
    ]
    for label, coef, se, pvalue in rows:
        lines.append(f"{label} & {_fmt(coef)}{_stars(pvalue)} & {_fmt(se)} \\\\")
    lines.extend(
        [
            r"\addlinespace",
            rf"Observations & {int(sub['n'].iloc[0]):,} & \\",
            r"Member-closure fixed effects & Yes & \\",
            r"Relative-period and calendar-month fixed effects & Yes & \\",
            r"\bottomrule",
            r"\end{tabular}",
            r"\vspace{1mm}",
            r"\fnote{Notes: The dependent variable is novelty-seeking. Low and high pre-novelty groups are split at the sample median of episode-level pre-period novelty among members with observed pre-period novelty. The low pre-novelty row estimates $\delta_L^D$ in equation~\eqref{eq:pre_novelty_heterogeneity}. The high pre-novelty increment estimates $\theta^D$. The implied high pre-novelty effect is $\delta_L^D+\theta^D$; a separate standard error for this linear combination is not reported. Standard errors are clustered at the member level where reported. *** $p<0.01$, ** $p<0.05$, * $p<0.1$.}",
            r"\end{table}",
            "",
        ]
    )
    print("\n% --- pre_novelty_heterogeneity ---")
    print("\n".join(lines).rstrip())


def write_magnitude_summary() -> None:
    purchase = _load_sample(PURCHASE_DIR, "n_purchases")
    novelty = _load_sample(NOVELTY_DIR, "variety_seeking")
    market = _load_sample(MARKET_NEW_DIR, "variety_seeking")
    purchase_coef, purchase_se, purchase_p = _read_coef(
        PURCHASE_DIR / "ddd_binary_results.csv", "binary_collapsed", "post_X_treated_X_disp"
    )
    novelty_coef, novelty_se, novelty_p = _read_coef(
        NOVELTY_DIR / "ddd_binary_results.csv", "binary_collapsed", "post_X_treated_X_disp"
    )
    market_coef, market_se, market_p = _read_coef(
        MARKET_NEW_DIR / "ddd_binary_results.csv", "binary_collapsed", "post_X_treated_X_disp"
    )
    rows = [
        {
            "outcome": "purchase_frequency",
            "coef": purchase_coef,
            "se": purchase_se,
            "pvalue": purchase_p,
            "pre_mean": purchase.loc[purchase["rel_t"] < 0, "n_purchases"].mean(),
        },
        {
            "outcome": "novelty_seeking",
            "coef": novelty_coef,
            "se": novelty_se,
            "pvalue": novelty_p,
            "pre_mean": novelty.loc[novelty["rel_t"] < 0, "variety_seeking"].mean(),
        },
        {
            "outcome": "new_product_seeking",
            "coef": market_coef,
            "se": market_se,
            "pvalue": market_p,
            "pre_mean": market.loc[market["rel_t"] < 0, "variety_seeking"].mean(),
        },
    ]
    summary = pd.DataFrame(rows).assign(relative_to_pre_mean=lambda x: x["coef"] / x["pre_mean"])
    print("\n% --- magnitude_summary.csv ---")
    print(summary.to_csv(index=False).rstrip())


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    write_main_results_decomposition_table()
    write_appendix_main_specification_tables()
    write_new_product_seeking_table()
    write_balance_table()
    write_closure_shock_figure()
    write_novelty_intention_paths_figure()
    write_heterogeneity_table()
    write_magnitude_summary()


if __name__ == "__main__":
    main()
