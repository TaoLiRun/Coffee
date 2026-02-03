# Model-Free Folder Organization Guide

This document describes the reorganized structure of the `model-free` folder, which contains analysis scripts and data for studying customer purchase behavior, push notifications, and coupon effects.

## 📁 New Folder Structure

```
model-free/
├── data/                           # All data files organized by processing stage
│   ├── raw/                        # Raw data files (to be populated)
│   ├── processed/                  # Processed/cleaned data files (10 files)
│   │   ├── combined_data_1000.csv
│   │   ├── combined_data_10.csv
│   │   ├── combined_push_purchase_analysis.parquet
│   │   ├── customer_history.csv
│   │   ├── no_push_members.csv
│   │   ├── order_commodity_result_processed.csv
│   │   ├── order_member_no_push.csv
│   │   ├── policy_dt.csv
│   │   ├── product_mapping.csv
│   │   └── summary_statistics.csv
│   ├── intermediate/               # Intermediate data files
│   └── analysis_outputs/           # Analysis results (28 files)
│       ├── weekly_regression/      # Panel regression outputs (11 files)
│       ├── push_sensitivity/       # DiD & survival analysis (17 files)
│       └── basic_distribution/     # Basic analysis outputs
│
├── scripts/                        # All analysis code organized by task
│   ├── push_analysis/              # Push notification analysis scripts
│   │   ├── basic_distribution/     # Basic push and purchase distributions
│   │   │   ├── combine_push_buy.py
│   │   │   ├── compare_customers_with_and_without_push.py
│   │   │   ├── select_no_push_customers.py
│   │   │   └── run.sh
│   │   ├── sensitivity_analysis/   # Push sensitivity analysis project
│   │   │   └── push_sensitivity_analysis/
│   │   │       ├── scripts/
│   │   │       │   ├── 01_preprocess_data.py
│   │   │       │   ├── 02_intrinsic_preferences.py
│   │   │       │   ├── 03_push_sensitivity.py
│   │   │       │   ├── 04_survival_analysis.py
│   │   │       │   └── 05_regression_analysis.R
│   │   │       ├── outputs/
│   │   │       │   ├── tables/
│   │   │       │   ├── figures/
│   │   │       │   └── logs/
│   │   │       └── README.md
│   │   ├── combine_push_order.r    # Combines push and order data
│   │   ├── policy.r                # Processes push policy data
│   │   └── read_combined.r         # Analyzes combined push-purchase data
│   │
│   ├── coupon_analysis/            # Coupon and discount effect analysis
│   │   ├── analyze_consumer.py     # Consumer product exploration analysis
│   │   ├── process_dept.py         # Department-level demand processing
│   │   ├── process_order_commodity.py  # Order commodity processing
│   │   ├── removal_impact.py       # Product removal impact analysis
│   │   ├── visualize.py            # Visualization functions
│   │   └── wait.r                  # Coupon effect on future purchases
│   │
│   ├── regression_analysis/        # Regression models and statistical analysis
│   │   └── weekly_models/          # Weekly panel regression models
│   │       ├── regression_no_push_customers.R
│   │       ├── regression_with_two_groups.R
│   │       └── regression_with_two_groups_customer_removed.R
│   │
│   └── exploratory_notebooks/      # Jupyter notebooks for exploration
│       ├── order.ipynb             # Order data exploration
│       ├── product.ipynb           # Product data exploration
│       ├── push.ipynb              # Push notification exploration
│       └── push_buy.ipynb          # Push-purchase relationship exploration
│
├── outputs/                        # All analysis outputs
│   ├── plots/                      # All visualizations
│   │   ├── basic_distribution/
│   │   ├── coupon_analysis/
│   │   └── (other plot subfolders)
│   ├── results/                    # Analysis results and tables
│   └── logs/                       # Execution logs
│
└── README.md                       # Main project README
```

## 📊 Data Organization

### data/processed/
Contains cleaned and processed datasets ready for analysis (10 files):

- **combined_data_1000.csv / combined_data_10.csv**: Combined push and purchase data for sampled customers
- **combined_push_purchase_analysis.parquet**: Unified push-purchase panel with dormancy flags
- **customer_history.csv**: Customer transaction history
- **no_push_members.csv**: List of customers who opted out of push notifications (push=0)
- **order_commodity_result_processed.csv**: Processed order commodity data
- **order_member_no_push.csv**: Orders from customers without push notifications
- **policy_dt.csv**: Aggregated push policy data by date
- **product_mapping.csv**: Product ID to name mappings
- **summary_statistics.csv**: Statistical summaries

### data/analysis_outputs/
Contains results from running analyses (28 files):

#### weekly_regression/ (11 files)
- **analysis_dataset.csv / analysis_dataset_customer_removed.csv**: Main analysis datasets
- **customer_week_panel.csv / customer_week_panel_customer_removed.csv**: Customer-week level panels
- **product_lifecycle_detailed.csv / product_lifecycle_detailed_customer_removed.csv**: Product lifecycle data
- **product_panel.csv / product_panel_customer_removed.csv**: Product-level panels
- **store_week_panel_complete.csv / store_week_panel_complete_customer_removed.csv**: Store-week panels
- **customer_removed_panel.csv**: Customer-specific removed products panel

#### push_sensitivity/ (17 files)
- **analysis_data.parquet**: Preprocessed data for sensitivity analysis
- **cox_model*_summary.csv**: Cox regression model summaries
- **customer_pre_period_metrics.csv**: Pre-period customer metrics
- **did_dataset.csv**: Difference-in-differences dataset
- **group_comparison_results.csv**: Statistical comparison between groups
- **regression_comparison_table.csv**: Regression model comparisons
- **summary_statistics.csv / summary_table.csv**: Summary statistics
- **survival_dataset.csv / survival_summary_statistics.csv**: Survival analysis data

## 🔬 Script Organization

### 1. Push Analysis (`scripts/push_analysis/`)

#### Basic Distribution Scripts
- **combine_push_buy.py**: Builds unified push-purchase panel with features like customer dormancy and days since purchase
- **compare_customers_with_and_without_push.py**: Statistical comparison between push opt-in (push=1) and opt-out (push=0) customers
- **select_no_push_customers.py**: Filters and analyzes customers who opted out of push notifications
- **combine_push_order.r**: Combines push notification data with order data for sampled consumers
- **policy.r**: Processes and aggregates push notification policy data
- **read_combined.r**: Analyzes push timing patterns (how long customers wait before receiving a push)

#### Sensitivity Analysis (`sensitivity_analysis/push_sensitivity_analysis/`)
Complete pipeline for analyzing differential push sensitivity:
- **01_preprocess_data.py**: Prepares analysis dataset with dormancy indicators
- **02_intrinsic_preferences.py**: Tests H1 - compares pre-dormant behavior between groups
- **03_push_sensitivity.py**: Tests H2 - DiD analysis of push effectiveness
- **04_survival_analysis.py**: Competing risks survival analysis (wake-up vs churn)
- **05_regression_analysis.R**: High-dimensional fixed effects regression

### 2. Coupon Analysis (`scripts/coupon_analysis/`)

- **analyze_consumer.py**: Analyzes consumer product exploration and repurchase rates
- **process_dept.py**: Processes department-level weekly demand data
- **process_order_commodity.py**: Processes order commodity data for demand analysis
- **removal_impact.py**: Analyzes impact of product removal on store demand
- **visualize.py**: Provides visualization functions for demand analysis
- **wait.r**: Examines whether coupon usage decreases future non-coupon purchases

### 3. Regression Analysis (`scripts/regression_analysis/weekly_models/`)

- **regression_no_push_customers.R**: Panel regression for customers without push notifications
- **regression_with_two_groups.R**: Compares push=0 vs push=1 customer groups
- **regression_with_two_groups_customer_removed.R**: Same analysis using customer-specific removed products

### 4. Exploratory Notebooks (`scripts/exploratory_notebooks/`)

- **order.ipynb**: Order data exploration (patterns, distributions, temporal trends)
- **product.ipynb**: Product analysis (popularity, categories, lifecycle)
- **push.ipynb**: Push notification data exploration (timing, frequency)
- **push_buy.ipynb**: Push-purchase relationship exploration

## 🎯 Key Research Questions

1. **Push Notification Effects**
   - How do push notifications affect customer purchase behavior?
   - Do privacy-conscious customers (push=0) respond differently to marketing?
   - What is the optimal timing for push notifications?

2. **Coupon/Discount Effects**
   - Do coupons reduce future non-discounted purchases?
   - How do discounts affect customer lifetime value?

3. **Product Assortment**
   - How does product removal affect store demand?
   - What drives product exploration behavior?

## 🚀 Getting Started

### Running Push Sensitivity Analysis
```bash
cd scripts/push_analysis/sensitivity_analysis/push_sensitivity_analysis/scripts
python 01_preprocess_data.py
python 02_intrinsic_preferences.py
python 03_push_sensitivity.py
python 04_survival_analysis.py
Rscript 05_regression_analysis.R
```

### Running Coupon Analysis
```bash
cd scripts/coupon_analysis
python process_order_commodity.py
```

### Running Regression Models
```bash
cd scripts/regression_analysis/weekly_models
Rscript regression_with_two_groups.R
```

## 📝 Notes

- All scripts now have descriptive comments at the beginning explaining their purpose
- File paths in scripts have been updated to work with the new structure
- Raw data should be placed in `data/raw/` (currently points to `../../data/data1031/`)
- All outputs are centralized in the `outputs/` folder
- The original folder structure is preserved for reference

## 🔄 Migration from Old Structure

The old structure had:
- Data files scattered in root and `processed_data/`
- Scripts mixed in root and various subfolders
- Outputs in multiple nested locations

The new structure:
- Centralizes all data in `data/` with clear processing stages
- Organizes scripts hierarchically by research task
- Consolidates outputs in a single `outputs/` folder
- Adds clear documentation to all code files

---

**Last Updated**: February 3, 2026
