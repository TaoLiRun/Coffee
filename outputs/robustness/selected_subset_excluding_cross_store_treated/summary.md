# Displacement Effect Estimation Summary

- Sample rows: 317,032
- Unique members: 39,629
- Unique closures: 18
- Event FE units: 39,629
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Robustness design: exclude treated members with any cross-store purchase during closure
- Treated exclusion rate: 7.0230%
- Excluded treated member-events: 519


## Binary Specs
| spec             | term                  |      n |   r2_within |         coef |          se |    pvalue |
|:-----------------|:----------------------|-------:|------------:|-------------:|------------:|----------:|
| binary_collapsed | post_X_treated        | 317032 |   0.0132502 |  0.000561809 | 0.000661768 | 0.395913  |
| binary_collapsed | post_X_disp           | 317032 |   0.0132502 | -0.0343486   | 0.00114282  | 0         |
| binary_collapsed | post_X_treated_X_disp | 317032 |   0.0132502 |  0.00515003  | 0.00254446  | 0.0429752 |

## Score Spec
| spec            | term                   |      n |   r2_within |        coef |          se |    pvalue |
|:----------------|:-----------------------|-------:|------------:|------------:|------------:|----------:|
| score_collapsed | post_X_treated         | 317032 |   0.0185003 |  0.0014784  | 0.000826121 | 0.0735299 |
| score_collapsed | post_X_score           | 317032 |   0.0185003 | -0.0567765  | 0.00168676  | 0         |
| score_collapsed | post_X_treated_X_score | 317032 |   0.0185003 |  0.00638265 | 0.00369931  | 0.0844694 |

## Event-study Specs
| spec           | term                                                              |         coef |          se |      pvalue |      n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|------------:|------------:|-------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00189548  | 0.00125371  | 0.13057     | 317032 | 0.000198779 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.00155192  | 0.00120221  | 0.196751    | 317032 | 0.000198779 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.000141647 | 0.00105423  | 0.893118    | 317032 | 0.000198779 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00319549  | 0.00104816  | 0.00230009  | 317032 | 0.000198779 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00123847  | 0.00111999  | 0.268826    | 317032 | 0.000198779 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00787051  | 0.00118983  | 3.76781e-11 | 317032 | 0.000198779 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00343048  | 0.0011696   | 0.00335862  | 317032 | 0.000198779 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00109042  | 0.00104687  | 0.297607    | 317032 | 0.0161569   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.000794764 | 0.000995185 | 0.424522    | 317032 | 0.0161569   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0022433   | 0.000842772 | 0.00777526  | 317032 | 0.0161569   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.000254341 | 0.000834906 | 0.760646    | 317032 | 0.0161569   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.000387609 | 0.000933643 | 0.678028    | 317032 | 0.0161569   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0031981   | 0.000989733 | 0.00123338  | 317032 | 0.0161569   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.000481812 | 0.000962237 | 0.616571    | 317032 | 0.0161569   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0109263   | 0.00397588  | 0.00599592  | 317032 | 0.0161569   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.00253322  | 0.0038045   | 0.505512    | 317032 | 0.0161569   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.00577226  | 0.00336069  | 0.0858813   | 317032 | 0.0161569   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.00801717  | 0.00336996  | 0.0173638   | 317032 | 0.0161569   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.00019868  | 0.00352249  | 0.955021    | 317032 | 0.0161569   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.0141073   | 0.00375964  | 0.000175473 | 317032 | 0.0161569   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.00654895  | 0.00369532  | 0.0763642   | 317032 | 0.0161569   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.00530875  | 0.00181525  | 0.00345179  | 317032 | 0.0161569   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.00449366  | 0.00172891  | 0.00934944  | 317032 | 0.0161569   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0231824   | 0.00155903  | 0           | 317032 | 0.0161569   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0260669   | 0.00153009  | 0           | 317032 | 0.0161569   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0242085   | 0.00165368  | 0           | 317032 | 0.0161569   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0323579   | 0.00164118  | 0           | 317032 | 0.0161569   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0324392   | 0.00171678  | 0           | 317032 | 0.0161569   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00101419  | 0.00103387  | 0.326619    | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.000897567 | 0.000982848 | 0.361127    | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00174876  | 0.000828721 | 0.0348486   | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00049618  | 0.000829316 | 0.549643    | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.000462529 | 0.000921919 | 0.61588     | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00331237  | 0.000977331 | 0.00070165  | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.000804854 | 0.00094949  | 0.396627    | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0158614   | 0.00531278  | 0.00283279  | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0066233   | 0.00520751  | 0.203425    | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.00243932  | 0.00445553  | 0.58405     | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.00587856  | 0.00449151  | 0.190604    | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.00633563  | 0.00476781  | 0.18391     | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.0195138   | 0.00503771  | 0.000107431 | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.010169    | 0.00483958  | 0.0356283   | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.00461226  | 0.00196502  | 0.018921    | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.00585619  | 0.00189606  | 0.00201233  | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0256641   | 0.00172943  | 0           | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0275849   | 0.00167515  | 0           | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0235241   | 0.00182767  | 0           | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0328682   | 0.00178866  | 0           | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.032822    | 0.00184138  | 0           | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_len              |  0.00123859  | 0.000908487 | 0.172777    | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_len              |  0.00194505  | 0.000865586 | 0.0246401   | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_len              | -0.00248231  | 0.00070303  | 0.000414653 | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_len               |  0.00252194  | 0.000686337 | 0.000238633 | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_len               | -0.00152797  | 0.000760918 | 0.0446437   | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated_X_len               | -0.00147397  | 0.000767733 | 0.0548785   | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated_X_len               |  0.000190328 | 0.0008294   | 0.8185      | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:disp_X_len                 | -0.00397201  | 0.00170727  | 0.0199954   | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:disp_X_len                 | -0.00652683  | 0.00162262  | 5.77169e-05 | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_X_len                 | -0.0100217   | 0.0014186   | 1.63869e-12 | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_X_len                  |  0.00719396  | 0.00142453  | 4.4363e-07  | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_X_len                  | -0.00119642  | 0.00153423  | 0.435502    | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:disp_X_len                  |  0.00377206  | 0.00157494  | 0.0166226   | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:disp_X_len                  |  0.00457536  | 0.00161982  | 0.00473611  | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:tXdXlen                    | -0.00572089  | 0.00370571  | 0.122643    | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:tXdXlen                    | -0.0039015   | 0.00361694  | 0.28074     | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:tXdXlen                    | -0.00307322  | 0.00305134  | 0.313859    | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:tXdXlen                     | -0.00373464  | 0.00315645  | 0.236746    | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:tXdXlen                     | -0.0062138   | 0.00334017  | 0.0628469   | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:tXdXlen                     | -0.00755969  | 0.0035671   | 0.0340728   | 317032 | 0.0183068   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:tXdXlen                     | -0.00711699  | 0.0034208   | 0.0374859   | 317032 | 0.0183068   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00191882  | 0.00131044  | 0.143134    | 317032 | 0.0214067   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.00154415  | 0.00125549  | 0.218736    | 317032 | 0.0214067   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.000873985 | 0.0010945   | 0.424573    | 317032 | 0.0214067   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00209248  | 0.00108351  | 0.0534642   | 317032 | 0.0214067   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -3.28797e-05 | 0.00115251  | 0.977241    | 317032 | 0.0214067   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00663473  | 0.00123165  | 7.21128e-08 | 317032 | 0.0214067   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00177347  | 0.00120497  | 0.141083    | 317032 | 0.0214067   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.0204677   | 0.0056672   | 0.00030469  | 317032 | 0.0214067   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.00936204  | 0.00537851  | 0.0817548   | 317032 | 0.0214067   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.0020544   | 0.00475619  | 0.665785    | 317032 | 0.0214067   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.0125289   | 0.00496727  | 0.0116632   | 317032 | 0.0214067   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.00290599  | 0.00508737  | 0.567855    | 317032 | 0.0214067   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.0251159   | 0.00553633  | 5.73465e-06 | 317032 | 0.0214067   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.0130969   | 0.00538282  | 0.014975    | 317032 | 0.0214067   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.0094371   | 0.00262481  | 0.000324347 | 317032 | 0.0214067   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.00395166  | 0.00248841  | 0.112288    | 317032 | 0.0214067   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0295771   | 0.00224525  | 0           | 317032 | 0.0214067   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0447894   | 0.0022755   | 0           | 317032 | 0.0214067   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0442886   | 0.00242776  | 0           | 317032 | 0.0214067   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.0576062   | 0.00242462  | 0           | 317032 | 0.0214067   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.056428    | 0.00256795  | 0           | 317032 | 0.0214067   |

## Pre-trend Joint Tests
| spec           | test                                    |   n_restrictions |   statistic |      pvalue |      n |
|:---------------|:----------------------------------------|-----------------:|------------:|------------:|-------:|
| event_att      | pretrend_att_joint_zero                 |                3 |     3.23756 | 0.356428    | 317032 |
| event_binary_B | pretrend_baseline_joint_zero            |                3 |    11.1924  | 0.0107298   | 317032 |
| event_binary_B | pretrend_displacement_joint_zero        |                3 |    19.9305  | 0.000175469 | 317032 |
| event_binary_D | pretrend_length_displacement_joint_zero |                3 |     2.46558 | 0.481543    | 317032 |
| event_binary_D | pretrend_length_baseline_joint_zero     |                3 |    33.7693  | 2.21623e-07 | 317032 |
| event_score_C  | pretrend_score_baseline_joint_zero      |                3 |     2.35378 | 0.502296    | 317032 |
| event_score_C  | pretrend_score_slope_joint_zero         |                3 |    20.3999  | 0.000140245 | 317032 |