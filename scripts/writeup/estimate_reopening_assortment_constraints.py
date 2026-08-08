"""Estimate and document the reopening-assortment alternative explanation.

The script builds a fixed-week matched-store panel around the 18 retained
closures, estimates treated-store post-reopening differences in realized
assortment, tests pre-trends and balanced-panel sensitivity, and relates early
assortment gaps to closure-specific novelty DDD estimates.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


SEED = 20260807
RELATIVE_WEEKS = (-4, -3, -2, -1, 1, 2, 3, 4)
OUTCOMES = ("core_coverage", "rarefied_products_50", "menu_jaccard_pre")
OUTCOME_LABELS = {
    "core_coverage": "Core-product coverage",
    "rarefied_products_50": "Products per 50 baskets",
    "menu_jaccard_pre": "Overlap with pre-closure menu",
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
    parser.add_argument(
        "--figure-path",
        type=Path,
        default=Path("writeup/figures/reopening_assortment_event_study.png"),
    )
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
        "rows_scanned": int(rows_scanned),
        "rows_retained": int(len(orders)),
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
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
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
            if relative_week < 0:
                start = event_store["closure_start"] + pd.Timedelta(days=start_offset)
                end = event_store["closure_start"] + pd.Timedelta(days=end_offset)
            else:
                start = event_store["closure_end"] + pd.Timedelta(days=start_offset)
                end = event_store["closure_end"] + pd.Timedelta(days=end_offset)
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
    for event_id, store_id in panel[["closure_event_id", "store_id"]].drop_duplicates().itertuples(index=False):
        appearances: dict[int, int] = {}
        for relative_week in (-4, -3, -2, -1):
            for product_id in product_cache[(str(event_id), int(store_id), relative_week)]:
                appearances[product_id] = appearances.get(product_id, 0) + 1
        core_sets[(str(event_id), int(store_id))] = {
            product_id for product_id, count in appearances.items() if count >= 3
        }

    coverage: list[float] = []
    overlap: list[float] = []
    for row in panel.itertuples(index=False):
        key = (str(row.closure_event_id), int(row.store_id))
        current = product_cache[(key[0], key[1], int(row.rel_t))]
        core = core_sets[key]
        pre_union = set().union(
            *(product_cache[(key[0], key[1], relative_week)] for relative_week in (-4, -3, -2, -1))
        )
        coverage.append(len(current & core) / len(core) if core else np.nan)
        denominator = current | pre_union
        overlap.append(len(current & pre_union) / len(denominator) if denominator else np.nan)
    panel["core_coverage"] = coverage
    panel["menu_jaccard_pre"] = overlap
    panel["event_store_fe"] = panel["closure_event_id"] + "|" + panel["store_id"].astype(str)
    panel["event_rel_fe"] = panel["closure_event_id"] + "|" + panel["rel_t"].astype(str)
    panel["treated_store_X_post"] = panel["treated_store"] * panel["post"]

    event_gaps: list[dict] = []
    for event_id, group in panel.groupby("closure_event_id"):
        result: dict = {"closure_event_id": event_id}
        for outcome in OUTCOMES:
            pivot = group.pivot_table(
                index="rel_t", columns="treated_store", values=outcome, aggfunc="mean"
            )
            if {-1, 1}.issubset(pivot.index) and {0, 1}.issubset(pivot.columns):
                result[f"{outcome}_early_did"] = (
                    (pivot.loc[1, 1] - pivot.loc[-1, 1])
                    - (pivot.loc[1, 0] - pivot.loc[-1, 0])
                )
            else:
                result[f"{outcome}_early_did"] = np.nan
        event_gaps.append(result)

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
    return panel, pd.DataFrame(event_gaps), audit


def drop_singleton_fixed_effects(df: pd.DataFrame, fe_cols: list[str]) -> pd.DataFrame:
    work = df.copy()
    while True:
        keep = np.ones(len(work), dtype=bool)
        for column in fe_cols:
            keep &= work.groupby(column, observed=True)[column].transform("size").to_numpy() > 1
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


def estimate_store_models(
    panel: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    results: list[dict] = []
    event_paths: list[dict] = []
    pretrends: list[dict] = []
    support: list[dict] = []
    for outcome in OUTCOMES:
        for sample in ("available_unbalanced", "complete_8_period_pairs"):
            work = panel.dropna(subset=[outcome]).copy()
            if sample == "complete_8_period_pairs":
                pair_counts = work.groupby("event_store_fe")["rel_t"].nunique()
                complete_pairs = set(pair_counts[pair_counts.eq(8)].index)
                work = work[work["event_store_fe"].isin(complete_pairs)].copy()
            support.append(
                {
                    "outcome": outcome,
                    "sample": sample,
                    "rows": int(len(work)),
                    "event_store_pairs": int(work["event_store_fe"].nunique()),
                    "treated_pairs": int(
                        work.loc[work["treated_store"].eq(1), "event_store_fe"].nunique()
                    ),
                    "control_pairs": int(
                        work.loc[work["treated_store"].eq(0), "event_store_fe"].nunique()
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
            pooled_row.update({"outcome": outcome, "sample": sample, "model": "pooled_post"})
            results.append(pooled_row)

            terms: list[str] = []
            term_map: dict[str, int] = {}
            for relative_week in RELATIVE_WEEKS:
                if relative_week == -1:
                    continue
                suffix = f"m{abs(relative_week)}" if relative_week < 0 else f"p{relative_week}"
                term = f"rt_{suffix}_X_treated_store"
                work[term] = work["rel_t"].eq(relative_week).astype(int) * work["treated_store"]
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
            immediate_row.update({"outcome": outcome, "sample": sample, "model": "immediate_post"})
            results.append(immediate_row)

            pre_terms = [term for term, relative_week in term_map.items() if relative_week < -1]
            indices = [dynamic["names"].index(term) for term in pre_terms]
            restriction = dynamic["beta"][indices]
            restriction_covariance = dynamic["covariance"][np.ix_(indices, indices)]
            q = len(indices)
            f_statistic = float(
                restriction.T @ np.linalg.pinv(restriction_covariance) @ restriction / q
            )
            pretrends.append(
                {
                    "outcome": outcome,
                    "sample": sample,
                    "f_statistic": f_statistic,
                    "df_num": q,
                    "df_denom": dynamic["cluster_df"],
                    "pvalue": float(stats.f.sf(f_statistic, q, dynamic["cluster_df"])),
                }
            )
            if sample == "available_unbalanced":
                for term, relative_week in term_map.items():
                    row = extract_term(dynamic, term)
                    row.update({"outcome": outcome, "rel_t": relative_week})
                    event_paths.append(row)
    return (
        pd.DataFrame(results),
        pd.DataFrame(event_paths),
        pd.DataFrame(pretrends),
        pd.DataFrame(support),
    )


def estimate_novelty_moderation(project_root: Path, gaps: pd.DataFrame) -> pd.DataFrame:
    effects_path = (
        project_root
        / "outputs/05_robustness/missing_new_products/effect_vs_introductions/"
        "closure_level_effects_vs_control_introductions.csv"
    )
    effects = pd.read_csv(effects_path, encoding="utf-8-sig")
    effects["closure_start"] = normalize_date(effects["closure_start"])
    effects["closure_event_id"] = (
        "dept_"
        + effects["dept_id"].astype(int).astype(str)
        + "_closure_"
        + effects["closure_start"].dt.strftime("%Y-%m-%d")
    )
    merged = effects.merge(gaps, on="closure_event_id", how="inner", validate="one_to_one")
    rows: list[dict] = []
    rng = np.random.default_rng(SEED)
    for outcome in OUTCOMES:
        metric = f"{outcome}_early_did"
        work = merged.dropna(subset=[metric, "variety_binary_coef", "variety_binary_se"])
        x = work[metric].astype(float).to_numpy()
        y = work["variety_binary_coef"].astype(float).to_numpy()
        weights = 1.0 / np.square(work["variety_binary_se"].astype(float).to_numpy())
        weighted_mean = np.average(x, weights=weights)
        weighted_sd = np.sqrt(np.average(np.square(x - weighted_mean), weights=weights))
        standardized_x = (x - weighted_mean) / weighted_sd
        X = np.column_stack([np.ones(len(x)), standardized_x])
        root_weights = np.sqrt(weights)
        observed = float(
            np.linalg.lstsq(X * root_weights[:, None], y * root_weights, rcond=None)[0][1]
        )
        permuted: list[float] = []
        for _ in range(5000):
            X_permuted = np.column_stack([np.ones(len(x)), rng.permutation(standardized_x)])
            permuted.append(
                float(
                    np.linalg.lstsq(
                        X_permuted * root_weights[:, None], y * root_weights, rcond=None
                    )[0][1]
                )
            )
        pvalue = (1 + sum(abs(value) >= abs(observed) for value in permuted)) / (
            len(permuted) + 1
        )
        rows.append(
            {
                "menu_metric": metric,
                "n_closures": int(len(work)),
                "wls_slope_per_sd": observed,
                "permutation_pvalue_two_sided": pvalue,
                "pearson_correlation": float(np.corrcoef(x, y)[0, 1]),
            }
        )
    return pd.DataFrame(rows)


def plot_event_study(event_paths: pd.DataFrame, figure_path: Path) -> None:
    figure_path.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 3, figsize=(12.6, 3.8))
    for axis, outcome in zip(axes, OUTCOMES):
        work = event_paths[event_paths["outcome"].eq(outcome)].sort_values("rel_t")
        reference = pd.DataFrame(
            {"rel_t": [-1], "coef": [0.0], "ci_low": [0.0], "ci_high": [0.0]}
        )
        work = pd.concat([work[["rel_t", "coef", "ci_low", "ci_high"]], reference]).sort_values(
            "rel_t"
        )
        scale = 1.0 if outcome == "rarefied_products_50" else 100.0
        axis.errorbar(
            work["rel_t"],
            work["coef"] * scale,
            yerr=np.vstack(
                [
                    (work["coef"] - work["ci_low"]) * scale,
                    (work["ci_high"] - work["coef"]) * scale,
                ]
            ),
            fmt="o-",
            color="#1f4e79",
            ecolor="#6f8fae",
            capsize=2.5,
            linewidth=1.3,
            markersize=4,
        )
        axis.axhline(0, color="black", linewidth=0.8)
        axis.axvline(0, color="gray", linestyle="--", linewidth=0.8)
        axis.set_xticks(RELATIVE_WEEKS)
        axis.set_title(OUTCOME_LABELS[outcome], fontsize=10)
        axis.set_xlabel("Relative week")
        axis.set_ylabel("Difference (percentage points)" if scale == 100 else "Difference (products)")
        axis.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(figure_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    args = parse_args()
    project_root = args.project_root.resolve()
    output_dir = resolve_under_root(project_root, args.output_dir).resolve()
    figure_path = resolve_under_root(project_root, args.figure_path).resolve()
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
    panel, event_gaps, panel_audit = build_store_event_panel(registry, orders)
    results, event_paths, pretrends, support = estimate_store_models(panel)
    moderation = estimate_novelty_moderation(project_root, event_gaps)
    group_means = (
        panel.groupby(["treated_store", "post"])[[*OUTCOMES, "n_baskets"]]
        .mean()
        .reset_index()
    )

    panel.to_csv(output_dir / "store_assortment_panel.csv", index=False)
    results.to_csv(output_dir / "store_assortment_results.csv", index=False)
    event_paths.to_csv(output_dir / "store_assortment_event_study.csv", index=False)
    pretrends.to_csv(output_dir / "store_assortment_pretrend_tests.csv", index=False)
    support.to_csv(output_dir / "store_assortment_support.csv", index=False)
    group_means.to_csv(output_dir / "store_assortment_group_means.csv", index=False)
    event_gaps.to_csv(output_dir / "store_assortment_event_gaps.csv", index=False)
    moderation.to_csv(output_dir / "assortment_novelty_moderation.csv", index=False)
    plot_event_study(event_paths, figure_path)

    audit = {
        "project_root": str(project_root),
        "output_dir": str(output_dir),
        "figure_path": str(figure_path),
        "seed": SEED,
        "relative_weeks": list(RELATIVE_WEEKS),
        "rarefaction": {"basket_target": 50, "draws": 100},
        "store_orders": order_audit,
        "store_panel": panel_audit,
    }
    (output_dir / "run_metadata.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    summary = [
        "# Reopening Assortment Constraints",
        "",
        "The analysis uses four fixed seven-day periods before closure and four after reopening.",
        "Realized assortment is compared between each treated store and its five matched controls.",
        "",
        "## Main and balanced-panel estimates",
        results.to_markdown(index=False),
        "",
        "## Joint pre-trend tests",
        pretrends.to_markdown(index=False),
        "",
        "## Closure-level moderation of the novelty DDD",
        moderation.to_markdown(index=False),
        "",
        "Product sales proxy realized assortment; a product without a recorded sale may still have been available.",
    ]
    (output_dir / "summary.md").write_text("\n".join(summary), encoding="utf-8")
    print(output_dir)
    print(figure_path)


if __name__ == "__main__":
    main()
