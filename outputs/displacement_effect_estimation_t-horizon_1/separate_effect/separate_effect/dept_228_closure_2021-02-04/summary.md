# Displacement Effect Estimation Summary

- Sample rows: 1,772
- Unique members: 886
- Unique closures: 1
- Event FE units: 886
- Relative periods: [-1, 1]
- Estimation mode: separate_effect=true
- Closure event: `dept_228_closure_2021-02-04`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |         coef |         se |      pvalue |
|:-----------------|:----------------------|-----:|------------:|-------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 1772 |   0.0433924 | -0.000584847 | 0.00547637 | 0.914976    |
| binary_collapsed | post_X_disp           | 1772 |   0.0433924 | -0.0464245   | 0.00955287 | 1.39007e-06 |
| binary_collapsed | post_X_treated_X_disp | 1772 |   0.0433924 |  0.0378093   | 0.0229781  | 0.100233    |

## Score Spec
| spec            | term                   |    n |   r2_within |        coef |         se |      pvalue |
|:----------------|:-----------------------|-----:|------------:|------------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 1772 |   0.0749858 |  0.00665173 | 0.00770934 | 0.388473    |
| score_collapsed | post_X_score           | 1772 |   0.0749858 | -0.0868405  | 0.0136393  | 3.09412e-10 |
| score_collapsed | post_X_treated_X_score | 1772 |   0.0749858 |  0.0743244  | 0.0354544  | 0.0363359   |

## Event-study Specs
| spec           | term                                                             |         coef |         se |      pvalue |    n |   r2_within |
|:---------------|:-----------------------------------------------------------------|-------------:|-----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.0139561   | 0.00711134 | 0.0500151   | 1772 |  0.00222134 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                    | -0.000584847 | 0.00547637 | 0.914976    | 1772 |  0.0433924  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp             |  0.0378093   | 0.0229781  | 0.100233    | 1772 |  0.0433924  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                | -0.0464245   | 0.00955287 | 1.39007e-06 | 1772 |  0.0433924  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.00665173  | 0.00770934 | 0.388473    | 1772 |  0.0749858  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score            |  0.0743244   | 0.0354544  | 0.0363359   | 1772 |  0.0749858  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered | -0.0868405   | 0.0136393  | 3.09412e-10 | 1772 |  0.0749858  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                0 |         nan |      nan | 1772 |
| event_binary_B | pretrend_baseline_joint_zero       |                0 |         nan |      nan | 1772 |
| event_binary_B | pretrend_displacement_joint_zero   |                0 |         nan |      nan | 1772 |
| event_score_C  | pretrend_score_baseline_joint_zero |                0 |         nan |      nan | 1772 |
| event_score_C  | pretrend_score_slope_joint_zero    |                0 |         nan |      nan | 1772 |