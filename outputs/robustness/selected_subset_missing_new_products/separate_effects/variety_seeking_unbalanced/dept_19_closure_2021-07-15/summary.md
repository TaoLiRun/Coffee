# Displacement Effect Estimation Summary

- Sample rows: 26,408
- Unique members: 3,301
- Unique closures: 1
- Event FE units: 3,301
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_19_closure_2021-07-15`
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Length-heterogeneity event-study spec skipped: true
- Model type: DDD


## Binary Specs
| spec             | term                  |    n |   r2_within |       coef |        se |   pvalue |
|:-----------------|:----------------------|-----:|------------:|-----------:|----------:|---------:|
| binary_collapsed | post_X_treated        | 6476 | 0.000700729 |  0.0557411 | 0.0478219 | 0.243943 |
| binary_collapsed | post_X_disp           | 6476 | 0.000700729 |  0.0343446 | 0.0229848 | 0.135305 |
| binary_collapsed | post_X_treated_X_disp | 6476 | 0.000700729 | -0.0794524 | 0.0587084 | 0.17613  |

## Score Spec
| spec            | term                   |    n |   r2_within |       coef |        se |   pvalue |
|:----------------|:-----------------------|-----:|------------:|-----------:|----------:|---------:|
| score_collapsed | post_X_treated         | 6476 |  0.00133566 |  0.0427018 | 0.0386097 | 0.268891 |
| score_collapsed | post_X_score           | 6476 |  0.00133566 |  0.0943628 | 0.0376794 | 0.012362 |
| score_collapsed | post_X_treated_X_score | 6476 |  0.00133566 | -0.124937  | 0.0878121 | 0.154989 |

## Event-study Specs
| spec           | term                                                              |        coef |        se |      pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|------------:|----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0672184  | 0.0481684 | 0.163054    | 6476 |  0.00084384 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0842309  | 0.0623901 | 0.177177    | 6476 |  0.00084384 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0614094  | 0.0483128 | 0.203878    | 6476 |  0.00084384 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.0166769  | 0.0597071 | 0.78004     | 6476 |  0.00084384 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0146516  | 0.0557196 | 0.79262     | 6476 |  0.00084384 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0611275  | 0.0525395 | 0.24481     | 6476 |  0.00084384 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0384064  | 0.0526649 | 0.465945    | 6476 |  0.00084384 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0314428  | 0.071055  | 0.658175    | 6476 |  0.00543583 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0999143  | 0.10681   | 0.349695    | 6476 |  0.00543583 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.102426   | 0.0803343 | 0.202489    | 6476 |  0.00543583 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0292086  | 0.0919877 | 0.750883    | 6476 |  0.00543583 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00666408 | 0.080798  | 0.934276    | 6476 |  0.00543583 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.018687   | 0.082108  | 0.819992    | 6476 |  0.00543583 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0213367  | 0.0812738 | 0.792946    | 6476 |  0.00543583 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             | -0.0652265  | 0.096537  | 0.499348    | 6476 |  0.00543583 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0155993  | 0.13261   | 0.906372    | 6476 |  0.00543583 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0676059  | 0.0997213 | 0.497898    | 6476 |  0.00543583 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0898164  | 0.118709  | 0.449392    | 6476 |  0.00543583 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.043635   | 0.110492  | 0.692956    | 6476 |  0.00543583 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              | -0.0876102  | 0.103119  | 0.395666    | 6476 |  0.00543583 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.118003   | 0.105386  | 0.262993    | 6476 |  0.00543583 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.0949395  | 0.0395185 | 0.0163961   | 6476 |  0.00543583 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.0521384  | 0.0408768 | 0.202309    | 6476 |  0.00543583 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.00655279 | 0.041599  | 0.874852    | 6476 |  0.00543583 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  0.0453284  | 0.0449583 | 0.313489    | 6476 |  0.00543583 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.0287056  | 0.0440278 | 0.514499    | 6476 |  0.00543583 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.0503528  | 0.0423277 | 0.234375    | 6476 |  0.00543583 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.150433   | 0.0416477 | 0.000312775 | 6476 |  0.00543583 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.058785   | 0.0606047 | 0.3322      | 6476 |  0.00727738 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.104636   | 0.0884448 | 0.236951    | 6476 |  0.00727738 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0910114  | 0.0696017 | 0.191187    | 6476 |  0.00727738 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00382515 | 0.0743827 | 0.958993    | 6476 |  0.00727738 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0157376  | 0.0683918 | 0.818035    | 6476 |  0.00727738 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0348091  | 0.067765  | 0.607548    | 6476 |  0.00727738 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00225604 | 0.0660509 | 0.972757    | 6476 |  0.00727738 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            | -0.0207367  | 0.153479  | 0.89254     | 6476 |  0.00727738 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.0736241  | 0.200678  | 0.713757    | 6476 |  0.00727738 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.124787   | 0.164902  | 0.449313    | 6476 |  0.00727738 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.0501427  | 0.167207  | 0.764302    | 6476 |  0.00727738 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.0305958  | 0.164823  | 0.852759    | 6476 |  0.00727738 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             | -0.124071   | 0.15759   | 0.431214    | 6476 |  0.00727738 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             | -0.193527   | 0.157535  | 0.219446    | 6476 |  0.00727738 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered |  0.14173    | 0.0655492 | 0.030745    | 6476 |  0.00727738 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.0467681  | 0.0693888 | 0.500404    | 6476 |  0.00727738 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0302339  | 0.0677646 | 0.655539    | 6476 |  0.00727738 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  |  0.0493384  | 0.0719698 | 0.493096    | 6476 |  0.00727738 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  |  0.0461095  | 0.0731845 | 0.528752    | 6476 |  0.00727738 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  |  0.142493   | 0.0678741 | 0.035934    | 6476 |  0.00727738 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  |  0.314089   | 0.0660112 | 2.1224e-06  | 6476 |  0.00727738 |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                3 |    2.73291  | 0.434664 | 6476 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |    2.11749  | 0.548383 | 6476 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |    1.82654  | 0.609177 | 6476 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |    2.35547  | 0.501978 | 6476 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |    0.979934 | 0.806107 | 6476 |