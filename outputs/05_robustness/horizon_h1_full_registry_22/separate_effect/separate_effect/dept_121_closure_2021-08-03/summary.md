# Displacement Effect Estimation Summary

- Sample rows: 4,436
- Unique members: 2,218
- Unique closures: 1
- Event FE units: 2,218
- Relative periods: [-1, 1]
- Estimation mode: separate_effect=true
- Closure event: `dept_121_closure_2021-08-03`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |         coef |         se |     pvalue |
|:-----------------|:----------------------|-----:|------------:|-------------:|-----------:|-----------:|
| binary_collapsed | post_X_treated        | 4436 |  0.00805365 |  0.00429662  | 0.00324325 | 0.185378   |
| binary_collapsed | post_X_disp           | 4436 |  0.00805365 | -0.0143307   | 0.00546017 | 0.00873501 |
| binary_collapsed | post_X_treated_X_disp | 4436 |  0.00805365 |  0.000817613 | 0.0141744  | 0.954007   |

## Score Spec
| spec            | term                   |    n |   r2_within |         coef |         se |     pvalue |
|:----------------|:-----------------------|-----:|------------:|-------------:|-----------:|-----------:|
| score_collapsed | post_X_treated         | 4436 |   0.0111674 |  0.00438087  | 0.00460153 | 0.341176   |
| score_collapsed | post_X_score           | 4436 |   0.0111674 | -0.024266    | 0.00850578 | 0.00437265 |
| score_collapsed | post_X_treated_X_score | 4436 |   0.0111674 |  0.000433891 | 0.0215263  | 0.983921   |

## Event-study Specs
| spec           | term                                                             |         coef |         se |     pvalue |    n |   r2_within |
|:---------------|:-----------------------------------------------------------------|-------------:|-----------:|-----------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.00476228  | 0.00415212 | 0.251526   | 4436 | 0.000663732 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.00429662  | 0.00324325 | 0.185378   | 4436 | 0.00805365  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp             |  0.000817613 | 0.0141744  | 0.954007   | 4436 | 0.00805365  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                | -0.0143307   | 0.00546017 | 0.00873501 | 4436 | 0.00805365  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.00438087  | 0.00460153 | 0.341176   | 4436 | 0.0111674   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score            |  0.000433891 | 0.0215263  | 0.983921   | 4436 | 0.0111674   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered | -0.024266    | 0.00850578 | 0.00437265 | 4436 | 0.0111674   |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                0 |         nan |      nan | 4436 |
| event_binary_B | pretrend_baseline_joint_zero       |                0 |         nan |      nan | 4436 |
| event_binary_B | pretrend_displacement_joint_zero   |                0 |         nan |      nan | 4436 |
| event_score_C  | pretrend_score_baseline_joint_zero |                0 |         nan |      nan | 4436 |
| event_score_C  | pretrend_score_slope_joint_zero    |                0 |         nan |      nan | 4436 |