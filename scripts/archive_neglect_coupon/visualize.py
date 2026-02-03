import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

def visualize_dept_daily_demand(dept_daily_demand_complete, output_folder='plots'):
    """
    Visualize the daily demand for each store.
    
    Parameters:
    -----------
    dept_daily_demand_complete : pd.DataFrame
        DataFrame with columns: dept_id, dt, daily_demand
    output_folder : str
        Folder path to save the plots (default: 'plots')
    """
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Ensure dt is datetime
    if not pd.api.types.is_datetime64_any_dtype(dept_daily_demand_complete['dt']):
        dept_daily_demand_complete['dt'] = pd.to_datetime(dept_daily_demand_complete['dt'])
    
    # Sort by date for proper plotting
    dept_daily_demand_complete = dept_daily_demand_complete.sort_values(['dept_id', 'dt'])
    
    # Get unique stores
    unique_depts = sorted(dept_daily_demand_complete['dept_id'].unique())
    num_depts = len(unique_depts)
    
    print(f"\nVisualizing daily demand for {num_depts} stores...")
    
    # Create a comprehensive plot with all stores
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Use a colormap for different stores
    colors = plt.cm.tab20(np.linspace(0, 1, min(20, num_depts)))
    if num_depts > 20:
        # If more than 20 stores, cycle through colors
        colors = plt.cm.tab20(np.linspace(0, 1, 20))
        color_cycle = np.tile(colors, (num_depts // 20 + 1, 1))[:num_depts]
    else:
        color_cycle = colors
    
    # Plot each store
    for i, dept_id in enumerate(unique_depts):
        dept_data = dept_daily_demand_complete[dept_daily_demand_complete['dept_id'] == dept_id]
        ax.plot(dept_data['dt'], dept_data['daily_demand'], 
                alpha=0.7, linewidth=1.5, color=color_cycle[i % len(color_cycle)])
    
    ax.set_xlabel('Date', fontsize=14)
    ax.set_ylabel('Daily Demand', fontsize=14)
    ax.set_title('Daily Demand by store Over Time', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3)
    #ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8, ncol=2)
    
    plt.tight_layout()
    output_path = os.path.join(output_folder, 'dept_daily_demand_all.pdf')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved comprehensive plot to: {output_path}")
    plt.close()
    
    # Create a summary statistics plot
    dept_summary = dept_daily_demand_complete.groupby('dept_id')['daily_demand'].agg([
        'mean', 'std', 'max', 'min'
    ]).reset_index()
    dept_summary = dept_summary.sort_values('mean', ascending=False)
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    # Mean daily demand
    axes[0, 0].bar(range(len(dept_summary)), dept_summary['mean'], color='steelblue', alpha=0.7)
    axes[0, 0].set_xlabel('store (sorted by mean)', fontsize=12)
    axes[0, 0].set_ylabel('Mean Daily Demand', fontsize=12)
    axes[0, 0].set_title('Mean Daily Demand by store', fontsize=14, fontweight='bold')
    axes[0, 0].grid(True, alpha=0.3, axis='y')
    
    # Max daily demand
    axes[0, 1].bar(range(len(dept_summary)), dept_summary['max'], color='coral', alpha=0.7)
    axes[0, 1].set_xlabel('store (sorted by mean)', fontsize=12)
    axes[0, 1].set_ylabel('Max Daily Demand', fontsize=12)
    axes[0, 1].set_title('Max Daily Demand by store', fontsize=14, fontweight='bold')
    axes[0, 1].grid(True, alpha=0.3, axis='y')
    
    # Standard deviation
    axes[1, 0].bar(range(len(dept_summary)), dept_summary['std'], color='mediumseagreen', alpha=0.7)
    axes[1, 0].set_xlabel('store (sorted by mean)', fontsize=12)
    axes[1, 0].set_ylabel('Std Dev of Daily Demand', fontsize=12)
    axes[1, 0].set_title('Standard Deviation of Daily Demand by store', fontsize=14, fontweight='bold')
    axes[1, 0].grid(True, alpha=0.3, axis='y')
    
    # Distribution of mean daily demand
    axes[1, 1].hist(dept_summary['mean'], bins=30, color='purple', alpha=0.7, edgecolor='black')
    axes[1, 1].set_xlabel('Mean Daily Demand', fontsize=12)
    axes[1, 1].set_ylabel('Number of stores', fontsize=12)
    axes[1, 1].set_title('Distribution of Mean Daily Demand', fontsize=14, fontweight='bold')
    axes[1, 1].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    output_path = os.path.join(output_folder, 'dept_demand_summary_statistics.pdf')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved summary statistics plot to: {output_path}")
    plt.close()
    
    print(f"\nAll plots saved to folder: {output_folder}")

def visualize_product_dept_daily_demand(product_id, product_name, first_day, last_day, 
                                        product_dept_daily, all_dept_ids, rank, 
                                        output_folder='plots'):
    """
    Visualize daily demand by store for a specific product.
    
    Parameters:
    -----------
    product_id : int
        The product ID
    product_name : str
        The product name
    first_day : pd.Timestamp or datetime
        First day the product was on market
    last_day : pd.Timestamp or datetime
        Last day the product was on market
    product_dept_daily : pd.DataFrame
        DataFrame with columns: dt, dept_id, demand
    all_dept_ids : array-like
        List of all store IDs that have this product
    rank : int
        Rank of this product (for filename)
    output_folder : str
        Folder path to save the plot (default: 'plots')
    """
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Ensure dates are datetime
    first_day = pd.to_datetime(first_day)
    last_day = pd.to_datetime(last_day)
    product_dept_daily['dt'] = pd.to_datetime(product_dept_daily['dt'])
    
    # Create complete date range from first_day to last_day
    date_range = pd.date_range(start=first_day, end=last_day, freq='D')
    
    # Create plot
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Plot each dept as a separate line
    colors = plt.cm.tab20(np.linspace(0, 1, min(20, len(all_dept_ids))))
    if len(all_dept_ids) > 20:
        colors = plt.cm.tab20(np.linspace(0, 1, 20))
        color_cycle = np.tile(colors, (len(all_dept_ids) // 20 + 1, 1))[:len(all_dept_ids)]
    else:
        color_cycle = colors
    
    for i, dept_id in enumerate(sorted(all_dept_ids)):
        dept_data = product_dept_daily[product_dept_daily['dept_id'] == dept_id].copy()
        
        # Create complete date series for this dept
        dept_complete = pd.DataFrame({'dt': date_range})
        dept_complete = dept_complete.merge(dept_data[['dt', 'demand']], on='dt', how='left')
        dept_complete['demand'] = dept_complete['demand'].fillna(0)
        
        ax.plot(dept_complete['dt'], dept_complete['demand'], #label=f'Dept {dept_id}',
               alpha=0.7, linewidth=1.5, color=color_cycle[i % len(color_cycle)])
    
    ax.set_xlabel('Date', fontsize=14)
    ax.set_ylabel('Daily Demand', fontsize=14)
    ax.set_title(f'Daily Demand by store - {product_name} (Product ID: {product_id})', 
                fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Adjust legend if too many depts
    #if len(all_dept_ids) <= 15:
    #    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8, ncol=1)
    #else:
    #    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=6, ncol=2)
    
    plt.tight_layout()
    
    # Save plot
    safe_name = product_name.replace('/', '_').replace('\\', '_').replace(':', '_')
    output_path = os.path.join(output_folder, f'top5_product_{rank}_{product_id}_{safe_name}.pdf')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return output_path

def visualize_product_first_last_appearance(
    df,
    product_id,
    first_appearance,
    last_appearance,
    output_folder='plots',
    dept_static_path='data1031/dept_result_static.csv',
):
    """
    Visualize the first and last day a product appeared in each store.
    
    Parameters:
    -----------
    product_id : int
        The product ID
    first_appearance : pd.DataFrame
        DataFrame with columns: dept_id, first_day
    last_appearance : pd.DataFrame
        DataFrame with columns: dept_id, last_day
    output_folder : str
        Folder path to save the plots (default: 'plots')
    """
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Ensure dates are datetime
    first_appearance['first_day'] = pd.to_datetime(first_appearance['first_day'])
    last_appearance['last_day'] = pd.to_datetime(last_appearance['last_day'])
    
    # Sort by date for better visualization
    first_appearance = first_appearance.sort_values('first_day')
    last_appearance = last_appearance.sort_values('last_day')
    
    # Read store setup/shutdown info
    try:
        dept_static = pd.read_csv(
            dept_static_path,
            encoding='utf-8-sig',
            usecols=['dept_id', 'set_up_time', 'shut_up_time'],
        )
        # coerce to datetime
        dept_static['set_up_time'] = pd.to_datetime(dept_static['set_up_time'], errors='coerce')
        dept_static['shut_up_time'] = pd.to_datetime(dept_static['shut_up_time'], errors='coerce')
    except Exception as e:
        print(f"Warning: failed to read {dept_static_path}: {e}")
        dept_static = pd.DataFrame(columns=['dept_id', 'set_up_time', 'shut_up_time'])
    
    df = df[['dept_id', 'dt']].drop_duplicates(subset=['dept_id'])
    df['first_record_day'] = df.groupby('dept_id')['dt'].transform('min')
    df['last_record_day'] = df.groupby('dept_id')['dt'].transform('max')
    
    # Merge to know if first/last equals set_up/shut_up
    first_appearance = first_appearance.merge(dept_static, on='dept_id', how='left')
    first_appearance = first_appearance.merge(df, on='dept_id', how='left')
    first_appearance['is_first_record_day'] = (first_appearance['first_day'] == first_appearance['first_record_day']) | (first_appearance['first_day'] == first_appearance['set_up_time'])


    last_appearance = last_appearance.merge(dept_static, on='dept_id', how='left')
    last_appearance = last_appearance.merge(df, on='dept_id', how='left')
    last_appearance['is_last_record_day'] = (last_appearance['last_day'] == last_appearance['last_record_day']) | (last_appearance['last_day'] == last_appearance['shut_up_time'])

    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))
    
    # Plot 1: First appearance dates
    ax1.scatter(
        first_appearance['first_day'],
        range(len(first_appearance)),
        alpha=0.6,
        s=50,
        color='steelblue',
        label='First appearance',
    )
    # Highlight points where first_day == set_up_time
    setup_mask = first_appearance['is_first_record_day'].fillna(False)
    if setup_mask.any():
        ax1.scatter(
            first_appearance.loc[setup_mask, 'first_day'],
            first_appearance.index[setup_mask],
            color='orange',
            s=10,
            marker='D',
            label='First day == store setup',
            alpha=0.6,
        )
    ax1.set_xlabel('Date', fontsize=14)
    ax1.set_ylabel('store Index (sorted by first appearance)', fontsize=14)
    ax1.set_title(f'First Appearance Date by store - Product ID: {product_id}', 
                 fontsize=16, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Add vertical lines for min and max dates
    min_first = first_appearance['first_day'].min()
    max_first = first_appearance['first_day'].max()
    ax1.axvline(min_first, color='green', linestyle='--', alpha=0.7, label=f'Earliest: {min_first.date()}')
    ax1.axvline(max_first, color='red', linestyle='--', alpha=0.7, label=f'Latest: {max_first.date()}')
    ax1.legend()
    
    # Plot 2: Last appearance dates
    ax2.scatter(
        last_appearance['last_day'],
        range(len(last_appearance)),
        alpha=0.6,
        s=50,
        color='coral',
        label='Last appearance',
    )
    # Highlight points where last_day == shut_up_time
    shutdown_mask = last_appearance['is_last_record_day'].fillna(False)
    if shutdown_mask.any():
        ax2.scatter(
            last_appearance.loc[shutdown_mask, 'last_day'],
            last_appearance.index[shutdown_mask],
            color='purple',
            s=10,
            marker='D',
            label='Last day == store shutdown',
            alpha=0.6,
        )
    ax2.set_xlabel('Date', fontsize=14)
    ax2.set_ylabel('store Index (sorted by last appearance)', fontsize=14)
    ax2.set_title(f'Last Appearance Date by store - Product ID: {product_id}', 
                 fontsize=16, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # Add vertical lines for min and max dates
    min_last = last_appearance['last_day'].min()
    max_last = last_appearance['last_day'].max()
    ax2.axvline(min_last, color='green', linestyle='--', alpha=0.7, label=f'Earliest: {min_last.date()}')
    ax2.axvline(max_last, color='red', linestyle='--', alpha=0.7, label=f'Latest: {max_last.date()}')
    ax2.legend()
    
    plt.tight_layout()
    
    # Save plot
    output_path = os.path.join(output_folder, f'product_{product_id}_first_last_appearance.pdf')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"   First/Last appearance plot saved to: {output_path}")
    plt.close()
    
    return output_path

def visualize_dept_week_order_daily(dept_week_order, output_folder='plots'):
    """
    Visualize dept_week_order data by converting weekly totals to daily demand.
    Divides each weekly total by 7 to approximate daily demand (each day in a week has the same demand).
    
    Parameters:
    -----------
    dept_week_order : pd.DataFrame
        DataFrame with columns: dept_id, monday_date, coffee_num, drink_not_coffee_num, etc.
    output_folder : str
        Folder path to save the plots (default: 'plots')
    """
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Ensure monday_date is datetime
    dept_week_order = dept_week_order.copy()
    dept_week_order['monday_date'] = pd.to_datetime(dept_week_order['monday_date'])
    
    # Calculate total weekly demand (coffee + drink_not_coffee)
    dept_week_order['weekly_total'] = dept_week_order['coffee_num'] + dept_week_order['drink_not_coffee_num']
    
    # Divide by 7 to get approximate daily demand
    dept_week_order['daily_demand'] = dept_week_order['weekly_total'] / 7
    
    # Expand weekly data to daily data (each day in the week gets the same daily_demand)
    daily_records = []
    
    for _, row in dept_week_order.iterrows():
        dept_id = row['dept_id']
        monday_date = row['monday_date']
        daily_demand = row['daily_demand']
        
        # Create 7 days for this week (Monday to Sunday)
        for day_offset in range(7):
            dt = monday_date + pd.Timedelta(days=day_offset)
            daily_records.append({
                'dept_id': dept_id,
                'dt': dt,
                'daily_demand': daily_demand
            })
    
    # Create daily dataframe
    daily_df = pd.DataFrame(daily_records)
    daily_df = daily_df.sort_values(['dept_id', 'dt'])
    
    # Get unique stores
    unique_stores = sorted(daily_df['dept_id'].unique())
    num_stores = len(unique_stores)
    
    print(f"\nVisualizing daily demand (from weekly data) for {num_stores} stores...")
    
    # Create plot
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Use a colormap for different stores
    colors = plt.cm.tab20(np.linspace(0, 1, min(20, num_stores)))
    if num_stores > 20:
        colors = plt.cm.tab20(np.linspace(0, 1, 20))
        color_cycle = np.tile(colors, (num_stores // 20 + 1, 1))[:num_stores]
    else:
        color_cycle = colors
    
    # Plot each store as a separate line
    for i, store_id in enumerate(unique_stores):
        store_data = daily_df[daily_df['dept_id'] == store_id]
        ax.plot(store_data['dt'], store_data['daily_demand'], 
               label=f'Store {store_id}', alpha=0.7, linewidth=1.5, 
               color=color_cycle[i % len(color_cycle)])
    
    ax.set_xlabel('Date', fontsize=14)
    ax.set_ylabel('Daily Demand (Approximated from Weekly Data)', fontsize=14)
    ax.set_title('Daily Demand by Store (from Weekly Data)', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Only show legend if reasonable number of stores
    if num_stores <= 20:
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8, ncol=1)
    
    plt.tight_layout()
    
    # Save plot
    output_path = os.path.join(output_folder, 'dept_week_order_daily_demand.pdf')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved plot to: {output_path}")
    plt.close()
    
    return output_path

def visualize_demand_ratio_by_period(
    dept_id,
    product_id,
    df,
    intro_start,
    intro_end,
    removal_start,
    removal_end,
    first_day,
    last_day,
    output_folder='plots',):
    """
    Visualize demand ratio across products in a store for two periods:
    - Two weeks before and after product introduction
    - Two weeks before and after product removal
    
    Parameters:
    -----------
    dept_id : int
        Store ID
    product_id : int
        Product ID being analyzed
    df : pd.DataFrame
        Dataframe with columns: product_id, dt, dept_id
    intro_start, intro_end : datetime
        Introduction period boundaries
    removal_start, removal_end : datetime
        Removal period boundaries
    output_folder : str
        Folder to save plots
    """
    os.makedirs(output_folder, exist_ok=True)
    
    # Ensure dt is datetime
    if not pd.api.types.is_datetime64_any_dtype(df['dt']):
        df['dt'] = pd.to_datetime(df['dt'])
    
    # Filter store data
    store_data = df[df['dept_id'] == dept_id].copy()
    
    # Define sub-periods: before/after intro and before/after removal
    intro_before = store_data[(store_data['dt'] >= intro_start) & (store_data['dt'] < first_day)]
    intro_after = store_data[(store_data['dt'] >= first_day) & (store_data['dt'] < intro_end)]
    removal_before = store_data[(store_data['dt'] > removal_start) & (store_data['dt'] <= last_day)]
    removal_after = store_data[(store_data['dt'] > last_day) & (store_data['dt'] <= removal_end)]
    
    def _compute_ratio(df_slice):
        demand = df_slice.groupby('product_id').size().reset_index(name='demand')
        total = demand['demand'].sum()
        if total > 0:
            demand['ratio'] = demand['demand'] / total * 100
        else:
            demand['ratio'] = 0
        # Keep all products with positive ratio
        demand = demand[demand['ratio'] > 0].sort_values('ratio', ascending=False)
        return demand

    intro_before_ratio = _compute_ratio(intro_before)
    intro_after_ratio = _compute_ratio(intro_after)
    removal_before_ratio = _compute_ratio(removal_before)
    removal_after_ratio = _compute_ratio(removal_after)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    plots = [
        (intro_before_ratio, axes[0, 0], 'Introduction - Before'),
        (intro_after_ratio, axes[0, 1], 'Introduction - After'),
        (removal_before_ratio, axes[1, 0], 'Removal - Before'),
        (removal_after_ratio, axes[1, 1], 'Removal - After'),
    ]

    for ratio_df, ax, title in plots:
        if len(ratio_df) == 0:
            ax.set_title(f'{title}\n(No data)', fontsize=14, fontweight='bold')
            ax.axis('off')
            continue
        colors = ['steelblue' if pid == product_id else 'lightblue' for pid in ratio_df['product_id']]
        ax.barh(range(len(ratio_df)), ratio_df['ratio'], color=colors)
        # don't show the yticks
        ax.set_yticks([])
        #ax.set_yticks(range(len(ratio_df)))
        #ax.set_yticklabels([f'Product {pid}' for pid in ratio_df['product_id']], fontsize=9)
        ax.set_xlabel('Demand Ratio (%)', fontsize=11)
        ax.set_title(f'{title}\nStore {dept_id}', fontsize=13, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')

    plt.tight_layout()
    output_path = os.path.join(output_folder, f'store_{dept_id}_product_{product_id}_demand_ratio.pdf')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"   Saved demand ratio plot to: {output_path}")
    plt.close()

    # --- Total daily demand (all products) during the four periods ---
    intro_before_total = intro_before.groupby('dt').size().reset_index(name='total_demand')
    intro_after_total = intro_after.groupby('dt').size().reset_index(name='total_demand')
    removal_before_total = removal_before.groupby('dt').size().reset_index(name='total_demand')
    removal_after_total = removal_after.groupby('dt').size().reset_index(name='total_demand')

    fig2, (ax_top, ax_bottom) = plt.subplots(2, 1, figsize=(12, 8))

    # Intro combined: before + after
    intro_combined = pd.concat([intro_before_total, intro_after_total]).sort_values('dt')
    if len(intro_combined) > 0:
        ax_top.plot(intro_combined['dt'], intro_combined['total_demand'],
                    marker='o', linewidth=2, markersize=5, color='steelblue')
        ax_top.set_title(f'Introduction Period (Before + After)\nStore {dept_id}', fontsize=14, fontweight='bold')
        ax_top.set_ylabel('Total Daily Demand', fontsize=12)
        ax_top.grid(True, alpha=0.3)
        ax_top.tick_params(axis='x', rotation=45)
        ax_top.axvline(first_day, color='green', linestyle='--', alpha=0.7, label='Introduction day')
        if len(ax_top.get_legend_handles_labels()[0]) > 0:
            ax_top.legend()
    else:
        ax_top.set_title('Introduction Period (No data)', fontsize=14, fontweight='bold')
        ax_top.axis('off')

    # Removal combined: before + after
    removal_combined = pd.concat([removal_before_total, removal_after_total]).sort_values('dt')
    if len(removal_combined) > 0:
        ax_bottom.plot(removal_combined['dt'], removal_combined['total_demand'],
                       marker='o', linewidth=2, markersize=5, color='coral')
        ax_bottom.set_title(f'Removal Period (Before + After)\nStore {dept_id}', fontsize=14, fontweight='bold')
        ax_bottom.set_xlabel('Date', fontsize=12)
        ax_bottom.set_ylabel('Total Daily Demand', fontsize=12)
        ax_bottom.grid(True, alpha=0.3)
        ax_bottom.tick_params(axis='x', rotation=45)
        ax_bottom.axvline(last_day, color='red', linestyle='--', alpha=0.7, label='Removal day')
        if len(ax_bottom.get_legend_handles_labels()[0]) > 0:
            ax_bottom.legend()
    else:
        ax_bottom.set_title('Removal Period (No data)', fontsize=14, fontweight='bold')
        ax_bottom.axis('off')

    plt.tight_layout()
    output_path_total = os.path.join(output_folder, f'store_{dept_id}_product_{product_id}_total_daily_demand.pdf')
    plt.savefig(output_path_total, dpi=300, bbox_inches='tight')
    print(f"   Saved total daily demand plot to: {output_path_total}")
    plt.close()
    
    return output_path

def visualize_weekly_demand_by_period(
    dept_id,
    product_id,
    df,
    intro_start,
    intro_end,
    removal_start,
    removal_end,
    output_folder='plots',):
    """
    Visualize total weekly demand in a store for introduction and removal periods.
    
    Parameters:
    -----------
    dept_id : int
        Store ID
    product_id : int
        Product ID being analyzed
    df : pd.DataFrame
        Dataframe with columns: product_id, dt, dept_id
    intro_start, intro_end : datetime
        Introduction period boundaries
    removal_start, removal_end : datetime
        Removal period boundaries
    output_folder : str
        Folder to save plots
    """
    os.makedirs(output_folder, exist_ok=True)
    
    # Read weekly demand data
    dept_week_order = pd.read_csv('data1031/dept_result_week_order.csv', encoding='utf-8-sig')
    dept_week_order['monday_date'] = pd.to_datetime(dept_week_order['monday_date'])
    
    # Filter for this store
    store_weekly = dept_week_order[dept_week_order['dept_id'] == dept_id].copy()
    store_weekly['weekly_total'] = store_weekly['coffee_num'] + store_weekly['drink_not_coffee_num']
    
    # Filter for introduction period (find weeks that overlap)
    intro_weeks = store_weekly[
        (store_weekly['monday_date'] + pd.Timedelta(days=6) >= intro_start) &
        (store_weekly['monday_date'] <= intro_end)
    ]
    
    # Filter for removal period
    removal_weeks = store_weekly[
        (store_weekly['monday_date'] + pd.Timedelta(days=6) >= removal_start) &
        (store_weekly['monday_date'] <= removal_end)
    ]
    
    # Create visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 9))
    
    # Introduction period
    if len(intro_weeks) > 0:
        ax1.bar(intro_weeks['monday_date'], intro_weeks['weekly_total'], 
                color='steelblue', alpha=0.75)
        ax1.set_xlabel('Week Starting Date', fontsize=13)
        ax1.set_ylabel('Weekly Total Demand', fontsize=13)
        ax1.set_title(f'Weekly Total Demand - Introduction Period\nStore {dept_id}', 
                     fontsize=15, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)
    
    # Removal period
    if len(removal_weeks) > 0:
        ax2.bar(removal_weeks['monday_date'], removal_weeks['weekly_total'], 
                color='coral', alpha=0.75)
        ax2.set_xlabel('Week Starting Date', fontsize=13)
        ax2.set_ylabel('Weekly Total Demand', fontsize=13)
        ax2.set_title(f'Weekly Total Demand - Removal Period\nStore {dept_id}', 
                     fontsize=15, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    output_path = os.path.join(output_folder, f'store_{dept_id}_product_{product_id}_weekly_demand.pdf')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"   Saved weekly demand plot to: {output_path}")
    plt.close()
    
    return output_path

def visualize_product_line_changes(dept_id, product_id, product_changes, period_start, 
                                   period_end, output_folder='plots'):
    """
    Visualize product line changes during the analysis period.
    
    Parameters:
    -----------
    dept_id : int
        Store ID
    product_id : int
        Main product ID being analyzed
    product_changes : list
        List of dicts with 'week', 'introduced', 'removed' keys
    period_start, period_end : datetime
        Period boundaries
    output_folder : str
        Folder to save plots
    """
    os.makedirs(output_folder, exist_ok=True)
    
    # Create timeline visualization
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Plot changes over time
    weeks = [change['week'] for change in product_changes]
    introduced_counts = [len(change['introduced']) for change in product_changes]
    removed_counts = [len(change['removed']) for change in product_changes]
    
    x_pos = range(len(weeks))
    width = 0.35
    
    ax.bar([x - width/2 for x in x_pos], introduced_counts, width, label='Introduced', color='green', alpha=0.7)
    ax.bar([x + width/2 for x in x_pos], removed_counts, width, label='Removed', color='red', alpha=0.7)
    
    ax.set_xlabel('Week', fontsize=14)
    ax.set_ylabel('Number of Products', fontsize=14)
    ax.set_title(f'Product Line Changes Over Time\nStore {dept_id} (Product {product_id} Analysis)', 
                fontsize=16, fontweight='bold')
    ax.set_xticks(x_pos)
    # Custom labels for the specific file/store combination if length matches
    custom_labels = [-2, -1, 1, 2, -2, -1, 1, 2]
    if len(weeks) == len(custom_labels):
        ax.set_xticklabels(custom_labels)
    else:
        ax.set_xticklabels([str(w) for w in weeks], rotation=45, ha='right')
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    output_path = os.path.join(output_folder, f'store_{dept_id}_product_{product_id}_line_changes.pdf')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"   Saved product line changes plot to: {output_path}")
    plt.close()
    
    return output_path

def visualize_changed_product_demand(dept_id, changed_products, intro_start, intro_end,
                                    removal_start, removal_end, product_dept_demand, output_folder='plots'):
    """
    Visualize daily demand changes of products that were introduced/removed.
    
    Parameters:
    -----------
    dept_id : int
        Store ID
    changed_products : set
        Set of product IDs that changed
    intro_start, intro_end : datetime
        Introduction period boundaries
    removal_start, removal_end : datetime
        Removal period boundaries
    product_dept_demand : pd.DataFrame
        Table with columns: product_id, dt, dept_id, demand
    output_folder : str
        Folder to save plots
    """
    os.makedirs(output_folder, exist_ok=True)
    
    # Limit to top 5 changed products to avoid clutter
    changed_products_list = list(changed_products)[:5]
    
    if len(changed_products_list) == 0:
        return None
    
    # Create subplots for each changed product
    n_products = len(changed_products_list)
    n_cols = min(3, n_products)
    n_rows = (n_products + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(6*n_cols, 5*n_rows))
    if n_products == 1:
        axes = [axes]
    else:
        axes = axes.flatten()
    
    for idx, changed_product_id in enumerate(changed_products_list):
        # Get demand data for this product at this store during the 8-week period
        # (both introduction and removal periods)
        product_data = product_dept_demand[
            (product_dept_demand['product_id'] == changed_product_id) &
            (product_dept_demand['dept_id'] == dept_id) &
            (
                ((product_dept_demand['dt'] >= intro_start) & (product_dept_demand['dt'] <= intro_end)) |
                ((product_dept_demand['dt'] >= removal_start) & (product_dept_demand['dt'] <= removal_end))
            )
        ].copy()
        
        if len(product_data) > 0:
            product_data = product_data.sort_values('dt')
            axes[idx].bar(product_data['dt'], product_data['demand'],
                          color='purple', alpha=0.75)
            axes[idx].set_xlabel('Date', fontsize=12)
            axes[idx].set_ylabel('Daily Demand', fontsize=12)
            axes[idx].set_title(f'Product {changed_product_id} Daily Demand\nStore {dept_id}', 
                              fontsize=14, fontweight='bold')
            axes[idx].grid(True, alpha=0.3)
            axes[idx].tick_params(axis='x', rotation=45)
        else:
            axes[idx].text(0.5, 0.5, f'No data for\nProduct {changed_product_id}', 
                          ha='center', va='center', transform=axes[idx].transAxes)
            axes[idx].set_title(f'Product {changed_product_id}\nStore {dept_id}', fontsize=14)
    
    # Hide unused subplots
    for idx in range(n_products, len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    output_path = os.path.join(output_folder, f'store_{dept_id}_changed_products_demand.pdf')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"   Saved changed products demand plot to: {output_path}")
    plt.close()
    
    return output_path


def visualize_consumer_new_product_curve(stats_df, output_folder='plots'):
    """
    Visualize how many consumers purchase a new product at each purchase index.
    stats_df columns: purchase_idx, new_count, total, ratio
    """
    os.makedirs(output_folder, exist_ok=True)
    stats_df = stats_df.sort_values("purchase_idx")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(stats_df["purchase_idx"], stats_df["new_count"], color="steelblue", alpha=0.7, label="New product count")
    ax2 = ax.twinx()
    ax2.plot(stats_df["purchase_idx"], stats_df["ratio"], color="coral", linewidth=2, marker="o", label="Ratio new")

    ax.set_xlabel("Purchase index", fontsize=12)
    ax.set_ylabel("Number of consumers (new product)", fontsize=12)
    ax2.set_ylabel("Ratio of new product", fontsize=12)
    ax.set_title("New Product Adoption by Purchase Index", fontsize=14, fontweight="bold")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left")
    ax2.legend(loc="upper right")

    plt.tight_layout()
    output_path = os.path.join(output_folder, "consumer_new_product_curve.png")
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Saved new product curve plot to: {output_path}")
    plt.close()
    return output_path


def visualize_immediate_repurchase_rate(rate_df, output_folder='plots'):
    """
    Visualize immediate repurchase rate vs purchase index.
    rate_df columns: purchase_idx, immediate_repurchase_rate
    """
    os.makedirs(output_folder, exist_ok=True)
    rate_df = rate_df.sort_values("purchase_idx")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(rate_df["purchase_idx"], rate_df["immediate_repurchase_rate"],
            marker="o", linewidth=2, color="purple")
    ax.set_xlabel("Purchase index", fontsize=12)
    ax.set_ylabel("Immediate repurchase rate", fontsize=12)
    ax.set_title("Immediate Repurchase Rate by Purchase Index", fontsize=14, fontweight="bold")
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 1)

    plt.tight_layout()
    output_path = os.path.join(output_folder, "consumer_immediate_repurchase_rate.png")
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Saved immediate repurchase rate plot to: {output_path}")
    plt.close()
    return output_path

