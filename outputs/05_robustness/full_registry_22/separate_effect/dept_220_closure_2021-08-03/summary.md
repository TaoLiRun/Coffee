# Displacement Effect Estimation Summary

- Sample rows: 14,672
- Unique members: 1,834
- Unique closures: 1
- Event FE units: 1,834
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_220_closure_2021-08-03`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |     n |   r2_within |        coef |         se |      pvalue |
|:-----------------|:----------------------|------:|------------:|------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 14672 |   0.0142945 | -0.0097525  | 0.00287914 | 0.000720787 |
| binary_collapsed | post_X_disp           | 14672 |   0.0142945 | -0.0430469  | 0.00842454 | 3.56269e-07 |
| binary_collapsed | post_X_treated_X_disp | 14672 |   0.0142945 | -0.00690021 | 0.0181334  | 0.7036      |

## Score Spec
| spec            | term                   |     n |   r2_within |       coef |         se |     pvalue |
|:----------------|:-----------------------|------:|------------:|-----------:|-----------:|-----------:|
| score_collapsed | post_X_treated         | 14672 |   0.0227978 | -0.0127577 | 0.00609765 | 0.0365543  |
| score_collapsed | post_X_score           | 14672 |   0.0227978 | -0.0740932 | 0.0109785  | 1.9913e-11 |
| score_collapsed | post_X_treated_X_score | 14672 |   0.0227978 | -0.0144034 | 0.0268749  | 0.592064   |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00810317  | 0.00557863 | 0.146524    | 14672 |   0.0020038 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.0137961   | 0.00593253 | 0.0201538   | 14672 |   0.0020038 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0118009   | 0.00497904 | 0.0178854   | 14672 |   0.0020038 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00342553  | 0.00400826 | 0.392874    | 14672 |   0.0020038 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00737397  | 0.00484833 | 0.12845     | 14672 |   0.0020038 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00648836  | 0.00519531 | 0.211865    | 14672 |   0.0020038 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00176195  | 0.00479407 | 0.713269    | 14672 |   0.0020038 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00347882  | 0.00469838 | 0.459134    | 14672 |   0.0376959 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.00827804  | 0.00505667 | 0.101791    | 14672 |   0.0376959 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0104152   | 0.00424178 | 0.0141657   | 14672 |   0.0376959 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.0037968   | 0.00308504 | 0.218589    | 14672 |   0.0376959 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0062278   | 0.00372327 | 0.0945631   | 14672 |   0.0376959 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.000807114 | 0.00416688 | 0.846434    | 14672 |   0.0376959 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00600622  | 0.00391663 | 0.125321    | 14672 |   0.0376959 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0447248   | 0.024313   | 0.0659971   | 14672 |   0.0376959 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0564526   | 0.0246634  | 0.022197    | 14672 |   0.0376959 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0305811   | 0.0196406  | 0.119635    | 14672 |   0.0376959 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.002646    | 0.0200576  | 0.895062    | 14672 |   0.0376959 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.00192719  | 0.0241382  | 0.936374    | 14672 |   0.0376959 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.0521065   | 0.0252955  | 0.0395482   | 14672 |   0.0376959 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.0474779   | 0.022896   | 0.0382525   | 14672 |   0.0376959 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.0432175   | 0.0135464  | 0.00144518  | 14672 |   0.0376959 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.062815    | 0.0124601  | 5.08031e-07 | 14672 |   0.0376959 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.075588    | 0.0113078  | 3.06344e-11 | 14672 |   0.0376959 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  2.50348e-05 | 0.0113072  | 0.998234    | 14672 |   0.0376959 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.036734    | 0.0127841  | 0.00410749  | 14672 |   0.0376959 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.000900814 | 0.0119905  | 0.940122    | 14672 |   0.0376959 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.028227    | 0.0124732  | 0.0237517   | 14672 |   0.0376959 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.0203249   | 0.00815876 | 0.01282     | 14672 |   0.0501725 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.0268108   | 0.00860141 | 0.00185522  | 14672 |   0.0501725 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0218972   | 0.0068902  | 0.00150754  | 14672 |   0.0501725 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00277035  | 0.00674598 | 0.681365    | 14672 |   0.0501725 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00477296  | 0.00807332 | 0.554458    | 14672 |   0.0501725 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.01622     | 0.00846981 | 0.0556427   | 14672 |   0.0501725 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00932521  | 0.00777971 | 0.230816    | 14672 |   0.0501725 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.0882061   | 0.0324435  | 0.0066145   | 14672 |   0.0501725 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.0897759   | 0.0340885  | 0.00851928  | 14672 |   0.0501725 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.0634102   | 0.0269144  | 0.0185778   | 14672 |   0.0501725 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.00791504  | 0.0295962  | 0.789165    | 14672 |   0.0501725 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.0126816   | 0.0357466  | 0.722807    | 14672 |   0.0501725 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.0873543   | 0.0368475  | 0.0178574   | 14672 |   0.0501725 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.0758277   | 0.0337357  | 0.0247138   | 14672 |   0.0501725 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered |  0.0758496   | 0.0185452  | 4.50057e-05 | 14672 |   0.0501725 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.098091    | 0.0167527  | 5.63208e-09 | 14672 |   0.0501725 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.102097    | 0.0156074  | 7.87339e-11 | 14672 |   0.0501725 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.00922329  | 0.0151933  | 0.543884    | 14672 |   0.0501725 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  |  0.0415415   | 0.0174452  | 0.0173551   | 14672 |   0.0501725 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.0110001   | 0.0164608  | 0.504054    | 14672 |   0.0501725 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.0416533   | 0.0168777  | 0.01368     | 14672 |   0.0501725 |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |     pvalue |     n |
|:---------------|:-----------------------------------|-----------------:|------------:|-----------:|------:|
| event_att      | pretrend_att_joint_zero            |                3 |     7.16173 | 0.0669177  | 14672 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |     6.34314 | 0.0960584  | 14672 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |     5.74855 | 0.124506   | 14672 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |    13.7008  | 0.00334208 | 14672 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |     9.99351 | 0.0186214  | 14672 |