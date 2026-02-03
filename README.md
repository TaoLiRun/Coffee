# Coffee Model-Free Analysis

A comprehensive analysis of customer purchase behavior, push notification effects, and coupon impacts in a coffee retail business.

**🔗 GitHub Repository:** https://github.com/TaoLiRun/Coffee.git

## 📁 Project Structure

```
model-free/
├── data/                    # All data files (excluded from git)
│   ├── processed/           # Cleaned/processed data (10 files)
│   └── intermediate/        # Intermediate analysis datasets
│       └── analysis_data.parquet  # Preprocessed push sensitivity data
├── scripts/                 # All analysis code
│   ├── push_analysis/       # Push notification analysis
│   ├── coupon_analysis/     # Coupon and discount effects
│   ├── regression_analysis/ # Statistical models
│   ├── exploratory_notebooks/ # Jupyter notebooks
│   └── archive_neglect_coupon/ # Archived coupon analysis
└── plots/                   # Visualization outputs
```

## 🎯 Research Questions

1. **Push Notification Effects**: How do push notifications affect customer purchase behavior?
2. **Privacy Preferences**: Do privacy-conscious customers (push=0) respond differently to marketing?
3. **Coupon Effects**: Do coupons reduce future non-discounted purchases?
4. **Product Assortment**: How does product removal affect store demand?

## 🚀 Quick Start

### Push Sensitivity Analysis
```bash
cd scripts/push_analysis/sensitivity_analysis/push_sensitivity_analysis/scripts
python 01_preprocess_data.py
python 02_intrinsic_preferences.py
python 03_push_sensitivity.py
python 04_survival_analysis.py
Rscript 05_regression_analysis.R
```

### Coupon Analysis
```bash
cd scripts/coupon_analysis
python process_order_commodity.py
Rscript wait.r
```

### Weekly Regression Models
```bash
cd scripts/regression_analysis/weekly_models
Rscript regression_with_two_groups.R
```

## 📊 Key Scripts

### Push Analysis (`scripts/push_analysis/`)
- `combine_push_order.r` - Combines push and order data for analysis
- `policy.r` - Processes push notification policy data
- `read_combined.r` - Analyzes push timing patterns
- `basic_distribution/*.py` - Basic push-purchase distribution analysis
- `sensitivity_analysis/` - Complete DiD and survival analysis pipeline

### Coupon Analysis (`scripts/coupon_analysis/`)
- `process_order_commodity.py` - Processes order commodity data
- `analyze_consumer.py` - Analyzes consumer exploration behavior
- `wait.r` - Studies coupon effects on future purchases
- `visualize.py` - Visualization functions

### Regression Analysis (`scripts/regression_analysis/weekly_models/`)
- `regression_no_push_customers.R` - Analysis for push=0 customers
- `regression_with_two_groups.R` - Compares push=0 vs push=1 groups
- `regression_with_two_groups_customer_removed.R` - Customer-specific removed products

## 📝 Data Organization

### Processed Data (`data/processed/`)
- `combined_push_purchase_analysis.parquet` - Main analysis dataset
- `order_commodity_result_processed.csv` - Processed order data
- `no_push_members.csv` - Customers who opted out of push notifications
- `product_mapping.csv` - Product ID mappings
- And more...

### Intermediate Data (`data/intermediate/`)
- `analysis_data.parquet` - Preprocessed dataset for push sensitivity analysis with dormant period indicators

## 🔧 Setup

### Prerequisites
- Python 3.x with: pandas, numpy, scipy, statsmodels, matplotlib, seaborn, lifelines
- R with: data.table, lubridate, lfe, ggplot2

### Data Note
The `data/` folder is excluded from git (see `.gitignore`). Obtain data files separately and place in appropriate subfolders.

## 📋 Project History

**February 3, 2026 - Complete Reorganization:**
- ✅ Hierarchical folder structure created
- ✅ Data consolidated in `data/` with subfolders by type
- ✅ Scripts organized by research task
- ✅ All code files documented with descriptions
- ✅ Duplicates removed and cleaned up
- ✅ Pushed to GitHub with proper .gitignore
- ✅ Archive folders preserved for reference

## �� Key Findings

### H1: Heterogeneous Intrinsic Preferences
Counter-intuitively, push=0 members (privacy-conscious) are MORE active purchasers than push=1 members, even before receiving any pushes.

### H2: Differential Push Sensitivity
Push notifications have differential effects on wake-up probability between the two groups, with nuanced patterns in timing and intensity.

## 🤝 Contributing

This is a research project. To contribute:
1. Clone the repository
2. Create a feature branch
3. Make your changes with clear commit messages
4. Submit a pull request

## 📄 License

Research project - please contact the authors for usage permissions.

## 📧 Contact

For questions about this analysis, please open an issue on GitHub.

---

**Repository:** https://github.com/TaoLiRun/Coffee.git  
**Last Updated:** February 3, 2026
