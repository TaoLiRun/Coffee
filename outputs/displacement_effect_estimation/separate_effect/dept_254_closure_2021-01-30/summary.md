# Displacement Effect Estimation Summary

- Sample rows: 7,248
- Unique members: 906
- Unique closures: 1
- Event FE units: 906
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_254_closure_2021-01-30`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |        coef |         se |      pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 7248 |  0.00885127 |  0.00136933 | 0.00465948 | 0.768917    |
| binary_collapsed | post_X_disp           | 7248 |  0.00885127 | -0.0201645  | 0.00438525 | 4.86606e-06 |
| binary_collapsed | post_X_treated_X_disp | 7248 |  0.00885127 | -0.0115488  | 0.0112048  | 0.302956    |

## Score Spec
| spec            | term                   |    n |   r2_within |         coef |         se |      pvalue |
|:----------------|:-----------------------|-----:|------------:|-------------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 7248 |   0.0130248 | -0.000595263 | 0.00402605 | 0.882492    |
| score_collapsed | post_X_score           | 7248 |   0.0130248 | -0.0320217   | 0.00638254 | 6.31471e-07 |
| score_collapsed | post_X_treated_X_score | 7248 |   0.0130248 | -0.0245697   | 0.0192556  | 0.20229     |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0149847   | 0.00859174 | 0.0814844   | 7248 | 0.000942177 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0118253   | 0.00733008 | 0.107038    | 7248 | 0.000942177 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0104332   | 0.00515298 | 0.043193    | 7248 | 0.000942177 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00288114  | 0.00746632 | 0.699673    | 7248 | 0.000942177 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0135383   | 0.00721314 | 0.0608538   | 7248 | 0.000942177 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0103169   | 0.00770398 | 0.180853    | 7248 | 0.000942177 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0118594   | 0.00730497 | 0.104837    | 7248 | 0.000942177 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0245016   | 0.00716065 | 0.000650178 | 7248 | 0.0180148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0155746   | 0.0055708  | 0.00528748  | 7248 | 0.0180148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00752535  | 0.00427334 | 0.078576    | 7248 | 0.0180148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00799483  | 0.00661953 | 0.227453    | 7248 | 0.0180148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0144519   | 0.00595176 | 0.0153688   | 7248 | 0.0180148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.00621896  | 0.00730216 | 0.394628    | 7248 | 0.0180148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0134585   | 0.00579081 | 0.0203398   | 7248 | 0.0180148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0113487   | 0.0193667  | 0.558026    | 7248 | 0.0180148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.000955986 | 0.0166961  | 0.954352    | 7248 | 0.0180148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.00853486  | 0.0112427  | 0.447962    | 7248 | 0.0180148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.000476122 | 0.0164451  | 0.976909    | 7248 | 0.0180148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.0112883   | 0.0155191  | 0.467181    | 7248 | 0.0180148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              | -0.0201277   | 0.0163867  | 0.219656    | 7248 | 0.0180148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.0105332   | 0.0157472  | 0.503734    | 7248 | 0.0180148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.0362696   | 0.00747143 | 1.42161e-06 | 7248 | 0.0180148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                | -0.0241444   | 0.00624832 | 0.000119436 | 7248 | 0.0180148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                | -0.00312597  | 0.00547334 | 0.568055    | 7248 | 0.0180148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0379213   | 0.00562022 | 2.68563e-11 | 7248 | 0.0180148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.038187    | 0.006423   | 3.93582e-09 | 7248 | 0.0180148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0271154   | 0.00640011 | 2.5005e-05  | 7248 | 0.0180148   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0409744   | 0.00656815 | 6.78183e-10 | 7248 | 0.0180148   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0216626   | 0.00632228 | 0.000639182 | 7248 | 0.0253941   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0153571   | 0.00524152 | 0.00347586  | 7248 | 0.0253941   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.010938    | 0.00383366 | 0.00442746  | 7248 | 0.0253941   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00721107  | 0.0058277  | 0.216267    | 7248 | 0.0253941   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0163525   | 0.00523839 | 0.00185545  | 7248 | 0.0253941   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0107739   | 0.00632655 | 0.088918    | 7248 | 0.0253941   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0160014   | 0.00519141 | 0.00211641  | 7248 | 0.0253941   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.00875227  | 0.0338888  | 0.796261    | 7248 | 0.0253941   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            | -0.0029596   | 0.0283276  | 0.916813    | 7248 | 0.0253941   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.0071971   | 0.0174024  | 0.679288    | 7248 | 0.0253941   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.0119024   | 0.0273115  | 0.663084    | 7248 | 0.0253941   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.0292353   | 0.0248939  | 0.240544    | 7248 | 0.0253941   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             | -0.0369264   | 0.026197   | 0.159011    | 7248 | 0.0253941   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             | -0.0216192   | 0.0262264  | 0.409968    | 7248 | 0.0253941   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.05946     | 0.0109065  | 6.43335e-08 | 7248 | 0.0253941   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered | -0.0405062   | 0.00933788 | 1.60073e-05 | 7248 | 0.0253941   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered | -0.0138767   | 0.00816016 | 0.0893735   | 7248 | 0.0253941   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0595365   | 0.00821553 | 9.13714e-13 | 7248 | 0.0253941   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0643598   | 0.00947975 | 2.03901e-11 | 7248 | 0.0253941   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.0488648   | 0.0094111  | 2.5666e-07  | 7248 | 0.0253941   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.0691685   | 0.00962766 | 1.41043e-12 | 7248 | 0.0253941   |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |     pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|-----------:|-----:|
| event_att      | pretrend_att_joint_zero            |                3 |    5.13357  | 0.162273   | 7248 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |   12.4402   | 0.00601773 | 7248 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |    1.52238  | 0.677114   | 7248 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |   15.0937   | 0.0017383  | 7248 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |    0.425542 | 0.934917   | 7248 |