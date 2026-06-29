# Displacement Effect Estimation Summary

- Sample rows: 3,378
- Unique members: 1,689
- Unique closures: 1
- Event FE units: 1,689
- Relative periods: [-1, 1]
- Estimation mode: separate_effect=true
- Closure event: `dept_238_closure_2021-07-24`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |        coef |         se |    pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|-----------:|----------:|
| binary_collapsed | post_X_treated        | 3378 |  0.00742114 |  0.00402264 | 0.00331556 | 0.225199  |
| binary_collapsed | post_X_disp           | 3378 |  0.00742114 | -0.0140662  | 0.00593746 | 0.0179455 |
| binary_collapsed | post_X_treated_X_disp | 3378 |  0.00742114 |  0.0013756  | 0.00814915 | 0.865972  |

## Score Spec
| spec            | term                   |    n |   r2_within |        coef |         se |     pvalue |
|:----------------|:-----------------------|-----:|------------:|------------:|-----------:|-----------:|
| score_collapsed | post_X_treated         | 3378 |    0.015695 |  0.00446389 | 0.00303771 | 0.141886   |
| score_collapsed | post_X_score           | 3378 |    0.015695 | -0.0293263  | 0.00943673 | 0.00191709 |
| score_collapsed | post_X_treated_X_score | 3378 |    0.015695 |  0.00464879 | 0.0126616  | 0.713547   |

## Event-study Specs
| spec           | term                                                             |        coef |         se |     pvalue |    n |   r2_within |
|:---------------|:-----------------------------------------------------------------|------------:|-----------:|-----------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.00408598 | 0.00392329 | 0.297808   | 3378 | 0.000613013 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.00402264 | 0.00331556 | 0.225199   | 3378 | 0.00742114  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp             |  0.0013756  | 0.00814915 | 0.865972   | 3378 | 0.00742114  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                | -0.0140662  | 0.00593746 | 0.0179455  | 3378 | 0.00742114  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.00446389 | 0.00303771 | 0.141886   | 3378 | 0.015695    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score            |  0.00464879 | 0.0126616  | 0.713547   | 3378 | 0.015695    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered | -0.0293263  | 0.00943673 | 0.00191709 | 3378 | 0.015695    |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                0 |         nan |      nan | 3378 |
| event_binary_B | pretrend_baseline_joint_zero       |                0 |         nan |      nan | 3378 |
| event_binary_B | pretrend_displacement_joint_zero   |                0 |         nan |      nan | 3378 |
| event_score_C  | pretrend_score_baseline_joint_zero |                0 |         nan |      nan | 3378 |
| event_score_C  | pretrend_score_slope_joint_zero    |                0 |         nan |      nan | 3378 |