# Runnable Versions for `run_with_logging.sh`

This note summarizes the main versions you can run with:

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh [flags...]
```

The script is a thin wrapper around:

```bash
conda run -n JAX-py python src/displacement_effect_estimation/run.py
```

It forwards all CLI flags to `run.py` and writes the shell log to:

```text
outputs/03_main_18_closures/purchase_frequency_ddd_h4/logs/run.log
```

## Default Run

If you run the script with no flags:

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh
```

you get:

- `outcome=n_purchases`
- pooled estimation across all closure events
- closure registry from `outputs/customer-store/closure_pair_registry.csv` (the 18-closure main sample)
- unbalanced panel
- DDD model
- no closure-duration filter
- no recency filter
- outputs under `outputs/03_main_18_closures/purchase_frequency_ddd_h4`

The previous 22-closure registry is preserved at
`outputs/customer-store/closure_pair_registry_full.csv`, with archived result bundles under
`outputs/05_robustness/full_registry_22`.

## Main Run Dimensions

### 1. Outcome

You can run two outcomes:

- `--outcome n_purchases`
  Measures purchase-day intensity in each event-time window.
- `--outcome variety_seeking`
  Measures variety seeking from product-level purchase history.

### 2. Panel Structure and Implied Model

The model type is implied by the panel structure.

For `n_purchases`:

- default: unbalanced panel -> DDD
- `--no-unbalanced-panel`: balanced panel -> DiD

For `variety_seeking`:

- default: unbalanced panel -> DDD (same as purchase-frequency default)
- `--balanced-panel`: balanced panel -> DiD
- `--no-balanced-panel`: same as default (kept for backward compatibility; do not combine with `--balanced-panel`)

### 3. Estimation Scope

- default: pooled across all closure events
- `--separate-effect`: estimate one result bundle per closure event

When `--separate-effect` is on, outputs are saved under:

```text
<output-dir>/separate_effect/<closure_event_id>/
```

plus an index file:

```text
<output-dir>/separate_effect/event_index.csv
```

### 4. Sample Filters

- `--closure-duration-days N`
  Keeps only closures with exactly `N` days.
- `--select-recency-consumers N`
  Keeps only consumers with `days_since_last_purchase < N`.
  This is only valid together with `--separate-effect`.

### 5. Variety-Seeking-Specific Options

These only matter when `--outcome variety_seeking`.

- `--variety-seeking-mode distinct`
  Default. Counts each `product_id` once per member per window.
- `--variety-seeking-mode instance`
  Counts every purchase row, so repeated purchases carry more weight.
- `--variety-seeking-mode distinct-only-new`
  Among distinct `product_id` values purchased in the window: share whose global first-sale date lies in **this** calendar window **or** the **chronologically previous** panel window (inclusive bounds). Leftmost pre bin has no previous window, so only the current window applies. Period-0 plots use the union of the closure window and the `rel_t=-1` window.

- `--keep-period0-purchasers`
  When using `--balanced-panel`, variety-seeking runs otherwise drop treated members who purchase during the closure window and controls who do not, to keep the treatment contrast clean. This flag keeps them. (Unbalanced DDD runs do not apply that filter by default.)

### 6. Pre-novelty heterogeneity (distinct variety, pooled DDD)

This is an **optional extension** for headline novelty-seeking (`--outcome variety_seeking` with `--variety-seeking-mode distinct`, **unbalanced** panel / DDD only).

- **`--variety-pre-novelty-heterogeneity`**
  - For each **member–closure** episode, compute the **pre-period** mean of the distinct novelty outcome (all `rel_t < 0` rows with non-missing outcome in that episode).
  - Form a binary indicator **high pre-novelty** vs **low** by comparing that episode mean to a cross-sectional threshold computed **across episodes** in the built estimation sample. The default threshold is the **sample median** of those episode means; set `spec.variety_pre_novelty_split_method` to **`"mode"`** in `config.json` to use instead the **statistical mode** of the episode means (after rounding to 10 decimal places so the mode is well defined for near-continuous values). **High** means strictly **above** the threshold; **at or below** counts as low.
  - The indicator is merged to all rows of the episode (constant within member–closure over `rel_t`).
  - **Collapsed pooled DDD** is fully saturated by pre-novelty type. It adds `post × high pre-novelty` as well as that term's interactions with treatment and predicted incidence. The first three coefficients summarize the **low** pre-novelty subgroup; the four type-interaction terms capture the high type's general post shift and incremental components. Algebraically equivalent output specifications estimate both subgroup DDDs and all four treated-control effects directly, with covariance-aware standard errors. Omitting `post × high pre-novelty` is invalid because type-specific general post changes would load onto the treatment interactions.
  - The event-study analog is saturated in the same way and includes a direct parameterization of the low- and high-pre-novelty DDD paths and their joint pretrend tests. The separate script `scripts/writeup/validate_pre_novelty_heterogeneity.py` adds a continuous interaction, leave-one-closure-out estimates and multiple-testing diagnostics for the final 18-event sample.
  - **Not supported together with** `--balanced-panel`, `--separate-effect`, or `--variety-seeking-mode` other than `distinct`.

Suggested output directory label: `variety_seeking_distinct_pre_novelty_heterogeneity`.

### 7. Assumption-gap diagnostic bundles

The pooled DDD runner now writes the paper-style assumption diagnostics when the model is a DDD rather than a balanced DiD:

- `ddd_binary_results_matched.csv`
- `event_study_results_matched.csv`
- `pretrend_joint_tests_matched.csv`
- `matched_episode_support_summary.csv`
- `blocked_gap_event_study_matched.csv`
- `blocked_gap_event_study_plot_data_matched.csv`
- `blocked_gap_event_study_matched.png`
- `pretrend_bias_equality.csv`

The main diagnostic bundles currently saved are:

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh \
  --outcome n_purchases \
  --output-dir outputs/04_diagnostics_18_closures/purchase_common_support

./scripts/displacement_effect_estimation/run_with_logging.sh \
  --outcome variety_seeking \
  --output-dir outputs/04_diagnostics_18_closures/novelty_common_support

./scripts/displacement_effect_estimation/run_with_logging.sh \
  --outcome variety_seeking \
  --variety-pre-novelty-heterogeneity \
  --customer-median-split true \
  --output-dir outputs/04_diagnostics_18_closures/novelty_common_support_heterogeneity_median

./scripts/displacement_effect_estimation/run_with_logging.sh \
  --outcome variety_seeking \
  --variety-pre-novelty-heterogeneity \
  --customer-median-split false \
  --output-dir outputs/04_diagnostics_18_closures/novelty_common_support_heterogeneity_quartile_tails
```

The large row-level `estimation_sample.csv` files in these assumption-gap directories are reproducible and intentionally ignored. The versioned files are the summaries, coefficient tables, plots, and logs.

## Supported Run Matrix

### `n_purchases`

1. Aggregate, default DDD

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh
```

2. Aggregate, balanced-panel DiD

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh \
  --no-unbalanced-panel \
  --output-dir outputs/04_diagnostics_18_closures/purchase_balanced_did
```

3. Separate effect by closure event, DDD

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh \
  --separate-effect \
  --output-dir outputs/04_diagnostics_18_closures/purchase_separate_effect
```

4. Separate effect with recency filter

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh \
  --separate-effect \
  --select-recency-consumers 10 \
  --output-dir outputs/04_diagnostics_18_closures/purchase_separate_effect_recency10
```

5. Separate effect for one closure duration

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh \
  --separate-effect \
  --closure-duration-days 10 \
  --output-dir outputs/04_diagnostics_18_closures/purchase_separate_effect_duration10
```

6. Separate effect for one closure duration plus recency filter

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh \
  --separate-effect \
  --closure-duration-days 10 \
  --select-recency-consumers 10 \
  --output-dir outputs/04_diagnostics_18_closures/separate_effect_duration10_recency10
```

### `variety_seeking`

1. Aggregate, default unbalanced-panel DDD, `distinct` mode

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh \
  --outcome variety_seeking \
  --output-dir outputs/03_main_18_closures/novelty_member_first_ddd_h4
```

2. Aggregate, unbalanced-panel DDD, `instance` mode

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh \
  --outcome variety_seeking \
  --variety-seeking-mode instance \
  --output-dir outputs/04_diagnostics_18_closures/novelty_instance
```

3. Aggregate, unbalanced-panel DDD, `distinct-only-new` mode

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh \
  --outcome variety_seeking \
  --variety-seeking-mode distinct-only-new \
  --output-dir outputs/03_main_18_closures/novelty_market_new_ddd_h4
```

4. Aggregate, balanced-panel DiD

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh \
  --outcome variety_seeking \
  --balanced-panel \
  --output-dir outputs/04_diagnostics_18_closures/novelty_balanced_did
```

5. Aggregate, keep period-0 purchasers (only relevant with `--balanced-panel`)

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh \
  --outcome variety_seeking \
  --balanced-panel \
  --keep-period0-purchasers \
  --output-dir outputs/04_diagnostics_18_closures/novelty_balanced_keep_period0
```

6. Separate effect by closure event

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh \
  --outcome variety_seeking \
  --separate-effect \
  --output-dir outputs/04_diagnostics_18_closures/novelty_separate_effect
```

7. Separate effect with recency filter

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh \
  --outcome variety_seeking \
  --separate-effect \
  --select-recency-consumers 10 \
  --output-dir outputs/04_diagnostics_18_closures/novelty_separate_effect_recency10
```

8. Separate effect with explicit unbalanced panel (same as default)

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh \
  --outcome variety_seeking \
  --separate-effect \
  --no-balanced-panel \
  --output-dir outputs/04_diagnostics_18_closures/novelty_separate_effect_unbalanced
```

9. Aggregate, unbalanced-panel DDD, `distinct` mode, pre-novelty heterogeneity (collapsed DDD with `post` × treatment × displacement × high/low pre-novelty split)

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh \
  --outcome variety_seeking \
  --variety-seeking-mode distinct \
  --variety-pre-novelty-heterogeneity \
  --output-dir outputs/04_diagnostics_18_closures/novelty_pre_heterogeneity_median
```

Use `spec.variety_pre_novelty_split_method` in `config.json` (`"median"` default, or `"mode"`) to choose the cross-episode threshold for the episode-level pre-period mean distinct novelty measure.

## Important Constraints

- `--select-recency-consumers N` requires `--separate-effect`.
- `--closure-duration-days N` must use a positive integer.
- `--select-recency-consumers N` must use a positive integer.
- `--t-horizon` must be at least `1`.
- `--variety-seeking-mode` must be one of `distinct`, `instance`, or `distinct-only-new`.
- `--no-unbalanced-panel` is only meaningful for `n_purchases`.
- `--balanced-panel`, `--no-balanced-panel`, `--variety-seeking-mode`, and `--keep-period0-purchasers` are only meaningful for `variety_seeking`.
- `--variety-pre-novelty-heterogeneity` requires `--outcome variety_seeking`, `--variety-seeking-mode distinct`, pooled estimation (not `--separate-effect`), and unbalanced-panel DDD (do not use `--balanced-panel`).

## Other Useful Flags

- `--output-dir <path>`
  Changes where estimation outputs are saved.
- `--log-file <path>`
  Overrides the Python log destination.
- `--log-level DEBUG|INFO|WARNING|ERROR`
  Changes logging verbosity.
- `--cluster-col <column>`
  Changes the clustering column used in the regressions. Production runs use
  `closure_event_id`, matching inference to the level of the closure shock.
- `--t-horizon N`
  Changes the number of pre and post bins included.

## Recommended Naming Convention

To keep runs easy to compare, it helps to encode the key choices in `--output-dir`, for example:

- `outputs/03_main_18_closures/purchase_frequency_ddd_h4`
- `outputs/03_main_18_closures/novelty_member_first_ddd_h4`
- `outputs/03_main_18_closures/novelty_market_new_ddd_h4`
- `outputs/04_diagnostics_18_closures/purchase_common_support`
- `outputs/04_diagnostics_18_closures/novelty_common_support`
- `outputs/04_diagnostics_18_closures/novelty_pre_heterogeneity_median`
- `outputs/05_robustness/full_registry_22/<legacy_run_name>`
