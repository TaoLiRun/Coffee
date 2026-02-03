# Push Analysis Scripts

This folder contains scripts for analyzing push notification effects on customer behavior.

## Contents

### Main Scripts
- `combine_push_order.r` - Combines push notification data with order data to analyze the relationship between marketing pushes and customer purchases
- `policy.r` - Processes push notification policy data by aggregating push counts by date, policy ID, and trigger tag
- `read_combined.r` - Analyzes combined push and purchase data to understand push timing patterns

### Subfolders
- `basic_distribution/` - Basic push-purchase distribution analysis
- `sensitivity_analysis/` - Advanced DiD and survival analysis (see subfolder README)

## Usage

Run scripts from the repository root directory:
```bash
Rscript scripts/push_analysis/combine_push_order.r
Rscript scripts/push_analysis/policy.r
Rscript scripts/push_analysis/read_combined.r
```
