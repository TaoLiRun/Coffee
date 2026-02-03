import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from pathlib import Path
from scipy import stats

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler('compare_customers_with_and_without_push.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Set style for plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)


# ============================================================================
# STATISTICAL TESTING HELPER FUNCTIONS
# ============================================================================

def check_skewness(data, threshold=1.0):
    """Check if data is highly skewed."""
    data_clean = data.dropna()
    if len(data_clean) == 0:
        return False, 0
    skewness = stats.skew(data_clean)
    return abs(skewness) > threshold, skewness


def perform_ttest(group1_data, group2_data, metric_name, group1_name="push=0", group2_name="push=1"):
    """
    Perform independent t-test with automatic skewness detection.
    Reports both untransformed and log-transformed results if skewed.
    """
    # Remove NaN values
    g1 = group1_data.dropna()
    g2 = group2_data.dropna()
    
    if len(g1) == 0 or len(g2) == 0:
        logger.warning(f"Cannot perform t-test for {metric_name}: empty groups")
        return
    
    # Descriptive statistics
    logger.info(f"\n  {metric_name}:")
    logger.info(f"    {group1_name}: n={len(g1)}, mean={g1.mean():.4f}, median={g1.median():.4f}, std={g1.std():.4f}")
    logger.info(f"    {group2_name}: n={len(g2)}, mean={g2.mean():.4f}, median={g2.median():.4f}, std={g2.std():.4f}")
    
    # Untransformed t-test
    t_stat, p_value = stats.ttest_ind(g1, g2, equal_var=False)
    sig_marker = "***" if p_value < 0.001 else "**" if p_value < 0.01 else "*" if p_value < 0.05 else "ns"
    logger.info(f"    Untransformed t-test: t={t_stat:.4f}, p={p_value:.6f} {sig_marker}")
    
    # Check skewness
    is_skewed_g1, skew_g1 = check_skewness(g1)
    is_skewed_g2, skew_g2 = check_skewness(g2)
    
    if is_skewed_g1 or is_skewed_g2:
        logger.info(f"    Skewness detected: {group1_name}={skew_g1:.2f}, {group2_name}={skew_g2:.2f}")
        # Log transform (adding 1 to handle zeros)
        g1_log = np.log1p(g1)
        g2_log = np.log1p(g2)
        t_stat_log, p_value_log = stats.ttest_ind(g1_log, g2_log, equal_var=False)
        sig_marker_log = "***" if p_value_log < 0.001 else "**" if p_value_log < 0.01 else "*" if p_value_log < 0.05 else "ns"
        logger.info(f"    Log-transformed t-test: t={t_stat_log:.4f}, p={p_value_log:.6f} {sig_marker_log}")
        logger.info(f"      Log-transformed means: {group1_name}={g1_log.mean():.4f}, {group2_name}={g2_log.mean():.4f}")


def perform_chi_square(group1_success, group1_total, group2_success, group2_total, 
                       metric_name, group1_name="push=0", group2_name="push=1"):
    """
    Perform chi-square test for proportion comparison.
    """
    if group1_total == 0 or group2_total == 0:
        logger.warning(f"Cannot perform chi-square test for {metric_name}: zero totals")
        return
    
    prop1 = group1_success / group1_total if group1_total > 0 else 0
    prop2 = group2_success / group2_total if group2_total > 0 else 0
    
    logger.info(f"\n  {metric_name}:")
    logger.info(f"    {group1_name}: {group1_success}/{group1_total} = {prop1:.4f}")
    logger.info(f"    {group2_name}: {group2_success}/{group2_total} = {prop2:.4f}")
    
    # Create contingency table
    contingency_table = np.array([
        [group1_success, group1_total - group1_success],
        [group2_success, group2_total - group2_success]
    ])
    
    chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
    sig_marker = "***" if p_value < 0.001 else "**" if p_value < 0.01 else "*" if p_value < 0.05 else "ns"
    logger.info(f"    Chi-square test: χ²={chi2:.4f}, p={p_value:.6f} {sig_marker}")


# ============================================================================
# DATA LOADING AND GROUP STATISTICS
# ============================================================================

def load_data():
    """Load no_push_members and combined_push_purchase_analysis data"""
    logger.info("Loading data...")
    
    # Load no_push_members
    no_push_members = pd.read_csv('../processed_data/no_push_members.csv')
    no_push_member_ids = set(no_push_members['member_id'].unique())
    
    # Load combined_push_purchase_analysis
    combined_data = pd.read_parquet('combined_push_purchase_analysis.parquet')

    logger.info(f"Unique members in combined data: {combined_data['member_id'].nunique()}")
    
    # Split into two groups
    group_no_push = combined_data[combined_data['member_id'].isin(no_push_member_ids)].copy()
    group_with_push = combined_data[~combined_data['member_id'].isin(no_push_member_ids)].copy()
    
    logger.info(f"Group push=0: {group_no_push['member_id'].nunique()} unique members, {len(group_no_push)} records")
    logger.info(f"Group push=1: {group_with_push['member_id'].nunique()} unique members, {len(group_with_push)} records")
    
    # ========================================================================
    # DETAILED MEMBER-LEVEL STATISTICS
    # ========================================================================
    logger.info("\n" + "="*80)
    logger.info("DETAILED GROUP STATISTICS (Member-Level Analysis)")
    logger.info("="*80)
    
    # Calculate member-level metrics for both groups
    for group_name, group_data in [("push=0", group_no_push), ("push=1", group_with_push)]:
        logger.info(f"\n--- {group_name} Group Statistics ---")
        
        # Purchases per member
        purchases_per_member = group_data[group_data['data_source'] == 1].groupby('member_id').size()
        logger.info(f"Purchases per member: min={purchases_per_member.min()}, mean={purchases_per_member.mean():.2f}, "
                   f"median={purchases_per_member.median():.0f}, max={purchases_per_member.max()}")
        
        # Dormant episodes per member
        dormant_episodes = group_data.groupby('member_id')['dormant_period'].max()
        logger.info(f"Dormant episodes per member: min={dormant_episodes.min()}, mean={dormant_episodes.mean():.2f}, "
                   f"median={dormant_episodes.median():.0f}, max={dormant_episodes.max()}")
        
        # Purchase values (only for purchase records)
        purchase_records = group_data[group_data['data_source'] == 1].copy()
        if len(purchase_records) > 0:
            avg_order_value = purchase_records.groupby('member_id')['origin_money'].mean()
            avg_basket_size = purchase_records.groupby('member_id')['total_items'].mean()
            logger.info(f"Avg order value per member: min={avg_order_value.min():.2f}, mean={avg_order_value.mean():.2f}, "
                       f"median={avg_order_value.median():.2f}, max={avg_order_value.max():.2f}")
            logger.info(f"Avg basket size per member: min={avg_basket_size.min():.2f}, mean={avg_basket_size.mean():.2f}, "
                       f"median={avg_basket_size.median():.2f}, max={avg_basket_size.max():.2f}")
        
        # Inter-purchase intervals for active periods (dormant_period == 0)
        active_purchases = group_data[(group_data['data_source'] == 1) & (group_data['dormant_period'] == 0)].copy()
        active_purchases = active_purchases.sort_values(['member_id', 'dt'])
        active_purchases['days_to_next'] = active_purchases.groupby('member_id')['dt'].diff().dt.days
        inter_purchase_days = active_purchases['days_to_next'].dropna()
        if len(inter_purchase_days) > 0:
            logger.info(f"Inter-purchase days (active periods): min={inter_purchase_days.min():.0f}, "
                       f"mean={inter_purchase_days.mean():.2f}, median={inter_purchase_days.median():.0f}, "
                       f"max={inter_purchase_days.max():.0f}")
    
    # ========================================================================
    # STATISTICAL COMPARISONS BETWEEN GROUPS
    # ========================================================================
    logger.info("\n" + "="*80)
    logger.info("STATISTICAL TESTS: Group Comparisons")
    logger.info("="*80)
    
    # Purchases per member comparison
    purchases_g0 = group_no_push[group_no_push['data_source'] == 1].groupby('member_id').size()
    purchases_g1 = group_with_push[group_with_push['data_source'] == 1].groupby('member_id').size()
    perform_ttest(purchases_g0, purchases_g1, "Purchases per member")
    
    # Dormant episodes comparison
    dormant_g0 = group_no_push.groupby('member_id')['dormant_period'].max()
    dormant_g1 = group_with_push.groupby('member_id')['dormant_period'].max()
    perform_ttest(dormant_g0, dormant_g1, "Dormant episodes per member")
    
    # Average order value comparison
    avg_order_g0 = group_no_push[group_no_push['data_source'] == 1].groupby('member_id')['origin_money'].mean()
    avg_order_g1 = group_with_push[group_with_push['data_source'] == 1].groupby('member_id')['origin_money'].mean()
    perform_ttest(avg_order_g0, avg_order_g1, "Average order value per member")
    
    # Average basket size comparison
    avg_basket_g0 = group_no_push[group_no_push['data_source'] == 1].groupby('member_id')['total_items'].mean()
    avg_basket_g1 = group_with_push[group_with_push['data_source'] == 1].groupby('member_id')['total_items'].mean()
    perform_ttest(avg_basket_g0, avg_basket_g1, "Average basket size per member")
    
    # Inter-purchase days comparison (active periods)
    active_g0 = group_no_push[(group_no_push['data_source'] == 1) & (group_no_push['dormant_period'] == 0)].copy()
    active_g0 = active_g0.sort_values(['member_id', 'dt'])
    active_g0['days_to_next'] = active_g0.groupby('member_id')['dt'].diff().dt.days
    
    active_g1 = group_with_push[(group_with_push['data_source'] == 1) & (group_with_push['dormant_period'] == 0)].copy()
    active_g1 = active_g1.sort_values(['member_id', 'dt'])
    active_g1['days_to_next'] = active_g1.groupby('member_id')['dt'].diff().dt.days
    
    perform_ttest(active_g0['days_to_next'].dropna(), active_g1['days_to_next'].dropna(), 
                 "Inter-purchase days (active periods)")
    
    return group_no_push, group_with_push


def calculate_pushes_before_order(group_data):
    """
    Calculate pushes-before-order at the (member_id, dormant_period) level.
    For each dormant period, take the first purchase and count pushes in that
    period before that purchase.
    """
    
    group_data = group_data.sort_values(['member_id', 'dormant_period', 'dt']).reset_index(drop=True)
    
    group_data['is_purchase'] = (group_data['data_source'] == 1).astype(int)
    group_data['is_push'] = (group_data['data_source'] == 0).astype(int)
    
    # Count pushes within each dormant period
    group_data['pushes_before'] = group_data.groupby(['member_id', 'dormant_period'])['is_push'].cumsum()
    
    purchase_rows = group_data[group_data['is_purchase'] == 1].copy()
    
    # One purchase per dormant period (take the earliest)
    purchase_rows_in_dormant = purchase_rows[purchase_rows['dormant_period'] > 0]
    purchase_rows_not_in_dormant = purchase_rows[purchase_rows['dormant_period'] == 0]
    
    stats = {
        'mean_pushes_before_order': purchase_rows['pushes_before'].mean(),
        'median_pushes_before_order': purchase_rows['pushes_before'].median(),
        'std_pushes_before_order': purchase_rows['pushes_before'].std(),
        'min_pushes_before_order': purchase_rows['pushes_before'].min(),
        'max_pushes_before_order': purchase_rows['pushes_before'].max(),
        'total_purchases': len(purchase_rows),
        'purchases_with_pushes_before': len(purchase_rows_in_dormant)/len(purchase_rows),
        'purchases_without_pushes_before': len(purchase_rows_not_in_dormant)/len(purchase_rows)
    }

    logger.info(f"Stats: {stats}")
    
    return stats


def calculate_time_to_order(group_data):
    """
    Calculate time in dormant per dormant period.
    Only dormant_period > 0 is considered.
    """
    logger.info("Calculating time in dormant (consumer-dormant-period level)...")
    group_data = group_data[group_data['dormant_period'] > 0].copy()

    # Count time in dormant within each dormant period
    # Use transform to broadcast the max value back to each row
    group_data['cumulative_time_in_dormant'] = group_data.groupby(['member_id', 'dormant_period'])['days_since_purchase'].transform('max')
    
    purchase_rows = group_data[group_data['data_source'] == 1].copy()
    
    
    stats = {
        'mean_time_in_dormant': purchase_rows['cumulative_time_in_dormant'].mean(),
        'median_time_in_dormant': purchase_rows['cumulative_time_in_dormant'].median(),
        'std_time_in_dormant': purchase_rows['cumulative_time_in_dormant'].std(),
        'min_time_in_dormant': purchase_rows['cumulative_time_in_dormant'].min(),
        'max_time_in_dormant': purchase_rows['cumulative_time_in_dormant'].max(),
    }

    logger.info(f"Stats: {stats}")
    
    return stats


def analyze_coupon_discount_usage(group_data):
    """
    Analyze coupon/discount usage per dormant period.
    In each member_id-dormant_period, find:
    - the push with the largest days_since_purchase
    - the purchase (only one)
    Then calculate:
    1. the days_diff between the push and the purchase
    2. match rate: if pushed discount and used discount diff < 0.1, 
       or if there's a pushed coupon and purchase used a coupon
    """
    logger.info("Analyzing coupon/discount usage at dormant-period level...")

    # Filter to dormant periods only
    group_data = group_data[group_data['dormant_period'] > 0].copy()
    
    # Separate pushes and purchases
    push_data = group_data[group_data['data_source'] == 0].copy()
    purchase_data = group_data[group_data['data_source'] == 1].copy()
    
    # For each (member_id, dormant_period), find:
    # 1. Push with largest days_since_purchase
    push_max_days = push_data.groupby(['member_id', 'dormant_period']).agg({
        'days_since_purchase': 'max',
        'dt': 'last',  # If multiple pushes have same max days, take the last one
        'coupon': 'last',
        'discount': 'last',
    }).reset_index()
    push_max_days.columns = ['member_id', 'dormant_period', 'push_days_since_purchase', 'push_dt', 'push_coupon', 'push_discount']
    
    # 2. Purchase (should be only one per dormant period)
    purchase_summary = purchase_data.groupby(['member_id', 'dormant_period']).agg({
        'dt': 'first',
        'days_since_purchase': 'first',
        'use_coupon_num': 'first',
        'use_discount': 'first'  # This should exist from push_buy.py
    }).reset_index()
    purchase_summary.columns = ['member_id', 'dormant_period', 'purchase_dt', 'purchase_days_since_purchase', 'use_coupon_num', 'use_discount']
    
    # Merge push and purchase at the period level
    period_merged = pd.merge(
        purchase_summary,
        push_max_days,
        on=['member_id', 'dormant_period'],
        how='inner'  # Only keep periods with both push and purchase
    )
    
    # Calculate days_diff between push and purchase
    period_merged['days_diff'] = (period_merged['purchase_dt'] - period_merged['push_dt']).dt.days
    
    # Calculate match:
    # 1. Discount match: if push_discount exists and use_discount exists, check if abs(diff) < 0.1
    # 2. Coupon match: if push_coupon exists and use_coupon_num > 0
    period_merged['discount_match'] = (
        period_merged['push_discount'].notna() &
        period_merged['use_discount'].notna() &
        (np.abs(period_merged['push_discount']/10 - period_merged['use_discount']) < 0.05)
    ).astype(int)
    
    period_merged['coupon_match'] = (
        period_merged['push_coupon'].notna() &
        (period_merged['use_coupon_num'] > 0)
    ).astype(int)
    
    # Overall match: discount match OR coupon match
    period_merged['match'] = ((period_merged['discount_match'] == 1) | (period_merged['coupon_match'] == 1)).astype(int)
    
    # Calculate statistics
    stats = {
        'total_periods': len(period_merged),
        'periods_with_push_and_purchase': len(period_merged),
        'match_rate': period_merged['match'].mean(),
        'mean_days_diff': period_merged['days_diff'].mean(),
        'median_days_diff': period_merged['days_diff'].median(),
        'discount_match_rate': period_merged['discount_match'].mean(),
        'coupon_match_rate': period_merged['coupon_match'].mean(),
    }
    
    logger.info(f"Stats: {stats}")
    
    # ========================================================================
    # STRATEGIC DISCOUNT BEHAVIOR ANALYSIS (for mismatch cases)
    # ========================================================================
    discount_mismatch = period_merged[
        (period_merged['discount_match'] == 0) &
        period_merged['push_discount'].notna() &
        period_merged['use_discount'].notna()
    ].copy()
    
    if len(discount_mismatch) > 0:
        logger.info(f"\n  Discount Mismatch Analysis ({len(discount_mismatch)} cases):")
        
        # Calculate discount difference (use_discount - push_discount/10)
        # Negative = customer got deeper discount (better deal)
        # Positive = customer got weaker discount
        discount_mismatch['discount_diff'] = discount_mismatch['use_discount'] - discount_mismatch['push_discount'] / 10
        
        logger.info(f"    Mean pushed discount: {(discount_mismatch['push_discount'] / 10).mean():.4f}")
        logger.info(f"    Mean used discount: {discount_mismatch['use_discount'].mean():.4f}")
        logger.info(f"    Mean difference (used - pushed): {discount_mismatch['discount_diff'].mean():.4f}")
        logger.info(f"    Pushed discounts: {discount_mismatch['push_discount'].unique()}")
        logger.info(f"    Used discount: {discount_mismatch['use_discount'].unique()}")
        
        
        # Distribution of discount differences
        deeper_discount = (discount_mismatch['discount_diff'] < 0).sum()
        weaker_discount = (discount_mismatch['discount_diff'] > 0).sum()
        same_discount = (discount_mismatch['discount_diff'] == 0).sum()
        
        logger.info(f"    Cases with DEEPER discount than pushed: {deeper_discount} ({deeper_discount/len(discount_mismatch)*100:.2f}%)")
        logger.info(f"    Cases with WEAKER discount than pushed: {weaker_discount} ({weaker_discount/len(discount_mismatch)*100:.2f}%)")
        logger.info(f"    Cases with SAME discount (edge cases): {same_discount} ({same_discount/len(discount_mismatch)*100:.2f}%)")
        
        # Percentiles of discount difference
        percentiles = [10, 25, 50, 75, 90]
        discount_diff_pct = np.percentile(discount_mismatch['discount_diff'], percentiles)
        logger.info(f"    Discount difference percentiles:")
        for pct, val in zip(percentiles, discount_diff_pct):
            logger.info(f"      {pct}th: {val:.4f}")
        
        stats['discount_mismatch_count'] = len(discount_mismatch)
        stats['mean_pushed_discount'] = (discount_mismatch['push_discount'] / 10).mean()
        stats['mean_used_discount'] = discount_mismatch['use_discount'].mean()
        stats['pct_deeper_discount'] = deeper_discount / len(discount_mismatch)
        stats['pct_weaker_discount'] = weaker_discount / len(discount_mismatch)
    else:
        logger.info("\n  No discount mismatch cases found.")

    return stats


def analyze_trigger_effectiveness(group_data, trigger_tag_value=None):
    """
    Analyze push effectiveness for specific trigger type(s).
    For each push, find if there's a next purchase in the same dormant period.
    Vectorized implementation for efficiency.
    
    Args:
        group_data: DataFrame with combined push/purchase data
        trigger_tag_value: Specific trigger tag to analyze (None = all)
    """
    if trigger_tag_value is not None:
        analysis_name = f"trigger_tag={trigger_tag_value}"
    else:
        analysis_name = "all triggers"
    
    logger.info(f"Analyzing {analysis_name} effectiveness...")
    
    # Filter to dormant periods only
    df = group_data[group_data['dormant_period'] > 0].copy()
    df = df.sort_values(['member_id', 'dormant_period', 'dt']).reset_index(drop=True)
    
    # Filter to specific trigger type if requested
    if trigger_tag_value is not None:
        push_mask = (df['data_source'] == 0) & (df['trigger_tag'] == trigger_tag_value)
    else:
        push_mask = df['data_source'] == 0
    
    pushes = df[push_mask].copy()
    
    if len(pushes) == 0:
        logger.info(f"  No pushes found for {analysis_name}")
        return {'total_pushes': 0, 'response_rate': 0, 'mean_days_to_purchase': np.nan}
    
    # For each push, find the next event in the same dormant period
    pushes['next_member_id'] = df.loc[pushes.index, 'member_id'].shift(-1).values
    pushes['next_dormant_period'] = df.loc[pushes.index, 'dormant_period'].shift(-1).values
    pushes['next_data_source'] = df.loc[pushes.index, 'data_source'].shift(-1).values
    pushes['next_dt'] = df.loc[pushes.index, 'dt'].shift(-1).values
    
    # Check if next event is a purchase in the same (member, dormant_period)
    pushes['has_response'] = (
        (pushes['member_id'] == pushes['next_member_id']) &
        (pushes['dormant_period'] == pushes['next_dormant_period']) &
        (pushes['next_data_source'] == 1)
    )
    
    # Calculate days to response for those with responses
    pushes['days_to_response'] = (pushes['next_dt'] - pushes['dt']).dt.days
    pushes.loc[~pushes['has_response'], 'days_to_response'] = np.nan
    
    # Calculate statistics
    total_pushes = len(pushes)
    total_responses = pushes['has_response'].sum()
    response_rate = total_responses / total_pushes if total_pushes > 0 else 0
    
    responses_only = pushes[pushes['has_response']]
    mean_days = responses_only['days_to_response'].mean() if len(responses_only) > 0 else np.nan
    median_days = responses_only['days_to_response'].median() if len(responses_only) > 0 else np.nan
    
    stats = {
        'total_pushes': total_pushes,
        'total_responses': int(total_responses),
        'response_rate': response_rate,
        'mean_days_to_purchase': mean_days,
        'median_days_to_purchase': median_days,
        'days_to_purchase_data': responses_only['days_to_response'].values if len(responses_only) > 0 else np.array([])
    }
    
    logger.info(f"  Total {analysis_name} pushes: {total_pushes}")
    logger.info(f"  Pushes with response: {total_responses} ({response_rate*100:.2f}%)")
    if len(responses_only) > 0:
        logger.info(f"  Days to purchase (for responders): mean={mean_days:.2f}, median={median_days:.2f}")
    
    return stats


def analyze_wakeup_effectiveness(group_data):
    """
    Analyze dormant period outcomes: wake-up rate, time to wake-up, push intensity.
    Vectorized implementation.
    """
    logger.info("Analyzing wake-up effectiveness...")
    
    # Filter to dormant periods only
    df = group_data[group_data['dormant_period'] > 0].copy()
    
    # Aggregate at (member_id, dormant_period) level
    period_stats = df.groupby(['member_id', 'dormant_period']).agg({
        'data_source': lambda x: (x == 1).any(),  # Has purchase
        'days_since_purchase': 'max',  # Max days in dormant
        'dt': 'count'  # Total events
    }).reset_index()
    period_stats.columns = ['member_id', 'dormant_period', 'has_wakeup', 'max_days_in_dormant', 'total_events']
    
    # Count pushes per period
    pushes_per_period = df[df['data_source'] == 0].groupby(['member_id', 'dormant_period']).size().reset_index(name='push_count')
    period_stats = period_stats.merge(pushes_per_period, on=['member_id', 'dormant_period'], how='left')
    period_stats['push_count'] = period_stats['push_count'].fillna(0)
    
    # Statistics
    total_periods = len(period_stats)
    wakeup_count = period_stats['has_wakeup'].sum()
    wakeup_rate = wakeup_count / total_periods if total_periods > 0 else 0
    
    wakeup_periods = period_stats[period_stats['has_wakeup']]
    mean_days_to_wakeup = wakeup_periods['max_days_in_dormant'].mean() if len(wakeup_periods) > 0 else np.nan
    mean_pushes_per_period = period_stats['push_count'].mean()
    
    stats = {
        'total_dormant_periods': total_periods,
        'periods_with_wakeup': int(wakeup_count),
        'wakeup_rate': wakeup_rate,
        'mean_days_to_wakeup': mean_days_to_wakeup,
        'mean_pushes_per_period': mean_pushes_per_period,
        'wakeup_flag_data': period_stats['has_wakeup'].astype(int).values,
        'days_to_wakeup_data': wakeup_periods['max_days_in_dormant'].values if len(wakeup_periods) > 0 else np.array([]),
        'pushes_per_period_data': period_stats['push_count'].values
    }
    
    logger.info(f"  Total dormant periods: {total_periods}")
    logger.info(f"  Periods ending with purchase (wake-up): {wakeup_count} ({wakeup_rate*100:.2f}%)")
    logger.info(f"  Mean days to wake-up: {mean_days_to_wakeup:.2f}")
    logger.info(f"  Mean pushes per dormant period: {mean_pushes_per_period:.2f}")
    
    return stats


def analyze_purchase_activity(group_data):
    """
    Analyze purchase patterns during active periods (not dormant).
    Includes basket size, purchase frequency, coupon/discount usage.
    Vectorized implementation.
    """
    logger.info("Analyzing purchase activity during active periods...")
    
    # Filter to purchases in active periods (dormant_period == 0)
    purchases = group_data[
        (group_data['data_source'] == 1) & 
        (group_data['dormant_period'] == 0)
    ].copy()
    
    if len(purchases) == 0:
        logger.info("  No active period purchases found.")
        return {}
    
    # Per-purchase metrics
    mean_basket_value = purchases['origin_money'].mean()
    mean_basket_size = purchases['total_items'].mean()
    mean_top_items = purchases['total_top_items'].mean()
    
    # Coupon/discount usage rates
    coupon_usage_rate = (purchases['use_coupon_num'] > 0).mean()
    discount_usage_rate = (purchases['use_discount'] > 0).mean()
    
    # Inter-purchase intervals
    purchases_sorted = purchases.sort_values(['member_id', 'dt'])
    purchases_sorted['days_since_last'] = purchases_sorted.groupby('member_id')['dt'].diff().dt.days
    inter_purchase_days = purchases_sorted['days_since_last'].dropna()
    mean_inter_purchase = inter_purchase_days.mean() if len(inter_purchase_days) > 0 else np.nan
    
    stats = {
        'total_active_purchases': len(purchases),
        'mean_basket_value': mean_basket_value,
        'mean_basket_size': mean_basket_size,
        'mean_top_items': mean_top_items,
        'coupon_usage_rate': coupon_usage_rate,
        'discount_usage_rate': discount_usage_rate,
        'mean_inter_purchase_days': mean_inter_purchase,
        'basket_value_data': purchases['origin_money'].values,
        'basket_size_data': purchases['total_items'].values,
        'inter_purchase_days_data': inter_purchase_days.values
    }
    
    logger.info(f"  Total active purchases: {len(purchases)}")
    logger.info(f"  Mean basket value: {mean_basket_value:.2f}")
    logger.info(f"  Mean basket size: {mean_basket_size:.2f}")
    logger.info(f"  Coupon usage rate: {coupon_usage_rate*100:.2f}%")
    logger.info(f"  Discount usage rate: {discount_usage_rate*100:.2f}%")
    logger.info(f"  Mean inter-purchase days: {mean_inter_purchase:.2f}")
    
    return stats


def compare_groups(group_no_push, group_with_push):
    """
    Compare responsiveness metrics between the two groups with statistical tests.
    """
    logger.info("=" * 80)
    logger.info("BEHAVIORAL COMPARISON: push=0 vs push=1")
    logger.info("=" * 80)
    
    # ========================================================================
    # 1. WAKE-UP EFFECTIVENESS ANALYSIS
    # ========================================================================
    logger.info("\n--- Analysis 1: Wake-up Effectiveness ---")
    logger.info("Group push=0:")
    wakeup_g0 = analyze_wakeup_effectiveness(group_no_push)
    logger.info("\nGroup push=1:")
    wakeup_g1 = analyze_wakeup_effectiveness(group_with_push)
    
    # Statistical tests
    logger.info("\nStatistical Tests:")
    perform_chi_square(
        wakeup_g0['periods_with_wakeup'], wakeup_g0['total_dormant_periods'],
        wakeup_g1['periods_with_wakeup'], wakeup_g1['total_dormant_periods'],
        "Wake-up rate (% dormant periods ending with purchase)"
    )
    if len(wakeup_g0['days_to_wakeup_data']) > 0 and len(wakeup_g1['days_to_wakeup_data']) > 0:
        perform_ttest(
            pd.Series(wakeup_g0['days_to_wakeup_data']),
            pd.Series(wakeup_g1['days_to_wakeup_data']),
            "Days to wake-up (for successful wake-ups)"
        )
    perform_ttest(
        pd.Series(wakeup_g0['pushes_per_period_data']),
        pd.Series(wakeup_g1['pushes_per_period_data']),
        "Pushes per dormant period"
    )
    
    # ========================================================================
    # 2. PURCHASE ACTIVITY DURING ACTIVE PERIODS
    # ========================================================================
    logger.info("\n" + "="*80)
    logger.info("--- Analysis 2: Purchase Activity (Active Periods) ---")
    logger.info("Group push=0:")
    activity_g0 = analyze_purchase_activity(group_no_push)
    logger.info("\nGroup push=1:")
    activity_g1 = analyze_purchase_activity(group_with_push)
    
    if activity_g0 and activity_g1:
        logger.info("\nStatistical Tests:")
        perform_ttest(
            pd.Series(activity_g0['basket_value_data']),
            pd.Series(activity_g1['basket_value_data']),
            "Basket value (origin_money)"
        )
        perform_ttest(
            pd.Series(activity_g0['basket_size_data']),
            pd.Series(activity_g1['basket_size_data']),
            "Basket size (total_items)"
        )
        perform_ttest(
            pd.Series(activity_g0['inter_purchase_days_data']),
            pd.Series(activity_g1['inter_purchase_days_data']),
            "Inter-purchase days"
        )
        perform_chi_square(
            int(activity_g0['coupon_usage_rate'] * activity_g0['total_active_purchases']),
            activity_g0['total_active_purchases'],
            int(activity_g1['coupon_usage_rate'] * activity_g1['total_active_purchases']),
            activity_g1['total_active_purchases'],
            "Coupon usage rate"
        )
        perform_chi_square(
            int(activity_g0['discount_usage_rate'] * activity_g0['total_active_purchases']),
            activity_g0['total_active_purchases'],
            int(activity_g1['discount_usage_rate'] * activity_g1['total_active_purchases']),
            activity_g1['total_active_purchases'],
            "Discount usage rate"
        )
    
    # ========================================================================
    # 3. COUPON/DISCOUNT STRATEGIC BEHAVIOR
    # ========================================================================
    logger.info("\n" + "="*80)
    logger.info("--- Analysis 3: Coupon/Discount Usage & Strategic Behavior ---")
    logger.info("Group push=0:")
    coupon_g0 = analyze_coupon_discount_usage(group_no_push)
    logger.info("\nGroup push=1:")
    coupon_g1 = analyze_coupon_discount_usage(group_with_push)
    
    # Statistical tests
    logger.info("\nStatistical Tests:")
    perform_chi_square(
        int(coupon_g0['match_rate'] * coupon_g0['total_periods']),
        coupon_g0['total_periods'],
        int(coupon_g1['match_rate'] * coupon_g1['total_periods']),
        coupon_g1['total_periods'],
        "Overall match rate (coupon or discount)"
    )
    
    if 'pct_deeper_discount' in coupon_g0 and 'pct_deeper_discount' in coupon_g1:
        perform_chi_square(
            int(coupon_g0['pct_deeper_discount'] * coupon_g0['discount_mismatch_count']),
            coupon_g0['discount_mismatch_count'],
            int(coupon_g1['pct_deeper_discount'] * coupon_g1['discount_mismatch_count']),
            coupon_g1['discount_mismatch_count'],
            "Strategic behavior: % using deeper discount than pushed"
        )
    
    # ========================================================================
    # 4. TRIGGER-SPECIFIC EFFECTIVENESS (All Trigger Types)
    # ========================================================================
    logger.info("\n" + "="*80)
    logger.info("--- Analysis 4: Trigger-Specific Effectiveness ---")
    
    # Analyze each trigger type
    trigger_types = [1, 2, 3, 4, 5]
    trigger_names = {
        1: "issue_coupon/discount",
        2: "expiration_reminder",
        3: "new_product_notification",
        4: "special_zone_reminder",
        5: "other"
    }
    
    for trigger_type in trigger_types:
        logger.info(f"\n  Trigger Type {trigger_type}: {trigger_names[trigger_type]}")
        logger.info("  Group push=0:")
        trigger_g0 = analyze_trigger_effectiveness(group_no_push, trigger_type)
        logger.info("  Group push=1:")
        trigger_g1 = analyze_trigger_effectiveness(group_with_push, trigger_type)
        
        if trigger_g0['total_pushes'] and trigger_g1['total_pushes']:
            # Statistical tests
            if trigger_g0['total_pushes'] > 0 and trigger_g1['total_pushes'] > 0:
                logger.info("  Statistical Tests:")
                perform_chi_square(
                    trigger_g0['total_responses'], trigger_g0['total_pushes'],
                    trigger_g1['total_responses'], trigger_g1['total_pushes'],
                    f"Response rate for trigger {trigger_type}"
                )
                
                if len(trigger_g0['days_to_purchase_data']) > 0 and len(trigger_g1['days_to_purchase_data']) > 0:
                    perform_ttest(
                        pd.Series(trigger_g0['days_to_purchase_data']),
                        pd.Series(trigger_g1['days_to_purchase_data']),
                        f"Days to purchase for trigger {trigger_type} (responders only)"
                    )
    
    # ========================================================================
    # 5. LEGACY METRICS (for continuity)
    # ========================================================================
    logger.info("\n" + "="*80)
    logger.info("--- Legacy Metrics ---")
    logger.info("\nPushes before order:")
    logger.info("Group push=0:")
    calculate_pushes_before_order(group_no_push)
    logger.info("\nGroup push=1:")
    calculate_pushes_before_order(group_with_push)
    
    logger.info("\nTime in dormant:")
    logger.info("Group push=0:")
    calculate_time_to_order(group_no_push)
    logger.info("\nGroup push=1:")
    calculate_time_to_order(group_with_push)

def main():
    """Main function to run the analysis"""
    logger.info("Starting customer push responsiveness comparison analysis...")
    
    # Load data
    group_no_push, group_with_push = load_data()
    # Compare groups
    compare_groups(group_no_push, group_with_push)
    
    logger.info("Analysis complete!")


if __name__ == "__main__":
    main()




