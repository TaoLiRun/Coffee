# Displacement Effect Estimation Summary

- Sample rows: 516
- Unique members: 258
- Unique closures: 1
- Event FE units: 258
- Relative periods: [-1, 1]
- Estimation mode: separate_effect=true
- Closure event: `dept_220_closure_2021-08-03`
- Closure duration filter days: 10
- Recency filter days: 10
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |   n |   r2_within |        coef |        se |   pvalue |
|:-----------------|:----------------------|----:|------------:|------------:|----------:|---------:|
| binary_collapsed | post_X_treated        | 516 |  0.00213125 | -0.00857488 | 0.0252283 | 0.734216 |
| binary_collapsed | post_X_disp           | 516 |  0.00213125 |  0.00253623 | 0.0220971 | 0.908712 |
| binary_collapsed | post_X_treated_X_disp | 516 |  0.00213125 |  0.0305446  | 0.0657937 | 0.642863 |

## Score Spec
| spec            | term                   |   n |   r2_within |        coef |        se |   pvalue |
|:----------------|:-----------------------|----:|------------:|------------:|----------:|---------:|
| score_collapsed | post_X_treated         | 516 | 0.000628641 |  0.0049498  | 0.0347309 | 0.886782 |
| score_collapsed | post_X_score           | 516 | 0.000628641 | -0.00288894 | 0.0334026 | 0.931145 |
| score_collapsed | post_X_treated_X_score | 516 | 0.000628641 |  0.0296475  | 0.108399  | 0.784686 |

## Event-study Specs
| spec           | term                                                             |        coef |        se |   pvalue |   n |   r2_within |
|:---------------|:-----------------------------------------------------------------|------------:|----------:|---------:|----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.00260345 | 0.0282018 | 0.92652  | 516 | 4.17202e-05 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                    | -0.00857488 | 0.0252283 | 0.734216 | 516 | 0.00213125  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp             |  0.0305446  | 0.0657937 | 0.642863 | 516 | 0.00213125  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                |  0.00253623 | 0.0220971 | 0.908712 | 516 | 0.00213125  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.0049498  | 0.0347309 | 0.886782 | 516 | 0.000628641 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score            |  0.0296475  | 0.108399  | 0.784686 | 516 | 0.000628641 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered | -0.00288894 | 0.0334026 | 0.931145 | 516 | 0.000628641 |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |   n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|----:|
| event_att      | pretrend_att_joint_zero            |                0 |         nan |      nan | 516 |
| event_binary_B | pretrend_baseline_joint_zero       |                0 |         nan |      nan | 516 |
| event_binary_B | pretrend_displacement_joint_zero   |                0 |         nan |      nan | 516 |
| event_score_C  | pretrend_score_baseline_joint_zero |                0 |         nan |      nan | 516 |
| event_score_C  | pretrend_score_slope_joint_zero    |                0 |         nan |      nan | 516 |