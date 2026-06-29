# Displacement Effect Estimation Summary

- Sample rows: 24,760
- Unique members: 3,095
- Unique closures: 1
- Event FE units: 3,095
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_124_closure_2021-07-22`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |     n |   r2_within |         coef |         se |      pvalue |
|:-----------------|:----------------------|------:|------------:|-------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 24760 |  0.00775133 |  0.000600484 | 0.00176246 | 0.733347    |
| binary_collapsed | post_X_disp           | 24760 |  0.00775133 | -0.0223871   | 0.00336573 | 3.41758e-11 |
| binary_collapsed | post_X_treated_X_disp | 24760 |  0.00775133 |  0.00405235  | 0.0051394  | 0.430472    |

## Score Spec
| spec            | term                   |     n |   r2_within |        coef |         se |     pvalue |
|:----------------|:-----------------------|------:|------------:|------------:|-----------:|-----------:|
| score_collapsed | post_X_treated         | 24760 |   0.0110404 |  0.00177394 | 0.00165334 | 0.28338    |
| score_collapsed | post_X_score           | 24760 |   0.0110404 | -0.0372085  | 0.0051972  | 1.0083e-12 |
| score_collapsed | post_X_treated_X_score | 24760 |   0.0110404 |  0.00593025 | 0.00813205 | 0.465907   |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00158471  | 0.00338625 | 0.63983     | 24760 | 0.000356791 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.00165846  | 0.00321138 | 0.605589    | 24760 | 0.000356791 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.000766423 | 0.00279883 | 0.784228    | 24760 | 0.000356791 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00150613  | 0.00305906 | 0.622506    | 24760 | 0.000356791 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00216722  | 0.00300843 | 0.471343    | 24760 | 0.000356791 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00609232  | 0.00332732 | 0.0671964   | 24760 | 0.000356791 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00213037  | 0.0035398  | 0.547328    | 24760 | 0.000356791 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.000828253 | 0.00259074 | 0.749219    | 24760 | 0.0113223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.00267526  | 0.00238049 | 0.261173    | 24760 | 0.0113223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00115127  | 0.00187215 | 0.538636    | 24760 | 0.0113223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.000977339 | 0.00239541 | 0.683298    | 24760 | 0.0113223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.000579777 | 0.00213627 | 0.786103    | 24760 | 0.0113223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00221972  | 0.00221784 | 0.316979    | 24760 | 0.0113223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.000480387 | 0.00253139 | 0.8495      | 24760 | 0.0113223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.00694694  | 0.00719315 | 0.334234    | 24760 | 0.0113223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             | -0.001181    | 0.00683528 | 0.862836    | 24760 | 0.0113223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.000309143 | 0.00594554 | 0.958535    | 24760 | 0.0113223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.00358523  | 0.00644233 | 0.577902    | 24760 | 0.0113223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  5.15086e-05 | 0.00631194 | 0.993489    | 24760 | 0.0113223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.0111871   | 0.00702206 | 0.11123     | 24760 | 0.0113223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.00684231  | 0.00742873 | 0.357091    | 24760 | 0.0113223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.0167645   | 0.0051989  | 0.00127452  | 24760 | 0.0113223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                | -0.00752947  | 0.00481324 | 0.117844    | 24760 | 0.0113223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.00916869  | 0.00404767 | 0.0235707   | 24760 | 0.0113223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0209123   | 0.00439599 | 2.0536e-06  | 24760 | 0.0113223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0275937   | 0.00434411 | 2.43725e-10 | 24760 | 0.0113223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0272221   | 0.0047234  | 9.06237e-09 | 24760 | 0.0113223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0289456   | 0.00487708 | 3.26339e-09 | 24760 | 0.0113223   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.000230564 | 0.0023523  | 0.921926    | 24760 | 0.0167026   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.00104798  | 0.00216746 | 0.628772    | 24760 | 0.0167026   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00133302  | 0.00181708 | 0.463242    | 24760 | 0.0167026   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00145889  | 0.00213532 | 0.49452     | 24760 | 0.0167026   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.000485238 | 0.00204026 | 0.812028    | 24760 | 0.0167026   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00426529  | 0.00218456 | 0.050973    | 24760 | 0.0167026   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00134121  | 0.00241036 | 0.577953    | 24760 | 0.0167026   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.0199007   | 0.0110466  | 0.0717172   | 24760 | 0.0167026   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.00918288  | 0.0104101  | 0.377783    | 24760 | 0.0167026   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.00183527  | 0.00913456 | 0.840778    | 24760 | 0.0167026   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.00975069  | 0.0102494  | 0.341507    | 24760 | 0.0167026   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.00231795  | 0.010047   | 0.817556    | 24760 | 0.0167026   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.0238958   | 0.0111726  | 0.0325313   | 24760 | 0.0167026   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.0186754   | 0.0116043  | 0.107641    | 24760 | 0.0167026   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.0386299   | 0.00790029 | 1.06149e-06 | 24760 | 0.0167026   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered | -0.023418    | 0.0074246  | 0.00162535  | 24760 | 0.0167026   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.00626647  | 0.00612397 | 0.30626     | 24760 | 0.0167026   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0396636   | 0.00702363 | 1.77886e-08 | 24760 | 0.0167026   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0511193   | 0.00691397 | 1.82965e-13 | 24760 | 0.0167026   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.0550679   | 0.00750572 | 2.78222e-13 | 24760 | 0.0167026   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.0587645   | 0.00757114 | 1.13243e-14 | 24760 | 0.0167026   |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |     n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|------:|
| event_att      | pretrend_att_joint_zero            |                3 |    0.848634 | 0.837802 | 24760 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |    3.99607  | 0.261889 | 24760 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |    2.21424  | 0.529149 | 24760 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |    1.72201  | 0.632052 | 24760 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |    4.00321  | 0.261117 | 24760 |