import pandas as pd
from datetime import datetime, timedelta
from visualize import visualize_dept_week_order_daily
import matplotlib.pyplot as plt
import numpy as np
import os

def dept_weekly_demand(dept_week_order_path='data1031/dept_result_week_order.csv', output_folder='plots'):
    """
    Process weekly demand data and visualize it as daily demand.
    
    Parameters:
    -----------
    dept_week_order_path : str
        Path to dept_result_week_order.csv
    output_folder : str
        Folder path to save the plots (default: 'plots')
    """
    dept_week_order = pd.read_csv(dept_week_order_path, encoding='utf-8-sig')
    # group by dept_id and monday_date, sum the coffee_num and drink_not_coffee_num
    dept_week_order_grouped = dept_week_order.groupby(['dept_id', 'monday_date']).agg({'coffee_num': 'sum', 'drink_not_coffee_num': 'sum'}).reset_index()
    # sum coffee_num and drink_not_coffee_num
    dept_week_order_grouped['total'] = dept_week_order_grouped['coffee_num'] + dept_week_order_grouped['drink_not_coffee_num']
    # drop coffee_num and drink_not_coffee_num
    dept_week_order_grouped = dept_week_order_grouped.drop(columns=['coffee_num', 'drink_not_coffee_num'])
    # divide over 7 and print summary statistics
    dept_week_order_grouped['total'] = dept_week_order_grouped['total'] / 7
    print("\nSummary statistics of daily demand (approximated from weekly data):")
    print(dept_week_order_grouped['total'].describe())
    
    # Visualize the data
    print("\n" + "="*60)
    print("Visualizing weekly order data as daily demand...")
    print("="*60)
    visualize_dept_week_order_daily(dept_week_order, output_folder=output_folder)


def compare_week_demand(dept_id, monday_date, df,
                         dept_week_order_path='data1031/dept_result_week_order.csv'):
    """
    Compare the total demand count of a specific week for a specific store between:
    - dept_result_week_order.csv (aggregated weekly data)
    - df (processed order_commodity_result data)
    
    Parameters:
    -----------
    dept_id : int
        The store ID to check
    monday_date : str or datetime
        The Monday date of the week to check (format: 'YYYY-MM-DD')
    df : pd.DataFrame
        Processed dataframe from order_commodity_result_processed.csv
        Should have columns: member_id, dt, dept_id, is_top, product_id
    dept_week_order_path : str
        Path to dept_result_week_order.csv
    
    Returns:
    --------
    dict : Comparison results with total count
    """
    # Read the aggregated weekly data
    dept_week_order = pd.read_csv(dept_week_order_path, encoding='utf-8-sig')
    
    # Convert monday_date to datetime if it's a string
    if isinstance(monday_date, str):
        monday_date = pd.to_datetime(monday_date)
    else:
        monday_date = pd.to_datetime(monday_date)
    
    # Calculate the week range (Monday to Sunday)
    sunday_date = monday_date + timedelta(days=6)
    week_end = sunday_date + timedelta(days=1)  # Exclusive end for filtering
    
    print(f"\nComparing total demand for Dept {dept_id} for week starting {monday_date.date()}")
    print(f"Week range: {monday_date.date()} to {sunday_date.date()}")
    
    # Get the aggregated data from dept_result_week_order.csv
    week_order_data = dept_week_order[
        (dept_week_order['dept_id'] == dept_id) & 
        (pd.to_datetime(dept_week_order['monday_date']) == monday_date)
    ]
    
    if week_order_data.empty:
        print(f"\nWarning: No data found in dept_result_week_order.csv for dept_id={dept_id}, week={monday_date.date()}")
        return None
    
    # Extract the aggregated total count
    aggregated_coffee_num = week_order_data['coffee_num'].iloc[0]
    aggregated_drink_not_coffee_num = week_order_data['drink_not_coffee_num'].iloc[0]
    #aggregated_food_num = week_order_data['food_num'].iloc[0]
    aggregated_total = aggregated_coffee_num + aggregated_drink_not_coffee_num# + aggregated_food_num
    
    print(f"\nFrom dept_result_week_order.csv:")
    print(f"  Total count: {aggregated_total}")
    
    # Process df to calculate total demand for the same week
    # Ensure dt is datetime
    if not pd.api.types.is_datetime64_any_dtype(df['dt']):
        df['dt'] = pd.to_datetime(df['dt'])
    
    # Filter for the specific dept_id and week
    week_orders = df[
        (df['dept_id'] == dept_id) &
        (df['dt'] >= monday_date) &
        (df['dt'] < week_end)
    ].copy()
        
    # Count total items - each row represents one item/commodity
    calculated_total = len(week_orders)
    
    print(f"\nFrom df (calculated):")
    print(f"  Total count: {calculated_total}")
    
    # Compare the results
    print(f"\n" + "="*60)
    print("COMPARISON RESULTS:")
    print("="*60)
    
    total_match = (aggregated_total == calculated_total)
    
    print(f"Total count: {'✓ MATCH' if total_match else '✗ MISMATCH'}")
    if not total_match:
        print(f"  Difference: {abs(aggregated_total - calculated_total)}")
        print(f"  Aggregated: {aggregated_total}, Calculated: {calculated_total}")
    
    # Return results
    return {
        'dept_id': dept_id,
        'monday_date': monday_date.date(),
        'aggregated_total': aggregated_total,
        'calculated_total': calculated_total,
        'match': total_match,
        'difference': abs(aggregated_total - calculated_total) if not total_match else 0
    }

def visualize_zero_demand_days(data_path='processed_data/order_commodity_result_processed.csv', 
                                output_folder='plots', max_stores=None, max_dates=None):
    """
    Visualize days where each store has zero demand (no records in the data).
    
    Parameters:
    -----------
    data_path : str
        Path to the processed order_commodity_result_processed.csv file
    output_folder : str
        Folder path to save the plot (default: 'plots')
    max_stores : int, optional
        Maximum number of stores to visualize (for performance). If None, visualize all stores.
    max_dates : int, optional
        Maximum number of dates to visualize (for performance). If None, visualize all dates.
    
    Returns:
    --------
    str : Path to the saved plot
    """
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    print("\n" + "="*60)
    print("Visualizing zero demand days for each store...")
    print("="*60)
    
    # Load the processed data
    print(f"\nLoading data from: {data_path}")
    df = pd.read_csv(data_path)
    df['dt'] = pd.to_datetime(df['dt'])
    
    print(f"Total rows in data: {len(df)}")
    
    # Get all unique dates and dept_ids from the data
    all_dates = sorted(df['dt'].unique())
    all_dept_ids = sorted(df['dept_id'].unique())
    
    print(f"Total unique dates: {len(all_dates)}")
    print(f"Total unique stores: {len(all_dept_ids)}")
    print(f"Date range: {all_dates[0].date()} to {all_dates[-1].date()}")
    
    # Optionally limit the number of stores/dates for visualization
    if max_stores is not None and len(all_dept_ids) > max_stores:
        print(f"\nLimiting visualization to {max_stores} stores (out of {len(all_dept_ids)})")
        all_dept_ids = all_dept_ids[:max_stores]
    
    if max_dates is not None and len(all_dates) > max_dates:
        print(f"\nLimiting visualization to {max_dates} dates (out of {len(all_dates)})")
        # Sample dates evenly
        step = len(all_dates) // max_dates
        all_dates = all_dates[::step][:max_dates]
    
    # Create a complete grid of all date × dept_id combinations
    complete_grid = pd.MultiIndex.from_product(
        [all_dates, all_dept_ids], 
        names=['dt', 'dept_id']
    ).to_frame(index=False)
    
    # Get actual records (store-date combinations that have demand)
    actual_records = df.groupby(['dt', 'dept_id']).size().reset_index(name='count')
    actual_records = actual_records[['dt', 'dept_id']]
    
    # Merge to identify which combinations have no records (zero demand)
    merged = complete_grid.merge(
        actual_records, 
        on=['dt', 'dept_id'], 
        how='left', 
        indicator=True
    )
    
    # Mark zero demand: 1 if no record (zero demand), 0 if record exists (has demand)
    merged['zero_demand'] = (merged['_merge'] == 'left_only').astype(int)
    
    # Create a pivot table for visualization: dates as columns, stores as rows
    # Ensure the order is preserved by using reindex
    pivot_table = merged.pivot(index='dept_id', columns='dt', values='zero_demand')
    # Reindex to ensure correct order
    pivot_table = pivot_table.reindex(index=all_dept_ids, columns=all_dates)
    
    # Calculate statistics
    total_cells = len(complete_grid)
    zero_demand_cells = merged['zero_demand'].sum()
    zero_demand_pct = (zero_demand_cells / total_cells) * 100
    
    print(f"\nStatistics:")
    print(f"  Total store-date combinations: {total_cells}")
    print(f"  Zero demand days: {zero_demand_cells} ({zero_demand_pct:.2f}%)")
    print(f"  Days with demand: {total_cells - zero_demand_cells} ({100 - zero_demand_pct:.2f}%)")
    
    # Create the visualization
    print(f"\nCreating heatmap visualization...")
    fig, ax = plt.subplots(figsize=(max(12, len(all_dates) * 0.1), max(8, len(all_dept_ids) * 0.15)))
    
    # Create the heatmap using imshow
    im = ax.imshow(pivot_table.values, aspect='auto', cmap='Reds', interpolation='nearest', vmin=0, vmax=1)
    
    # Set labels
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Store ID (dept_id)', fontsize=12, fontweight='bold')
    ax.set_title('Zero Demand Days by Store\n(Red = Zero Demand, White = Has Demand)', 
                 fontsize=14, fontweight='bold')
    
    # Set x-axis ticks (dates)
    # Show a subset of dates to avoid overcrowding
    n_ticks = min(20, len(all_dates))
    date_indices = np.linspace(0, len(all_dates) - 1, n_ticks, dtype=int)
    ax.set_xticks(date_indices)
    ax.set_xticklabels([all_dates[i].strftime('%Y-%m-%d') for i in date_indices], 
                       rotation=45, ha='right', fontsize=8)
    
    # Set y-axis ticks (store IDs)
    # Show a subset of store IDs
    n_store_ticks = min(30, len(all_dept_ids))
    store_indices = np.linspace(0, len(all_dept_ids) - 1, n_store_ticks, dtype=int)
    ax.set_yticks(store_indices)
    ax.set_yticklabels([all_dept_ids[i] for i in store_indices], fontsize=8)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax, fraction=0.02, pad=0.04)
    cbar.set_label('Zero Demand (1=No Demand, 0=Has Demand)', fontsize=10)
    cbar.set_ticks([0, 1])
    cbar.set_ticklabels(['Has Demand', 'Zero Demand'])
    
    plt.tight_layout()
    
    # Save the plot
    output_path = os.path.join(output_folder, 'zero_demand_days_heatmap.pdf')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\nPlot saved to: {output_path}")
    plt.close()
    
    # Also create a summary plot showing zero demand days per store
    zero_demand_by_store = merged.groupby('dept_id')['zero_demand'].sum().reset_index(name='zero_demand_days')
    zero_demand_by_store = zero_demand_by_store.sort_values('zero_demand_days', ascending=False)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(range(len(zero_demand_by_store)), zero_demand_by_store['zero_demand_days'], 
           color='coral', alpha=0.7)
    ax.set_xlabel('Store ID (sorted by zero demand days)', fontsize=12)
    ax.set_ylabel('Number of Zero Demand Days', fontsize=12)
    ax.set_title('Zero Demand Days per Store', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    summary_output_path = os.path.join(output_folder, 'zero_demand_days_by_store.pdf')
    plt.savefig(summary_output_path, dpi=300, bbox_inches='tight')
    print(f"Summary plot saved to: {summary_output_path}")
    plt.close()
    
    print(f"\nZero demand visualization complete!")
    print(f"  - Heatmap: {output_path}")
    print(f"  - Summary: {summary_output_path}")
    
    return output_path

'''
{'dept_id': 24, 'monday_date': datetime.date(2020, 6, 1), 'aggregated_total': 201, 'calculated_total': 81, 'match': False, 'difference': 120}
'''

if __name__ == "__main__":
    #dept_weekly_demand()
    visualize_zero_demand_days()
