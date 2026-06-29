# Displacement Effect Estimation Summary

- Sample rows: 4,320
- Unique members: 540
- Unique closures: 1
- Event FE units: 540
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_246_closure_2021-07-27`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |        coef |         se |      pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 4320 |   0.0439205 | -0.00375586 | 0.00475898 | 0.430334    |
| binary_collapsed | post_X_disp           | 4320 |   0.0439205 | -0.0410404  | 0.00792714 | 3.18513e-07 |
| binary_collapsed | post_X_treated_X_disp | 4320 |   0.0439205 | -0.119605   | 0.0861973  | 0.165842    |

## Score Spec
| spec            | term                   |    n |   r2_within |       coef |        se |      pvalue |
|:----------------|:-----------------------|-----:|------------:|-----------:|----------:|------------:|
| score_collapsed | post_X_treated         | 4320 |   0.0588454 | -0.0543096 | 0.0299188 | 0.0700437   |
| score_collapsed | post_X_score           | 4320 |   0.0588454 | -0.0578577 | 0.0105328 | 6.09646e-08 |
| score_collapsed | post_X_treated_X_score | 4320 |   0.0588454 | -0.212575  | 0.125062  | 0.0897527   |

## Event-study Specs
| spec           | term                                                              |         coef |         se |     pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|-----------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00906534  | 0.0093058  | 0.330414   | 4320 |  0.00265403 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.0107858   | 0.0111369  | 0.333242   | 4320 |  0.00265403 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0011249   | 0.00792974 | 0.887245   | 4320 |  0.00265403 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.0144582   | 0.00732493 | 0.0489102  | 4320 |  0.00265403 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0112159   | 0.0146188  | 0.443284   | 4320 |  0.00265403 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0102564   | 0.0157159  | 0.514284   | 4320 |  0.00265403 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0199504   | 0.0149834  | 0.183589   | 4320 |  0.00265403 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0118279   | 0.00775159 | 0.127629   | 4320 |  0.0595853  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.00288173  | 0.00976834 | 0.768102   | 4320 |  0.0595853  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00422654  | 0.0057562  | 0.46311    | 4320 |  0.0595853  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00867722  | 0.00523651 | 0.0980889  | 4320 |  0.0595853  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00178027  | 0.00626756 | 0.776485   | 4320 |  0.0595853  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  1.92116e-05 | 0.0073867  | 0.997926   | 4320 |  0.0595853  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0093048   | 0.00612941 | 0.129586   | 4320 |  0.0595853  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0461006   | 0.0451206  | 0.307372   | 4320 |  0.0595853  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0967205   | 0.0375155  | 0.0101974  | 4320 |  0.0595853  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.00168783  | 0.0444306  | 0.969711   | 4320 |  0.0595853  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0551292   | 0.0411663  | 0.181075   | 4320 |  0.0595853  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.0995991   | 0.105303   | 0.344657   | 4320 |  0.0595853  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              | -0.0925131   | 0.114603   | 0.419881   | 4320 |  0.0595853  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.0900436   | 0.112562   | 0.424096   | 4320 |  0.0595853  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.0284915   | 0.0150214  | 0.0583979  | 4320 |  0.0595853  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.0380891   | 0.0150062  | 0.0114221  | 4320 |  0.0595853  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0529699   | 0.0133223  | 7.9628e-05 | 4320 |  0.0595853  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0085849   | 0.0116601  | 0.461889   | 4320 |  0.0595853  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0258865   | 0.0115806  | 0.0258038  | 4320 |  0.0595853  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.00849702  | 0.0122296  | 0.487485   | 4320 |  0.0595853  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.00164249  | 0.0121135  | 0.892194   | 4320 |  0.0595853  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00068248  | 0.0162556  | 0.966527   | 4320 |  0.073874   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.0381264   | 0.0170891  | 0.0260892  | 4320 |  0.073874   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00903961  | 0.0153309  | 0.555685   | 4320 |  0.073874   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.032619    | 0.0149603  | 0.0296622  | 4320 |  0.073874   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0448136   | 0.039175   | 0.253159   | 4320 |  0.073874   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0423698   | 0.0414163  | 0.306755   | 4320 |  0.073874   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0495876   | 0.0420439  | 0.23875    | 4320 |  0.073874   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.0442361   | 0.0555085  | 0.425845   | 4320 |  0.073874   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.138901    | 0.0582086  | 0.0173645  | 4320 |  0.073874   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.0270759   | 0.0574203  | 0.637447   | 4320 |  0.073874   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.100029    | 0.0608518  | 0.100799   | 4320 |  0.073874   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.181656    | 0.165605   | 0.273165   | 4320 |  0.073874   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             | -0.182561    | 0.173164   | 0.292232   | 4320 |  0.073874   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             | -0.175841    | 0.17695    | 0.320799   | 4320 |  0.073874   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered |  0.0269542   | 0.0210528  | 0.200987   | 4320 |  0.073874   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.0494335   | 0.0206504  | 0.0170146  | 4320 |  0.073874   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0617268   | 0.0193326  | 0.0014908  | 4320 |  0.073874   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0191322   | 0.0167403  | 0.253596   | 4320 |  0.073874   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0413938   | 0.0158137  | 0.00910399 | 4320 |  0.073874   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.0238048   | 0.0175327  | 0.175115   | 4320 |  0.073874   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.00898541  | 0.0170357  | 0.598102   | 4320 |  0.073874   |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |    pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|----------:|-----:|
| event_att      | pretrend_att_joint_zero            |                3 |     5.52309 | 0.137264  | 4320 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |     6.4844  | 0.0902798 | 4320 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |    10.9329  | 0.0120943 | 4320 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |     8.4714  | 0.0372107 | 4320 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |     7.79622 | 0.0504165 | 4320 |