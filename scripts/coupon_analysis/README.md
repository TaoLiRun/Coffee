# Coupon and Discount Analysis

This folder contains scripts for analyzing coupon effects and discount impacts on customer behavior.

## Scripts

- `process_order_commodity.py` - Processes order commodity data to analyze product demand patterns at the department and product level
- `analyze_consumer.py` - Analyzes consumer product exploration behavior and immediate repurchase rates
- `process_dept.py` - Processes department-level weekly demand data and visualizes it as daily demand
- `removal_impact.py` - Analyzes the impact of removing a product from a store's product line
- `visualize.py` - Provides visualization functions for demand analysis
- `wait.r` - Analyzes whether purchases with coupons decrease consumers' tendency to purchase without coupons in the future

## Usage

```bash
cd scripts/coupon_analysis
python process_order_commodity.py
Rscript wait.r
```
