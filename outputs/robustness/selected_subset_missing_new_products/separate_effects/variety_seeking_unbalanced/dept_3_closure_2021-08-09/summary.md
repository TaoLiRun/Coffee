# Displacement Effect Estimation Summary

- Sample rows: 11,888
- Unique members: 1,486
- Unique closures: 1
- Event FE units: 1,486
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_3_closure_2021-08-09`
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Length-heterogeneity event-study spec skipped: true
- Model type: DDD


## Binary Specs
| spec             | term                  |    n |   r2_within |      coef |        se |      pvalue |
|:-----------------|:----------------------|-----:|------------:|----------:|----------:|------------:|
| binary_collapsed | post_X_treated        | 3441 |   0.0072904 | -0.156991 | 0.0418427 | 0.000187248 |
| binary_collapsed | post_X_disp           | 3441 |   0.0072904 | -0.102979 | 0.045971  | 0.0253396   |
| binary_collapsed | post_X_treated_X_disp | 3441 |   0.0072904 |  0.115097 | 0.0587813 | 0.0505473   |

## Score Spec
| spec            | term                   |    n |   r2_within |      coef |        se |      pvalue |
|:----------------|:-----------------------|-----:|------------:|----------:|----------:|------------:|
| score_collapsed | post_X_treated         | 3441 |  0.00659519 | -0.137907 | 0.0359519 | 0.000134261 |
| score_collapsed | post_X_score           | 3441 |  0.00659519 | -0.118372 | 0.0752887 | 0.116262    |
| score_collapsed | post_X_treated_X_score | 3441 |  0.00659519 |  0.185342 | 0.100082  | 0.0643835   |

## Event-study Specs
| spec           | term                                                              |        coef |        se |     pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|------------:|----------:|-----------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00656005 | 0.0574811 | 0.909165   | 3441 |  0.00933453 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0560937  | 0.058558  | 0.338374   | 3441 |  0.00933453 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00783005 | 0.0580534 | 0.892741   | 3441 |  0.00933453 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.0400056  | 0.0584297 | 0.493731   | 3441 |  0.00933453 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0927979  | 0.0613803 | 0.130939   | 3441 |  0.00933453 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.190575   | 0.0598364 | 0.0015     | 3441 |  0.00933453 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.179412   | 0.0581537 | 0.00209974 | 3441 |  0.00933453 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0697255  | 0.0890206 | 0.433695   | 3441 |  0.0141235  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0892822  | 0.0923662 | 0.33401    | 3441 |  0.0141235  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0156622  | 0.0962922 | 0.87083    | 3441 |  0.0141235  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.130746   | 0.095146  | 0.16975    | 3441 |  0.0141235  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.163761   | 0.100072  | 0.102116   | 3441 |  0.0141235  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.259788   | 0.0931783 | 0.00541931 | 3441 |  0.0141235  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.266608   | 0.0886284 | 0.00270496 | 3441 |  0.0141235  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.112859   | 0.118169  | 0.339812   | 3441 |  0.0141235  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0385226  | 0.118974  | 0.746176   | 3441 |  0.0141235  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.018421   | 0.119227  | 0.877249   | 3441 |  0.0141235  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.161171   | 0.11776   | 0.171468   | 3441 |  0.0141235  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.133401   | 0.124906  | 0.285817   | 3441 |  0.0141235  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.128571   | 0.122282  | 0.293356   | 3441 |  0.0141235  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.203847   | 0.119371  | 0.0880567  | 3441 |  0.0141235  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.0757895  | 0.0907165 | 0.403694   | 3441 |  0.0141235  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                | -0.0479543  | 0.0880813 | 0.586286   | 3441 |  0.0141235  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0469722  | 0.0940454 | 0.617581   | 3441 |  0.0141235  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.1948     | 0.0943509 | 0.0392571  | 3441 |  0.0141235  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0840527  | 0.106223  | 0.428996   | 3441 |  0.0141235  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0701565  | 0.0993411 | 0.480243   | 3441 |  0.0141235  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.131063   | 0.0966119 | 0.175266   | 3441 |  0.0141235  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0483735  | 0.0764468 | 0.52705    | 3441 |  0.0137166  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0975715  | 0.0803553 | 0.224985   | 3441 |  0.0137166  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0397797  | 0.0865777 | 0.646014   | 3441 |  0.0137166  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.125675   | 0.080122  | 0.117123   | 3441 |  0.0137166  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.148642   | 0.0859424 | 0.084068   | 3441 |  0.0137166  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.241332   | 0.0806943 | 0.00286285 | 3441 |  0.0137166  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.239748   | 0.0764621 | 0.00177384 | 3441 |  0.0137166  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.156548   | 0.204364  | 0.443871   | 3441 |  0.0137166  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.139828   | 0.204684  | 0.494701   | 3441 |  0.0137166  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.14158    | 0.215539  | 0.511442   | 3441 |  0.0137166  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.372067   | 0.196518  | 0.0586543  | 3441 |  0.0137166  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.253411   | 0.212331  | 0.233014   | 3441 |  0.0137166  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.201954   | 0.217397  | 0.353169   | 3441 |  0.0137166  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.343658   | 0.198021  | 0.0830164  | 3441 |  0.0137166  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.183541   | 0.151082  | 0.224758   | 3441 |  0.0137166  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered | -0.137503   | 0.144806  | 0.342598   | 3441 |  0.0137166  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered | -0.075542   | 0.172397  | 0.661362   | 3441 |  0.0137166  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.407312   | 0.152114  | 0.00755475 | 3441 |  0.0137166  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.136625   | 0.177061  | 0.440547   | 3441 |  0.0137166  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.0774888  | 0.175547  | 0.659024   | 3441 |  0.0137166  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.239704   | 0.155515  | 0.123597   | 3441 |  0.0137166  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                3 |    1.23046  | 0.745709 | 3441 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |    1.29675  | 0.729905 | 3441 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |    1.13008  | 0.769819 | 3441 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |    1.56121  | 0.668217 | 3441 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |    0.739297 | 0.863924 | 3441 |