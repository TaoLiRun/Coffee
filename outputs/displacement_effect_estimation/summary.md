# Displacement Effect Estimation Summary

- Sample rows: 440,904
- Unique members: 54,823
- Unique closures: 29
- Event FE units: 55,113
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]

## Binary Specs
| spec             | term                  |      n |   r2_within |        coef |          se |    pvalue |
|:-----------------|:----------------------|-------:|------------:|------------:|------------:|----------:|
| binary_collapsed | post_X_treated        | 440904 |   0.0127449 |  0.00152921 | 0.000619392 | 0.0135562 |
| binary_collapsed | post_X_disp           | 440904 |   0.0127449 | -0.0339218  | 0.000957431 | 0         |
| binary_collapsed | post_X_treated_X_disp | 440904 |   0.0127449 |  0.00182468 | 0.00226671  | 0.420828  |

## Score Spec
| spec            | term                   |      n |   r2_within |        coef |          se |     pvalue |
|:----------------|:-----------------------|-------:|------------:|------------:|------------:|-----------:|
| score_collapsed | post_X_treated         | 440904 |   0.0187942 |  0.00206681 | 0.000758723 | 0.00645041 |
| score_collapsed | post_X_score           | 440904 |   0.0187942 | -0.0591425  | 0.00145461  | 0          |
| score_collapsed | post_X_treated_X_score | 440904 |   0.0187942 |  0.00289968 | 0.00346215  | 0.402295   |

## Event-study Specs
| spec           | term                                                              |         coef |          se |      pvalue |      n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|------------:|------------:|-------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00197761  | 0.00113331  | 0.0809941   | 440904 | 0.000126539 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.00068356  | 0.00106829  | 0.522264    | 440904 | 0.000126539 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00026714  | 0.00094711  | 0.7779      | 440904 | 0.000126539 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00261869  | 0.000990844 | 0.00822248  | 440904 | 0.000126539 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.000538955 | 0.00107762  | 0.616983    | 440904 | 0.000126539 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00608147  | 0.00112331  | 6.19259e-08 | 440904 | 0.000126539 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00224667  | 0.0011268   | 0.0461729   | 440904 | 0.000126539 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.000344189 | 0.000949839 | 0.71708     | 440904 | 0.0156202   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.000725191 | 0.000857969 | 0.39798     | 440904 | 0.0156202   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00139852  | 0.000729961 | 0.0553842   | 440904 | 0.0156202   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0013849   | 0.000770408 | 0.0722427   | 440904 | 0.0156202   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00144621  | 0.000857664 | 0.0917585   | 440904 | 0.0156202   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00442754  | 0.000926683 | 1.7765e-06  | 440904 | 0.0156202   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00145011  | 0.000893966 | 0.104786    | 440904 | 0.0156202   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.00487868  | 0.00333535  | 0.14355     | 440904 | 0.0156202   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             | -0.00153717  | 0.00319254  | 0.630171    | 440904 | 0.0156202   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.0061143   | 0.00285239  | 0.0320714   | 440904 | 0.0156202   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.00318843  | 0.00295182  | 0.280077    | 440904 | 0.0156202   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.00402806  | 0.00316687  | 0.203401    | 440904 | 0.0156202   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.00437887  | 0.00326634  | 0.180054    | 440904 | 0.0156202   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.00131664  | 0.00329633  | 0.689581    | 440904 | 0.0156202   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.0139542   | 0.00149241  | 0           | 440904 | 0.0156202   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                | -0.00264531  | 0.00144589  | 0.0673254   | 440904 | 0.0156202   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0170522   | 0.0012975   | 0           | 440904 | 0.0156202   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0296513   | 0.00128761  | 0           | 440904 | 0.0156202   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0315867   | 0.00137745  | 0           | 440904 | 0.0156202   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0368913   | 0.00139216  | 0           | 440904 | 0.0156202   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0369013   | 0.00144952  | 0           | 440904 | 0.0156202   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.000440932 | 0.000920658 | 0.631989    | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.000974977 | 0.00083616  | 0.243613    | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00110319  | 0.000700934 | 0.11552     | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00164379  | 0.000750094 | 0.0284241   | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00134945  | 0.000829712 | 0.103869    | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00439653  | 0.000897017 | 9.54856e-07 | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00138982  | 0.000864132 | 0.107765    | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.00685976  | 0.00412774  | 0.0965447   | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             | -0.00087881  | 0.00402473  | 0.827155    | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.00414147  | 0.00356273  | 0.24506     | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.000598486 | 0.00367668  | 0.870693    | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.00381441  | 0.00405873  | 0.347321    | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.00529379  | 0.00409038  | 0.1956      | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.00225798  | 0.00412003  | 0.58366     | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.0144545   | 0.00164917  | 0           | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                | -0.00220616  | 0.00162614  | 0.174887    | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0188737   | 0.00147918  | 0           | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0314558   | 0.00145023  | 0           | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0319852   | 0.00156596  | 0           | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.038505    | 0.00155791  | 0           | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0378152   | 0.00159535  | 0           | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_len              | -0.00015889  | 0.000802458 | 0.843043    | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_len              |  0.000740509 | 0.000722231 | 0.305222    | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_len              | -0.0016012   | 0.00061275  | 0.00897385  | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_len               |  0.00108685  | 0.000618544 | 0.0789052   | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_len               | -0.00164382  | 0.000692618 | 0.017631    | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated_X_len               | -0.00172595  | 0.000725373 | 0.0173443   | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated_X_len               | -0.00205128  | 0.000764168 | 0.00726975  | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:disp_X_len                 |  0.00061178  | 0.00139327  | 0.660593    | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:disp_X_len                 | -0.00258037  | 0.00136038  | 0.0578586   | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_X_len                 | -0.00671276  | 0.00119737  | 2.07722e-08 | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_X_len                  |  0.0069662   | 0.00120417  | 7.28717e-09 | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_X_len                  |  0.0025119   | 0.00128823  | 0.0511951   | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:disp_X_len                  |  0.00722332  | 0.00132825  | 5.40399e-08 | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:disp_X_len                  |  0.00473356  | 0.00136941  | 0.000547379 | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:tXdXlen                    | -0.00345585  | 0.0030149   | 0.251694    | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:tXdXlen                    | -0.000984997 | 0.00293422  | 0.737103    | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:tXdXlen                    |  0.00127692  | 0.00255074  | 0.616647    | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:tXdXlen                     |  0.0030351   | 0.00266825  | 0.255339    | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:tXdXlen                     |  0.00111386  | 0.00291604  | 0.70248     | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:tXdXlen                     | -0.00174939  | 0.00299839  | 0.559596    | 440904 | 0.0170235   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:tXdXlen                     | -0.000516901 | 0.00301414  | 0.863837    | 440904 | 0.0170235   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00167279  | 0.0011282   | 0.138159    | 440904 | 0.0217311   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.000226584 | 0.00106347  | 0.83128     | 440904 | 0.0217311   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.000362002 | 0.000939502 | 0.700007    | 440904 | 0.0217311   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00224961  | 0.000972131 | 0.0206659   | 440904 | 0.0217311   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00034173  | 0.00105342  | 0.745636    | 440904 | 0.0217311   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00565266  | 0.0011039   | 3.05543e-07 | 440904 | 0.0217311   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00181122  | 0.00110548  | 0.101345    | 440904 | 0.0217311   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.0128356   | 0.00489908  | 0.00879548  | 440904 | 0.0217311   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.00209849  | 0.00456065  | 0.645425    | 440904 | 0.0217311   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.00526887  | 0.00412855  | 0.201889    | 440904 | 0.0217311   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.00675062  | 0.00445182  | 0.129431    | 440904 | 0.0217311   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.0037351   | 0.00481974  | 0.438368    | 440904 | 0.0217311   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.012268    | 0.00500679  | 0.014278    | 440904 | 0.0217311   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.00646795  | 0.00503787  | 0.199194    | 440904 | 0.0217311   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.0213233   | 0.0022328   | 0           | 440904 | 0.0217311   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered | -0.00333278  | 0.0021518   | 0.121427    | 440904 | 0.0217311   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0225409   | 0.00192564  | 0           | 440904 | 0.0217311   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0509521   | 0.00194858  | 0           | 440904 | 0.0217311   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0563062   | 0.00207915  | 0           | 440904 | 0.0217311   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.0660367   | 0.00210334  | 0           | 440904 | 0.0217311   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.0650576   | 0.00220195  | 0           | 440904 | 0.0217311   |

## Pre-trend Joint Tests
| spec           | test                                    |   n_restrictions |   statistic |      pvalue |      n |
|:---------------|:----------------------------------------|-----------------:|------------:|------------:|-------:|
| event_att      | pretrend_att_joint_zero                 |                3 |     4.58896 | 0.204491    | 440904 |
| event_binary_B | pretrend_baseline_joint_zero            |                3 |     3.77342 | 0.286993    | 440904 |
| event_binary_B | pretrend_displacement_joint_zero        |                3 |    14.2195  | 0.00262111  | 440904 |
| event_binary_D | pretrend_length_displacement_joint_zero |                3 |     3.04846 | 0.384213    | 440904 |
| event_binary_D | pretrend_length_baseline_joint_zero     |                3 |    12.7159  | 0.00529318  | 440904 |
| event_score_C  | pretrend_score_baseline_joint_zero      |                3 |     3.84952 | 0.278179    | 440904 |
| event_score_C  | pretrend_score_slope_joint_zero         |                3 |    17.6356  | 0.000522896 | 440904 |