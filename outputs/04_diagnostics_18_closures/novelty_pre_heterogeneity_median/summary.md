# Displacement Effect Estimation Summary

- Sample rows: 207,152
- Unique members: 25,894
- Unique closures: 18
- Event FE units: 25,894
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=false
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Model type: DDD
- Event-study reference period: -1
- Pre-novelty heterogeneity: collapsed DDD includes post×(treatment, displacement)×high-pre split
- Customer median split: True


## Binary Specs
| spec                               | term                                     |     n |   r2_within |       coef |         se |      pvalue |
|:-----------------------------------|:-----------------------------------------|------:|------------:|-----------:|-----------:|------------:|
| binary_collapsed                   | post_X_treated                           | 95986 | 0.000566364 |  0.031339  | 0.0119918  | 0.00897169  |
| binary_collapsed                   | post_X_disp                              | 95986 | 0.000566364 |  0.0384063 | 0.00638615 | 1.83868e-09 |
| binary_collapsed                   | post_X_treated_X_disp                    | 95986 | 0.000566364 | -0.0415532 | 0.0144941  | 0.00414904  |
| binary_collapsed_pre_novelty_split | post_X_treated                           | 95986 | 0.0338967   |  0.260594  | 0.014641   | 0           |
| binary_collapsed_pre_novelty_split | post_X_disp                              | 95986 | 0.0338967   |  0.1301    | 0.00650563 | 0           |
| binary_collapsed_pre_novelty_split | post_X_treated_X_disp                    | 95986 | 0.0338967   | -0.262761  | 0.0173015  | 0           |
| binary_collapsed_pre_novelty_split | post_X_treated_X_novelty_pre_high        | 95986 | 0.0338967   | -0.481443  | 0.0183036  | 0           |
| binary_collapsed_pre_novelty_split | post_X_disp_X_novelty_pre_high           | 95986 | 0.0338967   | -0.308758  | 0.00719021 | 0           |
| binary_collapsed_pre_novelty_split | post_X_treated_X_disp_X_novelty_pre_high | 95986 | 0.0338967   |  0.492343  | 0.0237559  | 0           |

## Score Spec
| spec            | term                   |     n |   r2_within |       coef |         se |      pvalue |
|:----------------|:-----------------------|------:|------------:|-----------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 95986 |  0.00043449 |  0.0190095 | 0.0102181  | 0.0628477   |
| score_collapsed | post_X_score           | 95986 |  0.00043449 |  0.0538617 | 0.00980345 | 3.96953e-08 |
| score_collapsed | post_X_treated_X_score | 95986 |  0.00043449 | -0.0453383 | 0.0220531  | 0.0398073   |

## Event-study Specs
| spec                             | term                                                                     |         coef |         se |      pvalue |     n |   r2_within |
|:---------------------------------|:-------------------------------------------------------------------------|-------------:|-----------:|------------:|------:|------------:|
| event_att                        | C(rel_t, contr.treatment(base=-1))[-4]:treated                           | -0.0125684   | 0.0126526  | 0.320553    | 95986 | 0.000331647 |
| event_att                        | C(rel_t, contr.treatment(base=-1))[-3]:treated                           | -0.00429424  | 0.0127413  | 0.736096    | 95986 | 0.000331647 |
| event_att                        | C(rel_t, contr.treatment(base=-1))[-2]:treated                           | -0.0242433   | 0.0121857  | 0.0466594   | 95986 | 0.000331647 |
| event_att                        | C(rel_t, contr.treatment(base=-1))[1]:treated                            |  0.0299806   | 0.013095   | 0.0220618   | 95986 | 0.000331647 |
| event_att                        | C(rel_t, contr.treatment(base=-1))[2]:treated                            | -0.00867322  | 0.0133617  | 0.516273    | 95986 | 0.000331647 |
| event_att                        | C(rel_t, contr.treatment(base=-1))[3]:treated                            | -0.0264801   | 0.013372   | 0.0476855   | 95986 | 0.000331647 |
| event_att                        | C(rel_t, contr.treatment(base=-1))[4]:treated                            | -0.0170574   | 0.0133803  | 0.202388    | 95986 | 0.000331647 |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[-4]:treated                           | -0.02617     | 0.022782   | 0.250687    | 95986 | 0.00130448  |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[-3]:treated                           | -0.0211656   | 0.0232683  | 0.363026    | 95986 | 0.00130448  |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[-2]:treated                           | -0.0358051   | 0.0236186  | 0.129541    | 95986 | 0.00130448  |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[1]:treated                            |  0.0393287   | 0.024002   | 0.101319    | 95986 | 0.00130448  |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[2]:treated                            |  0.0169638   | 0.0232645  | 0.465904    | 95986 | 0.00130448  |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[3]:treated                            | -0.0159788   | 0.0239145  | 0.504038    | 95986 | 0.00130448  |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[4]:treated                            |  0.00452552  | 0.0240641  | 0.850831    | 95986 | 0.00130448  |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp                    |  0.022457    | 0.0271757  | 0.408608    | 95986 | 0.00130448  |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp                    |  0.0264345   | 0.027598   | 0.338154    | 95986 | 0.00130448  |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp                    |  0.0158414   | 0.0273081  | 0.561854    | 95986 | 0.00130448  |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp                     | -0.0149976   | 0.0284253  | 0.597773    | 95986 | 0.00130448  |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp                     | -0.0417272   | 0.0283147  | 0.140579    | 95986 | 0.00130448  |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp                     | -0.0170335   | 0.0286657  | 0.552377    | 95986 | 0.00130448  |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp                     | -0.035715    | 0.0287696  | 0.214467    | 95986 | 0.00130448  |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                       |  0.039398    | 0.0116972  | 0.000758062 | 95986 | 0.00130448  |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                       |  0.0325963   | 0.0116501  | 0.00514761  | 95986 | 0.00130448  |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                       |  0.0157529   | 0.0120223  | 0.190106    | 95986 | 0.00130448  |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                        |  0.0422948   | 0.0124188  | 0.000661116 | 95986 | 0.00130448  |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                        |  0.0698429   | 0.0123953  | 1.77579e-08 | 95986 | 0.00130448  |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                        |  0.0676203   | 0.0129338  | 1.72765e-07 | 95986 | 0.00130448  |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                        |  0.066255    | 0.0127623  | 2.10507e-07 | 95986 | 0.00130448  |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-4]:treated                           |  0.024795    | 0.032434   | 0.444593    | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-3]:treated                           |  0.0394228   | 0.0334217  | 0.23819     | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-2]:treated                           | -0.0172232   | 0.0349112  | 0.621775    | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[1]:treated                            |  0.299549    | 0.0321171  | 0           | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[2]:treated                            |  0.270205    | 0.031737   | 0           | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[3]:treated                            |  0.257154    | 0.0316568  | 4.44089e-16 | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[4]:treated                            |  0.273526    | 0.031536   | 0           | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp                    | -0.0345244   | 0.0376615  | 0.359309    | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp                    | -0.0166407   | 0.0384489  | 0.665164    | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp                    |  8.32073e-05 | 0.0391459  | 0.998304    | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp                     | -0.267855    | 0.0372676  | 6.81899e-13 | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp                     | -0.269028    | 0.0372956  | 5.63549e-13 | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp                     | -0.280791    | 0.0370568  | 3.66374e-14 | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp                     | -0.298881    | 0.0368117  | 4.44089e-16 | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                       |  0.042167    | 0.0123786  | 0.000659356 | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                       |  0.0296806   | 0.0123022  | 0.015846    | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                       |  0.00916998  | 0.012664   | 0.469012    | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                        |  0.127293    | 0.0129425  | 0           | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                        |  0.168918    | 0.0130339  | 0           | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                        |  0.160891    | 0.0134876  | 0           | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                        |  0.149639    | 0.0132631  | 0           | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_novelty_pre_high        | -0.0551033   | 0.038772   | 0.155269    | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_novelty_pre_high        | -0.0813356   | 0.0397577  | 0.0407898   | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_novelty_pre_high        | -0.0244871   | 0.0408927  | 0.549304    | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[1]:treated_X_novelty_pre_high         | -0.512082    | 0.0401716  | 0           | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[2]:treated_X_novelty_pre_high         | -0.505256    | 0.0390629  | 0           | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[3]:treated_X_novelty_pre_high         | -0.539959    | 0.0395932  | 0           | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[4]:treated_X_novelty_pre_high         | -0.529644    | 0.0398389  | 0           | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-4]:disp_X_novelty_pre_high           |  0.0117082   | 0.0142346  | 0.410791    | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-3]:disp_X_novelty_pre_high           |  0.0236316   | 0.0137452  | 0.0855803   | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-2]:disp_X_novelty_pre_high           |  0.0255666   | 0.0128216  | 0.0461617   | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[1]:disp_X_novelty_pre_high            | -0.26762     | 0.0143365  | 0           | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[2]:disp_X_novelty_pre_high            | -0.314575    | 0.0145525  | 0           | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[3]:disp_X_novelty_pre_high            | -0.309206    | 0.0152774  | 0           | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[4]:disp_X_novelty_pre_high            | -0.28206     | 0.0154258  | 0           | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp_X_novelty_pre_high |  0.0702783   | 0.0488588  | 0.150336    | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp_X_novelty_pre_high |  0.037488    | 0.0498077  | 0.451666    | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp_X_novelty_pre_high |  0.02623     | 0.0494727  | 0.595985    | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp_X_novelty_pre_high  |  0.525778    | 0.0505529  | 0           | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp_X_novelty_pre_high  |  0.469178    | 0.0503361  | 0           | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp_X_novelty_pre_high  |  0.557608    | 0.0506609  | 0           | 95986 | 0.0351276   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp_X_novelty_pre_high  |  0.544332    | 0.0514087  | 0           | 95986 | 0.0351276   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-4]:treated                           | -0.0246253   | 0.0229659  | 0.283618    | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-3]:treated                           | -0.0147504   | 0.0236067  | 0.532083    | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-2]:treated                           | -0.0366378   | 0.0240333  | 0.127408    | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[1]:treated                            |  0.0372733   | 0.024673   | 0.130882    | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[2]:treated                            |  0.0185546   | 0.023434   | 0.428497    | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[3]:treated                            | -0.0149261   | 0.0241393  | 0.536364    | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[4]:treated                            |  0.0062944   | 0.0242532  | 0.79523     | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp                    |  0.000470399 | 0.0290963  | 0.987101    | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp                    |  0.00104142  | 0.0295944  | 0.971929    | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp                    |  0.00624144  | 0.0290553  | 0.829916    | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp                     | -0.0348278   | 0.0311942  | 0.264227    | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp                     | -0.0492156   | 0.0300702  | 0.101709    | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp                     | -0.0206679   | 0.030765   | 0.501718    | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp                     | -0.0479046   | 0.0305449  | 0.116818    | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                       |  0.0404306   | 0.0117735  | 0.000595789 | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                       |  0.0349618   | 0.0117053  | 0.00282206  | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                       |  0.0146519   | 0.012086   | 0.22541     | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                        |  0.0431975   | 0.0125278  | 0.000565569 | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                        |  0.0740846   | 0.0124695  | 2.87073e-09 | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                        |  0.0700916   | 0.013032   | 7.5906e-08  | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                        |  0.0702154   | 0.0128469  | 4.66516e-08 | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_len                     | -0.00585875  | 0.0188117  | 0.755468    | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_len                     | -0.0357022   | 0.018808   | 0.0576764   | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_len                     |  0.0143242   | 0.0180642  | 0.427809    | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[1]:treated_X_len                      |  0.00321763  | 0.0191192  | 0.866354    | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[2]:treated_X_len                      | -0.0282638   | 0.0187491  | 0.131704    | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[3]:treated_X_len                      | -0.0188093   | 0.0189377  | 0.320615    | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[4]:treated_X_len                      | -0.0457062   | 0.0202606  | 0.0240859   | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-4]:disp_X_len                        |  2.13632e-05 | 0.00774892 | 0.9978      | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-3]:disp_X_len                        | -0.0050215   | 0.00695556 | 0.470339    | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-2]:disp_X_len                        |  0.00773224  | 0.00595145 | 0.193882    | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[1]:disp_X_len                         | -0.00510147  | 0.0068951  | 0.459388    | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[2]:disp_X_len                         | -0.0214354   | 0.00740208 | 0.00378498  | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[3]:disp_X_len                         | -0.0193423   | 0.00792225 | 0.0146336   | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[4]:disp_X_len                         | -0.0379549   | 0.0102157  | 0.000203412 | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-4]:tXdXlen                           |  0.0304319   | 0.0228526  | 0.182986    | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-3]:tXdXlen                           |  0.0619471   | 0.0228646  | 0.00674781  | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-2]:tXdXlen                           | -0.00716293  | 0.0216516  | 0.740778    | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[1]:tXdXlen                            |  0.0206159   | 0.0235512  | 0.381384    | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[2]:tXdXlen                            |  0.0423764   | 0.0235219  | 0.0716268   | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[3]:tXdXlen                            |  0.0248271   | 0.0235429  | 0.291643    | 95986 | 0.00204338  |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[4]:tXdXlen                            |  0.0652651   | 0.0247234  | 0.00830102  | 95986 | 0.00204338  |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[-4]:treated                           | -0.0235038   | 0.0196746  | 0.232247    | 95986 | 0.00124376  |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[-3]:treated                           | -0.0160061   | 0.0199402  | 0.422156    | 95986 | 0.00124376  |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[-2]:treated                           | -0.0363034   | 0.0206919  | 0.0793641   | 95986 | 0.00124376  |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[1]:treated                            |  0.0278954   | 0.0205781  | 0.175246    | 95986 | 0.00124376  |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[2]:treated                            |  0.000666795 | 0.0199051  | 0.973277    | 95986 | 0.00124376  |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[3]:treated                            | -0.0233088   | 0.0204724  | 0.254903    | 95986 | 0.00124376  |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[4]:treated                            | -0.00313598  | 0.020724   | 0.879724    | 95986 | 0.00124376  |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score                   |  0.0364139   | 0.0412206  | 0.377035    | 95986 | 0.00124376  |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score                   |  0.0377477   | 0.0415762  | 0.363932    | 95986 | 0.00124376  |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score                   |  0.0340976   | 0.0424107  | 0.421414    | 95986 | 0.00124376  |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score                    |  0.00587134  | 0.0427168  | 0.890678    | 95986 | 0.00124376  |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score                    | -0.0326024   | 0.04252    | 0.443236    | 95986 | 0.00124376  |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score                    | -0.0114022   | 0.0429683  | 0.790731    | 95986 | 0.00124376  |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score                    | -0.049506    | 0.0435608  | 0.255769    | 95986 | 0.00124376  |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered        |  0.0745606   | 0.0181196  | 3.88722e-05 | 95986 | 0.00124376  |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered        |  0.0595512   | 0.0181989  | 0.00106866  | 95986 | 0.00124376  |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered        |  0.0340838   | 0.0189497  | 0.0720878   | 95986 | 0.00124376  |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered         |  0.068576    | 0.0187902  | 0.000263288 | 95986 | 0.00124376  |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered         |  0.112847    | 0.0190582  | 3.24428e-09 | 95986 | 0.00124376  |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered         |  0.107744    | 0.0198152  | 5.46264e-08 | 95986 | 0.00124376  |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered         |  0.103559    | 0.019428   | 9.89613e-08 | 95986 | 0.00124376  |

## Pre-trend Joint Tests
| spec                             | test                                            |   n_restrictions |   statistic |     pvalue |     n |
|:---------------------------------|:------------------------------------------------|-----------------:|------------:|-----------:|------:|
| event_att                        | pretrend_att_joint_zero                         |                3 |     4.78338 | 0.188364   | 95986 |
| event_binary_B                   | pretrend_baseline_joint_zero                    |                3 |     2.46833 | 0.481042   | 95986 |
| event_binary_B                   | pretrend_displacement_joint_zero                |                3 |     1.02218 | 0.795886   | 95986 |
| event_binary_B_pre_novelty_split | pretrend_displacement_lower_group_joint_zero    |                3 |     1.17012 | 0.76018    | 95986 |
| event_binary_B_pre_novelty_split | pretrend_displacement_high_increment_joint_zero |                3 |     2.15691 | 0.540486   | 95986 |
| event_binary_D                   | pretrend_length_displacement_joint_zero         |                3 |    11.5604  | 0.00905121 | 95986 |
| event_binary_D                   | pretrend_length_baseline_joint_zero             |                3 |     8.03219 | 0.045351   | 95986 |
| event_score_C                    | pretrend_score_baseline_joint_zero              |                3 |     3.306   | 0.346809   | 95986 |
| event_score_C                    | pretrend_score_slope_joint_zero                 |                3 |     1.09283 | 0.778805   | 95986 |