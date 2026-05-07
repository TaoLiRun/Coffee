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


## Binary Specs
| spec                   | term                  |      n |   r2_within |       coef |         se |    pvalue |
|:-----------------------|:----------------------|-------:|------------:|-----------:|-----------:|----------:|
| binary_collapsed       | post_X_treated        | 321184 |   0.0106505 |  0.0110281 | 0.00443339 | 0.012868  |
| binary_collapsed       | post_X_disp           | 321184 |   0.0106505 | -0.168781  | 0.00422108 | 0         |
| binary_collapsed       | post_X_treated_X_disp | 321184 |   0.0106505 |  0.003676  | 0.00964036 | 0.702972  |
| binary_collapsed_logit | post_X_treated        | 321184 | nan         |  0.0551024 | 0.0262677  | 0.0359293 |
| binary_collapsed_logit | post_X_disp           | 321184 | nan         |  1.66773   | 0.0190623  | 0         |
| binary_collapsed_logit | post_X_treated_X_disp | 321184 | nan         |  0.0110643 | 0.0443696  | 0.803077  |

## Score Spec
| spec            | term                   |      n |   r2_within |        coef |         se |     pvalue |
|:----------------|:-----------------------|-------:|------------:|------------:|-----------:|-----------:|
| score_collapsed | post_X_treated         | 321184 |    0.016146 |  0.0109336  | 0.00392039 | 0.00529102 |
| score_collapsed | post_X_score           | 321184 |    0.016146 | -0.292552   | 0.00552387 | 0          |
| score_collapsed | post_X_treated_X_score | 321184 |    0.016146 |  0.00973719 | 0.0122424  | 0.426405   |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |      n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|-------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.000177793 | 0.0072262  | 0.980371    | 321184 |  0.00011149 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00406475  | 0.00704576 | 0.564006    | 321184 |  0.00011149 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00300674  | 0.00667308 | 0.652297    | 321184 |  0.00011149 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0147617   | 0.00642251 | 0.0215421   | 321184 |  0.00011149 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0034823   | 0.00663589 | 0.599747    | 321184 |  0.00011149 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0280216   | 0.00673834 | 3.2096e-05  | 321184 |  0.00011149 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00990424  | 0.00693817 | 0.153444    | 321184 |  0.00011149 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00292551  | 0.008138   | 0.719233    | 321184 |  0.0151918  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00214215  | 0.00785393 | 0.785048    | 321184 |  0.0151918  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0153236   | 0.00731307 | 0.0361441   | 321184 |  0.0151918  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0168449   | 0.00710294 | 0.0177192   | 321184 |  0.0151918  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0111083   | 0.00732841 | 0.129581    | 321184 |  0.0151918  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0259752   | 0.00749123 | 0.000526044 | 321184 |  0.0151918  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00743283  | 0.00762468 | 0.329647    | 321184 |  0.0151918  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             | -0.0145061   | 0.0171686  | 0.39816     | 321184 |  0.0151918  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             | -0.013997    | 0.016831   | 0.405629    | 321184 |  0.0151918  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.042809    | 0.0159792  | 0.00738637  | 321184 |  0.0151918  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0151632   | 0.0155011  | 0.327979    | 321184 |  0.0151918  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.0353912   | 0.0160012  | 0.026987    | 321184 |  0.0151918  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              | -0.00138925  | 0.0161403  | 0.931409    | 321184 |  0.0151918  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.0031314   | 0.0168117  | 0.852239    | 321184 |  0.0151918  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.0122151   | 0.00759997 | 0.108006    | 321184 |  0.0151918  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.0485045   | 0.00730952 | 3.26863e-11 | 321184 |  0.0151918  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.180528    | 0.00694747 | 0           | 321184 |  0.0151918  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0874498   | 0.00695458 | 0           | 321184 |  0.0151918  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.108162    | 0.0071648  | 0           | 321184 |  0.0151918  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.125292    | 0.00726865 | 0           | 321184 |  0.0151918  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.137909    | 0.00739489 | 0           | 321184 |  0.0151918  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00302713  | 0.00819178 | 0.711733    | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00238941  | 0.00791768 | 0.76282     | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0125968   | 0.00733496 | 0.0859194   | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0178179   | 0.00714985 | 0.0127044   | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0106858   | 0.00737174 | 0.14719     | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0258209   | 0.00754075 | 0.00061728  | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00684079  | 0.00768586 | 0.373445    | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0139385   | 0.0196562  | 0.478257    | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0291574   | 0.0193714  | 0.132286    | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -1.69568e-05 | 0.0183301  | 0.999262    | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0164024   | 0.0179036  | 0.359594    | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.00977853  | 0.0182367  | 0.591824    | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.0280873   | 0.018519   | 0.129356    | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.0275013   | 0.0192692  | 0.153526    | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.00424947  | 0.00775568 | 0.583752    | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.0573518   | 0.00749027 | 1.95399e-14 | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.193645    | 0.00709837 | 0           | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0856087   | 0.00718554 | 0           | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.101382    | 0.00738859 | 0           | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.117752    | 0.00746528 | 0           | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.132439    | 0.007529   | 0           | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_len              |  0.00615946  | 0.00763843 | 0.42003     | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_len              |  0.0102664   | 0.00728802 | 0.158942    | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_len              | -0.0191007   | 0.00652751 | 0.00343344  | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_len               |  0.0193908   | 0.00652901 | 0.00298022  | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_len               | -0.0116736   | 0.00668907 | 0.0809613   | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated_X_len               | -0.00358753  | 0.00680393 | 0.598007    | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated_X_len               | -0.00673165  | 0.00723841 | 0.352381    | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:disp_X_len                 | -0.0384908   | 0.00688284 | 2.25549e-08 | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:disp_X_len                 | -0.0410227   | 0.00644023 | 1.91382e-10 | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_X_len                 | -0.0518197   | 0.00595381 | 0           | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_X_len                  | -0.00348391  | 0.00609425 | 0.567548    | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_X_len                  | -0.0235303   | 0.00632175 | 0.000197827 | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:disp_X_len                  | -0.0273846   | 0.00648551 | 2.42219e-05 | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:disp_X_len                  | -0.022416    | 0.00690929 | 0.00117825  | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:tXdXlen                    | -0.0230121   | 0.015234   | 0.130904    | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:tXdXlen                    | -0.0464595   | 0.0149435  | 0.00187844  | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:tXdXlen                    | -0.00934159  | 0.0138566  | 0.500212    | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:tXdXlen                     | -0.0161205   | 0.0136924  | 0.239072    | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:tXdXlen                     | -0.0074494   | 0.0141916  | 0.599644    | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:tXdXlen                     | -0.0193786   | 0.0142917  | 0.175127    | 321184 |  0.0162182  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:tXdXlen                     | -0.02118     | 0.0149948  | 0.157814    | 321184 |  0.0162182  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00110688  | 0.00722392 | 0.878222    | 321184 |  0.0203791  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00589225  | 0.00702275 | 0.401461    | 321184 |  0.0203791  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00434379  | 0.0065892  | 0.509752    | 321184 |  0.0203791  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0120129   | 0.0063629  | 0.0590381   | 321184 |  0.0203791  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.000744063 | 0.00656772 | 0.9098      | 321184 |  0.0203791  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0246139   | 0.00667765 | 0.000228093 | 321184 |  0.0203791  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0052434   | 0.00687479 | 0.445647    | 321184 |  0.0203791  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.000884528 | 0.020023   | 0.964765    | 321184 |  0.0203791  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            | -0.0231798   | 0.0189061  | 0.220188    | 321184 |  0.0203791  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.0355538   | 0.0179936  | 0.0481713   | 321184 |  0.0203791  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.00689051  | 0.0187825  | 0.713728    | 321184 |  0.0203791  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.0336226   | 0.0196226  | 0.0866348   | 321184 |  0.0203791  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.0157705   | 0.0197009  | 0.423428    | 321184 |  0.0203791  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.00799824  | 0.0205008  | 0.696433    | 321184 |  0.0203791  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.00820322  | 0.00909199 | 0.366931    | 321184 |  0.0203791  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.0885007   | 0.00843584 | 0           | 321184 |  0.0203791  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.244076    | 0.00795384 | 0           | 321184 |  0.0203791  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.171252    | 0.00861335 | 0           | 321184 |  0.0203791  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.199693    | 0.00891711 | 0           | 321184 |  0.0203791  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.232563    | 0.00909154 | 0           | 321184 |  0.0203791  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.243652    | 0.00929018 | 0           | 321184 |  0.0203791  |

## Pre-trend Joint Tests
| spec           | test                                    |   n_restrictions |   statistic |      pvalue |      n |
|:---------------|:----------------------------------------|-----------------:|------------:|------------:|-------:|
| event_att      | pretrend_att_joint_zero                 |                3 |     1.07216 | 0.783798    | 321184 |
| event_binary_B | pretrend_baseline_joint_zero            |                3 |     6.22977 | 0.100951    | 321184 |
| event_binary_B | pretrend_displacement_joint_zero        |                3 |     8.13288 | 0.0433439   | 321184 |
| event_binary_D | pretrend_length_displacement_joint_zero |                3 |    11.3359  | 0.0100414   | 321184 |
| event_binary_D | pretrend_length_baseline_joint_zero     |                3 |    19.5719  | 0.000208197 | 321184 |
| event_score_C  | pretrend_score_baseline_joint_zero      |                3 |     2.2289  | 0.526278    | 321184 |
| event_score_C  | pretrend_score_slope_joint_zero         |                3 |     6.29938 | 0.0979191   | 321184 |