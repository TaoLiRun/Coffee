# Displacement Effect Estimation Summary

- Sample rows: 1,812
- Unique members: 906
- Unique closures: 1
- Event FE units: 906
- Relative periods: [-1, 1]
- Estimation mode: separate_effect=true
- Closure event: `dept_254_closure_2021-01-30`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |         coef |         se |     pvalue |
|:-----------------|:----------------------|-----:|------------:|-------------:|-----------:|-----------:|
| binary_collapsed | post_X_treated        | 1812 |   0.0529899 | -0.00799483  | 0.00661266 | 0.226971   |
| binary_collapsed | post_X_disp           | 1812 |   0.0529899 | -0.0379213   | 0.00561439 | 2.5649e-11 |
| binary_collapsed | post_X_treated_X_disp | 1812 |   0.0529899 | -0.000476122 | 0.016428   | 0.976885   |

## Score Spec
| spec            | term                   |    n |   r2_within |        coef |         se |      pvalue |
|:----------------|:-----------------------|-----:|------------:|------------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 1812 |   0.0774895 | -0.00721107 | 0.00582165 | 0.215791    |
| score_collapsed | post_X_score           | 1812 |   0.0774895 | -0.0595365  | 0.00820701 | 8.66862e-13 |
| score_collapsed | post_X_treated_X_score | 1812 |   0.0774895 | -0.0119024  | 0.0272831  | 0.662756    |

## Event-study Specs
| spec           | term                                                             |         coef |         se |      pvalue |    n |   r2_within |
|:---------------|:-----------------------------------------------------------------|-------------:|-----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                    | -0.00288114  | 0.00746168 | 0.699495    | 1812 | 0.000167875 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                    | -0.00799483  | 0.00661266 | 0.226971    | 1812 | 0.0529899   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp             | -0.000476122 | 0.016428   | 0.976885    | 1812 | 0.0529899   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                | -0.0379213   | 0.00561439 | 2.5649e-11  | 1812 | 0.0529899   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                    | -0.00721107  | 0.00582165 | 0.215791    | 1812 | 0.0774895   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score            | -0.0119024   | 0.0272831  | 0.662756    | 1812 | 0.0774895   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered | -0.0595365   | 0.00820701 | 8.66862e-13 | 1812 | 0.0774895   |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                0 |         nan |      nan | 1812 |
| event_binary_B | pretrend_baseline_joint_zero       |                0 |         nan |      nan | 1812 |
| event_binary_B | pretrend_displacement_joint_zero   |                0 |         nan |      nan | 1812 |
| event_score_C  | pretrend_score_baseline_joint_zero |                0 |         nan |      nan | 1812 |
| event_score_C  | pretrend_score_slope_joint_zero    |                0 |         nan |      nan | 1812 |