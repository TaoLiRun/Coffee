from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from data_processing import (
    CLOSURES_CSV,
    DEFAULT_LOWEST_PURCHASES,
    DEFAULT_LOWEST_RATIO,
    MAX_CLOSURE_DURATION_DAYS,
    MIN_CTRL_TREAT_RATIO,
    MIN_GROUP_SIZE,
    OUTPUT_CUSTOMER_STORE_DIR,
    OUTPUT_DIR,
    USE_SET_UP_TIME_MATCHED_CONTROL,
    PreparedData,
    build_week_level_panel,
    filter_closures_shorter_than_max,
    load_order_commodity_data,
    load_order_result_data,
    get_customer_store_preference,
    subset_week_level_panel,
)


METRICS = [
    ("n_purchases_per_week", "Purchases per Week", True),
    ("new_product_ratio", "New Product Ratio", False),
    ("total_discount", "Mean Total Discount", False),
    ("coupon_usage_rate", "Coupon Usage Rate", False),
]

def aggregate_by_group_t(panel: pd.DataFrame) -> pd.DataFrame:
    metrics = ["n_purchases_per_week", "new_product_ratio", "total_discount", "coupon_usage_rate"]
    agg_dict = {}
    for m in metrics:
        if m in panel.columns:
            agg_dict[m] = ["mean", "std"]
    if not agg_dict:
        return pd.DataFrame()

    agg = panel.groupby(["group", "t"]).agg(agg_dict).reset_index()
    new_cols = []
    for c in agg.columns:
        if isinstance(c, tuple) and len(c) == 2:
            new_cols.append(f"{c[0]}_{c[1]}" if c[1] else c[0])
        else:
            new_cols.append(c)
    agg.columns = new_cols
    return agg


def plot_trend_lines(agg: pd.DataFrame, window_weeks: int, output_path) -> None:
    t_vals = sorted(agg["t"].unique())
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()

    colors = {"treatment": "#d62728", "control": "#1f77b4"}

    for ax, (metric_col, metric_label, _) in zip(axes, METRICS):
        mean_col = f"{metric_col}_mean"
        std_col = f"{metric_col}_std"

        if mean_col not in agg.columns or std_col not in agg.columns:
            continue

        for group in ["treatment", "control"]:
            sub = agg[agg["group"] == group].sort_values("t")
            if sub.empty:
                continue
            x = sub["t"].values
            y = sub[mean_col].values
            std = sub[std_col].values
            std = np.where(np.isnan(std), 0, std)
            ax.plot(x, y, "o-", color=colors[group], linewidth=2, markersize=6, label=group.capitalize())
            ax.fill_between(x, y - std, y + std, color=colors[group], alpha=0.2)

        ax.axvline(x=0, color="gray", linestyle="--", alpha=0.6)
        ax.set_xlabel("Period t (0 = during closure)", fontsize=10)
        ax.set_ylabel(metric_label, fontsize=10)
        ax.set_title(metric_label, fontsize=11, fontweight="bold")
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.set_xticks(t_vals)

    fig.suptitle(
        f"Treatment vs Control: Behavior Across Closure Periods\n"
        f"(window = {window_weeks} weeks, mean ± std over customers and closures)",
        fontsize=12, fontweight="bold",
    )
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {output_path}")


def run_trend_analysis(
    prepared: PreparedData,
    week_windows: tuple[int, ...] = (2, 4, 8),
    lowest_purchases: int = DEFAULT_LOWEST_PURCHASES,
    lowest_ratio: float = DEFAULT_LOWEST_RATIO,
    use_set_up_time_matched_control: bool = USE_SET_UP_TIME_MATCHED_CONTROL,
    event_panel: pd.DataFrame | None = None,
) -> None:
    closures = prepared.closures.copy()
    print(f"\nLoaded {len(closures)} closures for trend analysis.")
    print(f"  Control: use_set_up_time_matched_control={use_set_up_time_matched_control}")

    if event_panel is None or event_panel.empty:
        max_weeks = max(week_windows)
        print(f"\nBuilding shared weekly panel once for max window={max_weeks} weeks...")
        event_panel = build_week_level_panel(
            df_commodity=prepared.df_commodity,
            df_order=prepared.df_order,
            closures=closures,
            customer_preference=prepared.customer_preference,
            window_weeks=max_weeks,
            lowest_purchases=lowest_purchases,
            lowest_ratio=lowest_ratio,
            use_set_up_time_matched_control=use_set_up_time_matched_control,
        )

    for window_weeks in week_windows:
        print(f"\n--- Using shared panel for {window_weeks}-week window ---")
        panel = subset_week_level_panel(event_panel, window_weeks=window_weeks)
        print(f"  Panel rows: {len(panel):,}")

        agg = aggregate_by_group_t(panel)
        print(f"  (group, t) combinations: {len(agg)}")

        out_path = OUTPUT_DIR / f"closure_trend_lines_w{window_weeks}.pdf"
        plot_trend_lines(agg, window_weeks, out_path)


def main(limit_closures: int | None = None):
    print("=" * 60)
    print("Closure Trend Line Plots (weekly periods)")
    print("=" * 60)

    df = load_order_commodity_data()
    df_order = load_order_result_data()
    closures = pd.read_csv(CLOSURES_CSV, encoding="utf-8-sig")
    closures = filter_closures_shorter_than_max(
        closures,
        max_duration_days=MAX_CLOSURE_DURATION_DAYS,
        context="trend",
    )
    if limit_closures:
        closures = closures.head(limit_closures)

    customer_preference = get_customer_store_preference(df, lowest_purchases=DEFAULT_LOWEST_PURCHASES)
    prepared = PreparedData(
        df_commodity=df,
        df_order=df_order,
        closures=closures,
        customer_preference=customer_preference,
        unique_visits=df[["member_id", "date", "dept_id"]].drop_duplicates(),
    )
    run_trend_analysis(prepared)


if __name__ == "__main__":
    import sys
    limit = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else None
    main(limit_closures=limit)
