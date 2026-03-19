"""
specs.py
--------
Econometric specifications for the habit-breaking analysis.

All regressions use pyfixest.feols(), which absorbs fixed effects via
the Frisch-Waugh-Lovell within-transformation instead of constructing
explicit dummy columns.  This is orders of magnitude faster than
statsmodels OLS with C(event_fe_id) for large panels.

Fixed effects absorbed in every specification
---------------------------------------------
  event_fe_id    : consumer-closure fixed effect phi_{ie}.
                   Absorbs all time-invariant consumer-closure
                   characteristics, including the main effects of
                   `treated` and `disp_binary` / `displacement_prob_centered`
                   (both constant within a consumer-closure pair).
                   Also absorbs the main effect of `closure_length_std`.
  rel_t          : relative-time fixed effect omega_t.
                   Absorbs common purchase dynamics in event time.
  calendar_month : calendar-month fixed effect gamma_m.
                   Absorbs seasonality not captured by omega_t, since
                   closures occur at different calendar dates.

Required columns in the input DataFrame
----------------------------------------
  outcome                      : purchases per day (float)
  treated                      : 1 = treated consumer, 0 = control  (float)
  disp_binary                  : 1 = displaced, 0 = non-displaced    (float)
  displacement_prob_centered   : s_tilde_{ie} = s_{ie} - mean(s)    (float)
  closure_length_std           : L_tilde_e = (L_e - mean) / sd      (float)
  rel_t                        : integer relative period (-4,...,-1,1,...)
                                 t = 0 (closure window) must already
                                 be excluded from df before calling.
  event_fe_id                  : string/int consumer-closure pair id
  calendar_month               : integer or string month of the period
  post                         : 1 if rel_t > 0, 0 if rel_t < 0     (float)
                                 (collapsed specs only)
  member_id (default cluster)  : consumer id for SE clustering

Specification map (matches identification_rewrite.md section 2.3)
------------------------------------------------------------------
  Collapsed (post-dummy) specs  ->  fit_collapsed_specs()
      binary_collapsed           : Spec B collapsed   (delta^B, delta^D, beta)
      score_collapsed            : Spec C collapsed   (delta^B, delta^S, beta^S)

  Event-study specs             ->  fit_event_study_specs()
      event_att                  : Spec A  (delta_l)
      event_binary_B             : Spec B  (delta^B_l, delta^D_l, beta_l)
      event_binary_D             : Spec D  (adds theta_l, kappa_l for length)
      event_score_C              : Spec C  (delta^B_l, delta^S_l, beta^S_l)

Pre-trend joint-zero F-tests are produced for every event-study spec.

Duplication-safety note
-----------------------
pyfixest names i(rel_t, x, ref=-1) terms as
    "C(rel_t, contr.treatment(base=-1))[<t>]:<x>"
Using substring `in` to match ":treated" would also match
":treated_X_disp", ":treated_X_len", etc., causing duplicate rows.
All extraction helpers below use str.endswith() for exact suffix
matching and str.startswith() is never used for term selection.
"""

from __future__ import annotations

import re
import warnings
from typing import Sequence

import numpy as np
import pandas as pd
import pyfixest as pf


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _assert_columns(df: pd.DataFrame, required: list[str]) -> None:
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"DataFrame is missing required columns: {missing}")


def _tidy_row(fit, term: str, spec: str) -> dict:
    """Extract one named coefficient row from a pyfixest result."""
    tidy = fit.tidy()
    row: dict = {
        "spec":      spec,
        "term":      term,
        "n":         fit._N,
        "r2_within": fit._r2_within,
    }
    if term in tidy.index:
        row["coef"]   = float(tidy.loc[term, "Estimate"])
        row["se"]     = float(tidy.loc[term, "Std. Error"])
        row["pvalue"] = float(tidy.loc[term, "Pr(>|t|)"])
    else:
        row["coef"] = row["se"] = row["pvalue"] = float("nan")
    return row


def _tidy_rows_suffix(fit, suffix: str, spec: str) -> list[dict]:
    """
    Extract all coefficient rows whose name ends exactly with `suffix`.

    endswith() is mandatory here: ":treated" must NOT match
    ":treated_X_disp", ":treated_X_len", or ":treated_X_score".
    """
    tidy = fit.tidy()
    out: list[dict] = []
    for term in tidy.index:
        if str(term).endswith(suffix):
            out.append({
                "spec":      spec,
                "term":      str(term),
                "coef":      float(tidy.loc[term, "Estimate"]),
                "se":        float(tidy.loc[term, "Std. Error"]),
                "pvalue":    float(tidy.loc[term, "Pr(>|t|)"]),
                "n":         fit._N,
                "r2_within": fit._r2_within,
            })
    return out


def _fit_row(fit, spec: str, formula: str) -> dict:
    return {
        "spec":      spec,
        "formula":   formula,
        "n":         fit._N,
        "r2":        fit._r2,
        "r2_within": fit._r2_within,
    }


def _pre_period_terms(tidy_index: pd.Index,
                      pre_periods: list[int],
                      suffix: str) -> list[str]:
    """
    Return coefficient names that satisfy both:
      (a) correspond to one of `pre_periods` in the i()-interaction bracket, AND
      (b) end exactly with `suffix`.

    pyfixest names i(rel_t, x, ref=-1) terms as
        "C(rel_t, contr.treatment(base=-1))[<t>]:<x>"
    We extract all [...] tokens and intersect with the pre-period set,
    then apply endswith() for the suffix to avoid false matches.
    """
    tokens = {f"[{t}]" for t in pre_periods}   # e.g. {"[-4]","[-3]","[-2]"}
    selected: list[str] = []
    for name in tidy_index:
        brackets = set(re.findall(r"\[[-\d]+\]", str(name)))
        if not brackets.intersection(tokens):
            continue
        if str(name).endswith(suffix):
            selected.append(str(name))
    return selected


def _joint_zero_test(fit,
                     terms: list[str],
                     spec: str,
                     test_name: str) -> dict:
    """
    Joint chi2/F test that all coefficients in `terms` equal zero,
    using pyfixest's wald_test(R=...) interface.
    """
    row: dict = {
        "spec":           spec,
        "test":           test_name,
        "n_restrictions": len(terms),
        "statistic":      float("nan"),
        "pvalue":         float("nan"),
        "n":              fit._N,
    }
    if not terms:
        return row

    tidy       = fit.tidy()
    coef_names = list(tidy.index)
    idx        = {str(name): i for i, name in enumerate(coef_names)}

    valid = [t for t in terms if t in idx]
    if not valid:
        return row

    p = len(coef_names)
    R = np.zeros((len(valid), p), dtype=float)
    for i, name in enumerate(valid):
        R[i, idx[name]] = 1.0

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")   # suppress chi2-upgrade warning
        result = fit.wald_test(R=R)

    row["statistic"]      = float(result.iloc[0])
    row["pvalue"]         = float(result.iloc[1])
    row["n_restrictions"] = len(valid)
    return row


# ---------------------------------------------------------------------------
# Collapsed (post-dummy) specifications
# ---------------------------------------------------------------------------

def fit_collapsed_specs(
    df:          pd.DataFrame,
    outcome:     str,
    cluster_col: str = "member_id",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Collapsed (post vs. pre) binary and continuous-score DDD specs.

    These pool all post-periods into a single `post` dummy and serve
    as compact scalar summaries alongside the event-study versions.
    The event-study versions are the primary specifications; these
    are reported as supplementary scalars.

    t = 0 rows must be excluded from df before calling.
    `post` must be a column in df: 1 if rel_t > 0, 0 if rel_t < 0.

    Spec B collapsed
    ----------------
    y_{iet} = delta^B * post * treated_{ie}
            + delta^D * post * treated_{ie} * D_{ie}
            + beta    * post * D_{ie}
            + phi_{ie} + omega_t + gamma_m + nu_{iet}

    delta^B : baseline-demand effect (non-displaced treated vs control)
    delta^D : displacement effect (additional reduction for displaced)
    beta    : post-period level shift for displaced consumers (all groups)

    Spec C collapsed
    ----------------
    y_{iet} = delta^B * post * treated_{ie}
            + delta^S * post * treated_{ie} * s_tilde_{ie}
            + beta^S  * post * s_tilde_{ie}
            + phi_{ie} + omega_t + gamma_m + nu_{iet}

    delta^B : baseline-demand effect at mean propensity (s_tilde = 0)
    delta^S : marginal displacement effect per unit of centered score
    beta^S  : propensity-purchase relationship pooled across groups

    Returns
    -------
    coef_df : one row per extracted coefficient
    fit_df  : one row per fitted model (formula, n, R2)
    """
    _assert_columns(df, [
        outcome, "post", "treated", "disp_binary",
        "displacement_prob_centered",
        "event_fe_id", "rel_t", "calendar_month", cluster_col,
    ])

    # Pre-compute interaction columns.
    # event_fe_id absorbs `treated`, `disp_binary`, and
    # `displacement_prob_centered` (all time-invariant within a
    # consumer-closure pair).  Only their products with `post`
    # (which varies within the pair) survive FE absorption.
    df = df.copy()
    df["post_X_treated"]         = df["post"] * df["treated"]
    df["post_X_disp"]            = df["post"] * df["disp_binary"]
    df["post_X_treated_X_disp"]  = df["post"] * df["treated"] * df["disp_binary"]
    df["post_X_score"]           = df["post"] * df["displacement_prob_centered"]
    df["post_X_treated_X_score"] = df["post"] * df["treated"] * df["displacement_prob_centered"]

    vcov     = {"CRV1": cluster_col}
    fe_str   = "event_fe_id + rel_t + calendar_month"
    rows:     list[dict] = []
    fit_rows: list[dict] = []

    # ------------------------------------------------------------------
    # Spec B collapsed
    # ------------------------------------------------------------------
    spec    = "binary_collapsed"
    formula = (
        f"{outcome} ~ "
        f"post_X_treated + post_X_disp + post_X_treated_X_disp"
        f" | {fe_str}"
    )
    fit = pf.feols(formula, data=df, vcov=vcov)
    fit_rows.append(_fit_row(fit, spec, formula))
    for term in ("post_X_treated", "post_X_disp", "post_X_treated_X_disp"):
        rows.append(_tidy_row(fit, term, spec))

    # ------------------------------------------------------------------
    # Spec C collapsed
    # ------------------------------------------------------------------
    spec    = "score_collapsed"
    formula = (
        f"{outcome} ~ "
        f"post_X_treated + post_X_score + post_X_treated_X_score"
        f" | {fe_str}"
    )
    fit = pf.feols(formula, data=df, vcov=vcov)
    fit_rows.append(_fit_row(fit, spec, formula))
    for term in ("post_X_treated", "post_X_score", "post_X_treated_X_score"):
        rows.append(_tidy_row(fit, term, spec))

    return pd.DataFrame(rows), pd.DataFrame(fit_rows)


# ---------------------------------------------------------------------------
# Event-study specifications
# ---------------------------------------------------------------------------

def fit_event_study_specs(
    df:          pd.DataFrame,
    outcome:     str,
    cluster_col: str = "member_id",
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Event-study versions of Specs A, B, C, D (identification_rewrite.md
    section 2.3).

    All specifications use i(rel_t, <var>, ref=-1) to interact relative-time
    dummies with treatment/displacement variables, with t = -1 as the omitted
    reference period.  t = 0 rows must already be excluded from df.

    Fixed effects absorbed in all specs: event_fe_id + rel_t + calendar_month.
    Because event_fe_id is a consumer-closure FE (phi_{ie}), it absorbs:
      - main effects of `treated`, `disp_binary`, `displacement_prob_centered`,
        `closure_length_std`  (all time-invariant within a consumer-closure)
      - all products of these variables with each other (also time-invariant)
    Only their products with the time-varying rel_t dummies are identified.

    Interaction columns pre-computed to avoid formula-parser collisions
    -------------------------------------------------------------------
    treated_X_disp   = treated  * disp_binary              (delta^D)
    treated_X_len    = treated  * closure_length_std        (kappa)
    disp_X_len       = disp_binary * closure_length_std     (lower-order)
    tXdXlen          = treated  * disp_binary * closure_length_std  (theta)
    treated_X_score  = treated  * displacement_prob_centered (delta^S)

    Pre-trend tests produced
    ------------------------
    Spec A : delta_l         for l < -1  (ATT parallel trends)
    Spec B : delta^B_l       for l < -1  (baseline parallel trends)
             delta^D_l       for l < -1  (displacement parallel trends)
    Spec C : delta^B_l       for l < -1  (baseline parallel trends)
             delta^S_l       for l < -1  (score-slope falsification)
    Spec D : theta_l         for l < -1  (length x displacement falsification)
             kappa_l         for l < -1  (length x baseline falsification)

    Returns
    -------
    coef_df     : one row per (spec, term, period)
    fit_df      : one row per fitted model
    pretrend_df : one row per joint pre-trend F-test
    """
    _assert_columns(df, [
        outcome, "treated", "disp_binary",
        "displacement_prob_centered", "closure_length_std",
        "event_fe_id", "rel_t", "calendar_month", cluster_col,
    ])

    df = df.copy()
    df["treated_X_disp"]  = df["treated"]  * df["disp_binary"]
    df["treated_X_len"]   = df["treated"]  * df["closure_length_std"]
    df["disp_X_len"]      = df["disp_binary"] * df["closure_length_std"]
    df["tXdXlen"]         = df["treated"]  * df["disp_binary"] * df["closure_length_std"]
    df["treated_X_score"] = df["treated"]  * df["displacement_prob_centered"]

    pre_periods: list[int] = sorted(int(t) for t in df["rel_t"].unique() if int(t) < -1)
    vcov    = {"CRV1": cluster_col}
    fe_str  = "event_fe_id + rel_t + calendar_month"

    rows:     list[dict] = []
    fit_rows: list[dict] = []
    pre_rows: list[dict] = []

    # ------------------------------------------------------------------
    # Spec A: Overall ATT event study
    #
    # y_{iet} = sum_{l != -1} delta_l * 1(t=l) * treated_{ie}
    #           + phi_{ie} + omega_t + gamma_m + nu_{iet}
    #
    # i(rel_t, treated, ref=-1) produces one delta_l per period l != -1.
    #
    # Interpretation:
    #   l < -1 : pre-trend test -- should be jointly zero
    #   l > 0  : post-closure ATT (displacement + baseline combined)
    # ------------------------------------------------------------------
    spec    = "event_att"
    formula = f"{outcome} ~ i(rel_t, treated, ref=-1) | {fe_str}"
    fit     = pf.feols(formula, data=df, vcov=vcov)
    fit_rows.append(_fit_row(fit, spec, formula))
    rows.extend(_tidy_rows_suffix(fit, ":treated", spec))
    pre_rows.append(_joint_zero_test(
        fit       = fit,
        terms     = _pre_period_terms(fit.tidy().index, pre_periods, ":treated"),
        spec      = spec,
        test_name = "pretrend_att_joint_zero",
    ))

    # ------------------------------------------------------------------
    # Spec B: Triple-difference, binary displacement
    #
    # y_{iet} = sum_{l!=-1} delta^B_l * 1(t=l) * treated_{ie}
    #         + sum_{l!=-1} delta^D_l * 1(t=l) * treated_{ie} * D_{ie}
    #         + sum_{l!=-1} beta_l    * 1(t=l) * D_{ie}
    #         + phi_{ie} + omega_t + gamma_m + nu_{iet}
    #
    # Cell means at l > 0 (after FE, relative to t=-1):
    #   Control  x Non-disp :  0
    #   Control  x Displaced:  beta_l
    #   Treated  x Non-disp :  delta^B_l
    #   Treated  x Displaced:  delta^B_l + beta_l + delta^D_l
    #
    # Triple-difference:
    #   delta^D_l = (Treated-Disp - Treated-NonDisp)
    #             - (Control-Disp - Control-NonDisp)
    #
    # Pre-trend tests:
    #   delta^B_l = 0 for l < -1  ->  baseline parallel trends
    #   delta^D_l = 0 for l < -1  ->  displacement parallel trends
    # ------------------------------------------------------------------
    spec    = "event_binary_B"
    formula = (
        f"{outcome} ~ "
        f"i(rel_t, treated,       ref=-1) + "
        f"i(rel_t, treated_X_disp, ref=-1) + "
        f"i(rel_t, disp_binary,   ref=-1) "
        f"| {fe_str}"
    )
    fit = pf.feols(formula, data=df, vcov=vcov)
    fit_rows.append(_fit_row(fit, spec, formula))
    # delta^B_l : terms ending ":treated"        (NOT ":treated_X_disp")
    rows.extend(_tidy_rows_suffix(fit, ":treated",        spec))
    # delta^D_l : terms ending ":treated_X_disp"
    rows.extend(_tidy_rows_suffix(fit, ":treated_X_disp", spec))
    # beta_l    : terms ending ":disp_binary"
    rows.extend(_tidy_rows_suffix(fit, ":disp_binary",    spec))
    pre_rows.append(_joint_zero_test(
        fit       = fit,
        terms     = _pre_period_terms(fit.tidy().index, pre_periods, ":treated"),
        spec      = spec,
        test_name = "pretrend_baseline_joint_zero",
    ))
    pre_rows.append(_joint_zero_test(
        fit       = fit,
        terms     = _pre_period_terms(fit.tidy().index, pre_periods, ":treated_X_disp"),
        spec      = spec,
        test_name = "pretrend_displacement_joint_zero",
    ))

    # ------------------------------------------------------------------
    # Spec D: Closure-length heterogeneity
    #
    # Augments Spec B with interactions involving L_tilde_e:
    #
    # y_{iet} = [Spec B terms]
    #         + sum_{l!=-1} kappa_l * 1(t=l) * treated_{ie} * L_tilde_e
    #         + sum_{l!=-1} theta_l * 1(t=l) * treated_{ie} * D_{ie} * L_tilde_e
    #         + [lower-order: l * disp * len]
    #         + phi_{ie} + omega_t + gamma_m + nu_{iet}
    #
    # All lower-order interactions involving L_tilde_e are included:
    #   i(rel_t, disp_X_len,    ref=-1)  : 1(t=l) x D x L_tilde
    #   i(rel_t, treated_X_len, ref=-1)  : 1(t=l) x treated x L_tilde  (kappa)
    #   i(rel_t, tXdXlen,       ref=-1)  : 1(t=l) x treated x D x L_tilde (theta)
    #
    # The main effects of L_tilde_e and treated*L_tilde_e are absorbed by
    # event_fe_id; theta_l and kappa_l are identified only through their
    # interaction with the time-varying rel_t dummies.
    #
    # Interpretation:
    #   delta^D_l : displacement effect at mean closure length (L_tilde=0)
    #   theta_l   : change in displacement effect per 1-SD longer closure
    #   kappa_l   : change in baseline effect per 1-SD longer closure
    #
    # Pre-trend tests:
    #   theta_l = 0 for l < -1  ->  length x displacement falsification
    #   kappa_l = 0 for l < -1  ->  length x baseline falsification
    # ------------------------------------------------------------------
    spec    = "event_binary_D"
    formula = (
        f"{outcome} ~ "
        f"i(rel_t, treated,        ref=-1) + "
        f"i(rel_t, treated_X_disp, ref=-1) + "
        f"i(rel_t, disp_binary,    ref=-1) + "
        f"i(rel_t, treated_X_len,  ref=-1) + "
        f"i(rel_t, disp_X_len,     ref=-1) + "
        f"i(rel_t, tXdXlen,        ref=-1) "
        f"| {fe_str}"
    )
    fit = pf.feols(formula, data=df, vcov=vcov)
    fit_rows.append(_fit_row(fit, spec, formula))
    rows.extend(_tidy_rows_suffix(fit, ":treated",        spec))   # delta^B_l
    rows.extend(_tidy_rows_suffix(fit, ":treated_X_disp", spec))   # delta^D_l
    rows.extend(_tidy_rows_suffix(fit, ":disp_binary",    spec))   # beta_l
    rows.extend(_tidy_rows_suffix(fit, ":treated_X_len",  spec))   # kappa_l
    rows.extend(_tidy_rows_suffix(fit, ":disp_X_len",     spec))   # lower-order
    rows.extend(_tidy_rows_suffix(fit, ":tXdXlen",        spec))   # theta_l
    pre_rows.append(_joint_zero_test(
        fit       = fit,
        terms     = _pre_period_terms(fit.tidy().index, pre_periods, ":tXdXlen"),
        spec      = spec,
        test_name = "pretrend_length_displacement_joint_zero",
    ))
    pre_rows.append(_joint_zero_test(
        fit       = fit,
        terms     = _pre_period_terms(fit.tidy().index, pre_periods, ":treated_X_len"),
        spec      = spec,
        test_name = "pretrend_length_baseline_joint_zero",
    ))

    # ------------------------------------------------------------------
    # Spec C: Continuous displacement-score DDD
    #
    # y_{iet} = sum_{l!=-1} delta^B_l * 1(t=l) * treated_{ie}
    #         + sum_{l!=-1} delta^S_l * 1(t=l) * treated_{ie} * s_tilde_{ie}
    #         + sum_{l!=-1} beta^S_l  * 1(t=l) * s_tilde_{ie}
    #         + phi_{ie} + omega_t + gamma_m + nu_{iet}
    #
    # s_tilde_{ie} = displacement_prob_centered is already mean-centered,
    # so delta^B_l is the treatment effect at the average propensity.
    #
    # Interpretation:
    #   delta^B_l : baseline-demand effect at mean propensity (l > 0)
    #   delta^S_l : marginal displacement effect per unit of s_tilde (l > 0)
    #               total effect for consumer with s_tilde = v:
    #                   delta^B_l + v * delta^S_l
    #   beta^S_l  : propensity-purchase relationship pooled across groups
    #
    # Pre-trend tests:
    #   delta^B_l = 0 for l < -1  ->  baseline parallel trends
    #   delta^S_l = 0 for l < -1  ->  score-slope falsification
    #               (non-zero pre-period slope indicates the score is
    #                picking up pre-existing purchase dynamics, not
    #                a displacement effect)
    # ------------------------------------------------------------------
    spec    = "event_score_C"
    formula = (
        f"{outcome} ~ "
        f"i(rel_t, treated,                   ref=-1) + "
        f"i(rel_t, treated_X_score,           ref=-1) + "
        f"i(rel_t, displacement_prob_centered, ref=-1) "
        f"| {fe_str}"
    )
    fit = pf.feols(formula, data=df, vcov=vcov)
    fit_rows.append(_fit_row(fit, spec, formula))
    rows.extend(_tidy_rows_suffix(fit, ":treated",                   spec))  # delta^B_l
    rows.extend(_tidy_rows_suffix(fit, ":treated_X_score",           spec))  # delta^S_l
    rows.extend(_tidy_rows_suffix(fit, ":displacement_prob_centered", spec)) # beta^S_l
    pre_rows.append(_joint_zero_test(
        fit       = fit,
        terms     = _pre_period_terms(fit.tidy().index, pre_periods, ":treated"),
        spec      = spec,
        test_name = "pretrend_score_baseline_joint_zero",
    ))
    pre_rows.append(_joint_zero_test(
        fit       = fit,
        terms     = _pre_period_terms(fit.tidy().index, pre_periods, ":treated_X_score"),
        spec      = spec,
        test_name = "pretrend_score_slope_joint_zero",
    ))

    return pd.DataFrame(rows), pd.DataFrame(fit_rows), pd.DataFrame(pre_rows)
