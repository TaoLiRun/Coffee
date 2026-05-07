# Displacement Effect Estimation Summary

- Sample rows: 21,704
- Unique members: 2,713
- Unique closures: 1
- Event FE units: 2,713
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_131_closure_2021-08-29`
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Length-heterogeneity event-study spec skipped: true
- Model type: DDD


## Binary Specs
| spec             | term                  |    n |   r2_within |       coef |        se |   pvalue |
|:-----------------|:----------------------|-----:|------------:|-----------:|----------:|---------:|
| binary_collapsed | post_X_treated        | 4629 |  0.00227417 |  0.0756333 | 0.048985  | 0.122852 |
| binary_collapsed | post_X_disp           | 4629 |  0.00227417 |  0.0681558 | 0.0279658 | 0.014951 |
| binary_collapsed | post_X_treated_X_disp | 4629 |  0.00227417 | -0.0749911 | 0.0625692 | 0.23095  |

## Score Spec
| spec            | term                   |    n |   r2_within |       coef |        se |   pvalue |
|:----------------|:-----------------------|-----:|------------:|-----------:|----------:|---------:|
| score_collapsed | post_X_treated         | 4629 |  0.00131569 |  0.0650475 | 0.0417535 | 0.119525 |
| score_collapsed | post_X_score           | 4629 |  0.00131569 |  0.0696818 | 0.0433897 | 0.10855  |
| score_collapsed | post_X_treated_X_score | 4629 |  0.00131569 | -0.131609  | 0.101591  | 0.195409 |

## Event-study Specs
| spec           | term                                                              |        coef |        se |     pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|------------:|----------:|-----------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.117139   | 0.0620696 | 0.0593737  | 4629 |  0.0027084  |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00723801 | 0.0631871 | 0.908822   | 4629 |  0.0027084  |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0588008  | 0.0568453 | 0.30116    | 4629 |  0.0027084  |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.0656269  | 0.066487  | 0.323813   | 4629 |  0.0027084  |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0248246  | 0.06436   | 0.699777   | 4629 |  0.0027084  |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0313726  | 0.0659094 | 0.634165   | 4629 |  0.0027084  |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0310597  | 0.0614923 | 0.613583   | 4629 |  0.0027084  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.120337   | 0.0894871 | 0.178967   | 4629 |  0.00843126 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0388577  | 0.101844  | 0.70287    | 4629 |  0.00843126 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0490439  | 0.0868155 | 0.572234   | 4629 |  0.00843126 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.0461506  | 0.100154  | 0.645029   | 4629 |  0.00843126 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00461889 | 0.0912224 | 0.959626   | 4629 |  0.00843126 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00355952 | 0.0933266 | 0.969582   | 4629 |  0.00843126 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.106094   | 0.0861533 | 0.218396   | 4629 |  0.00843126 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0106248  | 0.124028  | 0.931747   | 4629 |  0.00843126 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0477895  | 0.128029  | 0.709013   | 4629 |  0.00843126 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.020659   | 0.114201  | 0.856477   | 4629 |  0.00843126 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0388924  | 0.131338  | 0.767186   | 4629 |  0.00843126 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.0539706  | 0.128858  | 0.67541    | 4629 |  0.00843126 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.0645237  | 0.131285  | 0.623179   | 4629 |  0.00843126 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.191835   | 0.122264  | 0.116909   | 4629 |  0.00843126 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.0115062  | 0.0494994 | 0.816228   | 4629 |  0.00843126 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.0702235  | 0.0496069 | 0.157155   | 4629 |  0.00843126 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0501805  | 0.0498291 | 0.314116   | 4629 |  0.00843126 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  0.0350005  | 0.0504102 | 0.487621   | 4629 |  0.00843126 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.130079   | 0.0513444 | 0.0114217  | 4629 |  0.00843126 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.0570289  | 0.0539151 | 0.290382   | 4629 |  0.00843126 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.146097   | 0.0521004 | 0.00512717 | 4629 |  0.00843126 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.122667   | 0.0752605 | 0.103386   | 4629 |  0.00682098 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0282158  | 0.0857392 | 0.742147   | 4629 |  0.00682098 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0772716  | 0.077707  | 0.320232   | 4629 |  0.00682098 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.0555844  | 0.0826181 | 0.501213   | 4629 |  0.00682098 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0126468  | 0.0762302 | 0.868262   | 4629 |  0.00682098 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00255761 | 0.0786175 | 0.974053   | 4629 |  0.00682098 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.063912   | 0.0717645 | 0.373336   | 4629 |  0.00682098 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.0299602  | 0.18549   | 0.871712   | 4629 |  0.00682098 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.0659987  | 0.201864  | 0.743766   | 4629 |  0.00682098 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.0689656  | 0.196226  | 0.725305   | 4629 |  0.00682098 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.0667299  | 0.201902  | 0.741076   | 4629 |  0.00682098 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.0980824  | 0.194043  | 0.613324   | 4629 |  0.00682098 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.178683   | 0.210876  | 0.396977   | 4629 |  0.00682098 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             | -0.306524   | 0.184797  | 0.0974381  | 4629 |  0.00682098 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.0296409  | 0.0731552 | 0.68542    | 4629 |  0.00682098 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.082426   | 0.0854291 | 0.334818   | 4629 |  0.00682098 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0254387  | 0.0795604 | 0.749221   | 4629 |  0.00682098 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  |  0.00618212 | 0.0742555 | 0.933663   | 4629 |  0.00682098 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  |  0.128189   | 0.079165  | 0.105656   | 4629 |  0.00682098 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  |  0.0409753  | 0.077974  | 0.599334   | 4629 |  0.00682098 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  |  0.159967   | 0.0782559 | 0.0411586  | 4629 |  0.00682098 |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                3 |    5.22623  | 0.155961 | 4629 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |    1.94113  | 0.584715 | 4629 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |    0.301891 | 0.959672 | 4629 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |    3.14781  | 0.369392 | 4629 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |    0.162529 | 0.983399 | 4629 |