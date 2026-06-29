# Displacement Effect Estimation Summary

- Sample rows: 21,152
- Unique members: 2,644
- Unique closures: 1
- Event FE units: 2,644
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_62_closure_2021-08-04`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |     n |   r2_within |         coef |         se |      pvalue |
|:-----------------|:----------------------|------:|------------:|-------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 21152 |   0.0153239 | -0.000655315 | 0.00291932 | 0.822405    |
| binary_collapsed | post_X_disp           | 21152 |   0.0153239 | -0.0396665   | 0.00519568 | 3.15303e-14 |
| binary_collapsed | post_X_treated_X_disp | 21152 |   0.0153239 | -0.00788711  | 0.0148501  | 0.595383    |

## Score Spec
| spec            | term                   |     n |   r2_within |        coef |         se |   pvalue |
|:----------------|:-----------------------|------:|------------:|------------:|-----------:|---------:|
| score_collapsed | post_X_treated         | 21152 |    0.021416 | -0.00485781 | 0.00489733 | 0.321323 |
| score_collapsed | post_X_score           | 21152 |    0.021416 | -0.070014   | 0.00800525 | 0        |
| score_collapsed | post_X_treated_X_score | 21152 |    0.021416 | -0.0148213  | 0.0227402  | 0.514608 |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00523539  | 0.00635501 | 0.410115    | 21152 | 0.000238897 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00866451  | 0.00612366 | 0.157208    | 21152 | 0.000238897 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.000350502 | 0.00539181 | 0.948174    | 21152 | 0.000238897 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.000377909 | 0.00430318 | 0.930026    | 21152 | 0.000238897 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00346233  | 0.0047724  | 0.468216    | 21152 | 0.000238897 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.00216257  | 0.00615687 | 0.725433    | 21152 | 0.000238897 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00182788  | 0.00592025 | 0.757536    | 21152 | 0.000238897 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.000799411 | 0.00509123 | 0.875243    | 21152 | 0.0264223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.006711    | 0.00452778 | 0.138411    | 21152 | 0.0264223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0065908   | 0.00430931 | 0.126277    | 21152 | 0.0264223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00216942  | 0.00303064 | 0.474161    | 21152 | 0.0264223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00115712  | 0.00369404 | 0.754124    | 21152 | 0.0264223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00167558  | 0.00473264 | 0.723332    | 21152 | 0.0264223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00029109  | 0.00409897 | 0.943391    | 21152 | 0.0264223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.026987    | 0.0250365  | 0.281173    | 21152 | 0.0264223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             | -0.00514173  | 0.0258321  | 0.842244    | 21152 | 0.0264223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.0240073   | 0.0211766  | 0.257034    | 21152 | 0.0264223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.00979484  | 0.0186866  | 0.600209    | 21152 | 0.0264223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.0126239   | 0.0197302  | 0.52234     | 21152 | 0.0264223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              | -0.0202367   | 0.0256909  | 0.430943    | 21152 | 0.0264223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.0106446   | 0.0259127  | 0.681261    | 21152 | 0.0264223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.0218094   | 0.0079168  | 0.0059126   | 21152 | 0.0264223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.0345766   | 0.0081041  | 2.05496e-05 | 21152 | 0.0264223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0607682   | 0.0074973  | 6.66134e-16 | 21152 | 0.0264223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0248393   | 0.00590418 | 2.67317e-05 | 21152 | 0.0264223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.00215892  | 0.0069098  | 0.754729    | 21152 | 0.0264223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.00152925  | 0.0074244  | 0.836826    | 21152 | 0.0264223   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.016043    | 0.00714748 | 0.0248787   | 21152 | 0.0264223   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00977912  | 0.00853126 | 0.251788    | 21152 | 0.0345154   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00684213  | 0.00875369 | 0.434503    | 21152 | 0.0345154   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00241969  | 0.00710183 | 0.733346    | 21152 | 0.0345154   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.000678431 | 0.00654849 | 0.917494    | 21152 | 0.0345154   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00508269  | 0.00657585 | 0.439631    | 21152 | 0.0345154   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.00456588  | 0.00900715 | 0.612255    | 21152 | 0.0345154   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00510442  | 0.00863079 | 0.554289    | 21152 | 0.0345154   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.0357414   | 0.0380123  | 0.347171    | 21152 | 0.0345154   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            | -0.00739085  | 0.0416613  | 0.859205    | 21152 | 0.0345154   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.0214165   | 0.0320981  | 0.504691    | 21152 | 0.0345154   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.0237445   | 0.0341393  | 0.486793    | 21152 | 0.0345154   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.0178264   | 0.0308911  | 0.563939    | 21152 | 0.0345154   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             | -0.0311578   | 0.045566   | 0.494164    | 21152 | 0.0345154   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             | -0.0271114   | 0.0430401  | 0.528808    | 21152 | 0.0345154   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered |  0.0447696   | 0.0121813  | 0.000242321 | 21152 | 0.0345154   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.0627081   | 0.0123079  | 3.73467e-07 | 21152 | 0.0345154   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0980299   | 0.0116313  | 0           | 21152 | 0.0345154   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0410799   | 0.00950303 | 1.59745e-05 | 21152 | 0.0345154   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.00550035  | 0.0112038  | 0.623513    | 21152 | 0.0345154   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  |  0.00156005  | 0.0117735  | 0.894595    | 21152 | 0.0345154   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.0295281   | 0.0116282  | 0.0111627   | 21152 | 0.0345154   |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |    pvalue |     n |
|:---------------|:-----------------------------------|-----------------:|------------:|----------:|------:|
| event_att      | pretrend_att_joint_zero            |                3 |     4.90472 | 0.178908  | 21152 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |     7.55766 | 0.0560953 | 21152 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |     4.09042 | 0.251865  | 21152 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |     3.63375 | 0.303825  | 21152 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |     2.19467 | 0.532999  | 21152 |