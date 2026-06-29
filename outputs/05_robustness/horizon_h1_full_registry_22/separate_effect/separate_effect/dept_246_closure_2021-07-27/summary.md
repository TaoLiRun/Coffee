# Displacement Effect Estimation Summary

- Sample rows: 1,080
- Unique members: 540
- Unique closures: 1
- Event FE units: 540
- Relative periods: [-1, 1]
- Estimation mode: separate_effect=true
- Closure event: `dept_246_closure_2021-07-27`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |        coef |         se |    pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|-----------:|----------:|
| binary_collapsed | post_X_treated        | 1080 |   0.0192903 | -0.00867722 | 0.00522981 | 0.0976606 |
| binary_collapsed | post_X_disp           | 1080 |   0.0192903 | -0.0085849  | 0.0116452  | 0.461317  |
| binary_collapsed | post_X_treated_X_disp | 1080 |   0.0192903 | -0.0551292  | 0.0411136  | 0.180518  |

## Score Spec
| spec            | term                   |    n |   r2_within |       coef |        se |    pvalue |
|:----------------|:-----------------------|-----:|------------:|-----------:|----------:|----------:|
| score_collapsed | post_X_treated         | 1080 |    0.033675 | -0.032619  | 0.0149412 | 0.0294549 |
| score_collapsed | post_X_score           | 1080 |    0.033675 | -0.0191322 | 0.0167189 | 0.252989  |
| score_collapsed | post_X_treated_X_score | 1080 |    0.033675 | -0.100029  | 0.060774  | 0.100364  |

## Event-study Specs
| spec           | term                                                             |        coef |         se |    pvalue |    n |   r2_within |
|:---------------|:-----------------------------------------------------------------|------------:|-----------:|----------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                    | -0.0144582  | 0.00732068 | 0.0487797 | 1080 |  0.00505898 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                    | -0.00867722 | 0.00522981 | 0.0976606 | 1080 |  0.0192903  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp             | -0.0551292  | 0.0411136  | 0.180518  | 1080 |  0.0192903  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                | -0.0085849  | 0.0116452  | 0.461317  | 1080 |  0.0192903  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                    | -0.032619   | 0.0149412  | 0.0294549 | 1080 |  0.033675   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score            | -0.100029   | 0.060774   | 0.100364  | 1080 |  0.033675   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered | -0.0191322  | 0.0167189  | 0.252989  | 1080 |  0.033675   |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                0 |         nan |      nan | 1080 |
| event_binary_B | pretrend_baseline_joint_zero       |                0 |         nan |      nan | 1080 |
| event_binary_B | pretrend_displacement_joint_zero   |                0 |         nan |      nan | 1080 |
| event_score_C  | pretrend_score_baseline_joint_zero |                0 |         nan |      nan | 1080 |
| event_score_C  | pretrend_score_slope_joint_zero    |                0 |         nan |      nan | 1080 |