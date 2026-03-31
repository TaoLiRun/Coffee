# Displacement Effect Estimation Summary

- Sample rows: 6,756
- Unique members: 1,689
- Unique closures: 1
- Event FE units: 1,689
- Relative periods: [-2, -1, 1, 2]
- Estimation mode: separate_effect=true
- Closure event: `dept_238_closure_2021-07-24`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |        coef |         se |      pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 6756 |   0.0134324 |  0.00250195 | 0.00294899 | 0.396332    |
| binary_collapsed | post_X_disp           | 6756 |   0.0134324 | -0.0194845  | 0.00488045 | 6.82281e-05 |
| binary_collapsed | post_X_treated_X_disp | 6756 |   0.0134324 | -0.00685556 | 0.00682289 | 0.315143    |

## Score Spec
| spec            | term                   |    n |   r2_within |        coef |         se |      pvalue |
|:----------------|:-----------------------|-----:|------------:|------------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 6756 |   0.0224303 |  0.00136111 | 0.00263068 | 0.604947    |
| score_collapsed | post_X_score           | 6756 |   0.0224303 | -0.0360181  | 0.00785654 | 4.88607e-06 |
| score_collapsed | post_X_treated_X_score | 6756 |   0.0224303 | -0.00867745 | 0.01069    | 0.417058    |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00320199  | 0.00332638 | 0.335884    | 6756 |  0.00111236 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00408598  | 0.00392416 | 0.297915    | 6756 |  0.00111236 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00433088  | 0.00411396 | 0.292616    | 6756 |  0.00111236 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  8.86255e-05 | 0.00261375 | 0.972955    | 6756 |  0.0204061  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00402264  | 0.00331679 | 0.225371    | 6756 |  0.0204061  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00106987  | 0.00340542 | 0.753432    | 6756 |  0.0204061  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.00680663  | 0.00693778 | 0.326686    | 6756 |  0.0204061  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.0013756   | 0.00815217 | 0.866021    | 6756 |  0.0204061  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.00828009  | 0.00835599 | 0.321869    | 6756 |  0.0204061  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                | -0.00544406  | 0.00487431 | 0.264201    | 6756 |  0.0204061  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0140662   | 0.00593966 | 0.017988    | 6756 |  0.0204061  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0303468   | 0.00568742 | 1.0802e-07  | 6756 |  0.0204061  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0018127   | 0.00234993 | 0.440588    | 6756 |  0.030572   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00446389  | 0.00303883 | 0.142033    | 6756 |  0.030572   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  7.10201e-05 | 0.00307316 | 0.981565    | 6756 |  0.030572   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.00975542  | 0.0104312  | 0.349811    | 6756 |  0.030572   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.00464879  | 0.0126663  | 0.713649    | 6756 |  0.030572   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.0122483   | 0.0129784  | 0.345437    | 6756 |  0.030572   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered | -0.00928026  | 0.00734847 | 0.206806    | 6756 |  0.030572   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0293263   | 0.00944023 | 0.00192453  | 6756 |  0.030572   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0519902   | 0.009033   | 1.02349e-08 | 6756 |  0.030572   |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                1 |  0.926606   | 0.335746 | 6756 |
| event_binary_B | pretrend_baseline_joint_zero       |                1 |  0.00114972 | 0.972951 | 6756 |
| event_binary_B | pretrend_displacement_joint_zero   |                1 |  0.962548   | 0.326546 | 6756 |
| event_score_C  | pretrend_score_baseline_joint_zero |                1 |  0.595031   | 0.44048  | 6756 |
| event_score_C  | pretrend_score_slope_joint_zero    |                1 |  0.874628   | 0.349677 | 6756 |