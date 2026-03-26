# Displacement Effect Estimation Summary

- Sample rows: 2,696
- Unique members: 674
- Unique closures: 1
- Event FE units: 674
- Relative periods: [-2, -1, 1, 2]
- Estimation mode: separate_effect=true
- Closure event: `dept_8_closure_2021-05-27`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |        coef |         se |    pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|-----------:|----------:|
| binary_collapsed | post_X_treated        | 2696 |   0.0108551 | -0.00276899 | 0.00526876 | 0.599375  |
| binary_collapsed | post_X_disp           | 2696 |   0.0108551 | -0.025878   | 0.010599   | 0.0148807 |
| binary_collapsed | post_X_treated_X_disp | 2696 |   0.0108551 | -0.00698057 | 0.022205   | 0.753338  |

## Score Spec
| spec            | term                   |    n |   r2_within |        coef |         se |     pvalue |
|:----------------|:-----------------------|-----:|------------:|------------:|-----------:|-----------:|
| score_collapsed | post_X_treated         | 2696 |   0.0171915 | -0.00450709 | 0.00680608 | 0.50806    |
| score_collapsed | post_X_score           | 2696 |   0.0171915 | -0.0414666  | 0.0156486  | 0.00824153 |
| score_collapsed | post_X_treated_X_score | 2696 |   0.0171915 | -0.0182085  | 0.0331182  | 0.582636   |

## Event-study Specs
| spec           | term                                                              |         coef |         se |     pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|-----------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0117018   | 0.00891177 | 0.189606   | 2696 |  0.00118092 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  2.45919e-05 | 0.0092625  | 0.997882   | 2696 |  0.00118092 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00218179  | 0.0100475  | 0.828158   | 2696 |  0.00118092 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00405063  | 0.00740239 | 0.584418   | 2696 |  0.012268   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.000137131 | 0.00683129 | 0.98399    | 2696 |  0.012268   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00162447  | 0.00694195 | 0.81505    | 2696 |  0.012268   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0219283   | 0.0232148  | 0.345212   | 2696 |  0.012268   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.00492151  | 0.0248733  | 0.843212   | 2696 |  0.012268   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.00304566  | 0.0271227  | 0.910626   | 2696 |  0.012268   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                | -0.000222871 | 0.0108647  | 0.98364    | 2696 |  0.012268   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0275765   | 0.0124909  | 0.0275992  | 2696 |  0.012268   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0244023   | 0.0116674  | 0.0368577  | 2696 |  0.012268   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0109723   | 0.00794558 | 0.167758   | 2696 |  0.0185302  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00158598  | 0.00802129 | 0.843322   | 2696 |  0.0185302  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.000372148 | 0.00868699 | 0.965842   | 2696 |  0.0185302  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.0174521   | 0.0335626  | 0.603244   | 2696 |  0.0185302  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.00330544  | 0.0363411  | 0.927555   | 2696 |  0.0185302  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.0222704   | 0.0368263  | 0.545555   | 2696 |  0.0185302  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered | -0.00351188  | 0.0153307  | 0.818881   | 2696 |  0.0185302  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0468353   | 0.0179329  | 0.00921025 | 2696 |  0.0185302  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0396098   | 0.0170453  | 0.0204334  | 2696 |  0.0185302  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                1 |    1.72416  | 0.189158 | 2696 |
| event_binary_B | pretrend_baseline_joint_zero       |                1 |    0.299435 | 0.584237 | 2696 |
| event_binary_B | pretrend_displacement_joint_zero   |                1 |    0.892233 | 0.344873 | 2696 |
| event_score_C  | pretrend_score_baseline_joint_zero |                1 |    1.90697  | 0.1673   | 2696 |
| event_score_C  | pretrend_score_slope_joint_zero    |                1 |    0.270386 | 0.603073 | 2696 |