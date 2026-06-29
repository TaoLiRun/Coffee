from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from data import get_project_root, load_config
from menu_features import (
    build_and_save_menu_features,
    detect_menu_feature_paths,
    load_kept_closures,
)


def setup_logging(log_file: Path, log_level: str = "INFO") -> logging.Logger:
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("displacement_effect_estimation.menu_features")
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
    default_t_horizon = int(cfg.get("spec", {}).get("t_horizon", 4))
    project_root = get_project_root()
    default_output_dir = "outputs/04_diagnostics_18_closures/menu_features"

    parser = argparse.ArgumentParser(
        description="Construct closure-level, horizon-specific menu-change features."
    )
    parser.add_argument(
        "--t-horizon",
        type=int,
        default=default_t_horizon,
        help="Number of horizons h to compute, where each h compares [closure_start - hW, closure_start] with [closure_end, closure_end + hW].",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=default_output_dir,
        help="Directory, relative to project root, where menu-feature outputs are saved.",
    )
    parser.add_argument(
        "--chunksize",
        type=int,
        default=1_000_000,
        help="Chunk size used when reading processed product orders.",
    )
    parser.add_argument("--log-file", type=str, default=None, help="Path to log file.")
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        help="Logging level (DEBUG, INFO, WARNING, ERROR).",
    )
    args = parser.parse_args()

    if args.t_horizon < 1:
        raise ValueError("--t-horizon must be >= 1")

    output_dir = project_root / args.output_dir
    log_file = Path(args.log_file) if args.log_file else output_dir / "logs" / "run_menu_features.log"
    logger = setup_logging(log_file=log_file, log_level=args.log_level)

    paths = detect_menu_feature_paths(project_root=project_root)
    closures = load_kept_closures(paths=paths)

    logger.info("Starting menu-feature construction")
    logger.info("Using closure registry: %s", paths.closure_registry)
    logger.info("Using product orders: %s", paths.product_orders)
    logger.info("Using product mapping: %s", paths.product_mapping)
    logger.info(
        "Arguments: t_horizon=%s, output_dir=%s, chunksize=%s, kept_closures=%s",
        args.t_horizon,
        output_dir,
        args.chunksize,
        len(closures),
    )

    long_df, wide_df, detail_df = build_and_save_menu_features(
        t_horizon=args.t_horizon,
        output_dir=output_dir,
        chunksize=args.chunksize,
        paths=paths,
    )

    logger.info("Saved long output: %s rows", f"{len(long_df):,}")
    logger.info("Saved wide output: %s rows", f"{len(wide_df):,}")
    logger.info("Saved detail output: %s rows", f"{len(detail_df):,}")
    logger.info("Outputs written to: %s", output_dir)


if __name__ == "__main__":
    main()
