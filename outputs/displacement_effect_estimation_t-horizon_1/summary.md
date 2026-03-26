# Displacement Effect Estimation Summary

- Sample rows: 89,716
- Unique members: 44,858
- Unique closures: 22
- Event FE units: 44,858
- Relative periods: [-1, 1]
- Estimation mode: separate_effect=false
- Closure duration filter days: False
- Recency filter days: False


## Binary Specs
| spec             | term                  |     n |   r2_within |         coef |          se |    pvalue |
|:-----------------|:----------------------|------:|------------:|-------------:|------------:|----------:|
| binary_collapsed | post_X_treated        | 89716 |   0.0175622 |  0.000282065 | 0.000831306 | 0.734382  |
| binary_collapsed | post_X_disp           | 89716 |   0.0175622 | -0.0275798   | 0.00144617  | 0         |
| binary_collapsed | post_X_treated_X_disp | 89716 |   0.0175622 |  0.00594455  | 0.0031085   | 0.0558371 |

## Score Spec
| spec            | term                   |     n |   r2_within |        coef |         se |    pvalue |
|:----------------|:-----------------------|------:|------------:|------------:|-----------:|----------:|
| score_collapsed | post_X_treated         | 89716 |   0.0267241 |  0.00160753 | 0.00103401 | 0.120035  |
| score_collapsed | post_X_score           | 89716 |   0.0267241 | -0.0475635  | 0.00214907 | 0         |
| score_collapsed | post_X_treated_X_score | 89716 |   0.0267241 |  0.00868906 | 0.00454404 | 0.0558581 |

## Event-study Specs
| spec           | term                                                             |         coef |          se |      pvalue |     n |   r2_within |
|:---------------|:-----------------------------------------------------------------|-------------:|------------:|------------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.00251725  | 0.00103248  | 0.0147699   | 89716 | 0.000117931 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.000282065 | 0.000831306 | 0.734382    | 89716 | 0.0175622   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp             |  0.00594455  | 0.0031085   | 0.0558371   | 89716 | 0.0175622   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                | -0.0275798   | 0.00144617  | 0           | 89716 | 0.0175622   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.000772031 | 0.000822034 | 0.347648    | 89716 | 0.0189209   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp             |  0.00244663  | 0.00398126  | 0.538864    | 89716 | 0.0189209   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                | -0.0284674   | 0.00154901  | 0           | 89716 | 0.0189209   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_len              |  0.00235488  | 0.000748637 | 0.0016588   | 89716 | 0.0189209   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_X_len                 |  0.00623326  | 0.00135556  | 4.27144e-06 | 89716 | 0.0189209   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:tXdXlen                    | -2.50038e-05 | 0.00280554  | 0.992889    | 89716 | 0.0189209   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.00160753  | 0.00103401  | 0.120035    | 89716 | 0.0267241   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score            |  0.00868906  | 0.00454404  | 0.0558581   | 89716 | 0.0267241   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered | -0.0475635   | 0.00214907  | 0           | 89716 | 0.0267241   |

## Pre-trend Joint Tests
| spec           | test                                    |   n_restrictions |   statistic |   pvalue |     n |
|:---------------|:----------------------------------------|-----------------:|------------:|---------:|------:|
| event_att      | pretrend_att_joint_zero                 |                0 |         nan |      nan | 89716 |
| event_binary_B | pretrend_baseline_joint_zero            |                0 |         nan |      nan | 89716 |
| event_binary_B | pretrend_displacement_joint_zero        |                0 |         nan |      nan | 89716 |
| event_binary_D | pretrend_length_displacement_joint_zero |                0 |         nan |      nan | 89716 |
| event_binary_D | pretrend_length_baseline_joint_zero     |                0 |         nan |      nan | 89716 |
| event_score_C  | pretrend_score_baseline_joint_zero      |                0 |         nan |      nan | 89716 |
| event_score_C  | pretrend_score_slope_joint_zero         |                0 |         nan |      nan | 89716 |