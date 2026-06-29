# Displacement Effect Estimation Summary

- Sample rows: 27,072
- Unique members: 3,384
- Unique closures: 1
- Event FE units: 3,384
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_47_closure_2021-07-30`
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Length-heterogeneity event-study spec skipped: true
- Model type: DDD


## Binary Specs
| spec             | term                  |     n |   r2_within |        coef |         se |    pvalue |
|:-----------------|:----------------------|------:|------------:|------------:|-----------:|----------:|
| binary_collapsed | post_X_treated        | 27072 |   0.0130045 | -0.00538705 | 0.00240609 | 0.0252255 |
| binary_collapsed | post_X_disp           | 27072 |   0.0130045 | -0.0382503  | 0.00435188 | 0         |
| binary_collapsed | post_X_treated_X_disp | 27072 |   0.0130045 |  0.0235583  | 0.0135333  | 0.0818151 |

## Score Spec
| spec            | term                   |     n |   r2_within |         coef |         se |   pvalue |
|:----------------|:-----------------------|------:|------------:|-------------:|-----------:|---------:|
| score_collapsed | post_X_treated         | 27072 |   0.0150115 |  0.000732379 | 0.00433853 | 0.865958 |
| score_collapsed | post_X_score           | 27072 |   0.0150115 | -0.0550462   | 0.00601242 | 0        |
| score_collapsed | post_X_treated_X_score | 27072 |   0.0150115 |  0.019196    | 0.0185243  | 0.300156 |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00293932  | 0.00524972 | 0.575585    | 27072 | 0.000155279 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.00693311  | 0.00542816 | 0.201602    | 27072 | 0.000155279 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0101329   | 0.00593579 | 0.0878967   | 27072 | 0.000155279 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.000701069 | 0.00542211 | 0.897129    | 27072 | 0.000155279 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00676359  | 0.0064848  | 0.297027    | 27072 | 0.000155279 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00860198  | 0.00527972 | 0.103354    | 27072 | 0.000155279 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00392484  | 0.00514181 | 0.445327    | 27072 | 0.000155279 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00148528  | 0.00456906 | 0.745146    | 27072 | 0.0254067   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.00352597  | 0.00522995 | 0.500238    | 27072 | 0.0254067   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00209086  | 0.00395009 | 0.596619    | 27072 | 0.0254067   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00739415  | 0.00377388 | 0.0501604   | 27072 | 0.0254067   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00431967  | 0.00460593 | 0.348388    | 27072 | 0.0254067   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.00292398  | 0.00447857 | 0.513877    | 27072 | 0.0254067   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00696057  | 0.00437857 | 0.111998    | 27072 | 0.0254067   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0198507   | 0.0177652  | 0.263905    | 27072 | 0.0254067   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0156494   | 0.0162601  | 0.335897    | 27072 | 0.0254067   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0557217   | 0.0186116  | 0.00277407  | 27072 | 0.0254067   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.0359874   | 0.0207239  | 0.0825628   | 27072 | 0.0254067   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.0497084   | 0.0239944  | 0.0383724   | 27072 | 0.0254067   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.0513696   | 0.0180052  | 0.0043566   | 27072 | 0.0254067   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.0483897   | 0.0176524  | 0.00615269  | 27072 | 0.0254067   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.000924443 | 0.00673762 | 0.890876    | 27072 | 0.0254067   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.0219744   | 0.00652255 | 0.000762889 | 27072 | 0.0254067   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0523859   | 0.00636386 | 2.22045e-16 | 27072 | 0.0254067   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.022372    | 0.00556245 | 5.89721e-05 | 27072 | 0.0254067   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.00332255  | 0.00654993 | 0.612002    | 27072 | 0.0254067   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0236913   | 0.00633292 | 0.000186348 | 27072 | 0.0254067   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0301795   | 0.00640173 | 2.52361e-06 | 27072 | 0.0254067   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00480721  | 0.0062755  | 0.443713    | 27072 | 0.0270568   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.00881038  | 0.00624152 | 0.158166    | 27072 | 0.0270568   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0152184   | 0.00623727 | 0.0147418   | 27072 | 0.0270568   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00186361  | 0.00681642 | 0.784563    | 27072 | 0.0270568   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0100963   | 0.00785544 | 0.198786    | 27072 | 0.0270568   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0120996   | 0.00635756 | 0.0571013   | 27072 | 0.0270568   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00770595  | 0.0062622  | 0.218577    | 27072 | 0.0270568   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.0321555   | 0.0249909  | 0.198291    | 27072 | 0.0270568   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.0284622   | 0.0231177  | 0.218339    | 27072 | 0.0270568   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.0780666   | 0.0236602  | 0.000978629 | 27072 | 0.0270568   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.0238836   | 0.0285886  | 0.403538    | 27072 | 0.0270568   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.0577929   | 0.0317818  | 0.0690876   | 27072 | 0.0270568   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.0641503   | 0.0253003  | 0.0112717   | 27072 | 0.0270568   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.0696415   | 0.0261019  | 0.00766547  | 27072 | 0.0270568   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.00356376  | 0.00952793 | 0.708404    | 27072 | 0.0270568   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.0280917   | 0.00885432 | 0.00152403  | 27072 | 0.0270568   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0681832   | 0.00869779 | 5.9952e-15  | 27072 | 0.0270568   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0340228   | 0.00768382 | 9.81898e-06 | 27072 | 0.0270568   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.00980966  | 0.00924117 | 0.288531    | 27072 | 0.0270568   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.0390401   | 0.008968   | 1.38095e-05 | 27072 | 0.0270568   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.0446012   | 0.00916646 | 1.19263e-06 | 27072 | 0.0270568   |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |    pvalue |     n |
|:---------------|:-----------------------------------|-----------------:|------------:|----------:|------:|
| event_att      | pretrend_att_joint_zero            |                3 |     3.32855 | 0.343688  | 27072 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |     1.45858 | 0.691862  | 27072 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |     9.26618 | 0.0259534 | 27072 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |     6.2277  | 0.101042  | 27072 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |    11.1885  | 0.0107488 | 27072 |