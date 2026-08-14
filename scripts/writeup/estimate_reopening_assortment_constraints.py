"""Estimate the reopening-assortment analyses specified in the manuscript.

The primary analysis follows realized assortment at each of the 18 treated
stores over four fixed seven-day periods after reopening.  It estimates week
2--4 changes relative to week 1 with closure-event fixed effects and tests
whether those changes are jointly zero.  The secondary analysis retains the
manuscript's matched-store comparison as a supplementary check.

Product transactions identify realized assortment, not the exact menu shown
or inventory available to an individual customer.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from scipy import stats


SEED = 20260807
RELATIVE_WEEKS = (-4, -3, -2, -1, 1, 2, 3, 4)
POST_WEEKS = (1, 2, 3, 4)
OUTCOMES = ("core_coverage", "rarefied_products_50", "menu_jaccard_pre")
OUTCOME_LABELS = {
    "core_coverage": "Core-product coverage",
    "rarefied_products_50": "Products per 50 baskets",
    "menu_jaccard_pre": "Pre-menu overlap",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/05_robustness/reopening_assortment_constraints"),
    )
    parser.add_argument("--bootstrap-reps", type=int, default=9999)
    return parser.parse_args()


def resolve_under_root(project_root: Path, path: Path) -> Path:
    return path if path.is_absolute() else project_root / path


def ensure_columns(df: pd.DataFrame, required: Iterable[str], label: str) -> None:
    missing = sorted(set(required) - set(df.columns))
    if missing:
        raise ValueError(f"{label} is missing required columns: {missing}")


def normalize_date(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, errors="coerce").dt.normalize()


def parse_control_ids(value: object) -> list[int]:
    if pd.isna(value):
        return []
    return [int(float(item)) for item in str(value).split("|") if item.strip()]


def read_registry(project_root: Path) -> pd.DataFrame:
    path = project_root / "outputs/customer-store/closure_pair_registry.csv"
    registry = pd.read_csv(path, encoding="utf-8-sig")
    ensure_columns(
        registry,
        ["dept_id", "closure_start", "closure_end", "control_store_ids", "status"],
        "closure registry",
    )
    registry = registry[registry["status"].fillna("").str.lower().eq("kept")].copy()
    registry["dept_id"] = registry["dept_id"].astype(int)
    registry["closure_start"] = normalize_date(registry["closure_start"])
    registry["closure_end"] = normalize_date(registry["closure_end"])
    registry["closure_event_id"] = (
        "dept_"
        + registry["dept_id"].astype(str)
        + "_closure_"
        + registry["closure_start"].dt.strftime("%Y-%m-%d")
    )
    if len(registry) != 18:
        raise ValueError(f"Expected 18 retained closures, found {len(registry)}.")
    if registry["closure_event_id"].duplicated().any():
        raise ValueError("Closure registry contains duplicate retained events.")
    return registry


def load_store_product_orders(
    project_root: Path,
    store_ids: set[int],
    min_date: pd.Timestamp,
    max_date: pd.Timestamp,
) -> tuple[pd.DataFrame, dict]:
    path = project_root / "data/processed/order_commodity_result_processed.csv"
    frames: list[pd.DataFrame] = []
    rows_scanned = 0
    store_strings = {str(store_id) for store_id in store_ids}
    for chunk in pd.read_csv(
        path,
        encoding="utf-8-sig",
        usecols=["member_id", "dept_id", "dt", "product_id"],
        chunksize=1_000_000,
    ):
        rows_scanned += len(chunk)
        chunk = chunk[chunk["dept_id"].astype(str).isin(store_strings)].copy()
        if chunk.empty:
            continue
        chunk["dt"] = normalize_date(chunk["dt"])
        chunk = chunk[chunk["dt"].between(min_date, max_date)]
        if not chunk.empty:
            frames.append(chunk)
    if not frames:
        raise ValueError("No product transactions matched the selected stores and dates.")
    orders = pd.concat(frames, ignore_index=True)
    orders["member_id"] = orders["member_id"].astype(int)
    orders["dept_id"] = orders["dept_id"].astype(int)
    orders["product_id"] = orders["product_id"].astype(int)
    orders = orders.drop_duplicates(["member_id", "dept_id", "dt", "product_id"])
    orders["basket_id"] = (
        orders["member_id"].astype(str)
        + "|"
        + orders["dept_id"].astype(str)
        + "|"
        + orders["dt"].dt.strftime("%Y-%m-%d")
    )
    audit = {
        "source": str(path),
        "rows_scanned": int(rows_scanned),
        "deduplicated_product_rows_retained": int(len(orders)),
        "members": int(orders["member_id"].nunique()),
        "stores_with_transactions": int(orders["dept_id"].nunique()),
        "date_min": str(orders["dt"].min().date()),
        "date_max": str(orders["dt"].max().date()),
    }
    return orders, audit


def rarefied_product_count(
    group: pd.DataFrame,
    *,
    basket_target: int = 50,
    draws: int = 100,
    seed_offset: int = 0,
) -> float:
    baskets = group["basket_id"].drop_duplicates().to_numpy()
    if len(baskets) < basket_target:
        return np.nan
    product_sets = group.groupby("basket_id")["product_id"].agg(
        lambda values: set(values.astype(int))
    )
    rng = np.random.default_rng(SEED + seed_offset)
    counts: list[int] = []
    for _ in range(draws):
        selected = rng.choice(baskets, size=basket_target, replace=False)
        products: set[int] = set()
        for basket in selected:
            products.update(product_sets.loc[basket])
        counts.append(len(products))
    return float(np.mean(counts))


def build_store_event_panel(
    registry: pd.DataFrame,
    orders: pd.DataFrame,
) -> tuple[pd.DataFrame, dict]:
    store_rows: list[dict] = []
    for _, event in registry.iterrows():
        stores = [(int(event["dept_id"]), 1)] + [
            (store_id, 0) for store_id in parse_control_ids(event["control_store_ids"])
        ]
        if len(stores) != 6:
            raise ValueError(
                f"{event['closure_event_id']} does not have one treated and five controls."
            )
        for store_id, treated_store in stores:
            store_rows.append(
                {
                    "closure_event_id": event["closure_event_id"],
                    "treated_dept_id": int(event["dept_id"]),
                    "store_id": int(store_id),
                    "treated_store": int(treated_store),
                    "closure_start": event["closure_start"],
                    "closure_end": event["closure_end"],
                }
            )
    event_stores = pd.DataFrame(store_rows)

    fixed_bins = {
        -4: (-28, -22),
        -3: (-21, -15),
        -2: (-14, -8),
        -1: (-7, -1),
        1: (1, 7),
        2: (8, 14),
        3: (15, 21),
        4: (22, 28),
    }
    rows: list[dict] = []
    product_cache: dict[tuple[str, int, int], set[int]] = {}
    for event_index, event_store in event_stores.iterrows():
        event_id = str(event_store["closure_event_id"])
        store_id = int(event_store["store_id"])
        store_orders = orders[orders["dept_id"].eq(store_id)]
        for relative_week, (start_offset, end_offset) in fixed_bins.items():
            anchor = (
                event_store["closure_start"]
                if relative_week < 0
                else event_store["closure_end"]
            )
            start = anchor + pd.Timedelta(days=start_offset)
            end = anchor + pd.Timedelta(days=end_offset)
            group = store_orders[store_orders["dt"].between(start, end)]
            key = (event_id, store_id, relative_week)
            product_cache[key] = set(group["product_id"].unique())
            rows.append(
                {
                    **event_store.to_dict(),
                    "rel_t": int(relative_week),
                    "post": int(relative_week > 0),
                    "period_start": start,
                    "period_end": end,
                    "n_baskets": int(group["basket_id"].nunique()),
                    "n_members": int(group["member_id"].nunique()),
                    "n_products": int(group["product_id"].nunique()),
                    "rarefied_products_50": rarefied_product_count(
                        group,
                        basket_target=50,
                        draws=100,
                        seed_offset=event_index * 10 + relative_week,
                    ),
                }
            )
    panel = pd.DataFrame(rows)

    core_sets: dict[tuple[str, int], set[int]] = {}
    pre_unions: dict[tuple[str, int], set[int]] = {}
    for event_id, store_id in panel[
        ["closure_event_id", "store_id"]
    ].drop_duplicates().itertuples(index=False):
        appearances: dict[int, int] = {}
        pre_sets = []
        for relative_week in (-4, -3, -2, -1):
            products = product_cache[(str(event_id), int(store_id), relative_week)]
            pre_sets.append(products)
            for product_id in products:
                appearances[product_id] = appearances.get(product_id, 0) + 1
        key = (str(event_id), int(store_id))
        core_sets[key] = {
            product_id for product_id, count in appearances.items() if count >= 3
        }
        pre_unions[key] = set().union(*pre_sets)

    coverage: list[float] = []
    overlap: list[float] = []
    for row in panel.itertuples(index=False):
        key = (str(row.closure_event_id), int(row.store_id))
        current = product_cache[(key[0], key[1], int(row.rel_t))]
        core = core_sets[key]
        pre_union = pre_unions[key]
        coverage.append(len(current & core) / len(core) if core else np.nan)
        denominator = current | pre_union
        overlap.append(len(current & pre_union) / len(denominator) if denominator else np.nan)
    panel["core_coverage"] = coverage
    panel["menu_jaccard_pre"] = overlap
    panel["event_store_fe"] = panel["closure_event_id"] + "|" + panel["store_id"].astype(str)
    panel["event_rel_fe"] = panel["closure_event_id"] + "|" + panel["rel_t"].astype(str)
    panel["treated_store_X_post"] = panel["treated_store"] * panel["post"]
    if panel.duplicated(["closure_event_id", "store_id", "rel_t"]).any():
        raise ValueError("Store-event panel is not unique at its intended grain.")

    audit = {
        "closures": int(panel["closure_event_id"].nunique()),
        "event_store_pairs": int(panel["event_store_fe"].nunique()),
        "rows": int(len(panel)),
        "treated_event_store_pairs": int(
            panel.loc[panel["treated_store"].eq(1), "event_store_fe"].nunique()
        ),
        "control_event_store_pairs": int(
            panel.loc[panel["treated_store"].eq(0), "event_store_fe"].nunique()
        ),
        "share_rarefied_observed": float(panel["rarefied_products_50"].notna().mean()),
        "median_baskets": float(panel["n_baskets"].median()),
    }
    return panel, audit


def drop_singleton_fixed_effects(df: pd.DataFrame, fe_cols: list[str]) -> pd.DataFrame:
    work = df.copy()
    while True:
        keep = np.ones(len(work), dtype=bool)
        for column in fe_cols:
            keep &= (
                work.groupby(column, observed=True)[column]
                .transform("size")
                .to_numpy()
                > 1
            )
        if keep.all():
            return work
        work = work.loc[keep].copy()


def residualize_fixed_effects(
    values: np.ndarray,
    codes_list: list[np.ndarray],
    tolerance: float = 1e-10,
    max_iterations: int = 1000,
) -> np.ndarray:
    residual = np.asarray(values, dtype=np.float64).copy()
    if residual.ndim == 1:
        residual = residual[:, None]
    for _ in range(max_iterations):
        previous = residual.copy()
        for codes in codes_list:
            n_groups = int(codes.max()) + 1
            counts = np.bincount(codes, minlength=n_groups).astype(np.float64)
            for column in range(residual.shape[1]):
                sums = np.bincount(codes, weights=residual[:, column], minlength=n_groups)
                residual[:, column] -= (sums / counts)[codes]
        if float(np.max(np.abs(residual - previous))) < tolerance:
            return residual
    raise RuntimeError("Fixed-effect absorption failed to converge.")


def fit_fe_ols(
    df: pd.DataFrame,
    outcome: str,
    regressors: list[str],
    fe_cols: list[str],
    cluster_col: str,
) -> dict:
    required = [outcome, *regressors, *fe_cols, cluster_col]
    work = drop_singleton_fixed_effects(df.dropna(subset=required), fe_cols)
    codes_list = [pd.factorize(work[column], sort=False)[0] for column in fe_cols]
    matrix = work[[outcome, *regressors]].to_numpy(dtype=np.float64)
    residualized = residualize_fixed_effects(matrix, codes_list)
    y = residualized[:, 0]
    X = residualized[:, 1:]
    bread = np.linalg.inv(X.T @ X)
    beta = bread @ (X.T @ y)
    errors = y - X @ beta
    within_r2 = 1.0 - float(errors @ errors) / float(y @ y)
    cluster_codes, cluster_labels = pd.factorize(work[cluster_col], sort=False)
    n_clusters = len(cluster_labels)
    scores = np.zeros((n_clusters, len(regressors)), dtype=np.float64)
    np.add.at(scores, cluster_codes, X * errors[:, None])
    n = len(work)
    k = len(regressors)
    correction = (n_clusters / (n_clusters - 1)) * ((n - 1) / (n - k))
    covariance = correction * bread @ (scores.T @ scores) @ bread
    standard_errors = np.sqrt(np.maximum(np.diag(covariance), 0.0))
    degrees_freedom = n_clusters - 1
    pvalues = 2 * stats.t.sf(np.abs(beta / standard_errors), df=degrees_freedom)
    critical = stats.t.ppf(0.975, df=degrees_freedom)
    return {
        "names": regressors,
        "beta": beta,
        "covariance": covariance,
        "standard_errors": standard_errors,
        "pvalues": pvalues,
        "ci_low": beta - critical * standard_errors,
        "ci_high": beta + critical * standard_errors,
        "n": n,
        "n_clusters": n_clusters,
        "cluster_df": degrees_freedom,
        "event_store_pairs": int(work["event_store_fe"].nunique()),
        "within_r2": within_r2,
        "work": work,
        "X": X,
        "y": y,
        "bread": bread,
        "cluster_codes": cluster_codes,
        "cluster_labels": cluster_labels,
        "correction": correction,
    }


def extract_term(fit: dict, term: str) -> dict:
    index = fit["names"].index(term)
    return {
        "term": term,
        "coef": float(fit["beta"][index]),
        "se_crv1": float(fit["standard_errors"][index]),
        "pvalue_crv1": float(fit["pvalues"][index]),
        "ci_low": float(fit["ci_low"][index]),
        "ci_high": float(fit["ci_high"][index]),
        "n": int(fit["n"]),
        "n_clusters": int(fit["n_clusters"]),
        "event_store_pairs": int(fit["event_store_pairs"]),
        "within_r2": float(fit["within_r2"]),
    }


def joint_zero_test(fit: dict, terms: list[str]) -> dict:
    indices = [fit["names"].index(term) for term in terms]
    restriction = fit["beta"][indices]
    covariance = fit["covariance"][np.ix_(indices, indices)]
    q = len(indices)
    f_statistic = float(restriction.T @ np.linalg.pinv(covariance) @ restriction / q)
    return {
        "f_statistic": f_statistic,
        "df_num": q,
        "df_denom": int(fit["cluster_df"]),
        "pvalue": float(stats.f.sf(f_statistic, q, fit["cluster_df"])),
    }


def restricted_wild_cluster_joint_pvalue(
    fit: dict,
    terms: list[str],
    repetitions: int,
    seed: int,
) -> float:
    indices = [fit["names"].index(term) for term in terms]
    X = fit["X"]
    y = fit["y"]
    cluster_codes = fit["cluster_codes"]
    group_count = len(fit["cluster_labels"])
    keep = [index for index in range(X.shape[1]) if index not in indices]
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

    observed_beta = fit["beta"][indices]
    observed_covariance = fit["covariance"][np.ix_(indices, indices)]
    observed_statistic = float(
        observed_beta.T @ np.linalg.pinv(observed_covariance) @ observed_beta
    )
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
        restricted_beta = beta_star[indices]
        restricted_covariance = covariance_star[np.ix_(indices, indices)]
        statistic_star = float(
            restricted_beta.T
            @ np.linalg.pinv(restricted_covariance)
            @ restricted_beta
        )
        exceedances += int(statistic_star >= observed_statistic)
    return (exceedances + 1) / (repetitions + 1)


def complete_period_sample(
    df: pd.DataFrame,
    outcome: str,
    periods: tuple[int, ...],
) -> pd.DataFrame:
    work = df[df["rel_t"].isin(periods)].dropna(subset=[outcome]).copy()
    counts = work.groupby("event_store_fe")["rel_t"].nunique()
    complete_pairs = set(counts[counts.eq(len(periods))].index)
    return work[work["event_store_fe"].isin(complete_pairs)].copy()


def estimate_treated_post_paths(
    panel: pd.DataFrame,
    bootstrap_reps: int,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    results: list[dict] = []
    joint_tests: list[dict] = []
    support: list[dict] = []
    weekly_means: list[dict] = []
    checks: list[dict] = []
    base = panel[panel["treated_store"].eq(1) & panel["rel_t"].isin(POST_WEEKS)].copy()
    for week in POST_WEEKS[1:]:
        base[f"week_{week}"] = base["rel_t"].eq(week).astype(int)
    terms = [f"week_{week}" for week in POST_WEEKS[1:]]

    for outcome in OUTCOMES:
        samples = {
            "complete_4_post_weeks": complete_period_sample(base, outcome, POST_WEEKS),
            "available_post_weeks": base.dropna(subset=[outcome]).copy(),
        }
        for sample_name, work in samples.items():
            fit = fit_fe_ols(
                work,
                outcome,
                terms,
                ["closure_event_id"],
                "closure_event_id",
            )
            for term in terms:
                row = extract_term(fit, term)
                row.update(
                    {
                        "outcome": outcome,
                        "sample": sample_name,
                        "relative_week": int(term.split("_")[-1]),
                    }
                )
                results.append(row)
            joint = joint_zero_test(fit, terms)
            joint.update(
                {
                    "outcome": outcome,
                    "sample": sample_name,
                    "n": int(fit["n"]),
                    "n_clusters": int(fit["n_clusters"]),
                    "pvalue_wild_restricted": restricted_wild_cluster_joint_pvalue(
                        fit,
                        terms,
                        bootstrap_reps,
                        SEED + 1000 * OUTCOMES.index(outcome) + len(sample_name),
                    ),
                    "bootstrap_reps": bootstrap_reps,
                }
            )
            joint_tests.append(joint)
            support.append(
                {
                    "outcome": outcome,
                    "sample": sample_name,
                    "observations": int(fit["n"]),
                    "treated_stores": int(fit["n_clusters"]),
                    "week_1_mean": float(
                        fit["work"].loc[fit["work"]["rel_t"].eq(1), outcome].mean()
                    ),
                }
            )
            for week, group in fit["work"].groupby("rel_t"):
                weekly_means.append(
                    {
                        "outcome": outcome,
                        "sample": sample_name,
                        "relative_week": int(week),
                        "mean": float(group[outcome].mean()),
                        "observations": int(len(group)),
                    }
                )

            if sample_name == "complete_4_post_weeks":
                pivot = fit["work"].pivot(
                    index="closure_event_id", columns="rel_t", values=outcome
                )
                for term in terms:
                    week = int(term.split("_")[-1])
                    model_coef = extract_term(fit, term)["coef"]
                    direct_coef = float((pivot[week] - pivot[1]).mean())
                    checks.append(
                        {
                            "check": f"{outcome}: week {week} coefficient equals mean within-event change",
                            "passed": bool(np.isclose(model_coef, direct_coef, atol=1e-10)),
                            "observed": model_coef,
                            "expected": direct_coef,
                        }
                    )
    return (
        pd.DataFrame(results),
        pd.DataFrame(joint_tests),
        pd.DataFrame(support),
        pd.DataFrame(weekly_means),
        pd.DataFrame(checks),
    )


def estimate_matched_store_models(
    panel: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    results: list[dict] = []
    event_paths: list[dict] = []
    pretrends: list[dict] = []
    support: list[dict] = []
    for outcome in OUTCOMES:
        for sample_name in ("available_unbalanced", "complete_8_period_pairs"):
            work = panel.dropna(subset=[outcome]).copy()
            if sample_name == "complete_8_period_pairs":
                work = complete_period_sample(work, outcome, RELATIVE_WEEKS)
            support.append(
                {
                    "outcome": outcome,
                    "sample": sample_name,
                    "rows_before_singleton_pruning": int(len(work)),
                    "event_store_pairs_before_singleton_pruning": int(
                        work["event_store_fe"].nunique()
                    ),
                    "closures": int(work["closure_event_id"].nunique()),
                }
            )

            pooled = fit_fe_ols(
                work,
                outcome,
                ["treated_store_X_post"],
                ["event_store_fe", "event_rel_fe"],
                "closure_event_id",
            )
            pooled_row = extract_term(pooled, "treated_store_X_post")
            pooled_row.update(
                {"outcome": outcome, "sample": sample_name, "model": "pooled_post"}
            )
            results.append(pooled_row)

            terms: list[str] = []
            term_map: dict[str, int] = {}
            for relative_week in RELATIVE_WEEKS:
                if relative_week == -1:
                    continue
                suffix = f"m{abs(relative_week)}" if relative_week < 0 else f"p{relative_week}"
                term = f"rt_{suffix}_X_treated_store"
                work[term] = work["rel_t"].eq(relative_week).astype(int) * work[
                    "treated_store"
                ]
                terms.append(term)
                term_map[term] = relative_week
            dynamic = fit_fe_ols(
                work,
                outcome,
                terms,
                ["event_store_fe", "event_rel_fe"],
                "closure_event_id",
            )
            immediate_row = extract_term(dynamic, "rt_p1_X_treated_store")
            immediate_row.update(
                {"outcome": outcome, "sample": sample_name, "model": "immediate_post"}
            )
            results.append(immediate_row)

            pre_terms = [term for term, period in term_map.items() if period < -1]
            pretrend = joint_zero_test(dynamic, pre_terms)
            pretrend.update({"outcome": outcome, "sample": sample_name})
            pretrends.append(pretrend)
            if sample_name == "available_unbalanced":
                for term, relative_week in term_map.items():
                    row = extract_term(dynamic, term)
                    row.update({"outcome": outcome, "relative_week": relative_week})
                    event_paths.append(row)
    return (
        pd.DataFrame(results),
        pd.DataFrame(event_paths),
        pd.DataFrame(pretrends),
        pd.DataFrame(support),
    )


def read_treated_member_events(project_root: Path) -> pd.DataFrame:
    path = (
        project_root
        / "outputs/03_main_18_closures/novelty_member_first_ddd_h4/estimation_sample.csv"
    )
    sample = pd.read_csv(
        path,
        encoding="utf-8-sig",
        usecols=[
            "member_id",
            "dept_id",
            "closure_event_id",
            "closure_end",
            "treated",
            "disp_binary",
        ],
    ).drop_duplicates(["member_id", "closure_event_id"])
    sample = sample[sample["treated"].eq(1)].copy()
    sample["member_id"] = sample["member_id"].astype(int)
    sample["dept_id"] = sample["dept_id"].astype(int)
    sample["disp_binary"] = sample["disp_binary"].astype(int)
    sample["closure_end"] = normalize_date(sample["closure_end"])
    if sample.duplicated("member_id").any():
        raise ValueError("A treated member belongs to more than one closure event.")
    if sample["closure_event_id"].nunique() != 18:
        raise ValueError("Treated member sample does not contain all 18 closure events.")
    return sample


def load_member_product_histories(
    project_root: Path,
    member_events: pd.DataFrame,
) -> tuple[dict[int, set[int]], dict]:
    """Load each treated member's product history through the closure end date."""
    path = project_root / "data/processed/order_commodity_result_processed.csv"
    member_ids = set(member_events["member_id"].astype(int))
    closure_ends = member_events.set_index("member_id")["closure_end"]
    frames: list[pd.DataFrame] = []
    rows_scanned = 0
    for chunk in pd.read_csv(
        path,
        encoding="utf-8-sig",
        usecols=["member_id", "dt", "product_id"],
        chunksize=1_000_000,
    ):
        rows_scanned += len(chunk)
        chunk = chunk[chunk["member_id"].isin(member_ids)].copy()
        if chunk.empty:
            continue
        chunk["dt"] = normalize_date(chunk["dt"])
        chunk["closure_end"] = chunk["member_id"].map(closure_ends)
        chunk = chunk[
            chunk["dt"].notna()
            & chunk["product_id"].notna()
            & chunk["dt"].le(chunk["closure_end"])
        ]
        if not chunk.empty:
            frames.append(chunk[["member_id", "product_id"]])
    if not frames:
        raise ValueError("No pre-reopening product histories found for treated members.")
    histories = pd.concat(frames, ignore_index=True)
    histories["member_id"] = histories["member_id"].astype(int)
    histories["product_id"] = histories["product_id"].astype(int)
    histories = histories.drop_duplicates(["member_id", "product_id"])
    history_sets = {
        int(member_id): set(group["product_id"].astype(int))
        for member_id, group in histories.groupby("member_id", observed=True)
    }
    missing_members = member_ids - set(history_sets)
    for member_id in missing_members:
        history_sets[int(member_id)] = set()
    audit = {
        "source": str(path),
        "rows_scanned": int(rows_scanned),
        "members": int(len(history_sets)),
        "members_with_empty_product_history": int(len(missing_members)),
        "distinct_member_product_pairs": int(len(histories)),
        "history_cutoff": "member-specific closure_end (inclusive)",
    }
    return history_sets, audit


def build_first_return_exposure(
    member_events: pd.DataFrame,
    orders: pd.DataFrame,
    panel: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    visit_days = orders[["member_id", "dept_id", "dt"]].drop_duplicates()
    visit_days = visit_days[visit_days["member_id"].isin(member_events["member_id"])]
    visits = member_events.merge(
        visit_days,
        on=["member_id", "dept_id"],
        how="left",
        validate="one_to_many",
    )
    visits = visits[
        visits["dt"].gt(visits["closure_end"])
        & visits["dt"].le(visits["closure_end"] + pd.Timedelta(days=28))
    ].copy()
    visits["days_after_reopening"] = (visits["dt"] - visits["closure_end"]).dt.days
    visits["relative_week"] = (
        (visits["days_after_reopening"] - 1) // 7 + 1
    ).astype(int)
    first_returns = (
        visits.sort_values(["member_id", "dt"])
        .drop_duplicates(["member_id", "closure_event_id"])
        .copy()
    )

    treated_weeks = panel[
        panel["treated_store"].eq(1) & panel["rel_t"].isin(POST_WEEKS)
    ][["closure_event_id", "store_id", "rel_t", *OUTCOMES]].rename(
        columns={"store_id": "dept_id", "rel_t": "relative_week"}
    )
    first_returns = first_returns.merge(
        treated_weeks,
        on=["closure_event_id", "dept_id", "relative_week"],
        how="left",
        validate="many_to_one",
    )
    if first_returns[["core_coverage", "menu_jaccard_pre"]].isna().any().any():
        raise ValueError("First-return panel failed to map realized assortment.")
    first_returns["event_store_fe"] = first_returns["closure_event_id"]

    timing = member_events.merge(
        first_returns[["member_id", "days_after_reopening", "relative_week"]],
        on="member_id",
        how="left",
        validate="one_to_one",
    )
    timing["returned_within_28_days"] = timing["days_after_reopening"].notna().astype(int)
    distribution = (
        timing.groupby("disp_binary", observed=True)
        .agg(
            eligible_members=("member_id", "size"),
            returned_within_28_days=("returned_within_28_days", "sum"),
            share_returned_within_28_days=("returned_within_28_days", "mean"),
            mean_days_after_reopening=("days_after_reopening", "mean"),
            median_days_after_reopening=("days_after_reopening", "median"),
        )
        .reset_index()
    )
    week_distribution = (
        first_returns.groupby(["disp_binary", "relative_week"], observed=True)
        .size()
        .rename("returners")
        .reset_index()
    )
    week_distribution["share_of_group_returners"] = week_distribution[
        "returners"
    ] / week_distribution.groupby("disp_binary")["returners"].transform("sum")
    distribution = distribution.merge(
        week_distribution.pivot(
            index="disp_binary",
            columns="relative_week",
            values="share_of_group_returners",
        )
        .rename(columns=lambda week: f"share_returning_week_{int(week)}")
        .reset_index(),
        on="disp_binary",
        how="left",
        validate="one_to_one",
    )
    return first_returns, distribution


def build_return_week_novel_opportunity(
    first_returns: pd.DataFrame,
    history_sets: dict[int, set[int]],
    orders: pd.DataFrame,
    panel: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Measure personal novel-product opportunity in each possible return week.

    The realized assortment for a member-week excludes any product sold only to
    that member, retaining products also purchased by somebody else. Novel
    products are those absent from the member's purchase
    history through the focal closure's end date.  The timing deviation compares
    the actual return week's opportunity with the same member's equal-weighted
    mean opportunity across all four post-reopening weeks.
    """
    treated_weeks = panel[
        panel["treated_store"].eq(1) & panel["rel_t"].isin(POST_WEEKS)
    ][
        [
            "closure_event_id",
            "store_id",
            "rel_t",
            "period_start",
            "period_end",
        ]
    ].copy()
    week_products: dict[tuple[str, int], set[int]] = {}
    member_exclusive_products: dict[tuple[str, int, int], set[int]] = {}
    for week in treated_weeks.itertuples(index=False):
        group = orders[
            orders["dept_id"].eq(int(week.store_id))
            & orders["dt"].between(week.period_start, week.period_end)
        ]
        key = (str(week.closure_event_id), int(week.rel_t))
        week_products[key] = set(group["product_id"].astype(int))
        product_buyers = group[["member_id", "product_id"]].drop_duplicates()
        buyer_counts = product_buyers.groupby("product_id", observed=True)[
            "member_id"
        ].transform("size")
        exclusive = product_buyers[buyer_counts.eq(1)]
        for member_id, member_group in exclusive.groupby("member_id", observed=True):
            member_exclusive_products[(key[0], key[1], int(member_id))] = set(
                member_group["product_id"].astype(int)
            )

    rows: list[dict] = []
    for member in first_returns.itertuples(index=False):
        event_id = str(member.closure_event_id)
        member_id = int(member.member_id)
        history = history_sets[member_id]
        for week in POST_WEEKS:
            full_set = week_products[(event_id, week)]
            exclusive_products = member_exclusive_products.get(
                (event_id, week, member_id), set()
            )
            leave_one_out_set = full_set - exclusive_products
            novel_set = leave_one_out_set - history
            rows.append(
                {
                    "member_id": member_id,
                    "closure_event_id": event_id,
                    "dept_id": int(member.dept_id),
                    "disp_binary": int(member.disp_binary),
                    "actual_return_week": int(member.relative_week),
                    "candidate_return_week": int(week),
                    "is_actual_return_week": int(week == int(member.relative_week)),
                    "history_products_through_closure": int(len(history)),
                    "realized_products_leave_one_out": int(len(leave_one_out_set)),
                    "novel_products_leave_one_out": int(len(novel_set)),
                    "novel_opportunity_share_leave_one_out": (
                        len(novel_set) / len(leave_one_out_set)
                        if leave_one_out_set
                        else np.nan
                    ),
                }
            )
    opportunity_panel = pd.DataFrame(rows)
    if opportunity_panel.duplicated(
        ["member_id", "closure_event_id", "candidate_return_week"]
    ).any():
        raise ValueError("Novel-opportunity panel is not unique at member-event-week grain.")
    if not opportunity_panel.groupby(
        ["member_id", "closure_event_id"], observed=True
    ).size().eq(4).all():
        raise ValueError("Each first returner must have four candidate return weeks.")

    for outcome in (
        "realized_products_leave_one_out",
        "novel_products_leave_one_out",
        "novel_opportunity_share_leave_one_out",
    ):
        observed_weeks = opportunity_panel.groupby(
            ["member_id", "closure_event_id"], observed=True
        )[outcome].transform("count")
        opportunity_panel[f"complete_4_week_{outcome}"] = observed_weeks.eq(4).astype(int)
        opportunity_panel[f"four_week_mean_{outcome}"] = opportunity_panel.groupby(
            ["member_id", "closure_event_id"], observed=True
        )[outcome].transform("mean")
        opportunity_panel[f"timing_deviation_{outcome}"] = (
            opportunity_panel[outcome]
            - opportunity_panel[f"four_week_mean_{outcome}"]
        )

    actual = opportunity_panel[opportunity_panel["is_actual_return_week"].eq(1)].copy()
    if len(actual) != len(first_returns):
        raise ValueError("Actual-return opportunity records do not match first returners.")
    actual["event_store_fe"] = actual["closure_event_id"]
    return opportunity_panel, actual


def estimate_return_week_novel_opportunity(
    actual_opportunity: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    results: list[dict] = []
    cell_means: list[dict] = []
    outcomes = (
        "novel_opportunity_share_leave_one_out",
        "timing_deviation_novel_opportunity_share_leave_one_out",
        "novel_products_leave_one_out",
        "timing_deviation_novel_products_leave_one_out",
    )
    for outcome in outcomes:
        work = actual_opportunity
        if "novel_opportunity_share" in outcome:
            work = work[
                work[
                    "complete_4_week_novel_opportunity_share_leave_one_out"
                ].eq(1)
            ].copy()
        fit = fit_fe_ols(
            work,
            outcome,
            ["disp_binary"],
            ["closure_event_id"],
            "closure_event_id",
        )
        row = extract_term(fit, "disp_binary")
        row.update(
            {
                "outcome": outcome,
                "estimand": "high_minus_low_among_treated_first_returners",
            }
        )
        results.append(row)
        for high, group in fit["work"].groupby("disp_binary"):
            cell_means.append(
                {
                    "outcome": outcome,
                    "disp_binary": int(high),
                    "mean": float(group[outcome].mean()),
                    "observations": int(len(group)),
                }
            )
    return pd.DataFrame(results), pd.DataFrame(cell_means)


def estimate_first_return_exposure(
    first_returns: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    results: list[dict] = []
    cell_means: list[dict] = []
    for outcome in ("days_after_reopening", *OUTCOMES):
        fit = fit_fe_ols(
            first_returns,
            outcome,
            ["disp_binary"],
            ["closure_event_id"],
            "closure_event_id",
        )
        row = extract_term(fit, "disp_binary")
        row.update(
            {
                "outcome": outcome,
                "estimand": "high_minus_low_among_treated_first_returners",
            }
        )
        results.append(row)
        for high, group in fit["work"].groupby("disp_binary"):
            cell_means.append(
                {
                    "outcome": outcome,
                    "disp_binary": int(high),
                    "mean": float(group[outcome].mean()),
                    "observations": int(len(group)),
                }
            )
    return pd.DataFrame(results), pd.DataFrame(cell_means)


def write_summary(
    output_dir: Path,
    path_results: pd.DataFrame,
    path_joint: pd.DataFrame,
    path_support: pd.DataFrame,
    matched_results: pd.DataFrame,
    matched_pretrends: pd.DataFrame,
    return_distribution: pd.DataFrame,
    return_exposure: pd.DataFrame,
    return_means: pd.DataFrame,
    novel_opportunity_results: pd.DataFrame,
    novel_opportunity_means: pd.DataFrame,
    checks: pd.DataFrame,
) -> None:
    def markdown_table(frame: pd.DataFrame) -> str:
        display = frame.copy()
        for column in display.columns:
            if pd.api.types.is_float_dtype(display[column]):
                display[column] = display[column].map(
                    lambda value: "" if pd.isna(value) else f"{value:.8g}"
                )
            else:
                display[column] = display[column].map(
                    lambda value: "" if pd.isna(value) else str(value)
                )
        headers = [str(column) for column in display.columns]
        lines = [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join("---" for _ in headers) + " |",
        ]
        for row in display.itertuples(index=False, name=None):
            lines.append("| " + " | ".join(str(value) for value in row) + " |")
        return "\n".join(lines)

    primary_results = path_results[path_results["sample"].eq("complete_4_post_weeks")]
    primary_joint = path_joint[path_joint["sample"].eq("complete_4_post_weeks")]
    primary_support = path_support[path_support["sample"].eq("complete_4_post_weeks")]
    matched_primary = matched_results[
        matched_results["sample"].eq("available_unbalanced")
    ]
    matched_pre = matched_pretrends[
        matched_pretrends["sample"].eq("available_unbalanced")
    ]
    summary = [
        "# Reopening Assortment",
        "",
        "## Primary manuscript test: evolution across four weeks after reopening",
        "",
        "The primary specification uses treated stores, requires four observed post-reopening weeks for each outcome, includes closure-event fixed effects, and clusters CRV1 standard errors by closure event. Week 1 is the reference period.",
        "",
        markdown_table(primary_results),
        "",
        "### Joint week-equality tests",
        "",
        markdown_table(primary_joint),
        "",
        "### Primary-sample support",
        "",
        markdown_table(primary_support),
        "",
        "## Return timing and realized assortment at first return",
        "",
        "The return sample contains treated consumers whose first purchase at the reopened focal store occurs within 28 days. Exposure outcomes assign the realized assortment in that seven-day return week. High-minus-low regressions include closure-event fixed effects and cluster CRV1 standard errors by closure event.",
        "",
        markdown_table(return_distribution),
        "",
        markdown_table(return_exposure),
        "",
        markdown_table(return_means),
        "",
        "### Personal novel-product opportunity at the actual return week",
        "",
        "For each possible return week, the product set is leave-one-customer-out: products purchased only by the focal consumer are removed, while products also purchased by somebody else remain. A product is personally novel if the consumer did not purchase it anywhere in the chain through the closure end date. The timing-deviation outcomes subtract the same consumer's equal-weighted four-week mean, so they isolate assortment exposure due to return timing. Share regressions require a nonempty leave-one-out product set in all four weeks.",
        "",
        markdown_table(novel_opportunity_results),
        "",
        markdown_table(novel_opportunity_means),
        "",
        "## Supplementary matched-store comparison",
        "",
        markdown_table(matched_primary),
        "",
        "### Matched-store pretrend tests",
        "",
        markdown_table(matched_pre),
        "",
        "## Validation",
        "",
        markdown_table(checks),
        "",
        "Product sales proxy realized assortment; a product without a recorded sale may still have been displayed or available.",
    ]
    (output_dir / "summary.md").write_text("\n".join(summary), encoding="utf-8")


def main() -> None:
    args = parse_args()
    project_root = args.project_root.resolve()
    output_dir = resolve_under_root(project_root, args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    registry = read_registry(project_root)
    store_ids = set(registry["dept_id"].astype(int))
    for value in registry["control_store_ids"]:
        store_ids.update(parse_control_ids(value))
    min_date = registry["closure_start"].min() - pd.Timedelta(days=28)
    max_date = registry["closure_end"].max() + pd.Timedelta(days=28)
    orders, order_audit = load_store_product_orders(
        project_root, store_ids, min_date, max_date
    )
    panel, panel_audit = build_store_event_panel(registry, orders)
    (
        path_results,
        path_joint,
        path_support,
        path_means,
        validation_checks,
    ) = estimate_treated_post_paths(panel, args.bootstrap_reps)
    (
        matched_results,
        matched_event_study,
        matched_pretrends,
        matched_support,
    ) = estimate_matched_store_models(panel)
    member_events = read_treated_member_events(project_root)
    first_returns, return_distribution = build_first_return_exposure(
        member_events, orders, panel
    )
    return_exposure, return_means = estimate_first_return_exposure(first_returns)
    timing_effect = return_exposure.loc[
        return_exposure["outcome"].eq("days_after_reopening"), "coef"
    ].iloc[0]
    if timing_effect >= 0:
        raise RuntimeError(
            "The timing-channel analysis expected high-intention returners to return earlier."
        )
    history_sets, history_audit = load_member_product_histories(
        project_root, member_events
    )
    opportunity_panel, actual_opportunity = build_return_week_novel_opportunity(
        first_returns, history_sets, orders, panel
    )
    novel_opportunity_results, novel_opportunity_means = (
        estimate_return_week_novel_opportunity(actual_opportunity)
    )

    structural_checks = pd.DataFrame(
        [
            {
                "check": "registry contains 18 retained closures",
                "passed": panel_audit["closures"] == 18,
                "observed": panel_audit["closures"],
                "expected": 18,
            },
            {
                "check": "panel contains one treated store per closure",
                "passed": panel_audit["treated_event_store_pairs"] == 18,
                "observed": panel_audit["treated_event_store_pairs"],
                "expected": 18,
            },
            {
                "check": "panel grain is unique",
                "passed": not panel.duplicated(
                    ["closure_event_id", "store_id", "rel_t"]
                ).any(),
                "observed": int(
                    panel.duplicated(["closure_event_id", "store_id", "rel_t"]).sum()
                ),
                "expected": 0,
            },
            {
                "check": "first-return panel is unique at member-event grain",
                "passed": not first_returns.duplicated(
                    ["member_id", "closure_event_id"]
                ).any(),
                "observed": int(
                    first_returns.duplicated(
                        ["member_id", "closure_event_id"]
                    ).sum()
                ),
                "expected": 0,
            },
            {
                "check": "first-return panel covers 18 closure events",
                "passed": first_returns["closure_event_id"].nunique() == 18,
                "observed": int(first_returns["closure_event_id"].nunique()),
                "expected": 18,
            },
            {
                "check": "novel-opportunity panel has four weeks per returner",
                "passed": len(opportunity_panel) == 4 * len(first_returns),
                "observed": int(len(opportunity_panel)),
                "expected": int(4 * len(first_returns)),
            },
            {
                "check": "novel-opportunity share lies in the unit interval",
                "passed": opportunity_panel[
                    "novel_opportunity_share_leave_one_out"
                ].dropna().between(0, 1).all(),
                "observed": float(
                    opportunity_panel[
                        "novel_opportunity_share_leave_one_out"
                    ].max()
                ),
                "expected": "maximum no greater than 1",
            },
            {
                "check": "leave-one-out novel-opportunity share is observed",
                "passed": opportunity_panel[
                    "novel_opportunity_share_leave_one_out"
                ].notna().any(),
                "observed": float(
                    opportunity_panel[
                        "novel_opportunity_share_leave_one_out"
                    ].notna().mean()
                ),
                "expected": "reported; missing means no leave-one-customer-out sale",
            },
            {
                "check": "timing deviations average to zero within returner",
                "passed": bool(
                    np.allclose(
                        opportunity_panel.groupby(
                            ["member_id", "closure_event_id"], observed=True
                        )[
                            "timing_deviation_novel_opportunity_share_leave_one_out"
                        ].mean(),
                        0.0,
                        atol=1e-12,
                    )
                ),
                "observed": float(
                    opportunity_panel.groupby(
                        ["member_id", "closure_event_id"], observed=True
                    )[
                        "timing_deviation_novel_opportunity_share_leave_one_out"
                    ].mean().abs().max()
                ),
                "expected": 0,
            },
            {
                "check": "high-intention returners return earlier within closure",
                "passed": timing_effect < 0,
                "observed": float(timing_effect),
                "expected": "negative high-minus-low coefficient",
            },
        ]
    )
    validation_checks = pd.concat(
        [structural_checks, validation_checks], ignore_index=True
    )
    if not validation_checks["passed"].all():
        failed = validation_checks.loc[~validation_checks["passed"], "check"].tolist()
        raise RuntimeError(f"Validation checks failed: {failed}")

    panel.to_csv(output_dir / "store_week_assortment_panel.csv", index=False)
    path_results.to_csv(output_dir / "treated_post_path_results.csv", index=False)
    path_joint.to_csv(output_dir / "treated_post_path_joint_tests.csv", index=False)
    path_support.to_csv(output_dir / "treated_post_path_support.csv", index=False)
    path_means.to_csv(output_dir / "treated_post_path_weekly_means.csv", index=False)
    matched_results.to_csv(output_dir / "matched_store_results.csv", index=False)
    matched_event_study.to_csv(
        output_dir / "matched_store_event_study.csv", index=False
    )
    matched_pretrends.to_csv(
        output_dir / "matched_store_pretrend_tests.csv", index=False
    )
    matched_support.to_csv(output_dir / "matched_store_support.csv", index=False)
    first_returns.to_csv(output_dir / "treated_first_return_exposure.csv", index=False)
    return_distribution.to_csv(
        output_dir / "treated_return_timing_distribution.csv", index=False
    )
    return_exposure.to_csv(
        output_dir / "treated_first_return_exposure_results.csv", index=False
    )
    return_means.to_csv(
        output_dir / "treated_first_return_exposure_means.csv", index=False
    )
    opportunity_panel.to_csv(
        output_dir / "treated_return_week_novel_opportunity.csv", index=False
    )
    novel_opportunity_results.to_csv(
        output_dir / "treated_return_week_novel_opportunity_results.csv", index=False
    )
    novel_opportunity_means.to_csv(
        output_dir / "treated_return_week_novel_opportunity_means.csv", index=False
    )
    validation_checks.to_csv(output_dir / "validation_checks.csv", index=False)

    audit = {
        "project_root": str(project_root),
        "output_dir": str(output_dir),
        "seed": SEED,
        "relative_weeks": list(RELATIVE_WEEKS),
        "primary_post_weeks": list(POST_WEEKS),
        "primary_sample_rule": "complete four-week treated-store panel within outcome",
        "inference": "CRV1 clustered by closure event; t/F reference distributions use G-1 degrees of freedom; treated-store joint tests also use a restricted Rademacher wild-cluster bootstrap",
        "bootstrap_reps": args.bootstrap_reps,
        "rarefaction": {"basket_target": 50, "draws": 100},
        "store_orders": order_audit,
        "store_panel": panel_audit,
        "treated_member_product_history": history_audit,
        "treated_members": int(len(member_events)),
        "treated_first_returns_within_28_days": int(len(first_returns)),
    }
    (output_dir / "run_metadata.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_summary(
        output_dir,
        path_results,
        path_joint,
        path_support,
        matched_results,
        matched_pretrends,
        return_distribution,
        return_exposure,
        return_means,
        novel_opportunity_results,
        novel_opportunity_means,
        validation_checks,
    )
    print(output_dir)


if __name__ == "__main__":
    main()
