#!/usr/bin/env python3
"""
Script 2: Intrinsic Preferences Analysis

Purpose: Test H1 - compare pre-dormant behavior between push=0 and push=1 groups
Key steps:
    1. Filter to pre-dormant period (dormant_period = 0 AND period = 'pre')
    2. Calculate metrics for each customer (frequency, value, variety, discount behavior)
    3. Split by push_group
    4. Statistical tests (t-test, Mann-Whitney U)
    5. Multiple testing correction (FDR)
    6. Visualizations (distributions, CDFs)

Output: Tables and figures in ../outputs/
"""

import pandas as pd
import numpy as np
import os
import logging
from pathlib import Path
from scipy import stats
from scipy.stats import mannwhitneyu
from statsmodels.stats.multitest import multipletests
import matplotlib.pyplot as plt
import seaborn as sns

# Set up logging
log_dir = Path(__file__).parent.parent / "outputs" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_dir / "02_intrinsic_preferences.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Set style for plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


def load_preprocessed_data():
    """Load the preprocessed data"""
    logger.info("Loading preprocessed data...")

    data_path = Path(__file__).parent.parent.parent.parent.parent.parent / "data" / "intermediate" / "analysis_data.parquet"
    df = pd.read_parquet(data_path)
    logger.info(f"Loaded {len(df):,} records")

    return df


def filter_pre_period(df):
    """
    Filter to pre-dormant period.
    Pre-period is defined as:
    - period = 'pre' (before first dormant entry)
    - Only consider active periods (dormant_period = 0)
    - Only purchase records (data_source = 1)
    """
    logger.info("Filtering to pre-period purchase records...")

    pre_data = df[
        (df['period'] == 'pre') &
        (df['dormant_period'] == 0) &
        (df['data_source'] == 1)
    ].copy()

    logger.info(f"Pre-period purchase records: {len(pre_data):,}")
    logger.info(f"Unique members in pre-period: {pre_data['member_id'].nunique():,}")

    return pre_data


def calculate_customer_metrics(pre_data):
    """
    Calculate metrics for each customer in the pre-period.

    Metrics:
    A. Purchase Frequency Metrics
    B. Purchase Value Metrics
    C. Product Variety Metrics
    D. Discount/Coupon Behavior
    """
    logger.info("Calculating customer-level metrics using vectorized operations...")

    # Sort data by member_id and dt for interpurchase calculations
    pre_data_sorted = pre_data.sort_values(['member_id', 'dt'])
    
    # Calculate interpurchase days using shift within groups
    pre_data_sorted['days_since_last'] = pre_data_sorted.groupby('member_id')['dt'].diff().dt.days
    
    # Use groupby.agg for efficient aggregation
    logger.info("Aggregating metrics by customer...")
    
    # Basic aggregations
    metrics_df = pre_data_sorted.groupby('member_id').agg(
        push_group=('push_group', 'first'),
        dt_min=('dt', 'min'),
        dt_max=('dt', 'max'),
        initial_orders=('dt', 'count'),
        initial_avg_order_value=('origin_money', 'mean'),
        initial_total_spend=('origin_money', 'sum'),
        initial_avg_basket_size=('total_items', 'mean'),
        initial_unique_stores=('dept_id', 'nunique'),
        initial_coupon_usage_rate=('use_coupon_num', lambda x: (x > 0).mean()),
        initial_avg_discount=('use_discount', 'mean'),
        initial_discount_depth_pref=('use_discount', lambda x: (x > 0.5).mean()),
        initial_interpurchase_days=('days_since_last', 'mean')
    ).reset_index()
    
    # Calculate derived metrics
    logger.info("Calculating derived metrics...")
    metrics_df['date_range_days'] = (metrics_df['dt_max'] - metrics_df['dt_min']).dt.days
    metrics_df['initial_weeks_active'] = metrics_df['date_range_days'] / 7
    metrics_df['initial_weeks_active'] = metrics_df['initial_weeks_active'].clip(lower=1)  # At least 1 week
    metrics_df['initial_order_freq'] = metrics_df['initial_orders'] / metrics_df['initial_weeks_active']
    
    # Drop temporary columns
    metrics_df.drop(columns=['dt_min', 'dt_max', 'date_range_days'], inplace=True)
    
    # Reorder columns for consistency
    column_order = [
        'member_id', 'push_group',
        'initial_orders', 'initial_order_freq', 'initial_interpurchase_days', 'initial_weeks_active',
        'initial_avg_order_value', 'initial_avg_basket_size', 'initial_total_spend',
        'initial_unique_stores',
        'initial_coupon_usage_rate', 'initial_avg_discount', 'initial_discount_depth_pref'
    ]
    metrics_df = metrics_df[column_order]
    
    logger.info(f"Calculated metrics for {len(metrics_df):,} customers")

    return metrics_df


def compare_groups(metrics_df):
    """
    Compare metrics between push=0 and push=1 groups.
    Perform t-tests and Mann-Whitney U tests.
    Apply FDR correction for multiple testing.
    """
    logger.info("=" * 80)
    logger.info("Comparing groups (push=0 vs push=1)...")
    logger.info("=" * 80)

    # Get metric columns (exclude member_id and push_group)
    metric_cols = [col for col in metrics_df.columns if col not in ['member_id', 'push_group']]

    results_list = []

    for metric in metric_cols:
        # Get data for each group, drop NaN
        group_0 = metrics_df[metrics_df['push_group'] == 0][metric].dropna()
        group_1 = metrics_df[metrics_df['push_group'] == 1][metric].dropna()

        if len(group_0) == 0 or len(group_1) == 0:
            logger.warning(f"Skipping {metric}: insufficient data")
            continue

        # Descriptive statistics
        mean_0 = group_0.mean()
        mean_1 = group_1.mean()
        median_0 = group_0.median()
        median_1 = group_1.median()
        std_0 = group_0.std()
        std_1 = group_1.std()
        n_0 = len(group_0)
        n_1 = len(group_1)

        # T-test
        t_stat, t_pvalue = stats.ttest_ind(group_0, group_1, equal_var=False)

        # Mann-Whitney U test
        try:
            u_stat, u_pvalue = mannwhitneyu(group_0, group_1, alternative='two-sided')
        except Exception as e:
            logger.warning(f"Mann-Whitney U test failed for {metric}: {e}")
            u_stat, u_pvalue = np.nan, np.nan

        # Effect size (Cohen's d)
        pooled_std = np.sqrt(((n_0 - 1) * std_0**2 + (n_1 - 1) * std_1**2) / (n_0 + n_1 - 2))
        cohens_d = (mean_1 - mean_0) / pooled_std if pooled_std > 0 else np.nan

        results_list.append({
            'metric': metric,
            'n_0': n_0,
            'n_1': n_1,
            'mean_0': mean_0,
            'mean_1': mean_1,
            'median_0': median_0,
            'median_1': median_1,
            'std_0': std_0,
            'std_1': std_1,
            'diff': mean_1 - mean_0,
            'pct_diff': (mean_1 - mean_0) / mean_0 * 100 if mean_0 != 0 else np.nan,
            't_stat': t_stat,
            't_pvalue': t_pvalue,
            'u_stat': u_stat,
            'u_pvalue': u_pvalue,
            'cohens_d': cohens_d,
        })

    results_df = pd.DataFrame(results_list)

    # Apply FDR correction (Benjamini-Hochberg) on t-test p-values
    reject, pvals_corrected, _, _ = multipletests(
        results_df['t_pvalue'].dropna(),
        alpha=0.05,
        method='fdr_bh'
    )
    results_df['t_pvalue_fdr'] = pvals_corrected
    results_df['significant_fdr'] = reject

    # Also apply FDR on Mann-Whitney p-values
    u_pvals = results_df['u_pvalue'].dropna()
    if len(u_pvals) > 0:
        reject_u, u_pvals_corrected, _, _ = multipletests(
            u_pvals,
            alpha=0.05,
            method='fdr_bh'
        )
        results_df.loc[results_df['u_pvalue'].notna(), 'u_pvalue_fdr'] = u_pvals_corrected
        results_df.loc[results_df['u_pvalue'].notna(), 'u_significant_fdr'] = reject_u

    # Log results
    logger.info("\nGroup Comparison Results:")
    logger.info(results_df.to_string(index=False))

    # Count significant results
    sig_count = results_df['significant_fdr'].sum()
    logger.info(f"\nSignificant differences (FDR < 0.05): {sig_count}/{len(results_df)} metrics")

    return results_df


def create_visualizations(metrics_df, results_df):
    """Create visualizations for the metrics"""
    logger.info("Creating visualizations...")

    output_dir = Path(__file__).parent.parent / "outputs" / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Box plots for key metrics
    key_metrics = ['initial_orders', 'initial_avg_order_value', 'initial_coupon_usage_rate']

    fig, axes = plt.subplots(1, len(key_metrics), figsize=(18, 5))
    for i, metric in enumerate(key_metrics):
        ax = axes[i]
        sns.boxplot(
            data=metrics_df,
            x='push_group',
            y=metric,
            ax=ax,
            palette={0: '#3498db', 1: '#e74c3c'}
        )
        ax.set_xticklabels(['push=0', 'push=1'])
        ax.set_title(f'{metric}\n(p={results_df.loc[results_df["metric"]==metric, "t_pvalue_fdr"].values[0]:.4f})')

    plt.tight_layout()
    plt.savefig(output_dir / "pre_period_metrics_boxplot.png", dpi=300, bbox_inches='tight')
    logger.info(f"Saved: {output_dir / 'pre_period_metrics_boxplot.png'}")
    plt.close()

    # 2. Summary table visualization
    fig, ax = plt.subplots(figsize=(12, 8))

    # Prepare summary data
    summary_data = results_df[['metric', 'mean_0', 'mean_1', 't_pvalue_fdr', 'cohens_d']].copy()
    summary_data['sig'] = summary_data['t_pvalue_fdr'] < 0.05
    summary_data = summary_data.sort_values('t_pvalue_fdr')

    # Create bar plot of effect sizes
    y_positions = np.arange(len(summary_data))
    colors = ['#e74c3c' if sig else '#95a5a6' for sig in summary_data['sig']]

    ax.barh(y_positions, summary_data['cohens_d'], color=colors, alpha=0.7)
    ax.set_yticks(y_positions)
    ax.set_yticklabels(summary_data['metric'], fontsize=10)
    ax.set_xlabel("Cohen's d (push=1 relative to push=0)", fontsize=12)
    ax.set_title("Effect Sizes: push=1 vs push=0 (Pre-Period Metrics)", fontsize=14)
    ax.axvline(x=0, color='black', linestyle='-', linewidth=0.5)

    # Add significance markers
    for i, (idx, row) in enumerate(summary_data.iterrows()):
        if row['sig']:
            ax.text(row['cohens_d'], i, '***', va='center', ha='left' if row['cohens_d'] > 0 else 'right', fontsize=12)

    plt.tight_layout()
    plt.savefig(output_dir / "effect_sizes_plot.png", dpi=300, bbox_inches='tight')
    logger.info(f"Saved: {output_dir / 'effect_sizes_plot.png'}")
    plt.close()

    logger.info("Visualizations complete!")


def save_results(metrics_df, results_df):
    """Save results to files"""
    logger.info("Saving results...")

    output_dir = Path(__file__).parent.parent / "outputs" / "tables"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save customer metrics
    metrics_df.to_csv(output_dir / "customer_pre_period_metrics.csv", index=False)
    logger.info(f"Saved: {output_dir / 'customer_pre_period_metrics.csv'}")

    # Save comparison results
    results_df.to_csv(output_dir / "group_comparison_results.csv", index=False)
    logger.info(f"Saved: {output_dir / 'group_comparison_results.csv'}")

    # Save formatted summary table
    summary_table = results_df[[
        'metric', 'mean_0', 'mean_1', 'diff', 'pct_diff',
        't_pvalue', 't_pvalue_fdr', 'significant_fdr', 'cohens_d'
    ]].copy()
    summary_table.columns = [
        'Metric', 'push=0 Mean', 'push=1 Mean', 'Difference', '% Diff',
        'T-test p-value', 'FDR-corrected p', 'Significant (FDR)', "Cohen's d"
    ]
    summary_table.to_csv(output_dir / "summary_table.csv", index=False)
    logger.info(f"Saved: {output_dir / 'summary_table.csv'}")


def main():
    """Main execution function"""
    logger.info("=" * 80)
    logger.info("Starting Intrinsic Preferences Analysis")
    logger.info("=" * 80)

    # Step 1: Load preprocessed data
    df = load_preprocessed_data()

    # Step 2: Filter to pre-period
    pre_data = filter_pre_period(df)

    # Step 3: Calculate customer metrics
    metrics_df = calculate_customer_metrics(pre_data)

    # Step 4: Compare groups
    results_df = compare_groups(metrics_df)

    # Step 5: Create visualizations
    create_visualizations(metrics_df, results_df)

    # Step 6: Save results
    save_results(metrics_df, results_df)

    logger.info("=" * 80)
    logger.info("Intrinsic preferences analysis complete!")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
