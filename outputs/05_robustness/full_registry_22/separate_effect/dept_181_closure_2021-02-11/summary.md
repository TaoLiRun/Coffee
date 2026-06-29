# Displacement Effect Estimation Summary

- Sample rows: 3,528
- Unique members: 441
- Unique closures: 1
- Event FE units: 441
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_181_closure_2021-02-11`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |        coef |         se |    pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|-----------:|----------:|
| binary_collapsed | post_X_treated        | 3528 |   0.0186496 |  0.00451297 | 0.00894363 | 0.614091  |
| binary_collapsed | post_X_disp           | 3528 |   0.0186496 | -0.0404752  | 0.00929685 | 1.667e-05 |
| binary_collapsed | post_X_treated_X_disp | 3528 |   0.0186496 | -0.0101381  | 0.0298998  | 0.734719  |

## Score Spec
| spec            | term                   |    n |   r2_within |         coef |        se |      pvalue |
|:----------------|:-----------------------|-----:|------------:|-------------:|----------:|------------:|
| score_collapsed | post_X_treated         | 3528 |   0.0265574 | -0.000755814 | 0.0112281 | 0.946362    |
| score_collapsed | post_X_score           | 3528 |   0.0265574 | -0.06527     | 0.0140137 | 4.24392e-06 |
| score_collapsed | post_X_treated_X_score | 3528 |   0.0265574 | -0.0286387   | 0.0428929 | 0.504688    |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.0415332   | 0.0211127  | 0.0497863   | 3528 |  0.00657325 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.0518796   | 0.0271722  | 0.0568754   | 3528 |  0.00657325 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0314324   | 0.0199813  | 0.116418    | 3528 |  0.00657325 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0545908   | 0.0174966  | 0.001927    | 3528 |  0.00657325 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0198122   | 0.0174227  | 0.256095    | 3528 |  0.00657325 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00430447  | 0.0141188  | 0.760605    | 3528 |  0.00657325 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0122707   | 0.0180558  | 0.497117    | 3528 |  0.00657325 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.012757    | 0.0119411  | 0.285958    | 3528 |  0.0358833  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.00524805  | 0.0111793  | 0.638986    | 3528 |  0.0358833  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00507234  | 0.0113078  | 0.653962    | 3528 |  0.0358833  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0266034   | 0.0144721  | 0.0666985   | 3528 |  0.0358833  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00704036  | 0.0171464  | 0.681563    | 3528 |  0.0358833  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00657178  | 0.00891292 | 0.461314    | 3528 |  0.0358833  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.000913723 | 0.00953989 | 0.92374     | 3528 |  0.0358833  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0711132   | 0.0425783  | 0.0955959   | 3528 |  0.0358833  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.102865    | 0.0533407  | 0.054443    | 3528 |  0.0358833  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0500458   | 0.0397917  | 0.20917     | 3528 |  0.0358833  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.0720365   | 0.0351598  | 0.0410712   | 3528 |  0.0358833  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.0458587   | 0.0356597  | 0.199116    | 3528 |  0.0358833  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.0205816   | 0.0291147  | 0.479993    | 3528 |  0.0358833  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.0449942   | 0.0366723  | 0.220507    | 3528 |  0.0358833  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.0395115   | 0.0161285  | 0.0146826   | 3528 |  0.0358833  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                | -0.0311474   | 0.0153332  | 0.0428183   | 3528 |  0.0358833  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.00392248  | 0.0143413  | 0.78459     | 3528 |  0.0358833  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0460625   | 0.0117312  | 0.000100029 | 3528 |  0.0358833  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0555268   | 0.0136507  | 5.62724e-05 | 3528 |  0.0358833  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0664691   | 0.0157178  | 2.85821e-05 | 3528 |  0.0358833  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0605786   | 0.0148575  | 5.40759e-05 | 3528 |  0.0358833  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.0335006   | 0.0163047  | 0.040502    | 3528 |  0.0454296  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.0404485   | 0.0211416  | 0.0563688   | 3528 |  0.0454296  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0205418   | 0.0156218  | 0.189211    | 3528 |  0.0454296  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0516711   | 0.015161   | 0.000714229 | 3528 |  0.0454296  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0197797   | 0.0168458  | 0.240965    | 3528 |  0.0454296  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00901976  | 0.0106817  | 0.398899    | 3528 |  0.0454296  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0109972   | 0.0123393  | 0.373288    | 3528 |  0.0454296  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.107117    | 0.0631981  | 0.090794    | 3528 |  0.0454296  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.127123    | 0.0688979  | 0.0656969   | 3528 |  0.0454296  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.0936544   | 0.0492945  | 0.0581001   | 3528 |  0.0454296  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.0695301   | 0.0498158  | 0.163495    | 3528 |  0.0454296  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.0509081   | 0.0449678  | 0.258208    | 3528 |  0.0454296  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.0238599   | 0.0431449  | 0.580532    | 3528 |  0.0454296  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.069041    | 0.0643277  | 0.283738    | 3528 |  0.0454296  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.0643834   | 0.0226899  | 0.00475649  | 3528 |  0.0454296  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered | -0.0482643   | 0.0227001  | 0.0340451   | 3528 |  0.0454296  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.00104818  | 0.0209614  | 0.960141    | 3528 |  0.0454296  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0758068   | 0.0169928  | 1.03669e-05 | 3528 |  0.0454296  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0867163   | 0.0200606  | 1.90779e-05 | 3528 |  0.0454296  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.110779    | 0.0231068  | 2.23835e-06 | 3528 |  0.0454296  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.0993777   | 0.0216341  | 5.69746e-06 | 3528 |  0.0454296  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                3 |     4.23522 | 0.237159 | 3528 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |     1.41793 | 0.701336 | 3528 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |     3.75801 | 0.288808 | 3528 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |     4.53601 | 0.209101 | 3528 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |     5.26803 | 0.153191 | 3528 |