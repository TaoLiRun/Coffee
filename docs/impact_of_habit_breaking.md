# Impact of Habit Breaking: Technical Record

This document is the project-level technical record for the model-free analysis behind **“What Happens After Customers' Purchase Intention is Blocked”**. It is written to be self-contained: a new reader should be able to understand the research design, the data flow, the implemented pipeline, the main estimation choices, and where each part lives in the codebase.

The project studies whether a temporary closure of a customer’s usual Luckin Coffee store breaks later purchasing behavior. The central empirical distinction is between:

- **baseline post-closure demand shifts**, which affect treated customers in general; and
- **blocked purchase effects**, which affect customers who likely would have bought during the closure window had the store remained open.

The pipeline is implemented under:

- scripts: `model-free/scripts`
- source code: `model-free/src`
- main report: `model-free/reports/main_results.qmd`

The current codebase already implements the full main pipeline: closure identification, treatment/control construction, blocked-buyer prediction, pooled and separate-effect estimation, pretrend tests, novelty variants, robustness scripts, and post-reopening push-targeting checks. This file records that full state.

---

## 1. Project Question and Empirical Object

### 1.1 Research question

The project asks:

1. When a customer’s regular store closes temporarily, do they buy less from Luckin after reopening?
2. If not, does the closure still change **what** they buy, especially their willingness to try new products?
3. Can we separate a general post-closure shift in demand from the more specific effect of having an active purchase intention blocked?

The write-up in [main_results.qmd](/home/litao/Coffee/model-free/reports/main_results.qmd:1) frames the key estimand as the additional post-reopening effect for treated customers who were genuinely due to purchase during the closure.

### 1.2 Core conceptual distinction

The project does **not** treat all treated customers as equally interrupted. Instead it distinguishes:

- **blocked buyers**: customers who would have purchased during the closure window absent disruption;
- **non-blocked buyers**: customers assigned to the treated closure event but who would not have purchased in that window anyway.

For treated customers, blocked status is counterfactual and must be predicted. For controls, it is observed from actual behavior during the matched closure window. This asymmetry is the foundation of the blocked-buyer classifier and the triple-difference design.

### 1.3 Why the design is multi-stage

The pipeline has four linked empirical stages:

1. build the closure sample and matched treated/control registry;
2. train a model that predicts closure-window purchase intention using only pre-closure information;
3. attach predicted blocked-buyer measures to member-closure pairs;
4. estimate DiD / DDD / event-study specifications on post-reopening outcomes.

That architecture is reflected directly in the code layout:

- closure and pairing pipeline: [main_customer_store.py](/home/litao/Coffee/model-free/src/customer-store/main_customer_store.py:1)
- blocked-buyer classification: [main.py](/home/litao/Coffee/model-free/src/displacement_classification/main.py:1)
- displacement-effect estimation: [run.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/run.py:1)

---

## 2. Codebase Map

### 2.1 Main runnable entry points

The most important top-level runners are:

- customer-store pipeline wrapper: [scripts/customer-store/run_with_logging.sh](/home/litao/Coffee/model-free/scripts/customer-store/run_with_logging.sh:1)
- displacement-classification wrapper: [scripts/displacement_classification/run_with_logging.sh](/home/litao/Coffee/model-free/scripts/displacement_classification/run_with_logging.sh:1)
- displacement-effect-estimation wrapper: [scripts/displacement_effect_estimation/run_with_logging.sh](/home/litao/Coffee/model-free/scripts/displacement_effect_estimation/run_with_logging.sh:1)
- main-results bundle runner: [scripts/displacement_effect_estimation/run_main_results.sh](/home/litao/Coffee/model-free/scripts/displacement_effect_estimation/run_main_results.sh:1)
- push-targeting-after-reopening runner: [scripts/push_targeting_after_reopening/run_push_targeting_analysis.py](/home/litao/Coffee/model-free/scripts/push_targeting_after_reopening/run_push_targeting_analysis.py:1)

### 2.2 Main source modules

The core logic is spread across these modules:

- store closure detection: [src/store/identify_closures.py](/home/litao/Coffee/model-free/src/store/identify_closures.py:1)
- treatment/control registry and descriptive panels: [src/customer-store/data_processing.py](/home/litao/Coffee/model-free/src/customer-store/data_processing.py:1), [src/customer-store/did_analysis.py](/home/litao/Coffee/model-free/src/customer-store/did_analysis.py:1), [src/customer-store/trend_analysis.py](/home/litao/Coffee/model-free/src/customer-store/trend_analysis.py:1)
- displacement classification data/feature engineering: [src/displacement_classification/data_loading_feature_constructing.py](/home/litao/Coffee/model-free/src/displacement_classification/data_loading_feature_constructing.py:1)
- displacement classification model training and artifact export: [src/displacement_classification/model.py](/home/litao/Coffee/model-free/src/displacement_classification/model.py:1)
- push-feature caching and feature computation for the classifier: [src/displacement_classification/push_event_cache.py](/home/litao/Coffee/model-free/src/displacement_classification/push_event_cache.py:1)
- estimation sample builder: [src/displacement_effect_estimation/data.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/data.py:1)
- econometric specifications: [src/displacement_effect_estimation/specs.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/specs.py:1)
- output writing and diagnostic figures: [src/displacement_effect_estimation/report.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/report.py:1)
- menu-change and control-menu-introduction helpers: [src/displacement_effect_estimation/menu_features.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/menu_features.py:1), [src/displacement_effect_estimation/control_menu_features.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/control_menu_features.py:1)

### 2.3 Important configuration files

- classifier config: [src/displacement_classification/config.json](/home/litao/Coffee/model-free/src/displacement_classification/config.json:1)
- estimator config: [src/displacement_effect_estimation/config.json](/home/litao/Coffee/model-free/src/displacement_effect_estimation/config.json:1)
- push-targeting config: [scripts/push_targeting_after_reopening/config.json](/home/litao/Coffee/model-free/scripts/push_targeting_after_reopening/config.json:1)

---

## 3. Data Inputs and Raw Objects

### 3.1 Main raw data used by the pipeline

The project uses:

- `order_result.csv`: order-level behavior, store, discount, coupon, basket-related columns
- `order_commodity_result.csv` and processed commodity data: product-level purchase history
- `member_result.csv`: member demographics and app attributes
- push CSVs matching `sleep_push_result_*.csv`
- store metadata including `set_up_time`
- geocoded store metadata for closure construction

Relevant loading code:

- customer-store commodity loader: [data_processing.py](/home/litao/Coffee/model-free/src/customer-store/data_processing.py:48)
- customer-store order loader: [data_processing.py](/home/litao/Coffee/model-free/src/customer-store/data_processing.py:73)
- classifier order loader: [data_loading_feature_constructing.py](/home/litao/Coffee/model-free/src/displacement_classification/data_loading_feature_constructing.py:211)
- demographics loader: [data_loading_feature_constructing.py](/home/litao/Coffee/model-free/src/displacement_classification/data_loading_feature_constructing.py:162)

### 3.2 Key derived datasets

The main derived objects are:

- store closures: `outputs/store/store_closures.csv`
- non-university closure sample: `outputs/store/non_uni_store_closures.csv`
- closure-pair registry: `outputs/customer-store/closure_pair_registry.csv`
- full pre-estimation classifier panel with scores: `outputs/displacement_classification/panel_with_scores_*.parquet`
- ex-ante closure-window score file: `outputs/displacement_classification/displacement_scores_t0_ex_ante.csv`
- final estimation samples and regression outputs under `outputs/displacement_effect_estimation/...`

---

## 4. Stage 1: Store Closure Identification

### 4.1 Definition of a closure

Closures are identified as spells of **at least 10 consecutive zero-demand days** for a store, with non-zero demand observed both before and after the zero-demand spell. This is implemented in:

- zero-demand grid construction: [identify_closures.py](/home/litao/Coffee/model-free/src/store/identify_closures.py:45)
- consecutive-zero detection: [identify_closures.py](/home/litao/Coffee/model-free/src/store/identify_closures.py:88)

The exact closure record written out contains:

- `dept_id`
- `closure_start`
- `closure_end`
- `closure_duration_days`

See [identify_closures.py](/home/litao/Coffee/model-free/src/store/identify_closures.py:144).

### 4.2 Geographic and university filtering

After closure spells are found, the script:

- merges geocoded store metadata,
- keeps stores successfully geocoded and within Nanjing bounds,
- flags stores whose address contains `大学` or `学院`,
- writes both the full closure list and a non-university version.

Implemented in:

- geocode merge and coordinate validation: [identify_closures.py](/home/litao/Coffee/model-free/src/store/identify_closures.py:165)
- university flag: [identify_closures.py](/home/litao/Coffee/model-free/src/store/identify_closures.py:202)
- output writing: [identify_closures.py](/home/litao/Coffee/model-free/src/store/identify_closures.py:250)

### 4.3 Closure-duration filter used downstream

The customer-store and estimation pipelines further restrict to closures with:

- `closure_duration_days < 30`

This is enforced by `filter_closures_shorter_than_max()` in [data_processing.py](/home/litao/Coffee/model-free/src/customer-store/data_processing.py:155), with `MAX_CLOSURE_DURATION_DAYS = 30` defined at [data_processing.py](/home/litao/Coffee/model-free/src/customer-store/data_processing.py:28).

So there are two nested closure scopes:

- a broader raw closure table from the zero-demand rule;
- the analysis closure scope after dropping university closures and long closures.

---

## 5. Stage 2: Treated / Control Construction and Closure Registry

### 5.1 Unit of analysis

The core unit is the **member-closure event pair**. A customer can appear multiple times if they are exposed to multiple closures. This logic is baked into the closure registry and every later panel.

### 5.2 “Regular customer” thresholds

A customer is considered eligible only if, before a given closure:

- they have at least `5` unique purchase days;
- their preferred-store loyalty ratio is at least `0.8`.

Defaults are defined at:

- [data_processing.py](/home/litao/Coffee/model-free/src/customer-store/data_processing.py:23)
- [data_loading_feature_constructing.py](/home/litao/Coffee/model-free/src/displacement_classification/data_loading_feature_constructing.py:117)

### 5.3 Preferred-store calculation

Preferred store and preferred-store ratio are computed from unique `(member_id, date, dept_id)` visits. Implemented in:

- full-sample preference function: [data_processing.py](/home/litao/Coffee/model-free/src/customer-store/data_processing.py:177)
- closure-date-specific preference recomputation: [data_processing.py](/home/litao/Coffee/model-free/src/customer-store/data_processing.py:340)

The closure-date-specific version is what matters for treatment and control assignment.

### 5.4 Treatment definition

For a closure event, treated members are those whose **pre-closure preferred store equals the closed store**, with the purchase and loyalty thresholds satisfied. The operative code path is:

- [get_treatment_and_control_members_for_closure()](/home/litao/Coffee/model-free/src/customer-store/data_processing.py:382)

Inside the set-up-time matched mode, treatment is built from the closure-date-specific preferred store:

- [data_processing.py](/home/litao/Coffee/model-free/src/customer-store/data_processing.py:399)

### 5.5 Control-store matching

The default analysis mode uses **set-up-time matched controls**:

- candidate control stores must not be treated stores;
- each control store can be used only once across closures;
- stores with excluded keywords in identifying text are removed from the candidate pool;
- the `n=5` nearest stores by `set_up_time` are selected.

Implemented in:

- setup-time loading: [data_processing.py](/home/litao/Coffee/model-free/src/customer-store/data_processing.py:94)
- keyword exclusion helper: [data_processing.py](/home/litao/Coffee/model-free/src/customer-store/data_processing.py:148)
- nearest-store matching: [data_processing.py](/home/litao/Coffee/model-free/src/customer-store/data_processing.py:282)

The constant `SET_UP_TIME_NEAREST_N = 5` is defined at [data_processing.py](/home/litao/Coffee/model-free/src/customer-store/data_processing.py:34).

### 5.6 Control-member definition

For each closure, control members are customers whose closure-date-specific preferred store belongs to the matched control-store set, and who pass the same purchase and loyalty thresholds. Implemented in:

- [get_closure_control_members_set_up_matched()](/home/litao/Coffee/model-free/src/customer-store/data_processing.py:360)
- [get_treatment_and_control_members_for_closure()](/home/litao/Coffee/model-free/src/customer-store/data_processing.py:382)

### 5.7 Alternative control construction

The codebase still contains an alternative “never-treated control pool” mode, but the active pipeline uses the set-up-time matched design:

- mode switch: `USE_SET_UP_TIME_MATCHED_CONTROL = True` at [data_processing.py](/home/litao/Coffee/model-free/src/customer-store/data_processing.py:32)

### 5.8 Closure-level screening rules

Even after treatment/control assignment, a closure is dropped unless:

- treatment group size is at least `50`;
- control group size is at least `50`;
- control purchase rate during the closure is at least `2.0 ×` the treatment purchase rate during the closure.

Threshold constants:

- `MIN_GROUP_SIZE = 50`: [data_processing.py](/home/litao/Coffee/model-free/src/customer-store/data_processing.py:35)
- `MIN_CTRL_TREAT_RATIO = 2.0`: [data_processing.py](/home/litao/Coffee/model-free/src/customer-store/data_processing.py:36)

These rules are applied when constructing the registry in:

- [build_closure_pair_registry()](/home/litao/Coffee/model-free/src/customer-store/data_processing.py:607)

The closure-level status logic appears at:

- [data_processing.py](/home/litao/Coffee/model-free/src/customer-store/data_processing.py:676)

### 5.9 The closure registry

The closure registry is the project’s central glue dataset. It stores, for each closure:

- closure timing and duration;
- treated store metadata;
- control store IDs, addresses, and set-up times;
- treatment/control counts;
- during-closure treated/control purchase rates;
- screening status and skip reason.

Implemented in:

- [build_closure_pair_registry()](/home/litao/Coffee/model-free/src/customer-store/data_processing.py:607)
- kept-only export wrapper: [build_kept_closure_registry()](/home/litao/Coffee/model-free/src/customer-store/data_processing.py:780)

The main customer-store runner:

- loads and filters inputs,
- builds the kept registry,
- merges descriptive DiD summaries into it,
- then runs weekly trend analysis.

See [main_customer_store.py](/home/litao/Coffee/model-free/src/customer-store/main_customer_store.py:18).

### 5.10 Full vs main registry

The project currently distinguishes:

- `closure_pair_registry_full.csv`: broader retained registry
- `closure_pair_registry.csv`: the main 18-closure registry used for the headline report

The main-results script validates that the main registry contains exactly 18 unique closures and excludes 4 closures relative to the full registry:

- [run_main_results.sh](/home/litao/Coffee/model-free/scripts/displacement_effect_estimation/run_main_results.sh:27)
- registry-scope validation: [run_main_results.sh](/home/litao/Coffee/model-free/scripts/displacement_effect_estimation/run_main_results.sh:53)

---

## 6. Stage 3: Descriptive Customer-Store Panels

Before the blocked-buyer model and the formal DDD pipeline, the code constructs descriptive panels used for the earlier customer-store analysis.

### 6.1 Per-period behavior measures

For each member, period, and closure, the descriptive code computes:

- purchase days per day
- new-product ratio
- mean total discount
- coupon-usage rate

Implemented in:

- [_compute_customer_behavior()](/home/litao/Coffee/model-free/src/customer-store/did_analysis.py:45)

### 6.2 Descriptive pre/during/post windows

The descriptive DiD script builds:

- pre window
- during-closure window
- post window

using user-specified `window_days`, typically 14 or 28. See:

- [analyze_closure_impact()](/home/litao/Coffee/model-free/src/customer-store/did_analysis.py:138)

### 6.3 Weekly trend panels

The project also builds weekly event-time panels for trend plots. These use:

- pre weeks in 7-day bins,
- the closure window as `t=0`,
- post weeks in 7-day bins.

Implemented in:

- [build_week_level_panel()](/home/litao/Coffee/model-free/src/customer-store/data_processing.py:498)
- [run_trend_analysis()](/home/litao/Coffee/model-free/src/customer-store/trend_analysis.py:98)

This descriptive weekly panel is separate from the later event-length-normalized DDD estimation panel.

---

## 7. Stage 4: Blocked-Buyer Classification

### 7.1 Purpose of the classifier

The classifier predicts whether a member would have made at least one Luckin purchase during the closure window had the store remained available. In the code and outputs this is often called:

- displacement
- predicted displaced
- predicted purchase intention
- ex-ante t0 score

These labels all refer to the same substantive object: predicted closure-window purchase intention.

### 7.2 Why the classifier is trained on pre-period rows

The training panel uses only pre-closure periods to learn the mapping from past behavior to whether the member buys at least once in a window of length `D`, where `D` is the closure duration. The classifier then scores the ex-ante closure window (`t=0`) for both treated and control members.

### 7.3 Training panel construction

The classifier constructs a panel with:

- periods `-4, -3, -2, -1` for treated and control
- period `0` for controls only, used for evaluation

Each period length equals that closure’s duration `D = closure_duration_days`.

Implemented in:

- [build_training_panel()](/home/litao/Coffee/model-free/src/displacement_classification/data_loading_feature_constructing.py:324)

Key details:

- closures before the configured filter date are dropped in [main.py](/home/litao/Coffee/model-free/src/displacement_classification/main.py:90)
- panel rows are restricted to closures with `status == kept` in the registry: [filter_closures_to_registry_kept()](/home/litao/Coffee/model-free/src/displacement_classification/data_loading_feature_constructing.py:283)
- closures are skipped if there is insufficient history for `4 × D + 8` days before closure start: [data_loading_feature_constructing.py](/home/litao/Coffee/model-free/src/displacement_classification/data_loading_feature_constructing.py:371)
- members are further required to have first purchase before the earliest pre-period start: [data_loading_feature_constructing.py](/home/litao/Coffee/model-free/src/displacement_classification/data_loading_feature_constructing.py:412)

The label is:

- `1` if the member purchased at least once in that `D`-day window,
- `0` otherwise.

See row construction at [data_loading_feature_constructing.py](/home/litao/Coffee/model-free/src/displacement_classification/data_loading_feature_constructing.py:433).

### 7.4 Ex-ante t0 scoring panel

After training, the project builds a separate panel with one row per treated or control member at the closure window start:

- `period = 0`
- `score_time = "t0_ex_ante"`
- features use only information available before closure start

Implemented in:

- [build_t0_ex_ante_panel()](/home/litao/Coffee/model-free/src/displacement_classification/data_loading_feature_constructing.py:491)

This is the panel that receives the ex-ante blocked-buyer scores used downstream in the DDD estimation.

### 7.5 Classifier features

The classifier engineers a large member-level feature set from order history and demographics. The implementation is in:

- [compute_features_for_panel()](/home/litao/Coffee/model-free/src/displacement_classification/data_loading_feature_constructing.py:626)

Feature families include:

- closure-event covariates:
  - `closure_start_month`, `closure_start_weekday`, `closure_start_season`, `share_visited_stores_closed`, `tenure_days`
  - [data_loading_feature_constructing.py](/home/litao/Coffee/model-free/src/displacement_classification/data_loading_feature_constructing.py:681)
- recency/frequency:
  - total purchase days before the cutoff
  - purchases per week over all history, last 4 weeks, last 2 weeks, last week
  - `days_since_last_purchase`, `purchased_in_last_7_days`, `purchased_in_last_14_days`
  - [data_loading_feature_constructing.py](/home/litao/Coffee/model-free/src/displacement_classification/data_loading_feature_constructing.py:776)
- order counts and spend:
  - total orders and spend, recent spend
  - [data_loading_feature_constructing.py](/home/litao/Coffee/model-free/src/displacement_classification/data_loading_feature_constructing.py:822)
- habit / regularity:
  - mean and standard deviation of interpurchase gaps
  - max purchase gap
  - coefficient of variation of interpurchase interval
  - longest consecutive streak
  - share of weeks with purchase
  - [data_loading_feature_constructing.py](/home/litao/Coffee/model-free/src/displacement_classification/data_loading_feature_constructing.py:852)
- day-of-week preference:
  - day shares, modal purchase day, day-of-week entropy
  - [data_loading_feature_constructing.py](/home/litao/Coffee/model-free/src/displacement_classification/data_loading_feature_constructing.py:910)
- basket and category breadth:
  - average basket size
  - average number of order categories
  - [data_loading_feature_constructing.py](/home/litao/Coffee/model-free/src/displacement_classification/data_loading_feature_constructing.py:942)
- store loyalty:
  - unique stores visited
  - preferred-store ratio
  - second-store ratio
  - [data_loading_feature_constructing.py](/home/litao/Coffee/model-free/src/displacement_classification/data_loading_feature_constructing.py:969)
- order-level aggregates:
  - average discount
  - coupon usage rate
  - average coffee count
  - average food count
  - average coffee-wallet usage
  - average delivery pay
  - coffee-share of orders
  - take-address rate
  - [data_loading_feature_constructing.py](/home/litao/Coffee/model-free/src/displacement_classification/data_loading_feature_constructing.py:998)
- demographics:
  - encoded gender, level, inviter status, manufacturer, callphone, push
  - [load_member_demographics()](/home/litao/Coffee/model-free/src/displacement_classification/data_loading_feature_constructing.py:162)

The code is deliberately strict: if expected source columns or merges are missing, it raises errors rather than silently filling.

### 7.6 Push features in the classifier

The classifier can optionally augment the feature matrix with push-notification history. This branch is controlled by:

- `push_features.enabled` in [src/displacement_classification/config.json](/home/litao/Coffee/model-free/src/displacement_classification/config.json:1)

Push rows are filtered and cached to parquet using:

- [load_or_build_push_events_cache()](/home/litao/Coffee/model-free/src/displacement_classification/push_event_cache.py:95)

Push-derived features include:

- counts of pushes in rolling windows such as 7, 14, 28 days
- trigger-tag composition shares
- counts and shares of pushes with coupon / discount
- coupon and discount intensity
- push-to-purchase latency measures
- follow-up purchase probabilities by trigger tag
- pushes since last purchase

Implemented in:

- [compute_push_features_for_batch()](/home/litao/Coffee/model-free/src/displacement_classification/push_event_cache.py:227)

### 7.7 Feature-matrix caching

To avoid repeated expensive push loading and feature computation, the pipeline caches:

- training feature matrices
- ex-ante t0 feature matrices

The cache key depends on closures, members, push-subset bounds, and run flags. This logic lives in:

- [feature_matrix_cache.py](/home/litao/Coffee/model-free/src/displacement_classification/feature_matrix_cache.py:1)

### 7.8 Model training

The classifier trains one **XGBoost model per closure duration**. This is important because the prediction target is “any purchase within a `D`-day window,” and the base rate changes with `D`.

Main training loop:

- [main.py](/home/litao/Coffee/model-free/src/displacement_classification/main.py:302)

Model settings from config:

- `max_depth = 6`
- `eta = 0.1`
- `objective = binary:logistic`
- `eval_metric = auc`
- `tree_method = hist`
- `num_boost_round = 500`
- `decision_threshold = 0.5`

See [src/displacement_classification/config.json](/home/litao/Coffee/model-free/src/displacement_classification/config.json:1).

GPU availability is auto-detected in:

- [check_gpu()](/home/litao/Coffee/model-free/src/displacement_classification/model.py:47)

### 7.9 Train/evaluation split and audits

The effective split is:

- train: periods `<= -2`
- evaluation on pre period: `-1`
- evaluation on control during-closure period: `0`

This is handled in the model-training loop in [main.py](/home/litao/Coffee/model-free/src/displacement_classification/main.py:318) and summarized in the label-balance audit created at [main.py](/home/litao/Coffee/model-free/src/displacement_classification/main.py:267).

### 7.10 Classifier outputs

For each duration-specific model, the pipeline writes:

- model JSON
- feature importance CSV
- prediction-accuracy CSV
- scored panel parquet
- score summary CSV

Implemented in:

- [save_model_artifacts()](/home/litao/Coffee/model-free/src/displacement_classification/model.py:88)

The ex-ante score file used downstream contains:

- `displacement_prob_t0_ex_ante`
- `predicted_displaced_t0_ex_ante`

These are later normalized to:

- `displacement_prob`
- `disp_binary`

inside the estimation sample builder at [data.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/data.py:104).

---

## 8. Stage 5: Estimation Sample Construction

### 8.1 Main sample source

The estimator starts from:

- the main closure registry
- the ex-ante blocked-buyer scores
- order history for purchase outcomes
- commodity history for novelty outcomes

The entry point is:

- [build_estimation_sample()](/home/litao/Coffee/model-free/src/displacement_effect_estimation/data.py:776)

### 8.2 Loading and harmonizing blocked-buyer scores

`load_displacement_scores()`:

- loads `displacement_scores_t0_ex_ante.csv`
- enforces required columns
- filters scores to the closure scope in the active registry
- merges `days_since_last_purchase` from the cached t0 feature matrix
- constructs standardized downstream fields:
  - `treated`
  - `disp_binary`
  - `displacement_prob`

See:

- [load_displacement_scores()](/home/litao/Coffee/model-free/src/displacement_effect_estimation/data.py:104)

### 8.3 Event-time structure

For each closure and each relative period:

- pre bins: `-K, ..., -1`
- post bins: `1, ..., K`
- period `0` is excluded from the estimation panel

The default `K = 4` is read from config:

- [config.json](/home/litao/Coffee/model-free/src/displacement_effect_estimation/config.json:1)

Window bounds are computed in:

- [_window_bounds()](/home/litao/Coffee/model-free/src/displacement_effect_estimation/data.py:501)

and the main closure loop that builds period rows is in:

- [data.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/data.py:891)

Each pre and post period uses a bin length equal to that event’s `closure_duration_days`.

### 8.4 Outcomes

The estimator supports three outcomes:

- `n_purchases`
- `purchase_incidence_binary`
- `variety_seeking`

Support is declared at:

- [data.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/data.py:791)

#### Purchase-frequency outcome

For `n_purchases`, the outcome is:

- number of purchase days in the period divided by closure duration

Implemented in:

- [data.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/data.py:975)

#### Purchase-incidence-binary outcome

For `purchase_incidence_binary`, the outcome is:

- indicator of any purchase in the period

Implemented at:

- [data.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/data.py:988)

#### Variety-seeking outcome

For `variety_seeking`, the estimator loads member-level product history and computes a window-specific novelty share in:

- [_compute_variety_seeking_for_window()](/home/litao/Coffee/model-free/src/displacement_effect_estimation/data.py:391)

Three modes are implemented:

- `distinct`: each product counted once per member-window
- `instance`: repeated purchase rows count multiple times
- `distinct-only-new`: share of distinct products whose global first-sale date falls in the current or previous estimation window

See:

- [data.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/data.py:404)
- CLI option handling in [run.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/run.py:154)

### 8.5 Balanced vs unbalanced panels

The estimator supports different panel constructions, which determine whether the model is DiD or DDD.

For `n_purchases`:

- default: unbalanced panel -> DDD
- `--no-unbalanced-panel`: balanced panel -> DiD

For `variety_seeking`:

- default: unbalanced panel -> DDD
- `--balanced-panel`: balanced panel -> DiD

These rules are enforced in:

- [run.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/run.py:240)

The actual within-closure balanced-panel filtering is applied inside `build_estimation_sample()` at:

- [data.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/data.py:1010)

For balanced variety panels, there is also an optional period-0 contrast filter that can drop:

- treated members who purchase during the closure window
- control members who do not purchase during the closure window

That filter is implemented in:

- [_filter_members_with_period0_purchases()](/home/litao/Coffee/model-free/src/displacement_effect_estimation/data.py:562)

### 8.6 Optional sample filters

The estimation code supports:

- exact closure-duration filtering
- separate-effect estimation by closure event
- recency filtering based on `days_since_last_purchase`

These are resolved in:

- [_resolve_closure_duration_days()](/home/litao/Coffee/model-free/src/displacement_effect_estimation/data.py:531)
- [_resolve_recency_days()](/home/litao/Coffee/model-free/src/displacement_effect_estimation/data.py:513)
- recency member filtering: [data.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/data.py:546)

### 8.7 Final estimation-sample columns

After the closure loop, the sample builder adds:

- `event_fe_id = member_id | dept_id | closure_start`
- `displacement_prob_centered`
- standardized closure length `closure_length_std`
- optional pre-novelty heterogeneity columns

Implemented in:

- [data.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/data.py:1064)

---

## 9. Stage 6: Econometric Specifications

### 9.1 Estimation engine

All main fixed-effects regressions use `pyfixest.feols()` with:

- member-closure fixed effects
- relative-time fixed effects
- calendar-month fixed effects
- clustered standard errors, default at `member_id`

This is documented and implemented in:

- [specs.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/specs.py:1)

### 9.2 Fixed effects and absorbed variation

Every main specification absorbs:

- `event_fe_id`: member-closure fixed effect
- `rel_t`: relative-period fixed effect
- `calendar_month`: month fixed effect

See the design notes at:

- [specs.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/specs.py:11)

### 9.3 Collapsed specifications

`fit_collapsed_specs()` implements the scalar post-vs-pre models:

- DiD collapsed
- binary blocked-buyer DDD
- continuous-score DDD
- optional pre-novelty heterogeneity extension

Entry point:

- [fit_collapsed_specs()](/home/litao/Coffee/model-free/src/displacement_effect_estimation/specs.py:210)

#### Binary DDD

The binary DDD includes:

- `post_X_treated`
- `post_X_disp`
- `post_X_treated_X_disp`

implemented at:

- [specs.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/specs.py:297)

Interpretation:

- `post_X_treated`: baseline treatment effect for non-blocked customers
- `post_X_disp`: blocked-vs-non-blocked post shift pooled across groups
- `post_X_treated_X_disp`: blocked-buyer treatment effect of interest

#### Continuous-score DDD

The score specification includes:

- `post_X_treated`
- `post_X_score`
- `post_X_treated_X_score`

implemented at:

- [specs.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/specs.py:342)

#### Supplementary logit

For `purchase_incidence_binary`, a supplementary collapsed logit is also fit:

- [specs.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/specs.py:356)

### 9.4 Event-study specifications

`fit_event_study_specs()` implements:

- overall ATT event study
- binary DDD event study
- closure-length heterogeneity event study
- continuous-score event study

Entry point:

- [fit_event_study_specs()](/home/litao/Coffee/model-free/src/displacement_effect_estimation/specs.py:404)

#### Event-study ATT

Specification `event_att` is implemented at:

- [specs.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/specs.py:479)

#### Event-study binary DDD

Specification `event_binary_B` is implemented at:

- [specs.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/specs.py:506)

#### Closure-length heterogeneity

Specification `event_binary_D` augments the binary DDD with length interactions:

- [specs.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/specs.py:557)

The standardized closure-length variable used here comes from:

- [data.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/data.py:1077)

#### Continuous-score event study

Specification `event_score_C` is implemented at:

- [specs.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/specs.py:619)

### 9.5 Pretrend joint tests

The code automatically constructs joint zero tests for pre-period coefficients in each event-study specification using:

- [_joint_zero_test()](/home/litao/Coffee/model-free/src/displacement_effect_estimation/specs.py:164)

Produced tests include:

- ATT pretrend
- baseline pretrend
- displacement pretrend
- score-slope pretrend
- length-interaction pretrends

The specific calls appear throughout:

- [specs.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/specs.py:496)
- [specs.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/specs.py:544)
- [specs.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/specs.py:606)
- [specs.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/specs.py:657)

#### 9.5.1 Audit update: purchase pretrend selector bug, refreshed diagnostics, and reference-period robustness

In the May 2026 audit pass, the pooled purchase-frequency event-study output was found to contain an invalid `pretrend_joint_tests.csv` despite the underlying event-study regression having run successfully. The issue was in coefficient-name selection for the Wald tests, not in the regression formulas themselves.

The event-study formulas are generated in [fit_event_study_specs()](/home/litao/Coffee/model-free/src/displacement_effect_estimation/specs.py:409), while the joint tests rely on `_pre_period_terms()` plus `_joint_zero_test()` in [specs.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/specs.py:140). `pyfixest` named interaction terms in two formats across different runs:

- `C(rel_t, contr.treatment(base=...))[t]:var`
- `rel_t::t:var`

The earlier selector only matched one of those formats, so the pooled purchase bundle ended up with zero matched pre-period restrictions and `NaN` pretrend p-values even though `event_study_results.csv` already contained the relevant coefficients. `_pre_period_terms()` was then extended so it recognizes both naming schemes. After that fix, the canonical headline bundle was regenerated with:

- [run_main_results.sh](/home/litao/Coffee/model-free/scripts/displacement_effect_estimation/run_main_results.sh:1)

and recorded in:

- [run_manifest.json](/home/litao/Coffee/model-free/outputs/displacement_effect_estimation/metadata/run_manifest.json:1)

The refreshed diagnostic conclusions are:

- purchase-frequency ATT pretrend test: non-rejection;
- purchase-frequency blocked-buyer displacement pretrend test: rejection;
- novelty ATT pretrend test: non-rejection;
- novelty blocked-buyer displacement pretrend test: non-rejection.

For the maintained report narrative, the key object is the **blocked-buyer DDD path**, not the overall purchase ATT path. The important technical conclusion is therefore that the **purchase-frequency blocked-buyer event-study fails the stricter dynamic pretrend test** in the refreshed pooled run, even though the simpler purchase ATT pretrend test does not reject.

The same audit pass also introduced a configurable event-study omitted pre-period through `--event-study-ref-period` in:

- [run.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/run.py:97)
- [fit_event_study_specs()](/home/litao/Coffee/model-free/src/displacement_effect_estimation/specs.py:409)

This was used to test whether choosing the first pre period (`rel_t = -4`) as the omitted category materially improved the purchase-frequency dynamic evidence. It did not. The individual event-study coefficients were re-centered, but the joint pretrend tests were unchanged. The temporary `ref=-4` bundles were therefore deleted, and the maintained canonical outputs remain the default `ref=-1` runs.

The same audit workflow was also applied to the `distinct-only-new` market-new novelty outcome. That bundle was rerun under the maintained `ref=-1` normalization, and the refreshed event-study diagnostics remained supportive:

- market-new ATT pretrend test: non-rejection;
- market-new blocked-buyer displacement pretrend test: non-rejection.

So, across the two novelty outcomes now maintained in the report:

- member-first novelty-seeking: dynamic pretrend diagnostics are acceptable;
- market-new novelty-seeking (`distinct-only-new`): dynamic pretrend diagnostics are also acceptable;
- purchase-frequency blocked-buyer dynamics remain the only headline outcome with a rejected blocked-buyer event-study pretrend test.

---

## 10. Stage 7: Output Writing and Main Estimation Runs

### 10.1 Output bundle written for each run

Each estimation run writes:

- `estimation_sample.csv`
- `ddd_binary_results.csv`
- `ddd_binary_fit.csv`
- `ddd_score_results.csv`
- `ddd_score_fit.csv`
- `event_study_results.csv`
- `event_study_fit.csv`
- `pretrend_joint_tests.csv`
- `spec_comparison.csv`
- `summary.md`

Implemented in:

- [save_outputs()](/home/litao/Coffee/model-free/src/displacement_effect_estimation/report.py:18)

### 10.2 Variety diagnostic plot

For `variety_seeking` runs, the code can also create:

- period-0 inclusive variety panel trend plot
- per-period treatment/control mean-SD statistics

Implemented in:

- [save_variety_panel_plot()](/home/litao/Coffee/model-free/src/displacement_effect_estimation/report.py:78)

### 10.3 Event-study coefficient plots

The reporting layer now also writes dynamic coefficient-path figures directly from the event-study regression output. This is implemented in:

- [save_event_study_plots()](/home/litao/Coffee/model-free/src/displacement_effect_estimation/report.py:146)

The plotting helper:

- parses `rel_t` back out of the pyfixest term names;
- classifies coefficients into ATT, baseline-treatment, and displacement paths;
- computes pointwise 95% confidence intervals as `coef ± 1.96 * se`;
- writes `event_study_plot_data.csv`;
- saves publication-ready PNG figures.

For pooled headline runs, the new files are:

- `event_study_att.png`
- `event_study_baseline.png`
- `event_study_displacement.png`

These figures are now generated for:

- the purchase-frequency bundle;
- the headline member-first novelty-seeking bundle;
- the market-new novelty bundle (`distinct-only-new`);

and are referenced from the main report where relevant.

### 10.4 Dynamic heterogeneity event study for pre-novelty groups

The original pre-novelty heterogeneity implementation was **collapsed only**: the lower-pre-novelty group (`novelty_pre_high == 0`) was the baseline subgroup, and the higher-pre-novelty group entered through additional post interactions. This is implemented in [fit_collapsed_specs()](/home/litao/Coffee/model-free/src/displacement_effect_estimation/specs.py:220).

In the May 2026 extension, the same logic was implemented period by period in the event-study specification so that the dynamic path matches the collapsed heterogeneity design rather than an ad hoc sample split.

The event-study heterogeneity specification augments the binary DDD event study with:

- `i(rel_t, treated_X_novelty_pre_high, ref=ref_period)`
- `i(rel_t, disp_X_novelty_pre_high, ref=ref_period)`
- `i(rel_t, treated_X_disp_X_novelty_pre_high, ref=ref_period)`

alongside the original baseline-path terms:

- `i(rel_t, treated, ref=ref_period)`
- `i(rel_t, treated_X_disp, ref=ref_period)`
- `i(rel_t, disp_binary, ref=ref_period)`

This is implemented in:

- [fit_event_study_specs()](/home/litao/Coffee/model-free/src/displacement_effect_estimation/specs.py:409)

Interpretation:

- the `:treated_X_disp` path inside `event_binary_B_pre_novelty_split` is the **lower-group dynamic blocked-buyer triple interaction**;
- the `:treated_X_disp_X_novelty_pre_high` path is the **high-group increment relative to the lower group**;
- the high-group blocked-buyer path is therefore the period-by-period sum of those two coefficient paths.

This mirrors the collapsed heterogeneity interpretation exactly:

- lower group = baseline coefficients;
- high group = baseline + incremental coefficients.

Two pooled runs are now maintained for this extension:

- median split: `outputs/displacement_effect_estimation/variety_seeking_distinct_pre_novelty_heterogeneity`
- quartile-tail split: `outputs/displacement_effect_estimation/variety_seeking_distinct_pre_novelty_heterogeneity_quartile_tails`

The lower-group dynamic displacement plots saved from that exact event-study heterogeneity specification are:

- [event_study_displacement_lower_group_median.png](/home/litao/Coffee/model-free/outputs/displacement_effect_estimation/variety_seeking_distinct_pre_novelty_heterogeneity/event_study_displacement_lower_group_median.png:1)
- [event_study_displacement_lower_group_quartile_tails.png](/home/litao/Coffee/model-free/outputs/displacement_effect_estimation/variety_seeking_distinct_pre_novelty_heterogeneity_quartile_tails/event_study_displacement_lower_group_quartile_tails.png:1)

The resulting dynamic estimates line up with the collapsed heterogeneity table:

- under the median split, the lower-group post-period blocked-buyer path is strongly negative, approximately `-0.268`, `-0.269`, `-0.281`, and `-0.299` in periods `1` through `4`;
- under the quartile-tail split, the lower-group post-period blocked-buyer path is even more negative, approximately `-0.419`, `-0.397`, `-0.415`, and `-0.452`;
- the corresponding high-group increment path is strongly positive in post periods, consistent with the collapsed heterogeneity result that the high-pre-novelty subgroup reverses the sign of the lower-group effect.

This extension was added because plotting the baseline event-study on a filtered heterogeneity sample does **not** reproduce the same estimand as the collapsed heterogeneity regression. The maintained implementation now uses the correct event-study analog of the heterogeneity specification already used in the report.

### 10.5 Main pooled runner

The main estimator CLI is:

- [run.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/run.py:97)

It:

- parses all run options,
- builds the sample,
- fits collapsed and event-study specs,
- writes outputs,
- optionally writes pre-novelty histograms and variety plots,
- optionally runs separate-effect bundles.

Aggregate run path:

- [run.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/run.py:366)

Separate-effect run path:

- [run.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/run.py:295)

### 10.6 Supported run matrix

The maintained run matrix and examples are documented in:

- [scripts/displacement_effect_estimation/RUN_VERSIONS.md](/home/litao/Coffee/model-free/scripts/displacement_effect_estimation/RUN_VERSIONS.md:1)

This file is the best compact reference for:

- pooled vs separate-effect runs
- balanced vs unbalanced panels
- novelty mode variants
- pre-novelty heterogeneity variant
- recency and duration filters

### 10.7 Main-results bundle script

The most reproducible high-level script for the headline results is:

- [run_main_results.sh](/home/litao/Coffee/model-free/scripts/displacement_effect_estimation/run_main_results.sh:1)

It:

- validates the closure-registry scope,
- snapshots the active registry,
- runs the pooled purchase-frequency, purchase-incidence, and novelty pipelines,
- validates each output bundle,
- writes a run manifest,
- assembles a report body fragment from regression outputs.

See especially:

- output validation: [run_main_results.sh](/home/litao/Coffee/model-free/scripts/displacement_effect_estimation/run_main_results.sh:96)
- purchase / incidence / novelty runs: [run_main_results.sh](/home/litao/Coffee/model-free/scripts/displacement_effect_estimation/run_main_results.sh:168)

---

## 11. Novelty-Seeking Extensions and Heterogeneity

### 11.1 Distinct vs instance vs distinct-only-new

The project implements three novelty definitions in the estimator. The most important implementation details are in:

- [_compute_variety_seeking_for_window()](/home/litao/Coffee/model-free/src/displacement_effect_estimation/data.py:391)

Interpretations:

- `distinct`: variety share over distinct products in the member-window
- `instance`: variety share over all purchase instances in the member-window
- `distinct-only-new`: share of distinct products that are newly introduced at the chain level in the current or previous estimation bin

### 11.2 Pre-period novelty heterogeneity

The project includes an additional pooled DDD extension for the headline `distinct` novelty measure. It:

- computes each member-closure episode’s mean pre-period novelty;
- splits episodes into high vs baseline using either the median or the mode threshold;
- optionally uses only top and bottom quartile tails;
- augments the collapsed DDD with:
  - `post × treated × high`
  - `post × blocked × high`
  - `post × treated × blocked × high`

Implemented in:

- heterogeneity-column builder: [_attach_novelty_pre_heterogeneity_cols()](/home/litao/Coffee/model-free/src/displacement_effect_estimation/data.py:688)
- regression augmentation: [specs.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/specs.py:311)
- histogram export: [save_pre_novelty_histogram()](/home/litao/Coffee/model-free/src/displacement_effect_estimation/report.py:143)

The CLI constraints and examples are documented in:

- [RUN_VERSIONS.md](/home/litao/Coffee/model-free/scripts/displacement_effect_estimation/RUN_VERSIONS.md:109)

---

## 12. Robustness and Mechanism Scripts

### 12.1 Excluding treated cross-store purchasers during closure

To test whether same-chain substitution during the closure explains the main effects, the project identifies treated member-events that purchased at a different Luckin store during the closure window.

Implemented in:

- treated cross-store flag builder: [run_excluding_cross_store_treated.py](/home/litao/Coffee/model-free/scripts/displacement_effect_estimation/run_excluding_cross_store_treated.py:59)
- sample attachment and filtering: [run_excluding_cross_store_treated.py](/home/litao/Coffee/model-free/scripts/displacement_effect_estimation/run_excluding_cross_store_treated.py:99)
- pooled subgroup-difference DDD test: [run_excluding_cross_store_treated.py](/home/litao/Coffee/model-free/scripts/displacement_effect_estimation/run_excluding_cross_store_treated.py:130)

This script writes both:

- reduced-sample main-effect bundles
- pooled equality tests comparing cross-store vs non-cross-store treated subgroups

### 12.2 Missing new products / missed menu exposure mechanism

The project includes a mechanism script for whether treated customers miss exposure to new products introduced elsewhere in the chain during the closure.

Main runner:

- [run_missing_new_products.py](/home/litao/Coffee/model-free/scripts/displacement_effect_estimation/run_missing_new_products.py:1)

This script:

- builds separate-effect estimates for each closure;
- extracts closure-level blocked-buyer coefficients;
- computes control-store menu-introduction intensity during the closure;
- studies the relation between introduction intensity and closure-level effects;
- runs within-length-bin permutation tests.

### 12.3 Menu-change feature builders

Two helper modules support these exercises:

- treatment-store menu before/after closure windows:
  - [menu_features.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/menu_features.py:199)
- control-store introduced products during the treatment store’s closure:
  - [control_menu_features.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/control_menu_features.py:145)

These modules write CSVs summarizing:

- menu size before and after
- products introduced and removed
- control-store introduction counts during closure

---

## 13. Post-Reopening Push-Targeting Check

### 13.1 Purpose

One concern is that blocked and non-blocked customers might receive different push marketing after reopening, which could contaminate the interpretation of the blocked-buyer coefficients.

### 13.2 Input objects

The push-targeting analysis starts from:

- the main closure registry
- the ex-ante blocked-buyer scores
- raw push CSVs

These are loaded in:

- [load_main_scores()](/home/litao/Coffee/model-free/scripts/push_targeting_after_reopening/run_push_targeting_analysis.py:41)

### 13.3 Construction of post-reopening windows

The script builds the same post-reopening event-length windows used in the main analysis:

- [build_post_windows()](/home/litao/Coffee/model-free/scripts/push_targeting_after_reopening/run_push_targeting_analysis.py:122)

### 13.4 Push filtering and panel creation

Push records are:

- loaded chunkwise from all matching CSVs,
- filtered to sample members and relevant dates,
- matched into member-event-window rows,
- aggregated into counts and intensity measures.

Implemented in:

- [filter_push_records()](/home/litao/Coffee/model-free/scripts/push_targeting_after_reopening/run_push_targeting_analysis.py:150)
- [build_push_panel()](/home/litao/Coffee/model-free/scripts/push_targeting_after_reopening/run_push_targeting_analysis.py:231)

Main metrics include:

- `n_push`
- `push_per_day`
- `n_push_with_coupon`
- `share_push_coupon`
- `mean_coupon`
- `n_push_with_discount`
- `share_push_discount`
- `mean_discount`

### 13.5 Inferential checks

The script reports:

- group summaries
- Welch mean tests within treatment and control groups
- subgroup regressions
- treatment-minus-control gap-difference tests

This is why the report can argue that differential push targeting does not explain the headline blocked-buyer results.

---

## 14. Reproducibility Sequence

For a new user who wants the main pipeline in order, the logical sequence is:

1. Build closures.
   - run [identify_closures.py](/home/litao/Coffee/model-free/src/store/identify_closures.py:1)
2. Build the customer-store registry and descriptive outputs.
   - run [scripts/customer-store/run_with_logging.sh](/home/litao/Coffee/model-free/scripts/customer-store/run_with_logging.sh:1)
3. Train the blocked-buyer classifier and generate ex-ante t0 scores.
   - run [scripts/displacement_classification/run_with_logging.sh](/home/litao/Coffee/model-free/scripts/displacement_classification/run_with_logging.sh:1)
4. Run the pooled displacement-effect estimation.
   - run [scripts/displacement_effect_estimation/run_with_logging.sh](/home/litao/Coffee/model-free/scripts/displacement_effect_estimation/run_with_logging.sh:1)
5. For the headline bundle, use:
   - [run_main_results.sh](/home/litao/Coffee/model-free/scripts/displacement_effect_estimation/run_main_results.sh:1)
6. For push-targeting and mechanism checks, run the dedicated helper scripts:
   - [run_push_targeting_analysis.py](/home/litao/Coffee/model-free/scripts/push_targeting_after_reopening/run_push_targeting_analysis.py:1)
   - [run_excluding_cross_store_treated.py](/home/litao/Coffee/model-free/scripts/displacement_effect_estimation/run_excluding_cross_store_treated.py:1)
   - [run_missing_new_products.py](/home/litao/Coffee/model-free/scripts/displacement_effect_estimation/run_missing_new_products.py:1)

---

## 15. What the Current Pipeline Produces

At the current state of the codebase, the project can produce:

- a validated main closure registry for the 18-closure headline sample;
- ex-ante blocked-buyer scores for treated and control members;
- pooled DDD estimates for:
  - purchase frequency
  - purchase incidence
  - novelty seeking
- continuous-score DDD estimates;
- event-study estimates with joint pretrend tests;
- closure-length heterogeneity event-study terms;
- separate-effect bundles for each closure event;
- novelty robustness variants:
  - `distinct`
  - `instance`
  - `distinct-only-new`
- pre-period novelty heterogeneity splits;
- cross-store-treated exclusion robustness;
- control-menu-introduction / missing-new-products mechanism outputs;
- post-reopening push-targeting diagnostics.

So the project is no longer in an early “descriptive only” stage. The current codebase already implements the full blocked-buyer causal pipeline described in the main report.

---

## 16. File References Summary

If someone new wants the shortest path into the project, these are the highest-value files:

- research narrative: [main_results.qmd](/home/litao/Coffee/model-free/reports/main_results.qmd:1)
- registry and treated/control construction: [data_processing.py](/home/litao/Coffee/model-free/src/customer-store/data_processing.py:607)
- classifier panel and features: [data_loading_feature_constructing.py](/home/litao/Coffee/model-free/src/displacement_classification/data_loading_feature_constructing.py:324), [data_loading_feature_constructing.py](/home/litao/Coffee/model-free/src/displacement_classification/data_loading_feature_constructing.py:626)
- classifier training: [main.py](/home/litao/Coffee/model-free/src/displacement_classification/main.py:72)
- estimation sample builder: [data.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/data.py:776)
- econometric specs: [specs.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/specs.py:210), [specs.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/specs.py:404)
- pooled runner: [run.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/run.py:97)
- headline bundle script: [run_main_results.sh](/home/litao/Coffee/model-free/scripts/displacement_effect_estimation/run_main_results.sh:1)
