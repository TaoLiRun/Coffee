# Displacement Effect Estimation Summary

- Sample rows: 3,668
- Unique members: 1,834
- Unique closures: 1
- Event FE units: 1,834
- Relative periods: [-1, 1]
- Estimation mode: separate_effect=true
- Closure event: `dept_220_closure_2021-08-03`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |         coef |         se |   pvalue |
|:-----------------|:----------------------|-----:|------------:|-------------:|-----------:|---------:|
| binary_collapsed | post_X_treated        | 3668 | 0.000386045 | -0.0037968   | 0.00308388 | 0.218416 |
| binary_collapsed | post_X_disp           | 3668 | 0.000386045 |  2.50348e-05 | 0.011303   | 0.998233 |
| binary_collapsed | post_X_treated_X_disp | 3668 | 0.000386045 |  0.002646    | 0.0200501  | 0.895023 |

## Score Spec
| spec            | term                   |    n |   r2_within |        coef |         se |   pvalue |
|:----------------|:-----------------------|-----:|------------:|------------:|-----------:|---------:|
| score_collapsed | post_X_treated         | 3668 | 0.000976813 | -0.00277035 | 0.00674344 | 0.681252 |
| score_collapsed | post_X_score           | 3668 | 0.000976813 | -0.00922329 | 0.0151876  | 0.543733 |
| score_collapsed | post_X_treated_X_score | 3668 | 0.000976813 |  0.00791504 | 0.0295851  | 0.789087 |

## Event-study Specs
| spec           | term                                                             |         coef |         se |   pvalue |    n |   r2_within |
|:---------------|:-----------------------------------------------------------------|-------------:|-----------:|---------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                    | -0.00342553  | 0.00400757 | 0.392794 | 3668 | 0.000348295 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                    | -0.0037968   | 0.00308388 | 0.218416 | 3668 | 0.000386045 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp             |  0.002646    | 0.0200501  | 0.895023 | 3668 | 0.000386045 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                |  2.50348e-05 | 0.011303   | 0.998233 | 3668 | 0.000386045 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                    | -0.00277035  | 0.00674344 | 0.681252 | 3668 | 0.000976813 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score            |  0.00791504  | 0.0295851  | 0.789087 | 3668 | 0.000976813 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered | -0.00922329  | 0.0151876  | 0.543733 | 3668 | 0.000976813 |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                0 |         nan |      nan | 3668 |
| event_binary_B | pretrend_baseline_joint_zero       |                0 |         nan |      nan | 3668 |
| event_binary_B | pretrend_displacement_joint_zero   |                0 |         nan |      nan | 3668 |
| event_score_C  | pretrend_score_baseline_joint_zero |                0 |         nan |      nan | 3668 |
| event_score_C  | pretrend_score_slope_joint_zero    |                0 |         nan |      nan | 3668 |