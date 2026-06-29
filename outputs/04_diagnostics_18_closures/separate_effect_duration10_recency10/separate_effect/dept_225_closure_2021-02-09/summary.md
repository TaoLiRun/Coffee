# Displacement Effect Estimation Summary

- Sample rows: 6,136
- Unique members: 767
- Unique closures: 1
- Event FE units: 767
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_225_closure_2021-02-09`
- Closure duration filter days: 10
- Recency filter days: 10
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |        coef |         se |      pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 6136 |   0.0119042 | -0.00729325 | 0.00803258 | 0.364185    |
| binary_collapsed | post_X_disp           | 6136 |   0.0119042 | -0.044373   | 0.00718995 | 1.09554e-09 |
| binary_collapsed | post_X_treated_X_disp | 6136 |   0.0119042 | -0.00787342 | 0.0209586  | 0.70727     |

## Score Spec
| spec            | term                   |    n |   r2_within |       coef |        se |      pvalue |
|:----------------|:-----------------------|-----:|------------:|-----------:|----------:|------------:|
| score_collapsed | post_X_treated         | 6136 |   0.0171564 | -0.0112488 | 0.0110307 | 0.308156    |
| score_collapsed | post_X_score           | 6136 |   0.0171564 | -0.0846231 | 0.0131258 | 2.01681e-10 |
| score_collapsed | post_X_treated_X_score | 6136 |   0.0171564 | -0.0238946 | 0.0425604 | 0.574671    |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00380213  | 0.0162258  | 0.814794    | 6136 | 0.000557776 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00706191  | 0.0166165  | 0.670959    | 6136 | 0.000557776 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0035124   | 0.0159511  | 0.825775    | 6136 | 0.000557776 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.0134188   | 0.0139086  | 0.334958    | 6136 | 0.000557776 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0132033   | 0.0172987  | 0.445548    | 6136 | 0.000557776 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0150487   | 0.0139401  | 0.280695    | 6136 | 0.000557776 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00484829  | 0.0158937  | 0.760414    | 6136 | 0.000557776 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -9.12131e-05 | 0.0140412  | 0.994819    | 6136 | 0.0194394   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0083308   | 0.0143387  | 0.56141     | 6136 | 0.0194394   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00810277  | 0.0150231  | 0.5898      | 6136 | 0.0194394   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00305564  | 0.0153111  | 0.84187     | 6136 | 0.0194394   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0220128   | 0.0174022  | 0.206277    | 6136 | 0.0194394   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0259197   | 0.0118832  | 0.0294719   | 6136 | 0.0194394   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00529036  | 0.0184914  | 0.77488     | 6136 | 0.0194394   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.00689121  | 0.0300562  | 0.818714    | 6136 | 0.0194394   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0023308   | 0.0305582  | 0.939221    | 6136 | 0.0194394   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0206361   | 0.0291251  | 0.478829    | 6136 | 0.0194394   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0183444   | 0.0263207  | 0.486041    | 6136 | 0.0194394   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.0155461   | 0.0325606  | 0.633177    | 6136 | 0.0194394   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.0191197   | 0.025722   | 0.457515    | 6136 | 0.0194394   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.017957    | 0.0303306  | 0.553996    | 6136 | 0.0194394   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.00571748  | 0.0103428  | 0.580562    | 6136 | 0.0194394   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.0392634   | 0.0112347  | 0.000501614 | 6136 | 0.0194394   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.051103    | 0.0106446  | 1.90007e-06 | 6136 | 0.0194394   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.015931    | 0.00991869 | 0.108651    | 6136 | 0.0194394   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.00764755  | 0.0124039  | 0.537718    | 6136 | 0.0194394   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0378154   | 0.0113933  | 0.000945824 | 6136 | 0.0194394   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.020014    | 0.0115477  | 0.0834713   | 6136 | 0.0194394   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00355101  | 0.0158357  | 0.822629    | 6136 | 0.0281015   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0072106   | 0.0161902  | 0.65618     | 6136 | 0.0281015   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00318568  | 0.0153179  | 0.835307    | 6136 | 0.0281015   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.0132099   | 0.0136131  | 0.332162    | 6136 | 0.0281015   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0132228   | 0.0169429  | 0.435378    | 6136 | 0.0281015   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0150745   | 0.0134767  | 0.263675    | 6136 | 0.0281015   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00396203  | 0.0153248  | 0.796062    | 6136 | 0.0281015   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.0246935   | 0.0574805  | 0.667609    | 6136 | 0.0281015   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.000563289 | 0.0562166  | 0.992008    | 6136 | 0.0281015   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.00820346  | 0.0501847  | 0.870195    | 6136 | 0.0281015   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.0118032   | 0.0487622  | 0.808801    | 6136 | 0.0281015   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.00629114  | 0.0638048  | 0.921482    | 6136 | 0.0281015   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.0194229   | 0.0513301  | 0.705244    | 6136 | 0.0281015   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             | -0.0760288   | 0.0518445  | 0.142929    | 6136 | 0.0281015   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.00172091  | 0.0182492  | 0.924895    | 6136 | 0.0281015   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.0613062   | 0.0189588  | 0.00127452  | 6136 | 0.0281015   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.103832    | 0.0178326  | 8.52047e-09 | 6136 | 0.0281015   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0373089   | 0.0169992  | 0.0284821   | 6136 | 0.0281015   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0195275   | 0.0217589  | 0.369761    | 6136 | 0.0281015   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.0750091   | 0.020333   | 0.00024103  | 6136 | 0.0281015   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.0432294   | 0.0208531  | 0.0385022   | 6136 | 0.0281015   |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                3 |    0.855923 | 0.836049 | 6136 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |    0.694795 | 0.874428 | 6136 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |    0.616126 | 0.892731 | 6136 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |    0.853368 | 0.836664 | 6136 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |    0.372411 | 0.945881 | 6136 |