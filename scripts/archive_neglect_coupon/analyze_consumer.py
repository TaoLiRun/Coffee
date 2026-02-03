import pandas as pd
import numpy as np
from datetime import datetime
from visualize import (
    visualize_consumer_new_product_curve,
    visualize_immediate_repurchase_rate,
)


def load_and_prepare_data(
    order_path="data1031/order_commodity_result.csv",
    product_mapping_path="processed_data/product_mapping.csv",
):
    # Read orders with selected columns
    cols = [
        "member_id",
        "create_hour",
        "dept_id",
        "is_top_commodity_coffee_tag",
        "is_top_commodity_not_coffee_tag",
        "coffee_commodity_name",
        "drink_not_coffee_commodity_name",
    ]
    df = pd.read_csv(order_path, usecols=cols, encoding="utf-8-sig")

    # Parse datetime
    df["dt"] = pd.to_datetime(df["create_hour"], errors="coerce")
    df = df.dropna(subset=["dt"])

    # Normalize names and map to product_id
    df["coffee_commodity_name"] = df["coffee_commodity_name"].replace("", pd.NA)
    df["drink_not_coffee_commodity_name"] = df["drink_not_coffee_commodity_name"].replace("", pd.NA)
    df["name"] = df["coffee_commodity_name"].combine_first(df["drink_not_coffee_commodity_name"])

    product_mapping = pd.read_csv(product_mapping_path, encoding="utf-8-sig")
    df = df.merge(product_mapping[["product_id", "name"]], on="name", how="left")
    df = df.dropna(subset=["product_id"])
    df["product_id"] = df["product_id"].astype(int)

    # Combine is_top flags
    df["is_top"] = (
        df[["is_top_commodity_coffee_tag", "is_top_commodity_not_coffee_tag"]]
        .fillna(0)
        .max(axis=1)
    )

    # Keep only needed columns
    df = df[["member_id", "dt", "dept_id", "product_id", "is_top"]]
    df = df.sort_values(["member_id", "dt"])
    return df


def compute_sequences(df: pd.DataFrame):
    # Add purchase index per member
    df = df.copy()
    df["purchase_idx"] = df.groupby("member_id").cumcount() + 1
    counts = df.groupby("member_id")["purchase_idx"].max().rename("purchase_count")
    return df.merge(counts, on="member_id")


def analyze_single_purchases(df_seq):
    singles = df_seq[df_seq["purchase_count"] == 1]
    if len(singles) == 0:
        return None
    ratio_top = (singles["is_top"] > 0).mean()
    return ratio_top


def analyze_double_purchases(df_seq):
    doubles = df_seq[df_seq["purchase_count"] == 2]
    if len(doubles) == 0:
        return None, None
    first = doubles[doubles["purchase_idx"] == 1][["member_id", "product_id"]].set_index("member_id")
    second = doubles[doubles["purchase_idx"] == 2][["member_id", "product_id", "is_top"]].set_index("member_id")
    merged = first.join(second, lsuffix="_first", rsuffix="_second", how="inner")
    same_as_first_ratio = (merged["product_id_first"] == merged["product_id_second"]).mean()
    top_when_not_same = merged[merged["product_id_first"] != merged["product_id_second"]]
    top_ratio = (top_when_not_same["is_top"] > 0).mean() if len(top_when_not_same) > 0 else None
    return same_as_first_ratio, top_ratio


def analyze_triple_purchases(df_seq):
    triples = df_seq[df_seq["purchase_count"] == 3]
    if len(triples) == 0:
        return None, None
    first = triples[triples["purchase_idx"] == 1][["member_id", "product_id"]].set_index("member_id")
    second = triples[triples["purchase_idx"] == 2][["member_id", "product_id"]].set_index("member_id")
    third = triples[triples["purchase_idx"] == 3][["member_id", "product_id", "is_top"]].set_index("member_id")
    merged = first.join(second, lsuffix="_1", rsuffix="_2", how="inner").join(third, how="inner")
    same_all_three = (
        (merged["product_id_1"] == merged["product_id_2"])
        & (merged["product_id_2"] == merged["product_id"])
    )
    same_all_three_ratio = same_all_three.mean()
    not_same = merged[~same_all_three]
    top_ratio = (not_same["is_top"] > 0).mean() if len(not_same) > 0 else None
    return same_all_three_ratio, top_ratio


def analyze_new_product_curve(df_seq, percentile=0.9):
    # Consider users with >=4 purchases up to p90
    purchase_counts = df_seq.groupby("member_id")["purchase_idx"].max()
    max_len = int(np.ceil(purchase_counts.quantile(percentile)))
    filtered_users = purchase_counts[(purchase_counts >= 4) & (purchase_counts <= max_len)].index
    df_f = df_seq[df_seq["member_id"].isin(filtered_users)].copy()

    # For each user, track new product introduction per position
    records = []
    for uid, grp in df_f.groupby("member_id"):
        seen = set()
        grp_sorted = grp.sort_values("purchase_idx")
        for _, row in grp_sorted.iterrows():
            pid = row["product_id"]
            pos = int(row["purchase_idx"])
            is_new = pid not in seen
            seen.add(pid)
            records.append({"purchase_idx": pos, "is_new": is_new})
    rec_df = pd.DataFrame(records)
    stats = (
        rec_df.groupby("purchase_idx")["is_new"]
        .agg(new_count="sum", total="count", ratio=lambda x: x.mean())
        .reset_index()
    )
    stats = stats[stats["purchase_idx"] <= max_len]
    return stats


def analyze_immediate_repurchase_rate(df_seq, max_positions=30):
    records = []
    max_pos = min(max_positions, int(df_seq["purchase_idx"].max()))
    for k in range(2, max_pos + 1):
        at_k = df_seq[df_seq["purchase_idx"] == k]
        prev = df_seq[df_seq["purchase_idx"] == k - 1][["member_id", "product_id"]].set_index("member_id")
        curr = at_k[["member_id", "product_id"]].set_index("member_id")
        merged = curr.join(prev, lsuffix="_curr", rsuffix="_prev", how="inner")
        if len(merged) == 0:
            continue
        rate = (merged["product_id_curr"] == merged["product_id_prev"]).mean()
        records.append({"purchase_idx": k, "immediate_repurchase_rate": rate})
    return pd.DataFrame(records)


def main():
    df = load_and_prepare_data()
    df_seq = compute_sequences(df)

    # 2. Singles
    single_top_ratio = analyze_single_purchases(df_seq)
    print("\nSingles: ratio purchased top:", single_top_ratio)

    # 3. Doubles and triples
    same_as_first_ratio, top_ratio_not_same = analyze_double_purchases(df_seq)
    print("\nDoubles: ratio second same as first:", same_as_first_ratio)
    print("Doubles: ratio second is top when not same:", top_ratio_not_same)

    same_all_three_ratio, triple_top_not_same = analyze_triple_purchases(df_seq)
    print("\nTriples: ratio third same as previous two:", same_all_three_ratio)
    print("Triples: ratio third is top when not same:", triple_top_not_same)

    # 4. New product curve
    new_product_stats = analyze_new_product_curve(df_seq, percentile=0.75)
    print("\nNew product curve stats (first rows):")
    print(new_product_stats.head())

    # 5. Immediate repurchase rate
    repurchase_df = analyze_immediate_repurchase_rate(df_seq, max_positions=30)
    print("\nImmediate repurchase rate (first rows):")
    print(repurchase_df.head())

    # Visualizations
    visualize_consumer_new_product_curve(new_product_stats)
    visualize_immediate_repurchase_rate(repurchase_df)


if __name__ == "__main__":
    main()

