# This script analyzes the impact of removing a product from a store's product line.
# It examines changes in demand patterns before and after product removal.

import pandas as pd
import numpy as np
from datetime import timedelta
from visualize import (
    visualize_demand_ratio_by_period,
    visualize_weekly_demand_by_period,
    visualize_product_line_changes,
    visualize_changed_product_demand
)

def analyze_removal_impact(product_id, product_dept_demand, df, output_folder='plots'):
    """
    Analyze the impact of removing a product (product_id 213) on a specific store.
    
    Parameters:
    -----------
    product_id : int
        The product ID to analyze (default: 213)
    product_dept_demand : pd.DataFrame
        Table with columns: product_id, dt, dept_id, demand
    df : pd.DataFrame
        Processed dataframe with columns: product_id, dt, dept_id, etc.
    output_folder : str
        Folder path to save the plots (default: 'plots')
    """
    product_dept_demand = product_dept_demand[product_dept_demand['demand'] > 0]
    print("\n" + "="*60)
    print(f"ANALYZING REMOVAL IMPACT FOR PRODUCT ID: {product_id}")
    print("="*60)
    
    # Ensure dt is datetime
    if not pd.api.types.is_datetime64_any_dtype(product_dept_demand['dt']):
        product_dept_demand['dt'] = pd.to_datetime(product_dept_demand['dt'])
    if not pd.api.types.is_datetime64_any_dtype(df['dt']):
        df['dt'] = pd.to_datetime(df['dt'])

    sub_df = (
        df.groupby('dept_id')['dt']
        .agg(first_record_day='min', last_record_day='max')
        .reset_index()
    )
    
    # 1. Pick a dept_id that offered this product with constraints:
    #    - first_day after 2020-07-01
    #    - first_day is NOT the store set_up_time (if available)
    #    - last_day  is NOT the store shut_up_time (if available)
    product_stores = product_dept_demand[product_dept_demand['product_id'] == product_id]['dept_id'].unique()
    if len(product_stores) == 0:
        print(f"\nError: Product {product_id} was never offered in any store!")
        return

    # Read store setup/shutdown info
    try:
        dept_static = pd.read_csv(
            'data1031/dept_result_static.csv',
            encoding='utf-8-sig',
            usecols=['dept_id', 'set_up_time', 'shut_up_time'],
        )
        dept_static['set_up_time'] = pd.to_datetime(dept_static['set_up_time'], errors='coerce')
        dept_static['shut_up_time'] = pd.to_datetime(dept_static['shut_up_time'], errors='coerce')
    except Exception as e:
        print(f"\nWarning: could not read dept_result_static.csv: {e}")
        dept_static = pd.DataFrame(columns=['dept_id', 'set_up_time', 'shut_up_time'])

    product_dept_demand_selected = product_dept_demand[product_dept_demand['product_id'] == product_id]
    selected_dept_id = None

    for candidate_index, candidate in enumerate(product_stores):
        store_data = product_dept_demand_selected[product_dept_demand_selected['dept_id'] == candidate]
        first_day_candidate = store_data['dt'].min()
        last_day_candidate = store_data['dt'].max()

        # Must be after 2020-07-01
        if first_day_candidate <= pd.to_datetime('2020-07-01'):
            continue

        # Check against store setup/shutdown dates
        setup_series = dept_static.loc[dept_static['dept_id'] == candidate, 'set_up_time']
        shutdown_series = dept_static.loc[dept_static['dept_id'] == candidate, 'shut_up_time']
        setup_time = setup_series.iloc[0] if not setup_series.empty else pd.NaT
        shutdown_time = shutdown_series.iloc[0] if not shutdown_series.empty else pd.NaT

        first_record_series = sub_df.loc[sub_df['dept_id'] == candidate, 'first_record_day']
        last_record_series = sub_df.loc[sub_df['dept_id'] == candidate, 'last_record_day']
        first_record_day = first_record_series.iloc[0] if not first_record_series.empty else pd.NaT
        last_record_day = last_record_series.iloc[0] if not last_record_series.empty else pd.NaT

        if pd.notna(setup_time) and (first_day_candidate - timedelta(days=14) < setup_time):
            continue
        if pd.notna(shutdown_time) and (last_day_candidate + timedelta(days=14) > shutdown_time):
            continue
        if pd.notna(first_record_day) and (first_day_candidate - timedelta(days=14) < first_record_day):
            continue
        if pd.notna(last_record_day) and (last_day_candidate + timedelta(days=14) > last_record_day):
            continue
        # make sure the interval between first_day_candidate and last_day_candidate is at least 14 days
        if (last_day_candidate - first_day_candidate).days < 28:
            continue

        selected_dept_id = candidate
        break

    if selected_dept_id is None:
        print("\nError: No suitable store found that meets the selection criteria.")
        return
    
    print(f"\n1. Randomly selected store (dept_id): {selected_dept_id}")
    
    # Get demand data for this product at this store
    product_store_demand = product_dept_demand[
        (product_dept_demand['product_id'] == product_id) &
        (product_dept_demand['dept_id'] == selected_dept_id)
    ].copy()

    # Find first and last day this product appeared at this store
    product_store_demand_positive = product_store_demand[product_store_demand['demand'] > 0]
    if len(product_store_demand_positive) == 0:
        print(f"\nError: Product {product_id} never had positive demand at store {selected_dept_id}!")
        return
    
    first_day = product_store_demand_positive['dt'].min()
    last_day = product_store_demand_positive['dt'].max()
    
    print(f"   First day product appeared: {first_day.date()}")
    print(f"   Last day product appeared: {last_day.date()}")
    
    # Calculate periods: 2 weeks before/after introduction and removal
    # Period 1: 2 weeks before first_day to 2 weeks after first_day (4 weeks total)
    intro_2weeks_before = first_day - timedelta(days=14)
    intro_2weeks_after = first_day + timedelta(days=14)
    
    # Period 2: 2 weeks before last_day to 2 weeks after last_day (4 weeks total)
    removal_2weeks_before = last_day - timedelta(days=14)
    removal_2weeks_after = last_day + timedelta(days=14)
    
    print(f"\n   Analysis periods:")
    print(f"   - Introduction period: 2 weeks before ({intro_2weeks_before.date()}) to 2 weeks after ({intro_2weeks_after.date()})")
    print(f"   - Removal period: 2 weeks before ({removal_2weeks_before.date()}) to 2 weeks after ({removal_2weeks_after.date()})")
    print(f"   - Total 8-week period: {intro_2weeks_before.date()} to {removal_2weeks_after.date()}")
    
    # 2. Visualize demand ratio across products
    print("\n2. Visualizing demand ratio across products...")
    visualize_demand_ratio_by_period(
        dept_id=selected_dept_id,
        product_id=product_id,
        df=df,
        intro_start=intro_2weeks_before,
        intro_end=intro_2weeks_after,
        removal_start=removal_2weeks_before,
        removal_end=removal_2weeks_after,
        first_day=first_day,
        last_day=last_day,
        output_folder=output_folder
    )
    
    # 3. Visualize total weekly demand
    print("\n3. Visualizing total weekly demand...")
    visualize_weekly_demand_by_period(
        dept_id=selected_dept_id,
        product_id=product_id,
        df=df,
        intro_start=intro_2weeks_before,
        intro_end=intro_2weeks_after,
        removal_start=removal_2weeks_before,
        removal_end=removal_2weeks_after,
        output_folder=output_folder
    )
    
    # 4. Check for product line changes during 8-week period
    print("\n4. Checking for product line changes...")
    # 8-week period consists of:
    # - Period 1: 2 weeks before first_day to 2 weeks after first_day
    # - Period 2: 2 weeks before last_day to 2 weeks after last_day
    # Helper: detect product line changes within a slice and tag with label
    def detect_changes(df_slice, label):
        if df_slice.empty:
            return []
        df_slice = df_slice.copy()
        df_slice['week'] = df_slice['dt'].dt.to_period('W')
        products_by_week = df_slice.groupby('week')['product_id'].apply(lambda x: set(x.unique())).reset_index()
        products_by_week.columns = ['week', 'products']
        changes = []
        for i in range(1, len(products_by_week)):
            prev_products = products_by_week.iloc[i-1]['products']
            curr_products = products_by_week.iloc[i]['products']
            introduced = curr_products - prev_products
            removed = prev_products - curr_products
            if introduced or removed:
                changes.append({
                    'week': f"{products_by_week.iloc[i]['week']} ({label})",
                    'introduced': introduced,
                    'removed': removed
                })
        return changes

    # Slice data for the four-week windows (intro and removal)
    intro_slice = df[
        (df['dept_id'] == selected_dept_id) &
        (df['dt'] >= intro_2weeks_before) & (df['dt'] <= intro_2weeks_after)
    ].copy()
    removal_slice = df[
        (df['dept_id'] == selected_dept_id) &
        (df['dt'] >= removal_2weeks_before) & (df['dt'] <= removal_2weeks_after)
    ].copy()
    
    product_changes = []
    product_changes += detect_changes(intro_slice, 'Intro')
    product_changes += detect_changes(removal_slice, 'Removal')
    
    if len(product_changes) > 0:
        print(f"   Found {len(product_changes)} weeks with product line changes")
        for change in product_changes:
            print(f"   Week {change['week']}: Introduced {len(change['introduced'])} products, Removed {len(change['removed'])} products")
        
        # Visualize product line changes
        visualize_product_line_changes(
            dept_id=selected_dept_id,
            product_id=product_id,
            product_changes=product_changes,
            period_start=min(intro_2weeks_before, removal_2weeks_before),
            period_end=max(intro_2weeks_after, removal_2weeks_after),
            output_folder=output_folder
        )
        
        # Visualize daily demand changes of changed products
        all_changed_products = set()
        for change in product_changes:
            all_changed_products.update(change['introduced'])
            all_changed_products.update(change['removed'])
        all_changed_products.discard(product_id)  # Exclude the main product
        
        if len(all_changed_products) > 0:
            print(f"\n5. Visualizing daily demand changes of {len(all_changed_products)} changed products...")
            visualize_changed_product_demand(
                dept_id=selected_dept_id,
                changed_products=all_changed_products,
                intro_start=intro_2weeks_before,
                intro_end=intro_2weeks_after,
                removal_start=removal_2weeks_before,
                removal_end=removal_2weeks_after,
                product_dept_demand=product_dept_demand,
                output_folder=output_folder
            )
        else:
            print(f"\n5. No other products changed (only product {product_id} changed)")
    else:
        print(f"   No product line changes detected during the 8-week period")
    
    print("\n" + "="*60)
    print("Analysis complete!")
    print("="*60)

if __name__ == "__main__":
    # Example usage
    import sys
    sys.path.append('.')
    from process_order_commodity import create_product_dept_daily_demand
    
    # This would be called from the main script
    # analyze_removal_impact(product_id=213, product_dept_demand=product_dept_demand, df=df)

