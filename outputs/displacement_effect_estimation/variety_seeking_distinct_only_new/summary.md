# Displacement Effect Estimation Summary

- Sample rows: 321,184
- Unique members: 40,148
- Unique closures: 18
- Event FE units: 40,148
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=false
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Model type: DDD
- Event-study reference period: -1


## Binary Specs
| spec             | term                  |     n |   r2_within |        coef |         se |      pvalue |
|:-----------------|:----------------------|------:|------------:|------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 99644 | 0.000755907 |  0.00804591 | 0.00916266 | 0.379888    |
| binary_collapsed | post_X_disp           | 99644 | 0.000755907 |  0.0300485  | 0.00500086 | 1.89819e-09 |
| binary_collapsed | post_X_treated_X_disp | 99644 | 0.000755907 | -0.0417174  | 0.0114672  | 0.000275368 |

## Score Spec
| spec            | term                   |     n |   r2_within |       coef |         se |      pvalue |
|:----------------|:-----------------------|------:|------------:|-----------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 99644 | 0.000702329 | -0.0033179 | 0.00779034 | 0.670186    |
| score_collapsed | post_X_score           | 99644 | 0.000702329 |  0.046849  | 0.00774491 | 1.47958e-09 |
| score_collapsed | post_X_treated_X_score | 99644 | 0.000702329 | -0.0486139 | 0.0174677  | 0.00538903  |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.0156277   | 0.00905603 | 0.0844199   | 99644 | 0.000262061 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.0121175   | 0.0095657  | 0.205252    | 99644 | 0.000262061 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.000536251 | 0.00930073 | 0.954022    | 99644 | 0.000262061 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.004205    | 0.00933646 | 0.652437    | 99644 | 0.000262061 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0152482   | 0.01116    | 0.171849    | 99644 | 0.000262061 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0186551   | 0.0106739  | 0.0805222   | 99644 | 0.000262061 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00783792  | 0.00988341 | 0.427764    | 99644 | 0.000262061 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.000586762 | 0.016222   | 0.971147    | 99644 | 0.00121359  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0017261   | 0.0173263  | 0.920644    | 99644 | 0.00121359  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00431836  | 0.0181552  | 0.811993    | 99644 | 0.00121359  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00606452  | 0.0171632  | 0.723834    | 99644 | 0.00121359  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00538422  | 0.0192633  | 0.779859    | 99644 | 0.00121359  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00754107  | 0.0186675  | 0.68624     | 99644 | 0.00121359  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00815957  | 0.0175105  | 0.641233    | 99644 | 0.00121359  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0251072   | 0.0195444  | 0.198937    | 99644 | 0.00121359  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0213796   | 0.0207153  | 0.302051    | 99644 | 0.00121359  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.00476292  | 0.0209956  | 0.820539    | 99644 | 0.00121359  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0155302   | 0.0203331  | 0.445001    | 99644 | 0.00121359  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.0335538   | 0.0236244  | 0.155533    | 99644 | 0.00121359  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              | -0.0438429   | 0.0227112  | 0.0535633   | 99644 | 0.00121359  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.0263951   | 0.0211045  | 0.211061    | 99644 | 0.00121359  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.0215207   | 0.00785713 | 0.00616736  | 99644 | 0.00121359  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.0192259   | 0.00861188 | 0.0255926   | 99644 | 0.00121359  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0183883   | 0.00857282 | 0.0319667   | 99644 | 0.00121359  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  0.0374098   | 0.00866918 | 1.60065e-05 | 99644 | 0.00121359  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.057648    | 0.00987861 | 5.42933e-09 | 99644 | 0.00121359  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.0533915   | 0.010028   | 1.02306e-07 | 99644 | 0.00121359  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.0334146   | 0.0091606  | 0.000265229 | 99644 | 0.00121359  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  8.74652e-07 | 0.0159349  | 0.999956    | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00578951  | 0.0169988  | 0.73342     | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00344281  | 0.0178046  | 0.846673    | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00456183  | 0.0169059  | 0.787288    | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.006699    | 0.0190107  | 0.724556    | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00324511  | 0.0186098  | 0.861571    | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0105117   | 0.0175864  | 0.550034    | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.022264    | 0.0193199  | 0.249175    | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0191879   | 0.0205184  | 0.349717    | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.00963759  | 0.0208006  | 0.643131    | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.011599    | 0.0208851  | 0.578647    | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.0303404   | 0.0237275  | 0.201014    | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              | -0.028404    | 0.0240291  | 0.237191    | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.0161912   | 0.0223377  | 0.468561    | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.0182431   | 0.00776032 | 0.0187407   | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.0103439   | 0.00852637 | 0.225079    | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.00811591  | 0.00851419 | 0.340488    | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  0.0308734   | 0.00863106 | 0.000348256 | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.0522685   | 0.00979611 | 9.60935e-08 | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.0434719   | 0.0101108  | 1.71843e-05 | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.0285588   | 0.009243   | 0.00200547  | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_len              |  0.00246736  | 0.0145479  | 0.865324    | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_len              |  0.0264696   | 0.014932   | 0.0762964   | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_len              |  0.00867038  | 0.0155564  | 0.577292    | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_len               |  0.00547203  | 0.0145109  | 0.706104    | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_len               | -0.0180583   | 0.0167916  | 0.28219     | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated_X_len               |  0.0271207   | 0.014867   | 0.0681316   | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated_X_len               | -0.0329486   | 0.0151104  | 0.0292283   | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:disp_X_len                 |  0.0117665   | 0.00527659 | 0.0257603   | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:disp_X_len                 |  0.0357705   | 0.00501396 | 1.00187e-12 | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_X_len                 |  0.0374319   | 0.00420719 | 0           | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_X_len                  |  0.0202903   | 0.00480739 | 2.44515e-05 | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_X_len                  |  0.0143932   | 0.00610884 | 0.0184749   | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:disp_X_len                  |  0.0316946   | 0.00589156 | 7.53429e-08 | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:disp_X_len                  | -0.00109202  | 0.00750805 | 0.884359    | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:tXdXlen                    | -0.00371328  | 0.0170642  | 0.827737    | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:tXdXlen                    | -0.0374102   | 0.0176703  | 0.0342595   | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:tXdXlen                    | -0.0329481   | 0.017852   | 0.0649598   | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:tXdXlen                     | -0.0467054   | 0.0173591  | 0.0071388   | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:tXdXlen                     |  0.00323039  | 0.0203973  | 0.874164    | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:tXdXlen                     | -0.0593954   | 0.0183458  | 0.00120727  | 99644 | 0.00315095  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:tXdXlen                     |  0.00925279  | 0.0185218  | 0.617388    | 99644 | 0.00315095  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.0090166   | 0.0139106  | 0.516874    | 99644 | 0.00132866  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.00148676  | 0.014817   | 0.920074    | 99644 | 0.00132866  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00437251  | 0.015552   | 0.778595    | 99644 | 0.00132866  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00409615  | 0.0143849  | 0.775836    | 99644 | 0.00132866  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00739098  | 0.0159535  | 0.643166    | 99644 | 0.00132866  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.00583446  | 0.0155957  | 0.708327    | 99644 | 0.00132866  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00329425  | 0.0148644  | 0.824612    | 99644 | 0.00132866  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.0228252   | 0.0293344  | 0.436517    | 99644 | 0.00132866  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.0339059   | 0.0313932  | 0.280136    | 99644 | 0.00132866  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.00971391  | 0.0317429  | 0.759594    | 99644 | 0.00132866  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.0263422   | 0.029819   | 0.377027    | 99644 | 0.00132866  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.02498     | 0.0343431  | 0.467008    | 99644 | 0.00132866  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             | -0.0448836   | 0.0331623  | 0.175924    | 99644 | 0.00132866  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             | -0.0404302   | 0.0310772  | 0.193285    | 99644 | 0.00132866  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered |  0.0464935   | 0.0120375  | 0.000112593 | 99644 | 0.00132866  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.0375613   | 0.0133178  | 0.00480075  | 99644 | 0.00132866  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0314518   | 0.0135212  | 0.0200209   | 99644 | 0.00132866  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  |  0.0676584   | 0.0130535  | 2.19962e-07 | 99644 | 0.00132866  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  |  0.100436    | 0.0147247  | 9.26415e-12 | 99644 | 0.00132866  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  |  0.0874984   | 0.0150862  | 6.72079e-09 | 99644 | 0.00132866  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  |  0.0525287   | 0.0138087  | 0.000142728 | 99644 | 0.00132866  |

## Pre-trend Joint Tests
| spec           | test                                    |   n_restrictions |   statistic |    pvalue |     n |
|:---------------|:----------------------------------------|-----------------:|------------:|----------:|------:|
| event_att      | pretrend_att_joint_zero                 |                3 |    4.93528  | 0.176598  | 99644 |
| event_binary_B | pretrend_baseline_joint_zero            |                3 |    0.112185 | 0.990336  | 99644 |
| event_binary_B | pretrend_displacement_joint_zero        |                3 |    2.28684  | 0.515046  | 99644 |
| event_binary_D | pretrend_length_displacement_joint_zero |                3 |    7.93247  | 0.0474281 | 99644 |
| event_binary_D | pretrend_length_baseline_joint_zero     |                3 |    4.61588  | 0.202184  | 99644 |
| event_score_C  | pretrend_score_baseline_joint_zero      |                3 |    1.07874  | 0.782209  | 99644 |
| event_score_C  | pretrend_score_slope_joint_zero         |                3 |    1.33495  | 0.720851  | 99644 |