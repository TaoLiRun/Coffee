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
- Event-study reference period: -1


## Binary Specs
| spec                           | estimand                               | term                  |      n |   r2_within |         coef |          se |     pvalue |       ci_low |     ci_high |
|:-------------------------------|:---------------------------------------|:----------------------|-------:|------------:|-------------:|------------:|-----------:|-------------:|------------:|
| binary_collapsed               | low_predicted_incidence_effect_delta_b | post_X_treated        | 321184 |   0.0130244 |  0.000891858 | 0.000665864 | 0.180448   | -0.000413251 |  0.00219697 |
| binary_collapsed               | common_high_minus_low_post_shift       | post_X_disp           | 321184 |   0.0130244 | -0.0343661   | 0.00114263  | 0          | -0.0366057   | -0.0321265  |
| binary_collapsed               | high_minus_low_ddd                     | post_X_treated_X_disp | 321184 |   0.0130244 |  0.00582887  | 0.00251942  | 0.0206961  |  0.000890746 |  0.010767   |
| binary_collapsed_group_effects | low_predicted_incidence_effect         | post_X_treated_X_low  | 321184 |   0.0130244 |  0.000891858 | 0.000665864 | 0.180448   | -0.000413251 |  0.00219697 |
| binary_collapsed_group_effects | high_predicted_incidence_effect        | post_X_treated_X_high | 321184 |   0.0130244 |  0.00672073  | 0.00243419  | 0.00576554 |  0.00194967  |  0.0114918  |

## Score Spec
| spec            |   estimand | term                   |      n |   r2_within |        coef |          se |     pvalue |       ci_low |     ci_high |
|:----------------|-----------:|:-----------------------|-------:|------------:|------------:|------------:|-----------:|-------------:|------------:|
| score_collapsed |        nan | post_X_treated         | 321184 |   0.0182391 |  0.00227767 | 0.000811223 | 0.00499203 |  0.000687658 |  0.00386769 |
| score_collapsed |        nan | post_X_score           | 321184 |   0.0182391 | -0.056816   | 0.00168632  | 0          | -0.0601213   | -0.0535108  |
| score_collapsed |        nan | post_X_treated_X_score | 321184 |   0.0182391 |  0.00758612 | 0.00369529  | 0.040087   |  0.000343272 |  0.014829   |

## Event-study Specs
| spec           | estimand   | term                                                              |         coef |          se |      pvalue |       ci_low |      ci_high |      n |   r2_within |
|:---------------|:-----------|:------------------------------------------------------------------|-------------:|------------:|------------:|-------------:|-------------:|-------:|------------:|
| event_att      |            | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.000217695 | 0.00126337  | 0.863192    | -0.00225854  |  0.00269393  | 321184 | 0.000180302 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -6.3972e-05  | 0.00120637  | 0.957709    | -0.00242848  |  0.00230054  | 321184 | 0.000180302 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.000637519 | 0.00106308  | 0.548715    | -0.00272117  |  0.00144614  | 321184 | 0.000180302 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0026216   | 0.00106969  | 0.0142579   |  0.000524986 |  0.00471822  | 321184 | 0.000180302 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.000205661 | 0.00114845  | 0.857879    | -0.00204533  |  0.00245665  | 321184 | 0.000180302 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00656805  | 0.00121716  | 6.84408e-08 |  0.0041824   |  0.00895371  | 321184 | 0.000180302 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00179919  | 0.00119879  | 0.133405    | -0.000550467 |  0.00414885  | 321184 | 0.000180302 |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00130498  | 0.00105227  | 0.214924    | -0.00336745  |  0.000757493 | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.000183354 | 0.001004    | 0.855095    | -0.00178452  |  0.00215123  | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0016303   | 0.000847375 | 0.054369    | -3.05745e-05 |  0.00329118  | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.000501284 | 0.000855345 | 0.557838    | -0.00117521  |  0.00217778  | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.000447551 | 0.000941185 | 0.63442     | -0.00139719  |  0.00229229  | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00316421  | 0.000989491 | 0.00138582  |  0.00122478  |  0.00510363  | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00012099  | 0.000961387 | 0.899852    | -0.00176335  |  0.00200533  | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.00500733  | 0.00381344  | 0.189165    | -0.0024671   |  0.0124818   | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             | -0.00178669  | 0.00362437  | 0.62204     | -0.00889055  |  0.00531717  | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.00777542  | 0.00322894  | 0.0160427   | -0.0141042   | -0.00144663  | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.00646497  | 0.0032523   | 0.0468386   |  9.03969e-05 |  0.0128395   | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.00223429  | 0.00345928  | 0.518359    | -0.00901455  |  0.00454598  | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.0108627   | 0.00368337  | 0.00318856  |  0.00364324  |  0.0180822   | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.00391458  | 0.00363834  | 0.281968    | -0.00321666  |  0.0110458   | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.00529345  | 0.00181497  | 0.00354126  | -0.00885084  | -0.00173606  | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.0044973   | 0.00172871  | 0.00928401  |  0.001109    |  0.00788561  | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0231833   | 0.00155897  | 0           |  0.0201277   |  0.0262389   | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0260961   | 0.00152986  | 0           | -0.0290946   | -0.0230975   | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0242329   | 0.00165348  | 0           | -0.0274738   | -0.020992    | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0323743   | 0.00164105  | 0           | -0.0355908   | -0.0291578   | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0324197   | 0.00171654  | 0           | -0.0357841   | -0.0290552   | 321184 | 0.0158694   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00122509  | 0.0010377   | 0.23778     | -0.00325901  |  0.00080884  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.000310962 | 0.000989797 | 0.753396    | -0.00162906  |  0.00225099  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00113599  | 0.000831883 | 0.172082    | -0.000494517 |  0.0027665   | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.000760541 | 0.000848804 | 0.37025     | -0.000903134 |  0.00242422  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.000530503 | 0.000928353 | 0.5677      | -0.00128909  |  0.0023501   | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00328463  | 0.000975956 | 0.000764622 |  0.00137173  |  0.00519753  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.000441403 | 0.00094752  | 0.641324    | -0.00141576  |  0.00229856  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.00983469  | 0.0050082   | 0.0495698   |  1.84991e-05 |  0.0196509   | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.000710328 | 0.00486924  | 0.884016    | -0.00883348  |  0.0102541   | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.000850474 | 0.00425739  | 0.841666    | -0.00919506  |  0.00749412  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.002921    | 0.00431052  | 0.498002    | -0.00552772  |  0.0113697   | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.00340808  | 0.00465695  | 0.464279    | -0.00571965  |  0.0125358   | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.015374    | 0.00488822  | 0.00166142  |  0.005793    |  0.0249551   | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.00747051  | 0.00470174  | 0.112095    | -0.00174501  |  0.016686    | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.00460547  | 0.00196506  | 0.0190994   | -0.00845704  | -0.00075391  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.00586166  | 0.00189602  | 0.00199246  |  0.00214541  |  0.0095779   | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0256676   | 0.0017294   | 0           |  0.0222779   |  0.0290572   | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0275874   | 0.00167511  | 0           | -0.0308707   | -0.0243042   | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0235287   | 0.00182763  | 0           | -0.0271109   | -0.0199465   | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0328725   | 0.00178861  | 0           | -0.0363782   | -0.0293668   | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0328235   | 0.00184136  | 0           | -0.0364327   | -0.0292144   | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_len              |  0.00134507  | 0.000920231 | 0.14384     | -0.000458603 |  0.00314875  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_len              |  0.00218679  | 0.000866709 | 0.0116366   |  0.000488019 |  0.00388556  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_len              | -0.00224227  | 0.000705209 | 0.00147598  | -0.0036245   | -0.000860045 | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:treated_X_len               |  0.00277313  | 0.000708135 | 9.01395e-05 |  0.00138517  |  0.00416109  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:treated_X_len               | -0.00130807  | 0.00076416  | 0.0869464   | -0.00280584  |  0.000189704 | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:treated_X_len               | -0.00127638  | 0.00076934  | 0.097111    | -0.00278431  |  0.000231541 | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:treated_X_len               |  0.00037899  | 0.000828855 | 0.647497    | -0.00124559  |  0.00200357  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:disp_X_len                 | -0.003933    | 0.00170836  | 0.0213283   | -0.00728143  | -0.000584581 | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:disp_X_len                 | -0.0065043   | 0.00162294  | 6.14164e-05 | -0.0096853   | -0.0033233   | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:disp_X_len                 | -0.0100241   | 0.00141851  | 1.61293e-12 | -0.0128044   | -0.00724381  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:disp_X_len                  |  0.00716779  | 0.00142464  | 4.89215e-07 |  0.00437548  |  0.00996011  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:disp_X_len                  | -0.00123114  | 0.00153436  | 0.422337    | -0.00423853  |  0.00177624  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:disp_X_len                  |  0.00376585  | 0.00157501  | 0.0168073   |  0.000678787 |  0.00685291  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:disp_X_len                  |  0.00458769  | 0.00162016  | 0.00463352  |  0.00141214  |  0.00776324  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:tXdXlen                    | -0.00564846  | 0.00353726  | 0.110308    | -0.0125816   |  0.00128466  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:tXdXlen                    | -0.00195422  | 0.00341753  | 0.567445    | -0.00865266  |  0.00474422  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:tXdXlen                    | -0.00143781  | 0.00293542  | 0.624267    | -0.0071913   |  0.00431567  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:tXdXlen                     | -0.00214199  | 0.00304291  | 0.481481    | -0.00810616  |  0.00382218  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:tXdXlen                     | -0.00509052  | 0.00326392  | 0.118854    | -0.0114879   |  0.00130683  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:tXdXlen                     | -0.00644897  | 0.00346667  | 0.0628536   | -0.0132437   |  0.000345784 | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:tXdXlen                     | -0.00720218  | 0.00335581  | 0.0318643   | -0.0137796   | -0.000624719 | 321184 | 0.0180207   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  2.29874e-05 | 0.00125913  | 0.985434    | -0.00244493  |  0.0024909   | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.000325676 | 0.00120012  | 0.786109    | -0.00267794  |  0.00202659  | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00039927  | 0.00105057  | 0.703909    | -0.00245841  |  0.00165987  | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00212335  | 0.00104791  | 0.0427443   |  6.94148e-05 |  0.00417728  | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.000290397 | 0.00112699  | 0.796659    | -0.00249932  |  0.00191852  | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00592337  | 0.00119775  | 7.6286e-07  |  0.00357576  |  0.00827099  | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.000930395 | 0.00117581  | 0.428785    | -0.00137422  |  0.00323501  | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.0102337   | 0.00541626  | 0.0588403   | -0.000382305 |  0.0208497   | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.00115289  | 0.00510117  | 0.821199    | -0.00884553  |  0.0111513   | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.00680765  | 0.00454492  | 0.134177    | -0.0157158   |  0.00210049  | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.0099851   | 0.00475397  | 0.0357026   |  0.000667203 |  0.019303    | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.00100651  | 0.00500201  | 0.840527    | -0.0108106   |  0.00879754  | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.0188734   | 0.00540433  | 0.000479441 |  0.0082808   |  0.029466    | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.00753387  | 0.00531549  | 0.15639     | -0.0028846   |  0.0179523   | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.00942803  | 0.00262423  | 0.000327684 | -0.0145716   | -0.00428447  | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.00394732  | 0.00248799  | 0.112623    | -0.000929197 |  0.00882383  | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0295799   | 0.00224516  | 0           |  0.0251794   |  0.0339805   | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0448489   | 0.00227499  | 0           | -0.049308    | -0.0403899   | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0443395   | 0.00242732  | 0           | -0.0490971   | -0.0395819   | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.0576474   | 0.00242434  | 0           | -0.0623992   | -0.0528957   | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.0564218   | 0.00256734  | 0           | -0.0614539   | -0.0513898   | 321184 | 0.0210658   |

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

## Matched-Sample Support
| treated   | match_cell                                                    |   blocked_available |   non_blocked_available |   retained_per_group |   common_support |   episodes_before |   episodes_after |   blocked_retained |   non_blocked_retained |   treated_retained |   control_retained |
|:----------|:--------------------------------------------------------------|--------------------:|------------------------:|---------------------:|-----------------:|------------------:|-----------------:|-------------------:|-----------------------:|-------------------:|-------------------:|
| 0         | 0|(20074.5, 30111.25]|(30111.25, 40148.0]|(0.999, 10037.75]   |                 591 |                    1349 |                  591 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(0.999, 10037.75]|(10037.75, 20074.5]   |                  87 |                     422 |                   87 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(30111.25, 40148.0]|(30111.25, 40148.0]|(0.999, 10037.75]   |                3978 |                    1024 |                 1024 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(0.999, 10037.75]|(20074.5, 30111.25]   |                 119 |                    1134 |                  119 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(30111.25, 40148.0]|(10037.75, 20074.5] |                 115 |                     271 |                  115 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(0.999, 10037.75]|(20074.5, 30111.25]   |                 155 |                     582 |                  155 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(0.999, 10037.75]|(10037.75, 20074.5]   |                 551 |                     504 |                  504 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(0.999, 10037.75]|(0.999, 10037.75]|(20074.5, 30111.25]     |                   1 |                     759 |                    1 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(0.999, 10037.75]|(0.999, 10037.75]|(30111.25, 40148.0]     |                   4 |                    3095 |                    4 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(30111.25, 40148.0]|(0.999, 10037.75]   |                  29 |                     353 |                   29 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(30111.25, 40148.0]|(0.999, 10037.75]|(10037.75, 20074.5]   |                 447 |                     235 |                  235 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(30111.25, 40148.0]|(30111.25, 40148.0]|(10037.75, 20074.5] |                 337 |                     124 |                  124 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(30111.25, 40148.0]|(10037.75, 20074.5] |                   7 |                      92 |                    7 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(30111.25, 40148.0]|(0.999, 10037.75]|(20074.5, 30111.25]   |                  43 |                     140 |                   43 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(30111.25, 40148.0]|(20074.5, 30111.25]|(0.999, 10037.75]   |                 166 |                      56 |                   56 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(20074.5, 30111.25]|(0.999, 10037.75]   |                 167 |                     214 |                  167 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(20074.5, 30111.25]|(10037.75, 20074.5] |                 451 |                     725 |                  451 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(20074.5, 30111.25]|(0.999, 10037.75]   |                  34 |                     191 |                   34 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(30111.25, 40148.0]|(20074.5, 30111.25]|(10037.75, 20074.5] |                 369 |                     227 |                  227 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(20074.5, 30111.25]|(10037.75, 20074.5] |                 115 |                     469 |                  115 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(0.999, 10037.75]|(30111.25, 40148.0]   |                   0 |                       2 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(0.999, 10037.75]|(30111.25, 40148.0]   |                   0 |                      27 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(0.999, 10037.75]|(10037.75, 20074.5]|(20074.5, 30111.25]   |                   0 |                    1655 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(0.999, 10037.75]|(10037.75, 20074.5]|(30111.25, 40148.0]   |                   0 |                    2664 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(10037.75, 20074.5]|(10037.75, 20074.5] |                 249 |                    1120 |                  249 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(30111.25, 40148.0]|(10037.75, 20074.5]|(20074.5, 30111.25] |                   3 |                      57 |                    3 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(10037.75, 20074.5]|(10037.75, 20074.5] |                  25 |                     323 |                   25 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(10037.75, 20074.5]|(20074.5, 30111.25] |                   6 |                     459 |                    6 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(30111.25, 40148.0]|(10037.75, 20074.5]|(10037.75, 20074.5] |                 446 |                     450 |                  446 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(10037.75, 20074.5]|(20074.5, 30111.25] |                  17 |                     418 |                   17 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(30111.25, 40148.0]|(10037.75, 20074.5]|(0.999, 10037.75]   |                  37 |                      11 |                   11 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(10037.75, 20074.5]|(0.999, 10037.75]   |                  12 |                      23 |                   12 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(10037.75, 20074.5]|(30111.25, 40148.0] |                   0 |                      74 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(20074.5, 30111.25]|(20074.5, 30111.25] |                  98 |                    1743 |                   98 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(20074.5, 30111.25]|(30111.25, 40148.0] |                  13 |                    2339 |                   13 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(20074.5, 30111.25]|(20074.5, 30111.25] |                 114 |                     507 |                  114 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(30111.25, 40148.0]|(20074.5, 30111.25]|(20074.5, 30111.25] |                  38 |                      95 |                   38 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(20074.5, 30111.25]|(30111.25, 40148.0] |                   0 |                       1 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(0.999, 10037.75]|(20074.5, 30111.25]   |                  41 |                     121 |                   41 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(0.999, 10037.75]|(0.999, 10037.75]|(30111.25, 40148.0]     |                   3 |                     728 |                    3 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(30111.25, 40148.0]|(0.999, 10037.75]|(10037.75, 20074.5]   |                  81 |                      30 |                   30 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(30111.25, 40148.0]|(10037.75, 20074.5] |                  41 |                      56 |                   41 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(30111.25, 40148.0]|(0.999, 10037.75]   |                 142 |                     280 |                  142 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(0.999, 10037.75]|(20074.5, 30111.25]   |                  45 |                     251 |                   45 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(0.999, 10037.75]|(10037.75, 20074.5]   |                  93 |                      88 |                   88 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(30111.25, 40148.0]|(30111.25, 40148.0]|(0.999, 10037.75]   |                 806 |                     203 |                  203 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(30111.25, 40148.0]|(10037.75, 20074.5] |                   0 |                      12 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(0.999, 10037.75]|(10037.75, 20074.5]   |                  24 |                      75 |                   24 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(30111.25, 40148.0]|(30111.25, 40148.0]|(10037.75, 20074.5] |                 111 |                      25 |                   25 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(0.999, 10037.75]|(0.999, 10037.75]|(20074.5, 30111.25]     |                   0 |                     114 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(30111.25, 40148.0]|(0.999, 10037.75]   |                  14 |                      77 |                   14 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(30111.25, 40148.0]|(0.999, 10037.75]|(20074.5, 30111.25]   |                   7 |                      19 |                    7 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(20074.5, 30111.25]|(10037.75, 20074.5] |                  36 |                     101 |                   36 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(20074.5, 30111.25]|(10037.75, 20074.5] |                 134 |                     186 |                  134 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(30111.25, 40148.0]|(20074.5, 30111.25]|(10037.75, 20074.5] |                 112 |                      47 |                   47 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(20074.5, 30111.25]|(0.999, 10037.75]   |                  67 |                      58 |                   58 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(30111.25, 40148.0]|(20074.5, 30111.25]|(0.999, 10037.75]   |                  37 |                      16 |                   16 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(20074.5, 30111.25]|(0.999, 10037.75]   |                  20 |                      53 |                   20 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(0.999, 10037.75]|(30111.25, 40148.0]   |                   0 |                       9 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(0.999, 10037.75]|(30111.25, 40148.0]   |                   0 |                       1 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(10037.75, 20074.5]|(10037.75, 20074.5] |                   0 |                      85 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(0.999, 10037.75]|(10037.75, 20074.5]|(30111.25, 40148.0]   |                   0 |                     543 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(0.999, 10037.75]|(10037.75, 20074.5]|(20074.5, 30111.25]   |                   1 |                     470 |                    1 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(10037.75, 20074.5]|(20074.5, 30111.25] |                   3 |                     147 |                    3 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(10037.75, 20074.5]|(10037.75, 20074.5] |                  48 |                     286 |                   48 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(30111.25, 40148.0]|(10037.75, 20074.5]|(10037.75, 20074.5] |                  85 |                     120 |                   85 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(10037.75, 20074.5]|(20074.5, 30111.25] |                   0 |                     120 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(30111.25, 40148.0]|(10037.75, 20074.5]|(20074.5, 30111.25] |                   0 |                       9 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(30111.25, 40148.0]|(10037.75, 20074.5]|(0.999, 10037.75]   |                   9 |                       5 |                    5 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(10037.75, 20074.5]|(0.999, 10037.75]   |                   4 |                      11 |                    4 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(10037.75, 20074.5]|(30111.25, 40148.0] |                   0 |                      42 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(20074.5, 30111.25]|(20074.5, 30111.25] |                  36 |                     356 |                   36 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(30111.25, 40148.0]|(20074.5, 30111.25]|(20074.5, 30111.25] |                  10 |                      22 |                   10 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(20074.5, 30111.25]|(20074.5, 30111.25] |                  29 |                      93 |                   29 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(20074.5, 30111.25]|(30111.25, 40148.0] |                   2 |                     490 |                    2 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| all       | __overall__                                                   |               10865 |                   29283 |                 6317 |                1 |             40148 |            12634 |               6317 |                   6317 |               2394 |              10240 |

## Matched Binary Specs
| spec                           | estimand                               | term                  |      n |   r2_within |        coef |         se |     pvalue |      ci_low |    ci_high |
|:-------------------------------|:---------------------------------------|:----------------------|-------:|------------:|------------:|-----------:|-----------:|------------:|-----------:|
| binary_collapsed               | low_predicted_incidence_effect_delta_b | post_X_treated        | 101072 | 0.000246829 |  0.00686845 | 0.00212031 | 0.00120104 |  0.00271233 | 0.0110246  |
| binary_collapsed               | common_high_minus_low_post_shift       | post_X_disp           | 101072 | 0.000246829 | -0.00177021 | 0.00158093 | 0.262852   | -0.00486908 | 0.00132866 |
| binary_collapsed               | high_minus_low_ddd                     | post_X_treated_X_disp | 101072 | 0.000246829 | -0.00405668 | 0.00342941 | 0.236867   | -0.0107788  | 0.00266548 |
| binary_collapsed_group_effects | low_predicted_incidence_effect         | post_X_treated_X_low  | 101072 | 0.000246829 |  0.00686845 | 0.00212031 | 0.00120104 |  0.00271233 | 0.0110246  |
| binary_collapsed_group_effects | high_predicted_incidence_effect        | post_X_treated_X_high | 101072 | 0.000246829 |  0.00281177 | 0.00273688 | 0.30427    | -0.00255293 | 0.00817647 |

## Matched Event-study Specs
| spec           | estimand   | term                                                              |         coef |         se |      pvalue |       ci_low |      ci_high |      n |   r2_within |
|:---------------|:-----------|:------------------------------------------------------------------|-------------:|-----------:|------------:|-------------:|-------------:|-------:|------------:|
| event_att      |            | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00935193  | 0.0027157  | 0.00057577  | -0.0146751   | -0.00402875  | 101072 | 0.000452776 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00644432  | 0.00273795 | 0.0186027   | -0.0118111   | -0.00107752  | 101072 | 0.000452776 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00648525  | 0.00241824 | 0.00733208  | -0.0112254   | -0.00174514  | 101072 | 0.000452776 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00138297  | 0.00219816 | 0.529265    | -0.00292577  |  0.0056917   | 101072 | 0.000452776 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00490891  | 0.00238851 | 0.0398784   | -0.00959076  | -0.000227068 | 101072 | 0.000452776 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00370095  | 0.00252963 | 0.143481    | -0.0012575   |  0.00865941  | 101072 | 0.000452776 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00245698  | 0.00252252 | 0.330066    | -0.00740149  |  0.00248754  | 101072 | 0.000452776 |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0127294   | 0.0035945  | 0.000399498 | -0.0197752   | -0.00568366  | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0105751   | 0.00372082 | 0.00448836  | -0.0178685   | -0.00328172  | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00287266  | 0.00317812 | 0.366073    | -0.00910225  |  0.00335694  | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.000310511 | 0.00284686 | 0.913147    | -0.00589078  |  0.00526976  | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.000375204 | 0.00310263 | 0.903748    | -0.00645684  |  0.00570643  | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00284838  | 0.00310715 | 0.359308    | -0.0032421   |  0.00893887  | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.000544116 | 0.00302291 | 0.857157    | -0.00646948  |  0.00538124  | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.00611149  | 0.00538103 | 0.256084    | -0.00443615  |  0.0166591   | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0072303   | 0.00541807 | 0.182071    | -0.00338995  |  0.0178506   | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.00684784  | 0.00474994 | 0.149421    | -0.0161584   |  0.00246277  | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.00311422  | 0.00436858 | 0.475941    | -0.00544886  |  0.0116773   | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.00931672  | 0.004745   | 0.0496121   | -0.0186176   | -1.57996e-05 | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.00138588  | 0.00500385 | 0.781813    | -0.00842243  |  0.0111942   | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.00429295  | 0.00498873 | 0.389513    | -0.0140716   |  0.00548572  | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.00253875  | 0.00264278 | 0.336754    | -0.00771899  |  0.0026415   | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.00314328  | 0.00249589 | 0.207916    | -0.00174904  |  0.00803559  | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0271364   | 0.00217325 | 0           |  0.0228765   |  0.0313963   | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  0.0048791   | 0.00208853 | 0.0194994   |  0.000785266 |  0.00897293  | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.00699755  | 0.0022821  | 0.00217199  |  0.00252429  |  0.0114708   | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.00397635  | 0.0022718  | 0.0800897   | -0.000476727 |  0.00842942  | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.0048889   | 0.00234799 | 0.0373478   |  0.000286477 |  0.00949132  | 101072 | 0.00323746  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0131939   | 0.00359428 | 0.000242787 | -0.0202392   | -0.00614855  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.011122    | 0.0037297  | 0.00286919  | -0.0184328   | -0.00381119  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00375532  | 0.00320138 | 0.240805    | -0.0100305   |  0.00251987  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.000378548 | 0.00284837 | 0.894275    | -0.00596179  |  0.00520469  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.000355684 | 0.00311909 | 0.909212    | -0.00646957  |  0.00575821  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00279625  | 0.00312294 | 0.370596    | -0.00332518  |  0.00891768  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.000301044 | 0.00301338 | 0.920423    | -0.00620772  |  0.00560564  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0109602   | 0.00691417 | 0.112949    | -0.00259258  |  0.0245131   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.01202     | 0.00695056 | 0.0837701   | -0.00160417  |  0.0256441   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.000349801 | 0.00599507 | 0.953472    | -0.012101    |  0.0114014   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.00125792  | 0.00563148 | 0.823248    | -0.00978063  |  0.0122965   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.0070529   | 0.00613313 | 0.250178    | -0.0190748   |  0.00496896  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.00685839  | 0.00671939 | 0.307423    | -0.00631264  |  0.0200294   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.00199036  | 0.00653939 | 0.760855    | -0.0148086   |  0.0108278   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.000452187 | 0.00282593 | 0.872873    | -0.00508706  |  0.00599143  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.00748663  | 0.00269157 | 0.00541873  |  0.00221074  |  0.0127625   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0342377   | 0.00239187 | 0           |  0.0295493   |  0.0389261   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  0.00655904  | 0.00229906 | 0.00433888  |  0.00205254  |  0.0110655   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.0119785   | 0.00252249 | 2.07001e-06 |  0.00703403  |  0.016923    | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.00762086  | 0.00245835 | 0.00193952  |  0.00280213  |  0.0124396   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.00810923  | 0.00247388 | 0.00104851  |  0.00326005  |  0.0129584   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_len              |  0.00410753  | 0.00293974 | 0.162365    | -0.0016548   |  0.00986987  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_len              |  0.00607146  | 0.00300429 | 0.0433077   |  0.000182607 |  0.0119603   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_len              | -0.000212649 | 0.00257975 | 0.934306    | -0.00526934  |  0.00484404  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:treated_X_len               |  0.00876033  | 0.00228055 | 0.000122971 |  0.00429011  |  0.0132306   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:treated_X_len               | -0.00300547  | 0.00242133 | 0.214538    | -0.00775164  |  0.00174071  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:treated_X_len               | -0.00178706  | 0.00240818 | 0.458054    | -0.00650746  |  0.00293334  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:treated_X_len               |  0.00139422  | 0.00258654 | 0.589877    | -0.00367579  |  0.00646423  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:disp_X_len                 | -0.0103077   | 0.00218184 | 2.33395e-06 | -0.0145844   | -0.00603095  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:disp_X_len                 | -0.0148983   | 0.0019511  | 2.39808e-14 | -0.0187228   | -0.0110739   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:disp_X_len                 | -0.0200347   | 0.00161381 | 0           | -0.023198    | -0.0168714   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:disp_X_len                  | -0.00338146  | 0.0016416  | 0.0394325   | -0.00659924  | -0.000163679 | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:disp_X_len                  | -0.0132145   | 0.00184239 | 7.77378e-13 | -0.0168259   | -0.00960315  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:disp_X_len                  | -0.00999061  | 0.00192754 | 2.21619e-07 | -0.0137689   | -0.00621233  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:disp_X_len                  | -0.006224    | 0.00212403 | 0.00339273  | -0.0103874   | -0.00206057  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:tXdXlen                    | -0.00461845  | 0.00493345 | 0.349215    | -0.0142888   |  0.00505187  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:tXdXlen                    | -0.00408203  | 0.00490776 | 0.405566    | -0.013702    |  0.00553793  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:tXdXlen                    |  0.000921891 | 0.0041827  | 0.825559    | -0.00727684  |  0.00912062  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:tXdXlen                     | -0.00460669  | 0.00397728 | 0.246783    | -0.0124028   |  0.00318938  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:tXdXlen                     |  0.00689127  | 0.00426306 | 0.10601     | -0.00146498  |  0.0152475   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:tXdXlen                     |  0.000100967 | 0.00462238 | 0.982573    | -0.0089596   |  0.00916154  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:tXdXlen                     | -0.000684278 | 0.00464246 | 0.882822    | -0.0097842   |  0.00841564  | 101072 | 0.0067064   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0129652   | 0.00295917 | 1.1889e-05  | -0.0187656   | -0.00716478  | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0102561   | 0.00300986 | 0.000657671 | -0.0161558   | -0.00435629  | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00383419  | 0.00251541 | 0.127464    | -0.00876478  |  0.0010964   | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0009169   | 0.00230468 | 0.690753    | -0.00360062  |  0.00543442  | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00171958  | 0.00256904 | 0.503286    | -0.00675528  |  0.00331612  | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00272115  | 0.00259016 | 0.293475    | -0.00235596  |  0.00779826  | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00089357  | 0.00252113 | 0.723021    | -0.00583537  |  0.00404823  | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.0163736   | 0.0103497  | 0.113666    | -0.00391338  |  0.0366606   | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.0157991   | 0.0102549  | 0.123432    | -0.00430217  |  0.0359003   | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.0136282   | 0.00885479 | 0.123811    | -0.0309849   |  0.00372853  | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -9.66483e-05 | 0.00877114 | 0.991209    | -0.0172894   |  0.0170961   | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.0194016   | 0.00939347 | 0.0389028   | -0.0378142   | -0.000988919 | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.00215162  | 0.0102809  | 0.834231    | -0.0180006   |  0.0223038   | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             | -0.0123027   | 0.0101895  | 0.227307    | -0.0322757   |  0.00767036  | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.0176961   | 0.00535418 | 0.000952092 | -0.0281911   | -0.00720105  | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered | -0.00844906  | 0.00501913 | 0.0923279   | -0.0182873   |  0.0013892   | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.05106     | 0.00441339 | 0           |  0.0424091   |  0.0597109   | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.00630824  | 0.0044536  | 0.156672    | -0.015038    |  0.00242149  | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.00577647  | 0.00480599 | 0.229413    | -0.015197    |  0.003644    | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.0137346   | 0.00482277 | 0.00440829  | -0.023188    | -0.00428129  | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.0112452   | 0.00505566 | 0.0261479   | -0.021155    | -0.00133529  | 101072 | 0.00551063  |

## Matched Pre-trend Joint Tests
| spec           | test                                    |   n_restrictions |   statistic |      pvalue |      n |
|:---------------|:----------------------------------------|-----------------:|------------:|------------:|-------:|
| event_att      | pretrend_att_joint_zero                 |                3 |    13.4841  | 0.00369853  | 101072 |
| event_binary_B | pretrend_baseline_joint_zero            |                3 |    14.9697  | 0.00184274  | 101072 |
| event_binary_B | pretrend_displacement_joint_zero        |                3 |     9.47001 | 0.0236526   | 101072 |
| event_binary_D | pretrend_length_displacement_joint_zero |                3 |     1.8795  | 0.597789    | 101072 |
| event_binary_D | pretrend_length_baseline_joint_zero     |                3 |     6.67048 | 0.0831764   | 101072 |
| event_score_C  | pretrend_score_baseline_joint_zero      |                3 |    21.4698  | 8.40851e-05 | 101072 |
| event_score_C  | pretrend_score_slope_joint_zero         |                3 |    13.392   | 0.00386112  | 101072 |

## Blocked Gap Event Study
| spec              | estimand   | term                                                       |         coef |         se |      pvalue |       ci_low |    ci_high |      n |   r2_within |
|:------------------|:-----------|:-----------------------------------------------------------|-------------:|-----------:|------------:|-------------:|-----------:|-------:|------------:|
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[-4]:blocked_treated_gap | -0.00648854  | 0.00399305 | 0.104196    | -0.0143155   | 0.00133844 | 101072 |  0.00288848 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[-3]:blocked_treated_gap |  0.00201064  | 0.00392405 | 0.608388    | -0.00568109  | 0.00970236 | 101072 |  0.00288848 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[-2]:blocked_treated_gap |  0.0179889   | 0.00342045 | 1.47018e-07 |  0.0112843   | 0.0246935  | 101072 |  0.00288848 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[1]:blocked_treated_gap  |  0.00772338  | 0.00321286 | 0.0162356   |  0.0014257   | 0.0140211  | 101072 |  0.00288848 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[2]:blocked_treated_gap  | -0.00264599  | 0.00346593 | 0.445222    | -0.00943974  | 0.00414776 | 101072 |  0.00288848 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[3]:blocked_treated_gap  |  0.00762327  | 0.00386893 | 0.0488161   |  3.95915e-05 | 0.015207   | 101072 |  0.00288848 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[4]:blocked_treated_gap  |  0.000139009 | 0.00393875 | 0.971847    | -0.00758154  | 0.00785956 | 101072 |  0.00288848 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[-4]:blocked_control_gap |  2.57408e-07 | 0.00249845 | 0.999918    | -0.00489708  | 0.0048976  | 101072 |  0.00288848 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[-3]:blocked_control_gap |  0.00519477  | 0.00237851 | 0.028977    |  0.000532539 | 0.009857   | 101072 |  0.00288848 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[-2]:blocked_control_gap |  0.0276831   | 0.00208389 | 0           |  0.0235984   | 0.0317679  | 101072 |  0.00288848 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[1]:blocked_control_gap  |  0.00492795  | 0.00200581 | 0.0140301   |  0.000996252 | 0.00885964 | 101072 |  0.00288848 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[2]:blocked_control_gap  |  0.00705554  | 0.00219546 | 0.00131368  |  0.0027521   | 0.011359   | 101072 |  0.00288848 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[3]:blocked_control_gap  |  0.00341142  | 0.00218126 | 0.117849    | -0.000864171 | 0.00768702 | 101072 |  0.00288848 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[4]:blocked_control_gap  |  0.00498371  | 0.00225266 | 0.026959    |  0.000568158 | 0.00939926 | 101072 |  0.00288848 |

## Pre-period Bias Equality Tests
| spec                   | test                 | term                             |         coef |          se |      pvalue |      n | sample_scope   |
|:-----------------------|:---------------------|:---------------------------------|-------------:|------------:|------------:|-------:|:---------------|
| pretrend_bias_equality | pretrend_bias_linear | non_blocked_treated_control_bias |  0.00083553  | 0.000347048 | 0.0160605   | 160592 | full           |
| pretrend_bias_equality | pretrend_bias_linear | bias_equality_difference         | -0.00125276  | 0.00125232  | 0.317139    | 160592 | full           |
| pretrend_bias_equality | pretrend_bias_linear | blocked_treated_control_bias     | -0.000417229 | 0.00120327  | 0.728781    | 160592 | full           |
| pretrend_bias_equality | pretrend_bias_linear | non_blocked_treated_control_bias |  0.00547976  | 0.00119975  | 4.93802e-06 |  50536 | matched        |
| pretrend_bias_equality | pretrend_bias_linear | bias_equality_difference         | -0.0021888   | 0.00179087  | 0.221633    |  50536 | matched        |
| pretrend_bias_equality | pretrend_bias_linear | blocked_treated_control_bias     |  0.00329096  | 0.00132959  | 0.0133173   |  50536 | matched        |