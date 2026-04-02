# Displacement Effect Estimation Summary

- Sample rows: 136,464
- Unique members: 17,058
- Unique closures: 22
- Event FE units: 17,058
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=false
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: True
- Model type: DDD


## Binary Specs
| spec             | term                  |     n |   r2_within |       coef |         se |      pvalue |
|:-----------------|:----------------------|------:|------------:|-----------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 62835 |  0.00128214 |  0.0676744 | 0.0133568  | 4.10458e-07 |
| binary_collapsed | post_X_disp           | 62835 |  0.00128214 |  0.0550812 | 0.00906894 | 1.28589e-09 |
| binary_collapsed | post_X_treated_X_disp | 62835 |  0.00128214 | -0.0477725 | 0.0159919  | 0.00281998  |

## Score Spec
| spec            | term                   |     n |   r2_within |       coef |        se |      pvalue |
|:----------------|:-----------------------|------:|------------:|-----------:|----------:|------------:|
| score_collapsed | post_X_treated         | 62835 |  0.00134497 |  0.0511852 | 0.0092584 | 3.29255e-08 |
| score_collapsed | post_X_score           | 62835 |  0.00134497 |  0.0873741 | 0.0133571 | 6.32541e-11 |
| score_collapsed | post_X_treated_X_score | 62835 |  0.00134497 | -0.0665827 | 0.0243629 | 0.00628556  |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0236056   | 0.0136663  | 0.0841405   | 62835 |  0.0012886  |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.013122    | 0.0137929  | 0.341443    | 62835 |  0.0012886  |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0248026   | 0.0133466  | 0.0631425   | 62835 |  0.0012886  |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0679296   | 0.0140704  | 1.39625e-06 | 62835 |  0.0012886  |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0111859   | 0.0142629  | 0.432899    | 62835 |  0.0012886  |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0103536   | 0.0143572  | 0.470833    | 62835 |  0.0012886  |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0100262   | 0.0143469  | 0.484663    | 62835 |  0.0012886  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0522048   | 0.0254584  | 0.0403268   | 62835 |  0.00257051 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0488639   | 0.0257369  | 0.0576407   | 62835 |  0.00257051 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0469674   | 0.0267305  | 0.0789294   | 62835 |  0.00257051 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0890732   | 0.0255552  | 0.000492805 | 62835 |  0.00257051 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0376878   | 0.0250792  | 0.132929    | 62835 |  0.00257051 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00244998  | 0.0258127  | 0.924385    | 62835 |  0.00257051 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00920272  | 0.0258298  | 0.721635    | 62835 |  0.00257051 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0502726   | 0.030109   | 0.0950058   | 62835 |  0.00257051 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0567438   | 0.0304259  | 0.062206    | 62835 |  0.00257051 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0303451   | 0.0306528  | 0.322211    | 62835 |  0.00257051 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0261572   | 0.0305475  | 0.391859    | 62835 |  0.00257051 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.0310844   | 0.030596   | 0.309666    | 62835 |  0.00257051 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              | -0.0102578   | 0.0310997  | 0.741528    | 62835 |  0.00257051 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.011317    | 0.0310904  | 0.715862    | 62835 |  0.00257051 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.012655    | 0.0170871  | 0.458941    | 62835 |  0.00257051 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                | -0.00142831  | 0.0167754  | 0.932149    | 62835 |  0.00257051 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                | -0.0187061   | 0.0175666  | 0.286954    | 62835 |  0.00257051 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  0.046614    | 0.0163724  | 0.00441886  | 62835 |  0.00257051 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.0683682   | 0.0165513  | 3.63961e-05 | 62835 |  0.00257051 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.0526753   | 0.017576   | 0.00273175  | 62835 |  0.00257051 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.0469804   | 0.0174369  | 0.00706281  | 62835 |  0.00257051 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0511461   | 0.0254912  | 0.044832    | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0469599   | 0.025776   | 0.0685019   | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0473511   | 0.0268381  | 0.077701    | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0853604   | 0.0257634  | 0.000924767 | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0358161   | 0.0251082  | 0.153757    | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.000675963 | 0.0258594  | 0.979146    | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0154904   | 0.0258996  | 0.549788    | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0370997   | 0.0312469  | 0.235128    | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0450071   | 0.0314672  | 0.152659    | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0234999   | 0.0316153  | 0.45731     | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.043095    | 0.0321317  | 0.17988     | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.0332701   | 0.0315175  | 0.291168    | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              | -0.0130071   | 0.0323019  | 0.687195    | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.00774246  | 0.032139   | 0.809632    | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.013778    | 0.0171056  | 0.420565    | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                | -0.000322143 | 0.0167793  | 0.984683    | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                | -0.0201517   | 0.0175674  | 0.25136     | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  0.0458004   | 0.01637    | 0.0051524   | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.0693206   | 0.0165504  | 2.82738e-05 | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.0518633   | 0.0175861  | 0.00319265  | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.0452597   | 0.017452   | 0.00951441  | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_len              | -0.0111741   | 0.0201786  | 0.579751    | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_len              | -0.0389258   | 0.0199027  | 0.0505102   | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_len              |  0.0131116   | 0.0193928  | 0.498985    | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_len               |  0.017896    | 0.0195283  | 0.359467    | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_len               | -0.0324578   | 0.0195674  | 0.0971866   | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated_X_len               | -0.0214785   | 0.0195018  | 0.270761    | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated_X_len               | -0.060027    | 0.0213584  | 0.00495452  | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:disp_X_len                 | -0.00119341  | 0.00970213 | 0.902105    | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:disp_X_len                 | -0.000715969 | 0.00874669 | 0.934762    | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_X_len                 |  0.0146631   | 0.00747609 | 0.0498619   | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_X_len                  |  0.000787141 | 0.0080763  | 0.92236     | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_X_len                  | -0.0223571   | 0.0087752  | 0.0108533   | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:disp_X_len                  | -0.0190779   | 0.00964365 | 0.0479177   | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:disp_X_len                  | -0.0651398   | 0.0127996  | 3.6463e-07  | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:tXdXlen                    |  0.0325458   | 0.0249215  | 0.1916      | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:tXdXlen                    |  0.0528079   | 0.0247139  | 0.0326352   | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:tXdXlen                    | -0.0130102   | 0.0237085  | 0.583181    | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:tXdXlen                     |  0.00703649  | 0.02491    | 0.777583    | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:tXdXlen                     |  0.0453782   | 0.0252978  | 0.0728745   | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:tXdXlen                     |  0.0286459   | 0.025071   | 0.25323     | 62835 |  0.00400618 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:tXdXlen                     |  0.0853581   | 0.026681   | 0.00138141  | 62835 |  0.00400618 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0397291   | 0.017702   | 0.0248284   | 62835 |  0.00256711 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0286724   | 0.0178187  | 0.107615    | 62835 |  0.00256711 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0380749   | 0.0185327  | 0.03995     | 62835 |  0.00256711 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0785613   | 0.0177217  | 9.36702e-06 | 62835 |  0.00256711 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.023429    | 0.017445   | 0.17929     | 62835 |  0.00256711 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.00364107  | 0.0179194  | 0.838988    | 62835 |  0.00256711 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00498271  | 0.0179293  | 0.781087    | 62835 |  0.00256711 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.106747    | 0.0456103  | 0.019277    | 62835 |  0.00256711 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.0903022   | 0.0459248  | 0.049285    | 62835 |  0.00256711 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.0597369   | 0.047156   | 0.205252    | 62835 |  0.00256711 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.026312    | 0.0457642  | 0.565337    | 62835 |  0.00256711 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.0172869   | 0.0457054  | 0.70527     | 62835 |  0.00256711 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.0104173   | 0.0458773  | 0.820374    | 62835 |  0.00256711 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.0239768   | 0.0462839  | 0.604441    | 62835 |  0.00256711 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered |  0.00441867  | 0.0252257  | 0.860953    | 62835 |  0.00256711 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered | -0.00181023  | 0.0249004  | 0.942047    | 62835 |  0.00256711 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered | -0.0250923   | 0.0260592  | 0.335616    | 62835 |  0.00256711 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  |  0.074853    | 0.0237364  | 0.00161693  | 62835 |  0.00256711 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  |  0.102268    | 0.024304   | 2.59536e-05 | 62835 |  0.00256711 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  |  0.079096    | 0.0256395  | 0.0020403   | 62835 |  0.00256711 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  |  0.0738535   | 0.0251753  | 0.00335677  | 62835 |  0.00256711 |

## Pre-trend Joint Tests
| spec           | test                                    |   n_restrictions |   statistic |    pvalue |     n |
|:---------------|:----------------------------------------|-----------------:|------------:|----------:|------:|
| event_att      | pretrend_att_joint_zero                 |                3 |     4.41137 | 0.220334  | 62835 |
| event_binary_B | pretrend_baseline_joint_zero            |                3 |     5.27625 | 0.152651  | 62835 |
| event_binary_B | pretrend_displacement_joint_zero        |                3 |     4.06771 | 0.254245  | 62835 |
| event_binary_D | pretrend_length_displacement_joint_zero |                3 |     8.79713 | 0.0321134 | 62835 |
| event_binary_D | pretrend_length_baseline_joint_zero     |                3 |     7.7989  | 0.050356  | 62835 |
| event_score_C  | pretrend_score_baseline_joint_zero      |                3 |     6.14482 | 0.104773  | 62835 |
| event_score_C  | pretrend_score_slope_joint_zero         |                3 |     6.13456 | 0.105244  | 62835 |