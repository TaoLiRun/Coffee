# Displacement Effect Estimation Summary

- Sample rows: 8,872
- Unique members: 2,218
- Unique closures: 1
- Event FE units: 2,218
- Relative periods: [-2, -1, 1, 2]
- Estimation mode: separate_effect=true
- Closure event: `dept_121_closure_2021-08-03`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |        coef |         se |      pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 8872 |   0.0256627 |  0.00455327 | 0.0026499  | 0.0858852   |
| binary_collapsed | post_X_disp           | 8872 |   0.0256627 | -0.0355932  | 0.00452594 | 5.77316e-15 |
| binary_collapsed | post_X_treated_X_disp | 8872 |   0.0256627 |  0.00989459 | 0.0107181  | 0.356022    |

## Score Spec
| spec            | term                   |    n |   r2_within |        coef |         se |      pvalue |
|:----------------|:-----------------------|-----:|------------:|------------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 8872 |   0.0306549 |  0.00705364 | 0.00350259 | 0.044147    |
| score_collapsed | post_X_score           | 8872 |   0.0306549 | -0.0552799  | 0.0069307  | 2.44249e-15 |
| score_collapsed | post_X_treated_X_score | 8872 |   0.0306549 |  0.0116496  | 0.0153371  | 0.447592    |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  1.12955e-05 | 0.00404235 | 0.997771    | 8872 |  0.00124855 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00476228  | 0.00415282 | 0.251606    | 8872 |  0.00124855 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0104188   | 0.00398901 | 0.00906515  | 8872 |  0.00124855 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00168857  | 0.00254985 | 0.507896    | 8872 |  0.0474862  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00429662  | 0.00324417 | 0.185502    | 8872 |  0.0474862  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00649849  | 0.0029644  | 0.0284701   | 8872 |  0.0474862  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.00347337  | 0.0142906  | 0.807987    | 8872 |  0.0474862  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.000817613 | 0.0141784  | 0.95402     | 8872 |  0.0474862  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.0154982   | 0.0139358  | 0.266209    | 8872 |  0.0474862  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.044949    | 0.00659262 | 1.18547e-11 | 8872 |  0.0474862  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0143307   | 0.00546171 | 0.00875396  | 8872 |  0.0474862  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0119067   | 0.00594343 | 0.0452634   | 8872 |  0.0474862  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00112316  | 0.00440982 | 0.798982    | 8872 |  0.0548694  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00438087  | 0.00460282 | 0.341312    | 8872 |  0.0548694  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0108496   | 0.00443537 | 0.0145163   | 8872 |  0.0548694  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.000923247 | 0.0217516  | 0.966148    | 8872 |  0.0548694  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.000433891 | 0.0215324  | 0.983925    | 8872 |  0.0548694  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.0237886   | 0.0206114  | 0.248565    | 8872 |  0.0548694  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0664851   | 0.0100789  | 5.24991e-11 | 8872 |  0.0548694  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.024266    | 0.00850818 | 0.00438369  | 8872 |  0.0548694  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0198087   | 0.00933786 | 0.0340046   | 8872 |  0.0548694  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                1 | 7.80803e-06 | 0.99777  | 8872 |
| event_binary_B | pretrend_baseline_joint_zero       |                1 | 0.438541    | 0.507828 | 8872 |
| event_binary_B | pretrend_displacement_joint_zero   |                1 | 0.0590748   | 0.807964 | 8872 |
| event_score_C  | pretrend_score_baseline_joint_zero |                1 | 0.0648699   | 0.798958 | 8872 |
| event_score_C  | pretrend_score_slope_joint_zero    |                1 | 0.00180158  | 0.966144 | 8872 |