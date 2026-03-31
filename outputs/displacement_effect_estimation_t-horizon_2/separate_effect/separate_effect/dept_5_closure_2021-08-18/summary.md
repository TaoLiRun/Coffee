# Displacement Effect Estimation Summary

- Sample rows: 9,756
- Unique members: 2,439
- Unique closures: 1
- Event FE units: 2,439
- Relative periods: [-2, -1, 1, 2]
- Estimation mode: separate_effect=true
- Closure event: `dept_5_closure_2021-08-18`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |        coef |         se |     pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|-----------:|-----------:|
| binary_collapsed | post_X_treated        | 9756 |  0.00153084 | -0.00632374 | 0.00230039 | 0.00602194 |
| binary_collapsed | post_X_disp           | 9756 |  0.00153084 | -0.0101307  | 0.007634   | 0.184616   |
| binary_collapsed | post_X_treated_X_disp | 9756 |  0.00153084 | -0.00550887 | 0.0250073  | 0.825663   |

## Score Spec
| spec            | term                   |    n |   r2_within |        coef |         se |   pvalue |
|:----------------|:-----------------------|-----:|------------:|------------:|-----------:|---------:|
| score_collapsed | post_X_treated         | 9756 |  0.00088338 | -0.00864489 | 0.00588246 | 0.141798 |
| score_collapsed | post_X_score           | 9756 |  0.00088338 | -0.00858613 | 0.0113165  | 0.44809  |
| score_collapsed | post_X_treated_X_score | 9756 |  0.00088338 | -0.0127942  | 0.0238769  | 0.592117 |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00870249  | 0.00242831 | 0.000345324 | 9756 | 0.000839805 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.0011962   | 0.00298196 | 0.688348    | 9756 | 0.000839805 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.000748905 | 0.00355298 | 0.833075    | 9756 | 0.000839805 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00179845  | 0.00184658 | 0.330186    | 9756 | 0.00679667  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00564468  | 0.00262505 | 0.0316283   | 9756 | 0.00679667  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00520435  | 0.00316789 | 0.100544    | 9756 | 0.00679667  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0869461   | 0.0194122  | 7.84742e-06 | 9756 | 0.00679667  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.0435956   | 0.0245035  | 0.0753387   | 9756 | 0.00679667  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.0323328   | 0.0302649  | 0.285479    | 9756 | 0.00679667  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                | -0.026547    | 0.00911619 | 0.00362305  | 9756 | 0.00679667  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0214201   | 0.00934947 | 0.0220457   | 9756 | 0.00679667  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0253883   | 0.0101477  | 0.0124185   | 9756 | 0.00679667  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0260689   | 0.00553882 | 2.6602e-06  | 9756 | 0.00884714  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0055606   | 0.00668984 | 0.405942    | 9756 | 0.00884714  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00321847  | 0.0073874  | 0.663114    | 9756 | 0.00884714  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.120052    | 0.0232405  | 2.5905e-07  | 9756 | 0.00884714  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.0516194   | 0.027315   | 0.0589056   | 9756 | 0.00884714  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.0428439   | 0.0294692  | 0.146116    | 9756 | 0.00884714  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered | -0.0506065   | 0.0131504  | 0.000122001 | 9756 | 0.00884714  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0285132   | 0.0136749  | 0.0371663   | 9756 | 0.00884714  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0392656   | 0.0142906  | 0.00604667  | 9756 | 0.00884714  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |      pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|------------:|-----:|
| event_att      | pretrend_att_joint_zero            |                1 |   12.8433   | 0.000338683 | 9756 |
| event_binary_B | pretrend_baseline_joint_zero       |                1 |    0.948547 | 0.33009     | 9756 |
| event_binary_B | pretrend_displacement_joint_zero   |                1 |   20.0609   | 7.50161e-06 | 9756 |
| event_score_C  | pretrend_score_baseline_joint_zero |                1 |   22.1518   | 2.51919e-06 | 9756 |
| event_score_C  | pretrend_score_slope_joint_zero    |                1 |   26.6836   | 2.39649e-07 | 9756 |