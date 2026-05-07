# Displacement Effect Estimation Summary

- Sample rows: 13,512
- Unique members: 1,689
- Unique closures: 1
- Event FE units: 1,689
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_238_closure_2021-07-24`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |     n |   r2_within |         coef |         se |      pvalue |
|:-----------------|:----------------------|------:|------------:|-------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 13512 |  0.00942795 | -0.000880948 | 0.00275475 | 0.749165    |
| binary_collapsed | post_X_disp           | 13512 |  0.00942795 | -0.0165529   | 0.00415593 | 7.09542e-05 |
| binary_collapsed | post_X_treated_X_disp | 13512 |  0.00942795 | -0.00841561  | 0.00603239 | 0.163178    |

## Score Spec
| spec            | term                   |     n |   r2_within |        coef |         se |      pvalue |
|:----------------|:-----------------------|------:|------------:|------------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 13512 |   0.0139942 | -0.00248213 | 0.00241389 | 0.303969    |
| score_collapsed | post_X_score           | 13512 |   0.0139942 | -0.0293209  | 0.00665675 | 1.12593e-05 |
| score_collapsed | post_X_treated_X_score | 13512 |   0.0139942 | -0.0111998  | 0.00955791 | 0.24145     |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00340465  | 0.00460829 | 0.460125    | 13512 |  0.00151995 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.0079332   | 0.00393812 | 0.0441192   | 13512 |  0.00151995 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00320199  | 0.00332675 | 0.335938    | 13512 |  0.00151995 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00408598  | 0.0039246  | 0.297969    | 13512 |  0.00151995 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00433088  | 0.00411442 | 0.29267     | 13512 |  0.00151995 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.00380256  | 0.00455358 | 0.403797    | 13512 |  0.00151995 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00439842  | 0.00434572 | 0.311622    | 13512 |  0.00151995 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.000841146 | 0.00327506 | 0.797338    | 13512 |  0.015251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.00308969  | 0.00294177 | 0.29374     | 13512 |  0.015251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  8.86255e-05 | 0.00261423 | 0.97296     | 13512 |  0.015251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00402264  | 0.0033174  | 0.225457    | 13512 |  0.015251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00106987  | 0.00340605 | 0.753476    | 13512 |  0.015251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.00398337  | 0.00339045 | 0.240208    | 13512 |  0.015251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00061348  | 0.00355303 | 0.862936    | 13512 |  0.015251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.00672572  | 0.00960069 | 0.483683    | 13512 |  0.015251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0113668   | 0.00821123 | 0.166449    | 13512 |  0.015251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.00680663  | 0.00693907 | 0.326776    | 13512 |  0.015251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.0013756   | 0.00815369 | 0.866046    | 13512 |  0.015251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.00828009  | 0.00835754 | 0.321958    | 13512 |  0.015251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.00290422  | 0.00937501 | 0.756764    | 13512 |  0.015251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.00476302  | 0.00886613 | 0.59119     | 13512 |  0.015251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.0171305   | 0.00650653 | 0.00854523  | 13512 |  0.015251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                | -0.0172416   | 0.00570636 | 0.00255332  | 13512 |  0.015251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                | -0.00544406  | 0.00487521 | 0.264289    | 13512 |  0.015251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0140662   | 0.00594076 | 0.0180093   | 13512 |  0.015251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0303468   | 0.00568848 | 1.086e-07   | 13512 |  0.015251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0286179   | 0.0064497  | 9.70821e-06 | 13512 |  0.015251   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.032997    | 0.00641471 | 3.00375e-07 | 13512 |  0.015251   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00215647  | 0.00308863 | 0.485151    | 13512 |  0.0221576  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.00587038  | 0.00266956 | 0.0280126   | 13512 |  0.0221576  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0018127   | 0.00235037 | 0.440673    | 13512 |  0.0221576  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00446389  | 0.0030394  | 0.142107    | 13512 |  0.0221576  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  7.10201e-05 | 0.00307373 | 0.981569    | 13512 |  0.0221576  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.00327958  | 0.00313435 | 0.295557    | 13512 |  0.0221576  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00134433  | 0.00320803 | 0.675232    | 13512 |  0.0221576  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.0145365   | 0.0150629  | 0.334655    | 13512 |  0.0221576  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.0185946   | 0.0127786  | 0.145817    | 13512 |  0.0221576  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.00975542  | 0.0104331  | 0.3499      | 13512 |  0.0221576  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.00464879  | 0.0126686  | 0.7137      | 13512 |  0.0221576  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.0122483   | 0.0129808  | 0.345526    | 13512 |  0.0221576  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.00901444  | 0.0148596  | 0.544172    | 13512 |  0.0221576  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             | -0.00332752  | 0.0139781  | 0.811869    | 13512 |  0.0221576  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.033513    | 0.0101995  | 0.00103799  | 13512 |  0.0221576  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered | -0.0317047   | 0.00892321 | 0.000391245 | 13512 |  0.0221576  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered | -0.00928026  | 0.00734983 | 0.20689     | 13512 |  0.0221576  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0293263   | 0.00944198 | 0.00192826  | 13512 |  0.0221576  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0519902   | 0.00903468 | 1.02985e-08 | 13512 |  0.0221576  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.0518418   | 0.0102877  | 5.17662e-07 | 13512 |  0.0221576  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.0586233   | 0.0102124  | 1.11776e-08 | 13512 |  0.0221576  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |     n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|------:|
| event_att      | pretrend_att_joint_zero            |                3 |     4.97154 | 0.173893 | 13512 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |     1.34845 | 0.717661 | 13512 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |     2.14806 | 0.542251 | 13512 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |     5.23494 | 0.15538  | 13512 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |     2.14878 | 0.542107 | 13512 |