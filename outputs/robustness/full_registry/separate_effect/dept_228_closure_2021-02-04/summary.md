# Displacement Effect Estimation Summary

- Sample rows: 7,088
- Unique members: 886
- Unique closures: 1
- Event FE units: 886
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_228_closure_2021-02-04`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |        coef |         se |      pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 7088 |   0.0146553 | -0.00462081 | 0.00400217 | 0.248576    |
| binary_collapsed | post_X_disp           | 7088 |   0.0146553 | -0.0352211  | 0.00681282 | 2.89775e-07 |
| binary_collapsed | post_X_treated_X_disp | 7088 |   0.0146553 |  0.0090101  | 0.019562   | 0.645204    |

## Score Spec
| spec            | term                   |    n |   r2_within |        coef |         se |      pvalue |
|:----------------|:-----------------------|-----:|------------:|------------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 7088 |    0.023026 | -0.00505391 | 0.00657026 | 0.441973    |
| score_collapsed | post_X_score           | 7088 |    0.023026 | -0.0622842  | 0.00985232 | 4.09533e-10 |
| score_collapsed | post_X_treated_X_score | 7088 |    0.023026 |  0.0159781  | 0.03609    | 0.658069    |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.0204375   | 0.00857823 | 0.0174063   | 7088 |  0.00130069 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.0207581   | 0.00765787 | 0.00684428  | 7088 |  0.00130069 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0226716   | 0.0066644  | 0.000699187 | 7088 |  0.00130069 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0139561   | 0.00711486 | 0.0501283   | 7088 |  0.00130069 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0148106   | 0.00802006 | 0.0651242   | 7088 |  0.00130069 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0207442   | 0.00722846 | 0.00420513  | 7088 |  0.00130069 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0212933   | 0.00899622 | 0.0181514   | 7088 |  0.00130069 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.0172543   | 0.00717221 | 0.0163451   | 7088 |  0.0265405  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.0148827   | 0.00674082 | 0.0275108   | 7088 |  0.0265405  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00971826  | 0.00452299 | 0.0319339   | 7088 |  0.0265405  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.000584847 | 0.00548141 | 0.915054    | 7088 |  0.0265405  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00664072  | 0.00681862 | 0.330367    | 7088 |  0.0265405  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00743168  | 0.00506009 | 0.142273    | 7088 |  0.0265405  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00988443  | 0.00655844 | 0.132133    | 7088 |  0.0265405  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             | -0.00495016  | 0.0260459  | 0.84931     | 7088 |  0.0265405  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.00673869  | 0.022548   | 0.765118    | 7088 |  0.0265405  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0442312   | 0.0226532  | 0.0511895   | 7088 |  0.0265405  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.0378093   | 0.0229993  | 0.100545    | 7088 |  0.0265405  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.00848681  | 0.0232554  | 0.715243    | 7088 |  0.0265405  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.0171468   | 0.0215033  | 0.425431    | 7088 |  0.0265405  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.0186172   | 0.0295925  | 0.529435    | 7088 |  0.0265405  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.0364466   | 0.0104903  | 0.000537016 | 7088 |  0.0265405  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                | -0.0357251   | 0.00965597 | 0.000229086 | 7088 |  0.0265405  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                | -0.0203921   | 0.00842526 | 0.0157062   | 7088 |  0.0265405  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0464245   | 0.00956166 | 1.42096e-06 | 7088 |  0.0265405  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0514321   | 0.0109092  | 2.81301e-06 | 7088 |  0.0265405  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0772136   | 0.0102259  | 1.07692e-13 | 7088 |  0.0265405  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0583781   | 0.0106628  | 5.70299e-08 | 7088 |  0.0265405  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.0127662   | 0.00904661 | 0.158548    | 7088 |  0.0386986  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.0143042   | 0.00802856 | 0.0751459   | 7088 |  0.0386986  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0208607   | 0.00730576 | 0.00439915  | 7088 |  0.0386986  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00665173  | 0.00771643 | 0.38891     | 7088 |  0.0386986  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00455758  | 0.00831972 | 0.583964    | 7088 |  0.0386986  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00605385  | 0.00684178 | 0.376485    | 7088 |  0.0386986  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0104524   | 0.00993204 | 0.292909    | 7088 |  0.0386986  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.0102269   | 0.0399331  | 0.797932    | 7088 |  0.0386986  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.0285213   | 0.0363895  | 0.43338     | 7088 |  0.0386986  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.0799452   | 0.0341534  | 0.0194655   | 7088 |  0.0386986  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.0743244   | 0.0354871  | 0.0365076   | 7088 |  0.0386986  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.0314273   | 0.0387034  | 0.417008    | 7088 |  0.0386986  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.0315269   | 0.0331289  | 0.341538    | 7088 |  0.0386986  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.0453274   | 0.0526292  | 0.389329    | 7088 |  0.0386986  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.0676708   | 0.0150664  | 8.00852e-06 | 7088 |  0.0386986  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered | -0.0638414   | 0.0142208  | 8.08996e-06 | 7088 |  0.0386986  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered | -0.0428715   | 0.0123266  | 0.000529858 | 7088 |  0.0386986  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0868405   | 0.0136519  | 3.20904e-10 | 7088 |  0.0386986  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0966062   | 0.0165285  | 7.12604e-09 | 7088 |  0.0386986  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.133732    | 0.0152641  | 0           | 7088 |  0.0386986  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.106342    | 0.0156932  | 2.24798e-11 | 7088 |  0.0386986  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |     pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|-----------:|-----:|
| event_att      | pretrend_att_joint_zero            |                3 |    14.3691  | 0.00244343 | 7088 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |     9.7142  | 0.0211585  | 7088 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |     5.00009 | 0.17179    | 7088 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |     8.68249 | 0.0338242  | 7088 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |     5.87685 | 0.117758   | 7088 |