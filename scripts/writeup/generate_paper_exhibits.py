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
    return pd.read_csv(path / "ddd_binary_results.csv").set_index("term")


def _coef_cell(row: pd.Series) -> str:
    return f"{_fmt(float(row['coef']), 4)}{_stars(float(row['pvalue']))}"


def _se_cell(row: pd.Series) -> str:
    return f"({_fmt(float(row['se']), 4)})"


def write_main_results_decomposition_table() -> None:
    purchase = _coef_rows(PURCHASE_DIR)
    novelty = _coef_rows(NOVELTY_DIR)
    purchase_high = float(purchase.loc["post_X_treated", "coef"] + purchase.loc["post_X_treated_X_disp", "coef"])
    novelty_high = float(novelty.loc["post_X_treated", "coef"] + novelty.loc["post_X_treated_X_disp", "coef"])

    lines = [
        r"\begin{table}[h!]",
        r"\centering",
        r"\caption{Decomposition of main results}",
        r"\label{tab:main_results_decomposition}",
        r"\small",
        r"\begin{tabular}{lcc}",
        r"\toprule",
        r"Component & Purchase frequency & Novelty-seeking \\",
        r"\midrule",
        rf"Baseline closure exposure, low-intention ($\delta^B$) & {_coef_cell(purchase.loc['post_X_treated'])} & {_coef_cell(novelty.loc['post_X_treated'])} \\",
        rf" & {_se_cell(purchase.loc['post_X_treated'])} & {_se_cell(novelty.loc['post_X_treated'])} \\",
        rf"Common high-intention post shift ($\beta$) & {_coef_cell(purchase.loc['post_X_disp'])} & {_coef_cell(novelty.loc['post_X_disp'])} \\",
        rf" & {_se_cell(purchase.loc['post_X_disp'])} & {_se_cell(novelty.loc['post_X_disp'])} \\",
        rf"Blocked-intention effect ($\delta^D$) & {_coef_cell(purchase.loc['post_X_treated_X_disp'])} & {_coef_cell(novelty.loc['post_X_treated_X_disp'])} \\",
        rf" & {_se_cell(purchase.loc['post_X_treated_X_disp'])} & {_se_cell(novelty.loc['post_X_treated_X_disp'])} \\",
        r"\addlinespace",
        rf"Implied treatment effect for high-intention episodes ($\delta^B+\delta^D$) & {_fmt(purchase_high, 4)} & {_fmt(novelty_high, 4)} \\",
        rf"Observations & {int(purchase['n'].iloc[0]):,} & {int(novelty['n'].iloc[0]):,} \\",
        rf"Within $R^2$ & {_fmt(float(purchase['r2_within'].iloc[0]), 3)} & {_fmt(float(novelty['r2_within'].iloc[0]), 3)} \\",
        r"\bottomrule",
        r"\end{tabular}",
        r"\vspace{1mm}",
        r"\fnote{Notes: The first three rows report coefficients from the binary triple-differences specification. Standard errors, clustered at the individual level, are in parentheses. The high-intention indicator is the ex-ante predicted purchase-intention indicator. The blocked-intention effect applies to treated high-intention episodes, where the closure is predicted to interrupt a planned purchase. The final row is the arithmetic sum of the baseline closure effect and the blocked-intention effect; no separate standard error is reported for this sum. *** $p<0.01$, ** $p<0.05$, * $p<0.1$.}",
        r"\end{table}",
        "",
    ]
    _print_snippet("main_results_decomposition", lines)


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
    novelty_trend = pd.read_csv(NOVELTY_DIR / "variety_panel_trend_stats.csv")

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.3), sharex=True)
    colors = {"control": "#1f77b4", "treatment": "#d62728"}
    labels = {"control": "Control", "treatment": "Treated"}
    panels = [
        (axes[0], purchase_trend, "Purchase frequency", "Purchase days per calendar day"),
        (axes[1], novelty_trend, "Novelty-seeking", "Share of products new to member"),
    ]
    for ax, trend, title, ylabel in panels:
        for group in ["control", "treatment"]:
            sub = trend[trend["group"] == group].sort_values("rel_t")
            ax.plot(
                sub["rel_t"],
                sub["mean"],
                marker="o",
                linewidth=2,
                color=colors[group],
                label=labels[group],
            )
        ax.axvline(0, color="0.45", linestyle="--", linewidth=1)
        ax.set_title(title)
        ax.set_xlabel("Relative period")
        ax.set_ylabel(ylabel)
        ax.set_xticks([-4, -3, -2, -1, 0, 1, 2, 3, 4])
        ax.grid(axis="y", alpha=0.25)
    axes[0].legend(frameon=False, loc="best")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "closure_shock_purchase_novelty.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def _read_coef(path: Path, spec: str, term: str) -> tuple[float, float, float]:
    df = pd.read_csv(path)
    row = df[(df["spec"] == spec) & (df["term"] == term)].iloc[0]
    return float(row["coef"]), float(row["se"]), float(row["pvalue"])


def write_market_new_table() -> None:
    rows = [
        (
            "Baseline treatment effect",
            *_read_coef(MARKET_NEW_DIR / "ddd_binary_results.csv", "binary_collapsed", "post_X_treated"),
        ),
        (
            "High-intention post shift",
            *_read_coef(MARKET_NEW_DIR / "ddd_binary_results.csv", "binary_collapsed", "post_X_disp"),
        ),
        (
            "Displacement effect",
            *_read_coef(MARKET_NEW_DIR / "ddd_binary_results.csv", "binary_collapsed", "post_X_treated_X_disp"),
        ),
        (
            "Continuous-score displacement slope",
            *_read_coef(MARKET_NEW_DIR / "ddd_score_results.csv", "score_collapsed", "post_X_treated_X_score"),
        ),
    ]
    lines = [
        r"\begin{table}[h!]",
        r"\centering",
        r"\caption{Robustness: market-new novelty}",
        r"\label{tab:market_new_robustness}",
        r"\small",
        r"\begin{tabular}{lcc}",
        r"\toprule",
        r"Coefficient & Estimate & SE \\",
        r"\midrule",
    ]
    for label, coef, se, pvalue in rows:
        lines.append(f"{label} & {_fmt(coef)}{_stars(pvalue)} & {_fmt(se)} \\\\")
    lines.extend(
        [
            r"\bottomrule",
            r"\end{tabular}",
            r"\vspace{1mm}",
            r"\fnote{Notes: The dependent variable is market-new novelty, defined as the share of purchased products whose first observed catalog introduction occurs in the current or immediately previous event window. The first three rows use the binary high-intention triple-differences specification; the last row replaces the high-intention indicator with the continuous predicted purchase-intention probability. Standard errors are clustered at the individual level. *** $p<0.01$, ** $p<0.05$, * $p<0.1$.}",
            r"\end{table}",
            "",
        ]
    )
    _print_snippet("market_new_robustness", lines)


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
    _print_snippet("pre_novelty_heterogeneity", lines)


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
            "outcome": "member_first_novelty",
            "coef": novelty_coef,
            "se": novelty_se,
            "pvalue": novelty_p,
            "pre_mean": novelty.loc[novelty["rel_t"] < 0, "variety_seeking"].mean(),
        },
        {
            "outcome": "market_new_novelty",
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
    write_balance_table()
    write_closure_shock_figure()
    write_market_new_table()
    write_heterogeneity_table()
    write_magnitude_summary()


if __name__ == "__main__":
    main()
