from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
SAMPLE_PATH = (
    ROOT
    / "outputs"
    / "04_diagnostics_18_closures"
    / "novelty_pre_heterogeneity_median"
    / "estimation_sample.csv"
)
ORDER_PATH = ROOT.parent / "data" / "data1031" / "order_result.csv"
COMMODITY_PATH = ROOT / "data" / "processed" / "order_commodity_result_processed.csv"
OUTPUT_DIR = ROOT / "outputs" / "paper" / "heterogeneity_audit"
CHUNKSIZE = 1_000_000


def _build_episode_frame(sample: pd.DataFrame) -> pd.DataFrame:
    pre = sample.loc[sample["rel_t"] < 0].copy()
    pre["period_start"] = pd.to_datetime(pre["period_start"])
    pre["closure_start"] = pd.to_datetime(pre["closure_start"])
    pre["purchase_days"] = np.rint(
        pre["purchase_frequency"] * pre["closure_duration_days"]
    ).astype(int)

    episode = (
        pre.groupby("event_fe_id", sort=False)
        .agg(
            member_id=("member_id", "first"),
            closure_event_id=("closure_event_id", "first"),
            closure_start=("closure_start", "first"),
            closure_duration_days=("closure_duration_days", "first"),
            treated=("treated", "first"),
            disp_binary=("disp_binary", "first"),
            novelty_pre_high=("novelty_pre_high", "first"),
            novelty_pre_mean=("novelty_pre_mean", "first"),
            pre_start=("period_start", "min"),
            pre_purchase_days=("purchase_days", "sum"),
            pre_purchasing_windows=("purchase_days", lambda values: int((values > 0).sum())),
        )
        .reset_index()
    )
    episode["pre_end"] = episode["closure_start"] - pd.Timedelta(days=1)
    if episode["member_id"].duplicated().any():
        raise ValueError("The exact heterogeneity cohort unexpectedly contains repeated members.")
    if len(episode) != 25_894 or episode["closure_event_id"].nunique() != 18:
        raise ValueError(
            f"Unexpected cohort: episodes={len(episode):,}, "
            f"closures={episode['closure_event_id'].nunique()}"
        )
    if (episode["pre_purchase_days"] < 1).any():
        raise ValueError("Every heterogeneity episode should have a purchasing pre-period.")
    return episode


def _load_selected_orders(member_ids: set[int]) -> pd.DataFrame:
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
        raise ValueError("No order rows found for the heterogeneity cohort.")
    return pd.concat(parts, ignore_index=True).drop_duplicates(
        ["member_id", "order_id"]
    )


def _load_selected_commodities(member_ids: set[int]) -> pd.DataFrame:
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
        raise ValueError("No commodity rows found for the heterogeneity cohort.")
    return pd.concat(parts, ignore_index=True)


def _attach_order_counts(episode: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    dated = orders.merge(
        episode[["event_fe_id", "member_id", "pre_start", "pre_end"]],
        on="member_id",
        how="inner",
        validate="many_to_one",
    )
    dated["is_pre"] = dated["date"].between(dated["pre_start"], dated["pre_end"])
    dated["is_prior"] = dated["date"] < dated["pre_start"]
    counts = (
        dated.groupby("event_fe_id", sort=False)
        .agg(
            pre_orders=("is_pre", "sum"),
            prior_orders=("is_prior", "sum"),
            observed_orders_through_pre_end=(
                "date",
                lambda values: int((values <= dated.loc[values.index, "pre_end"]).sum()),
            ),
        )
        .reset_index()
    )
    return episode.merge(counts, on="event_fe_id", how="left", validate="one_to_one")


def _attach_product_counts(
    episode: pd.DataFrame, commodities: pd.DataFrame
) -> pd.DataFrame:
    dated = commodities.merge(
        episode[
            [
                "event_fe_id",
                "member_id",
                "pre_start",
                "pre_end",
                "closure_duration_days",
            ]
        ],
        on="member_id",
        how="inner",
        validate="many_to_one",
    )
    pre = dated.loc[dated["date"].between(dated["pre_start"], dated["pre_end"])].copy()
    prior = dated.loc[dated["date"] < dated["pre_start"]].copy()
    pre["pre_window"] = (
        (pre["date"] - pre["pre_start"]).dt.days // pre["closure_duration_days"]
    ).astype(int)

    pre_counts = (
        pre.groupby("event_fe_id", sort=False)
        .agg(
            pre_product_rows=("product_id", "size"),
            pre_distinct_products=("product_id", "nunique"),
            pre_product_window_choices=(
                "product_id",
                lambda values: int(
                    pre.loc[values.index, ["pre_window", "product_id"]]
                    .drop_duplicates()
                    .shape[0]
                ),
            ),
        )
        .reset_index()
    )
    prior_counts = (
        prior.groupby("event_fe_id", sort=False)
        .agg(
            prior_product_rows=("product_id", "size"),
            prior_distinct_products=("product_id", "nunique"),
        )
        .reset_index()
    )
    result = episode.merge(
        pre_counts, on="event_fe_id", how="left", validate="one_to_one"
    ).merge(prior_counts, on="event_fe_id", how="left", validate="one_to_one")
    for column in [
        "pre_product_rows",
        "pre_distinct_products",
        "pre_product_window_choices",
        "prior_product_rows",
        "prior_distinct_products",
    ]:
        result[column] = result[column].fillna(0).astype(int)
    return result


def _group_summary(episode: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict] = []
    for high, block in episode.groupby("novelty_pre_high", sort=True):
        rows.append(
            {
                "pre_novelty_group": "high" if high else "low",
                "episodes": len(block),
                "mean_pre_novelty": block["novelty_pre_mean"].mean(),
                "mean_pre_orders": block["pre_orders"].mean(),
                "median_pre_orders": block["pre_orders"].median(),
                "mean_pre_purchase_days": block["pre_purchase_days"].mean(),
                "median_pre_purchase_days": block["pre_purchase_days"].median(),
                "mean_pre_purchasing_windows": block["pre_purchasing_windows"].mean(),
                "mean_pre_product_window_choices": block[
                    "pre_product_window_choices"
                ].mean(),
                "median_pre_product_window_choices": block[
                    "pre_product_window_choices"
                ].median(),
                "mean_prior_orders": block["prior_orders"].mean(),
                "share_exactly_one_pre_order": (block["pre_orders"] == 1).mean(),
                "share_exactly_one_pre_purchase_day": (
                    block["pre_purchase_days"] == 1
                ).mean(),
                "share_exactly_one_purchasing_window": (
                    block["pre_purchasing_windows"] == 1
                ).mean(),
                "share_exactly_one_product_window_choice": (
                    block["pre_product_window_choices"] == 1
                ).mean(),
                "share_no_prior_orders": (block["prior_orders"] == 0).mean(),
                "share_one_pre_order_and_no_prior_orders": (
                    (block["pre_orders"] == 1) & (block["prior_orders"] == 0)
                ).mean(),
                "share_pre_novelty_exactly_one": np.isclose(
                    block["novelty_pre_mean"], 1
                ).mean(),
                "share_pre_novelty_exactly_zero": np.isclose(
                    block["novelty_pre_mean"], 0
                ).mean(),
            }
        )
    return pd.DataFrame(rows)


def _order_count_table(episode: pd.DataFrame) -> pd.DataFrame:
    labels = ["0", "1", "2", "3", "4", "5-6", "7-10", "11+"]
    episode = episode.copy()
    episode["pre_order_bin"] = pd.cut(
        episode["pre_orders"],
        bins=[-1, 0, 1, 2, 3, 4, 6, 10, np.inf],
        labels=labels,
    )
    return (
        episode.groupby("pre_order_bin", observed=True, sort=True)
        .agg(
            episodes=("event_fe_id", "size"),
            share_of_cohort=("event_fe_id", lambda values: len(values) / len(episode)),
            share_high_pre_novelty=("novelty_pre_high", "mean"),
            mean_pre_novelty=("novelty_pre_mean", "mean"),
            share_pre_novelty_one=(
                "novelty_pre_mean",
                lambda values: np.isclose(values, 1).mean(),
            ),
            mean_prior_orders=("prior_orders", "mean"),
            mean_product_window_choices=("pre_product_window_choices", "mean"),
        )
        .reset_index()
    )


def _single_order_table(episode: pd.DataFrame) -> pd.DataFrame:
    one = episode.loc[episode["pre_orders"] == 1].copy()
    one["prior_purchase_history"] = np.where(
        one["prior_orders"] == 0, "no prior observed order", "one or more prior orders"
    )
    return (
        one.groupby("prior_purchase_history", sort=True)
        .agg(
            episodes=("event_fe_id", "size"),
            share_high_pre_novelty=("novelty_pre_high", "mean"),
            mean_pre_novelty=("novelty_pre_mean", "mean"),
            share_pre_novelty_one=(
                "novelty_pre_mean",
                lambda values: np.isclose(values, 1).mean(),
            ),
            share_pre_novelty_zero=(
                "novelty_pre_mean",
                lambda values: np.isclose(values, 0).mean(),
            ),
            mean_product_window_choices=("pre_product_window_choices", "mean"),
        )
        .reset_index()
    )


def _write_report(
    episode: pd.DataFrame,
    group_summary: pd.DataFrame,
    order_counts: pd.DataFrame,
    single_order: pd.DataFrame,
) -> None:
    low = group_summary.set_index("pre_novelty_group").loc["low"]
    high = group_summary.set_index("pre_novelty_group").loc["high"]
    one = episode.loc[episode["pre_orders"] == 1]
    prior_observed = one.loc[one["prior_orders"] > 0]
    one_product_choice = episode.loc[
        episode["pre_product_window_choices"] == 1
    ]
    pearson = episode[["pre_orders", "novelty_pre_mean"]].corr().iloc[0, 1]
    spearman = episode[["pre_orders", "novelty_pre_mean"]].corr(
        method="spearman"
    ).iloc[0, 1]
    lines = [
        "# Pre-novelty type and pre-period purchase-count diagnostic",
        "",
        "## Scope",
        "",
        "This diagnostic uses the exact 25,894-episode, 18-closure heterogeneity cohort. It does not alter the classifier, sample, main DDD estimates or paper. Order counts come from `order_result.csv`; product counts come from the same processed commodity file used to construct novelty-seeking.",
        "",
        "## Main finding",
        "",
        "Pre-period novelty type is strongly related to how much behavior is observed before closure. The relationship is partly mechanical and partly substantive: sparse histories make extreme novelty values much more likely, but one pre-period order does not automatically imply novelty equal to one when the consumer bought a familiar product.",
        "",
        f"- Low-pre-novelty episodes average {low.mean_pre_orders:.2f} pre-period orders, {low.mean_pre_purchase_days:.2f} purchase days and {low.mean_pre_purchasing_windows:.2f} purchasing windows.",
        f"- High-pre-novelty episodes average {high.mean_pre_orders:.2f} orders, {high.mean_pre_purchase_days:.2f} purchase days and {high.mean_pre_purchasing_windows:.2f} purchasing windows.",
        f"- Exactly one pre-period order occurs in {low.share_exactly_one_pre_order:.1%} of low-type episodes and {high.share_exactly_one_pre_order:.1%} of high-type episodes.",
        f"- Among all {len(one):,} one-pre-order episodes, {(one['novelty_pre_high'] == 1).mean():.1%} are classified high novelty and {np.isclose(one['novelty_pre_mean'], 1).mean():.1%} have pre-novelty exactly one.",
        f"- Exactly one distinct product-window choice occurs in {low.share_exactly_one_product_window_choice:.1%} of low-type episodes and {high.share_exactly_one_product_window_choice:.1%} of high-type episodes. For these {len(one_product_choice):,} episodes, novelty is mechanically binary: {np.isclose(one_product_choice['novelty_pre_mean'], 1).mean():.1%} equal one and {np.isclose(one_product_choice['novelty_pre_mean'], 0).mean():.1%} equal zero.",
        "- No one-pre-order episode lacks earlier observed purchase history in this cohort; the single pre-period order is therefore not necessarily the consumer's first observed order.",
        f"- Among the {len(prior_observed):,} one-pre-order episodes with prior purchase history, only {np.isclose(prior_observed['novelty_pre_mean'], 1).mean():.1%} have novelty exactly one; {np.isclose(prior_observed['novelty_pre_mean'], 0).mean():.1%} have novelty exactly zero.",
        f"- Across all episodes, the Pearson correlation between pre-order count and pre-novelty is {pearson:.3f}; the Spearman correlation is {spearman:.3f}.",
        "",
        "## Interpretation",
        "",
        "The user's proposed concern is therefore real: the high-novelty group has materially fewer observed pre-period purchases and contains many more one-order episodes. A single pre-period order yields novelty one only if its product mix is entirely new relative to the consumer's earlier observed history. Thus the split combines an exploration tendency with history length and sampling noise. This helps explain the large general `Post × pre-novelty type` movement and strengthens the case for a longer or minimum-exposure initialization window before treating the split as consumer type.",
        "",
        "This measurement problem does not make the omitted `Post × type` term optional. Any future heterogeneity model using this type definition must remain fully saturated.",
        "",
        "## Output files",
        "",
        "- `pre_novelty_purchase_count_episode_diagnostic.csv`",
        "- `pre_novelty_purchase_count_group_summary.csv`",
        "- `pre_novelty_by_pre_order_count.csv`",
        "- `pre_novelty_single_pre_order_diagnostic.csv`",
    ]
    (OUTPUT_DIR / "PRE_NOVELTY_PURCHASE_COUNT_DIAGNOSTIC.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    sample = pd.read_csv(SAMPLE_PATH)
    episode = _build_episode_frame(sample)
    members = set(episode["member_id"].astype(int))

    orders = _load_selected_orders(members)
    episode = _attach_order_counts(episode, orders)
    commodities = _load_selected_commodities(members)
    episode = _attach_product_counts(episode, commodities)

    for column in ["pre_orders", "prior_orders", "observed_orders_through_pre_end"]:
        episode[column] = episode[column].fillna(0).astype(int)
    if (episode["pre_orders"] < episode["pre_purchase_days"]).any():
        raise ValueError("Pre-period order counts cannot be below purchase-day counts.")

    group_summary = _group_summary(episode)
    order_counts = _order_count_table(episode)
    single_order = _single_order_table(episode)

    episode.to_csv(
        OUTPUT_DIR / "pre_novelty_purchase_count_episode_diagnostic.csv", index=False
    )
    group_summary.to_csv(
        OUTPUT_DIR / "pre_novelty_purchase_count_group_summary.csv", index=False
    )
    order_counts.to_csv(
        OUTPUT_DIR / "pre_novelty_by_pre_order_count.csv", index=False
    )
    single_order.to_csv(
        OUTPUT_DIR / "pre_novelty_single_pre_order_diagnostic.csv", index=False
    )
    _write_report(episode, group_summary, order_counts, single_order)
    print((OUTPUT_DIR / "PRE_NOVELTY_PURCHASE_COUNT_DIAGNOSTIC.md").read_text())


if __name__ == "__main__":
    main()
