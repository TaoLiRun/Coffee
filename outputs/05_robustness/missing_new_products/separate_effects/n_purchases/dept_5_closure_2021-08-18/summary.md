# Displacement Effect Estimation Summary

- Sample rows: 19,512
- Unique members: 2,439
- Unique closures: 1
- Event FE units: 2,439
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_5_closure_2021-08-18`
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Length-heterogeneity event-study spec skipped: true
- Model type: DDD


## Binary Specs
| spec             | term                  |     n |   r2_within |        coef |         se |      pvalue |
|:-----------------|:----------------------|------:|------------:|------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 19512 |  0.00818087 | -0.00923097 | 0.00208481 | 9.94291e-06 |
| binary_collapsed | post_X_disp           | 19512 |  0.00818087 | -0.0274892  | 0.00598475 | 4.58696e-06 |
| binary_collapsed | post_X_treated_X_disp | 19512 |  0.00818087 | -0.0271327  | 0.0241433  | 0.2612      |

## Score Spec
| spec            | term                   |     n |   r2_within |       coef |         se |      pvalue |
|:----------------|:-----------------------|------:|------------:|-----------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 19512 |   0.0123917 | -0.0240113 | 0.00523915 | 4.81343e-06 |
| score_collapsed | post_X_score           | 19512 |   0.0123917 | -0.0452109 | 0.00865061 | 1.87589e-07 |
| score_collapsed | post_X_treated_X_score | 19512 |   0.0123917 | -0.0669217 | 0.0219855  | 0.00236029  |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.0161261   | 0.00432019 | 0.000193756 | 19512 |  0.00161507 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.0142184   | 0.00417768 | 0.000676208 | 19512 |  0.00161507 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00870249  | 0.00242844 | 0.000345566 | 19512 |  0.00161507 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.0011962   | 0.00298211 | 0.688364    | 19512 |  0.00161507 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.000748905 | 0.00355316 | 0.833083    | 19512 |  0.00161507 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00706874  | 0.00325381 | 0.0299177   | 19512 |  0.00161507 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00579333  | 0.00314765 | 0.0658128   | 19512 |  0.00161507 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.0119048   | 0.00388829 | 0.00222486  | 19512 |  0.0181928  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.00891796  | 0.00344801 | 0.00975563  | 19512 |  0.0181928  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00179845  | 0.00184677 | 0.330236    | 19512 |  0.0181928  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00564468  | 0.00262532 | 0.0316458   | 19512 |  0.0181928  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00520435  | 0.00316821 | 0.100579    | 19512 |  0.0181928  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0029815   | 0.00290991 | 0.305653    | 19512 |  0.0181928  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.000472159 | 0.00283335 | 0.867664    | 19512 |  0.0181928  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0633478   | 0.0391484  | 0.10576     | 19512 |  0.0181928  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.138412    | 0.0405317  | 0.00064845  | 19512 |  0.0181928  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0869461   | 0.0194142  | 7.86419e-06 | 19512 |  0.0181928  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.0435956   | 0.0245061  | 0.0753687   | 19512 |  0.0181928  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.0323328   | 0.030268   | 0.285528    | 19512 |  0.0181928  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.063299    | 0.0249069  | 0.0111018   | 19512 |  0.0181928  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.0409483   | 0.0183134  | 0.0254432   | 19512 |  0.0181928  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.0126942   | 0.0101969  | 0.213285    | 19512 |  0.0181928  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.00450301  | 0.00965977 | 0.641142    | 19512 |  0.0181928  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                | -0.026547    | 0.00911713 | 0.00362651  | 19512 |  0.0181928  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0214201   | 0.00935043 | 0.0220593   | 19512 |  0.0181928  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0253883   | 0.0101487  | 0.0124275   | 19512 |  0.0181928  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0606145   | 0.00900921 | 2.13527e-11 | 19512 |  0.0181928  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0372719   | 0.0100652  | 0.000217767 | 19512 |  0.0181928  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.0419583   | 0.0097793  | 1.85209e-05 | 19512 |  0.0288756  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.059258    | 0.0106405  | 2.84106e-08 | 19512 |  0.0288756  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0253079   | 0.00539865 | 2.91344e-06 | 19512 |  0.0288756  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00523341  | 0.00652921 | 0.422898    | 19512 |  0.0288756  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00294691  | 0.00721793 | 0.683106    | 19512 |  0.0288756  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0127504   | 0.00626105 | 0.0418123   | 19512 |  0.0288756  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0095483   | 0.00535745 | 0.0748335   | 19512 |  0.0288756  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.14883     | 0.0419701  | 0.000398339 | 19512 |  0.0288756  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.239591    | 0.0445824  | 8.42588e-08 | 19512 |  0.0288756  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.120052    | 0.0232429  | 2.59778e-07 | 19512 |  0.0288756  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.0516194   | 0.0273178  | 0.0589315   | 19512 |  0.0288756  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.0428439   | 0.0294722  | 0.146157    | 19512 |  0.0288756  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.0875389   | 0.025505   | 0.000608644 | 19512 |  0.0288756  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.0587843   | 0.0227155  | 0.0097152   | 19512 |  0.0288756  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.0128588   | 0.0144738  | 0.374402    | 19512 |  0.0288756  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.0121398   | 0.0137824  | 0.378502    | 19512 |  0.0288756  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered | -0.0506065   | 0.0131517  | 0.000122197 | 19512 |  0.0288756  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0285132   | 0.0136763  | 0.0371857   | 19512 |  0.0288756  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0392656   | 0.0142921  | 0.00605186  | 19512 |  0.0288756  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.0980043   | 0.0129459  | 5.24025e-14 | 19512 |  0.0288756  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.0663859   | 0.0142383  | 3.29291e-06 | 19512 |  0.0288756  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |      pvalue |     n |
|:---------------|:-----------------------------------|-----------------:|------------:|------------:|------:|
| event_att      | pretrend_att_joint_zero            |                3 |     22.3449 | 5.52926e-05 | 19512 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |     12.475  | 0.00592118  | 19512 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |     27.0825 | 5.65736e-06 | 19512 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |     47.2486 | 3.07714e-10 | 19512 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |     47.0867 | 3.33114e-10 | 19512 |