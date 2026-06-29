# Displacement Effect Estimation Summary

- Sample rows: 12,616
- Unique members: 1,577
- Unique closures: 1
- Event FE units: 1,577
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_182_closure_2021-08-03`
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Length-heterogeneity event-study spec skipped: true
- Model type: DDD


## Binary Specs
| spec             | term                  |     n |   r2_within |        coef |         se |      pvalue |
|:-----------------|:----------------------|------:|------------:|------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 12616 |  0.00769001 |  0.00477702 | 0.00375354 | 0.203323    |
| binary_collapsed | post_X_disp           | 12616 |  0.00769001 | -0.0263155  | 0.00586179 | 7.66352e-06 |
| binary_collapsed | post_X_treated_X_disp | 12616 |  0.00769001 |  0.0201587  | 0.0153805  | 0.190162    |

## Score Spec
| spec            | term                   |     n |   r2_within |       coef |         se |      pvalue |
|:----------------|:-----------------------|------:|------------:|-----------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 12616 |   0.0124553 |  0.0103389 | 0.00487665 | 0.0341554   |
| score_collapsed | post_X_score           | 12616 |   0.0124553 | -0.0470806 | 0.00875829 | 8.78079e-08 |
| score_collapsed | post_X_treated_X_score | 12616 |   0.0124553 |  0.0349408 | 0.0273213  | 0.201125    |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00736391  | 0.00687893 | 0.284557    | 12616 |  0.00178558 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.00278351  | 0.00655331 | 0.671077    | 12616 |  0.00178558 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0037879   | 0.00534262 | 0.478431    | 12616 |  0.00178558 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0113426   | 0.0052789  | 0.0318123   | 12616 |  0.00178558 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00989497  | 0.00490832 | 0.0439739   | 12616 |  0.00178558 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0153246   | 0.00675837 | 0.0234942   | 12616 |  0.00178558 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00356021  | 0.006382   | 0.577025    | 12616 |  0.00178558 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0100755   | 0.005586   | 0.071467    | 12616 |  0.0117933  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00201805  | 0.00588585 | 0.731746    | 12616 |  0.0117933  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.000176288 | 0.00384051 | 0.963394    | 12616 |  0.0117933  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00957064  | 0.00512843 | 0.0622002   | 12616 |  0.0117933  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00184847  | 0.00430117 | 0.66743     | 12616 |  0.0117933  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00497885  | 0.00607701 | 0.412743    | 12616 |  0.0117933  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00551027  | 0.00536741 | 0.304759    | 12616 |  0.0117933  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0112613   | 0.0236109  | 0.633462    | 12616 |  0.0117933  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0204592   | 0.0211868  | 0.334364    | 12616 |  0.0117933  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0118801   | 0.019175   | 0.535635    | 12616 |  0.0117933  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.010645    | 0.0161391  | 0.509623    | 12616 |  0.0117933  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.0532332   | 0.0159142  | 0.000842107 | 12616 |  0.0117933  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.047857    | 0.0216831  | 0.02745     | 12616 |  0.0117933  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.0125003   | 0.0215731  | 0.562375    | 12616 |  0.0117933  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.000102989 | 0.00907668 | 0.990948    | 12616 |  0.0117933  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                | -0.00261107  | 0.00902143 | 0.77229     | 12616 |  0.0117933  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0169385   | 0.00788677 | 0.0318891   | 12616 |  0.0117933  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0176351   | 0.00744613 | 0.0179872   | 12616 |  0.0117933  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0235989   | 0.0079237  | 0.0029431   | 12616 |  0.0117933  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0259582   | 0.00839104 | 0.00201239  | 12616 |  0.0117933  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0236396   | 0.00918504 | 0.0101523   | 12616 |  0.0117933  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00788322  | 0.00742873 | 0.288771    | 12616 |  0.0162549  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.00276081  | 0.00698609 | 0.692758    | 12616 |  0.0162549  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00319504  | 0.00578015 | 0.580505    | 12616 |  0.0162549  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.01267     | 0.00563917 | 0.0247913   | 12616 |  0.0162549  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.012113    | 0.00518073 | 0.0195074   | 12616 |  0.0162549  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0172409   | 0.00718266 | 0.0164946   | 12616 |  0.0162549  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0025958   | 0.00687871 | 0.705951    | 12616 |  0.0162549  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            | -0.0068178   | 0.040177   | 0.865273    | 12616 |  0.0162549  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.0193758   | 0.0358561  | 0.589013    | 12616 |  0.0162549  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.0155246   | 0.0316235  | 0.623551    | 12616 |  0.0162549  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.0338424   | 0.0287245  | 0.238906    | 12616 |  0.0162549  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.0741029   | 0.0233656  | 0.00154599  | 12616 |  0.0162549  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.0534089   | 0.0379209  | 0.159201    | 12616 |  0.0162549  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.0064916   | 0.0366375  | 0.859386    | 12616 |  0.0162549  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered |  0.0145405   | 0.0128251  | 0.257071    | 12616 |  0.0162549  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.0119957   | 0.0127729  | 0.347799    | 12616 |  0.0162549  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0300583   | 0.0110075  | 0.00639021  | 12616 |  0.0162549  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0276892   | 0.0107272  | 0.00993466  | 12616 |  0.0162549  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0361296   | 0.0114428  | 0.00162197  | 12616 |  0.0162549  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.0373433   | 0.0123943  | 0.0026286   | 12616 |  0.0162549  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.0305659   | 0.0135205  | 0.0239137   | 12616 |  0.0162549  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |     n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|------:|
| event_att      | pretrend_att_joint_zero            |                3 |    2.85797  | 0.414046 | 12616 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |    4.30258  | 0.23059  | 12616 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |    0.945581 | 0.814416 | 12616 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |    2.56935  | 0.462888 | 12616 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |    0.583365 | 0.90023  | 12616 |