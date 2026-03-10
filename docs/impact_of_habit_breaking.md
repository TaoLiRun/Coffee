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

### 2.1 Treatment and Control (Conceptual)

- **Treated:** Consumers who are **regular Luckin purchasers** and whose access to Luckin was **disrupted by a closure** (e.g., their preferred or only accessible store closed).
- **Control:** Regular Luckin purchasers who were **not** exposed to any closure in the same calendar window, and who are comparable in geography and behavior so that post-closure comparisons identify the effect of the closure.

Treatment is defined at the **consumer–closure event** level: each time a consumer is exposed to a closure is one “observation”; consumers with multiple closures contribute multiple observations.

### 2.2 Displacement (Unobservable for Treated)

For each consumer–closure pair, define:

- **Displaced:** Would have made at least one Luckin purchase during the closure window in the counterfactual where the store remained open.
- **Non-displaced:** Would not have made a Luckin purchase in that window even without the closure.

For **treated** consumers we do not observe this; for **control** consumers we do (their behavior during the same calendar window is the counterfactual). So we **train a classifier** on pre-closure (and control) behavior to predict “would have purchased during closure window,” and then use this predicted displacement status in the regression.

### 2.3 Regression Framework

**Time:** For each closure event, define:

- **Pre:** \( t < 0 \) (e.g., \( N \) periods before closure onset).
- **Closure:** \( t = 0 \) (closure window; length may vary by event).
- **Post:** \( t > 0 \) (e.g., \( M \) periods after closure resolution).

Time can be normalized (e.g., in weeks) so that different closure lengths are comparable.

**Overall ATT (difference-in-differences):**

\[
\text{Purchases}_{it} = \delta \cdot \mathbb{1}(t > 0) \times \mathbb{1}(\text{Treated}_i) + \phi_i + \omega_t + \nu_{it}
\]

- \(\phi_i\): consumer (or consumer–closure) fixed effects.  
- \(\omega_t\): period fixed effects.  
- Sample excludes \(t = 0\).  
- \(\delta\) is the overall ATT (displacement + baseline demand combined).  
- An **event study** version replaces the single post dummy with dummies for each \(t\) to trace dynamics and pre-trends.

**Triple-difference to isolate displacement (Paper 2, Equation 9):**

\[
\text{Purchases}_{it} = \delta^B \cdot \mathbb{1}(t>0) \times \mathbb{1}(\text{Treated}_i) + \delta^D \cdot \mathbb{1}(t>0) \times \mathbb{1}(\text{Treated}_i) \times \mathbb{1}(\text{Displaced}_i) + \beta \cdot \mathbb{1}(t>0) \times \mathbb{1}(\text{Displaced}_i) + \phi_i + \omega_t + \nu_{it}
\]

- \(\delta^B\): ATT for **non-displaced** treated (baseline-demand effect).  
- \(\delta^D\): **displacement effect**—additional post-closure reduction for consumers whose planned purchases were interrupted.  
- \(\beta\): main effect of being displaced (allowed to differ for control).  
- Event-study version: replace single post dummies with \(t\)-specific dummies in the same way.

**Closure-length heterogeneity (unique to our setting):**

\[
\delta^D(\text{length}) = \delta^D_0 + \delta^D_1 \times \text{ClosureLength}
\]

This tests whether longer interruptions lead to larger or more persistent displacement effects, as in habit-formation models where longer gaps erode habits more.

### 2.4 Identifying Assumptions (Paper 2 Logic)

1. **Parallel trends:** Within displacement group (displaced / non-displaced), treated and control have the same trend in pre-closure purchases; or the trend difference is the same across displacement groups so that the triple-difference is still identified.
2. **Equal baseline-demand effects:** The baseline-demand shift (B) is the same for displaced and non-displaced treated consumers.
3. **Displacement classification:** Misclassification of displacement attenuates \(\delta^D\) toward zero; we can use control behavior at \(t=0\) to estimate error rates and apply Paper 2’s correction (e.g., Appendix D) to bound the true displacement effect.

---

## 3. What Has Been Done

The script `model-free/scripts/customer-store/analyze_closure_impact.py` implements the following.

### 3.1 Data and Sample

- **Order data:** `order_commodity_result.csv`, `order_result.csv` (commodity-level and order-level, with store `dept_id`, `member_id`, date, discount, coupon).
- **Closures:** `store_closures.csv` with `dept_id`, `closure_start`, `closure_end`, `closure_duration_days`, and optionally latitude, longitude, address.
- **Thresholds:** “Regular” customer: at least **5** pre-closure purchases (`DEFAULT_LOWEST_PURCHASES`) and preferred-store loyalty ratio **≥ 0.8** (`DEFAULT_LOWEST_RATIO`). The script includes **threshold justification** (coverage at different purchase and ratio cutoffs).

### 3.2 Treatment and Control (Current)

- **Treatment (per closure):** Customers whose **preferred store** is the closed store and whose **preferred-store ratio ≥ 0.8** (computed over full pre-closure history).
- **Control (closure-specific):** For each closure, control = never-treated consumers who, **before that closure’s start**, had ≥5 purchases and ≥4 of those at one store (ratio ≥ 0.8). The never-treated pool = consumers whose preferred store never closed; from this pool we select those qualified at the time of each closure. The same consumer can be control for multiple closures.

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
- No regression-based DiD or triple-difference yet; no displacement classification; no event-study or formal pre-trend tests.

### 3.7 Outputs

- Summary CSV per closure (treatment/control sizes, purchase rates during closure).  
- Period-level behavior CSV.  
- Statistical test results CSV.  
- PDFs: behavior comparison (main, robustness window), duration-split, push-split.

---

## 4. What Has Not Been Done (To-Do)

The following steps align the analysis with Paper 2 and exploit our multi-closure, varying-length structure.

---

### Step 1: Finalize and Validate the Treatment/Control Definition

**1a. Verify the treatment definition at the consumer level.**

- Document and justify: **How many pre-closure purchases** define “regular” (current: 5); sensitivity to this choice.
- **Boundary consumers:** If a consumer’s nearest store closed but another store was within a reasonable distance, are they treated or excluded? Define and implement a rule (e.g., distance threshold, or “all stores within X km closed”).
- **Multiple closures:** Construct **one observation per consumer–closure event**. Decide how to handle consumers who experience several closures (e.g., allow multiple rows per consumer with clustering at consumer or consumer–closure level in inference).

**1b. Verify the control definition (closure-specific).**

- **Global pool:** Control candidates are regular Luckin purchasers whose preferred store **never** appears in the closures list (“never-treated” pool). They are not exposed to any closure.
- **Closure-specific selection:** For **each closure event**, the control group is redefined as those never-treated consumers who, **before that closure’s start date**, satisfy:
  - At least **5** Luckin purchases (pre-closure).
  - At least **4 of those 5** purchases at the **same store** (i.e., pre-closure preferred-store share ≥ 0.8).
- This ensures control consumers are **frequent purchasers at the time the closure happened**, comparable to the treated. The **same consumer can be in the control group for multiple closures** if they meet the pre-closure criteria for each.
- **Additional checks (if feasible):** Geographic and demographic comparability to treated; exclude anyone in regions with closures at nearby dates (anticipation or spillover).

**1c. Exploit variation across closure events.**

- Document distribution of closures by:  
  - **Geography** (e.g., district, campus vs non-campus).  
  - **Timing** (calendar date, season).  
  - **Duration** (length of closure; key for later heterogeneity).  
  - **Severity** (e.g., share of a consumer’s historically visited stores that were closed).

Use this to strengthen identification and to run heterogeneity by closure length and severity.

---

### Step 2: Build and Validate the Displacement Classification Model

**2a. Define the prediction target.**

- For each **consumer–closure** observation, the binary label is: **Would this consumer have made a Luckin purchase during the closure window in the counterfactual without the closure?**
- For treated consumers this is unobserved; the model is trained on **pre-closure periods** (and control) where the label is observed (whether a purchase was made in that period).

**2b. Training data selection.**

- **Unit:** One observation = (consumer, closure, period), where period is either a **pre-closure week** (e.g., weeks −2, −1 for 2-week pre; weeks −4, −3, −2, −1 for 4-week) or the **closure window** for **control** consumers (observed; used for evaluation only).
- **Label:** Binary = 1 if consumer made ≥1 Luckin purchase in that period, 0 otherwise.
- **Features:** All from **history strictly before** period start (no look-ahead).
- **Training set:** All (consumer–closure–period) with observed labels: all pre-closure periods for treated and control. Control closure period (t=0) used for evaluation, not training.
- **Prediction target:** For each consumer–closure, predict purchase during closure window (t=0).

**2c. Feature variables (≥50).**

Data sources: `order_commodity_result.csv`, `order_result.csv`, `member_result.csv`, `store_closures.csv`, `no_push_members.csv`. See table below.

| # | Variable | Source | Construction |
|---|----------|--------|--------------|
| 1–12 | Purchase freq/recency | order_commodity, order_result | purchases_per_week (all, 4w, 2w, 1w), days_since_last, purchased_in_last_7/14_days, total_purchase_days, total_orders, total_spend (all, 4w, 2w) |
| 13–18 | Regularity/habit | order_commodity | mean/std/cv inter_purchase_interval, longest_streak, share_weeks_with_purchase, max_gap |
| 19–27 | Temporal (dow) | order_commodity | share_purchases_mon…sun, modal_purchase_dow, entropy_dow |
| 28–32 | Temporal (tod) | order_result | share_morning/afternoon/evening, hour_mean, hour_std |
| 33–38 | Product/basket | order_commodity, order_result | unique_products, new_product_ratio, coffee_share, avg_basket_size, avg_discount, coupon_usage_rate |
| 39–41 | Store | order_commodity | unique_stores, preferred_store_ratio, second_store_ratio |
| 42–53 | Demographics | member_result | gender, birth_year, age, level, has_inviter, manufacturer, callphone, camera, location, network, push, sdcard |
| 54–60 | Closure-specific | store_closures, visits | closure_length_days, closure_start_month/weekday/season, is_treated, share_visited_stores_closed, tenure_days |
| 61–65 | Order-level | order_result | avg_coffee_num, avg_food_num, avg_use_coffee_wallet, avg_delivery_pay, take_address_rate |

**2d. Train random forest.**

- 500 trees; tune `max_features` (mtry) via OOB or cross-validation.
- One global model across all closure events; closure characteristics as features.
- Impute missing: numeric → median; categorical → mode.

**2e. Evaluation.**

- **Variable importance:** Permutation importance or mean decrease in impurity; rank by contribution to accuracy.
- **Accuracy by group and period:**
  - **Treatment, Pre (t=−1):** OOB accuracy for last pre-closure week.
  - **Control, Pre (t=−1):** Same.
  - **Control, During (t=0):** Predicted vs actual; accuracy, precision, recall, F1, false positive rate (µ), false negative rate (λ).

**2f. Outputs from running the code.**

1. **Variable importance ranking:** Table/CSV with `feature`, `importance`, `rank` (sorted descending).
2. **Prediction accuracy table:**

| Group | Period | Accuracy | Precision | Recall | F1 | n |
|-------|--------|----------|------------|--------|-----|---|
| Treatment | Pre (t=−1) | … | … | … | … | … |
| Control | Pre (t=−1) | … | … | … | … | … |
| Control | During (t=0) | … | … | … | … | … |

3. **Optional:** Accuracy by closure length (short/medium/long).

**2g. Classify displaced vs non-displaced.**

- **Displaced** = predicted probability > 0.5 (or tuned threshold).
- **Correction (Paper 2):** For control, replace predicted with observed at t=0; drop misclassified controls.

---

### Step 3: Construct the Estimation Sample

**3a. Time window.**

- Pre: \(N\) periods before closure onset (e.g., 9).  
- Closure: t = 0 (possibly normalized to one “period” or expressed in common time units).  
- Post: \(M\) periods after resolution.  
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
- Present as **event study** (e.g. \(\delta_l\) by period \(l\)): check no pre-trend, drop at t = 1, gradual recovery.

**4b. Triple-difference.**

- Estimate Equation 9 (or event-study version): \(\delta^B\), \(\delta^D\), \(\beta\).  
- Present event study for displacement effect over time.

**4c. Closure-length interaction.**

- Add \(\delta^D_1 \times \text{ClosureLength}\) (and possibly level) to test whether longer closures increase or prolong displacement effects.

---

### Step 5: Robustness Checks

**5a. Parallel pre-trends.**

- Event study by displaced vs non-displaced; test formally (e.g. Paper 2 Appendix C) whether pre-trend slope differs by treatment within displacement group and whether any violation is equal across displacement groups.

**5b. Matched subsample.**

- Match displaced to non-displaced on pre-closure purchase frequency (e.g. share of periods with a purchase) and revisit probability; re-estimate triple-difference on matched sample.

**5c. Classification threshold.**

- Try thresholds for “displaced” (e.g. predicted probability &gt; 0.4, 0.5, 0.6); show displacement effect stability.

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
| **Treatment/control** | Preferred-store-based treatment; never-treated control; threshold justification | Boundary/multi-closure rules; control comparability; closure distribution (geo, timing, duration, severity) |
| **Displacement** | — | Target definition; training data; full feature set; RF training; OOB and control-window evaluation; classification + Paper 2 correction |
| **Sample** | Pre/during/post windows; period-level behavior panel | Normalized time units; stacked consumer–closure; clustering design |
| **Estimation** | Descriptive stats, t-tests, visual comparison | DiD ATT; triple-difference; event study; closure-length interaction |
| **Robustness** | 14 vs 28 day window; duration-split and push-split plots | Parallel trends test; matching; threshold sensitivity; severity subsample; attenuation bound |
| **Heterogeneity** | Duration-split, push-split (visual) | Competitor, habit strength, demographics, push0 vs push1 (regression) |

---

*References:*  
- Levine, J., & Hristakeva, S. (2026). *Stopping Shopping at Stop and Shop? How Temporary Disruptions Affect Store Choice.* Draft January 5, 2026 (Paper 2).  
- Script: `model-free/scripts/customer-store/analyze_closure_impact.py`  
- Closures: `model-free/plots/nanjing_store_locations/store_closures.csv`
