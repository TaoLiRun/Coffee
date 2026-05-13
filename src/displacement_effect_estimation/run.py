from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

from data import build_estimation_sample, get_project_root, load_config
from report import save_outputs, save_variety_panel_plot
from specs import fit_collapsed_specs, fit_event_study_specs


def setup_logging(log_file: Path, log_level: str = "INFO") -> logging.Logger:
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("displacement_effect_estimation")
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    logger.propagate = False

    logger.handlers.clear()

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def fit_spec_bundle(
    *,
    sample: pd.DataFrame,
    outcome: str,
    cluster_col: str,
    include_length_heterogeneity: bool,
    use_did: bool = False,
    variety_pre_novelty_heterogeneity: bool = False,
) -> dict[str, pd.DataFrame]:
    collapsed_terms, collapsed_fit = fit_collapsed_specs(
        df=sample,
        outcome=outcome,
        cluster_col=cluster_col,
        use_did=use_did,
        variety_pre_novelty_heterogeneity=variety_pre_novelty_heterogeneity,
    )
    event_terms, event_fit, pretrend_tests = fit_event_study_specs(
        df=sample,
        outcome=outcome,
        cluster_col=cluster_col,
        include_length_heterogeneity=include_length_heterogeneity,
        use_did=use_did,
    )
    if use_did:
        return {
            "binary_terms": collapsed_terms.copy(),
            "score_terms": pd.DataFrame(columns=collapsed_terms.columns),
            "binary_fit": collapsed_fit.copy(),
            "score_fit": pd.DataFrame(columns=collapsed_fit.columns),
            "event_terms": event_terms.copy(),
            "event_fit": event_fit.copy(),
            "pretrend_tests": pretrend_tests.copy(),
        }
    bin_spec_mask = collapsed_terms["spec"].str.startswith("binary_collapsed")
    bin_fit_mask = collapsed_fit["spec"].str.startswith("binary_collapsed")
    return {
        "binary_terms": collapsed_terms[bin_spec_mask].copy(),
        "score_terms": collapsed_terms[collapsed_terms["spec"] == "score_collapsed"].copy(),
        "binary_fit": collapsed_fit[bin_fit_mask].copy(),
        "score_fit": collapsed_fit[collapsed_fit["spec"] == "score_collapsed"].copy(),
        "event_terms": event_terms.copy(),
        "event_fit": event_fit.copy(),
        "pretrend_tests": pretrend_tests.copy(),
    }


def main() -> None:
    cfg = load_config()
    defaults = cfg["spec"]
    project_root = get_project_root()
    default_output_dir = cfg["paths"]["output_dir"]

    parser = argparse.ArgumentParser(description="Run parallel causal specs for displacement effect.")
    parser.add_argument("--t-horizon", type=int, default=defaults.get("t_horizon", 4), help="Number of pre/post bins to include (excluding t=0).")
    parser.add_argument("--outcome", type=str, default=defaults["outcome"])
    parser.add_argument("--cluster-col", type=str, default=defaults["cluster_col"])
    parser.add_argument(
        "--closure-duration-days",
        type=int,
        default=None,
        help="Restrict estimation to closures with this exact duration in days.",
    )
    parser.add_argument(
        "--separate-effect",
        action="store_true",
        default=None,
        help="Estimate one set of effects per closure/event instead of pooling all events.",
    )
    parser.add_argument(
        "--select-recency-consumers",
        type=int,
        default=None,
        help="Keep only consumers with a purchase in (closure_start - N, closure_start). Only valid with --separate-effect.",
    )
    parser.add_argument(
        "--no-balanced-panel",
        action="store_true",
        default=False,
        help=(
            "For outcome=variety_seeking: same as the default (unbalanced panel, DDD). "
            "Kept for backward compatibility; do not combine with --balanced-panel."
        ),
    )
    parser.add_argument(
        "--balanced-panel",
        action="store_true",
        default=False,
        help=(
            "For outcome=variety_seeking: drop member-closure pairs missing variety_seeking in "
            "any period and estimate DiD. Default is unbalanced panel with DDD."
        ),
    )
    parser.add_argument(
        "--no-unbalanced-panel",
        action="store_true",
        default=False,
        help=(
            "For outcome=n_purchases: restrict to members who purchased in every "
            "pre-period (balanced panel) and estimate a DiD model. Default is "
            "unbalanced panel with DDD."
        ),
    )
    parser.add_argument(
        "--variety-seeking-mode",
        type=str,
        choices=["distinct", "instance", "distinct-only-new"],
        default="distinct",
        help=(
            "For outcome=variety_seeking: 'distinct' (default) counts each product_id once "
            "per window (set cardinality); 'instance' counts every purchase row so repeated "
            "buys of the same product contribute proportionally; 'distinct-only-new' is the "
            "share of distinct products in the window whose global first-sale date falls in "
            "this window or the chronologically previous panel window (current window only for "
            "the leftmost pre period)."
        ),
    )
    parser.add_argument(
        "--keep-period0-purchasers",
        action="store_true",
        default=False,
        help=(
            "For outcome=variety_seeking: keep all member-closure pairs regardless of period-0 "
            "(closure-window) purchases. With --balanced-panel, treated members who purchase in "
            "period 0 and controls who do not are still dropped unless this flag is set."
        ),
    )
    parser.add_argument(
        "--variety-pre-novelty-heterogeneity",
        action="store_true",
        default=False,
        help=(
            "For outcome=variety_seeking with --variety-seeking-mode distinct and unbalanced DDD: "
            "split member-closure episodes by pre-period mean novelty vs sample median or mode "
            "(config spec.variety_pre_novelty_split_method), and fit an extended collapsed DDD "
            "with post×treatment×displacement interactions with the high-pre indicator."
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=default_output_dir,
        help="Directory, relative to project root, where estimation outputs are saved.",
    )
    parser.add_argument("--log-file", type=str, default=None, help="Path to log file.")
    parser.add_argument("--log-level", type=str, default="INFO", help="Logging level (DEBUG, INFO, WARNING, ERROR).")
    args = parser.parse_args()

    if args.balanced_panel and args.outcome != "variety_seeking":
        parser.error("--balanced-panel is only valid with --outcome variety_seeking")
    if args.outcome == "variety_seeking" and args.balanced_panel and args.no_balanced_panel:
        parser.error("Cannot combine --balanced-panel with --no-balanced-panel.")

    closure_duration_days = (
        args.closure_duration_days
        if args.closure_duration_days is not None
        else defaults.get("closure_duration_days", False)
    )
    separate_effect = (
        args.separate_effect if args.separate_effect is not None else bool(defaults.get("separate_effect", False))
    )
    select_recency_consumers = (
        args.select_recency_consumers
        if args.select_recency_consumers is not None
        else defaults.get("select_recency_consumers", False)
    )
    if args.variety_pre_novelty_heterogeneity:
        if args.outcome != "variety_seeking":
            parser.error("--variety-pre-novelty-heterogeneity requires --outcome variety_seeking")
        if args.variety_seeking_mode != "distinct":
            parser.error("--variety-pre-novelty-heterogeneity requires --variety-seeking-mode distinct")
        if args.balanced_panel:
            parser.error("--variety-pre-novelty-heterogeneity cannot be used with --balanced-panel")
        if separate_effect:
            parser.error("--variety-pre-novelty-heterogeneity cannot be used with --separate-effect")
    out_dir = project_root / args.output_dir
    log_file = Path(args.log_file) if args.log_file else out_dir / "logs" / "run.log"

    logger = setup_logging(log_file=log_file, log_level=args.log_level)
    logger.info("Starting displacement effect estimation run")
    if args.outcome == "variety_seeking":
        require_balanced_panel = bool(args.balanced_panel)
    else:
        require_balanced_panel = None if not args.no_balanced_panel else False
    drop_period0_purchasers = (
        args.outcome == "variety_seeking"
        and not args.keep_period0_purchasers
        and args.balanced_panel
    )
    unbalanced_panel = not args.no_unbalanced_panel
    # Determine model type: DiD for balanced variety panels; DDD for unbalanced variety;
    # purchase outcomes use --no-unbalanced-panel for DiD.
    if args.outcome == "variety_seeking":
        use_did = bool(args.balanced_panel)
    else:
        use_did = not unbalanced_panel

    logger.info(
        "Arguments: outcome=%s, t_horizon=%s, cluster_col=%s, closure_duration_days=%s, "
        "separate_effect=%s, select_recency_consumers=%s, require_balanced_panel=%s, "
        "drop_period0_purchasers=%s, "
        "variety_seeking_mode=%s, unbalanced_panel=%s, use_did=%s, "
        "variety_pre_novelty_heterogeneity=%s, output_dir=%s",
        args.outcome,
        args.t_horizon,
        args.cluster_col,
        closure_duration_days,
        separate_effect,
        select_recency_consumers,
        require_balanced_panel,
        drop_period0_purchasers,
        args.variety_seeking_mode,
        unbalanced_panel,
        use_did,
        args.variety_pre_novelty_heterogeneity,
        args.output_dir,
    )

    sample = build_estimation_sample(
        outcome=args.outcome,
        cfg=cfg,
        t_horizon=args.t_horizon,
        closure_duration_days=closure_duration_days,
        separate_effect=separate_effect,
        select_recency_consumers=select_recency_consumers,
        require_balanced_panel=require_balanced_panel,
        variety_seeking_mode=args.variety_seeking_mode,
        drop_period0_purchasers=drop_period0_purchasers,
        unbalanced_panel=unbalanced_panel,
        variety_pre_novelty_heterogeneity=args.variety_pre_novelty_heterogeneity,
    )
    logger.info("Built estimation sample: %s rows", f"{len(sample):,}")

    if separate_effect:
        separate_dir = out_dir / "separate_effect"
        separate_dir.mkdir(parents=True, exist_ok=True)

        event_index_rows: list[dict] = []
        event_groups = list(
            sample.groupby(["dept_id", "closure_start", "closure_end", "closure_event_id"], sort=False)
        )
        logger.info("Running separate estimation for %s closure events", len(event_groups))

        for event_idx, ((dept_id, closure_start, closure_end, closure_event_id), event_sample) in enumerate(event_groups, start=1):
            logger.info(
                "Fitting event %s/%s: closure_event_id=%s rows=%s members=%s",
                event_idx,
                len(event_groups),
                closure_event_id,
                f"{len(event_sample):,}",
                f"{event_sample['member_id'].nunique():,}",
            )
            results = fit_spec_bundle(
                sample=event_sample,
                outcome=args.outcome,
                cluster_col=args.cluster_col,
                include_length_heterogeneity=False,
                use_did=use_did,
                variety_pre_novelty_heterogeneity=args.variety_pre_novelty_heterogeneity,
            )
            event_output_dir = separate_dir / closure_event_id
            save_outputs(
                output_dir=event_output_dir,
                sample=event_sample,
                binary_terms=results["binary_terms"],
                binary_fit=results["binary_fit"],
                score_terms=results["score_terms"],
                score_fit=results["score_fit"],
                event_terms=results["event_terms"],
                event_fit=results["event_fit"],
                pretrend_tests=results["pretrend_tests"],
                summary_notes=[
                    "- Estimation mode: separate_effect=true",
                    f"- Closure event: `{closure_event_id}`",
                    f"- Closure duration filter days: {closure_duration_days}",
                    f"- Recency filter days: {select_recency_consumers}",
                    f"- Drop period-0 purchasers: {drop_period0_purchasers}",
                    "- Length-heterogeneity event-study spec skipped: true",
                    f"- Model type: {'DiD' if use_did else 'DDD'}",
                ],
            )
            if args.outcome == "variety_seeking":
                save_variety_panel_plot(
                    output_dir=event_output_dir,
                    sample=event_sample,
                    cfg=cfg,
                    variety_seeking_mode=args.variety_seeking_mode,
                )
            event_index_rows.append(
                {
                    "closure_event_id": closure_event_id,
                    "dept_id": dept_id,
                    "closure_start": closure_start,
                    "closure_end": closure_end,
                    "closure_duration_days": int(event_sample["closure_duration_days"].iloc[0]),
                    "members": event_sample["member_id"].nunique(),
                    "rows": len(event_sample),
                    "output_dir": str(event_output_dir.relative_to(project_root)),
                }
            )

        pd.DataFrame(event_index_rows).to_csv(separate_dir / "event_index.csv", index=False)
        logger.info("Saved separate-event outputs to: %s", separate_dir)
    else:
        results = fit_spec_bundle(
            sample=sample,
            outcome=args.outcome,
            cluster_col=args.cluster_col,
            include_length_heterogeneity=True,
            use_did=use_did,
            variety_pre_novelty_heterogeneity=args.variety_pre_novelty_heterogeneity,
        )
        logger.info("Fitted aggregate collapsed/event-study specs")
        agg_notes = [
            "- Estimation mode: separate_effect=false",
            f"- Closure duration filter days: {closure_duration_days}",
            f"- Recency filter days: {select_recency_consumers}",
            f"- Drop period-0 purchasers: {drop_period0_purchasers}",
            f"- Model type: {'DiD' if use_did else 'DDD'}",
        ]
        if args.variety_pre_novelty_heterogeneity:
            agg_notes.append(
                "- Pre-novelty heterogeneity: collapsed DDD includes post×(treatment, displacement)×high-pre split"
            )
        save_outputs(
            output_dir=out_dir,
            sample=sample,
            binary_terms=results["binary_terms"],
            binary_fit=results["binary_fit"],
            score_terms=results["score_terms"],
            score_fit=results["score_fit"],
            event_terms=results["event_terms"],
            event_fit=results["event_fit"],
            pretrend_tests=results["pretrend_tests"],
            summary_notes=agg_notes,
        )
        if args.outcome == "variety_seeking":
            save_variety_panel_plot(
                output_dir=out_dir,
                sample=sample,
                cfg=cfg,
                variety_seeking_mode=args.variety_seeking_mode,
            )
        logger.info("Saved outputs to: %s", out_dir)

    logger.info("Rows in estimation sample: %s", f"{len(sample):,}")


if __name__ == "__main__":
    main()
