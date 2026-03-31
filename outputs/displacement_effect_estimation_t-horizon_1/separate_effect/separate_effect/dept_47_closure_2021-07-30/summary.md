# Displacement Effect Estimation Summary

- Sample rows: 6,768
- Unique members: 3,384
- Unique closures: 1
- Event FE units: 3,384
- Relative periods: [-1, 1]
- Estimation mode: separate_effect=true
- Closure event: `dept_47_closure_2021-07-30`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |        coef |         se |      pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 6768 |   0.0106343 | -0.00739415 | 0.00377312 | 0.0501137   |
| binary_collapsed | post_X_disp           | 6768 |   0.0106343 | -0.022372   | 0.00556132 | 5.87686e-05 |
| binary_collapsed | post_X_treated_X_disp | 6768 |   0.0106343 |  0.0359874  | 0.0207197  | 0.0825005   |

## Score Spec
| spec            | term                   |    n |   r2_within |        coef |         se |      pvalue |
|:----------------|:-----------------------|-----:|------------:|------------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 6768 |   0.0132042 |  0.00201499 | 0.0069741  | 0.772657    |
| score_collapsed | post_X_score           | 6768 |   0.0132042 | -0.0340228  | 0.00768226 | 9.77833e-06 |
| score_collapsed | post_X_treated_X_score | 6768 |   0.0132042 |  0.0238836  | 0.0285828  | 0.403442    |

## Event-study Specs
| spec           | term                                                             |         coef |         se |      pvalue |    n |   r2_within |
|:---------------|:-----------------------------------------------------------------|-------------:|-----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.000701069 | 0.00542161 | 0.89712     | 6768 | 3.77994e-06 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                    | -0.00739415  | 0.00377312 | 0.0501137   | 6768 | 0.0106343   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp             |  0.0359874   | 0.0207197  | 0.0825005   | 6768 | 0.0106343   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                | -0.022372    | 0.00556132 | 5.87686e-05 | 6768 | 0.0106343   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.00201499  | 0.0069741  | 0.772657    | 6768 | 0.0132042   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score            |  0.0238836   | 0.0285828  | 0.403442    | 6768 | 0.0132042   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered | -0.0340228   | 0.00768226 | 9.77833e-06 | 6768 | 0.0132042   |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                0 |         nan |      nan | 6768 |
| event_binary_B | pretrend_baseline_joint_zero       |                0 |         nan |      nan | 6768 |
| event_binary_B | pretrend_displacement_joint_zero   |                0 |         nan |      nan | 6768 |
| event_score_C  | pretrend_score_baseline_joint_zero |                0 |         nan |      nan | 6768 |
| event_score_C  | pretrend_score_slope_joint_zero    |                0 |         nan |      nan | 6768 |