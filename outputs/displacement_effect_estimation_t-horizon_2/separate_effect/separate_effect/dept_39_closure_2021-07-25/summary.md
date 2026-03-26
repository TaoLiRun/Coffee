# Displacement Effect Estimation Summary

- Sample rows: 11,564
- Unique members: 2,891
- Unique closures: 1
- Event FE units: 2,891
- Relative periods: [-2, -1, 1, 2]
- Estimation mode: separate_effect=true
- Closure event: `dept_39_closure_2021-07-25`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |     n |   r2_within |        coef |         se |   pvalue |
|:-----------------|:----------------------|------:|------------:|------------:|-----------:|---------:|
| binary_collapsed | post_X_treated        | 11564 |   0.0243555 | -0.00434934 | 0.00331009 | 0.188962 |
| binary_collapsed | post_X_disp           | 11564 |   0.0243555 | -0.0288663  | 0.00296533 | 0        |
| binary_collapsed | post_X_treated_X_disp | 11564 |   0.0243555 | -0.017815   | 0.0116264  | 0.125559 |

## Score Spec
| spec            | term                   |     n |   r2_within |       coef |         se |    pvalue |
|:----------------|:-----------------------|------:|------------:|-----------:|-----------:|----------:|
| score_collapsed | post_X_treated         | 11564 |     0.03811 | -0.0049396 | 0.00298053 | 0.0975696 |
| score_collapsed | post_X_score           | 11564 |     0.03811 | -0.0553158 | 0.00526265 | 0         |
| score_collapsed | post_X_treated_X_score | 11564 |     0.03811 | -0.0392044 | 0.020342   | 0.054044  |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0158832   | 0.00590038 | 0.00714566  | 11564 |  0.00275556 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.0164071   | 0.0064061  | 0.0104823   | 11564 |  0.00275556 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0271267   | 0.00663405 | 4.45035e-05 | 11564 |  0.00275556 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00558844  | 0.00398584 | 0.161001    | 11564 |  0.0263592  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00449486  | 0.0038525  | 0.243412    | 11564 |  0.0263592  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00979226  | 0.00357263 | 0.00616464  | 11564 |  0.0263592  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.0229346   | 0.0126634  | 0.0702303   | 11564 |  0.0263592  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0233067   | 0.0133755  | 0.081529    | 11564 |  0.0263592  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.035258    | 0.0137008  | 0.010119    | 11564 |  0.0263592  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.00376981  | 0.00335209 | 0.260846    | 11564 |  0.0263592  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0273453   | 0.00335707 | 4.44089e-16 | 11564 |  0.0263592  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0266175   | 0.00371178 | 9.41025e-13 | 11564 |  0.0263592  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00850979  | 0.00343146 | 0.0131973   | 11564 |  0.0405475  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00550569  | 0.00357072 | 0.123207    | 11564 |  0.0405475  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0128833   | 0.00344927 | 0.00019128  | 11564 |  0.0405475  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.0444019   | 0.02215    | 0.0450985   | 11564 |  0.0405475  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.0509699   | 0.0233095  | 0.0288474   | 11564 |  0.0405475  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.0718409   | 0.023561   | 0.00231575  | 11564 |  0.0405475  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered | -0.000829838 | 0.00572826 | 0.884826    | 11564 |  0.0405475  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0569594   | 0.00592197 | 0           | 11564 |  0.0405475  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0545021   | 0.00657908 | 2.22045e-16 | 11564 |  0.0405475  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |    pvalue |     n |
|:---------------|:-----------------------------------|-----------------:|------------:|----------:|------:|
| event_att      | pretrend_att_joint_zero            |                1 |     7.24631 | 0.0071047 | 11564 |
| event_binary_B | pretrend_baseline_joint_zero       |                1 |     1.96581 | 0.160894  | 11564 |
| event_binary_B | pretrend_displacement_joint_zero   |                1 |     3.28006 | 0.0701265 | 11564 |
| event_score_C  | pretrend_score_baseline_joint_zero |                1 |     6.15006 | 0.0131408 | 11564 |
| event_score_C  | pretrend_score_slope_joint_zero    |                1 |     4.01844 | 0.0450054 | 11564 |