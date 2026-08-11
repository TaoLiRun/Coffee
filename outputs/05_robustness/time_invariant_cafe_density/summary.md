# Time-invariant local café-density robustness

## Bottom line

**Evidence classification: Challenging.** The collapsed estimates remain directionally similar, but the density-interacted event study displays a systematic pre-period warning. The three pre-period density-gradient coefficients (periods -4, -3, and -2 relative to -1) are 0.1309, 0.0906, 0.0695; their joint cluster-df F test has p=0.002. Because all three estimates point in the same direction and the joint test rejects, the interacted dynamic design does not provide a clean robustness result, even though the stronger additive local-shock fixed effects are stable.

The paper-facing member-first novelty-seeking DDD is -0.0415 (95% CI [-0.0804, -0.0026]). Allowing the complete post-period interaction hierarchy with the fixed raw 500-meter café count gives a fitted DDD of -0.0333 at the member-event mean (95% CI [-0.0635, -0.0031]; restricted wild-cluster p=0.090, 9,999 repetitions). This is an absolute change of 0.0082, or 19.8% of the absolute baseline magnitude. The density gradient is 0.0300 per one-SD increase (95% CI [-0.0515, 0.1114]).

At raw 500-meter counts 2, 5, and 13, the fitted DDDs are -0.0503, -0.0439, and -0.0270, respectively. Their 95% intervals are [-0.1167, 0.0161], [-0.0950, 0.0071], and [-0.0535, -0.0006]. The locked 25% magnitude benchmark reads: member_event_mean: within benchmark; raw_count_2: within benchmark; raw_count_13: outside benchmark.

At a raw count of zero, the continuous model predicts -0.0545 (95% CI [-0.1315, 0.0226]). Only three treated design stores have zero observed 500-meter counts, so this is a sparse-support model prediction rather than a separate confirmatory estimate.

## Support and leverage

The raw 500-meter treated-minus-control standardized mean difference is -0.397. Treated and control design stores overlap from counts 0 through 19; the fitted figures mark this range explicitly. Leaving out one closure and its five matched controls at a time gives count-2 fitted DDDs from -0.0710 to -0.0318 and count-13 fitted DDDs from -0.0325 to -0.0115.

The density-gradient pre-period test uses 3 restrictions and 18 closure clusters. Its rejection is substantively relevant because the coefficients are directionally aligned, but it does not identify the source of the differential pattern. By comparison, the preferred-store-by-event-by-period-FE event-study pretest has p=0.880. The collapsed preferred-store-by-event-by-post-FE DDD is -0.0445 (95% CI [-0.0807, -0.0084]). These fixed effects absorb arbitrary additive store-level local shocks, but not shocks that affect high- and low-predicted-incidence members differently within a store.

## Low-density descriptive check

The locked rule `cafe_count_500m <= 3` retains 42 design stores (9 treated and 33 controls), 9,835 member-events, 41,175 outcome observations, and 16 contributing closure clusters. Its DDD is -0.0539 (95% CI [-0.1317, 0.0240]). Only 8 matched sets contain low-density stores on both treatment sides. This estimate is descriptive and its wide interval is limited information, not affirmative evidence for or against the baseline.

## Outcome-definition sensitivity

Using market-new novelty, the unchanged baseline DDD is -0.0417 (95% CI [-0.0606, -0.0228]). With the raw 500-meter interaction, the fitted DDD at the member-event mean is -0.0385, and the density gradient is -0.0132 per SD. Fitted DDDs at counts 2, 5, and 13 are -0.0310, -0.0338, and -0.0412. This is an outcome-definition sensitivity; member-first novelty remains primary.

## Interpretation boundary

The source counts locations classified as cafés. It does not identify brands, operating status, the POI provider, the counting procedure, or the snapshot date. The CSV file timestamp postdates the 2020-2021 treatment period and is not a measurement date. These results therefore test whether the novelty DDD is concentrated in locations with high observed café density. They do not directly measure other-brand competition, competitor closures, or a pre-treatment covariate, and the counts were not used to rematch, reweight, trim, or select specifications.

## Reproducibility

The analysis joins density through the pre-closure preferred store reconstructed from unique member-date-store visits using the original five-day and 80% rules. It reproduces the published baseline before fitting any density interaction, retains the unweighted `event_fe_id + rel_t + calendar_month` fixed effects, and clusters CRV1 inference by the 18 closure events. See `run_metadata.json`, `validation_checks.csv`, `model_specifications.csv`, and `validation_report.md` for provenance and QA.
