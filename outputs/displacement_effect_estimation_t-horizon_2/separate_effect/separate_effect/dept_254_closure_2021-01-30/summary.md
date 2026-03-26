# Displacement Effect Estimation Summary

- Sample rows: 3,624
- Unique members: 906
- Unique closures: 1
- Event FE units: 906
- Relative periods: [-2, -1, 1, 2]
- Estimation mode: separate_effect=true
- Closure event: `dept_254_closure_2021-01-30`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |        coef |         se |      pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 3624 |   0.0327328 | -0.00746071 | 0.00533187 | 0.162075    |
| binary_collapsed | post_X_disp           | 3624 |   0.0327328 | -0.0364912  | 0.00483409 | 1.07248e-13 |
| binary_collapsed | post_X_treated_X_disp | 3624 |   0.0327328 | -0.00161478 | 0.0138303  | 0.907079    |

## Score Spec
| spec            | term                   |    n |   r2_within |        coef |         se |      pvalue |
|:----------------|:-----------------------|-----:|------------:|------------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 3624 |    0.045138 | -0.00631276 | 0.00462621 | 0.17273     |
| score_collapsed | post_X_score           | 3624 |    0.045138 | -0.0550098  | 0.007145   | 3.59712e-14 |
| score_collapsed | post_X_treated_X_score | 3624 |    0.045138 | -0.0169703  | 0.0235536  | 0.471405    |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0104332   | 0.00515192 | 0.0431497   | 3624 |  0.00160404 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00288114  | 0.00746477 | 0.699614    | 3624 |  0.00160404 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0135383   | 0.00721164 | 0.0608004   | 3624 |  0.00160404 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00752535  | 0.00427186 | 0.0784728   | 3624 |  0.0348091  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00799483  | 0.00661723 | 0.227293    | 3624 |  0.0348091  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0144519   | 0.0059497  | 0.0153335   | 3624 |  0.0348091  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.00853486  | 0.0112388  | 0.447805    | 3624 |  0.0348091  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.000476122 | 0.0164394  | 0.976901    | 3624 |  0.0348091  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.0112883   | 0.0155137  | 0.467027    | 3624 |  0.0348091  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                | -0.00312597  | 0.00547145 | 0.567921    | 3624 |  0.0348091  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0379213   | 0.00561828 | 2.6448e-11  | 3624 |  0.0348091  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.038187    | 0.00642078 | 3.88849e-09 | 3624 |  0.0348091  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.010938    | 0.00383234 | 0.00441384  | 3624 |  0.0487255  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00721107  | 0.00582568 | 0.216108    | 3624 |  0.0487255  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0163525   | 0.00523658 | 0.00184872  | 3624 |  0.0487255  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.0071971   | 0.0173964  | 0.679183    | 3624 |  0.0487255  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.0119024   | 0.027302   | 0.662975    | 3624 |  0.0487255  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.0292353   | 0.0248853  | 0.240382    | 3624 |  0.0487255  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered | -0.0138767   | 0.00815734 | 0.0892628   | 3624 |  0.0487255  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0595365   | 0.00821269 | 8.97948e-13 | 3624 |  0.0487255  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0643598   | 0.00947647 | 2.00764e-11 | 3624 |  0.0487255  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |     pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|-----------:|-----:|
| event_att      | pretrend_att_joint_zero            |                1 |    4.10105  | 0.0428566  | 3624 |
| event_binary_B | pretrend_baseline_joint_zero       |                1 |    3.10327  | 0.0781352  | 3624 |
| event_binary_B | pretrend_displacement_joint_zero   |                1 |    0.576704 | 0.447607   | 3624 |
| event_score_C  | pretrend_score_baseline_joint_zero |                1 |    8.14612  | 0.00431534 | 3624 |
| event_score_C  | pretrend_score_slope_joint_zero    |                1 |    0.171157 | 0.679085   | 3624 |