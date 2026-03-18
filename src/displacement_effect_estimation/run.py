from __future__ import annotations

import argparse

from data import build_estimation_sample, get_project_root, load_config
from report import save_outputs
from specs import fit_event_study_specs, fit_score_spec, fit_threshold_specs


def _parse_thresholds(text: str) -> list[float]:
    vals = [x.strip() for x in text.split(",") if x.strip()]
    if not vals:
        raise ValueError("threshold list is empty")
    return [float(v) for v in vals]


def main() -> None:
    cfg = load_config()
    defaults = cfg["spec"]

    parser = argparse.ArgumentParser(description="Run parallel causal specs for displacement effect.")
    parser.add_argument("--window", type=int, default=defaults["window_days"], help="Length (days) of each pre/post event-study bin.")
    parser.add_argument("--t-horizon", type=int, default=defaults.get("t_horizon", 4), help="Number of pre/post bins to include (excluding t=0).")
    parser.add_argument("--outcome", type=str, default=defaults["outcome"])
    parser.add_argument("--thresholds", type=str, default=",".join(str(x) for x in defaults["thresholds"]))
    parser.add_argument("--cluster-col", type=str, default=defaults["cluster_col"])
    args = parser.parse_args()

    thresholds = _parse_thresholds(args.thresholds)
    sample = build_estimation_sample(
        window_days=args.window,
        outcome=args.outcome,
        thresholds=thresholds,
        cfg=cfg,
        t_horizon=args.t_horizon,
    )

    threshold_terms, threshold_fit = fit_threshold_specs(
        sample,
        outcome=args.outcome,
        thresholds=thresholds,
        cluster_col=args.cluster_col,
    )
    score_terms, score_fit = fit_score_spec(
        sample,
        outcome=args.outcome,
        cluster_col=args.cluster_col,
    )
    event_terms, event_fit = fit_event_study_specs(
        sample,
        outcome=args.outcome,
        thresholds=thresholds,
        cluster_col=args.cluster_col,
    )

    out_dir = get_project_root() / cfg["paths"]["output_dir"]
    save_outputs(
        output_dir=out_dir,
        sample=sample,
        threshold_terms=threshold_terms,
        threshold_fit=threshold_fit,
        score_terms=score_terms,
        score_fit=score_fit,
        event_terms=event_terms,
        event_fit=event_fit,
    )

    print(f"Saved outputs to: {out_dir}")
    print(f"Rows in estimation sample: {len(sample):,}")


if __name__ == "__main__":
    main()
