# Displacement Effect Estimation Summary

- Sample rows: 24,760
- Unique members: 3,095
- Unique closures: 1
- Event FE units: 3,095
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_124_closure_2021-07-22`
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Length-heterogeneity event-study spec skipped: true
- Model type: DDD


## Binary Specs
| spec             | term                  |     n |   r2_within |       coef |        se |   pvalue |
|:-----------------|:----------------------|------:|------------:|-----------:|----------:|---------:|
| binary_collapsed | post_X_treated        | 10821 | 0.000147217 |  0.0146958 | 0.0336486 | 0.662339 |
| binary_collapsed | post_X_disp           | 10821 | 0.000147217 |  0.0234772 | 0.0235258 | 0.318421 |
| binary_collapsed | post_X_treated_X_disp | 10821 | 0.000147217 | -0.0256246 | 0.0380257 | 0.50046  |

## Score Spec
| spec            | term                   |     n |   r2_within |         coef |        se |   pvalue |
|:----------------|:-----------------------|------:|------------:|-------------:|----------:|---------:|
| score_collapsed | post_X_treated         | 10821 | 4.36923e-05 |  0.000168407 | 0.0295797 | 0.995458 |
| score_collapsed | post_X_score           | 10821 | 4.36923e-05 | -0.0101553   | 0.0353327 | 0.773819 |
| score_collapsed | post_X_treated_X_score | 10821 | 4.36923e-05 | -0.00897553  | 0.0564795 | 0.873749 |

## Event-study Specs
| spec           | term                                                              |         coef |        se |    pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|----------:|----------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00232056  | 0.0281946 | 0.934412  | 10821 |  0.00205446 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.00602549  | 0.0286664 | 0.833536  | 10821 |  0.00205446 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00193737  | 0.0271346 | 0.943087  | 10821 |  0.00205446 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0716687   | 0.028747  | 0.0127358 | 10821 |  0.00205446 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.037981    | 0.0306221 | 0.214989  | 10821 |  0.00205446 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0289186   | 0.0296607 | 0.329676  | 10821 |  0.00205446 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0198729   | 0.0291681 | 0.495738  | 10821 |  0.00205446 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0656426   | 0.0678538 | 0.333443  | 10821 |  0.00398973 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0551542   | 0.0654821 | 0.399722  | 10821 |  0.00398973 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0113385   | 0.0652787 | 0.862122  | 10821 |  0.00398973 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.101768    | 0.0630972 | 0.106914  | 10821 |  0.00398973 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0918358   | 0.0652348 | 0.159338  | 10821 |  0.00398973 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0125382   | 0.0655043 | 0.848222  | 10821 |  0.00398973 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0850466   | 0.0655461 | 0.19459   | 10821 |  0.00398973 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0758274   | 0.0744617 | 0.308627  | 10821 |  0.00398973 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0741829   | 0.0728662 | 0.308755  | 10821 |  0.00398973 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0158329   | 0.0717437 | 0.825357  | 10821 |  0.00398973 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0456575   | 0.0708743 | 0.519509  | 10821 |  0.00398973 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.0676377   | 0.0739287 | 0.36034   | 10821 |  0.00398973 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              | -0.0303706   | 0.0733866 | 0.679029  | 10821 |  0.00398973 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.0829705   | 0.0730606 | 0.25623   | 10821 |  0.00398973 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.0399016   | 0.0444385 | 0.369333  | 10821 |  0.00398973 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.00185076  | 0.0434134 | 0.965999  | 10821 |  0.00398973 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.00873403  | 0.0437767 | 0.84188   | 10821 |  0.00398973 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  0.0264717   | 0.0435281 | 0.543149  | 10821 |  0.00398973 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.0321543   | 0.0438412 | 0.463376  | 10821 |  0.00398973 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.0657996   | 0.0470663 | 0.162246  | 10821 |  0.00398973 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.0218715   | 0.0454209 | 0.630188  | 10821 |  0.00398973 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0573975   | 0.0571027 | 0.314927  | 10821 |  0.00378598 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0282873   | 0.0567729 | 0.618355  | 10821 |  0.00378598 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0108275   | 0.0567161 | 0.848616  | 10821 |  0.00378598 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0844357   | 0.054023  | 0.118204  | 10821 |  0.00378598 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0757135   | 0.0565188 | 0.180507  | 10821 |  0.00378598 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0348168   | 0.0558453 | 0.533051  | 10821 |  0.00378598 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0657847   | 0.055744  | 0.238078  | 10821 |  0.00378598 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.120764    | 0.107192  | 0.260027  | 10821 |  0.00378598 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.0726839   | 0.107297  | 0.498217  | 10821 |  0.00378598 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.0271329   | 0.107133  | 0.800088  | 10821 |  0.00378598 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.0407885   | 0.102526  | 0.690791  | 10821 |  0.00378598 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.0885456   | 0.10793   | 0.412078  | 10821 |  0.00378598 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             | -0.000545938 | 0.105674  | 0.995878  | 10821 |  0.00378598 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.108888    | 0.104754  | 0.298704  | 10821 |  0.00378598 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered |  0.0767168   | 0.064675  | 0.235674  | 10821 |  0.00378598 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.031003    | 0.0647964 | 0.632364  | 10821 |  0.00378598 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0954589   | 0.066384  | 0.15058   | 10821 |  0.00378598 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  |  0.0285792   | 0.063101  | 0.650656  | 10821 |  0.00378598 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  |  0.0269832   | 0.0645654 | 0.676046  | 10821 |  0.00378598 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  |  0.0837667   | 0.0690758 | 0.225381  | 10821 |  0.00378598 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  |  0.0197184   | 0.0650482 | 0.761815  | 10821 |  0.00378598 |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |     n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|------:|
| event_att      | pretrend_att_joint_zero            |                3 |     0.10386 | 0.99137  | 10821 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |     1.29175 | 0.731092 | 10821 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |     1.59076 | 0.661486 | 10821 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |     1.7989  | 0.615175 | 10821 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |     2.36547 | 0.500096 | 10821 |