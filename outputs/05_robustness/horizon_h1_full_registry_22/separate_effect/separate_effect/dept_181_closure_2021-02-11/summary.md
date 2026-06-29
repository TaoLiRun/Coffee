# Displacement Effect Estimation Summary

- Sample rows: 882
- Unique members: 441
- Unique closures: 1
- Event FE units: 441
- Relative periods: [-1, 1]
- Estimation mode: separate_effect=true
- Closure event: `dept_181_closure_2021-02-11`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |   n |   r2_within |       coef |        se |      pvalue |
|:-----------------|:----------------------|----:|------------:|-----------:|----------:|------------:|
| binary_collapsed | post_X_treated        | 882 |   0.0800125 |  0.0266034 | 0.0144473 | 0.0662351   |
| binary_collapsed | post_X_disp           | 882 |   0.0800125 | -0.0460625 | 0.0117112 | 9.73628e-05 |
| binary_collapsed | post_X_treated_X_disp | 882 |   0.0800125 |  0.0720365 | 0.0350997 | 0.0407275   |

## Score Spec
| spec            | term                   |   n |   r2_within |       coef |        se |      pvalue |
|:----------------|:-----------------------|----:|------------:|-----------:|----------:|------------:|
| score_collapsed | post_X_treated         | 882 |   0.0989839 |  0.0516711 | 0.0151351 | 0.000699489 |
| score_collapsed | post_X_score           | 882 |   0.0989839 | -0.0758068 | 0.0169637 | 1.00189e-05 |
| score_collapsed | post_X_treated_X_score | 882 |   0.0989839 |  0.0695301 | 0.0497306 | 0.162777    |

## Event-study Specs
| spec           | term                                                             |       coef |        se |      pvalue |   n |   r2_within |
|:---------------|:-----------------------------------------------------------------|-----------:|----------:|------------:|----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.0545908 | 0.0174817 | 0.00191004  | 882 |   0.0302031 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.0266034 | 0.0144473 | 0.0662351   | 882 |   0.0800125 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp             |  0.0720365 | 0.0350997 | 0.0407275   | 882 |   0.0800125 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                | -0.0460625 | 0.0117112 | 9.73628e-05 | 882 |   0.0800125 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                    |  0.0516711 | 0.0151351 | 0.000699489 | 882 |   0.0989839 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score            |  0.0695301 | 0.0497306 | 0.162777    | 882 |   0.0989839 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered | -0.0758068 | 0.0169637 | 1.00189e-05 | 882 |   0.0989839 |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |   n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|----:|
| event_att      | pretrend_att_joint_zero            |                0 |         nan |      nan | 882 |
| event_binary_B | pretrend_baseline_joint_zero       |                0 |         nan |      nan | 882 |
| event_binary_B | pretrend_displacement_joint_zero   |                0 |         nan |      nan | 882 |
| event_score_C  | pretrend_score_baseline_joint_zero |                0 |         nan |      nan | 882 |
| event_score_C  | pretrend_score_slope_joint_zero    |                0 |         nan |      nan | 882 |