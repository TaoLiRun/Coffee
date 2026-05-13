# Displacement Effect Estimation

This module implements two parallel causal specifications on top of the existing displacement-model outputs:

1. Binary-label DDD (directly uses `predicted_displaced_t0_ex_ante`)
2. Continuous-score DDD (`Post × Treated × displacement_prob`)
3. Event-study ATT/DDD with closure-length heterogeneity and pre-trend joint tests

## Inputs

- Displacement scores: `outputs/displacement_classification/displacement_scores_t0_ex_ante.csv`
- Closure registry: `outputs/customer-store/closure_pair_registry.csv` (the 18-closure main sample)
- Ex-ante feature cache: `../outputs/displacement_classification/cache/features_t0_<hash>.parquet`
- Orders history: `data/data1031/order_result.csv` (auto-detected under workspace)

For `outcome=variety_seeking`, purchase-product history is loaded from
`data/processed/order_commodity_result_processed.csv`.

### Variety-seeking definition

The formula is implemented in `data.py` (`_compute_variety_seeking_for_window`):

- `variety_seeking = |new products in window| / |products in window|`
- `distinct` mode (default): each `product_id` is counted once per member per window.
- `instance` mode: each purchase row is counted (repeated buys increase weight).
- `distinct-only-new` mode: among distinct products purchased in the window, the share whose **global** first-sale date falls in **this** window’s dates or in the **chronologically previous** panel window’s dates (inclusive). For the leftmost pre bin there is no previous window, so only the current window is used. Period-0 plots use the union of the closure window and the `rel_t=-1` window.

`period 0` means the closure window `[closure_start, closure_end]`.

## Run

From this folder:

```bash
python run.py --outcome n_purchases --t-horizon 4
```

CLI examples:

```bash
# Aggregate effect across all closures/events
python run.py --outcome n_purchases --t-horizon 4

# Aggregate binary purchase-incidence outcome with supplementary logit in collapsed DDD
python run.py --outcome purchase_incidence_binary --t-horizon 4 \
  --output-dir outputs/displacement_effect_estimation/purchase_incidence_binary

# Separate effect for each closure/event
python run.py --outcome n_purchases --t-horizon 4 --separate-effect

# Separate effect for each closure/event, with recency filter
python run.py --outcome n_purchases --t-horizon 4 --separate-effect --select-recency-consumers 10

# Separate effect for 10-day closures only, saved to a custom folder
python run.py --outcome n_purchases --t-horizon 4 --separate-effect --closure-duration-days 10 --select-recency-consumers 10 --output-dir outputs/displacement_effect_estimation/separate_effect_d10_r10

# Variety-seeking: keep period-0 purchasers when using --balanced-panel (otherwise that filter applies)
python run.py --outcome variety_seeking --balanced-panel --keep-period0-purchasers

# Variety-seeking: global catalog-age share (distinct products in-window)
python run.py --outcome variety_seeking --variety-seeking-mode distinct-only-new \
  --output-dir outputs/displacement_effect_estimation/variety_seeking_distinct_only_new
```

Behavior is controlled by `config.json`:

- `paths.closure_registry_file` points to the closure registry used as the main analysis sample.
- `paths.feature_t0_cache_dir` points to the directory containing `features_t0_<hash>.parquet`.
- `paths.feature_cache_key` selects which cached `features_t0_<hash>.parquet` to load.
- `spec.closure_duration_days = false` keeps all closure durations.
- `spec.closure_duration_days = 10` restricts the estimation sample to 10-day closures.
- `spec.separate_effect = false` keeps the current aggregate estimation across all closures.
- `spec.separate_effect = true` runs one estimation per closure/event and skips the closure-length heterogeneity event-study spec, which is not identified within a single event.
- `spec.select_recency_consumers = false` keeps the full scored consumer base.
- `spec.select_recency_consumers = 10` is only valid when `spec.separate_effect = true` and keeps consumers with `days_since_last_purchase < 10` from the cached `features_t0` file, while `order_result.csv` is still used to build event-time outcomes.
- For `outcome=variety_seeking`, the default is an **unbalanced** panel and a **DDD** specification (aligned with `n_purchases`). Pass `--balanced-panel` for a balanced panel and DiD. With `--balanced-panel`, member-closure pairs are dropped when treated members purchase during the closure window or control members do not, unless you pass `--keep-period0-purchasers`.
- `--output-dir ...` overrides `paths.output_dir` for a single run without changing the config file.

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
