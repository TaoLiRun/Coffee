# Displacement Effect Estimation Summary

- Sample rows: 6,602
- Unique members: 3,301
- Unique closures: 1
- Event FE units: 3,301
- Relative periods: [-1, 1]
- Estimation mode: separate_effect=true
- Closure event: `dept_19_closure_2021-07-15`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |        coef |         se |    pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|-----------:|----------:|
| binary_collapsed | post_X_treated        | 6602 |   0.0977112 | -0.00670773 | 0.00323518 | 0.0382149 |
| binary_collapsed | post_X_disp           | 6602 |   0.0977112 | -0.074672   | 0.00787472 | 0         |
| binary_collapsed | post_X_treated_X_disp | 6602 |   0.0977112 | -0.0457932  | 0.019303   | 0.017733  |

## Score Spec
| spec            | term                   |    n |   r2_within |       coef |         se |      pvalue |
|:----------------|:-----------------------|-----:|------------:|-----------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 6602 |    0.153139 | -0.0244688 | 0.00614015 | 6.89238e-05 |
| score_collapsed | post_X_score           | 6602 |    0.153139 | -0.135788  | 0.011597   | 0           |
| score_collapsed | post_X_treated_X_score | 6602 |    0.153139 | -0.0707421 | 0.0267049  | 0.00811077  |

## Event-study Specs
| spec           | term                                                             |        coef |         se |      pvalue |    n |   r2_within |
|:---------------|:-----------------------------------------------------------------|------------:|-----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                    | -0.00969702 | 0.00452916 | 0.0323453   | 6602 |  0.00122559 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                    | -0.00670773 | 0.00323518 | 0.0382149   | 6602 |  0.0977112  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp             | -0.0457932  | 0.019303   | 0.017733    | 6602 |  0.0977112  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                | -0.074672   | 0.00787472 | 0           | 6602 |  0.0977112  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                    | -0.0244688  | 0.00614015 | 6.89238e-05 | 6602 |  0.153139   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score            | -0.0707421  | 0.0267049  | 0.00811077  | 6602 |  0.153139   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered | -0.135788   | 0.011597   | 0           | 6602 |  0.153139   |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                0 |         nan |      nan | 6602 |
| event_binary_B | pretrend_baseline_joint_zero       |                0 |         nan |      nan | 6602 |
| event_binary_B | pretrend_displacement_joint_zero   |                0 |         nan |      nan | 6602 |
| event_score_C  | pretrend_score_baseline_joint_zero |                0 |         nan |      nan | 6602 |
| event_score_C  | pretrend_score_slope_joint_zero    |                0 |         nan |      nan | 6602 |