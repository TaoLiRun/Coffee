# Displacement Effect Estimation Summary

- Sample rows: 4,954
- Unique members: 2,477
- Unique closures: 1
- Event FE units: 2,477
- Relative periods: [-1, 1]
- Estimation mode: separate_effect=true
- Closure event: `dept_225_closure_2021-02-09`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |        coef |         se |      pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 4954 |   0.0210045 | -0.00322739 | 0.00454405 | 0.477619    |
| binary_collapsed | post_X_disp           | 4954 |   0.0210045 | -0.0291855  | 0.00687354 | 2.25581e-05 |
| binary_collapsed | post_X_treated_X_disp | 4954 |   0.0210045 | -0.0271579  | 0.0175774  | 0.122464    |

## Score Spec
| spec            | term                   |    n |   r2_within |       coef |         se |      pvalue |
|:----------------|:-----------------------|-----:|------------:|-----------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 4954 |    0.028187 | -0.0123726 | 0.00593149 | 0.0370878   |
| score_collapsed | post_X_score           | 4954 |    0.028187 | -0.0497411 | 0.0100933  | 8.85119e-07 |
| score_collapsed | post_X_treated_X_score | 4954 |    0.028187 | -0.0419205 | 0.0259327  | 0.106111    |

## Event-study Specs
| spec           | term                                                             |        coef |         se |      pvalue |    n |   r2_within |
|:---------------|:-----------------------------------------------------------------|------------:|-----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                    | -0.00791843 | 0.00548002 | 0.148595    | 4954 | 0.000715837 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                    | -0.00322739 | 0.00454405 | 0.477619    | 4954 | 0.0210045   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp             | -0.0271579  | 0.0175774  | 0.122464    | 4954 | 0.0210045   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                | -0.0291855  | 0.00687354 | 2.25581e-05 | 4954 | 0.0210045   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                    | -0.0123726  | 0.00593149 | 0.0370878   | 4954 | 0.028187    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score            | -0.0419205  | 0.0259327  | 0.106111    | 4954 | 0.028187    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered | -0.0497411  | 0.0100933  | 8.85119e-07 | 4954 | 0.028187    |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                0 |         nan |      nan | 4954 |
| event_binary_B | pretrend_baseline_joint_zero       |                0 |         nan |      nan | 4954 |
| event_binary_B | pretrend_displacement_joint_zero   |                0 |         nan |      nan | 4954 |
| event_score_C  | pretrend_score_baseline_joint_zero |                0 |         nan |      nan | 4954 |
| event_score_C  | pretrend_score_slope_joint_zero    |                0 |         nan |      nan | 4954 |