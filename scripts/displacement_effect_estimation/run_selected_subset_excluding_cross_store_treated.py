from __future__ import annotations

import json
import os
from pathlib import Path

import pandas as pd


def detect_data_dir(project_root: Path) -> Path:
    candidates = [
        project_root.parent / "data" / "data1031",
        project_root / "data" / "data1031",
    ]
    for candidate in candidates:
        if (candidate / "order_result.csv").exists():
            return candidate
    return candidates[0]


def load_member_store_orders(member_ids: set[int], project_root: Path) -> pd.DataFrame:
    data_dir = detect_data_dir(project_root=project_root)
    order_path = data_dir / "order_result.csv"
    if not order_path.exists():
        raise FileNotFoundError(f"order_result.csv not found: {order_path}")

    if not member_ids:
        return pd.DataFrame(columns=["member_id", "date", "dept_id"])

    frames: list[pd.DataFrame] = []
    for chunk in pd.read_csv(
        order_path,
        encoding="utf-8-sig",
        usecols=["member_id", "create_hour", "dept_id"],
        chunksize=1_000_000,
    ):
        chunk = chunk[chunk["member_id"].isin(member_ids)]
        if chunk.empty:
            continue
        chunk["date"] = pd.to_datetime(chunk["create_hour"], errors="coerce").dt.normalize()
        chunk = chunk.dropna(subset=["date", "dept_id"])
        if chunk.empty:
            continue
        chunk["dept_id"] = pd.to_numeric(chunk["dept_id"], errors="coerce")
        chunk = chunk.dropna(subset=["dept_id"])
        if chunk.empty:
            continue
        chunk["dept_id"] = chunk["dept_id"].astype(int)
        frames.append(chunk[["member_id", "date", "dept_id"]])

    if not frames:
        return pd.DataFrame(columns=["member_id", "date", "dept_id"])

    out = pd.concat(frames, ignore_index=True).drop_duplicates()
    return out.sort_values(["member_id", "date"]).reset_index(drop=True)


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    os.environ["DISPLACEMENT_EFFECT_CLOSURE_REGISTRY"] = (
        "outputs/customer-store/closure_pair_registry_selected.csv"
    )

    # Lazy imports so this script can be run from repo root.
    import sys

    src_dir = project_root / "src" / "displacement_effect_estimation"
    sys.path.insert(0, str(src_dir))
    from data import build_estimation_sample, load_config
    from report import save_outputs
    from specs import fit_collapsed_specs, fit_event_study_specs

    cfg = load_config()
    output_dir = project_root / "outputs/robustness/selected_subset_excluding_cross_store_treated"
    output_dir.mkdir(parents=True, exist_ok=True)

    sample = build_estimation_sample(
        outcome="n_purchases",
        cfg=cfg,
        t_horizon=4,
        closure_duration_days=False,
        separate_effect=False,
        select_recency_consumers=False,
        require_balanced_panel=None,
        variety_seeking_mode="distinct",
        drop_period0_purchasers=False,
        unbalanced_panel=True,
    )

    treated_events = sample.loc[
        sample["treated"] == 1,
        ["member_id", "dept_id", "closure_start", "closure_end"],
    ].drop_duplicates()
    treated_events["closure_start_dt"] = pd.to_datetime(treated_events["closure_start"])
    treated_events["closure_end_dt"] = pd.to_datetime(treated_events["closure_end"])
    treated_events["dept_id"] = treated_events["dept_id"].astype(int)

    orders = load_member_store_orders(
        member_ids=set(treated_events["member_id"].astype(int).tolist()),
        project_root=project_root,
    )

    merged = treated_events.merge(orders, on="member_id", how="left")
    during_closure = merged[
        (merged["date"] >= merged["closure_start_dt"])
        & (merged["date"] <= merged["closure_end_dt"])
        & (merged["dept_id_y"] != merged["dept_id_x"])
    ].copy()

    excluded_keys = (
        during_closure[["member_id", "dept_id_x", "closure_start"]]
        .drop_duplicates()
        .rename(columns={"dept_id_x": "dept_id"})
    )
    excluded_keys["exclude_treated_cross_store_during_closure"] = 1

    treated_flag = treated_events[["member_id", "dept_id", "closure_start"]].copy()
    treated_flag = treated_flag.merge(
        excluded_keys,
        on=["member_id", "dept_id", "closure_start"],
        how="left",
    )
    treated_flag["exclude_treated_cross_store_during_closure"] = (
        treated_flag["exclude_treated_cross_store_during_closure"].fillna(0).astype(int)
    )

    sample_with_flag = sample.merge(
        treated_flag,
        on=["member_id", "dept_id", "closure_start"],
        how="left",
    )
    sample_with_flag["exclude_treated_cross_store_during_closure"] = (
        sample_with_flag["exclude_treated_cross_store_during_closure"].fillna(0).astype(int)
    )

    filtered_sample = sample_with_flag[
        ~(
            (sample_with_flag["treated"] == 1)
            & (sample_with_flag["exclude_treated_cross_store_during_closure"] == 1)
        )
    ].copy()

    exclusion_rate = float(
        treated_flag["exclude_treated_cross_store_during_closure"].mean()
        if len(treated_flag) > 0
        else 0.0
    )

    exclusion_by_closure = (
        treated_flag.groupby(["dept_id", "closure_start"], as_index=False)[
            "exclude_treated_cross_store_during_closure"
        ]
        .sum()
        .rename(columns={"exclude_treated_cross_store_during_closure": "excluded_treated_members"})
        .sort_values(["closure_start", "dept_id"])
    )
    exclusion_by_closure.to_csv(
        output_dir / "excluded_treated_during_closure_summary.csv", index=False
    )

    coef_df, fit_df = fit_collapsed_specs(
        df=filtered_sample,
        outcome="n_purchases",
        cluster_col="member_id",
        use_did=False,
    )
    event_df, event_fit_df, pretrend_df = fit_event_study_specs(
        df=filtered_sample,
        outcome="n_purchases",
        cluster_col="member_id",
        include_length_heterogeneity=True,
        use_did=False,
    )

    save_outputs(
        output_dir=output_dir,
        sample=filtered_sample,
        binary_terms=coef_df[coef_df["spec"].isin(["binary_collapsed", "binary_collapsed_logit"])].copy(),
        binary_fit=fit_df[fit_df["spec"].isin(["binary_collapsed", "binary_collapsed_logit"])].copy(),
        score_terms=coef_df[coef_df["spec"] == "score_collapsed"].copy(),
        score_fit=fit_df[fit_df["spec"] == "score_collapsed"].copy(),
        event_terms=event_df,
        event_fit=event_fit_df,
        pretrend_tests=pretrend_df,
        summary_notes=[
            "- Robustness design: exclude treated members with any cross-store purchase during closure",
            f"- Treated exclusion rate: {exclusion_rate:.4%}",
            f"- Excluded treated member-events: {int(treated_flag['exclude_treated_cross_store_during_closure'].sum())}",
        ],
    )

    selected_event = pd.read_csv(
        project_root / "outputs/robustness/selected_subset/n_purchases/event_study_results.csv",
        encoding="utf-8-sig",
    )
    filtered_event = event_df.copy()
    selected_att = selected_event[selected_event["spec"] == "event_att"].copy()
    filtered_att = filtered_event[filtered_event["spec"] == "event_att"].copy()
    selected_att["period"] = selected_att["term"].str.extract(r"\[(-?\d+)\]").astype(int)
    filtered_att["period"] = filtered_att["term"].str.extract(r"\[(-?\d+)\]").astype(int)

    comparison = selected_att[["period", "coef", "se", "pvalue"]].merge(
        filtered_att[["period", "coef", "se", "pvalue"]],
        on="period",
        suffixes=("_selected_subset", "_exclude_cross_store"),
    )
    comparison["delta_coef"] = (
        comparison["coef_exclude_cross_store"] - comparison["coef_selected_subset"]
    )
    comparison = comparison.sort_values("period")
    comparison.to_csv(output_dir / "event_att_comparison_vs_selected_subset.csv", index=False)

    # Also estimate the overall collapsed treatment effects for the binary incidence outcome
    binary_sample = build_estimation_sample(
        outcome="purchase_incidence_binary",
        cfg=cfg,
        t_horizon=4,
        closure_duration_days=False,
        separate_effect=False,
        select_recency_consumers=False,
        require_balanced_panel=None,
        variety_seeking_mode="distinct",
        drop_period0_purchasers=False,
        unbalanced_panel=True,
    )
    binary_sample = binary_sample.merge(
        treated_flag[["member_id", "dept_id", "closure_start", "exclude_treated_cross_store_during_closure"]],
        on=["member_id", "dept_id", "closure_start"],
        how="left",
    )
    binary_sample["exclude_treated_cross_store_during_closure"] = (
        binary_sample["exclude_treated_cross_store_during_closure"].fillna(0).astype(int)
    )
    binary_filtered = binary_sample[
        ~(
            (binary_sample["treated"] == 1)
            & (binary_sample["exclude_treated_cross_store_during_closure"] == 1)
        )
    ].copy()

    binary_before_terms, _ = fit_collapsed_specs(
        df=binary_sample,
        outcome="purchase_incidence_binary",
        cluster_col="member_id",
        use_did=False,
    )
    binary_after_terms, _ = fit_collapsed_specs(
        df=binary_filtered,
        outcome="purchase_incidence_binary",
        cluster_col="member_id",
        use_did=False,
    )
    keep_terms = ["post_X_treated", "post_X_treated_X_disp"]
    overall_binary_compare = binary_before_terms[
        (binary_before_terms["spec"] == "binary_collapsed")
        & (binary_before_terms["term"].isin(keep_terms))
    ][["term", "coef", "pvalue"]].merge(
        binary_after_terms[
            (binary_after_terms["spec"] == "binary_collapsed")
            & (binary_after_terms["term"].isin(keep_terms))
        ][["term", "coef", "pvalue"]],
        on="term",
        suffixes=("_selected_subset", "_exclude_cross_store"),
    )
    overall_binary_compare["coef_change"] = (
        overall_binary_compare["coef_exclude_cross_store"]
        - overall_binary_compare["coef_selected_subset"]
    )
    overall_binary_compare.to_csv(
        output_dir / "overall_effect_purchase_incidence_binary_comparison.csv",
        index=False,
    )

    # Save corresponding n_purchases overall-effect before-vs-after in one file
    selected_binary = pd.read_csv(
        project_root / "outputs/robustness/selected_subset/n_purchases/ddd_binary_results.csv",
        encoding="utf-8-sig",
    )
    filtered_binary = coef_df.copy()
    overall_np_compare = selected_binary[
        (selected_binary["spec"] == "binary_collapsed")
        & (selected_binary["term"].isin(keep_terms))
    ][["term", "coef", "pvalue"]].merge(
        filtered_binary[
            (filtered_binary["spec"] == "binary_collapsed")
            & (filtered_binary["term"].isin(keep_terms))
        ][["term", "coef", "pvalue"]],
        on="term",
        suffixes=("_selected_subset", "_exclude_cross_store"),
    )
    overall_np_compare["coef_change"] = (
        overall_np_compare["coef_exclude_cross_store"]
        - overall_np_compare["coef_selected_subset"]
    )
    overall_np_compare.to_csv(
        output_dir / "overall_effect_n_purchases_comparison.csv",
        index=False,
    )

    metadata = {
        "date": "2026-04-27",
        "source_registry_path": "outputs/customer-store/closure_pair_registry_selected.csv",
        "filter_definition": "exclude treated member-event if member made >=1 purchase at dept_id != treated dept_id during [closure_start, closure_end]",
        "treated_member_events_before_filter": int(len(treated_flag)),
        "treated_member_events_excluded": int(
            treated_flag["exclude_treated_cross_store_during_closure"].sum()
        ),
        "treated_exclusion_rate": exclusion_rate,
        "sample_rows_before_filter": int(len(sample)),
        "sample_rows_after_filter": int(len(filtered_sample)),
        "unique_members_before_filter": int(sample["member_id"].nunique()),
        "unique_members_after_filter": int(filtered_sample["member_id"].nunique()),
    }
    (output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(metadata, ensure_ascii=True))


if __name__ == "__main__":
    main()
