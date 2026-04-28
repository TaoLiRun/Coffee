# Displacement Effect Estimation Summary

- Sample rows: 5,392
- Unique members: 674
- Unique closures: 1
- Event FE units: 674
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_8_closure_2021-05-27`
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Length-heterogeneity event-study spec skipped: true
- Model type: DDD


## Binary Specs
| spec             | term                  |    n |   r2_within |         coef |        se |   pvalue |
|:-----------------|:----------------------|-----:|------------:|-------------:|----------:|---------:|
| binary_collapsed | post_X_treated        | 1965 |  0.00304146 |  0.107547    | 0.0820856 | 0.19079  |
| binary_collapsed | post_X_disp           | 1965 |  0.00304146 |  0.000837529 | 0.0478624 | 0.986046 |
| binary_collapsed | post_X_treated_X_disp | 1965 |  0.00304146 | -0.00692988  | 0.102403  | 0.946076 |

## Score Spec
| spec            | term                   |    n |   r2_within |       coef |        se |    pvalue |
|:----------------|:-----------------------|-----:|------------:|-----------:|----------:|----------:|
| score_collapsed | post_X_treated         | 1965 |  0.00326538 |  0.115156  | 0.0681939 | 0.0919672 |
| score_collapsed | post_X_score           | 1965 |  0.00326538 | -0.0214724 | 0.062906  | 0.733004  |
| score_collapsed | post_X_treated_X_score | 1965 |  0.00326538 | -0.0352901 | 0.141882  | 0.803682  |

## Event-study Specs
| spec           | term                                                              |        coef |        se |    pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|------------:|----------:|----------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00378785 | 0.0949838 | 0.968207  | 1965 |  0.00724797 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.0650801  | 0.083158  | 0.434262  | 1965 |  0.00724797 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0821446  | 0.0884339 | 0.35344   | 1965 |  0.00724797 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0861702  | 0.0993828 | 0.386366  | 1965 |  0.00724797 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.185337   | 0.0995929 | 0.0633918 | 1965 |  0.00724797 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0998515  | 0.101843  | 0.327382  | 1965 |  0.00724797 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00551782 | 0.0904256 | 0.951369  | 1965 |  0.00724797 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.174483   | 0.163095  | 0.285263  | 1965 |  0.017953   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.348122   | 0.139722  | 0.0130723 | 1965 |  0.017953   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.018453   | 0.175419  | 0.916268  | 1965 |  0.017953   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.124634   | 0.167165  | 0.456306  | 1965 |  0.017953   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.404819   | 0.160254  | 0.0118691 | 1965 |  0.017953   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.328678   | 0.175058  | 0.0610793 | 1965 |  0.017953   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0697356  | 0.153235  | 0.64926   | 1965 |  0.017953   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             | -0.273931   | 0.195928  | 0.162754  | 1965 |  0.017953   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             | -0.449212   | 0.166582  | 0.0072624 | 1965 |  0.017953   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.157737   | 0.200949  | 0.432882  | 1965 |  0.017953   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0470825  | 0.205343  | 0.818748  | 1965 |  0.017953   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.356176   | 0.201795  | 0.0782241 | 1965 |  0.017953   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              | -0.382591   | 0.209691  | 0.0687207 | 1965 |  0.017953   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.118923   | 0.183077  | 0.516289  | 1965 |  0.017953   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.00974196 | 0.0762182 | 0.89835   | 1965 |  0.017953   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                | -0.00233501 | 0.0734015 | 0.974636  | 1965 |  0.017953   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                | -0.0967712  | 0.0732215 | 0.186954  | 1965 |  0.017953   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0108172  | 0.081455  | 0.89441   | 1965 |  0.017953   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0497868  | 0.0775374 | 0.52113   | 1965 |  0.017953   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.0241592  | 0.0836887 | 0.772957  | 1965 |  0.017953   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0612125  | 0.0918375 | 0.505407  | 1965 |  0.017953   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.0963759  | 0.138343  | 0.486377  | 1965 |  0.0144762  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.207625   | 0.118867  | 0.0813581 | 1965 |  0.0144762  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0410249  | 0.154915  | 0.791265  | 1965 |  0.0144762  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.10863    | 0.136983  | 0.428178  | 1965 |  0.0144762  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.2982     | 0.139079  | 0.0325494 | 1965 |  0.0144762  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.256826   | 0.147537  | 0.0823969 | 1965 |  0.0144762  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00477871 | 0.133528  | 0.971467  | 1965 |  0.0144762  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            | -0.290109   | 0.26614   | 0.27626   | 1965 |  0.0144762  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            | -0.453625   | 0.226823  | 0.0461009 | 1965 |  0.0144762  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.136486   | 0.286181  | 0.633645  | 1965 |  0.0144762  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.0505679  | 0.276797  | 0.855122  | 1965 |  0.0144762  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.362926   | 0.259154  | 0.162063  | 1965 |  0.0144762  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             | -0.525012   | 0.287408  | 0.0683929 | 1965 |  0.0144762  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.00272723 | 0.251181  | 0.991342  | 1965 |  0.0144762  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered |  0.0153609  | 0.104329  | 0.883012  | 1965 |  0.0144762  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.0154036  | 0.102602  | 0.880729  | 1965 |  0.0144762  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered | -0.0640358  | 0.108747  | 0.556253  | 1965 |  0.0144762  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0261776  | 0.107571  | 0.807841  | 1965 |  0.0144762  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.057869   | 0.096349  | 0.548391  | 1965 |  0.0144762  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  |  0.0323051  | 0.106203  | 0.761128  | 1965 |  0.0144762  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.0730406  | 0.112669  | 0.517133  | 1965 |  0.0144762  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |    pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|----------:|-----:|
| event_att      | pretrend_att_joint_zero            |                3 |     4.08319 | 0.25262   | 1965 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |     8.4581  | 0.0374348 | 1965 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |     8.10963 | 0.0437994 | 1965 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |     5.4111  | 0.144054  | 1965 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |     4.51173 | 0.211247  | 1965 |