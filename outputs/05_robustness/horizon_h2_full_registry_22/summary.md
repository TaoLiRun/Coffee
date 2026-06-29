# Displacement Effect Estimation Summary

- Sample rows: 179,432
- Unique members: 44,858
- Unique closures: 22
- Event FE units: 44,858
- Relative periods: [-2, -1, 1, 2]
- Estimation mode: separate_effect=false
- Closure duration filter days: False
- Recency filter days: False


## Binary Specs
| spec             | term                  |      n |   r2_within |         coef |          se |    pvalue |
|:-----------------|:----------------------|-------:|------------:|-------------:|------------:|----------:|
| binary_collapsed | post_X_treated        | 179432 |   0.0198035 | -0.000663494 | 0.000716812 | 0.35465   |
| binary_collapsed | post_X_disp           | 179432 |   0.0198035 | -0.0370765   | 0.00122272  | 0         |
| binary_collapsed | post_X_treated_X_disp | 179432 |   0.0198035 |  0.00459621  | 0.00267475  | 0.0857356 |

## Score Spec
| spec            | term                   |      n |   r2_within |         coef |          se |   pvalue |
|:----------------|:-----------------------|-------:|------------:|-------------:|------------:|---------:|
| score_collapsed | post_X_treated         | 179432 |   0.0267131 |  0.000296549 | 0.000886319 | 0.73794  |
| score_collapsed | post_X_score           | 179432 |   0.0267131 | -0.0600203   | 0.0018071   | 0        |
| score_collapsed | post_X_treated_X_score | 179432 |   0.0267131 |  0.00542947  | 0.00389563  | 0.163405 |

## Event-study Specs
| spec           | term                                                              |         coef |          se |      pvalue |      n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|------------:|------------:|-------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.000458833 | 0.00103469  | 0.657443    | 179432 | 5.28102e-05 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00272803  | 0.00103377  | 0.00831992  | 179432 | 5.28102e-05 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.000362876 | 0.00111708  | 0.7453      | 179432 | 5.28102e-05 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00238226  | 0.000820104 | 0.00367633  | 179432 | 0.0235255   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.000392565 | 0.000829226 | 0.635922    | 179432 | 0.0235255   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.000387716 | 0.000914598 | 0.671626    | 179432 | 0.0235255   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.00387856  | 0.00310053  | 0.210965    | 179432 | 0.0235255   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.0067248   | 0.00311535  | 0.0308866   | 179432 | 0.0235255   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.00187262  | 0.0033412   | 0.575166    | 179432 | 0.0235255   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0223413   | 0.00146554  | 0           | 179432 | 0.0235255   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0270211   | 0.00143166  | 0           | 179432 | 0.0235255   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0249627   | 0.00156681  | 0           | 179432 | 0.0235255   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00152045  | 0.000802642 | 0.0581909   | 179432 | 0.0270785   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.000719728 | 0.000822734 | 0.381687    | 179432 | 0.0270785   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.000473307 | 0.000902153 | 0.599835    | 179432 | 0.0270785   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.00114088  | 0.00400044  | 0.775501    | 179432 | 0.0270785   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.00252814  | 0.00400534  | 0.527919    | 179432 | 0.0270785   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.00304975  | 0.00440358  | 0.488588    | 179432 | 0.0270785   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0239832   | 0.00159428  | 0           | 179432 | 0.0270785   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0284159   | 0.00155122  | 0           | 179432 | 0.0270785   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0240934   | 0.00171051  | 0           | 179432 | 0.0270785   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_len              | -0.000700915 | 0.000747362 | 0.348326    | 179432 | 0.0270785   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_len               |  0.00348671  | 0.000692722 | 4.83852e-07 | 179432 | 0.0270785   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_len               | -0.00161131  | 0.000749509 | 0.0315752   | 179432 | 0.0270785   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_X_len                 | -0.00910116  | 0.00133892  | 1.07869e-11 | 179432 | 0.0270785   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_X_len                  |  0.00725186  | 0.0013205   | 4.0015e-08  | 179432 | 0.0270785   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_X_len                  | -0.00235385  | 0.00143309  | 0.100493    | 179432 | 0.0270785   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:tXdXlen                    | -0.00232999  | 0.00275188  | 0.397173    | 179432 | 0.0270785   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:tXdXlen                     | -0.00153532  | 0.00281476  | 0.585445    | 179432 | 0.0270785   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:tXdXlen                     | -0.00338747  | 0.00307555  | 0.270721    | 179432 | 0.0270785   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00153426  | 0.00104799  | 0.143203    | 179432 | 0.0298931   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0020511   | 0.00102839  | 0.0461049   | 179432 | 0.0298931   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.000376973 | 0.0011114   | 0.734469    | 179432 | 0.0298931   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.00113754  | 0.00436439  | 0.794371    | 179432 | 0.0298931   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.010204    | 0.00455076  | 0.024949    | 179432 | 0.0298931   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.00129746  | 0.00483394  | 0.788388    | 179432 | 0.0298931   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0280881   | 0.00211064  | 0           | 179432 | 0.0298931   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0464486   | 0.00211728  | 0           | 179432 | 0.0298931   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0458246   | 0.00230309  | 0           | 179432 | 0.0298931   |

## Pre-trend Joint Tests
| spec           | test                                    |   n_restrictions |   statistic |     pvalue |      n |
|:---------------|:----------------------------------------|-----------------:|------------:|-----------:|-------:|
| event_att      | pretrend_att_joint_zero                 |                1 |   0.196647  | 0.657441   | 179432 |
| event_binary_B | pretrend_baseline_joint_zero            |                1 |   8.43803   | 0.00367454 | 179432 |
| event_binary_B | pretrend_displacement_joint_zero        |                1 |   1.56484   | 0.210959   | 179432 |
| event_binary_D | pretrend_length_displacement_joint_zero |                1 |   0.716883  | 0.397168   | 179432 |
| event_binary_D | pretrend_length_baseline_joint_zero     |                1 |   0.879566  | 0.348321   | 179432 |
| event_score_C  | pretrend_score_baseline_joint_zero      |                1 |   2.14328   | 0.143196   | 179432 |
| event_score_C  | pretrend_score_slope_joint_zero         |                1 |   0.0679335 | 0.79437    | 179432 |