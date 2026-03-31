# Displacement Effect Estimation Summary

- Sample rows: 6,190
- Unique members: 3,095
- Unique closures: 1
- Event FE units: 3,095
- Relative periods: [-1, 1]
- Estimation mode: separate_effect=true
- Closure event: `dept_124_closure_2021-07-22`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |         coef |         se |      pvalue |
|:-----------------|:----------------------|-----:|------------:|-------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 6190 |   0.0134633 |  0.000977339 | 0.00239473 | 0.683213    |
| binary_collapsed | post_X_disp           | 6190 |   0.0134633 | -0.0209123   | 0.00439475 | 2.04005e-06 |
| binary_collapsed | post_X_treated_X_disp | 6190 |   0.0134633 |  0.00358523  | 0.0064405  | 0.577794    |

## Score Spec
| spec            | term                   |    n |   r2_within |        coef |         se |      pvalue |
|:----------------|:-----------------------|-----:|------------:|------------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 6190 |   0.0232204 |  0.00145889 | 0.00213471 | 0.494398    |
| score_collapsed | post_X_score           | 6190 |   0.0232204 | -0.0396636  | 0.00702164 | 1.76257e-08 |
| score_collapsed | post_X_treated_X_score | 6190 |   0.0232204 |  0.00975069 | 0.0102465  | 0.34137     |

## Event-study Specs
| spec           | term                                                             |         coef |         se |      pvalue |    n |   r2_within |
|:---------------|:-----------------------------------------------------------------|-------------:|-----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.00150613  | 0.00305856 | 0.622449    | 6190 |  7.6242e-05 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.000977339 | 0.00239473 | 0.683213    | 6190 |  0.0134633  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp             |  0.00358523  | 0.0064405  | 0.577794    | 6190 |  0.0134633  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                | -0.0209123   | 0.00439475 | 2.04005e-06 | 6190 |  0.0134633  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.00145889  | 0.00213471 | 0.494398    | 6190 |  0.0232204  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score            |  0.00975069  | 0.0102465  | 0.34137     | 6190 |  0.0232204  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered | -0.0396636   | 0.00702164 | 1.76257e-08 | 6190 |  0.0232204  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                0 |         nan |      nan | 6190 |
| event_binary_B | pretrend_baseline_joint_zero       |                0 |         nan |      nan | 6190 |
| event_binary_B | pretrend_displacement_joint_zero   |                0 |         nan |      nan | 6190 |
| event_score_C  | pretrend_score_baseline_joint_zero |                0 |         nan |      nan | 6190 |
| event_score_C  | pretrend_score_slope_joint_zero    |                0 |         nan |      nan | 6190 |