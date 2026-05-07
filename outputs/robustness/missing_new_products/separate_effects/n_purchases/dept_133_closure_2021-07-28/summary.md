# Displacement Effect Estimation Summary

- Sample rows: 17,552
- Unique members: 2,194
- Unique closures: 1
- Event FE units: 2,194
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_133_closure_2021-07-28`
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Length-heterogeneity event-study spec skipped: true
- Model type: DDD


## Binary Specs
| spec             | term                  |     n |   r2_within |        coef |         se |     pvalue |
|:-----------------|:----------------------|------:|------------:|------------:|-----------:|-----------:|
| binary_collapsed | post_X_treated        | 17552 |   0.0147159 |  0.00204086 | 0.0027199  | 0.453129   |
| binary_collapsed | post_X_disp           | 17552 |   0.0147159 | -0.0274039  | 0.00319555 | 0          |
| binary_collapsed | post_X_treated_X_disp | 17552 |   0.0147159 |  0.0283383  | 0.00881994 | 0.00133273 |

## Score Spec
| spec            | term                   |     n |   r2_within |        coef |         se |     pvalue |
|:----------------|:-----------------------|------:|------------:|------------:|-----------:|-----------:|
| score_collapsed | post_X_treated         | 17552 |   0.0206432 |  0.00751372 | 0.0027101  | 0.00561001 |
| score_collapsed | post_X_score           | 17552 |   0.0206432 | -0.0501364  | 0.00570031 | 0          |
| score_collapsed | post_X_treated_X_score | 17552 |   0.0206432 |  0.0459426  | 0.0151174  | 0.00240126 |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00123349  | 0.00535066 | 0.817701    | 17552 |  0.00160517 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0076227   | 0.00516259 | 0.139946    | 17552 |  0.00160517 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00621511  | 0.00433253 | 0.151567    | 17552 |  0.00160517 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0129791   | 0.00455464 | 0.00441766  | 17552 |  0.00160517 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00370676  | 0.00407967 | 0.363665    | 17552 |  0.00160517 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0102655   | 0.00419249 | 0.0144218   | 17552 |  0.00160517 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0115883   | 0.00531495 | 0.0293395   | 17552 |  0.00160517 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00694867  | 0.00331979 | 0.0364545   | 17552 |  0.0212465  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00211032  | 0.00359826 | 0.557612    | 17552 |  0.0212465  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00107585  | 0.00306137 | 0.725302    | 17552 |  0.0212465  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00185613  | 0.004078   | 0.649041    | 17552 |  0.0212465  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00305612  | 0.003059   | 0.317878    | 17552 |  0.0212465  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.000960578 | 0.00352389 | 0.785194    | 17552 |  0.0212465  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00605312  | 0.00473542 | 0.201291    | 17552 |  0.0212465  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.013479    | 0.0152408  | 0.376577    | 17552 |  0.0212465  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             | -0.0158244   | 0.0143322  | 0.269665    | 17552 |  0.0212465  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.0181828   | 0.0119201  | 0.127306    | 17552 |  0.0212465  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.0404259   | 0.0115828  | 0.000492272 | 17552 |  0.0212465  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.0143243   | 0.0109708  | 0.1918      | 17552 |  0.0212465  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.0276408   | 0.0109286  | 0.0115011   | 17552 |  0.0212465  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.0104339   | 0.0135355  | 0.440876    | 17552 |  0.0212465  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.0167065   | 0.00479037 | 0.000497123 | 17552 |  0.0212465  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.00547535  | 0.00455957 | 0.229941    | 17552 |  0.0212465  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0175927   | 0.00421407 | 3.09983e-05 | 17552 |  0.0212465  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0228791   | 0.00412636 | 3.3002e-08  | 17552 |  0.0212465  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0258937   | 0.00419996 | 8.35393e-10 | 17552 |  0.0212465  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0284276   | 0.00430806 | 5.18459e-11 | 17552 |  0.0212465  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0260537   | 0.00481075 | 6.77131e-08 | 17552 |  0.0212465  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00452281  | 0.00397365 | 0.255161    | 17552 |  0.0288708  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00600135  | 0.00390908 | 0.124871    | 17552 |  0.0288708  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00395215  | 0.00324893 | 0.223946    | 17552 |  0.0288708  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00575245  | 0.00381372 | 0.131607    | 17552 |  0.0288708  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00153764  | 0.00321791 | 0.632813    | 17552 |  0.0288708  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00423567  | 0.00349153 | 0.225212    | 17552 |  0.0288708  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00712808  | 0.00456569 | 0.118614    | 17552 |  0.0288708  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.0188939   | 0.0264283  | 0.47474     | 17552 |  0.0288708  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            | -0.0228918   | 0.0236226  | 0.332621    | 17552 |  0.0288708  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.014721    | 0.0197114  | 0.455249    | 17552 |  0.0288708  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.0726276   | 0.0170328  | 2.09318e-05 | 17552 |  0.0288708  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.0311798   | 0.017163   | 0.0694019   | 17552 |  0.0288708  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.043429    | 0.0179539  | 0.0156474   | 17552 |  0.0288708  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.0178148   | 0.0222557  | 0.423531    | 17552 |  0.0288708  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.0348838   | 0.00822835 | 2.33346e-05 | 17552 |  0.0288708  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.0033902   | 0.00768653 | 0.659216    | 17552 |  0.0288708  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0222478   | 0.00719989 | 0.00202659  | 17552 |  0.0288708  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0450046   | 0.00735829 | 1.13161e-09 | 17552 |  0.0288708  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0545442   | 0.00729478 | 1.09246e-13 | 17552 |  0.0288708  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.0550067   | 0.00762449 | 7.42517e-13 | 17552 |  0.0288708  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.055236    | 0.00852971 | 1.161e-10   | 17552 |  0.0288708  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |    pvalue |     n |
|:---------------|:-----------------------------------|-----------------:|------------:|----------:|------:|
| event_att      | pretrend_att_joint_zero            |                3 |     4.22625 | 0.238047  | 17552 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |     5.62079 | 0.13159   | 17552 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |    11.2344  | 0.0105238 | 17552 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |     2.60296 | 0.45697   | 17552 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |     7.73913 | 0.0517223 | 17552 |