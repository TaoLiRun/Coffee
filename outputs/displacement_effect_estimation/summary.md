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
- Pre-novelty heterogeneity: collapsed DDD includes post×(treatment, displacement)×high-pre split
- Customer median split: False


## Binary Specs
| spec                               | term                                     |     n |   r2_within |       coef |        se |    pvalue |
|:-----------------------------------|:-----------------------------------------|------:|------------:|-----------:|----------:|----------:|
| binary_collapsed                   | post_X_treated                           | 44508 |  0.00877777 |  0.0417019 | 0.0173799 | 0.0164368 |
| binary_collapsed                   | post_X_disp                              | 44508 |  0.00877777 |  0.127856  | 0.0093776 | 0         |
| binary_collapsed                   | post_X_treated_X_disp                    | 44508 |  0.00877777 | -0.0535877 | 0.0223137 | 0.0163417 |
| binary_collapsed_pre_novelty_split | post_X_treated                           | 44508 |  0.0878764  |  0.412424  | 0.0194017 | 0         |
| binary_collapsed_pre_novelty_split | post_X_disp                              | 44508 |  0.0878764  |  0.211791  | 0.0090269 | 0         |
| binary_collapsed_pre_novelty_split | post_X_treated_X_disp                    | 44508 |  0.0878764  | -0.40986   | 0.0231408 | 0         |
| binary_collapsed_pre_novelty_split | post_X_treated_X_novelty_pre_high        | 44508 |  0.0878764  | -0.698239  | 0.0229241 | 0         |
| binary_collapsed_pre_novelty_split | post_X_disp_X_novelty_pre_high           | 44508 |  0.0878764  | -0.556319  | 0.0136762 | 0         |
| binary_collapsed_pre_novelty_split | post_X_treated_X_disp_X_novelty_pre_high | 44508 |  0.0878764  |  0.738466  | 0.0368481 | 0         |

## Score Spec
| spec            | term                   |     n |   r2_within |       coef |        se |   pvalue |
|:----------------|:-----------------------|------:|------------:|-----------:|----------:|---------:|
| score_collapsed | post_X_treated         | 44508 |   0.0101833 |  0.0252347 | 0.0144678 | 0.081151 |
| score_collapsed | post_X_score           | 44508 |   0.0101833 |  0.212038  | 0.0137091 | 0        |
| score_collapsed | post_X_treated_X_score | 44508 |   0.0101833 | -0.0441926 | 0.0322616 | 0.17077  |

## Event-study Specs
| spec           | term                                 |         coef |         se |      pvalue |     n |   r2_within |
|:---------------|:-------------------------------------|-------------:|-----------:|------------:|------:|------------:|
| event_att      | rel_t::-4:treated                    | -0.0215067   | 0.0153438  | 0.161048    | 44508 | 0.000349939 |
| event_att      | rel_t::-3:treated                    | -0.00797874  | 0.0151527  | 0.598513    | 44508 | 0.000349939 |
| event_att      | rel_t::-2:treated                    | -0.0488234   | 0.0140973  | 0.000535595 | 44508 | 0.000349939 |
| event_att      | rel_t::1:treated                     |  0.00252228  | 0.0197037  | 0.898143    | 44508 | 0.000349939 |
| event_att      | rel_t::2:treated                     | -0.00533878  | 0.0196941  | 0.786331    | 44508 | 0.000349939 |
| event_att      | rel_t::3:treated                     | -0.0250554   | 0.0197416  | 0.204408    | 44508 | 0.000349939 |
| event_att      | rel_t::4:treated                     | -0.0140898   | 0.0195061  | 0.470106    | 44508 | 0.000349939 |
| event_binary_B | rel_t::-4:treated                    | -0.0403701   | 0.0243707  | 0.0976488   | 44508 | 0.0113472   |
| event_binary_B | rel_t::-3:treated                    | -0.0278573   | 0.0243726  | 0.253073    | 44508 | 0.0113472   |
| event_binary_B | rel_t::-2:treated                    | -0.0663274   | 0.0243317  | 0.00642136  | 44508 | 0.0113472   |
| event_binary_B | rel_t::1:treated                     |  0.00221721  | 0.0310284  | 0.943035    | 44508 | 0.0113472   |
| event_binary_B | rel_t::2:treated                     |  0.0249661   | 0.0289991  | 0.389298    | 44508 | 0.0113472   |
| event_binary_B | rel_t::3:treated                     | -0.00817469  | 0.0304753  | 0.78852     | 44508 | 0.0113472   |
| event_binary_B | rel_t::4:treated                     |  0.0159854   | 0.0300883  | 0.595233    | 44508 | 0.0113472   |
| event_binary_B | rel_t::-4:treated_X_disp             |  0.0371192   | 0.0309493  | 0.230415    | 44508 | 0.0113472   |
| event_binary_B | rel_t::-3:treated_X_disp             |  0.0365283   | 0.0307685  | 0.235176    | 44508 | 0.0113472   |
| event_binary_B | rel_t::-2:treated_X_disp             |  0.0235435   | 0.0295144  | 0.425066    | 44508 | 0.0113472   |
| event_binary_B | rel_t::1:treated_X_disp              |  0.00552447  | 0.0394124  | 0.888528    | 44508 | 0.0113472   |
| event_binary_B | rel_t::2:treated_X_disp              | -0.0530083   | 0.0390681  | 0.174867    | 44508 | 0.0113472   |
| event_binary_B | rel_t::3:treated_X_disp              | -0.0257023   | 0.0393033  | 0.513159    | 44508 | 0.0113472   |
| event_binary_B | rel_t::4:treated_X_disp              | -0.0547822   | 0.0388768  | 0.158827    | 44508 | 0.0113472   |
| event_binary_B | rel_t::-4:disp_binary                |  0.077674    | 0.012336   | 3.15836e-10 | 44508 | 0.0113472   |
| event_binary_B | rel_t::-3:disp_binary                |  0.0625661   | 0.0122129  | 3.05847e-07 | 44508 | 0.0113472   |
| event_binary_B | rel_t::-2:disp_binary                |  0.0102697   | 0.0124138  | 0.408094    | 44508 | 0.0113472   |
| event_binary_B | rel_t::1:disp_binary                 |  0.12441     | 0.0159688  | 7.32747e-15 | 44508 | 0.0113472   |
| event_binary_B | rel_t::2:disp_binary                 |  0.191774    | 0.0163526  | 0           | 44508 | 0.0113472   |
| event_binary_B | rel_t::3:disp_binary                 |  0.178088    | 0.0167948  | 0           | 44508 | 0.0113472   |
| event_binary_B | rel_t::4:disp_binary                 |  0.177445    | 0.0164835  | 0           | 44508 | 0.0113472   |
| event_binary_D | rel_t::-4:treated                    | -0.0391147   | 0.0245477  | 0.111095    | 44508 | 0.0122925   |
| event_binary_D | rel_t::-3:treated                    | -0.0255985   | 0.0247191  | 0.300424    | 44508 | 0.0122925   |
| event_binary_D | rel_t::-2:treated                    | -0.0656451   | 0.0248254  | 0.00819817  | 44508 | 0.0122925   |
| event_binary_D | rel_t::1:treated                     |  0.00274666  | 0.0318742  | 0.931331    | 44508 | 0.0122925   |
| event_binary_D | rel_t::2:treated                     |  0.0250066   | 0.0290846  | 0.389923    | 44508 | 0.0122925   |
| event_binary_D | rel_t::3:treated                     | -0.00691113  | 0.0306216  | 0.821443    | 44508 | 0.0122925   |
| event_binary_D | rel_t::4:treated                     |  0.0138589   | 0.0301903  | 0.646205    | 44508 | 0.0122925   |
| event_binary_D | rel_t::-4:treated_X_disp             |  0.0264374   | 0.0321384  | 0.410747    | 44508 | 0.0122925   |
| event_binary_D | rel_t::-3:treated_X_disp             |  0.026567    | 0.031753   | 0.402792    | 44508 | 0.0122925   |
| event_binary_D | rel_t::-2:treated_X_disp             |  0.0133791   | 0.0305404  | 0.661338    | 44508 | 0.0122925   |
| event_binary_D | rel_t::1:treated_X_disp              | -0.00458968  | 0.0410999  | 0.911086    | 44508 | 0.0122925   |
| event_binary_D | rel_t::2:treated_X_disp              | -0.0651665   | 0.0391508  | 0.0960405   | 44508 | 0.0122925   |
| event_binary_D | rel_t::3:treated_X_disp              | -0.0260163   | 0.0398922  | 0.514309    | 44508 | 0.0122925   |
| event_binary_D | rel_t::4:treated_X_disp              | -0.0555927   | 0.0397219  | 0.161676    | 44508 | 0.0122925   |
| event_binary_D | rel_t::-4:disp_binary                |  0.0787298   | 0.0123152  | 1.69317e-10 | 44508 | 0.0122925   |
| event_binary_D | rel_t::-3:disp_binary                |  0.0639349   | 0.0121935  | 1.60571e-07 | 44508 | 0.0122925   |
| event_binary_D | rel_t::-2:disp_binary                |  0.0115805   | 0.012376   | 0.349439    | 44508 | 0.0122925   |
| event_binary_D | rel_t::1:disp_binary                 |  0.124771    | 0.0159288  | 5.32907e-15 | 44508 | 0.0122925   |
| event_binary_D | rel_t::2:disp_binary                 |  0.192912    | 0.0162822  | 0           | 44508 | 0.0122925   |
| event_binary_D | rel_t::3:disp_binary                 |  0.178385    | 0.016767   | 0           | 44508 | 0.0122925   |
| event_binary_D | rel_t::4:disp_binary                 |  0.177973    | 0.0164608  | 0           | 44508 | 0.0122925   |
| event_binary_D | rel_t::-4:treated_X_len              | -0.0107399   | 0.0207328  | 0.604458    | 44508 | 0.0122925   |
| event_binary_D | rel_t::-3:treated_X_len              | -0.0206486   | 0.0191332  | 0.280521    | 44508 | 0.0122925   |
| event_binary_D | rel_t::-2:treated_X_len              | -0.000211945 | 0.0185412  | 0.99088     | 44508 | 0.0122925   |
| event_binary_D | rel_t::1:treated_X_len               | -0.0190024   | 0.0245682  | 0.43927     | 44508 | 0.0122925   |
| event_binary_D | rel_t::2:treated_X_len               | -0.0324735   | 0.0242865  | 0.181217    | 44508 | 0.0122925   |
| event_binary_D | rel_t::3:treated_X_len               | -0.0475819   | 0.0240098  | 0.0475299   | 44508 | 0.0122925   |
| event_binary_D | rel_t::4:treated_X_len               | -0.0688379   | 0.0256692  | 0.00733499  | 44508 | 0.0122925   |
| event_binary_D | rel_t::-4:disp_X_len                 | -0.00929858  | 0.00937755 | 0.321424    | 44508 | 0.0122925   |
| event_binary_D | rel_t::-3:disp_X_len                 | -0.0114531   | 0.00840499 | 0.173021    | 44508 | 0.0122925   |
| event_binary_D | rel_t::-2:disp_X_len                 | -0.00884882  | 0.00714204 | 0.21538     | 44508 | 0.0122925   |
| event_binary_D | rel_t::1:disp_X_len                  | -0.0091598   | 0.0103003  | 0.373876    | 44508 | 0.0122925   |
| event_binary_D | rel_t::2:disp_X_len                  | -0.0233305   | 0.0115626  | 0.043642    | 44508 | 0.0122925   |
| event_binary_D | rel_t::3:disp_X_len                  | -0.0219217   | 0.0116394  | 0.0596714   | 44508 | 0.0122925   |
| event_binary_D | rel_t::4:disp_X_len                  | -0.0558382   | 0.014626   | 0.000135417 | 44508 | 0.0122925   |
| event_binary_D | rel_t::-4:tXdXlen                    |  0.0376813   | 0.0263843  | 0.15327     | 44508 | 0.0122925   |
| event_binary_D | rel_t::-3:tXdXlen                    |  0.0441936   | 0.0250237  | 0.0774112   | 44508 | 0.0122925   |
| event_binary_D | rel_t::-2:tXdXlen                    |  0.0267775   | 0.0236937  | 0.258436    | 44508 | 0.0122925   |
| event_binary_D | rel_t::1:tXdXlen                     |  0.0401197   | 0.032302   | 0.214256    | 44508 | 0.0122925   |
| event_binary_D | rel_t::2:tXdXlen                     |  0.0695333   | 0.0331665  | 0.036061    | 44508 | 0.0122925   |
| event_binary_D | rel_t::3:tXdXlen                     |  0.0507369   | 0.0321353  | 0.114399    | 44508 | 0.0122925   |
| event_binary_D | rel_t::4:tXdXlen                     |  0.0929619   | 0.0336864  | 0.00579622  | 44508 | 0.0122925   |
| event_score_C  | rel_t::-4:treated                    | -0.0325207   | 0.021088   | 0.123068    | 44508 | 0.0128779   |
| event_score_C  | rel_t::-3:treated                    | -0.00949206  | 0.020554   | 0.644226    | 44508 | 0.0128779   |
| event_score_C  | rel_t::-2:treated                    | -0.0580926   | 0.0212075  | 0.0061678   | 44508 | 0.0128779   |
| event_score_C  | rel_t::1:treated                     |  0.00358601  | 0.0259815  | 0.890226    | 44508 | 0.0128779   |
| event_score_C  | rel_t::2:treated                     |  0.00542326  | 0.0244018  | 0.824125    | 44508 | 0.0128779   |
| event_score_C  | rel_t::3:treated                     | -0.0138684   | 0.0253526  | 0.584374    | 44508 | 0.0128779   |
| event_score_C  | rel_t::4:treated                     |  0.00561072  | 0.0252763  | 0.824337    | 44508 | 0.0128779   |
| event_score_C  | rel_t::-4:treated_X_score            |  0.0572158   | 0.049604   | 0.24875     | 44508 | 0.0128779   |
| event_score_C  | rel_t::-3:treated_X_score            |  0.0151371   | 0.0484064  | 0.754508    | 44508 | 0.0128779   |
| event_score_C  | rel_t::-2:treated_X_score            |  0.0311256   | 0.048803   | 0.523631    | 44508 | 0.0128779   |
| event_score_C  | rel_t::1:treated_X_score             |  0.0196699   | 0.0588413  | 0.738169    | 44508 | 0.0128779   |
| event_score_C  | rel_t::2:treated_X_score             | -0.0194826   | 0.0583389  | 0.73842     | 44508 | 0.0128779   |
| event_score_C  | rel_t::3:treated_X_score             | -0.0165509   | 0.057892   | 0.774966    | 44508 | 0.0128779   |
| event_score_C  | rel_t::4:treated_X_score             | -0.0694228   | 0.0579263  | 0.230761    | 44508 | 0.0128779   |
| event_score_C  | rel_t::-4:displacement_prob_centered |  0.137016    | 0.0196856  | 3.59002e-12 | 44508 | 0.0128779   |
| event_score_C  | rel_t::-3:displacement_prob_centered |  0.104888    | 0.0196563  | 9.68368e-08 | 44508 | 0.0128779   |
| event_score_C  | rel_t::-2:displacement_prob_centered |  0.0190651   | 0.0202414  | 0.346271    | 44508 | 0.0128779   |
| event_score_C  | rel_t::1:displacement_prob_centered  |  0.220797    | 0.023839   | 0           | 44508 | 0.0128779   |
| event_score_C  | rel_t::2:displacement_prob_centered  |  0.319228    | 0.0248498  | 0           | 44508 | 0.0128779   |
| event_score_C  | rel_t::3:displacement_prob_centered  |  0.304437    | 0.0252481  | 0           | 44508 | 0.0128779   |
| event_score_C  | rel_t::4:displacement_prob_centered  |  0.287859    | 0.0247949  | 0           | 44508 | 0.0128779   |

## Pre-trend Joint Tests
| spec           | test                                    |   n_restrictions |   statistic |   pvalue |     n |
|:---------------|:----------------------------------------|-----------------:|------------:|---------:|------:|
| event_att      | pretrend_att_joint_zero                 |                0 |         nan |      nan | 44508 |
| event_binary_B | pretrend_baseline_joint_zero            |                0 |         nan |      nan | 44508 |
| event_binary_B | pretrend_displacement_joint_zero        |                0 |         nan |      nan | 44508 |
| event_binary_D | pretrend_length_displacement_joint_zero |                0 |         nan |      nan | 44508 |
| event_binary_D | pretrend_length_baseline_joint_zero     |                0 |         nan |      nan | 44508 |
| event_score_C  | pretrend_score_baseline_joint_zero      |                0 |         nan |      nan | 44508 |
| event_score_C  | pretrend_score_slope_joint_zero         |                0 |         nan |      nan | 44508 |