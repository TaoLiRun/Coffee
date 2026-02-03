# Weekly Panel Regression Models

This folder contains R scripts for weekly panel regression analysis comparing customer groups.

## Scripts

- `regression_no_push_customers.R` - Panel regression analysis for customers who opted out of push notifications (push=0)
- `regression_with_two_groups.R` - Compares purchase behavior between push=0 and push=1 customer groups
- `regression_with_two_groups_customer_removed.R` - Same analysis using customer-specific removed products instead of store-level

## Usage

```bash
cd scripts/regression_analysis/weekly_models
Rscript regression_with_two_groups.R
```

## Output

Results are saved to `data/analysis_outputs/weekly_regression/`
