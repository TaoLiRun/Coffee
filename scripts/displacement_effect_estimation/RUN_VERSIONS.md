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
- unbalanced panel
- DDD model
- no closure-duration filter
- no recency filter
- outputs under `outputs/displacement_effect_estimation`

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

- default: balanced panel -> DiD
- `--no-balanced-panel`: unbalanced panel -> DDD

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
- `--variety-seeking-mode instance-only-old`
  Measures the share of purchase rows on products that already existed before the event's earliest pre window.

- `--keep-period0-purchasers`
  By default, variety-seeking runs drop period-0 purchasers to keep the treatment contrast clean.
  This flag keeps them.

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

1. Aggregate, default balanced-panel DiD, `distinct` mode

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh \
  --outcome variety_seeking \
  --output-dir outputs/displacement_effect_estimation/variety_seeking
```

2. Aggregate, balanced-panel DiD, `instance` mode

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh \
  --outcome variety_seeking \
  --variety-seeking-mode instance \
  --output-dir outputs/displacement_effect_estimation/variety_seeking_instance
```

3. Aggregate, balanced-panel DiD, `instance-only-old` mode

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh \
  --outcome variety_seeking \
  --variety-seeking-mode instance-only-old \
  --output-dir outputs/displacement_effect_estimation/variety_seeking_instance_only_old
```

4. Aggregate, unbalanced-panel DDD

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh \
  --outcome variety_seeking \
  --no-balanced-panel \
  --output-dir outputs/displacement_effect_estimation/variety_seeking_unbalanced
```

5. Aggregate, keep period-0 purchasers

```bash
./scripts/displacement_effect_estimation/run_with_logging.sh \
  --outcome variety_seeking \
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

8. Separate effect with unbalanced panel

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
- `--variety-seeking-mode` must be one of `distinct`, `instance`, or `instance-only-old`.
- `--no-unbalanced-panel` is only meaningful for `n_purchases`.
- `--no-balanced-panel`, `--variety-seeking-mode`, and `--keep-period0-purchasers` are only meaningful for `variety_seeking`.

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
- `variety_seeking_unbalanced`
