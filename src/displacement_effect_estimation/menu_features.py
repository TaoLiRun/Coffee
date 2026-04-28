from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path

import pandas as pd

from data import get_project_root, load_config


@dataclass(frozen=True)
class MenuFeaturePaths:
    closure_registry: Path
    product_orders: Path
    product_mapping: Path | None


def _normalize_date(s: pd.Series) -> pd.Series:
    return pd.to_datetime(s, errors="coerce").dt.normalize()


def _build_closure_event_id(*, dept_id: object, closure_start: object) -> str:
    return f"dept_{dept_id}_closure_{pd.Timestamp(closure_start).strftime('%Y-%m-%d')}"


def detect_menu_feature_paths(project_root: Path | None = None) -> MenuFeaturePaths:
    project_root = project_root or get_project_root()

    closure_registry_rel = os.environ.get(
        "DISPLACEMENT_EFFECT_CLOSURE_REGISTRY",
        "outputs/customer-store/closure_pair_registry.csv",
    )
    closure_registry = project_root / closure_registry_rel

    product_candidates = [
        project_root / "processed_data" / "order_commodity_result_processed.csv",
        project_root / "data" / "processed" / "order_commodity_result_processed.csv",
    ]
    product_orders = next((p for p in product_candidates if p.exists()), product_candidates[0])

    mapping_candidates = [
        project_root / "processed_data" / "product_mapping.csv",
        project_root / "data" / "processed" / "product_mapping.csv",
    ]
    product_mapping = next((p for p in mapping_candidates if p.exists()), None)

    return MenuFeaturePaths(
        closure_registry=closure_registry,
        product_orders=product_orders,
        product_mapping=product_mapping,
    )


def load_kept_closures(paths: MenuFeaturePaths | None = None) -> pd.DataFrame:
    paths = paths or detect_menu_feature_paths()
    if not paths.closure_registry.exists():
        raise FileNotFoundError(f"Closure registry not found: {paths.closure_registry}")

    closures = pd.read_csv(paths.closure_registry, encoding="utf-8-sig")
    required = {"dept_id", "closure_start", "closure_end", "closure_duration_days"}
    missing = required - set(closures.columns)
    if missing:
        raise ValueError(
            f"Missing required columns in {paths.closure_registry.name}: {sorted(missing)}"
        )

    closures = closures.assign(
        closure_start=_normalize_date(closures["closure_start"]),
        closure_end=_normalize_date(closures["closure_end"]),
        closure_duration_days=pd.to_numeric(
            closures["closure_duration_days"], errors="coerce"
        ).astype("Int64"),
    )
    closures = closures.dropna(
        subset=["dept_id", "closure_start", "closure_end", "closure_duration_days"]
    ).copy()

    if "status" in closures.columns:
        closures = closures[
            closures["status"].fillna("").str.lower().eq("kept")
        ].copy()

    closures["closure_duration_days"] = closures["closure_duration_days"].astype(int)
    closures["closure_event_id"] = closures.apply(
        lambda row: _build_closure_event_id(
            dept_id=row["dept_id"], closure_start=row["closure_start"]
        ),
        axis=1,
    )

    return closures[
        ["dept_id", "closure_start", "closure_end", "closure_duration_days", "closure_event_id"]
    ].drop_duplicates().sort_values(["closure_start", "dept_id"]).reset_index(drop=True)


def load_store_product_orders(
    *,
    closure_depts: set[int] | set[str] | set[object],
    paths: MenuFeaturePaths | None = None,
    chunksize: int = 1_000_000,
) -> pd.DataFrame:
    paths = paths or detect_menu_feature_paths()
    if not paths.product_orders.exists():
        raise FileNotFoundError(f"Processed product-order file not found: {paths.product_orders}")

    keep_depts = {str(dept_id) for dept_id in closure_depts}
    if not keep_depts:
        return pd.DataFrame(columns=["dept_id", "dt", "product_id"])

    frames: list[pd.DataFrame] = []
    usecols = ["dept_id", "dt", "product_id"]

    for chunk in pd.read_csv(
        paths.product_orders,
        encoding="utf-8-sig",
        usecols=usecols,
        chunksize=chunksize,
    ):
        chunk = chunk[chunk["dept_id"].astype(str).isin(keep_depts)]
        if chunk.empty:
            continue
        chunk["dt"] = _normalize_date(chunk["dt"])
        chunk = chunk.dropna(subset=["dt", "product_id"])
        if chunk.empty:
            continue
        frames.append(chunk[usecols].drop_duplicates())

    if not frames:
        return pd.DataFrame(columns=usecols)

    orders = pd.concat(frames, ignore_index=True).drop_duplicates()
    return orders.sort_values(["dept_id", "dt", "product_id"]).reset_index(drop=True)


def load_product_mapping(paths: MenuFeaturePaths | None = None) -> pd.DataFrame:
    paths = paths or detect_menu_feature_paths()
    if paths.product_mapping is None or not paths.product_mapping.exists():
        return pd.DataFrame(columns=["product_id", "name"])

    mapping = pd.read_csv(paths.product_mapping, encoding="utf-8-sig")
    required = {"product_id", "name"}
    missing = required - set(mapping.columns)
    if missing:
        raise ValueError(
            f"Missing required columns in {paths.product_mapping.name}: {sorted(missing)}"
        )
    return mapping[["product_id", "name"]].drop_duplicates().reset_index(drop=True)


def _window_bounds(
    *,
    closure_start: pd.Timestamp,
    closure_end: pd.Timestamp,
    closure_duration_days: int,
    horizon: int,
) -> tuple[pd.Timestamp, pd.Timestamp, pd.Timestamp, pd.Timestamp]:
    if horizon < 1:
        raise ValueError("horizon must be >= 1")
    if closure_duration_days < 1:
        raise ValueError("closure_duration_days must be >= 1")

    pre_start = closure_start - pd.Timedelta(days=horizon * closure_duration_days)
    pre_end = closure_start
    post_start = closure_end
    post_end = closure_end + pd.Timedelta(days=horizon * closure_duration_days)
    return pre_start, pre_end, post_start, post_end


def _products_in_window(
    dept_orders: pd.DataFrame,
    *,
    start_dt: pd.Timestamp,
    end_dt: pd.Timestamp,
) -> list[int]:
    if dept_orders.empty:
        return []

    window = dept_orders[
        dept_orders["dt"].between(start_dt, end_dt, inclusive="both")
    ]
    if window.empty:
        return []
    return sorted(window["product_id"].astype(int).unique().tolist())


def _join_product_ids(values: list[int]) -> str:
    if not values:
        return ""
    return "|".join(str(v) for v in values)


def _join_product_names(values: list[int], name_lookup: dict[int, str]) -> str:
    if not values:
        return ""
    return "|".join(name_lookup.get(v, f"product_{v}") for v in values)


def build_menu_feature_outputs(
    *,
    closures: pd.DataFrame,
    orders: pd.DataFrame,
    product_mapping: pd.DataFrame,
    t_horizon: int,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    if t_horizon < 1:
        raise ValueError("t_horizon must be >= 1")

    name_lookup = {
        int(row["product_id"]): str(row["name"])
        for _, row in product_mapping.dropna(subset=["product_id"]).iterrows()
    }
    orders_by_dept = {
        dept_id: dept_orders[["dt", "product_id"]].copy()
        for dept_id, dept_orders in orders.groupby("dept_id", sort=False)
    }

    long_rows: list[dict] = []
    detail_rows: list[dict] = []

    for _, closure in closures.iterrows():
        dept_id = closure["dept_id"]
        closure_start = pd.Timestamp(closure["closure_start"])
        closure_end = pd.Timestamp(closure["closure_end"])
        duration_days = int(closure["closure_duration_days"])
        closure_event_id = closure["closure_event_id"]
        dept_orders = orders_by_dept.get(
            dept_id, pd.DataFrame(columns=["dt", "product_id"])
        )

        for horizon in range(1, t_horizon + 1):
            pre_start, pre_end, post_start, post_end = _window_bounds(
                closure_start=closure_start,
                closure_end=closure_end,
                closure_duration_days=duration_days,
                horizon=horizon,
            )
            pre_products = _products_in_window(
                dept_orders, start_dt=pre_start, end_dt=pre_end
            )
            post_products = _products_in_window(
                dept_orders, start_dt=post_start, end_dt=post_end
            )

            pre_set = set(pre_products)
            post_set = set(post_products)
            removed_products = sorted(pre_set - post_set)
            introduced_products = sorted(post_set - pre_set)

            long_rows.append(
                {
                    "dept_id": dept_id,
                    "closure_start": closure_start.strftime("%Y-%m-%d"),
                    "closure_end": closure_end.strftime("%Y-%m-%d"),
                    "closure_duration_days": duration_days,
                    "closure_event_id": closure_event_id,
                    "h": horizon,
                    "pre_start": pre_start.strftime("%Y-%m-%d"),
                    "pre_end": pre_end.strftime("%Y-%m-%d"),
                    "post_start": post_start.strftime("%Y-%m-%d"),
                    "post_end": post_end.strftime("%Y-%m-%d"),
                    "window_days_inclusive": horizon * duration_days + 1,
                    "menu_size_pre": len(pre_set),
                    "menu_size_post": len(post_set),
                    "n_removed": len(removed_products),
                    "n_introduced": len(introduced_products),
                    "net_menu_change": len(post_set) - len(pre_set),
                    "menu_churn": len(removed_products) + len(introduced_products),
                    "menu_overlap": len(pre_set & post_set),
                }
            )
            detail_rows.append(
                {
                    "dept_id": dept_id,
                    "closure_start": closure_start.strftime("%Y-%m-%d"),
                    "closure_end": closure_end.strftime("%Y-%m-%d"),
                    "closure_duration_days": duration_days,
                    "closure_event_id": closure_event_id,
                    "h": horizon,
                    "pre_product_ids": _join_product_ids(pre_products),
                    "post_product_ids": _join_product_ids(post_products),
                    "removed_product_ids": _join_product_ids(removed_products),
                    "introduced_product_ids": _join_product_ids(introduced_products),
                    "pre_product_names": _join_product_names(pre_products, name_lookup),
                    "post_product_names": _join_product_names(post_products, name_lookup),
                    "removed_product_names": _join_product_names(
                        removed_products, name_lookup
                    ),
                    "introduced_product_names": _join_product_names(
                        introduced_products, name_lookup
                    ),
                }
            )

    long_df = pd.DataFrame(long_rows).sort_values(
        ["closure_start", "dept_id", "h"]
    ).reset_index(drop=True)
    detail_df = pd.DataFrame(detail_rows).sort_values(
        ["closure_start", "dept_id", "h"]
    ).reset_index(drop=True)

    feature_cols = [
        "menu_size_pre",
        "menu_size_post",
        "n_removed",
        "n_introduced",
        "net_menu_change",
        "menu_churn",
        "menu_overlap",
        "window_days_inclusive",
    ]
    wide_df = long_df[
        [
            "dept_id",
            "closure_start",
            "closure_end",
            "closure_duration_days",
            "closure_event_id",
            "h",
            *feature_cols,
        ]
    ].pivot(
        index=[
            "dept_id",
            "closure_start",
            "closure_end",
            "closure_duration_days",
            "closure_event_id",
        ],
        columns="h",
        values=feature_cols,
    )
    wide_df.columns = [f"{col}_h{h}" for col, h in wide_df.columns]
    wide_df = wide_df.reset_index().sort_values(
        ["closure_start", "dept_id"]
    ).reset_index(drop=True)

    return long_df, wide_df, detail_df


def save_menu_feature_outputs(
    *,
    output_dir: Path,
    long_df: pd.DataFrame,
    wide_df: pd.DataFrame,
    detail_df: pd.DataFrame,
    t_horizon: int,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    long_df.to_csv(output_dir / "closure_menu_features_long.csv", index=False)
    wide_df.to_csv(output_dir / "closure_menu_features_wide.csv", index=False)
    detail_df.to_csv(output_dir / "closure_menu_product_lists.csv", index=False)

    mean_by_horizon = (
        long_df.groupby("h")[
            ["menu_size_pre", "menu_size_post", "n_removed", "n_introduced", "menu_churn"]
        ]
        .mean()
        .round(3)
    )

    summary_lines = [
        "# Closure Menu Features",
        "",
        f"- Closures: {wide_df.shape[0]:,}",
        f"- Horizon count: {t_horizon}",
        f"- Long rows: {long_df.shape[0]:,}",
        f"- Detail rows: {detail_df.shape[0]:,}",
        "",
        "## Mean Counts By Horizon",
        mean_by_horizon.to_string(),
    ]
    (output_dir / "summary.md").write_text("\n".join(summary_lines), encoding="utf-8")


def build_and_save_menu_features(
    *,
    t_horizon: int,
    output_dir: Path,
    chunksize: int = 1_000_000,
    paths: MenuFeaturePaths | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    paths = paths or detect_menu_feature_paths()
    closures = load_kept_closures(paths=paths)
    orders = load_store_product_orders(
        closure_depts=set(closures["dept_id"].tolist()),
        paths=paths,
        chunksize=chunksize,
    )
    product_mapping = load_product_mapping(paths=paths)
    long_df, wide_df, detail_df = build_menu_feature_outputs(
        closures=closures,
        orders=orders,
        product_mapping=product_mapping,
        t_horizon=t_horizon,
    )
    save_menu_feature_outputs(
        output_dir=output_dir,
        long_df=long_df,
        wide_df=wide_df,
        detail_df=detail_df,
        t_horizon=t_horizon,
    )
    return long_df, wide_df, detail_df
