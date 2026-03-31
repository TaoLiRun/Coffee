# Displacement Effect Estimation Summary

- Sample rows: 23,128
- Unique members: 2,891
- Unique closures: 1
- Event FE units: 2,891
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_39_closure_2021-07-25`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |     n |   r2_within |       coef |         se |    pvalue |
|:-----------------|:----------------------|------:|------------:|-----------:|-----------:|----------:|
| binary_collapsed | post_X_treated        | 23128 |   0.0132165 | -0.0112999 | 0.00439158 | 0.0101294 |
| binary_collapsed | post_X_disp           | 23128 |   0.0132165 | -0.0236337 | 0.00276716 | 0         |
| binary_collapsed | post_X_treated_X_disp | 23128 |   0.0132165 | -0.0117546 | 0.0112106  | 0.294484  |

## Score Spec
| spec            | term                   |     n |   r2_within |       coef |         se |     pvalue |
|:----------------|:-----------------------|------:|------------:|-----------:|-----------:|-----------:|
| score_collapsed | post_X_treated         | 23128 |   0.0189002 | -0.010637  | 0.00375998 | 0.00470142 |
| score_collapsed | post_X_score           | 23128 |   0.0189002 | -0.0430565 | 0.00486613 | 0          |
| score_collapsed | post_X_treated_X_score | 23128 |   0.0189002 | -0.0317999 | 0.0189662  | 0.0937173  |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.009596    | 0.00840762 | 0.253821    | 23128 |  0.00259785 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.000920078 | 0.00785052 | 0.90671     | 23128 |  0.00259785 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0158832   | 0.00590089 | 0.00715064  | 23128 |  0.00259785 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.0164071   | 0.00640666 | 0.010489    | 23128 |  0.00259785 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0271267   | 0.00663462 | 4.4571e-05  | 23128 |  0.00259785 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.022651    | 0.00673598 | 0.000781928 | 23128 |  0.00259785 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0294369   | 0.00680631 | 1.5774e-05  | 23128 |  0.00259785 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00852817  | 0.00782432 | 0.275823    | 23128 |  0.0170351  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.012487    | 0.00765258 | 0.102843    | 23128 |  0.0170351  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00558844  | 0.00398636 | 0.161056    | 23128 |  0.0170351  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00449486  | 0.003853   | 0.243473    | 23128 |  0.0170351  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00979226  | 0.0035731  | 0.0061713   | 23128 |  0.0170351  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.00740911  | 0.00430129 | 0.0850801   | 23128 |  0.0170351  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00807643  | 0.00418602 | 0.0537812   | 23128 |  0.0170351  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             | -0.0381918   | 0.0173677  | 0.0279562   | 23128 |  0.0170351  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             | -0.0247589   | 0.0164011  | 0.131257    | 23128 |  0.0170351  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.0229346   | 0.0126651  | 0.0702667   | 23128 |  0.0170351  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0233067   | 0.0133772  | 0.0815686   | 23128 |  0.0170351  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.035258    | 0.0137026  | 0.0101288   | 23128 |  0.0170351  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              | -0.0304484   | 0.0139172  | 0.028762    | 23128 |  0.0170351  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.0438905   | 0.0137839  | 0.00146698  | 23128 |  0.0170351  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.0148045   | 0.00394786 | 0.00018029  | 23128 |  0.0170351  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                | -0.00567332  | 0.00384951 | 0.140651    | 23128 |  0.0170351  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.00376981  | 0.00335252 | 0.260908    | 23128 |  0.0170351  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0273453   | 0.00335751 | 4.44089e-16 | 23128 |  0.0170351  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0266175   | 0.00371226 | 9.47242e-13 | 23128 |  0.0170351  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0288336   | 0.00399482 | 6.72351e-13 | 23128 |  0.0170351  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0284465   | 0.00396907 | 9.68781e-13 | 23128 |  0.0170351  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00188072  | 0.00640583 | 0.769089    | 23128 |  0.025185   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.00904972  | 0.00645531 | 0.161052    | 23128 |  0.025185   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00850979  | 0.00343191 | 0.0132092   | 23128 |  0.025185   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00550569  | 0.00357118 | 0.123256    | 23128 |  0.025185   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0128833   | 0.00344972 | 0.000191647 | 23128 |  0.025185   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.00929778  | 0.00394538 | 0.0185082   | 23128 |  0.025185   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0124407   | 0.00390806 | 0.00147136  | 23128 |  0.025185   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            | -0.059455    | 0.0304696  | 0.0511189   | 23128 |  0.025185   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            | -0.0442216   | 0.0281959  | 0.116903    | 23128 |  0.025185   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.0444019   | 0.0221529  | 0.0451264   | 23128 |  0.025185   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.0509699   | 0.0233125  | 0.0288681   | 23128 |  0.025185   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.0718409   | 0.0235641  | 0.00231879  | 23128 |  0.025185   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             | -0.0653325   | 0.0234568  | 0.00538381  | 23128 |  0.025185   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             | -0.087135    | 0.0231572  | 0.000171384 | 23128 |  0.025185   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.0379591   | 0.00675212 | 2.07002e-08 | 23128 |  0.025185   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered | -0.0188914   | 0.00658709 | 0.00416144  | 23128 |  0.025185   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered | -0.000829838 | 0.005729   | 0.884841    | 23128 |  0.025185   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0569594   | 0.00592274 | 0           | 23128 |  0.025185   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0545021   | 0.00657993 | 2.22045e-16 | 23128 |  0.025185   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.0587602   | 0.00681846 | 0           | 23128 |  0.025185   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.0596848   | 0.00702845 | 0           | 23128 |  0.025185   |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |     pvalue |     n |
|:---------------|:-----------------------------------|-----------------:|------------:|-----------:|------:|
| event_att      | pretrend_att_joint_zero            |                3 |    15.1078  | 0.00172678 | 23128 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |     7.09047 | 0.0690694  | 23128 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |     5.90503 | 0.116323   | 23128 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |    13.4799  | 0.00370575 | 23128 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |     5.52545 | 0.137124   | 23128 |