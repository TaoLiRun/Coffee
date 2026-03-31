"""
Entry point for the displacement classification pipeline.

Usage
-----
    python main.py
    python main.py --max-closures 20
    python main.py --tail-closures 20
    python main.py --sample 50000 --max-closures 5
    python main.py --max-closures 1 --max-members 10   # smoke test (registry-kept closure + 10 members)

See --help for all options.
"""

from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import numpy as np
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
    build_t0_ex_ante_panel,
    compute_features_for_panel,
    load_or_build_closure_pair_registry,
    filter_closures_to_registry_kept,
    parse_control_store_ids,
    USE_SET_UP_TIME_MATCHED_CONTROL,
    get_treatment_and_control_members_for_closure,
    USE_SET_UP_TIME_MATCHED_CONTROL,
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
from push_event_cache import load_or_build_push_events_cache
from feature_matrix_cache import (
    feature_matrix_cache_key,
    save_feature_matrix_cache,
    try_load_feature_matrix_cache,
)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(
    max_closures: Optional[int] = None,
    tail_closures: Optional[int] = None,
    *,
    max_members: Optional[int] = None,
    rebuild_push_cache: bool = False,
    rebuild_feature_cache: bool = False,
) -> None:
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

    closures = filter_closures_to_registry_kept(logger, closures)

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
    t0_panel = build_t0_ex_ante_panel(
        logger, df_order_full, closures, customer_preference, unique_visits,
    )

    if max_members is not None:
        mids = panel["member_id"].unique()
        if len(mids) > max_members:
            rng = np.random.RandomState(42)
            keep = set(rng.choice(mids, size=max_members, replace=False).tolist())
            panel = panel[panel["member_id"].isin(keep)].copy()
            if not t0_panel.empty:
                t0_panel = t0_panel[t0_panel["member_id"].isin(keep)].copy()
            df_order_full = df_order_full[df_order_full["member_id"].isin(keep)].copy()
            log_print(logger, f"  [DEBUG] Limited to {max_members} member(s) for testing")

    members_for_push = set(panel["member_id"].unique())
    if not t0_panel.empty:
        members_for_push |= set(t0_panel["member_id"].unique())
    earliest_date = pd.Timestamp(df_order_full["date"].min())
    period_max = pd.Timestamp(panel["period_start"].max())
    if not t0_panel.empty:
        period_max = max(period_max, pd.Timestamp(t0_panel["period_start"].max()))
    t_max = period_max - pd.Timedelta(days=1)

    run_flags = {
        "displacement_sample": os.environ.get("DISPLACEMENT_SAMPLE"),
        "max_closures": max_closures,
        "tail_closures": tail_closures,
        "max_members": max_members,
    }
    fm_key = feature_matrix_cache_key(
        closures=closures,
        members_for_push=members_for_push,
        earliest_date=earliest_date,
        t_max=t_max,
        run_flags=run_flags,
        use_set_up_time_matched_control=USE_SET_UP_TIME_MATCHED_CONTROL,
    )

    cached = None
    if not rebuild_feature_cache:
        cached = try_load_feature_matrix_cache(logger=logger, cache_key=fm_key)

    if cached is not None:
        features_df, t0_features_df = cached
        log_print(
            logger,
            "\nUsing cached feature matrices (skipping push load and compute_features_for_panel).",
        )
    else:
        df_push = load_or_build_push_events_cache(
            logger,
            members_for_push=members_for_push,
            earliest_date=earliest_date,
            t_max=t_max,
            rebuild=rebuild_push_cache,
        )

        features_df = compute_features_for_panel(
            logger, panel, df_order_full, member_demographics,
            df_push_events=df_push,
        )
        if t0_panel.empty:
            log_print(logger, "  Ex-ante t0 panel is empty; no t0 scores will be generated.", level="warning")
            t0_features_df = pd.DataFrame()
        else:
            t0_features_df = compute_features_for_panel(
                logger, t0_panel, df_order_full, member_demographics,
                df_push_events=df_push,
            )
        save_feature_matrix_cache(
            logger=logger,
            features_df=features_df,
            t0_features_df=t0_features_df,
            cache_key=fm_key,
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
        t0_score_chunks = []

        for D in durations:
            sub = features_df[features_df["closure_duration_days"] == D]
            train_df = sub[sub["period"] <= -2]
            eval_pre = sub[sub["period"] == -1]
            eval_during = sub[(sub["period"] == 0) & (sub["group"] == "control")]
            t0_sub = (
                t0_features_df[t0_features_df["closure_duration_days"] == D].copy()
                if not t0_features_df.empty
                else pd.DataFrame()
            )

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

            if not t0_sub.empty:
                dt0 = xgb.DMatrix(t0_sub[feature_cols], feature_names=feature_cols)
                t0_sub["displacement_prob_t0_ex_ante"] = model.predict(dt0)
                threshold = cfg_model.get("classification_threshold", 0.5)
                t0_sub["predicted_displaced_t0_ex_ante"] = (
                    t0_sub["displacement_prob_t0_ex_ante"] >= threshold
                ).astype(int)
                t0_score_chunks.append(
                    t0_sub[
                        [
                            "member_id",
                            "dept_id",
                            "closure_start",
                            "closure_end",
                            "closure_duration_days",
                            "group",
                            "is_treated",
                            "score_time",
                            "displacement_prob_t0_ex_ante",
                            "predicted_displaced_t0_ex_ante",
                        ]
                    ]
                )

        if t0_score_chunks:
            t0_scores = pd.concat(t0_score_chunks, ignore_index=True)
            t0_scores_path = OUTPUT_DIR / "displacement_scores_t0_ex_ante.csv"
            t0_scores.to_csv(t0_scores_path, index=False)
            log_print(logger, f"\nSaved ex-ante t0 scores: {t0_scores_path} ({len(t0_scores):,} rows)")
        else:
            log_print(logger, "\nNo ex-ante t0 scores generated (all duration slices empty).", level="warning")

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
    parser.add_argument(
        "--rebuild-push-cache",
        action="store_true",
        help="Rebuild filtered push-event parquet even if cache exists.",
    )
    parser.add_argument(
        "--rebuild-feature-cache",
        action="store_true",
        help="Ignore cached feature-matrix parquet(s) and recompute (still uses push cache unless --rebuild-push-cache).",
    )
    parser.add_argument(
        "--max-members",
        type=int,
        default=None,
        help="Keep at most this many distinct member_ids (random subset; for smoke tests).",
    )
    args = parser.parse_args()

    if args.sample:
        os.environ["DISPLACEMENT_SAMPLE"] = str(args.sample)

    main(
        max_closures=args.max_closures,
        tail_closures=args.tail_closures,
        max_members=args.max_members,
        rebuild_push_cache=args.rebuild_push_cache,
        rebuild_feature_cache=args.rebuild_feature_cache,
    )
