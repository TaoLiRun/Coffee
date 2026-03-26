# Displacement Effect Estimation Summary

- Sample rows: 5,426
- Unique members: 2,713
- Unique closures: 1
- Event FE units: 2,713
- Relative periods: [-1, 1]
- Estimation mode: separate_effect=true
- Closure event: `dept_131_closure_2021-08-29`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |        coef |         se |      pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 5426 |   0.0659048 | -0.00367092 | 0.00430626 | 0.394034    |
| binary_collapsed | post_X_disp           | 5426 |   0.0659048 | -0.0808625  | 0.011421   | 1.82698e-12 |
| binary_collapsed | post_X_treated_X_disp | 5426 |   0.0659048 |  0.0395572  | 0.0259506  | 0.127544    |

## Score Spec
| spec            | term                   |    n |   r2_within |        coef |         se |      pvalue |
|:----------------|:-----------------------|-----:|------------:|------------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 5426 |   0.0766898 |  0.00674893 | 0.00830238 | 0.416352    |
| score_collapsed | post_X_score           | 5426 |   0.0766898 | -0.113552   | 0.0148835  | 3.24185e-14 |
| score_collapsed | post_X_treated_X_score | 5426 |   0.0766898 |  0.0337699  | 0.0348083  | 0.332049    |

## Event-study Specs
| spec           | term                                                             |         coef |         se |      pvalue |    n |   r2_within |
|:---------------|:-----------------------------------------------------------------|-------------:|-----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.000392617 | 0.00524189 | 0.9403      | 5426 | 2.00864e-06 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                    | -0.00367092  | 0.00430626 | 0.394034    | 5426 | 0.0659048   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp             |  0.0395572   | 0.0259506  | 0.127544    | 5426 | 0.0659048   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                | -0.0808625   | 0.011421   | 1.82698e-12 | 5426 | 0.0659048   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.00674893  | 0.00830238 | 0.416352    | 5426 | 0.0766898   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score            |  0.0337699   | 0.0348083  | 0.332049    | 5426 | 0.0766898   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered | -0.113552    | 0.0148835  | 3.24185e-14 | 5426 | 0.0766898   |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                0 |         nan |      nan | 5426 |
| event_binary_B | pretrend_baseline_joint_zero       |                0 |         nan |      nan | 5426 |
| event_binary_B | pretrend_displacement_joint_zero   |                0 |         nan |      nan | 5426 |
| event_score_C  | pretrend_score_baseline_joint_zero |                0 |         nan |      nan | 5426 |
| event_score_C  | pretrend_score_slope_joint_zero    |                0 |         nan |      nan | 5426 |