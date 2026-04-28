# Displacement Effect Estimation Summary

- Sample rows: 27,072
- Unique members: 3,384
- Unique closures: 1
- Event FE units: 3,384
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_47_closure_2021-07-30`
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Length-heterogeneity event-study spec skipped: true
- Model type: DDD


## Binary Specs
| spec             | term                  |    n |   r2_within |       coef |        se |      pvalue |
|:-----------------|:----------------------|-----:|------------:|-----------:|----------:|------------:|
| binary_collapsed | post_X_treated        | 7031 |  0.00249981 |  0.0558594 | 0.0708277 | 0.430417    |
| binary_collapsed | post_X_disp           | 7031 |  0.00249981 |  0.0750685 | 0.0221367 | 0.000711913 |
| binary_collapsed | post_X_treated_X_disp | 7031 |  0.00249981 | -0.0473377 | 0.096657  | 0.624374    |

## Score Spec
| spec            | term                   |    n |   r2_within |       coef |        se |     pvalue |
|:----------------|:-----------------------|-----:|------------:|-----------:|----------:|-----------:|
| score_collapsed | post_X_treated         | 7031 |  0.00200612 |  0.0718379 | 0.0652766 | 0.271263   |
| score_collapsed | post_X_score           | 7031 |  0.00200612 |  0.106364  | 0.0342178 | 0.00191183 |
| score_collapsed | post_X_treated_X_score | 7031 |  0.00200612 | -0.1614    | 0.1802    | 0.370553   |

## Event-study Specs
| spec           | term                                                              |         coef |        se |      pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00125249  | 0.0868879 | 0.988501    | 7031 | 0.000723253 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0432817   | 0.075855  | 0.568356    | 7031 | 0.000723253 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0271582   | 0.0832126 | 0.744183    | 7031 | 0.000723253 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.000324557 | 0.0877846 | 0.997051    | 7031 | 0.000723253 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0589702   | 0.0876967 | 0.501399    | 7031 | 0.000723253 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0348271   | 0.0886188 | 0.69437     | 7031 | 0.000723253 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0782933   | 0.0898918 | 0.383892    | 7031 | 0.000723253 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.109199    | 0.147859  | 0.460291    | 7031 | 0.00811097  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.017499    | 0.115163  | 0.879245    | 7031 | 0.00811097  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.236219    | 0.171637  | 0.168919    | 7031 | 0.00811097  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0525587   | 0.18354   | 0.774637    | 7031 | 0.00811097  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00227009  | 0.153704  | 0.988218    | 7031 | 0.00811097  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0228721   | 0.138513  | 0.868865    | 7031 | 0.00811097  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.15592     | 0.147548  | 0.290781    | 7031 | 0.00811097  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.211252    | 0.17599   | 0.230166    | 7031 | 0.00811097  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             | -0.0275908   | 0.149321  | 0.853427    | 7031 | 0.00811097  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.314672    | 0.191571  | 0.100653    | 7031 | 0.00811097  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0317209   | 0.208336  | 0.879001    | 7031 | 0.00811097  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.11124     | 0.18108   | 0.539091    | 7031 | 0.00811097  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.104046    | 0.179802  | 0.562887    | 7031 | 0.00811097  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.136299    | 0.183317  | 0.457272    | 7031 | 0.00811097  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.106941    | 0.0416926 | 0.0104028   | 7031 | 0.00811097  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.095723    | 0.0407267 | 0.0188678   | 7031 | 0.00811097  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0917338   | 0.0417445 | 0.028118    | 7031 | 0.00811097  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  0.0956954   | 0.0423394 | 0.0239346   | 7031 | 0.00811097  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.126684    | 0.0409791 | 0.00202413  | 7031 | 0.00811097  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.177752    | 0.0427339 | 3.34763e-05 | 7031 | 0.00811097  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.197469    | 0.0447839 | 1.10133e-05 | 7031 | 0.00811097  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.161932    | 0.122147  | 0.185113    | 7031 | 0.00811181  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0536319   | 0.103663  | 0.604968    | 7031 | 0.00811181  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.225153    | 0.144575  | 0.119574    | 7031 | 0.00811181  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0108996   | 0.169938  | 0.948867    | 7031 | 0.00811181  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00968191  | 0.11876   | 0.935034    | 7031 | 0.00811181  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0257837   | 0.117753  | 0.826705    | 7031 | 0.00811181  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.154307    | 0.122088  | 0.206439    | 7031 | 0.00811181  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.582083    | 0.27167   | 0.0322852   | 7031 | 0.00811181  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            | -0.00641888  | 0.266862  | 0.980813    | 7031 | 0.00811181  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.572647    | 0.293422  | 0.0511473   | 7031 | 0.00811181  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.0358818   | 0.384967  | 0.92575     | 7031 | 0.00811181  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.14357     | 0.262625  | 0.584676    | 7031 | 0.00811181  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.160679    | 0.302705  | 0.595619    | 7031 | 0.00811181  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.232507    | 0.288909  | 0.42106     | 7031 | 0.00811181  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered |  0.140781    | 0.0639398 | 0.0278145   | 7031 | 0.00811181  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.157544    | 0.061804  | 0.0108871   | 7031 | 0.00811181  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.144094    | 0.0632971 | 0.0229414   | 7031 | 0.00811181  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  |  0.141609    | 0.0614643 | 0.0213461   | 7031 | 0.00811181  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  |  0.160341    | 0.0602389 | 0.00784643  | 7031 | 0.00811181  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  |  0.269439    | 0.0637803 | 2.52115e-05 | 7031 | 0.00811181  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  |  0.293577    | 0.0657089 | 8.42044e-06 | 7031 | 0.00811181  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |    pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|----------:|-----:|
| event_att      | pretrend_att_joint_zero            |                3 |    0.508452 | 0.917031  | 7031 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |    2.30152  | 0.512229  | 7031 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |    4.57642  | 0.205574  | 7031 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |    3.17492  | 0.365434  | 7031 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |    8.69997  | 0.0335578 | 7031 |