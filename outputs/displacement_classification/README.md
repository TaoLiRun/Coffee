# Displacement Classification Outputs

This folder stores the ex-ante blocked-purchase classifier outputs.

Key files:

- `displacement_scores_t0_ex_ante.csv`: member-closure prediction file used by the DDD estimator.
- `prediction_accuracy_*.csv`: classifier performance by holdout/run.
- `variable_importance_*.csv`: feature-importance tables.
- `label_balance_audit.csv`: label balance diagnostics.

The feature cache used by the estimator is configured separately in `src/displacement_effect_estimation/config.json`.
