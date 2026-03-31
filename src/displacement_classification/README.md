# Displacement Classification Model

Trains a binary classifier to predict whether a consumer would have made a Luckin purchase during a store closure window (displacement classification for habit-breaking analysis).

## Usage

```bash
cd /path/to/model-free
PYTHONPATH=src/customer-store:src/displacement_classification \
  python src/displacement_classification/main.py
```

Or with the helper script (logs to `outputs/displacement_classification/logs/displacement_classification.log`):

```bash
cd scripts/displacement_classification
./run_with_logging.sh displacement
./run_with_logging.sh displacement --tail-closures 3
./run_with_logging.sh displacement --rebuild-push-cache
```

For a quick test with sampled data:

```bash
python src/displacement_classification/main.py --sample 10000
```

Smoke test (one closure from the registry with `status=kept`, ten members, fast push-cache reuse on second run):

```bash
python src/displacement_classification/main.py --max-closures 1 --max-members 10
```

## Push notification features

`config.json` includes `push_features`: CSV glob under `data/data1031`, rolling windows (default 7/14/28 days), and `cache_relative_dir`. Filtered push rows for the current panel members and date range are saved as `push_events_filtered_<hash>.parquet` under that cache directory. The next run loads this file instead of re-reading all CSVs unless you pass `--rebuild-push-cache`. Set `push_features.enabled` to `false` to skip push features entirely.

## Outputs

- **train_displacement_model.log** — Full log (variable statistics, training progress, accuracy)
- **variable_importance.csv** — Feature importance ranking
- **prediction_accuracy.csv** — Accuracy by group (Treatment Pre, Control Pre, Control During)

## Requirements

- pandas, numpy
- xgboost (for GPU: CUDA-enabled XGBoost)
- analyze_closure_impact from customer-store (same project)

## GPU

The script checks for GPU availability and uses `device='cuda'` in XGBoost when available. Install CUDA-enabled XGBoost for GPU training.
