# Displacement Effect Estimation Summary

- Sample rows: 115,688
- Unique members: 14,461
- Unique closures: 18
- Event FE units: 14,461
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=false
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Model type: DDD
- Event-study reference period: -1
- Pre-novelty heterogeneity: collapsed DDD includes post×(treatment, displacement)×high-pre split
- Customer median split: False


## Binary Specs
| spec                               | term                                     |     n |   r2_within |       coef |         se |    pvalue |
|:-----------------------------------|:-----------------------------------------|------:|------------:|-----------:|-----------:|----------:|
| binary_collapsed                   | post_X_treated                           | 44508 |  0.00877777 |  0.0417019 | 0.0173799  | 0.0164367 |
| binary_collapsed                   | post_X_disp                              | 44508 |  0.00877777 |  0.127856  | 0.00937762 | 0         |
| binary_collapsed                   | post_X_treated_X_disp                    | 44508 |  0.00877777 | -0.0535877 | 0.0223137  | 0.0163416 |
| binary_collapsed_pre_novelty_split | post_X_treated                           | 44508 |  0.0878764  |  0.412424  | 0.0194017  | 0         |
| binary_collapsed_pre_novelty_split | post_X_disp                              | 44508 |  0.0878764  |  0.211791  | 0.00902692 | 0         |
| binary_collapsed_pre_novelty_split | post_X_treated_X_disp                    | 44508 |  0.0878764  | -0.40986   | 0.0231408  | 0         |
| binary_collapsed_pre_novelty_split | post_X_treated_X_novelty_pre_high        | 44508 |  0.0878764  | -0.698239  | 0.0229241  | 0         |
| binary_collapsed_pre_novelty_split | post_X_disp_X_novelty_pre_high           | 44508 |  0.0878764  | -0.556319  | 0.0136762  | 0         |
| binary_collapsed_pre_novelty_split | post_X_treated_X_disp_X_novelty_pre_high | 44508 |  0.0878764  |  0.738466  | 0.0368481  | 0         |

## Score Spec
| spec            | term                   |     n |   r2_within |       coef |        se |    pvalue |
|:----------------|:-----------------------|------:|------------:|-----------:|----------:|----------:|
| score_collapsed | post_X_treated         | 44508 |   0.0101833 |  0.0252347 | 0.0144677 | 0.0811508 |
| score_collapsed | post_X_score           | 44508 |   0.0101833 |  0.212038  | 0.0137091 | 0         |
| score_collapsed | post_X_treated_X_score | 44508 |   0.0101833 | -0.0441926 | 0.0322615 | 0.17077   |

## Event-study Specs
| spec                             | term                                                                     |         coef |         se |      pvalue |     n |   r2_within |
|:---------------------------------|:-------------------------------------------------------------------------|-------------:|-----------:|------------:|------:|------------:|
| event_att                        | C(rel_t, contr.treatment(base=-1))[-4]:treated                           | -0.0215067   | 0.0153438  | 0.161047    | 44508 | 0.000349939 |
| event_att                        | C(rel_t, contr.treatment(base=-1))[-3]:treated                           | -0.00797874  | 0.0151527  | 0.598513    | 44508 | 0.000349939 |
| event_att                        | C(rel_t, contr.treatment(base=-1))[-2]:treated                           | -0.0488234   | 0.0140973  | 0.000535595 | 44508 | 0.000349939 |
| event_att                        | C(rel_t, contr.treatment(base=-1))[1]:treated                            |  0.00252228  | 0.0197037  | 0.898143    | 44508 | 0.000349939 |
| event_att                        | C(rel_t, contr.treatment(base=-1))[2]:treated                            | -0.00533878  | 0.0196942  | 0.786331    | 44508 | 0.000349939 |
| event_att                        | C(rel_t, contr.treatment(base=-1))[3]:treated                            | -0.0250554   | 0.0197416  | 0.204407    | 44508 | 0.000349939 |
| event_att                        | C(rel_t, contr.treatment(base=-1))[4]:treated                            | -0.0140898   | 0.0195061  | 0.470106    | 44508 | 0.000349939 |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[-4]:treated                           | -0.0403701   | 0.0243706  | 0.0976479   | 44508 | 0.0113472   |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[-3]:treated                           | -0.0278573   | 0.0243725  | 0.253072    | 44508 | 0.0113472   |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[-2]:treated                           | -0.0663274   | 0.0243317  | 0.00642134  | 44508 | 0.0113472   |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[1]:treated                            |  0.0022172   | 0.0310284  | 0.943035    | 44508 | 0.0113472   |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[2]:treated                            |  0.0249661   | 0.028999   | 0.389297    | 44508 | 0.0113472   |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[3]:treated                            | -0.0081747   | 0.0304752  | 0.788519    | 44508 | 0.0113472   |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[4]:treated                            |  0.0159854   | 0.0300882  | 0.595232    | 44508 | 0.0113472   |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp                    |  0.0371192   | 0.0309492  | 0.230415    | 44508 | 0.0113472   |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp                    |  0.0365283   | 0.0307685  | 0.235175    | 44508 | 0.0113472   |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp                    |  0.0235435   | 0.0295144  | 0.425065    | 44508 | 0.0113472   |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp                     |  0.00552448  | 0.0394123  | 0.888527    | 44508 | 0.0113472   |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp                     | -0.0530083   | 0.039068   | 0.174865    | 44508 | 0.0113472   |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp                     | -0.0257023   | 0.0393032  | 0.513158    | 44508 | 0.0113472   |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp                     | -0.0547822   | 0.0388768  | 0.158826    | 44508 | 0.0113472   |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                       |  0.077674    | 0.012336   | 3.15902e-10 | 44508 | 0.0113472   |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                       |  0.0625661   | 0.012213   | 3.0588e-07  | 44508 | 0.0113472   |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                       |  0.0102697   | 0.0124138  | 0.408094    | 44508 | 0.0113472   |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                        |  0.12441     | 0.0159689  | 7.32747e-15 | 44508 | 0.0113472   |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                        |  0.191774    | 0.0163528  | 0           | 44508 | 0.0113472   |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                        |  0.178088    | 0.016795   | 0           | 44508 | 0.0113472   |
| event_binary_B                   | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                        |  0.177445    | 0.0164836  | 0           | 44508 | 0.0113472   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-4]:treated                           |  0.024203    | 0.0295445  | 0.412686    | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-3]:treated                           |  0.0271932   | 0.0305052  | 0.372718    | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-2]:treated                           | -0.0402379   | 0.0316704  | 0.203925    | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[1]:treated                            |  0.438219    | 0.0381809  | 0           | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[2]:treated                            |  0.400079    | 0.0369132  | 0           | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[3]:treated                            |  0.401038    | 0.0374853  | 0           | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[4]:treated                            |  0.432964    | 0.0361771  | 0           | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp                    | -0.0153651   | 0.0363568  | 0.67258     | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp                    | -0.0162838   | 0.0370602  | 0.660389    | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp                    |  0.00435442  | 0.0366587  | 0.90545     | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp                     | -0.419081    | 0.0458251  | 0           | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp                     | -0.396856    | 0.0452506  | 0           | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp                     | -0.415018    | 0.0450751  | 0           | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp                     | -0.45195     | 0.0436937  | 0           | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                       |  0.0957819   | 0.0125464  | 2.4647e-14  | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                       |  0.0743074   | 0.0123916  | 2.07804e-09 | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                       |  0.0123797   | 0.0125825  | 0.325196    | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                        |  0.211279    | 0.0158829  | 0           | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                        |  0.292133    | 0.016321   | 0           | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                        |  0.272482    | 0.0166568  | 0           | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                        |  0.266832    | 0.0163724  | 0           | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_novelty_pre_high        | -0.0211028   | 0.0335655  | 0.529554    | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_novelty_pre_high        | -0.0347178   | 0.034517   | 0.314524    | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_novelty_pre_high        | -0.0145759   | 0.0350116  | 0.677187    | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[1]:treated_X_novelty_pre_high         | -0.738197    | 0.0466079  | 0           | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[2]:treated_X_novelty_pre_high         | -0.660841    | 0.0443208  | 0           | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[3]:treated_X_novelty_pre_high         | -0.722683    | 0.0451774  | 0           | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[4]:treated_X_novelty_pre_high         | -0.735591    | 0.0439322  | 0           | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-4]:disp_X_novelty_pre_high           | -0.0821772   | 0.0143641  | 1.08643e-08 | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-3]:disp_X_novelty_pre_high           | -0.0611578   | 0.014199   | 1.66754e-05 | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-2]:disp_X_novelty_pre_high           | -0.0478836   | 0.0129627  | 0.000221847 | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[1]:disp_X_novelty_pre_high            | -0.541332    | 0.0241936  | 0           | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[2]:disp_X_novelty_pre_high            | -0.63194     | 0.0245536  | 0           | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[3]:disp_X_novelty_pre_high            | -0.633012    | 0.0265826  | 0           | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[4]:disp_X_novelty_pre_high            | -0.617136    | 0.026802   | 0           | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp_X_novelty_pre_high |  0.0487324   | 0.0466702  | 0.296421    | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp_X_novelty_pre_high |  0.0733722   | 0.046948   | 0.118119    | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp_X_novelty_pre_high |  0.0585136   | 0.0456269  | 0.199716    | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp_X_novelty_pre_high  |  0.807606    | 0.0714504  | 0           | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp_X_novelty_pre_high  |  0.697137    | 0.0705757  | 0           | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp_X_novelty_pre_high  |  0.820748    | 0.0699472  | 0           | 44508 | 0.0914114   |
| event_binary_B_pre_novelty_split | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp_X_novelty_pre_high  |  0.812805    | 0.073035   | 0           | 44508 | 0.0914114   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-4]:treated                           | -0.0391147   | 0.0245476  | 0.111094    | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-3]:treated                           | -0.0255985   | 0.0247191  | 0.300423    | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-2]:treated                           | -0.0656451   | 0.0248254  | 0.00819815  | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[1]:treated                            |  0.00274665  | 0.0318741  | 0.931331    | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[2]:treated                            |  0.0250066   | 0.0290845  | 0.389922    | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[3]:treated                            | -0.00691113  | 0.0306215  | 0.821442    | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[4]:treated                            |  0.0138589   | 0.0301902  | 0.646205    | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp                    |  0.0264374   | 0.0321384  | 0.410746    | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp                    |  0.026567    | 0.0317529  | 0.402791    | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp                    |  0.0133791   | 0.0305404  | 0.661338    | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp                     | -0.00458967  | 0.0410997  | 0.911086    | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp                     | -0.0651665   | 0.0391506  | 0.0960393   | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp                     | -0.0260163   | 0.0398921  | 0.514308    | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp                     | -0.0555927   | 0.0397219  | 0.161676    | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                       |  0.0787298   | 0.0123153  | 1.69353e-10 | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                       |  0.0639349   | 0.0121935  | 1.60589e-07 | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                       |  0.0115805   | 0.012376   | 0.34944     | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                        |  0.124771    | 0.015929   | 5.32907e-15 | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                        |  0.192912    | 0.0162824  | 0           | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                        |  0.178385    | 0.0167672  | 0           | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                        |  0.177973    | 0.0164609  | 0           | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_len                     | -0.0107399   | 0.0207328  | 0.604458    | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_len                     | -0.0206486   | 0.0191332  | 0.280521    | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_len                     | -0.000211945 | 0.0185412  | 0.99088     | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[1]:treated_X_len                      | -0.0190024   | 0.0245682  | 0.439269    | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[2]:treated_X_len                      | -0.0324735   | 0.0242865  | 0.181217    | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[3]:treated_X_len                      | -0.0475819   | 0.0240098  | 0.0475297   | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[4]:treated_X_len                      | -0.0688379   | 0.0256692  | 0.00733497  | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-4]:disp_X_len                        | -0.00929858  | 0.00937755 | 0.321424    | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-3]:disp_X_len                        | -0.0114531   | 0.00840499 | 0.173021    | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-2]:disp_X_len                        | -0.00884882  | 0.00714203 | 0.21538     | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[1]:disp_X_len                         | -0.0091598   | 0.0103003  | 0.373876    | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[2]:disp_X_len                         | -0.0233305   | 0.0115626  | 0.043642    | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[3]:disp_X_len                         | -0.0219217   | 0.0116394  | 0.0596714   | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[4]:disp_X_len                         | -0.0558382   | 0.014626   | 0.000135418 | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-4]:tXdXlen                           |  0.0376813   | 0.0263843  | 0.153271    | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-3]:tXdXlen                           |  0.0441936   | 0.0250237  | 0.0774113   | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[-2]:tXdXlen                           |  0.0267775   | 0.0236937  | 0.258436    | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[1]:tXdXlen                            |  0.0401197   | 0.0323019  | 0.214255    | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[2]:tXdXlen                            |  0.0695333   | 0.0331665  | 0.0360609   | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[3]:tXdXlen                            |  0.0507369   | 0.0321353  | 0.114398    | 44508 | 0.0122925   |
| event_binary_D                   | C(rel_t, contr.treatment(base=-1))[4]:tXdXlen                            |  0.0929619   | 0.0336864  | 0.00579623  | 44508 | 0.0122925   |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[-4]:treated                           | -0.0325207   | 0.0210879  | 0.123066    | 44508 | 0.0128779   |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[-3]:treated                           | -0.00949206  | 0.020554   | 0.644226    | 44508 | 0.0128779   |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[-2]:treated                           | -0.0580926   | 0.0212075  | 0.00616777  | 44508 | 0.0128779   |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[1]:treated                            |  0.00358601  | 0.0259815  | 0.890226    | 44508 | 0.0128779   |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[2]:treated                            |  0.00542326  | 0.0244018  | 0.824124    | 44508 | 0.0128779   |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[3]:treated                            | -0.0138684   | 0.0253525  | 0.584372    | 44508 | 0.0128779   |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[4]:treated                            |  0.00561072  | 0.0252763  | 0.824337    | 44508 | 0.0128779   |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score                   |  0.0572158   | 0.0496038  | 0.248748    | 44508 | 0.0128779   |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score                   |  0.0151371   | 0.0484062  | 0.754507    | 44508 | 0.0128779   |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score                   |  0.0311256   | 0.048803   | 0.52363     | 44508 | 0.0128779   |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score                    |  0.0196699   | 0.0588412  | 0.738169    | 44508 | 0.0128779   |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score                    | -0.0194825   | 0.0583386  | 0.738419    | 44508 | 0.0128779   |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score                    | -0.0165509   | 0.0578918  | 0.774965    | 44508 | 0.0128779   |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score                    | -0.0694228   | 0.0579263  | 0.23076     | 44508 | 0.0128779   |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered        |  0.137016    | 0.0196857  | 3.59091e-12 | 44508 | 0.0128779   |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered        |  0.104888    | 0.0196564  | 9.68487e-08 | 44508 | 0.0128779   |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered        |  0.0190651   | 0.0202414  | 0.346271    | 44508 | 0.0128779   |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered         |  0.220797    | 0.0238392  | 0           | 44508 | 0.0128779   |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered         |  0.319228    | 0.0248501  | 0           | 44508 | 0.0128779   |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered         |  0.304437    | 0.0252483  | 0           | 44508 | 0.0128779   |
| event_score_C                    | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered         |  0.287859    | 0.024795   | 0           | 44508 | 0.0128779   |

## Pre-trend Joint Tests
| spec                             | test                                            |   n_restrictions |   statistic |     pvalue |     n |
|:---------------------------------|:------------------------------------------------|-----------------:|------------:|-----------:|------:|
| event_att                        | pretrend_att_joint_zero                         |                3 |   15.2703   | 0.00159965 | 44508 |
| event_binary_B                   | pretrend_baseline_joint_zero                    |                3 |    7.73043  | 0.0519241  | 44508 |
| event_binary_B                   | pretrend_displacement_joint_zero                |                3 |    1.81204  | 0.612319   | 44508 |
| event_binary_B_pre_novelty_split | pretrend_displacement_lower_group_joint_zero    |                3 |    0.501772 | 0.918502   | 44508 |
| event_binary_B_pre_novelty_split | pretrend_displacement_high_increment_joint_zero |                3 |    2.65605  | 0.447747   | 44508 |
| event_binary_D                   | pretrend_length_displacement_joint_zero         |                3 |    3.38274  | 0.336292   | 44508 |
| event_binary_D                   | pretrend_length_baseline_joint_zero             |                3 |    1.51335  | 0.679193   | 44508 |
| event_score_C                    | pretrend_score_baseline_joint_zero              |                3 |    9.11486  | 0.0278021  | 44508 |
| event_score_C                    | pretrend_score_slope_joint_zero                 |                3 |    1.54015  | 0.673035   | 44508 |