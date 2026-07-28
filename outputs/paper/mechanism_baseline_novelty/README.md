# Baseline-novelty mechanism result

This directory contains the accepted continuous baseline-novelty heterogeneity specification used in the manuscript's mechanism section. It is intentionally narrower than the private specification-search archive.

## Definition

Baseline novelty-seeking is the episode-level mean of within-period novelty-seeking over relative periods -8 through -1, calculated over periods in which the customer purchases. Relative periods are closure-length windows, not calendar weeks. Eligible episodes must contain at least five orders over these eight periods. Baseline novelty and `log(1 + baseline orders)` are standardized over eligible episodes.

The fully saturated collapsed model interacts Post, treatment exposure, high predicted purchase incidence, standardized baseline novelty, and standardized baseline log orders through the required lower-order terms. Customer-closure, relative-period, and calendar-month fixed effects are absorbed. Standard errors use CRV1 clustering by the 18 closure events.

The mechanism coefficient is the four-way interaction between Post, treatment, high predicted purchase incidence, and baseline novelty. The model predicts a positive coefficient: the interruption-related novelty response should be more negative for customers with lower baseline novelty-seeking.

## Accepted result

- Mechanism coefficient per one-standard-deviation increase in baseline novelty: 0.0294.
- Closure-clustered standard error: 0.0147.
- One-sided p-value for the predicted alternative `theta^D > 0`: 0.031.
- Two-sided p-value, retained in the output but not displayed in the manuscript: 0.062.
- Joint pretrend p-value for relative periods -4, -3, and -2: 0.561.
- Eligible customer-closure episodes: 18,525.
- Eligible episodes with at least one observed novelty outcome before fixed-effect singleton removal: 17,866.
- Regression observations: 79,578.

The raw baseline-novelty measure spans 0 to 1 across 18,525 eligible episodes. Its mean is 0.508, its standard deviation is 0.269 and its median is 0.500; the 10th and 90th percentiles are 0.167 and 0.889. These values describe the trait-standardization sample. Of these episodes, 17,866 have at least one observed novelty outcome before fixed-effect singleton removal.

## Baseline-order diagnostic and sensitivity

Baseline novelty is strongly related to the amount of purchase history used to construct it. In the raw eligible-episode data, its Pearson correlation with log(1 + baseline orders) is -0.329. Mean baseline novelty is 0.620 among episodes with exactly five baseline orders and 0.365 among episodes with at least 20 orders. The share at the upper boundary of one falls from 19.3% to 0.1% across these groups. This relationship may combine genuine behavioral differences with finite-history measurement, so the accepted model allows the DDD to vary separately with baseline order history.

The appendix sensitivity removes the complete Post-by-baseline-order interaction hierarchy but otherwise retains the same sample and specification. The mechanism coefficient remains positive at 0.0229 (SE 0.0143), but its one-sided p-value rises to 0.064. Its joint pretrend p-value is 0.409. The direction therefore survives, but the no-order-adjustment estimate does not meet the manuscript's 5% one-sided threshold.

## Files

- `baseline_novelty_results.csv`: complete collapsed coefficient vector and both p-value conventions.
- `baseline_novelty_event_study.csv`: continuous heterogeneity coefficient path relative to period -1.
- `baseline_novelty_pretrend_test.csv`: joint pretrend test.
- `baseline_novelty_support.csv`: four-cell episode support and baseline-trait summaries.
- `baseline_novelty_distribution_summary.csv`: range, moments, percentiles and boundary mass for the raw baseline trait.
- `baseline_novelty_distribution_bins.csv`: ten-bin frequency distribution used in the manuscript figure.
- `baseline_novelty_headline_results.csv`: the mean-trait DDD and baseline-novelty gradient in percentage-point units, with regression fit statistics.
- `baseline_novelty_manifest.json`: exact inputs, formula, standardization, sample counts, and headline values.
- `inputs/episode_window_novelty_components.csv`: period-level novelty components used to construct the accepted baseline trait.
- `inputs/episode_window_order_counts.csv`: matching period-level order counts used for the minimum-order screen and order-history adjustment.

The reproducible estimator is `scripts/writeup/estimate_baseline_novelty_mechanism.py`.

- baseline_order_diagnostic_summary.csv: raw Pearson and Spearman associations between baseline novelty and baseline order history.
- baseline_order_diagnostic_groups.csv: raw baseline-novelty moments by baseline-order-count group.
- baseline_novelty_results_without_order_adjustment.csv: complete collapsed coefficient vector after removing the Post-by-baseline-order hierarchy.
- baseline_novelty_event_study_without_order_adjustment.csv: corresponding event-study coefficient path.
- baseline_novelty_pretrend_without_order_adjustment.csv: corresponding joint pretrend test.
- baseline_novelty_order_adjustment_comparison.csv: side-by-side headline estimates from the accepted and no-order-adjustment specifications.

## Scope

Alternative grouping rules, metric definitions, period lengths, minimum-order screens, nonlinear specifications, alternative covariance estimators, and rejected two-period results are preserved in the private remote archives. They are not displayed in the manuscript. The two component files required by the accepted specification are copied into this directory's `inputs/` subdirectory so the maintained estimator does not depend on the rejected audit outputs.
