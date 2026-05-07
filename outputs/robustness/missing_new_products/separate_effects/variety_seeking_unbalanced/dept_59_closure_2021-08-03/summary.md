# Displacement Effect Estimation Summary

- Sample rows: 25,488
- Unique members: 3,186
- Unique closures: 1
- Event FE units: 3,186
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_59_closure_2021-08-03`
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Length-heterogeneity event-study spec skipped: true
- Model type: DDD


## Binary Specs
| spec             | term                  |    n |   r2_within |       coef |        se |   pvalue |
|:-----------------|:----------------------|-----:|------------:|-----------:|----------:|---------:|
| binary_collapsed | post_X_treated        | 8706 |  0.00122345 |  0.0454934 | 0.0451218 | 0.313466 |
| binary_collapsed | post_X_disp           | 8706 |  0.00122345 |  0.0560038 | 0.0221951 | 0.011706 |
| binary_collapsed | post_X_treated_X_disp | 8706 |  0.00122345 | -0.0301661 | 0.0589706 | 0.609028 |

## Score Spec
| spec            | term                   |    n |   r2_within |       coef |        se |     pvalue |
|:----------------|:-----------------------|-----:|------------:|-----------:|----------:|-----------:|
| score_collapsed | post_X_treated         | 8706 |  0.00140326 |  0.0338729 | 0.0400495 | 0.39778    |
| score_collapsed | post_X_score           | 8706 |  0.00140326 |  0.0946922 | 0.0329405 | 0.00408849 |
| score_collapsed | post_X_treated_X_score | 8706 |  0.00140326 | -0.0176811 | 0.0983809 | 0.85739    |

## Event-study Specs
| spec           | term                                                              |       coef |        se |     pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|-----------:|----------:|-----------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0965249 | 0.0580247 | 0.0963693  | 8706 | 0.000963743 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.104216  | 0.058986  | 0.0774174  | 8706 | 0.000963743 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.089516  | 0.0573415 | 0.118661   | 8706 | 0.000963743 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.0964676 | 0.0592457 | 0.10363    | 8706 | 0.000963743 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0474134 | 0.059679  | 0.427016   | 8706 | 0.000963743 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0414215 | 0.0617744 | 0.5026     | 8706 | 0.000963743 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0331    | 0.0604171 | 0.583852   | 8706 | 0.000963743 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.166789  | 0.0967973 | 0.0850322  | 8706 | 0.00382964  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.14597   | 0.112427  | 0.194316   | 8706 | 0.00382964  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.131441  | 0.108665  | 0.226579   | 8706 | 0.00382964  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.137227  | 0.0966776 | 0.155934   | 8706 | 0.00382964  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0516164 | 0.0991582 | 0.602742   | 8706 | 0.00382964  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0968931 | 0.105295  | 0.35758    | 8706 | 0.00382964  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0249341 | 0.103597  | 0.809825   | 8706 | 0.00382964  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.120204  | 0.121218  | 0.3215     | 8706 | 0.00382964  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0664651 | 0.130863  | 0.611583   | 8706 | 0.00382964  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0720674 | 0.126901  | 0.570166   | 8706 | 0.00382964  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.0669634 | 0.122139  | 0.583578   | 8706 | 0.00382964  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.0116443 | 0.124526  | 0.925509   | 8706 | 0.00382964  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.108721  | 0.129749  | 0.402172   | 8706 | 0.00382964  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.0153382 | 0.12718   | 0.904018   | 8706 | 0.00382964  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.0441022 | 0.0404413 | 0.275616   | 8706 | 0.00382964  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.0680987 | 0.0403707 | 0.0917945  | 8706 | 0.00382964  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0745043 | 0.0445918 | 0.0949195  | 8706 | 0.00382964  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  0.0612749 | 0.0424001 | 0.148572   | 8706 | 0.00382964  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.113928  | 0.0415629 | 0.00617915 | 8706 | 0.00382964  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.123532  | 0.0451263 | 0.00624733 | 8706 | 0.00382964  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.1128    | 0.0429732 | 0.00873496 | 8706 | 0.00382964  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.120719  | 0.0882972 | 0.171724   | 8706 | 0.00329507  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.13125   | 0.099153  | 0.185754   | 8706 | 0.00329507  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.094476  | 0.101529  | 0.352212   | 8706 | 0.00329507  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.13419   | 0.0887402 | 0.130652   | 8706 | 0.00329507  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0571816 | 0.092376  | 0.535982   | 8706 | 0.00329507  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0392527 | 0.0930395 | 0.67315    | 8706 | 0.00329507  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0202571 | 0.0941553 | 0.829676   | 8706 | 0.00329507  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.104124  | 0.215479  | 0.628992   | 8706 | 0.00329507  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.107111  | 0.235731  | 0.649606   | 8706 | 0.00329507  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.0378891 | 0.242538  | 0.875876   | 8706 | 0.00329507  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.189258  | 0.228652  | 0.407935   | 8706 | 0.00329507  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.0675066 | 0.2238    | 0.76296    | 8706 | 0.00329507  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.0247378 | 0.217778  | 0.909573   | 8706 | 0.00329507  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             | -0.030535  | 0.221336  | 0.890288   | 8706 | 0.00329507  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered |  0.0766017 | 0.0628552 | 0.223104   | 8706 | 0.00329507  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.0837579 | 0.0638474 | 0.189726   | 8706 | 0.00329507  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.100371  | 0.0704027 | 0.154125   | 8706 | 0.00329507  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  |  0.103231  | 0.0645764 | 0.110072   | 8706 | 0.00329507  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  |  0.172711  | 0.0634157 | 0.0065171  | 8706 | 0.00329507  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  |  0.190036  | 0.0674662 | 0.00489968 | 8706 | 0.00329507  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  |  0.174196  | 0.0638945 | 0.00646184 | 8706 | 0.00329507  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                3 |    3.70554  | 0.295066 | 8706 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |    3.01829  | 0.388814 | 8706 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |    1.02719  | 0.794673 | 8706 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |    2.0776   | 0.556457 | 8706 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |    0.324147 | 0.955425 | 8706 |