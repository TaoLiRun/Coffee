# This script selects and analyzes customers who opted out of push notifications (push=0).
# It filters order data for these customers and generates statistics on their purchase behavior.

import pandas as pd
import glob

def select_no_push_orders():
    # Step 1: Read processed_data/order_commodity_result_processed.csv
    full_data = pd.read_csv('../../data/processed/order_commodity_result_processed.csv', usecols=['member_id', 'dept_id', 'product_id', 'dt'])
    print(f"Total unique customers (no push): {full_data['member_id'].nunique()}") #778285

    # Step 2: Read data1031/member_result.csv
    member_data = pd.read_csv('../../../data/data1031/member_result.csv', usecols=['member_id', 'push'])

    # Step 3: Select consumers with push=0
    no_push_members = member_data[member_data['push'] == 0]['member_id']
    # save no_push_members to processed_data/no_push_members.csv
    no_push_members.to_csv('../../data/processed/no_push_members.csv', index=False, encoding='utf-8-sig')

    # Step 4: Filter full_data for rows where member_id is in no_push_members
    no_push_data = full_data[full_data['member_id'].isin(no_push_members)]

    # Step 5: Save the filtered data to processed_data/order_member_no_push.csv
    no_push_data.to_csv('../../data/processed/order_member_no_push.csv', index=False, encoding='utf-8-sig')

def analyze_statistics():
    # Step 1: Read processed_data/order_member_no_push.csv
    no_push_data = pd.read_csv('../../data/processed/order_member_no_push.csv')

    # Step 2: Convert 'dt' to datetime format
    no_push_data['dt'] = pd.to_datetime(no_push_data['dt'])

    # Step 3: Calculate statistics
    unique_customers = no_push_data['member_id'].nunique()
    purchase_counts = no_push_data.groupby('member_id').size()
    unique_products_per_customer = no_push_data.groupby('member_id')['product_id'].nunique()
    unique_stores_per_customer = no_push_data.groupby('member_id')['dept_id'].nunique()
    purchase_intervals = no_push_data.groupby('member_id')['dt'].apply(lambda x: x.sort_values().diff().mean())
    # Step 4: print statistics
    print(f"Total unique customers (no push): {unique_customers}")
    print(f"purchase count per customer (no push): {purchase_counts.describe()}")
    print(f"unique products per customer (no push): {unique_products_per_customer.describe()}")
    print(f"unique stores per customer (no push): {unique_stores_per_customer.describe()}")
    print(f"purchase interval per customer (no push): {purchase_intervals.describe()}")

def check_push_validity():
    print("Checking push validity...")
    # Step 1: Read the selected no-push customers
    try:
        no_push_data = pd.read_csv('../processed_data/order_member_no_push.csv', usecols=['member_id'])
        no_push_members = set(no_push_data['member_id'].unique())
        print(f"Loaded {len(no_push_members)} unique no-push members.") #119839
    except FileNotFoundError:
        print("processed_data/order_member_no_push.csv not found. Please run select_no_push_orders() first.")
        return

    # Step 2: Get list of push files
    push_files = glob.glob('../../data/data1031/sleep_push_result_*.csv')
    
    found_in_push = set()
    intersected_push_data = []  # Store push data for intersected members
    
    # Step 3: Check each push file
    for file_path in push_files:
        print(f"Checking {file_path}...")
        try:
            push_data = pd.read_csv(file_path, usecols=['dt', 'member_id', 'channel', 'trigger_tag'])
            push_members = set(push_data['member_id'].unique())
            
            # Find intersection
            intersection = no_push_members.intersection(push_members)
            if intersection:
                print(f"  Found {len(intersection)} members in {file_path} who are in the no-push list.")
                found_in_push.update(intersection)
                # Store push data for intersected members
                intersected_data = push_data[push_data['member_id'].isin(intersection)]
                intersected_push_data.append(intersected_data)
        except Exception as e:
            print(f"  Error reading {file_path}: {e}")

    # Step 4: Report results
    if found_in_push:
        print(f"WARNING: Found {len(found_in_push)} members who were supposed to be no-push but appeared in push files.") #118253
        
        # Step 5: Analyze push details for intersected members
        if intersected_push_data:
            all_intersected_data = pd.concat(intersected_push_data, ignore_index=True)
            print(f"\nTotal push records: {len(all_intersected_data)}")
            
            print("\n--- Distribution of 'dt' for intersected members ---")
            dt_dist = all_intersected_data['dt'].describe()
            print(dt_dist)

            print("\n--- Distribution of 'channel' for intersected members ---")
            channel_dist = all_intersected_data['channel'].value_counts()
            print(channel_dist)
            
            print("\n--- Distribution of 'trigger_tag' for intersected members ---")
            trigger_tag_dist = all_intersected_data['trigger_tag'].value_counts()
            print(trigger_tag_dist)
            
            # Also show cross-tabulation if useful
            print("\n--- Cross-tabulation of 'channel' and 'trigger_tag' ---")
            crosstab = pd.crosstab(all_intersected_data['channel'], all_intersected_data['trigger_tag'])
            print(crosstab)
    else:
        print("Verification passed: No selected no-push members appeared in push files.")

if __name__ == "__main__":
    select_no_push_orders()
    check_push_validity()
    analyze_statistics()
