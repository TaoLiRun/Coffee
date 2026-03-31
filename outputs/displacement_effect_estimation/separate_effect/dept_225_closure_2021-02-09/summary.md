# Displacement Effect Estimation Summary

- Sample rows: 19,816
- Unique members: 2,477
- Unique closures: 1
- Event FE units: 2,477
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_225_closure_2021-02-09`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |     n |   r2_within |        coef |         se |   pvalue |
|:-----------------|:----------------------|------:|------------:|------------:|-----------:|---------:|
| binary_collapsed | post_X_treated        | 19816 |   0.0136025 | -0.00163742 | 0.00297321 | 0.581873 |
| binary_collapsed | post_X_disp           | 19816 |   0.0136025 | -0.0395703  | 0.00461297 | 0        |
| binary_collapsed | post_X_treated_X_disp | 19816 |   0.0136025 | -0.00591563 | 0.0143608  | 0.680428 |

## Score Spec
| spec            | term                   |     n |   r2_within |        coef |         se |   pvalue |
|:----------------|:-----------------------|------:|------------:|------------:|-----------:|---------:|
| score_collapsed | post_X_treated         | 19816 |   0.0182609 | -0.00494798 | 0.00458665 | 0.280791 |
| score_collapsed | post_X_score           | 19816 |   0.0182609 | -0.0652718  | 0.00708992 | 0        |
| score_collapsed | post_X_treated_X_score | 19816 |   0.0182609 | -0.0154828  | 0.0220418  | 0.482477 |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.0021122   | 0.0061037  | 0.729332    | 19816 | 0.000256779 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00826857  | 0.00608586 | 0.17438     | 19816 | 0.000256779 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00389064  | 0.00548376 | 0.478091    | 19816 | 0.000256779 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00791843  | 0.00548072 | 0.148646    | 19816 | 0.000256779 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00262006  | 0.00659217 | 0.691069    | 19816 | 0.000256779 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.000919072 | 0.00610754 | 0.880397    | 19816 | 0.000256779 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00197838  | 0.00615473 | 0.747904    | 19816 | 0.000256779 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00500954  | 0.00485433 | 0.302185    | 19816 | 0.0233881   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00249053  | 0.00451561 | 0.581315    | 19816 | 0.0233881   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00207735  | 0.00404312 | 0.607439    | 19816 | 0.0233881   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00322739  | 0.00454531 | 0.477741    | 19816 | 0.0233881   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00123775  | 0.00522596 | 0.812796    | 19816 | 0.0233881   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.000751219 | 0.00480171 | 0.875693    | 19816 | 0.0233881   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.000891637 | 0.00490471 | 0.855761    | 19816 | 0.0233881   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             | -0.0158415   | 0.0207336  | 0.444911    | 19816 | 0.0233881   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             | -0.0187267   | 0.0214547  | 0.382831    | 19816 | 0.0233881   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.000994153 | 0.0190881  | 0.958467    | 19816 | 0.0233881   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0271579   | 0.0175823  | 0.122568    | 19816 | 0.0233881   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.00827649  | 0.0226265  | 0.714555    | 19816 | 0.0233881   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              | -0.0100249   | 0.0204375  | 0.623813    | 19816 | 0.0233881   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.0117773   | 0.0206743  | 0.568962    | 19816 | 0.0233881   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.014073    | 0.00755048 | 0.0624596   | 19816 | 0.0233881   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.0264933   | 0.00802224 | 0.000971958 | 19816 | 0.0233881   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0374525   | 0.00693534 | 7.28879e-08 | 19816 | 0.0233881   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0291855   | 0.00687545 | 2.26762e-05 | 19816 | 0.0233881   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.00976142  | 0.00805871 | 0.225901    | 19816 | 0.0233881   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0394363   | 0.00807713 | 1.11442e-06 | 19816 | 0.0233881   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.030025    | 0.00783244 | 0.000129523 | 19816 | 0.0233881   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.000245792 | 0.0069281  | 0.971702    | 19816 | 0.029753    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00820815  | 0.00697081 | 0.239108    | 19816 | 0.029753    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00169919  | 0.00624567 | 0.785599    | 19816 | 0.029753    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.0123726   | 0.00593314 | 0.0371404   | 19816 | 0.029753    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00509113  | 0.00746442 | 0.49527     | 19816 | 0.029753    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.00599434  | 0.00663565 | 0.366426    | 19816 | 0.029753    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00648696  | 0.00677271 | 0.338252    | 19816 | 0.029753    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            | -0.0168816   | 0.0308248  | 0.583974    | 19816 | 0.029753    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            | -0.0393313   | 0.0309903  | 0.204508    | 19816 | 0.029753    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.0151119   | 0.0272821  | 0.579689    | 19816 | 0.029753    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.0419205   | 0.0259399  | 0.106209    | 19816 | 0.029753    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.0308852   | 0.0336851  | 0.359295    | 19816 | 0.029753    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             | -0.0280759   | 0.0294846  | 0.341077    | 19816 | 0.029753    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             | -0.0323745   | 0.0299334  | 0.279558    | 19816 | 0.029753    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.030808    | 0.0110709  | 0.0054302   | 19816 | 0.029753    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.0343019   | 0.0117196  | 0.00345489  | 19816 | 0.029753    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0545907   | 0.0102239  | 1.01661e-07 | 19816 | 0.029753    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0497411   | 0.0100961  | 8.9128e-07  | 19816 | 0.029753    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0211654   | 0.012384   | 0.0875594   | 19816 | 0.029753    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.073271    | 0.0120093  | 1.21831e-09 | 19816 | 0.029753    |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.058825    | 0.0118853  | 7.94447e-07 | 19816 | 0.029753    |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |     n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|------:|
| event_att      | pretrend_att_joint_zero            |                3 |     4.09803 | 0.251071 | 19816 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |     2.82399 | 0.419566 | 19816 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |     1.47295 | 0.688526 | 19816 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |     2.25788 | 0.520639 | 19816 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |     1.84781 | 0.604586 | 19816 |