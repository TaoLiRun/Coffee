import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
pd.set_option('display.width', 1000)  # Increase total width
pd.set_option('display.max_columns', 10)  # Show more columns
import glob
import os
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def build_and_save_combined_dataset(parquet_path: str = "combined_push_purchase_analysis.parquet") -> pd.DataFrame:
    """
    End-to-end pipeline to build the unified push + purchase panel with:
      - harmonized columns (push & purchase),
      - 'new' flag for first appearance of each member,
      - 'days_since_purchase' for every row,
      - 'dormant' flag (>= 30 days since last purchase for existing members),
    and save it to a parquet file.
    """

    # ------------------------------------------------------------------
    # 1. Load and prepare push data
    # ------------------------------------------------------------------
    push_files = glob.glob("../../data/data1031/sleep_push_result_*.csv")
    all_push_data_list = []
    for file in push_files:
        df = pd.read_csv(file)
        # Keep only the columns we need from push logs
        df = df[["dt", "member_id", "trigger_tag", "coupon", "discount"]]
        all_push_data_list.append(df)

    all_push_data = pd.concat(all_push_data_list, ignore_index=True)
    all_push_data["dt"] = pd.to_datetime(all_push_data["dt"])
    all_push_data["data_source"] = "push"

    # ------------------------------------------------------------------
    # 2. Load and prepare purchase (order) data
    # ------------------------------------------------------------------
    folder_path = "../../data/data1031"
    file_path = os.path.join(folder_path, "order_result.csv")
    order_cols = [
        "member_id",
        "create_hour",
        "dept_id",
        "coffee_origin_money",
        "drink_not_coffee_origin_money",
        "coffee_commodity_num",
        "coffee_top_commodity_num",
        "not_coffee_commodity_num",
        "not_coffee_top_commodity_num",
        "food_commodity_num",
        "use_coupon_num",
        "coffee_discount",
        "disount_tag",
        "drink_not_coffee_discount",
    ]

    order_result = pd.read_csv(file_path, usecols=order_cols)
    # Convert create_hour to date and then to datetime
    order_result["dt"] = pd.to_datetime(order_result["create_hour"], format="%Y-%m-%d %H").dt.date
    order_result["dt"] = pd.to_datetime(order_result["dt"])

    # ------------------------------------------------------------------
    # 2a. Aggregate multiple orders on the same day for each consumer
    # ------------------------------------------------------------------
    # We aggregate monetary and count variables by sum, and keep an arbitrary
    # department id (dept_id) for that member-day via 'first'.
    order_result = (
        order_result
        .groupby(["member_id", "dt"], as_index=False)
        .agg(
            dept_id=("dept_id", "first"),
            coffee_origin_money=("coffee_origin_money", "sum"),
            drink_not_coffee_origin_money=("drink_not_coffee_origin_money", "sum"),
            coffee_commodity_num=("coffee_commodity_num", "sum"),
            coffee_top_commodity_num=("coffee_top_commodity_num", "sum"),
            not_coffee_commodity_num=("not_coffee_commodity_num", "sum"),
            not_coffee_top_commodity_num=("not_coffee_top_commodity_num", "sum"),
            food_commodity_num=("food_commodity_num", "sum"),
            use_coupon_num=("use_coupon_num", "sum"),
            coffee_discount=("coffee_discount", "first"),
            disount_tag=("disount_tag", "first"),
            drink_not_coffee_discount=("drink_not_coffee_discount", "first"),
        )
    )

    # Basic purchase-side aggregations at the daily consumer level
    order_result["origin_money"] = (
        order_result["coffee_origin_money"] + order_result["drink_not_coffee_origin_money"]
    )
    order_result["total_items"] = (
        order_result["coffee_commodity_num"] + order_result["not_coffee_commodity_num"] - order_result["food_commodity_num"]
    )
    order_result["total_top_items"] = (
        order_result["coffee_top_commodity_num"] + order_result["not_coffee_top_commodity_num"]
    )
    # make "use_discount" the mean of "coffee_discount" and "drink_not_coffee_discount" if both are not null,
    # otherwise make it the one that is not null, or 0 if both are null
    order_result["use_discount"] = (
        order_result["coffee_discount"].fillna(0) + order_result["drink_not_coffee_discount"].fillna(0)
    ) / 2.0

    # delete columns
    order_result = order_result.drop(columns=['coffee_origin_money', 'drink_not_coffee_origin_money', 
    'food_commodity_num', 'coffee_commodity_num', 'not_coffee_commodity_num', 
    'coffee_top_commodity_num', 'not_coffee_top_commodity_num', 'coffee_discount', 'drink_not_coffee_discount'])

    # Remove rows without valid dt
    order_result = order_result[order_result["dt"].notna()]
    order_result["data_source"] = "purchase"

    # ------------------------------------------------------------------
    # 3. Harmonize schema and stack push + purchase
    # ------------------------------------------------------------------
    push_cols = set(all_push_data.columns)
    purchase_cols = set(order_result.columns)

    push_full = all_push_data.copy()
    purchase_full = order_result.copy()

    # Add purchase-only columns to push with NaN
    for col in purchase_cols - push_cols:
        push_full[col] = np.nan

    # Add push-only columns to purchase with NaN
    for col in push_cols - purchase_cols:
        purchase_full[col] = np.nan

    # Combine into one panel and sort by member and time
    combined_data = pd.concat([push_full, purchase_full], ignore_index=True)
    combined_data = combined_data.sort_values(["member_id", "dt"]).reset_index(drop=True)

    # ------------------------------------------------------------------
    # 4. Mark first appearance per member ('new' flag)
    # ------------------------------------------------------------------
    combined_data["new"] = 0
    # Earliest dt per member is marked as new = 1
    first_appearances = combined_data.groupby("member_id")["dt"].idxmin()
    combined_data.loc[first_appearances, "new"] = 1
    logger.info("Combined push & purchase data; marked first appearances with 'new'=1.")

    # ------------------------------------------------------------------
    # 5. Compute days_since_purchase and dormant flag (vectorized)
    # ------------------------------------------------------------------
    panel = combined_data.copy()
    panel["dormant"] = 0

    # Build a purchase-only frame with last_purchase_date for each event
    purchase_dates = panel[panel["data_source"] == "purchase"][["member_id", "dt"]].rename(
        columns={"dt": "last_purchase_date"}
    )

    # Sort for merge_asof: first by time, then by member_id
    panel_sorted = panel.sort_values(["dt", "member_id"]).reset_index(drop=True)
    purchase_dates_sorted = purchase_dates.sort_values(["last_purchase_date", "member_id"]).reset_index(drop=True)

    # For each record, find the most recent purchase before its dt for that member
    merged = pd.merge_asof(
        panel_sorted,
        purchase_dates_sorted,
        left_on="dt",
        right_on="last_purchase_date",
        by="member_id",
        direction="backward",
        allow_exact_matches=False,  # exclude purchases on the same date
    )

    # Days since last purchase (NaN if no purchase yet)
    merged["days_since_purchase"] = (merged["dt"] - merged["last_purchase_date"]).dt.days

    # Dormant definition:
    #   - not a brand-new member (new == 0)
    #   - and (no previous purchase OR > 30 days since last purchase)
    dormant_mask = (merged["new"] == 0) & (
        merged["last_purchase_date"].isna() | (merged["days_since_purchase"] > 30)
    )
    merged.loc[dormant_mask, "dormant"] = 1

    # Drop helper column and restore original column order plus new features
    final_data = merged.drop(columns=["last_purchase_date"])

    # map "data_source" "push" to 0, "purchase" to 1
    final_data["data_source"] = final_data["data_source"].map({"push": 0, "purchase": 1})

    # ------------------------------------------------------------------
    # 5b. For each member, keep only rows starting from (and including) their first purchase
    # Identify first purchase ("data_source" == 1) index per member
    # Compute minimum row index of first purchase per member
    min_first_purchase_idx = final_data[final_data["data_source"] == 1].groupby("member_id").apply(lambda x: x.index.min())
    # For each row, mark if index is >= first purchase index for that member
    final_data["keep_from_first_purchase"] = final_data.apply(
        lambda row: row.name >= min_first_purchase_idx.get(row["member_id"], float('inf')),
        axis=1
    )
    final_data = final_data[final_data["keep_from_first_purchase"]].drop(columns=["keep_from_first_purchase"])
    # Re-sort to make sure first events are well-defined
    final_data = final_data.sort_values(["member_id", "dt"]).reset_index(drop=True)
    
    # ------------------------------------------------------------------
    # 5c. Add calendar-based dormant periods and dormant_start dates
    # ------------------------------------------------------------------
    # Calendar-based definition:
    #   - Each purchase increments a purchase_cycle_id within a member.
    #   - A dormant state starts 31 days after the previous purchase.
    #   - A row is in dormant_period == previous purchase_cycle_id
    #     once its dt >= prev_purchase_dt + 31 days.

    # Ensure sorted chronologically per member
    final_data = final_data.sort_values(["member_id", "dt"])

    # Identify purchase events
    is_purchase = final_data["data_source"] == 1

    # Cumulative purchase-cycle id per member: 1,2,3,... for each new purchase
    final_data["purchase_cycle_id"] = final_data.groupby("member_id")["data_source"].transform(
        lambda x: (x == 1).cumsum()
    )

    # Previous purchase date for each row
    final_data["prev_purchase_dt"] = final_data["dt"].where(is_purchase)
    final_data["prev_purchase_dt"] = final_data.groupby("member_id")["prev_purchase_dt"].shift(1)
    final_data["prev_purchase_dt"] = final_data.groupby("member_id")["prev_purchase_dt"].ffill()

    # Calendar-based dormant start: 31 days after previous purchase
    final_data["calc_dormant_start"] = final_data["prev_purchase_dt"] + pd.Timedelta(days=31)

    # In dormant state if we've had a previous purchase and today >= dormant start
    is_dormant_calendar = (final_data["prev_purchase_dt"].notna()) & (
        final_data["dt"] >= final_data["calc_dormant_start"]
    )

    # Use previous purchase cycle for dormant_period assignment
    final_data["prev_purchase_cycle_id"] = (
        final_data.groupby("member_id")["purchase_cycle_id"].shift(1).fillna(0)
    )
    final_data["prev_purchase_cycle_id"] = (
        final_data.groupby("member_id")["prev_purchase_cycle_id"].ffill().astype(int)
    )

    final_data["dormant_period"] = 0
    final_data.loc[is_dormant_calendar, "dormant_period"] = final_data.loc[
        is_dormant_calendar, "prev_purchase_cycle_id"
    ]

    final_data["dormant_start"] = pd.NaT
    final_data.loc[is_dormant_calendar, "dormant_start"] = final_data.loc[
        is_dormant_calendar, "calc_dormant_start"
    ]

    # Reindex dormant_periods within each member so that they start at 1
    # and are consecutive (1, 2, 3, ...) regardless of purchase_cycle_id.
    dormant_period_keys = (
        final_data[final_data["dormant_period"] > 0][["member_id", "dormant_period", "dormant_start"]]
        .drop_duplicates()
        .sort_values(["member_id", "dormant_start"])
    )
    if not dormant_period_keys.empty:
        dormant_period_keys["new_dormant_period"] = (
            dormant_period_keys.groupby("member_id").cumcount() + 1
        )
        # Build a mapping from (member_id, old_period) -> new_period
        mapper = (
            dormant_period_keys.set_index(["member_id", "dormant_period"])["new_dormant_period"]
        )
        final_data["dormant_period"] = final_data.set_index(
            ["member_id", "dormant_period"]
        ).index.map(lambda idx: mapper.get(idx, 0))

    # check
    # final_data[final_data["member_id"]==5]
    # rename "disount_tag" to "discount_tag"
    final_data = final_data.rename(columns={"disount_tag": "discount_tag"})
    # Cleanup helper columns
    final_data = final_data.drop(
        columns=["purchase_cycle_id", "prev_purchase_dt", "calc_dormant_start", "prev_purchase_cycle_id",
                "dormant_start"]
    )

    # ------------------------------------------------------------------
    # 6. Persist and log summary
    # ------------------------------------------------------------------
    final_data.to_parquet(parquet_path, index=False)
    logger.info(f"Parquet data saved to: {parquet_path}")
    logger.info(f"Final dataset shape: {final_data.shape}")
    logger.info("\nData types:")
    logger.info(final_data.dtypes)
    logger.info("\nFirst 10 rows (key columns):")
    logger.info(final_data[["member_id", "dt", "data_source", "new", "dormant"]].head(10))

    logger.info("\n=== BASIC STATISTICS ===")
    logger.info(f"Total records: {len(final_data)}")
    logger.info(f"Unique members: {final_data['member_id'].nunique()}")
    logger.info(f"Push records: {len(final_data[final_data['data_source'] == 0])}")
    logger.info(f"Purchase records: {len(final_data[final_data['data_source'] == 1])}")

    logger.info("\n=== STATUS DISTRIBUTION ===")
    # average total dormant periods per member: agg over member_id
    logger.info(f"Average total dormant periods per member: {final_data.groupby('member_id')['dormant_period'].max().mean()}")
    
    logger.info("\n=== VALIDATION ===")
    new_members_dormant = final_data[final_data["new"] == 1]["dormant"].value_counts()
    logger.info("Dormant status for new members (should all be 0):")
    logger.info(new_members_dormant)

    new_counts = final_data.groupby("member_id")["new"].sum()
    logger.info(f"\nMembers with exactly one 'new' mark: {(new_counts == 1).sum()}")
    logger.info(f"Members with no 'new' mark: {(new_counts == 0).sum()}")
    logger.info(f"Members with multiple 'new' marks: {(new_counts > 1).sum()}")

    logger.info("\n=== SAMPLE MEMBER TIMELINES ===")
    sample_members = final_data["member_id"].unique()[:2]
    for member_id in sample_members:
        logger.info(f"\nMember {member_id}:")
        timeline = (
            final_data[final_data["member_id"] == member_id][
                ["dt", "data_source", "new", "dormant"]
            ]
            .sort_values("dt")
            .reset_index(drop=True)
        )
        logger.info(timeline)

    return final_data

def dormant_analysis():
    logger.info("=== DORMANT ANALYSIS ===")
    final_data = pd.read_parquet('combined_push_purchase_analysis.parquet')
    final_data = final_data[['member_id', 'dt', 'data_source', 'new', 'dormant',
                             'days_since_purchase', 'trigger_tag', 'dormant_period', 'dormant_start']]
    
    # Mark dormant periods per consumer
    final_data = final_data.sort_values(['member_id', 'dt']).reset_index(drop=True)
    final_data['prev_dormant'] = final_data.groupby('member_id')['dormant'].shift(1).fillna(0)
    final_data['dormant_start'] = ((final_data['dormant'] == 1) & (final_data['prev_dormant'] == 0)).astype(int)
    final_data['dormant_period'] = final_data.groupby('member_id')['dormant_start'].cumsum()
    final_data.loc[final_data['dormant'] == 0, 'dormant_period'] = 0
    
    # Analysis 1: Members who ever entered dormant status
    dormant_members = final_data[final_data['dormant_start'] == 1]['member_id'].unique()
    total_members = final_data['member_id'].nunique()
    
    logger.info("=== DORMANT MEMBER ANALYSIS ===")
    logger.info(f"Total unique members: {total_members:,}")
    logger.info(f"Members who ever entered dormant status: {len(dormant_members):,}")
    logger.info(f"Percentage of members who went dormant: {len(dormant_members)/total_members*100:.1f}%")
    
    # Analysis 2: Distribution of dormant period counts per member
    dormant_periods_per_member = (
        final_data[final_data['dormant_start'] == 1]
        .groupby('member_id')
        .size()
        .reset_index(name='dormant_period_count')
    )
    
    logger.info(f"\n=== DORMANT PERIOD DISTRIBUTION ===")
    logger.info("Number of dormant periods per member:")
    distribution = dormant_periods_per_member['dormant_period_count'].value_counts().sort_index()
    for count, freq in distribution.items():
        percentage = freq / len(dormant_members) * 100
        logger.info(f"  {count} period(s): {freq:,} members ({percentage:.1f}%)")
    
    # Summary statistics
    logger.info(f"\n=== SUMMARY STATISTICS ===")
    logger.info(f"Average dormant periods per dormant member: {dormant_periods_per_member['dormant_period_count'].mean():.2f}")
    logger.info(f"Median dormant periods per dormant member: {dormant_periods_per_member['dormant_period_count'].median():.1f}")
    logger.info(f"Max dormant periods for a single member: {dormant_periods_per_member['dormant_period_count'].max()}")
    logger.info(f"Standard deviation: {dormant_periods_per_member['dormant_period_count'].std():.2f}")
    
    # Analysis 3: Members by dormant frequency categories
    dormant_periods_per_member['frequency_category'] = pd.cut(
        dormant_periods_per_member['dormant_period_count'],
        bins=[0, 1, 2, 3, 5, 10, 100],
        labels=['1', '2', '3', '4-5', '6-10', '10+'],
        right=False
    )
    
    category_summary = dormant_periods_per_member['frequency_category'].value_counts().sort_index()
    logger.info(f"\n=== DORMANT FREQUENCY CATEGORIES ===")
    for category, count in category_summary.items():
        percentage = count / len(dormant_members) * 100
        logger.info(f"  {category} period(s): {count:,} members ({percentage:.1f}%)")

 # Ultra-fast fully vectorized version (period-level)
def analyze_causal_effect_DID(final_data, first_purchase_members):
    """
    Fully vectorized version using calendar-based dormant period calculation
    at the (member_id, dormant_period) level.
    """
    # Filter to the experimental population and assume dormant_period is already present
    df = final_data[final_data['member_id'].isin(first_purchase_members)].copy()
    df = df.sort_values(['member_id', 'dt'])
    
    # Identify all dormant periods (member, period_id)
    periods_df = (
        df[df['dormant_period'] > 0]  # Use your new dormant_period column
        [['member_id', 'dormant_period']]
        .drop_duplicates()
        .rename(columns={'dormant_period': 'dormant_period_id'})
    )
    
    # Treatment: dormant periods with push at day 31 (30-32 window)
    # We need to calculate days_since_purchase for the calendar-based approach
    treatment_mask = (
        (df['dormant_period'] > 0) &  # In a dormant period (your new definition)
        (df['data_source'] == 'push') &
        (df['days_since_purchase'].notna()) &
        (df['days_since_purchase']==31)
    )
    
    treatment_periods = (
        df.loc[treatment_mask, ['member_id', 'dormant_period']]
        .drop_duplicates()
        .assign(treatment_flag=1)
        .rename(columns={'dormant_period': 'dormant_period_id'})
    )

    # Wake-up outcomes (purchase between 30.5-31.5 days)
    wakeup_mask = (
        (df['dormant_period'] > 0) &  # if on day 31 member makes 2 purchases, then this will exclude one
        (df['data_source'] == 'purchase') &
        (df['days_since_purchase'].notna()) &
        (df['days_since_purchase']==31) 
    )
    
    wakeup_periods = (
        df.loc[wakeup_mask, ['member_id', 'dormant_period']]
        .drop_duplicates()
        .assign(wakeup_flag=1)
        .rename(columns={'dormant_period': 'dormant_period_id'})
    )
    
    # Merge treatment / wake-up indicators
    periods_df = (
        periods_df
        .merge(treatment_periods, on=['member_id', 'dormant_period_id'], how='left')
        .merge(wakeup_periods, on=['member_id', 'dormant_period_id'], how='left')
    )
    
    periods_df['treatment'] = periods_df.get('treatment_flag', 0).fillna(0).astype(int)
    periods_df['wakeup'] = periods_df.get('wakeup_flag', 0).fillna(0).astype(int)
    periods_df = periods_df[['member_id', 'dormant_period_id', 'treatment', 'wakeup']]

    control_mask = periods_df['treatment'] == 0
    treatment_mask = periods_df['treatment'] == 1

    control_count = control_mask.sum()
    treatment_count = treatment_mask.sum()
    total_periods = len(periods_df)

    control_wakeups = periods_df.loc[control_mask, 'wakeup'].sum()
    treatment_wakeups = periods_df.loc[treatment_mask, 'wakeup'].sum()

    logger.info("Experimental population (calendar-based dormant periods):")
    logger.info(f"  - Total dormant periods: {total_periods}")
    logger.info(f"  - Treatment periods (pushed at day 31): {treatment_count}")
    logger.info(f"  - Control periods (not pushed at day 31): {control_count}")
    logger.info(f"  - Periods with wake-up 31-35: {periods_df['wakeup'].sum()}")

    return periods_df, control_wakeups, treatment_wakeups

def analyze_causal_effect_DID_old(final_data, first_purchase_members):
    """
    Fully vectorized version that handles the complete experimental population
    at the (member_id, dormant_period) level without materializing tuple keys.
    """
    # Filter and prepare data
    df = (
        final_data[final_data['member_id'].isin(first_purchase_members)]
        .sort_values(['member_id', 'dt'])
        .assign(
            prev_dormant=lambda x: x.groupby('member_id')['dormant'].shift(1).fillna(0),
            prev_data_source=lambda x: x.groupby('member_id')['data_source'].shift(1).fillna(''),
            dormant_start=lambda x: (x['dormant'] == 1) & ((x['prev_dormant'] == 0) | (x['prev_data_source'] == 'purchase'))
        )
    )
    df['dormant_period_id'] = df.groupby('member_id')['dormant_start'].cumsum()
    df['valid_period'] = df['dormant_period_id'] > 0

    # Identify all dormant periods (member, period_id)
    periods_df = (
        df[df['dormant_start']]
        [['member_id', 'dormant_period_id']]
        .drop_duplicates()
    )

    # Treatment: dormant periods with push at day 31 (30-32 window)
    treatment_mask = (
        df['valid_period'] &
        (df['dormant'] == 1) &
        (df['data_source'] == 'push') &
        (df['days_since_purchase'].notna()) &
        (df['days_since_purchase'].between(30.5, 31.5))
    )
    treatment_periods = (
        df.loc[treatment_mask, ['member_id', 'dormant_period_id']]
        .drop_duplicates()
        .assign(treatment_flag=1)
    )

    # Wake-up outcomes (purchase between 31-35 days)
    wakeup_mask = (
        df['valid_period'] &
        (df['dormant'] == 1) &
        (df['data_source'] == 'purchase') &
        (df['days_since_purchase'].notna()) &
        (df['days_since_purchase'].between(30.5, 31.5))
    )
    wakeup_periods = (
        df.loc[wakeup_mask, ['member_id', 'dormant_period_id']]
        .drop_duplicates()
        .assign(wakeup_flag=1)
    )
    # Merge treatment / wake-up indicators
    periods_df = (
        periods_df
        .merge(treatment_periods, on=['member_id', 'dormant_period_id'], how='left')
        .merge(wakeup_periods, on=['member_id', 'dormant_period_id'], how='left')
    )
    periods_df['treatment'] = periods_df.get('treatment_flag', 0).fillna(0).astype(int)
    periods_df['wakeup'] = periods_df.get('wakeup_flag', 0).fillna(0).astype(int)
    periods_df = periods_df[['member_id', 'dormant_period_id', 'treatment', 'wakeup']]

    control_mask = periods_df['treatment'] == 0
    treatment_mask = periods_df['treatment'] == 1

    control_count = control_mask.sum()
    treatment_count = treatment_mask.sum()
    total_periods = len(periods_df)

    control_wakeups = periods_df.loc[control_mask, 'wakeup'].sum()
    treatment_wakeups = periods_df.loc[treatment_mask, 'wakeup'].sum()

    logger.info("Experimental population (dormant periods):")
    logger.info(f"  - Total dormant periods: {total_periods}")
    logger.info(f"  - Treatment periods (pushed at day 31): {treatment_count}")
    logger.info(f"  - Control periods (not pushed at day 31): {control_count}")
    logger.info(f"  - Periods with wake-up 31: {periods_df['wakeup'].sum()}")

    return periods_df, control_wakeups, treatment_wakeups

def analyze_data():
    final_data = pd.read_parquet('combined_push_purchase_analysis.parquet')
    final_data = final_data[['member_id', 'dt', 'data_source', 'new', 'dormant', 'days_since_purchase', 'trigger_tag']]
    
    # Analysis 1: For members whose new=1 correspond to data_source=push, 
    # plot distribution of trigger_tag
    logger.info("\n=== ANALYSIS 1: Trigger Tag Distribution for New Members (Push) ===")
    new_push_members = final_data[(final_data['new'] == 1) & (final_data['data_source'] == 'push')]
    logger.info(f"Number of members who start with push: {new_push_members['member_id'].nunique()}")
    
    # Plot trigger_tag distribution
    trigger_tag_counts = new_push_members['trigger_tag'].value_counts().sort_index()
    logger.info(f"\nTrigger tag distribution:\n{trigger_tag_counts}")
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=trigger_tag_counts.index, y=trigger_tag_counts.values)
    plt.title('Distribution of Trigger Tag for New Members (Push)', fontsize=16)
    plt.xlabel('Trigger Tag', fontsize=14)
    plt.ylabel('Count', fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.savefig('plots/analysis1_trigger_tag_distribution.pdf', dpi=300)

    # Analysis 2: Filter members who start with a purchase, 
    # find rows when they are dormant and data_source=push, 
    # plot distribution of days_since_purchase
    logger.info("\n=== ANALYSIS 2: Days Since Purchase for Dormant Push Events ===")
    
    # Find members who start with a purchase
    first_purchase_members = final_data[
        (final_data['new'] == 1) & (final_data['data_source'] == 'purchase')
    ]['member_id'].unique()
    logger.info(f"Number of members who start with purchase: {len(first_purchase_members)}")
    
    members_start_with_purchase_data = final_data[
        final_data['member_id'].isin(first_purchase_members)
    ]

    
    # Analysis 2.1: filter rows of push where dormant=0
    logger.info("\n=== ANALYSIS 2.1: Days Since Purchase Distribution by Trigger Type for Push Events where Dormant=0 ===")
    push_data_not_dormant = members_start_with_purchase_data[
        (members_start_with_purchase_data['data_source'] == 'push') & (members_start_with_purchase_data['dormant'] == 0)
    ]
    logger.info(f"Ratio of push rows where dormant=0: {len(push_data_not_dormant) / len(members_start_with_purchase_data[members_start_with_purchase_data['data_source'] == 'push'])}")
    logger.info(f"Unique trigger types: {push_data_not_dormant['trigger_tag'].nunique()}")
    # get top trigger types
    trigger_counts = push_data_not_dormant['trigger_tag'].value_counts()
    top_triggers = trigger_counts.index.tolist()  # Top 8 most frequent triggers
    logger.info(f"Top {len(top_triggers)} trigger types: {top_triggers}")
    # filter for top triggers only
    filtered_push_data_not_dormant = push_data_not_dormant[push_data_not_dormant['trigger_tag'].isin(top_triggers)]
    # plot distribution of days_since_purchase, using different color per trigger type
    plt.figure(figsize=(8, 6))
    colors = plt.cm.tab10.colors  # Use a palette from matplotlib
    for idx, trigger in enumerate(top_triggers):
        trigger_data = filtered_push_data_not_dormant[filtered_push_data_not_dormant['trigger_tag'] == trigger]['days_since_purchase']
        logger.info(f'statistics for trigger {trigger}\n{trigger_data.describe()}')

    # Analysis 2.2: For members who start with purchase, plot days_since_purchase distribution by trigger type
    logger.info("\n=== ANALYSIS 2.2: Days Since Purchase Distribution by Trigger Type ===")

    # Filter only push events with valid days_since_purchase
    push_events = members_start_with_purchase_data[
        (members_start_with_purchase_data['data_source'] == 'push') & 
        (members_start_with_purchase_data['days_since_purchase'].notna())
    ]

    logger.info(f"Total push events for analysis: {len(push_events)}")
    logger.info(f"Unique trigger types: {push_events['trigger_tag'].nunique()}")

    # Get top trigger types (most frequent ones)
    trigger_counts = push_events['trigger_tag'].value_counts()
    top_triggers = trigger_counts.index.tolist()  # Top 8 most frequent triggers
    logger.info(f"Top {len(top_triggers)} trigger types: {top_triggers}")

    # Filter for top triggers only
    filtered_push_events = push_events[push_events['trigger_tag'].isin(top_triggers)]

    for trigger in top_triggers:
        trigger_data = filtered_push_events[filtered_push_events['trigger_tag'] == trigger]['days_since_purchase']
        logger.info(f'statistics for trigger {trigger}\n{trigger_data.describe()}')


    # Filter data for these members, where dormant=1 and data_source=push
    dormant_push_data = final_data[
        (final_data['member_id'].isin(first_purchase_members)) &
        (final_data['dormant'] == 1) &
        (final_data['data_source'] == 'push') &
        (final_data['days_since_purchase'].notna())
    ]
    logger.info(f"\nNumber of dormant push rows: {len(dormant_push_data)}")

    # for each trigger type, print the statistics of days_since_purchase
    for trigger in top_triggers:
        trigger_data = dormant_push_data[dormant_push_data['trigger_tag'] == trigger]['days_since_purchase']
        logger.info(f'statistics for trigger {trigger}\n{trigger_data.describe()}')
    
    # Analysis 3: Filter members who start with a purchase,
    # for each time they become dormant, find the row with the first push,
    # and plot distribution of days_since_purchase
    logger.info("\n=== ANALYSIS 3: Days Since Purchase for First Push in Each Dormant Period ===")

    def find_first_push_in_dormant_periods_efficient(final_data, first_purchase_members):
        """
        Efficient vectorized approach to find first push in each dormant period
        """
        # Filter data for relevant members only
        relevant_data = final_data[final_data['member_id'].isin(first_purchase_members)].copy()
        
        # Sort by member_id and dt for proper timeline processing
        relevant_data = relevant_data.sort_values(['member_id', 'dt']).reset_index(drop=True)
        
        # Add helper columns for efficient processing
        relevant_data['member_changed'] = relevant_data['member_id'] != relevant_data['member_id'].shift(1)
        relevant_data['dormant_changed'] = relevant_data['dormant'] != relevant_data['dormant'].shift(1)
        relevant_data['period_id'] = ((relevant_data['member_changed'] | relevant_data['dormant_changed']).cumsum())
        
        # Filter only dormant periods that start with dormant=1
        dormant_periods = relevant_data[relevant_data['dormant'] == 1].copy()
        
        if len(dormant_periods) == 0:
            return pd.DataFrame()
        
        # For each dormant period, find the first push
        first_pushes = []
        
        for period_id, period_data in dormant_periods.groupby('period_id'):
            # Get the first row of this period to check if it's truly a dormant period start
            period_start = period_data.iloc[0]
            
            # Check if previous row was not dormant (this is a true dormant period start)
            member_prev_data = relevant_data[
                (relevant_data['member_id'] == period_start['member_id']) & 
                (relevant_data['dt'] < period_start['dt'])
            ].tail(1)
            
            if len(member_prev_data) > 0 and member_prev_data.iloc[0]['dormant'] == 0:
                # This is a true dormant period start, find first push
                pushes_in_period = period_data[
                    (period_data['data_source'] == 'push') & 
                    (period_data['days_since_purchase'].notna())
                ]
                
                if len(pushes_in_period) > 0:
                    first_push = pushes_in_period.iloc[0]
                    first_pushes.append(first_push)
        
        return pd.DataFrame(first_pushes) if first_pushes else pd.DataFrame()

    # Alternative even faster approach using shift operations
    def find_first_push_in_dormant_periods_fast(final_data, first_purchase_members):
        """
        Ultra-fast approach using shift operations
        """
        # Filter and sort
        mask = final_data['member_id'].isin(first_purchase_members)
        relevant_data = final_data[mask].sort_values(['member_id', 'dt']).copy()
        
        # Identify dormant period starts (dormant=1 and previous was dormant=0 or new member)
        relevant_data['prev_dormant'] = relevant_data.groupby('member_id')['dormant'].shift(1)
        relevant_data['prev_data_source'] = relevant_data.groupby('member_id')['data_source'].shift(1)
        
        # A dormant period starts when:
        # 1. Current row is dormant=1, AND
        # 2. (Previous row is dormant=0 OR Previous row is a purchase)
        dormant_starts = (relevant_data['dormant'] == 1) & (
            (relevant_data['prev_dormant'] == 0) | (relevant_data['prev_data_source'] == 'purchase')
        )
        
        # Assign period IDs to each dormant period
        relevant_data['dormant_period_id'] = (dormant_starts).cumsum()
        
        # Filter only dormant periods and find first push in each
        dormant_data = relevant_data[relevant_data['dormant'] == 1].copy()
        
        if len(dormant_data) == 0:
            return pd.DataFrame()
        
        # For each dormant period, get the first push
        first_pushes = (dormant_data[dormant_data['data_source'] == 'push']
                    .groupby('dormant_period_id')
                    .first()
                    .reset_index())
        
        # Filter out pushes without days_since_purchase
        first_pushes = first_pushes[first_pushes['days_since_purchase'].notna()]
        
        return first_pushes

    # Use the fastest method
    logger.info("Finding first push events in dormant periods...")
    first_push_df = find_first_push_in_dormant_periods_fast(final_data, first_purchase_members)

    if len(first_push_df) > 0:
        logger.info(f"Number of first push events in dormant periods: {len(first_push_df)}")
        
        # for each trigger type, print the statistics of days_since_purchase
        for trigger in top_triggers:
            trigger_data = first_push_df[first_push_df['trigger_tag'] == trigger]['days_since_purchase']
            logger.info(f'statistics for trigger {trigger}\n{trigger_data.describe()}')
        
    else:
        logger.info("No first push events found in dormant periods.")
    
    # Analysis 3.1: Causal effect of push at day 31 (RANDOM ASSIGNMENT)
    logger.info("\n=== ANALYSIS 3.1: Causal Effect of Push at Day 31 (Random Assignment) ===")

    # Run the analysis
    logger.info("Running comprehensive causal effect analysis...")
    period_summary_df, control_wakeups, treatment_wakeups = analyze_causal_effect_DID(
        final_data, first_purchase_members
    )
    control_periods = period_summary_df[period_summary_df['treatment'] == 0]
    treatment_periods = period_summary_df[period_summary_df['treatment'] == 1]
    total_periods = len(period_summary_df)

    # Calculate and display results
    logger.info(f"\n=== EXPERIMENTAL RESULTS ===")
    logger.info(f"Control group (dormant periods not pushed at day 31):")
    logger.info(f"  - Size: {len(control_periods)}")
    logger.info(f"  - Woke up between days 31: {control_wakeups}")
    control_size = len(control_periods)
    treatment_size = len(treatment_periods)
    logger.info(f"  - Wake-up rate: {control_wakeups/control_size*100:.2f}%" if control_size > 0 else "  - Wake-up rate: N/A")

    logger.info(f"\nTreatment group (dormant periods pushed at day 31):")
    logger.info(f"  - Size: {treatment_size}") 
    logger.info(f"  - Woke up between days 31: {treatment_wakeups}")
    logger.info(f"  - Wake-up rate: {treatment_wakeups/treatment_size*100:.2f}%" if treatment_size > 0 else "  - Wake-up rate: N/A")

    # Causal effect calculation
    if control_size > 0 and treatment_size > 0:
        control_rate = control_wakeups / control_size
        treatment_rate = treatment_wakeups / treatment_size
        
        logger.info(f"\n=== CAUSAL EFFECT ===")
        logger.info(f"Absolute difference: {(treatment_rate - control_rate)*100:.2f} percentage points")
        logger.info(f"Relative effect: {treatment_rate/control_rate:.2f}x")
        
        # Statistical significance
        from statsmodels.stats.proportion import proportions_ztest
        count = [treatment_wakeups, control_wakeups]
        nobs = [treatment_size, control_size]
        
        if sum(count) > 0:
            stat, pval = proportions_ztest(count, nobs)
            logger.info(f"P-value: {pval:.4f}")
            logger.info(f"Statistically significant: {'YES' if pval < 0.05 else 'NO'}")
            
            # Confidence intervals
            from statsmodels.stats.proportion import proportion_confint
            control_ci = proportion_confint(control_wakeups, control_size, alpha=0.05, method='wilson')
            treatment_ci = proportion_confint(treatment_wakeups, treatment_size, alpha=0.05, method='wilson')
            logger.info(f"Control 95% CI: [{control_ci[0]*100:.1f}%, {control_ci[1]*100:.1f}%]")
            logger.info(f"Treatment 95% CI: [{treatment_ci[0]*100:.1f}%, {treatment_ci[1]*100:.1f}%]")

    # Balance check
    logger.info(f"\n=== BALANCE CHECK ===")
    balance_cols = {'total_items', 'total_top_items', 'has_discount'}
    if control_size > 0 and treatment_size > 0 and balance_cols.issubset(set(final_data.columns)):
        control_member_ids = set(control_periods['member_id'].unique())
        treatment_member_ids = set(treatment_periods['member_id'].unique())
        # Compare pre-dormancy characteristics
        pre_dormant_data = final_data[
            (final_data['member_id'].isin(control_member_ids.union(treatment_member_ids))) &
            (final_data['data_source'] == 'purchase') &
            (final_data['dormant'] == 0)  # Pre-dormancy purchases
        ]
        
        if not pre_dormant_data.empty:
            balance_stats = pre_dormant_data.groupby(
                pre_dormant_data['member_id'].isin(treatment_member_ids).map({True: 'treatment', False: 'control'})
            ).agg({
                'total_items': ['count', 'mean', 'std'],
                'total_top_items': 'mean',
                'has_discount': 'mean'
            }).round(3)
            
            logger.info("Pre-dormancy characteristics (should be balanced due to randomization):")
            logger.info(balance_stats)
        else:
            logger.info("Not enough pre-dormancy purchase data available for balance check.")
    else:
        missing_cols = balance_cols - set(final_data.columns)
        if missing_cols:
            logger.info(f"Skipping balance check; missing columns: {sorted(missing_cols)}")
        else:
            logger.info("Skipping balance check; insufficient control/treatment sizes.")

def analyze_consumers_1st_purchase():
    """
    Deep dive into consumers whose very first interaction is a purchase.
    Focus on dormant periods, push strategies, and wake-up dynamics.
    """
    final_data = pd.read_parquet('combined_push_purchase_analysis.parquet')
    final_data = final_data[['member_id', 'dt', 'data_source', 'new', 'dormant', 'days_since_purchase', 'trigger_tag']]
    
    logger.info("\n=== ANALYSIS 4: Consumers Who Start With Purchase ===")
    first_purchase_members = final_data[
        (final_data['new'] == 1) & (final_data['data_source'] == 'purchase')
    ]['member_id'].unique()
    logger.info(f"Total consumers starting with purchase: {len(first_purchase_members):,}")

    consumer_df = final_data[final_data['member_id'].isin(first_purchase_members)].copy()
    
    # Sort for sequential calculations
    consumer_df = consumer_df.sort_values(['member_id', 'dt']).reset_index(drop=True)

    # Mark dormant periods per consumer
    consumer_df['prev_dormant'] = consumer_df.groupby('member_id')['dormant'].shift(1).fillna(0)
    consumer_df['prev_data_source'] = consumer_df.groupby('member_id')['data_source'].shift(1).fillna('')
    consumer_df['dormant_start'] = ((consumer_df['dormant'] == 1) & ((consumer_df['prev_dormant'] != 1) | (consumer_df['prev_data_source'] == 'purchase'))).astype(int)
    consumer_df['dormant_period'] = consumer_df.groupby('member_id')['dormant_start'].cumsum()
    consumer_df.loc[consumer_df['dormant'] == 0, 'dormant_period'] = 0
    
    # ASSERTION: Each dormant period should have at most one purchase
    purchase_counts_per_period = (
        consumer_df[consumer_df['dormant_period'] > 0]  # Only dormant periods
        .groupby(['member_id', 'dormant_period'])
        .apply(lambda x: (x['data_source'] == 'purchase').sum())
        .reset_index(name='purchase_count')
    )

    # Check if any period has more than one purchase
    periods_with_multiple_purchases = purchase_counts_per_period[purchase_counts_per_period['purchase_count'] > 1]

    if len(periods_with_multiple_purchases) > 0:
        logger.info(f"VIOLATION: {len(periods_with_multiple_purchases)} dormant periods have multiple purchases:")
        logger.info(periods_with_multiple_purchases.head(10))  # Show first 10 violations
        raise AssertionError(f"Found {len(periods_with_multiple_purchases)} dormant periods with multiple purchases")
    else:
        logger.info("ASSERTION PASSED: All dormant periods have at most one purchase")


    # Discard push rows that are outside dormant periods and report the ratio
    push_mask = consumer_df['data_source'] == 'push'
    push_outside_dormant = consumer_df[push_mask & (consumer_df['dormant'] == 0)]
    total_pushes = push_mask.sum()
    outside_ratio = len(push_outside_dormant) / total_pushes if total_pushes > 0 else 0
    logger.info(f"Push events outside dormant periods: {len(push_outside_dormant):,} "
                f"({outside_ratio*100:.4f}% of pushes)")

    consumer_df = consumer_df[~(push_mask & (consumer_df['dormant'] == 0))].copy()

    # Focus on dormant pushes
    dormant_pushes = consumer_df[
        (consumer_df['data_source'] == 'push') &
        (consumer_df['dormant'] == 1)
    ].copy()
    if dormant_pushes.empty:
        logger.info("No push events found within dormant periods for these consumers.")
        return

    dormant_pushes['days_since_purchase_int'] = (
        dormant_pushes['days_since_purchase'].round().astype('Int64')
    )
    # Calculating the sequence number of each push within each dormant period
    dormant_pushes['push_order_in_period'] = (
        dormant_pushes.sort_values('dt')
        .groupby(['member_id', 'dormant_period'])
        .cumcount() + 1
    )

    logger.info("\n--- Push Timing & Trigger Types (Dormant Periods) ---")
    push_day_stats = (
        dormant_pushes
        .groupby(['days_since_purchase_int', 'trigger_tag'])
        .size()
        .reset_index(name='push_count')
        .sort_values('push_count', ascending=False)
        .head(30)
    )
    logger.info(push_day_stats.to_string(index=False))

    # Period-level summary to understand wake-up dynamics and sequences
    period_records = []
    dormant_period_data = consumer_df[consumer_df['dormant_period'] > 0].copy()

    for (member_id, period_id), group in dormant_period_data.groupby(['member_id', 'dormant_period']):
        group = group.sort_values('dt')
        pushes = group[group['data_source'] == 'push']
        purchases = group[group['data_source'] == 'purchase']

        woke_up = not purchases.empty
        wakeup_dt = purchases.iloc[0]['dt'] if woke_up else pd.NaT
        wakeup_day = purchases.iloc[0]['days_since_purchase'] if woke_up else np.nan
        pushes_before_wakeup = (
            pushes[pushes['dt'] <= wakeup_dt].shape[0] if woke_up else pushes.shape[0]
        )
        trigger_sequence = pushes['trigger_tag'].tolist()
        push_days_sequence = pushes['days_since_purchase'].tolist()
        
        # For periods with wakeup, use the last push before/on wakeup date
        # For periods without wakeup, use the absolute last push in the period
        if woke_up and not pushes.empty:
            pushes_before_or_on_wakeup = pushes[pushes['dt'] <= wakeup_dt]
            if not pushes_before_or_on_wakeup.empty:
                last_push_before_wakeup = pushes_before_or_on_wakeup['days_since_purchase'].iloc[-1]
                last_push_day = last_push_before_wakeup
                wakeup_delay_from_last_push = (
                    wakeup_day - last_push_before_wakeup
                    if pd.notna(wakeup_day) and pd.notna(last_push_before_wakeup)
                    else np.nan
                )
            else:
                last_push_day = np.nan
                wakeup_delay_from_last_push = np.nan
        else:
            # No wakeup: use absolute last push in period
            last_push_day = pushes['days_since_purchase'].iloc[-1] if not pushes.empty else np.nan
            wakeup_delay_from_last_push = np.nan

        period_records.append({
            'member_id': member_id,
            'dormant_period': period_id,
            'push_count': pushes.shape[0],
            'woke_up': woke_up,
            'wakeup_day_since_last_purchase': wakeup_day,
            'pushes_before_wakeup_or_end': pushes_before_wakeup,
            'trigger_sequence': trigger_sequence,
            'push_days_sequence': push_days_sequence,
            'last_push_day_since_purchase': last_push_day,
            'wakeup_delay_from_last_push': wakeup_delay_from_last_push
        })

    if not period_records:
        logger.info("No dormant periods found after filtering.")
        return

    period_summary = pd.DataFrame(period_records)
    logger.info(f"Total consumer-dormant_period pairs analyzed: {len(period_summary):,}")
    wakeup_periods = period_summary[period_summary['woke_up']]
    no_wakeup_periods = period_summary[~period_summary['woke_up']]

    # number of consumer-dormant_period pairs with only one row (which is purchase)
    single_purchase_periods = period_summary[period_summary['push_count'] == 0]
    logger.info(f"Number of consumer-dormant_period pairs with only one row (which is purchase): {len(single_purchase_periods):,}")

    logger.info("\n--- Wake-up Dynamics ---")
    if not wakeup_periods.empty:
        logger.info(f"Periods with wake-up: {len(wakeup_periods):,}")
        logger.info("Pushes before wake-up: "
                    f"mean={wakeup_periods['pushes_before_wakeup_or_end'].mean():.2f}, "
                    f"median={wakeup_periods['pushes_before_wakeup_or_end'].median():.0f}")
    else:
        logger.info("No wake-up events observed within dormant periods.")

    if not no_wakeup_periods.empty:
        logger.info(f"Periods where firm gave up (no wake-up recorded): {len(no_wakeup_periods):,}")
        logger.info("Pushes before giving up: "
                    f"mean={no_wakeup_periods['pushes_before_wakeup_or_end'].mean():.2f}, "
                    f"median={no_wakeup_periods['pushes_before_wakeup_or_end'].median():.0f}")
    else:
        logger.info("Every dormant period ended with a wake-up event.")

    # AN example row of the longest sequence with wake-up
    longest_sequence_with_wakeup = period_summary[period_summary['woke_up']].sort_values('pushes_before_wakeup_or_end', ascending=False).head(1)
    logger.info(f"Example row of the longest sequence with wake-up: {longest_sequence_with_wakeup}")
    # AN example row of the longest sequence without wake-up
    longest_sequence_without_wakeup = period_summary[~period_summary['woke_up']].sort_values('pushes_before_wakeup_or_end', ascending=False).head(1)
    logger.info(f"Example row of the longest sequence without wake-up: {longest_sequence_without_wakeup}")

    logger.info("\n--- Additional Context ---")
    logger.info(period_summary.groupby('woke_up')['push_count'].describe().round(2))

    # Detailed sequence outcomes
    sequence_df = (
        period_summary[period_summary['trigger_sequence'].map(len) > 0]
        .copy()
    )
    if not sequence_df.empty:
        sequence_df['sequence_tuple'] = sequence_df['trigger_sequence'].apply(tuple)

        # total number of unique sequences
        total_sequences = sequence_df['sequence_tuple'].nunique()
        logger.info(f"Total number of unique sequences: {total_sequences}")

        # compute mean gaps between consecutive pushes for sequences shorter than 8
        gap_metrics = {}
        for seq_tuple, grp in sequence_df.groupby('sequence_tuple'):
            seq_len = len(seq_tuple)
            if 1 < seq_len < 8:
                diffs_list = []
                for days_seq in grp['push_days_sequence']:
                    if len(days_seq) == seq_len:
                        diffs = np.diff(days_seq)
                        if len(diffs) == seq_len - 1:
                            diffs_list.append(diffs)
                if diffs_list:
                    diffs_arr = np.vstack(diffs_list)
                    gap_metrics[seq_tuple] = tuple(np.round(np.nanmean(diffs_arr, axis=0), 2))

        seq_outcome_stats_full = (
            sequence_df
            .assign(wakeup_flag=sequence_df['woke_up'].astype(int))
            .groupby('sequence_tuple')
            .agg(
                total_periods=('wakeup_flag', 'size'),
                wakeups=('wakeup_flag', 'sum'),
                wakeup_rate=('wakeup_flag', 'mean'),
                avg_wakeup_delay=('wakeup_delay_from_last_push', 'mean'),
                median_wakeup_delay=('wakeup_delay_from_last_push', 'median')
            )
            .sort_values('total_periods', ascending=False)
        )
        # check the sum of total_periods (all sequences, not just top 50)
        logger.info(f"Sum of total_periods (all sequences): {seq_outcome_stats_full['total_periods'].sum()}")
        logger.info(f"Sum of total_periods (top 50 sequences only): {seq_outcome_stats_full.head(50)['total_periods'].sum()}")
        
        # Show only top 50 for display
        seq_outcome_stats = seq_outcome_stats_full.head(50)
        seq_outcome_stats['mean_gap_between_pushes'] = seq_outcome_stats.index.map(
            lambda seq: gap_metrics.get(seq)
        )
        logger.info("\n--- Sequence Wake-up Outcomes ---")
        logger.info(seq_outcome_stats.round(3))
    else:
        logger.info("No push sequences available.")

def RD_analysis():
    logger.info("=== EFFICIENT RD ANALYSIS ===")
    
    # --- 1. Data Loading and Initial Prep ---
    final_data = pd.read_parquet('combined_push_purchase_analysis.parquet')
    # Column selection (always good practice)
    final_data = final_data[['member_id', 'dt', 'data_source', 'new', 'dormant',
                             'days_since_purchase', 'trigger_tag', 'dormant_period', 'dormant_start']]

    first_purchase_members = final_data[
            (final_data['new'] == 1) & (final_data['data_source'] == 'purchase')
        ]['member_id'].unique()
    logger.info(f"Number of members who start with purchase: {len(first_purchase_members)}")
    
    final_data = final_data[final_data['member_id'].isin(first_purchase_members)].copy()
    logger.info(f"Dormant periods: {final_data[final_data['dormant_period'] > 0][['member_id', 'dormant_period']].drop_duplicates().shape[0]}")
    
    logger.info("=== SIMPLE RD ANALYSIS (DAY 30 vs 31) ===")
    
    # 1. Calculate #group2 (The Survivors)
    # These are unique periods that successfully reached Day 31.
    # We count unique 'dormant_period' IDs where the ID > 0.
    survivors_to_31 = final_data[final_data['dormant_period'] > 0][['member_id', 'dormant_period']].drop_duplicates().shape[0]
    
    # 2. Calculate wake_up_31 (Purchases on Day 31)
    # Condition: In a dormant period, source is purchase, and days_since_purchase == 31
    wake_up_31_mask = (
        (final_data['dormant_period'] > 0) & # if on day 31 member makes 2 purchases, then this will exclude one
        (final_data['data_source'] == 'purchase') &
        (final_data['days_since_purchase'].notna()) &
        (final_data['days_since_purchase'] == 31)
    )
    wake_up_31 = int(wake_up_31_mask.sum())
    
    # push on day 31
    push_on_31 = len(final_data[
        (final_data['data_source'] == 'push') & 
        (final_data['days_since_purchase'] == 31)
    ])
    logger.info(f"Push on day 31: {push_on_31}")

    # 3. Calculate wake_up_30 (Purchases on Day 30)
    # A purchase on day 30 means days_since_purchase == 30.
    wake_up_30 = int(len(final_data[
        (final_data['data_source'] == 'purchase') &
        (final_data['days_since_purchase'] == 30)
    ]))

    # 4. The Rates (Your Logic)
    
    # Day 30 Calculation
    # Denominator = Survived to 31 + Died at 30
    n_at_risk_30 = survivors_to_31 + wake_up_30
    rate_30 = wake_up_30 / n_at_risk_30 if n_at_risk_30 > 0 else 0
    
    # Day 31 Calculation
    # Denominator = Survived to 31 (Everyone in group2 is at risk on day 31)
    n_at_risk_31 = survivors_to_31
    rate_31 = wake_up_31 / n_at_risk_31 if n_at_risk_31 > 0 else 0
    
    # 5. Output Results
    results = {
        'metric': ['Purchases (Numerator)', 'At Risk Population (Denominator)', 'Daily Purchase Rate', 'Lift'],
        'Day 30 (Control)': [wake_up_30, n_at_risk_30, f"{rate_30:.4%}", '-'],
        'Day 31 (Treatment)': [wake_up_31, n_at_risk_31, f"{rate_31:.4%}", f"{(rate_31 - rate_30)*100:.3f} pts"]
    }
    
    results_df = pd.DataFrame(results)
    
    # Optional: Calculate relative lift
    relative_lift = (rate_31 - rate_30) / rate_30 if rate_30 > 0 else 0
    logger.info(f"\nRelative Lift: {relative_lift:.2%}")

    logger.info(results_df.to_string(index=False))

    
    
    

    
if __name__ == "__main__":
    combined_data = build_and_save_combined_dataset()
    #calculate_dormant_status(combined_data)
    #analyze_data()
    #analyze_consumers_1st_purchase()
    #RD_analysis()

    