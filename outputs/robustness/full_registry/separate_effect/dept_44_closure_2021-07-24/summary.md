# Displacement Effect Estimation Summary

- Sample rows: 12,504
- Unique members: 1,563
- Unique closures: 1
- Event FE units: 1,563
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_44_closure_2021-07-24`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |     n |   r2_within |        coef |         se |     pvalue |
|:-----------------|:----------------------|------:|------------:|------------:|-----------:|-----------:|
| binary_collapsed | post_X_treated        | 12504 |   0.0229984 |  0.004438   | 0.00326083 | 0.17371    |
| binary_collapsed | post_X_disp           | 12504 |   0.0229984 | -0.046617   | 0.00580345 | 1.9984e-15 |
| binary_collapsed | post_X_treated_X_disp | 12504 |   0.0229984 |  0.00138963 | 0.013242   | 0.916436   |

## Score Spec
| spec            | term                   |     n |   r2_within |        coef |         se |   pvalue |
|:----------------|:-----------------------|------:|------------:|------------:|-----------:|---------:|
| score_collapsed | post_X_treated         | 12504 |   0.0317049 |  0.00415489 | 0.00443158 | 0.348613 |
| score_collapsed | post_X_score           | 12504 |   0.0317049 | -0.0711767  | 0.00795357 | 0        |
| score_collapsed | post_X_treated_X_score | 12504 |   0.0317049 | -0.00306347 | 0.0186505  | 0.86955  |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.011462    | 0.00587567 | 0.0512642   | 12504 |  0.00139089 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.000210172 | 0.00523159 | 0.96796     | 12504 |  0.00139089 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00260687  | 0.00510841 | 0.609906    | 12504 |  0.00139089 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0130328   | 0.0058055  | 0.0249137   | 12504 |  0.00139089 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00683244  | 0.00582946 | 0.241354    | 12504 |  0.00139089 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.01344     | 0.00655673 | 0.040551    | 12504 |  0.00139089 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0036019   | 0.00639248 | 0.573203    | 12504 |  0.00139089 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.000719398 | 0.00505449 | 0.886839    | 12504 |  0.0348104  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00297368  | 0.0039173  | 0.447899    | 12504 |  0.0348104  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0063845   | 0.0036471  | 0.080217    | 12504 |  0.0348104  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.000686209 | 0.00431091 | 0.873548    | 12504 |  0.0348104  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0028384   | 0.00437893 | 0.516954    | 12504 |  0.0348104  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00764534  | 0.00548287 | 0.163394    | 12504 |  0.0348104  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00349553  | 0.0051309  | 0.495802    | 12504 |  0.0348104  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0437323   | 0.0188134  | 0.0202247   | 12504 |  0.0348104  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0110071   | 0.0179488  | 0.539802    | 12504 |  0.0348104  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0206965   | 0.0178085  | 0.245344    | 12504 |  0.0348104  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.0397768   | 0.0199123  | 0.0459331   | 12504 |  0.0348104  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.00794772  | 0.0199093  | 0.689804    | 12504 |  0.0348104  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.0141517   | 0.0213325  | 0.507181    | 12504 |  0.0348104  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.0191181   | 0.0211964  | 0.367222    | 12504 |  0.0348104  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.0433036   | 0.00997399 | 1.50503e-05 | 12504 |  0.0348104  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                | -0.00479165  | 0.0101171  | 0.63584     | 12504 |  0.0348104  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0196355   | 0.00823843 | 0.0172724   | 12504 |  0.0348104  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0649697   | 0.00931088 | 4.41402e-12 | 12504 |  0.0348104  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0438179   | 0.00950742 | 4.3792e-06  | 12504 |  0.0348104  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0514247   | 0.00942079 | 5.57228e-08 | 12504 |  0.0348104  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0547155   | 0.0100636  | 6.2795e-08  | 12504 |  0.0348104  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.0124777   | 0.00652371 | 0.0559738   | 12504 |  0.0459176  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.000260419 | 0.00590315 | 0.964818    | 12504 |  0.0459176  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.000181945 | 0.00580576 | 0.975003    | 12504 |  0.0459176  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0116217   | 0.00655362 | 0.0763709   | 12504 |  0.0459176  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00458052  | 0.00657262 | 0.485963    | 12504 |  0.0459176  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0110506   | 0.00728057 | 0.129263    | 12504 |  0.0459176  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00192297  | 0.0071882  | 0.789106    | 12504 |  0.0459176  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.0706851   | 0.0254156  | 0.00548132  | 12504 |  0.0459176  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.0211882   | 0.0237305  | 0.372066    | 12504 |  0.0459176  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.0272328   | 0.0237257  | 0.251219    | 12504 |  0.0459176  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.0474085   | 0.0275112  | 0.0850428   | 12504 |  0.0459176  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.00982155  | 0.0279891  | 0.725706    | 12504 |  0.0459176  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.0144597   | 0.0302733  | 0.632974    | 12504 |  0.0459176  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.0351624   | 0.0303213  | 0.246365    | 12504 |  0.0459176  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.0661284   | 0.0130951  | 4.93995e-07 | 12504 |  0.0459176  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered | -0.0155307   | 0.0134728  | 0.249191    | 12504 |  0.0459176  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0270502   | 0.0111539  | 0.0154141   | 12504 |  0.0459176  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0983956   | 0.0128115  | 2.79776e-14 | 12504 |  0.0459176  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.070999    | 0.0129809  | 5.24827e-08 | 12504 |  0.0459176  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.0806102   | 0.0128548  | 4.63827e-10 | 12504 |  0.0459176  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.0893111   | 0.0134978  | 5.03231e-11 | 12504 |  0.0459176  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |    pvalue |     n |
|:---------------|:-----------------------------------|-----------------:|------------:|----------:|------:|
| event_att      | pretrend_att_joint_zero            |                3 |     7.49637 | 0.0576518 | 12504 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |     3.51496 | 0.318827  | 12504 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |     6.961   | 0.0731513 | 12504 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |     6.15757 | 0.104191  | 12504 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |     9.08504 | 0.0281813 | 12504 |