# Displacement Effect Estimation Summary

- Sample rows: 17,744
- Unique members: 2,218
- Unique closures: 1
- Event FE units: 2,218
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_121_closure_2021-08-03`
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Length-heterogeneity event-study spec skipped: true
- Model type: DDD


## Binary Specs
| spec             | term                  |     n |   r2_within |       coef |         se |      pvalue |
|:-----------------|:----------------------|------:|------------:|-----------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 17744 |   0.0199266 |  0.0114154 | 0.00234312 | 1.18358e-06 |
| binary_collapsed | post_X_disp           | 17744 |   0.0199266 | -0.0362503 | 0.00437818 | 2.22045e-16 |
| binary_collapsed | post_X_treated_X_disp | 17744 |   0.0199266 |  0.0107334 | 0.0101021  | 0.28813     |

## Score Spec
| spec            | term                   |     n |   r2_within |       coef |         se |      pvalue |
|:----------------|:-----------------------|------:|------------:|-----------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 17744 |   0.0258955 |  0.0141502 | 0.00318307 | 9.20328e-06 |
| score_collapsed | post_X_score           | 17744 |   0.0258955 | -0.0601904 | 0.0067441  | 0           |
| score_collapsed | post_X_treated_X_score | 17744 |   0.0258955 |  0.0185906 | 0.0148232  | 0.209918    |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00915479  | 0.0045651  | 0.0450428   | 17744 |  0.00333081 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00783128  | 0.00392017 | 0.0458722   | 17744 |  0.00333081 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  1.12955e-05 | 0.00404246 | 0.997771    | 17744 |  0.00333081 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00476228  | 0.00415294 | 0.251619    | 17744 |  0.00333081 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0104188   | 0.00398912 | 0.00906709  | 17744 |  0.00333081 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0166038   | 0.0046453  | 0.000358636 | 17744 |  0.00333081 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00987815  | 0.00443556 | 0.026045    | 17744 |  0.00333081 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0127384   | 0.00350051 | 0.000279937 | 17744 |  0.0298126  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00989654  | 0.00303993 | 0.00114892  | 17744 |  0.0298126  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00168857  | 0.00255006 | 0.507932    | 17744 |  0.0298126  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00429662  | 0.00324444 | 0.185539    | 17744 |  0.0298126  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00649849  | 0.00296465 | 0.0284835   | 17744 |  0.0298126  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0103614   | 0.00354781 | 0.00352983  | 17744 |  0.0298126  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00355874  | 0.00324426 | 0.272789    | 17744 |  0.0298126  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0164494   | 0.0153864  | 0.285145    | 17744 |  0.0298126  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.00947838  | 0.0132942  | 0.475938    | 17744 |  0.0298126  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.00347337  | 0.0142918  | 0.808003    | 17744 |  0.0298126  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.000817613 | 0.0141796  | 0.954024    | 17744 |  0.0298126  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.0154982   | 0.013937   | 0.26625     | 17744 |  0.0298126  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.024035    | 0.0160616  | 0.134684    | 17744 |  0.0298126  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.0250371   | 0.0155851  | 0.108312    | 17744 |  0.0298126  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.0179264   | 0.00788344 | 0.0230654   | 17744 |  0.0298126  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.0103122   | 0.00660264 | 0.118471    | 17744 |  0.0298126  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.044949    | 0.00659318 | 1.19014e-11 | 17744 |  0.0298126  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0143307   | 0.00546217 | 0.00875965  | 17744 |  0.0298126  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0119067   | 0.00594394 | 0.0452816   | 17744 |  0.0298126  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0270741   | 0.00593712 | 5.39034e-06 | 17744 |  0.0298126  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0185024   | 0.00649088 | 0.00440506  | 17744 |  0.0298126  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00814702  | 0.00485631 | 0.0935632   | 17744 |  0.0373341  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0071259   | 0.0041883  | 0.0890115   | 17744 |  0.0373341  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00111731  | 0.00429067 | 0.794576    | 17744 |  0.0373341  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00437812  | 0.00449821 | 0.330509    | 17744 |  0.0373341  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0106988   | 0.00433317 | 0.0136222   | 17744 |  0.0373341  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0169676   | 0.00505678 | 0.000805801 | 17744 |  0.0373341  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0104007   | 0.0048556  | 0.0323026   | 17744 |  0.0373341  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.0210698   | 0.0225887  | 0.351045    | 17744 |  0.0373341  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.0167812   | 0.0189274  | 0.375386    | 17744 |  0.0373341  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.000923247 | 0.0217534  | 0.966151    | 17744 |  0.0373341  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.000433891 | 0.0215342  | 0.983926    | 17744 |  0.0373341  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.0237886   | 0.0206132  | 0.248605    | 17744 |  0.0373341  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.0471092   | 0.0250478  | 0.0601346   | 17744 |  0.0373341  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.0418052   | 0.0248078  | 0.0920972   | 17744 |  0.0373341  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered |  0.0291161   | 0.0118457  | 0.0140496   | 17744 |  0.0373341  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.0172164   | 0.0100703  | 0.0874751   | 17744 |  0.0373341  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0664851   | 0.0100798  | 5.26934e-11 | 17744 |  0.0373341  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.024266    | 0.0085089  | 0.00438701  | 17744 |  0.0373341  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0198087   | 0.00933865 | 0.0340197   | 17744 |  0.0373341  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.0509328   | 0.00913569 | 2.77418e-08 | 17744 |  0.0373341  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.0329366   | 0.0104039  | 0.00156758  | 17744 |  0.0373341  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |      pvalue |     n |
|:---------------|:-----------------------------------|-----------------:|------------:|------------:|------:|
| event_att      | pretrend_att_joint_zero            |                3 |     7.50097 | 0.0575335   | 17744 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |    21.8854  | 6.89119e-05 | 17744 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |     2.24158 | 0.523805    | 17744 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |     6.18752 | 0.102835    | 17744 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |     1.58912 | 0.661859    | 17744 |