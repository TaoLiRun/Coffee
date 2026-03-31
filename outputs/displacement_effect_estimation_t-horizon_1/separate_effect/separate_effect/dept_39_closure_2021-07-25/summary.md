# Displacement Effect Estimation Summary

- Sample rows: 5,782
- Unique members: 2,891
- Unique closures: 1
- Event FE units: 2,891
- Relative periods: [-1, 1]
- Estimation mode: separate_effect=true
- Closure event: `dept_39_closure_2021-07-25`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |        coef |         se |      pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 5782 |   0.0395378 | -0.00449486 | 0.00385183 | 0.243331    |
| binary_collapsed | post_X_disp           | 5782 |   0.0395378 | -0.0273453  | 0.00335649 | 6.66134e-16 |
| binary_collapsed | post_X_treated_X_disp | 5782 |   0.0395378 | -0.0233067  | 0.0133732  | 0.0814763   |

## Score Spec
| spec            | term                   |    n |   r2_within |        coef |         se |    pvalue |
|:----------------|:-----------------------|-----:|------------:|------------:|-----------:|----------:|
| score_collapsed | post_X_treated         | 5782 |   0.0711894 | -0.00550569 | 0.0035701  | 0.123143  |
| score_collapsed | post_X_score           | 5782 |   0.0711894 | -0.0569594  | 0.00592094 | 0         |
| score_collapsed | post_X_treated_X_score | 5782 |   0.0711894 | -0.0509699  | 0.0233055  | 0.0288197 |

## Event-study Specs
| spec           | term                                                             |        coef |         se |      pvalue |    n |   r2_within |
|:---------------|:-----------------------------------------------------------------|------------:|-----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                    | -0.0164071  | 0.00640555 | 0.0104756   | 5782 |  0.00329066 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                    | -0.00449486 | 0.00385183 | 0.243331    | 5782 |  0.0395378  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp             | -0.0233067  | 0.0133732  | 0.0814763   | 5782 |  0.0395378  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                | -0.0273453  | 0.00335649 | 6.66134e-16 | 5782 |  0.0395378  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                    | -0.00550569 | 0.0035701  | 0.123143    | 5782 |  0.0711894  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score            | -0.0509699  | 0.0233055  | 0.0288197   | 5782 |  0.0711894  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered | -0.0569594  | 0.00592094 | 0           | 5782 |  0.0711894  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                0 |         nan |      nan | 5782 |
| event_binary_B | pretrend_baseline_joint_zero       |                0 |         nan |      nan | 5782 |
| event_binary_B | pretrend_displacement_joint_zero   |                0 |         nan |      nan | 5782 |
| event_score_C  | pretrend_score_baseline_joint_zero |                0 |         nan |      nan | 5782 |
| event_score_C  | pretrend_score_slope_joint_zero    |                0 |         nan |      nan | 5782 |