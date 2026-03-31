# Displacement Effect Estimation Summary

- Sample rows: 4,388
- Unique members: 2,194
- Unique closures: 1
- Event FE units: 2,194
- Relative periods: [-1, 1]
- Estimation mode: separate_effect=true
- Closure event: `dept_133_closure_2021-07-28`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |        coef |         se |      pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 4388 |   0.0219883 | -0.00185613 | 0.00407625 | 0.648901    |
| binary_collapsed | post_X_disp           | 4388 |   0.0219883 | -0.0228791  | 0.00412459 | 3.25635e-08 |
| binary_collapsed | post_X_treated_X_disp | 4388 |   0.0219883 |  0.0404259  | 0.0115779  | 0.000489543 |

## Score Spec
| spec            | term                   |    n |   r2_within |       coef |         se |      pvalue |
|:----------------|:-----------------------|-----:|------------:|-----------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 4388 |   0.0344251 |  0.0062128 | 0.00386346 | 0.107959    |
| score_collapsed | post_X_score           | 4388 |   0.0344251 | -0.0450046 | 0.00735514 | 1.11349e-09 |
| score_collapsed | post_X_treated_X_score | 4388 |   0.0344251 |  0.0726276 | 0.0170255  | 2.07628e-05 |

## Event-study Specs
| spec           | term                                                             |        coef |         se |      pvalue |    n |   r2_within |
|:---------------|:-----------------------------------------------------------------|------------:|-----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.0129791  | 0.00455347 | 0.00440755  | 4388 |  0.00237601 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                    | -0.00185613 | 0.00407625 | 0.648901    | 4388 |  0.0219883  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp             |  0.0404259  | 0.0115779  | 0.000489543 | 4388 |  0.0219883  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                | -0.0228791  | 0.00412459 | 3.25635e-08 | 4388 |  0.0219883  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.0062128  | 0.00386346 | 0.107959    | 4388 |  0.0344251  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score            |  0.0726276  | 0.0170255  | 2.07628e-05 | 4388 |  0.0344251  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered | -0.0450046  | 0.00735514 | 1.11349e-09 | 4388 |  0.0344251  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                0 |         nan |      nan | 4388 |
| event_binary_B | pretrend_baseline_joint_zero       |                0 |         nan |      nan | 4388 |
| event_binary_B | pretrend_displacement_joint_zero   |                0 |         nan |      nan | 4388 |
| event_score_C  | pretrend_score_baseline_joint_zero |                0 |         nan |      nan | 4388 |
| event_score_C  | pretrend_score_slope_joint_zero    |                0 |         nan |      nan | 4388 |