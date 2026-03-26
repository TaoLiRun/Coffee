# Displacement Effect Estimation Summary

- Sample rows: 13,536
- Unique members: 3,384
- Unique closures: 1
- Event FE units: 3,384
- Relative periods: [-2, -1, 1, 2]
- Estimation mode: separate_effect=true
- Closure event: `dept_47_closure_2021-07-30`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |     n |   r2_within |        coef |         se |      pvalue |
|:-----------------|:----------------------|------:|------------:|------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 13536 |   0.0165917 | -0.00481148 | 0.00310439 | 0.12126     |
| binary_collapsed | post_X_disp           | 13536 |   0.0165917 | -0.0390402  | 0.00493862 | 3.55271e-15 |
| binary_collapsed | post_X_treated_X_disp | 13536 |   0.0165917 |  0.0149871  | 0.0193821  | 0.439434    |

## Score Spec
| spec            | term                   |     n |   r2_within |        coef |         se |      pvalue |
|:----------------|:-----------------------|------:|------------:|------------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 13536 |   0.0193681 | -0.00161779 | 0.00610022 | 0.790871    |
| score_collapsed | post_X_score           | 13536 |   0.0193681 | -0.0560078  | 0.00674347 | 2.22045e-16 |
| score_collapsed | post_X_treated_X_score | 13536 |   0.0193681 |  0.00180494 | 0.023748   | 0.93942     |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0101329   | 0.00593546 | 0.0878791   | 13536 | 0.000281521 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.000701069 | 0.00542181 | 0.897124    | 13536 | 0.000281521 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00676359  | 0.00648444 | 0.297       | 13536 | 0.000281521 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00209086  | 0.00394972 | 0.596585    | 13536 | 0.0379932   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00739415  | 0.00377354 | 0.0501392   | 13536 | 0.0379932   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00431967  | 0.0046055  | 0.348343    | 13536 | 0.0379932   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0557217   | 0.0186099  | 0.00277157  | 13536 | 0.0379932   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.0359874   | 0.020722   | 0.0825345   | 13536 | 0.0379932   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.0497084   | 0.0239922  | 0.0383546   | 13536 | 0.0379932   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0523859   | 0.00636327 | 2.22045e-16 | 13536 | 0.0379932   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.022372    | 0.00556193 | 5.88795e-05 | 13536 | 0.0379932   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.00332255  | 0.00654933 | 0.611969    | 13536 | 0.0379932   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0157132   | 0.0063665  | 0.0136319   | 13536 | 0.0397041   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00201499  | 0.00697487 | 0.772681    | 13536 | 0.0397041   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0104627   | 0.00802188 | 0.192231    | 13536 | 0.0397041   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.0780666   | 0.023658   | 0.00097757  | 13536 | 0.0397041   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.0238836   | 0.028586   | 0.403494    | 13536 | 0.0397041   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.0577929   | 0.0317789  | 0.0690619   | 13536 | 0.0397041   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0681832   | 0.00869699 | 5.9952e-15  | 13536 | 0.0397041   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0340228   | 0.00768311 | 9.80048e-06 | 13536 | 0.0397041   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.00980966  | 0.00924031 | 0.288486    | 13536 | 0.0397041   |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |      pvalue |     n |
|:---------------|:-----------------------------------|-----------------:|------------:|------------:|------:|
| event_att      | pretrend_att_joint_zero            |                1 |    2.91449  | 0.0877874   | 13536 |
| event_binary_B | pretrend_baseline_joint_zero       |                1 |    0.280231 | 0.59655     | 13536 |
| event_binary_B | pretrend_displacement_joint_zero   |                1 |    8.96524  | 0.00275164  | 13536 |
| event_score_C  | pretrend_score_baseline_joint_zero |                1 |    6.09158  | 0.0135828   | 13536 |
| event_score_C  | pretrend_score_slope_joint_zero    |                1 |   10.8887   | 0.000967545 | 13536 |