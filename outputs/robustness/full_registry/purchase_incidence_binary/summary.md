# Displacement Effect Estimation Summary

- Sample rows: 358,864
- Unique members: 44,858
- Unique closures: 22
- Event FE units: 44,858
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=false
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Model type: DDD


## Binary Specs
| spec                   | term                  |      n |   r2_within |        coef |         se |    pvalue |
|:-----------------------|:----------------------|-------:|------------:|------------:|-----------:|----------:|
| binary_collapsed       | post_X_treated        | 358864 |   0.0105927 |  0.0114987  | 0.00423184 | 0.0065866 |
| binary_collapsed       | post_X_disp           | 358864 |   0.0105927 | -0.166985   | 0.00393568 | 0         |
| binary_collapsed       | post_X_treated_X_disp | 358864 |   0.0105927 | -0.00065215 | 0.00914538 | 0.943152  |
| binary_collapsed_logit | post_X_treated        | 358864 | nan         |  0.0408207  | 0.0248961  | 0.10108   |
| binary_collapsed_logit | post_X_disp           | 358864 | nan         |  1.64236    | 0.0178159  | 0         |
| binary_collapsed_logit | post_X_treated_X_disp | 358864 | nan         |  0.00950213 | 0.0421881  | 0.821798  |

## Score Spec
| spec            | term                   |      n |   r2_within |        coef |         se |     pvalue |
|:----------------|:-----------------------|-------:|------------:|------------:|-----------:|-----------:|
| score_collapsed | post_X_treated         | 358864 |   0.0159013 |  0.00970772 | 0.00374894 | 0.00961596 |
| score_collapsed | post_X_score           | 358864 |   0.0159013 | -0.287753   | 0.00514617 | 0          |
| score_collapsed | post_X_treated_X_score | 358864 |   0.0159013 |  0.00143147 | 0.0117169  | 0.902763   |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |      n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|-------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00142477  | 0.00692558 | 0.837006    | 358864 |  0.00011404 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00517528  | 0.006708   | 0.44041     | 358864 |  0.00011404 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00224052  | 0.00633514 | 0.723591    | 358864 |  0.00011404 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0126377   | 0.00616241 | 0.0402958   | 358864 |  0.00011404 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0041395   | 0.00638598 | 0.516848    | 358864 |  0.00011404 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0292823   | 0.00646318 | 5.89593e-06 | 358864 |  0.00011404 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00962918  | 0.00664828 | 0.14752     | 358864 |  0.00011404 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00563419  | 0.00781883 | 0.471165    | 358864 |  0.0153375  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00280326  | 0.00751209 | 0.709026    | 358864 |  0.0153375  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0144106   | 0.00694999 | 0.0381342   | 358864 |  0.0153375  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0148524   | 0.00682382 | 0.0295193   | 358864 |  0.0153375  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0123365   | 0.00707298 | 0.0811353   | 358864 |  0.0153375  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.02814     | 0.00718764 | 9.05176e-05 | 358864 |  0.0153375  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00878162  | 0.00730458 | 0.22929     | 358864 |  0.0153375  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             | -0.0180079   | 0.0163845  | 0.271738    | 358864 |  0.0153375  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             | -0.0130878   | 0.0159273  | 0.411241    | 358864 |  0.0153375  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.0371447   | 0.0151271  | 0.0140721   | 358864 |  0.0153375  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0161497   | 0.0148157  | 0.275704    | 358864 |  0.0153375  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.0381193   | 0.0152937  | 0.0126889   | 358864 |  0.0153375  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              | -0.00590112  | 0.0154195  | 0.70194     | 358864 |  0.0153375  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.0102263   | 0.0160529  | 0.524101    | 358864 |  0.0153375  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.0193396   | 0.00710594 | 0.00649889  | 358864 |  0.0153375  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.0460534   | 0.00680303 | 1.30775e-11 | 358864 |  0.0153375  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.178212    | 0.00649205 | 0           | 358864 |  0.0153375  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0884354   | 0.00649732 | 0           | 358864 |  0.0153375  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.107498    | 0.00671284 | 0           | 358864 |  0.0153375  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.12806     | 0.00679204 | 0           | 358864 |  0.0153375  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.139233    | 0.00689179 | 0           | 358864 |  0.0153375  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00556781  | 0.00786163 | 0.478809    | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00338773  | 0.00756464 | 0.654272    | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0119881   | 0.00696996 | 0.0854447   | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0157915   | 0.00686147 | 0.0213694   | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0119983   | 0.00710555 | 0.0913075   | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0281165   | 0.00722647 | 0.00010007  | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00811582  | 0.00735519 | 0.269854    | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.00451314  | 0.0185192  | 0.807464    | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0272386   | 0.0178833  | 0.127733    | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.00178802  | 0.0170021  | 0.916245    | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0193151   | 0.0168506  | 0.251696    | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.0166826   | 0.0171923  | 0.331877    | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.0179835   | 0.0175097  | 0.3044      | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.0157305   | 0.0181403  | 0.38586     | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.0122273   | 0.0072271  | 0.0906781   | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.0540164   | 0.00693324 | 6.66134e-15 | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.18844     | 0.00660955 | 0           | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0860227   | 0.00668536 | 0           | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.101108    | 0.00688512 | 0           | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.122483    | 0.00695737 | 0           | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.133717    | 0.00699826 | 0           | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_len              |  0.00290764  | 0.0072895  | 0.689983    | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_len              |  0.00783067  | 0.00695486 | 0.260202    | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_len              | -0.0169445   | 0.00621165 | 0.00637723  | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_len               |  0.0194144   | 0.00627232 | 0.00196764  | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_len               | -0.0120961   | 0.00644276 | 0.0604605   | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated_X_len               | -0.00246257  | 0.00653237 | 0.706191    | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated_X_len               | -0.00798961  | 0.0069177  | 0.248116    | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:disp_X_len                 | -0.0393189   | 0.00634319 | 5.74579e-10 | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:disp_X_len                 | -0.0412948   | 0.00593631 | 3.54095e-12 | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_X_len                 | -0.0447628   | 0.00552815 | 4.44089e-16 | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_X_len                  | -0.00737671  | 0.00562283 | 0.189554    | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_X_len                  | -0.0242689   | 0.00583345 | 3.18437e-05 | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:disp_X_len                  | -0.0214721   | 0.00599538 | 0.000342064 | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:disp_X_len                  | -0.0257433   | 0.00635356 | 5.09122e-05 | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:tXdXlen                    | -0.0121768   | 0.0143484  | 0.396079    | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:tXdXlen                    | -0.0428928   | 0.0138665  | 0.00198095  | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:tXdXlen                    | -0.0131734   | 0.0128966  | 0.307041    | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:tXdXlen                     | -0.0102471   | 0.0128748  | 0.426094    | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:tXdXlen                     | -0.00203723  | 0.0133583  | 0.878788    | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:tXdXlen                     | -0.0176876   | 0.0134829  | 0.189578    | 358864 |  0.0162128  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:tXdXlen                     | -0.0136745   | 0.0140782  | 0.331392    | 358864 |  0.0162128  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.000719344 | 0.00694261 | 0.917477    | 358864 |  0.0203044  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00620363  | 0.00671338 | 0.355455    | 358864 |  0.0203044  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00510492  | 0.00628448 | 0.41662     | 358864 |  0.0203044  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00937009  | 0.0061267  | 0.126176    | 358864 |  0.0203044  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.000647442 | 0.00633712 | 0.918625    | 358864 |  0.0203044  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0251664   | 0.00641946 | 8.85586e-05 | 358864 |  0.0203044  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00426219  | 0.00660559 | 0.518776    | 358864 |  0.0203044  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            | -0.00571514  | 0.0191468  | 0.76533     | 358864 |  0.0203044  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            | -0.0232121   | 0.0179109  | 0.19499     | 358864 |  0.0203044  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.0304006   | 0.017001   | 0.0737559   | 358864 |  0.0203044  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.0119135   | 0.0179946  | 0.507937    | 358864 |  0.0203044  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.0429965   | 0.0188463  | 0.0225279   | 358864 |  0.0203044  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.00794176  | 0.0188571  | 0.673644    | 358864 |  0.0203044  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             | -0.00598465  | 0.0196493  | 0.760693    | 358864 |  0.0203044  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.0221156   | 0.00849359 | 0.00922281  | 358864 |  0.0203044  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.0802576   | 0.00784686 | 0           | 358864 |  0.0203044  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.237694    | 0.0074084  | 0           | 358864 |  0.0203044  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.171827    | 0.00802797 | 0           | 358864 |  0.0203044  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.199505    | 0.00834798 | 0           | 358864 |  0.0203044  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.238395    | 0.00848048 | 0           | 358864 |  0.0203044  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.24616     | 0.00864592 | 0           | 358864 |  0.0203044  |

## Pre-trend Joint Tests
| spec           | test                                    |   n_restrictions |   statistic |     pvalue |      n |
|:---------------|:----------------------------------------|-----------------:|------------:|-----------:|-------:|
| event_att      | pretrend_att_joint_zero                 |                3 |     1.53924 | 0.673244   | 358864 |
| event_binary_B | pretrend_baseline_joint_zero            |                3 |     6.53929 | 0.0881259  | 358864 |
| event_binary_B | pretrend_displacement_joint_zero        |                3 |     6.4925  | 0.0899587  | 358864 |
| event_binary_D | pretrend_length_displacement_joint_zero |                3 |    10.9134  | 0.0122033  | 358864 |
| event_binary_D | pretrend_length_baseline_joint_zero     |                3 |    15.2589  | 0.00160821 | 358864 |
| event_score_C  | pretrend_score_baseline_joint_zero      |                3 |     3.04423 | 0.384856   | 358864 |
| event_score_C  | pretrend_score_slope_joint_zero         |                3 |     4.32068 | 0.228853   | 358864 |