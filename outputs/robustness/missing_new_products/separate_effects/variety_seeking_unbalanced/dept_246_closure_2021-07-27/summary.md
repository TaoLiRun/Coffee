# Displacement Effect Estimation Summary

- Sample rows: 4,320
- Unique members: 540
- Unique closures: 1
- Event FE units: 540
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_246_closure_2021-07-27`
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Length-heterogeneity event-study spec skipped: true
- Model type: DDD


## Binary Specs
| spec             | term                  |    n |   r2_within |      coef |        se |    pvalue |
|:-----------------|:----------------------|-----:|------------:|----------:|----------:|----------:|
| binary_collapsed | post_X_treated        | 1077 |  0.00620687 |  0.149534 | 0.156226  | 0.33932   |
| binary_collapsed | post_X_disp           | 1077 |  0.00620687 |  0.090486 | 0.0587034 | 0.124359  |
| binary_collapsed | post_X_treated_X_disp | 1077 |  0.00620687 | -0.404636 | 0.200253  | 0.0442807 |

## Score Spec
| spec            | term                   |    n |   r2_within |       coef |        se |   pvalue |
|:----------------|:-----------------------|-----:|------------:|-----------:|----------:|---------:|
| score_collapsed | post_X_treated         | 1077 |  0.00459475 |  0.0505183 | 0.123995  | 0.684014 |
| score_collapsed | post_X_score           | 1077 |  0.00459475 |  0.105893  | 0.0832454 | 0.204418 |
| score_collapsed | post_X_treated_X_score | 1077 |  0.00459475 | -0.613073  | 0.393688  | 0.120552 |

## Event-study Specs
| spec           | term                                                              |        coef |       se |     pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|------------:|---------:|-----------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.130435   | 0.155968 | 0.403711   | 1077 |  0.00252279 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0979386  | 0.13241  | 0.46013    | 1077 |  0.00252279 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0519794  | 0.142314 | 0.715207   | 1077 |  0.00252279 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.0510557  | 0.225381 | 0.820955   | 1077 |  0.00252279 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0458191  | 0.159593 | 0.774251   | 1077 |  0.00252279 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.06691    | 0.179634 | 0.709821   | 1077 |  0.00252279 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0652877  | 0.180395 | 0.717691   | 1077 |  0.00252279 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.0379848  | 0.258011 | 0.883064   | 1077 |  0.0312204  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0691094  | 0.116658 | 0.55406    | 1077 |  0.0312204  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0215335  | 0.198571 | 0.913723   | 1077 |  0.0312204  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0407358  | 0.271644 | 0.880905   | 1077 |  0.0312204  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.153588   | 0.143359 | 0.284945   | 1077 |  0.0312204  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0821498  | 0.214658 | 0.702236   | 1077 |  0.0312204  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.370122   | 0.217481 | 0.0899044  | 1077 |  0.0312204  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             | -0.338671   | 0.319728 | 0.290409   | 1077 |  0.0312204  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             | -0.0813636  | 0.302113 | 0.787888   | 1077 |  0.0312204  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.11822    | 0.293557 | 0.687468   | 1077 |  0.0312204  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.00829501 | 0.322443 | 0.979495   | 1077 |  0.0312204  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.755954   | 0.260256 | 0.00397298 | 1077 |  0.0312204  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              | -0.293408   | 0.350836 | 0.403701   | 1077 |  0.0312204  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.743104   | 0.367488 | 0.0441253  | 1077 |  0.0312204  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.131795   | 0.11396  | 0.248472   | 1077 |  0.0312204  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.121111   | 0.107027 | 0.258783   | 1077 |  0.0312204  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                | -0.183885   | 0.109036 | 0.0928321  | 1077 |  0.0312204  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  0.0650981  | 0.119554 | 0.586529   | 1077 |  0.0312204  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.0450539  | 0.1039   | 0.664896   | 1077 |  0.0312204  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.143562   | 0.105845 | 0.176095   | 1077 |  0.0312204  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.199265   | 0.116325 | 0.0878307  | 1077 |  0.0312204  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0911808  | 0.186685 | 0.625638   | 1077 |  0.0281805  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0422641  | 0.134707 | 0.753947   | 1077 |  0.0281805  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0027759  | 0.184556 | 0.98801    | 1077 |  0.0281805  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0249732  | 0.222642 | 0.910772   | 1077 |  0.0281805  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0474462  | 0.139049 | 0.733197   | 1077 |  0.0281805  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0201323  | 0.183322 | 0.912632   | 1077 |  0.0281805  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.149745   | 0.180486 | 0.407434   | 1077 |  0.0281805  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            | -0.146318   | 0.371877 | 0.694284   | 1077 |  0.0281805  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            | -0.481557   | 0.232736 | 0.0394631  | 1077 |  0.0281805  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.0136188  | 0.355616 | 0.969479   | 1077 |  0.0281805  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.0625754  | 0.394702 | 0.874148   | 1077 |  0.0281805  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -1.36912    | 0.461483 | 0.00327193 | 1077 |  0.0281805  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             | -0.89305    | 0.477881 | 0.0627102  | 1077 |  0.0281805  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             | -1.64671    | 0.535591 | 0.00231861 | 1077 |  0.0281805  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered |  0.222033   | 0.172704 | 0.199646   | 1077 |  0.0281805  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.292803   | 0.162302 | 0.0723069  | 1077 |  0.0281805  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered | -0.169029   | 0.16191  | 0.29741    | 1077 |  0.0281805  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  |  0.124746   | 0.162798 | 0.444173   | 1077 |  0.0281805  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  |  0.0888031  | 0.147129 | 0.546622   | 1077 |  0.0281805  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  |  0.286316   | 0.151052 | 0.0590698  | 1077 |  0.0281805  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  |  0.341105   | 0.167856 | 0.0430943  | 1077 |  0.0281805  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                3 |    2.98808  | 0.393467 | 1077 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |    0.480587 | 0.923135 | 1077 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |    3.35327  | 0.340296 | 1077 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |    0.402529 | 0.939719 | 1077 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |    4.88441  | 0.18046  | 1077 |