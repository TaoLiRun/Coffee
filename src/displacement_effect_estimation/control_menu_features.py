from __future__ import annotations

from pathlib import Path

import pandas as pd

from menu_features import detect_menu_feature_paths, load_product_mapping, load_store_product_orders


def _normalize_date(s: pd.Series) -> pd.Series:
    return pd.to_datetime(s, errors="coerce").dt.normalize()


def _build_closure_event_id(*, dept_id: object, closure_start: object) -> str:
    return f"dept_{dept_id}_closure_{pd.Timestamp(closure_start).strftime('%Y-%m-%d')}"


def _parse_control_store_ids(serialized: object) -> list[int]:
    if pd.isna(serialized):
        return []
    values = str(serialized).strip()
    if not values:
        return []
    out: list[int] = []
    for part in values.split("|"):
        part = part.strip()
        if not part:
            continue
        out.append(int(part))
    return out


def load_kept_closures_with_controls(paths=None) -> pd.DataFrame:
    paths = paths or detect_menu_feature_paths()
    registry = paths.closure_registry
    if not registry.exists():
        raise FileNotFoundError(f"Closure registry not found: {registry}")

    closures = pd.read_csv(registry, encoding="utf-8-sig")
    required = {
        "dept_id",
        "closure_start",
        "closure_end",
        "closure_duration_days",
        "control_store_ids",
    }
    missing = required - set(closures.columns)
    if missing:
        raise ValueError(
            f"Missing required columns in {registry.name}: {sorted(missing)}"
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
    closures["control_dept_ids"] = closures["control_store_ids"].apply(
        _parse_control_store_ids
    )
    closures = closures[closures["control_dept_ids"].map(bool)].copy()
    closures["closure_event_id"] = closures.apply(
        lambda row: _build_closure_event_id(
            dept_id=row["dept_id"], closure_start=row["closure_start"]
        ),
        axis=1,
    )

    keep_cols = [
        "dept_id",
        "closure_start",
        "closure_end",
        "closure_duration_days",
        "closure_event_id",
        "control_store_ids",
        "control_dept_ids",
        "n_control_stores",
    ]
    keep_cols = [col for col in keep_cols if col in closures.columns]
    return (
        closures[keep_cols]
        .drop_duplicates(subset=["dept_id", "closure_start", "closure_end"])
        .sort_values(["closure_start", "dept_id"])
        .reset_index(drop=True)
    )


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


def _pre_during_window_bounds(
    *,
    closure_start: pd.Timestamp,
    closure_end: pd.Timestamp,
    closure_duration_days: int,
) -> tuple[pd.Timestamp, pd.Timestamp, pd.Timestamp, pd.Timestamp]:
    if closure_duration_days < 1:
        raise ValueError("closure_duration_days must be >= 1")

    during_start = closure_start
    during_end = closure_end
    pre_end = closure_start - pd.Timedelta(days=1)
    pre_start = pre_end - pd.Timedelta(days=closure_duration_days - 1)
    return pre_start, pre_end, during_start, during_end


def build_control_menu_introduction_outputs(
    *,
    closures: pd.DataFrame,
    orders: pd.DataFrame,
    product_mapping: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    name_lookup = {
        int(row["product_id"]): str(row["name"])
        for _, row in product_mapping.dropna(subset=["product_id"]).iterrows()
    }
    orders_by_dept = {
        dept_id: dept_orders[["dt", "product_id"]].copy()
        for dept_id, dept_orders in orders.groupby("dept_id", sort=False)
    }

    detail_rows: list[dict] = []
    summary_rows: list[dict] = []

    for _, closure in closures.iterrows():
        treatment_dept_id = int(closure["dept_id"])
        closure_start = pd.Timestamp(closure["closure_start"])
        closure_end = pd.Timestamp(closure["closure_end"])
        closure_duration_days = int(closure["closure_duration_days"])
        closure_event_id = str(closure["closure_event_id"])
        control_dept_ids = [int(v) for v in closure["control_dept_ids"]]

        pre_start, pre_end, during_start, during_end = _pre_during_window_bounds(
            closure_start=closure_start,
            closure_end=closure_end,
            closure_duration_days=closure_duration_days,
        )

        introduced_counts: list[int] = []

        for control_dept_id in control_dept_ids:
            dept_orders = orders_by_dept.get(
                control_dept_id, pd.DataFrame(columns=["dt", "product_id"])
            )
            pre_products = _products_in_window(
                dept_orders, start_dt=pre_start, end_dt=pre_end
            )
            during_products = _products_in_window(
                dept_orders, start_dt=during_start, end_dt=during_end
            )
            introduced_products = sorted(set(during_products) - set(pre_products))
            introduced_counts.append(len(introduced_products))

            detail_rows.append(
                {
                    "treatment_dept_id": treatment_dept_id,
                    "closure_start": closure_start.strftime("%Y-%m-%d"),
                    "closure_end": closure_end.strftime("%Y-%m-%d"),
                    "closure_duration_days": closure_duration_days,
                    "closure_event_id": closure_event_id,
                    "control_dept_id": control_dept_id,
                    "pre_start": pre_start.strftime("%Y-%m-%d"),
                    "pre_end": pre_end.strftime("%Y-%m-%d"),
                    "during_start": during_start.strftime("%Y-%m-%d"),
                    "during_end": during_end.strftime("%Y-%m-%d"),
                    "n_products_pre": len(set(pre_products)),
                    "n_products_during": len(set(during_products)),
                    "n_introduced_during": len(introduced_products),
                    "introduced_product_ids": _join_product_ids(introduced_products),
                    "introduced_product_names": _join_product_names(
                        introduced_products, name_lookup
                    ),
                }
            )

        summary_rows.append(
            {
                "treatment_dept_id": treatment_dept_id,
                "closure_start": closure_start.strftime("%Y-%m-%d"),
                "closure_end": closure_end.strftime("%Y-%m-%d"),
                "closure_duration_days": closure_duration_days,
                "closure_event_id": closure_event_id,
                "control_store_ids": "|".join(str(v) for v in control_dept_ids),
                "n_control_stores": len(control_dept_ids),
                "avg_n_introduced_during_control": (
                    float(pd.Series(introduced_counts, dtype="float64").mean())
                    if introduced_counts
                    else 0.0
                ),
                "min_n_introduced_during_control": min(introduced_counts)
                if introduced_counts
                else 0,
                "max_n_introduced_during_control": max(introduced_counts)
                if introduced_counts
                else 0,
                "total_n_introduced_during_control": sum(introduced_counts),
            }
        )

    detail_df = pd.DataFrame(detail_rows).sort_values(
        ["closure_start", "treatment_dept_id", "control_dept_id"]
    ).reset_index(drop=True)
    summary_df = pd.DataFrame(summary_rows).sort_values(
        ["closure_start", "treatment_dept_id"]
    ).reset_index(drop=True)
    return summary_df, detail_df


def save_control_menu_introduction_outputs(
    *,
    output_dir: Path,
    summary_df: pd.DataFrame,
    detail_df: pd.DataFrame,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    summary_df.to_csv(
        output_dir / "control_menu_introductions_during_closure.csv", index=False
    )
    detail_df.to_csv(
        output_dir / "control_menu_introductions_during_closure_detail.csv",
        index=False,
    )

    summary_lines = [
        "# Control Menu Introductions During Closure",
        "",
        "- Definition: introduced products in a control store are products sold during the treatment store's closure window that were not sold in the immediately preceding equal-length window.",
        f"- Treatment closures: {summary_df.shape[0]:,}",
        f"- Control-store detail rows: {detail_df.shape[0]:,}",
    ]
    if not summary_df.empty:
        summary_lines.extend(
            [
                f"- Mean average introduced products across controls: {summary_df['avg_n_introduced_during_control'].mean():.3f}",
                f"- Mean total introduced products across the 5 controls: {summary_df['total_n_introduced_during_control'].mean():.3f}",
            ]
        )

    (output_dir / "control_menu_introductions_summary.md").write_text(
        "\n".join(summary_lines), encoding="utf-8"
    )


def build_and_save_control_menu_introductions(
    *,
    output_dir: Path,
    chunksize: int = 1_000_000,
    paths=None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    paths = paths or detect_menu_feature_paths()
    closures = load_kept_closures_with_controls(paths=paths)
    all_control_depts = {
        int(control_dept_id)
        for control_dept_ids in closures["control_dept_ids"]
        for control_dept_id in control_dept_ids
    }
    orders = load_store_product_orders(
        closure_depts=all_control_depts,
        paths=paths,
        chunksize=chunksize,
    )
    product_mapping = load_product_mapping(paths=paths)
    summary_df, detail_df = build_control_menu_introduction_outputs(
        closures=closures,
        orders=orders,
        product_mapping=product_mapping,
    )
    save_control_menu_introduction_outputs(
        output_dir=output_dir,
        summary_df=summary_df,
        detail_df=detail_df,
    )
    return summary_df, detail_df
