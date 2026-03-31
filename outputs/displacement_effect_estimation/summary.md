# Displacement Effect Estimation Summary

- Sample rows: 358,864
- Unique members: 44,858
- Unique closures: 22
- Event FE units: 44,858
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=false
- Recency filter days: false


## Binary Specs
| spec             | term                  |      n |   r2_within |         coef |          se |    pvalue |
|:-----------------|:----------------------|-------:|------------:|-------------:|------------:|----------:|
| binary_collapsed | post_X_treated        | 358864 |   0.0129964 |  0.000775815 | 0.000635149 | 0.221915  |
| binary_collapsed | post_X_disp           | 358864 |   0.0129964 | -0.0343645   | 0.00106132  | 0         |
| binary_collapsed | post_X_treated_X_disp | 358864 |   0.0129964 |  0.00487985  | 0.00241379  | 0.0432185 |

## Score Spec
| spec            | term                   |      n |   r2_within |        coef |         se |    pvalue |
|:----------------|:-----------------------|-------:|------------:|------------:|-----------:|----------:|
| score_collapsed | post_X_treated         | 358864 |   0.0181608 |  0.00184184 | 0.00079147 | 0.0199637 |
| score_collapsed | post_X_score           | 358864 |   0.0181608 | -0.0566893  | 0.00156466 | 0         |
| score_collapsed | post_X_treated_X_score | 358864 |   0.0181608 |  0.00584218 | 0.00355855 | 0.100653  |

## Event-study Specs
| spec           | term                                                              |         coef |          se |      pvalue |      n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|------------:|------------:|-------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00043436  | 0.00121332  | 0.72035     | 358864 | 0.000152819 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.000282038 | 0.00116449  | 0.808628    | 358864 | 0.000152819 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.000313581 | 0.00102194  | 0.75896     | 358864 | 0.000152819 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00254148  | 0.00103261  | 0.0138506   | 358864 | 0.000152819 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.000163434 | 0.00111593  | 0.883563    | 358864 | 0.000152819 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00623115  | 0.00116723  | 9.42259e-08 | 358864 | 0.000152819 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00175002  | 0.00115576  | 0.129987    | 358864 | 0.000152819 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00115029  | 0.00100633  | 0.253024    | 358864 | 0.0159894   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.000142158 | 0.000958001 | 0.882036    | 358864 | 0.0159894   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00150323  | 0.000809207 | 0.0632243   | 358864 | 0.0159894   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.000288583 | 0.000828768 | 0.727686    | 358864 | 0.0159894   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.000267223 | 0.000914378 | 0.7701      | 358864 | 0.0159894   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00292068  | 0.000947831 | 0.00206129  | 358864 | 0.0159894   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -3.04048e-05 | 0.000925589 | 0.973795    | 358864 | 0.0159894   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.00537178  | 0.00364887  | 0.14098     | 358864 | 0.0159894   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             | -0.00114646  | 0.00349636  | 0.742988    | 358864 | 0.0159894   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.00547549  | 0.00309139  | 0.0765336   | 358864 | 0.0159894   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.00655432  | 0.00311216  | 0.035207    | 358864 | 0.0159894   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.00199718  | 0.00333859  | 0.549703    | 358864 | 0.0159894   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.00998331  | 0.00350829  | 0.00443435  | 358864 | 0.0159894   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.00383811  | 0.00348448  | 0.270691    | 358864 | 0.0159894   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.00801267  | 0.00169301  | 2.22113e-06 | 358864 | 0.0159894   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.003544    | 0.00162081  | 0.0287798   | 358864 | 0.0159894   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.021813    | 0.00145473  | 0           | 358864 | 0.0159894   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.027326    | 0.00142897  | 0           | 358864 | 0.0159894   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0248244   | 0.00156046  | 0           | 358864 | 0.0159894   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0341254   | 0.00155293  | 0           | 358864 | 0.0159894   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0338323   | 0.00160991  | 0           | 358864 | 0.0159894   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00112598  | 0.00099471  | 0.257652    | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -5.6405e-05  | 0.000946528 | 0.952481    | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00103257  | 0.000796658 | 0.194939    | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.000562637 | 0.00082303  | 0.494221    | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.000362556 | 0.00090325  | 0.688135    | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00308262  | 0.000936755 | 0.00100001  | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.000214687 | 0.000913772 | 0.814252    | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.00931515  | 0.00467403  | 0.046272    | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.00133786  | 0.00458976  | 0.770679    | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.00112934  | 0.0039989   | 0.777629    | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.00261512  | 0.00400671  | 0.513962    | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.00301619  | 0.00440447  | 0.493472    | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.0128057   | 0.0045321   | 0.00472197  | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.00660867  | 0.00440938  | 0.133939    | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.0076481   | 0.00181306  | 2.46601e-05 | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.00494377  | 0.00175921  | 0.00495276  | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0239807   | 0.00159249  | 0           | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0286484   | 0.00155227  | 0           | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0239524   | 0.00170962  | 0           | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0347653   | 0.00168198  | 0           | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0340507   | 0.00171804  | 0           | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_len              |  0.000424012 | 0.000857895 | 0.621134    | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_len              |  0.00185232  | 0.000816911 | 0.0233662   | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_len              | -0.00184359  | 0.000666939 | 0.00570761  | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_len               |  0.00282405  | 0.000684027 | 3.65682e-05 | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_len               | -0.00136843  | 0.000736873 | 0.0633071   | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated_X_len               | -0.000968257 | 0.000736445 | 0.188593    | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated_X_len               | -0.000373202 | 0.000794823 | 0.638685    | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:disp_X_len                 | -0.00325314  | 0.00155871  | 0.0368872   | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:disp_X_len                 | -0.0074067   | 0.00150114  | 8.08323e-07 | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_X_len                 | -0.00974478  | 0.00130381  | 7.90479e-14 | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_X_len                  |  0.00665987  | 0.00131288  | 3.93728e-07 | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_X_len                  | -0.00219976  | 0.00142891  | 0.123696    | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:disp_X_len                  |  0.00462324  | 0.00147018  | 0.00166376  | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:disp_X_len                  |  0.00315309  | 0.00150606  | 0.0363007   | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:tXdXlen                    | -0.00413456  | 0.00327965  | 0.207434    | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:tXdXlen                    | -0.0011381   | 0.00319201  | 0.721433    | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:tXdXlen                    | -0.0019872   | 0.00274292  | 0.468774    | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:tXdXlen                     | -0.000937103 | 0.00281289  | 0.739026    | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:tXdXlen                     | -0.00383893  | 0.00307275  | 0.211545    | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:tXdXlen                     | -0.0051337   | 0.0032088   | 0.109632    | 358864 | 0.0180856   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:tXdXlen                     | -0.00478372  | 0.00313261  | 0.12675     | 358864 | 0.0180856   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.000337798 | 0.00122415  | 0.782592    | 358864 | 0.0212446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.000481536 | 0.00117456  | 0.681828    | 358864 | 0.0212446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  9.91302e-05 | 0.00102442  | 0.922911    | 358864 | 0.0212446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00191389  | 0.00102599  | 0.0621315   | 358864 | 0.0212446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.000500645 | 0.00110884  | 0.651628    | 358864 | 0.0212446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00543165  | 0.00116279  | 3.00309e-06 | 358864 | 0.0212446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.000691269 | 0.00114856  | 0.547271    | 358864 | 0.0212446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.0114113   | 0.00520438  | 0.0283391   | 358864 | 0.0212446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.00159588  | 0.00491414  | 0.74537     | 358864 | 0.0212446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.00379202  | 0.00434321  | 0.382618    | 358864 | 0.0212446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.00997437  | 0.00454586  | 0.0282285   | 358864 | 0.0212446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.00145677  | 0.00482874  | 0.762892    | 358864 | 0.0212446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.0171972   | 0.00515268  | 0.000845966 | 358864 | 0.0212446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.00712277  | 0.0051041   | 0.162873    | 358864 | 0.0212446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.0145422   | 0.00244091  | 2.57769e-09 | 358864 | 0.0212446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.00185797  | 0.00232755  | 0.424728    | 358864 | 0.0212446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.027109    | 0.0020916   | 0           | 358864 | 0.0212446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0469161   | 0.00211038  | 0           | 358864 | 0.0212446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0454863   | 0.00228873  | 0           | 358864 | 0.0212446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.0606673   | 0.00228689  | 0           | 358864 | 0.0212446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.0592371   | 0.00239526  | 0           | 358864 | 0.0212446   |

## Pre-trend Joint Tests
| spec           | test                                    |   n_restrictions |   statistic |      pvalue |      n |
|:---------------|:----------------------------------------|-----------------:|------------:|------------:|-------:|
| event_att      | pretrend_att_joint_zero                 |                3 |    0.552381 | 0.907242    | 358864 |
| event_binary_B | pretrend_baseline_joint_zero            |                3 |    7.00292  | 0.0718048   | 358864 |
| event_binary_B | pretrend_displacement_joint_zero        |                3 |   10.9466   | 0.0120184   | 358864 |
| event_binary_D | pretrend_length_displacement_joint_zero |                3 |    2.10873  | 0.550148    | 358864 |
| event_binary_D | pretrend_length_baseline_joint_zero     |                3 |   25.2984   | 1.33738e-05 | 358864 |
| event_score_C  | pretrend_score_baseline_joint_zero      |                3 |    0.655748 | 0.88356     | 358864 |
| event_score_C  | pretrend_score_slope_joint_zero         |                3 |   10.8654   | 0.0124765   | 358864 |