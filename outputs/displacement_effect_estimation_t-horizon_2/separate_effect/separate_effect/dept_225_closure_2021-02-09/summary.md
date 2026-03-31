# Displacement Effect Estimation Summary

- Sample rows: 9,908
- Unique members: 2,477
- Unique closures: 1
- Event FE units: 2,477
- Relative periods: [-2, -1, 1, 2]
- Estimation mode: separate_effect=true
- Closure event: `dept_225_closure_2021-02-09`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |       coef |         se |      pvalue |
|:-----------------|:----------------------|-----:|------------:|-----------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 9908 |   0.0171127 | -0.0011939 | 0.00384642 | 0.756289    |
| binary_collapsed | post_X_disp           | 9908 |   0.0171127 | -0.0381997 | 0.00576953 | 4.36127e-11 |
| binary_collapsed | post_X_treated_X_disp | 9908 |   0.0171127 | -0.0182143 | 0.0159159  | 0.252566    |

## Score Spec
| spec            | term                   |    n |   r2_within |        coef |         se |      pvalue |
|:----------------|:-----------------------|-----:|------------:|------------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 9908 |   0.0220485 | -0.00788228 | 0.00528788 | 0.136186    |
| score_collapsed | post_X_score           | 9908 |   0.0220485 | -0.0627486  | 0.00859898 | 3.93685e-13 |
| score_collapsed | post_X_treated_X_score | 9908 |   0.0220485 | -0.0288469  | 0.0240015  | 0.229525    |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00389064  | 0.00548362 | 0.47808     | 9908 | 0.000216623 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00791843  | 0.00548058 | 0.148636    | 9908 | 0.000216623 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00262006  | 0.006592   | 0.691062    | 9908 | 0.000216623 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00207735  | 0.00404281 | 0.607412    | 9908 | 0.0269931   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00322739  | 0.00454497 | 0.477708    | 9908 | 0.0269931   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00123775  | 0.00522556 | 0.812782    | 9908 | 0.0269931   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.000994153 | 0.0190867  | 0.958464    | 9908 | 0.0269931   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0271579   | 0.017581   | 0.122539    | 9908 | 0.0269931   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.00827649  | 0.0226248  | 0.714534    | 9908 | 0.0269931   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0374525   | 0.00693481 | 7.27238e-08 | 9908 | 0.0269931   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0291855   | 0.00687493 | 2.26439e-05 | 9908 | 0.0269931   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.00976142  | 0.0080581  | 0.225865    | 9908 | 0.0269931   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00169919  | 0.0062452  | 0.785583    | 9908 | 0.0310791   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.0123726   | 0.00593269 | 0.0371261   | 9908 | 0.0310791   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00509113  | 0.00746386 | 0.495237    | 9908 | 0.0310791   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.0151119   | 0.02728    | 0.57966     | 9908 | 0.0310791   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.0419205   | 0.0259379  | 0.106182    | 9908 | 0.0310791   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.0308852   | 0.0336826  | 0.359259    | 9908 | 0.0310791   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0545907   | 0.0102231  | 1.01437e-07 | 9908 | 0.0310791   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0497411   | 0.0100954  | 8.89596e-07 | 9908 | 0.0310791   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0211654   | 0.0123831  | 0.0875354   | 9908 | 0.0310791   |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                1 |  0.503393   | 0.478013 | 9908 |
| event_binary_B | pretrend_baseline_joint_zero       |                1 |  0.264029   | 0.607366 | 9908 |
| event_binary_B | pretrend_displacement_joint_zero   |                1 |  0.00271298 | 0.95846  | 9908 |
| event_score_C  | pretrend_score_baseline_joint_zero |                1 |  0.0740274  | 0.785561 | 9908 |
| event_score_C  | pretrend_score_slope_joint_zero    |                1 |  0.306865   | 0.57961  | 9908 |