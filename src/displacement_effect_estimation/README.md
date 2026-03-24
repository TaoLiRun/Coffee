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

CLI examples:

```bash
# Aggregate effect across all closures/events
python run.py --outcome n_purchases --t-horizon 4

# Separate effect for each closure/event
python run.py --outcome n_purchases --t-horizon 4 --separate-effect

# Separate effect for each closure/event, with recency filter
python run.py --outcome n_purchases --t-horizon 4 --separate-effect --select-recency-consumers 10
```

Behavior is controlled by `config.json`:

- `spec.separate_effect = false` keeps the current aggregate estimation across all closures.
- `spec.separate_effect = true` runs one estimation per closure/event and skips the closure-length heterogeneity event-study spec, which is not identified within a single event.
- `spec.select_recency_consumers = false` keeps the full scored consumer base.
- `spec.select_recency_consumers = 10` is only valid when `spec.separate_effect = true` and restricts each event to consumers with a purchase in `(closure_start - 10, closure_start)`.

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

When `spec.separate_effect = true`, outputs are saved under
`outputs/displacement_effect_estimation/separate_effect/<closure_event_id>/`
with one subdirectory per closure/event, plus
`outputs/displacement_effect_estimation/separate_effect/event_index.csv`.
