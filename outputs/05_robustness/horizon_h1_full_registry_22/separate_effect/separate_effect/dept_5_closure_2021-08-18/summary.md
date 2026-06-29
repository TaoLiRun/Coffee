# Displacement Effect Estimation Summary

- Sample rows: 4,878
- Unique members: 2,439
- Unique closures: 1
- Event FE units: 2,439
- Relative periods: [-1, 1]
- Estimation mode: separate_effect=true
- Closure event: `dept_5_closure_2021-08-18`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |        coef |         se |    pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|-----------:|----------:|
| binary_collapsed | post_X_treated        | 4878 |  0.00718947 | -0.00564468 | 0.00262451 | 0.0315934 |
| binary_collapsed | post_X_disp           | 4878 |  0.00718947 | -0.0214201  | 0.00934756 | 0.0220184 |
| binary_collapsed | post_X_treated_X_disp | 4878 |  0.00718947 |  0.0435956  | 0.0244985  | 0.0752789 |

## Score Spec
| spec            | term                   |    n |   r2_within |       coef |         se |    pvalue |
|:----------------|:-----------------------|-----:|------------:|-----------:|-----------:|----------:|
| score_collapsed | post_X_treated         | 4878 |  0.00616785 |  0.0055606 | 0.00668847 | 0.405846  |
| score_collapsed | post_X_score           | 4878 |  0.00616785 | -0.0285132 | 0.0136721  | 0.0371274 |
| score_collapsed | post_X_treated_X_score | 4878 |  0.00616785 |  0.0516194 | 0.0273094  | 0.0588537 |

## Event-study Specs
| spec           | term                                                             |        coef |         se |    pvalue |    n |   r2_within |
|:---------------|:-----------------------------------------------------------------|------------:|-----------:|----------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                    | -0.0011962  | 0.00298165 | 0.688318  | 4878 | 2.66797e-05 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                    | -0.00564468 | 0.00262451 | 0.0315934 | 4878 | 0.00718947  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp             |  0.0435956  | 0.0244985  | 0.0752789 | 4878 | 0.00718947  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                | -0.0214201  | 0.00934756 | 0.0220184 | 4878 | 0.00718947  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.0055606  | 0.00668847 | 0.405846  | 4878 | 0.00616785  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score            |  0.0516194  | 0.0273094  | 0.0588537 | 4878 | 0.00616785  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered | -0.0285132  | 0.0136721  | 0.0371274 | 4878 | 0.00616785  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                0 |         nan |      nan | 4878 |
| event_binary_B | pretrend_baseline_joint_zero       |                0 |         nan |      nan | 4878 |
| event_binary_B | pretrend_displacement_joint_zero   |                0 |         nan |      nan | 4878 |
| event_score_C  | pretrend_score_baseline_joint_zero |                0 |         nan |      nan | 4878 |
| event_score_C  | pretrend_score_slope_joint_zero    |                0 |         nan |      nan | 4878 |