# Push Sensitivity Analysis

## Overview

This project analyzes how customers' self-disclosed privacy attitudes (opting out vs. in to push notifications) affect their purchase behavior and responsiveness to marketing pushes. This is a unique setting where:

- **push=0 group**: Customers who opted out of push notifications (privacy-conscious)
- **push=1 group**: Customers who opted in to push notifications

**Key Finding**: Counter-intuitively, push=0 members are MORE active, not less.

---

## Research Questions

### H1: Heterogeneous Intrinsic Preferences
Do push=0 and push=1 members have different baseline purchase behaviors BEFORE any push interventions?

### H2: Differential Push Sensitivity
Does the effect of pushes on wake-up probability differ between push=0 and push=1 groups?

---

## Folder Structure

```
push_sensitivity_analysis/
├── data/                           # Processed data files
│   └── analysis_data.parquet       # Main analysis dataset
├── scripts/                        # Analysis scripts
│   ├── 01_preprocess_data.py       # Data preprocessing
│   ├── 02_intrinsic_preferences.py # Pre-dormant behavior comparison
│   ├── 03_push_sensitivity.py      # DiD analysis
│   ├── 04_survival_analysis.py     # Competing risks survival analysis
│   └── 05_regression_analysis.R    # Fixed effects regression (R)
├── outputs/
│   ├── tables/                     # Result tables
│   ├── figures/                    # Visualization plots
│   └── logs/                       # Execution logs
└── README.md                       # This file
```

---

## Prerequisites

### Python Requirements
```bash
pip install pandas numpy scipy statsmodels matplotlib seaborn lifelines linearmodels
```

### R Requirements
```r
install.packages(c("data.table", "lfe", "glmnet", "sandwich", "lmtest"))
```

---

## Usage

### Step 1: Preprocess Data
```bash
cd scripts
python 01_preprocess_data.py
```
**Output**: `../data/analysis_data.parquet`

### Step 2: Intrinsic Preferences Analysis
```bash
python 02_intrinsic_preferences.py
```
**Output**: Pre-period customer metrics, group comparison tables, effect size plots

### Step 3: Push Sensitivity DiD Analysis
```bash
python 03_push_sensitivity.py
```
**Output**: DiD regression results, event study plots, heterogeneous effects

### Step 4: Survival Analysis
```bash
python 04_survival_analysis.py
```
**Output**: Cumulative incidence curves, Cox model results, hazard ratios

### Step 5: Fixed Effects Regression (R)
```bash
Rscript 05_regression_analysis.R
```
**Output**: Regression comparison tables, coefficient plots

---

## Analysis Details

### Script 1: `01_preprocess_data.py`

**Purpose**: Prepare analysis dataset from `combined_push_purchase_analysis.parquet`

**Key Steps**:
1. Load parquet file and `no_push_members.csv`
2. Assign `push_group` flag (0=privacy-conscious, 1=opt-in)
3. Identify first dormant period entry per customer
4. Create `pre` vs `post` period indicators
5. Calculate summary statistics

**Output Variables**:
- `push_group`: 0 or 1
- `period`: 'pre' or 'post'
- `is_post_period`: 0 or 1

---

### Script 2: `02_intrinsic_preferences.py`

**Purpose**: Compare pre-dormant behavior (before any pushes)

**Metrics Calculated**:

| Category | Metric | Description |
|----------|--------|-------------|
| Frequency | `initial_orders` | Total orders before first dormant |
| Frequency | `initial_order_freq` | Orders per week |
| Frequency | `initial_interpurchase_days` | Avg days between orders |
| Value | `initial_avg_order_value` | Mean order value |
| Value | `initial_avg_basket_size` | Mean items per order |
| Variety | `initial_unique_stores` | Count of unique stores visited |
| Discount | `initial_coupon_usage_rate` | % orders using coupons |
| Discount | `initial_avg_discount` | Mean discount rate |

**Statistical Tests**:
- Independent t-test (Welch's)
- Mann-Whitney U test
- FDR correction (Benjamini-Hochberg)
- Effect size (Cohen's d)

---

### Script 3: `03_push_sensitivity.py`

**Purpose**: DiD analysis of push effectiveness

**Models**:
1. **Basic DiD**: `wakeup ~ push_group`
2. **Adjusted DiD**: `wakeup ~ push_group + pre_order_freq + pre_avg_value`
3. **Push Intensity**: `wakeup ~ push_group * total_pushes`

**Outcomes**:
- `wakeup`: Binary indicator (1=wake-up during dormant period)
- `days_to_wakeup`: Days from dormant entry to purchase
- `wakeup_order_value`: Order value at wake-up

**Push Exposure Metrics**:
- `total_pushes`: Total pushes received in dormant period
- `push_intensity_first_7d`: Pushes in first 7 days of dormant
- `avg_push_discount`: Mean discount offered
- `trigger_diversity`: Count of unique trigger types

---

### Script 4: `04_survival_analysis.py`

**Purpose**: Competing risks survival analysis

**Events**:
- Event 1: Wake-up (purchase during dormant period)
- Event 2: Censoring (no purchase by end of observation)

**Models**:
1. **Cox PH Model 1**: Unadjusted (push_group only)
2. **Cox PH Model 2**: Adjusted for push intensity
3. **Cox PH Model 3**: Adjusted for intensity and discount
4. **Cox PH Model 4**: Interaction model (push_group × intensity)

**Visualizations**:
- Cumulative incidence curves by push_group
- Hazard ratio forest plot
- Sample size over time

---

### Script 5: `05_regression_analysis.R`

**Purpose**: High-dimensional fixed effects regression

**Models**:
1. **Model 1**: OLS unadjusted
2. **Model 2**: OLS with pre-period controls (robust SE)
3. **Model 3**: OLS with push intensity interaction
4. **Model 4**: OLS with push characteristics
5. **Model 5**: Logistic regression

**Fixed Effects**:
- Customer FE (controls for time-invariant customer characteristics)
- Week FE (controls for common time trends)
- Store FE (controls for store characteristics)

---

## Expected Outputs

### Tables (`outputs/tables/`)
1. `customer_pre_period_metrics.csv` - Customer-level pre-period metrics
2. `group_comparison_results.csv` - T-test results for all metrics
3. `summary_table.csv` - Formatted summary statistics
4. `did_dataset.csv` - DiD analysis dataset
5. `survival_dataset.csv` - Survival analysis dataset
6. `regression_comparison_table.csv` - Cross-model comparison

### Figures (`outputs/figures/`)
1. `pre_period_metrics_boxplot.png` - Box plots of key pre-period metrics
2. `effect_sizes_plot.png` - Effect sizes with significance markers
3. `event_study_plot.png` - Pre/post comparison by group
4. `cumulative_incidence_curves.png` - CIF by push_group
5. `hazard_ratio_forest_plot.png` - Cox model hazard ratios
6. `coefficient_plot.png` - Regression coefficients comparison

### Logs (`outputs/logs/`)
- `01_preprocess_data.log`
- `02_intrinsic_preferences.log`
- `03_push_sensitivity.log`
- `04_survival_analysis.log`
- `05_regression_analysis.log`

---

## Data Sources

1. **`../processed_data/combined_push_purchase_analysis.parquet`**
   - Main data file with push and purchase events
   - Columns: member_id, dt, data_source, dormant_period, days_since_purchase, etc.

2. **`../processed_data/no_push_members.csv`**
   - List of customers with push=0
   - Used to assign push_group flags

---

## Key Findings (from prior analysis)

| Metric | push=0 | push=1 | Difference |
|--------|--------|--------|------------|
| Purchases per member | 13.79 | 7.71 | **+79%** |
| Wake-up rate | 73.79% | 62.03% | **+11.8 pp** |
| Days to wake-up | 86.49 | 92.37 | **-5.9 days** |
| Inter-purchase days | 16.42 | 18.63 | **-2.2 days** |

**Interpretation**: Privacy-conscious customers (push=0) are MORE engaged, not less.

---

## Troubleshooting

### Memory Issues
The parquet file is large (~64M records). If you encounter memory issues:
1. Use `chunksize` parameter in `pd.read_parquet()`
2. Filter data early (e.g., by member_id or date range)
3. Use `dask` for out-of-core computation

### Package Installation
If `lifelines` fails to install:
```bash
conda install -c conda-forge lifelines
```

If R packages fail to install:
```r
install.packages("lfe", repos = "http://R-Forge.R-project.org")
```

---

## Citation

If you use this code for research, please cite:
```
Push Sensitivity Analysis (2026). https://github.com/yourusername/push-sensitivity
```

---

## Contact

For questions or issues, please open an issue on GitHub or contact [your email].

---

*Last updated: 2026-02-02*
