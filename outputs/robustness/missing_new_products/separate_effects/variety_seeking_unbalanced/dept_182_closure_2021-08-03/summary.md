# Displacement Effect Estimation Summary

- Sample rows: 12,616
- Unique members: 1,577
- Unique closures: 1
- Event FE units: 1,577
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_182_closure_2021-08-03`
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Length-heterogeneity event-study spec skipped: true
- Model type: DDD


## Binary Specs
| spec             | term                  |    n |   r2_within |       coef |        se |     pvalue |
|:-----------------|:----------------------|-----:|------------:|-----------:|----------:|-----------:|
| binary_collapsed | post_X_treated        | 3646 |  0.00355029 |  0.155076  | 0.0578311 | 0.00746178 |
| binary_collapsed | post_X_disp           | 3646 |  0.00355029 |  0.0357802 | 0.0323821 | 0.26948    |
| binary_collapsed | post_X_treated_X_disp | 3646 |  0.00355029 | -0.203349  | 0.0710416 | 0.00430135 |

## Score Spec
| spec            | term                   |    n |   r2_within |       coef |        se |    pvalue |
|:----------------|:-----------------------|-----:|------------:|-----------:|----------:|----------:|
| score_collapsed | post_X_treated         | 3646 |  0.00263714 |  0.107421  | 0.0480464 | 0.0256088 |
| score_collapsed | post_X_score           | 3646 |  0.00263714 |  0.0174583 | 0.0489088 | 0.721208  |
| score_collapsed | post_X_treated_X_score | 3646 |  0.00263714 | -0.274387  | 0.123479  | 0.02652   |

## Event-study Specs
| spec           | term                                                              |        coef |        se |    pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|------------:|----------:|----------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0621389  | 0.0749599 | 0.407344  | 3646 |  0.00429376 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.0741558  | 0.0719586 | 0.303034  | 3646 |  0.00429376 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0427949  | 0.0752865 | 0.569886  | 3646 |  0.00429376 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.101399   | 0.0744646 | 0.173627  | 3646 |  0.00429376 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0877003  | 0.077365  | 0.257266  | 3646 |  0.00429376 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0479918  | 0.0790465 | 0.543914  | 3646 |  0.00429376 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0345005  | 0.0789017 | 0.662028  | 3646 |  0.00429376 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0508414  | 0.117096  | 0.664258  | 3646 |  0.00902612 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.0703759  | 0.114101  | 0.537531  | 3646 |  0.00902612 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00384542 | 0.116686  | 0.973718  | 3646 |  0.00902612 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.200738   | 0.108032  | 0.0634734 | 3646 |  0.00902612 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.155399   | 0.119388  | 0.193371  | 3646 |  0.00902612 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.199757   | 0.118964  | 0.0934685 | 3646 |  0.00902612 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0926119  | 0.120362  | 0.441829  | 3646 |  0.00902612 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             | -0.0119156  | 0.151581  | 0.937361  | 3646 |  0.00902612 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0177156  | 0.144505  | 0.902455  | 3646 |  0.00902612 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.0750396  | 0.153398  | 0.62483   | 3646 |  0.00902612 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.197934   | 0.150553  | 0.18894   | 3646 |  0.00902612 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.121558   | 0.156133  | 0.436444  | 3646 |  0.00902612 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              | -0.313626   | 0.154643  | 0.0428458 | 3646 |  0.00902612 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.268503   | 0.153641  | 0.0808708 | 3646 |  0.00902612 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.0325686  | 0.0610329 | 0.593733  | 3646 |  0.00902612 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                | -0.0120478  | 0.0595072 | 0.839604  | 3646 |  0.00902612 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.014995   | 0.0634169 | 0.813136  | 3646 |  0.00902612 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0049416  | 0.0648434 | 0.93927   | 3646 |  0.00902612 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.0435533  | 0.067469  | 0.518747  | 3646 |  0.00902612 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.0267902  | 0.0683005 | 0.694972  | 3646 |  0.00902612 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.0443014  | 0.0627954 | 0.480687  | 3646 |  0.00902612 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00190667 | 0.103394  | 0.985291  | 3646 |  0.00796054 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.104561   | 0.101086  | 0.301234  | 3646 |  0.00796054 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0500466  | 0.108027  | 0.643275  | 3646 |  0.00796054 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.17702    | 0.0925637 | 0.0561386 | 3646 |  0.00796054 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.167639   | 0.10232   | 0.101689  | 3646 |  0.00796054 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.148897   | 0.103063  | 0.148884  | 3646 |  0.00796054 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0420329  | 0.100642  | 0.676304  | 3646 |  0.00796054 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            | -0.269913   | 0.23574   | 0.252528  | 3646 |  0.00796054 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            | -0.0933058  | 0.254024  | 0.713472  | 3646 |  0.00796054 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.00902698 | 0.270481  | 0.973384  | 3646 |  0.00796054 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.362158   | 0.263487  | 0.169632  | 3646 |  0.00796054 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.354517   | 0.272394  | 0.193424  | 3646 |  0.00796054 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             | -0.537795   | 0.268314  | 0.0453291 | 3646 |  0.00796054 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             | -0.323741   | 0.240342  | 0.178316  | 3646 |  0.00796054 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered |  0.111333   | 0.0948304 | 0.240693  | 3646 |  0.00796054 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.0339792  | 0.092587  | 0.713707  | 3646 |  0.00796054 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0164624  | 0.106417  | 0.877094  | 3646 |  0.00796054 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  |  0.0159377  | 0.0967037 | 0.869131  | 3646 |  0.00796054 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  |  0.0874134  | 0.0978098 | 0.371715  | 3646 |  0.00796054 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  |  0.0861402  | 0.104569  | 0.41029   | 3646 |  0.00796054 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  |  0.0853703  | 0.0950322 | 0.369248  | 3646 |  0.00796054 |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                3 |    5.23761  | 0.155202 | 3646 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |    1.67263  | 0.643036 | 3646 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |    0.503056 | 0.918219 | 3646 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |    2.9735   | 0.395729 | 3646 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |    1.78872  | 0.617392 | 3646 |