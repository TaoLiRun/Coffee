# Displacement Effect Estimation Summary

- Sample rows: 358,864
- Unique members: 44,858
- Unique closures: 22
- Event FE units: 44,858
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]

## Binary Specs
| spec             | term                  |      n |   r2_within |         coef |          se |    pvalue |
|:-----------------|:----------------------|-------:|------------:|-------------:|------------:|----------:|
| binary_collapsed | post_X_treated        | 358864 |   0.0121649 |  0.000808555 | 0.000641836 | 0.207765  |
| binary_collapsed | post_X_disp           | 358864 |   0.0121649 | -0.033527    | 0.00107463  | 0         |
| binary_collapsed | post_X_treated_X_disp | 358864 |   0.0121649 |  0.00516862  | 0.00240616  | 0.0317127 |

## Score Spec
| spec            | term                   |      n |   r2_within |        coef |          se |     pvalue |
|:----------------|:-----------------------|-------:|------------:|------------:|------------:|-----------:|
| score_collapsed | post_X_treated         | 358864 |   0.0179496 |  0.00205062 | 0.000784427 | 0.00894779 |
| score_collapsed | post_X_score           | 358864 |   0.0179496 | -0.057871   | 0.00161447  | 0          |
| score_collapsed | post_X_treated_X_score | 358864 |   0.0179496 |  0.00719398 | 0.00362643  | 0.0472879  |

## Event-study Specs
| spec           | term                                                              |         coef |          se |      pvalue |      n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|------------:|------------:|-------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00043436  | 0.00121332  | 0.72035     | 358864 | 0.000152819 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.000282038 | 0.00116449  | 0.808628    | 358864 | 0.000152819 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.000313581 | 0.00102194  | 0.75896     | 358864 | 0.000152819 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00254148  | 0.00103261  | 0.0138506   | 358864 | 0.000152819 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.000163434 | 0.00111593  | 0.883563    | 358864 | 0.000152819 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00623115  | 0.00116723  | 9.42259e-08 | 358864 | 0.000152819 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00175002  | 0.00115576  | 0.129987    | 358864 | 0.000152819 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00104412  | 0.00101767  | 0.304903    | 358864 | 0.0155148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  3.79213e-05 | 0.000933044 | 0.967581    | 358864 | 0.0155148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00166852  | 0.000801482 | 0.0373666   | 358864 | 0.0155148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.000455712 | 0.000808123 | 0.572815    | 358864 | 0.0155148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  8.6243e-05  | 0.000915792 | 0.924972    | 358864 | 0.0155148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00344354  | 0.00096636  | 0.000366444 | 358864 | 0.0155148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.000120955 | 0.00092423  | 0.895878    | 358864 | 0.0155148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.00495015  | 0.00362285  | 0.171829    | 358864 | 0.0155148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             | -0.00227389  | 0.00353218  | 0.519732    | 358864 | 0.0155148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.00650637  | 0.00310781  | 0.0363052   | 358864 | 0.0155148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.00626645  | 0.00313065  | 0.0453289   | 358864 | 0.0155148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.00104825  | 0.00332462  | 0.752536    | 358864 | 0.0155148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.0083888   | 0.0034633   | 0.0154309   | 358864 | 0.0155148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.00358536  | 0.00347389  | 0.302036    | 358864 | 0.0155148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.0140706   | 0.00169649  | 0           | 358864 | 0.0155148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                | -0.00219335  | 0.00163197  | 0.178959    | 358864 | 0.0155148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0190299   | 0.00146944  | 0           | 358864 | 0.0155148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0300472   | 0.00144043  | 0           | 358864 | 0.0155148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0282388   | 0.00157084  | 0           | 358864 | 0.0155148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0367808   | 0.0015654   | 0           | 358864 | 0.0155148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.036145    | 0.00162984  | 0           | 358864 | 0.0155148   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.000937413 | 0.00100218  | 0.349599    | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.000310857 | 0.00092067  | 0.735634    | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00118943  | 0.000783744 | 0.129117    | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.000781486 | 0.000798935 | 0.328001    | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.000141531 | 0.000899117 | 0.874922    | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.003597    | 0.000950776 | 0.00015501  | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.000357223 | 0.000908372 | 0.694132    | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.00769384  | 0.00486034  | 0.113432    | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             | -0.00166589  | 0.0049357   | 0.735727    | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.000187375 | 0.00424362  | 0.964781    | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -4.3801e-06  | 0.00420221  | 0.999168    | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.00290495  | 0.00459384  | 0.527156    | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.0103397   | 0.00466746  | 0.0267458   | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.00529253  | 0.00459328  | 0.249231    | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.0144468   | 0.00184423  | 4.88498e-15 | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                | -0.00129171  | 0.00180428  | 0.474049    | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0212675   | 0.00164501  | 0           | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0321047   | 0.00159164  | 0           | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0279287   | 0.00175267  | 0           | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0380611   | 0.00172398  | 0           | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0369122   | 0.0017664   | 0           | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_len              |  0.000379564 | 0.000859168 | 0.65865     | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_len              |  0.00148955  | 0.000785761 | 0.0580092   | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_len              | -0.00217056  | 0.000664759 | 0.00109475  | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_len               |  0.00224296  | 0.000651982 | 0.00058179  | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_len               | -0.00192327  | 0.000734087 | 0.00879739  | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated_X_len               | -0.00104577  | 0.000755523 | 0.166313    | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated_X_len               | -0.000741721 | 0.00079108  | 0.348452    | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:disp_X_len                 |  0.000390338 | 0.00156183  | 0.802648    | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:disp_X_len                 | -0.00450431  | 0.00151124  | 0.00287907  | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_X_len                 | -0.00895392  | 0.0013218   | 1.26767e-11 | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_X_len                  |  0.00867464  | 0.00131716  | 4.57174e-11 | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_X_len                  |  0.00035412  | 0.00143965  | 0.805702    | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:disp_X_len                  |  0.0067241   | 0.00147873  | 5.45009e-06 | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:disp_X_len                  |  0.00512336  | 0.00151675  | 0.000731153 | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:tXdXlen                    | -0.00411     | 0.00335004  | 0.219885    | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:tXdXlen                    |  0.000359487 | 0.00335415  | 0.914649    | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:tXdXlen                    | -0.00100778  | 0.00284988  | 0.723625    | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:tXdXlen                     |  0.00123267  | 0.00288949  | 0.669669    | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:tXdXlen                     | -0.00276036  | 0.0031495   | 0.380794    | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:tXdXlen                     | -0.00463323  | 0.00325264  | 0.154323    | 358864 | 0.0176994   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:tXdXlen                     | -0.00366416  | 0.00320098  | 0.25234     | 358864 | 0.0176994   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.000336607 | 0.00121247  | 0.781305    | 358864 | 0.0213315   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.000593126 | 0.0011636   | 0.610242    | 358864 | 0.0213315   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -3.0612e-05  | 0.00101583  | 0.97596     | 358864 | 0.0213315   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00207157  | 0.00101421  | 0.0411039   | 358864 | 0.0213315   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.000311449 | 0.0010976   | 0.7766      | 358864 | 0.0213315   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00559257  | 0.00114972  | 1.15247e-06 | 358864 | 0.0213315   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.000880737 | 0.00113597  | 0.438158    | 358864 | 0.0213315   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.011715    | 0.00527966  | 0.0264985   | 358864 | 0.0213315   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.0008017   | 0.00500721  | 0.872796    | 358864 | 0.0213315   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.00499331  | 0.00445191  | 0.262034    | 358864 | 0.0213315   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.0112474   | 0.00462812  | 0.0150935   | 358864 | 0.0213315   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.000548372 | 0.00492847  | 0.911406    | 358864 | 0.0213315   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.0170786   | 0.00520871  | 0.00104306  | 358864 | 0.0213315   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.00795368  | 0.00520449  | 0.126461    | 358864 | 0.0213315   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.0211556   | 0.00251644  | 0           | 358864 | 0.0213315   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered | -0.00228667  | 0.00240878  | 0.34247     | 358864 | 0.0213315   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0249955   | 0.00216554  | 0           | 358864 | 0.0213315   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0511949   | 0.00216064  | 0           | 358864 | 0.0213315   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0501291   | 0.00235184  | 0           | 358864 | 0.0213315   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.0651722   | 0.0023415   | 0           | 358864 | 0.0213315   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.0632615   | 0.00246005  | 0           | 358864 | 0.0213315   |

## Pre-trend Joint Tests
| spec           | test                                    |   n_restrictions |   statistic |      pvalue |      n |
|:---------------|:----------------------------------------|-----------------:|------------:|------------:|-------:|
| event_att      | pretrend_att_joint_zero                 |                3 |    0.552381 | 0.907242    | 358864 |
| event_binary_B | pretrend_baseline_joint_zero            |                3 |    7.225    | 0.0650618   | 358864 |
| event_binary_B | pretrend_displacement_joint_zero        |                3 |   13.3196   | 0.00399413  | 358864 |
| event_binary_D | pretrend_length_displacement_joint_zero |                3 |    3.03297  | 0.38657     | 358864 |
| event_binary_D | pretrend_length_baseline_joint_zero     |                3 |   24.1015   | 2.37899e-05 | 358864 |
| event_score_C  | pretrend_score_baseline_joint_zero      |                3 |    0.803974 | 0.848516    | 358864 |
| event_score_C  | pretrend_score_slope_joint_zero         |                3 |   13.1972   | 0.00422901  | 358864 |