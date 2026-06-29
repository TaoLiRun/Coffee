# Displacement Effect Estimation Summary

- Sample rows: 5,440
- Unique members: 2,720
- Unique closures: 1
- Event FE units: 2,720
- Relative periods: [-1, 1]
- Estimation mode: separate_effect=true
- Closure event: `dept_46_closure_2021-08-04`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |       coef |         se |    pvalue |
|:-----------------|:----------------------|-----:|------------:|-----------:|-----------:|----------:|
| binary_collapsed | post_X_treated        | 5440 |  0.00422685 | -0.0049765 | 0.00282827 | 0.0785956 |
| binary_collapsed | post_X_disp           | 5440 |  0.00422685 | -0.0117352 | 0.00564492 | 0.0377198 |
| binary_collapsed | post_X_treated_X_disp | 5440 |  0.00422685 |  0.0308108 | 0.0163669  | 0.0598739 |

## Score Spec
| spec            | term                   |    n |   r2_within |        coef |         se |    pvalue |
|:----------------|:-----------------------|-----:|------------:|------------:|-----------:|----------:|
| score_collapsed | post_X_treated         | 5440 |  0.00539596 |  0.00423838 | 0.00536438 | 0.429541  |
| score_collapsed | post_X_score           | 5440 |  0.00539596 | -0.0185698  | 0.00797888 | 0.0200184 |
| score_collapsed | post_X_treated_X_score | 5440 |  0.00539596 |  0.041117   | 0.0212179  | 0.0527457 |

## Event-study Specs
| spec           | term                                                             |        coef |         se |    pvalue |    n |   r2_within |
|:---------------|:-----------------------------------------------------------------|------------:|-----------:|----------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.00227921 | 0.00418083 | 0.58569   | 5440 | 6.87152e-05 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                    | -0.0049765  | 0.00282827 | 0.0785956 | 5440 | 0.00422685  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp             |  0.0308108  | 0.0163669  | 0.0598739 | 5440 | 0.00422685  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                | -0.0117352  | 0.00564492 | 0.0377198 | 5440 | 0.00422685  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.00423838 | 0.00536438 | 0.429541  | 5440 | 0.00539596  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score            |  0.041117   | 0.0212179  | 0.0527457 | 5440 | 0.00539596  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered | -0.0185698  | 0.00797888 | 0.0200184 | 5440 | 0.00539596  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                0 |         nan |      nan | 5440 |
| event_binary_B | pretrend_baseline_joint_zero       |                0 |         nan |      nan | 5440 |
| event_binary_B | pretrend_displacement_joint_zero   |                0 |         nan |      nan | 5440 |
| event_score_C  | pretrend_score_baseline_joint_zero |                0 |         nan |      nan | 5440 |
| event_score_C  | pretrend_score_slope_joint_zero    |                0 |         nan |      nan | 5440 |