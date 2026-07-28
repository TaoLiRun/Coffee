from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
MAIN_SAMPLE = (
    ROOT
    / "outputs"
    / "03_main_18_closures"
    / "novelty_member_first_ddd_h4"
    / "estimation_sample.csv"
)
LEGACY_HETEROGENEITY_SAMPLE = (
    ROOT
    / "outputs"
    / "04_diagnostics_18_closures"
    / "novelty_pre_heterogeneity_median"
    / "estimation_sample.csv"
)
ORDER_PATH = ROOT.parent / "data" / "data1031" / "order_result.csv"
COMMODITY_PATH = ROOT / "data" / "processed" / "order_commodity_result_processed.csv"
OUTPUT_DIR = ROOT / "outputs" / "paper" / "heterogeneity_audit" / "long_pre_window"
CHUNKSIZE = 1_000_000

# Overlapping variants extend the legacy type window through the estimation
# pre-periods. Separate variants end before relative period -4 and therefore do
# not reuse any outcome period from the DDD regression.
VARIANTS: dict[str, tuple[int, ...]] = {
    "overlap_4": tuple(range(-4, 0)),
    "overlap_8": tuple(range(-8, 0)),
    "overlap_12": tuple(range(-12, 0)),
    "separate_4": tuple(range(-8, -4)),
    "separate_8": tuple(range(-12, -4)),
}


def _episode_frame(sample: pd.DataFrame) -> pd.DataFrame:
    episode = (
        sample.sort_values("event_fe_id")
        .drop_duplicates("event_fe_id")
        [[
            "event_fe_id",
            "member_id",
            "closure_event_id",
            "closure_start",
            "closure_duration_days",
            "treated",
            "disp_binary",
        ]]
        .copy()
    )
    episode["closure_start"] = pd.to_datetime(episode["closure_start"])
    if len(episode) != 40_148 or episode["closure_event_id"].nunique() != 18:
        raise ValueError(
            f"Unexpected main cohort: episodes={len(episode):,}, "
            f"closures={episode['closure_event_id'].nunique()}"
        )
    if episode["member_id"].duplicated().any():
        raise ValueError("A member appears in more than one closure episode.")
    candidate_starts = [
        episode["closure_start"]
        + pd.to_timedelta(
            min(periods) * episode["closure_duration_days"], unit="D"
        )
        for periods in VARIANTS.values()
    ]
    earliest_candidate = pd.concat(candidate_starts, axis=1).min(axis=1).min()
    if earliest_candidate < pd.Timestamp("2020-06-01"):
        raise ValueError(
            f"Candidate initialization window begins before data coverage: {earliest_candidate}"
        )
    return episode


def _load_orders(member_ids: set[int]) -> pd.DataFrame:
    parts: list[pd.DataFrame] = []
    for chunk in pd.read_csv(
        ORDER_PATH,
        encoding="utf-8-sig",
        usecols=["member_id", "order_id", "create_hour"],
        chunksize=CHUNKSIZE,
    ):
        selected = chunk.loc[chunk["member_id"].isin(member_ids)].copy()
        if selected.empty:
            continue
        selected["date"] = pd.to_datetime(
            selected["create_hour"], errors="coerce"
        ).dt.normalize()
        selected = selected.dropna(subset=["date", "order_id"])
        parts.append(selected[["member_id", "order_id", "date"]])
    if not parts:
        raise ValueError("No order rows found for the main cohort.")
    return pd.concat(parts, ignore_index=True).drop_duplicates(
        ["member_id", "order_id"]
    )


def _load_commodities(member_ids: set[int]) -> pd.DataFrame:
    parts: list[pd.DataFrame] = []
    for chunk in pd.read_csv(
        COMMODITY_PATH,
        encoding="utf-8-sig",
        usecols=["member_id", "dt", "product_id"],
        chunksize=CHUNKSIZE,
    ):
        selected = chunk.loc[chunk["member_id"].isin(member_ids)].copy()
        if selected.empty:
            continue
        selected["date"] = pd.to_datetime(selected["dt"], errors="coerce").dt.normalize()
        selected = selected.dropna(subset=["date", "product_id"])
        selected["product_id"] = selected["product_id"].astype(int)
        parts.append(selected[["member_id", "date", "product_id"]])
    if not parts:
        raise ValueError("No commodity rows found for the main cohort.")
    return pd.concat(parts, ignore_index=True)


def _assign_relative_period(
    rows: pd.DataFrame, episode: pd.DataFrame
) -> pd.DataFrame:
    dated = rows.merge(
        episode[
            ["event_fe_id", "member_id", "closure_start", "closure_duration_days"]
        ],
        on="member_id",
        how="inner",
        validate="many_to_one",
    )
    dated = dated.loc[dated["date"] < dated["closure_start"]].copy()
    dated["rel_t_history"] = np.floor(
        (dated["date"] - dated["closure_start"]).dt.days
        / dated["closure_duration_days"]
    ).astype(int)
    return dated.loc[dated["rel_t_history"].between(-12, -1)].copy()


def _build_window_novelty(
    episode: pd.DataFrame, commodities: pd.DataFrame
) -> pd.DataFrame:
    first_dates = (
        commodities.groupby(["member_id", "product_id"], sort=False)["date"]
        .min()
        .rename("first_date")
        .reset_index()
    )
    dated = _assign_relative_period(commodities, episode)
    dated = dated.merge(
        first_dates,
        on=["member_id", "product_id"],
        how="left",
        validate="many_to_one",
    )
    dated["window_start"] = dated["closure_start"] + pd.to_timedelta(
        dated["rel_t_history"] * dated["closure_duration_days"], unit="D"
    )
    dated["is_new"] = (dated["first_date"] >= dated["window_start"]).astype(int)
    choices = dated.drop_duplicates(
        ["event_fe_id", "rel_t_history", "product_id"]
    )
    return (
        choices.groupby(["event_fe_id", "rel_t_history"], sort=False)
        .agg(
            product_window_choices=("product_id", "size"),
            new_product_window_choices=("is_new", "sum"),
        )
        .reset_index()
        .assign(
            window_novelty=lambda data: data["new_product_window_choices"]
            / data["product_window_choices"]
        )
    )


def _build_window_orders(episode: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    dated = _assign_relative_period(orders, episode)
    return (
        dated.groupby(["event_fe_id", "rel_t_history"], sort=False)
        .agg(
            orders=("order_id", "nunique"),
            purchase_days=("date", "nunique"),
        )
        .reset_index()
    )


def _attach_variant_traits(
    episode: pd.DataFrame,
    novelty_by_window: pd.DataFrame,
    orders_by_window: pd.DataFrame,
) -> pd.DataFrame:
    result = episode.copy()
    support_rows: list[dict] = []
    for name, periods in VARIANTS.items():
        novelty = novelty_by_window.loc[
            novelty_by_window["rel_t_history"].isin(periods)
        ]
        novelty_agg = (
            novelty.groupby("event_fe_id", sort=False)
            .agg(
                novelty_mean=("window_novelty", "mean"),
                purchasing_windows=("rel_t_history", "nunique"),
                product_window_choices=("product_window_choices", "sum"),
                new_product_window_choices=("new_product_window_choices", "sum"),
            )
            .reset_index()
        )
        novelty_agg["novelty_pooled"] = (
            novelty_agg["new_product_window_choices"]
            / novelty_agg["product_window_choices"]
        )
        orders = orders_by_window.loc[orders_by_window["rel_t_history"].isin(periods)]
        order_agg = (
            orders.groupby("event_fe_id", sort=False)
            .agg(orders=("orders", "sum"), purchase_days=("purchase_days", "sum"))
            .reset_index()
        )
        combined = novelty_agg.merge(
            order_agg, on="event_fe_id", how="outer", validate="one_to_one"
        )
        rename = {
            column: f"{name}_{column}"
            for column in combined.columns
            if column != "event_fe_id"
        }
        combined = combined.rename(columns=rename)
        result = result.merge(
            combined, on="event_fe_id", how="left", validate="one_to_one"
        )
        for count_name in [
            "purchasing_windows",
            "product_window_choices",
            "new_product_window_choices",
            "orders",
            "purchase_days",
        ]:
            column = f"{name}_{count_name}"
            result[column] = result[column].fillna(0).astype(int)

        valid = result[f"{name}_novelty_mean"].notna()
        support_rows.append(
            {
                "variant": name,
                "periods": ",".join(str(value) for value in periods),
                "first_rel_t": min(periods),
                "last_rel_t": max(periods),
                "overlaps_main_preperiod": int(max(periods) >= -4),
                "eligible_episodes": int(valid.sum()),
                "share_main_cohort_eligible": float(valid.mean()),
                "mean_orders_eligible": float(
                    result.loc[valid, f"{name}_orders"].mean()
                ),
                "median_orders_eligible": float(
                    result.loc[valid, f"{name}_orders"].median()
                ),
                "mean_purchasing_windows_eligible": float(
                    result.loc[valid, f"{name}_purchasing_windows"].mean()
                ),
                "median_novelty_mean": float(
                    result.loc[valid, f"{name}_novelty_mean"].median()
                ),
                "median_novelty_pooled": float(
                    result.loc[valid, f"{name}_novelty_pooled"].median()
                ),
            }
        )
    support = pd.DataFrame(support_rows)
    return result, support


def _validate_legacy(result: pd.DataFrame) -> dict:
    legacy = (
        pd.read_csv(
            LEGACY_HETEROGENEITY_SAMPLE,
            usecols=["event_fe_id", "novelty_pre_mean", "novelty_pre_high"],
        )
        .drop_duplicates("event_fe_id")
        .merge(
            result[["event_fe_id", "overlap_4_novelty_mean"]],
            on="event_fe_id",
            how="left",
            validate="one_to_one",
        )
    )
    mean_matches = np.allclose(
        legacy["novelty_pre_mean"], legacy["overlap_4_novelty_mean"], atol=1e-12
    )
    median = float(result.loc[result["overlap_4_novelty_mean"].notna(), "overlap_4_novelty_mean"].median())
    high_matches = np.array_equal(
        legacy["novelty_pre_high"].astype(int),
        (legacy["overlap_4_novelty_mean"] > median).astype(int),
    )
    checks = {
        "legacy_episode_count": len(legacy),
        "computed_eligible_episode_count": int(
            result["overlap_4_novelty_mean"].notna().sum()
        ),
        "legacy_mean_matches": bool(mean_matches),
        "legacy_high_indicator_matches": bool(high_matches),
        "computed_legacy_median": median,
    }
    if not mean_matches or not high_matches or len(legacy) != 25_894:
        raise AssertionError(f"Legacy reconstruction failed: {checks}")
    return checks


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    sample = pd.read_csv(MAIN_SAMPLE)
    episode = _episode_frame(sample)
    members = set(episode["member_id"].astype(int))
    orders = _load_orders(members)
    commodities = _load_commodities(members)
    novelty_by_window = _build_window_novelty(episode, commodities)
    orders_by_window = _build_window_orders(episode, orders)
    traits, support = _attach_variant_traits(
        episode, novelty_by_window, orders_by_window
    )
    checks = _validate_legacy(traits)

    traits.to_csv(OUTPUT_DIR / "episode_long_pre_novelty_traits.csv", index=False)
    support.to_csv(OUTPUT_DIR / "long_pre_window_support.csv", index=False)
    novelty_by_window.to_csv(OUTPUT_DIR / "episode_window_novelty_components.csv", index=False)
    orders_by_window.to_csv(OUTPUT_DIR / "episode_window_order_counts.csv", index=False)
    pd.DataFrame([checks]).to_csv(
        OUTPUT_DIR / "legacy_reconstruction_checks.csv", index=False
    )
    print(support.to_string(index=False))
    print(checks)


if __name__ == "__main__":
    main()
