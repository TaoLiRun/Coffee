# Displacement Effect Estimation Summary

- Sample rows: 1,534
- Unique members: 767
- Unique closures: 1
- Event FE units: 767
- Relative periods: [-1, 1]
- Estimation mode: separate_effect=true
- Closure event: `dept_225_closure_2021-02-09`
- Closure duration filter days: 10
- Recency filter days: 10
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |        coef |         se |   pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|-----------:|---------:|
| binary_collapsed | post_X_treated        | 1534 |  0.00645369 | -0.00305564 | 0.0152974  | 0.84173  |
| binary_collapsed | post_X_disp           | 1534 |  0.00645369 | -0.015931   | 0.00990978 | 0.108334 |
| binary_collapsed | post_X_treated_X_disp | 1534 |  0.00645369 | -0.0183444  | 0.026297   | 0.485649 |

## Score Spec
| spec            | term                   |    n |   r2_within |       coef |        se |   pvalue |
|:----------------|:-----------------------|-----:|------------:|-----------:|----------:|---------:|
| score_collapsed | post_X_treated         | 1534 |  0.00936905 | -0.0132099 | 0.0136008 | 0.331727 |
| score_collapsed | post_X_score           | 1534 |  0.00936905 | -0.0373089 | 0.016984  | 0.02834  |
| score_collapsed | post_X_treated_X_score | 1534 |  0.00936905 | -0.0118032 | 0.0487184 | 0.808632 |

## Event-study Specs
| spec           | term                                                             |        coef |         se |   pvalue |    n |   r2_within |
|:---------------|:-----------------------------------------------------------------|------------:|-----------:|---------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                    | -0.0134188  | 0.0139029  | 0.33476  | 1534 |  0.00120335 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                    | -0.00305564 | 0.0152974  | 0.84173  | 1534 |  0.00645369 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp             | -0.0183444  | 0.026297   | 0.485649 | 1534 |  0.00645369 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                | -0.015931   | 0.00990978 | 0.108334 | 1534 |  0.00645369 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                    | -0.0132099  | 0.0136008  | 0.331727 | 1534 |  0.00936905 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score            | -0.0118032  | 0.0487184  | 0.808632 | 1534 |  0.00936905 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered | -0.0373089  | 0.016984   | 0.02834  | 1534 |  0.00936905 |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                0 |         nan |      nan | 1534 |
| event_binary_B | pretrend_baseline_joint_zero       |                0 |         nan |      nan | 1534 |
| event_binary_B | pretrend_displacement_joint_zero   |                0 |         nan |      nan | 1534 |
| event_score_C  | pretrend_score_baseline_joint_zero |                0 |         nan |      nan | 1534 |
| event_score_C  | pretrend_score_slope_joint_zero    |                0 |         nan |      nan | 1534 |