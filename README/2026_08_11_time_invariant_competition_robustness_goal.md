# Goal-mode instructions: robustness to time-invariant local café density

## Status and scope

This document was locked as the robustness-analysis goal before outcome estimation. The analysis was completed on August 11, 2026. The design instructions below are retained as the prespecification; the execution record in the next subsection is explicitly post-estimation.

The available variables measure nearby locations classified as **cafés**. They do not identify brands or store operating status. The analysis must therefore be described as a robustness check using a fixed proxy for **local café density**, which may reflect local competition, rather than as a direct control for other-brand competition or competitor shutdowns.

### Post-estimation execution record (August 11, 2026)

- Estimator: `scripts/writeup/estimate_time_invariant_cafe_density_robustness.py`
- Independent validator: `scripts/writeup/validate_time_invariant_cafe_density_robustness.py`
- Definitive output bundle: `outputs/05_robustness/time_invariant_cafe_density/`
- Paper-ready findings: `outputs/05_robustness/time_invariant_cafe_density/summary.md`
- Main table: `outputs/05_robustness/time_invariant_cafe_density/main_table.md`
- Validation: **PASS, 160/160 independent checks**; see `outputs/05_robustness/time_invariant_cafe_density/validation_report.md`
- Evidence classification: **Challenging**. The collapsed estimates remain negative and directionally similar across the prespecified density points, transformations, alternative radius, low-density descriptive sample, preferred-store local-shock fixed effects, and market-new outcome sensitivity. However, all three pre-period 500-meter density-gradient coefficients are positive (0.1309, 0.0906, and 0.0695), and their joint cluster-df test rejects (`p = 0.002`). The density-interacted dynamic design therefore does not deliver a clean robustness result.

The paper-facing member-first DDD is -0.0415 (95% CI [-0.0804, -0.0026]). In the primary raw 500-meter interaction, the fitted DDD is -0.0333 at the member-event mean and -0.0503, -0.0439, and -0.0270 at raw counts 2, 5, and 13. The restricted wild-cluster p-value at mean density is 0.090 using seed `20260811` and 9,999 repetitions. These results do not identify other-brand competition or competitor closures because the source limitations described below remain binding.

---

## Verified data source

### Authoritative raw file

- Server working directory: `/home/litao/Coffee/model-free`
- Raw source: `/home/litao/Coffee/data/data1031/dapt_id_address.csv`
- Relative path from the server working directory: `../data/data1031/dapt_id_address.csv`
- Source archive: `/home/litao/Coffee/data/data1031.zip`
- Encoding: GBK/GB18030, not UTF-8
- SHA-256: `361267209af83070d247aaa4b28d0d97e24654165089332566835673715419de`
- Grain and key: one row per Luckin store, keyed by `dept_id`

The exact count fields are:

| Raw field | English description | Role in this analysis |
| --- | --- | --- |
| `半径500m内店铺数(咖啡厅)` | Number of locations classified as cafés within 500 meters | Primary density measure, renamed `cafe_count_500m` in code |
| `半径1500m内店铺数(咖啡厅)` | Number of locations classified as cafés within 1,500 meters | Prespecified alternative-radius measure, renamed `cafe_count_1500m` |

An existing UTF-8 derivative, `outputs/nanjing_store_locations/nanjing_stores_geocoded.csv`, preserves both count fields and adds geocodes. A row-by-row check confirms that all 260 store IDs and both count fields match the raw CSV exactly. The derivative is useful for QA, but the GBK CSV above remains the authoritative count source.

### Facts verified before estimation

- The raw file contains 260 rows and 260 unique `dept_id` values.
- `dept_id`, address, and both count fields have no missing values; there are no duplicate store IDs.
- Both fields are nonnegative integers, and the 500-meter count never exceeds the 1,500-meter count.
- Across all 260 stores, the 500-meter count ranges from 0 to 81 and the 1,500-meter count ranges from 0 to 295. Both distributions are strongly right-skewed.
- The 18-event registry contains 18 treated and 90 distinct control stores. All 108 design stores match the count file by `dept_id`, and their normalized addresses agree with `outputs/customer-store/closure_pair_registry.csv`.
- Among the 108 design stores, the 500-meter count has a 25th percentile of 2, median of 5, and 75th percentile of 13. Thirteen stores have a zero count: 3 treated and 10 control stores.
- The design-store 33rd percentile of the 500-meter count is 3. The rule `cafe_count_500m <= 3` retains 42 stores: 9 treated and 33 controls. Only 8 closure-event matched sets contain both a low-density treated store and at least one low-density control store.

### Measurement limitations that govern the design

The raw labels say only “cafés.” The file does not document:

- whether Luckin locations, including the focal store, are included;
- whether other same-brand locations can enter the count;
- the brands of counted locations;
- whether counted locations were open, temporarily closed, permanently closed, or merely listed;
- the POI provider or counting procedure; or
- the date of the underlying POI snapshot.

The ZIP entry for `dapt_id_address.csv` is dated November 7, 2022, after the 2020–2021 analysis period. This is a file timestamp, not proof of the underlying measurement date. Because no pre-closure snapshot date is documented, **do not call either field pre-treatment or pre-closure, and do not use it to rematch stores**. Treat each field only as an observed, time-invariant store-level proxy. Time-invariant here means one fixed value per store in this file; it does not mean local market structure was economically constant during the pandemic.

---

## Goal

Assess whether the paper-facing novelty-seeking DDD is sensitive to cross-sectional differences in local café density around each member's pre-closure preferred Luckin store.

The analysis must answer three questions:

1. Do treated and control stores occupy different parts of the observed café-density distribution, and is there enough common support for an interacted regression?
2. Does the focal DDD remain economically similar after allowing post-reopening changes to vary flexibly with the fixed 500-meter café-density proxy?
3. Does the fitted DDD remain directionally similar at low, middle, and high observed density, and what—if anything—can be learned from the smaller low-density subsample?

This check cannot determine whether temporary closures of competing stores caused the focal result. It asks a narrower question: whether the result is concentrated in locations with high observed café density.

---

## Non-negotiable rules

- Assign density using each member's **pre-closure preferred Luckin store** for that closure event. Never assign it using a post-closure purchase destination.
- Do **not** merge the counts directly on `dept_id` in `displacement_scores_t0_ex_ante.csv` or the estimation panel. For control members, that field identifies the treated closure event, not the member's preferred control store.
- Reconstruct and retain `preferred_store` with the same pre-closure purchase-day logic used for cohort construction: at least five pre-closure purchase days and a preferred-store share of at least 80%.
- Do not add café density only as a level control. It is constant within a member-event and is absorbed by `event_fe_id`.
- Use `cafe_count_500m` as the primary measure. The only prespecified measurement sensitivities are standardized `log(1 + cafe_count_500m)`, the raw 1,500-meter count, and standardized `log(1 + cafe_count_1500m)`.
- Do not rematch or reweight stores on either density field because its measurement timing is undocumented and the available file metadata postdates treatment.
- Preserve the baseline outcome, treatment and high-predicted-incidence definitions, event window, sample restrictions, fixed effects, and inference. The paper-facing specification is unweighted; do not introduce regression weights.
- Reproduce the paper-facing baseline before modifying it. Save future code and outputs separately; do not overwrite baseline files.
- Do not change radii, transformations, cutoffs, samples, or interaction hierarchies after viewing the outcome results.
- Treat member-first novelty seeking as the primary outcome. Market-new novelty is an outcome-definition sensitivity. Purchase frequency remains descriptive because its high-minus-low pretrend test rejects in the current paper-facing analysis.
- Never describe the raw fields as counts of other-brand stores unless a separate, documented brand-level source is later obtained.

### Baseline implementation to preserve

- Registry: `outputs/customer-store/closure_pair_registry.csv`
- Scores: `outputs/displacement_classification/displacement_scores_t0_ex_ante.csv`
- Primary outcome bundle: `outputs/03_main_18_closures/novelty_member_first_ddd_h4/`
- Estimator: `src/displacement_effect_estimation/specs.py::fit_collapsed_specs`
- Outcome: `variety_seeking`, default member-first distinct-product definition
- Panel: unbalanced, relative periods -4 through +4, with closure period 0 excluded
- Fixed effects: `event_fe_id + rel_t + calendar_month`, where `event_fe_id` is member-by-closure-event
- Inference: CRV1 standard errors clustered by `closure_event_id`, with exactly 18 closure clusters in the full sample
- Regression weights: none

Use a new future script such as `scripts/writeup/estimate_time_invariant_cafe_density_robustness.py` and a separate output directory such as `outputs/05_robustness/time_invariant_cafe_density/`.

---

## Step 1: construct and validate the store-density merge

### 1A. Load and normalize the raw source

1. Read `../data/data1031/dapt_id_address.csv` with `encoding="gbk"` or `encoding="gb18030"`.
2. Normalize `dept_id` to integer without changing its values.
3. Rename the two Chinese fields to `cafe_count_500m` and `cafe_count_1500m` internally; preserve the raw names in metadata.
4. Assert one row per `dept_id`, no missing counts, nonnegative integer values, and `cafe_count_500m <= cafe_count_1500m`.
5. Record the raw path, file hash, encoding, row count, raw field names, and file timestamp in run metadata. Label the timestamp as file metadata, not the POI measurement date.

### 1B. Recover each member-event's preferred store

For every closure event, use the same transaction source and `get_preference_before_date()` logic used in `src/customer-store/data_processing.py`:

1. use unique member-date-store purchase visits strictly before `closure_start`;
2. select the store with the largest share of pre-closure purchase days;
3. apply the existing minimum of five purchase days and 80% preferred-store share;
4. retain the resulting `preferred_store` on each member-event; and
5. merge the café counts using `preferred_store = dept_id` from the raw source.

Required assertions:

- every treated member-event has `preferred_store` equal to the closing store;
- every control member-event has `preferred_store` in that event's `control_store_ids`;
- each member-event maps to exactly one preferred store and one value for each radius;
- counts are constant across periods within member-event and within preferred store;
- all 108 design stores and all baseline member-events are matched; and
- the merge does not change the baseline member-period row count or outcome missingness.

Any unmatched design store or member-event is an implementation failure to diagnose, not a complete case to drop. The verified source has full coverage of the 108 design stores.

### 1C. Define the prespecified variables

Let $C^{500}_s$ and $C^{1500}_s$ denote the raw café counts around preferred store $s$. The primary standardized variable is

$$
\widetilde C^{500}_s=
\frac{C^{500}_s-\bar C^{500}}{\operatorname{SD}(C^{500})}.
$$

Calculate the mean and standard deviation without regression weights, using one row per member-by-closure-event in the exact outcome-specific baseline estimation population. Do not repeatedly count member-period rows. This makes zero the mean exposure of member-events entering that regression.

Create three variables before examining outcomes:

1. primary: standardized raw $C^{500}_s$;
2. skewness sensitivity: standardized $\log(1+C^{500}_s)$;
3. alternative radius: standardized raw $C^{1500}_s$, with standardized $\log(1+C^{1500}_s)$ as its skewness sensitivity.

Do not winsorize or trim the count. Outlying stores are part of the observed support; diagnose leverage and report leave-one-store-out influence if a small number of stores drives the fitted gradient.

---

## Step 2: diagnose balance and common support

Use one row per preferred store and report the raw and log-count distributions separately for the 18 treated and 90 control stores. For both radii report:

- number of stores;
- mean, standard deviation, median, and interquartile range;
- standardized mean difference, using the pooled treated-control standard deviation;
- minimum and maximum;
- zero-count frequency; and
- an empirical CDF or a jittered dot plot showing the individual treated stores against controls.

Also report density by closure-event matched set. Show the treated store and its five prespecified controls rather than reducing each set to a single mean.

Interpretation rules:

- An absolute standardized mean difference below 0.10 is conventionally good descriptive balance, not proof of identification.
- Limited overlap means the continuous interaction may extrapolate at parts of the density range. Mark the common-support range in every fitted-DDD figure.
- Do not use a nonsignificant mean-difference test as evidence of balance.
- Do not respond to imbalance by changing matches, trimming stores, or selecting a different radius.

---

## Step 3: estimate the primary café-density-interacted DDD

Use the exact paper-facing collapsed DDD and add the complete post-period interaction hierarchy. Let:

- $Y_{iet}$ be member-first novelty seeking for member $i$, closure event $e$, and relative period $t$;
- $T_{ie}$ indicate assignment to the treated closing store;
- $H_{ie}$ indicate high predicted purchase incidence;
- $P_{et}$ indicate a post-reopening period; and
- $\widetilde C_s$ be the standardized raw 500-meter count assigned through the member's pre-closure preferred store.

Add

$$
P_{et}\Big[
\kappa_C\widetilde C_s
+\kappa_{TC}(T_{ie}\widetilde C_s)
+\kappa_{HC}(H_{ie}\widetilde C_s)
+\kappa_{THC}(T_{ie}H_{ie}\widetilde C_s)
\Big].
$$

Equivalently, add all four terms:

1. $P\times\widetilde C$;
2. $P\times T\times\widetilde C$;
3. $P\times H\times\widetilde C$; and
4. $P\times T\times H\times\widetilde C$.

These terms augment—rather than replace—the baseline $P\times T$, $P\times H$, and $P\times T\times H$ terms. Non-post interactions involving $T$, $H$, and density are time-invariant within member-event and are absorbed by `event_fe_id`.

Let $\delta_D$ be the coefficient on $P\times T\times H$. The fitted DDD at standardized density $c$ is

$$
\operatorname{DDD}(c)=\delta_D+\kappa_{THC}c.
$$

Report covariance-based estimates and confidence intervals for:

- the unmodified paper-facing baseline;
- the baseline after the preferred-store merge, which should be numerically identical because the source has no missing design-store counts;
- $\delta_D$, the fitted DDD at the unweighted mean across unique member-events;
- $\kappa_{THC}$, the change in the DDD for a one-standard-deviation increase in density;
- the fitted DDD at raw 500-meter counts of 2, 5, and 13—the design-store 25th percentile, median, and 75th percentile;
- the fitted DDD at a raw count of zero, clearly labeled as a continuous-model prediction supported by few treated stores; and
- the absolute and percentage change in the DDD at mean density relative to the unchanged baseline.

Use the full coefficient covariance matrix for every linear combination. Never add standard errors.

Do not interpret a nonsignificant $\kappa_{THC}$ as proof that local density is irrelevant. With 18 closure clusters, emphasize the confidence interval and the range of economically plausible DDD values.

---

## Step 4: run the prespecified supporting checks

### 4A. Transformation and radius sensitivity

Repeat Step 3, without altering any other component, for:

1. standardized $\log(1+C^{500}_s)$;
2. standardized raw $C^{1500}_s$; and
3. standardized $\log(1+C^{1500}_s)$.

Present these as measurement sensitivities. Do not choose a preferred transformation or radius based on statistical significance.

### 4B. Low-density subsample—descriptive only

The exact-zero 500-meter group contains only 3 treated stores and is too sparse for a confirmatory DDD. Do not present an exact-zero regression as decisive evidence.

Use the prespecified store-level rule `cafe_count_500m <= 3`, the observed 33rd-percentile cutoff among the 108 design stores. Apply the rule to each member's preferred store and estimate the unchanged baseline DDD only if the resulting design matrix is identified.

Report:

- the locked cutoff and how it was selected without outcomes;
- stores, member-events, outcome observations, closure clusters, and treated closure events retained;
- the number of matched sets containing both treated and control low-density stores;
- high- and low-predicted-incidence support on both sides of treatment within retained events; and
- the point estimate and confidence interval beside the full-sample baseline.

This check is descriptive because only 9 treated stores satisfy the cutoff and only 8 matched sets contain low-density stores on both treatment sides. Treat wide uncertainty as limited information, not evidence for or against the baseline result.

### 4C. Preferred-store-by-event-by-period fixed effects

As a stronger local-shock check, add preferred-store-by-closure-event-by-relative-period fixed effects to the event-study specification. For the collapsed post/pre model, use the corresponding preferred-store-by-closure-event-by-post fixed effects.

These effects absorb arbitrary additive time-varying shocks shared by high- and low-predicted-incidence members assigned to the same preferred store, including additive changes in competition, mobility, and local restrictions. The separate treated-by-post effect is absorbed, but $P\times T\times H$ remains identified from within-store high-minus-low changes compared across treated and control stores.

Before estimation, report how many store-event-period cells contain both high- and low-predicted-incidence members. State that this specification does not absorb a local shock that affects the two predicted-incidence groups differently within the same store.

### 4D. Café-density-interacted event study

Use the existing relative periods -4 through +4, exclude closure period 0, and retain -1 as the reference. Interact each nonreference relative-period indicator with the same complete density hierarchy used in Step 3.

For relative period $k$, report

$$
\operatorname{DDD}_k(c)=\delta_k+\kappa_k c
$$

at raw 500-meter counts of 2 and 13. Plot estimates and confidence intervals and mark the observed common-support range. Conduct a joint test that all pre-period $\kappa_k$ coefficients equal zero, while recognizing that nonrejection with 18 clusters does not establish equal latent trends.

---

## Step 5: inference and leverage

- Keep CRV1 clustering by `closure_event_id` so estimates remain comparable with the paper-facing baseline.
- For the primary collapsed specifications, also report restricted wild-cluster-bootstrap confidence intervals or p-values at the closure-event level, using seed `20260811` and at least 9,999 replications if computationally feasible.
- Report the actual number of contributing closure clusters for every restricted sample.
- Report point estimates and confidence intervals, not only significance stars.
- For the primary 500-meter interaction, add a leave-one-closure-event-out influence table for $\delta_D$, $\kappa_{THC}$, and the fitted DDD at counts 2 and 13. Remove the treated store and all of its matched controls together. This is a leverage diagnostic, not a specification-selection exercise.
- Do not call the robustness check successful merely because a coefficient remains statistically significant. Judge stability using magnitude, uncertainty, common support, and the fitted pattern across density.

---

## Step 6: organize future outputs

Create one main table with these columns:

1. paper-facing baseline;
2. primary raw 500-meter interaction;
3. log 500-meter interaction;
4. raw 1,500-meter interaction;
5. low-density sample (`cafe_count_500m <= 3`), labeled descriptive;
6. preferred-store-by-event-by-period fixed effects.

Include rows for the focal DDD, standard error, 95% confidence interval, wild-bootstrap inference, observations, member-events, preferred stores, treated stores, closure clusters, fixed effects, and sample restrictions. For interacted columns, also report the density gradient and fitted DDDs at the prespecified low, middle, and high raw counts.

Create:

1. a treated-control empirical CDF or dot plot for the 500-meter count, with common support marked;
2. a fitted DDD over the observed 500-meter count range with a 95% confidence band and markers at counts 2, 5, and 13; and
3. an appendix figure for the 1,500-meter sensitivity.

Add the density-interacted event-study figure only if it can be displayed without implying that imprecise individual coefficients establish or refute a dynamic pattern.

---

## Step 7: interpret the evidence

Classify the evidence without relying on one significance test.

### Supportive

- Treated and control stores have enough common support for the continuous interaction to be interpretable over the marked range.
- The fitted DDD at low, middle, and high 500-meter density has the baseline sign and remains economically similar to the baseline.
- The same qualitative pattern appears under the log transformation and 1,500-meter sensitivity.
- Density-interacted pre-period estimates show no systematic differential pattern, subject to low power.

The low-density subsample can strengthen this assessment if directionally consistent, but it is not required because the verified support is limited.

### Mixed

- Point estimates are broadly stable but confidence intervals allow economically important attenuation or reversal.
- Common support is narrow, the gradient is sensitive to individual treated stores, or alternative density definitions disagree.
- The low-density sample is too sparse to add useful information.

### Challenging

- The fitted DDD moves substantially toward zero or reverses within the region of common support.
- The estimated effect appears only at high café density.
- Treated and control stores have little overlap, so the primary interacted model relies heavily on extrapolation.
- Density-related differential trends appear before the closure.

Before estimation, record a substantive stability benchmark: the fitted DDD at the member-event mean and at raw counts 2 and 13 should not differ from the absolute paper-facing baseline by more than 25% of that baseline magnitude. Treat this as a transparent benchmark, not a pass/fail significance rule, and always report the estimates even when it is crossed.

---

## Required validation checks

The future task is complete only when all applicable checks pass:

- [ ] The raw source path, GBK/GB18030 encoding, raw Chinese field names, file hash, and timing limitation are recorded.
- [ ] The source has 260 unique stores, and all 108 design stores match by integer `dept_id` with no duplicate or missing counts.
- [ ] `preferred_store` is reconstructed separately before each closure with the baseline five-purchase-day and 80% share rules.
- [ ] Counts are joined on `preferred_store`, never on the closure-event `dept_id` carried by control observations.
- [ ] Every treated preferred store is the closing store and every control preferred store belongs to that event's five control stores.
- [ ] The merge leaves member-period rows and outcome missingness unchanged.
- [ ] The original baseline coefficient and standard error reproduce to the expected numerical tolerance.
- [ ] The specification remains unweighted and retains `event_fe_id + rel_t + calendar_month` fixed effects and CRV1 closure-event clustering.
- [ ] The primary measure is the raw 500-meter count; log and 1,500-meter variants are reported only as prespecified sensitivities.
- [ ] All four post-period density interactions are included.
- [ ] Marginal DDD estimates use the full coefficient covariance matrix.
- [ ] Treated-control overlap, matched-set support, and standardized mean differences are reported at the store level.
- [ ] No rematching, reweighting, trimming, or radius selection is performed using this timing-undocumented field.
- [ ] The low-density check is labeled descriptive and reports its limited treated-event support.
- [ ] Cluster counts and small-cluster inference are reported for each sample.
- [ ] No specification is selected because it produces a preferred statistical result.
- [ ] The paper does not call the field a count of other-brand competitors or claim to observe competitor openings or closures.

---

## Suggested manuscript language

> We assess sensitivity to local café density using the number of locations classified as cafés within 500 meters of each customer's pre-closure preferred store. This store-level field is fixed in the available data, so its level is absorbed by member-by-closure-event fixed effects. We interact the density proxy with the post-reopening, treatment, and predicted-incidence indicators and report the focal DDD across its observed support; a 1,500-meter count provides a prespecified radius sensitivity. The source does not identify brands, operating status, or the underlying POI snapshot date. These analyses therefore test whether the result is concentrated in locations with high observed café density; they do not measure other-brand competition directly or control for temporary competitor shutdowns.
