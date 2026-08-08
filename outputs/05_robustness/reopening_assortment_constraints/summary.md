# Reopening Assortment Constraints

The analysis uses four fixed seven-day periods before closure and four after reopening.
Realized assortment is compared between each treated store and its five matched controls.

## Main and balanced-panel estimates
| term                  |       coef |   se_crv1 |   pvalue_crv1 |     ci_low |   ci_high |   n |   n_clusters |   event_store_pairs |   within_r2 | outcome              | sample                  | model          |
|:----------------------|-----------:|----------:|--------------:|-----------:|----------:|----:|-------------:|--------------------:|------------:|:---------------------|:------------------------|:---------------|
| treated_store_X_post  | -0.0128912 | 0.034052  |      0.70969  | -0.0847347 | 0.0589522 | 736 |           18 |                  92 |  0.00096978 | core_coverage        | available_unbalanced    | pooled_post    |
| rt_p1_X_treated_store |  0.0205492 | 0.0364821 |      0.580606 | -0.0564212 | 0.0975196 | 736 |           18 |                  92 |  0.0150827  | core_coverage        | available_unbalanced    | immediate_post |
| treated_store_X_post  | -0.0128912 | 0.034052  |      0.70969  | -0.0847347 | 0.0589522 | 736 |           18 |                  92 |  0.00096978 | core_coverage        | complete_8_period_pairs | pooled_post    |
| rt_p1_X_treated_store |  0.0205492 | 0.0364821 |      0.580606 | -0.0564212 | 0.0975196 | 736 |           18 |                  92 |  0.0150827  | core_coverage        | complete_8_period_pairs | immediate_post |
| treated_store_X_post  |  0.306322  | 0.517775  |      0.561896 | -0.786088  | 1.39873   | 723 |           18 |                  92 |  0.00192421 | rarefied_products_50 | available_unbalanced    | pooled_post    |
| rt_p1_X_treated_store |  0.193525  | 0.87532   |      0.827655 | -1.65324   | 2.04029   | 723 |           18 |                  92 |  0.0141989  | rarefied_products_50 | available_unbalanced    | immediate_post |
| treated_store_X_post  |  0.546982  | 0.493226  |      0.282878 | -0.493634  | 1.5876    | 696 |           18 |                  87 |  0.0064402  | rarefied_products_50 | complete_8_period_pairs | pooled_post    |
| rt_p1_X_treated_store |  0.367197  | 0.976863  |      0.711645 | -1.6938    | 2.4282    | 696 |           18 |                  87 |  0.0126361  | rarefied_products_50 | complete_8_period_pairs | immediate_post |
| treated_store_X_post  |  0.0146201 | 0.0250067 |      0.566465 | -0.0381395 | 0.0673796 | 736 |           18 |                  92 |  0.00194329 | menu_jaccard_pre     | available_unbalanced    | pooled_post    |
| rt_p1_X_treated_store |  0.0494954 | 0.0293278 |      0.109737 | -0.012381  | 0.111372  | 736 |           18 |                  92 |  0.0118577  | menu_jaccard_pre     | available_unbalanced    | immediate_post |
| treated_store_X_post  |  0.0146201 | 0.0250067 |      0.566465 | -0.0381395 | 0.0673796 | 736 |           18 |                  92 |  0.00194329 | menu_jaccard_pre     | complete_8_period_pairs | pooled_post    |
| rt_p1_X_treated_store |  0.0494954 | 0.0293278 |      0.109737 | -0.012381  | 0.111372  | 736 |           18 |                  92 |  0.0118577  | menu_jaccard_pre     | complete_8_period_pairs | immediate_post |

## Joint pre-trend tests
| outcome              | sample                  |   f_statistic |   df_num |   df_denom |   pvalue |
|:---------------------|:------------------------|--------------:|---------:|-----------:|---------:|
| core_coverage        | available_unbalanced    |      2.3339   |        3 |         17 | 0.110308 |
| core_coverage        | complete_8_period_pairs |      2.3339   |        3 |         17 | 0.110308 |
| rarefied_products_50 | available_unbalanced    |      1.01066  |        3 |         17 | 0.412273 |
| rarefied_products_50 | complete_8_period_pairs |      0.787101 |        3 |         17 | 0.517549 |
| menu_jaccard_pre     | available_unbalanced    |      0.778963 |        3 |         17 | 0.521818 |
| menu_jaccard_pre     | complete_8_period_pairs |      0.778963 |        3 |         17 | 0.521818 |

## Closure-level moderation of the novelty DDD
| menu_metric                    |   n_closures |   wls_slope_per_sd |   permutation_pvalue_two_sided |   pearson_correlation |
|:-------------------------------|-------------:|-------------------:|-------------------------------:|----------------------:|
| core_coverage_early_did        |           18 |        -0.00110662 |                       0.963807 |           -0.124419   |
| rarefied_products_50_early_did |           17 |         0.0105605  |                       0.621076 |            0.0939173  |
| menu_jaccard_pre_early_did     |           18 |        -0.00108957 |                       0.962008 |           -0.00861157 |

Product sales proxy realized assortment; a product without a recorded sale may still have been available.