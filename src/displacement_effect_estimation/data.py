from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import pandas as pd


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_config() -> dict:
    cfg_path = Path(__file__).resolve().parent / "config.json"
    with open(cfg_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _normalize_closure_start(s: pd.Series) -> pd.Series:
    return pd.to_datetime(s, errors="coerce").dt.strftime("%Y-%m-%d")


def load_period_behavior(window_days: int, cfg: dict | None = None) -> pd.DataFrame:
    cfg = cfg or load_config()
    project_root = get_project_root()
    pattern = cfg["paths"]["period_behavior_pattern"].format(window=window_days)
    path = project_root / pattern
    if not path.exists():
        raise FileNotFoundError(f"Period behavior file not found: {path}")

    df = pd.read_csv(path, encoding="utf-8-sig")
    required = {"member_id", "dept_id", "closure_start", "group", "period"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in {path}: {sorted(missing)}")

    df = df.copy()
    df["closure_start"] = _normalize_closure_start(df["closure_start"])
    return df


def load_displacement_scores(score_period: int, cfg: dict | None = None) -> pd.DataFrame:
    cfg = cfg or load_config()
    project_root = get_project_root()
    scores_dir = project_root / cfg["paths"]["scores_dir"]
    files = sorted(scores_dir.glob("displacement_scores_*.csv"))
    if not files:
        raise FileNotFoundError(f"No displacement score files found in: {scores_dir}")

    frames = []
    for file_path in files:
        df = pd.read_csv(file_path, encoding="utf-8-sig")
        required = {"member_id", "dept_id", "closure_start", "period", "displacement_prob"}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns in {file_path.name}: {sorted(missing)}")
        frames.append(df)

    all_scores = pd.concat(frames, ignore_index=True)
    all_scores["closure_start"] = _normalize_closure_start(all_scores["closure_start"])
    score_df = all_scores[all_scores["period"] == score_period].copy()
    if score_df.empty:
        raise ValueError(f"No score rows found at period={score_period}")

    key_cols = ["member_id", "dept_id", "closure_start"]
    score_df = (
        score_df.sort_values(key_cols)
        .drop_duplicates(subset=key_cols, keep="first")
        .loc[:, key_cols + ["displacement_prob"]]
    )
    return score_df


def build_estimation_sample(
    window_days: int,
    outcome: str,
    score_period: int,
    thresholds: Iterable[float],
    cfg: dict | None = None,
) -> pd.DataFrame:
    cfg = cfg or load_config()
    panel = load_period_behavior(window_days=window_days, cfg=cfg)
    scores = load_displacement_scores(score_period=score_period, cfg=cfg)

    if outcome not in panel.columns:
        raise ValueError(f"Outcome '{outcome}' is not in period behavior columns")

    panel = panel[panel["period"].isin(["pre", "post"])].copy()
    panel["post"] = (panel["period"] == "post").astype(int)
    panel["treated"] = (panel["group"] == "treatment").astype(int)
    panel["closure_start"] = _normalize_closure_start(panel["closure_start"])

    merged = panel.merge(
        scores,
        on=["member_id", "dept_id", "closure_start"],
        how="left",
    )

    merged = merged.dropna(subset=["displacement_prob", outcome]).copy()
    merged["displacement_prob"] = merged["displacement_prob"].astype(float)

    for tau in thresholds:
        tag = str(tau).replace(".", "")
        merged[f"disp_{tag}"] = (merged["displacement_prob"] >= tau).astype(int)

    return merged
