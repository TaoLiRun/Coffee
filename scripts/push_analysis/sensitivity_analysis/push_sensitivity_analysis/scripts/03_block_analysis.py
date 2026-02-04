#!/usr/bin/env python3
"""
Script 3: Block Analysis - Customer Lifecycle Across Multiple Active/Dormant Periods

Purpose: Track customer behavior across multiple active/dormant cycles to understand
         how engagement and push sensitivity evolve over the customer lifecycle.

Key Innovation:
- Instead of just "pre" vs "post" first dormant period
- Track ALL periods: Active1 → Dormant1 → Active2 → Dormant2 → ...
- Analyze how metrics change across periods and how this differs by push_group

Output: Customer-period level dataset with metrics for up to 10 active and 10 dormant periods
"""

import pandas as pd
import numpy as np
import os
import logging
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set up logging
log_dir = Path(__file__).parent.parent / "outputs" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_dir / "03_block_analysis.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def load_preprocessed_data():
    """Load the preprocessed data"""
    logger.info("Loading preprocessed data...")

    data_path = Path(__file__).parent.parent.parent.parent.parent.parent / "data" / "intermediate" / "analysis_data.parquet"
    df = pd.read_parquet(data_path)
    logger.info(f"Loaded {len(df):,} records")

    return df


def identify_periods(df):
    """
    Identify all active and dormant periods for each customer (VECTORIZED).

    Period Structure:
    - Active Period 1: Before first dormant entry (dormant_period = 0)
    - Dormant Period 1: First dormant period (dormant_period > 0)
    - Active Period 2: After wake-up from Dormant 1, before Dormant 2
    - Dormant Period 2: Second dormant period
    - ...

    Returns:
        df_with_periods: DataFrame with period_type, active_period_num, dormant_period_num
    """
    logger.info("=" * 80)
    logger.info("Identifying All Active and Dormant Periods (Vectorized)")
    logger.info("=" * 80)

    # Sort by member_id and date
    df_sorted = df.sort_values(['member_id', 'dt']).copy()

    # Identify state transitions using shift within groups
    # is_dormant: True if dormant_period > 0
    df_sorted['is_dormant'] = (df_sorted['dormant_period'] > 0).astype(int)

    # Find transitions using groupby and shift
    # dormant_change: 1 when entering dormant, -1 when exiting, 0 otherwise
    df_sorted['prev_dormant_state'] = df_sorted.groupby('member_id')['is_dormant'].shift(1).fillna(0)
    df_sorted['dormant_change'] = df_sorted['is_dormant'] - df_sorted['prev_dormant_state']

    # Assign period numbers using cumulative sum
    # Each transition from active to dormant or vice versa increments a counter
    df_sorted['transition_counter'] = df_sorted.groupby('member_id')['dormant_change'].transform(
        lambda x: (x != 0).cumsum()
    )

    # For each customer, identify periods
    # First, create a unique identifier for each state (active/dormant episode)
    df_sorted['state_id'] = (
        df_sorted['member_id'].astype(str) + '_' +
        df_sorted['transition_counter'].astype(str)
    )

    # For each state_id, determine if it's active or dormant
    state_types = df_sorted.groupby('state_id')['is_dormant'].first().reset_index()
    state_types['period_type'] = state_types['is_dormant'].map({0: 'active', 1: 'dormant'})

    # Count active periods and dormant periods within each state_id
    # For each member, count how many active and dormant states they've had
    member_state_counts = state_types.copy()
    member_state_counts['member_id'] = member_state_counts['state_id'].str.split('_').str[0].astype(int)

    # Map period_type to separate counters using cumcount
    member_state_counts['active_period_num'] = np.where(
        member_state_counts['period_type'] == 'active',
        member_state_counts.groupby(['member_id', 'period_type']).cumcount() + 1,
        np.nan
    )
    member_state_counts['dormant_period_num'] = np.where(
        member_state_counts['period_type'] == 'dormant',
        member_state_counts.groupby(['member_id', 'period_type']).cumcount() + 1,
        np.nan
    )

    # Create mapping: state_id -> (period_type, active_period_num, dormant_period_num)
    period_mapping = member_state_counts[['state_id', 'period_type', 'active_period_num', 'dormant_period_num']]

    # Merge back to main dataframe
    df_sorted = df_sorted.merge(period_mapping, on='state_id', how='left')

    # Clean up temporary columns
    df_sorted = df_sorted.drop(columns=['is_dormant', 'prev_dormant_state', 'dormant_change',
                                         'transition_counter', 'state_id'])

    # Summary statistics
    n_members = df_sorted['member_id'].nunique()
    n_active_periods = df_sorted[df_sorted['period_type'] == 'active']['active_period_num'].max()
    n_dormant_periods = df_sorted[df_sorted['period_type'] == 'dormant']['dormant_period_num'].max()

    logger.info(f"Identified periods for {n_members:,} customers")
    logger.info(f"Maximum active periods: {n_active_periods}")
    logger.info(f"Maximum dormant periods: {n_dormant_periods}")

    return df_sorted


def calculate_active_period_metrics(df, max_periods=10):
    """
    Calculate metrics for each active period.

    Metrics (same as original "pre" period):
    - Frequency: orders, order_freq, interpurchase_days, weeks_active
    - Value: avg_order_value, avg_basket_size, total_spend
    - Variety: unique_stores
    - Discount: coupon_usage_rate, avg_discount, deep_discount_pref
    """
    logger.info("=" * 80)
    logger.info("Calculating Active Period Metrics")
    logger.info("=" * 80)

    # Filter to active periods only
    active_df = df[df['period_type'] == 'active'].copy()

    # Filter to purchases only
    active_purchases = active_df[active_df['data_source'] == 1].copy()

    metrics_list = []

    for period_num in range(1, max_periods + 1):
        period_data = active_purchases[active_purchases['active_period_num'] == period_num]

        if len(period_data) == 0:
            logger.info(f"Active Period {period_num}: No data")
            continue

        # Calculate metrics per member
        member_metrics = period_data.groupby('member_id').agg({
            'origin_money': ['mean', 'sum', 'count'],
            'total_items': 'mean',
            'dept_id': 'nunique',
            'use_coupon_num': lambda x: (x > 0).mean(),
            'use_discount': 'mean',
            'dt': ['min', 'max']
        })

        # Flatten column names
        member_metrics.columns = [
            'avg_order_value', 'total_spend', 'n_orders',
            'avg_basket_size',
            'unique_stores',
            'coupon_usage_rate',
            'avg_discount',
            'dt_min', 'dt_max'
        ]

        # Calculate additional metrics
        member_metrics['weeks_active'] = (member_metrics['dt_max'] - member_metrics['dt_min']).dt.days / 7
        member_metrics['weeks_active'] = member_metrics['weeks_active'].clip(lower=1)
        member_metrics.loc[member_metrics['n_orders'] == 1, 'weeks_active'] = 1
        member_metrics['order_freq'] = member_metrics['n_orders'] / member_metrics['weeks_active']

        # Deep discount preference
        period_data_copy = period_data.copy()
        period_data_copy['has_deep_discount'] = (period_data_copy['use_discount'] > 0.5).astype(int)
        deep_discount_pref = period_data_copy.groupby('member_id')['has_deep_discount'].mean()
        member_metrics = member_metrics.join(deep_discount_pref.rename('deep_discount_pref'))

        # Add period identifiers
        member_metrics['active_period_num'] = period_num
        member_metrics = member_metrics.reset_index()

        logger.info(f"Active Period {period_num}: {len(member_metrics):,} customers, "
                   f"{member_metrics['n_orders'].mean():.2f} avg orders")

        metrics_list.append(member_metrics)

    # Combine all periods
    all_active_metrics = pd.concat(metrics_list, ignore_index=True)

    logger.info(f"Total active period observations: {len(all_active_metrics):,}")

    return all_active_metrics


def calculate_dormant_period_metrics(df, max_periods=10):
    """
    Calculate metrics for each dormant period, separately for push=0 and push=1 groups.

    Metrics:
    - Length: dormant_length (days from entry to exit or censoring)
    - Push count: total_pushes, pushes_per_day
    - Push types: discount_push_count, discount_push_share, dept_diversity
    - Last push: last_push_dept, last_push_discount, days_from_last_push_to_wakeup
    - Wakeup: wakeup (binary), days_to_wakeup, wakeup_order_value
    """
    logger.info("=" * 80)
    logger.info("Calculating Dormant Period Metrics (Separately by push_group)")
    logger.info("=" * 80)

    # Filter to dormant periods only
    dormant_df = df[df['period_type'] == 'dormant'].copy()

    # Separate pushes and purchases
    dormant_pushes = dormant_df[dormant_df['data_source'] == 0].copy()
    dormant_purchases = dormant_df[dormant_df['data_source'] == 1].copy()

    metrics_list = []

    # Iterate over push groups and periods
    for push_group in [0, 1]:
        for period_num in range(1, max_periods + 1):
            # Filter by push_group and period_num
            period_pushes = dormant_pushes[
                (dormant_pushes['dormant_period_num'] == period_num) &
                (dormant_pushes['push_group'] == push_group)
            ]
            period_purchases = dormant_purchases[
                (dormant_purchases['dormant_period_num'] == period_num) &
                (dormant_purchases['push_group'] == push_group)
            ]

            if len(period_pushes) == 0 and len(period_purchases) == 0:
                logger.info(f"push={push_group}, Dormant Period {period_num}: No data")
                continue

            # Get all unique members in this period (VECTORIZED)
            all_member_ids = pd.concat([
                period_pushes['member_id'] if len(period_pushes) > 0 else pd.Series(dtype='int64'),
                period_purchases['member_id'] if len(period_purchases) > 0 else pd.Series(dtype='int64')
            ]).unique()

            # Calculate push metrics per member (FIXED: use correct column names)
            if len(period_pushes) > 0:
                # Build aggregation dict dynamically based on available columns
                agg_dict = {'dt': ['min', 'max', 'count']}

                # Add use_discount if available
                if 'use_discount' in period_pushes.columns:
                    agg_dict['use_discount'] = ['sum', 'mean', lambda x: (x > 0).mean()]

                # Add use_coupon_num if available (not 'coupon')
                if 'use_coupon_num' in period_pushes.columns:
                    agg_dict['use_coupon_num'] = ['sum', lambda x: (x > 0).mean()]

                # Add dept_id for diversity (not 'trigger_tag')
                if 'dept_id' in period_pushes.columns:
                    agg_dict['dept_id'] = 'nunique'

                push_metrics = period_pushes.groupby('member_id').agg(agg_dict)

                # Flatten column names
                push_metrics.columns = [
                    'first_push_date', 'last_push_date', 'push_days'
                ]

                # Add discount columns if present
                if 'use_discount' in period_pushes.columns:
                    push_metrics.columns = list(push_metrics.columns[:-3]) + [
                        'total_discount', 'avg_push_discount', 'discount_push_count'
                    ]

                # Add coupon columns if present
                if 'use_coupon_num' in period_pushes.columns:
                    push_metrics.columns = list(push_metrics.columns[:-2]) + [
                        'total_coupon', 'coupon_push_count'
                    ]

                # Add dept diversity if present
                if 'dept_id' in period_pushes.columns:
                    push_metrics.columns = list(push_metrics.columns) + ['dept_diversity']

                # total_pushes is the count of data_source (all pushes)
                push_metrics['total_pushes'] = push_metrics['push_days']

                # Calculate pushes per day
                push_metrics['pushes_per_day'] = push_metrics['total_pushes'] / push_metrics['push_days']
                if 'discount_push_count' in push_metrics.columns:
                    push_metrics['discount_push_share'] = push_metrics['discount_push_count']
            else:
                push_metrics = pd.DataFrame()

            # Calculate purchase (wake-up) metrics per member
            if len(period_purchases) > 0:
                purchase_metrics = period_purchases.groupby('member_id').agg({
                    'days_since_purchase': 'min',
                    'origin_money': 'first'
                }).rename(columns={
                    'days_since_purchase': 'days_to_wakeup',
                    'origin_money': 'wakeup_order_value'
                })
                purchase_metrics['wakeup'] = 1
            else:
                purchase_metrics = pd.DataFrame()

            # Get last push info before wake-up (VECTORIZED, FIXED column names)
            if len(period_pushes) > 0:
                # Sort by dt and get last push per member
                period_pushes_sorted = period_pushes.sort_values(['member_id', 'dt'])

                # Build aggregation dict for last push
                last_push_agg = {'dt': 'last'}
                if 'dept_id' in period_pushes.columns:
                    last_push_agg['dept_id'] = 'last'
                if 'use_discount' in period_pushes.columns:
                    last_push_agg['use_discount'] = 'last'
                if 'use_coupon_num' in period_pushes.columns:
                    last_push_agg['use_coupon_num'] = 'last'

                last_push_df = period_pushes_sorted.groupby('member_id').agg(last_push_agg)

                # Rename columns
                rename_dict = {'dt': 'last_push_date'}
                if 'dept_id' in last_push_df.columns:
                    rename_dict['dept_id'] = 'last_push_dept'
                if 'use_discount' in last_push_df.columns:
                    rename_dict['use_discount'] = 'last_push_discount'
                if 'use_coupon_num' in last_push_df.columns:
                    rename_dict['use_coupon_num'] = 'last_push_has_coupon'

                last_push_df = last_push_df.rename(columns=rename_dict)

                # Convert coupon to binary if present
                if 'last_push_has_coupon' in last_push_df.columns:
                    last_push_df['last_push_has_coupon'] = (last_push_df['last_push_has_coupon'] > 0).astype(int)

                # Get wakeup date for those who woke up
                if len(period_purchases) > 0:
                    wakeup_dates = period_purchases.groupby('member_id')['dt'].min().rename('wakeup_date')
                    last_push_df = last_push_df.join(wakeup_dates, how='left')

                    # Calculate days from last push to wakeup
                    last_push_df['days_from_last_push_to_wakeup'] = (
                        last_push_df['wakeup_date'] - last_push_df['last_push_date']
                    ).dt.days

                    # Drop wakeup_date column
                    last_push_df = last_push_df.drop(columns=['wakeup_date'])
                else:
                    last_push_df['days_from_last_push_to_wakeup'] = np.nan
            else:
                last_push_df = pd.DataFrame()

            # Combine all metrics
            member_metrics = pd.DataFrame({'member_id': all_member_ids})

            # Add push_group
            member_metrics['push_group'] = push_group

            # Merge push metrics
            if len(push_metrics) > 0:
                member_metrics = member_metrics.merge(
                    push_metrics.reset_index(),
                    on='member_id',
                    how='left'
                )

            # Merge purchase metrics
            if len(purchase_metrics) > 0:
                member_metrics = member_metrics.merge(
                    purchase_metrics.reset_index(),
                    on='member_id',
                    how='left'
                )

            # Merge last push info
            if len(last_push_df) > 0:
                member_metrics = member_metrics.merge(
                    last_push_df.reset_index(),
                    on='member_id',
                    how='left'
                )

            # Calculate dormant length (VECTORIZED)
            # If woke up: dormant_length = days_to_wakeup
            # If didn't wake up: dormant_length = last push date - first push date
            member_metrics['dormant_length'] = np.where(
                member_metrics['days_to_wakeup'].notna(),
                member_metrics['days_to_wakeup'],
                np.where(
                    member_metrics['last_push_date'].notna() & member_metrics['first_push_date'].notna(),
                    (member_metrics['last_push_date'] - member_metrics['first_push_date']).dt.days,
                    np.nan
                )
            )

            # Fill NaN values
            member_metrics['wakeup'] = member_metrics['wakeup'].fillna(0).astype(int)
            for col in ['total_pushes', 'pushes_per_day']:
                if col in member_metrics.columns:
                    member_metrics[col] = member_metrics[col].fillna(0)
            if 'discount_push_count' in member_metrics.columns:
                member_metrics['discount_push_count'] = member_metrics['discount_push_count'].fillna(0)
            if 'dept_diversity' in member_metrics.columns:
                member_metrics['dept_diversity'] = member_metrics['dept_diversity'].fillna(0)

            # Add period identifier
            member_metrics['dormant_period_num'] = period_num

            logger.info(f"push={push_group}, Dormant Period {period_num}: {len(member_metrics):,} customers, "
                       f"{member_metrics['wakeup'].mean():.2%} wakeup rate, "
                       f"{member_metrics['total_pushes'].mean():.2f} avg pushes")

            metrics_list.append(member_metrics)

    # Combine all periods
    all_dormant_metrics = pd.concat(metrics_list, ignore_index=True)

    logger.info(f"Total dormant period observations: {len(all_dormant_metrics):,}")

    return all_dormant_metrics


def create_block_dataset(active_metrics, dormant_metrics, df):
    """
    Create the final block dataset by combining active and dormant period metrics.

    Structure: One row per (member_id, period_type, period_number)
    """
    logger.info("=" * 80)
    logger.info("Creating Block Dataset")
    logger.info("=" * 80)

    # Get push_group for each member
    push_groups = df.groupby('member_id')['push_group'].first().reset_index()

    # Reshape active metrics to long format
    active_long = active_metrics.melt(
        id_vars=['member_id', 'active_period_num'],
        var_name='metric',
        value_name='value'
    )
    active_long['period_type'] = 'active'
    active_long['period_number'] = active_long['active_period_num']

    # Reshape dormant metrics to long format
    dormant_long = dormant_metrics.melt(
        id_vars=['member_id', 'dormant_period_num'],
        var_name='metric',
        value_name='value'
    )
    dormant_long['period_type'] = 'dormant'
    dormant_long['period_number'] = dormant_long['dormant_period_num']

    # Combine
    block_long = pd.concat([active_long, dormant_long], ignore_index=True)

    # Pivot to wide format
    block_wide = block_long.pivot_table(
        index=['member_id', 'period_type', 'period_number'],
        columns='metric',
        values='value',
        aggfunc='first'
    ).reset_index()

    # Add push_group
    block_wide = block_wide.merge(push_groups, on='member_id', how='left')

    logger.info(f"Created block dataset with {len(block_wide):,} observations")

    return block_wide


def save_results(active_metrics, dormant_metrics, block_dataset):
    """Save results to files"""
    logger.info("=" * 80)
    logger.info("Saving Results")
    logger.info("=" * 80)

    output_dir = Path(__file__).parent.parent / "outputs" / "tables"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save active period metrics
    active_metrics.to_csv(output_dir / "active_period_metrics.csv", index=False)
    logger.info(f"Saved: {output_dir / 'active_period_metrics.csv'}")

    # Save dormant period metrics
    dormant_metrics.to_csv(output_dir / "dormant_period_metrics.csv", index=False)
    logger.info(f"Saved: {output_dir / 'dormant_period_metrics.csv'}")

    # Save block dataset
    block_dataset.to_csv(output_dir / "block_dataset.csv", index=False)
    logger.info(f"Saved: {output_dir / 'block_dataset.csv'}")


def create_summary_statistics(active_metrics, dormant_metrics):
    """Create summary statistics by period and group"""
    logger.info("=" * 80)
    logger.info("Creating Summary Statistics")
    logger.info("=" * 80)

    output_dir = Path(__file__).parent.parent / "outputs" / "tables"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get push_group for each member
    push_groups = active_metrics.groupby('member_id')['push_group'].first()

    # Add push_group to metrics
    active_metrics_wg = active_metrics.merge(
        push_groups.reset_index(),
        on='member_id',
        how='left'
    )
    dormant_metrics_wg = dormant_metrics.merge(
        push_groups.reset_index(),
        on='member_id',
        how='left'
    )

    # Active period summary
    active_summary = active_metrics_wg.groupby(
        ['push_group', 'active_period_num']
    ).agg({
        'n_orders': ['mean', 'median'],
        'order_freq': ['mean', 'median'],
        'avg_order_value': ['mean', 'median'],
        'total_spend': ['mean', 'median'],
        'weeks_active': ['mean', 'median']
    })
    active_summary.to_csv(output_dir / "active_period_summary.csv")
    logger.info(f"Saved: {output_dir / 'active_period_summary.csv'}")

    # Dormant period summary
    dormant_summary = dormant_metrics_wg.groupby(
        ['push_group', 'dormant_period_num']
    ).agg({
        'dormant_length': ['mean', 'median'],
        'total_pushes': ['mean', 'median'],
        'pushes_per_day': ['mean', 'median'],
        'wakeup': ['mean', 'sum'],
        'days_to_wakeup': ['mean', 'median'],
        'days_from_last_push_to_wakeup': ['mean', 'median']
    })
    dormant_summary.to_csv(output_dir / "dormant_period_summary.csv")
    logger.info(f"Saved: {output_dir / 'dormant_period_summary.csv'}")

    logger.info("\nActive Period Summary:")
    logger.info(active_summary.to_string())

    logger.info("\nDormant Period Summary:")
    logger.info(dormant_summary.to_string())


def main():
    """Main execution function"""
    logger.info("=" * 80)
    logger.info("Starting Block Analysis")
    logger.info("=" * 80)

    # Step 1: Load preprocessed data
    df = load_preprocessed_data()

    # Step 2: Identify all periods
    df_with_periods = identify_periods(df)

    # Step 3: Calculate active period metrics
    active_metrics = calculate_active_period_metrics(df_with_periods, max_periods=10)

    # Step 4: Calculate dormant period metrics
    dormant_metrics = calculate_dormant_period_metrics(df_with_periods, max_periods=10)

    # Step 5: Create block dataset
    block_dataset = create_block_dataset(active_metrics, dormant_metrics, df)

    # Step 6: Create summary statistics
    create_summary_statistics(active_metrics, dormant_metrics)

    # Step 7: Save results
    save_results(active_metrics, dormant_metrics, block_dataset)

    logger.info("=" * 80)
    logger.info("Block analysis complete!")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
