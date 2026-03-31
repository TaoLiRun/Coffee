# Displacement Effect Estimation Summary

- Sample rows: 1,348
- Unique members: 674
- Unique closures: 1
- Event FE units: 674
- Relative periods: [-1, 1]
- Estimation mode: separate_effect=true
- Closure event: `dept_8_closure_2021-05-27`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |         coef |        se |    pvalue |
|:-----------------|:----------------------|-----:|------------:|-------------:|----------:|----------:|
| binary_collapsed | post_X_treated        | 1348 |   0.0152712 |  0.000137131 | 0.0068262 | 0.983978  |
| binary_collapsed | post_X_disp           | 1348 |   0.0152712 | -0.0275765   | 0.0124816 | 0.0274841 |
| binary_collapsed | post_X_treated_X_disp | 1348 |   0.0152712 |  0.00492151  | 0.0248548 | 0.843097  |

## Score Spec
| spec            | term                   |    n |   r2_within |        coef |         se |    pvalue |
|:----------------|:-----------------------|-----:|------------:|------------:|-----------:|----------:|
| score_collapsed | post_X_treated         | 1348 |   0.0265181 |  0.00158598 | 0.00801532 | 0.843207  |
| score_collapsed | post_X_score           | 1348 |   0.0265181 | -0.0468353  | 0.0179196  | 0.0091585 |
| score_collapsed | post_X_treated_X_score | 1348 |   0.0265181 |  0.00330544 | 0.0363141  | 0.927501  |

## Event-study Specs
| spec           | term                                                             |         coef |         se |    pvalue |    n |   r2_within |
|:---------------|:-----------------------------------------------------------------|-------------:|-----------:|----------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  2.45919e-05 | 0.00925906 | 0.997882  | 1348 | 9.34266e-09 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.000137131 | 0.0068262  | 0.983978  | 1348 | 0.0152712   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp             |  0.00492151  | 0.0248548  | 0.843097  | 1348 | 0.0152712   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                | -0.0275765   | 0.0124816  | 0.0274841 | 1348 | 0.0152712   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.00158598  | 0.00801532 | 0.843207  | 1348 | 0.0265181   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score            |  0.00330544  | 0.0363141  | 0.927501  | 1348 | 0.0265181   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered | -0.0468353   | 0.0179196  | 0.0091585 | 1348 | 0.0265181   |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                0 |         nan |      nan | 1348 |
| event_binary_B | pretrend_baseline_joint_zero       |                0 |         nan |      nan | 1348 |
| event_binary_B | pretrend_displacement_joint_zero   |                0 |         nan |      nan | 1348 |
| event_score_C  | pretrend_score_baseline_joint_zero |                0 |         nan |      nan | 1348 |
| event_score_C  | pretrend_score_slope_joint_zero    |                0 |         nan |      nan | 1348 |