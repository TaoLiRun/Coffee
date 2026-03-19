from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from scipy import stats

from data_processing import (
    DEFAULT_CLOSURE_TWO_GROUP_THRESHOLD,
    DEFAULT_LOWEST_PURCHASES,
    DEFAULT_LOWEST_RATIO,
    DEFAULT_WINDOW_DAYS,
    MAX_CLOSURE_DURATION_DAYS,
    MIN_CTRL_TREAT_RATIO,
    MIN_GROUP_SIZE,
    NO_PUSH_MEMBERS_PATH,
    OUTPUT_CUSTOMER_STORE_DIR,
    OUTPUT_DIR,
    ROBUSTNESS_WINDOW_DAYS,
    USE_SET_UP_TIME_MATCHED_CONTROL,
    PreparedData,
    _slice_by_date,
    build_date_sorted_index,
    filter_closures_shorter_than_max,
    get_control_stores_per_closure,
    get_never_treated_members,
    get_treatment_and_control_members_for_closure,
    load_store_set_up_times,
    DEPT_STATIC_PATH,
)


BEHAVIOR_METRICS = [
    ("n_purchases", "Purchase Days per Day"),
    ("new_product_ratio", "New Product Ratio"),
    ("total_discount", "Mean Total Discount"),
    ("coupon_usage_rate", "Coupon Usage Rate"),
]
PERIOD_ORDER = ["pre", "during", "post"]


def _compute_customer_behavior(
    df_commodity: pd.DataFrame,
    df_order: pd.DataFrame,
    member_ids: List,
    start_date,
    end_date,
    period_length_days: int,
) -> pd.DataFrame:
    if not member_ids:
        return pd.DataFrame()

    id_set = set(member_ids)
    result = pd.DataFrame({"member_id": member_ids})

    pc_date = _slice_by_date(df_commodity, start_date, end_date)
    pc = pc_date[pc_date["member_id"].isin(id_set)] if not pc_date.empty else pc_date

    po_date = _slice_by_date(df_order, start_date, end_date)
    po = po_date[po_date["member_id"].isin(id_set)] if not po_date.empty else po_date

    purchase_days = (
        pc[["member_id", "date"]].drop_duplicates()
        .groupby("member_id").size()
        .reindex(member_ids, fill_value=0)
        .astype(float)
    )
    result["purchase_days_count"] = purchase_days.values
    result["period_days"] = float(period_length_days)
    result["n_purchases"] = (purchase_days / period_length_days).values

    if not pc.empty:
        pcom_period = pc.dropna(subset=["product_name"])[["member_id", "product_name"]].drop_duplicates()
        if not pcom_period.empty:
            earliest_date = df_commodity["date"].iloc[0]
            history_end = (pd.Timestamp(start_date) - pd.Timedelta(days=1)).date()
            if history_end >= earliest_date:
                pc_hist = _slice_by_date(df_commodity, earliest_date, history_end)
                pc_hist_filt = (
                    pc_hist[pc_hist["member_id"].isin(id_set)]
                    .dropna(subset=["product_name"])[["member_id", "product_name"]]
                    .drop_duplicates()
                )
            else:
                pc_hist_filt = pd.DataFrame(columns=["member_id", "product_name"])

            merged = pcom_period.merge(
                pc_hist_filt.assign(_seen=True),
                on=["member_id", "product_name"],
                how="left",
            )
            merged["_is_new"] = merged["_seen"].isna()
            per_cust_new = merged.groupby("member_id").agg(
                _total=("product_name", "count"),
                _new=("_is_new", "sum"),
            )
            per_cust_new["new_product_ratio"] = per_cust_new["_new"] / per_cust_new["_total"]
            result["new_products_count"] = per_cust_new["_new"].reindex(member_ids, fill_value=0).values
            result["distinct_products_count"] = per_cust_new["_total"].reindex(member_ids, fill_value=0).values
            result["new_product_ratio"] = per_cust_new["new_product_ratio"].reindex(member_ids).values
        else:
            result["new_products_count"] = 0.0
            result["distinct_products_count"] = 0.0
            result["new_product_ratio"] = np.nan
    else:
        result["new_products_count"] = 0.0
        result["distinct_products_count"] = 0.0
        result["new_product_ratio"] = np.nan

    if not po.empty:
        discount_sum = po.groupby("member_id")["total_discount"].sum().reindex(member_ids, fill_value=0.0)
        order_count = po.groupby("member_id")["order_id"].count().reindex(member_ids, fill_value=0.0)
        coupon_used = po.groupby("member_id")["used_coupon"].sum().reindex(member_ids, fill_value=0.0)
        coupon_count = po.groupby("member_id")["used_coupon"].count().reindex(member_ids, fill_value=0.0)

        result["discount_sum"] = discount_sum.values
        result["order_count"] = order_count.values
        result["coupon_used_count"] = coupon_used.values
        result["coupon_order_count"] = coupon_count.values

        with np.errstate(divide="ignore", invalid="ignore"):
            result["total_discount"] = np.where(order_count.values > 0, discount_sum.values / order_count.values, np.nan)
            result["coupon_usage_rate"] = np.where(coupon_count.values > 0, coupon_used.values / coupon_count.values, np.nan)
    else:
        result["discount_sum"] = 0.0
        result["order_count"] = 0.0
        result["coupon_used_count"] = 0.0
        result["coupon_order_count"] = 0.0
        result["total_discount"] = np.nan
        result["coupon_usage_rate"] = np.nan

    return result


def analyze_closure_impact(
    df_commodity: pd.DataFrame,
    df_order: pd.DataFrame,
    closures: pd.DataFrame,
    customer_preference: pd.DataFrame,
    lowest_purchases: int = DEFAULT_LOWEST_PURCHASES,
    lowest_ratio: float = DEFAULT_LOWEST_RATIO,
    window_days: int = DEFAULT_WINDOW_DAYS,
    use_set_up_time_matched_control: bool = USE_SET_UP_TIME_MATCHED_CONTROL,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    print(f"\nAnalyzing closure impact (staggered DiD, window={window_days} days)...")
    print(f"  Config: lowest_purchases={lowest_purchases}, lowest_ratio={lowest_ratio}")
    print(f"  Control: use_set_up_time_matched_control={use_set_up_time_matched_control}")

    closures = filter_closures_shorter_than_max(
        closures,
        max_duration_days=MAX_CLOSURE_DURATION_DAYS,
        context=f"did_w{window_days}",
    )

    print("  Pre-sorting data by date for fast period slicing...")
    df_com_s = build_date_sorted_index(df_commodity)
    df_ord_s = build_date_sorted_index(df_order)

    unique_visits = df_commodity[["member_id", "date", "dept_id"]].drop_duplicates()

    if use_set_up_time_matched_control:
        store_df = load_store_set_up_times(DEPT_STATIC_PATH)
        treated_store_ids = set(closures["dept_id"].astype(int).unique())
        control_stores_by_closure = get_control_stores_per_closure(
            closures, store_df, n_nearest=5, treated_store_ids=treated_store_ids
        )
        control_pool = None
    else:
        control_pool = get_never_treated_members(
            closures, customer_preference, lowest_purchases, lowest_ratio
        )
        control_stores_by_closure = None

    summary_rows: List[Dict] = []
    period_frames: List[pd.DataFrame] = []

    for _, closure in closures.iterrows():
        dept_id = int(closure["dept_id"])
        closure_start = pd.to_datetime(closure["closure_start"])
        closure_end = pd.to_datetime(closure["closure_end"])

        pre_start = (closure_start - pd.Timedelta(days=window_days)).date()
        pre_end = (closure_start - pd.Timedelta(days=1)).date()
        dur_start = closure_start.date()
        dur_end = closure_end.date()
        post_start = (closure_end + pd.Timedelta(days=1)).date()
        post_end = (closure_end + pd.Timedelta(days=window_days)).date()

        treatment, closure_control, control_store_ids = get_treatment_and_control_members_for_closure(
            unique_visits=unique_visits,
            customer_preference=customer_preference,
            closure=closure,
            lowest_purchases=lowest_purchases,
            lowest_ratio=lowest_ratio,
            use_set_up_time_matched_control=use_set_up_time_matched_control,
            control_pool=control_pool,
            control_stores_by_closure=control_stores_by_closure,
        )

        if not treatment or not closure_control:
            continue
        if len(treatment) < MIN_GROUP_SIZE or len(closure_control) < MIN_GROUP_SIZE:
            continue

        during_slice = _slice_by_date(df_com_s, dur_start, dur_end)
        during_purch = during_slice[["member_id"]].drop_duplicates()
        t_rate = during_purch["member_id"].isin(treatment).sum() / len(treatment)
        c_rate = during_purch["member_id"].isin(closure_control).sum() / len(closure_control)
        if c_rate < MIN_CTRL_TREAT_RATIO * t_rate:
            continue

        closure_duration = int(closure["closure_duration_days"])
        period_lengths = {
            "pre": window_days,
            "during": max(closure_duration, 1),
            "post": window_days,
        }

        for group_label, members in [("treatment", treatment), ("control", closure_control)]:
            for period_label, s, e in [
                ("pre", pre_start, pre_end),
                ("during", dur_start, dur_end),
                ("post", post_start, post_end),
            ]:
                cust_df = _compute_customer_behavior(
                    df_com_s, df_ord_s, members, s, e, period_length_days=period_lengths[period_label]
                )
                if not cust_df.empty:
                    cust_df["dept_id"] = dept_id
                    cust_df["closure_start"] = closure["closure_start"]
                    cust_df["window_days"] = window_days
                    cust_df["closure_duration_days"] = closure["closure_duration_days"]
                    cust_df["group"] = group_label
                    cust_df["period"] = period_label
                    period_frames.append(cust_df)

        summary_rows.append({
            "dept_id": dept_id,
            "closure_start": closure["closure_start"],
            "closure_end": closure["closure_end"],
            "closure_duration_days": closure["closure_duration_days"],
            "window_days": window_days,
            "#treatment": len(treatment),
            "#control": len(closure_control),
            "treatment_purchase_rate_during": t_rate,
            "control_purchase_rate_during": c_rate,
            "selectivity_ratio": t_rate / c_rate if c_rate and c_rate > 0 else np.nan,
        })

    summary_df = pd.DataFrame(summary_rows).sort_values("closure_start").reset_index(drop=True)
    period_df_out = pd.concat(period_frames, ignore_index=True) if period_frames else pd.DataFrame()
    print(f"\n  Analyzed {len(summary_df)} closures.")
    return summary_df, period_df_out


def _aggregate_period_metrics(period_slice: pd.DataFrame) -> pd.DataFrame:
    group_keys = ["dept_id", "closure_start", "closure_duration_days", "group", "member_id"]
    agg = period_slice.groupby(group_keys, as_index=False).agg(
        purchase_days_count=("purchase_days_count", "sum"),
        period_days=("period_days", "sum"),
        new_products_count=("new_products_count", "sum"),
        distinct_products_count=("distinct_products_count", "sum"),
        discount_sum=("discount_sum", "sum"),
        order_count=("order_count", "sum"),
        coupon_used_count=("coupon_used_count", "sum"),
        coupon_order_count=("coupon_order_count", "sum"),
    )
    with np.errstate(divide="ignore", invalid="ignore"):
        agg["n_purchases"] = np.where(agg["period_days"] > 0, agg["purchase_days_count"] / agg["period_days"], np.nan)
        agg["new_product_ratio"] = np.where(agg["distinct_products_count"] > 0, agg["new_products_count"] / agg["distinct_products_count"], np.nan)
        agg["total_discount"] = np.where(agg["order_count"] > 0, agg["discount_sum"] / agg["order_count"], np.nan)
        agg["coupon_usage_rate"] = np.where(agg["coupon_order_count"] > 0, agg["coupon_used_count"] / agg["coupon_order_count"], np.nan)
    return agg


def build_period_panel_from_event_panel(event_panel: pd.DataFrame, window_days: int) -> pd.DataFrame:
    if event_panel is None or event_panel.empty:
        return pd.DataFrame()

    required_cols = {
        "dept_id", "closure_start", "closure_duration_days", "group", "member_id", "t",
        "purchase_days_count", "period_days", "new_products_count", "distinct_products_count",
        "discount_sum", "order_count", "coupon_used_count", "coupon_order_count",
        "n_purchases", "new_product_ratio", "total_discount", "coupon_usage_rate",
    }
    missing_cols = sorted(required_cols - set(event_panel.columns))
    if missing_cols:
        raise ValueError(
            "event_panel is missing required columns for period aggregation: "
            f"{missing_cols}"
        )

    window_weeks = int(window_days // 7)
    needed = event_panel[event_panel["t"].isin(list(range(-window_weeks, 0)) + [0] + list(range(1, window_weeks + 1)))].copy()
    if needed.empty:
        return pd.DataFrame()

    pre_raw = needed[needed["t"].between(-window_weeks, -1)]
    post_raw = needed[needed["t"].between(1, window_weeks)]
    during_raw = needed[needed["t"] == 0].copy()

    pre = _aggregate_period_metrics(pre_raw)
    pre["period"] = "pre"

    post = _aggregate_period_metrics(post_raw)
    post["period"] = "post"

    during = during_raw[[
        "dept_id", "closure_start", "closure_duration_days", "group", "member_id",
        "purchase_days_count", "period_days", "new_products_count", "distinct_products_count",
        "discount_sum", "order_count", "coupon_used_count", "coupon_order_count",
        "n_purchases", "new_product_ratio", "total_discount", "coupon_usage_rate",
    ]].copy()
    during["period"] = "during"

    period_df = pd.concat([pre, during, post], ignore_index=True)
    period_df["window_days"] = window_days
    return period_df


def summarize_closure_from_period(period_df: pd.DataFrame, window_days: int) -> pd.DataFrame:
    if period_df is None or period_df.empty:
        return pd.DataFrame()

    during = period_df[(period_df["window_days"] == window_days) & (period_df["period"] == "during")].copy()
    if during.empty:
        return pd.DataFrame()

    during["purchased_during"] = (during["n_purchases"].fillna(0) > 0).astype(float)
    closure_group = during.groupby(["dept_id", "closure_start", "closure_duration_days", "group"], as_index=False).agg(
        n_members=("member_id", "nunique"),
        purchase_rate_during=("purchased_during", "mean"),
    )

    treat = closure_group[closure_group["group"] == "treatment"].rename(
        columns={"n_members": "#treatment", "purchase_rate_during": "treatment_purchase_rate_during"}
    )
    ctrl = closure_group[closure_group["group"] == "control"].rename(
        columns={"n_members": "#control", "purchase_rate_during": "control_purchase_rate_during"}
    )

    out = treat.merge(
        ctrl[["dept_id", "closure_start", "#control", "control_purchase_rate_during"]],
        on=["dept_id", "closure_start"],
        how="inner",
    )
    out["window_days"] = window_days
    out["selectivity_ratio"] = np.where(
        out["control_purchase_rate_during"] > 0,
        out["treatment_purchase_rate_during"] / out["control_purchase_rate_during"],
        np.nan,
    )
    out = out[[
        "dept_id", "closure_start", "closure_duration_days", "window_days",
        "#treatment", "#control",
        "treatment_purchase_rate_during", "control_purchase_rate_during", "selectivity_ratio",
    ]].sort_values("closure_start").reset_index(drop=True)
    return out


def _sig_stars(pvalue: float) -> str:
    if np.isnan(pvalue):
        return "n/a"
    if pvalue < 0.001:
        return "***"
    if pvalue < 0.01:
        return "**"
    if pvalue < 0.05:
        return "*"
    return "ns"


def _cust_vals(df: pd.DataFrame, group: str, period: str, metric: str, deduplicate: bool = False) -> pd.Series:
    sub = df[(df["group"] == group) & (df["period"] == period)][["member_id", metric]].dropna()
    if deduplicate:
        return sub.groupby("member_id")[metric].mean()
    return sub.groupby("member_id")[metric].mean()


def _paired_ttest(df: pd.DataFrame, group: str, period_a: str, period_b: str, metric: str) -> Tuple[float, int]:
    a = _cust_vals(df, group, period_a, metric, deduplicate=True)
    b = _cust_vals(df, group, period_b, metric, deduplicate=True)
    common = a.index.intersection(b.index)
    if len(common) < 2:
        return np.nan, len(common)
    return float(stats.ttest_rel(a[common], b[common]).pvalue), len(common)


def _between_group_ttest(df: pd.DataFrame, period: str, metric: str) -> Tuple[float, int, int]:
    t_vals = _cust_vals(df, "treatment", period, metric, deduplicate=False)
    c_vals = _cust_vals(df, "control", period, metric, deduplicate=True)
    if len(t_vals) < 2 or len(c_vals) < 2:
        return np.nan, len(t_vals), len(c_vals)
    return float(stats.ttest_ind(t_vals, c_vals, equal_var=False).pvalue), len(t_vals), len(c_vals)


def run_statistical_tests(period_df: pd.DataFrame, window_days: int = DEFAULT_WINDOW_DAYS) -> pd.DataFrame:
    df = period_df[period_df["window_days"] == window_days].copy()
    if df.empty:
        return pd.DataFrame()

    rows: List[Dict] = []
    for metric, _ in BEHAVIOR_METRICS:
        p, n = _paired_ttest(df, "treatment", "pre", "post", metric)
        rows.append({"metric": metric, "comparison": "treat_pre_vs_post", "n": n, "pvalue": p, "stars": _sig_stars(p)})

        p, n = _paired_ttest(df, "control", "pre", "post", metric)
        rows.append({"metric": metric, "comparison": "ctrl_pre_vs_post", "n": n, "pvalue": p, "stars": _sig_stars(p)})

        p, nt, nc = _between_group_ttest(df, "pre", metric)
        rows.append({"metric": metric, "comparison": "T_vs_C_in_pre", "n": nt + nc, "pvalue": p, "stars": _sig_stars(p)})

        p, nt, nc = _between_group_ttest(df, "post", metric)
        rows.append({"metric": metric, "comparison": "T_vs_C_in_post", "n": nt + nc, "pvalue": p, "stars": _sig_stars(p)})

    return pd.DataFrame(rows)


def _add_bracket(ax, x1: float, x2: float, y: float, text: str, tick: float = 0.0, fontsize: int = 8, color: str = "black") -> None:
    ax.plot([x1, x1, x2, x2], [y, y + tick, y + tick, y], lw=0.9, c=color, clip_on=False)
    ax.text((x1 + x2) / 2, y + tick, text, ha="center", va="bottom", fontsize=fontsize, color=color)


def visualize_behavior_comparison(
    period_df: pd.DataFrame,
    window_days: int = DEFAULT_WINDOW_DAYS,
    tag: str = "",
    test_results: Optional[pd.DataFrame] = None,
) -> None:
    if period_df is None or period_df.empty:
        return
    df = period_df[period_df["window_days"] == window_days].copy()
    if df.empty:
        return
    if test_results is None or test_results.empty:
        test_results = run_statistical_tests(period_df, window_days)

    def _get_sig(metric: str, comparison: str) -> str:
        row = test_results[(test_results["metric"] == metric) & (test_results["comparison"] == comparison)]
        return row["stars"].values[0] if len(row) else ""

    n_metrics = len(BEHAVIOR_METRICS)
    x = np.arange(len(PERIOD_ORDER))
    width = 0.35
    colors = {"treatment": "#d62728", "control": "#1f77b4"}
    suffix = f"_w{window_days}" + (f"_{tag}" if tag else "")

    def _get_mean_std(grp_df: pd.DataFrame, metric: str) -> Tuple[List, List]:
        means, stds = [], []
        for period in PERIOD_ORDER:
            sub = grp_df[grp_df["period"] == period][["member_id", metric]].dropna()
            per_cust = sub.groupby("member_id")[metric].mean()
            means.append(float(per_cust.mean()) if len(per_cust) else np.nan)
            stds.append(float(per_cust.std()) if len(per_cust) > 1 else 0.0)
        return means, stds

    def _annotate_ax(ax, metric: str) -> None:
        half = width / 2
        x_tp = x[0] - half
        x_cp = x[0] + half
        x_tpo = x[2] - half
        x_cpo = x[2] + half
        all_means_stds: List[float] = []
        for group in ["treatment", "control"]:
            grp = df[df["group"] == group]
            means, stds = _get_mean_std(grp, metric)
            for m, s in zip(means, stds):
                if not np.isnan(m):
                    all_means_stds.append(m + (s if not np.isnan(s) else 0))
        y_data_top = max(all_means_stds) if all_means_stds else 0.0
        step = max(abs(y_data_top) * 0.08, 1e-6)
        tick = step * 0.25

        h1 = y_data_top + step
        s_tcp = _get_sig(metric, "T_vs_C_in_pre")
        s_tcpo = _get_sig(metric, "T_vs_C_in_post")
        if s_tcp:
            _add_bracket(ax, x_tp, x_cp, h1, s_tcp, tick=tick, fontsize=7, color="#444444")
        if s_tcpo:
            _add_bracket(ax, x_tpo, x_cpo, h1, s_tcpo, tick=tick, fontsize=7, color="#444444")

        h2 = h1 + step * 2.2
        s_treat = _get_sig(metric, "treat_pre_vs_post")
        s_ctrl = _get_sig(metric, "ctrl_pre_vs_post")
        if s_treat:
            _add_bracket(ax, x_tp, x_tpo, h2, s_treat, tick=tick, fontsize=7, color=colors["treatment"])
        if s_ctrl:
            _add_bracket(ax, x_cp, x_cpo, h2 + step * 0.9, s_ctrl, tick=tick, fontsize=7, color=colors["control"])
        ylo, _ = ax.get_ylim()
        ax.set_ylim(ylo, h2 + step * 2.5)

    fig, axes = plt.subplots(1, n_metrics, figsize=(5 * n_metrics, 6))
    if n_metrics == 1:
        axes = [axes]

    for ax, (metric, metric_label) in zip(axes, BEHAVIOR_METRICS):
        for i, group in enumerate(["treatment", "control"]):
            grp = df[df["group"] == group]
            means, stds = _get_mean_std(grp, metric)
            offset = (i - 0.5) * width
            ax.bar(
                x + offset, means, width,
                label=group.capitalize(), color=colors[group], alpha=0.75,
                yerr=stds, capsize=4,
                error_kw={"elinewidth": 1, "ecolor": "black"},
            )
        ax.set_xticks(x)
        ax.set_xticklabels(["Pre", "During", "Post"], fontsize=11)
        ax.set_ylabel(metric_label, fontsize=10)
        ax.set_title(metric_label, fontsize=11, fontweight="bold")
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3, axis="y")
        ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.2f"))
        _annotate_ax(ax, metric)

    plt.tight_layout(rect=[0, 0, 1, 0.90])
    combined_path = OUTPUT_DIR / f"behavior_comparison{suffix}.pdf"
    plt.savefig(combined_path, dpi=300, bbox_inches="tight")
    plt.close()


def visualize_behavior_comparison_by_duration_split(
    period_df: pd.DataFrame,
    window_days: int = DEFAULT_WINDOW_DAYS,
    threshold_days: int = DEFAULT_CLOSURE_TWO_GROUP_THRESHOLD,
    tag: str = "",
) -> None:
    if period_df is None or period_df.empty or "closure_duration_days" not in period_df.columns:
        return
    df_w = period_df[period_df["window_days"] == window_days]
    short = df_w[df_w["closure_duration_days"] < threshold_days]
    long_ = df_w[df_w["closure_duration_days"] >= threshold_days]

    base_tag = (f"_{tag}" if tag else "")
    if not short.empty:
        visualize_behavior_comparison(short, window_days=window_days, tag=f"short_lt{threshold_days}{base_tag}")
    if not long_.empty:
        visualize_behavior_comparison(long_, window_days=window_days, tag=f"long_ge{threshold_days}{base_tag}")


def load_no_push_member_ids() -> set:
    if not NO_PUSH_MEMBERS_PATH.exists():
        return set()
    df = pd.read_csv(NO_PUSH_MEMBERS_PATH, encoding="utf-8-sig")
    return set(df["member_id"].unique())


def visualize_behavior_comparison_push_split(
    period_df: pd.DataFrame,
    no_push_ids: set,
    window_days: int = DEFAULT_WINDOW_DAYS,
    tag: str = "",
) -> None:
    if period_df is None or period_df.empty or not no_push_ids:
        return
    df = period_df[period_df["window_days"] == window_days].copy()
    if df.empty:
        return

    treat_mask = df["group"] == "treatment"
    df.loc[treat_mask & df["member_id"].isin(no_push_ids), "group"] = "treatment_no_push"
    df.loc[treat_mask & ~df["member_id"].isin(no_push_ids), "group"] = "treatment_with_push"

    groups_to_plot = ["treatment_no_push", "treatment_with_push", "control"]
    colors = {
        "treatment_no_push": "#ff7f0e",
        "treatment_with_push": "#d62728",
        "control": "#1f77b4",
    }
    labels = {
        "treatment_no_push": "Treat (no push)",
        "treatment_with_push": "Treat (with push)",
        "control": "Control",
    }
    suffix = f"_w{window_days}_push_split" + (f"_{tag}" if tag else "")

    def _get_mean_std_push(grp: str, metric: str) -> Tuple[List, List]:
        means, stds = [], []
        for period in PERIOD_ORDER:
            sub = df[(df["group"] == grp) & (df["period"] == period)][["member_id", metric]].dropna()
            per_cust = sub.groupby("member_id")[metric].mean()
            means.append(float(per_cust.mean()) if len(per_cust) else np.nan)
            stds.append(float(per_cust.std()) if len(per_cust) > 1 else 0.0)
        return means, stds

    n_metrics = len(BEHAVIOR_METRICS)
    x = np.arange(len(PERIOD_ORDER))
    width = 0.25
    fig, axes = plt.subplots(1, n_metrics, figsize=(5 * n_metrics, 6))
    if n_metrics == 1:
        axes = [axes]

    for ax, (metric, metric_label) in zip(axes, BEHAVIOR_METRICS):
        for i, grp in enumerate(groups_to_plot):
            means, stds = _get_mean_std_push(grp, metric)
            offset = (i - (len(groups_to_plot) - 1) / 2) * width
            centres = x + offset
            ax.bar(
                centres, means, width,
                label=labels[grp], color=colors[grp], alpha=0.75,
                yerr=stds, capsize=3,
                error_kw={"elinewidth": 1, "ecolor": "black"},
            )
        ax.set_xticks(x)
        ax.set_xticklabels(["Pre", "During", "Post"], fontsize=11)
        ax.set_ylabel(metric_label, fontsize=10)
        ax.set_title(metric_label, fontsize=11, fontweight="bold")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3, axis="y")
        ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.2f"))

    plt.tight_layout(rect=[0, 0, 1, 0.90])
    out_path = OUTPUT_DIR / f"behavior_comparison{suffix}.pdf"
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()


def merge_with_closures(impact_df: pd.DataFrame, closures: pd.DataFrame) -> pd.DataFrame:
    closure_cols = [
        "dept_id", "closure_start", "closure_end", "closure_duration_days",
        "latitude", "longitude", "address",
    ]
    available = [c for c in closure_cols if c in closures.columns]
    join_keys = [c for c in ["dept_id", "closure_start", "closure_end", "closure_duration_days"] if c in available and c in impact_df.columns]
    result = impact_df.merge(closures[available], on=join_keys, how="left")
    return result.loc[:, ~result.columns.duplicated()]


def run_staggered_did(
    prepared: PreparedData,
    window_days: int,
    lowest_purchases: int = DEFAULT_LOWEST_PURCHASES,
    lowest_ratio: float = DEFAULT_LOWEST_RATIO,
    use_set_up_time_matched_control: bool = USE_SET_UP_TIME_MATCHED_CONTROL,
    event_panel: Optional[pd.DataFrame] = None,
    save_summary_csv: bool = True,
    save_stat_tests_csv: bool = True,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    if event_panel is not None and not event_panel.empty:
        period_df = build_period_panel_from_event_panel(event_panel, window_days=window_days)
        summary_df = summarize_closure_from_period(period_df, window_days=window_days)
    else:
        summary_df, period_df = analyze_closure_impact(
            prepared.df_commodity,
            prepared.df_order,
            prepared.closures,
            prepared.customer_preference,
            lowest_purchases=lowest_purchases,
            lowest_ratio=lowest_ratio,
            window_days=window_days,
            use_set_up_time_matched_control=use_set_up_time_matched_control,
        )

    final_df = merge_with_closures(summary_df, prepared.closures)
    tests_df = run_statistical_tests(period_df, window_days=window_days)

    if save_summary_csv:
        out_summary = OUTPUT_CUSTOMER_STORE_DIR / f"closure_impact_did_p{lowest_purchases}_r{int(lowest_ratio*100)}_w{window_days}.csv"
        out_summary.parent.mkdir(parents=True, exist_ok=True)
        final_df.to_csv(out_summary, index=False, encoding="utf-8-sig")

    if save_stat_tests_csv and not tests_df.empty:
        out_tests = OUTPUT_CUSTOMER_STORE_DIR / f"stat_tests_p{lowest_purchases}_r{int(lowest_ratio*100)}_w{window_days}.csv"
        out_tests.parent.mkdir(parents=True, exist_ok=True)
        tests_df.to_csv(out_tests, index=False, encoding="utf-8-sig")

    visualize_behavior_comparison(
        period_df,
        window_days=window_days,
        tag="" if window_days == DEFAULT_WINDOW_DAYS else "robustness",
        test_results=tests_df,
    )
    visualize_behavior_comparison_by_duration_split(
        period_df,
        window_days=window_days,
        threshold_days=DEFAULT_CLOSURE_TWO_GROUP_THRESHOLD,
        tag="" if window_days == DEFAULT_WINDOW_DAYS else "robustness",
    )
    no_push_ids = load_no_push_member_ids()
    visualize_behavior_comparison_push_split(
        period_df,
        no_push_ids=no_push_ids,
        window_days=window_days,
        tag="" if window_days == DEFAULT_WINDOW_DAYS else "robustness",
    )
    return final_df, tests_df


def run_did_for_windows(
    prepared: PreparedData,
    windows: tuple[int, ...] = (DEFAULT_WINDOW_DAYS, ROBUSTNESS_WINDOW_DAYS),
    lowest_purchases: int = DEFAULT_LOWEST_PURCHASES,
    lowest_ratio: float = DEFAULT_LOWEST_RATIO,
    use_set_up_time_matched_control: bool = USE_SET_UP_TIME_MATCHED_CONTROL,
    event_panel: Optional[pd.DataFrame] = None,
) -> Dict[int, pd.DataFrame]:
    summaries: Dict[int, pd.DataFrame] = {}
    for w in windows:
        summary_df, _ = run_staggered_did(
            prepared=prepared,
            window_days=w,
            lowest_purchases=lowest_purchases,
            lowest_ratio=lowest_ratio,
            use_set_up_time_matched_control=use_set_up_time_matched_control,
            event_panel=event_panel,
            save_summary_csv=True,
            save_stat_tests_csv=True,
        )
        summaries[w] = summary_df
    return summaries


def main() -> None:
    from data_processing import build_week_level_panel, prepare_shared_data

    prepared = prepare_shared_data(
        lowest_purchases=DEFAULT_LOWEST_PURCHASES,
        lowest_ratio=DEFAULT_LOWEST_RATIO,
    )

    shared_event_panel = build_week_level_panel(
        df_commodity=prepared.df_commodity,
        df_order=prepared.df_order,
        closures=prepared.closures,
        customer_preference=prepared.customer_preference,
        window_weeks=4,
        lowest_purchases=DEFAULT_LOWEST_PURCHASES,
        lowest_ratio=DEFAULT_LOWEST_RATIO,
        use_set_up_time_matched_control=USE_SET_UP_TIME_MATCHED_CONTROL,
    )

    run_did_for_windows(
        prepared=prepared,
        windows=(DEFAULT_WINDOW_DAYS, ROBUSTNESS_WINDOW_DAYS),
        lowest_purchases=DEFAULT_LOWEST_PURCHASES,
        lowest_ratio=DEFAULT_LOWEST_RATIO,
        use_set_up_time_matched_control=USE_SET_UP_TIME_MATCHED_CONTROL,
        event_panel=shared_event_panel,
    )


if __name__ == "__main__":
    main()
