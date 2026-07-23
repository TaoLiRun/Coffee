# Headline Coefficient Interpretation Audit

## Bottom line

The paper's headline coefficient is currently misdescribed.

In the pooled triple-differences regression, the coefficient
\(\delta^D\) is the **difference between the high- and low-predicted-incidence
treatment effects**. It is not, by itself, the treatment effect for
high-predicted-incidence customers.

For the main member-first novelty outcome, the three relevant quantities are:

| Quantity | Definition | Estimate | SE | p-value | 95% CI |
|---|---|---:|---:|---:|---:|
| Low-predicted-incidence closure effect | \(\delta^B\) | 0.0313 | 0.0120 | 0.009 | [0.0078, 0.0548] |
| High-predicted-incidence closure effect | \(\delta^B+\delta^D\) | -0.0102 | 0.0083 | 0.217 | [-0.0264, 0.0060] |
| High-minus-low differential | \(\delta^D\) | -0.0415 | 0.0145 | 0.004 | [-0.0699, -0.0131] |

Therefore, the defensible headline is:

> The post-reopening closure response in novelty-seeking is 4.15 percentage
> points lower for high- than for low-predicted-incidence episodes. Under the
> identifying assumption described below, this differential is attributable to
> the additional consequence of interrupting a likely purchase.

It is not correct to say:

> Treated high-intention consumers become 4.15 percentage points less likely
> to try a new product because of the closure.

The direct estimated closure effect for that high group is \(-1.02\) percentage
points, and it is not statistically distinguishable from zero at conventional
levels.

This note records the evidence, why the distinction matters, how the related
paper handles it, and the coding and writing changes needed to correct it. It
does not implement those changes.

## 1. The issue in plain language

The regression asks two related questions:

1. How does the outcome change for treated customers classified as having a
   low probability of purchasing during the closure?
2. How much larger or smaller is the treated response among customers
   classified as having a high probability of purchasing?

The first answer is \(\delta^B\). The second answer is \(\delta^D\).
Consequently, the effect for the high group is the sum:

\[
\text{high-group effect}=\delta^B+\delta^D.
\]

For novelty-seeking:

\[
\underbrace{-0.0102}_{\text{high-group effect}}
=
\underbrace{0.0313}_{\text{low-group effect}}
+
\underbrace{(-0.0415)}_{\text{high-minus-low differential}}.
\]

In words, the low group has an estimated 3.13-point increase, while the high
group has an estimated 1.02-point decrease. The gap between those responses is
4.15 points. Calling the 4.15-point gap the high-group effect omits the
low-group increase that must be included to obtain the high-group total.

An analogy makes the error clear. If one group gains 3 units and another loses
1 unit, the second group changes by \(-1\), while its change is 4 units lower
than the first group's. “Lost 1” and “did 4 worse than the other group” are not
the same claim.

## 2. Regression algebra

The paper estimates:

\[
Y_{iet}
=
\delta^B(\text{Post}\times\text{Treated})
+
\beta(\text{Post}\times\text{High})
+
\delta^D(\text{Post}\times\text{Treated}\times\text{High})
+
\text{fixed effects}
+
\varepsilon_{iet}.
\]

The treatment-versus-control post change within each predicted-incidence group
is:

| Predicted-incidence group | Treated-control post contrast |
|---|---:|
| Low (\(\text{High}=0\)) | \(\delta^B\) |
| High (\(\text{High}=1\)) | \(\delta^B+\delta^D\) |
| High minus low | \(\delta^D\) |

The coefficient \(\beta\) is not a treatment effect. It is the high-minus-low
post shift common to the treated and control arms. With episode fixed effects,
it also should not be described as an “overall level difference” between high-
and low-predicted-incidence customers.

## 3. Evidence in the manuscript and code

### 3.1 The equation and table already contain the correct decomposition

The equation in `writeup/main.tex:665-674` defines:

- `Post × Treated` as \(\delta^B\);
- `Post × Intent` as \(\beta\);
- `Post × Treated × Intent` as \(\delta^D\).

Table 3 at `writeup/main.tex:699-721` also reports:

- novelty \(\delta^B=0.0313\);
- novelty \(\delta^D=-0.0415\);
- the implied high-group effect
  \(\delta^B+\delta^D=-0.0102\).

Thus, the table's arithmetic already demonstrates that \(-0.0415\) is not the
high-group total.

### 3.2 The surrounding prose changes the estimand

The interpretation becomes incorrect in the results prose:

- `writeup/main.tex:728` says the purchase-frequency triple interaction
  indicates the change of treated high-intention customers relative to
  high-intention controls. That direct contrast is \(0.0067\), not \(0.0058\).
- `writeup/main.tex:736` says the novelty triple interaction means treated
  high-intention consumers become 4.15 points less likely to try new products
  relative to comparable high-intention controls. That direct contrast is
  \(-1.02\) points, not \(-4.15\) points.
- The “4.1 percentage point decline” in `writeup/main.tex:283`, along with the
  abstract and conclusion, inherits the same error when it is presented as a
  decline *for high-intention customers* rather than as a high-minus-low
  differential.

The interpretation in `writeup/main.tex:674`—“the additional post-reopening
effect”—is closer to correct. The problem is that later sentences silently
replace “additional relative to the low group” with “the total effect for the
high group.”

### 3.3 The implementation confirms the algebra

`src/displacement_effect_estimation/specs.py:239-248` documents the implemented
binary model, and `src/displacement_effect_estimation/specs.py:271-305`
constructs:

```python
post_X_treated = post * treated
post_X_disp = post * disp_binary
post_X_treated_X_disp = post * treated * disp_binary
```

The saved coefficient files report:

| Outcome | \(\delta^B\) | \(\delta^D\) | \(\delta^B+\delta^D\) |
|---|---:|---:|---:|
| Purchase frequency | 0.000892 | 0.005829 | 0.006721 |
| Member-first novelty | 0.031290 | -0.041489 | -0.010199 |
| First-observed-sale novelty | 0.008046 | -0.041717 | -0.033671 |

The paper-table generator at
`scripts/writeup/generate_paper_exhibits.py:87-113` currently computes the
high-group row as a bare arithmetic sum but does not obtain its covariance-aware
standard error. This makes the table visually emphasize the triple interaction
while leaving the actual high-group effect without uncertainty.

## 4. How the related paper handles the same estimate

The reference paper uses the same decomposition.

At
`literature/Levine-Hristakeva - Stopping Shopping at Stop and Shop How Temporary Disruptions Affect Store Choice.md:199-244`,
it first describes four cells:

- treated and predicted displaced;
- treated and predicted non-displaced;
- control and predicted displaced;
- control and predicted non-displaced.

It then explains that:

- the non-displaced difference-in-differences captures the baseline-demand
  response;
- the displaced difference-in-differences contains the baseline-demand
  response plus the displacement response;
- subtracting the first from the second identifies the displacement component
  if baseline-demand effects are comparable.

Most importantly, at line 244 the reference calls \(\delta^D\) the
**difference in ATTs between displaced and non-displaced households**. It does
not call \(\delta^D\) the ATT for displaced households.

The reference separates the empirical quantities across two tables:

- Table 4 reports subgroup ATTs from separate regressions:
  - displaced ATT: \(-0.1451\), SE \(0.0304\);
  - non-displaced ATT: \(0.0538\), SE \(0.0152\).
- Table 5 reports the unified DDD:
  - non-displaced/baseline ATT: \(0.0538\), SE \(0.0152\);
  - displaced-minus-non-displaced DDD: \(-0.1989\), SE \(0.0340\).

These numbers obey:

\[
-0.1451-0.0538=-0.1989.
\]

The reference therefore gives uncertainty for its displaced-group ATT through
the separate subgroup regression. It does **not** add a
\(\delta^B+\delta^D\) row with a covariance-based standard error in its unified
DDD table.

### Implication for this paper

A covariance-aware standard error for the high-group sum is not required merely
to imitate the reference. It is required if this paper chooses to display and
interpret the sum as an estimate. Every displayed estimate used for a
substantive claim should have uncertainty.

There are two defensible presentation choices:

1. **Preferred:** retain the pooled DDD and report the low effect, high effect,
   and high-minus-low differential, each with an SE or confidence interval.
   This keeps all three quantities tied to one estimation sample and one
   weighting scheme.
2. **Closer to the reference:** report low- and high-group DiDs from separate
   regressions, with their SEs, and report the pooled DDD separately. In this
   paper's unbalanced, purchase-conditional novelty sample, separate subgroup
   regressions need not reproduce the pooled-model linear combination exactly,
   so the source of any difference would need to be explained.

For that reason, the first option is cleaner here.

## 5. What causal assumption is actually needed?

The formal label “equal-baseline-response assumption” is not self-explanatory.
The paper should state the identifying logic in ordinary language before giving
it a short formal name.

A reader-facing version is:

> A closure may affect customers for general reasons even when it does not
> interrupt a likely purchase—for example, by changing convenience,
> promotions, substitution opportunities, or perceptions of the store. The
> low-predicted-incidence comparison is intended to capture these general
> closure effects. The high-predicted-incidence comparison contains the same
> general effects plus the consequence of interrupting a likely purchase. If
> the general closure effects would otherwise have been similar for the two
> groups, subtracting the low-group response from the high-group response
> isolates the additional response associated with the interruption.

A concise heading can then call this the:

> **Comparable general closure effects assumption**

The formal condition is that, absent the purchase interruption, the closure's
general treatment effect would be the same for the high- and low-predicted-
incidence groups. This condition is distinct from ordinary treated-control
parallel trends.

The causal statement must remain conditional:

> Under parallel triple trends and comparable general closure effects, the
> 4.15-point high-minus-low differential identifies the incremental response
> associated with interrupting a likely purchase.

Even this statement should use “predicted purchase incidence” or “likely
purchase” rather than asserting that the classifier directly observes a
psychological purchase intention.

## 6. Coding fix

No code should be changed until the table design is chosen. Once chosen, the
following implementation keeps the existing coefficient and adds exact
uncertainty for the low- and high-group effects.

### 6.1 Keep the existing parameterization for the DDD

The current model is useful because
`post_X_treated_X_disp` directly estimates the high-minus-low differential.
Retain it and label its output explicitly:

```text
low_intention_att
high_minus_low_ddd
common_high_post_shift
```

Do not label `post_X_treated_X_disp` as `high_intention_att`.

### 6.2 Fit an algebraically equivalent parameterization for group effects

Inside `fit_collapsed_specs()` in
`src/displacement_effect_estimation/specs.py`, construct:

```python
df["post_X_treated_X_low"] = (
    df["post"] * df["treated"] * (1 - df["disp_binary"])
)
df["post_X_treated_X_high"] = (
    df["post"] * df["treated"] * df["disp_binary"]
)

group_formula = (
    f"{outcome} ~ "
    "post_X_treated_X_low + post_X_disp + post_X_treated_X_high"
    f" | {fe_str}"
)
group_fit = pf.feols(group_formula, data=df, vcov=vcov)
```

This is not a new empirical specification. It spans the same regressors as the
existing model:

\[
\text{Post}\times\text{Treated}
=
\text{Post}\times\text{Treated}\times\text{Low}
+
\text{Post}\times\text{Treated}\times\text{High}.
\]

Under this parameterization:

- `post_X_treated_X_low` estimates \(\delta^B\);
- `post_X_treated_X_high` estimates \(\delta^B+\delta^D\);
- both coefficients receive their correct SEs, p-values, and confidence
  intervals directly from `group_fit.tidy()`.

The original fit still supplies \(\delta^D\) and its SE.

An equally valid implementation is a linear hypothesis on the original fit:

\[
\operatorname{Var}(\widehat{\delta^B+\delta^D})
=
\operatorname{Var}(\widehat{\delta^B})
+
\operatorname{Var}(\widehat{\delta^D})
+
2\operatorname{Cov}(\widehat{\delta^B},\widehat{\delta^D}).
\]

The equivalent parameterization is recommended because it uses the public
`tidy()` output and avoids hand-indexing a covariance matrix.

### 6.3 Preserve confidence intervals in exported results

Extend `_tidy_row()` and the equivalent group-effect extractor to retain the
lower and upper confidence-limit columns returned by `fit.tidy()`. Export a
long-form result with fields such as:

```text
outcome
estimand
term
coef
se
pvalue
ci_low
ci_high
n
r2_within
cluster_variable
number_of_clusters
```

The exhibit generator should read this estimand-level file. It should never
reconstruct the high effect from two rounded numbers.

### 6.4 Generate the table rather than pasting it

Revise `scripts/writeup/generate_paper_exhibits.py` so the main table has:

**Panel A. Closure effects within predicted-incidence group**

- low-predicted-incidence effect, with SE;
- high-predicted-incidence effect, with SE.

**Panel B. Incremental interruption contrast**

- high-minus-low DDD, with SE.

Move \(\beta\), the common high-group post shift, to a decomposition appendix
unless it is needed in the main text.

Write the result to a versioned `.tex` file and include it in the paper with
`\input{}`. The existing behavior of printing LaTeX to standard output leaves
too much room for stale manual values.

### 6.5 Add invariance checks

The run script should fail unless:

```python
assert np.isclose(low_coef, delta_b)
assert np.isclose(high_coef, delta_b + delta_d)
assert group_fit._N == original_fit._N
```

It should also check that the paper-facing output includes an SE and CI for
every reported effect row.

For the current results, the checks should recover:

| Outcome | High effect | SE | p-value |
|---|---:|---:|---:|
| Purchase frequency | 0.006721 | 0.002434 | 0.0058 |
| Member-first novelty | -0.010199 | 0.008256 | 0.2167 |
| First-observed-sale novelty | -0.033671 | 0.006920 | \(<0.001\) |

These values should be regenerated after any change to clustering, sample
construction, or outcome scope.

## 7. Writing fix

### 7.1 Main novelty result

Replace the current interpretation with language like:

> Among low-predicted-incidence episodes, the estimated post-reopening closure
> effect on novelty-seeking is an increase of 3.13 percentage points
> (SE 1.20). Among high-predicted-incidence episodes, the corresponding effect
> is a decrease of 1.02 points (SE 0.83; \(p=0.217\)). The high-group response is
> therefore 4.15 points lower than the low-group response (SE 1.45;
> \(p=0.004\)). Under parallel triple trends and the assumption that general
> closure effects would otherwise be comparable across the two predicted-
> incidence groups, this differential is the estimate of the incremental
> response associated with interrupting a likely purchase.

This wording reports the direct high-group effect honestly while preserving
the DDD as the mechanism-relevant estimand.

### 7.2 Main purchase-frequency result

Use the same structure:

> The estimated closure effect on purchase frequency is 0.09 percentage points
> per calendar day for low-predicted-incidence episodes and 0.67 points for
> high-predicted-incidence episodes. The latter is 0.58 points larger than the
> former. Because the high-minus-low purchase pretrend rejects, this estimate is
> descriptive/supporting rather than the paper's cleanest causal evidence.

Report the SE or CI for all three numbers.

### 7.3 Abstract, introduction, and conclusion

Do not write that high-intention customers have a significant 4.15-point
decline. Write:

> The post-reopening novelty response is 4.15 percentage points lower among
> customers with high rather than low predicted purchase incidence.

If space permits, immediately add:

> The direct high-group effect is a 1.02-point decline and is imprecisely
> estimated.

The abstract should not imply that the DDD establishes a large, statistically
significant absolute decline for the high group.

### 7.4 Terminology

Use a stable vocabulary:

| Current terms | Recommended term |
|---|---|
| intent, intention, active goal, propensity | predicted purchase incidence |
| high intention | high predicted purchase incidence |
| low intention | low predicted purchase incidence |
| blocked-intention effect | incremental interruption contrast |
| displacement effect | high-minus-low DDD, followed by the causal interpretation and assumptions |

“Blocked” should describe treated high-predicted-incidence episodes only.
Control high-predicted-incidence episodes provide a counterfactual but do not
experience a blocked store opportunity.

## 8. Scope of the correction

The interpretation should be corrected consistently in:

- `writeup/main.tex`;
- `scripts/writeup/generate_paper_exhibits.py`;
- `src/displacement_effect_estimation/specs.py` output labels and docstrings;
- `reports/main_results.qmd`;
- `README/econometric_specification.md`;
- `docs/technical_report.md`;
- any abstract, slide, or README that calls the triple interaction the
  high-group treatment effect.

The numerical results need not change solely because the interpretation is
fixed. The displayed table, its uncertainty rows, and the causal language do
need to change.

## 9. Acceptance criteria

The issue is resolved only when all of the following are true:

- \(\delta^D\) is consistently called a high-minus-low treatment-effect
  differential.
- \(\delta^B+\delta^D\) is consistently called the high-group treatment
  effect.
- Every displayed effect has an SE or confidence interval.
- The abstract, introduction, results, and conclusion use the same estimand.
- The causal interpretation is explicitly conditional on parallel triple
  trends and comparable general closure effects.
- \(\beta\) is described as a common high-minus-low post shift, not a treatment
  effect or a time-invariant level difference.
- Generated paper artifacts, code labels, and prose agree.
