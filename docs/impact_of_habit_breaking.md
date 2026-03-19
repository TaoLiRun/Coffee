# Impact of Habit Breaking: Store Closures and Consumer Purchasing at Luckin

This document describes the analysis of how temporary store closures affect consumer purchasing behavior at Luckin Coffee, in the direction of the identification and decomposition approach in Levine & Hristakeva (2026), *"Stopping Shopping at Stop and Shop? How Temporary Disruptions Affect Store Choice"* (Paper 2). It summarizes **context and identification**, **what has been done**, and **what remains to be done**.

---

## 1. Context and Research Question

### 1.1 Setting

- **Focal firm:** Luckin Coffee (store-level transactions in the data).
- **Shock:** Temporary store closures (e.g., campus/store renovations, operational closures). There are on the order of **~100 closure events** in the sample, with **varying geography, timing, and duration** (e.g., from roughly two weeks to several months).
- **Outcome of interest:** Consumer purchasing at Luckin—frequency, level, and persistence of purchases before, during, and after a closure.

### 1.2 Economic Question

We want to understand:

1. **Overall effect:** Do consumers who lose access to their usual Luckin store reduce purchases during the closure, and do they return to previous levels after reopening?
2. **Mechanism:** Can we separate:
   - **Displacement effect (D):** The effect of *forced non-purchase*—consumers who would have bought during the closure window but could not, and whose habit or state dependence is disrupted.
   - **Baseline-demand effect (B):** Any shift in baseline demand for Luckin (e.g., reputation, alternatives discovered, mentally affected by Covid Lockdown) that affects all exposed consumers regardless of whether they were “displaced.”

As in Paper 2, the displacement effect is the object of interest for **habit/state dependence**: it measures the persistent cost of interrupting a planned purchase, over and above any general demand shift.

### 1.3 Why This Differs from Paper 2

- **Multiple closure events:** We have many closures (different stores, dates, lengths) rather than one strike. This allows stacking consumer–closure observations and exploiting **variation in closure length** and **severity** (share of a consumer’s accessible stores closed).
- **Forced non-purchase vs. store substitution:** In our setting, “treatment” is often loss of access to Luckin at a location (e.g., campus); the relevant margin is “would have purchased at Luckin during the closure window” vs. “would not have,” rather than switching to another grocery chain. The **counterfactual purchase** during the closure is unobservable for treated consumers, so it must be predicted (displacement classification).

---

## 2. Identification

### 2.1 Treatment and Control

**Unit of observation.** The analysis is conducted at the **consumer–closure event** level. Each time a qualifying consumer is exposed to a closure event is one observation. Consumers who experience multiple closures contribute multiple observations, one per closure. Let $i$ index consumers, $e$ index closure events, and $t$ index time periods defined relative to the onset of closure event $e$.

**Treated consumers** (for closure event $e$): regular Luckin purchasers whose pre-closure preferred store is the store that closed in event $e$. "Regular" is defined as at least 5 pre-closure purchases and a preferred-store loyalty ratio of at least 0.8 (i.e., at least 80% of pre-closure purchases were at the closed store), measured using only orders strictly before the closure start date.

**Control consumers** (for closure event $e$): regular Luckin purchasers (same thresholds) whose pre-closure preferred store belongs to the set of stores matched to closure event $e$ by store set-up time, and whose preferred store did not close in any closure event during the same calendar window. Control stores are assigned one-to-one across closures (see Section 3.2). One consumer–closure observation is constructed for each control consumer matched to event $e$.

**Why this control construction supports identification.** Matching control stores by set-up time proxies for store age and market maturity, reducing systematic differences in customer base between treated and control consumers. This strengthens the parallel trends assumption (Section 2.4). Remaining threats — such as local economic shocks that affect the closed store's neighborhood but not the matched control store — are discussed in Section 2.4.

---

### 2.2 Decomposing the Strike's Effect: Displacement vs. Baseline Demand

The closure may affect post-closure Luckin purchasing through two distinct channels:

- **Displacement effect (D):** The causal effect of a forced interruption to a planned purchase. Consumers who would have bought Luckin during the closure window but could not, may have their purchasing habit disrupted, reducing subsequent purchases through state dependence.
- **Baseline-demand effect (B):** Any shift in consumers' underlying demand for Luckin that is independent of the missed purchase — for example, consumers discovering alternative coffee options during the closure, or Luckin responding to the closure with post-reopening promotions. This affects all exposed consumers regardless of whether they had a planned purchase during the closure.

The overall observed post-closure reduction in purchases conflates both channels. Our goal is to isolate the displacement effect.

**Displaced vs. non-displaced consumers.** For each consumer–closure pair $(i, e)$, define:

- **Displaced** ($D_{ie} = 1$): Consumer $i$ would have made at least one Luckin purchase during the closure window of event $e$ in the counterfactual where the store remained open.
- **Non-displaced** ($D_{ie} = 0$): Consumer $i$ would not have made any Luckin purchase in that window even without the closure.

For **treated** consumers, displacement status is unobservable — the closure happened, so we cannot observe counterfactual behavior. For **control** consumers, displacement status is directly observable, since their stores were unaffected and their actual behavior during the closure window is the counterfactual. We exploit this asymmetry to train a classifier (Section 3.8) and use control consumers to evaluate its accuracy.

**Identification intuition.** Non-displaced treated consumers did not have a planned purchase during the closure window. Any post-closure change in their purchasing therefore reflects only baseline-demand shifts — they serve as a clean estimate of $B$. Displaced treated consumers experienced both a missed purchase and any baseline-demand shift. The difference in post-closure outcomes between displaced and non-displaced treated consumers, after differencing out the same gap in control consumers (who face no supply disruption), isolates the displacement effect $D$.

---

### 2.3 Regression Framework

**Time index.** For each closure event $e$, time $t$ is defined in units of the closure duration $D_e$ (i.e., one period = $D_e$ days), centered on the closure window:

- **Pre-closure:** $t \in \{-4, -3, -2, -1\}$ (four periods of length $D_e$ before closure onset).
- **Closure window:** $t = 0$ (excluded from all regressions; used only for displacement classification).
- **Post-closure:** $t \in \{1, 2, \ldots, M\}$ (periods of length $D_e$ after closure resolution).

The reference period is $t = -1$ in all event-study specifications. Using a period length equal to the closure duration $D_e$ ensures that the prediction target for the displacement classifier (Section 3.8) — "would have purchased at least once in a window of length $D_e$?" — is consistent with the regression time unit. This also implies that the base purchase probability for the label varies with closure length; this is discussed further in Section 3.8.

**Period fixed effects.** The fixed effects $\omega_t$ in all specifications below are fixed effects for **relative event time** $t$, common across all closure events. They absorb common trends in relative time (e.g., any systematic pattern in purchases $k$ periods before any closure). Because closures occur at different calendar dates, $\omega_t$ does not absorb calendar seasonality. Calendar-month fixed effects are included as additional controls in all specifications to address this.

---

#### Specification (A): Overall ATT — Difference-in-Differences Event Study

The primary specification estimates the overall average treatment effect on the treated (ATT) at each relative period:

$$
\text{Purchases}_{iet} = \sum_{\ell \in \mathcal{T},\,\ell \neq -1} \delta_{\ell}\,\mathbb{1}(t = \ell) \times \mathbb{1}(\text{Treated}_{ie} = 1) + \phi_{ie} + \omega_t + \gamma_m + \nu_{iet}
$$

**Notation:**
- $\text{Purchases}_{iet}$: number of Luckin purchases by consumer $i$ in closure event $e$ at relative period $t$, normalized by period length (purchases per day).
- $\phi_{ie}$: consumer–closure fixed effects. These absorb all time-invariant characteristics of consumer $i$ in the context of closure event $e$, including the consumer's baseline purchase frequency, displacement status (which is fixed per consumer-closure pair), and closure-level attributes such as closure length. Since $\phi_{ie}$ absorbs any time-invariant term, the main effects of $\mathbb{1}(\text{Treated}_{ie})$ and $\mathbb{1}(\text{Displaced}_{ie})$ are not separately identified and are omitted.
- $\omega_t$: relative-time fixed effects (common across events).
- $\gamma_m$: calendar-month fixed effects (to absorb seasonality not captured by $\omega_t$).
- $\mathcal{T}$: the set of all relative periods in the sample, excluding $t = 0$ (closure window).

**Interpretation of coefficients:**
- $\delta_\ell$ for $\ell < -1$: **pre-trend tests**. Under the parallel trends assumption, these should be jointly indistinguishable from zero. A statistically significant pre-trend indicates that treated and control consumers were on different trajectories before the closure, violating the identifying assumption.
- $\delta_\ell$ for $\ell > 0$: **post-closure ATT**. The combined effect of displacement and baseline-demand shifts on treated consumers' purchases, relative to control, at $\ell$ periods after the closure. A negative and persistent $\delta_\ell$ indicates that treated consumers have not fully recovered their pre-closure purchasing rate.

This specification does not separate the two channels; it provides the total reduced-form effect and the pre-trend falsification evidence.

---

#### Specification (B): Triple-Difference — Isolating the Displacement Effect (Binary)

To separate the displacement effect from baseline-demand shifts, we exploit variation in displacement status across consumers within each group. The estimating equation is:

$$
\text{Purchases}_{iet} =
\sum_{\ell \neq -1} \delta^B_{\ell}\,\mathbb{1}(t=\ell)\times\mathbb{1}(\text{Treated}_{ie})
+ \sum_{\ell \neq -1} \delta^D_{\ell}\,\mathbb{1}(t=\ell)\times\mathbb{1}(\text{Treated}_{ie})\times D_{ie}
+ \sum_{\ell \neq -1} \beta_{\ell}\,\mathbb{1}(t=\ell)\times D_{ie}
+ \phi_{ie} + \omega_t + \gamma_m + \nu_{iet}
$$

where $D_{ie} \in \{0,1\}$ is the binary displacement indicator for consumer $i$ in closure event $e$.

**Cell means implied by the regression.** To see what each coefficient identifies, write out the expected outcome for each of the four groups at post-closure period $\ell > 0$ (relative to the reference period $t = -1$, after absorbing fixed effects):

| | Non-displaced ($D_{ie}=0$) | Displaced ($D_{ie}=1$) |
|---|---|---|
| **Control** | $0$ | $\beta_\ell$ |
| **Treated** | $\delta^B_\ell$ | $\delta^B_\ell + \beta_\ell + \delta^D_\ell$ |

The triple-difference estimator is:

$$
\delta^D_\ell = \underbrace{(\text{Treated-Displaced} - \text{Treated-NonDisp})}_{\text{DiD within treated}} - \underbrace{(\text{Control-Displaced} - \text{Control-NonDisp})}_{\text{DiD within control}}
$$

**Interpretation of coefficients:**
- $\delta^B_\ell$ for $\ell > 0$: the **baseline-demand effect** — the post-closure ATT for non-displaced treated consumers. Since non-displaced consumers did not have a planned purchase interrupted, any change in their purchasing relative to non-displaced control consumers reflects only shifts in baseline demand (e.g., discovered alternatives, Luckin promotions post-reopening). We expect this to be small in magnitude given that our closures are operational rather than reputational events.
- $\delta^D_\ell$ for $\ell > 0$: the **displacement effect** — the additional post-closure reduction in purchases for displaced treated consumers, beyond the baseline-demand effect. A negative and persistent $\delta^D_\ell$ is the primary evidence for structural state dependence: the mere interruption of a planned purchase causally reduces subsequent purchasing.
- $\beta_\ell$: the time-varying difference in purchases between displaced and non-displaced consumers, pooled across treated and control groups. This captures the fact that displaced consumers (by definition more frequent purchasers) have a different time profile of purchases even absent any treatment. Note that the main level effect of $D_{ie}$ is absorbed by $\phi_{ie}$ and is not separately identified.

**Pre-trend falsification.** For $\ell < -1$:
- $\delta^B_\ell \approx 0$ is required for the parallel trends assumption to hold for non-displaced consumers (baseline-demand channel).
- $\delta^D_\ell \approx 0$ is required for the parallel trends assumption to hold for the displaced-vs-non-displaced differential (displacement channel).

Both sets of pre-period coefficients must be reported and tested jointly. A violation in $\delta^B_\ell$ suggests treated and control non-displaced consumers were trending differently before the closure. A violation in $\delta^D_\ell$ suggests the displaced/non-displaced composition differs systematically between treated and control in ways that evolve over time.

**Constraint embedded in the specification.** The regression assumes that $\beta_\ell$ — the time profile of the displaced-vs-non-displaced gap — is the same for treated and control consumers. This is the equal-baseline-demand assumption (Section 2.4). We test this assumption empirically using the matched subsample (Section 5b) and the diagnostic in Section 2.4.

---

#### Specification (C): Triple-Difference — Continuous Displacement Score

As a complement to the binary DDD, we replace the hard-threshold displacement indicator $D_{ie}$ with the continuous predicted purchase propensity $\tilde{s}_{ie} = s_{ie} - \bar{s}$, where $s_{ie} \in [0,1]$ is the classifier's predicted probability of at least one purchase during the closure window, and $\bar{s}$ is its sample mean. Mean-centering ensures that $\delta^B_\ell$ is interpretable as the treatment effect at the average displacement propensity rather than at the extrapolated corner $s_{ie} = 0$.

$$
\text{Purchases}_{iet} =
\sum_{\ell \neq -1} \delta^B_{\ell}\,\mathbb{1}(t=\ell)\times\mathbb{1}(\text{Treated}_{ie})
+ \sum_{\ell \neq -1} \delta^S_{\ell}\,\mathbb{1}(t=\ell)\times\mathbb{1}(\text{Treated}_{ie})\times \tilde{s}_{ie}
+ \sum_{\ell \neq -1} \beta^S_{\ell}\,\mathbb{1}(t=\ell)\times \tilde{s}_{ie}
+ \phi_{ie} + \omega_t + \gamma_m + \nu_{iet}
$$

**Interpretation of coefficients:**
- $\delta^B_\ell$ for $\ell > 0$: the baseline-demand effect for a consumer with average displacement propensity $s_{ie} = \bar{s}$.
- $\delta^S_\ell$ for $\ell > 0$: the **marginal displacement effect** — how much the treatment effect increases per unit increase in displacement propensity, at period $\ell$. A consumer with $\tilde{s}_{ie} = 1 - \bar{s}$ (predicted certain to purchase) has a total treatment effect of $\delta^B_\ell + \delta^S_\ell \cdot (1 - \bar{s})$. A negative $\delta^S_\ell$ means that consumers more likely to have been displaced experienced larger post-closure purchase reductions, consistent with the displacement effect driving the result.
- $\beta^S_\ell$: the time-varying relationship between displacement propensity and purchases, common across treated and control.

**Advantages over binary classification.** This specification avoids dependence on any particular decision threshold and tests for a monotonic dose-response relationship: consumers with higher purchase propensity during the closure (i.e., more strongly displaced) should show larger post-closure reductions if state dependence is the mechanism. It is reported alongside Specification (B) as a robustness check.

**Pre-trend falsification.** Since $\tilde{s}_{ie}$ is mechanically correlated with pre-closure purchase frequency (more frequent buyers have higher $s_{ie}$), the interaction $\mathbb{1}(t=\ell) \times \tilde{s}_{ie}$ may capture heterogeneity in purchase levels across the pre-period time series even absent any treatment. We therefore require $\delta^S_\ell \approx 0$ for all $\ell < -1$ as a falsification test. A non-zero pre-period $\delta^S_\ell$ would indicate that the score is picking up pre-existing heterogeneity in purchase dynamics rather than a displacement effect.

---

#### Specification (D): Closure-Length Heterogeneity

A unique feature of our setting is that closure durations vary substantially across events (approximately 10 to 100 days). We augment Specification (B) to test whether the displacement effect is larger or more persistent for longer closures, consistent with habit-formation models in which longer gaps erode habits more severely:

$$
\text{Purchases}_{iet} =
\sum_{\ell \neq -1} \delta^B_{\ell}\,\mathbb{1}(t=\ell)\times\mathbb{1}(\text{Treated}_{ie})
+ \sum_{\ell \neq -1} \delta^D_{\ell}\,\mathbb{1}(t=\ell)\times\mathbb{1}(\text{Treated}_{ie})\times D_{ie}
+ \sum_{\ell \neq -1} \theta_{\ell}\,\mathbb{1}(t=\ell)\times\mathbb{1}(\text{Treated}_{ie})\times D_{ie} \times \widetilde{L}_e
+ \sum_{\ell \neq -1} \kappa_{\ell}\,\mathbb{1}(t=\ell)\times\mathbb{1}(\text{Treated}_{ie})\times \widetilde{L}_e
+ \sum_{\ell \neq -1} \beta_{\ell}\,\mathbb{1}(t=\ell)\times D_{ie}
+ \phi_{ie} + \omega_t + \gamma_m + \nu_{iet}
$$

where $\widetilde{L}_e = (L_e - \bar{L}) / \text{sd}(L)$ is the standardized closure length in days (mean zero, unit standard deviation), and all lower-order interactions involving $\widetilde{L}_e$ are included.

**Why $\widetilde{L}_e$ rather than raw days.** Closure length $L_e$ is a closure-level variable that does not vary across periods $t$ within a consumer-closure observation; its main effect is therefore absorbed by $\phi_{ie}$ and is not separately identified. Standardizing makes $\theta_\ell$ interpretable as the change in the displacement effect associated with a one-standard-deviation longer closure. The main effect of $\widetilde{L}_e$ and its interaction with $\mathbb{1}(\text{Treated}_{ie})$ are identified only through their interactions with the time dummies, which vary within the panel.

**Interpretation of coefficients:**
- $\delta^D_\ell$: the displacement effect at period $\ell$ for a closure of average length ($\widetilde{L}_e = 0$).
- $\theta_\ell$: how the displacement effect at period $\ell$ changes per one-standard-deviation increase in closure length. A negative $\theta_\ell$ in post-periods indicates that longer closures produce larger habit disruption.
- $\kappa_\ell$: how the baseline-demand effect at period $\ell$ varies with closure length (e.g., longer closures may trigger stronger firm responses such as promotions post-reopening).

**Linearity assumption.** The specification above is linear in $\widetilde{L}_e$. We additionally report a binned version (short: $L_e < 30$ days; medium: $30 \leq L_e < 60$ days; long: $L_e \geq 60$ days) to detect non-linearities, since habit decay may be concave in gap length.

---

### 2.4 Identifying Assumptions

The displacement effect $\delta^D_\ell$ is identified under two assumptions.

**Assumption 1: Parallel Trends.** Within each displacement group (displaced and non-displaced separately), treated and control consumers follow the same trend in Luckin purchases in the absence of the closure. Equivalently, the trend difference between treated and control may differ from zero, provided it is the same across the displaced and non-displaced groups — so that the triple-difference removes it.

*Why this is plausible in our setting.* Control stores are matched to closed stores by set-up time, which proxies for store age and customer base maturity. Within each closure event, treated and control consumers are drawn from stores of similar vintage operating in Nanjing, reducing systematic compositional differences. The main threat is local economic shocks affecting the neighborhood of the closed store but not the matched control store. We assess this empirically: pre-period coefficients $\delta^B_\ell$ and $\delta^D_\ell$ for $\ell < -1$ must be jointly indistinguishable from zero. Following the approach in Levine & Hristakeva (2026) Appendix C, we also formally test whether the linear pre-trend slope differs between treated and control within each displacement group, and whether any violation is equal across groups (which would leave the triple-difference unbiased even if within-group parallel trends fails).

**Assumption 2: Equal Baseline-Demand Effects.** The shift in baseline demand for Luckin caused by the closure (the $B$ channel) is the same for displaced and non-displaced treated consumers. If displaced and non-displaced consumers have different levels of underlying demand for Luckin, the closure may shift their baseline demand by different amounts — for example, a more habitual consumer (who is more likely to be displaced) may respond more strongly to post-reopening promotions.

*Why this is plausible in our setting.* Unlike a high-profile labor strike, our closures are operational events (renovations, temporary shutdowns) with low public salience. Large reputational effects or strategic firm responses that differentially affect displaced and non-displaced consumers are therefore unlikely. Nevertheless, displaced consumers are by definition more frequent buyers, which may make them more sensitive to any baseline-demand shift. We test this assumption using two approaches. First, we estimate Specification (B) on a matched subsample in which displaced and non-displaced consumers are balanced on pre-closure purchase frequency and revisit probability (the proxy for state dependence); similarity of $\delta^D_\ell$ estimates across the full and matched samples provides evidence that baseline-demand heterogeneity is not driving the result. Second, following the diagnostic in Levine & Hristakeva (2026), we estimate the difference in post-closure purchase trajectories between displaced and non-displaced consumers within the **control** group only: since control consumers are unaffected by the closure, any post-closure divergence between their displaced and non-displaced subgroups must reflect baseline-demand differences rather than displacement. If this divergence is small, the equal-baseline-demand assumption is supported.
---

## 3. What Has Been Done

The current production pipeline (primarily `model-free/src/customer-store/analyze_closure_impact.py` and `model-free/src/displacement_classification/*.py`) implements the following.

### 3.1 Data and Sample

- **Order data:** `order_commodity_result.csv`, `order_result.csv` (commodity-level and order-level, with store `dept_id`, `member_id`, date, discount, coupon).
- **Closures (constructed):** `model-free/src/store/identify_closures.py` identifies closures from daily store demand as **≥10 consecutive zero-demand days**, requiring **non-zero demand both before and after** the zero-demand spell. It then merges geocoded store metadata and keeps stores with valid coordinates within Nanjing bounds.
- **Analysis closure input:** `outputs/store/non_uni_store_closures.csv` (derived from `outputs/store/store_closures.csv` by excluding stores whose `address` contains `大学` or `学院`).
- **Thresholds:** “Regular” customer: at least **5** pre-closure purchases (`DEFAULT_LOWEST_PURCHASES`) and preferred-store loyalty ratio **≥ 0.8** (`DEFAULT_LOWEST_RATIO`). The script includes **threshold justification** (coverage at different purchase and ratio cutoffs).

### 3.2 Treatment and Control

- **Default mode (enabled): set-up-time–matched control (`USE_SET_UP_TIME_MATCHED_CONTROL=True`).**
  - **Treatment (per closure):** Using only visits **before closure start**, customers whose pre-closure preferred store is the closed store, with pre-closure `total_purchases ≥ 5` and `preferred_ratio ≥ 0.8`.
  - **Control stores (per closure):** Up to `SET_UP_TIME_NEAREST_N=5` stores chosen by nearest `set_up_time` to the closed store, restricted to non-treated stores; each control store is used at most once across closures (processed in closure-start order).
  - **Control members (per closure):** Customers whose pre-closure preferred store is in that closure’s matched control-store set, with the same pre-closure thresholds (`≥5` purchases and ratio `≥0.8`).
- **Alternative mode (disabled by default): never-treated closure-specific control.**
  - Never-treated pool = qualified loyal customers whose preferred store never appears in closures.
  - For each closure, keep pool members who were qualified at that closure date (`≥5` purchases before closure start and max single-store share `≥0.8`).

In both modes, one observation unit remains the **consumer–closure event**, and the same consumer can appear in multiple closures.

- **Boundary consumer rule in production selection:** Treatment assignment is based on **pre-closure preferred store = closed store** (no additional distance-based override is applied).
- **Cross-pipeline consistency:** Closure-specific matched controls are persisted in `outputs/customer-store/closure_pair_registry.csv`, and displacement training loads the same kept-closure registry.
- **Comparability diagnostics captured in outputs:** Closure timing/duration and treatment-control pairing metadata are persisted in registry fields (e.g., closure dates, `closure_duration_days`, matched control stores, status/skip reason), with closure-event covariates (`closure_start_month`, `closure_start_weekday`, `closure_start_season`, `share_visited_stores_closed`) carried into displacement panels.

### 3.3 Time Windows

- **Pre / during / post** defined per closure using a configurable **window** (default 14 days, robustness 28 days):  
  - Pre: `window_days` before closure start.  
  - During: closure start to closure end.  
  - Post: `window_days` after closure end.  
- Period lengths are used to normalize metrics (e.g., purchases per day).

### 3.4 Outcomes and Behavior

- **Behavior metrics** (per customer, per period):  
  - `n_purchases`: purchase days per day in the period.  
  - `new_product_ratio`, `total_discount`, `coupon_usage_rate`.  
- **Panel:** One row per (closure, group, period, member_id) in `period_df`.

### 3.5 Descriptive and Visual

- **Threshold justification:** Distribution of purchase counts and preferred-store ratio; fraction qualifying at different cutoffs.
- **Unique stores:** Histogram of number of distinct stores per customer (among qualified).
- **Closure impact summary:** Per-closure counts of treatment/control, purchase rates during closure, selectivity ratio.
- **Plots:**  
  - Treatment vs control, pre / during / post, for the four behavior metrics (with significance brackets).  
  - **Duration split:** Short vs long closures (e.g., &lt; 30 vs ≥ 30 days).  
  - **Push split:** Treatment subdivided into no-push vs with-push (using `no_push_members.csv`), vs control.

### 3.6 Inference (Current)

- **Paired t-tests:** Treatment and control, pre vs post (per customer, control deduplicated across closures).
- **Two-sample t-tests:** Treatment vs control in pre and in post.
- **Closure-level inclusion filters in analysis:**
  - Skip closure if either group size is below `MIN_GROUP_SIZE=50`.
  - Skip closure if control during-closure purchase rate is too low: `control_rate < 2.0 × treatment_rate` (`MIN_CTRL_TREAT_RATIO=2.0`).
  - The retained subset is exported as `outputs/customer-store/closures_used.csv`.
- No regression-based DiD or triple-difference yet; no displacement classification; no event-study or formal pre-trend tests.

### 3.7 Outputs

- Summary CSV per closure (treatment/control sizes, purchase rates during closure).  
- Period-level behavior CSV.  
- Statistical test results CSV.  
- PDFs: behavior comparison (main, robustness window), duration-split, push-split.

### 3.8 Displacement Classification Model

**3.8.1 Prediction target and panel construction**

- Label = whether a consumer made **at least one Luckin purchase** in a given consumer–closure–period row.
- Training panel uses periods `-4, -3, -2, -1` for treatment/control and period `0` for control evaluation.
- Period length equals closure duration `D = closure_duration_days`.
- History guardrails are enforced at closure and member levels (`closure_start ≥ earliest_order_date + 4D + 8 days`; first purchase before earliest pre-period start).
- Train/eval split is implemented as: train `period <= -2`, eval-pre `period = -1`, eval-during `period = 0 & group=control`.

**3.8.2 Features**

- Uses `order_result.csv` for behavioral/order features and `member_result.csv` for demographics.
- Builds 46 consumer-level features from history strictly prior to `period_start` (frequency/recency, regularity, DOW patterns, basket breadth, loyalty, order-level behavior, demographics).
- Stores additional closure-event covariates in panel outputs for downstream DiD/DDD estimation.

**3.8.3 Model training and evaluation**

- Trains XGBoost (`binary:logistic`, `max_depth=6`, `eta=0.1`, `tree_method=hist`, 500 rounds), using CUDA when available and CPU otherwise.
- Trains **one model per closure duration `D`**.
- Evaluates with group-period slices: Treatment-Pre (`t=-1`), Control-Pre (`t=-1`), Control-During (`t=0`), including FPR/FNR.
- Produces gain-based variable importance and label-balance audits by duration/split.

**3.8.4 Outputs and displacement classification**

- Duration-suffixed artifacts are generated: `displacement_model_D.json`, `variable_importance_D.csv`, `prediction_accuracy_D.csv`, `panel_with_scores_D.parquet`, `displacement_scores_D.csv`.
- Run-level artifacts include `label_balance_audit.csv` and training logs in `outputs/displacement_classification/logs/`.
- Binary displacement classification uses `predicted probability ≥ decision_threshold` (default 0.5), and continuous displacement scores are saved for score-based specifications.

---

## 4. What Has Not Been Done (To-Do)

The following steps align the remaining analysis with Paper 2 and exploit our multi-closure, varying-length structure.

---

### Step 3: Construct the Estimation Sample

**3a. Time window.**

- Pre: $N$ periods before closure onset (e.g., 9).  
- Closure: t = 0 (possibly normalized to one “period” or expressed in common time units).  
- Post: $M$ periods after resolution.  
- Given varying closure length, consider normalizing “during” to one period and expressing pre/post in consistent units (e.g., weeks) relative to onset/resolution.

**3b. Outcome.**

- **Primary:** Number of Luckin purchases per period (or binary “any purchase”) at consumer–period level.

**3c. Stack observations.**

- Stack **consumer–closure event** observations (as in Paper 1 with multiple hurricanes).  
- Time index relative to each closure.  
- Account for multiple closures per consumer in **standard errors** (e.g., cluster at consumer or consumer–closure).

---

### Step 4: Estimate the Displacement Effect

**4a. Overall ATT.**

- Run DiD: post vs pre, treated vs control (excluding t = 0).  
- Present as **event study** (e.g. $\delta_l$ by period $l$): check no pre-trend, drop at t = 1, gradual recovery.

**4b. Triple-difference.**

- Estimate Equation 9 (or event-study version): $\delta^B$, $\delta^D$, $\beta$.  
- Present event study for displacement effect over time.
- Also estimate a **continuous-score DDD** using predicted displacement propensity to avoid threshold arbitrariness and test monotonic dose-response.

**4c. Closure-length interaction.**

- Add $\delta^D_1 \times \text{ClosureLength}$ (and possibly level) to test whether longer closures increase or prolong displacement effects.

---

### Step 5: Robustness Checks

**5a. Parallel pre-trends.**

- Event study by displaced vs non-displaced; test formally (e.g. Paper 2 Appendix C) whether pre-trend slope differs by treatment within displacement group and whether any violation is equal across displacement groups.

**5b. Matched subsample.**

- Match displaced to non-displaced on pre-closure purchase frequency (e.g. share of periods with a purchase) and revisit probability; re-estimate triple-difference on matched sample.

**5c. Classification threshold.**

- Try thresholds for “displaced” (e.g. predicted probability &gt; 0.4, 0.5, 0.6); show displacement effect stability.
- Add score calibration and functional-form robustness for continuous-score specification (e.g., linear vs binned/spline score effects).

**5d. Subsample by closure severity.**

- Full vs partial closure (all vs some of consumer’s accessible stores closed); compare estimates.

**5e. Attenuation bound.**

- Use control-based µ and λ (Step 2e) and Paper 2 Appendix D–style correction to derive a **lower bound** on the true displacement effect.

---

### Step 6: Heterogeneity Analysis

**6a. Competitor.**  
If data allow: number of competitors near the store; test whether displacement effect varies with competition.

**6b. Closure length.**  
Already in Step 4c; interpret as main novel heterogeneity.

**6c. Habit strength.**  
Split by pre-closure regularity (e.g. daily vs weekly vs occasional). Test whether displacement effect is larger for stronger habits (habit capital depreciates) or smaller (entrenched preferences, quick return).

**6d. Demographics.**  
By age, income, city tier (analogous to Paper 2 Table 6).

**6e. Privacy / push.**  
Compare displacement effect between **push0** (opted out of push at first use) and **push1**; interpret as proxy for privacy sensitivity or engagement with the app.

---

## 5. Summary Table

| Area | Done | Not done |
|------|------|----------|
| **Treatment/control** | Pre-closure preferred-store-based treatment; default set-up-time–matched closure-specific control (with one-time control-store assignment); threshold justification; boundary rule under preferred-store assignment; multi-closure consumer–event handling; closure-level screening (`MIN_GROUP_SIZE`, control/treatment rate filter); pairing registry (`closure_pair_registry.csv`) shared across pipelines; comparability metadata captured in registry/panel covariates | — |
| **Displacement** | Registry-aligned panel (periods −4…−1 + control t=0, with period length = closure duration `D`); 46 behavioral/demographic features from `order_result.csv`; train/eval split (`<=-2`, `-1`, `0-control`); XGBoost trained per duration `D` (500 rounds, gain importance); duration-suffixed outputs (`displacement_model_D.json`, `variable_importance_D.csv`, `prediction_accuracy_D.csv`, `displacement_scores_D.csv`) plus `label_balance_audit.csv`; binary and continuous displacement scores persisted for downstream estimation | — |
| **Sample** | Pre/during/post windows; period-level behavior panel | Normalized time units; stacked consumer–closure; clustering design |
| **Estimation** | Descriptive stats, t-tests, visual comparison | DiD ATT; triple-difference; event study; closure-length interaction |
| **Robustness** | 14 vs 28 day window; duration-split and push-split plots; model evaluation by pre/during groups and duration | Parallel trends test; matching; threshold sensitivity; severity subsample; attenuation bound; continuous-score calibration robustness |
| **Heterogeneity** | Duration-split, push-split (visual) | Competitor, habit strength, demographics, push0 vs push1 (regression) |

---

*References:*  
- Levine, J., & Hristakeva, S. (2026). *Stopping Shopping at Stop and Shop? How Temporary Disruptions Affect Store Choice.* Draft January 5, 2026 (Paper 2).  
- Script: `model-free/src/customer-store/analyze_closure_impact.py`  
- Closure construction: `model-free/src/store/identify_closures.py`  
- Closures used for analysis: `model-free/outputs/store/non_uni_store_closures.csv`
