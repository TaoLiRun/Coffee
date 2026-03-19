# Displacement Effect Estimation

This module implements two parallel causal specifications on top of the existing displacement-model outputs:

1. Binary-label DDD (directly uses `predicted_displaced_t0_ex_ante`)
2. Continuous-score DDD (`Post × Treated × displacement_prob`)
3. Event-study ATT/DDD with closure-length heterogeneity and pre-trend joint tests

## Inputs

- Displacement scores: `outputs/displacement_classification/displacement_scores_t0_ex_ante.csv`
- Orders history: `data/data1031/order_result.csv` (auto-detected under workspace)

## Run

From this folder:

```bash
python run.py --outcome n_purchases --t-horizon 4
```

## Outputs

Saved to `outputs/displacement_effect_estimation/`:

- `estimation_sample.csv`
- `ddd_binary_results.csv`
- `ddd_binary_fit.csv`
- `ddd_score_results.csv`
- `ddd_score_fit.csv`
- `spec_comparison.csv`
- `event_study_results.csv`
- `event_study_fit.csv`
- `pretrend_joint_tests.csv`
- `summary.md`
