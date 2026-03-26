# Displacement Effect Estimation Summary

- Sample rows: 3,126
- Unique members: 1,563
- Unique closures: 1
- Event FE units: 1,563
- Relative periods: [-1, 1]
- Estimation mode: separate_effect=true
- Closure event: `dept_44_closure_2021-07-24`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |         coef |         se |      pvalue |
|:-----------------|:----------------------|-----:|------------:|-------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 3126 |   0.0668815 |  0.000686209 | 0.00430901 | 0.873493    |
| binary_collapsed | post_X_disp           | 3126 |   0.0668815 | -0.0649697   | 0.00930678 | 4.32143e-12 |
| binary_collapsed | post_X_treated_X_disp | 3126 |   0.0668815 |  0.0397768   | 0.0199035  | 0.0458376   |

## Score Spec
| spec            | term                   |    n |   r2_within |       coef |         se |      pvalue |
|:----------------|:-----------------------|-----:|------------:|-----------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 3126 |   0.0901337 |  0.0116217 | 0.00655073 | 0.0762415   |
| score_collapsed | post_X_score           | 3126 |   0.0901337 | -0.0983956 | 0.0128059  | 2.70894e-14 |
| score_collapsed | post_X_treated_X_score | 3126 |   0.0901337 |  0.0474085 | 0.0274991  | 0.0849056   |

## Event-study Specs
| spec           | term                                                             |         coef |         se |      pvalue |    n |   r2_within |
|:---------------|:-----------------------------------------------------------------|-------------:|-----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.0130328   | 0.00580434 | 0.0248848   | 3126 |  0.00288126 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.000686209 | 0.00430901 | 0.873493    | 3126 |  0.0668815  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp             |  0.0397768   | 0.0199035  | 0.0458376   | 3126 |  0.0668815  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                | -0.0649697   | 0.00930678 | 4.32143e-12 | 3126 |  0.0668815  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.0116217   | 0.00655073 | 0.0762415   | 3126 |  0.0901337  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score            |  0.0474085   | 0.0274991  | 0.0849056   | 3126 |  0.0901337  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered | -0.0983956   | 0.0128059  | 2.70894e-14 | 3126 |  0.0901337  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                0 |         nan |      nan | 3126 |
| event_binary_B | pretrend_baseline_joint_zero       |                0 |         nan |      nan | 3126 |
| event_binary_B | pretrend_displacement_joint_zero   |                0 |         nan |      nan | 3126 |
| event_score_C  | pretrend_score_baseline_joint_zero |                0 |         nan |      nan | 3126 |
| event_score_C  | pretrend_score_slope_joint_zero    |                0 |         nan |      nan | 3126 |