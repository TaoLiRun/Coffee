# Quick Reference - Model-Free Analysis

## 📂 Where to Find Things

### Data Files
- **Processed data**: `data/processed/`
- **Raw data**: Reference to `../../data/data1031/`
- **Analysis outputs**: `outputs/data/`

### Code Files by Task

#### Push Notification Analysis
- **Basic analysis**: `scripts/push_analysis/basic_distribution/`
- **Sensitivity study**: `scripts/push_analysis/sensitivity_analysis/push_sensitivity_analysis/`
- **Push-order combination**: `scripts/push_analysis/combine_push_order.r`

#### Coupon/Discount Analysis
- **All coupon scripts**: `scripts/coupon_analysis/`
- **Main entry point**: `process_order_commodity.py`

#### Regression Models
- **Weekly panel models**: `scripts/regression_analysis/weekly_models/`

#### Exploratory Analysis
- **Notebooks**: `scripts/exploratory_notebooks/`

### Output Files
- **Plots**: `outputs/plots/`
- **Results tables**: `outputs/results/`
- **Logs**: `outputs/logs/`

## 🔑 Key Scripts and Their Purpose

| Script | Location | Purpose |
|--------|----------|---------|
| `combine_push_buy.py` | push_analysis/basic_distribution/ | Build unified push-purchase panel |
| `compare_customers_with_and_without_push.py` | push_analysis/basic_distribution/ | Statistical comparison of push opt-in/out |
| `01_preprocess_data.py` | push_analysis/sensitivity_analysis/.../scripts/ | Preprocess for sensitivity analysis |
| `process_order_commodity.py` | coupon_analysis/ | Process order commodity data |
| `regression_with_two_groups.R` | regression_analysis/weekly_models/ | Panel regression comparing groups |

## 🏃 Quick Start Commands

### Sensitivity Analysis (Full Pipeline)
```bash
cd scripts/push_analysis/sensitivity_analysis/push_sensitivity_analysis/scripts
for script in 01_preprocess_data.py 02_intrinsic_preferences.py 03_push_sensitivity.py 04_survival_analysis.py; do
    python $script
done
Rscript 05_regression_analysis.R
```

### Basic Push Analysis
```bash
cd scripts/push_analysis/basic_distribution
python combine_push_buy.py
python compare_customers_with_and_without_push.py
```

### Coupon Analysis
```bash
cd scripts/coupon_analysis
python process_order_commodity.py
Rscript wait.r
```

### Regression Analysis
```bash
cd scripts/regression_analysis/weekly_models
Rscript regression_with_two_groups.R
```

## 📊 Data Flow

```
Raw Data (../../data/data1031/)
    ↓
Processing Scripts (scripts/*/process_*.py)
    ↓
Processed Data (data/processed/)
    ↓
Analysis Scripts (scripts/*/)
    ↓
Outputs (outputs/plots/, outputs/results/)
```

## 🔍 Finding Specific Analyses

- **Customer dormancy**: `push_analysis/sensitivity_analysis/`
- **Push timing**: `push_analysis/read_combined.r`
- **Coupon effects**: `coupon_analysis/wait.r`
- **Product removal**: `coupon_analysis/removal_impact.py`
- **Consumer exploration**: `coupon_analysis/analyze_consumer.py`
- **Store demand**: `coupon_analysis/process_dept.py`

## 📝 File Naming Conventions

- **Python scripts**: `snake_case.py` - Processing and analysis
- **R scripts**: `snake_case.R` or `snake_case.r` - Statistical models
- **Notebooks**: `descriptive_name.ipynb` - Exploratory analysis
- **Data files**: `descriptive_name.csv/parquet` - Processed data
- **Output plots**: `descriptive_name.pdf/png` - Visualizations

## 💡 Tips

1. **All scripts have descriptions**: Check the first few lines of each file
2. **Logs are centralized**: Check `outputs/logs/` for execution logs
3. **Data is organized by stage**: raw → intermediate → processed
4. **Scripts are organized by task**: push_analysis, coupon_analysis, regression_analysis
5. **Use ORGANIZATION_GUIDE.md**: For detailed documentation

---
For detailed information, see [ORGANIZATION_GUIDE.md](ORGANIZATION_GUIDE.md)
