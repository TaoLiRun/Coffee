# Displacement Effect Estimation Summary

- Sample rows: 14,672
- Unique members: 1,834
- Unique closures: 1
- Event FE units: 1,834
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_220_closure_2021-08-03`
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Length-heterogeneity event-study spec skipped: true
- Model type: DDD


## Binary Specs
| spec             | term                  |    n |   r2_within |       coef |        se |    pvalue |
|:-----------------|:----------------------|-----:|------------:|-----------:|----------:|----------:|
| binary_collapsed | post_X_treated        | 3044 |  0.00325949 | -0.082164  | 0.0498073 | 0.0994101 |
| binary_collapsed | post_X_disp           | 3044 |  0.00325949 |  0.0350298 | 0.033078  | 0.289916  |
| binary_collapsed | post_X_treated_X_disp | 3044 |  0.00325949 |  0.0820711 | 0.0679149 | 0.227235  |

## Score Spec
| spec            | term                   |    n |   r2_within |       coef |        se |   pvalue |
|:----------------|:-----------------------|-----:|------------:|-----------:|----------:|---------:|
| score_collapsed | post_X_treated         | 3044 |  0.00426201 | -0.0715806 | 0.0437972 | 0.102576 |
| score_collapsed | post_X_score           | 3044 |  0.00426201 |  0.0825388 | 0.0539964 | 0.12676  |
| score_collapsed | post_X_treated_X_score | 3044 |  0.00426201 |  0.131882  | 0.104957  | 0.20929  |

## Event-study Specs
| spec           | term                                                              |        coef |        se |     pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|------------:|----------:|-----------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.169936   | 0.0657578 | 0.00993472 | 3044 |  0.00641065 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.190895   | 0.06487   | 0.00334742 | 3044 |  0.00641065 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0768525  | 0.0635187 | 0.226668   | 3044 |  0.00641065 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0862387  | 0.078352  | 0.271377   | 3044 |  0.00641065 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0755884  | 0.06456   | 0.242019   | 3044 |  0.00641065 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.099987   | 0.0647849 | 0.123137   | 3044 |  0.00641065 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0177215  | 0.0677153 | 0.793615   | 3044 |  0.00641065 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.164707   | 0.10213   | 0.107199   | 3044 |  0.0121095  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.253652   | 0.104217  | 0.0151558  | 3044 |  0.0121095  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.104934   | 0.101454  | 0.301308   | 3044 |  0.0121095  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.069292   | 0.109441  | 0.526822   | 3044 |  0.0121095  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0166358  | 0.0948801 | 0.860861   | 3044 |  0.0121095  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0964345  | 0.0943508 | 0.307051   | 3044 |  0.0121095  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0580164  | 0.0989331 | 0.557759   | 3044 |  0.0121095  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0195093  | 0.13137   | 0.88198    | 3044 |  0.0121095  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             | -0.114171   | 0.131833  | 0.386734   | 3044 |  0.0121095  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.056042   | 0.128983  | 0.664048   | 3044 |  0.0121095  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.0629812  | 0.157966  | 0.690219   | 3044 |  0.0121095  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.149298   | 0.130856  | 0.254242   | 3044 |  0.0121095  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.0163124  | 0.132041  | 0.90171    | 3044 |  0.0121095  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.0683527  | 0.136625  | 0.617006   | 3044 |  0.0121095  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.00338893 | 0.07118   | 0.962038   | 3044 |  0.0121095  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.0103078  | 0.0751806 | 0.89098    | 3044 |  0.0121095  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                | -0.0101659  | 0.0717666 | 0.887391   | 3044 |  0.0121095  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  0.0240254  | 0.0704733 | 0.733257   | 3044 |  0.0121095  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.00150519 | 0.0731351 | 0.983585   | 3044 |  0.0121095  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.0169827  | 0.0735604 | 0.817477   | 3044 |  0.0121095  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.119948   | 0.0747558 | 0.108993   | 3044 |  0.0121095  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.158219   | 0.0975327 | 0.105151   | 3044 |  0.0143311  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.210753   | 0.0947524 | 0.0264101  | 3044 |  0.0143311  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0834337  | 0.0930827 | 0.370342   | 3044 |  0.0143311  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0512012  | 0.0987511 | 0.604262   | 3044 |  0.0143311  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0373801  | 0.0862512 | 0.664851   | 3044 |  0.0143311  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0930356  | 0.0863296 | 0.281502   | 3044 |  0.0143311  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0341725  | 0.0914755 | 0.708823   | 3044 |  0.0143311  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.0488685  | 0.222758  | 0.826411   | 3044 |  0.0143311  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            | -0.1051     | 0.212482  | 0.620998   | 3044 |  0.0143311  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.0577213  | 0.198608  | 0.77141    | 3044 |  0.0143311  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.21246    | 0.211211  | 0.314763   | 3044 |  0.0143311  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.208574   | 0.188735  | 0.269441   | 3044 |  0.0143311  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.0383775  | 0.196368  | 0.845101   | 3044 |  0.0143311  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             | -0.0860783  | 0.212602  | 0.685674   | 3044 |  0.0143311  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.0524583  | 0.113377  | 0.643714   | 3044 |  0.0143311  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered | -0.0649182  | 0.118507  | 0.583982   | 3044 |  0.0143311  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered | -0.124701   | 0.109968  | 0.257147   | 3044 |  0.0143311  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0371454  | 0.105867  | 0.725781   | 3044 |  0.0143311  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0300208  | 0.114569  | 0.793364   | 3044 |  0.0143311  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.0152046  | 0.111824  | 0.89188    | 3044 |  0.0143311  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  |  0.179353   | 0.112895  | 0.112531   | 3044 |  0.0143311  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |    pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|----------:|-----:|
| event_att      | pretrend_att_joint_zero            |                3 |   11.1211   | 0.0110887 | 3044 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |    6.32983  | 0.0966208 | 3044 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |    1.52951  | 0.675476  | 3044 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |    5.72092  | 0.126006  | 3044 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |    0.600766 | 0.896257  | 3044 |