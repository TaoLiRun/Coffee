from __future__ import annotations

from typing import Iterable

import pandas as pd
import statsmodels.formula.api as smf


def _extract_term(result, term: str, spec_name: str, n: int) -> dict:
    if term not in result.params.index:
        return {
            "spec": spec_name,
            "term": term,
            "coef": float("nan"),
            "se": float("nan"),
            "pvalue": float("nan"),
            "n": n,
            "r2": float(result.rsquared),
        }
    return {
        "spec": spec_name,
        "term": term,
        "coef": float(result.params[term]),
        "se": float(result.bse[term]),
        "pvalue": float(result.pvalues[term]),
        "n": n,
        "r2": float(result.rsquared),
    }


def _extract_terms_by_keyword(result, keyword: str, spec_name: str, n: int) -> list[dict]:
    rows: list[dict] = []
    for term in result.params.index:
        if keyword in term:
            rows.append(
                {
                    "spec": spec_name,
                    "term": term,
                    "coef": float(result.params[term]),
                    "se": float(result.bse[term]),
                    "pvalue": float(result.pvalues[term]),
                    "n": n,
                    "r2": float(result.rsquared),
                }
            )
    return rows


def fit_threshold_specs(
    df: pd.DataFrame,
    outcome: str,
    thresholds: Iterable[float],
    cluster_col: str = "member_id",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Collapsed (post vs pre) threshold DDD specs with event-unit FE."""
    rows = []
    fit_rows = []
    for tau in thresholds:
        tag = str(tau).replace(".", "")
        disp_col = f"disp_{tag}"
        formula = (
            f"{outcome} ~ post + treated + {disp_col} + "
            f"post:treated + post:{disp_col} + treated:{disp_col} + "
            f"post:treated:{disp_col} + C(event_fe_id) + C(rel_t)"
        )
        model = smf.ols(formula=formula, data=df)
        result = model.fit(cov_type="cluster", cov_kwds={"groups": df[cluster_col]})

        spec_name = f"threshold_{tau}"
        fit_rows.append(
            {
                "spec": spec_name,
                "formula": formula,
                "n": int(result.nobs),
                "r2": float(result.rsquared),
            }
        )
        rows.append(_extract_term(result, "post:treated", spec_name, int(result.nobs)))
        rows.append(_extract_term(result, f"post:treated:{disp_col}", spec_name, int(result.nobs)))

    return pd.DataFrame(rows), pd.DataFrame(fit_rows)


def fit_score_spec(
    df: pd.DataFrame,
    outcome: str,
    cluster_col: str = "member_id",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Collapsed (post vs pre) continuous-score DDD spec with event-unit FE."""
    formula = (
        f"{outcome} ~ post + treated + displacement_prob + "
        f"post:treated + post:displacement_prob + treated:displacement_prob + "
        f"post:treated:displacement_prob + C(event_fe_id) + C(rel_t)"
    )
    model = smf.ols(formula=formula, data=df)
    result = model.fit(cov_type="cluster", cov_kwds={"groups": df[cluster_col]})

    spec_name = "score_continuous"
    rows = [
        _extract_term(result, "post:treated", spec_name, int(result.nobs)),
        _extract_term(result, "post:treated:displacement_prob", spec_name, int(result.nobs)),
    ]
    fit_rows = [
        {
            "spec": spec_name,
            "formula": formula,
            "n": int(result.nobs),
            "r2": float(result.rsquared),
        }
    ]
    return pd.DataFrame(rows), pd.DataFrame(fit_rows)


def fit_event_study_specs(
    df: pd.DataFrame,
    outcome: str,
    thresholds: Iterable[float],
    cluster_col: str = "member_id",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Event-study ATT/DDD specs aligned with markdown framework (T-horizon panel)."""
    rows: list[dict] = []
    fit_rows: list[dict] = []
    rel = "C(rel_t, Treatment(reference=-1))"

    # ATT event-study
    spec_name = "event_att"
    formula = f"{outcome} ~ {rel}:treated + C(event_fe_id) + C(rel_t)"
    result = smf.ols(formula=formula, data=df).fit(cov_type="cluster", cov_kwds={"groups": df[cluster_col]})
    fit_rows.append({"spec": spec_name, "formula": formula, "n": int(result.nobs), "r2": float(result.rsquared)})
    rows.extend(_extract_terms_by_keyword(result, f"{rel}[", spec_name, int(result.nobs)))

    # Binary displacement DDD event-study + closure-length interaction
    for tau in thresholds:
        tag = str(tau).replace(".", "")
        disp_col = f"disp_{tag}"

        spec_name = f"event_threshold_{tau}"
        formula = (
            f"{outcome} ~ "
            f"{rel}:treated + "
            f"{rel}:treated:{disp_col} + "
            f"{rel}:{disp_col} + "
            f"{rel}:treated:{disp_col}:closure_duration_days + "
            f"C(event_fe_id) + C(rel_t)"
        )
        result = smf.ols(formula=formula, data=df).fit(
            cov_type="cluster", cov_kwds={"groups": df[cluster_col]}
        )
        fit_rows.append(
            {
                "spec": spec_name,
                "formula": formula,
                "n": int(result.nobs),
                "r2": float(result.rsquared),
            }
        )
        rows.extend(_extract_terms_by_keyword(result, f":treated:{disp_col}", spec_name, int(result.nobs)))
        rows.extend(_extract_terms_by_keyword(result, f":{disp_col}:closure_duration_days", spec_name, int(result.nobs)))

    # Continuous displacement score DDD event-study
    spec_name = "event_score_continuous"
    formula = (
        f"{outcome} ~ "
        f"{rel}:treated + "
        f"{rel}:treated:displacement_prob + "
        f"{rel}:displacement_prob + "
        f"C(event_fe_id) + C(rel_t)"
    )
    result = smf.ols(formula=formula, data=df).fit(cov_type="cluster", cov_kwds={"groups": df[cluster_col]})
    fit_rows.append({"spec": spec_name, "formula": formula, "n": int(result.nobs), "r2": float(result.rsquared)})
    rows.extend(_extract_terms_by_keyword(result, ":treated:displacement_prob", spec_name, int(result.nobs)))

    return pd.DataFrame(rows), pd.DataFrame(fit_rows)
