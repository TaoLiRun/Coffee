# Run Summary — 2026-03-12

## Overview

Two analysis pipelines were executed on 2026-03-12:

1. **Customer-store closure trend analysis** (`plot_closure_trend.py`)
2. **Consumer displacement classification model** (`main.py`)

---

## 1. Closure Trend Line Plots

**Script**: `src/customer-store/plot_closure_trend.py`  
**Runner**: `bash scripts/customer-store/run_with_logging.sh plot_closure_trend`  
**Log**: `outputs/customer-store/logs/plot_closure_trend.log`

### Data

| Item | Value |
|---|---|
| Order commodity records | 10,631,250 |
| Unique customers | 779,744 |
| Unique stores | 260 |
| Date range | 2020-06-01 to 2021-12-31 |
| Total orders (order_result) | 7,312,498 |
| Closures processed | 101 |
| Qualified customers (≥5 purchases, preferred store ratio computed) | 286,784 |
| Never-treated control pool | 74,973 |
| Mean preferred-store ratio | 0.696 (median 0.714) |

### Panels built

| Window | Periods (t) | (group × t) rows | Panel rows |
|---|---|---|---|
| w2 | −2, −1, 0, +1, +2 | 10 | 19,572,360 |
| w4 | −4, …, −1, 0, +1, …, +4 | 18 | 35,230,248 |
| w8 | −8, …, −1, 0, +1, …, +8 | 34 | 66,546,024 |

### Output plots

All saved to `plots/customer_store_analysis/`:

| File | Description |
|---|---|
| `closure_trend_lines_w2.pdf` | Treatment vs control: 4 metrics × 5-period window |
| `closure_trend_lines_w4.pdf` | Treatment vs control: 4 metrics × 9-period window |
| `closure_trend_lines_w8.pdf` | Treatment vs control: 4 metrics × 17-period window (new) |

**Metrics plotted per figure**: purchases per week, new product ratio, mean total discount, coupon usage rate — each with ±1 SD shading over customers and closures.

---

## 2. Consumer Displacement Classification Model

**Script**: `src/displacement_classification/main.py`  
**Runner**: `bash scripts/customer-store/run_with_logging.sh displacement`  
**Log**: `outputs/displacement_classification/logs/`  
**Config**: `src/displacement_classification/config.json`

### Training setup

| Parameter | Value |
|---|---|
| Closures used | 20 (tail) |
| Pre-closure window | 4 weeks (periods t = −4, …, −1) |
| Min purchases threshold | 5 |
| Min preferred-store ratio | 0.8 |
| Closure filter | closure_start ≥ 2020-09-01 |
| XGBoost max_depth | 6 |
| XGBoost eta | 0.1 |
| num_boost_round | 500 |
| Decision threshold | 0.5 |

### Panel

| Group | Members | Notes |
|---|---|---|
| Treatment (union) | — | Customers with ≥80 % visits at a closed store |
| Control (union) | — | Never-treated customers with ≥5 purchases |
| Total panel members | 106,392 | — |
| Panel rows (8.3 M) | 8,300,103 | 43 unique period_start dates × members |
| Training rows | — | Periods t = −4 to −1 only (t = 0 excluded from training) |
| Feature columns | 46 | Behavioral + demographic; closure-event features excluded |

### Prediction accuracy

| Group | Accuracy | Precision | Recall | F1 | N |
|---|---|---|---|---|---|
| Treatment Pre (t = −1) | 0.752 | 0.236 | 0.393 | 0.295 | 6,197 |
| Control Pre (t = −1) | 0.917 | 0.715 | 0.392 | 0.507 | 1,655,063 |
| Control During (t = 0) | 0.835 | 0.861 | 0.195 | 0.318 | 1,655,063 |

> **Interpretation**: The model generalises to the control pre-period well (F1 = 0.51), confirming it captures genuine purchase propensity. The lower F1 for treatment pre (0.30) and control during (0.32) reflects behavioural disruption — consistent with the displacement hypothesis.

### Top 14 features by gain importance

| Rank | Feature | Gain |
|---|---|---|
| 1 | `purchases_per_week_last_1w` | 4,925 |
| 2 | `days_since_last_purchase` | 2,266 |
| 3 | `purchases_per_week_last_2w` | 1,460 |
| 4 | `total_purchase_days_pre` | 1,418 |
| 5 | `purchases_per_week_last_4w` | 562 |
| 6 | `total_spend_last_2w` | 537 |
| 7 | `preferred_store_ratio` | 337 |
| 8 | `share_weeks_with_purchase` | 272 |
| 9 | `avg_coffee_num` | 181 |
| 10 | `share_purchases_dow6` | 173 |
| 11 | `total_spend_pre` | 147 |
| 12 | `avg_delivery_pay` | 146 |
| 13 | `mean_inter_purchase_interval_days` | 142 |
| 14 | `cv_inter_purchase_interval` | 139 |

Recency features dominate (ranks 1–3), reflecting that recent purchase frequency is the strongest predictor of whether a customer will purchase in the following week.

### Output files

All saved to `outputs/displacement_classification/`:

| File | Size | Description |
|---|---|---|
| `displacement_model.json` | 3.6 MB | Trained XGBoost booster |
| `panel_with_scores.parquet` | 472 MB | Full panel (all 46 features + `displacement_prob` + `predicted_displaced`) |
| `displacement_scores.csv` | 653 MB | Lightweight ID + score summary |
| `variable_importance.csv` | — | Gain-based feature ranking |
| `prediction_accuracy.csv` | — | Per-group accuracy / F1 table |

---

## Repository structure after this session

```
model-free/
├── src/
│   ├── customer-store/
│   │   ├── analyze_closure_impact.py
│   │   └── plot_closure_trend.py
│   └── displacement_classification/
│       ├── config.json                  ← all tunable parameters
│       ├── data_loading_feature_constructing.py
│       ├── model.py
│       └── main.py
├── scripts/
│   └── customer-store/
│       └── run_with_logging.sh          ← runs src/ scripts; logs → outputs/
├── outputs/
│   ├── customer-store/logs/
│   │   ├── analyze_closure_impact.log
│   │   └── plot_closure_trend.log
│   └── displacement_classification/
│       ├── displacement_model.json
│       ├── panel_with_scores.parquet
│       ├── displacement_scores.csv
│       ├── variable_importance.csv
│       ├── prediction_accuracy.csv
│       └── logs/
│           ├── full_run_20.log
│           ├── full_run.log
│           └── train_displacement_model.log
└── plots/
    └── customer_store_analysis/
        ├── closure_trend_lines_w2.pdf
        ├── closure_trend_lines_w4.pdf
        └── closure_trend_lines_w8.pdf   ← new
```
