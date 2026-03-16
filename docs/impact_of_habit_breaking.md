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

In addition to hard classification (displaced vs non-displaced), the predicted probability can be used as a **continuous displacement propensity score** to preserve more information from the model output.

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

**Continuous-score variant (recommended as a complement):**

\[
	ext{Purchases}_{it} = \delta^B \cdot \mathbb{1}(t>0)\times\mathbb{1}(\text{Treated}_i) + \delta^S \cdot \mathbb{1}(t>0)\times\mathbb{1}(\text{Treated}_i)\times s_i + \beta^S \cdot \mathbb{1}(t>0)\times s_i + \phi_i + \omega_t + \nu_{it}
\]

- \(s_i\): predicted purchase propensity during closure (continuous score from Step 2 model).
- \(\delta^S\): how treatment post-effect scales with displacement propensity.
- This avoids dependence on a single hard threshold and is reported alongside threshold-based DDD.

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

The script `model-free/src/customer-store/analyze_closure_impact.py` implements the following.

### 3.1 Data and Sample

- **Order data:** `order_commodity_result.csv`, `order_result.csv` (commodity-level and order-level, with store `dept_id`, `member_id`, date, discount, coupon).
- **Closures (constructed):** `model-free/src/store/identify_closures.py` identifies closures from daily store demand as **≥10 consecutive zero-demand days**, requiring **non-zero demand both before and after** the zero-demand spell. It then merges geocoded store metadata and keeps stores with valid coordinates within Nanjing bounds.
- **Analysis closure input:** `outputs/store/non_uni_store_closures.csv` (derived from `outputs/store/store_closures.csv` by excluding stores whose `address` contains `大学` or `学院`).
- **Thresholds:** “Regular” customer: at least **5** pre-closure purchases (`DEFAULT_LOWEST_PURCHASES`) and preferred-store loyalty ratio **≥ 0.8** (`DEFAULT_LOWEST_RATIO`). The script includes **threshold justification** (coverage at different purchase and ratio cutoffs).

### 3.2 Treatment and Control (Current)

- **Default mode (enabled): set-up-time–matched control (`USE_SET_UP_TIME_MATCHED_CONTROL=True`).**
  - **Treatment (per closure):** Using only visits **before closure start**, customers whose pre-closure preferred store is the closed store, with pre-closure `total_purchases ≥ 5` and `preferred_ratio ≥ 0.8`.
  - **Control stores (per closure):** Up to `SET_UP_TIME_NEAREST_N=5` stores chosen by nearest `set_up_time` to the closed store, restricted to non-treated stores; each control store is used at most once across closures (processed in closure-start order).
  - **Control members (per closure):** Customers whose pre-closure preferred store is in that closure’s matched control-store set, with the same pre-closure thresholds (`≥5` purchases and ratio `≥0.8`).
- **Alternative mode (disabled by default): never-treated closure-specific control.**
  - Never-treated pool = qualified loyal customers whose preferred store never appears in closures.
  - For each closure, keep pool members who were qualified at that closure date (`≥5` purchases before closure start and max single-store share `≥0.8`).

In both modes, one observation unit remains the **consumer–closure event**, and the same consumer can appear in multiple closures.

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

---

## 4. What Has Not Been Done (To-Do)

The following steps align the analysis with Paper 2 and exploit our multi-closure, varying-length structure.

---

### Step 1: Finalize and Validate the Treatment/Control Definition

**1a. Treatment definition (status: partially done).**

- Document and justify: **How many pre-closure purchases** define “regular” (current: 5); sensitivity to this choice.
- **Boundary consumers:** If a consumer’s nearest store closed but another store was within a reasonable distance, are they treated or excluded? Define and implement a rule (e.g., distance threshold, or “all stores within X km closed”).
- **Multiple closures:** Construct **one observation per consumer–closure event**. Decide how to handle consumers who experience several closures (e.g., allow multiple rows per consumer with clustering at consumer or consumer–closure level in inference).

**1b. Control definition (done in current codebase).**

- Implemented in production pipeline: closure-specific matched controls are generated via set-up-time matching and persisted in `outputs/customer-store/closure_pair_registry.csv`.
- Treatment/control pairing used by displacement training is now loaded from this registry (kept closures), ensuring consistency across customer-store and displacement pipelines.

**1c. Remaining validation tasks for treatment/control comparability.**

- Document distribution of closures by:  
  - **Geography** (e.g., district, campus vs non-campus).  
  - **Timing** (calendar date, season).  
  - **Duration** (length of closure; key for later heterogeneity).  
  - **Severity** (e.g., share of a consumer’s historically visited stores that were closed).

Use this to strengthen identification and to run heterogeneity by closure length and severity.

---

### Step 2: Build and Validate the Displacement Classification Model

**2a. Define the prediction target.**

- For each **consumer–closure–period** row, the binary label is: whether the customer made **at least one Luckin purchase** in that period.
- The model is used to predict purchase propensity around closure windows, with control period 0 used as observed validation for the during-closure counterfactual.

**2b. Training data selection.**

- **Sample:** Closures are filtered by `closure_start ≥ 2020-09-01` (from config).
- **Pair source:** Treatment/control pairing is loaded from `outputs/customer-store/closure_pair_registry.csv` (kept closures only), aligned with customer-store analysis logic.
- **Unit:** One observation = (consumer, closure, period), where periods are:
  - `-4, -3, -2, -1` for treatment and control;
  - `0` for control only (during-closure evaluation row).
- **Period length:** Each period length equals closure duration `D = closure_duration_days` (not fixed 7-day weeks).
- **History guardrails:**
  - Closure-level: skip closures lacking sufficient history (`closure_start` must be at least `earliest_order_date + 4D + 8 days`).
  - Member-level: keep only members with first purchase date strictly before earliest pre-period start (`closure_start - 4D`).
- **Label:** Binary = 1 if customer made ≥1 purchase in that period, else 0.
- **Features:** Computed strictly from history up to `period_start - 1 day` (no look-ahead).
- **Train/eval split:**
  - Train: `period <= -2`
  - Eval pre: `period = -1`
  - Eval during: `period = 0` and `group = control`

**2c. Feature variables.**

Single behavioral data source: `order_result.csv`. Demographics from `member_result.csv`. No `order_commodity_result.csv` is used; item-count columns (`coffee_commodity_num`, `food_commodity_num`, etc.) are embedded in `order_result.csv`.

**Features used in X (46 consumer-level features):** All computed from history strictly before `period_start`.

| # | Variable group | Variables | Construction |
|---|----------------|-----------|---------------|
| 1–12 | Purchase frequency & recency | `total_purchase_days_pre`, `purchases_per_week_all_pre`, `purchases_per_week_last_{4w,2w,1w}`, `days_since_last_purchase`, `purchased_in_last_{7,14}_days`, `total_orders_pre`, `total_spend_pre`, `total_spend_last_{4w,2w}` | Computed over all history before `period_start`; rolling windows use deduped purchase-day counts |
| 13–18 | Regularity / habit | `mean_inter_purchase_interval_days`, `std_inter_purchase_interval_days`, `cv_inter_purchase_interval`, `max_gap_between_purchases`, `longest_consecutive_streak_days`, `share_weeks_with_purchase` | Computed per member from sorted unique purchase dates before `period_start` |
| 19–27 | Day-of-week | `share_purchases_dow{0…6}`, `modal_purchase_dow`, `entropy_dow` | DoW share = fraction of all purchase-day rows falling on each weekday; entropy uses natural log |
| 28–29 | Basket & breadth | `avg_basket_size`, `n_order_categories_avg` | `avg_basket_size` = mean total items per order (sum of `*_commodity_num`); `n_order_categories_avg` = mean distinct non-zero category counts per order |
| 30–32 | Store loyalty | `unique_stores_pre`, `preferred_store_ratio`, `second_store_ratio` | Computed from visit-deduplicated (`member_id`, `date`, `dept_id`) order history |
| 33–40 | Order-level behaviour | `avg_discount_per_order`, `coupon_usage_rate`, `avg_coffee_num`, `avg_food_num`, `avg_use_coffee_wallet`, `avg_delivery_pay`, `coffee_share_orders`, `take_address_rate` | Mean per member over history; `avg_delivery_pay` treats NaN (pickup/in-store) as 0; `coffee_share_orders` = share of orders with `coffee_commodity_num > 0`; `take_address_rate` = share with non-null `take_address` |
| 41–46 | Demographics | `gender`, `level`, `has_inviter`, `manufacturer`, `callphone`, `push` | Integer-encoded categorical features (NaN → 1; sorted distinct values → 2, 3, …); encoding map saved to `data/intermediate/demo_encoding_map.csv`. Excludes `birth_year`, `camera`, `location`, `network`, `sdcard`. |

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
- **Scope:** One model is trained per unique closure duration `D` (e.g., `D=10,11,...`), not one global pooled model.

**2e. Evaluation.**

- **Variable importance:** Gain-based importance from `model.get_score(importance_type="gain")`; top 30 features printed and full ranking saved.
- **Accuracy by group and period** (threshold = 0.5):
  - **Treatment, Pre (t=−1):** Predicted vs observed for the last pre-closure week.
  - **Control, Pre (t=−1):** Same.
  - **Control, During (t=0):** Predicted vs observed for actual closure window; yields false positive rate µ and false negative rate λ used for Paper 2 attenuation correction.
- **Label-balance audit:** Saved by closure duration and data split (`train`, `eval_pre_treatment`, `eval_pre_control`, `eval_during`) to monitor class imbalance.

**2f. Outputs from running the code.**

For each duration `D`, artifacts are saved with suffix `_D`, including:

1. **`displacement_model_D.json`**
2. **`variable_importance_D.csv`**
3. **`prediction_accuracy_D.csv`**
4. **`panel_with_scores_D.parquet`**
5. **`displacement_scores_D.csv`**

Additional run-level artifacts:

- **`label_balance_audit.csv`** (class balance by duration and split)
- **training log** in `outputs/displacement_classification/logs/`

**2g. Classify displaced vs non-displaced.**

- **Displaced** = predicted probability ≥ 0.5 (configurable `decision_threshold`).
- **Continuous score use (recommended):** Use raw predicted probability as a soft displacement measure in regression (`Post × Treated × score`) in addition to binary classification.
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
- Also estimate a **continuous-score DDD** using predicted displacement propensity to avoid threshold arbitrariness and test monotonic dose-response.

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
| **Treatment/control** | Pre-closure preferred-store-based treatment; default set-up-time–matched closure-specific control (with one-time control-store assignment); threshold justification; closure-level screening (`MIN_GROUP_SIZE`, control/treatment rate filter); pairing registry (`closure_pair_registry.csv`) shared across pipelines | Boundary/multi-closure rules; formal geo comparability diagnostics; closure severity formalization in estimation |
| **Displacement** | Registry-aligned panel (periods −4…−1 + control t=0, with period length = closure duration `D`); 46 behavioral/demographic features from `order_result.csv`; train/eval split (`<=-2`, `-1`, `0-control`); XGBoost trained per duration `D` (500 rounds, gain importance); duration-suffixed outputs (`displacement_model_D.json`, `variable_importance_D.csv`, `prediction_accuracy_D.csv`, `displacement_scores_D.csv`) plus `label_balance_audit.csv` | Causal-stage displacement decomposition estimates (DDD/event study); continuous-score specification implementation; Paper 2 attenuation correction (µ, λ bounds); threshold/calibration robustness |
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
