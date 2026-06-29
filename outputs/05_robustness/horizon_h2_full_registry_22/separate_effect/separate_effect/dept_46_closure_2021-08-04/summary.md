# Displacement Effect Estimation Summary

- Sample rows: 10,880
- Unique members: 2,720
- Unique closures: 1
- Event FE units: 2,720
- Relative periods: [-2, -1, 1, 2]
- Estimation mode: separate_effect=true
- Closure event: `dept_46_closure_2021-08-04`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |     n |   r2_within |        coef |         se |      pvalue |
|:-----------------|:----------------------|------:|------------:|------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 10880 |    0.012177 | -0.00122123 | 0.00306897 | 0.690714    |
| binary_collapsed | post_X_disp           | 10880 |    0.012177 | -0.0277056  | 0.00460912 | 2.08982e-09 |
| binary_collapsed | post_X_treated_X_disp | 10880 |    0.012177 |  0.00195695 | 0.0129418  | 0.87982     |

## Score Spec
| spec            | term                   |     n |   r2_within |        coef |         se |      pvalue |
|:----------------|:-----------------------|------:|------------:|------------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 10880 |   0.0152095 | -0.00184486 | 0.00444084 | 0.67786     |
| score_collapsed | post_X_score           | 10880 |   0.0152095 | -0.0407939  | 0.00649718 | 3.96116e-10 |
| score_collapsed | post_X_treated_X_score | 10880 |   0.0152095 | -0.00115181 | 0.0164923  | 0.944326    |

## Event-study Specs
| spec           | term                                                              |        coef |         se |      pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|------------:|-----------:|------------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0159463  | 0.00468468 | 0.000673852 | 10880 |  0.00177209 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00227921 | 0.00418121 | 0.585724    | 10880 |  0.00177209 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0156808  | 0.00480407 | 0.00111185  | 10880 |  0.00177209 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00542319 | 0.00307506 | 0.0779107   | 10880 |  0.0262926  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.0049765  | 0.00282879 | 0.0786506   | 10880 |  0.0262926  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00795723 | 0.00420975 | 0.0588389   | 10880 |  0.0262926  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0591705  | 0.0158623  | 0.000195201 | 10880 |  0.0262926  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.0308108  | 0.0163699  | 0.0599209   | 10880 |  0.0262926  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.0322736  | 0.0163119  | 0.0479693   | 10880 |  0.0262926  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0295014  | 0.00593963 | 7.2254e-07  | 10880 |  0.0262926  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0117352  | 0.00564595 | 0.037755    | 10880 |  0.0262926  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0141747  | 0.00587297 | 0.0158639   | 10880 |  0.0262926  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0264189  | 0.00507937 | 2.12723e-07 | 10880 |  0.0309314  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00423838 | 0.00536537 | 0.429625    | 10880 |  0.0309314  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0184908  | 0.00563678 | 0.00104977  | 10880 |  0.0309314  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.102833   | 0.0197056  | 1.94e-07    | 10880 |  0.0309314  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.041117   | 0.0212218  | 0.0527892   | 10880 |  0.0309314  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.0594127  | 0.0200934  | 0.00313502  | 10880 |  0.0309314  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0358749  | 0.0081195  | 1.03341e-05 | 10880 |  0.0309314  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0185698  | 0.00798035 | 0.0200412   | 10880 |  0.0309314  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.027143   | 0.0080782  | 0.000790102 | 10880 |  0.0309314  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |      pvalue |     n |
|:---------------|:-----------------------------------|-----------------:|------------:|------------:|------:|
| event_att      | pretrend_att_joint_zero            |                1 |     11.5868 | 0.00066423  | 10880 |
| event_binary_B | pretrend_baseline_joint_zero       |                1 |      3.1103 | 0.0777984   | 10880 |
| event_binary_B | pretrend_displacement_joint_zero   |                1 |     13.9148 | 0.00019129  | 10880 |
| event_score_C  | pretrend_score_baseline_joint_zero |                1 |     27.0525 | 1.98e-07    | 10880 |
| event_score_C  | pretrend_score_slope_joint_zero    |                1 |     27.2324 | 1.80407e-07 | 10880 |