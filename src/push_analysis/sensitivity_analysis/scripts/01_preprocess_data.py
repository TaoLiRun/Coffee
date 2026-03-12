#!/usr/bin/env python3
"""
Script 1: Preprocess Data for Push Sensitivity Analysis

Purpose: Prepare analysis dataset from combined_push_purchase_analysis.parquet
Key steps:
    1. Load parquet file and no_push_members.csv
    2. Assign push_group flag (0=privacy-conscious, 1=opt-in)
    3. Identify first dormant period entry per customer
    4. Create pre-period and post-period indicators
    5. Calculate summary statistics
    6. Save processed data

Output: ../../../../../../data/intermediate/analysis_data.parquet
"""

import pandas as pd
import numpy as np
import os
import logging
from pathlib import Path
from datetime import datetime

# Set up logging
log_dir = Path(__file__).parent.parent / "outputs" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_dir / "01_preprocess_data.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def load_data():
    """Load the parquet file in chunks and no_push_members.csv"""
    logger.info("Loading data...")

    # Load combined push-purchase data using pyarrow directly with columns selection
    parquet_path = Path(__file__).parent.parent.parent.parent.parent.parent / "data" / "processed" / "combined_push_purchase_analysis.parquet"
    logger.info(f"Loading parquet file from: {parquet_path}")

    # Use pyarrow to read with column selection
    import pyarrow.parquet as pq
    import pyarrow as pa

    # Read only essential columns to save memory (include columns needed for downstream analysis)
    essential_columns = [
        'member_id', 'dt', 'data_source', 'dormant_period', 'trigger_tag', 'coupon', 'discount',
        'origin_money', 'dept_id', 'use_coupon_num', 'use_discount'
    ]

    # First get the schema to see available columns
    parquet_file = pq.ParquetFile(parquet_path)
    logger.info(f"Parquet file has {len(parquet_file.schema)} columns and {parquet_file.metadata.num_rows} rows")

    # Read with column selection
    table = pq.read_table(parquet_path, columns=essential_columns)
    df = table.to_pandas()
    logger.info(f"Loaded {len(df):,} records with {df['member_id'].nunique():,} unique members")

    # Load no_push_members
    no_push_path = Path(__file__).parent.parent.parent.parent.parent.parent / "data" / "processed" / "no_push_members.csv"
    logger.info(f"Loading no_push_members from: {no_push_path}")
    no_push_members = pd.read_csv(no_push_path)
    no_push_member_ids = set(no_push_members['member_id'].unique())
    logger.info(f"Found {len(no_push_member_ids):,} members with push=0")

    return df, no_push_member_ids

def assign_push_group(df, no_push_member_ids):
    """Assign push_group flag (0=privacy-conscious, 1=opt-in)"""
    logger.info("Assigning push_group flags...")
    df['push_group'] = df['member_id'].isin(no_push_member_ids).astype(int)
    # Flip the values: isin returns True (1) for no_push members, we want them to be 0
    df['push_group'] = 1 - df['push_group']

    # Log group statistics
    push_0_count = (df['push_group'] == 0).sum()
    push_1_count = (df['push_group'] == 1).sum()
    push_0_members = df[df['push_group'] == 0]['member_id'].nunique()
    push_1_members = df[df['push_group'] == 1]['member_id'].nunique()

    logger.info(f"Push=0 group: {push_0_members:,} members, {push_0_count:,} records")
    logger.info(f"Push=1 group: {push_1_members:,} members, {push_1_count:,} records")

    return df


def identify_first_dormant_entry(df):
    """
    Identify first dormant period entry per customer.
    dormant_period = 0 means active (not dormant)
    dormant_period > 0 means in dormant period
    """
    logger.info("Identifying first dormant period entry per customer...")

    # Get first purchase for each customer
    first_purchase = df[df['data_source'] == 1].groupby('member_id')['dt'].min().reset_index()
    first_purchase.columns = ['member_id', 'first_purchase_date']

    # Get first dormant entry for each customer (avoid copy for better performance)
    logger.info("Finding first dormant date for each customer...")
    first_dormant = df[df['dormant_period'] > 0].groupby('member_id')['dt'].min().reset_index()
    first_dormant.columns = ['member_id', 'first_dormant_date']

    # Merge
    customer_milestones = pd.merge(first_purchase, first_dormant, on='member_id', how='left')

    # Calculate days to first dormant
    customer_milestones['days_to_first_dormant'] = (
        customer_milestones['first_dormant_date'] - customer_milestones['first_purchase_date']
    ).dt.days

    logger.info(f"Customers who never entered dormant period: {customer_milestones['first_dormant_date'].isna().sum():,}")

    return customer_milestones


def create_period_indicators(df, customer_milestones):
    """Create pre-period and post-period indicators"""
    logger.info("Creating pre-period and post-period indicators...")

    # Use pandas map with Series for fast lookup
    logger.info("Creating first_dormant_date mapping...")
    first_dormant_series = customer_milestones.set_index('member_id')['first_dormant_date']
    
    logger.info("Mapping first_dormant_date to records (this may take a few minutes)...")
    first_dormant_mapped = df['member_id'].map(first_dormant_series)
    
    logger.info("Computing period indicators...")
    # Vectorized comparison using the mapped series directly without adding to df
    is_post_mask = pd.notna(first_dormant_mapped) & (df['dt'] >= first_dormant_mapped)
    
    # Assign to dataframe
    df['is_post_period'] = is_post_mask.astype('int8')
    df['period'] = 'pre'
    df.loc[is_post_mask, 'period'] = 'post'
    df['period'] = df['period'].astype('category')

    # Log statistics
    pre_records = (df['period'] == 'pre').sum()
    post_records = (df['period'] == 'post').sum()
    logger.info(f"Pre-period records: {pre_records:,}")
    logger.info(f"Post-period records: {post_records:,}")

    return df


def calculate_summary_statistics(df):
    """Calculate summary statistics by push_group and period"""
    logger.info("Calculating summary statistics...")

    stats_list = []

    for push_group in [0, 1]:
        for period in ['pre', 'post']:
            subset = df[(df['push_group'] == push_group) & (df['period'] == period)]

            # Purchase records only
            purchases = subset[subset['data_source'] == 1]
            pushes = subset[subset['data_source'] == 0]

            stats = {
                'push_group': push_group,
                'period': period,
                'total_records': len(subset),
                'purchase_records': len(purchases),
                'push_records': len(pushes),
                'unique_members': subset['member_id'].nunique(),
                'avg_order_value': purchases['origin_money'].mean() if len(purchases) > 0 else np.nan,
                'median_order_value': purchases['origin_money'].median() if len(purchases) > 0 else np.nan,
                'total_orders': len(purchases),
                'avg_pushes_per_member': pushes.groupby('member_id').size().mean() if len(pushes) > 0 else np.nan,
            }

            stats_list.append(stats)

    summary_df = pd.DataFrame(stats_list)
    logger.info("\nSummary Statistics:")
    logger.info(summary_df.to_string(index=False))

    return summary_df


def save_processed_data(df, summary_df, output_path):
    """Save processed data and summary statistics"""
    logger.info(f"Saving processed data to: {output_path}")

    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save main data
    df.to_parquet(output_path, index=False)
    logger.info(f"Saved {len(df):,} records to {output_path}")

    # Save summary statistics
    summary_path = output_path.parent / "summary_statistics.csv"
    summary_df.to_csv(summary_path, index=False)
    logger.info(f"Saved summary statistics to: {summary_path}")


def main():
    """Main execution function"""
    logger.info("=" * 80)
    logger.info("Starting Data Preprocessing for Push Sensitivity Analysis")
    logger.info("=" * 80)

    # Define paths
    output_path = Path(__file__).parent.parent.parent.parent.parent.parent / "data" / "intermediate" / "analysis_data.parquet"

    # Step 1: Load data
    df, no_push_member_ids = load_data()

    # Step 2: Assign push_group
    df = assign_push_group(df, no_push_member_ids)

    # Step 3: Identify first dormant entry
    customer_milestones = identify_first_dormant_entry(df)

    # Step 4: Create period indicators
    df = create_period_indicators(df, customer_milestones)

    # Step 5: Calculate summary statistics
    summary_df = calculate_summary_statistics(df)

    # Step 6: Save processed data
    save_processed_data(df, summary_df, output_path)

    logger.info("=" * 80)
    logger.info("Data preprocessing complete!")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
