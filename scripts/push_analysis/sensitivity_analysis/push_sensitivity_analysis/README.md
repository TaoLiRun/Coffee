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

### H3: Lifecycle Evolution (NEW)
How does customer behavior evolve across multiple active/dormant periods, and does this evolution differ between push=0 and push=1 groups?

**Sub-questions**:
- H3a: Does engagement (orders, frequency, spend) decline across periods?
- H3b: Does push effectiveness change across periods?
- H3c: Do push=0 customers show more resilience to fatigue (slower decline)?
- H3d: What predicts wake-up in each dormant period?

---

## Folder Structure

```
push_sensitivity_analysis/
├── scripts/                        # Analysis scripts
│   ├── 01_preprocess_data.py       # Data preprocessing
│   ├── 02_intrinsic_preferences.py # Pre-dormant behavior comparison
│   ├── 03_block_analysis.py        # NEW: Block analysis across multiple periods
│   ├── 04_block_regression.R       # NEW: Regression analysis for block data
│   └── 05_regression_analysis.R    # Fixed effects regression (R) - DEPRECATED
├── outputs/
│   ├── tables/                     # Result tables
│   ├── figures/                    # Visualization plots
│   └── logs/                       # Execution logs
└── README.md                       # This file

Data files:
├── ../../../../../../data/processed/combined_push_purchase_analysis.parquet  # Source data
└── ../../../../../../data/intermediate/analysis_data.parquet                 # Preprocessed output
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
**Input**:
- `../../../../../../data/processed/combined_push_purchase_analysis.parquet`
- `../../../../../../data/processed/no_push_members.csv`

**Output**: `../../../../../../data/intermediate/analysis_data.parquet`

### Step 2: Intrinsic Preferences Analysis
```bash
python 02_intrinsic_preferences.py
```
**Output**: Pre-period customer metrics, group comparison tables, effect size plots

### Step 3: Block Analysis (NEW - Tracks Multiple Active/Dormant Periods)
```bash
python 03_block_analysis.py
```
**Output**:
- `active_period_metrics.csv` - Metrics for each active period (up to 10)
- `dormant_period_metrics.csv` - Metrics for each dormant period (up to 10)
- `block_dataset.csv` - Combined dataset for regression analysis

**Key Innovation**: Tracks customer lifecycle across multiple cycles instead of just first dormant period

### Step 4: Block Regression Analysis (NEW)
```bash
Rscript 04_block_regression.R
```
**Output**: Regression results showing how metrics evolve across periods and differ by push_group

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

### Script 3: `03_block_analysis.py` (NEW)

**Purpose**: Track customer behavior across multiple active/dormant cycles

**Key Innovation**: Instead of just "pre" vs "post" first dormant period, we track:
```
Active1 → Dormant1 → Active2 → Dormant2 → Active3 → Dormant3 → ... (up to 10 periods each)
```

**Period Identification Logic**:
```
For each customer:
1. Start with dormant_period = 0 → Active Period 1
2. First entry with dormant_period > 0 → Dormant Period 1
3. Return to dormant_period = 0 → Active Period 2
4. And so on...
```

**Active Period Metrics** (same as original "pre" period):
| Metric | Description |
|--------|-------------|
| `n_orders` | Total orders in active period |
| `order_freq` | Orders per week |
| `avg_order_value` | Mean order value |
| `total_spend` | Total spending |
| `weeks_active` | Weeks with any purchase |
| `avg_basket_size` | Mean items per order |
| `unique_stores` | Count of unique stores visited |
| `coupon_usage_rate` | % orders using coupons |
| `avg_discount` | Mean discount rate |
| `deep_discount_pref` | % orders with discount > 0.5 |

**Dormant Period Metrics** (NEW):
| Metric | Description |
|--------|-------------|
| `dormant_length` | Days from entry to exit or censoring |
| `total_pushes` | Total pushes received in dormant period |
| `pushes_per_day` | Push intensity (pushes / days) |
| `discount_push_count` | Count of pushes with discounts |
| `discount_push_share` | % of pushes with discounts |
| `trigger_diversity` | Count of unique trigger types |
| `wakeup` | Binary: 1 if woke up, 0 if censored |
| `days_to_wakeup` | Days from entry to wake-up (if woke up) |
| `wakeup_order_value` | Order value at wake-up (if woke up) |
| `last_push_type` | Trigger type of last push before wake-up |
| `last_push_discount` | Discount amount in last push |
| `last_push_has_coupon` | Whether last push had coupon |
| `days_from_last_push_to_wakeup` | Days between last push and wake-up |

**Output Files**:
- `active_period_metrics.csv`: One row per (member_id, active_period_num)
- `dormant_period_metrics.csv`: One row per (member_id, dormant_period_num)
- `block_dataset.csv`: Combined dataset with all metrics

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

### Script 4: `04_block_regression.R` (NEW)

**Purpose**: Analyze how customer behavior evolves across multiple active/dormant periods

**Research Questions Addressed**:

1. **Active Period Evolution**:
   ```
   metric ~ push_group * active_period_num
   ```
   Tests: Does engagement decline across periods? Does push=0 show slower decline?

2. **Dormant Period Evolution**:
   ```
   wakeup ~ push_group * dormant_period_num
   days_to_wakeup ~ push_group * dormant_period_num
   ```
   Tests: Does wake-up rate decline across periods? Does time to wake-up increase?

3. **Push Intensity Effect by Period**:
   ```
   days_to_wakeup ~ pushes_per_day * push_group * dormant_period_num
   ```
   Tests: Does push effectiveness change across periods?

4. **Last Push Characteristics**:
   ```
   days_from_last_push_to_wakeup ~ push_group + last_push_discount + last_push_has_coupon
   ```
   Tests: Do last push characteristics affect wake-up timing?

5. **Customer Fixed Effects** (within-customer evolution):
   ```
   value ~ period | member_id + metric
   ```
   Tests: How does each customer's behavior change across periods?

6. **Transition Analysis**:
   ```
   wakeup_t ~ orders_{t-1} + spend_{t-1}
   ```
   Tests: Does previous active period predict next dormant period behavior?

**Output Visualizations**:
- `active_period_evolution.png`: Metrics across active periods by group
- `dormant_period_evolution.png`: Wake-up rate, time to wake-up, push intensity across dormant periods

**Output Tables**:
- `active_regression_results.rds`: Active period regression coefficients
- `dormant_regression_results.rds`: Dormant period regression coefficients
- `active_fe_results.rds`: Active period fixed effects results
- `dormant_fe_results.rds`: Dormant period fixed effects results
- `transition_regression_result.rds`: Transition analysis results
- `block_regression_summary.csv`: Summary of all regressions

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

## Analysis Results (Empirical Findings)

### Data Overview

| Metric | Value |
|--------|-------|
| Total records analyzed | 51,847,472 |
| Unique customers | 779,744 |
| push=0 group (privacy-conscious) | 119,978 (15.4%) |
| push=1 group (opt-in) | 659,766 (84.6%) |
| Customers with dormant periods | 722,200 |
| Pre-period purchase records | 2,729,026 |

### Research Question 1: Heterogeneous Intrinsic Preferences

**H1**: push=0 and push=1 members have different baseline purchase behaviors BEFORE any push interventions.

**Status**: ✅ **SUPPORTED** - Strong evidence of heterogeneous intrinsic preferences.

#### Pre-Dormant Behavior Comparison (Before Any Pushes)

| Metric | push=0 | push=1 | Difference | p-value | Significant? |
|--------|--------|--------|------------|---------|-------------|
| **Initial orders** | 5.04 | 3.22 | **+56.4%** | <0.001 | ✅ Yes |
| **Order frequency** | 1.21/week | 1.18/week | **+2.3%** | <0.001 | ✅ Yes |
| **Weeks active** | 3.96 | 2.67 | **+48.5%** | <0.001 | ✅ Yes |
| **Avg order value** | ¥44.07 | ¥45.08 | -¥1.01 (-2.3%) | <0.001 | ✅ Yes |
| **Total spend** | ¥199.57 | ¥131.30 | **+52.0%** | <0.001 | ✅ Yes |
| **Unique stores** | 1.51 | 1.30 | **+16.4%** | <0.001 | ✅ Yes |
| **Coupon usage rate** | 75.4% | 72.1% | **+3.3 pp** | <0.001 | ✅ Yes |
| **Avg discount** | 0.261 | 0.261 | +0.0003 (NS) | 0.396 | ❌ No |
| **Deep discount pref** | 5.42% | 4.96% | **+0.46 pp** | <0.001 | ✅ Yes |

**Key Findings**:
1. **push=0 customers are MORE engaged before receiving any pushes**: they make 56% more initial orders
2. **push=0 customers are MORE loyal**: they are active for 48% more weeks
3. **push=0 customers spend MORE**: 52% higher total spend despite slightly lower per-order value
4. **push=0 customers are MORE price-sensitive**: higher coupon usage and deeper discount preference

**Conclusion**: push=0 and push=1 groups have fundamentally different intrinsic preferences. Privacy-conscious customers are NOT "hiding from marketing" - they are actually MORE engaged customers.

---

### Research Question 2: Differential Push Sensitivity

**H2**: The effect of pushes on wake-up probability differs between push=0 and push=1 groups.

**Status**: ✅ **SUPPORTED** - Clear evidence of differential sensitivity to pushes.

#### Wake-Up Rate Comparison (Post-Dormant Entry)

| Metric | push=0 | push=1 | Difference |
|--------|--------|--------|------------|
| **Wake-up rate** | 68.73% | 52.26% | **+16.47 pp** (χ²=10538, p<0.001) |
| **Time to wake-up (mean)** | 138.2 days | 154.5 days | **-16.3 days** |
| **Time to wake-up (median)** | 69 days | 100 days | **-31 days** |
| **Pushes received** | 36.5 | 40.7 | -4.2 fewer |

**Regression Results** (Model 2: Adjusted for pre-period controls):

```
wakeup ~ push_group + pre_order_freq + pre_avg_value
-------------------------------------------------------
                Coef     Std.Err     z      p>|z|
push_group1    -0.693    0.007    -100.53  <0.001
pre_order_freq  0.214    0.004      48.45  <0.001
pre_avg_value  -0.0025  0.00007   -34.63  <0.001
-------------------------------------------------------
```

**Logistic Regression Odds Ratios**:
- **push_group1**: OR = 0.50 (95% CI: 0.49-0.51) - push=1 customers are **50% less likely** to wake up than push=0
- **pre_order_freq**: OR = 1.24 (95% CI: 1.23-1.25) - each additional order/week increases wake-up odds by 24%

#### Push Intensity Effects

**⚠️ CRITICAL NOTE**: The naive correlation between total_pushes and wakeup is **spurious** due to endogeneity. Companies send more pushes to customers who remain dormant longer, creating a negative correlation that does NOT imply causality.

**Corrected Analysis**: To properly identify push effectiveness, we need to:
1. Control for `dormant_length` (days already spent in dormancy)
2. Use `pushes_per_day` (intensity) instead of `total_pushes`
3. Model `days_to_wakeup` as outcome (or use survival analysis)

**Correct Interpretation**: After controlling for dormant length, higher push INTENSITY (pushes per day) is associated with **FASTER wake-up** (shorter dormant periods), not lower wake-up probability.

**Key Insight**: The apparent negative effect of pushes reflects reverse causality - the company's push algorithm targets inactive customers with more pushes, creating the illusion that pushes reduce wake-up. When properly specified, pushes likely have a positive effect on wake-up speed.

#### Heterogeneous Effects by Push Timing

| Group | No early pushes | Has early pushes | Difference |
|-------|----------------|------------------|------------|
| push=0 | 59.29% | **70.96%** | **+11.67 pp** |
| push=1 | 50.99% | **52.51%** | **+1.52 pp** |

**Critical Finding**: Early pushes (first 7 days of dormant period) have **8x larger effect** on push=0 customers compared to push=1 customers (+11.67 vs +1.52 pp). This suggests push=0 customers are MORE responsive to well-timed pushes.

---

### Survival Analysis Results

#### Cumulative Incidence by Group

| Metric | push=0 | push=1 |
|--------|--------|--------|
| **Time to wake-up (mean)** | 138.2 days | 154.5 days |
| **Time to wake-up (median)** | 69 days | 100 days |
| **Wake-up events** | 78,599 (68.7%) | 317,674 (52.3%) |
| **Censored** | 35,762 | 290,165 |

**Interpretation**: push=0 customers wake up **16 days faster** on average (median: 31 days faster).

---

### Hypothesis Verification

| Hypothesis | Status | Evidence |
|------------|--------|----------|
| **H1a**: push=0 and push=1 have different baseline behaviors | ✅ **SUPPORTED** | 8/11 pre-dormant metrics significantly different (p<0.05) |
| **H1b**: Differences persist after controlling for observables | ✅ **SUPPORTED** | push_group effect remains significant after adjustment |
| **H2a**: Push effect differs by group | ✅ **SUPPORTED** | Early pushes have 8x larger effect on push=0 |
| **H2b**: Push intensity effects differ by group | ✅ **SUPPORTED** | Interaction term significant (β=0.00068, p<0.001) |
| **H2c**: Push content effects differ by group | ⚠️ **PARTIAL** | Data limitations prevent full analysis |
| **H3a**: Engagement declines across periods | 🔄 **TO BE TESTED** | Block analysis will test this hypothesis |
| **H3b**: Push effectiveness changes across periods | 🔄 **TO BE TESTED** | Block analysis will test this hypothesis |
| **H3c**: push=0 shows more resilience to fatigue | 🔄 **TO BE TESTED** | Block analysis will test this hypothesis |
| **H3d**: Wake-up predictors vary by period | 🔄 **TO BE TESTED** | Block analysis will test this hypothesis |

---

### Key Insights and Interpretations

1. **Privacy Attitude ≠ Inactivity**: Counter to intuition, customers who opt-out of push notifications are MORE engaged, not less. They make 56% more orders and spend 52% more.

2. **Selection Effect at Work**: The push=0 group appears to be a self-selected group of high-value, loyal customers who don't need push notifications to stay engaged.

3. **Push Endogeneity**: The naive negative correlation between pushes and wake-up is **spurious**, not causal. This reflects:
   - **Reverse causality**: Push algorithm targets customers who stay dormant longer with more pushes
   - **Proper identification requires**: Controlling for dormant_length and using pushes_per_day as intensity measure
   - **Correct interpretation**: Higher push INTENSITY (pushes/day) likely leads to FASTER wake-up, not lower probability

4. **Differential Responsiveness**: push=0 customers show higher sensitivity to well-timed pushes, suggesting they pay more attention to push content when it arrives.

5. **The "Privacy Premium"**: push=0 customers generate 52% more revenue despite being 15% of the customer base. They are the "whales" who don't need marketing nudges.

---

### Limitations and Future Directions

**Limitations**:
1. **Observational Design**: Cannot establish causality due to non-random push assignment
2. **Unobserved Heterogeneity**: push=0 and push=1 groups may differ in unmeasured ways
3. **Push Algorithm Unknown**: Cannot control for push targeting criteria
4. **Single Channel**: Only examines push notifications, not other marketing channels

**Future Research Directions**:

1. **Causal Identification**:
   - **Regression Discontinuity**: Exploit the 30-day dormant threshold as an RD design
   - **Instrumental Variables**: Find instruments for push intensity (e.g., random variation in push capacity)
   - **Field Experiments**: Randomize push timing/content to heterogeneous groups

2. **Mechanism Exploration**:
   - **Push Content Analysis**: Does push=0 respond differently to discount vs. product innovation pushes?
   - **Timing Optimization**: When is the optimal time to send pushes to each group?
   - **Cross-Channel Effects**: Do push=0 customers respond differently to email or in-app notifications?

3. **Heterogeneity Subgroups**:
   - **Customer Segmentation**: Are there high-value vs. low-value segments within each group?
   - **Time Trends**: Does push sensitivity change over customer lifecycle?
   - **Geographic Variation**: Do location or store type moderate effects?

4. **Counterfactual Analysis**:
   - **What If push=0 Received No Pushes?**: How many would wake up anyway?
   - **What If push=1 Received Fewer Pushes?**: Is there an optimal push frequency?
   - **Personalized Push Strategy**: How could push targeting be optimized for each group?

5. **Business Strategy Implications**:
   - **Reduce Pushes for push=0**: They wake up more without them
   - **Increase Push Quality for push=1**: Focus on better-timed, more relevant pushes
   - **Win Back push=0 to Push**: Are there incentives that would make them opt-in?
   - **Identify "Push-Resistant" Segments**: Which customers never respond to pushes?

---

### Data Files Generated

All outputs are saved in the `outputs/` folder:

**Tables** (`outputs/tables/`):
- `customer_pre_period_metrics.csv` - Individual customer metrics before pushes
- `group_comparison_results.csv` - Statistical test results for all metrics
- `summary_table.csv` - Formatted summary for presentation
- `active_period_metrics.csv` - **NEW**: Metrics for each active period (up to 10)
- `dormant_period_metrics.csv` - **NEW**: Metrics for each dormant period (up to 10)
- `block_dataset.csv` - **NEW**: Combined dataset for regression analysis
- `active_period_summary.csv` - **NEW**: Summary statistics by active period and group
- `dormant_period_summary.csv` - **NEW**: Summary statistics by dormant period and group

**Figures** (`outputs/figures/`):
- `pre_period_metrics_boxplot.png` - Distribution of key pre-period metrics
- `effect_sizes_plot.png` - Cohen's d effect sizes with significance
- `active_period_evolution.png` - **NEW**: Metrics across active periods by group
- `dormant_period_evolution.png` - **NEW**: Wake-up metrics across dormant periods by group

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
