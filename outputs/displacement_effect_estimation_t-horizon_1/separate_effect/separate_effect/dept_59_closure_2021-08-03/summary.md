# Displacement Effect Estimation Summary

- Sample rows: 6,372
- Unique members: 3,186
- Unique closures: 1
- Event FE units: 3,186
- Relative periods: [-1, 1]
- Estimation mode: separate_effect=true
- Closure event: `dept_59_closure_2021-08-03`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |        coef |         se |    pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|-----------:|----------:|
| binary_collapsed | post_X_treated        | 6372 |  0.00292596 |  0.00261706 | 0.00325445 | 0.421371  |
| binary_collapsed | post_X_disp           | 6372 |  0.00292596 | -0.00533315 | 0.00429478 | 0.214411  |
| binary_collapsed | post_X_treated_X_disp | 6372 |  0.00292596 | -0.0191024  | 0.0111124  | 0.0857094 |

## Score Spec
| spec            | term                   |    n |   r2_within |        coef |         se |    pvalue |
|:----------------|:-----------------------|-----:|------------:|------------:|-----------:|----------:|
| score_collapsed | post_X_treated         | 6372 |   0.0054592 | -0.00331953 | 0.00393164 | 0.398559  |
| score_collapsed | post_X_score           | 6372 |   0.0054592 | -0.0152576  | 0.00650465 | 0.0190551 |
| score_collapsed | post_X_treated_X_score | 6372 |   0.0054592 | -0.0200522  | 0.0179238  | 0.263333  |

## Event-study Specs
| spec           | term                                                             |        coef |         se |    pvalue |    n |   r2_within |
|:---------------|:-----------------------------------------------------------------|------------:|-----------:|----------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                    | -0.001929   | 0.00379265 | 0.611057  | 6372 | 5.85444e-05 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.00261706 | 0.00325445 | 0.421371  | 6372 | 0.00292596  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp             | -0.0191024  | 0.0111124  | 0.0857094 | 6372 | 0.00292596  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                | -0.00533315 | 0.00429478 | 0.214411  | 6372 | 0.00292596  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                    | -0.00331953 | 0.00393164 | 0.398559  | 6372 | 0.0054592   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score            | -0.0200522  | 0.0179238  | 0.263333  | 6372 | 0.0054592   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered | -0.0152576  | 0.00650465 | 0.0190551 | 6372 | 0.0054592   |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                0 |         nan |      nan | 6372 |
| event_binary_B | pretrend_baseline_joint_zero       |                0 |         nan |      nan | 6372 |
| event_binary_B | pretrend_displacement_joint_zero   |                0 |         nan |      nan | 6372 |
| event_score_C  | pretrend_score_baseline_joint_zero |                0 |         nan |      nan | 6372 |
| event_score_C  | pretrend_score_slope_joint_zero    |                0 |         nan |      nan | 6372 |