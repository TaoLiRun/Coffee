# Displacement Effect Estimation Summary

- Sample rows: 3,068
- Unique members: 767
- Unique closures: 1
- Event FE units: 767
- Relative periods: [-2, -1, 1, 2]
- Estimation mode: separate_effect=true
- Closure event: `dept_225_closure_2021-02-09`
- Closure duration filter days: 10
- Recency filter days: 10
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |        coef |         se |     pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|-----------:|-----------:|
| binary_collapsed | post_X_treated        | 3068 |   0.0109125 | -0.00848282 | 0.0132228  | 0.521372   |
| binary_collapsed | post_X_disp           | 3068 |   0.0109125 | -0.0373408  | 0.00900752 | 3.7691e-05 |
| binary_collapsed | post_X_treated_X_disp | 3068 |   0.0109125 | -0.0117172  | 0.0240351  | 0.626041   |

## Score Spec
| spec            | term                   |    n |   r2_within |        coef |        se |      pvalue |
|:----------------|:-----------------------|-----:|------------:|------------:|----------:|------------:|
| score_collapsed | post_X_treated         | 3068 |    0.017798 | -0.0148092  | 0.0124317 | 0.233929    |
| score_collapsed | post_X_score           | 3068 |    0.017798 | -0.0803344  | 0.0153834 | 2.28094e-07 |
| score_collapsed | post_X_treated_X_score | 3068 |    0.017798 | -0.00685778 | 0.0463374 | 0.882384    |

## Event-study Specs
| spec           | term                                                              |        coef |         se |      pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|------------:|-----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0035124  | 0.0159498  | 0.825761    | 3068 | 0.000750812 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.0134188  | 0.0139074  | 0.334918    | 3068 | 0.000750812 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0132033  | 0.0172973  | 0.445511    | 3068 | 0.000750812 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00810277 | 0.0150195  | 0.589709    | 3068 | 0.0217726   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00305564 | 0.0153074  | 0.841832    | 3068 | 0.0217726   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0220128  | 0.0173979  | 0.206166    | 3068 | 0.0217726   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0206361  | 0.0291179  | 0.478721    | 3068 | 0.0217726   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0183444  | 0.0263142  | 0.485934    | 3068 | 0.0217726   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.0155461  | 0.0325526  | 0.633093    | 3068 | 0.0217726   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.051103   | 0.0106419  | 1.88925e-06 | 3068 | 0.0217726   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.015931   | 0.00991626 | 0.108564    | 3068 | 0.0217726   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.00764755 | 0.0124008  | 0.537618    | 3068 | 0.0217726   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00318568 | 0.0153141  | 0.835267    | 3068 | 0.0326172   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.0132099  | 0.0136097  | 0.332044    | 3068 | 0.0326172   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0132228  | 0.0169387  | 0.435265    | 3068 | 0.0326172   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.00820346 | 0.0501724  | 0.870164    | 3068 | 0.0326172   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.0118032  | 0.0487503  | 0.808755    | 3068 | 0.0326172   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.00629114 | 0.0637892  | 0.921463    | 3068 | 0.0326172   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.103832   | 0.0178282  | 8.45099e-09 | 3068 | 0.0326172   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0373089  | 0.0169951  | 0.0284433   | 3068 | 0.0326172   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0195275  | 0.0217536  | 0.369644    | 3068 | 0.0326172   |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                1 |   0.0484954 | 0.825702 | 3068 |
| event_binary_B | pretrend_baseline_joint_zero       |                1 |   0.291044  | 0.589552 | 3068 |
| event_binary_B | pretrend_displacement_joint_zero   |                1 |   0.502267  | 0.478506 | 3068 |
| event_score_C  | pretrend_score_baseline_joint_zero |                1 |   0.0432734 | 0.835211 | 3068 |
| event_score_C  | pretrend_score_slope_joint_zero    |                1 |   0.026734  | 0.870121 | 3068 |