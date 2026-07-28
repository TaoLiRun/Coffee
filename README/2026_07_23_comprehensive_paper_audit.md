# Comprehensive Paper Audit and Revision Plan

## Scope

This note records the writing, data-presentation, identification, inference,
classifier, mechanism, exhibit, and reproducibility issues identified in the
audit of:

- `writeup/main.tex`;
- the analysis code and saved outputs in this repository; and
- `literature/Levine-Hristakeva - Stopping Shopping at Stop and Shop How Temporary Disruptions Affect Store Choice.md`.

The separate note
`README/2026_07_23_headline_coefficient_interpretation_audit.md` covers the
most important estimand error: the headline triple-interaction coefficient is a
high-minus-low differential, not the high-group treatment effect.

Part I was updated on July 24, 2026 against the revised manuscript and then
checked against the outcome-construction code. Treatment is assigned through
the episode's focal store, but the classifier target and all three behavioral
outcomes aggregate purchases across the observed chain. The July 26 revision
also changes the production inference from member to closure-event clustering
and regenerates the 18-event results; it does not change the estimand, sample,
classifier or outcome construction.

The July 27 revision replaces the rejected discrete pre-novelty split with a
continuous baseline-novelty interaction in the mechanism section. The accepted
specification measures baseline novelty over relative periods -8 through -1,
requires at least five baseline orders, adjusts for standardized log baseline
orders through the complete interaction hierarchy, and retains closure-event
clustered inference. Rejected alternatives remain in a private working archive.

## Executive diagnosis

The central idea is understandable, the main paper is visually clean, and all
main-text tables and figures are referenced. The current draft is nevertheless
not submission-ready. The principal problems are:

1. The sample flow and outcome-specific attrition are not transparent.
2. There is no genuine descriptive-statistics table, particularly no
   four-cell table for the DDD design.
3. The paper must distinguish local treatment assignment from chain-wide
   outcome measurement. The code does not restrict the classifier target,
   purchase frequency or either product-choice outcome to the focal store.
4. Novelty is observed only after a purchase, and the probability of observing
   it varies sharply by predicted-incidence cell and over event time.
5. Key identifying assumptions are stated abstractly but are not mapped to
   focused diagnostics; important adverse diagnostics are omitted from the
   manuscript.
6. The original member-clustered inference did not address treatment assigned
   through only 18 closure events. This item was resolved on July 26 by making
   closure-event clustering the production convention.
7. The classifier is described more strongly than its validation supports.
8. Several tables omit uncertainty, mix estimands, or lack the information
   needed to understand the message.
9. The mechanism interpretation is substantially stronger than the evidence.
10. Paper numbers are manually transcribed rather than generated as immutable
    paper artifacts.

The earlier rubric-style assessment was approximately 58/100: the question and
basic narrative were stronger than the transparency of the sample, the
precision of the estimands, and the identification/inference evidence. The
number is only a revision-readiness summary, not a scientific grade.

The most efficient revision order is:

1. freeze and document the sample and outcome definitions;
2. state once in the main text that treatment is assigned through the focal
   store while outcomes are measured across the chain, and give the precise
   definitions in the appendix;
3. create sample-flow, purchase-probability/sample-entry, and four-cell descriptive exhibits;
4. repair inference and present all identification diagnostics;
5. rebuild result tables with correctly labeled estimands and uncertainty;
6. revise the mechanism claims and then perform the prose consistency pass.

# Part I. Data, sample construction, and descriptive statistics

## July 24, 2026 update: scope, estimand, and placement

A code check supersedes the earlier focal-outcome interpretation. For treated
customers, treatment is assigned through the preferred pre-closure store that
closes; for controls, assignment is through a preferred store among the
matched stores that remain open. The prediction target, purchase frequency,
novelty-seeking and new-product-seeking are then constructed from purchases at
all observed stores in the chain. The resulting estimand is the effect of a
local focal-store closure on the customer's chain-wide behavior. This is not
behavior across the full coffee market because purchases from competing
retailers are not observed.

Part I should therefore be implemented as a manuscript revision using the
existing estimates, not as a re-estimation. The scope distinction is important
but does not need repeated emphasis: state it once in the main data/outcome
description and use precise definitions in the appendix.

The placement of material follows the useful division in
Levine--Hristakeva, Gruber (1994), and the data/appendix organization in
Schaudt (2026):

| Placement | What this paper should include |
|---|---|
| Main data section | Data source, dates, geographic/store coverage, unit of observation, exact order and product-line counts, focal-store treatment assignment, one sentence on chain-wide outcome measurement, high/low classification, final sample size, four-cell descriptive statistics, and the identifying raw paths |
| Main text, one sentence plus appendix reference | Closure-screen summary, novelty missingness, variable event-window length, and the new-product-seeking alternative definition |
| Appendix | Full 101-to-18 event flow, exact registry screens, manual exclusions, outcome-specific observation flow, cell-by-period purchase probability and resulting novelty-sample entry, detailed matching procedure, event-level match diagnostics, complete variable definitions, and additional descriptive statistics |
| Omit unless used in interpretation | Mechanical file names, internal cache keys, implementation logs, and exhaustive intermediate variables |

This hierarchy follows Levine--Hristakeva's choice to define the outcome
scope, treated/control groups, final sample, classifier and four identifying
groups in the main paper while placing imputation, matching mechanics and
extended balance evidence in appendices. The reference paper's outcome is
focal-retailer trips; this paper's coded outcomes instead cover the observed
chain. Gruber's DDD discussion reinforces that readers must see the four cells
that generate the third difference. Schaudt's data appendix illustrates why
exhaustive source and variable definitions should not interrupt the main
empirical narrative.

The remaining Part I diagnoses should be read as follows:

- counts/dates, closure flow, observation flow, four-cell descriptives,
  purchase probability governing novelty-sample entry, and matching
  documentation still require manuscript revisions;
- the focal-store versus chain-wide diagnosis is resolved by the code check
  and is replaced below with a local-treatment/chain-wide-outcome wording
  check;
- the distinct-product novelty formula and the name
  ``new-product-seeking'' are already corrected in the current manuscript;
- unconditional-outcome, weighting, bounds, and fixed-window estimates remain
  possible empirical extensions, but they are outside this writing-only
  revision and should not be presented as completed analyses.

## 1. Correct the setting-level counts and dates

The repository logs support these exact setting-level counts:

| Item | Audited value | Evidence |
|---|---:|---|
| Product-line/commodity records | 10,631,250 | `outputs/customer-store/logs/main_customer_store.log` |
| Orders | 7,312,498 | same log |
| Unique customers | 779,744 | same log |
| Stores | 260 | same log |
| Data start | 2020-06-01 | same log |
| Data end | 2021-12-31 | same log |
| Calendar months covered | 19 | June 2020 through December 2021, inclusive |

The July 24 manuscript revision now uses one exact statement throughout:

> The data cover June 1, 2020 through December 31, 2021—19 calendar
> months—and contain 7,312,498 orders, represented by 10,631,250 product-line
> records, from 779,744 unique customers at 260 stores.

If the paper prefers rounded prose, use “approximately 779,000 customers” only
after giving the exact count in the data section. Do not call 10.6 million
product-line records “transactions” if the 7.3 million rows in `order_result`
are the order-level transactions.

The main estimation sample is narrower:

- 18 closure events;
- 40,148 customer-closure episodes;
- 40,148 unique customers—the current saved panel happens to contain exactly
  one episode per customer, although the estimator does not encode a general
  one-episode-per-customer rule;
- 321,184 customer-episode-period rows;
- exactly eight regression periods per episode:
  \(-4,-3,-2,-1,1,2,3,4\);
- nine `period_start` calendar months, March through November 2021.

The paper should distinguish the 19-month raw-data span from the nine calendar
months represented by regression-window start dates.

## 2. Explain why 23 of the 41 non-campus events disappear

### 2.1 What is currently recoverable

**Writing status.** The appendix now reports the complete 101-to-18 flow in
short paragraphs rather than a dense table. Each paragraph gives the count and
the reason for the corresponding screen, including the campus, duration,
design-support, closure-period purchase-rate and Lunar New Year restrictions.
The underlying reproducibility problem described below remains: the last four
exclusions are not produced by a coded rule.

The event flow is:

| Stage | Events | Removed at stage | Rule |
|---|---:|---:|---|
| Detected closure spells | 101 | — | `outputs/store/store_closures.csv` |
| Non-campus candidates | 41 spells at 38 stores | 60 | Campus/university screen |
| Duration-eligible candidates | 34 | 7 | Keep duration \(<30\) days |
| Registry-screened events | 22 | 12 | Treatment/control size and closure-period rate rules |
| Headline sample | 18 | 4 | Four early-February events manually removed |

Thus the 23 events lost after the 41-candidate stage are:

\[
23=7+12+4.
\]

The campus screen has an important measurement rationale. These store closures
occur during summer periods when Covid-19 policies may have moved students off
campus. The transaction data cover purchases in the focal city, so a student
who leaves the city also leaves the observed purchase panel. Zero transactions
at a campus store can therefore reflect the disappearance of its local
customer population rather than a supply disruption. The manuscript now
states this limitation directly.

### 2.2 The seven duration exclusions

`src/customer-store/data_processing.py:155-174` applies the strict rule
`closure_duration_days < 30`. These seven candidates fail it:

| Store | Start | Duration (days) |
|---:|---:|---:|
| 166 | 2021-01-12 | 54 |
| 253 | 2021-01-20 | 40 |
| 166 | 2021-06-29 | 101 |
| 147 | 2021-07-27 | 48 |
| 110 | 2021-07-28 | 40 |
| 160 | 2021-07-28 | 35 |
| 75 | 2021-07-31 | 44 |

The constant name `MAX_CLOSURE_DURATION_DAYS = 30` can be misread as including
30-day events. The paper and code comments should say “strictly shorter than
30 days.”

### 2.3 The 12 registry-screen exclusions

`src/customer-store/data_processing.py:676-685` applies, in order:

- at least one treated customer;
- at least one control customer;
- at least 50 customers in each arm;
- control purchase rate during the closure at least twice the treated rate.

The current run log records 22 kept out of 34, but
`build_kept_closure_registry()` at
`src/customer-store/data_processing.py:780-808` overwrites the 34-row decision
registry with its 22 kept rows. The current artifact therefore loses the 12
excluded rows and their reasons.

There is a second reproducibility consequence: rerunning
`src/customer-store/main_customer_store.py` regenerates the canonical
`closure_pair_registry.csv` as the 22 kept events. No current pipeline step
reapplies the four manual exclusions to regenerate the headline 18. The main
results runner checks that its input happens to contain 18 events, but cannot
produce that registry from the documented rules.

A historical version of the decision registry, recoverable at repository
commit `ee0bc5c`, records:

| Reason | Store/start pairs | Count |
|---|---|---:|
| `low_control_rate` | 101/2020-09-12; 64/2020-10-11; 64/2020-10-31; 21/2021-04-09; 57/2021-07-01; 68/2021-07-29; 64/2021-07-29; 165/2021-11-10 | 8 |
| `min_group_size` | 239/2020-09-05; 197/2021-08-03 | 2 |
| `no_control` | 189/2021-08-03; 196/2021-08-03 | 2 |

These historical rows should be verified by rerunning the current pipeline
after adding a durable audit output. A prior Git artifact is evidence about
what happened, not an acceptable substitute for a current generated sample
flow.

The closure-period purchase-rate rule itself also deserves scrutiny. It selects
events using behavior realized during treatment. Explain its design purpose,
show results without it, and consider replacing it with a rule based only on
pre-closure information.

### 2.4 The four manual exclusions

`outputs/customer-store/README.md` says the 18-event registry excludes:

| Store | Start |
|---:|---:|
| 254 | 2021-01-30 |
| 228 | 2021-02-04 |
| 225 | 2021-02-09 |
| 181 | 2021-02-11 |

The technical report calls these “early-February events with weaker fit,” but
the repository does not encode an ex-ante exclusion criterion. All four overlap
the Lunar New Year period, but that interpretation is not a documented rule in
the current pipeline.

This is a serious transparency issue because moving from 22 to 18 is manual.
The revision must either:

- define and encode an objective calendar/holiday or data-quality rule, then
  apply it to every candidate; or
- retain the 22-event sample as primary and present the 18-event restriction
  as a clearly labeled sensitivity analysis.

In either case, show both results. The archived 22-event estimates have the same
broad sign pattern, which is useful evidence, but it does not replace a
prospective rule.

### 2.5 Code changes needed to make the flow auditable

Change `build_kept_closure_registry()` so it never writes the all-candidate and
kept-only data to the same path. Proposed outputs:

```text
outputs/customer-store/closure_candidates_101.csv
outputs/customer-store/closure_noncampus_41.csv
outputs/customer-store/closure_duration_eligible_34.csv
outputs/customer-store/closure_screen_decisions_34.csv
outputs/customer-store/closure_pair_registry_full_22.csv
outputs/customer-store/closure_pair_registry_main_18.csv
outputs/customer-store/closure_sample_flow.csv
```

Each event row should retain:

```text
dept_id
closure_start
closure_end
duration
detection_source
campus_flag
duration_eligible
n_treatment
n_control
treatment_purchase_rate_during
control_purchase_rate_during
registry_status
registry_skip_reason
headline_status
headline_exclusion_reason
rule_version
```

Add assertions:

```python
assert len(candidate_101) == 101
assert len(noncampus_41) == 41
assert len(duration_34) == 34
assert (decision_34["status"] == "kept").sum() == 22
assert len(main_18) == 18
assert set(main_18_keys) <= set(full_22_keys)
```

The paper now explains the flow in readable appendix paragraphs. The full
event-level registry should still be included in the replication package.

## 3. Explain the 321,184 to 99,644 to 95,986 path

**Writing status.** The main data section now identifies product-choice
outcomes as conditional on purchase, and the appendix reconciles 321,184
potential rows, 105,854 nonmissing novelty rows, the 6,210 singleton-row
restriction, 99,644 main-regression observations and 95,986 heterogeneity
observations. The classifier-to-estimation flow remains undocumented.

The current paper says novelty has 99,644 observations because it is defined
only in periods with a purchase. That is incomplete. There are two separate
drops before the main novelty regression and two more selection stages for the
heterogeneity regression.

### 3.1 Confirmed row flow

| Stage | Rows | Episodes/customers | Reason |
|---|---:|---:|---|
| Rectangular purchase/novelty panel | 321,184 | 40,148 | 40,148 episodes × 8 periods |
| Novelty nonmissing | 105,854 | 29,573 | Customer purchases at least one product in that window |
| Main novelty regression | 99,644 | 23,363 | 6,210 one-observation episode-FE singletons dropped by `pyfixest` |
| Heterogeneity rectangular panel | 207,152 | 25,894 | Keep episodes with at least one nonmissing *pre-period* novelty value |
| Heterogeneity novelty nonmissing | 100,012 | 25,894 at rectangular-panel stage | Conditional-purchase observations |
| Heterogeneity regression | 95,986 | 21,868 | 4,026 one-observation episode-FE singletons dropped |

Among all 40,148 episodes:

- 10,575 have no observed novelty period;
- 6,210 have exactly one;
- 21,476 have two through seven;
- 1,887 have all eight.

Relative to the main novelty regression, the heterogeneity regression loses
3,658 effective observations and 1,495 effective customers. Those episodes
cannot be classified by pre-period novelty even if they purchase and reveal
novelty only after reopening.

The episode selection is highly uneven across DDD cells:

| Cell | Potential episodes | At least one novelty observation | Main regression (at least two) | Pre-novelty eligible | Heterogeneity regression |
|---|---:|---:|---:|---:|---:|
| Control, low | 23,934 | 15,309 | 10,457 | 12,317 | 9,265 |
| Treated, low | 5,349 | 3,415 | 2,334 | 2,745 | 2,040 |
| Control, high | 8,824 | 8,813 | 8,592 | 8,798 | 8,584 |
| Treated, high | 2,041 | 2,036 | 1,980 | 2,034 | 1,979 |

The pre-novelty restriction therefore retains almost every high-predicted-
incidence episode while removing many low-predicted-incidence episodes. It is
not an innocuous relabeling of the main sample.

### 3.2 Why this matters

The 99,644 observations are not merely “all windows with a purchase.” That
description ignores the 6,210 purchase windows discarded because the
customer-episode fixed effect has only one usable outcome.

The heterogeneity sample conditions on an additional pre-period behavior:
having at least one observed pre-period novelty value. It is therefore a more
selected, more purchase-active sample. Its results cannot be presented as if
they came from the main novelty population.

### 3.3 Code instrumentation

Add a reusable `build_sample_flow()` function after sample construction and
before estimation. It should output, by outcome and specification:

```text
stage
rows
unique_members
unique_episodes
unique_closures
treated_low
treated_high
control_low
control_high
reason
```

For fixed-effect regressions, calculate and save the singleton stage explicitly
rather than relying only on the estimator's final `_N`. The run should assert:

```python
n_effective == n_nonmissing - n_singleton_rows
```

Write both `sample_flow.csv` and a generated LaTeX appendix table. Correct the
inconsistent statement in `docs/technical_report.md` that refers to 105,854 as
the model observation count while another section reports 99,644.

The classifier exhibit also uses a broader pre-final-restriction cohort:
8,092 treated and 36,766 control episodes, compared with 7,390 treated and
32,758 controls in the main estimation panel. Its note acknowledges that it is
computed before final restrictions, but the 702 treated and 4,008 control
losses are not reconciled. Extend the same flow ledger through classifier
eligibility, scoring, registry filtering, history requirements, and final
estimation membership, separately by treatment and predicted-incidence group.

## 4. Add a real four-cell descriptive-statistics table

### 4.1 The reference-paper benchmark

The related paper does **not** present one comprehensive summary-statistics
table for all four DDD cells.

It distributes four-cell information across several exhibits:

- Table 1 is a symbolic four-cell identification decomposition, not observed
  statistics.
- Table 2 compares treated and control demographics but does not split by
  predicted displacement.
- Figure 5 plots the raw outcome path in all four empirical cells.
- Table A5 reports only two pre-strike covariates separately by displaced
  status within treatment and control.
- Figure A2 repeats four-cell paths in the matched sample.
- Table A7 reports four-cell counts for heterogeneity categories.

Thus, the reference shows all four cells conceptually and in raw outcome paths,
and provides limited four-cell balance/count information, but it does not show
means, SDs, and sample sizes for a broad variable set in one table. This paper
can improve materially on that benchmark.

### 4.2 Current four-cell episode counts

The current main sample contains:

| Cell | Customer-closure episodes |
|---|---:|
| Control, low predicted incidence | 23,934 |
| Treated, low predicted incidence | 5,349 |
| Control, high predicted incidence | 8,824 |
| Treated, high predicted incidence | 2,041 |
| Total | 40,148 |

These counts should appear in the main paper.

### 4.3 Recommended main table

**Writing status.** The manuscript now includes a compact four-cell table with
episode counts, predicted incidence, pre-period purchase frequency,
pre-period novelty, the share of windows with a purchase and closure duration. This is the
right amount for the main narrative. The broader customer-feature and
store-event tables described below remain useful appendix additions once they
can be generated reproducibly.

Use columns that make both within-predicted-incidence treatment-control
comparisons visible:

| Variable | Control, low | Treated, low | Standardized difference, low | Control, high | Treated, high | Standardized difference, high | Difference in gaps |
|---|---:|---:|---:|---:|---:|---:|---:|

For continuous variables, display the mean with the SD underneath. Prefer
standardized differences over star-heavy balance tests. High-versus-low
differences are expected by construction; the design question is whether
treated and controls are comparable *within* predicted-incidence stratum and
whether their pre-period gaps differ.

Recommended panels:

**Panel A. Sample composition and outcome support**

- customer-closure episodes;
- unique customers;
- closure events represented;
- focal/preferred stores represented;
- purchase-panel observations;
- novelty-seeking observations, which occur only in purchasing windows;
- realized purchase probability and resulting novelty-sample entry;
- probability of at least one pre-period purchase;
- probability of at least one post-period purchase;
- average number of post periods contributed.

**Panel B. Classifier support and purchasing propensity**

- predicted period-0 purchase probability;
- observed holdout purchase probability;
- recent purchase frequency over one, two, and four weeks;
- total pre-period purchase days;
- days since last purchase;
- preferred-store purchase share;
- average pre-period purchase frequency.

**Panel C. Pre-period outcomes and product behavior**

- purchase frequency;
- member-first novelty;
- first-observed-sale novelty;
- distinct products purchased;
- concentration in most-purchased product;
- repeat-product share;
- products per basket;
- spend per order, if used;
- share of windows with no purchase.

**Panel D. Customer history and engagement**

- days since first observed purchase;
- months of observed prehistory;
- coupon-use share;
- average discount;
- push-notification exposure;
- membership tenure and the demographics used by the classifier.

Put closure duration, store setup date, transactions per day, active customers,
assortment size, first-observed product sales, and match distance in a separate
**store-event matching table**. Report that table event-weighted. Repeating an
event characteristic for thousands of customers and treating those repetitions
as independent is not valid event-level balance inference.

### 4.4 Code plan for the table

Create `scripts/writeup/generate_descriptive_tables.py`, or an equivalent
well-delimited module called by the one-command paper build.

1. Read the 321,184-row main estimation sample.
2. Define:

   ```python
   cell = np.select(
       [
           (treated == 0) & (disp_binary == 0),
           (treated == 1) & (disp_binary == 0),
           (treated == 0) & (disp_binary == 1),
           (treated == 1) & (disp_binary == 1),
       ],
       ["control_low", "treated_low", "control_high", "treated_high"],
   )
   ```

3. Collapse period-varying pre-treatment variables to one row per
   `(member_id, dept_id, closure_start)` before computing episode-level
   descriptives.
4. Merge ex-ante features from the exact feature cache used to score the
   episode; do not rebuild features from a different run.
5. Compute mean, SD, median, p25, p75, and nonmissing \(N\) internally.
6. Compute within-stratum standardized mean differences:

   \[
   \frac{\bar X_T-\bar X_C}
        {\sqrt{(s_T^2+s_C^2)/2}}.
   \]

7. Compute any difference-in-gaps with closure-event bootstrap or
   randomization inference, not a naive customer-row SE.
8. Generate:

   ```text
   outputs/paper/descriptives/four_cell_summary.csv
   outputs/paper/descriptives/four_cell_summary.tex
   outputs/paper/descriptives/store_event_balance.csv
   outputs/paper/descriptives/store_event_balance.tex
   ```

9. Copy the verified table directly into `writeup/main.tex` and add a
   reproducibility check for the four cell counts above. Do not use
   `\input{tables/...}`; this repository keeps paper tables inline.

The main table can show means and SDs to remain readable. Add a generated
appendix table with \(N\), mean, SD, p25, median, p75, minimum, and maximum for
all continuous setting, customer, store, and outcome variables.

## 5. Report purchase probability and when novelty is defined

**Writing status.** The main four-cell table now reports the share of pre-period
windows with a purchase, and the appendix explains that this realized purchase
probability determines which windows enter the novelty-seeking sample. A full
cell-by-period purchase-probability exhibit is now reported; a selection DDD
remains an unreported extension.

### 5.1 Confirmed purchase probabilities and novelty-sample entry

Define \(R_{iet}=1\) when a customer makes at least one purchase in an
episode-period. Because novelty-seeking is defined exactly in those windows,
\(R_{iet}\) is also the indicator that the window enters the novelty sample. In
the current saved panel:

| Cell | Panel rows | Novelty-observed rows | \(P(R=1)\) |
|---|---:|---:|---:|
| Control, low | 191,472 | 39,403 | 0.2058 |
| Treated, low | 42,792 | 8,940 | 0.2089 |
| Control, high | 70,592 | 46,560 | 0.6596 |
| Treated, high | 16,328 | 10,951 | 0.6707 |

By relative period:

| Relative period | Panel rows | Novelty-observed rows | \(P(R=1)\) |
|---:|---:|---:|---:|
| -4 | 40,148 | 15,703 | 0.3911 |
| -3 | 40,148 | 15,049 | 0.3748 |
| -2 | 40,148 | 14,512 | 0.3615 |
| -1 | 40,148 | 12,364 | 0.3080 |
| +1 | 40,148 | 11,640 | 0.2899 |
| +2 | 40,148 | 12,192 | 0.3037 |
| +3 | 40,148 | 12,106 | 0.3015 |
| +4 | 40,148 | 12,288 | 0.3061 |

The very large low/high difference in purchase probability is unsurprising
because the classifier is designed to predict purchase incidence. It
nevertheless means that the conditional novelty regression compares selected
purchase occasions and that the selected population changes over time.

The full cell-by-period probabilities are:

| Relative period | Control, low | Treated, low | Control, high | Treated, high |
|---:|---:|---:|---:|---:|
| -4 | 0.265 | 0.261 | 0.732 | 0.731 |
| -3 | 0.233 | 0.220 | 0.765 | 0.755 |
| -2 | 0.180 | 0.190 | 0.846 | 0.840 |
| -1 | 0.177 | 0.172 | 0.660 | 0.684 |
| +1 | 0.180 | 0.191 | 0.577 | 0.598 |
| +2 | 0.201 | 0.207 | 0.579 | 0.574 |
| +3 | 0.199 | 0.219 | 0.560 | 0.605 |
| +4 | 0.211 | 0.213 | 0.557 | 0.578 |

An exploratory selection DDD using all 321,184 rows and the current member-
clustered specification gives:

- `Post × Treated`: 0.01131 (SE 0.00443, \(p=.011\));
- `Post × High`: -0.16762 (SE 0.00423, \(p<.001\));
- `Post × Treated × High`: 0.00334 (SE 0.00966, \(p=.730\)).

This fails to detect a differential treated-high change in purchase
probability, but the large level and time changes in entry into the novelty
sample remain. It does not establish missing at random and should be
regenerated with the paper's final inference procedure before citation.

### 5.2 Code for the purchase-probability exhibit

Immediately after building the novelty panel:

```python
audit = sample.copy()
audit["novelty_observed"] = audit["variety_seeking"].notna().astype(int)

cell_period = (
    audit.groupby(["treated", "disp_binary", "rel_t"], observed=True)
    .agg(
        panel_rows=("novelty_observed", "size"),
        observed_rows=("novelty_observed", "sum"),
        probability_observed=("novelty_observed", "mean"),
        unique_episodes=("event_fe_id", "nunique"),
    )
    .reset_index()
)
```

Generate:

- a table by cell and relative period;
- a four-line event-time plot of realized purchase probability \(P(R=1)\) with
  95% intervals;
- a DDD regression using `novelty_observed` as the outcome;
- the already available purchase-incidence result, clearly linked to this
  selection question.

Use closure-event-aware inference. Report levels as well as the DDD because a
zero DDD does not imply the composition of observed purchasers is stable.

## 6. Add unconditional exploration outcomes and selection sensitivity

Conditional novelty answers: *among products purchased in a window with a
purchase, what share are new?* That can be substantively useful, but treatment
can also affect whether a purchase occurs. The paper needs at least one outcome
defined for every episode-period.

### 6.1 Preferred unconditional outcomes

Construct:

1. **Any-new-product incidence**

   \[
   1\{\text{at least one new-to-member product is purchased in the window}\},
   \]

   coded zero when there is no purchase.

2. **New distinct products per calendar day**

   \[
   \frac{\#\{\text{distinct new-to-member products in the window}\}}
        {\text{window days}}.
   \]

3. **All distinct products per calendar day**, to distinguish a new-product
   decline from a general decline in product purchasing.

4. Optionally, **new-product purchase instances per calendar day** as a
   purchase-instance-weighted robustness measure.

Estimate the same event-study and collapsed DDD for each. Present a two-part
decomposition:

- purchase/observation incidence;
- novelty conditional on purchase;
- unconditional new-product acquisition.

Do not set conditional novelty to zero for nonbuyers and retain the label
“novelty share.” That produces a different compound outcome and should be
named accordingly.

### 6.2 Bounds

Because conditional novelty lies in \([0,1]\), report a transparent worst-case
missing-outcome sensitivity. For each cell-period, let:

- \(q=P(R=1)\);
- \(\mu=E[Y\mid R=1]\).

Without assumptions about missing outcomes, the full-cell mean is bounded by:

\[
[q\mu,\;q\mu+(1-q)].
\]

Apply the DDD's positive and negative signs to combine cell-period bounds:
positive terms use lower bounds when constructing the DDD lower bound and
upper bounds for its upper bound; negative terms do the reverse.

These bounds may be wide, and novelty for a nonpurchase is not a natural latent
share. Present them as a formal selection-sensitivity exercise, not as the
preferred economic estimand. The unconditional endpoints above are more
interpretable.

If a monotonicity assumption is defensible, add Lee-style trimming bounds, but
state exactly which group's observation probability is assumed to move
monotonically and test whether the observed selection rates have the required
ordering.

### 6.3 Weighting

As a sensitivity analysis, estimate the probability that novelty is observed
using only pre-treatment predictors plus event and relative-period structure.
Use cross-fitting, stabilized inverse-probability weights, overlap trimming,
and event-aware inference. Show:

- score overlap;
- weight distribution and maximum;
- effective sample size;
- unweighted and weighted estimates.

Post-treatment purchase is part of the causal response, so missing-at-random
weighting is a strong assumption and should not become the primary estimate.

## 7. Distinguish focal-store assignment from chain-wide measurement

**Writing status.** The manuscript now makes this distinction once in the main
data section and uses the precise chain-wide definitions in the outcome and
appendix variable descriptions.

The code implements a local treatment with chain-wide outcomes. It identifies
treated and control customers through their preferred pre-closure stores, but
the outcome loaders discard `dept_id` before constructing the classifier
target and behavioral measures. No subsequent outcome step filters purchases
to the episode store.

The main paper needs only one scope sentence:

> Treatment status is assigned through the customer's preferred pre-closure
> store, while the classifier and behavioral outcomes aggregate purchases
> across all stores in the chain.

Use the following appendix definitions:

> Purchase frequency is the number of calendar days in the event window on
> which the customer purchased from any observed store in the chain, divided
> by the number of calendar days in that window.

> Novelty-seeking is the share of distinct products purchased anywhere in the
> chain in the event window that the customer had not purchased anywhere in
> the chain before that window.

> New-product-seeking is the share of distinct products purchased anywhere in
> the chain whose first observed sale anywhere in the chain occurs in the
> current or immediately preceding event window.

Call this scope “chain-wide” rather than “market-wide” in technical
definitions. The data do not observe competing coffee retailers, so
“market-wide” could be read as covering purchases outside the chain.

## 8. Correct the remaining outcome definitions

### 8.1 Purchase frequency

The code counts **distinct purchase days per calendar day**, not orders,
quantities, spending, sales, or cups. Accordingly:

- replace “aggregate sales,” “consumption,” and broad “demand” claims with
  “purchase-day frequency” unless those additional outcomes are analyzed;
- state that multiple orders on one day count once;
- state that the denominator is the closure-specific window length.

Because the 18 closures last 10 to 29 days, four post periods span 40 to 116
days. Avoid calling this uniformly “long run” or “lasting.” State the range and
show dynamic effects.

### 8.2 Novelty-seeking

The current manuscript correctly defines the denominator as the number of
**distinct product IDs** purchased in the window; a repeatedly purchased
product counts once.

Use:

> Novelty-seeking is the share of distinct products purchased anywhere in the
> chain in the window that the customer had not purchased anywhere in the
> chain before the start of that window.

Use an explicit set-cardinality formula. Report purchase-instance weighting as
a robustness measure if it is substantively relevant.

Novelty status is left-censored at June 2020. Add:

- minimum observed-history/washout restrictions;
- results among customers observed well before their event;
- sensitivity to lookback length.

### 8.3 New-product-seeking

The current manuscript now correctly calls this robustness measure
new-product-seeking. It should continue to say that the measure uses a
product's earliest observed sale in the transaction data, not a verified
catalog-introduction date.

Explain that an early sale can reflect availability, demand, or data coverage,
not necessarily a formal introduction.

### 8.4 Fixed windows

Closure-length normalization does not remove all comparability concerns because
duration changes both exposure length and the calendar horizon represented by
four periods. Add fixed 7-, 14-, and 21-day-window estimates, duration strata,
and a table of the event weights underlying pooled results.

## Matching and customer assignment must be documented

The current prose says matching “ensures comparability,” which is stronger than
the implementation and evidence.

The code currently:

- computes each customer's preferred store separately before each closure,
  using all observed pre-closure purchase days;
- requires at least five pre-closure purchase days and a preferred-store share
  of at least 80%;
- chooses up to five control stores by nearest store setup date;
- excludes all treated stores, control stores already used for an earlier
  closure, and control addresses containing the university/college keywords
  `大学` or `学院`;
- proceeds greedily in closure-date order, so later control sets and later
  event retention depend on earlier choices.

Matching on setup date alone does not establish comparable demand, customer
composition, geography, assortment, promotions, or pretrends. The during-
closure purchase-rate screen is a later sample-selection rule, not a
pre-treatment match characteristic.

The paper and replication output should report:

- the exact distance metric, tie rule, and event ordering;
- candidate stores before and after every exclusion;
- selected control stores and setup-date gaps;
- whether matching is with or without replacement;
- geographic distances and local-market overlap;
- pre-match and post-match store/event balance;
- customer counts after the five-day and 80% rules;
- sensitivity to alternative orderings, matching with replacement, more store
  covariates, calipers, and propensity/reweighting approaches.

Save an event-level `control_match_audit.csv` containing candidate-pool counts,
each candidate's distance and exclusion reason, final rank, and selected flag.
Replace “ensures comparability” with a factual description of the implemented
match, followed by the balance evidence.

# Part II. Identification and inference

## July 26, 2026 implementation update

The Part II revision was deliberately narrower than the full menu originally
listed below. The production 18-event workflow now clusters inference by
`closure_event_id`, reruns purchase frequency, purchase incidence,
novelty-seeking and new-product-seeking, and records the clustering choice in
the run manifest. The 18-event registry, classifier scores, fixed effects,
event windows and pooled DDD estimand are unchanged. The headline DDDs under
closure clustering are:

| Outcome | DDD | SE | p-value |
|---|---:|---:|---:|
| Purchase frequency | 0.0058 | 0.0032 | 0.086 |
| Novelty-seeking | -0.0415 | 0.0184 | 0.038 |
| New-product-seeking | -0.0417 | 0.0090 | <0.001 |

The manuscript now uses a short assumption-to-evidence discussion rather than
the full map proposed in Section 9, qualifies the closure variation as
plausibly external, and reports the following verified design facts: each
customer appears in one event, treated stores are never controls, closure
windows overlap in calendar time, and pooled estimates weight events through
their customer-period observations. It mentions the cross-store exclusion
only as a post-treatment sample restriction.

The appendix now shows the novelty DDD event-study path with 95% confidence
intervals and reports common-support estimates using the same closure-clustered
inference. The matched purchase DDD changes sign (-0.0041, p=0.156); the
matched novelty DDD is about half the full-sample magnitude (-0.0211, p=0.295).
These results are presented as adverse or inconclusive diagnostics rather than
as supporting evidence.

At the author's direction, the few-cluster extensions listed below---wild
cluster bootstrap, CR2, randomization inference, two-way clustering and related
exercises---are not part of this implementation round.

The July 26 follow-up also replaces the broad twelve-row pretrend summary with
a focused novelty-seeking exhibit. The appendix now states the event-study
equation and joint null, reports the three lead coefficients with standard
errors and confidence intervals, gives the joint Wald statistic, and retains
the full coefficient-path figure. Purchase frequency's adverse DDD pretrend
and the new-product-seeking and continuous-score tests remain visible in the
surrounding prose. The plotting pipeline now uses the confidence limits
reported by the clustered estimator instead of reconstructing intervals with
a hard-coded normal critical value. With this presentation repair, the agreed
core Part II scope is complete; the few-cluster extensions remain explicitly
deferred.

## 9. Replace a generic assumptions section with an assumption-to-evidence map

Organize the section as:

| Assumption | Threat in this setting | Direct diagnostic | Remaining limitation |
|---|---|---|---|
| Closure timing is unanticipated and not outcome-targeted | Announced or systematic operational closures | Cause/announcement registry; lead behavior; exclude planned events | Unobserved local shocks |
| Treated and matched-control paths are parallel | Store/customer differences | Four-cell event studies with CIs | Low power with 18 events |
| General closure effects are comparable across predicted-incidence groups | High group differs in engagement and baseline demand | Matched/reweighted high-low design; bias sensitivity | Not proven by treated-control balance |
| Predicted-incidence classification transports across arms/events | Misclassification/calibration drift | Event/duration calibration; threshold and score sensitivity | Generated-group uncertainty |
| Controls are not contaminated | Diversion to nearby open stores | Distance exclusions; traffic/spillover tests | Network interference |
| Selection into the novelty sample is stable or addressed | Purchase-conditioned novelty | Purchase-probability DDD; unconditional outcomes; bounds | Principal-stratum interpretation |
| Product environments are comparable | Promotions, recommendations, availability | Store-period assortment/promotion controls | Unobserved exposure |
| Inference reflects treatment assignment | Only 18 common shocks | Event clustering, wild bootstrap, randomization inference | Few-cluster uncertainty |

Do not treat one diagnostic as validating a different assumption:

- covariate balance is not a parallel-trends test;
- the closure-period first stage is not a test of comparable general closure
  effects;
- nonrejection of pretrends is not classifier validation;
- feature importance is not proof of a psychological “active goal.”

## 10. Document closure exogeneity and anticipation

The paper calls closures “unexpected” and “exogenous” more strongly than the
current evidence supports. For every candidate event, record:

- closure cause;
- source;
- announcement date/time;
- scheduled versus emergency status;
- relation to local COVID restrictions;
- reopening information;
- nearby store closures;
- local promotion or assortment changes.

Show estimates:

- excluding announced/planned closures;
- excluding periods immediately before closure;
- with local date/geography controls;
- leaving each event out.

Until that evidence is presented, use “plausibly external operational
disruptions” rather than an unqualified “exogenous shocks.”

## 11. Show, do not summarize, the pretrend evidence

Current joint tests include:

| Outcome/specification | Pretrend p-value |
|---|---:|
| Purchase, overall ATT | 0.979 |
| Purchase, baseline/low | 0.604 |
| Purchase, high-minus-low displacement | 0.035 |
| Purchase, continuous score | 0.050 |
| Member-first novelty, overall ATT | 0.121 |
| Member-first novelty, baseline/low | 0.188 |
| Member-first novelty, displacement | 0.841 |
| Member-first novelty, continuous score | 0.619 |
| First-observed-sale novelty, overall ATT | 0.398 |
| First-observed-sale novelty, baseline/low | 0.991 |
| First-observed-sale novelty, displacement | 0.114 |
| First-observed-sale novelty, continuous score | 0.377 |

Under closure-clustered inference, the purchase high-minus-low pretrend rejects
at 5% and the continuous-score pretrend is borderline. The novelty DDD
pretrends do not reject; the revised appendix shows its coefficient path and
confidence intervals.

Required changes:

- put four-cell raw paths and DDD coefficient event studies with 95% CIs in the
  paper;
- report every lead coefficient, joint statistic, degrees of freedom, and
  number of clusters;
- say “does not reject,” never “passes” or “confirms”;
- discuss power and economically meaningful confidence intervals;
- add alternative trend controls, shorter prewindows, placebo dates, and
  leave-one-event-out paths;
- consider a formal sensitivity analysis such as HonestDiD.

The purchase result should be supporting/descriptive unless the pretrend
problem can be resolved.

## 12. Report the existing common-support results

The technical report contains diagnostics that are currently omitted from the
paper:

| Outcome | Full-sample DDD | Matched DDD | Matched pretrend |
|---|---:|---:|---:|
| Purchase frequency | +0.0058, \(p=.086\) | -0.0041, \(p=.156\) | \(p=.069\) |
| Member-first novelty | -0.0415, \(p=.038\) | -0.0211, \(p=.295\) | \(p=.871\) |

The matched novelty estimate is smaller and imprecise. The matched purchase
estimate changes sign and is accompanied by a rejected pretrend. These are
central assumption diagnostics, not optional technical details.

Report them transparently, explain the support restriction, show score overlap,
and avoid treating a linear “bias equality” nonrejection as proof that the
comparable-general-effect assumption holds.

## 13. Repair inference for 18 common shocks

The production configuration now clusters by `closure_event_id`, addressing
correlation induced by the common closure-level treatment shock. There are 18
headline events. The remaining items in this section are optional extensions
and were left unchanged in the July 26 implementation round at the author's
direction.

At minimum report:

1. closure-event-clustered inference;
2. two-way member and closure-event clustering, if supported and stable;
3. a few-cluster correction such as wild-cluster bootstrap or CR2;
4. event-level randomization/permutation inference using the actual matched
   assignment structure, where defensible;
5. leave-one-closure-out estimates;
6. equal-event-weighted and current customer-weighted estimates.

State the number of clusters in every table. For event-level variables such as
duration, never use thousands of repeated customer rows to create artificial
precision.

Classifier estimation creates another uncertainty layer. Use event-level
sample splitting/cross-fitting and bootstrap the classifier-plus-DDD pipeline,
not merely the second-stage regression, as a sensitivity analysis.

## 14. Clarify the stacked event design and weights

The current fixed effects are:

- customer-closure episode;
- relative period;
- calendar month.

Add or justify matched-closure-set-by-relative-period effects so treated and
control episodes are compared within the same event-specific calendar
environment. Explain:

- whether a customer can appear in multiple events—the current main sample
  happens not to, but this should be an explicit rule;
- whether control stores can later be treated;
- how overlapping closure windows are handled;
- whether control episodes are exposed to another closure;
- whether the pooled estimate weights events by customers, observations, or
  another implicit FE weight.

Provide an event-weight decomposition and equal-event-weighted robustness.

## 15. Address spillovers and treatment versions

Closures can divert customers to other chain stores and can increase traffic at
matched controls. This violates a simple no-interference assumption.

Estimate:

- focal-store purchase days;
- other-chain-store purchase days;
- total-chain purchase days;
- substitution probability during closure;
- distance-based control exclusions;
- results excluding control stores near the closed store;
- local traffic changes at control stores.

Do not use the exclusion of treated customers who buy at another store during
closure as mechanism proof. It conditions on post-treatment behavior and is
only a sample-restriction robustness check.

## 16. Multiple outcomes and specification hierarchy

Declare:

- one primary outcome;
- one primary predicted-incidence specification;
- one primary horizon;
- primary versus robustness novelty definitions;
- confirmatory versus exploratory heterogeneity tests.

Report family-wise or false-discovery-rate adjustments across the confirmatory
family. The code documentation says event studies are primary and collapsed
models supplementary, while the manuscript centers the collapsed model. Align
the hierarchy across code, paper, and replication documentation.

# Part III. Purchase-incidence classifier

## July 26, 2026 implementation update

The agreed classifier-reporting pass is complete. It uses the saved row-level
predictions and does not retrain a classifier or rerun the main DDD estimates.
`scripts/writeup/generate_classifier_diagnostics.py` restricts the prediction
panels to the exact final 18-event registry and 40,148 final episodes, explicitly
selects only durations present in that registry, and separately evaluates
treated period −1, control period −1 and control period 0. The script writes
machine-readable overall, duration, event, threshold, calibration and overlap
files plus an input-checksum manifest under `outputs/paper/classifier/`.

The exact-cohort headline diagnostics are:

| Evaluation slice | N | Prevalence | ROC-AUC | PR-AUC | Brier | Calibration slope |
|---|---:|---:|---:|---:|---:|---:|
| Treated, pre-period −1 | 7,390 | 0.314 | 0.818 | 0.697 | 0.162 | 0.537 |
| Control, pre-period −1 | 32,758 | 0.308 | 0.814 | 0.677 | 0.164 | 0.536 |
| Control, period 0 | 32,758 | 0.263 | 0.781 | 0.583 | 0.172 | 0.471 |

The results support a qualified conclusion. The classifier ranks purchase
incidence meaningfully: for period-0 controls, PR-AUC is 0.583 against 0.263
prevalence, and the Brier score improves from 0.194 under a constant-prevalence
prediction to 0.172. It is nevertheless overconfident. Mean period-0 control
predicted incidence is 0.307 versus 0.263 observed, and the calibration slope
is 0.471 rather than one. At the 0.5 cutoff, sensitivity is 0.548, specificity
is 0.830, positive predictive value is 0.534 and accuracy is 0.756 versus 0.737
for an always-negative rule. Period-0 control ROC-AUC ranges from 0.739 to 0.794
across the production-duration models, while calibration slopes range from
0.331 to 0.592.

The manuscript now describes the classifier as informative but imperfect,
replaces the opaque weighted-average table with exact-cohort discrimination and
calibration metrics, and adds detailed confusion matrices, calibration plots,
duration-specific results, predictive cutoff tradeoffs and treatment-control
score overlap to the appendix. The two remaining classifier/figure labels now
say ``predicted purchase incidence.'' Feature rankings were removed from the
main performance table because they do not validate a psychological construct.

The implementation also consolidates the threshold key: both training-output
and ex-ante scoring code now read `model.decision_threshold` and validate its
range. Duration-25 sensitivity artifacts remain in the shared classifier
directory, but the diagnostic manifest excludes them because duration 25 is not
in the final registry. The continuous-score DDD remains in the paper and avoids
the binary cutoff. A DDD outcome sensitivity over alternative binary cutoffs,
event-level cross-fitting and a bootstrap of the entire classifier-plus-DDD
pipeline remain possible later extensions; they were not required for this
classifier-performance pass.

## 17. Use construct-valid language

The model predicts purchase incidence from observed behavior. It does not
directly observe a plan, intention, or active psychological goal.

Preferred terms:

- predicted purchase probability;
- high/low predicted purchase incidence;
- likely interrupted purchase opportunity for treated-high episodes.

“Purchase intention” can be introduced as an operational proxy, with an
explicit construct-validity limitation. Do not infer an active goal from
feature importance.

## 18. Report complete predictive performance

The original table emphasized accuracy, precision, recall, F1, and feature
importance. The revised table and appendix now report the exact-cohort
discrimination, calibration, base-rate and confusion-matrix evidence described
above.

Implemented on the exact final estimation cohort:

- positive-label prevalence;
- always-negative accuracy;
- confusion-matrix counts;
- sensitivity/recall and specificity;
- false-positive and false-negative rates;
- positive and negative predictive value;
- ROC-AUC;
- PR-AUC;
- Brier score;
- calibration intercept/slope and calibration plot;
- performance by treatment arm, event, closure duration, and score decile.

Training counts and positive cases remain in the duration-level classifier
audit artifacts rather than the manuscript because they describe model fitting
rather than the final-cohort validation population. The earlier weighted
\(N=81,624\) row and its weighted-average F1 were removed. The paper now uses
exact-cohort metrics calculated from the pooled row-level predictions within
each evaluation slice.

## 19. Thresholds, calibration, and generated classification

The 0.5 cutoff is a fixed interpretive rule, not an empirically unique optimum.
The revised appendix reports its sensitivity-specificity tradeoff against
cutoffs from 0.3 to 0.7 and retains the continuous-score DDD. This predictive
cutoff table is not a substitute for rerunning the outcome model across the
same grid if binary-threshold robustness becomes a priority.

Current status:

- `decision_threshold` is now the single validated configuration key;
- predictive classification tradeoffs are reported over a 0.3--0.7 grid;
- the continuous centered-score specification is retained and its baseline
  interpretation is stated;
- treatment-control score overlap is shown;
- DDD outcome estimates over the threshold grid and any associated trimming
  remain unimplemented extensions.

Possible later extensions following the reference paper are:

- control episodes whose predicted closure-period status matches observed
  status;
- false-positive/false-negative sensitivity;
- misclassification bounds or simulation;
- whole-pipeline bootstrap/cross-fitting.

# Part IV. Tables and figures

## July 26, 2026 implementation update

The exhibit audit was rechecked against the current manuscript rather than
applied mechanically to the earlier draft. The current status is:

- **Table 1 substantially resolved.** It is now a four-cell descriptive table
  with episode counts, means, standard deviations and the pre-period share of
  windows containing a purchase. Stars and customer-level inference on closure duration were
  removed, and the text discusses the important level differences. A separate
  event-level store-matching exhibit remains an optional appendix addition.
- **Figure 1 resolved for the current draft.** The raw purchase-frequency paths
  now report closure-clustered 95% confidence intervals, group sizes,
  customer-weighted pooling, closure-window shading and the chain-wide outcome
  scope. The text quantifies the period -1, closure-period and period +1 means.
- **Table 2 resolved in Part III.** It now reports exact-cohort ranking,
  calibration and probability-loss metrics; feature importance is no longer
  presented as construct validation.
- **Figure 2 resolved for descriptive use.** The four raw novelty paths now
  report closure-clustered 95% confidence intervals and observed-window count
  ranges. The text explicitly treats the paths as intuition rather than the
  causal estimate.
- **Purchase probability added to the appendix.** A four-cell event-time plot
  reports the realized probability of at least one purchase, closure-clustered
  intervals, cell sizes and customer weighting. This probability also
  determines entry into the novelty-seeking sample. The main text refers to it
  and retains a conditional-on-purchase interpretation. A final-inference
  purchase-probability DDD, unconditional exploration outcomes and bounds
  remain Part I extensions, not claims made by the current exhibit.
- **Table 3 resolved.** The main table separately reports low-group,
  high-group and high-minus-low effects with covariance-aware standard errors,
  model metadata and closure-event clustering; the common high post shift is
  in the appendix.
- **The old Table 4 diagnosis is obsolete.** The main text now gives a short
  continuous-score robustness discussion, while the appendix reports complete
  binary and continuous specifications and the separately named
  new-product-seeking outcome.
- **The old Table 5 claim is withdrawn and Section 22 is resolved as an audit
  artifact.** Restoring the omitted lower-order interaction eliminates the
  apparent type difference. At the author's July 26 request, neither the
  corrected null nor the invalid legacy estimate is displayed in the current
  manuscript. The saturated estimates, support, pretrend tests and
  leave-one-closure-out diagnostics remain saved under
  `outputs/paper/heterogeneity_audit/` for later reconsideration.
- **The old Appendix B1 diagnosis is resolved.** The appendix now shows the
  novelty DDD pretrend coefficients, confidence intervals, joint test and full
  event-study path rather than only a p-value summary.

The figure source values are saved in
`outputs/paper/descriptives/raw_purchase_paths.csv`,
`outputs/paper/descriptives/raw_novelty_paths.csv` and
`outputs/paper/descriptives/purchase_probability_paths.csv`. They are generated
by `scripts/writeup/generate_paper_exhibits.py`; no main estimation model was
changed.

## 20. Exhibit-by-exhibit audit

The entries below record the problems in the audited draft. Use the July 26
status above to distinguish resolved items from remaining work.

### Table 1: current “balance” table

**Message currently visible:** treatment and control episodes look close on a
small set of variables.

**Problems:**

- it is not a summary-statistics table;
- it omits the four DDD cells;
- event duration is repeated at customer level;
- stars reflect huge customer counts rather than the 18-event design;
- the rounded means 0.050 and 0.046 do not visibly reconcile with the displayed
  difference \(-0.003\);
- significant baseline differences are under-discussed.

**Fix:** add the four-cell table described above, use standardized differences,
move event variables to an event-level match table, retain unrounded
calculations, and state weighting and inference.

### Figure 1: raw closure shock in purchase frequency

**Message:** the closure binds during period 0 and purchase-day frequency
returns near the comparison path after reopening.

**Problems:** no uncertainty, cell counts, weights, event-level variation, or
outcome-store scope.

**Fix:** add 95% intervals, \(N\), event weighting, closure-period shading, and
the exact focal-versus-chain definition. Quantify rather than visually assert
recovery.

### Table 2: classifier performance/importance

**Message:** recent behavior predicts near-term purchase incidence.

**Problems:** incomplete predictive metrics; accuracy lacks a base-rate
benchmark; feature importance is treated as construct validation; duration
model aggregation is unclear.

**Fix:** add the metrics in Section 18, normalize importance to gain shares,
state aggregation rules, and separate predictive validity from psychological
interpretation.

### Figure 2: novelty paths by predicted incidence

**Message:** the raw four-cell paths motivate the DDD.

**Strength:** this is the most intuitive bridge from design to result.

**Problems:** novelty is conditional on purchase; no intervals, observation
probabilities, cell sizes, or visible closure break.

**Fix:** show CIs and \(N\), pair it with the realized purchase-probability plot
that determines novelty-sample entry, state the selected-outcome
interpretation, and make it supporting intuition rather than the causal
estimate.

### Table 3: main results decomposition

**Message:** low-group effect, common high post shift, high-minus-low
differential, and implied high-group effect.

**Problems:** the high-group effect lacks an SE; prose mislabels the DDD; units,
window range, fixed effects, cluster count, premean, weighting, and selection
are incomplete.

**Fix:** follow the separate headline-coefficient audit. Prefer:

- Panel A: low and high treatment effects, each with SE/CI;
- Panel B: high-minus-low DDD with SE/CI;
- move the common high post shift to the appendix.

### Table 4: robustness

**Message:** novelty results are similar across binary, score, market-new, and
cross-store restrictions.

**Problems:** it combines terms from different models in one estimate column;
missing model-specific \(N\), within-\(R^2\), fixed effects, centering, and
premeans; “market-new” is inaccurately named.

**Fix:** use separate panels/columns for binary and continuous-score models,
report the complete model metadata, rename first-observed-sale novelty, and
identify post-treatment sample restrictions.

### Table 5: pre-novelty heterogeneity

**Message:** the DDD differs sharply by baseline novelty type.

**Problems:** implied high-type effect has no uncertainty; missing subgroup
counts, premeans, cutoff, raw paths, and leverage diagnostics; model is
incompletely saturated; type is constructed from the same outcome.

**Fix:** use a fully saturated specification, covariance-aware group effects,
longer/cross-fitted type measurement, continuous interactions, a coefficient
plot, subgroup support, and exploratory language.

**July 27 resolution:** the manuscript does not restore the old Table 5. It
reports one continuous baseline-novelty coefficient in the mechanism section's
prose, with its closure-clustered standard error and theory-signed one-sided
p-value. The complete split, metric, window and functional-form searches are
saved outside the manuscript.

### Appendix Tables A1–A3

**Problems:** useful but not referenced from the main paper; A1 does not fully
bridge sample attrition; A2's outcome descriptions are inaccurate; A3 lacks
enough support information.

**Fix:** cite each appendix exhibit at the relevant main-text claim, correct
definitions, and replace A1 with the generated event/customer/outcome sample
flow.

### Appendix Table B1

**Message:** joint pretrend tests.

**Problem:** central identification evidence is reduced to p-values and mostly
hidden.

**Fix:** put coefficient event studies with CIs in the main paper; retain the
full test statistics and alternative specifications in the appendix.

## 21. Recommended exhibit sequence

1. Setting timeline and closure first stage.
2. Event/customer/outcome sample flow.
3. Four-cell summary table plus store-event matching table.
4. Classifier performance and calibration.
5. Four-cell raw purchase and novelty paths.
6. Purchase-probability paths governing entry into the novelty sample.
7. DDD coefficient event studies.
8. Main low/high/DDD results table.
9. Robustness table with distinct model panels.
10. Baseline-novelty mechanism estimate in prose; rejected heterogeneity plots
    remain in the private working archive.

Every table note should define:

- outcome and units;
- analysis population;
- omitted cell;
- estimand;
- window;
- fixed effects;
- weights;
- missing-outcome treatment;
- cluster variable and number of clusters.

Captions should state the substantive message; notes should explain
construction.

# Part V. Heterogeneity, mechanisms, and model

## 22. Repair the heterogeneity specification and interpretation

**July 26 implementation update.** The diagnosis below applied to the legacy
specification. The production model and manuscript now include the omitted
`Post × pre-novelty type` term and all other lower-order terms implied by the
four-way interaction. Algebraically equivalent saturated parameterizations
estimate both subgroup DDDs and all four treated-control post contrasts with
their own covariance-aware standard errors. The corrected estimates are:

- low-pre-novelty DDD: -0.0257 (SE 0.0244; 95% CI [-0.0772, 0.0258]);
- high-pre-novelty DDD: -0.0131 (SE 0.0169; 95% CI [-0.0486, 0.0225]);
- high-minus-low pre-novelty difference: 0.0126 (SE 0.0237; p = 0.601);
- continuous pre-novelty slope: 0.0179 per unit (SE 0.0335; p = 0.600).

Treating the last two rows as a family of alternative heterogeneity tests gives
Holm-adjusted p-values of 1.000 for both.

The legacy magnitudes (-0.263 for the low type and +0.492 for the high-type
increment) were artifacts of the omitted lower-order interaction: in the
saturated model, that omitted `Post × type` coefficient is -0.4815 (SE
0.0091). The three subgroup event-study pretrend tests do not reject (p =
0.913 for the low type, 0.832 for the high type and 0.859 for their
difference). Leaving out one closure at a time keeps both subgroup DDDs
negative but small: [-0.0416, -0.0155] for the low type and [-0.0236, -0.0057]
for the high type. Thus the original heterogeneity claim does not survive the
specification correction.

At the author's July 26 request, the main text stopped using this corrected
median-split exercise as evidence for goal persistence. An initial revision
placed the corrected null in the appendix, but it was removed and kept as a
separate audit artifact instead. The July 27 continuous redesign described
below does not reinstate the rejected split. The reproducible split diagnostic is
`scripts/writeup/validate_pre_novelty_heterogeneity.py`; its manifest, exact
formulas, estimates, support cells, event-study results and event-leverage
outputs are in `outputs/paper/heterogeneity_audit/`. No classifier was
retrained and no main DDD estimate was changed.

A follow-up diagnostic tests whether the pre-novelty split is mechanically
related to sparse purchase histories. Its script is
`scripts/writeup/diagnose_pre_novelty_purchase_counts.py`, and its episode,
group, order-count and single-order outputs are stored in the same audit
directory. High-pre-novelty episodes average 4.29 pre-period orders versus 6.96
for low-pre-novelty episodes, and 30.5% versus 16.7% have exactly one
pre-period order. A second fully saturated sensitivity raises the minimum
pre-period order count from one through eleven. The general post-type shift
falls from -0.482 to -0.201, confirming that sparse histories explain a
substantial part of the extreme movement, but the type difference in the DDD
does not reject at any threshold (all p-values at least 0.247). The script is
`scripts/writeup/diagnose_pre_novelty_minimum_orders.py`; its coefficient table
and interpretation note are stored in the audit directory. These diagnostics
are not part of the paper.

A July 26 follow-up constructs the type over five alternative histories: the
existing periods -4 through -1, overlapping eight- and twelve-period
histories, and non-overlapping histories covering -8 through -5 or -12 through
-5. Each is crossed with minimum-order screens of 1, 3, 5, 10, 15, and 20 and
estimated as both a median split and a continuous interaction. The preferred
non-overlapping eight-period definition without an extra activity screen is
null: the high-minus-low DDD is -0.0167 (SE 0.0277; p = 0.555). Across the 56
identified type-difference tests, all Holm-adjusted p-values equal 1.000.

One post-hoc cell is nominally significant: the non-overlapping four-period
history with at least 15 orders gives a binary difference of -0.3024 (SE
0.1254; p = 0.027) and a continuous slope of -0.4794 (SE 0.2062; p = 0.033).
It is stable to leave-one-closure deletion and its difference-path joint
pretrend test does not reject (p = 0.583), but the binary split has only 346
high-type episodes and just 13 high-type, treated, low-predicted-incidence
episodes spanning six closures. More importantly, redefining high type at the
screened-sample median changes the binary difference to -0.0481 (SE 0.0915; p
= 0.606). Novelty remains negatively related to prior order count, and
adjacent four-period measures correlate only about 0.32. Longer histories
therefore improve availability but do not produce stable affirmative
heterogeneity evidence. The complete grid, support checks, threshold
sensitivity, event study, and closure-deletion results are stored under
`outputs/paper/heterogeneity_audit/long_pre_window/`; the reproducible scripts
are `scripts/writeup/build_long_pre_novelty_traits.py`,
`scripts/writeup/estimate_long_pre_novelty_heterogeneity.py`, and
`scripts/writeup/audit_long_pre_novelty_window.py`. These results remain
outside the paper.

Cross-fitting or shrinkage remains a possible redesign of the baseline trait.
The July 26 corrected split is null; the later continuous result below uses a
longer history and an order-count adjustment but is not cross-fitted.

A requested extreme-groups follow-up uses the overlapping periods -8 through
-1, requires at least 15 orders, retains only the bottom and top novelty
quartiles, and drops the middle half. The resulting low- and high-quartile
DDDs are 0.0167 (SE 0.0689; p = 0.811) and -0.0909 (SE 0.0790; p = 0.266).
Their difference is -0.1076 (SE 0.0904; 95% CI [-0.2984, 0.0831]; p =
0.250). Moreover, the joint pretrend test for the difference path rejects (p
= 0.023). This restriction therefore does not improve the heterogeneity
evidence. Exact outputs are the `overlap8_min15_extreme_quartile_*` files in
the long-window audit directory, generated by
`scripts/writeup/estimate_overlap8_extreme_quartile_heterogeneity.py`.

**July 27 continuous-mechanism decision.** After the grouping and metric
searches, the author selected a continuous specification for the mechanism
section. Baseline novelty-seeking is the episode-level mean of within-period
novelty-seeking over relative periods -8 through -1. These are eight
closure-length periods, not calendar weeks. Eligible episodes must contain at
least five baseline orders. Baseline novelty and `log(1 + baseline orders)` are
standardized, and the collapsed DDD includes the complete lower-order
interaction hierarchies for both variables.

The coefficient on
`Post × Treated × High predicted incidence × baseline novelty` is 0.0294 per
one-standard-deviation increase in baseline novelty (closure-event clustered
SE 0.0147; one-sided p = 0.031 for the model-predicted alternative that the
coefficient is positive). The continuous event-study interaction does not
reject the joint pretrend for periods -4, -3 and -2 (p = 0.561). The trait
and order restriction identifies 18,525 episodes; 17,866 have an observed
novelty outcome before fixed-effect singleton removal, and the regression uses
79,578 observations. The result's sign means that the interruption-related
novelty DDD is more negative among consumers with lower baseline novelty,
matching the familiar-choice-salience prediction.

The maintained estimator is
`scripts/writeup/estimate_baseline_novelty_mechanism.py`; its formula,
standardization constants, complete coefficient vector, support, event study,
pretrend test and manifest are in
`outputs/paper/mechanism_baseline_novelty/`. The mechanism section now defines
the trait, shows its frequency distribution, states the exact saturated
econometric specification and presents an inline table with the mean-trait DDD
and the baseline-novelty gradient. An appendix figure shows the corresponding
event-study path and confidence intervals. The manuscript reports CRV1
closure-clustered inference and the theory-directed one-sided p-value for the
gradient. It does not display alternative inference estimators, grouping
rules, nonlinear diagnostics or rejected specifications.

For reproducibility, the two period-level component files used by the accepted
estimator are copied into
`outputs/paper/mechanism_baseline_novelty/inputs/`. The broader split, window,
metric and functional-form searches remain in ignored private archives on the
remote analysis machine and are not part of the paper artifact.

**July 27 baseline-order-adjustment addendum.** The maintained estimator now
also records model-free evidence on why baseline order history enters the
preferred specification. Across the 18,525 eligible episodes, the Pearson
correlation between baseline novelty and log(1 + baseline orders) is -0.329.
Mean baseline novelty is 0.620 for episodes with exactly five orders and 0.365
for episodes with at least 20 orders; the share at novelty equal to one falls
from 19.3% to 0.1%. The manuscript presents this as an association that may
combine genuine behavioral differences with finite-history measurement.

For transparency, the appendix now reports an otherwise identical model that
deletes the complete Post-by-baseline-order interaction hierarchy. The
baseline-novelty gradient remains positive at 0.0229 (closure-clustered SE
0.0143), but its one-sided p-value rises to 0.064; its joint pretrend p-value
is 0.409. The direction and approximate magnitude therefore survive, but the
no-adjustment result does not meet the 5% one-sided threshold. Exact
no-adjustment coefficients, event-study path, pretrend test, raw order
diagnostic and side-by-side comparison are now stable outputs under
outputs/paper/mechanism_baseline_novelty/, rather than only temporary
exploration files.

Notation follows the main DDD throughout: `Post`, `Treated`, `High`,
`delta^B`, `beta` and `delta^D` retain their meanings from the main equation,
and `theta^D` denotes only the new baseline-novelty gradient of `delta^D`.

The added descriptive exhibit verifies that the raw trait spans 0 to 1 across
18,525 eligible episodes (mean 0.508, SD 0.269, median 0.500, p10 0.167 and p90
0.889). The regression sample contains 79,578 purchasing-period observations.
All four treatment-by-predicted-incidence cells retain all 18 closure events.
The maintained estimator writes the descriptive summary, ten-bin frequency
distribution and headline table inputs alongside the coefficient and
event-study files, so every number displayed in the new subsection is tied to
the accepted script rather than calculated manually.

The manuscript also labels the heterogeneity evidence exploratory because the
trait construction was selected after examining alternatives. This preserves
the mechanism interpretation without presenting the directional p-value as a
pre-specified confirmatory test.

For audit completeness, the broader search remains important. None of the 216
initial continuous specifications has a positive coefficient with a
conventional two-sided p-value below 0.05. An exact-period-length extension
produced a raw-significant two-period result, but that specification is
rejected because its joint pretrend fails (p = 0.000739), its relationship is
quadratic and non-monotone, and stricter two-period samples have critically
thin treated, low-incidence support. The selected eight-period result does not
survive a family-wide correction across the exploratory grid. These rejected
results, the alternative-inference calculations and the complete grouped-type
search are preserved in `tmp/pre_novelty_heterogeneity_archive/`, whose README
also corrects temporary `weeks_*` labels to relative-period terminology.

### Legacy diagnosis

The heterogeneity equation omits a `Post × H` lower-order interaction. A
saturated model should include all lower-order terms implied by the displayed
higher-order interactions, or the paper must defend the restriction.

Additional problems:

- baseline type uses pre-period values of the same noisy outcome;
- type availability selects purchase-active customers;
- regression-to-the-mean is likely;
- low- and high-type purchase frequency differs substantially
  (approximately 0.0966 versus 0.0537 in the median-split diagnostic);
- the implied high-type effect lacks an SE;
- the displayed \(-0.263+0.492=0.229\) can appear as 0.230 because of component
  rounding.

Fixes:

- measure type in a separate, longer initialization window;
- use empirical-Bayes/shrunken or cross-fitted baseline novelty;
- prefer a continuous interaction;
- show raw subgroup distributions and paths;
- report type threshold, counts, premeans, effect/SE/CI for every group;
- run placebo heterogeneity in preperiods;
- report event leverage and multiple-testing adjustment;
- label the analysis exploratory.

The legacy positive high-type total created a tension with the formal model's
assumption \(\lambda^L>\lambda^H\ge0\). That tension was itself an artifact of
the incomplete specification: both corrected subgroup point estimates are
negative, and neither differs statistically from zero or from the other.

## 23. Do not overstate mechanism evidence

The observed DDD is consistent with several channels:

- goal persistence/focused completion;
- missed assortment exposure;
- recommendation changes;
- promotions;
- habit or routine disruption;
- inventory and product availability;
- post-closure selection into purchasing.

The current data do not directly observe the intended product, goal salience,
awareness, or counterfactual thinking.

Use “consistent with” rather than “shows” or “demonstrates.” Stronger mechanism
claims require outcomes such as:

- return to the exact pre-closure favorite product;
- intended-item or basket similarity;
- time to first post-reopening purchase;
- substitution during closure followed by return;
- exposure to and adoption of products introduced during closure;
- promotion/recommendation controls.

The existing missed-new-product analysis finds no clear cross-event pattern in
the predicted direction. Report it as a weak/null descriptive mechanism check
or omit it; do not claim that it rules out exposure without the coefficient,
SE, plot, and power discussion.

The cross-store-buyer exclusion conditions on a treatment response. Keep the
full-sample intention-to-treat estimate primary and label the exclusion only as
a post-treatment sample-restriction sensitivity.

The stated 519 treated episodes—about 7%—with a during-closure purchase at
another chain store also needs a reproducible descriptive exhibit. Define the
store universe and denominator, show the rate by predicted-incidence group and
event with uncertainty, and compare it with control behavior. Substitution may
itself be informative: test whether high-predicted-incidence customers
disproportionately switch stores during closure and whether they subsequently
return to their prior store or favorite product.

**Manuscript decision (July 27).** The same-chain substitution subsection has
been removed from the paper. Its 7% descriptive rate and post-treatment
exclusion did not establish the proposed mechanism, and presenting them without
the event-level and control comparisons above was uninformative. This evidence
remains part of the audit trail and can be restored only after a reproducible,
properly benchmarked substitution analysis is completed.

## 24. Shorten and discipline the conceptual framework

The model occupies a large share of the paper before the data and assumes signs
that are not fully supported by the results. A more effective structure is:

- one to two pages of conceptual intuition;
- two or three explicit predictions;
- a table mapping each prediction to an empirical test and competing
  explanations;
- formal derivations in an appendix.

Resolve the prose/formal inconsistency over purchase frequency: one passage says
the mechanism predicts no substantial decline, while another says the model
has no signed frequency prediction.

Remove revision residue such as “remove notation” and hidden substantive
`\iffalse` blocks. The main text refers to a missed-exposure mechanism while
parts of its empirical discussion are hidden in source.

# Part VI. Writing and consistency

## 25. Abstract, introduction, and conclusion

### Title

The current title is a reasonable length, but it does not identify product
exploration/novelty even though that is the paper's main outcome. Consider a
title that names both the temporary supply disruption and the product-choice
margin. Finalize it only after deciding whether the empirical scope is
focal-store or chain-wide.

### Abstract

Current problems:

- approximately 207 words and diffuse;
- no coefficient with uncertainty;
- “exogenous” and “lasting” overclaim;
- says 800,000 consumers rather than the audited count;
- inherits the headline estimand error;
- mechanism language is too certain.

Target approximately 150 words:

1. question and setting;
2. design and identifying comparison;
3. correctly labeled primary estimate with uncertainty;
4. one identification caveat;
5. restrained mechanism interpretation.

### Introduction

Fix:

- “770,00”;
- “during the COVID-19 pandemic”;
- the high-group/DDD estimand;
- the thin comparison with the closest paper;
- missing roadmap and contribution hierarchy.

State exactly how the paper differs from Levine–Hristakeva: outcome, setting,
four-cell design, classifier, conditional novelty issue, and what evidence is
new.

### Conclusion

Report the principal magnitudes, distinguish direct group effects from the DDD,
and restate the main limitation. Remove untested managerial recommendations and
claims about persistent aggregate demand or product discovery that exceed the
measured window and outcome.

## 26. Adopt one lexicon

Use:

| Concept | Preferred term |
|---|---|
| Person | customer, unless “member” is required by a variable name |
| Unit | customer-closure episode |
| Prediction group | high/low predicted purchase incidence |
| Treatment cell | treated-high episode or likely interrupted opportunity |
| Main choice outcome | novelty-seeking (new to the customer's own observed history) |
| Robustness outcome | new-product-seeking (based on recently appearing products) |
| Purchase outcome | purchase-day frequency, with focal/chain scope stated |
| Time | pre-closure, closure, post-reopening |

Avoid switching among:

- consumer/customer/member;
- episode/member-event/member-closure;
- intention/intent/propensity/displacement/active goal;
- novelty/variety/exploration/discovery.

“Blocked” applies only to treated-high episodes. High controls are predicted to
purchase but do not experience the focal closure.

## 27. Narrow claims to measured outcomes and horizons

Do not infer:

- aggregate sales from purchase days;
- quantity or spending from purchase frequency;
- chain demand from a focal-store outcome, or focal-store choice from a
  chain-wide outcome;
- a long-run effect from 40–116 post-reopening days;
- a psychological goal from a purchase-incidence classifier;
- mechanism identification from heterogeneity alone.

Replace vague “lasting” claims with the exact event-time horizon and dynamic
pattern.

## 28. Technical presentation

- Use a separate day index \(d\in\mathcal W_{et}\) rather than reusing \(t\) for
  both event period and calendar day.
- State all denominators and whether products are distinct or
  purchase-instance weighted.
- Prefer vector PDF/SVG figures over PNG when the plotting library supports it.
- Reduce repeated “consistent with” and “counterfactual” phrasing by stating
  the interpretation once and using evidence-specific sentences afterward.
- Check hyphenation, apostrophes, COVID-19 capitalization, and malformed author
  footnotes.

# Part VII. Reproducibility

## 29. Generate every exhibit from immutable results

`scripts/writeup/generate_paper_exhibits.py` currently prints some LaTeX to
standard output, and Table 3 contains manually pasted values.

Required pipeline:

```text
raw/processed inputs
    -> versioned estimation sample and sample-flow audit
    -> versioned coefficient/contrast files
    -> generated CSV and auditable LaTeX snippets
    -> generated figures
    -> verified inline tables in `writeup/main.tex`
```

The paper deliberately keeps tables inline. Do not restore a `tables/` folder
or use `\input{tables/...}`. Generation scripts should write machine-checkable
CSV and optional copy-ready snippets; a build-time check should verify that the
numbers copied into `main.tex` match the immutable result files.

Add a manifest mapping every exhibit to:

- program;
- command;
- input files and checksums;
- output files and checksums;
- original timestamp;
- actual Git SHA;
- software versions;
- sample and specification ID.

Do not rewrite historical commands or timestamps after moving output
directories.

Make the build fail if:

- table sample sizes differ from estimator \(N\);
- a displayed effect lacks uncertainty;
- a table coefficient differs from the saved result;
- outcome labels disagree with configuration;
- classifier threshold keys differ;
- expected closure and cell counts fail.

Add a replication/data-availability statement and one command that regenerates
all paper exhibits.

# Part VIII. Prioritized implementation checklist

## Priority 1: estimand and data integrity

- [x] Decide focal-store versus chain-wide outcome scope.
- [x] Verify that classifier labels, purchase frequency, and novelty use the chosen
      scope.
- [ ] Preserve the 34-row event decision registry and encode the 22-to-18 rule.
- [ ] Generate the complete event/customer/outcome sample flow.
- [x] Correct exact customer, order, line-item, store, and month counts.
- [x] Correct the headline coefficient interpretation using the companion
      audit.

## Priority 2: identification and inference

- [x] Add the novelty DDD coefficient path with 95% CIs to the appendix.
- [ ] Add uncertainty and cell counts to the raw four-cell paths; retain the
      purchase coefficient path as an appendix diagnostic if shown.
- [x] Report the adverse purchase pretrends and matched-support estimates.
- [x] Make closure-event clustering the production inference convention.
- [ ] Add few-cluster corrections and leave-one-event-out estimates if this
      issue is reopened; these were deliberately deferred on July 26.
- [x] State the pooled observation weighting and contamination rules.
- [ ] Report score overlap and fixed-window/equal-event-weight sensitivity.
- [x] Add a brief assumption-to-evidence discussion and remaining limitations.

## Priority 3: descriptive and selection evidence

- [x] Add the compact four-cell summary table.
- [ ] Add the store-event matching table.
- [ ] Add a purchase-probability DDD to complement the completed path figure.
- [ ] Add unconditional new-product outcomes.
- [ ] Add bounds and carefully labeled weighting sensitivity.
- [x] Report the exact heterogeneity-sample selection.

## Priority 4: classifier and mechanisms

- [x] Add exact-cohort classifier discrimination and calibration diagnostics.
- [x] Consolidate the threshold configuration and report predictive cutoff
      tradeoffs.
- [ ] Rerun the DDD outcome models over a binary-threshold grid if this
      robustness exercise is pursued.
- [ ] Bootstrap/cross-fit the generated classification where feasible.
- [x] Saturate and redesign the heterogeneity model; preserve the corrected
      split null in the audit and report the selected continuous result in the
      mechanism section.
- [x] Present the baseline-novelty gradient as mechanism-consistent evidence,
      not a direct measure or unique identification of counterfactual thinking.

## Priority 5: presentation and reproducibility

- [x] Redesign the main tables around four-cell descriptives, classifier
      validation, decomposed DDD effects and continuous heterogeneity.
- [x] Reference and repair the maintained appendix tables and figures.
- [x] Generate and verify every displayed table value while keeping the tables
      inline in `main.tex`.
- [ ] Standardize vocabulary and outcome definitions.
- [ ] Rewrite the abstract, introduction, and conclusion after the empirical
      definitions are frozen.

## Completion standard

The revision is ready for another writing audit when a reader can answer, from
the paper alone:

1. How did 101 detected spells become 18 analysis events?
2. What exactly is a customer, episode, panel row, observed novelty row, and
   regression observation?
3. What are the sizes and pre-period characteristics of all four DDD cells?
4. Is each outcome focal-store or chain-wide, and how is it constructed?
5. Why and when is novelty missing, and what happens on an unconditional
   exploration outcome?
6. Which coefficient is the low effect, high effect, and high-minus-low DDD?
7. What identifying assumption turns the differential into an interruption
   effect?
8. What do the coefficient paths, matched diagnostics, and few-event inference
   show?
9. How accurate and calibrated is the generated prediction group?
10. Which evidence is causal, which is diagnostic, and which is exploratory or
    mechanism-consistent?
