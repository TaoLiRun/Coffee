# Displacement Effect Estimation Summary

- Sample rows: 3,154
- Unique members: 1,577
- Unique closures: 1
- Event FE units: 1,577
- Relative periods: [-1, 1]
- Estimation mode: separate_effect=true
- Closure event: `dept_182_closure_2021-08-03`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |        coef |         se |    pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|-----------:|----------:|
| binary_collapsed | post_X_treated        | 3154 |   0.0122188 |  0.00957064 | 0.00512579 | 0.0620655 |
| binary_collapsed | post_X_disp           | 3154 |   0.0122188 | -0.0176351  | 0.00744228 | 0.0179281 |
| binary_collapsed | post_X_treated_X_disp | 3154 |   0.0122188 |  0.010645   | 0.0161308  | 0.509405  |

## Score Spec
| spec            | term                   |    n |   r2_within |       coef |         se |     pvalue |
|:----------------|:-----------------------|-----:|------------:|-----------:|-----------:|-----------:|
| score_collapsed | post_X_treated         | 3154 |   0.0146188 |  0.0128845 | 0.00575332 | 0.0252626  |
| score_collapsed | post_X_score           | 3154 |   0.0146188 | -0.0276892 | 0.0107216  | 0.00989653 |
| score_collapsed | post_X_treated_X_score | 3154 |   0.0146188 |  0.0338424 | 0.0287097  | 0.238664   |

## Event-study Specs
| spec           | term                                                             |        coef |         se |     pvalue |    n |   r2_within |
|:---------------|:-----------------------------------------------------------------|------------:|-----------:|-----------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.0113426  | 0.00527743 | 0.031765   | 3154 |   0.0030814 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.00957064 | 0.00512579 | 0.0620655  | 3154 |   0.0122188 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp             |  0.010645   | 0.0161308  | 0.509405   | 3154 |   0.0122188 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                | -0.0176351  | 0.00744228 | 0.0179281  | 3154 |   0.0122188 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.0128845  | 0.00575332 | 0.0252626  | 3154 |   0.0146188 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score            |  0.0338424  | 0.0287097  | 0.238664   | 3154 |   0.0146188 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered | -0.0276892  | 0.0107216  | 0.00989653 | 3154 |   0.0146188 |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                0 |         nan |      nan | 3154 |
| event_binary_B | pretrend_baseline_joint_zero       |                0 |         nan |      nan | 3154 |
| event_binary_B | pretrend_displacement_joint_zero   |                0 |         nan |      nan | 3154 |
| event_score_C  | pretrend_score_baseline_joint_zero |                0 |         nan |      nan | 3154 |
| event_score_C  | pretrend_score_slope_joint_zero    |                0 |         nan |      nan | 3154 |