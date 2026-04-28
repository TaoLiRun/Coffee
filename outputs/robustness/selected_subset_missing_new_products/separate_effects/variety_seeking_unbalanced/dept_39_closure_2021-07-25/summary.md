# Displacement Effect Estimation Summary

- Sample rows: 23,128
- Unique members: 2,891
- Unique closures: 1
- Event FE units: 2,891
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_39_closure_2021-07-25`
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Length-heterogeneity event-study spec skipped: true
- Model type: DDD


## Binary Specs
| spec             | term                  |    n |   r2_within |       coef |        se |   pvalue |
|:-----------------|:----------------------|-----:|------------:|-----------:|----------:|---------:|
| binary_collapsed | post_X_treated        | 9398 |  0.00044597 |  0.106143  | 0.080535  | 0.187658 |
| binary_collapsed | post_X_disp           | 9398 |  0.00044597 |  0.0205586 | 0.0205535 | 0.317306 |
| binary_collapsed | post_X_treated_X_disp | 9398 |  0.00044597 | -0.127935  | 0.0868756 | 0.141006 |

## Score Spec
| spec            | term                   |    n |   r2_within |        coef |        se |   pvalue |
|:----------------|:-----------------------|-----:|------------:|------------:|----------:|---------:|
| score_collapsed | post_X_treated         | 9398 | 0.000103905 |  0.0482789  | 0.0667159 | 0.469363 |
| score_collapsed | post_X_score           | 9398 | 0.000103905 |  0.00484516 | 0.0324144 | 0.881193 |
| score_collapsed | post_X_treated_X_score | 9398 | 0.000103905 | -0.0981454  | 0.117906  | 0.405276 |

## Event-study Specs
| spec           | term                                                              |        coef |        se |   pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|------------:|----------:|---------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.0589193  | 0.0518223 | 0.255692 | 9398 | 0.000858933 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.0439875  | 0.0456797 | 0.335683 | 9398 | 0.000858933 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.052378   | 0.0479284 | 0.274592 | 9398 | 0.000858933 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.0266632  | 0.0531854 | 0.616195 | 9398 | 0.000858933 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0387492  | 0.0594208 | 0.514399 | 9398 | 0.000858933 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0254993  | 0.055767  | 0.647542 | 9398 | 0.000858933 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0323392  | 0.056161  | 0.564792 | 9398 | 0.000858933 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.0507948  | 0.107888  | 0.637826 | 9398 | 0.00273764  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.037886   | 0.0893424 | 0.671571 | 9398 | 0.00273764  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.126744   | 0.103359  | 0.220247 | 9398 | 0.00273764  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.119195   | 0.130253  | 0.360243 | 9398 | 0.00273764  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.192068   | 0.131248  | 0.143509 | 9398 | 0.00273764  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.123428   | 0.122215  | 0.312647 | 9398 | 0.00273764  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.138942   | 0.107513  | 0.196388 | 9398 | 0.00273764  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0126691  | 0.12306   | 0.918012 | 9398 | 0.00273764  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.112378   | 0.103729  | 0.278765 | 9398 | 0.00273764  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0989597  | 0.116442  | 0.3955   | 9398 | 0.00273764  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.124235   | 0.142468  | 0.383301 | 9398 | 0.00273764  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.190348   | 0.147053  | 0.195665 | 9398 | 0.00273764  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              | -0.115337   | 0.137237  | 0.400767 | 9398 | 0.00273764  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.140075   | 0.126089  | 0.266729 | 9398 | 0.00273764  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.00829925 | 0.0382472 | 0.828238 | 9398 | 0.00273764  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                | -0.0168982  | 0.0379944 | 0.656543 | 9398 | 0.00273764  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                | -0.0323978  | 0.0363977 | 0.373513 | 9398 | 0.00273764  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0288495  | 0.0389758 | 0.459269 | 9398 | 0.00273764  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.0103231  | 0.0405614 | 0.79913  | 9398 | 0.00273764  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.00627757 | 0.0387891 | 0.871449 | 9398 | 0.00273764  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.0448012  | 0.0394353 | 0.25606  | 9398 | 0.00273764  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.0971282  | 0.101386  | 0.338174 | 9398 | 0.00268634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.00689546 | 0.0832224 | 0.933974 | 9398 | 0.00268634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.113484   | 0.101056  | 0.261578 | 9398 | 0.00268634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.107806   | 0.109543  | 0.325161 | 9398 | 0.00268634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.17467    | 0.112818  | 0.121715 | 9398 | 0.00268634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0885063  | 0.111642  | 0.428003 | 9398 | 0.00268634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.07256    | 0.100109  | 0.468651 | 9398 | 0.00268634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            | -0.105202   | 0.190555  | 0.580953 | 9398 | 0.00268634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.0912175  | 0.153554  | 0.552549 | 9398 | 0.00268634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.138217   | 0.182885  | 0.44988  | 9398 | 0.00268634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.202548   | 0.199039  | 0.308973 | 9398 | 0.00268634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.321296   | 0.208938  | 0.124261 | 9398 | 0.00268634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             | -0.135424   | 0.189379  | 0.474633 | 9398 | 0.00268634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             | -0.101774   | 0.186689  | 0.585706 | 9398 | 0.00268634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered |  0.0543369  | 0.0612181 | 0.374862 | 9398 | 0.00268634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.0338428  | 0.0603297 | 0.574883 | 9398 | 0.00268634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.018483   | 0.0598548 | 0.757506 | 9398 | 0.00268634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0329139  | 0.0616544 | 0.593506 | 9398 | 0.00268634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  |  0.0728965  | 0.0634799 | 0.250961 | 9398 | 0.00268634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  |  0.00128241 | 0.0605878 | 0.983115 | 9398 | 0.00268634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  |  0.0866872  | 0.0616796 | 0.160039 | 9398 | 0.00268634  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                3 |     5.2998  | 0.151115 | 9398 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |     3.58571 | 0.309815 | 9398 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |     2.19787 | 0.532369 | 9398 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |     5.01126 | 0.170975 | 9398 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |     2.69906 | 0.440387 | 9398 |