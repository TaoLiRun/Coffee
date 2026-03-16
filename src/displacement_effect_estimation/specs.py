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


def fit_threshold_specs(
    df: pd.DataFrame,
    outcome: str,
    thresholds: Iterable[float],
    cluster_col: str = "member_id",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    fit_rows = []
    for tau in thresholds:
        tag = str(tau).replace(".", "")
        disp_col = f"disp_{tag}"
        formula = (
            f"{outcome} ~ post + treated + {disp_col} + "
            f"post:treated + post:{disp_col} + treated:{disp_col} + "
            f"post:treated:{disp_col} + C(dept_id) + C(closure_start)"
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
    formula = (
        f"{outcome} ~ post + treated + displacement_prob + "
        f"post:treated + post:displacement_prob + treated:displacement_prob + "
        f"post:treated:displacement_prob + C(dept_id) + C(closure_start)"
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
