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
| spec             | term                  |    n |   r2_within |        coef |        se |    pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|----------:|----------:|
| binary_collapsed | post_X_treated        | 6939 | 0.000745714 | -0.0714969  | 0.0644222 | 0.267255  |
| binary_collapsed | post_X_disp           | 6939 | 0.000745714 | -0.00127234 | 0.0241911 | 0.958061  |
| binary_collapsed | post_X_treated_X_disp | 6939 | 0.000745714 |  0.138      | 0.0754231 | 0.0674958 |

## Score Spec
| spec            | term                   |    n |   r2_within |       coef |        se |   pvalue |
|:----------------|:-----------------------|-----:|------------:|-----------:|----------:|---------:|
| score_collapsed | post_X_treated         | 6939 |  0.00117657 | -0.0908712 | 0.0584832 | 0.120443 |
| score_collapsed | post_X_score           | 6939 |  0.00117657 | -0.0208182 | 0.0393394 | 0.596749 |
| score_collapsed | post_X_treated_X_score | 6939 |  0.00117657 |  0.331567  | 0.131229  | 0.011618 |

## Event-study Specs
| spec           | term                                                              |        coef |        se |      pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|------------:|----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.063996   | 0.0679643 | 0.346543    | 6939 | 0.000516123 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0853178  | 0.0626661 | 0.17357     | 6939 | 0.000516123 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0567292  | 0.0588464 | 0.33519     | 6939 | 0.000516123 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.0120962  | 0.0604748 | 0.841492    | 6939 | 0.000516123 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0634214  | 0.0691137 | 0.358955    | 6939 | 0.000516123 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.00863898 | 0.0603035 | 0.886105    | 6939 | 0.000516123 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0308278  | 0.0622796 | 0.62068     | 6939 | 0.000516123 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.163829   | 0.124791  | 0.189441    | 6939 | 0.00670264  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0292276  | 0.107987  | 0.786692    | 6939 | 0.00670264  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.137718   | 0.108691  | 0.205332    | 6939 | 0.00670264  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0414566  | 0.114198  | 0.716638    | 6939 | 0.00670264  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0892422  | 0.12068   | 0.459722    | 6939 | 0.00670264  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0760098  | 0.111126  | 0.494082    | 6939 | 0.00670264  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0188615  | 0.11697   | 0.871918    | 6939 | 0.00670264  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             | -0.321058   | 0.147352  | 0.029498    | 6939 | 0.00670264  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             | -0.0689333  | 0.13249   | 0.602936    | 6939 | 0.00670264  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.280127   | 0.128816  | 0.0298137   | 6939 | 0.00670264  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0750082  | 0.133826  | 0.575228    | 6939 | 0.00670264  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.235982   | 0.147964  | 0.110954    | 6939 | 0.00670264  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.119927   | 0.131093  | 0.360429    | 6939 | 0.00670264  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.00588725 | 0.137339  | 0.965814    | 6939 | 0.00670264  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.154616   | 0.0459214 | 0.000779185 | 6939 | 0.00670264  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.133168   | 0.0460544 | 0.00388859  | 6939 | 0.00670264  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0905442  | 0.048124  | 0.0601      | 6939 | 0.00670264  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  0.127204   | 0.0480572 | 0.00820765  | 6939 | 0.00670264  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.0877529  | 0.0476534 | 0.065748    | 6939 | 0.00670264  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.0457503  | 0.0488391 | 0.349035    | 6939 | 0.00670264  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.125208   | 0.0485139 | 0.00994893  | 6939 | 0.00670264  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.180124   | 0.108889  | 0.098298    | 6939 | 0.0077932   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.0116164  | 0.0998121 | 0.907365    | 6939 | 0.0077932   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0798158  | 0.103833  | 0.442196    | 6939 | 0.0077932   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0493637  | 0.0985435 | 0.616491    | 6939 | 0.0077932   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0062189  | 0.112854  | 0.956061    | 6939 | 0.0077932   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0958627  | 0.0941062 | 0.308526    | 6939 | 0.0077932   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0252734  | 0.101741  | 0.803851    | 6939 | 0.0077932   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            | -0.67473    | 0.238979  | 0.00481453  | 6939 | 0.0077932   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            | -0.237406   | 0.217417  | 0.275035    | 6939 | 0.0077932   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.367236   | 0.229988  | 0.110529    | 6939 | 0.0077932   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.162256   | 0.212725  | 0.445732    | 6939 | 0.0077932   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.211613   | 0.243872  | 0.385686    | 6939 | 0.0077932   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.326023   | 0.203455  | 0.10927     | 6939 | 0.0077932   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.0264006  | 0.220442  | 0.904688    | 6939 | 0.0077932   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered |  0.285102   | 0.0778555 | 0.000258986 | 6939 | 0.0077932   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.257453   | 0.078744  | 0.00110175  | 6939 | 0.0077932   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.172315   | 0.0814078 | 0.0344504   | 6939 | 0.0077932   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  |  0.202817   | 0.0793291 | 0.010666    | 6939 | 0.0077932   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  |  0.155662   | 0.077209  | 0.0439663   | 6939 | 0.0077932   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  |  0.0642595  | 0.0792235 | 0.417428    | 6939 | 0.0077932   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  |  0.252144   | 0.0792967 | 0.00150404  | 6939 | 0.0077932   |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |    pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|----------:|-----:|
| event_att      | pretrend_att_joint_zero            |                3 |     1.96024 | 0.5807    | 6939 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |     4.15141 | 0.245572  | 6939 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |     8.29476 | 0.040297  | 6939 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |     3.78358 | 0.285802  | 6939 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |     9.01704 | 0.0290651 | 6939 |