"""
Entry point for the displacement classification pipeline.

Usage
-----
    python main.py
    python main.py --max-closures 20
    python main.py --tail-closures 20
    python main.py --sample 50000 --max-closures 5

See --help for all options.
"""

from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd

# ---------------------------------------------------------------------------
# Imports from sibling modules
# ---------------------------------------------------------------------------
from data_loading_feature_constructing import (
    # Functions
    setup_logging,
    log_print,
    load_no_push_ids,
    load_member_demographics,
    load_order_result_full,
    build_training_panel,
    compute_features_for_panel,
    # Constants
    CLOSURES_CSV,
    OUTPUT_DIR,
    WINDOW_WEEKS,
    CONFIG,
    # Re-exported from analyze_closure_impact
    DEFAULT_LOWEST_PURCHASES,
    DEFAULT_LOWEST_RATIO,
    get_customer_store_preference,
    get_never_treated_members,
    get_closure_specific_control_members,
    _get_treated_members_for_store,
)
from model import (
    check_gpu,
    print_variable_statistics,
    save_model_artifacts,
)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(max_closures: Optional[int] = None, tail_closures: Optional[int] = None) -> None:
    logger = setup_logging()
    log_print(logger, "=" * 80)
    log_print(logger, "Displacement Classification Model Training")
    log_print(logger, f"Started at {datetime.now().isoformat()}")
    log_print(logger, "=" * 80)

    # ---- Load data -------------------------------------------------------
    df_order_full = load_order_result_full(logger)
    closures = pd.read_csv(CLOSURES_CSV, encoding="utf-8-sig")

    # Retain only closures where all 4 pre-closure weeks fall after the earliest
    # order date (2020-06-01).  Period −4 starts at closure_start − 28 days,
    # so we require closure_start >= 2020-09-01 (ensuring ≥4 weeks of history).
    closures["closure_start_dt"] = pd.to_datetime(closures["closure_start"])
    closures = (
        closures[closures["closure_start_dt"] >= pd.Timestamp(CONFIG["data"]["closure_filter_start"])]
        .drop(columns=["closure_start_dt"])
        .reset_index(drop=True)
    )
    log_print(logger, f"  Closures after Aug-2020 filter: {len(closures)}")
    if closures.empty:
        raise ValueError("No closures remain after Aug-2020 filter.")

    if tail_closures is not None:
        closures = closures.tail(tail_closures).reset_index(drop=True)
        log_print(logger, f"  [DEBUG] Using last {len(closures)} closure(s) (tail)")
    elif max_closures is not None:
        closures = closures.head(max_closures).reset_index(drop=True)
        log_print(logger, f"  [DEBUG] Limiting to {len(closures)} closure(s) for testing")

    no_push_ids         = load_no_push_ids()
    log_print(logger, f"Loaded {len(no_push_ids):,} no-push members")
    member_demographics = load_member_demographics(logger, no_push_ids)

    customer_preference = get_customer_store_preference(
        df_order_full, lowest_purchases=DEFAULT_LOWEST_PURCHASES
    )

    # unique_visits is built from the FULL df_order_full so that
    # get_closure_specific_control_members can correctly assess pre-closure
    # visit counts for control candidates.
    unique_visits = df_order_full[["member_id", "date", "dept_id"]].drop_duplicates()

    # ---- Pre-filter order data to exact panel members --------------------
    log_print(logger, "\nPre-filtering data to exact panel members across all closures...")
    all_treated_members: set = set()
    all_control_members: set = set()
    never_treated_pool = get_never_treated_members(
        closures, customer_preference, DEFAULT_LOWEST_PURCHASES, DEFAULT_LOWEST_RATIO
    )
    for _, closure in closures.iterrows():
        treated = _get_treated_members_for_store(
            customer_preference, int(closure["dept_id"]), DEFAULT_LOWEST_RATIO
        )
        all_treated_members.update(treated)
        ctrl = get_closure_specific_control_members(
            unique_visits, never_treated_pool,
            pd.to_datetime(closure["closure_start"]).date(),
            DEFAULT_LOWEST_PURCHASES, DEFAULT_LOWEST_RATIO,
        )
        all_control_members.update(ctrl)

    panel_members = all_treated_members | all_control_members
    log_print(logger, f"  Treatment members (union):  {len(all_treated_members):,}")
    log_print(logger, f"  Control members (union):    {len(all_control_members):,}")
    log_print(logger, f"  Total panel members:        {len(panel_members):,}")

    n_ord_before  = len(df_order_full)
    df_order_full = df_order_full[df_order_full["member_id"].isin(panel_members)].copy()
    log_print(logger, f"  df_order_full: {n_ord_before:,} → {len(df_order_full):,} rows")

    # ---- Panel construction and feature engineering ----------------------
    panel = build_training_panel(
        logger, df_order_full, closures, customer_preference, unique_visits,
    )
    features_df = compute_features_for_panel(
        logger, panel, df_order_full, member_demographics,
    )

    # Feature columns: exclude identifiers, label, and closure-specific columns.
    # Closure-specific features (closure_length_days, closure_start_month, etc.)
    # describe the closure event, not the consumer's pre-closure behaviour.
    # They belong in the DiD regression (Step 4), not in the displacement classifier.
    exclude = {
        # --- identifiers / bookkeeping ---
        "member_id", "dept_id", "closure_start", "closure_end",
        "period", "group", "label", "is_treated", "period_start", "period_end",
        # --- closure-event features ---
        "closure_length_days", "closure_start_month", "closure_start_weekday",
        "closure_start_season", "share_visited_stores_closed", "tenure_days",
    }
    feature_cols = [
        c for c in features_df.columns
        if c not in exclude and pd.api.types.is_numeric_dtype(features_df[c])
    ]

    print_variable_statistics(logger, features_df, feature_cols)

    # ---- Dataset statistics ---------------------------------------------
    log_print(logger, "\n" + "=" * 80)
    log_print(logger, "Selected Data Statistics")
    log_print(logger, "=" * 80)
    train_df    = features_df[features_df["period"] != 0]   # exclude control period 0 from training
    eval_pre    = features_df[features_df["period"] == -1]
    eval_during = features_df[(features_df["period"] == 0) & (features_df["group"] == "control")]

    log_print(logger, f"  Training observations:         {len(train_df):,}")
    log_print(logger, f"  Treatment Pre (t=-1) eval:     {len(eval_pre[eval_pre['group']=='treatment']):,}")
    log_print(logger, f"  Control Pre (t=-1) eval:       {len(eval_pre[eval_pre['group']=='control']):,}")
    log_print(logger, f"  Control During (t=0) eval:     {len(eval_during):,}")
    log_print(logger, f"  Label rate (train):            {train_df['label'].mean():.4f}")

    # ---- Prepare training data ------------------------------------------
    # compute_features_for_panel raises on any NaN so the matrix is NaN-free.
    X_train = train_df[feature_cols].copy()
    y_train = train_df["label"].values

    # ---- Train ----------------------------------------------------------
    use_gpu = check_gpu()
    log_print(logger, f"\nGPU available: {use_gpu}")

    try:
        import xgboost as xgb
        cfg_model = CONFIG["model"]
        params = {
            **cfg_model["xgb_params"],
            "device": "cuda" if use_gpu else "cpu",
            "n_jobs": -1 if not use_gpu else 1,
        }
        dtrain = xgb.DMatrix(X_train, label=y_train, feature_names=feature_cols)
        model  = xgb.train(params, dtrain, num_boost_round=cfg_model["num_boost_round"])

        save_model_artifacts(
            model=model,
            features_df=features_df,
            feature_cols=feature_cols,
            eval_pre=eval_pre,
            eval_during=eval_during,
            output_dir=OUTPUT_DIR,
            logger=logger,
        )

    except ImportError:
        log_print(logger, "XGBoost not installed. Install with: pip install xgboost")
    except Exception as e:
        log_print(logger, f"Training error: {e}", level="error")
        raise

    log_print(logger, "\n" + "=" * 80)
    log_print(logger, f"Completed at {datetime.now().isoformat()}")
    log_print(logger, "=" * 80)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Train the consumer displacement classification model."
    )
    parser.add_argument(
        "--sample", type=int, default=None,
        help="Limit panel rows for quick testing (e.g. 10000).",
    )
    parser.add_argument(
        "--max-closures", type=int, default=None,
        help="Use only the first N closures from store_closures.csv (e.g. 5).",
    )
    parser.add_argument(
        "--tail-closures", type=int, default=None,
        help="Use the last N closures from store_closures.csv (e.g. 20).",
    )
    args = parser.parse_args()

    if args.sample:
        os.environ["DISPLACEMENT_SAMPLE"] = str(args.sample)

    main(max_closures=args.max_closures, tail_closures=args.tail_closures)
