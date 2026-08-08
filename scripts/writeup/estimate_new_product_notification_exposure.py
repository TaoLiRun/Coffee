from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


REL_PERIODS = (-4, -3, -2, -1, 0, 1, 2, 3, 4)
SEED = 20260808


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Test whether inactivity-triggered new-product notifications generate "
            "the exposure pattern required to explain the novelty-seeking DDD."
        )
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/05_robustness/new_product_notification_exposure"),
    )
    parser.add_argument(
        "--push-dir",
        type=Path,
        default=Path("../data/data1031"),
    )
    parser.add_argument("--bootstrap-reps", type=int, default=9999)
    return parser.parse_args()


def normalize_date(values: pd.Series) -> pd.Series:
    return pd.to_datetime(values, errors="coerce").dt.normalize()


def read_main_panel(project_root: Path) -> pd.DataFrame:
    path = (
        project_root
        / "outputs/03_main_18_closures/novelty_member_first_ddd_h4/estimation_sample.csv"
    )
    panel = pd.read_csv(path, encoding="utf-8-sig")
    required = {
        "member_id",
        "closure_event_id",
        "closure_start",
        "closure_end",
        "closure_duration_days",
        "treated",
        "disp_binary",
        "rel_t",
        "period_start",
        "calendar_month",
        "event_fe_id",
        "variety_seeking",
    }
    missing = sorted(required - set(panel.columns))
    if missing:
        raise ValueError(f"Main panel is missing columns: {missing}")
    panel["member_id"] = panel["member_id"].astype(int)
    for col in ["closure_start", "closure_end", "period_start"]:
        panel[col] = normalize_date(panel[col])
    panel["period_end"] = panel["period_start"] + pd.to_timedelta(
        panel["closure_duration_days"].astype(int) - 1, unit="D"
    )
    if panel.duplicated(["member_id", "closure_event_id", "rel_t"]).any():
        raise ValueError("Main panel is not unique at member-event-period grain.")
    if set(panel["rel_t"].unique()) != set(REL_PERIODS) - {0}:
        raise ValueError("Unexpected relative periods in main panel.")
    return panel


def add_closure_period(panel: pd.DataFrame) -> pd.DataFrame:
    member_cols = [
        "member_id",
        "closure_event_id",
        "closure_start",
        "closure_end",
        "closure_duration_days",
        "treated",
        "disp_binary",
        "event_fe_id",
    ]
    members = panel[member_cols].drop_duplicates()
    if members.duplicated("member_id").any():
        raise ValueError("A member belongs to more than one closure event.")
    during = members.copy()
    during["rel_t"] = 0
    during["period_start"] = during["closure_start"]
    during["period_end"] = during["closure_end"]
    during["calendar_month"] = during["period_start"].dt.to_period("M").astype(str)
    during["variety_seeking"] = np.nan
    keep = list(panel.columns)
    for col in keep:
        if col not in during.columns:
            during[col] = np.nan
    full = pd.concat([panel, during[keep]], ignore_index=True)
    full["rel_t"] = full["rel_t"].astype(int)
    full["treated"] = full["treated"].astype(int)
    full["disp_binary"] = full["disp_binary"].astype(int)
    full["closure_duration_days"] = full["closure_duration_days"].astype(int)
    full["phase"] = np.select(
        [full["rel_t"].lt(0), full["rel_t"].eq(0)],
        ["pre", "during"],
        default="post",
    )
    return full.sort_values(["member_id", "rel_t"]).reset_index(drop=True)


def map_relative_period(events: pd.DataFrame, member_events: pd.DataFrame) -> pd.DataFrame:
    matched = events.merge(member_events, on="member_id", how="inner", validate="many_to_one")
    before = matched["dt"].lt(matched["closure_start"])
    after = matched["dt"].gt(matched["closure_end"])
    matched["rel_t"] = 0
    pre_days = (matched.loc[before, "dt"] - matched.loc[before, "closure_start"]).dt.days
    matched.loc[before, "rel_t"] = np.floor(
        pre_days / matched.loc[before, "closure_duration_days"]
    ).astype(int)
    post_days = (
        matched.loc[after, "dt"]
        - (matched.loc[after, "closure_end"] + pd.Timedelta(days=1))
    ).dt.days
    matched.loc[after, "rel_t"] = (
        np.floor(post_days / matched.loc[after, "closure_duration_days"]).astype(int) + 1
    )
    matched["rel_t"] = matched["rel_t"].astype(int)
    return matched[matched["rel_t"].isin(REL_PERIODS)].copy()


def scan_push_records(
    push_dir: Path,
    member_events: pd.DataFrame,
    min_date: pd.Timestamp,
    max_date: pd.Timestamp,
) -> tuple[pd.DataFrame, dict]:
    paths = sorted(push_dir.glob("sleep_push_result_*.csv"))
    if not paths:
        raise FileNotFoundError(f"No sleep_push_result_*.csv under {push_dir}")
    member_ids = set(member_events["member_id"])
    desired = [
        "dt",
        "member_id",
        "policy_id",
        "action_type",
        "trigger_tag",
        "channel",
    ]
    frames: list[pd.DataFrame] = []
    rows_scanned = 0
    for file_index, path in enumerate(paths, start=1):
        print(f"[raw push {file_index}/{len(paths)}] {path.name}", flush=True)
        for chunk in pd.read_csv(
            path,
            encoding="utf-8-sig",
            usecols=lambda column: column in desired,
            chunksize=1_000_000,
        ):
            rows_scanned += len(chunk)
            chunk["member_id"] = pd.to_numeric(chunk["member_id"], errors="coerce")
            chunk = chunk.dropna(subset=["member_id", "dt"]).copy()
            chunk["member_id"] = chunk["member_id"].astype(int)
            chunk = chunk[chunk["member_id"].isin(member_ids)]
            if chunk.empty:
                continue
            chunk["dt"] = normalize_date(chunk["dt"])
            chunk = chunk[chunk["dt"].between(min_date, max_date)]
            if not chunk.empty:
                frames.append(chunk)
    raw = pd.concat(frames, ignore_index=True)
    raw["trigger_tag"] = pd.to_numeric(raw["trigger_tag"], errors="coerce")
    raw["action_type"] = pd.to_numeric(raw["action_type"], errors="coerce")
    raw["channel"] = pd.to_numeric(raw["channel"], errors="coerce")
    raw["is_new_product"] = raw["trigger_tag"].eq(3).astype(int)
    raw["policy_id_clean"] = raw["policy_id"].fillna("").astype(str).str.strip()
    missing_policy = raw["policy_id_clean"].eq("")
    raw.loc[missing_policy, "policy_id_clean"] = (
        "missing_policy__trigger_"
        + raw.loc[missing_policy, "trigger_tag"].fillna(-1).astype(int).astype(str)
        + "__action_"
        + raw.loc[missing_policy, "action_type"].fillna(-1).astype(int).astype(str)
        + "__channel_"
        + raw.loc[missing_policy, "channel"].fillna(-1).astype(int).astype(str)
    )
    exact_duplicate_rows = int(raw.duplicated(desired).sum())
    mapped = map_relative_period(raw, member_events)
    campaign_key = [
        "member_id",
        "closure_event_id",
        "rel_t",
        "dt",
        "policy_id_clean",
        "trigger_tag",
    ]
    campaign_day = mapped.drop_duplicates(campaign_key).copy()
    audit = {
        "push_files": len(paths),
        "rows_scanned": int(rows_scanned),
        "sample_date_filtered_rows": int(len(raw)),
        "rows_mapped_to_analysis_periods": int(len(mapped)),
        "exact_duplicate_rows_before_period_mapping": exact_duplicate_rows,
        "unique_campaign_day_rows": int(len(campaign_day)),
        "new_product_raw_rows": int(mapped["is_new_product"].sum()),
        "new_product_unique_campaign_day_rows": int(campaign_day["is_new_product"].sum()),
        "missing_policy_share": float(missing_policy.mean()),
        "trigger_tag_counts": {
            str(key): int(value)
            for key, value in mapped["trigger_tag"].value_counts(dropna=False).sort_index().items()
        },
    }
    return mapped, audit


def aggregate_exposure(mapped: pd.DataFrame, panel: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    keys = ["member_id", "closure_event_id", "rel_t"]
    campaign_key = keys + ["dt", "policy_id_clean", "trigger_tag"]
    campaign_day = mapped.drop_duplicates(campaign_key).copy()
    raw_counts = (
        mapped.groupby(keys, sort=False)
        .agg(
            n_push_records=("dt", "size"),
            n_new_push_records=("is_new_product", "sum"),
        )
        .reset_index()
    )
    campaign_counts = (
        campaign_day.groupby(keys, sort=False)
        .agg(
            n_campaign_days=("dt", "size"),
            n_new_campaign_days=("is_new_product", "sum"),
            n_push_days=("dt", "nunique"),
        )
        .reset_index()
    )
    new_days = (
        campaign_day[campaign_day["is_new_product"].eq(1)]
        .groupby(keys, sort=False)["dt"]
        .nunique()
        .rename("n_new_push_days")
        .reset_index()
    )
    counts = raw_counts.merge(campaign_counts, on=keys, how="outer", validate="one_to_one")
    counts = counts.merge(new_days, on=keys, how="left", validate="one_to_one")
    out = panel.merge(counts, on=keys, how="left", validate="one_to_one")
    count_columns = [
        "n_push_records",
        "n_new_push_records",
        "n_campaign_days",
        "n_new_campaign_days",
        "n_push_days",
        "n_new_push_days",
    ]
    out[count_columns] = out[count_columns].fillna(0).astype(int)
    days = out["closure_duration_days"].astype(float)
    out["push_records_per_day"] = out["n_push_records"] / days
    out["new_records_per_day"] = out["n_new_push_records"] / days
    out["campaigns_per_day"] = out["n_campaign_days"] / days
    out["new_campaigns_per_day"] = out["n_new_campaign_days"] / days
    out["new_push_days_per_day"] = out["n_new_push_days"] / days
    out["any_new_push"] = out["n_new_campaign_days"].gt(0).astype(int)
    out["new_campaign_share"] = np.where(
        out["n_campaign_days"].gt(0),
        out["n_new_campaign_days"] / out["n_campaign_days"],
        np.nan,
    )
    return out, campaign_day


def load_combined_events(
    project_root: Path,
    member_events: pd.DataFrame,
    min_date: pd.Timestamp,
    max_date: pd.Timestamp,
) -> pd.DataFrame:
    path = project_root / "data/processed/combined_push_purchase_analysis.parquet"
    columns = [
        "dt",
        "member_id",
        "trigger_tag",
        "data_source",
        "days_since_purchase",
        "dormant_period",
    ]
    print("[combined events] reading push-purchase timing file", flush=True)
    events = pd.read_parquet(path, columns=columns)
    member_ids = set(member_events["member_id"])
    events = events[events["member_id"].isin(member_ids)].copy()
    events["dt"] = normalize_date(events["dt"])
    events = events[events["dt"].between(min_date, max_date)]
    events["trigger_tag"] = pd.to_numeric(events["trigger_tag"], errors="coerce")
    return map_relative_period(events, member_events)


def add_purchase_timing_metrics(
    panel: pd.DataFrame,
    campaign_day: pd.DataFrame,
    combined: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    keys = ["member_id", "closure_event_id", "rel_t"]
    purchases = combined[combined["data_source"].eq(1)]
    first_purchase = (
        purchases.groupby(keys, sort=False)["dt"].min().rename("first_purchase_dt").reset_index()
    )
    out = panel.merge(first_purchase, on=keys, how="left", validate="one_to_one")
    new_campaigns = campaign_day[campaign_day["is_new_product"].eq(1)].merge(
        first_purchase, on=keys, how="left", validate="many_to_one"
    )
    new_campaigns["strictly_before_first_purchase"] = (
        new_campaigns["first_purchase_dt"].notna()
        & new_campaigns["dt"].lt(new_campaigns["first_purchase_dt"])
    )
    new_campaigns["on_or_before_first_purchase"] = (
        new_campaigns["first_purchase_dt"].notna()
        & new_campaigns["dt"].le(new_campaigns["first_purchase_dt"])
    )
    timing = (
        new_campaigns.groupby(keys, sort=False)
        .agg(
            n_new_strictly_before_first_purchase=("strictly_before_first_purchase", "sum"),
            n_new_on_or_before_first_purchase=("on_or_before_first_purchase", "sum"),
        )
        .reset_index()
    )
    out = out.merge(timing, on=keys, how="left", validate="one_to_one")
    timing_cols = [
        "n_new_strictly_before_first_purchase",
        "n_new_on_or_before_first_purchase",
    ]
    out[timing_cols] = out[timing_cols].fillna(0).astype(int)
    out["any_new_strictly_before_first_purchase"] = (
        out["n_new_strictly_before_first_purchase"].gt(0).astype(int)
    )

    combined_push = combined[combined["data_source"].eq(0)].copy()
    raw_counts = (
        campaign_day.groupby(keys, sort=False).size().rename("raw_unique_campaign_days").reset_index()
    )
    combined_counts = (
        combined_push.groupby(keys, sort=False).size().rename("combined_push_rows").reset_index()
    )
    reconciliation = raw_counts.merge(combined_counts, on=keys, how="outer").fillna(0)
    reconciliation["difference"] = (
        reconciliation["raw_unique_campaign_days"] - reconciliation["combined_push_rows"]
    )
    audit = {
        "purchasing_member_periods": int(out["first_purchase_dt"].notna().sum()),
        "main_panel_purchasing_rows": int(out["variety_seeking"].notna().sum()),
        "purchase_window_match_share": float(
            (out["first_purchase_dt"].notna() == out["variety_seeking"].notna()).mean()
        ),
        "raw_unique_vs_combined_exact_period_count_share": float(
            reconciliation["difference"].eq(0).mean()
        ),
        "raw_unique_vs_combined_total_difference": int(reconciliation["difference"].sum()),
        "raw_unique_vs_combined_max_abs_period_difference": int(
            reconciliation["difference"].abs().max()
        ),
    }
    return out, new_campaigns, audit


def drop_singletons(data: pd.DataFrame, fixed_effects: list[str]) -> tuple[pd.DataFrame, int]:
    work = data.copy()
    initial_rows = len(work)
    while True:
        keep = np.ones(len(work), dtype=bool)
        for column in fixed_effects:
            counts = work.groupby(column, observed=True)[column].transform("size").to_numpy()
            keep &= counts > 1
        if keep.all():
            return work, initial_rows - len(work)
        work = work.loc[keep].copy()


def residualize(
    values: np.ndarray,
    fixed_effect_codes: list[np.ndarray],
    tolerance: float = 1e-10,
    max_iterations: int = 1000,
) -> tuple[np.ndarray, int, float]:
    residual = np.asarray(values, dtype=np.float64).copy()
    if residual.ndim == 1:
        residual = residual[:, None]
    for iteration in range(1, max_iterations + 1):
        previous = residual.copy()
        for codes in fixed_effect_codes:
            group_count = int(codes.max()) + 1
            counts = np.bincount(codes, minlength=group_count).astype(float)
            for column in range(residual.shape[1]):
                sums = np.bincount(codes, weights=residual[:, column], minlength=group_count)
                residual[:, column] -= (sums / counts)[codes]
        error = float(np.max(np.abs(residual - previous)))
        if error < tolerance:
            return residual, iteration, error
    raise RuntimeError("Fixed-effect absorption failed to converge.")


def fit_fe_ols(
    data: pd.DataFrame,
    outcome: str,
    regressors: list[str],
    fixed_effects: list[str],
    cluster: str,
) -> dict:
    required = [outcome, *regressors, *fixed_effects, cluster]
    work = data.dropna(subset=required).copy()
    work, singleton_drops = drop_singletons(work, fixed_effects)
    codes = [pd.factorize(work[column], sort=False)[0] for column in fixed_effects]
    matrix = work[[outcome, *regressors]].to_numpy(dtype=float)
    residualized, iterations, absorption_error = residualize(matrix, codes)
    y = residualized[:, 0]
    X = residualized[:, 1:]
    xtx = X.T @ X
    if np.linalg.matrix_rank(xtx) < len(regressors):
        raise ValueError(f"Rank deficiency for {outcome} with {regressors}")
    bread = np.linalg.inv(xtx)
    beta = bread @ (X.T @ y)
    residuals = y - X @ beta
    cluster_codes, cluster_labels = pd.factorize(work[cluster], sort=False)
    group_count = len(cluster_labels)
    scores = np.zeros((group_count, len(regressors)))
    np.add.at(scores, cluster_codes, X * residuals[:, None])
    correction = (group_count / (group_count - 1)) * (
        (len(work) - 1) / (len(work) - len(regressors))
    )
    covariance = correction * bread @ (scores.T @ scores) @ bread
    standard_errors = np.sqrt(np.maximum(np.diag(covariance), 0))
    degrees_freedom = group_count - 1
    pvalues = 2 * stats.t.sf(np.abs(beta / standard_errors), degrees_freedom)
    critical = stats.t.ppf(0.975, degrees_freedom)
    return {
        "work": work,
        "X": X,
        "y": y,
        "beta": beta,
        "bread": bread,
        "covariance": covariance,
        "standard_errors": standard_errors,
        "pvalues": pvalues,
        "ci_low": beta - critical * standard_errors,
        "ci_high": beta + critical * standard_errors,
        "names": regressors,
        "cluster_codes": cluster_codes,
        "cluster_labels": cluster_labels,
        "correction": correction,
        "n": len(work),
        "singleton_drops": singleton_drops,
        "iterations": iterations,
        "absorption_error": absorption_error,
    }


def restricted_wild_cluster_pvalue(
    fit: dict,
    term: str,
    repetitions: int,
    seed: int,
) -> float:
    names = fit["names"]
    target = names.index(term)
    X = fit["X"]
    y = fit["y"]
    cluster_codes = fit["cluster_codes"]
    group_count = len(fit["cluster_labels"])
    keep = [index for index in range(X.shape[1]) if index != target]
    beta_null = np.zeros(X.shape[1])
    if keep:
        X_restricted = X[:, keep]
        beta_null[keep] = np.linalg.solve(X_restricted.T @ X_restricted, X_restricted.T @ y)
    residual_null = y - X @ beta_null
    score_null = np.zeros((group_count, X.shape[1]))
    np.add.at(score_null, cluster_codes, X * residual_null[:, None])
    xtx_by_cluster = np.zeros((group_count, X.shape[1], X.shape[1]))
    for group in range(group_count):
        X_group = X[cluster_codes == group]
        xtx_by_cluster[group] = X_group.T @ X_group
    observed_t = fit["beta"][target] / fit["standard_errors"][target]
    rng = np.random.default_rng(seed)
    exceedances = 0
    for _ in range(repetitions):
        weights = rng.choice(np.array([-1.0, 1.0]), size=group_count)
        beta_star = beta_null + fit["bread"] @ (score_null.T @ weights)
        delta = beta_star - beta_null
        bootstrap_scores = weights[:, None] * score_null - np.einsum(
            "gij,j->gi", xtx_by_cluster, delta
        )
        covariance_star = (
            fit["correction"]
            * fit["bread"]
            @ (bootstrap_scores.T @ bootstrap_scores)
            @ fit["bread"]
        )
        se_star = np.sqrt(max(covariance_star[target, target], 0))
        if se_star > 0:
            t_star = beta_star[target] / se_star
            exceedances += int(abs(t_star) >= abs(observed_t))
    return (exceedances + 1) / (repetitions + 1)


def fit_ddd(
    data: pd.DataFrame,
    outcome: str,
    comparison: str,
    bootstrap_reps: int,
) -> dict:
    if comparison == "post_vs_pre":
        work = data[data["rel_t"].ne(0)].copy()
        work["after"] = work["rel_t"].gt(0).astype(int)
    elif comparison == "during_vs_all_pre":
        work = data[data["rel_t"].le(0)].copy()
        work["after"] = work["rel_t"].eq(0).astype(int)
    elif comparison == "during_vs_last_pre":
        work = data[data["rel_t"].isin([-1, 0])].copy()
        work["after"] = work["rel_t"].eq(0).astype(int)
    else:
        raise ValueError(comparison)
    work["after_X_treated"] = work["after"] * work["treated"]
    work["after_X_high"] = work["after"] * work["disp_binary"]
    term = "after_X_treated_X_high"
    work[term] = work["after"] * work["treated"] * work["disp_binary"]
    regressors = ["after_X_treated", "after_X_high", term]
    fit = fit_fe_ols(
        work,
        outcome,
        regressors,
        ["event_fe_id", "rel_t", "calendar_month"],
        "closure_event_id",
    )
    index = regressors.index(term)
    wild_pvalue = restricted_wild_cluster_pvalue(
        fit, term, bootstrap_reps, SEED + len(outcome) + len(comparison)
    )
    return {
        "comparison": comparison,
        "outcome": outcome,
        "term": term,
        "coef": float(fit["beta"][index]),
        "se_crv1": float(fit["standard_errors"][index]),
        "pvalue_crv1": float(fit["pvalues"][index]),
        "pvalue_wild_restricted": float(wild_pvalue),
        "ci_low": float(fit["ci_low"][index]),
        "ci_high": float(fit["ci_high"][index]),
        "n": int(fit["n"]),
        "clusters": int(len(fit["cluster_labels"])),
        "singleton_drops": int(fit["singleton_drops"]),
        "absorption_error": float(fit["absorption_error"]),
    }


def fit_event_study(data: pd.DataFrame, outcome: str) -> tuple[pd.DataFrame, dict]:
    work = data.copy()
    regressors: list[str] = []
    triple_terms: list[str] = []
    term_to_period: dict[str, int] = {}
    for relative_period in REL_PERIODS:
        if relative_period == -1:
            continue
        suffix = f"m{abs(relative_period)}" if relative_period < 0 else f"p{relative_period}"
        indicator = work["rel_t"].eq(relative_period).astype(int)
        treated_term = f"rt_{suffix}_X_treated"
        high_term = f"rt_{suffix}_X_high"
        triple_term = f"rt_{suffix}_X_treated_X_high"
        work[treated_term] = indicator * work["treated"]
        work[high_term] = indicator * work["disp_binary"]
        work[triple_term] = indicator * work["treated"] * work["disp_binary"]
        regressors.extend([treated_term, high_term, triple_term])
        triple_terms.append(triple_term)
        term_to_period[triple_term] = relative_period
    fit = fit_fe_ols(
        work,
        outcome,
        regressors,
        ["event_fe_id", "rel_t", "calendar_month"],
        "closure_event_id",
    )
    rows = []
    for term in triple_terms:
        index = regressors.index(term)
        rows.append(
            {
                "outcome": outcome,
                "term": term,
                "rel_t": term_to_period[term],
                "coef": float(fit["beta"][index]),
                "se_crv1": float(fit["standard_errors"][index]),
                "pvalue_crv1": float(fit["pvalues"][index]),
                "ci_low": float(fit["ci_low"][index]),
                "ci_high": float(fit["ci_high"][index]),
            }
        )
    pre_terms = [term for term in triple_terms if term_to_period[term] < -1]
    restriction = np.array([fit["beta"][regressors.index(term)] for term in pre_terms])
    indices = [regressors.index(term) for term in pre_terms]
    restriction_covariance = fit["covariance"][np.ix_(indices, indices)]
    statistic = float(
        restriction.T @ np.linalg.pinv(restriction_covariance) @ restriction / len(pre_terms)
    )
    pretrend = {
        "outcome": outcome,
        "f_statistic": statistic,
        "df_num": len(pre_terms),
        "df_denom": len(fit["cluster_labels"]) - 1,
        "pvalue": float(stats.f.sf(statistic, len(pre_terms), len(fit["cluster_labels"]) - 1)),
    }
    return pd.DataFrame(rows).sort_values("rel_t"), pretrend


def make_descriptive_tables(panel: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    metrics = [
        "new_campaigns_per_day",
        "new_records_per_day",
        "any_new_push",
        "new_push_days_per_day",
        "campaigns_per_day",
        "new_campaign_share",
        "n_new_strictly_before_first_purchase",
        "any_new_strictly_before_first_purchase",
    ]
    phase_member = (
        panel.groupby(
            ["member_id", "closure_event_id", "treated", "disp_binary", "phase"],
            observed=True,
        )[metrics]
        .mean()
        .reset_index()
    )
    means = (
        phase_member.groupby(["treated", "disp_binary", "phase"], observed=True)[metrics]
        .agg(["count", "mean", "std"])
        .reset_index()
    )
    means.columns = [
        "_".join(str(piece) for piece in column if piece != "").rstrip("_")
        if isinstance(column, tuple)
        else column
        for column in means.columns
    ]
    treated = phase_member[phase_member["treated"].eq(1)]
    treated_means = (
        treated.groupby(["disp_binary", "phase"], observed=True)[metrics]
        .mean()
        .reset_index()
    )
    return means, treated_means


def dormancy_table(combined: pd.DataFrame) -> pd.DataFrame:
    new_pushes = combined[
        combined["data_source"].eq(0) & combined["trigger_tag"].eq(3)
    ].copy()
    new_pushes["phase"] = np.select(
        [new_pushes["rel_t"].lt(0), new_pushes["rel_t"].eq(0)],
        ["pre", "during"],
        default="post",
    )
    grouped = new_pushes.groupby(["treated", "disp_binary", "phase"], observed=True)
    rows = grouped["days_since_purchase"].agg(
        records="size", mean="mean", median="median", minimum="min", maximum="max"
    ).reset_index()
    quantiles = grouped["days_since_purchase"].quantile([0.25, 0.75, 0.9]).unstack()
    quantiles.columns = ["p25", "p75", "p90"]
    return rows.merge(quantiles.reset_index(), on=["treated", "disp_binary", "phase"])


def write_summary(
    output_dir: Path,
    audit: dict,
    ddd_results: pd.DataFrame,
    treated_means: pd.DataFrame,
    pretrend: dict,
) -> None:
    primary = ddd_results[ddd_results["outcome"].eq("new_campaigns_per_day")].copy()
    lines = [
        "# New-product notification mechanism test",
        "",
        "## Question",
        "",
        "Do treated low-intention consumers experience a relative increase in recorded new-product notification exposure during closure or after reopening, compared with the corresponding high-intention and control-group changes?",
        "",
        "## Metric",
        "",
        "The primary outcome is unique trigger-tag-3 policy campaigns per consumer-day. Each member-policy-date combination is counted once. Raw-record counts, notification days, any exposure, total campaign volume and new-product share are secondary outcomes.",
        "",
        "## Primary estimates",
        "",
        "```text",
        primary.to_string(index=False),
        "```",
        "",
        "A negative triple-difference coefficient is the direction required by the alternative explanation: low-intention treated consumers receive a larger relative increase in new-product notifications than high-intention treated consumers.",
        "",
        "## Treated-group descriptive means",
        "",
        "```text",
        treated_means.to_string(index=False),
        "```",
        "",
        "## Pretrend diagnostic",
        "",
        f"For the primary exposure outcome, the joint pretrend p-value is {pretrend['pvalue']:.4f}.",
        "",
        "## Data and interpretation limits",
        "",
        f"The raw scan read {audit['raw_push']['rows_scanned']:,} records and retained {audit['raw_push']['rows_mapped_to_analysis_periods']:,} records in the analysis windows. The source identifies recorded targeting entries; it does not establish delivery, impression, opening or reading.",
        "",
        "This test evaluates a necessary exposure pattern. Even a negative estimate would not show that notifications caused product choice. A null or positive, precisely estimated estimate would weigh against recorded new-product notifications as an explanation for the novelty DDD.",
    ]
    (output_dir / "SUMMARY.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    project_root = args.project_root.resolve()
    output_dir = (
        args.output_dir
        if args.output_dir.is_absolute()
        else project_root / args.output_dir
    )
    push_dir = (
        args.push_dir if args.push_dir.is_absolute() else project_root / args.push_dir
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    print("[1/7] Read main panel and add closure period", flush=True)
    main_panel = read_main_panel(project_root)
    panel = add_closure_period(main_panel)
    member_events = panel[
        [
            "member_id",
            "closure_event_id",
            "closure_start",
            "closure_end",
            "closure_duration_days",
            "treated",
            "disp_binary",
        ]
    ].drop_duplicates("member_id")
    min_date = panel["period_start"].min()
    max_date = panel["period_end"].max()

    print("[2/7] Scan raw push files", flush=True)
    mapped_pushes, raw_audit = scan_push_records(
        push_dir, member_events, min_date, max_date
    )
    print("[3/7] Aggregate new-product notification exposure", flush=True)
    panel, campaign_day = aggregate_exposure(mapped_pushes, panel)

    print("[4/7] Add purchase timing and validate source reconciliation", flush=True)
    combined = load_combined_events(project_root, member_events, min_date, max_date)
    panel, new_campaigns, timing_audit = add_purchase_timing_metrics(
        panel, campaign_day, combined
    )

    print("[5/7] Estimate exposure triple differences", flush=True)
    outcomes = [
        "new_campaigns_per_day",
        "new_records_per_day",
        "any_new_push",
        "new_push_days_per_day",
        "campaigns_per_day",
        "push_records_per_day",
        "new_campaign_share",
    ]
    comparisons = ["post_vs_pre", "during_vs_all_pre", "during_vs_last_pre"]
    estimates = []
    for outcome in outcomes:
        for comparison in comparisons:
            print(f"  {outcome}: {comparison}", flush=True)
            estimates.append(
                fit_ddd(panel, outcome, comparison, args.bootstrap_reps)
            )
    ddd_results = pd.DataFrame(estimates)
    event_study, pretrend = fit_event_study(panel, "new_campaigns_per_day")

    print("[6/7] Build descriptive and dormancy diagnostics", flush=True)
    descriptive, treated_means = make_descriptive_tables(panel)
    dormancy = dormancy_table(combined)
    purchase_match = (
        panel[panel["variety_seeking"].notna()]
        .groupby(["treated", "disp_binary", "phase"], observed=True)
        .agg(
            purchasing_windows=("member_id", "size"),
            share_preceded_by_new_product_push=(
                "any_new_strictly_before_first_purchase",
                "mean",
            ),
            mean_new_product_pushes_before_purchase=(
                "n_new_strictly_before_first_purchase",
                "mean",
            ),
        )
        .reset_index()
    )

    print("[7/7] Save outputs", flush=True)
    audit = {
        "analysis_date": "2026-08-08",
        "new_product_definition": "trigger_tag == 3",
        "record_interpretation": "recorded targeting entry, not verified delivery/impression",
        "panel_rows": int(len(panel)),
        "members": int(panel["member_id"].nunique()),
        "closure_events": int(panel["closure_event_id"].nunique()),
        "raw_push": raw_audit,
        "purchase_timing": timing_audit,
        "primary_pretrend": pretrend,
    }
    panel.to_parquet(output_dir / "new_product_push_panel.parquet", index=False)
    ddd_results.to_csv(output_dir / "new_product_push_ddd.csv", index=False)
    event_study.to_csv(output_dir / "new_product_push_event_study.csv", index=False)
    descriptive.to_csv(output_dir / "cell_phase_descriptives.csv", index=False)
    treated_means.to_csv(output_dir / "treated_high_low_means.csv", index=False)
    purchase_match.to_csv(output_dir / "purchase_timing_descriptives.csv", index=False)
    dormancy.to_csv(output_dir / "new_push_dormancy.csv", index=False)
    with (output_dir / "audit.json").open("w", encoding="utf-8") as file:
        json.dump(audit, file, ensure_ascii=False, indent=2)
    write_summary(output_dir, audit, ddd_results, treated_means, pretrend)
    print(json.dumps(audit, indent=2), flush=True)


if __name__ == "__main__":
    main()
