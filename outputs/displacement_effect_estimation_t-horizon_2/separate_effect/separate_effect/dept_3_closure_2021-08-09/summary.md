# Displacement Effect Estimation Summary

- Sample rows: 5,944
- Unique members: 1,486
- Unique closures: 1
- Event FE units: 1,486
- Relative periods: [-2, -1, 1, 2]
- Estimation mode: separate_effect=true
- Closure event: `dept_3_closure_2021-08-09`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |       coef |         se |      pvalue |
|:-----------------|:----------------------|-----:|------------:|-----------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 5944 |   0.0155172 |  0.0144847 | 0.00319343 | 6.20058e-06 |
| binary_collapsed | post_X_disp           | 5944 |   0.0155172 | -0.0432715 | 0.0150247  | 0.00403342  |
| binary_collapsed | post_X_treated_X_disp | 5944 |   0.0155172 |  0.0228566 | 0.0199382  | 0.251827    |

## Score Spec
| spec            | term                   |    n |   r2_within |       coef |        se |      pvalue |
|:----------------|:-----------------------|-----:|------------:|-----------:|----------:|------------:|
| score_collapsed | post_X_treated         | 5944 |   0.0188768 |  0.0228147 | 0.0059931 | 0.000146485 |
| score_collapsed | post_X_score           | 5944 |   0.0188768 | -0.070608  | 0.0201392 | 0.00046842  |
| score_collapsed | post_X_treated_X_score | 5944 |   0.0188768 |  0.0386922 | 0.0279346 | 0.166229    |

## Event-study Specs
| spec           | term                                                              |        coef |         se |      pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|------------:|-----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00716052 | 0.00458746 | 0.118763    | 5944 |  0.00528533 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0128701  | 0.00484616 | 0.00799824  | 5944 |  0.00528533 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0117469  | 0.00527244 | 0.0260317   | 5944 |  0.00528533 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00204929 | 0.00320643 | 0.522845    | 5944 |  0.0207825  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0147293  | 0.00395649 | 0.00020436  | 5944 |  0.0207825  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0162894  | 0.00389865 | 3.10936e-05 | 5944 |  0.0207825  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.0550916  | 0.0242234  | 0.0230891   | 5944 |  0.0207825  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.00161987 | 0.022407   | 0.942379    | 5944 |  0.0207825  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.0109983  | 0.0271376  | 0.68533     | 5944 |  0.0207825  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0226497  | 0.0193379  | 0.241682    | 5944 |  0.0207825  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0305191  | 0.0167921  | 0.0693461   | 5944 |  0.0207825  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0333742  | 0.0219073  | 0.127864    | 5944 |  0.0207825  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0106308  | 0.00745963 | 0.154334    | 5944 |  0.0215579  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0173117  | 0.00691937 | 0.0124592   | 5944 |  0.0215579  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.017687   | 0.00808761 | 0.0289038   | 5944 |  0.0215579  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.049719   | 0.0362286  | 0.170156    | 5944 |  0.0215579  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.0110179  | 0.0319763  | 0.730471    | 5944 |  0.0215579  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.0166475  | 0.0380713  | 0.661978    | 5944 |  0.0215579  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0169418  | 0.0282848  | 0.549282    | 5944 |  0.0215579  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0536652  | 0.0232357  | 0.0210468   | 5944 |  0.0215579  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.070609   | 0.0297365  | 0.0176998   | 5944 |  0.0215579  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                1 |    2.43637  | 0.11855  | 5944 |
| event_binary_B | pretrend_baseline_joint_zero       |                1 |    0.408472 | 0.522746 | 5944 |
| event_binary_B | pretrend_displacement_joint_zero   |                1 |    5.17251  | 0.022947 | 5944 |
| event_score_C  | pretrend_score_baseline_joint_zero |                1 |    2.03095  | 0.154124 | 5944 |
| event_score_C  | pretrend_score_slope_joint_zero    |                1 |    1.8834   | 0.169949 | 5944 |