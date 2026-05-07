# Displacement Effect Estimation Summary

- Sample rows: 25,488
- Unique members: 3,186
- Unique closures: 1
- Event FE units: 3,186
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_59_closure_2021-08-03`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |     n |   r2_within |         coef |         se |   pvalue |
|:-----------------|:----------------------|------:|------------:|-------------:|-----------:|---------:|
| binary_collapsed | post_X_treated        | 25488 |   0.0131757 | -0.000248547 | 0.00230477 | 0.914129 |
| binary_collapsed | post_X_disp           | 25488 |   0.0131757 | -0.0311891   | 0.00357036 | 0        |
| binary_collapsed | post_X_treated_X_disp | 25488 |   0.0131757 | -0.0083133   | 0.010131   | 0.411946 |

## Score Spec
| spec            | term                   |     n |   r2_within |        coef |         se |   pvalue |
|:----------------|:-----------------------|------:|------------:|------------:|-----------:|---------:|
| score_collapsed | post_X_treated         | 25488 |   0.0187929 | -0.00341171 | 0.00329454 | 0.300483 |
| score_collapsed | post_X_score           | 25488 |   0.0187929 | -0.0524053  | 0.00516159 | 0        |
| score_collapsed | post_X_treated_X_score | 25488 |   0.0187929 | -0.0137435  | 0.0158019  | 0.38451  |

## Event-study Specs
| spec           | term                                                              |        coef |         se |      pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|------------:|-----------:|------------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00740326 | 0.00513968 | 0.149849    | 25488 | 0.000604506 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.00609152 | 0.00448967 | 0.174945    | 25488 | 0.000604506 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00163419 | 0.0043046  | 0.70424     | 25488 | 0.000604506 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.001929   | 0.00379317 | 0.611106    | 25488 | 0.000604506 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00325102 | 0.00421513 | 0.440602    | 25488 | 0.000604506 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00966395 | 0.00418338 | 0.0209473   | 25488 | 0.000604506 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00780035 | 0.00437684 | 0.0748141   | 25488 | 0.000604506 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00274252 | 0.00414511 | 0.508258    | 25488 | 0.0226251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.00239609 | 0.00383949 | 0.532631    | 25488 | 0.0226251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00397879 | 0.00284416 | 0.16193     | 25488 | 0.0226251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00261706 | 0.00325528 | 0.42149     | 25488 | 0.0226251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00397804 | 0.00381898 | 0.297653    | 25488 | 0.0226251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00561007 | 0.00391791 | 0.152269    | 25488 | 0.0226251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00387412 | 0.00365772 | 0.289606    | 25488 | 0.0226251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0232814  | 0.0156102  | 0.13595     | 25488 | 0.0226251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0201692  | 0.0130151  | 0.121319    | 25488 | 0.0226251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.00644673 | 0.0137805  | 0.639949    | 25488 | 0.0226251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0191024  | 0.0111153  | 0.0857893   | 25488 | 0.0226251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.00171945 | 0.012179   | 0.887735    | 25488 | 0.0226251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.00976661 | 0.011773   | 0.406841    | 25488 | 0.0226251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.0113669  | 0.0132619  | 0.391449    | 25488 | 0.0226251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.0173875  | 0.00520486 | 0.000845508 | 25488 | 0.0226251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.0192984  | 0.00487892 | 7.80478e-05 | 25488 | 0.0226251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0486722  | 0.00440282 | 0           | 25488 | 0.0226251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.00533315 | 0.00429588 | 0.214528    | 25488 | 0.0226251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.00345276 | 0.00471397 | 0.463945    | 25488 | 0.0226251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0186757  | 0.00445281 | 2.81388e-05 | 25488 | 0.0226251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0119365  | 0.00495028 | 0.0159526   | 25488 | 0.0226251   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00993596 | 0.00531629 | 0.0617194   | 25488 | 0.0285769   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.00867284 | 0.00456156 | 0.0573546   | 25488 | 0.0285769   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00234185 | 0.0044984  | 0.602684    | 25488 | 0.0285769   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00331953 | 0.00393265 | 0.398679    | 25488 | 0.0285769   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00398957 | 0.00436852 | 0.361178    | 25488 | 0.0285769   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00771358 | 0.00429026 | 0.0722834   | 25488 | 0.0285769   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00689931 | 0.00456982 | 0.131205    | 25488 | 0.0285769   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.0446771  | 0.0239724  | 0.0624574   | 25488 | 0.0285769   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.042946   | 0.0199366  | 0.0313044   | 25488 | 0.0285769   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.00602405 | 0.0220976  | 0.78517     | 25488 | 0.0285769   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.0200522  | 0.0179284  | 0.263455    | 25488 | 0.0285769   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.00491252 | 0.0182845  | 0.7882      | 25488 | 0.0285769   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.0164286  | 0.0182891  | 0.369109    | 25488 | 0.0285769   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.0253362  | 0.0201903  | 0.209619    | 25488 | 0.0285769   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered |  0.0247457  | 0.00756368 | 0.00108061  | 25488 | 0.0285769   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.0261872  | 0.00712272 | 0.000240288 | 25488 | 0.0285769   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0672836  | 0.00658951 | 0           | 25488 | 0.0285769   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0152576  | 0.00650631 | 0.0190857   | 25488 | 0.0285769   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0139143  | 0.00696803 | 0.0459232   | 25488 | 0.0285769   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.0380352  | 0.00677452 | 2.1411e-08  | 25488 | 0.0285769   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.0241974  | 0.00750572 | 0.00127754  | 25488 | 0.0285769   |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |    pvalue |     n |
|:---------------|:-----------------------------------|-----------------:|------------:|----------:|------:|
| event_att      | pretrend_att_joint_zero            |                3 |     4.53171 | 0.209479  | 25488 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |     2.00913 | 0.570514  | 25488 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |     5.88156 | 0.117517  | 25488 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |     5.34648 | 0.148115  | 25488 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |     9.66386 | 0.0216506 | 25488 |