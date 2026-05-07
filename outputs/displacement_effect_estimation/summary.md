# Displacement Effect Estimation Summary

- Sample rows: 321,184
- Unique members: 40,148
- Unique closures: 18
- Event FE units: 40,148
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=false
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Model type: DDD


## Binary Specs
| spec             | term                  |      n |   r2_within |         coef |          se |    pvalue |
|:-----------------|:----------------------|-------:|------------:|-------------:|------------:|----------:|
| binary_collapsed | post_X_treated        | 321184 |   0.0130244 |  0.000891858 | 0.000665864 | 0.180448  |
| binary_collapsed | post_X_disp           | 321184 |   0.0130244 | -0.0343661   | 0.00114263  | 0         |
| binary_collapsed | post_X_treated_X_disp | 321184 |   0.0130244 |  0.00582887  | 0.00251942  | 0.0206961 |

## Score Spec
| spec            | term                   |      n |   r2_within |        coef |          se |     pvalue |
|:----------------|:-----------------------|-------:|------------:|------------:|------------:|-----------:|
| score_collapsed | post_X_treated         | 321184 |   0.0182391 |  0.00227767 | 0.000811223 | 0.00499203 |
| score_collapsed | post_X_score           | 321184 |   0.0182391 | -0.056816   | 0.00168632  | 0          |
| score_collapsed | post_X_treated_X_score | 321184 |   0.0182391 |  0.00758612 | 0.00369529  | 0.040087   |

## Event-study Specs
| spec           | term                                                              |         coef |          se |      pvalue |      n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|------------:|------------:|-------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.000217695 | 0.00126337  | 0.863192    | 321184 | 0.000180302 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -6.3972e-05  | 0.00120637  | 0.957709    | 321184 | 0.000180302 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.000637519 | 0.00106308  | 0.548715    | 321184 | 0.000180302 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0026216   | 0.00106969  | 0.0142579   | 321184 | 0.000180302 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.000205661 | 0.00114845  | 0.857879    | 321184 | 0.000180302 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00656805  | 0.00121716  | 6.84408e-08 | 321184 | 0.000180302 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00179919  | 0.00119879  | 0.133405    | 321184 | 0.000180302 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00130498  | 0.00105227  | 0.214924    | 321184 | 0.0158694   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.000183354 | 0.001004    | 0.855095    | 321184 | 0.0158694   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0016303   | 0.000847375 | 0.054369    | 321184 | 0.0158694   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.000501284 | 0.000855345 | 0.557838    | 321184 | 0.0158694   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.000447551 | 0.000941185 | 0.63442     | 321184 | 0.0158694   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00316421  | 0.000989491 | 0.00138582  | 321184 | 0.0158694   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00012099  | 0.000961387 | 0.899852    | 321184 | 0.0158694   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.00500733  | 0.00381344  | 0.189165    | 321184 | 0.0158694   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             | -0.00178669  | 0.00362437  | 0.62204     | 321184 | 0.0158694   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.00777542  | 0.00322894  | 0.0160427   | 321184 | 0.0158694   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.00646497  | 0.0032523   | 0.0468386   | 321184 | 0.0158694   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.00223429  | 0.00345928  | 0.518359    | 321184 | 0.0158694   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.0108627   | 0.00368337  | 0.00318856  | 321184 | 0.0158694   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.00391458  | 0.00363834  | 0.281968    | 321184 | 0.0158694   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.00529345  | 0.00181497  | 0.00354126  | 321184 | 0.0158694   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.0044973   | 0.00172871  | 0.00928401  | 321184 | 0.0158694   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0231833   | 0.00155897  | 0           | 321184 | 0.0158694   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0260961   | 0.00152986  | 0           | 321184 | 0.0158694   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0242329   | 0.00165348  | 0           | 321184 | 0.0158694   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0323743   | 0.00164105  | 0           | 321184 | 0.0158694   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0324197   | 0.00171654  | 0           | 321184 | 0.0158694   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00122509  | 0.0010377   | 0.23778     | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.000310962 | 0.000989797 | 0.753396    | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00113599  | 0.000831883 | 0.172082    | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.000760541 | 0.000848804 | 0.37025     | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.000530503 | 0.000928353 | 0.5677      | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00328463  | 0.000975956 | 0.000764622 | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.000441403 | 0.00094752  | 0.641324    | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.00983469  | 0.0050082   | 0.0495698   | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.000710328 | 0.00486924  | 0.884016    | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.000850474 | 0.00425739  | 0.841666    | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.002921    | 0.00431052  | 0.498002    | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.00340808  | 0.00465695  | 0.464279    | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.015374    | 0.00488822  | 0.00166142  | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.00747051  | 0.00470174  | 0.112095    | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.00460547  | 0.00196506  | 0.0190994   | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.00586166  | 0.00189602  | 0.00199246  | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0256676   | 0.0017294   | 0           | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0275874   | 0.00167511  | 0           | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0235287   | 0.00182763  | 0           | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0328725   | 0.00178861  | 0           | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0328235   | 0.00184136  | 0           | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_len              |  0.00134507  | 0.000920231 | 0.14384     | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_len              |  0.00218679  | 0.000866709 | 0.0116366   | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_len              | -0.00224227  | 0.000705209 | 0.00147598  | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_len               |  0.00277313  | 0.000708135 | 9.01395e-05 | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_len               | -0.00130807  | 0.00076416  | 0.0869464   | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated_X_len               | -0.00127638  | 0.00076934  | 0.097111    | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated_X_len               |  0.00037899  | 0.000828855 | 0.647497    | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:disp_X_len                 | -0.003933    | 0.00170836  | 0.0213283   | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:disp_X_len                 | -0.0065043   | 0.00162294  | 6.14164e-05 | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_X_len                 | -0.0100241   | 0.00141851  | 1.61293e-12 | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_X_len                  |  0.00716779  | 0.00142464  | 4.89215e-07 | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_X_len                  | -0.00123114  | 0.00153436  | 0.422337    | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:disp_X_len                  |  0.00376585  | 0.00157501  | 0.0168073   | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:disp_X_len                  |  0.00458769  | 0.00162016  | 0.00463352  | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:tXdXlen                    | -0.00564846  | 0.00353726  | 0.110308    | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:tXdXlen                    | -0.00195422  | 0.00341753  | 0.567445    | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:tXdXlen                    | -0.00143781  | 0.00293542  | 0.624267    | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:tXdXlen                     | -0.00214199  | 0.00304291  | 0.481481    | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:tXdXlen                     | -0.00509052  | 0.00326392  | 0.118854    | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:tXdXlen                     | -0.00644897  | 0.00346667  | 0.0628536   | 321184 | 0.0180207   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:tXdXlen                     | -0.00720218  | 0.00335581  | 0.0318643   | 321184 | 0.0180207   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  2.29874e-05 | 0.00125913  | 0.985434    | 321184 | 0.0210658   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.000325676 | 0.00120012  | 0.786109    | 321184 | 0.0210658   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00039927  | 0.00105057  | 0.703909    | 321184 | 0.0210658   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00212335  | 0.00104791  | 0.0427443   | 321184 | 0.0210658   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.000290397 | 0.00112699  | 0.796659    | 321184 | 0.0210658   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00592337  | 0.00119775  | 7.6286e-07  | 321184 | 0.0210658   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.000930395 | 0.00117581  | 0.428785    | 321184 | 0.0210658   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.0102337   | 0.00541626  | 0.0588403   | 321184 | 0.0210658   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.00115289  | 0.00510117  | 0.821199    | 321184 | 0.0210658   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.00680765  | 0.00454492  | 0.134177    | 321184 | 0.0210658   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.0099851   | 0.00475397  | 0.0357026   | 321184 | 0.0210658   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.00100651  | 0.00500201  | 0.840527    | 321184 | 0.0210658   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.0188734   | 0.00540433  | 0.000479441 | 321184 | 0.0210658   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.00753387  | 0.00531549  | 0.15639     | 321184 | 0.0210658   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.00942803  | 0.00262423  | 0.000327684 | 321184 | 0.0210658   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.00394732  | 0.00248799  | 0.112623    | 321184 | 0.0210658   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0295799   | 0.00224516  | 0           | 321184 | 0.0210658   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0448489   | 0.00227499  | 0           | 321184 | 0.0210658   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0443395   | 0.00242732  | 0           | 321184 | 0.0210658   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.0576474   | 0.00242434  | 0           | 321184 | 0.0210658   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.0564218   | 0.00256734  | 0           | 321184 | 0.0210658   |

## Pre-trend Joint Tests
| spec           | test                                    |   n_restrictions |   statistic |      pvalue |      n |
|:---------------|:----------------------------------------|-----------------:|------------:|------------:|-------:|
| event_att      | pretrend_att_joint_zero                 |                3 |    0.608094 | 0.894577    | 321184 |
| event_binary_B | pretrend_baseline_joint_zero            |                3 |    7.604    | 0.0549455   | 321184 |
| event_binary_B | pretrend_displacement_joint_zero        |                3 |   14.3226   | 0.00249732  | 321184 |
| event_binary_D | pretrend_length_displacement_joint_zero |                3 |    2.92506  | 0.403324    | 321184 |
| event_binary_D | pretrend_length_baseline_joint_zero     |                3 |   33.0977   | 3.07144e-07 | 321184 |
| event_score_C  | pretrend_score_baseline_joint_zero      |                3 |    0.224793 | 0.973491    | 321184 |
| event_score_C  | pretrend_score_slope_joint_zero         |                3 |   12.1829   | 0.00678227  | 321184 |