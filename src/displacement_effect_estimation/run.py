from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from data import build_estimation_sample, get_project_root, load_config
from report import save_outputs
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


def main() -> None:
    cfg = load_config()
    defaults = cfg["spec"]
    project_root = get_project_root()
    default_log_file = project_root / cfg["paths"]["output_dir"] / "logs" / "run.log"

    parser = argparse.ArgumentParser(description="Run parallel causal specs for displacement effect.")
    parser.add_argument("--t-horizon", type=int, default=defaults.get("t_horizon", 4), help="Number of pre/post bins to include (excluding t=0).")
    parser.add_argument("--outcome", type=str, default=defaults["outcome"])
    parser.add_argument("--cluster-col", type=str, default=defaults["cluster_col"])
    parser.add_argument("--log-file", type=str, default=str(default_log_file), help="Path to log file.")
    parser.add_argument("--log-level", type=str, default="INFO", help="Logging level (DEBUG, INFO, WARNING, ERROR).")
    args = parser.parse_args()

    logger = setup_logging(Path(args.log_file), args.log_level)
    logger.info("Starting displacement effect estimation run")
    logger.info("Arguments: outcome=%s, t_horizon=%s, cluster_col=%s", args.outcome, args.t_horizon, args.cluster_col)

    sample = build_estimation_sample(
        outcome=args.outcome,
        cfg=cfg,
        t_horizon=args.t_horizon,
    )
    logger.info("Built estimation sample: %s rows", f"{len(sample):,}")

    collapsed_terms, collapsed_fit = fit_collapsed_specs(
        sample,
        outcome=args.outcome,
        cluster_col=args.cluster_col,
    )
    binary_terms = collapsed_terms[collapsed_terms["spec"] == "binary_collapsed"].copy()
    score_terms = collapsed_terms[collapsed_terms["spec"] == "score_collapsed"].copy()
    binary_fit = collapsed_fit[collapsed_fit["spec"] == "binary_collapsed"].copy()
    score_fit = collapsed_fit[collapsed_fit["spec"] == "score_collapsed"].copy()
    logger.info("Fitted collapsed binary/score DDD specs")
    event_terms, event_fit, pretrend_tests = fit_event_study_specs(
        sample,
        outcome=args.outcome,
        cluster_col=args.cluster_col,
    )
    logger.info("Fitted event-study specs and pre-trend tests")

    out_dir = project_root / cfg["paths"]["output_dir"]
    save_outputs(
        output_dir=out_dir,
        sample=sample,
        binary_terms=binary_terms,
        binary_fit=binary_fit,
        score_terms=score_terms,
        score_fit=score_fit,
        event_terms=event_terms,
        event_fit=event_fit,
        pretrend_tests=pretrend_tests,
    )

    logger.info("Saved outputs to: %s", out_dir)
    logger.info("Rows in estimation sample: %s", f"{len(sample):,}")


if __name__ == "__main__":
    main()
