import pandas as pd
from visualize import visualize_dept_daily_demand, visualize_product_dept_daily_demand
from removal_impact import analyze_removal_impact
import numpy as np

def read_and_process_data():
    # Read the CSV file with only the specified columns
    columns_to_read = [
        'member_id', 
        'create_hour', 
        'dept_id', 
        'is_top_commodity_coffee_tag', 
        'is_top_commodity_not_coffee_tag', 
        'coffee_commodity_name', 
        'drink_not_coffee_commodity_name'
    ]

    # Read CSV file (handling BOM if present)
    df = pd.read_csv('data1031/order_commodity_result.csv', usecols=columns_to_read, encoding='utf-8-sig')
    print(f"Total rows before filtering: {len(df)}")
    # Process dt: extract only year-month-day
    # Assuming dt format is like '2021-05-29 17' or similar
    # Extract date part (first 10 characters: YYYY-MM-DD)
    df['dt'] = df['create_hour'].astype(str).str[:10]
    df['dt'] = pd.to_datetime(df['dt'])
    # filter out rows where dt is NaT
    df = df.dropna(subset=['dt'])

    # Replace empty strings with NaN for consistent handling
    df['coffee_commodity_name'] = df['coffee_commodity_name'].replace('', pd.NA)
    df['drink_not_coffee_commodity_name'] = df['drink_not_coffee_commodity_name'].replace('', pd.NA)

    # Filter out rows where both coffee_commodity_name and drink_not_coffee_commodity_name are NA
    # Keep rows where at least one of them is not NA
    df = df.dropna(subset=['coffee_commodity_name', 'drink_not_coffee_commodity_name'], how='all')

    # Combine is_top_commodity_coffee_tag and is_top_commodity_not_coffee_tag into "is_top"
    # Use fillna(0) to handle missing values, then take the maximum (if either is 1, is_top is 1)
    df['is_top'] = df[['is_top_commodity_coffee_tag', 'is_top_commodity_not_coffee_tag']].fillna(0).max(axis=1)

    # Combine coffee_commodity_name and drink_not_coffee_commodity_name into "name"
    # Since we filtered out rows where both are NA, at least one will have a value
    # Use combine_first to take the non-NA value (they are mutually exclusive)
    df['name'] = df['coffee_commodity_name'].combine_first(df['drink_not_coffee_commodity_name'])

    # Drop the original columns that were combined
    df = df.drop(columns=['create_hour', 'is_top_commodity_coffee_tag', 'is_top_commodity_not_coffee_tag', 
                        'coffee_commodity_name', 'drink_not_coffee_commodity_name'])

    # 1. Add product_id to different "names", create a placeholder to record the relationship
    # Create a mapping from name to product_id
    unique_names = df['name'].unique()
    product_mapping = pd.DataFrame({
        'product_id': range(1, len(unique_names) + 1),
        'name': unique_names
    })
    product_mapping = product_mapping.sort_values('name').reset_index(drop=True)
    product_mapping['product_id'] = range(1, len(product_mapping) + 1)

    # Merge product_id into df temporarily to calculate first_day and last_day
    df_temp = df.merge(product_mapping[['name', 'product_id']], on='name', how='left')
    
    # Calculate first_day and last_day for each product_id
    product_dates = df_temp.groupby('product_id')['dt'].agg(['min', 'max']).reset_index()
    product_dates.columns = ['product_id', 'first_day', 'last_day']
    product_mapping = product_mapping.merge(product_dates, on='product_id', how='left')

    # Merge product_id into df (final merge)
    df = df_temp.drop(columns=['name'])

    print("\n" + "="*50)
    print("Product ID Mapping (placeholder):")
    print("="*50)
    print(product_mapping)
    print(f"\nTotal unique products: {len(product_mapping)}")

    # Optionally save to files
    df.to_csv('processed_data/order_commodity_result_processed.csv', index=False)
    product_mapping.to_csv('processed_data/product_mapping.csv', index=False)

def data_statistics(df):
    # Mean daily demand of each product
    # Group by product_id and date, count occurrences, then average across dates
    product_daily_demand = df.groupby(['product_id', 'dt']).size().reset_index(name='daily_demand')
    product_mean_daily_demand = product_daily_demand.groupby('product_id')['daily_demand'].mean().reset_index(name='mean_daily_demand')
    print(f"\n1. Mean daily demand of each product:")
    print(product_mean_daily_demand['mean_daily_demand'].describe())

    # Total unique dept_id
    total_unique_depts = df['dept_id'].nunique()
    print(f"\n2. Total unique dept_id: {total_unique_depts}")

    # Mean daily demand of each dept_id
    # Group by dept_id and date, count occurrences
    dept_daily_demand = df.groupby(['dept_id', 'dt']).size().reset_index(name='daily_demand')

    # Fill in missing days (where a dept_id has no record) as daily_demand = 0
    # Create a complete combination of all dept_id and all dates
    all_dates = df['dt'].unique()
    all_dept_ids = df['dept_id'].unique()
    complete_dept_date = pd.MultiIndex.from_product([all_dept_ids, all_dates], names=['dept_id', 'dt']).to_frame(index=False)

    # Merge with actual daily demand, fill missing with 0
    dept_daily_demand_complete = complete_dept_date.merge(dept_daily_demand, on=['dept_id', 'dt'], how='left')
    dept_daily_demand_complete['daily_demand'] = dept_daily_demand_complete['daily_demand'].fillna(0)
    
    # Visualize daily demand for each store
    visualize_dept_daily_demand(dept_daily_demand_complete)

    # Now compute the mean
    dept_mean_daily_demand = dept_daily_demand_complete.groupby('dept_id')['daily_demand'].mean().reset_index(name='mean_daily_demand')
    print(f"\n3. Mean daily demand of each dept_id:")
    print(dept_mean_daily_demand['mean_daily_demand'].describe())

    # For each consumer, the number of dept_id he purchased from
    consumer_dept_count = df.groupby('member_id')['dept_id'].nunique().reset_index(name='num_dept_purchased_from')
    print(f"Total unique consumers: {len(consumer_dept_count)}")
    print(f"\n4. Number of dept_id each consumer purchased from:")
    print(consumer_dept_count['num_dept_purchased_from'].describe())

    # frequent consumers
    df_frequent = select_frequent_consumers(df)
    consumer_dept_count_frequent = df_frequent.groupby('member_id')['dept_id'].nunique().reset_index(name='num_dept_purchased_from')
    print(f"\n5. Number of dept_id each frequent consumer purchased from:")
    print(f"Total unique consumers: {len(consumer_dept_count_frequent)}")
    print(consumer_dept_count_frequent['num_dept_purchased_from'].describe())
    
    # For each consumer, how many days he made a purchase    
    consumer_days_count = df.groupby('member_id')['dt'].nunique().reset_index(name='num_days_purchased')
    
    print(f"\n5. Number of days each consumer made a purchase:")
    print(consumer_days_count['num_days_purchased'].describe())
    print("#"*30)
    # Check if there are any 0 values and investigate

def select_frequent_consumers(df):
    consumer_days_count = df.groupby('member_id')['dt'].nunique().reset_index(name='num_days_purchased')
    # df_frequent: select consumers with 3 <= num_days_purchased <= 8
    consumer_days_count_frequent = consumer_days_count[consumer_days_count['num_days_purchased'].between(3, 8)]
    # consumer id
    consumer_ids_frequent = consumer_days_count_frequent['member_id'].unique()
    # df_frequent: select rows where member_id is in consumer_ids_frequent
    df_frequent = df[df['member_id'].isin(consumer_ids_frequent)]
    return df_frequent

def check_product_zero_demand_days(df, product_mapping):
    """
    Check for each product_id, between first_day and last_day, 
    if its demand > 0 every day. If not, count zero demand days.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Processed dataframe with columns: product_id, dt, etc.
    product_mapping : pd.DataFrame
        Product mapping with columns: product_id, first_day, last_day
    
    Returns:
    --------
    pd.DataFrame with columns: product_id, dt, lifecycle, zero_demand_days
    """
    from datetime import timedelta
    
    results = []
    
    for _, product_row in product_mapping.iterrows():
        product_id = product_row['product_id']
        first_day = pd.to_datetime(product_row['first_day'])
        last_day = pd.to_datetime(product_row['last_day'])
        
        # Calculate lifecycle (total days on market)
        lifecycle = (last_day - first_day).days + 1
        
        # Create a complete date range from first_day to last_day
        date_range = pd.date_range(start=first_day, end=last_day, freq='D')
        
        # Get actual demand for this product by date
        product_demand = df[df['product_id'] == product_id].groupby('dt').size().reset_index(name='demand')
        product_demand['dt'] = pd.to_datetime(product_demand['dt'])
        
        # Create complete date-demand mapping
        complete_demand = pd.DataFrame({'dt': date_range})
        complete_demand = complete_demand.merge(product_demand, on='dt', how='left')
        complete_demand['demand'] = complete_demand['demand'].fillna(0)
        
        # Count zero demand days
        zero_demand_days = (complete_demand['demand'] == 0).sum()
        
        results.append({
            'product_id': product_id,
            'dt': first_day,  # Using first_day as representative date for the product
            'lifecycle': lifecycle,
            'zero_demand_days': zero_demand_days
        })
    
    result_df = pd.DataFrame(results)
    return result_df

def create_product_dept_daily_demand(df, product_mapping):
    """
    Create a table recording product daily demand at each dept between first_day and last_day.
    Then summarize for each product_id on a specific dt, how many unique dept_id have recorded demand.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Processed dataframe with columns: product_id, dt, dept_id, etc.
    product_mapping : pd.DataFrame
        Product mapping with columns: product_id, first_day, last_day
    
    Returns:
    --------
    pd.DataFrame with columns: product_id, dt, dept_id, demand
    """
    from datetime import timedelta
    
    # Create product daily demand by dept
    product_dept_demand = df.groupby(['product_id', 'dt', 'dept_id']).size().reset_index(name='demand')
    product_dept_demand['dt'] = pd.to_datetime(product_dept_demand['dt'])
    
    # For each product, fill in missing days between first_day and last_day with 0 demand
    all_records = []
    
    for _, product_row in product_mapping.iterrows():
        product_id = product_row['product_id']
        first_day = pd.to_datetime(product_row['first_day'])
        last_day = pd.to_datetime(product_row['last_day'])
        
        # Get all dept_ids that have this product
        product_depts = df[df['product_id'] == product_id]['dept_id'].unique()
        
        # Create complete date range
        date_range = pd.date_range(start=first_day, end=last_day, freq='D')
        
        # Create complete combination of dates and dept_ids
        complete_combinations = pd.MultiIndex.from_product(
            [date_range, product_depts], 
            names=['dt', 'dept_id']
        ).to_frame(index=False)
        
        # Merge with actual demand
        product_data = product_dept_demand[product_dept_demand['product_id'] == product_id]
        merged = complete_combinations.merge(
            product_data[['dt', 'dept_id', 'demand']], 
            on=['dt', 'dept_id'], 
            how='left'
        )
        merged['demand'] = merged['demand'].fillna(0)
        merged['product_id'] = product_id
        
        all_records.append(merged[['product_id', 'dt', 'dept_id', 'demand']])
    
    # Combine all records
    product_dept_daily_demand = pd.concat(all_records, ignore_index=True)
    
    # Summarize: for each product_id on a specific dt, how many unique dept_id have recorded demand (>0)
    summary = product_dept_daily_demand[product_dept_daily_demand['demand'] > 0].groupby(
        ['product_id']
    )['dept_id'].nunique().reset_index(name='num_dept_with_demand')

    print("\n" + "="*60)
    print("Summary: Number of unique dept_id with demand > 0 for each product_id")
    print("="*60)
    print(summary['num_dept_with_demand'].describe())
    
    daily_summary = product_dept_daily_demand[product_dept_daily_demand['demand'] > 0].groupby(
        ['product_id', 'dt']
    )['dept_id'].nunique().reset_index(name='num_dept_with_demand')
    
    print("\n" + "="*60)
    print("Summary: Number of unique dept_id with demand > 0 for each product_id on each dt")
    print("="*60)
    print(daily_summary['num_dept_with_demand'].describe())
    
    return product_dept_daily_demand, summary, daily_summary

def analyze_top10_products(df, product_mapping, output_folder='plots'):
    """
    Find the 10 most popular products based on highest daily demand,
    and visualize their demand by store.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Processed dataframe with columns: product_id, dt, dept_id, etc.
    product_mapping : pd.DataFrame
        Product mapping with columns: product_id, name, first_day, last_day
    output_folder : str
        Folder path to save the plots (default: 'plots')
    """    
    # Calculate daily demand for each product (groupby product_id and dt, count rows)
    product_daily_demand = df.groupby(['product_id', 'dt']).size().reset_index(name='daily_demand')
    
    # Calculate total daily demand for each product (sum across all days)
    product_total_demand = product_daily_demand.groupby('product_id')['daily_demand'].sum().reset_index(name='total_daily_demand')
    
    # Find top 5 products
    top10_products = product_total_demand.nlargest(10, 'total_daily_demand')
    top10_product_ids = top10_products['product_id'].values
    
    print("\n" + "="*60)
    print("TOP 10 MOST POPULAR PRODUCTS")
    print("="*60)
    
    # Get zero demand days for all products (reuse existing function)
    zero_demand_table = check_product_zero_demand_days(df, product_mapping)
    
    # For each top 5 product, print information and create plots
    for rank, product_id in enumerate(top10_product_ids, 1):
        product_info = product_mapping[product_mapping['product_id'] == product_id].iloc[0]
        product_name = product_info['name']
        first_day = pd.to_datetime(product_info['first_day'])
        last_day = pd.to_datetime(product_info['last_day'])
        
        # Get zero demand days
        zero_demand_info = zero_demand_table[zero_demand_table['product_id'] == product_id]
        zero_demand_days = zero_demand_info['zero_demand_days'].iloc[0] if len(zero_demand_info) > 0 else 0
        
        # Get number of dept it was ever sold at
        product_depts = df[df['product_id'] == product_id]['dept_id'].nunique()
        
        print(f"\n{rank}. Product ID: {product_id}")
        print(f"   Name: {product_name}")
        print(f"   First day: {first_day.date()}")
        print(f"   Last day: {last_day.date()}")
        print(f"   Zero demand days: {zero_demand_days}")
        print(f"   Number of depts sold at: {product_depts}")
        print(f"   Total daily demand: {top10_products[top10_products['product_id'] == product_id]['total_daily_demand'].iloc[0]}")
        
        # Get daily demand by dept for this product
        product_dept_daily = df[df['product_id'] == product_id].groupby(['dt', 'dept_id']).size().reset_index(name='demand')
        product_dept_daily['dt'] = pd.to_datetime(product_dept_daily['dt'])
        
        # Get all dept_ids that have this product
        all_dept_ids = df[df['product_id'] == product_id]['dept_id'].unique()
        
        # Create plot using the visualization function
        output_path = visualize_product_dept_daily_demand(
            product_id=product_id,
            product_name=product_name,
            first_day=first_day,
            last_day=last_day,
            product_dept_daily=product_dept_daily,
            all_dept_ids=all_dept_ids,
            rank=rank,
            output_folder=output_folder
        )
        print(f"   Plot saved to: {output_path}")
    
    print("\n" + "="*60)
    print("Analysis complete!")

def analyze_product(product_id, zero_demand_table, product_dept_demand, df, dept_daily_demand=None, output_folder='plots'):
    """
    Analyze a specific product: zero demand days, depts where it never appeared, 
    and first/last appearance dates in depts where it appeared.
    
    Parameters:
    -----------
    product_id : int
        The product ID to analyze
    zero_demand_table : pd.DataFrame
        Table with columns: product_id, dt, lifecycle, zero_demand_days
    product_dept_demand : pd.DataFrame
        Table with columns: product_id, dt, dept_id, demand
    df : pd.DataFrame
        Processed dataframe with columns: product_id, dt, dept_id, etc.
    dept_daily_demand : pd.DataFrame, optional
        Daily demand by dept (if None, will calculate from df)
    output_folder : str
        Folder path to save the plots (default: 'plots')
    """
    print("\n" + "="*60)
    print(f"ANALYZING PRODUCT ID: {product_id}")
    print("="*60)
    
    # 1. Print the number of days with zero demand
    zero_demand_info = zero_demand_table[zero_demand_table['product_id'] == product_id]
    if len(zero_demand_info) > 0:
        zero_demand_days = zero_demand_info['zero_demand_days'].iloc[0]
        print(f"\n1. Number of days with zero demand: {zero_demand_days}")
    else:
        print(f"\n1. Product {product_id} not found in zero_demand_table")
        return
    
    # Get all dept_ids in the dataset
    all_dept_ids = df['dept_id'].unique()
    
    # Get dept_ids where this product ever appeared
    product_dept_ids = product_dept_demand[product_dept_demand['product_id'] == product_id]['dept_id'].unique()
    
    # 2. Find dept_ids where product never appeared
    dept_ids_never_appeared = set(all_dept_ids) - set(product_dept_ids)
    print(f"\n2. Number of dept_ids where product never appeared: {len(dept_ids_never_appeared)}")
    
    if len(dept_ids_never_appeared) > 0:
        # Get daily demand for these depts
        if dept_daily_demand is None:
            # Calculate from df
            dept_daily_demand_all = df.groupby(['dept_id', 'dt']).size().reset_index(name='daily_demand')
        else:
            dept_daily_demand_all = dept_daily_demand.copy()
        
        # Filter for depts where product never appeared
        never_appeared_demand = dept_daily_demand_all[
            dept_daily_demand_all['dept_id'].isin(dept_ids_never_appeared)
        ]
        
        print(f"\n   Daily demand statistics for depts where product never appeared:")
        print(never_appeared_demand['daily_demand'].describe())
    else:
        print(f"\n   Product appeared in all dept_ids!")
    
    # 3. Find dept_ids where product ever appeared
    print(f"\n3. Number of dept_ids where product ever appeared: {len(product_dept_ids)}")
    
    if len(product_dept_ids) > 0:
        # Filter product_dept_demand for this product
        product_data = product_dept_demand[product_dept_demand['product_id'] == product_id].copy()
        
        # Find first day it appeared in each dept_id
        first_appearance = product_data[product_data['demand'] > 0].groupby('dept_id')['dt'].min().reset_index()
        first_appearance.columns = ['dept_id', 'first_day']
        
        # Find last day it appeared in each dept_id
        last_appearance = product_data[product_data['demand'] > 0].groupby('dept_id')['dt'].max().reset_index()
        last_appearance.columns = ['dept_id', 'last_day']
        
        print(f"\n   First appearance dates:")
        print(first_appearance.head(10))
        print(f"\n   Last appearance dates:")
        print(last_appearance.head(10))
        
        # Visualize first day appearance
        from visualize import visualize_product_first_last_appearance
        visualize_product_first_last_appearance(
            df=df,
            product_id=product_id,
            first_appearance=first_appearance,
            last_appearance=last_appearance,
            output_folder=output_folder
        )
        
        # 4. Analyze store types for stores that didn't offer this product
        analyze_store_types_for_non_offering_stores(product_dept_ids, all_dept_ids)
    else:
        print(f"\n   Product never appeared in any dept!")

def analyze_store_types_for_non_offering_stores(stores_with_product, all_stores, dept_static_path='data1031/dept_result_static.csv'):
    """
    Analyze whether stores that didn't offer a product are self-operation or franchise.
    
    Parameters:
    -----------
    stores_with_product : set or array-like
        Set of store IDs (dept_id) where the product appeared
    all_stores : set or array-like
        Set of all store IDs (dept_id) in the dataset
    dept_static_path : str
        Path to dept_result_static.csv
    """
    print("\n" + "="*60)
    print("4. Analyzing store types for stores that didn't offer this product")
    print("="*60)
    
    # Read dept_result_static.csv
    dept_static = pd.read_csv(dept_static_path, encoding='utf-8-sig', usecols=['dept_id', 'cooperation_sign'])
    
    # Convert to sets for easier operations
    stores_with_product_set = set(stores_with_product)
    all_stores_set = set(all_stores)
    
    # Find stores that didn't offer the product
    stores_without_product = all_stores_set - stores_with_product_set
    
    if len(stores_without_product) == 0:
        print("\n   All stores offered this product!")
        return
    
    print(f"\n   Number of stores that didn't offer this product: {len(stores_without_product)}")
    
    # Filter dept_static for stores without product
    stores_without_product_data = dept_static[dept_static['dept_id'].isin(stores_without_product)].copy()
    
    # Count self-operation stores (cooperation_sign == 1)
    self_operation_count = (stores_without_product_data['cooperation_sign'] == 1).sum()
    franchise_count = len(stores_without_product_data) - self_operation_count
    
    # Calculate ratio
    total_stores_without_product = len(stores_without_product_data)
    if total_stores_without_product > 0:
        self_operation_ratio = self_operation_count / total_stores_without_product
        
        print(f"\n   Store type breakdown for stores that didn't offer this product:")
        print(f"   - Self-operation stores (cooperation_sign=1): {self_operation_count}")
        print(f"   - Franchise stores (cooperation_sign≠1): {franchise_count}")
        print(f"   - Total stores analyzed: {total_stores_without_product}")
        print(f"\n   Ratio of self-operation stores: {self_operation_ratio:.4f} ({self_operation_ratio*100:.2f}%)")
    else:
        print(f"\n   No store data found for stores that didn't offer this product")

if __name__ == "__main__":
    #read_and_process_data()
    df = pd.read_csv('processed_data/order_commodity_result_processed.csv')
    df['dt'] = pd.to_datetime(df['dt'])
    
    # Display the final dataframe info
    print("\n" + "="*50)
    print("Final DataFrame Info:")
    print("="*50)
    print(f"Total rows: {len(df)}")
    print("\nFirst few rows:")
    print(df.head())
    print("\nData info:")
    print(df.info())

    # Load product_mapping to get first_day and last_day
    product_mapping = pd.read_csv('processed_data/product_mapping.csv')
    product_mapping['first_day'] = pd.to_datetime(product_mapping['first_day'])
    product_mapping['last_day'] = pd.to_datetime(product_mapping['last_day'])
    
    data_statistics(df)
    '''
    # Check product zero demand days
    #print("\n" + "="*60)
    #print("Checking product zero demand days...")
    #print("="*60)
    #zero_demand_table = check_product_zero_demand_days(df, product_mapping)
    #print("\nZero demand days table:")
    #print(zero_demand_table.head(20))
    #print(f"\nTotal products: {len(zero_demand_table)}")
    #print(zero_demand_table['zero_demand_days'].describe())
    
    # Create product dept daily demand table
    print("\n" + "="*60)
    print("Creating product dept daily demand table...")
    print("="*60)
    product_dept_demand, summary, daily_summary = create_product_dept_daily_demand(df, product_mapping)
    
    # Analyze top 5 products
    #print("\n" + "="*60)
    #print("Analyzing top 10 most popular products...")
    #print("="*60)
    #analyze_top10_products(df, product_mapping)
    '''
    '''
    Product ID: 28
    Name: 加浓美式_1
    First day: 2020-06-01
    Last day: 2021-09-14
    Zero demand days: 0
    Number of depts sold at: 226'''
    '''
    product_id = 28
    #analyze_product(product_id, zero_demand_table, product_dept_demand, df)
    analyze_removal_impact(product_id=product_id, product_dept_demand=product_dept_demand, df=df)

    product_id = 213
    analyze_product(product_id, zero_demand_table, product_dept_demand, df)
    '''