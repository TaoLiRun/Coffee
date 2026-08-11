from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
import warnings

import numpy as np
import pandas as pd
import pyfixest as pf
from scipy import stats


SEED = 20260811
CATEGORY_COLUMNS = {
    "coffee": "coffee_commodity_name",
    "food": "food_commodity_name",
    "noncoffee_drink": "drink_not_coffee_commodity_name",
    "other_noncoffee": "other_not_coffee_commodity_name",
}
NONCOFFEE_CATEGORIES = {"food", "noncoffee_drink", "other_noncoffee"}
SCOPES = {
    "all_noncoffee": NONCOFFEE_CATEGORIES,
    "noncoffee_consumables": {"food", "noncoffee_drink"},
    "noncoffee_drinks": {"noncoffee_drink"},
}
FIXED_EFFECTS = ["event_fe_id", "rel_t", "calendar_month"]
CLUSTER = "closure_event_id"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--chunksize", type=int, default=1_000_000)
    parser.add_argument("--bootstrap-reps", type=int, default=9_999)
    return parser.parse_args()


def present(series: pd.Series) -> pd.Series:
    return series.notna() & series.astype(str).str.strip().ne("")


def load_headline_grid(project_root: Path) -> tuple[pd.DataFrame, Path]:
    path = (
        project_root
        / "outputs/03_main_18_closures/novelty_member_first_ddd_h4/estimation_sample.csv"
    )
    panel = pd.read_csv(path, encoding="utf-8-sig")
    required = {
        "member_id",
        "closure_event_id",
        "event_fe_id",
        "closure_duration_days",
        "period_start",
        "calendar_month",
        "rel_t",
        "post",
        "treated",
        "disp_binary",
        "variety_seeking",
    }
    missing = required - set(panel.columns)
    if missing:
        raise ValueError(f"Headline sample is missing {sorted(missing)}")
    panel["period_start"] = pd.to_datetime(panel["period_start"], errors="raise").dt.normalize()
    panel["period_end"] = panel["period_start"] + pd.to_timedelta(
        panel["closure_duration_days"].astype(int) - 1, unit="D"
    )
    if panel.duplicated(["event_fe_id", "rel_t"]).any():
        raise ValueError("Headline grid is not unique at event_fe_id x rel_t")
    if set(panel["rel_t"].unique()) != {-4, -3, -2, -1, 1, 2, 3, 4}:
        raise ValueError("Unexpected relative periods in headline grid")
    return panel, path


def load_and_classify_transactions(
    raw_path: Path,
    member_ids: set[int],
    chunksize: int,
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    usecols = ["member_id", "create_hour", *CATEGORY_COLUMNS.values()]
    raw_rows = 0
    category_counts = Counter()
    sample_category_counts = Counter()
    invalid_timestamp_counts = Counter()
    nonempty_counts = Counter()
    global_name_counts = {category: Counter() for category in CATEGORY_COLUMNS}
    transaction_parts: list[pd.DataFrame] = []

    for chunk_number, chunk in enumerate(
        pd.read_csv(
            raw_path,
            encoding="utf-8-sig",
            usecols=usecols,
            chunksize=chunksize,
        ),
        start=1,
    ):
        raw_rows += len(chunk)
        masks = {
            category: present(chunk[column])
            for category, column in CATEGORY_COLUMNS.items()
        }
        field_count = pd.DataFrame(masks).sum(axis=1)
        nonempty_counts.update({int(k): int(v) for k, v in field_count.value_counts().items()})

        in_sample = chunk["member_id"].isin(member_ids)
        parsed_dates = pd.to_datetime(
            chunk["create_hour"].astype(str).str[:10], errors="coerce"
        ).dt.normalize()

        for category, column in CATEGORY_COLUMNS.items():
            mask = masks[category]
            category_counts[category] += int(mask.sum())
            counts = chunk.loc[mask, column].astype(str).str.strip().value_counts()
            global_name_counts[category].update(counts.to_dict())

            if category not in NONCOFFEE_CATEGORIES:
                continue
            selected_mask = mask & in_sample
            sample_category_counts[category] += int(selected_mask.sum())
            invalid_timestamp_counts[category] += int(
                parsed_dates.loc[selected_mask].isna().sum()
            )
            valid_mask = selected_mask & parsed_dates.notna()
            if not valid_mask.any():
                continue
            part = pd.DataFrame(
                {
                    "member_id": chunk.loc[valid_mask, "member_id"].to_numpy(),
                    "date": parsed_dates.loc[valid_mask].to_numpy(),
                    "category": category,
                    "product_name": (
                        chunk.loc[valid_mask, column].astype(str).str.strip().to_numpy()
                    ),
                }
            )
            transaction_parts.append(part)

        if chunk_number % 5 == 0:
            print(f"Scanned {raw_rows:,} raw commodity rows", flush=True)

    if not transaction_parts:
        raise ValueError("No non-coffee transactions found for headline members")
    transactions = pd.concat(transaction_parts, ignore_index=True)
    transactions["product_key"] = (
        transactions["category"] + "\x1f" + transactions["product_name"]
    )
    transactions["first_date"] = transactions.groupby(
        ["member_id", "product_key"], sort=False
    )["date"].transform("min")

    sample_profile = (
        transactions.groupby(["category", "product_name"], sort=True)
        .agg(
            sample_rows=("member_id", "size"),
            sample_members=("member_id", "nunique"),
            sample_first_date=("date", "min"),
            sample_last_date=("date", "max"),
        )
        .reset_index()
    )
    crosswalk_rows = []
    for category in NONCOFFEE_CATEGORIES:
        for product_name, count in sorted(global_name_counts[category].items()):
            crosswalk_rows.append(
                {
                    "category": category,
                    "product_name": product_name,
                    "product_key": f"{category}\x1f{product_name}",
                    "global_rows": int(count),
                    "is_all_noncoffee": 1,
                    "is_noncoffee_consumable": int(
                        category in SCOPES["noncoffee_consumables"]
                    ),
                    "is_noncoffee_drink": int(category == "noncoffee_drink"),
                }
            )
    crosswalk = pd.DataFrame(crosswalk_rows).merge(
        sample_profile,
        on=["category", "product_name"],
        how="left",
        validate="one_to_one",
    )
    for column in ["sample_rows", "sample_members"]:
        crosswalk[column] = crosswalk[column].fillna(0).astype(int)

    overlaps = []
    categories = sorted(NONCOFFEE_CATEGORIES)
    for left_index, left in enumerate(categories):
        left_names = set(global_name_counts[left])
        for right in categories[left_index + 1 :]:
            common = sorted(left_names.intersection(global_name_counts[right]))
            overlaps.append(
                {
                    "left": left,
                    "right": right,
                    "count": len(common),
                    "examples": common[:20],
                }
            )

    audit = {
        "raw_source": str(raw_path),
        "raw_rows": int(raw_rows),
        "global_category_rows": dict(category_counts),
        "global_distinct_names": {
            category: len(values) for category, values in global_name_counts.items()
        },
        "nonempty_category_fields_per_row": {
            str(key): int(value) for key, value in sorted(nonempty_counts.items())
        },
        "sample_member_count": int(len(member_ids)),
        "sample_noncoffee_rows_before_date_validation": dict(sample_category_counts),
        "sample_invalid_timestamp_rows": dict(invalid_timestamp_counts),
        "sample_noncoffee_rows_retained": int(len(transactions)),
        "sample_noncoffee_members": int(transactions["member_id"].nunique()),
        "sample_noncoffee_product_keys": int(transactions["product_key"].nunique()),
        "exact_name_overlaps_across_noncoffee_categories": overlaps,
    }
    return transactions, crosswalk, audit


def construct_outcomes(panel: pd.DataFrame, transactions: pd.DataFrame) -> pd.DataFrame:
    windows = panel[
        [
            "member_id",
            "event_fe_id",
            "closure_event_id",
            "rel_t",
            "period_start",
            "period_end",
        ]
    ].copy()
    mapped = transactions.merge(windows, on="member_id", how="inner", validate="many_to_many")
    mapped = mapped[
        mapped["date"].between(mapped["period_start"], mapped["period_end"], inclusive="both")
    ].copy()

    out = panel.copy()
    for scope, categories in SCOPES.items():
        current = mapped[mapped["category"].isin(categories)].copy()
        current = current.drop_duplicates(["event_fe_id", "rel_t", "product_key"])
        current["is_new"] = current["first_date"].ge(current["period_start"]).astype(int)
        aggregate = (
            current.groupby(["event_fe_id", "rel_t"], sort=False)
            .agg(
                **{
                    f"n_products_{scope}": ("product_key", "size"),
                    f"n_new_products_{scope}": ("is_new", "sum"),
                }
            )
            .reset_index()
        )
        out = out.merge(
            aggregate,
            on=["event_fe_id", "rel_t"],
            how="left",
            validate="one_to_one",
        )
        n_col = f"n_products_{scope}"
        new_col = f"n_new_products_{scope}"
        any_col = f"any_purchase_{scope}"
        outcome_col = f"novelty_{scope}"
        out[n_col] = out[n_col].fillna(0).astype(int)
        out[new_col] = out[new_col].fillna(0).astype(int)
        out[any_col] = out[n_col].gt(0).astype(int)
        out[outcome_col] = np.where(
            out[n_col].gt(0), out[new_col] / out[n_col], np.nan
        )
    return out


def add_collapsed_terms(data: pd.DataFrame) -> pd.DataFrame:
    work = data.copy()
    work["post_X_treated"] = work["post"] * work["treated"]
    work["post_X_disp"] = work["post"] * work["disp_binary"]
    work["post_X_treated_X_disp"] = (
        work["post"] * work["treated"] * work["disp_binary"]
    )
    work["post_X_treated_X_low"] = (
        work["post"] * work["treated"] * (1 - work["disp_binary"])
    )
    work["post_X_treated_X_high"] = (
        work["post"] * work["treated"] * work["disp_binary"]
    )
    return work


def tidy_value(fit, term: str) -> dict:
    tidy = fit.tidy()
    row = tidy.loc[term]
    return {
        "coef": float(row["Estimate"]),
        "se": float(row["Std. Error"]),
        "pvalue": float(row["Pr(>|t|)"]),
        "ci_low": float(row["2.5%"]),
        "ci_high": float(row["97.5%"]),
        "n": int(fit._N),
        "r2_within": float(fit._r2_within),
    }


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
                sums = np.bincount(
                    codes, weights=residual[:, column], minlength=group_count
                )
                residual[:, column] -= (sums / counts)[codes]
        error = float(np.max(np.abs(residual - previous)))
        if error < tolerance:
            return residual, iteration, error
    raise RuntimeError("Fixed-effect absorption failed to converge")


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
        raise ValueError(f"Rank deficiency for {outcome}")
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
    return {
        "work": work,
        "X": X,
        "y": y,
        "beta": beta,
        "bread": bread,
        "covariance": covariance,
        "standard_errors": standard_errors,
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
        beta_null[keep] = np.linalg.solve(
            X_restricted.T @ X_restricted, X_restricted.T @ y
        )
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


def fit_collapsed(
    data: pd.DataFrame,
    outcome: str,
    scope: str,
    outcome_type: str,
    bootstrap_reps: int,
    seed: int,
) -> tuple[list[dict], dict]:
    work = add_collapsed_terms(data)
    formula = (
        f"{outcome} ~ post_X_treated + post_X_disp + post_X_treated_X_disp"
        " | event_fe_id + rel_t + calendar_month"
    )
    fit = pf.feols(formula, data=work, vcov={"CRV1": CLUSTER})
    group_formula = (
        f"{outcome} ~ post_X_treated_X_low + post_X_disp + post_X_treated_X_high"
        " | event_fe_id + rel_t + calendar_month"
    )
    group_fit = pf.feols(group_formula, data=work, vcov={"CRV1": CLUSTER})

    low = tidy_value(group_fit, "post_X_treated_X_low")
    high = tidy_value(group_fit, "post_X_treated_X_high")
    ddd = tidy_value(fit, "post_X_treated_X_disp")
    common = tidy_value(fit, "post_X_disp")
    if not np.isclose(high["coef"], low["coef"] + ddd["coef"], atol=1e-10):
        raise AssertionError("Group-effect coefficient algebra failed")
    if not (fit._N == group_fit._N):
        raise AssertionError("Group-effect sample differs from DDD sample")

    wild_details = {
        "pvalue_wild_restricted": np.nan,
        "custom_coef": np.nan,
        "custom_se": np.nan,
        "custom_n": np.nan,
        "custom_singleton_drops": np.nan,
        "custom_absorption_error": np.nan,
    }
    if bootstrap_reps > 0:
        regressors = ["post_X_treated", "post_X_disp", "post_X_treated_X_disp"]
        custom = fit_fe_ols(work, outcome, regressors, FIXED_EFFECTS, CLUSTER)
        target = regressors.index("post_X_treated_X_disp")
        if not np.isclose(custom["beta"][target], ddd["coef"], atol=1e-8):
            raise AssertionError("Custom and pyfixest DDD coefficients differ")
        wild_details = {
            "pvalue_wild_restricted": restricted_wild_cluster_pvalue(
                custom,
                "post_X_treated_X_disp",
                repetitions=bootstrap_reps,
                seed=seed,
            ),
            "custom_coef": float(custom["beta"][target]),
            "custom_se": float(custom["standard_errors"][target]),
            "custom_n": int(custom["n"]),
            "custom_singleton_drops": int(custom["singleton_drops"]),
            "custom_absorption_error": float(custom["absorption_error"]),
        }

    rows = []
    for estimand, term, values in [
        ("low_predicted_incidence_effect", "post_X_treated_X_low", low),
        ("high_predicted_incidence_effect", "post_X_treated_X_high", high),
        ("high_minus_low_ddd", "post_X_treated_X_disp", ddd),
        ("common_high_minus_low_post_shift", "post_X_disp", common),
    ]:
        row = {
            "scope": scope,
            "outcome": outcome,
            "outcome_type": outcome_type,
            "estimand": estimand,
            "term": term,
            **values,
            "clusters": int(work.loc[work[outcome].notna(), CLUSTER].nunique()),
            "pvalue_wild_restricted": np.nan,
        }
        if estimand == "high_minus_low_ddd":
            row["pvalue_wild_restricted"] = wild_details[
                "pvalue_wild_restricted"
            ]
        rows.append(row)
    return rows, wild_details


def term_period(term: str) -> int | None:
    match = re.search(r"\[(-?\d+)\]", term)
    if match:
        return int(match.group(1))
    match = re.search(r"rel_t::(-?\d+):", term)
    return int(match.group(1)) if match else None


def joint_zero_test(fit, terms: list[str]) -> tuple[float, float]:
    tidy = fit.tidy()
    names = list(tidy.index)
    index = {str(name): position for position, name in enumerate(names)}
    valid = [term for term in terms if term in index]
    R = np.zeros((len(valid), len(names)))
    for row, term in enumerate(valid):
        R[row, index[term]] = 1.0
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        result = fit.wald_test(R=R)
    return float(result.iloc[0]), float(result.iloc[1])


def fit_event_study(
    data: pd.DataFrame,
    outcome: str,
    scope: str,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    work = data.copy()
    work["treated_X_disp"] = work["treated"] * work["disp_binary"]
    formula = (
        f"{outcome} ~ i(rel_t, treated, ref=-1) + "
        "i(rel_t, treated_X_disp, ref=-1) + "
        "i(rel_t, disp_binary, ref=-1) | "
        "event_fe_id + rel_t + calendar_month"
    )
    fit = pf.feols(formula, data=work, vcov={"CRV1": CLUSTER})
    tidy = fit.tidy()
    rows = []
    component_suffixes = {
        "baseline_treatment_effect": ":treated",
        "high_minus_low_ddd": ":treated_X_disp",
        "common_high_minus_low_shift": ":disp_binary",
    }
    for component, suffix in component_suffixes.items():
        for term in tidy.index:
            term_string = str(term)
            period = term_period(term_string)
            if period is None or not term_string.endswith(suffix):
                continue
            values = tidy.loc[term]
            rows.append(
                {
                    "scope": scope,
                    "outcome": outcome,
                    "component": component,
                    "rel_t": period,
                    "term": term_string,
                    "coef": float(values["Estimate"]),
                    "se": float(values["Std. Error"]),
                    "pvalue": float(values["Pr(>|t|)"]),
                    "ci_low": float(values["2.5%"]),
                    "ci_high": float(values["97.5%"]),
                    "n": int(fit._N),
                }
            )
    pre_rows = []
    for test_name, suffix in [
        ("pretrend_baseline_joint_zero", ":treated"),
        ("pretrend_ddd_joint_zero", ":treated_X_disp"),
    ]:
        terms = [
            str(term)
            for term in tidy.index
            if str(term).endswith(suffix)
            and term_period(str(term)) in {-4, -3, -2}
        ]
        statistic, pvalue = joint_zero_test(fit, terms)
        pre_rows.append(
            {
                "scope": scope,
                "outcome": outcome,
                "test": test_name,
                "n_restrictions": len(terms),
                "statistic": statistic,
                "pvalue": pvalue,
                "n": int(fit._N),
            }
        )
    return pd.DataFrame(rows), pd.DataFrame(pre_rows)


def build_support(panel: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for scope in SCOPES:
        outcome = f"novelty_{scope}"
        any_col = f"any_purchase_{scope}"
        n_col = f"n_products_{scope}"
        for keys, group in panel.groupby(
            ["treated", "disp_binary", "rel_t"], sort=True, dropna=False
        ):
            rows.append(
                {
                    "scope": scope,
                    "treated": int(keys[0]),
                    "disp_binary": int(keys[1]),
                    "rel_t": int(keys[2]),
                    "member_period_rows": int(len(group)),
                    "purchasing_rows": int(group[any_col].sum()),
                    "purchase_entry_rate": float(group[any_col].mean()),
                    "mean_novelty_conditional": float(group[outcome].mean()),
                    "mean_distinct_products_conditional": float(
                        group.loc[group[any_col].eq(1), n_col].mean()
                    ),
                }
            )
    return pd.DataFrame(rows)


def make_summary(
    ddd: pd.DataFrame,
    pretrends: pd.DataFrame,
    panel: pd.DataFrame,
    audit: dict,
) -> str:
    lines = [
        "# Non-coffee novelty-seeking robustness check",
        "",
        "## Result",
        "",
    ]
    for scope in SCOPES:
        novelty = ddd[
            (ddd["scope"].eq(scope))
            & (ddd["outcome_type"].eq("conditional_novelty"))
            & (ddd["estimand"].eq("high_minus_low_ddd"))
        ].iloc[0]
        entry = ddd[
            (ddd["scope"].eq(scope))
            & (ddd["outcome_type"].eq("purchase_entry"))
            & (ddd["estimand"].eq("high_minus_low_ddd"))
        ].iloc[0]
        pretrend = pretrends[
            (pretrends["scope"].eq(scope))
            & (pretrends["test"].eq("pretrend_ddd_joint_zero"))
        ].iloc[0]
        pre_mean = panel.loc[
            panel["rel_t"].lt(0), f"novelty_{scope}"
        ].mean()
        lines.extend(
            [
                f"- **{scope}**: novelty DDD {novelty.coef:+.4f} "
                f"(SE {novelty.se:.4f}, 95% CI [{novelty.ci_low:.4f}, {novelty.ci_high:.4f}], "
                f"CRV1 p={novelty.pvalue:.4f}, restricted wild p={novelty.pvalue_wild_restricted:.4f}; "
                f"N={int(novelty.n):,}). The conditional pre-period mean is {pre_mean:.4f}; "
                f"the differential pretrend p-value is {pretrend.pvalue:.4f}. "
                f"The any-purchase DDD is {entry.coef:+.4f} (SE {entry.se:.4f}, p={entry.pvalue:.4f}).",
            ]
        )
    headline = ddd[
        ddd["scope"].eq("headline_all_products")
        & ddd["estimand"].eq("high_minus_low_ddd")
    ].iloc[0]
    lines.extend(
        [
            "",
            "## Benchmark",
            "",
            f"The temporary estimator reproduces the headline all-product novelty DDD: "
            f"{headline.coef:+.4f} (SE {headline.se:.4f}, p={headline.pvalue:.4f}; N={int(headline.n):,}).",
            "",
            "## Construction",
            "",
            f"The raw scan covers {audit['raw_rows']:,} commodity rows. Every source row has exactly one populated category field. "
            "The primary definition combines non-coffee drinks, food and other non-coffee products; category and exact description jointly identify a product.",
            "",
            "The novelty outcome is conditional on purchasing at least one product in the selected non-coffee scope. "
            "The any-purchase DDD and cell-specific entry rates diagnose the resulting sample-selection margin.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    project_root = args.project_root.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    panel, headline_path = load_headline_grid(project_root)
    member_ids = set(panel["member_id"].dropna().astype(int).unique())
    raw_path = project_root.parent / "data/data1031/order_commodity_result.csv"
    transactions, crosswalk, audit = load_and_classify_transactions(
        raw_path, member_ids, args.chunksize
    )
    panel = construct_outcomes(panel, transactions)

    crosswalk.to_csv(output_dir / "product_classification.csv", index=False)
    transactions.to_parquet(output_dir / "noncoffee_transactions.parquet", index=False)
    panel.to_parquet(output_dir / "noncoffee_novelty_panel.parquet", index=False)
    with (output_dir / "classification_audit.json").open("w", encoding="utf-8") as handle:
        json.dump(audit, handle, ensure_ascii=False, indent=2, default=str)

    ddd_rows: list[dict] = []
    event_frames: list[pd.DataFrame] = []
    pretrend_frames: list[pd.DataFrame] = []
    wild_audit = []

    headline_rows, headline_wild = fit_collapsed(
        panel,
        "variety_seeking",
        "headline_all_products",
        "conditional_novelty",
        args.bootstrap_reps,
        SEED,
    )
    ddd_rows.extend(headline_rows)
    headline_event, headline_pretrend = fit_event_study(
        panel, "variety_seeking", "headline_all_products"
    )
    event_frames.append(headline_event)
    pretrend_frames.append(headline_pretrend)
    wild_audit.append({"scope": "headline_all_products", **headline_wild})

    for scope_index, scope in enumerate(SCOPES, start=1):
        novelty_outcome = f"novelty_{scope}"
        rows, wild = fit_collapsed(
            panel,
            novelty_outcome,
            scope,
            "conditional_novelty",
            args.bootstrap_reps,
            SEED + scope_index,
        )
        ddd_rows.extend(rows)
        wild_audit.append({"scope": scope, **wild})
        event, pretrend = fit_event_study(panel, novelty_outcome, scope)
        event_frames.append(event)
        pretrend_frames.append(pretrend)

        entry_outcome = f"any_purchase_{scope}"
        entry_rows, _ = fit_collapsed(
            panel,
            entry_outcome,
            scope,
            "purchase_entry",
            0,
            SEED + 100 + scope_index,
        )
        ddd_rows.extend(entry_rows)

    ddd = pd.DataFrame(ddd_rows)
    events = pd.concat(event_frames, ignore_index=True)
    pretrends = pd.concat(pretrend_frames, ignore_index=True)
    support = build_support(panel)
    wild_audit_df = pd.DataFrame(wild_audit)

    saved_headline = pd.read_csv(
        headline_path.parent / "ddd_binary_results.csv", encoding="utf-8-sig"
    )
    saved_ddd = saved_headline[
        saved_headline["estimand"].eq("high_minus_low_ddd")
    ].iloc[0]
    temporary_ddd = ddd[
        ddd["scope"].eq("headline_all_products")
        & ddd["estimand"].eq("high_minus_low_ddd")
    ].iloc[0]
    benchmark = pd.DataFrame(
        [
            {
                "saved_coef": float(saved_ddd.coef),
                "temporary_coef": float(temporary_ddd.coef),
                "coef_difference": float(temporary_ddd.coef - saved_ddd.coef),
                "saved_se": float(saved_ddd.se),
                "temporary_se": float(temporary_ddd.se),
                "se_difference": float(temporary_ddd.se - saved_ddd.se),
                "saved_n": int(saved_ddd.n),
                "temporary_n": int(temporary_ddd.n),
            }
        ]
    )

    ddd.to_csv(output_dir / "ddd_results.csv", index=False)
    events.to_csv(output_dir / "event_study_results.csv", index=False)
    pretrends.to_csv(output_dir / "pretrend_tests.csv", index=False)
    support.to_csv(output_dir / "sample_support.csv", index=False)
    wild_audit_df.to_csv(output_dir / "wild_bootstrap_audit.csv", index=False)
    benchmark.to_csv(output_dir / "headline_reproduction.csv", index=False)
    (output_dir / "SUMMARY.md").write_text(
        make_summary(ddd, pretrends, panel, audit), encoding="utf-8"
    )
    metadata = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "project_root": str(project_root),
        "output_dir": str(output_dir),
        "headline_sample": str(headline_path),
        "raw_commodity_source": str(raw_path),
        "python": sys.version,
        "pyfixest": pf.__version__,
        "bootstrap_reps": args.bootstrap_reps,
        "seed": SEED,
        "scopes": {key: sorted(value) for key, value in SCOPES.items()},
        "fixed_effects": FIXED_EFFECTS,
        "cluster": CLUSTER,
    }
    (output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print((output_dir / "SUMMARY.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
