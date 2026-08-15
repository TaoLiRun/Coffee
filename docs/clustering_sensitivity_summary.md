# Closure-event versus consumer-clustered inference audit

**Audit date:** 2026-08-14
**Manuscript:** `writeup/main.tex`
**Branch and audited commit:** `issue-4/further-selection`, `198e64f`
**Preferred manuscript inference:** CRV1 standard errors clustered by 18 closure events

## Bottom line

Several customer-level results in the manuscript can mechanically be reported with either closure-event or consumer clustering. The previously missing consumer-cluster counterparts have now been estimated on `mktserver` and copied into:

```text
outputs/06_inference_sensitivity/consumer_cluster/
```

The new bundle covers the complete baseline-novelty heterogeneity exercise, new-product notifications, customer return timing and personally novel opportunity, non-coffee novelty and sample entry, cafe-density specifications, and all three raw-path confidence-interval datasets. It also contains a freshly re-estimated purchase-frequency core bundle. Older consumer-cluster counterparts for the remaining core DDD, score, event-study, pretrend, and matched/common-support specifications remain recoverable from commit `8cba55a`.

No applicable customer-level result family identified in this audit now lacks a consumer-cluster counterpart. Store-week assortment results remain correctly classified as not applicable because consumer ID is not a dimension of those datasets. Consumer-level restricted wild-bootstrap p-values were not generated; they are neither required for CRV1 consumer clustering nor directly comparable to the manuscript's restricted bootstrap over 18 common closure shocks.

The closure-event specification should remain primary. Treatment is a common store-closure shock, and customers within a closure can share unobserved shocks. Consumer clustering treats different customers as independent clusters and therefore does not address this closure-level dependence. It is useful as a sensitivity calculation, not as a substitute for the design-aligned closure clustering.

## How the code clusters and obtains p-values

The production setting is in `src/displacement_effect_estimation/config.json`:

```json
"cluster_col": "closure_event_id"
```

The main estimator passes this to PyFixest as:

```python
vcov = {"CRV1": cluster_col}
fit = pf.feols(formula, data=df, vcov=vcov)
```

This is implemented in `src/displacement_effect_estimation/specs.py`. Coefficient estimates, standard errors, two-sided p-values, and confidence limits are copied from `fit.tidy()`, especially its `Pr(>|t|)` column. With closure clustering, the coefficient p-values correspond to a cluster-based t reference with 17 degrees of freedom; with consumer clustering, the very large number of clusters makes the reference distribution practically normal.

The main event-study joint pretrend tests are different. They call `fit.wald_test(R=R)` and save the returned p-value. In the current PyFixest path this is an asymptotic chi-square Wald test; it is not an F test with 17 denominator degrees of freedom. Thus changing the cluster variable changes the covariance matrix used by the Wald statistic, but the saved joint p-value is still based on the asymptotic chi-square reference distribution.

Some newer appendix scripts add small-cluster inference. The notification, non-coffee, assortment, and cafe-density analyses report restricted Rademacher wild-cluster p-values using closure events. Those p-values do not have a directly analogous “consumer-cluster” interpretation unless the bootstrap is also redesigned to resample consumer clusters. The new sensitivity bundle therefore reports consumer-cluster CRV1 inference and retains the manuscript's closure wild-bootstrap results as the appropriate small-shock comparison.

The reproducible sensitivity runner is `scripts/writeup/run_consumer_cluster_sensitivity.py`. It reads locked production samples or saved analysis panels, changes the CRV1 cluster passed to the estimator to `member_id`, and writes to the isolated sensitivity directory without overwriting paper-facing outputs.

## Results for which both cluster variants are available

All coefficients below use the same specification and sample across the two columns. Only the covariance estimator and resulting inference change. The purchase-frequency results were freshly re-estimated into the new sensitivity bundle. The remaining core consumer results are recoverable from commit `8cba55a` and are summarized here without overwriting the current closure-cluster files.

### Main binary DDD decomposition

| Outcome and estimand | Coefficient | Closure-cluster SE | Closure p | Consumer-cluster SE | Consumer p |
|---|---:|---:|---:|---:|---:|
| Purchase frequency: low-intention effect | 0.0009 | 0.0024 | 0.711 | 0.0007 | 0.180 |
| Purchase frequency: high-intention effect | 0.0067 | 0.0045 | 0.152 | 0.0024 | 0.006 |
| Purchase frequency: high-minus-low DDD | 0.0058 | 0.0032 | 0.086 | 0.0025 | 0.021 |
| Member-first novelty: low-intention effect | 0.0313 | 0.0178 | 0.098 | 0.0120 | 0.009 |
| Member-first novelty: high-intention effect | -0.0102 | 0.0072 | 0.175 | 0.0083 | 0.217 |
| Member-first novelty: high-minus-low DDD | -0.0415 | 0.0184 | 0.038 | 0.0145 | 0.004 |
| Market-new novelty: low-intention effect | 0.0080 | 0.0113 | 0.487 | 0.0092 | 0.380 |
| Market-new novelty: high-intention effect | -0.0337 | 0.0145 | 0.033 | 0.0069 | <0.001 |
| Market-new novelty: high-minus-low DDD | -0.0417 | 0.0089 | <0.001 | 0.0115 | <0.001 |

The purchase-frequency sample has 321,184 observations, 18 closure clusters, and 40,148 consumer clusters. Both novelty samples have 99,644 observations, 18 closure clusters, and 23,363 contributing consumer clusters after outcome-missingness and singleton handling.

The main substantive change is inferential rather than numerical. Under consumer clustering, the purchase high-group contrast and purchase DDD cross the 5% threshold, and the low-group member-first novelty contrast crosses the 1% threshold. The member-first novelty DDD is significant under both methods but has a smaller p-value with consumer clustering. The market-new novelty DDD is highly significant under both.

### Continuous predicted-intention score

| Outcome: `Post x Treated x score` | Coefficient | Closure-cluster SE | Closure p | Consumer-cluster SE | Consumer p |
|---|---:|---:|---:|---:|---:|
| Purchase frequency | 0.0076 | 0.0051 | 0.152 | 0.0037 | 0.040 |
| Member-first novelty | -0.0452 | 0.0276 | 0.120 | 0.0221 | 0.040 |
| Market-new novelty | -0.0486 | 0.0156 | 0.006 | 0.0175 | 0.005 |

Consumer clustering moves the purchase and member-first novelty score interactions from insignificant to significant at 5%. The market-new score result remains significant under both; in this case its consumer-clustered SE is slightly larger.

### Joint pretrend tests

These are the saved asymptotic Wald p-values described above.

| Outcome and DDD diagnostic | Closure-cluster p | Consumer-cluster p |
|---|---:|---:|
| Purchase frequency, binary high-minus-low leads | 0.0347 | 0.0025 |
| Purchase frequency, score-slope leads | 0.0504 | 0.0068 |
| Member-first novelty, binary high-minus-low leads | 0.8407 | 0.7973 |
| Member-first novelty, score-slope leads | 0.6190 | 0.7781 |
| Market-new novelty, binary high-minus-low leads | 0.1140 | 0.5150 |
| Market-new novelty, score-slope leads | 0.3771 | 0.7209 |

The qualitative diagnostic conclusion is stable: purchase-frequency dynamics fail or are borderline, while the two novelty measures do not show a rejected focal DDD pretrend. The numerical p-values are nevertheless cluster-dependent.

### Matched/common-support DDDs

| Outcome | Coefficient | Closure-cluster SE | Closure p | Consumer-cluster SE | Consumer p |
|---|---:|---:|---:|---:|---:|
| Purchase frequency | -0.0041 | 0.0027 | 0.156 | 0.0034 | 0.237 |
| Member-first novelty | -0.0211 | 0.0195 | 0.295 | 0.0217 | 0.331 |

Both matched estimates remain insignificant under either method. Consumer-clustered event-study and matched-pretrend files also exist in commit `8cba55a`, although no current consumer-sensitivity copy is preserved.

## Baseline-novelty heterogeneity

The complete adjusted and unadjusted specifications, including their event studies and pretrend tests, are now saved under `baseline_novelty_heterogeneity/`.

| Specification and focal coefficient | Coefficient | Closure SE | Closure two-sided p | Closure one-sided p | Consumer SE | Consumer two-sided p | Consumer one-sided p |
|---|---:|---:|---:|---:|---:|---:|---:|
| With baseline-order adjustment | 0.0294 | 0.0147 | 0.0625 | 0.0312 | 0.0160 | 0.0664 | 0.0332 |
| Without baseline-order adjustment | 0.0229 | 0.0143 | 0.1273 | 0.0636 | 0.0152 | 0.1318 | 0.0659 |

Both use 79,578 observations. The consumer-cluster fits have 16,459 contributing clusters after fixed-effect singleton removal. The adjusted heterogeneity result retains essentially the same directional significance, while the unadjusted result remains just above the 5% one-sided threshold.

The adjusted joint pretrend p-value changes from 0.5611 with closure clustering to 0.7193 with consumer clustering. The unadjusted pretrend p-value changes from 0.4094 to 0.6628. Thus the heterogeneity conclusion is stable across the two covariance choices.

## Newly completed appendix counterparts

### New-product notifications

| Focal exposure contrast | Coefficient | Closure SE | Closure CRV1 p | Closure wild p | Consumer SE | Consumer CRV1 p |
|---|---:|---:|---:|---:|---:|---:|
| During versus all pre-periods | 0.0041 | 0.0011 | 0.0012 | 0.0032 | 0.0009 | <0.001 |
| During versus period -1 | 0.0043 | 0.0013 | 0.0043 | 0.0111 | 0.0009 | <0.001 |
| Post versus pre-periods | 0.0017 | 0.0007 | 0.0343 | 0.0469 | 0.0007 | 0.0249 |

The coefficients count new-product campaigns per consumer-day. All signs remain positive, so consumer clustering strengthens rather than changes the manuscript's conclusion that recorded notification exposure has the wrong sign to explain the negative novelty DDD. The focal dynamic pretrend p-value is 0.500 under the manuscript's closure-cluster F test and 0.665 under consumer clustering.

### Return timing and personally novel opportunity

| Result | Coefficient | Closure SE | Closure p | Consumer SE | Consumer p |
|---|---:|---:|---:|---:|---:|
| Days to first return, high minus low | -2.8724 | 0.2936 | <0.001 | 0.3266 | <0.001 |
| Timing deviation: novel-product share | -0.0010 | 0.0006 | 0.0930 | 0.0005 | 0.0517 |
| Timing deviation: novel-product count | -0.2756 | 0.3848 | 0.4836 | 0.1995 | 0.1673 |

The share contrast becomes borderline at 5%, but its coefficient is unchanged and remains only about one-fortieth of the main novelty DDD. The count contrast remains insignificant. Because each returning consumer contributes one regression row, clustering by consumer is close to a heteroskedasticity-robust calculation.

### Non-coffee novelty and sample entry

| Outcome | Coefficient | Closure SE | Closure CRV1 p | Closure pretrend p | Consumer SE | Consumer p | Consumer pretrend p |
|---|---:|---:|---:|---:|---:|---:|---:|
| All non-coffee novelty | -0.0413 | 0.0340 | 0.242 | 0.006 | 0.0267 | 0.122 | 0.112 |
| Non-coffee consumables novelty | -0.0411 | 0.0339 | 0.242 | 0.006 | 0.0267 | 0.124 | 0.107 |
| Non-coffee beverages novelty | -0.0626 | 0.0412 | 0.147 | 0.226 | 0.0323 | 0.053 | 0.187 |
| Any all-non-coffee purchase | -0.0170 | 0.0100 | 0.107 | 0.093 | 0.0082 | 0.038 | 0.135 |
| Any non-coffee-consumables purchase | -0.0175 | 0.0101 | 0.102 | 0.088 | 0.0082 | 0.033 | 0.128 |
| Any non-coffee-beverage purchase | -0.0224 | 0.0090 | 0.023 | 0.121 | 0.0073 | 0.002 | 0.281 |

Consumer clustering makes the conditional beverage-novelty estimate borderline and the sample-entry estimates more precise. More importantly, it no longer rejects the all-non-coffee and consumables pretrends. This is not a reason to replace the manuscript conclusion: the common treatment variation remains at the closure level, so the closure-cluster pretrend failures are the design-aligned diagnostics and the exercise should remain a sensitivity check.

The contributing consumer clusters after outcome missingness and fixed-effect singleton removal are 9,824 for all non-coffee novelty, 9,818 for consumables novelty, 7,308 for beverage novelty, and 40,148 for each entry regression.

### Cafe-density specifications

| Specification or fitted point | Coefficient | Closure SE | Closure CRV1 p | Consumer SE | Consumer p |
|---|---:|---:|---:|---:|---:|
| Raw 500m count, member-event mean | -0.0333 | 0.0143 | 0.0328 | 0.0155 | 0.0316 |
| Log 500m count, member-event mean | -0.0392 | 0.0176 | 0.0402 | 0.0145 | 0.0069 |
| Raw 1,500m count, member-event mean | -0.0404 | 0.0164 | 0.0251 | 0.0147 | 0.0061 |
| Log 1,500m count, member-event mean | -0.0411 | 0.0159 | 0.0192 | 0.0147 | 0.0052 |
| Raw 500m fitted DDD at count 2 | -0.0503 | 0.0315 | 0.1287 | 0.0191 | 0.0086 |
| Raw 500m fitted DDD at count 5 | -0.0439 | 0.0242 | 0.0872 | 0.0157 | 0.0051 |
| Raw 500m fitted DDD at count 13 | -0.0270 | 0.0125 | 0.0458 | 0.0187 | 0.1478 |
| Change in DDD per SD of raw 500m density | 0.0300 | 0.0386 | 0.4485 | 0.0311 | 0.3358 |
| Low-density sample, count <=3 | -0.0539 | 0.0365 | 0.1608 | 0.0224 | 0.0161 |
| Preferred-store-event-post fixed effects | -0.0445 | 0.0171 | 0.0188 | 0.0149 | 0.0028 |

The density gradient remains insignificant under both covariance choices. Point-specific precision changes substantially: consumer clustering favors the low-density fitted points, while closure clustering favors the count-13 point. The density-gradient dynamic pretrend p-value changes from 0.0023 with closure clustering to 0.2195 with consumer clustering. Because local density and closure exposure are organized at store/event levels, the closure-cluster warning remains the relevant one for causal interpretation.

### Raw customer-path confidence intervals

Consumer-cluster CRV1 means, SEs, and 95% confidence intervals are now saved for:

- closure-shock purchase-frequency paths, including a reconstructed period 0;
- novelty paths by treatment and predicted-intention group; and
- purchase-probability paths by treatment and predicted-intention group.

Every plotted mean exactly matches its closure-cluster source. Only the uncertainty intervals change. The sensitivity runner saves the numerical path data and does not replace the manuscript's closure-cluster figures.

## Coverage audit of all manuscript inference

| Manuscript result or exhibit | Observation level | Could consumer clustering be run? | Consumer counterpart status |
|---|---|---|---|
| Raw closure-shock purchase-frequency confidence intervals | Consumer-period | Yes | Completed under `raw_paths/`; the manuscript figure remains closure clustered |
| Raw novelty-path confidence intervals | Consumer-period | Yes | Completed under `raw_paths/`; the manuscript figure remains closure clustered |
| Raw purchase-probability confidence intervals | Consumer-period | Yes | Completed under `raw_paths/`; the manuscript figure remains closure clustered |
| Main binary purchase DDD | Consumer-period | Yes | Freshly completed under `core/purchase_frequency/` and also exists in commit `8cba55a` |
| Main member-first novelty DDD | Consumer-period | Yes | Exists in Git commit `8cba55a`; numerical comparison is recorded above |
| Purchase binary and score event studies/pretrends | Consumer-period | Yes | Freshly completed under `core/purchase_frequency/` and also exists in commit `8cba55a` |
| Member-first novelty binary and score event studies/pretrends | Consumer-period | Yes | Exists in Git commit `8cba55a`; numerical comparison is recorded above |
| Continuous-score purchase DDD | Consumer-period | Yes | Freshly completed under `core/purchase_frequency/` and also exists in commit `8cba55a` |
| Continuous-score member-first novelty DDD | Consumer-period | Yes | Exists in Git commit `8cba55a`; numerical comparison is recorded above |
| Market-new novelty, binary and score DDDs/pretrends | Consumer-period | Yes | Exists in Git commit `8cba55a`; absent as current dedicated output |
| Matched/common-support DDDs and dynamics | Consumer-period | Yes | Exists in Git commit `8cba55a`; absent as current dedicated output |
| Baseline-novelty heterogeneity | Consumer-period | Yes | Completed: both collapsed specifications, event studies, and pretrends |
| New-product-notification DDDs and dynamics | Consumer-period | Yes | Completed with consumer CRV1; closure wild-bootstrap results remain separate |
| Return timing and personally novel opportunity | One row per returning consumer | Mechanically yes | Completed; consumer clustering is close to heteroskedasticity-robust inference here |
| Non-coffee novelty and qualifying-purchase DDDs | Consumer-period | Yes | Completed: collapsed, event-study, entry, and pretrend outputs |
| Cafe-density interactions, fitted DDDs, and dynamics | Consumer-period | Yes | Completed with consumer CRV1; closure wild-bootstrap results remain separate |
| Treated-store assortment path after reopening | Store-week | **No** | Consumer ID is not an observation-level dimension; not applicable |
| Treated-versus-matched-store assortment analysis | Store-event-week | **No** | Consumer ID is not an observation-level dimension; not applicable |
| Classifier performance, calibration, descriptives, sample counts, coefficients, and R-squared values | Various | Clustering does not define these quantities | Not applicable; these are unchanged by the covariance choice |

## Direct answer: which consumer counterparts are still missing?

None among the applicable customer-level manuscript result families identified in this audit. The formerly missing results are now in the isolated consumer-cluster bundle. Two exclusions are intentional:

1. consumer-cluster restricted wild-bootstrap p-values were not computed because the manuscript's bootstrap is designed around the 18 common closure shocks; and
2. treated-store and matched-store assortment regressions cannot be clustered by consumer because their observations have no consumer identifier.

The older main novelty, market-new, score, matched/common-support, and corresponding dynamic consumer-cluster results continue to exist in commit `8cba55a`. A fresh purchase-frequency core bundle was additionally produced during this run.

## Output organization

The sensitivity is isolated at:

```text
outputs/06_inference_sensitivity/consumer_cluster/
├── baseline_novelty_heterogeneity/
├── cafe_density/
├── core/purchase_frequency/
├── new_product_notification_exposure/
├── noncoffee_novelty/
├── raw_paths/
└── return_timing_novel_opportunity/
```

The runner records the cluster variable, package version, source inputs, sample sizes, and other family-specific metadata. It does not alter `outputs/03_main_18_closures/`, `outputs/05_robustness/`, `outputs/paper/`, or `writeup/main.tex`.

For the main causal claims, a small-cluster procedure at the closure level is more informative than replacing closure clusters with consumers. The newer robustness analyses already use restricted wild-cluster inference; the headline DDD and heterogeneity results currently do not have an analogous maintained wild-cluster sensitivity.

## Provenance

- Current clustering configuration: `src/displacement_effect_estimation/config.json`
- Main estimator and p-value extraction: `src/displacement_effect_estimation/specs.py`
- Current paper-facing main outputs: `outputs/03_main_18_closures/`
- Current baseline-novelty outputs: `outputs/paper/mechanism_baseline_novelty/`
- Consumer-cluster sensitivity runner: `scripts/writeup/run_consumer_cluster_sensitivity.py`
- New consumer-cluster output bundle: `outputs/06_inference_sensitivity/consumer_cluster/`
- Consumer-cluster historical source: Git commit `8cba55a`
- Closure-cluster replacement commit: Git commit `97d9454`
- Manuscript cluster statement and results: `writeup/main.tex`

The new regressions were run on `mktserver` with Python 3.11 and PyFixest 0.50.1. The compact output directory was then copied back into the local working tree. A coefficient/mean reconciliation check confirms equality with the corresponding closure-cluster sources to numerical precision; only covariance-dependent quantities changed.
