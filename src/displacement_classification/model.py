"""
Model training utilities, evaluation helpers, and model persistence for
the displacement classification pipeline.

Exports
-------
Functions : print_variable_statistics, check_gpu, eval_metrics,
            save_model_artifacts, load_displacement_model
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd

from data_loading_feature_constructing import log_print, OUTPUT_DIR, CONFIG


# ---------------------------------------------------------------------------
# Diagnostics
# ---------------------------------------------------------------------------


def print_variable_statistics(logger: logging.Logger, df: pd.DataFrame, feature_cols: List[str]) -> None:
    """Print mean, min, max for each variable."""
    log_print(logger, "\n" + "=" * 80)
    log_print(logger, "Variable Statistics (mean, min, max)")
    log_print(logger, "=" * 80)
    for col in feature_cols:
        if col not in df.columns:
            continue
        s = df[col]
        if pd.api.types.is_numeric_dtype(s):
            valid = s.dropna()
            if len(valid) > 0:
                log_print(logger, f"  {col}: mean={valid.mean():.4f}, min={valid.min():.4f}, max={valid.max():.4f}")
            else:
                log_print(logger, f"  {col}: (all NaN)")
        else:
            log_print(logger, f"  {col}: categorical, n_unique={s.nunique()}")


def check_gpu() -> bool:
    """Return True if CUDA is available for XGBoost."""
    try:
        import xgboost as xgb
        dtrain = xgb.DMatrix(np.array([[1, 2], [3, 4]]), label=[0, 1])
        params = {"tree_method": "hist", "device": "cuda"}
        xgb.train(params, dtrain, num_boost_round=1)
        return True
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------


def eval_metrics(y_true: np.ndarray, y_pred_proba: np.ndarray, threshold: float = 0.5) -> dict:
    """Compute binary classification metrics at a given probability threshold."""
    y_pred = (y_pred_proba >= threshold).astype(int)
    tp = ((y_true == 1) & (y_pred == 1)).sum()
    tn = ((y_true == 0) & (y_pred == 0)).sum()
    fp = ((y_true == 0) & (y_pred == 1)).sum()
    fn = ((y_true == 1) & (y_pred == 0)).sum()
    acc  = (tp + tn) / len(y_true) if len(y_true) > 0 else 0
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0
    rec  = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1   = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0
    fpr  = fp / (fp + tn) if (fp + tn) > 0 else 0
    fnr  = fn / (fn + tp) if (fn + tp) > 0 else 0
    return {
        "accuracy": acc, "precision": prec, "recall": rec,
        "f1": f1, "fpr": fpr, "fnr": fnr, "n": len(y_true),
    }


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------


def save_model_artifacts(
    model,                          # xgb.Booster
    features_df: pd.DataFrame,
    feature_cols: List[str],
    eval_pre: pd.DataFrame,
    eval_during: pd.DataFrame,
    output_dir: Path,
    logger: logging.Logger,
) -> None:
    """Persist all model artifacts produced by a training run.

    Writes five files to *output_dir*:

    * ``displacement_model.json``   – XGBoost booster (load with
      :func:`load_displacement_model`).
    * ``variable_importance.csv``   – gain-based feature importances.
    * ``prediction_accuracy.csv``   – per-group accuracy / F1 table.
    * ``panel_with_scores.parquet`` – full panel with ``displacement_prob``
      and ``predicted_displaced`` appended.
    * ``displacement_scores.csv``   – lightweight ID + score summary.
    """
    import xgboost as xgb

    # ---- 1. Model -------------------------------------------------------
    model_path = output_dir / "displacement_model.json"
    model.save_model(str(model_path))
    log_print(logger, f"\nSaved model → {model_path}")

    # ---- 2. Variable importance -----------------------------------------
    imp = model.get_score(importance_type="gain")
    imp_df = pd.DataFrame([{"feature": k, "importance": v} for k, v in imp.items()])
    imp_df = imp_df.sort_values("importance", ascending=False).reset_index(drop=True)
    imp_df["rank"] = imp_df.index + 1
    log_print(logger, "\n" + "=" * 80)
    log_print(logger, "Variable Importance Ranking (top 30)")
    log_print(logger, "=" * 80)
    for _, r in imp_df.head(30).iterrows():
        log_print(logger, f"  {r['rank']:3d}. {r['feature']}: {r['importance']:.2f}")
    imp_df.to_csv(output_dir / "variable_importance.csv", index=False)
    log_print(logger, f"\nSaved variable_importance.csv → {output_dir}")

    # ---- 3. Prediction accuracy table -----------------------------------
    results = []
    for name, sub in [
        ("Treatment_Pre_t-1", eval_pre[eval_pre["group"] == "treatment"]),
        ("Control_Pre_t-1",   eval_pre[eval_pre["group"] == "control"]),
        ("Control_During_t0", eval_during),
    ]:
        if sub.empty:
            continue
        X = sub[feature_cols].copy()
        d = xgb.DMatrix(X, feature_names=feature_cols)
        pred = model.predict(d)
        m = eval_metrics(sub["label"].values, pred)
        m["group"] = name
        results.append(m)
    log_print(logger, "\n" + "=" * 80)
    log_print(logger, "Prediction Accuracy Table")
    log_print(logger, "=" * 80)
    res_df = pd.DataFrame(results)
    log_print(logger, res_df.to_string(index=False))
    res_df.to_csv(output_dir / "prediction_accuracy.csv", index=False)
    log_print(logger, f"\nSaved prediction_accuracy.csv → {output_dir}")

    # ---- 4. Score full panel --------------------------------------------
    log_print(logger, "\nScoring full panel...")
    X_all = features_df[feature_cols].copy()
    d_all = xgb.DMatrix(X_all, feature_names=feature_cols)
    features_df = features_df.copy()  # avoid mutating caller's frame
    features_df["displacement_prob"]   = model.predict(d_all)
    threshold = CONFIG["model"]["decision_threshold"]
    features_df["predicted_displaced"] = (features_df["displacement_prob"] >= threshold).astype(int)

    keep_cols = [
        "member_id", "dept_id", "closure_start", "closure_end",
        "period", "period_start", "period_end",
        "is_treated", "group", "label",
        "displacement_prob", "predicted_displaced",
        # Closure-event features kept for DiD heterogeneity analysis
        "closure_length_days", "closure_start_month",
        "closure_start_weekday", "closure_start_season",
        "share_visited_stores_closed", "tenure_days",
    ] + feature_cols
    seen: set = set()
    out_cols = [c for c in keep_cols if c in features_df.columns and not (c in seen or seen.add(c))]

    scored_path = output_dir / "panel_with_scores.parquet"
    features_df[out_cols].to_parquet(str(scored_path), index=False)
    log_print(logger, f"Saved scored panel ({len(features_df):,} rows) → {scored_path}")

    summary_cols = [
        "member_id", "dept_id", "closure_start", "closure_end",
        "period", "period_start", "period_end",
        "is_treated", "group", "label",
        "displacement_prob", "predicted_displaced",
    ]
    summary_cols = [c for c in summary_cols if c in features_df.columns]
    scores_csv_path = output_dir / "displacement_scores.csv"
    features_df[summary_cols].to_csv(str(scores_csv_path), index=False)
    log_print(logger, f"Saved score summary CSV → {scores_csv_path}")


def load_displacement_model(model_path):
    """Load a saved XGBoost displacement model.

    Parameters
    ----------
    model_path : str or pathlib.Path
        Path to ``displacement_model.json`` produced by
        :func:`save_model_artifacts`.

    Returns
    -------
    xgb.Booster
        Ready-to-use booster.  Score new data with::

            import xgboost as xgb
            import pandas as pd
            model = load_displacement_model("...outputs/displacement_model.json")
            d = xgb.DMatrix(df[feature_cols], feature_names=feature_cols)
            probs = model.predict(d)   # float array in [0, 1]
    """
    import xgboost as xgb
    booster = xgb.Booster()
    booster.load_model(str(model_path))
    return booster
