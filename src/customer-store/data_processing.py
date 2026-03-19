from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # model-free directory
DATA_DIR = PROJECT_ROOT.parent / "data" / "data1031"
ORDER_COMMODITY_PATH = DATA_DIR / "order_commodity_result.csv"
ORDER_RESULT_PATH = DATA_DIR / "order_result.csv"
CLOSURES_CSV = PROJECT_ROOT / "outputs" / "store" / "non_uni_store_closures.csv"
OUTPUT_DIR = PROJECT_ROOT / "plots" / "customer_store_analysis"
OUTPUT_CUSTOMER_STORE_DIR = PROJECT_ROOT / "outputs" / "customer-store"
PAIR_REGISTRY_CSV = OUTPUT_CUSTOMER_STORE_DIR / "closure_pair_registry.csv"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Default config values
DEFAULT_LOWEST_PURCHASES = 5
DEFAULT_LOWEST_RATIO = 0.8
DEFAULT_WINDOW_DAYS = 14
ROBUSTNESS_WINDOW_DAYS = 28
DEFAULT_CLOSURE_TWO_GROUP_THRESHOLD = 30
MAX_CLOSURE_DURATION_DAYS = 30
NO_PUSH_MEMBERS_PATH = PROJECT_ROOT / "data" / "processed" / "no_push_members.csv"
EXCLUDED_CONTROL_STORE_KEYWORDS = ("大学", "学院")

USE_SET_UP_TIME_MATCHED_CONTROL = True
DEPT_STATIC_PATH = DATA_DIR / "dept_result_static.csv"
SET_UP_TIME_NEAREST_N = 5
MIN_GROUP_SIZE = 50
MIN_CTRL_TREAT_RATIO = 2.0


@dataclass
class PreparedData:
    df_commodity: pd.DataFrame
    df_order: pd.DataFrame
    closures: pd.DataFrame
    customer_preference: pd.DataFrame
    unique_visits: pd.DataFrame


def load_order_commodity_data() -> pd.DataFrame:
    print(f"Loading order commodity data from: {ORDER_COMMODITY_PATH}")
    df = pd.read_csv(ORDER_COMMODITY_PATH, encoding="utf-8-sig")

    df["dt"] = pd.to_datetime(df["create_hour"], errors="coerce")
    df = df.dropna(subset=["dt"])
    df["date"] = df["dt"].dt.date

    product_cols = [
        "coffee_commodity_name",
        "food_commodity_name",
        "drink_not_coffee_commodity_name",
        "other_not_coffee_commodity_name",
    ]
    df["product_name"] = df[product_cols].apply(
        lambda row: next((v for v in row if pd.notna(v) and v != ""), np.nan), axis=1
    )

    print(f"  Total records: {len(df):,}")
    print(f"  Unique customers: {df['member_id'].nunique():,}")
    print(f"  Unique stores: {df['dept_id'].nunique():,}")
    print(f"  Date range: {df['dt'].min().date()} to {df['dt'].max().date()}")
    return df


def load_order_result_data() -> pd.DataFrame:
    print(f"Loading order result data from: {ORDER_RESULT_PATH}")
    df = pd.read_csv(ORDER_RESULT_PATH, encoding="utf-8-sig")
    df["dt"] = pd.to_datetime(df["create_hour"], errors="coerce")
    df = df.dropna(subset=["dt"])
    df["date"] = df["dt"].dt.date

    discount_cols = [
        "coffee_discount",
        "drink_not_coffee_discount",
        "food_discount",
        "other_discount",
    ]
    existing_discount = [c for c in discount_cols if c in df.columns]
    df["total_discount"] = df[existing_discount].sum(axis=1, min_count=1)
    df["used_coupon"] = (df["use_coupon_num"] > 0).astype(int) if "use_coupon_num" in df.columns else 0

    print(f"  Total orders: {len(df):,}")
    return df[["member_id", "order_id", "dt", "date", "dept_id", "total_discount", "used_coupon", "disount_tag"]]


def load_store_set_up_times(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Store static file not found: {path}")
    df = pd.read_csv(path, encoding="utf-8-sig")
    if "dept_id" not in df.columns or "set_up_time" not in df.columns:
        raise ValueError(f"Store static must have columns dept_id and set_up_time; got {list(df.columns)}")
    df["dept_id"] = df["dept_id"].astype(str).str.strip().replace(r"^0+", "", regex=True)
    df = df[df["dept_id"] != ""]
    df["dept_id"] = df["dept_id"].astype(int)
    df["set_up_time"] = pd.to_datetime(df["set_up_time"], errors="coerce")
    if df["set_up_time"].isna().any():
        bad = df[df["set_up_time"].isna()]["dept_id"].tolist()
        raise ValueError(f"Store static has missing or invalid set_up_time for dept_id: {bad[:10]}{'...' if len(bad) > 10 else ''}")
    df["set_up_time"] = df["set_up_time"].dt.date

    out_cols = ["dept_id", "set_up_time"]
    for c in ["name", "dept_name", "store_name", "address"]:
        if c in df.columns:
            out_cols.append(c)

    return df[out_cols].drop_duplicates(subset=["dept_id"])


def load_store_static_features(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Store static file not found: {path}")

    df = pd.read_csv(path, encoding="utf-8-sig")
    required = {"dept_id", "set_up_time"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Store static must have columns {sorted(required)}; missing={sorted(missing)}")

    df["dept_id"] = df["dept_id"].astype(str).str.strip().replace(r"^0+", "", regex=True)
    df = df[df["dept_id"] != ""]
    df["dept_id"] = df["dept_id"].astype(int)
    df["set_up_time"] = pd.to_datetime(df["set_up_time"], errors="coerce").dt.date

    if df["set_up_time"].isna().any():
        bad = df[df["set_up_time"].isna()]["dept_id"].tolist()
        raise ValueError(
            f"Store static has missing or invalid set_up_time for dept_id: "
            f"{bad[:10]}{'...' if len(bad) > 10 else ''}"
        )

    out_cols = ["dept_id", "set_up_time"]
    if "address" in df.columns:
        out_cols.append("address")
    else:
        df["address"] = ""
        out_cols.append("address")
    return df[out_cols].drop_duplicates(subset=["dept_id"])


def contains_excluded_control_store_keyword(text: Any) -> bool:
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return False
    s = str(text)
    return any(k in s for k in EXCLUDED_CONTROL_STORE_KEYWORDS)


def filter_closures_shorter_than_max(
    closures: pd.DataFrame,
    max_duration_days: int = MAX_CLOSURE_DURATION_DAYS,
    context: str = "analysis",
) -> pd.DataFrame:
    if "closure_duration_days" not in closures.columns:
        raise ValueError("closures is missing required column: closure_duration_days")

    out = closures[closures["closure_duration_days"] < max_duration_days].copy()
    dropped = len(closures) - len(out)
    if dropped > 0:
        print(
            f"  [{context}] Filtered out {dropped} closure(s) with "
            f"closure_duration_days >= {max_duration_days}."
        )
    if out.empty:
        raise ValueError(
            f"No closures remain after applying closure_duration_days < {max_duration_days} filter."
        )
    return out.reset_index(drop=True)


def get_customer_store_preference(
    df: pd.DataFrame, lowest_purchases: int = DEFAULT_LOWEST_PURCHASES
) -> pd.DataFrame:
    print(f"\nCalculating customer store preferences (min {lowest_purchases} purchases)...")
    unique_visits = df[["member_id", "date", "dept_id"]].drop_duplicates()
    customer_store_counts = (
        unique_visits.groupby(["member_id", "dept_id"]).size().reset_index(name="store_purchases")
    )
    customer_totals = unique_visits.groupby("member_id").size().reset_index(name="total_purchases")
    qualified = customer_totals[customer_totals["total_purchases"] >= lowest_purchases]["member_id"]
    customer_store_counts = customer_store_counts[customer_store_counts["member_id"].isin(qualified)]
    max_idx = customer_store_counts.groupby("member_id")["store_purchases"].idxmax()
    preferred_stores = customer_store_counts.loc[max_idx].copy()
    preferred_stores = preferred_stores.merge(customer_totals, on="member_id")
    preferred_stores["preferred_ratio"] = (
        preferred_stores["store_purchases"] / preferred_stores["total_purchases"]
    )
    preferred_stores = preferred_stores.rename(
        columns={"dept_id": "preferred_store", "store_purchases": "preferred_store_purchases"}
    )
    print(f"  Qualified customers: {len(preferred_stores):,}")
    return preferred_stores


def build_date_sorted_index(df: pd.DataFrame, date_col: str = "date") -> pd.DataFrame:
    return df.sort_values(date_col).reset_index(drop=True)


def _slice_by_date(df_sorted: pd.DataFrame, start_date, end_date) -> pd.DataFrame:
    dates = df_sorted["date"].values
    lo = int(np.searchsorted(dates, start_date, side="left"))
    hi = int(np.searchsorted(dates, end_date, side="right"))
    return df_sorted.iloc[lo:hi]


def _get_treated_members_for_store(
    customer_preference: pd.DataFrame,
    dept_id: int,
    lowest_ratio: float,
) -> List:
    return (
        customer_preference[
            (customer_preference["preferred_store"] == dept_id) &
            (customer_preference["preferred_ratio"] >= lowest_ratio)
        ]["member_id"].tolist()
    )


def get_never_treated_members(
    closures: pd.DataFrame,
    customer_preference: pd.DataFrame,
    lowest_purchases: int,
    lowest_ratio: float,
) -> List:
    all_treated: set = set()
    for _, closure in closures.iterrows():
        all_treated.update(
            _get_treated_members_for_store(
                customer_preference, int(closure["dept_id"]), lowest_ratio
            )
        )
    qualified = set(
        customer_preference[
            (customer_preference["total_purchases"] >= lowest_purchases) &
            (customer_preference["preferred_ratio"] >= lowest_ratio)
        ]["member_id"].tolist()
    )
    never_treated = sorted(qualified - all_treated)
    print(f"  Never-treated control pool: {len(never_treated):,} customers")
    return never_treated


def get_closure_specific_control_members(
    unique_visits: pd.DataFrame,
    control_pool: List,
    closure_start_date,
    lowest_purchases: int,
    lowest_ratio: float,
) -> List:
    if not control_pool:
        return []

    pool_set = set(control_pool)
    pre = unique_visits[
        (unique_visits["member_id"].isin(pool_set)) &
        (unique_visits["date"] < closure_start_date)
    ]
    if pre.empty:
        return []

    pre_counts = pre.groupby("member_id").size()
    qualified = pre_counts[pre_counts >= lowest_purchases].index.tolist()
    if not qualified:
        return []

    pre_qual = pre[pre["member_id"].isin(qualified)]
    cust_store = pre_qual.groupby(["member_id", "dept_id"]).size().reset_index(name="store_purchases")
    cust_total = pre_qual.groupby("member_id").size().reset_index(name="total_purchases")
    cust_store = cust_store.merge(cust_total, on="member_id")
    cust_store["ratio"] = cust_store["store_purchases"] / cust_store["total_purchases"]
    max_ratio = cust_store.groupby("member_id")["ratio"].max()
    qualified_loyal = max_ratio[max_ratio >= lowest_ratio].index.tolist()
    return sorted(qualified_loyal)


def get_control_stores_per_closure(
    closures_df: pd.DataFrame,
    store_df: pd.DataFrame,
    n_nearest: int,
    treated_store_ids: set,
) -> Dict[Tuple[int, Any], List[int]]:
    store_df = store_df.dropna(subset=["set_up_time"]).copy()
    text_cols = [c for c in ["name", "dept_name", "store_name", "address"] if c in store_df.columns]
    if text_cols:
        joined_text = (
            store_df[text_cols]
            .fillna("")
            .astype(str)
            .agg(" ".join, axis=1)
        )
        store_df["_exclude_for_control"] = joined_text.apply(contains_excluded_control_store_keyword)
    else:
        store_df["_exclude_for_control"] = False

    closures_sorted = closures_df.sort_values("closure_start").reset_index(drop=True)
    used_control_store_ids: set = set()
    result: Dict[Tuple[int, Any], List[int]] = {}

    for _, closure in closures_sorted.iterrows():
        closed_dept_id = int(closure["dept_id"])
        closure_start = closure["closure_start"]
        closure_key = (closed_dept_id, closure_start)

        if closed_dept_id not in store_df["dept_id"].values:
            raise ValueError(
                f"Closed store dept_id={closed_dept_id} (closure_start={closure_start}) "
                f"not found in store static. Cannot get set_up_time."
            )

        t0 = store_df.loc[store_df["dept_id"] == closed_dept_id, "set_up_time"].iloc[0]

        candidates = store_df[
            (~store_df["dept_id"].isin(treated_store_ids))
            & (~store_df["dept_id"].isin(used_control_store_ids))
            & (~store_df["_exclude_for_control"])
        ].copy()
        if candidates.empty:
            raise ValueError(
                f"No eligible control store candidates for closure {closure_key}. "
                "All similar stores may be treated, excluded by keywords, or already used."
            )

        candidates["_diff"] = candidates["set_up_time"].apply(
            lambda d: abs((d - t0).days) if hasattr(d - t0, "days") else float("inf")
        )
        candidates = candidates.sort_values("_diff")
        chosen = candidates.head(n_nearest)["dept_id"].tolist()
        used_control_store_ids.update(chosen)
        result[closure_key] = chosen

    return result


def get_preference_before_date(
    unique_visits: pd.DataFrame,
    cutoff_date: Any,
) -> pd.DataFrame:
    pre = unique_visits[unique_visits["date"] < pd.Timestamp(cutoff_date).date()]
    if pre.empty:
        return pd.DataFrame(columns=["member_id", "preferred_store", "preferred_ratio", "total_purchases"])

    cust_store = pre.groupby(["member_id", "dept_id"]).size().reset_index(name="store_purchases")
    cust_total = pre.groupby("member_id").size().reset_index(name="total_purchases")
    cust_store = cust_store.merge(cust_total, on="member_id")
    cust_store["ratio"] = cust_store["store_purchases"] / cust_store["total_purchases"]
    idx_max = cust_store.groupby("member_id")["ratio"].idxmax()
    preferred = cust_store.loc[idx_max].rename(
        columns={"dept_id": "preferred_store", "ratio": "preferred_ratio", "total_purchases": "total_purchases"}
    )[["member_id", "preferred_store", "preferred_ratio", "total_purchases"]]
    preferred["preferred_store"] = preferred["preferred_store"].astype(int)
    return preferred


def get_closure_control_members_set_up_matched(
    unique_visits: pd.DataFrame,
    closure_start_date: Any,
    control_store_ids: List[int],
    lowest_purchases: int,
    lowest_ratio: float,
    closure_key: Tuple[int, Any],
) -> List[int]:
    if not control_store_ids:
        return []

    pref = get_preference_before_date(unique_visits, closure_start_date)
    control_set = set(control_store_ids)
    out = pref[
        (pref["preferred_store"].isin(control_set))
        & (pref["total_purchases"] >= lowest_purchases)
        & (pref["preferred_ratio"] >= lowest_ratio)
    ]["member_id"].tolist()

    return sorted(out) if out else []


def get_treatment_and_control_members_for_closure(
    unique_visits: pd.DataFrame,
    customer_preference: pd.DataFrame,
    closure: pd.Series,
    lowest_purchases: int,
    lowest_ratio: float,
    use_set_up_time_matched_control: bool,
    control_pool: Optional[List] = None,
    control_stores_by_closure: Optional[Dict[Tuple[int, Any], List[int]]] = None,
) -> Tuple[List, List, List[int]]:
    dept_id = int(closure["dept_id"])
    closure_start = pd.to_datetime(closure["closure_start"])

    if use_set_up_time_matched_control:
        if control_stores_by_closure is None:
            raise ValueError("control_stores_by_closure is required when use_set_up_time_matched_control=True")

        closure_key = (dept_id, closure["closure_start"])
        pref = get_preference_before_date(unique_visits, closure_start.date())
        treatment = pref[
            (pref["preferred_store"] == dept_id)
            & (pref["preferred_ratio"] >= lowest_ratio)
            & (pref["total_purchases"] >= lowest_purchases)
        ]["member_id"].tolist()

        control_store_ids = control_stores_by_closure.get(closure_key, [])
        closure_control = get_closure_control_members_set_up_matched(
            unique_visits,
            closure_start.date(),
            control_store_ids,
            lowest_purchases,
            lowest_ratio,
            closure_key,
        )
        return treatment, closure_control, control_store_ids

    treatment = _get_treated_members_for_store(
        customer_preference, dept_id, lowest_ratio
    )
    closure_control = get_closure_specific_control_members(
        unique_visits,
        control_pool or [],
        closure_start.date(),
        lowest_purchases,
        lowest_ratio,
    )
    return treatment, closure_control, []


def _serialize_int_list(values: List[int]) -> str:
    return "|".join(str(int(v)) for v in values)


def _serialize_text_list(values: List[Any]) -> str:
    return "|".join("" if pd.isna(v) else str(v) for v in values)


def _pair_key(dept_id: int, closure_start: str) -> tuple[int, str]:
    return int(dept_id), pd.to_datetime(closure_start).strftime("%Y-%m-%d")


def _parse_control_store_ids(serialized: object) -> List[int]:
    if serialized is None or (isinstance(serialized, float) and np.isnan(serialized)):
        return []
    s = str(serialized).strip()
    if not s:
        return []
    return [int(x) for x in s.split("|") if x != ""]


def _filter_control_store_ids_from_registry_row(reg_row: pd.Series) -> List[int]:
    control_store_ids = _parse_control_store_ids(reg_row.get("control_store_ids", ""))
    if not control_store_ids:
        return []

    addr_serialized = reg_row.get("control_store_addresses", "")
    addresses = str(addr_serialized).split("|") if pd.notna(addr_serialized) else []
    if not addresses:
        return control_store_ids

    kept: List[int] = []
    for idx, sid in enumerate(control_store_ids):
        addr = addresses[idx] if idx < len(addresses) else ""
        if not contains_excluded_control_store_keyword(addr):
            kept.append(sid)
    return kept


def load_kept_registry_rows() -> Dict[tuple[int, str], pd.Series]:
    if not PAIR_REGISTRY_CSV.exists():
        raise FileNotFoundError(
            f"Missing pair registry: {PAIR_REGISTRY_CSV}. "
            "Run main_customer_store.py first to generate closure_pair_registry.csv."
        )

    registry = pd.read_csv(PAIR_REGISTRY_CSV, encoding="utf-8-sig")
    required_cols = {"dept_id", "closure_start", "control_store_ids"}
    missing = required_cols - set(registry.columns)
    if missing:
        raise ValueError(
            f"Invalid pair registry at {PAIR_REGISTRY_CSV}: missing columns {sorted(missing)}"
        )

    kept = registry.copy()
    if "status" in registry.columns:
        kept = registry[registry["status"] == "kept"].copy()
    if kept.empty:
        raise ValueError(f"No kept rows found in {PAIR_REGISTRY_CSV}.")

    rows_map: Dict[tuple[int, str], pd.Series] = {
        _pair_key(int(r["dept_id"]), r["closure_start"]): r
        for _, r in kept.iterrows()
    }
    return rows_map


def build_week_level_panel(
    df_commodity: pd.DataFrame,
    df_order: pd.DataFrame,
    closures: pd.DataFrame,
    customer_preference: pd.DataFrame,
    window_weeks: int,
    lowest_purchases: int,
    lowest_ratio: float,
    use_set_up_time_matched_control: bool = False,
) -> pd.DataFrame:
    if not use_set_up_time_matched_control:
        raise ValueError("trend analysis requires set-up-time matched control via pair registry")

    from did_analysis import _compute_customer_behavior

    df_com_s = build_date_sorted_index(df_commodity)
    df_ord_s = build_date_sorted_index(df_order)
    unique_visits = df_commodity[["member_id", "date", "dept_id"]].drop_duplicates()

    registry_rows = load_kept_registry_rows()

    rows: List[Dict] = []
    n_closures = len(closures)
    for idx, (_, closure) in enumerate(closures.iterrows()):
        if (idx + 1) % 20 == 0 or idx == 0:
            print(f"    Processing closure {idx + 1}/{n_closures}...")
        dept_id = int(closure["dept_id"])
        closure_start = pd.to_datetime(closure["closure_start"])
        closure_end = pd.to_datetime(closure["closure_end"])
        closure_duration = max(int(closure["closure_duration_days"]), 1)

        reg_key = _pair_key(dept_id, closure["closure_start"])
        reg_row = registry_rows.get(reg_key)
        if reg_row is None:
            continue

        control_store_ids = _filter_control_store_ids_from_registry_row(reg_row)
        if not control_store_ids:
            continue

        treatment, closure_control, _ = get_treatment_and_control_members_for_closure(
            unique_visits=unique_visits,
            customer_preference=customer_preference,
            closure=closure,
            lowest_purchases=lowest_purchases,
            lowest_ratio=lowest_ratio,
            use_set_up_time_matched_control=True,
            control_pool=None,
            control_stores_by_closure={(dept_id, closure["closure_start"]): control_store_ids},
        )

        if not treatment or not closure_control:
            continue
        if len(treatment) < MIN_GROUP_SIZE or len(closure_control) < MIN_GROUP_SIZE:
            continue

        dur_start = closure_start.date()
        dur_end = closure_end.date()
        during_slice = _slice_by_date(df_com_s, dur_start, dur_end)
        during_purch = during_slice[["member_id"]].drop_duplicates()
        t_rate = during_purch["member_id"].isin(treatment).sum() / len(treatment)
        c_rate = during_purch["member_id"].isin(closure_control).sum() / len(closure_control)
        if c_rate < MIN_CTRL_TREAT_RATIO * t_rate:
            continue

        for group_label, members in [("treatment", treatment), ("control", closure_control)]:
            for w in range(-window_weeks, 0):
                start = (closure_start + pd.Timedelta(days=7 * w)).date()
                end = (closure_start + pd.Timedelta(days=7 * w + 6)).date()
                cust_df = _compute_customer_behavior(df_com_s, df_ord_s, members, start, end, period_length_days=7)
                cust_df["dept_id"] = dept_id
                cust_df["closure_start"] = closure_start.date()
                cust_df["closure_duration_days"] = closure_duration
                cust_df["group"] = group_label
                cust_df["t"] = w
                rows.append(cust_df)

            cust_df = _compute_customer_behavior(
                df_com_s, df_ord_s, members, dur_start, dur_end, period_length_days=closure_duration
            )
            cust_df["dept_id"] = dept_id
            cust_df["closure_start"] = closure_start.date()
            cust_df["closure_duration_days"] = closure_duration
            cust_df["group"] = group_label
            cust_df["t"] = 0
            rows.append(cust_df)

            for w in range(1, window_weeks + 1):
                start = (closure_end + pd.Timedelta(days=7 * (w - 1) + 1)).date()
                end = (closure_end + pd.Timedelta(days=7 * w)).date()
                cust_df = _compute_customer_behavior(df_com_s, df_ord_s, members, start, end, period_length_days=7)
                cust_df["dept_id"] = dept_id
                cust_df["closure_start"] = closure_start.date()
                cust_df["closure_duration_days"] = closure_duration
                cust_df["group"] = group_label
                cust_df["t"] = w
                rows.append(cust_df)

    panel = pd.concat(rows, ignore_index=True)
    panel["n_purchases_per_week"] = panel["n_purchases"] * 7
    return panel


def subset_week_level_panel(panel: pd.DataFrame, window_weeks: int) -> pd.DataFrame:
    if panel is None or panel.empty:
        return pd.DataFrame()
    return panel[panel["t"].between(-window_weeks, window_weeks)].copy()


def build_closure_pair_registry(
    df_orders_like: pd.DataFrame,
    closures: pd.DataFrame,
    customer_preference: pd.DataFrame,
    unique_visits: Optional[pd.DataFrame] = None,
    lowest_purchases: int = DEFAULT_LOWEST_PURCHASES,
    lowest_ratio: float = DEFAULT_LOWEST_RATIO,
    use_set_up_time_matched_control: bool = USE_SET_UP_TIME_MATCHED_CONTROL,
    min_group_size: int = MIN_GROUP_SIZE,
    min_ctrl_treat_ratio: float = MIN_CTRL_TREAT_RATIO,
    output_path: Optional[Path] = None,
) -> pd.DataFrame:
    closures = filter_closures_shorter_than_max(
        closures,
        max_duration_days=MAX_CLOSURE_DURATION_DAYS,
        context="registry",
    )

    if unique_visits is None:
        unique_visits = df_orders_like[["member_id", "date", "dept_id"]].drop_duplicates()

    df_s = build_date_sorted_index(df_orders_like)

    if use_set_up_time_matched_control:
        store_setups = load_store_set_up_times(DEPT_STATIC_PATH)
        treated_store_ids = set(closures["dept_id"].astype(int).unique())
        control_stores_by_closure = get_control_stores_per_closure(
            closures,
            store_setups,
            n_nearest=SET_UP_TIME_NEAREST_N,
            treated_store_ids=treated_store_ids,
        )
        control_pool = None
    else:
        control_pool = get_never_treated_members(
            closures, customer_preference, lowest_purchases, lowest_ratio
        )
        control_stores_by_closure = None

    static_df = load_store_static_features(DEPT_STATIC_PATH)
    static_map = static_df.set_index("dept_id")

    rows: List[Dict[str, Any]] = []
    for _, closure in closures.iterrows():
        dept_id = int(closure["dept_id"])
        closure_start = pd.to_datetime(closure["closure_start"])
        closure_end = pd.to_datetime(closure["closure_end"])

        treatment, closure_control, control_store_ids = get_treatment_and_control_members_for_closure(
            unique_visits=unique_visits,
            customer_preference=customer_preference,
            closure=closure,
            lowest_purchases=lowest_purchases,
            lowest_ratio=lowest_ratio,
            use_set_up_time_matched_control=use_set_up_time_matched_control,
            control_pool=control_pool,
            control_stores_by_closure=control_stores_by_closure,
        )

        dur_start = closure_start.date()
        dur_end = closure_end.date()
        during_slice = _slice_by_date(df_s, dur_start, dur_end)
        during_purch = during_slice[["member_id"]].drop_duplicates()

        n_treat = len(treatment)
        n_ctrl = len(closure_control)
        t_rate = during_purch["member_id"].isin(treatment).sum() / n_treat if n_treat > 0 else np.nan
        c_rate = during_purch["member_id"].isin(closure_control).sum() / n_ctrl if n_ctrl > 0 else np.nan

        if n_treat == 0:
            status, skip_reason = "skipped", "no_treatment"
        elif n_ctrl == 0:
            status, skip_reason = "skipped", "no_control"
        elif n_treat < min_group_size or n_ctrl < min_group_size:
            status, skip_reason = "skipped", "min_group_size"
        elif c_rate < min_ctrl_treat_ratio * t_rate:
            status, skip_reason = "skipped", "low_control_rate"
        else:
            status, skip_reason = "kept", ""

        treated_setup_time = static_map.at[dept_id, "set_up_time"] if dept_id in static_map.index else ""
        treated_address = static_map.at[dept_id, "address"] if dept_id in static_map.index else ""

        ctrl_setups = [static_map.at[sid, "set_up_time"] if sid in static_map.index else "" for sid in control_store_ids]
        ctrl_addrs = [static_map.at[sid, "address"] if sid in static_map.index else "" for sid in control_store_ids]

        rows.append({
            "dept_id": dept_id,
            "closure_start": closure["closure_start"],
            "closure_end": closure["closure_end"],
            "closure_duration_days": closure["closure_duration_days"],
            "selection_mode": "set_up_time_matched" if use_set_up_time_matched_control else "never_treated_pool",
            "lowest_purchases": lowest_purchases,
            "lowest_ratio": lowest_ratio,
            "min_group_size": min_group_size,
            "min_ctrl_treat_ratio": min_ctrl_treat_ratio,
            "treated_store_set_up_time": treated_setup_time,
            "treated_store_address": treated_address,
            "control_store_ids": _serialize_int_list(control_store_ids),
            "control_store_set_up_times": _serialize_text_list(ctrl_setups),
            "control_store_addresses": _serialize_text_list(ctrl_addrs),
            "n_control_stores": len(control_store_ids),
            "n_treatment": n_treat,
            "n_control": n_ctrl,
            "treatment_purchase_rate_during": t_rate,
            "control_purchase_rate_during": c_rate,
            "selectivity_ratio": (t_rate / c_rate) if pd.notna(t_rate) and pd.notna(c_rate) and c_rate > 0 else np.nan,
            "status": status,
            "skip_reason": skip_reason,
        })

    registry = pd.DataFrame(rows).sort_values("closure_start").reset_index(drop=True)

    if output_path is None:
        output_path = OUTPUT_CUSTOMER_STORE_DIR / "closure_pair_registry.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    registry.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"  Closure pair registry saved to: {output_path} ({len(registry)} rows)")
    print(f"  Kept closures in registry: {(registry['status'] == 'kept').sum()} / {len(registry)}")
    return registry


def prepare_shared_data(
    lowest_purchases: int = DEFAULT_LOWEST_PURCHASES,
    lowest_ratio: float = DEFAULT_LOWEST_RATIO,
) -> PreparedData:
    df_commodity = load_order_commodity_data()
    df_order = load_order_result_data()

    # Pre-filter to customers with enough overall unique purchase days.
    # This is safe for downstream analyses because any customer who can satisfy
    # a closure-time threshold of >= lowest_purchases must also satisfy it in
    # the full sample horizon.
    unique_visits_all = df_commodity[["member_id", "date", "dept_id"]].drop_duplicates()
    purchase_days = unique_visits_all.groupby("member_id").size()
    eligible_member_ids = set(purchase_days[purchase_days >= lowest_purchases].index)

    before_n_members = df_commodity["member_id"].nunique()
    before_n_rows_com = len(df_commodity)
    before_n_rows_ord = len(df_order)

    df_commodity = df_commodity[df_commodity["member_id"].isin(eligible_member_ids)].copy()
    df_order = df_order[df_order["member_id"].isin(eligible_member_ids)].copy()

    after_n_members = df_commodity["member_id"].nunique()
    print(
        f"\nCustomer pre-filter (>= {lowest_purchases} unique purchase days): "
        f"members {before_n_members:,} -> {after_n_members:,}; "
        f"commodity rows {before_n_rows_com:,} -> {len(df_commodity):,}; "
        f"order rows {before_n_rows_ord:,} -> {len(df_order):,}"
    )

    closures = pd.read_csv(CLOSURES_CSV, encoding="utf-8-sig")
    closures = filter_closures_shorter_than_max(
        closures,
        max_duration_days=MAX_CLOSURE_DURATION_DAYS,
        context="main_shared",
    )

    customer_preference = get_customer_store_preference(
        df_commodity, lowest_purchases=lowest_purchases
    )
    unique_visits = df_commodity[["member_id", "date", "dept_id"]].drop_duplicates()

    return PreparedData(
        df_commodity=df_commodity,
        df_order=df_order,
        closures=closures,
        customer_preference=customer_preference,
        unique_visits=unique_visits,
    )


def build_kept_closure_registry(
    prepared: PreparedData,
    lowest_purchases: int = DEFAULT_LOWEST_PURCHASES,
    lowest_ratio: float = DEFAULT_LOWEST_RATIO,
    use_set_up_time_matched_control: bool = USE_SET_UP_TIME_MATCHED_CONTROL,
    output_path: Path | None = None,
) -> pd.DataFrame:
    if output_path is None:
        output_path = OUTPUT_CUSTOMER_STORE_DIR / "closure_pair_registry.csv"

    registry = build_closure_pair_registry(
        df_orders_like=prepared.df_commodity,
        closures=prepared.closures,
        customer_preference=prepared.customer_preference,
        unique_visits=prepared.unique_visits,
        lowest_purchases=lowest_purchases,
        lowest_ratio=lowest_ratio,
        use_set_up_time_matched_control=use_set_up_time_matched_control,
        min_group_size=MIN_GROUP_SIZE,
        min_ctrl_treat_ratio=MIN_CTRL_TREAT_RATIO,
        output_path=output_path,
    )

    kept = registry[registry["status"] == "kept"].copy()
    kept = kept.sort_values("closure_start").reset_index(drop=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    kept.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"  Kept-only closure registry saved to: {output_path} ({len(kept)} rows)")
    return kept


def merge_did_summaries_into_registry(
    registry_kept: pd.DataFrame,
    summary_by_window: Dict[int, pd.DataFrame],
    output_path: Path | None = None,
) -> pd.DataFrame:
    if output_path is None:
        output_path = OUTPUT_CUSTOMER_STORE_DIR / "closure_pair_registry.csv"

    merged = registry_kept.copy()

    for window_days, summary_df in summary_by_window.items():
        if summary_df is None or summary_df.empty:
            continue

        cols = [
            "dept_id",
            "closure_start",
            "#treatment",
            "#control",
            "treatment_purchase_rate_during",
            "control_purchase_rate_during",
            "selectivity_ratio",
        ]
        available = [c for c in cols if c in summary_df.columns]
        piece = summary_df[available].copy()

        rename_map = {
            "#treatment": f"w{window_days}_n_treatment",
            "#control": f"w{window_days}_n_control",
            "treatment_purchase_rate_during": f"w{window_days}_treat_rate_during",
            "control_purchase_rate_during": f"w{window_days}_ctrl_rate_during",
            "selectivity_ratio": f"w{window_days}_selectivity_ratio",
        }
        piece = piece.rename(columns=rename_map)

        merged = merged.merge(piece, on=["dept_id", "closure_start"], how="left")

    merged.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"  Registry with merged DiD summaries saved to: {output_path}")
    return merged
