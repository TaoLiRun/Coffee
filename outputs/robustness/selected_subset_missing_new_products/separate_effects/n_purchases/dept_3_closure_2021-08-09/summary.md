# Displacement Effect Estimation Summary

- Sample rows: 11,888
- Unique members: 1,486
- Unique closures: 1
- Event FE units: 1,486
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_3_closure_2021-08-09`
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Length-heterogeneity event-study spec skipped: true
- Model type: DDD


## Binary Specs
| spec             | term                  |     n |   r2_within |       coef |        se |      pvalue |
|:-----------------|:----------------------|------:|------------:|-----------:|----------:|------------:|
| binary_collapsed | post_X_treated        | 11888 |   0.0146172 |  0.019472  | 0.0028222 | 7.69718e-12 |
| binary_collapsed | post_X_disp           | 11888 |   0.0146172 | -0.0449962 | 0.0126034 | 0.00036812  |
| binary_collapsed | post_X_treated_X_disp | 11888 |   0.0146172 |  0.0373336 | 0.016723  | 0.0257323   |

## Score Spec
| spec            | term                   |     n |   r2_within |       coef |         se |      pvalue |
|:----------------|:-----------------------|------:|------------:|-----------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 11888 |   0.0175825 |  0.03148   | 0.00493387 | 2.35469e-10 |
| score_collapsed | post_X_score           | 11888 |   0.0175825 | -0.0750475 | 0.0172032  | 1.37503e-05 |
| score_collapsed | post_X_treated_X_score | 11888 |   0.0175825 |  0.0614797 | 0.0234318  | 0.00878537  |

## Event-study Specs
| spec           | term                                                              |        coef |         se |      pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|------------:|-----------:|------------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0307197  | 0.00600613 | 3.55144e-07 | 11888 |   0.0134406 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0197199  | 0.00504605 | 9.72577e-05 | 11888 |   0.0134406 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00716052 | 0.00458785 | 0.118794    | 11888 |   0.0134406 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0128701  | 0.00484656 | 0.00800352  | 11888 |   0.0134406 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0117469  | 0.00527288 | 0.0260442   | 11888 |   0.0134406 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0168143  | 0.0053964  | 0.00186941  | 11888 |   0.0134406 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00464008 | 0.00581308 | 0.424874    | 11888 |   0.0134406 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0227843  | 0.00472466 | 1.56388e-06 | 11888 |   0.035548  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00942451 | 0.00387201 | 0.0150497   | 11888 |   0.035548  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00204929 | 0.00320697 | 0.522915    | 11888 |   0.035548  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0147293  | 0.00395715 | 0.000204864 | 11888 |   0.035548  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0162894  | 0.0038993  | 3.11888e-05 | 11888 |   0.035548  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0201774  | 0.00426147 | 2.40121e-06 | 11888 |   0.035548  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00346769 | 0.0047259  | 0.46321     | 11888 |   0.035548  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             | -0.0250993  | 0.0285955  | 0.38023     | 11888 |   0.035548  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             | -0.0463427  | 0.0241985  | 0.0556705   | 11888 |   0.035548  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.0550916  | 0.0242275  | 0.0231122   | 11888 |   0.035548  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.00161987 | 0.0224108  | 0.942388    | 11888 |   0.035548  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.0109983  | 0.0271422  | 0.68538     | 11888 |   0.035548  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.00445218 | 0.0260636  | 0.864389    | 11888 |   0.035548  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.0277269  | 0.0263362  | 0.292601    | 11888 |   0.035548  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.0420907  | 0.0227994  | 0.0650714   | 11888 |   0.035548  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                | -0.0166605  | 0.0188046  | 0.375771    | 11888 |   0.035548  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0226497  | 0.0193412  | 0.241761    | 11888 |   0.035548  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0305191  | 0.0167949  | 0.069393    | 11888 |   0.035548  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0333742  | 0.021911   | 0.127929    | 11888 |   0.035548  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0593981  | 0.0207335  | 0.00423096  | 11888 |   0.035548  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0927948  | 0.0208634  | 9.32456e-06 | 11888 |   0.035548  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0298639  | 0.00868798 | 0.000603601 | 11888 |   0.0334762 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0210336  | 0.00740044 | 0.00454142  | 11888 |   0.0334762 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0103157  | 0.00724719 | 0.154829    | 11888 |   0.0334762 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0172418  | 0.00674878 | 0.0107236   | 11888 |   0.0334762 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0175814  | 0.00787348 | 0.0256979   | 11888 |   0.0334762 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0252081  | 0.00784619 | 0.00134274  | 11888 |   0.0334762 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00467521 | 0.00806942 | 0.562425    | 11888 |   0.0334762 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            | -0.0548242  | 0.0416425  | 0.188195    | 11888 |   0.0334762 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            | -0.0629483  | 0.0362733  | 0.0828791   | 11888 |   0.0334762 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.049719   | 0.0362347  | 0.170228    | 11888 |   0.0334762 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.0110179  | 0.0319817  | 0.730515    | 11888 |   0.0334762 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.0166475  | 0.0380777  | 0.662031    | 11888 |   0.0334762 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.031404   | 0.0380719  | 0.409583    | 11888 |   0.0334762 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.0193577  | 0.0380266  | 0.610788    | 11888 |   0.0334762 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.0402319  | 0.0320596  | 0.209709    | 11888 |   0.0334762 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered | -0.0149854  | 0.0271941  | 0.581681    | 11888 |   0.0334762 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0169418  | 0.0282895  | 0.549349    | 11888 |   0.0334762 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0536652  | 0.0232396  | 0.0210684   | 11888 |   0.0334762 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.070609   | 0.0297415  | 0.0177189   | 11888 |   0.0334762 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.0976923  | 0.0295911  | 0.000984835 | 11888 |   0.0334762 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.116499   | 0.0302817  | 0.000124549 | 11888 |   0.0334762 |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |      pvalue |     n |
|:---------------|:-----------------------------------|-----------------:|------------:|------------:|------:|
| event_att      | pretrend_att_joint_zero            |                3 |    29.1581  | 2.07452e-06 | 11888 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |    29.9154  | 1.43776e-06 | 11888 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |     6.32694 | 0.0967434   | 11888 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |    13.2229  | 0.0041786   | 11888 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |     3.02139 | 0.38834     | 11888 |