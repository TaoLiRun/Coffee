# Basic Push-Purchase Distribution Analysis

This folder contains scripts for analyzing basic distributions and comparisons of push notifications and purchase behavior.

## Scripts

- `combine_push_buy.py` - Builds unified push-purchase panel with features like customer dormancy and days since purchase
- `compare_customers_with_and_without_push.py` - Statistical comparison between push opt-in (push=1) and opt-out (push=0) customers
- `select_no_push_customers.py` - Filters and analyzes customers who opted out of push notifications
- `run.sh` - Batch execution script

## Usage

```bash
cd scripts/push_analysis/basic_distribution
python combine_push_buy.py
python compare_customers_with_and_without_push.py
python select_no_push_customers.py
```
