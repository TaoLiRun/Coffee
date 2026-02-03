#!/usr/bin/env python3
"""
Script 3: Push Sensitivity Analysis (Difference-in-Differences)

Purpose: Test H2 - DiD analysis of push effectiveness on wake-up behavior
Key steps:
    1. Calculate post-dormant metrics (wakeup outcomes, push exposure)
    2. Construct DiD dataset (pre-post × push_group)
    3. Run basic DiD regression
    4. Run extended DiD with push intensity
    5. Run heterogeneous effects by push characteristics
    6. Event study visualization

Output: Regression tables, event study plots
"""

import pandas as pd
import numpy as np
import os
import logging
from pathlib import Path
import statsmodels.formula.api as smf
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
from linearmodels.panel import PanelOLS
import warnings
warnings.filterwarnings('ignore')

# Set up logging
log_dir = Path(__file__).parent.parent / "outputs" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_dir / "03_push_sensitivity.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Set style for plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 6)


def load_preprocessed_data():
    """Load the preprocessed data"""
    logger.info("Loading preprocessed data...")

    data_path = Path(__file__).parent.parent / "data" / "analysis_data.parquet"
    df = pd.read_parquet(data_path)
    logger.info(f"Loaded {len(df):,} records")

    return df


def calculate_did_metrics(df):
    """
    Calculate DiD metrics at the customer-dormant_period level.
    Focus on FIRST dormant period only (primary analysis).
    Vectorized implementation for efficiency.
    """
    logger.info("Calculating DiD metrics...")

    # Get push_group for each member
    push_groups = df.groupby('member_id')['push_group'].first()
    
    # Find first dormant period for each member
    dormant_data = df[df['dormant_period'] > 0].groupby('member_id')['dormant_period'].min()
    dormant_data = dormant_data.to_frame('first_dormant_id')
    
    # Get first dormant entry date for each member
    first_dormant_dates = df[df['dormant_period'] > 0].groupby('member_id').agg({
        'dt': 'min'
    }).rename(columns={'dt': 'first_dormant_date'})
    
    dormant_data = dormant_data.join(first_dormant_dates)
    
    logger.info(f"Found {len(dormant_data):,} customers with dormant periods")
    
    # --- PRE-PERIOD METRICS ---
    # Filter to pre-period purchases only
    df_with_dormant = df.merge(dormant_data[['first_dormant_date']], left_on='member_id', right_index=True, how='inner')
    
    pre_purchases = df_with_dormant[
        (df_with_dormant['dormant_period'] == 0) &
        (df_with_dormant['data_source'] == 1) &
        (df_with_dormant['dt'] < df_with_dormant['first_dormant_date'])
    ].copy()
    
    # Calculate pre-period metrics
    pre_metrics = pre_purchases.groupby('member_id').agg({
        'origin_money': 'mean',
        'dt': ['min', 'max', 'count']
    })
    pre_metrics.columns = ['pre_avg_value', 'pre_dt_min', 'pre_dt_max', 'pre_orders']
    
    # Calculate pre-period frequency
    pre_metrics['pre_weeks'] = (pre_metrics['pre_dt_max'] - pre_metrics['pre_dt_min']).dt.days / 7
    pre_metrics['pre_weeks'] = pre_metrics['pre_weeks'].clip(lower=1)
    pre_metrics.loc[pre_metrics['pre_orders'] == 1, 'pre_weeks'] = 1
    pre_metrics['pre_order_freq'] = pre_metrics['pre_orders'] / pre_metrics['pre_weeks']
    pre_metrics = pre_metrics[['pre_orders', 'pre_order_freq', 'pre_avg_value']]
    
    # --- POST-PERIOD METRICS ---
    # Merge to get first_dormant_id for filtering
    df_post = df.merge(dormant_data[['first_dormant_id']], left_on='member_id', right_index=True, how='inner')
    post_data = df_post[df_post['dormant_period'] == df_post['first_dormant_id']].copy()
    
    # Separate pushes and purchases
    post_pushes = post_data[post_data['data_source'] == 0]
    post_purchases = post_data[post_data['data_source'] == 1]
    
    # Wakeup metrics from purchases
    wakeup_metrics = post_purchases.groupby('member_id').agg({
        'days_since_purchase': 'min',
        'origin_money': 'first'
    }).rename(columns={
        'days_since_purchase': 'days_to_wakeup',
        'origin_money': 'wakeup_order_value'
    })
    wakeup_metrics['wakeup'] = 1
    
    # Push intensity metrics
    push_metrics = post_pushes.groupby('member_id').agg({
        'days_since_purchase': 'min',
        'use_discount': ['mean', lambda x: (x > 0).mean()],
        'dept_id': 'nunique'
    })
    push_metrics.columns = ['min_days_since_purchase', 'avg_push_discount', 'discount_push_share', 'trigger_diversity']
    push_metrics['first_push_timing'] = push_metrics['min_days_since_purchase'] - 30
    push_metrics['total_pushes'] = post_pushes.groupby('member_id').size()
    
    # Push intensity in first 7 days
    early_pushes = post_pushes[post_pushes['days_since_purchase'] <= 37]
    push_metrics['push_intensity_first_7d'] = early_pushes.groupby('member_id').size()
    
    push_metrics = push_metrics[['total_pushes', 'first_push_timing', 'push_intensity_first_7d', 
                                 'avg_push_discount', 'discount_push_share', 'trigger_diversity']]
    
    # --- COMBINE ALL METRICS ---
    did_df = dormant_data[['first_dormant_id']].copy()
    did_df['push_group'] = push_groups
    
    # Join pre-period metrics
    did_df = did_df.join(pre_metrics, how='left')
    
    # Join wakeup metrics
    did_df = did_df.join(wakeup_metrics, how='left')
    did_df['wakeup'] = did_df['wakeup'].fillna(0).astype(int)
    
    # Join push metrics
    did_df = did_df.join(push_metrics, how='left')
    did_df['total_pushes'] = did_df['total_pushes'].fillna(0).astype(int)
    did_df['push_intensity_first_7d'] = did_df['push_intensity_first_7d'].fillna(0).astype(int)
    did_df['avg_push_discount'] = did_df['avg_push_discount'].fillna(0)
    did_df['discount_push_share'] = did_df['discount_push_share'].fillna(0)
    did_df['trigger_diversity'] = did_df['trigger_diversity'].fillna(0).astype(int)
    
    # Reset index to make member_id a column
    did_df = did_df.reset_index()
    
    logger.info(f"Created DiD dataset with {len(did_df):,} customers")
    logger.info(f"push=0: {len(did_df[did_df['push_group'] == 0])} customers")
    logger.info(f"push=1: {len(did_df[did_df['push_group'] == 1])} customers")

    return did_df


def run_basic_did(did_df):
    """
    Run basic DiD regression:
    wakeup ~ push_group + post + push_group:post
    Note: In our data, we're comparing POST-dormant outcomes only,
    so we compare wakeup rates between push=0 and push=1 groups.
    """
    logger.info("=" * 80)
    logger.info("Running Basic DiD Regression")
    logger.info("=" * 80)

    # Since we have post-period outcomes, the "DiD" simplifies to comparing
    # wakeup rates between groups, controlling for pre-period characteristics

    # Simple comparison of wakeup rates
    wakeup_by_group = did_df.groupby('push_group')['wakeup'].agg(['mean', 'count', 'std'])
    logger.info("\nWakeup rates by group:")
    logger.info(wakeup_by_group.to_string())

    # Chi-square test
    from scipy.stats import chi2_contingency
    contingency = pd.crosstab(did_df['push_group'], did_df['wakeup'])
    chi2, p_value, dof, expected = chi2_contingency(contingency)
    logger.info(f"\nChi-square test: χ²={chi2:.4f}, p={p_value:.6f}")

    # Logistic regression: wakeup ~ push_group + pre_order_freq + pre_avg_value
    did_df['const'] = 1

    # Model 1: Unadjusted
    X1 = did_df[['const', 'push_group']]
    y = did_df['wakeup']

    # Remove rows with NaN
    valid_idx = did_df[['const', 'push_group', 'wakeup']].notna().all(axis=1)
    X1_valid = X1[valid_idx]
    y_valid = y[valid_idx]

    logit_model1 = sm.Logit(y_valid, X1_valid)
    result1 = logit_model1.fit(disp=0)

    logger.info("\nModel 1: wakeup ~ push_group")
    logger.info(result1.summary().tables[1])

    # Model 2: Adjusted for pre-period characteristics
    did_df_adj = did_df.dropna(subset=['push_group', 'wakeup', 'pre_order_freq', 'pre_avg_value'])
    X2 = did_df_adj[['const', 'push_group', 'pre_order_freq', 'pre_avg_value']]
    y2 = did_df_adj['wakeup']

    logit_model2 = sm.Logit(y2, X2)
    result2 = logit_model2.fit(disp=0)

    logger.info("\nModel 2: wakeup ~ push_group + pre_order_freq + pre_avg_value")
    logger.info(result2.summary().tables[1])

    results = {
        'model1': result1,
        'model2': result2,
        'wakeup_by_group': wakeup_by_group,
        'chi2': chi2,
        'p_value': p_value,
    }

    return results


def run_push_intensity_analysis(did_df):
    """
    Analyze how push INTENSITY affects wake-up, separately for each group.
    wakeup ~ push_intensity + push_intensity:push_group
    """
    logger.info("=" * 80)
    logger.info("Running Push Intensity Analysis")
    logger.info("=" * 80)

    # Filter to customers with at least one push
    push_df = did_df[did_df['total_pushes'] > 0].copy()
    logger.info(f"Customers with pushes: {len(push_df):,}")

    # Descriptive statistics
    logger.info("\nPush intensity by group:")
    intensity_stats = push_df.groupby('push_group')['total_pushes'].describe()
    logger.info(intensity_stats.to_string())

    # Correlation between push intensity and wakeup
    for group_val, group_name in [(0, 'push=0'), (1, 'push=1')]:
        group_data = push_df[push_df['push_group'] == group_val]
        if len(group_data) > 1:
            corr = group_data[['total_pushes', 'wakeup']].corr().iloc[0, 1]
            logger.info(f"\n{group_name}: correlation between pushes and wakeup = {corr:.4f}")

    # Regression: wakeup ~ total_pushes (separate by group)
    results_by_group = {}

    for group_val, group_name in [(0, 'push=0'), (1, 'push=1')]:
        group_data = push_df[push_df['push_group'] == group_val].copy()
        group_data['const'] = 1

        X = group_data[['const', 'total_pushes']]
        y = group_data['wakeup']

        logit_model = sm.Logit(y, X)
        result = logit_model.fit(disp=0)
        results_by_group[group_name] = result

        logger.info(f"\n{group_name}: wakeup ~ total_pushes")
        logger.info(result.summary().tables[1])

    return results_by_group


def run_heterogeneous_effects(did_df):
    """
    Analyze heterogeneous effects by push characteristics:
    - Discount depth (deep vs shallow)
    - Trigger type
    - Timing (early vs late pushes)
    """
    logger.info("=" * 80)
    logger.info("Running Heterogeneous Effects Analysis")
    logger.info("=" * 80)

    results = {}

    # A. By discount depth
    logger.info("\n--- Analysis by Discount Depth ---")

    # Classify pushes by discount depth
    did_df['has_discount_push'] = (did_df['discount_push_share'] > 0).astype(int)

    discount_stats = did_df.groupby(['push_group', 'has_discount_push'])['wakeup'].agg(['mean', 'count'])
    logger.info("\nWakeup rate by discount push availability:")
    logger.info(discount_stats.to_string())

    results['discount_depth'] = discount_stats

    # B. By trigger diversity
    logger.info("\n--- Analysis by Trigger Diversity ---")

    did_df['high_trigger_diversity'] = (did_df['trigger_diversity'] >= 2).astype(int)

    trigger_stats = did_df.groupby(['push_group', 'high_trigger_diversity'])['wakeup'].agg(['mean', 'count'])
    logger.info("\nWakeup rate by trigger diversity:")
    logger.info(trigger_stats.to_string())

    results['trigger_diversity'] = trigger_stats

    # C. By push timing (early pushes in first 7 days)
    logger.info("\n--- Analysis by Push Timing ---")

    did_df['has_early_pushes'] = (did_df['push_intensity_first_7d'] > 0).astype(int)

    timing_stats = did_df.groupby(['push_group', 'has_early_pushes'])['wakeup'].agg(['mean', 'count'])
    logger.info("\nWakeup rate by early push availability:")
    logger.info(timing_stats.to_string())

    results['timing'] = timing_stats

    return results


def create_event_study_plot(did_df):
    """
    Create event study visualization.
    Since we have first-dormant-period data, we show:
    - Pre-period metrics by group
    - Post-period wakeup rates by group
    """
    logger.info("Creating event study visualization...")

    output_dir = Path(__file__).parent.parent / "outputs" / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # Plot 1: Pre-period order frequency
    ax = axes[0]
    for group_val, group_name in [(0, 'push=0'), (1, 'push=1')]:
        group_data = did_df[did_df['push_group'] == group_val]['pre_order_freq'].dropna()
        ax.hist(group_data, bins=50, alpha=0.5, label=group_name, density=True)

    ax.set_xlabel('Pre-period Order Frequency')
    ax.set_ylabel('Density')
    ax.set_title('Pre-period: Order Frequency Distribution')
    ax.legend()
    ax.set_xlim(0, did_df['pre_order_freq'].quantile(0.95))

    # Plot 2: Wakeup rate comparison
    ax = axes[1]
    wakeup_rates = did_df.groupby('push_group')['wakeup'].mean()
    ax.bar(['push=0', 'push=1'], wakeup_rates.values,
           color=['#3498db', '#e74c3c'], alpha=0.7, edgecolor='black')
    ax.set_ylabel('Wake-up Rate')
    ax.set_title('Post-period: Wake-up Rate by Group')
    ax.set_ylim(0, 1)

    # Add percentage labels
    for i, (idx, val) in enumerate(wakeup_rates.items()):
        ax.text(i, val + 0.02, f'{val:.1%}', ha='center', fontsize=12)

    # Plot 3: Push intensity vs wakeup
    ax = axes[2]
    for group_val, group_name, color in [(0, 'push=0', '#3498db'), (1, 'push=1', '#e74c3c')]:
        group_data = did_df[(did_df['push_group'] == group_val) & (did_df['total_pushes'] > 0)]
        if len(group_data) > 0:
            # Bin by push count and calculate wakeup rate
            group_data['push_bin'] = pd.cut(group_data['total_pushes'],
                                           bins=[0, 5, 10, 20, 50, 100, 500],
                                           labels=['1-5', '6-10', '11-20', '21-50', '51-100', '100+'])
            binned = group_data.groupby('push_bin', observed=True)['wakeup'].mean()
            ax.plot(range(len(binned)), binned.values, marker='o', label=group_name, color=color)

    ax.set_xticks(range(6))
    ax.set_xticklabels(['1-5', '6-10', '11-20', '21-50', '51-100', '100+'])
    ax.set_xlabel('Number of Pushes')
    ax.set_ylabel('Wake-up Rate')
    ax.set_title('Push Intensity vs Wake-up Rate')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_dir / "event_study_plot.png", dpi=300, bbox_inches='tight')
    logger.info(f"Saved: {output_dir / 'event_study_plot.png'}")
    plt.close()


def save_results(did_df, basic_results, intensity_results, heterogeneous_results):
    """Save results to files"""
    logger.info("Saving results...")

    output_dir = Path(__file__).parent.parent / "outputs" / "tables"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save DiD dataset
    did_df.to_csv(output_dir / "did_dataset.csv", index=False)
    logger.info(f"Saved: {output_dir / 'did_dataset.csv'}")

    # Save summary statistics
    summary_stats = did_df.groupby('push_group').agg({
        'wakeup': ['mean', 'count'],
        'total_pushes': ['mean', 'median'],
        'days_to_wakeup': ['mean', 'median'],
        'pre_order_freq': 'mean',
    })
    summary_stats.to_csv(output_dir / "summary_statistics.csv")
    logger.info(f"Saved: {output_dir / 'summary_statistics.csv'}")


def main():
    """Main execution function"""
    logger.info("=" * 80)
    logger.info("Starting Push Sensitivity DiD Analysis")
    logger.info("=" * 80)

    # Step 1: Load preprocessed data
    df = load_preprocessed_data()

    # Step 2: Calculate DiD metrics
    did_df = calculate_did_metrics(df)

    # Step 3: Run basic DiD regression
    basic_results = run_basic_did(did_df)

    # Step 4: Run push intensity analysis
    intensity_results = run_push_intensity_analysis(did_df)

    # Step 5: Run heterogeneous effects analysis
    heterogeneous_results = run_heterogeneous_effects(did_df)

    # Step 6: Create visualizations
    create_event_study_plot(did_df)

    # Step 7: Save results
    save_results(did_df, basic_results, intensity_results, heterogeneous_results)

    logger.info("=" * 80)
    logger.info("Push sensitivity DiD analysis complete!")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
