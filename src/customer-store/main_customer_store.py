from __future__ import annotations

from data_processing import (
    DEFAULT_LOWEST_PURCHASES,
    DEFAULT_LOWEST_RATIO,
    DEFAULT_WINDOW_DAYS,
    ROBUSTNESS_WINDOW_DAYS,
    USE_SET_UP_TIME_MATCHED_CONTROL,
    build_week_level_panel,
    build_kept_closure_registry,
    merge_did_summaries_into_registry,
    prepare_shared_data,
)
from did_analysis import run_did_for_windows
from trend_analysis import run_trend_analysis


def main(
    lowest_purchases: int = DEFAULT_LOWEST_PURCHASES,
    lowest_ratio: float = DEFAULT_LOWEST_RATIO,
    use_set_up_time_matched_control: bool = USE_SET_UP_TIME_MATCHED_CONTROL,
) -> None:
    print("=" * 70)
    print("Customer-Store Unified Pipeline")
    print("=" * 70)

    prepared = prepare_shared_data(
        lowest_purchases=lowest_purchases,
        lowest_ratio=lowest_ratio,
    )

    print("\n" + "=" * 70)
    print("Build Kept-Only Closure Registry")
    print("=" * 70)
    registry_kept = build_kept_closure_registry(
        prepared=prepared,
        lowest_purchases=lowest_purchases,
        lowest_ratio=lowest_ratio,
        use_set_up_time_matched_control=use_set_up_time_matched_control,
    )

    trend_windows = (4, 8)
    did_windows = (DEFAULT_WINDOW_DAYS, ROBUSTNESS_WINDOW_DAYS)
    max_did_weeks = max(w // 7 for w in did_windows)
    max_trend_weeks = max(trend_windows)
    max_shared_weeks = max(max_did_weeks, max_trend_weeks)

    print("\n" + "=" * 70)
    print(f"Build Shared Event-Time Panel (max_weeks={max_shared_weeks})")
    print("=" * 70)
    shared_event_panel = build_week_level_panel(
        df_commodity=prepared.df_commodity,
        df_order=prepared.df_order,
        closures=prepared.closures,
        customer_preference=prepared.customer_preference,
        window_weeks=max_shared_weeks,
        lowest_purchases=lowest_purchases,
        lowest_ratio=lowest_ratio,
        use_set_up_time_matched_control=use_set_up_time_matched_control,
    )

    did_summaries = run_did_for_windows(
        prepared=prepared,
        windows=did_windows,
        lowest_purchases=lowest_purchases,
        lowest_ratio=lowest_ratio,
        use_set_up_time_matched_control=use_set_up_time_matched_control,
        event_panel=shared_event_panel,
    )

    merge_did_summaries_into_registry(
        registry_kept=registry_kept,
        summary_by_window=did_summaries,
    )

    print("\n" + "=" * 70)
    print("Run Weekly Trend Analysis")
    print("=" * 70)
    run_trend_analysis(
        prepared=prepared,
        week_windows=trend_windows,
        lowest_purchases=lowest_purchases,
        lowest_ratio=lowest_ratio,
        use_set_up_time_matched_control=use_set_up_time_matched_control,
        event_panel=shared_event_panel,
    )

    print("\n" + "=" * 70)
    print("Unified pipeline complete")
    print("=" * 70)


if __name__ == "__main__":
    main()
