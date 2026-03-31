# Displacement Effect Estimation Summary

- Sample rows: 3,544
- Unique members: 886
- Unique closures: 1
- Event FE units: 886
- Relative periods: [-2, -1, 1, 2]
- Estimation mode: separate_effect=true
- Closure event: `dept_228_closure_2021-02-04`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |        coef |         se |      pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 3544 |     0.02318 | -0.00183119 | 0.00430108 | 0.670393    |
| binary_collapsed | post_X_disp           | 3544 |     0.02318 | -0.0387323  | 0.00794927 | 1.30586e-06 |
| binary_collapsed | post_X_treated_X_disp | 3544 |     0.02318 |  0.00103246 | 0.0167606  | 0.950895    |

## Score Spec
| spec            | term                   |    n |   r2_within |        coef |         se |      pvalue |
|:----------------|:-----------------------|-----:|------------:|------------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 3544 |   0.0370702 | -0.00482568 | 0.00577393 | 0.403509    |
| score_collapsed | post_X_score           | 3544 |   0.0370702 | -0.0702876  | 0.011659   | 2.42558e-09 |
| score_collapsed | post_X_treated_X_score | 3544 |   0.0370702 |  0.0129033  | 0.0282291  | 0.647718    |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0226716   | 0.00666299 | 0.000697368 | 3544 |  0.00219974 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0139561   | 0.00711335 | 0.0500798   | 3544 |  0.00219974 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0148106   | 0.00801836 | 0.0650674   | 3544 |  0.00219974 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00971826  | 0.00452139 | 0.0318734   | 3544 |  0.0298502  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.000584847 | 0.00547947 | 0.915024    | 3544 |  0.0298502  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00664072  | 0.0068162  | 0.330196    | 3544 |  0.0298502  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0442312   | 0.0226452  | 0.0511074   | 3544 |  0.0298502  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.0378093   | 0.0229911  | 0.100425    | 3544 |  0.0298502  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.00848681  | 0.0232471  | 0.715147    | 3544 |  0.0298502  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                | -0.0203921   | 0.00842228 | 0.0156695   | 3544 |  0.0298502  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0464245   | 0.00955828 | 1.409e-06   | 3544 |  0.0298502  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0514321   | 0.0109054  | 2.7906e-06  | 3544 |  0.0298502  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0208607   | 0.00730318 | 0.00438529  | 3544 |  0.047558   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00665173  | 0.0077137  | 0.388742    | 3544 |  0.047558   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00455758  | 0.00831678 | 0.583831    | 3544 |  0.047558   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.0799452   | 0.0341413  | 0.0194226   | 3544 |  0.047558   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.0743244   | 0.0354745  | 0.0364415   | 3544 |  0.047558   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.0314273   | 0.0386897  | 0.416843    | 3544 |  0.047558   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered | -0.0428715   | 0.0123223  | 0.000527462 | 3544 |  0.047558   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0868405   | 0.0136471  | 3.16435e-10 | 3544 |  0.047558   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0966062   | 0.0165227  | 7.04125e-09 | 3544 |  0.047558   |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |      pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|------------:|-----:|
| event_att      | pretrend_att_joint_zero            |                1 |    11.5778  | 0.000667432 | 3544 |
| event_binary_B | pretrend_baseline_joint_zero       |                1 |     4.61991 | 0.0316029   | 3544 |
| event_binary_B | pretrend_displacement_joint_zero   |                1 |     3.8151  | 0.0507926   | 3544 |
| event_score_C  | pretrend_score_baseline_joint_zero |                1 |     8.15893 | 0.00428497  | 3544 |
| event_score_C  | pretrend_score_slope_joint_zero    |                1 |     5.48306 | 0.0192016   | 3544 |