# Displacement Effect Estimation Summary

- Sample rows: 2,972
- Unique members: 1,486
- Unique closures: 1
- Event FE units: 1,486
- Relative periods: [-1, 1]
- Estimation mode: separate_effect=true
- Closure event: `dept_3_closure_2021-08-09`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |        coef |         se |      pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 2972 |   0.0185879 |  0.0147293  | 0.00395515 | 0.000203356 |
| binary_collapsed | post_X_disp           | 2972 |   0.0185879 | -0.0305191  | 0.0167864  | 0.0692524   |
| binary_collapsed | post_X_treated_X_disp | 2972 |   0.0185879 |  0.00161987 | 0.0223995  | 0.942359    |

## Score Spec
| spec            | term                   |    n |   r2_within |       coef |         se |    pvalue |
|:----------------|:-----------------------|-----:|------------:|-----------:|-----------:|----------:|
| score_collapsed | post_X_treated         | 2972 |   0.0223387 |  0.0173117 | 0.00691703 | 0.0124297 |
| score_collapsed | post_X_score           | 2972 |   0.0223387 | -0.0536652 | 0.0232279  | 0.0210036 |
| score_collapsed | post_X_treated_X_score | 2972 |   0.0223387 |  0.0110179 | 0.0319655  | 0.730384  |

## Event-study Specs
| spec           | term                                                             |        coef |         se |      pvalue |    n |   r2_within |
|:---------------|:-----------------------------------------------------------------|------------:|-----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.0128701  | 0.00484534 | 0.00798769  | 2972 |  0.00487569 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.0147293  | 0.00395515 | 0.000203356 | 2972 |  0.0185879  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp             |  0.00161987 | 0.0223995  | 0.942359    | 2972 |  0.0185879  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                | -0.0305191  | 0.0167864  | 0.0692524   | 2972 |  0.0185879  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.0173117  | 0.00691703 | 0.0124297   | 2972 |  0.0223387  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score            |  0.0110179  | 0.0319655  | 0.730384    | 2972 |  0.0223387  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered | -0.0536652  | 0.0232279  | 0.0210036   | 2972 |  0.0223387  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                0 |         nan |      nan | 2972 |
| event_binary_B | pretrend_baseline_joint_zero       |                0 |         nan |      nan | 2972 |
| event_binary_B | pretrend_displacement_joint_zero   |                0 |         nan |      nan | 2972 |
| event_score_C  | pretrend_score_baseline_joint_zero |                0 |         nan |      nan | 2972 |
| event_score_C  | pretrend_score_slope_joint_zero    |                0 |         nan |      nan | 2972 |