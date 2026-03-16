# Displacement Effect Estimation

This module implements two parallel causal specifications on top of the existing displacement-model outputs:

1. Thresholded DDD (`score >= 0.5` by default)
2. Continuous-score DDD (`Post × Treated × displacement_prob`)

## Inputs

- Period outcomes: `plots/customer_store_analysis/period_behavior_p5_r80_w{window}.csv`
- Displacement scores: `outputs/displacement_classification/displacement_scores_t0_ex_ante.csv`

## Run

From this folder:

```bash
python run.py --window 14 --outcome n_purchases --thresholds 0.5
```

## Outputs

Saved to `outputs/displacement_effect_estimation/`:

- `estimation_sample.csv`
- `ddd_threshold_results.csv`
- `ddd_threshold_fit.csv`
- `ddd_score_results.csv`
- `ddd_score_fit.csv`
- `spec_comparison.csv`
- `summary.md`
