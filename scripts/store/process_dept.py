import pandas as pd
from datetime import datetime, timedelta
from visualize import visualize_dept_week_order_daily

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

'''
{'dept_id': 24, 'monday_date': datetime.date(2020, 6, 1), 'aggregated_total': 201, 'calculated_total': 81, 'match': False, 'difference': 120}
'''

if __name__ == "__main__":
    dept_weekly_demand()
