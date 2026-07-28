from __future__ import annotations

import math
import os
from pathlib import Path
import sys

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")
os.environ.setdefault("XDG_CACHE_HOME", "/tmp")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import t as student_t

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.displacement_effect_estimation.data import (
    _slice_by_date,
    load_orders_for_behavior_members,
)


MAIN_DIR = ROOT / "outputs" / "03_main_18_closures"
DIAG_DIR = ROOT / "outputs" / "04_diagnostics_18_closures"
FIG_DIR = ROOT / "writeup" / "figures"
PAPER_OUTPUT_DIR = ROOT / "outputs" / "paper" / "descriptives"

PURCHASE_DIR = MAIN_DIR / "purchase_frequency_ddd_h4"
NOVELTY_DIR = MAIN_DIR / "novelty_member_first_ddd_h4"
MARKET_NEW_DIR = MAIN_DIR / "novelty_market_new_ddd_h4"
BASELINE_NOVELTY_DIR = ROOT / "outputs" / "paper" / "mechanism_baseline_novelty"


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


def _clustered_mean_summary(
    frame: pd.DataFrame,
    value: str,
    by: list[str],
    cluster: str = "closure_event_id",
) -> pd.DataFrame:
    """Summarize pooled means with CRV1 intervals clustered by closure event."""

    rows: list[dict[str, float | int | str]] = []
    for keys, group in frame.dropna(subset=[value]).groupby(by, sort=True):
        key_values = keys if isinstance(keys, tuple) else (keys,)
        values = group[value].astype(float)
        mean = float(values.mean())
        n = int(len(group))
        cluster_scores = (values - mean).groupby(group[cluster]).sum()
        n_clusters = int(cluster_scores.size)
        if n_clusters < 2:
            se = float("nan")
            critical_value = float("nan")
        else:
            variance = (n_clusters / (n_clusters - 1)) * float(
                (cluster_scores**2).sum()
            ) / (n**2)
            se = math.sqrt(variance)
            critical_value = float(student_t.ppf(0.975, df=n_clusters - 1))
        row = dict(zip(by, key_values))
        row.update(
            {
                "mean": mean,
                "se_cluster": se,
                "ci_low": mean - critical_value * se,
                "ci_high": mean + critical_value * se,
                "n": n,
                "n_clusters": n_clusters,
            }
        )
        rows.append(row)
    return pd.DataFrame(rows)


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


def _bold_coef_cell(row: pd.Series) -> str:
    return rf"\textbf{{{_coef_cell(row)}}}"


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
        rf"High minus low ($\delta^D$) & {_bold_coef_cell(purchase_ddd)} & {_bold_coef_cell(novelty_ddd)} \\",
        rf" & {_se_cell(purchase_ddd)} & {_se_cell(novelty_ddd)} \\",
        r"\addlinespace",
        rf"Pre-period outcome mean & {_fmt(_pre_mean(PURCHASE_DIR, 'n_purchases'), 4)} & {_fmt(_pre_mean(NOVELTY_DIR, 'variety_seeking'), 4)} \\",
        rf"Observations & {int(purchase_low['n']):,} & {int(novelty_low['n']):,} \\",
        rf"$R^2$ & {_fmt(float(purchase_fit['r2']), 3)} & {_fmt(float(novelty_fit['r2']), 3)} \\",
        rf"Within $R^2$ & {_fmt(float(purchase_low['r2_within']), 3)} & {_fmt(float(novelty_low['r2_within']), 3)} \\",
        r"\bottomrule",
        r"\end{tabularx}",
        r"\vspace{1mm}",
        r"\fnote{Notes: Panel A reports treated-control post contrasts within low- and high-predicted-incidence episodes. Panel B reports their difference, the triple-differences coefficient; boldface marks this focal estimand. Purchase frequency is purchase days per calendar day. Novelty-seeking is the share of distinct products purchased in a window that the consumer had not purchased before that window and is defined only for windows with a purchase. The high-group effects are estimated in algebraically equivalent parameterizations and have their own cluster-robust standard errors. Standard errors, clustered by closure event (18 clusters), are in parentheses. All regressions include member-closure, relative-period and calendar-month fixed effects and omit the closure window. $R^2$ includes the absorbed fixed effects; within $R^2$ is calculated after absorbing them. *** $p<0.01$, ** $p<0.05$, * $p<0.1$.}",
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
        coefficient_formatter = (
            _bold_coef_cell if term == "post_X_treated_X_disp" else _coef_cell
        )
        binary_lines.append(
            f"{row_label} & "
            + " & ".join(
                coefficient_formatter(binary_results[label][term])
                for label, _ in outcomes
            )
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
            r"\fnote{Notes: This table reports every coefficient from equation~\eqref{eq:main_ddd}. Post $\times$ Treated is the low-predicted-incidence treated-control post contrast. Post $\times$ High captures the high-minus-low post shift common to treated and control episodes and is not a treatment effect. The triple interaction is the high-minus-low DDD and is shown in boldface. The closure window is omitted. Novelty-seeking is conditional on a purchase in the window. Standard errors, clustered by closure event (18 clusters), are in parentheses. See Table~\ref{tab:main_results_decomposition} for the directly estimated high-group effects and detailed outcome definitions. *** $p<0.01$, ** $p<0.05$, * $p<0.1$.}",
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
        coefficient_formatter = (
            _bold_coef_cell if term == "post_X_treated_X_score" else _coef_cell
        )
        score_lines.append(
            f"{row_label} & "
            + " & ".join(
                coefficient_formatter(score_results[label][term])
                for label, _ in outcomes
            )
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
            r"\fnote{Notes: The predicted-incidence score is centered at its estimation-sample mean. Post $\times$ Treated therefore gives the treated-control post contrast at the mean score. The score coefficient is the post-period score gradient common to treated and control episodes. The triple interaction, shown in boldface, is the focal coefficient and shows how the treated-control post contrast changes with the predicted-incidence score. All remaining conventions and outcome definitions follow Table~\ref{tab:appendix_binary_main_results}. Standard errors, clustered by closure event (18 clusters), are in parentheses. *** $p<0.01$, ** $p<0.05$, * $p<0.1$.}",
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
        rf"High minus low DDD & {_bold_coef_cell(ddd)} & -- \\",
        rf" & {_se_cell(ddd)} & \\",
        r"\addlinespace",
        r"\multicolumn{3}{l}{\textit{Panel B. Complete regression coefficients}} \\",
        rf"Post $\times$ Treated & {_coef_cell(low)} & {_coef_cell(score_treated)} \\",
        rf" & {_se_cell(low)} & {_se_cell(score_treated)} \\",
        rf"Post $\times$ Predicted incidence & {_coef_cell(binary_common)} & {_coef_cell(score_common)} \\",
        rf" & {_se_cell(binary_common)} & {_se_cell(score_common)} \\",
        rf"Post $\times$ Treated $\times$ Predicted incidence & {_bold_coef_cell(ddd)} & {_bold_coef_cell(score_ddd)} \\",
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
        r"\fnote{Notes: Column (1) uses the binary high-predicted-incidence indicator; column (2) uses the mean-centered predicted-incidence score. In Panel A, the low- and high-incidence rows are directly estimated treated-control post contrasts, and the high-minus-low row is their DDD. These discrete group effects are not defined for column (2). In Panel B, Post $\times$ Predicted incidence is the common post shift across treated and control episodes; it is not a treatment effect. Boldface marks the focal DDD coefficients. In column (2), a one-unit change corresponds to moving across the full predicted-incidence scale. Standard errors, clustered by closure event (18 clusters), are in parentheses. All regressions omit the closure window. *** $p<0.01$, ** $p<0.05$, * $p<0.1$.}",
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
            r"\fnote{Notes: The unit is a member-closure episode. Pre-period purchase frequency is averaged over relative periods -4 to -1. Pre-period novelty-seeking is averaged over pre-period windows in which the member purchased at least one product. Difference is treatment minus control. Standard errors are heteroskedasticity-robust difference-in-means standard errors at the member-closure level. *** $p<0.01$, ** $p<0.05$, * $p<0.1$.}",
            r"\end{table}",
            "",
        ]
    )
    _print_snippet("treatment_control_balance", lines)


def _purchase_trend_with_period0() -> pd.DataFrame:
    sample = _load_sample(PURCHASE_DIR, "n_purchases")
    base = sample[["closure_event_id", "group", "rel_t", "n_purchases"]].copy()
    base = base.rename(columns={"n_purchases": "mean_source"})

    keys = ["member_id", "dept_id", "closure_start"]
    members = (
        sample[
            keys
            + [
                "closure_end",
                "closure_duration_days",
                "closure_event_id",
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
        parts.append(block[["closure_event_id", "group", "rel_t", "mean_source"]])

    panel = pd.concat([base, *parts], ignore_index=True)
    return _clustered_mean_summary(
        panel,
        value="mean_source",
        by=["group", "rel_t"],
    )


def write_closure_shock_figure() -> None:
    purchase_trend = _purchase_trend_with_period0()
    PAPER_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    purchase_trend.to_csv(PAPER_OUTPUT_DIR / "raw_purchase_paths.csv", index=False)

    fig, ax = plt.subplots(figsize=(7.2, 4.3))
    colors = {"control": "#1f77b4", "treatment": "#d62728"}
    labels = {"control": "Control", "treatment": "Treated"}
    marker_faces = {"control": "white", "treatment": colors["treatment"]}
    line_styles = {"control": "--", "treatment": "-"}

    for group in ["control", "treatment"]:
        sub = purchase_trend[purchase_trend["group"] == group].sort_values("rel_t")
        ax.errorbar(
            sub["rel_t"],
            sub["mean"],
            yerr=[sub["mean"] - sub["ci_low"], sub["ci_high"] - sub["mean"]],
            marker="o",
            linewidth=2,
            linestyle=line_styles[group],
            color=colors[group],
            markerfacecolor=marker_faces[group],
            markeredgecolor=colors[group],
            markeredgewidth=1.6,
            capsize=2.5,
            label=labels[group],
        )
    ax.axvspan(-0.45, 0.45, color="0.92", zorder=0)
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
    trend = _clustered_mean_summary(
        novelty,
        value="variety_seeking",
        by=["disp_binary", "treated", "rel_t"],
    )
    PAPER_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    trend.to_csv(PAPER_OUTPUT_DIR / "raw_novelty_paths.csv", index=False)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.3), sharex=True, sharey=True)
    colors = {0: "#1f77b4", 1: "#d62728"}
    labels = {0: "Control", 1: "Treated"}
    marker_faces = {0: "white", 1: colors[1]}
    line_styles = {0: "--", 1: "-"}
    panel_titles = {0: "Low predicted incidence", 1: "High predicted incidence"}

    for disp_binary, ax in zip([0, 1], axes):
        panel = trend[trend["disp_binary"] == disp_binary]
        for treated in [0, 1]:
            sub = panel[panel["treated"] == treated].sort_values("rel_t")
            ax.errorbar(
                sub["rel_t"],
                sub["mean"],
                yerr=[sub["mean"] - sub["ci_low"], sub["ci_high"] - sub["mean"]],
                marker="o",
                linewidth=2,
                linestyle=line_styles[treated],
                color=colors[treated],
                markerfacecolor=marker_faces[treated],
                markeredgecolor=colors[treated],
                markeredgewidth=1.6,
                capsize=2.5,
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


def write_purchase_probability_figure() -> None:
    novelty = pd.read_csv(NOVELTY_DIR / "estimation_sample.csv")
    novelty["treated"] = novelty["treated"].astype(int)
    novelty["disp_binary"] = novelty["disp_binary"].astype(int)
    novelty["rel_t"] = novelty["rel_t"].astype(int)
    novelty = novelty[novelty["rel_t"] != 0].copy()
    novelty["novelty_observed"] = novelty["variety_seeking"].notna().astype(float)
    trend = _clustered_mean_summary(
        novelty,
        value="novelty_observed",
        by=["disp_binary", "treated", "rel_t"],
    )
    trend = trend.rename(columns={"mean": "purchase_probability"})
    PAPER_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    trend.to_csv(PAPER_OUTPUT_DIR / "purchase_probability_paths.csv", index=False)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.3), sharex=True, sharey=True)
    colors = {0: "#1f77b4", 1: "#d62728"}
    labels = {0: "Control", 1: "Treated"}
    marker_faces = {0: "white", 1: colors[1]}
    line_styles = {0: "--", 1: "-"}
    panel_titles = {0: "Low predicted incidence", 1: "High predicted incidence"}

    for disp_binary, ax in zip([0, 1], axes):
        panel = trend[trend["disp_binary"] == disp_binary]
        for treated in [0, 1]:
            sub = panel[panel["treated"] == treated].sort_values("rel_t")
            ax.errorbar(
                sub["rel_t"],
                sub["purchase_probability"],
                yerr=[
                    sub["purchase_probability"] - sub["ci_low"],
                    sub["ci_high"] - sub["purchase_probability"],
                ],
                marker="o",
                linewidth=2,
                linestyle=line_styles[treated],
                color=colors[treated],
                markerfacecolor=marker_faces[treated],
                markeredgecolor=colors[treated],
                markeredgewidth=1.6,
                capsize=2.5,
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

    axes[0].set_ylabel("Probability of at least one purchase")
    axes[0].legend(frameon=False, loc="best")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "purchase_probability_paths.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def write_novelty_ddd_event_study_figure() -> None:
    rows = pd.read_csv(NOVELTY_DIR / "event_study_results.csv")
    rows["rel_t"] = rows["term"].str.extract(r"\[(-?\d+)\]")[0]
    rows["rel_t"] = pd.to_numeric(rows["rel_t"], errors="coerce")
    rows = rows.loc[
        (rows["spec"] == "event_binary_B")
        & rows["term"].str.endswith(":treated_X_disp")
        & rows["rel_t"].notna(),
        ["rel_t", "coef", "ci_low", "ci_high"],
    ].copy()
    rows["rel_t"] = rows["rel_t"].astype(int)
    reference = pd.DataFrame(
        [{"rel_t": -1, "coef": 0.0, "ci_low": 0.0, "ci_high": 0.0}]
    )
    rows = pd.concat([rows, reference], ignore_index=True).sort_values("rel_t")
    for col in ["coef", "ci_low", "ci_high"]:
        rows[col] = 100 * rows[col]

    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    ax.axhline(0, color="0.35", linewidth=1)
    ax.axvspan(-0.35, 0.35, color="0.92", zorder=0)
    ax.errorbar(
        rows["rel_t"],
        rows["coef"],
        yerr=[rows["coef"] - rows["ci_low"], rows["ci_high"] - rows["coef"]],
        fmt="o-",
        color="#1f4e79",
        markerfacecolor="#1f4e79",
        linewidth=1.7,
        markersize=5,
        capsize=3,
    )
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
    ax.set_xlabel("Relative period")
    ax.set_ylabel("High-minus-low DDD (percentage points)")
    ax.set_xticks([-4, -3, -2, -1, 0, 1, 2, 3, 4])
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "novelty_ddd_event_study.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def write_common_support_table() -> None:
    outcomes = [
        ("Purchase frequency", PURCHASE_DIR),
        ("Novelty-seeking", NOVELTY_DIR),
    ]
    table_rows = []
    for label, path in outcomes:
        full = _estimand_row(_coef_rows(path), "high_minus_low_ddd")
        matched_rows = pd.read_csv(path / "ddd_binary_results_matched.csv")
        matched = matched_rows.loc[
            (matched_rows["spec"] == "binary_collapsed")
            & (matched_rows["term"] == "post_X_treated_X_disp")
        ]
        if len(matched) != 1:
            raise ValueError(f"Expected one matched DDD row for {label}; found {len(matched)}.")
        table_rows.append((label, full, matched.iloc[0]))

    lines = [
        r"\begin{table}[H]",
        r"\centering",
        r"\caption{Common-support sensitivity of the DDD estimates}",
        r"\label{tab:appendix_common_support}",
        r"\small",
        r"\begin{tabularx}{\textwidth}{Xcccc}",
        r"\toprule",
        " & \\multicolumn{2}{c}{Full sample} & \\multicolumn{2}{c}{Matched common support} \\\\",
        r"\cmidrule(lr){2-3}\cmidrule(lr){4-5}",
        "Outcome & DDD & Observations & DDD & Observations \\\\",
        r"\midrule",
    ]
    for label, full, matched in table_rows:
        lines.append(
            f"{label} & {_bold_coef_cell(full)} & {int(full['n']):,} & "
            f"{_bold_coef_cell(matched)} & {int(matched['n']):,} \\\\"
        )
        lines.append(f" & {_se_cell(full)} & & {_se_cell(matched)} & \\\\ ")
    lines.extend(
        [
            r"\bottomrule",
            r"\end{tabularx}",
            r"\vspace{1mm}",
            r"\fnote{Notes: The table reports the high-minus-low DDD, with all DDD coefficients shown in boldface. The matched sample imposes common support between high- and low-predicted-incidence episodes separately within treated and control groups using coarsened cells in pre-period purchase frequency, the most recent pre-period purchase frequency and purchase recency; novelty additionally matches on pre-period purchase incidence because the outcome is defined only in purchasing windows. Standard errors are clustered by closure event (18 clusters). The matched estimates are sensitivity diagnostics rather than preferred estimates. *** $p<0.01$, ** $p<0.05$, * $p<0.1$.}",
            r"\end{table}",
            "",
        ]
    )
    _print_snippet("appendix_common_support", lines)


def _read_coef(path: Path, spec: str, term: str) -> tuple[float, float, float]:
    df = pd.read_csv(path)
    row = df[(df["spec"] == spec) & (df["term"] == term)].iloc[0]
    return float(row["coef"]), float(row["se"]), float(row["pvalue"])


def write_baseline_novelty_figures() -> None:
    summary = pd.read_csv(
        BASELINE_NOVELTY_DIR / "baseline_novelty_distribution_summary.csv"
    ).set_index("statistic")["value"]
    bins = pd.read_csv(
        BASELINE_NOVELTY_DIR / "baseline_novelty_distribution_bins.csv"
    )

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.bar(
        bins["bin_midpoint"],
        100 * bins["share"],
        width=0.088,
        color="#5b8db8",
        edgecolor="white",
        linewidth=0.8,
    )
    mean = float(summary.loc["mean"])
    ax.axvline(mean, color="#9c2f2f", linewidth=1.5)
    ax.text(
        mean + 0.015,
        ax.get_ylim()[1] * 0.94,
        f"Mean = {mean:.3f}",
        color="#7f2020",
        ha="left",
        va="top",
        fontsize=9,
    )
    ax.set_xlim(0, 1)
    ax.set_xticks(np.linspace(0, 1, 6))
    ax.set_xlabel("Baseline novelty-seeking")
    ax.set_ylabel("Share of eligible customer-closure episodes (percent)")
    ax.grid(axis="y", alpha=0.22)
    fig.tight_layout()
    fig.savefig(
        FIG_DIR / "baseline_novelty_distribution.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close(fig)

    event_study = pd.read_csv(
        BASELINE_NOVELTY_DIR / "baseline_novelty_event_study.csv"
    )
    reference = pd.DataFrame(
        [{"rel_t": -1, "estimate": 0.0, "ci_low": 0.0, "ci_high": 0.0}]
    )
    event_study = pd.concat([event_study, reference], ignore_index=True).sort_values(
        "rel_t"
    )
    for column in ["estimate", "ci_low", "ci_high"]:
        event_study[column] = 100 * event_study[column]

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.axhline(0, color="0.35", linewidth=1)
    ax.axvspan(-0.35, 0.35, color="0.92", zorder=0)
    ax.errorbar(
        event_study["rel_t"],
        event_study["estimate"],
        yerr=[
            event_study["estimate"] - event_study["ci_low"],
            event_study["ci_high"] - event_study["estimate"],
        ],
        fmt="o-",
        color="#1f4e79",
        markerfacecolor="#1f4e79",
        linewidth=1.7,
        markersize=5,
        capsize=3,
    )
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
    ax.set_xlabel("Relative period")
    ax.set_ylabel("Baseline-novelty gradient of the DDD\n(percentage points per SD)")
    ax.set_xticks([-4, -3, -2, -1, 0, 1, 2, 3, 4])
    ax.grid(axis="y", alpha=0.22)
    fig.tight_layout()
    fig.savefig(
        FIG_DIR / "baseline_novelty_event_study.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close(fig)


def validate_baseline_novelty_mechanism() -> None:
    results = pd.read_csv(BASELINE_NOVELTY_DIR / "baseline_novelty_results.csv")
    pretrend = pd.read_csv(BASELINE_NOVELTY_DIR / "baseline_novelty_pretrend_test.csv")
    distribution = pd.read_csv(
        BASELINE_NOVELTY_DIR / "baseline_novelty_distribution_summary.csv"
    ).set_index("statistic")["value"]
    headline = pd.read_csv(
        BASELINE_NOVELTY_DIR / "baseline_novelty_headline_results.csv"
    )
    no_order_results = pd.read_csv(
        BASELINE_NOVELTY_DIR
        / "baseline_novelty_results_without_order_adjustment.csv"
    )
    no_order_pretrend = pd.read_csv(
        BASELINE_NOVELTY_DIR
        / "baseline_novelty_pretrend_without_order_adjustment.csv"
    )
    order_diagnostic = pd.read_csv(
        BASELINE_NOVELTY_DIR / "baseline_order_diagnostic_summary.csv"
    ).set_index("statistic")["value"]
    order_groups = pd.read_csv(
        BASELINE_NOVELTY_DIR / "baseline_order_diagnostic_groups.csv"
    ).set_index("baseline_order_group")
    term = "post_X_treated_X_incidence_X_baseline_novelty"
    row = results.loc[results["term"] == term].iloc[0]
    no_order_row = no_order_results.loc[no_order_results["term"] == term].iloc[0]
    checks = {
        "theta": np.isclose(float(row["estimate"]), 0.029393510392843047, atol=5e-6),
        "se": np.isclose(float(row["se"]), 0.014742947467874495, atol=5e-6),
        "one_sided_p": np.isclose(
            float(row["pvalue_one_sided_positive"]), 0.03123908199511194, atol=5e-6
        ),
        "observations": int(row["n"]) == 79_578,
        "pretrend_p": np.isclose(float(pretrend.iloc[0]["pvalue"]), 0.5611208302311628, atol=5e-6),
        "eligible_episodes": int(distribution.loc["eligible_episodes"]) == 18_525,
        "distribution_mean": np.isclose(float(distribution.loc["mean"]), 0.5083409538),
        "distribution_sd": np.isclose(float(distribution.loc["sd"]), 0.2687628878),
        "headline_rows": len(headline) == 2,
        "no_order_theta": np.isclose(
            float(no_order_row["estimate"]), 0.0229269365, atol=5e-6
        ),
        "no_order_one_sided_p": np.isclose(
            float(no_order_row["pvalue_one_sided_positive"]),
            0.0636325223,
            atol=5e-6,
        ),
        "no_order_pretrend": np.isclose(
            float(no_order_pretrend.iloc[0]["pvalue"]), 0.4094134225, atol=5e-6
        ),
        "novelty_log_order_correlation": np.isclose(
            float(order_diagnostic.loc["pearson_novelty_log_orders"]),
            -0.3291597095,
            atol=5e-6,
        ),
        "five_order_mean_novelty": np.isclose(
            float(order_groups.loc["5", "mean_baseline_novelty"]),
            0.6203227304,
            atol=5e-6,
        ),
        "twenty_plus_mean_novelty": np.isclose(
            float(order_groups.loc["20+", "mean_baseline_novelty"]),
            0.3651570711,
            atol=5e-6,
        ),
    }
    if not all(checks.values()):
        raise AssertionError(f"Baseline-novelty mechanism values drifted: {checks}")
    print("\n% --- baseline_novelty_mechanism (validated; prose remains inline in main.tex) ---")
    print(
        f"% theta={float(row['estimate']):.6f}; SE={float(row['se']):.6f}; "
        f"one-sided p={float(row['pvalue_one_sided_positive']):.6f}; "
        f"pretrend p={float(pretrend.iloc[0]['pvalue']):.6f}; N={int(row['n']):,}"
    )


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
    write_purchase_probability_figure()
    write_novelty_ddd_event_study_figure()
    write_common_support_table()
    write_baseline_novelty_figures()
    validate_baseline_novelty_mechanism()
    write_magnitude_summary()


if __name__ == "__main__":
    main()
