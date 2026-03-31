# Displacement Effect Estimation Summary

- Sample rows: 13,784
- Unique members: 1,723
- Unique closures: 22
- Event FE units: 1,723
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=false
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: True


## Binary Specs
| spec             | term                  |     n |   r2_within |       coef |        se |    pvalue |
|:-----------------|:----------------------|------:|------------:|-----------:|----------:|----------:|
| binary_collapsed | post_X_treated        | 13784 |  0.00132249 |  0.0818672 | 0.0868992 | 0.346277  |
| binary_collapsed | post_X_disp           | 13784 |  0.00132249 |  0.107972  | 0.0530476 | 0.0419654 |
| binary_collapsed | post_X_treated_X_disp | 13784 |  0.00132249 | -0.0513753 | 0.0879665 | 0.559275  |

## Score Spec
| spec            | term                   |     n |   r2_within |       coef |        se |    pvalue |
|:----------------|:-----------------------|------:|------------:|-----------:|----------:|----------:|
| score_collapsed | post_X_treated         | 13784 |   0.0011661 |  0.0323747 | 0.0144259 | 0.0249459 |
| score_collapsed | post_X_score           | 13784 |   0.0011661 |  0.115589  | 0.0500797 | 0.0211118 |
| score_collapsed | post_X_treated_X_score | 13784 |   0.0011661 | -0.0729666 | 0.101542  | 0.472494  |

## Event-study Specs
| spec           | term                                                              |         coef |        se |      pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|----------:|------------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0243757   | 0.0270804 | 0.368181    | 13784 |  0.00116384 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.000992052 | 0.0273212 | 0.971039    | 13784 |  0.00116384 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0166945   | 0.0251267 | 0.506516    | 13784 |  0.00116384 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0410109   | 0.0274631 | 0.135539    | 13784 |  0.00116384 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0415101   | 0.0279822 | 0.138138    | 13784 |  0.00116384 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0176313   | 0.0263784 | 0.50397     | 13784 |  0.00116384 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0213173   | 0.0253747 | 0.40097     | 13784 |  0.00116384 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.223912    | 0.159573  | 0.160739    | 13784 |  0.00279422 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0710213   | 0.174722  | 0.684439    | 13784 |  0.00279422 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.138091    | 0.14344   | 0.335828    | 13784 |  0.00279422 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.0209217   | 0.16209   | 0.897314    | 13784 |  0.00279422 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0274659   | 0.152196  | 0.85681     | 13784 |  0.00279422 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0342042   | 0.178325  | 0.847915    | 13784 |  0.00279422 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0230824   | 0.126962  | 0.855757    | 13784 |  0.00279422 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.207938    | 0.162151  | 0.199882    | 13784 |  0.00279422 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0757511   | 0.176657  | 0.668121    | 13784 |  0.00279422 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.12859     | 0.145496  | 0.376924    | 13784 |  0.00279422 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.0687487   | 0.164625  | 0.676286    | 13784 |  0.00279422 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.0758576   | 0.155101  | 0.624844    | 13784 |  0.00279422 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.055553    | 0.180254  | 0.757973    | 13784 |  0.00279422 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.00579527  | 0.129603  | 0.964339    | 13784 |  0.00279422 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.103802    | 0.0883206 | 0.240044    | 13784 |  0.00279422 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                | -0.00475002  | 0.078905  | 0.952004    | 13784 |  0.00279422 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.00498499  | 0.0913218 | 0.956474    | 13784 |  0.00279422 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  0.102476    | 0.0926596 | 0.268907    | 13784 |  0.00279422 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.0917841   | 0.0885161 | 0.299919    | 13784 |  0.00279422 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.016415    | 0.105476  | 0.876344    | 13784 |  0.00279422 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.117118    | 0.0794756 | 0.140764    | 13784 |  0.00279422 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.235765    | 0.160925  | 0.143086    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0739271   | 0.157998  | 0.639917    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.105056    | 0.131211  | 0.423435    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.0155366   | 0.16115   | 0.923206    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0357913   | 0.164385  | 0.827666    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0220063   | 0.183637  | 0.904627    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0591832   | 0.136998  | 0.665796    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.20757     | 0.163478  | 0.204359    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0710903   | 0.16032   | 0.657513    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0865242   | 0.133672  | 0.517531    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.0587048   | 0.163849  | 0.720173    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.086291    | 0.166735  | 0.60485     | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.0361936   | 0.18559   | 0.845401    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.0317368   | 0.139171  | 0.81964     | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.102926    | 0.0886844 | 0.245972    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                | -0.00437361  | 0.078961  | 0.955835    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.00589124  | 0.0912684 | 0.948541    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  0.0994378   | 0.0929426 | 0.284821    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.0843029   | 0.08974   | 0.347651    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.00930917  | 0.105861  | 0.929936    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.0850102   | 0.0847272 | 0.315837    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_len              | -0.0435522   | 0.153709  | 0.776949    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_len              | -0.0178693   | 0.143682  | 0.901039    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_len              |  0.174725    | 0.0756521 | 0.021029    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_len               |  0.0485022   | 0.133163  | 0.715731    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_len               | -0.0241383   | 0.148838  | 0.871185    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated_X_len               |  0.0948018   | 0.147551  | 0.520634    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated_X_len               | -0.079629    | 0.106456  | 0.454563    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:disp_X_len                 |  0.0126705   | 0.0159345 | 0.426629    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:disp_X_len                 |  0.00565822  | 0.0136249 | 0.677985    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_X_len                 |  0.0246148   | 0.0115085 | 0.0325886   | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_X_len                  |  0.00221422  | 0.0117009 | 0.849931    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_X_len                  | -0.0208108   | 0.0137365 | 0.129956    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:disp_X_len                  |  0.00183908  | 0.0151526 | 0.903411    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:disp_X_len                  | -0.106971    | 0.0258894 | 3.77142e-05 | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:tXdXlen                    |  0.0683702   | 0.155713  | 0.66066     | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:tXdXlen                    |  0.0390708   | 0.145448  | 0.788252    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:tXdXlen                    | -0.179257    | 0.078866  | 0.0231534   | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:tXdXlen                     | -0.0567156   | 0.135415  | 0.675395    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:tXdXlen                     |  0.0216654   | 0.150934  | 0.885878    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:tXdXlen                     | -0.10694     | 0.149329  | 0.474003    | 13784 |  0.00675368 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:tXdXlen                     |  0.103322    | 0.109109  | 0.343793    | 13784 |  0.00675368 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0253335   | 0.0266217 | 0.341427    | 13784 |  0.0025055  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.000878423 | 0.0268305 | 0.973886    | 13784 |  0.0025055  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0140769   | 0.0250374 | 0.574029    | 13784 |  0.0025055  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0447674   | 0.0274663 | 0.103304    | 13784 |  0.0025055  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.045118    | 0.0281613 | 0.10931     | 13784 |  0.0025055  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0196048   | 0.0261664 | 0.453816    | 13784 |  0.0025055  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0194075   | 0.0256689 | 0.44971     | 13784 |  0.0025055  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.104993    | 0.18956   | 0.579736    | 13784 |  0.0025055  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.0463312   | 0.197401  | 0.814465    | 13784 |  0.0025055  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.111963    | 0.178786  | 0.53124     | 13784 |  0.0025055  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.0396471   | 0.194713  | 0.838676    | 13784 |  0.0025055  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.0210979   | 0.180123  | 0.90677     | 13784 |  0.0025055  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.0483706   | 0.197968  | 0.807       | 13784 |  0.0025055  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             | -0.140014    | 0.165397  | 0.397375    | 13784 |  0.0025055  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.0949904   | 0.0921865 | 0.30296     | 13784 |  0.0025055  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.00436298  | 0.0821795 | 0.957666    | 13784 |  0.0025055  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0120561   | 0.094887  | 0.898909    | 13784 |  0.0025055  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  |  0.0952444   | 0.0935413 | 0.308722    | 13784 |  0.0025055  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  |  0.101752    | 0.0922698 | 0.270282    | 13784 |  0.0025055  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  |  0.0239954   | 0.0980278 | 0.806655    | 13784 |  0.0025055  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  |  0.16134     | 0.0860801 | 0.0610587   | 13784 |  0.0025055  |

## Pre-trend Joint Tests
| spec           | test                                    |   n_restrictions |   statistic |    pvalue |     n |
|:---------------|:----------------------------------------|-----------------:|------------:|----------:|------:|
| event_att      | pretrend_att_joint_zero                 |                3 |    1.48419  | 0.685924  | 13784 |
| event_binary_B | pretrend_baseline_joint_zero            |                3 |    3.54668  | 0.314759  | 13784 |
| event_binary_B | pretrend_displacement_joint_zero        |                3 |    2.7756   | 0.427532  | 13784 |
| event_binary_D | pretrend_length_displacement_joint_zero |                3 |    8.03701  | 0.045253  | 13784 |
| event_binary_D | pretrend_length_baseline_joint_zero     |                3 |    8.16776  | 0.0426689 | 13784 |
| event_score_C  | pretrend_score_baseline_joint_zero      |                3 |    1.49575  | 0.683251  | 13784 |
| event_score_C  | pretrend_score_slope_joint_zero         |                3 |    0.628703 | 0.889831  | 13784 |