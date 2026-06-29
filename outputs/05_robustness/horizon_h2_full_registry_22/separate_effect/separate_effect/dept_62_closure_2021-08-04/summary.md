# Displacement Effect Estimation Summary

- Sample rows: 10,576
- Unique members: 2,644
- Unique closures: 1
- Event FE units: 2,644
- Relative periods: [-2, -1, 1, 2]
- Estimation mode: separate_effect=true
- Closure event: `dept_62_closure_2021-08-04`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |     n |   r2_within |        coef |         se |    pvalue |
|:-----------------|:----------------------|------:|------------:|------------:|-----------:|----------:|
| binary_collapsed | post_X_treated        | 10576 |   0.0246578 | -0.00495867 | 0.00301203 | 0.0998236 |
| binary_collapsed | post_X_disp           | 10576 |   0.0246578 | -0.0438832  | 0.00522653 | 0         |
| binary_collapsed | post_X_treated_X_disp | 10576 |   0.0246578 |  0.0105891  | 0.0140152  | 0.449989  |

## Score Spec
| spec            | term                   |     n |   r2_within |        coef |         se |   pvalue |
|:----------------|:-----------------------|------:|------------:|------------:|-----------:|---------:|
| score_collapsed | post_X_treated         | 10576 |   0.0301575 | -0.00341198 | 0.00489023 | 0.485418 |
| score_collapsed | post_X_score           | 10576 |   0.0301575 | -0.0723051  | 0.00819476 | 0        |
| score_collapsed | post_X_treated_X_score | 10576 |   0.0301575 |  0.0136673  | 0.0231057  | 0.554229 |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.000350502 | 0.00539168 | 0.948173    | 10576 | 6.34104e-05 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.000377909 | 0.00430307 | 0.930024    | 10576 | 6.34104e-05 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00346233  | 0.00477229 | 0.468206    | 10576 | 6.34104e-05 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0065908   | 0.004309   | 0.12625     | 10576 | 0.0510747   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00216942  | 0.00303043 | 0.47413     | 10576 | 0.0510747   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00115712  | 0.00369378 | 0.754107    | 10576 | 0.0510747   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.0240073   | 0.0211751  | 0.257       | 10576 | 0.0510747   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.00979484  | 0.0186853  | 0.600183    | 10576 | 0.0510747   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.0126239   | 0.0197288  | 0.52231     | 10576 | 0.0510747   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0607682   | 0.00749677 | 6.66134e-16 | 10576 | 0.0510747   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0248393   | 0.00590376 | 2.66967e-05 | 10576 | 0.0510747   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.00215892  | 0.00690931 | 0.754712    | 10576 | 0.0510747   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00241969  | 0.00710133 | 0.733328    | 10576 | 0.061269    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.000678431 | 0.00654802 | 0.917488    | 10576 | 0.061269    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00508269  | 0.00657538 | 0.439599    | 10576 | 0.061269    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.0214165   | 0.0320958  | 0.50466     | 10576 | 0.061269    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.0237445   | 0.0341369  | 0.486762    | 10576 | 0.061269    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.0178264   | 0.0308889  | 0.563911    | 10576 | 0.061269    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0980299   | 0.0116305  | 0           | 10576 | 0.061269    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0410799   | 0.00950235 | 1.59524e-05 | 10576 | 0.061269    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.00550035  | 0.011203   | 0.623488    | 10576 | 0.061269    |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |     n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|------:|
| event_att      | pretrend_att_joint_zero            |                1 |  0.00422602 | 0.948168 | 10576 |
| event_binary_B | pretrend_baseline_joint_zero       |                1 |  2.3395     | 0.12613  | 10576 |
| event_binary_B | pretrend_displacement_joint_zero   |                1 |  1.2854     | 0.256898 | 10576 |
| event_score_C  | pretrend_score_baseline_joint_zero |                1 |  0.116103   | 0.733301 | 10576 |
| event_score_C  | pretrend_score_slope_joint_zero    |                1 |  0.445244   | 0.504602 | 10576 |