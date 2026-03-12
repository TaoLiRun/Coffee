# Displacement Classification Model

Trains a binary classifier to predict whether a consumer would have made a Luckin purchase during a store closure window (displacement classification for habit-breaking analysis).

## Usage

```bash
cd /home/litao/Coffee/model-free/scripts/displacement_classification
python train_displacement_model.py
```

For a quick test with sampled data:
```bash
python train_displacement_model.py --sample 10000
```

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
