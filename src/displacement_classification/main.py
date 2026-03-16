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
    load_or_build_closure_pair_registry,
    parse_control_store_ids,
    USE_SET_UP_TIME_MATCHED_CONTROL,
    get_treatment_and_control_members_for_closure,
    # Constants
    CLOSURES_CSV,
    OUTPUT_DIR,
    CONFIG,
    # Re-exported from analyze_closure_impact
    DEFAULT_LOWEST_PURCHASES,
    DEFAULT_LOWEST_RATIO,
    get_customer_store_preference,
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

    # Retain only closures where closure_start is on or after the filter date
    # (CONFIG["data"]["closure_filter_start"]).  Panel building further skips
    # closures that do not have enough history for num_pre_periods of length D.
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
    pair_registry = load_or_build_closure_pair_registry(
        logger, df_order_full, closures, customer_preference, unique_visits
    )
    reg_map = {
        (int(r["dept_id"]), pd.to_datetime(r["closure_start"]).strftime("%Y-%m-%d")): r
        for _, r in pair_registry.iterrows()
    }

    for _, closure in closures.iterrows():
        dept_id = int(closure["dept_id"])
        key = (dept_id, pd.to_datetime(closure["closure_start"]).strftime("%Y-%m-%d"))
        reg_row = reg_map.get(key)
        if reg_row is None or reg_row.get("status") != "kept":
            continue

        control_stores = parse_control_store_ids(reg_row.get("control_store_ids", ""))
        treated, ctrl, _ = get_treatment_and_control_members_for_closure(
            unique_visits=unique_visits,
            customer_preference=customer_preference,
            closure=closure,
            lowest_purchases=DEFAULT_LOWEST_PURCHASES,
            lowest_ratio=DEFAULT_LOWEST_RATIO,
            use_set_up_time_matched_control=USE_SET_UP_TIME_MATCHED_CONTROL,
            control_pool=None,
            control_stores_by_closure={(dept_id, closure["closure_start"]): control_stores},
        )

        all_treated_members.update(treated)
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
    # closure_length_days / closure_duration_days are not used as features.
    exclude = {
        # --- identifiers / bookkeeping ---
        "member_id", "dept_id", "closure_start", "closure_end",
        "period", "group", "label", "is_treated", "period_start", "period_end",
        # --- closure-event features ---
        "closure_length_days", "closure_duration_days", "closure_start_month",
        "closure_start_weekday", "closure_start_season",
        "share_visited_stores_closed", "tenure_days",
    }
    feature_cols = [
        c for c in features_df.columns
        if c not in exclude and pd.api.types.is_numeric_dtype(features_df[c])
    ]

    print_variable_statistics(logger, features_df, feature_cols)

    # ---- Label imbalance audit (from data) ------------------------------
    log_print(logger, "\n" + "=" * 80)
    log_print(logger, "Label balance audit (by closure_duration_days)")
    log_print(logger, "=" * 80)
    audit_rows = []
    for D in sorted(features_df["closure_duration_days"].unique()):
        sub = features_df[features_df["closure_duration_days"] == D]
        train_sub = sub[sub["period"] <= -2]
        eval_pre_sub = sub[sub["period"] == -1]
        eval_during_sub = sub[(sub["period"] == 0) & (sub["group"] == "control")]
        for slice_name, slice_df in [
            ("train", train_sub),
            ("eval_pre_treatment", eval_pre_sub[eval_pre_sub["group"] == "treatment"]),
            ("eval_pre_control", eval_pre_sub[eval_pre_sub["group"] == "control"]),
            ("eval_during", eval_during_sub),
        ]:
            if slice_df.empty:
                continue
            n = len(slice_df)
            n_pos = slice_df["label"].sum()
            rate = n_pos / n if n else 0
            audit_rows.append({
                "closure_duration_days": D,
                "slice": slice_name,
                "n_rows": n,
                "n_positive": int(n_pos),
                "label_rate": round(rate, 4),
            })
            log_print(logger, f"  D={D} {slice_name}: n={n:,}, n_positive={int(n_pos):,}, label_rate={rate:.4f}")
    if audit_rows:
        audit_df = pd.DataFrame(audit_rows)
        audit_path = OUTPUT_DIR / "label_balance_audit.csv"
        audit_df.to_csv(audit_path, index=False)
        log_print(logger, f"  Saved {audit_path}")

    # ---- Train one model per unique closure_duration_days ---------------
    use_gpu = check_gpu()
    log_print(logger, f"\nGPU available: {use_gpu}")

    try:
        import xgboost as xgb
        cfg_model = CONFIG["model"]
        params_base = {
            **cfg_model["xgb_params"],
            "device": "cuda" if use_gpu else "cpu",
            "n_jobs": -1 if not use_gpu else 1,
        }
        durations = sorted(features_df["closure_duration_days"].unique())
        log_print(logger, f"\nTraining {len(durations)} model(s), one per duration: {durations}")

        for D in durations:
            sub = features_df[features_df["closure_duration_days"] == D]
            train_df = sub[sub["period"] <= -2]
            eval_pre = sub[sub["period"] == -1]
            eval_during = sub[(sub["period"] == 0) & (sub["group"] == "control")]

            if train_df.empty:
                log_print(logger, f"  Duration D={D}: no training rows, skipping.")
                continue

            X_train = train_df[feature_cols].copy()
            y_train = train_df["label"].values
            dtrain = xgb.DMatrix(X_train, label=y_train, feature_names=feature_cols)
            model = xgb.train(
                params_base, dtrain,
                num_boost_round=cfg_model["num_boost_round"],
            )

            log_print(logger, f"\n  Duration D={D}: train n={len(train_df):,}, eval_pre n={len(eval_pre):,}, eval_during n={len(eval_during):,}")
            save_model_artifacts(
                model=model,
                features_df=sub,
                feature_cols=feature_cols,
                eval_pre=eval_pre,
                eval_during=eval_during,
                output_dir=OUTPUT_DIR,
                logger=logger,
                model_suffix=str(D),
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
