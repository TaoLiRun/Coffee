from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--estimator", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def load_estimator(path: Path):
    spec = importlib.util.spec_from_file_location("noncoffee_estimator", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main() -> None:
    args = parse_args()
    module = load_estimator(args.estimator.resolve())
    output_dir = args.output_dir.resolve()
    panel = pd.read_parquet(output_dir / "noncoffee_novelty_panel.parquet")
    event_frames = []
    pretrend_frames = []
    for scope in module.SCOPES:
        outcome = f"any_purchase_{scope}"
        event, pretrend = module.fit_event_study(panel, outcome, scope)
        event_frames.append(event)
        pretrend_frames.append(pretrend)
    events = pd.concat(event_frames, ignore_index=True)
    pretrends = pd.concat(pretrend_frames, ignore_index=True)
    events.to_csv(output_dir / "entry_event_study_results.csv", index=False)
    pretrends.to_csv(output_dir / "entry_pretrend_tests.csv", index=False)
    print(
        pretrends[pretrends["test"].eq("pretrend_ddd_joint_zero")].to_string(
            index=False
        )
    )
    print(
        events[events["component"].eq("high_minus_low_ddd")][
            ["scope", "rel_t", "coef", "se", "pvalue"]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()
