from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import scipy.stats as st
import statsmodels.formula.api as smf


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]
CONFIG_PATH = SCRIPT_DIR / "config.json"


def load_config(*, config_path: Path = CONFIG_PATH) -> dict[str, Any]:
    with open(config_path, encoding="utf-8") as f:
        return json.load(f)


def project_path(*, relative_path: str) -> Path:
    return (PROJECT_ROOT / relative_path).resolve()


def normalize_date(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, errors="coerce").dt.normalize()


def build_event_id(*, df: pd.DataFrame) -> pd.Series:
    return (
        "dept_"
        + df["dept_id"].astype(int).astype(str)
        + "_closure_"
        + normalize_date(df["closure_start"]).dt.strftime("%Y-%m-%d")
    )


def load_selected_scores(*, cfg: dict[str, Any]) -> pd.DataFrame:
    paths_cfg = cfg["paths"]
    registry_path = project_path(relative_path=paths_cfg["selected_closure_registry"])
    score_path = project_path(relative_path=paths_cfg["score_file"])

    registry = pd.read_csv(registry_path, encoding="utf-8-sig")
    registry_required = {"dept_id", "closure_start", "closure_end", "closure_duration_days"}
    registry_missing = registry_required - set(registry.columns)
    if registry_missing:
        raise ValueError(f"Missing selected registry columns: {sorted(registry_missing)}")

    registry = registry.assign(
        dept_id=registry["dept_id"].astype(int),
        closure_start=normalize_date(registry["closure_start"]),
        closure_end=normalize_date(registry["closure_end"]),
        closure_duration_days=pd.to_numeric(
            registry["closure_duration_days"], errors="raise"
        ).astype(int),
    )
    registry = registry[
        ["dept_id", "closure_start", "closure_end", "closure_duration_days"]
    ].drop_duplicates()

    scores = pd.read_csv(score_path, encoding="utf-8-sig")
    score_required = {
        "member_id",
        "dept_id",
        "closure_start",
        "closure_end",
        "closure_duration_days",
        "group",
        "is_treated",
        "displacement_prob_t0_ex_ante",
        "predicted_displaced_t0_ex_ante",
    }
    score_missing = score_required - set(scores.columns)
    if score_missing:
        raise ValueError(f"Missing score columns: {sorted(score_missing)}")

    scores = scores.assign(
        member_id=scores["member_id"].astype(int),
        dept_id=scores["dept_id"].astype(int),
        closure_start=normalize_date(scores["closure_start"]),
        closure_end=normalize_date(scores["closure_end"]),
        closure_duration_days=pd.to_numeric(
            scores["closure_duration_days"], errors="raise"
        ).astype(int),
        is_treated=scores["is_treated"].astype(int),
        predicted_purchase_intention=scores["predicted_displaced_t0_ex_ante"].astype(int),
        displacement_prob=scores["displacement_prob_t0_ex_ante"].astype(float),
    )

    key_cols = ["dept_id", "closure_start", "closure_end", "closure_duration_days"]
    scores = scores.merge(
        registry,
        on=key_cols,
        how="inner",
        validate="many_to_one",
    )
    scores["closure_event_id"] = build_event_id(df=scores)
    scores["treated"] = scores["is_treated"].astype(int)

    out_cols = [
        "member_id",
        "dept_id",
        "closure_start",
        "closure_end",
        "closure_duration_days",
        "closure_event_id",
        "group",
        "is_treated",
        "treated",
        "displacement_prob",
        "predicted_purchase_intention",
    ]
    scores = scores[out_cols].drop_duplicates(
        subset=["member_id", "dept_id", "closure_start"], keep="first"
    )
    return scores.sort_values(["closure_start", "dept_id", "member_id"]).reset_index(drop=True)


def build_post_windows(*, selected_scores: pd.DataFrame, rel_t_values: list[int]) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for rel_t in rel_t_values:
        frame = selected_scores.copy()
        duration = frame["closure_duration_days"].astype(int)
        post_anchor = frame["closure_end"] + pd.Timedelta(days=1)
        frame["rel_t"] = int(rel_t)
        frame["period_start"] = post_anchor + pd.to_timedelta((rel_t - 1) * duration, unit="D")
        frame["period_end"] = frame["period_start"] + pd.to_timedelta(duration - 1, unit="D")
        frame["window_days"] = duration
        frame["calendar_month"] = frame["period_start"].dt.strftime("%Y-%m")
        frame["member_event_window_id"] = (
            frame["member_id"].astype(str)
            + "_"
            + frame["closure_event_id"].astype(str)
            + "_rel_"
            + frame["rel_t"].astype(str)
        )
        frames.append(frame)
    return pd.concat(frames, ignore_index=True)


def list_push_paths(*, cfg: dict[str, Any]) -> list[Path]:
    paths_cfg = cfg["paths"]
    push_dir = project_path(relative_path=paths_cfg["push_data_dir"])
    return sorted(push_dir.glob(paths_cfg["push_file_pattern"]))


def filter_push_records(*, cfg: dict[str, Any], windows: pd.DataFrame) -> pd.DataFrame:
    analysis_cfg = cfg["analysis"]
    processing_cfg = cfg["processing"]
    push_paths = list_push_paths(cfg=cfg)
    if not push_paths:
        raise FileNotFoundError("No push files matched the configured pattern.")

    member_ids = set(windows["member_id"].astype(int).tolist())
    min_dt = windows["period_start"].min()
    max_dt = windows["period_end"].max()
    window_cols = [
        "member_id",
        "dept_id",
        "closure_start",
        "closure_end",
        "closure_duration_days",
        "closure_event_id",
        "group",
        "is_treated",
        "treated",
        "predicted_purchase_intention",
        "displacement_prob",
        "rel_t",
        "period_start",
        "period_end",
        "window_days",
        "calendar_month",
        "member_event_window_id",
    ]
    windows_for_merge = windows[window_cols].copy()

    records: list[pd.DataFrame] = []
    for push_path in push_paths:
        for chunk in pd.read_csv(
            push_path,
            encoding="utf-8-sig",
            usecols=lambda col: col in analysis_cfg["push_columns"],
            chunksize=int(processing_cfg["chunksize"]),
        ):
            chunk = chunk.dropna(subset=["dt", "member_id"]).copy()
            if chunk.empty:
                continue
            chunk["member_id"] = chunk["member_id"].astype(int)
            chunk = chunk[chunk["member_id"].isin(member_ids)].copy()
            if chunk.empty:
                continue
            chunk["dt"] = normalize_date(chunk["dt"])
            chunk = chunk[(chunk["dt"] >= min_dt) & (chunk["dt"] <= max_dt)].copy()
            if chunk.empty:
                continue
            chunk["coupon"] = pd.to_numeric(chunk["coupon"], errors="coerce")
            chunk["discount"] = pd.to_numeric(chunk["discount"], errors="coerce")
            matched = chunk.merge(
                windows_for_merge,
                on="member_id",
                how="inner",
                validate="many_to_many",
            )
            matched = matched[
                (matched["dt"] >= matched["period_start"])
                & (matched["dt"] <= matched["period_end"])
            ].copy()
            if not matched.empty:
                records.append(matched)

    if not records:
        return pd.DataFrame(
            columns=[
                "dt",
                "member_id",
                "policy_id",
                "coupon",
                "discount",
                *window_cols[1:],
            ]
        )
    return pd.concat(records, ignore_index=True).sort_values(
        ["closure_start", "dept_id", "member_id", "rel_t", "dt"]
    ).reset_index(drop=True)


def build_push_panel(*, windows: pd.DataFrame, push_records: pd.DataFrame) -> pd.DataFrame:
    panel = windows.copy()
    metric_defaults = {
        "n_push": 0,
        "n_push_with_coupon": 0,
        "n_push_with_discount": 0,
        "mean_coupon": 0.0,
        "mean_discount": 0.0,
        "n_distinct_policy": 0,
    }
    if push_records.empty:
        for col, value in metric_defaults.items():
            panel[col] = value
    else:
        records = push_records.copy()
        records["coupon_value"] = records["coupon"].fillna(0.0)
        records["discount_value"] = records["discount"].fillna(0.0)
        records["has_coupon"] = records["coupon_value"].ne(0.0).astype(int)
        records["has_discount"] = records["discount_value"].ne(0.0).astype(int)
        grouped = (
            records.groupby("member_event_window_id", sort=False)
            .agg(
                n_push=("dt", "size"),
                n_push_with_coupon=("has_coupon", "sum"),
                n_push_with_discount=("has_discount", "sum"),
                mean_coupon=("coupon_value", "mean"),
                mean_discount=("discount_value", "mean"),
                n_distinct_policy=("policy_id", "nunique"),
            )
            .reset_index()
        )
        panel = panel.merge(
            grouped,
            on="member_event_window_id",
            how="left",
            validate="one_to_one",
        )
        for col, value in metric_defaults.items():
            panel[col] = panel[col].fillna(value)

    panel["n_push"] = panel["n_push"].astype(int)
    panel["n_push_with_coupon"] = panel["n_push_with_coupon"].astype(int)
    panel["n_push_with_discount"] = panel["n_push_with_discount"].astype(int)
    panel["n_distinct_policy"] = panel["n_distinct_policy"].astype(int)
    panel["push_per_day"] = panel["n_push"] / panel["window_days"]
    panel["share_push_coupon"] = np.where(
        panel["n_push"].gt(0),
        panel["n_push_with_coupon"] / panel["n_push"],
        0.0,
    )
    panel["share_push_discount"] = np.where(
        panel["n_push"].gt(0),
        panel["n_push_with_discount"] / panel["n_push"],
        0.0,
    )
    return panel.sort_values(
        ["closure_start", "dept_id", "member_id", "rel_t"]
    ).reset_index(drop=True)


def summarize_groups(*, panel: pd.DataFrame, metrics: list[str]) -> pd.DataFrame:
    return (
        panel.groupby(["treated", "predicted_purchase_intention"], sort=True)[metrics]
        .agg(["count", "mean", "std", "median"])
        .reset_index()
    )


def flatten_columns(*, df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [
        "_".join([str(part) for part in col if str(part)])
        if isinstance(col, tuple)
        else str(col)
        for col in out.columns
    ]
    return out


def confidence_interval_from_diff(
    *,
    diff: float,
    se: float,
    dfree: float,
    confidence_level: float,
) -> tuple[float, float]:
    alpha = 1.0 - confidence_level
    critical = float(st.t.ppf(1.0 - alpha / 2.0, dfree))
    return diff - critical * se, diff + critical * se


def welch_mean_tests(*, panel: pd.DataFrame, metrics: list[str], confidence_level: float) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for treated_value, treatment_panel in panel.groupby("treated", sort=True):
        for metric in metrics:
            group0 = treatment_panel.loc[
                treatment_panel["predicted_purchase_intention"].eq(0), metric
            ].astype(float)
            group1 = treatment_panel.loc[
                treatment_panel["predicted_purchase_intention"].eq(1), metric
            ].astype(float)
            n0 = int(group0.shape[0])
            n1 = int(group1.shape[0])
            mean0 = float(group0.mean())
            mean1 = float(group1.mean())
            var0 = float(group0.var(ddof=1))
            var1 = float(group1.var(ddof=1))
            se = math.sqrt(var0 / n0 + var1 / n1)
            numerator = (var0 / n0 + var1 / n1) ** 2
            denominator = ((var0 / n0) ** 2 / (n0 - 1)) + ((var1 / n1) ** 2 / (n1 - 1))
            dfree = float(numerator / denominator)
            diff = mean1 - mean0
            t_stat = diff / se
            pvalue = float(2.0 * st.t.sf(abs(t_stat), dfree))
            ci_low, ci_high = confidence_interval_from_diff(
                diff=diff,
                se=se,
                dfree=dfree,
                confidence_level=confidence_level,
            )
            rows.append(
                {
                    "treated": int(treated_value),
                    "sample": "treatment" if int(treated_value) == 1 else "control",
                    "metric": metric,
                    "comparison": "predicted_1_minus_0",
                    "n_predicted_0": n0,
                    "n_predicted_1": n1,
                    "mean_predicted_0": mean0,
                    "mean_predicted_1": mean1,
                    "difference": diff,
                    "se": se,
                    "t_stat": t_stat,
                    "df": dfree,
                    "pvalue": pvalue,
                    "ci_low": ci_low,
                    "ci_high": ci_high,
                }
            )
    return pd.DataFrame(rows)


def subgroup_regression_tests(
    *,
    panel: pd.DataFrame,
    metrics: list[str],
    cluster_col: str,
    confidence_level: float,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    work_df = panel.copy()
    work_df["closure_window_fe"] = work_df["closure_event_id"] + "_rel_" + work_df["rel_t"].astype(str)
    for treated_value, treatment_df in work_df.groupby("treated", sort=True):
        for metric in metrics:
            formula = f"{metric} ~ predicted_purchase_intention + C(closure_window_fe)"
            fit = smf.ols(formula=formula, data=treatment_df).fit(
                cov_type="cluster",
                cov_kwds={"groups": treatment_df[cluster_col]},
            )
            term = "predicted_purchase_intention"
            coef = float(fit.params[term])
            se = float(fit.bse[term])
            alpha = 1.0 - confidence_level
            ci_low, ci_high = fit.conf_int(alpha=alpha).loc[term].astype(float).tolist()
            rows.append(
                {
                    "treated": int(treated_value),
                    "sample": "treatment" if int(treated_value) == 1 else "control",
                    "metric": metric,
                    "term": term,
                    "formula": formula,
                    "coef": coef,
                    "se": se,
                    "t_stat": float(fit.tvalues[term]),
                    "pvalue": float(fit.pvalues[term]),
                    "ci_low": float(ci_low),
                    "ci_high": float(ci_high),
                    "n": int(fit.nobs),
                    "r2": float(fit.rsquared),
                    "cov_type": "cluster",
                    "cluster_col": cluster_col,
                }
            )
    return pd.DataFrame(rows)


def gap_difference_tests(
    *,
    panel: pd.DataFrame,
    metrics: list[str],
    cluster_col: str,
    confidence_level: float,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    work_df = panel.copy()
    work_df["closure_window_fe"] = work_df["closure_event_id"] + "_rel_" + work_df["rel_t"].astype(str)
    work_df["predicted_X_treated"] = (
        work_df["predicted_purchase_intention"] * work_df["treated"]
    )
    for metric in metrics:
        formula = (
            f"{metric} ~ predicted_purchase_intention + treated + predicted_X_treated "
            "+ C(closure_window_fe)"
        )
        fit = smf.ols(formula=formula, data=work_df).fit(
            cov_type="cluster",
            cov_kwds={"groups": work_df[cluster_col]},
        )
        alpha = 1.0 - confidence_level
        ci = fit.conf_int(alpha=alpha)
        for term, interpretation in [
            ("predicted_purchase_intention", "control subgroup gap"),
            ("predicted_X_treated", "treatment minus control subgroup gap"),
        ]:
            ci_low, ci_high = ci.loc[term].astype(float).tolist()
            rows.append(
                {
                    "metric": metric,
                    "term": term,
                    "interpretation": interpretation,
                    "formula": formula,
                    "coef": float(fit.params[term]),
                    "se": float(fit.bse[term]),
                    "t_stat": float(fit.tvalues[term]),
                    "pvalue": float(fit.pvalues[term]),
                    "ci_low": float(ci_low),
                    "ci_high": float(ci_high),
                    "n": int(fit.nobs),
                    "r2": float(fit.rsquared),
                    "cov_type": "cluster",
                    "cluster_col": cluster_col,
                }
            )
    return pd.DataFrame(rows)


def write_summary(
    *,
    output_dir: Path,
    summary_filename: str,
    selected_scores: pd.DataFrame,
    push_records: pd.DataFrame,
    panel: pd.DataFrame,
    mean_tests: pd.DataFrame,
    subgroup_results: pd.DataFrame,
    gap_difference_results: pd.DataFrame,
) -> None:
    group_counts = (
        selected_scores.groupby(["treated", "predicted_purchase_intention"], sort=True)
        .size()
        .rename("n")
        .reset_index()
    )
    treated_rows = selected_scores[selected_scores["treated"].eq(1)]
    control_rows = selected_scores[selected_scores["treated"].eq(0)]
    lines = [
        "# Push Targeting After Reopening",
        "",
        f"- Selected member-events: {len(selected_scores):,}",
        f"- Treatment member-events: {len(treated_rows):,}",
        f"- Control member-events: {len(control_rows):,}",
        f"- Member-event-window rows: {len(panel):,}",
        f"- Filtered push records: {len(push_records):,}",
        "",
        "## Member-Event Counts",
        "",
        group_counts.to_markdown(index=False),
        "",
        "## Welch Mean Tests",
        "",
        mean_tests.to_markdown(index=False),
        "",
        "## Closure-Window Adjusted Subgroup Regressions",
        "",
        subgroup_results[
            ["sample", "metric", "coef", "se", "pvalue", "ci_low", "ci_high", "n", "r2"]
        ].to_markdown(index=False),
        "",
        "## Treatment-Control Difference in Subgroup Gaps",
        "",
        gap_difference_results[
            [
                "metric",
                "term",
                "interpretation",
                "coef",
                "se",
                "pvalue",
                "ci_low",
                "ci_high",
                "n",
                "r2",
            ]
        ].to_markdown(index=False),
    ]
    (output_dir / summary_filename).write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    cfg = load_config()
    paths_cfg = cfg["paths"]
    outputs_cfg = cfg["outputs"]
    analysis_cfg = cfg["analysis"]

    processed_dir = project_path(relative_path=paths_cfg["processed_dir"])
    output_dir = project_path(relative_path=paths_cfg["output_dir"])
    processed_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    selected_scores = load_selected_scores(cfg=cfg)
    windows = build_post_windows(
        selected_scores=selected_scores,
        rel_t_values=[int(value) for value in analysis_cfg["post_rel_t_values"]],
    )
    push_records = filter_push_records(cfg=cfg, windows=windows)
    panel = build_push_panel(windows=windows, push_records=push_records)

    metrics = list(analysis_cfg["metrics"])
    group_summary = flatten_columns(df=summarize_groups(panel=panel, metrics=metrics))
    mean_tests = welch_mean_tests(
        panel=panel,
        metrics=metrics,
        confidence_level=float(analysis_cfg["confidence_level"]),
    )
    subgroup_results = subgroup_regression_tests(
        panel=panel,
        metrics=metrics,
        cluster_col=str(analysis_cfg["cluster_col"]),
        confidence_level=float(analysis_cfg["confidence_level"]),
    )
    gap_difference_results = gap_difference_tests(
        panel=panel,
        metrics=metrics,
        cluster_col=str(analysis_cfg["cluster_col"]),
        confidence_level=float(analysis_cfg["confidence_level"]),
    )

    push_records.to_parquet(processed_dir / outputs_cfg["push_records"], index=False)
    panel.to_parquet(processed_dir / outputs_cfg["push_panel"], index=False)
    group_summary.to_csv(processed_dir / outputs_cfg["group_summary"], index=False)
    mean_tests.to_csv(output_dir / outputs_cfg["mean_tests"], index=False)
    subgroup_results.to_csv(output_dir / outputs_cfg["subgroup_regression_tests"], index=False)
    gap_difference_results.to_csv(output_dir / outputs_cfg["gap_difference_tests"], index=False)

    metadata = {
        "selected_closure_registry": paths_cfg["selected_closure_registry"],
        "score_file": paths_cfg["score_file"],
        "push_data_dir": paths_cfg["push_data_dir"],
        "push_file_pattern": paths_cfg["push_file_pattern"],
        "post_rel_t_values": analysis_cfg["post_rel_t_values"],
        "metrics": metrics,
        "selected_member_events": int(len(selected_scores)),
        "treatment_member_events": int(selected_scores["treated"].sum()),
        "control_member_events": int(selected_scores["treated"].eq(0).sum()),
        "member_event_windows": int(len(panel)),
        "filtered_push_records": int(len(push_records)),
        "processed_outputs": {
            "push_records": str((processed_dir / outputs_cfg["push_records"]).relative_to(PROJECT_ROOT)),
            "push_panel": str((processed_dir / outputs_cfg["push_panel"]).relative_to(PROJECT_ROOT)),
            "group_summary": str((processed_dir / outputs_cfg["group_summary"]).relative_to(PROJECT_ROOT)),
        },
        "analysis_outputs": {
            "mean_tests": str((output_dir / outputs_cfg["mean_tests"]).relative_to(PROJECT_ROOT)),
            "subgroup_regression_tests": str(
                (output_dir / outputs_cfg["subgroup_regression_tests"]).relative_to(PROJECT_ROOT)
            ),
            "gap_difference_tests": str(
                (output_dir / outputs_cfg["gap_difference_tests"]).relative_to(PROJECT_ROOT)
            ),
        },
    }
    (output_dir / outputs_cfg["run_metadata"]).write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_summary(
        output_dir=output_dir,
        summary_filename=str(outputs_cfg["summary"]),
        selected_scores=selected_scores,
        push_records=push_records,
        panel=panel,
        mean_tests=mean_tests,
        subgroup_results=subgroup_results,
        gap_difference_results=gap_difference_results,
    )


if __name__ == "__main__":
    main()
