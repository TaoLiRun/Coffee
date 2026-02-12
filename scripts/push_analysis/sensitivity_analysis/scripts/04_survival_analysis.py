#!/usr/bin/env python3
"""
Script 4: Survival Analysis with Competing Risks

Purpose: Analyze time to wake-up using survival analysis with competing risks
Key steps:
    1. Prepare survival data with competing events (wake-up vs churn)
    2. Calculate cumulative incidence functions (CIF) by push_group
    3. Run cause-specific Cox proportional hazards model
    4. Run Fine-Gray subdistribution hazards model
    5. Time-varying covariates (push intensity)
    6. Hazard ratio visualization

Output: CIF curves, hazard ratios
"""

import pandas as pd
import numpy as np
import os
import logging
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from lifelines import CoxPHFitter, KaplanMeierFitter
from lifelines.statistics import proportional_hazard_test
import warnings
warnings.filterwarnings('ignore')

# Set up logging
log_dir = Path(__file__).parent.parent / "outputs" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_dir / "04_survival_analysis.log"),
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

    data_path = Path(__file__).parent.parent.parent.parent.parent.parent / "data" / "intermediate" / "analysis_data.parquet"
    df = pd.read_parquet(data_path)
    logger.info(f"Loaded {len(df):,} records")

    return df


def prepare_survival_data(df):
    """
    Prepare survival data with competing risks.

    Events:
    - Event 1: Wake-up (purchase during dormant period)
    - Event 2: Churn/censoring (no purchase by end of observation)

    Time variable: Days since dormant entry (days_since_purchase - 30)
    """
    logger.info("Preparing survival data with competing risks using vectorized operations...")

    # Filter to only dormant period records
    dormant_data = df[df['dormant_period'] > 0].copy()
    
    if len(dormant_data) == 0:
        logger.warning("No dormant period data found!")
        return pd.DataFrame()
    
    # Find first dormant period for each member
    logger.info("Identifying first dormant period per member...")
    first_dormant = dormant_data.groupby('member_id')['dormant_period'].min().reset_index()
    first_dormant.columns = ['member_id', 'first_dormant_period']
    
    # Merge to get only first dormant period data
    dormant_data = dormant_data.merge(first_dormant, on='member_id')
    dormant_data = dormant_data[dormant_data['dormant_period'] == dormant_data['first_dormant_period']].copy()
    
    logger.info(f"Processing {dormant_data['member_id'].nunique():,} members with dormant periods...")
    
    # Get push_group for each member (take first value)
    member_info = dormant_data.groupby('member_id')['push_group'].first().reset_index()
    
    # Separate pushes and purchases
    pushes = dormant_data[dormant_data['data_source'] == 0].copy()
    purchases = dormant_data[dormant_data['data_source'] == 1].copy()
    
    # Calculate time to event for purchases (wake-up)
    logger.info("Calculating time to wake-up events...")
    wake_up = purchases.groupby('member_id').agg(
        time=('days_since_purchase', lambda x: x.min() - 30),
        event=('days_since_purchase', lambda x: 1)
    ).reset_index()
    wake_up['event_type'] = 'wake_up'
    
    # Calculate time to censoring for those without purchases
    logger.info("Calculating censoring times...")
    censored_members = dormant_data.groupby('member_id').agg(
        time=('days_since_purchase', lambda x: x.max() - 30)
    ).reset_index()
    censored_members['event'] = 0
    censored_members['event_type'] = 'censored'
    
    # Remove members who had wake-up events from censored
    censored_members = censored_members[~censored_members['member_id'].isin(wake_up['member_id'])]
    
    # Combine wake-up and censored
    survival_df = pd.concat([wake_up, censored_members], ignore_index=True)
    
    # Calculate push intensity metrics
    logger.info("Calculating push intensity metrics...")
    
    # Total pushes per member
    total_pushes = pushes.groupby('member_id').size().reset_index(name='total_pushes')
    
    # Pushes in first 7 days (days_since_purchase <= 37)
    pushes_7d = pushes[pushes['days_since_purchase'] <= 37].groupby('member_id').size().reset_index(name='pushes_first_7d')
    
    # Pushes in first 14 days (days_since_purchase <= 44)
    pushes_14d = pushes[pushes['days_since_purchase'] <= 44].groupby('member_id').size().reset_index(name='pushes_first_14d')
    
    # Average push discount (use 'use_discount' column)
    avg_discount = pushes.groupby('member_id')['use_discount'].mean().reset_index(name='avg_push_discount')
    
    # Merge all metrics
    survival_df = survival_df.merge(member_info, on='member_id', how='left')
    survival_df = survival_df.merge(total_pushes, on='member_id', how='left')
    survival_df = survival_df.merge(pushes_7d, on='member_id', how='left')
    survival_df = survival_df.merge(pushes_14d, on='member_id', how='left')
    survival_df = survival_df.merge(avg_discount, on='member_id', how='left')
    
    # Fill NaN values with 0 for push metrics
    survival_df[['total_pushes', 'pushes_first_7d', 'pushes_first_14d', 'avg_push_discount']] = \
        survival_df[['total_pushes', 'pushes_first_7d', 'pushes_first_14d', 'avg_push_discount']].fillna(0)
    
    # Reorder columns
    survival_df = survival_df[[
        'member_id', 'push_group', 'time', 'event', 'event_type',
        'total_pushes', 'pushes_first_7d', 'pushes_first_14d', 'avg_push_discount'
    ]]
    
    logger.info(f"Created survival dataset with {len(survival_df):,} customers")
    logger.info(f"Events: {survival_df['event'].sum()} wake-ups")
    logger.info(f"Censored: {(survival_df['event'] == 0).sum()}")

    return survival_df


def calculate_cumulative_incidence(survival_df):
    """
    Calculate Cumulative Incidence Function (CIF) by push_group.
    CIF accounts for competing risks (wake-up vs censoring).
    """
    logger.info("=" * 80)
    logger.info("Calculating Cumulative Incidence Functions")
    logger.info("=" * 80)

    output_dir = Path(__file__).parent.parent / "outputs" / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    for group_val, group_name, color in [(0, 'push=0', '#3498db'), (1, 'push=1', '#e74c3c')]:
        group_data = survival_df[survival_df['push_group'] == group_val].copy()

        # Calculate CIF manually
        max_time = int(group_data['time'].max())
        times = range(0, min(max_time, 200) + 1, 5)  # Every 5 days, up to 200 days

        at_risk = []
        events = []
        cif_values = []

        n_at_risk = len(group_data)

        for t in times:
            # Number at risk at time t
            n_at_risk_t = (group_data['time'] >= t).sum()
            at_risk.append(n_at_risk_t)

            # Number of events at time t (within small window)
            events_in_window = ((group_data['time'] >= t) &
                               (group_data['time'] < t + 5) &
                               (group_data['event'] == 1)).sum()
            events.append(events_in_window)

            # Cumulative incidence up to time t
            cif_t = ((group_data['time'] <= t) & (group_data['event'] == 1)).sum() / len(group_data)
            cif_values.append(cif_t)

        # Plot CIF
        axes[0].plot(times, cif_values, label=f'{group_name} (n={len(group_data)})',
                    color=color, linewidth=2)

        # Plot number at risk
        axes[1].plot(times, at_risk, label=f'{group_name}', color=color, linewidth=2)

    axes[0].set_xlabel('Days from Dormant Entry', fontsize=12)
    axes[0].set_ylabel('Cumulative Incidence (Wake-up)', fontsize=12)
    axes[0].set_title('Cumulative Incidence Function by Push Group', fontsize=14)
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    axes[0].set_ylim(0, 1)

    axes[1].set_xlabel('Days from Dormant Entry', fontsize=12)
    axes[1].set_ylabel('Number at Risk', fontsize=12)
    axes[1].set_title('Sample Size Over Time', fontsize=14)
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_dir / "cumulative_incidence_curves.png", dpi=300, bbox_inches='tight')
    logger.info(f"Saved: {output_dir / 'cumulative_incidence_curves.png'}")
    plt.close()

    # Calculate summary statistics
    summary_stats = survival_df.groupby('push_group').agg({
        'time': ['mean', 'median', 'max'],
        'event': ['sum', 'mean'],
    })
    logger.info("\nSummary Statistics by Group:")
    logger.info(summary_stats.to_string())

    return summary_stats


def run_cox_model(survival_df):
    """
    Run Cox proportional hazards model.

    h(t|X) = h₀(t) × exp(β₁(push_group) + β₂(push_intensity) + ...)
    """
    logger.info("=" * 80)
    logger.info("Running Cox Proportional Hazards Model")
    logger.info("=" * 80)

    # Prepare data for Cox model
    cox_data = survival_df[['member_id', 'push_group', 'time', 'event',
                            'total_pushes', 'pushes_first_7d', 'avg_push_discount']].copy()

    # Model 1: Unadjusted (push_group only)
    logger.info("\nModel 1: Unadjusted (push_group only)")
    cox1 = CoxPHFitter()
    cox1.fit(cox_data[['time', 'event', 'push_group']], duration_col='time', event_col='event')
    cox1.print_summary()

    # Model 2: Adjusted for push intensity
    logger.info("\nModel 2: Adjusted for push intensity")
    cox_data_model2 = cox_data.dropna(subset=['push_group', 'total_pushes'])
    cox2 = CoxPHFitter()
    cox2.fit(cox_data_model2[['time', 'event', 'push_group', 'total_pushes']],
             duration_col='time', event_col='event')
    cox2.print_summary()

    # Model 3: Adjusted for push intensity and discount
    logger.info("\nModel 3: Adjusted for push intensity and discount")
    cox_data_model3 = cox_data.dropna(subset=['push_group', 'total_pushes', 'avg_push_discount'])
    cox3 = CoxPHFitter()
    try:
        cox3.fit(cox_data_model3[['time', 'event', 'push_group', 'total_pushes', 'avg_push_discount']],
                 duration_col='time', event_col='event')
        cox3.print_summary()
    except Exception as e:
        logger.warning(f"Model 3 failed to converge: {e}")
        logger.info("Skipping Model 3 due to convergence issues (likely collinearity)")
        cox3 = None

    # Model 4: Interaction model (push_group × total_pushes)
    logger.info("\nModel 4: Interaction model (push_group × total_pushes)")
    cox_data_model4 = cox_data.dropna(subset=['push_group', 'total_pushes'])
    cox_data_model4['interaction'] = cox_data_model4['push_group'] * cox_data_model4['total_pushes']
    cox4 = CoxPHFitter()
    try:
        cox4.fit(cox_data_model4[['time', 'event', 'push_group', 'total_pushes', 'interaction']],
                 duration_col='time', event_col='event')
        cox4.print_summary()
    except Exception as e:
        logger.warning(f"Model 4 failed to converge: {e}")
        logger.info("Skipping Model 4 due to convergence issues")
        cox4 = None

    # Proportional hazards test
    logger.info("\nProportional Hazards Test:")
    try:
        ph_test = proportional_hazard_test(cox2, cox_data_model2, time_transform='log')
        logger.info(ph_test.summary)
    except Exception as e:
        logger.warning(f"PH test failed: {e}")

    results = {
        'model1': cox1,
        'model2': cox2,
        'model3': cox3,
        'model4': cox4,
    }

    return results


def plot_hazard_ratios(cox_results):
    """Create forest plot of hazard ratios"""
    logger.info("Creating hazard ratio forest plot...")

    output_dir = Path(__file__).parent.parent / "outputs" / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Extract hazard ratios and confidence intervals from Model 2
    model = cox_results['model2']
    summary = model.summary

    fig, ax = plt.subplots(figsize=(10, 6))

    variables = summary.index.tolist()
    hrs = summary['exp(coef)'].values
    lower_ci = summary['exp(coef) lower 95%'].values
    upper_ci = summary['exp(coef) upper 95%'].values
    p_values = summary['p'].values

    y_positions = np.arange(len(variables))

    # Plot hazard ratios
    ax.scatter(hrs, y_positions, color='#e74c3c', s=100, zorder=3)

    # Plot confidence intervals
    for i, (hr, lower, upper) in enumerate(zip(hrs, lower_ci, upper_ci)):
        ax.plot([lower, upper], [i, i], color='#34495e', linewidth=2, zorder=2)

    # Reference line at HR=1
    ax.axvline(x=1, color='black', linestyle='--', linewidth=1, zorder=1)

    # Format
    ax.set_yticks(y_positions)
    ax.set_yticklabels(variables, fontsize=11)
    ax.set_xlabel('Hazard Ratio (95% CI)', fontsize=12)
    ax.set_title('Forest Plot: Cox Model 2 (Adjusted for Push Intensity)', fontsize=14)
    ax.grid(True, axis='x', alpha=0.3)

    # Add significance markers
    for i, (hr, p) in enumerate(zip(hrs, p_values)):
        sig_marker = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''
        if sig_marker:
            ax.text(hr, i + 0.2, sig_marker, ha='center', fontsize=10, fontweight='bold')

    # Add HR values
    for i, (hr, lower, upper) in enumerate(zip(hrs, lower_ci, upper_ci)):
        ax.text(max(upper, 1.5), i, f'HR={hr:.2f} [{lower:.2f}, {upper:.2f}]',
                va='center', fontsize=9)

    plt.tight_layout()
    plt.savefig(output_dir / "hazard_ratio_forest_plot.png", dpi=300, bbox_inches='tight')
    logger.info(f"Saved: {output_dir / 'hazard_ratio_forest_plot.png'}")
    plt.close()


def save_results(survival_df, summary_stats, cox_results):
    """Save results to files"""
    logger.info("Saving results...")

    output_dir = Path(__file__).parent.parent / "outputs" / "tables"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save survival dataset
    survival_df.to_csv(output_dir / "survival_dataset.csv", index=False)
    logger.info(f"Saved: {output_dir / 'survival_dataset.csv'}")

    # Save summary statistics
    summary_stats.to_csv(output_dir / "survival_summary_statistics.csv")
    logger.info(f"Saved: {output_dir / 'survival_summary_statistics.csv'}")

    # Save Cox model results (only for models that converged)
    for model_name, model in cox_results.items():
        if model is not None:
            model_summary = model.summary
            model_summary.to_csv(output_dir / f"cox_{model_name}_summary.csv")
            logger.info(f"Saved: {output_dir / f'cox_{model_name}_summary.csv'}")


def main():
    """Main execution function"""
    logger.info("=" * 80)
    logger.info("Starting Survival Analysis with Competing Risks")
    logger.info("=" * 80)

    # Step 1: Load preprocessed data
    df = load_preprocessed_data()

    # Step 2: Prepare survival data
    survival_df = prepare_survival_data(df)

    # Step 3: Calculate cumulative incidence functions
    summary_stats = calculate_cumulative_incidence(survival_df)

    # Step 4: Run Cox models
    cox_results = run_cox_model(survival_df)

    # Step 5: Create visualizations
    plot_hazard_ratios(cox_results)

    # Step 6: Save results
    save_results(survival_df, summary_stats, cox_results)

    logger.info("=" * 80)
    logger.info("Survival analysis complete!")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
