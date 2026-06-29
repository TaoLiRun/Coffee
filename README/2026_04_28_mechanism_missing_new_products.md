# 2026-04-28 Mechanism Check: Missing New Products During Closures

This note records the standalone mechanism check for the main-sample closure sample in [outputs/customer-store/closure_pair_registry.csv](/home/litao/Coffee/model-free/outputs/customer-store/closure_pair_registry.csv).

Question:

- if treated customers miss access to products newly introduced at comparable open stores during the closure, do closures with more control-store product introductions show more prominent effects?

## Implementation

I implemented the workflow in:

- [scripts/displacement_effect_estimation/run_missing_new_products.py](/home/litao/Coffee/model-free/scripts/displacement_effect_estimation/run_missing_new_products.py)

and also updated:

- [src/displacement_effect_estimation/menu_features.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/menu_features.py)

so the menu-feature code can use the main-sample closure registry through the same `DISPLACEMENT_EFFECT_CLOSURE_REGISTRY` override used by the DDD pipeline.

Outputs are saved under:

- [outputs/05_robustness/missing_new_products/menu_features](/home/litao/Coffee/model-free/outputs/05_robustness/missing_new_products/menu_features)
- [outputs/05_robustness/missing_new_products/separate_effects](/home/litao/Coffee/model-free/outputs/05_robustness/missing_new_products/separate_effects)
- [outputs/05_robustness/missing_new_products/effect_vs_introductions](/home/litao/Coffee/model-free/outputs/05_robustness/missing_new_products/effect_vs_introductions)

For the closure-level comparison, I use the key DDD estimate from the binary collapsed specification:

- `post_X_treated_X_disp`

for each selected store, estimated separately for:

- `n_purchases`
- `variety_seeking_unbalanced`

## 1. Recomputed control-store menu introductions

For the main sample, there are **18** kept closures.

Using [src/displacement_effect_estimation/control_menu_features.py](/home/litao/Coffee/model-free/src/displacement_effect_estimation/control_menu_features.py), the closure-level control-store introduction measure is:

- mean `avg_n_introduced_during_control`: **9.344**
- median `avg_n_introduced_during_control`: **8.900**
- range: **1.8 to 15.4**

The detailed outputs are:

- [outputs/05_robustness/missing_new_products/menu_features/control_menu_introductions_during_closure.csv](/home/litao/Coffee/model-free/outputs/05_robustness/missing_new_products/menu_features/control_menu_introductions_during_closure.csv)
- [outputs/05_robustness/missing_new_products/menu_features/control_menu_introductions_during_closure_detail.csv](/home/litao/Coffee/model-free/outputs/05_robustness/missing_new_products/menu_features/control_menu_introductions_during_closure_detail.csv)

## 2. Ran store-level DDD separately for both outcomes

I ran separate-effect DDD for all **18** selected closures for both outcomes.

Store-level outputs are in:

- [outputs/05_robustness/missing_new_products/separate_effects/n_purchases](/home/litao/Coffee/model-free/outputs/05_robustness/missing_new_products/separate_effects/n_purchases)
- [outputs/05_robustness/missing_new_products/separate_effects/variety_seeking_unbalanced](/home/litao/Coffee/model-free/outputs/05_robustness/missing_new_products/separate_effects/variety_seeking_unbalanced)

The event indexes are:

- [outputs/05_robustness/missing_new_products/separate_effects/n_purchases/event_index.csv](/home/litao/Coffee/model-free/outputs/05_robustness/missing_new_products/separate_effects/n_purchases/event_index.csv)
- [outputs/05_robustness/missing_new_products/separate_effects/variety_seeking_unbalanced/event_index.csv](/home/litao/Coffee/model-free/outputs/05_robustness/missing_new_products/separate_effects/variety_seeking_unbalanced/event_index.csv)

## 3. Do more control-store introductions line up with more prominent effects?

The merged closure-level comparison is:

- [outputs/05_robustness/missing_new_products/effect_vs_introductions/closure_level_effects_vs_control_introductions.csv](/home/litao/Coffee/model-free/outputs/05_robustness/missing_new_products/effect_vs_introductions/closure_level_effects_vs_control_introductions.csv)

The summary and scatter plots are:

- [outputs/05_robustness/missing_new_products/effect_vs_introductions/summary.md](/home/litao/Coffee/model-free/outputs/05_robustness/missing_new_products/effect_vs_introductions/summary.md)
- [outputs/05_robustness/missing_new_products/effect_vs_introductions/n_purchases_binary_coef_vs_avg_introductions.png](/home/litao/Coffee/model-free/outputs/05_robustness/missing_new_products/effect_vs_introductions/n_purchases_binary_coef_vs_avg_introductions.png)
- [outputs/05_robustness/missing_new_products/effect_vs_introductions/variety_seeking_unbalanced_binary_coef_vs_avg_introductions.png](/home/litao/Coffee/model-free/outputs/05_robustness/missing_new_products/effect_vs_introductions/variety_seeking_unbalanced_binary_coef_vs_avg_introductions.png)

### A. `n_purchases`

Across the 18 closures:

- correlation between `avg_n_introduced_during_control` and the store-level key DDD effect: **0.088**
- mean key effect for above-median introduction closures: **0.0055**
- mean key effect for below-median introduction closures: **-0.0100**

Interpretation:

- there is at most a very weak positive relationship;
- the pattern is noisy and not sharp enough to be persuasive as mechanism evidence.

### B. `variety_seeking_unbalanced`

Across the 18 closures:

- correlation between `avg_n_introduced_during_control` and the store-level key DDD effect: **0.050**
- mean key effect for above-median introduction closures: **-0.0255**
- mean key effect for below-median introduction closures: **-0.0650**

Interpretation:

- this does **not** support the mechanism prediction that more control-store introductions should be associated with a more negative novelty effect;
- if anything, the median-split comparison goes in the opposite direction, because the lower-introduction closures have the more negative average novelty effect.

### C. Closures with statistically significant negative novelty effects

There are **3** closures with a negative store-level novelty DDD effect significant at 5%:

| dept_id | avg_n_introduced_during_control | variety DDD coef | p-value |
|---|---:|---:|---:|
| 246 | 6.0 | -0.4046 | 0.0443 |
| 121 | 10.2 | -0.1782 | 0.0029 |
| 182 | 8.4 | -0.2033 | 0.0043 |

These are not concentrated among the highest-introduction closures.

Two useful contrasts:

- highest-introduction closure in the main sample: `dept_id = 238`, average introductions = **15.4**, novelty DDD = **0.0045** (`p = 0.9301`)
- lowest-introduction closure in the main sample: `dept_id = 3`, average introductions = **1.8**, novelty DDD = **0.1151** (`p = 0.0505`)

So the cross-closure pattern is not lining up with the simple “more missing new products -> more negative novelty effect” story.

## Bottom line

This store-level robustness exercise does **not** provide strong support for the missing-new-products mechanism in the main sample.

- The control-store introduction measure was successfully recomputed for all 18 selected closures.
- Separate DDD was successfully estimated for both `n_purchases` and `variety_seeking_unbalanced` at the store level.
- For `n_purchases`, the relationship with control-store introductions is weak.
- For `variety_seeking_unbalanced`, the relationship is not in the predicted direction overall.

At this point, I would treat this mechanism check as descriptive and not as confirmatory evidence for the novelty channel.
