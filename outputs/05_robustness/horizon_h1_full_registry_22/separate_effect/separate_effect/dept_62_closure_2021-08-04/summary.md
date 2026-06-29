# Displacement Effect Estimation Summary

- Sample rows: 5,288
- Unique members: 2,644
- Unique closures: 1
- Event FE units: 2,644
- Relative periods: [-1, 1]
- Estimation mode: separate_effect=true
- Closure event: `dept_62_closure_2021-08-04`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |        coef |         se |      pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 5288 |   0.0166822 | -0.00216942 | 0.00302985 | 0.474046    |
| binary_collapsed | post_X_disp           | 5288 |   0.0166822 | -0.0248393  | 0.00590264 | 2.66034e-05 |
| binary_collapsed | post_X_treated_X_disp | 5288 |   0.0166822 |  0.00979484 | 0.0186817  | 0.600114    |

## Score Spec
| spec            | term                   |    n |   r2_within |         coef |         se |      pvalue |
|:----------------|:-----------------------|-----:|------------:|-------------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 5288 |    0.020115 |  0.000678431 | 0.00654678 | 0.917472    |
| score_collapsed | post_X_score           | 5288 |    0.020115 | -0.0410799   | 0.00950055 | 1.58937e-05 |
| score_collapsed | post_X_treated_X_score | 5288 |    0.020115 |  0.0237445   | 0.0341305  | 0.486679    |

## Event-study Specs
| spec           | term                                                             |         coef |         se |      pvalue |    n |   r2_within |
|:---------------|:-----------------------------------------------------------------|-------------:|-----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.000377909 | 0.00430267 | 0.930017    | 5288 | 1.87364e-06 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                    | -0.00216942  | 0.00302985 | 0.474046    | 5288 | 0.0166822   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp             |  0.00979484  | 0.0186817  | 0.600114    | 5288 | 0.0166822   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                | -0.0248393   | 0.00590264 | 2.66034e-05 | 5288 | 0.0166822   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.000678431 | 0.00654678 | 0.917472    | 5288 | 0.020115    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score            |  0.0237445   | 0.0341305  | 0.486679    | 5288 | 0.020115    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered | -0.0410799   | 0.00950055 | 1.58937e-05 | 5288 | 0.020115    |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                0 |         nan |      nan | 5288 |
| event_binary_B | pretrend_baseline_joint_zero       |                0 |         nan |      nan | 5288 |
| event_binary_B | pretrend_displacement_joint_zero   |                0 |         nan |      nan | 5288 |
| event_score_C  | pretrend_score_baseline_joint_zero |                0 |         nan |      nan | 5288 |
| event_score_C  | pretrend_score_slope_joint_zero    |                0 |         nan |      nan | 5288 |