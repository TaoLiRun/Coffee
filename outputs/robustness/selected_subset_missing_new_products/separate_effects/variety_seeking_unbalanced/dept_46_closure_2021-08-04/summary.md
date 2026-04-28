# Displacement Effect Estimation Summary

- Sample rows: 21,760
- Unique members: 2,720
- Unique closures: 1
- Event FE units: 2,720
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_46_closure_2021-08-04`
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Length-heterogeneity event-study spec skipped: true
- Model type: DDD


## Binary Specs
| spec             | term                  |    n |   r2_within |       coef |        se |    pvalue |
|:-----------------|:----------------------|-----:|------------:|-----------:|----------:|----------:|
| binary_collapsed | post_X_treated        | 6931 |  0.00177026 | 0.00155131 | 0.0538835 | 0.977036  |
| binary_collapsed | post_X_disp           | 6931 |  0.00177026 | 0.0558939  | 0.0225658 | 0.0133525 |
| binary_collapsed | post_X_treated_X_disp | 6931 |  0.00177026 | 0.0442298  | 0.0708009 | 0.532251  |

## Score Spec
| spec            | term                   |    n |   r2_within |      coef |        se |    pvalue |
|:----------------|:-----------------------|-----:|------------:|----------:|----------:|----------:|
| score_collapsed | post_X_treated         | 6931 |  0.00140421 | 0.0128683 | 0.0415355 | 0.756742  |
| score_collapsed | post_X_score           | 6931 |  0.00140421 | 0.0697628 | 0.0321514 | 0.0301644 |
| score_collapsed | post_X_treated_X_score | 6931 |  0.00140421 | 0.0756952 | 0.107001  | 0.479403  |

## Event-study Specs
| spec           | term                                                              |         coef |        se |    pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|----------:|----------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0117275   | 0.083159  | 0.887868  | 6931 |  0.00148403 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00214104  | 0.0847829 | 0.979856  | 6931 |  0.00148403 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0629685   | 0.0778436 | 0.418685  | 6931 |  0.00148403 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.109412    | 0.0834878 | 0.190207  | 6931 |  0.00148403 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00555605  | 0.0777137 | 0.943014  | 6931 |  0.00148403 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0302919   | 0.0852833 | 0.722492  | 6931 |  0.00148403 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0813318   | 0.0856513 | 0.342472  | 6931 |  0.00148403 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0318625   | 0.124616  | 0.798226  | 6931 |  0.00693265 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0709964   | 0.131588  | 0.589591  | 6931 |  0.00693265 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.102945    | 0.12426   | 0.407531  | 6931 |  0.00693265 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0190403   | 0.126765  | 0.880624  | 6931 |  0.00693265 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0178397   | 0.11938   | 0.881228  | 6931 |  0.00693265 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.11107     | 0.130024  | 0.393106  | 6931 |  0.00693265 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0717872   | 0.12775   | 0.574237  | 6931 |  0.00693265 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.031061    | 0.168528  | 0.853795  | 6931 |  0.00693265 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.109665    | 0.172139  | 0.524168  | 6931 |  0.00693265 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.0611673   | 0.159128  | 0.700739  | 6931 |  0.00693265 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.160716    | 0.167988  | 0.338857  | 6931 |  0.00693265 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.0589523   | 0.157374  | 0.708007  | 6931 |  0.00693265 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.167533    | 0.169953  | 0.324397  | 6931 |  0.00693265 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.0127946   | 0.172654  | 0.940936  | 6931 |  0.00693265 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.0329922   | 0.0418949 | 0.431104  | 6931 |  0.00693265 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                | -0.0480992   | 0.0404436 | 0.234498  | 6931 |  0.00693265 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                | -0.0764178   | 0.0434781 | 0.0790003 | 6931 |  0.00693265 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0123036   | 0.0429433 | 0.774526  | 6931 |  0.00693265 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.0782591   | 0.0440963 | 0.0761293 | 6931 |  0.00693265 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.0322512   | 0.0468257 | 0.491079  | 6931 |  0.00693265 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.0435103   | 0.0447303 | 0.330834  | 6931 |  0.00693265 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0364294   | 0.0995498 | 0.714456  | 6931 |  0.00684727 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.039054    | 0.103194  | 0.705145  | 6931 |  0.00684727 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0890493   | 0.102789  | 0.386437  | 6931 |  0.00684727 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0585897   | 0.0975126 | 0.548028  | 6931 |  0.00684727 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00676972  | 0.0943658 | 0.942818  | 6931 |  0.00684727 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0748382   | 0.100495  | 0.456564  | 6931 |  0.00684727 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0723914   | 0.101181  | 0.474427  | 6931 |  0.00684727 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.115802    | 0.235318  | 0.622709  | 6931 |  0.00684727 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.144085    | 0.237741  | 0.54456   | 6931 |  0.00684727 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.0727172   | 0.230018  | 0.751939  | 6931 |  0.00684727 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.284646    | 0.24019   | 0.236154  | 6931 |  0.00684727 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.0905478   | 0.233264  | 0.697936  | 6931 |  0.00684727 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.297593    | 0.242522  | 0.219971  | 6931 |  0.00684727 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.0831447   | 0.244537  | 0.733893  | 6931 |  0.00684727 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered |  0.0697129   | 0.0604074 | 0.24865   | 6931 |  0.00684727 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered | -0.0630422   | 0.0584909 | 0.281277  | 6931 |  0.00684727 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered | -0.0943955   | 0.0633446 | 0.136368  | 6931 |  0.00684727 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -2.77887e-05 | 0.0594461 | 0.999627  | 6931 |  0.00684727 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  |  0.115476    | 0.0624588 | 0.0646622 | 6931 |  0.00684727 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  |  0.00735148  | 0.0645017 | 0.909273  | 6931 |  0.00684727 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  |  0.0936419   | 0.0610789 | 0.125438  | 6931 |  0.00684727 |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                3 |     1.54529 | 0.671858 | 6931 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |     2.33648 | 0.505568 | 6931 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |     1.42971 | 0.698586 | 6931 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |     2.00246 | 0.571896 | 6931 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |     1.1723  | 0.759655 | 6931 |