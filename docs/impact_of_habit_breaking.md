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

- **Sample:** Only closures with `closure_start ≥ 2020-09-01` are used (89 of 101 total), ensuring all 4 pre-closure weeks fall within the data window (2020-06-01 to 2021-12-31).
- **Eligibility:** A consumer is included in treatment or control only if their **first ever order predates `closure_start − 28 days`** (i.e., they must have been active before the earliest pre-closure week). This prevents look-ahead contamination and guarantees computable history features for period −4.
- **Unit:** One observation = (consumer, closure, period), where period ∈ {−4, −3, −2, −1} (pre-closure weeks) for both treatment and control, plus period 0 (closure window) for **control only** (observed; used for evaluation, not training).
- **Label:** Binary = 1 if consumer made ≥1 Luckin purchase in that 7-day period, 0 otherwise.
- **Features:** All computed from order history **strictly before** the period start date (no look-ahead).
- **Training set:** All (consumer–closure–period) rows with period ∈ {−4, −3, −2, −1}. Control period 0 is held out for evaluation.
- **Prediction target:** For each consumer–closure, predict purchase during closure window (t=0).

**2c. Feature variables.**

Single behavioral data source: `order_result.csv`. Demographics from `member_result.csv`. No `order_commodity_result.csv` is used; item-count columns (`coffee_commodity_num`, `food_commodity_num`, etc.) are embedded in `order_result.csv`.

**Features used in X (46 consumer-level features):** All computed from history strictly before `period_start`. Closure-specific features are deliberately excluded — consumers cannot forecast a closure, so those features carry no information about pre-closure purchase propensity.

| # | Variable group | Variables | Construction |
|---|----------------|-----------|---------------|
| 1–12 | Purchase frequency & recency | `total_purchase_days_pre`, `purchases_per_week_all_pre`, `purchases_per_week_last_{4w,2w,1w}`, `days_since_last_purchase`, `purchased_in_last_{7,14}_days`, `total_orders_pre`, `total_spend_pre`, `total_spend_last_{4w,2w}` | Computed over all history before `period_start`; rolling windows use deduped purchase-day counts |
| 13–18 | Regularity / habit | `mean_inter_purchase_interval_days`, `std_inter_purchase_interval_days`, `cv_inter_purchase_interval`, `max_gap_between_purchases`, `longest_consecutive_streak_days`, `share_weeks_with_purchase` | Computed per member from sorted unique purchase dates before `period_start` |
| 19–27 | Day-of-week | `share_purchases_dow{0…6}`, `modal_purchase_dow`, `entropy_dow` | DoW share = fraction of all purchase-day rows falling on each weekday; entropy uses natural log |
| 28–29 | Basket & breadth | `avg_basket_size`, `n_order_categories_avg` | `avg_basket_size` = mean total items per order (sum of `*_commodity_num`); `n_order_categories_avg` = mean distinct non-zero category counts per order |
| 30–32 | Store loyalty | `unique_stores_pre`, `preferred_store_ratio`, `second_store_ratio` | Computed from visit-deduplicated (`member_id`, `date`, `dept_id`) order history |
| 33–40 | Order-level behaviour | `avg_discount_per_order`, `coupon_usage_rate`, `avg_coffee_num`, `avg_food_num`, `avg_use_coffee_wallet`, `avg_delivery_pay`, `coffee_share_orders`, `take_address_rate` | Mean per member over history; `avg_delivery_pay` treats NaN (pickup/in-store) as 0; `coffee_share_orders` = share of orders with `coffee_commodity_num > 0`; `take_address_rate` = share with non-null `take_address` |
| 41–46 | Demographics | `gender`, `level`, `has_inviter`, `manufacturer`, `callphone`, `push` | Integer-encoded (NaN → 1; sorted distinct values → 2, 3, …); encoding map saved to `data/intermediate/demo_encoding_map.csv`. Excludes `birth_year`, `camera`, `location`, `network`, `sdcard`. |

**Features stored in panel but excluded from X (used in Step 4 DiD regression):**

| Variable | Construction |
|----------|--------------|
| `closure_length_days` | Duration of the closure in days |
| `closure_start_month` | Calendar month of closure start (1–12) |
| `closure_start_weekday` | Day-of-week of closure start (0=Monday) |
| `closure_start_season` | Season of closure start (1–4) |
| `share_visited_stores_closed` | Whether this is a treatment consumer (= `is_treated`); captures treatment assignment |
| `tenure_days` | Days from first order in data to `period_start`; proxy for how long the member has been active |

**2d. Train XGBoost.**

- **Algorithm:** XGBoost gradient-boosted trees (`binary:logistic`, eval metric: AUC).
- **Hyperparameters:** 500 boosting rounds, `max_depth = 6`, `eta = 0.1`, `tree_method = hist`.
- **Hardware:** Uses `device = cuda` when a GPU is detected; falls back to CPU otherwise. No manual imputation is needed — the pipeline raises `ValueError` on any NaN in the feature matrix, so the training matrix is guaranteed NaN-free.
- **Scope:** One global model trained across all 89 closure events; closure characteristics (`closure_length_days`, `closure_start_month`, etc.) are included as features to capture event-level heterogeneity.

**2e. Evaluation.**

- **Variable importance:** Gain-based importance from `model.get_score(importance_type="gain")`; top 30 features printed and full ranking saved.
- **Accuracy by group and period** (threshold = 0.5):
  - **Treatment, Pre (t=−1):** Predicted vs observed for the last pre-closure week.
  - **Control, Pre (t=−1):** Same.
  - **Control, During (t=0):** Predicted vs observed for actual closure window; yields false positive rate µ and false negative rate λ used for Paper 2 attenuation correction.

**2f. Outputs from running the code.**

1. **`variable_importance.csv`:** Columns `feature`, `importance` (gain), `rank` (sorted descending).
2. **`prediction_accuracy.csv`:** One row per evaluation group with columns `accuracy`, `precision`, `recall`, `f1`, `fpr`, `fnr`, `n`, `group`.
3. **`train_displacement_model.log`:** Full log including variable statistics (mean, min, max for all 52 features), dataset counts, and the complete accuracy table.

Example accuracy table (1-closure test, closure Sept 5 2020, dept 239, 46 behavioral/demographic features):

| group | accuracy | precision | recall | f1 | fpr | fnr | n |
|-------|----------|-----------|--------|----|-----|-----|---|
| Treatment_Pre_t-1 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | 4 |
| Control_Pre_t-1 | 0.816 | 0.863 | 0.694 | 0.769 | 0.087 | 0.306 | 16,705 |
| Control_During_t0 | 0.579 | 0.727 | 0.513 | 0.602 | 0.314 | 0.487 | 16,705 |

**2g. Classify displaced vs non-displaced.**

- **Displaced** = predicted probability > 0.5 (default threshold; sensitivity to 0.4 and 0.6 is a robustness check, Step 5c).
- **Correction (Paper 2, future):** For control consumers, replace model prediction with observed purchase at t=0; use µ (FPR) and λ (FNR) from the Control_During_t0 row to bound the attenuation in the displacement effect estimate (Paper 2 Appendix D). Not yet implemented.

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
| **Displacement** | Target definition; 4-week panel (periods −4…−1 + control t=0); 46 behavioral/demographic features from `order_result.csv` (closure-event features excluded from X, stored for Step 4); XGBoost (500 rounds, gain importance); accuracy table (Treatment/Control pre & during); `variable_importance.csv`, `prediction_accuracy.csv` | Displacement label assignment to treatment consumers; Paper 2 attenuation correction (µ, λ bounds); accuracy by closure length |
| **Sample** | Pre/during/post windows; period-level behavior panel | Normalized time units; stacked consumer–closure; clustering design |
| **Estimation** | Descriptive stats, t-tests, visual comparison | DiD ATT; triple-difference; event study; closure-length interaction |
| **Robustness** | 14 vs 28 day window; duration-split and push-split plots | Parallel trends test; matching; threshold sensitivity; severity subsample; attenuation bound |
| **Heterogeneity** | Duration-split, push-split (visual) | Competitor, habit strength, demographics, push0 vs push1 (regression) |

---

*References:*  
- Levine, J., & Hristakeva, S. (2026). *Stopping Shopping at Stop and Shop? How Temporary Disruptions Affect Store Choice.* Draft January 5, 2026 (Paper 2).  
- Script: `model-free/scripts/customer-store/analyze_closure_impact.py`  
- Closures: `model-free/plots/nanjing_store_locations/store_closures.csv`
