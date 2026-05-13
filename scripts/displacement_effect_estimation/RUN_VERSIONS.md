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
outputs/displacement_effect_estimation/logs/run.log
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
- outputs under `outputs/displacement_effect_estimation`

The previous 22-closure registry is preserved at
`outputs/customer-store/closure_pair_registry_full.csv`, with archived result bundles under
`outputs/robustness/full_registry`.

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
  --output-dir outputs/displacement_effect_estimation/balanced_did
```

3. Separate effect by closure event, DDD

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh \
  --separate-effect \
  --output-dir outputs/displacement_effect_estimation/separate_effect
```

4. Separate effect with recency filter

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh \
  --separate-effect \
  --select-recency-consumers 10 \
  --output-dir outputs/displacement_effect_estimation/separate_effect_r10
```

5. Separate effect for one closure duration

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh \
  --separate-effect \
  --closure-duration-days 10 \
  --output-dir outputs/displacement_effect_estimation/separate_effect_d10
```

6. Separate effect for one closure duration plus recency filter

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh \
  --separate-effect \
  --closure-duration-days 10 \
  --select-recency-consumers 10 \
  --output-dir outputs/displacement_effect_estimation/separate_effect_d10_r10
```

### `variety_seeking`

1. Aggregate, default unbalanced-panel DDD, `distinct` mode

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh \
  --outcome variety_seeking \
  --output-dir outputs/displacement_effect_estimation/variety_seeking
```

2. Aggregate, unbalanced-panel DDD, `instance` mode

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh \
  --outcome variety_seeking \
  --variety-seeking-mode instance \
  --output-dir outputs/displacement_effect_estimation/variety_seeking_instance
```

3. Aggregate, unbalanced-panel DDD, `distinct-only-new` mode

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh \
  --outcome variety_seeking \
  --variety-seeking-mode distinct-only-new \
  --output-dir outputs/displacement_effect_estimation/variety_seeking_distinct_only_new
```

4. Aggregate, balanced-panel DiD

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh \
  --outcome variety_seeking \
  --balanced-panel \
  --output-dir outputs/displacement_effect_estimation/variety_seeking_balanced
```

5. Aggregate, keep period-0 purchasers (only relevant with `--balanced-panel`)

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh \
  --outcome variety_seeking \
  --balanced-panel \
  --keep-period0-purchasers \
  --output-dir outputs/displacement_effect_estimation/variety_seeking_keep_p0
```

6. Separate effect by closure event

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh \
  --outcome variety_seeking \
  --separate-effect \
  --output-dir outputs/displacement_effect_estimation/variety_seeking_separate
```

7. Separate effect with recency filter

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh \
  --outcome variety_seeking \
  --separate-effect \
  --select-recency-consumers 10 \
  --output-dir outputs/displacement_effect_estimation/variety_seeking_separate_r10
```

8. Separate effect with explicit unbalanced panel (same as default)

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh \
  --outcome variety_seeking \
  --separate-effect \
  --no-balanced-panel \
  --output-dir outputs/displacement_effect_estimation/variety_seeking_separate_unbalanced
```

## Important Constraints

- `--select-recency-consumers N` requires `--separate-effect`.
- `--closure-duration-days N` must use a positive integer.
- `--select-recency-consumers N` must use a positive integer.
- `--t-horizon` must be at least `1`.
- `--variety-seeking-mode` must be one of `distinct`, `instance`, or `distinct-only-new`.
- `--no-unbalanced-panel` is only meaningful for `n_purchases`.
- `--balanced-panel`, `--no-balanced-panel`, `--variety-seeking-mode`, and `--keep-period0-purchasers` are only meaningful for `variety_seeking`.

## Other Useful Flags

- `--output-dir <path>`
  Changes where estimation outputs are saved.
- `--log-file <path>`
  Overrides the Python log destination.
- `--log-level DEBUG|INFO|WARNING|ERROR`
  Changes logging verbosity.
- `--cluster-col <column>`
  Changes the clustering column used in the regressions.
- `--t-horizon N`
  Changes the number of pre and post bins included.

## Recommended Naming Convention

To keep runs easy to compare, it helps to encode the key choices in `--output-dir`, for example:

- `balanced_did`
- `separate_effect`
- `separate_effect_d10_r10`
- `variety_seeking_instance`
- `variety_seeking_distinct_only_new`
- `variety_seeking_balanced`
