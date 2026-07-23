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
| spec                           | estimand                               | term                  |      n |   r2_within |       coef |         se |    pvalue |       ci_low |     ci_high |
|:-------------------------------|:---------------------------------------|:----------------------|-------:|------------:|-----------:|-----------:|----------:|-------------:|------------:|
| binary_collapsed               | low_predicted_incidence_effect_delta_b | post_X_treated        | 321184 |   0.0106505 |  0.0110281 | 0.00443339 | 0.012868  |   0.00233857 |   0.0197177 |
| binary_collapsed               | common_high_minus_low_post_shift       | post_X_disp           | 321184 |   0.0106505 | -0.168781  | 0.00422108 | 0         |  -0.177055   |  -0.160508  |
| binary_collapsed               | high_minus_low_ddd                     | post_X_treated_X_disp | 321184 |   0.0106505 |  0.003676  | 0.00964036 | 0.702972  |  -0.0152193  |   0.0225713 |
| binary_collapsed_group_effects | low_predicted_incidence_effect         | post_X_treated_X_low  | 321184 |   0.0106505 |  0.0110281 | 0.00443339 | 0.012868  |   0.00233857 |   0.0197177 |
| binary_collapsed_group_effects | high_predicted_incidence_effect        | post_X_treated_X_high | 321184 |   0.0106505 |  0.0147041 | 0.00856669 | 0.0860912 |  -0.00208679 |   0.031495  |
| binary_collapsed_logit         | nan                                    | post_X_treated        | 321184 | nan         |  0.0551024 | 0.0262677  | 0.0359293 | nan          | nan         |
| binary_collapsed_logit         | nan                                    | post_X_disp           | 321184 | nan         |  1.66773   | 0.0190623  | 0         | nan          | nan         |
| binary_collapsed_logit         | nan                                    | post_X_treated_X_disp | 321184 | nan         |  0.0110643 | 0.0443696  | 0.803077  | nan          | nan         |

## Score Spec
| spec            |   estimand | term                   |      n |   r2_within |        coef |         se |     pvalue |      ci_low |    ci_high |
|:----------------|-----------:|:-----------------------|-------:|------------:|------------:|-----------:|-----------:|------------:|-----------:|
| score_collapsed |        nan | post_X_treated         | 321184 |    0.016146 |  0.0109336  | 0.00392039 | 0.00529102 |  0.00324957 |  0.0186177 |
| score_collapsed |        nan | post_X_score           | 321184 |    0.016146 | -0.292552   | 0.00552387 | 0          | -0.303379   | -0.281725  |
| score_collapsed |        nan | post_X_treated_X_score | 321184 |    0.016146 |  0.00973719 | 0.0122424  | 0.426405   | -0.0142582  |  0.0337325 |

## Event-study Specs
| spec           | estimand   | term                                                              |         coef |         se |      pvalue |       ci_low |      ci_high |      n |   r2_within |
|:---------------|:-----------|:------------------------------------------------------------------|-------------:|-----------:|------------:|-------------:|-------------:|-------:|------------:|
| event_att      |            | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.000177793 | 0.0072262  | 0.980371    | -0.0139857   |  0.0143413   | 321184 |  0.00011149 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00406475  | 0.00704576 | 0.564006    | -0.0178746   |  0.00974511  | 321184 |  0.00011149 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00300674  | 0.00667308 | 0.652297    | -0.0100726   |  0.0160861   | 321184 |  0.00011149 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0147617   | 0.00642251 | 0.0215421   |  0.00217346  |  0.02735     | 321184 |  0.00011149 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0034823   | 0.00663589 | 0.599747    | -0.0095242   |  0.0164888   | 321184 |  0.00011149 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0280216   | 0.00673834 | 3.2096e-05  |  0.0148143   |  0.0412289   | 321184 |  0.00011149 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00990424  | 0.00693817 | 0.153444    | -0.00369473  |  0.0235032   | 321184 |  0.00011149 |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00292551  | 0.008138   | 0.719233    | -0.0130252   |  0.0188762   | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00214215  | 0.00785393 | 0.785048    | -0.017536    |  0.0132517   | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0153236   | 0.00731307 | 0.0361441   |  0.000989827 |  0.0296574   | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0168449   | 0.00710294 | 0.0177192   |  0.00292292  |  0.0307668   | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0111083   | 0.00732841 | 0.129581    | -0.00325553  |  0.0254722   | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0259752   | 0.00749123 | 0.000526044 |  0.0112922   |  0.0406582   | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00743283  | 0.00762468 | 0.329647    | -0.00751173  |  0.0223774   | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             | -0.0145061   | 0.0171686  | 0.39816     | -0.0481569   |  0.0191447   | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             | -0.013997    | 0.016831   | 0.405629    | -0.0469862   |  0.0189922   | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.042809    | 0.0159792  | 0.00738637  | -0.0741287   | -0.0114893   | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0151632   | 0.0155011  | 0.327979    | -0.0455457   |  0.0152193   | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.0353912   | 0.0160012  | 0.026987    | -0.0667539   | -0.00402852  | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              | -0.00138925  | 0.0161403  | 0.931409    | -0.0330246   |  0.0302461   | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.0031314   | 0.0168117  | 0.852239    | -0.0360828   |  0.02982     | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.0122151   | 0.00759997 | 0.108006    | -0.0271112   |  0.00268102  | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.0485045   | 0.00730952 | 3.26863e-11 |  0.0341776   |  0.0628313   | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.180528    | 0.00694747 | 0           |  0.166911    |  0.194145    | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0874498   | 0.00695458 | 0           | -0.101081    | -0.0738187   | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.108162    | 0.0071648  | 0           | -0.122205    | -0.0941185   | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.125292    | 0.00726865 | 0           | -0.139539    | -0.111045    | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.137909    | 0.00739489 | 0           | -0.152403    | -0.123415    | 321184 |  0.0151918  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00302713  | 0.00819178 | 0.711733    | -0.0130289   |  0.0190832   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00238941  | 0.00791768 | 0.76282     | -0.0179083   |  0.0131294   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0125968   | 0.00733496 | 0.0859194   | -0.00177985  |  0.0269735   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0178179   | 0.00714985 | 0.0127044   |  0.00380401  |  0.0318318   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0106858   | 0.00737174 | 0.14719     | -0.00376302  |  0.0251345   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0258209   | 0.00754075 | 0.00061728  |  0.0110408   |  0.0406009   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00684079  | 0.00768586 | 0.373445    | -0.00822368  |  0.0219053   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0139385   | 0.0196562  | 0.478257    | -0.0245881   |  0.0524652   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0291574   | 0.0193714  | 0.132286    | -0.00881097  |  0.0671258   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -1.69568e-05 | 0.0183301  | 0.999262    | -0.0359443   |  0.0359104   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0164024   | 0.0179036  | 0.359594    | -0.0514938   |  0.0186891   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.00977853  | 0.0182367  | 0.591824    | -0.045523    |  0.0259659   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.0280873   | 0.018519   | 0.129356    | -0.0082103   |  0.064385    | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.0275013   | 0.0192692  | 0.153526    | -0.0102668   |  0.0652695   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.00424947  | 0.00775568 | 0.583752    | -0.0194508   |  0.0109518   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.0573518   | 0.00749027 | 1.95399e-14 |  0.0426707   |  0.0720329   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.193645    | 0.00709837 | 0           |  0.179732    |  0.207558    | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0856087   | 0.00718554 | 0           | -0.0996926   | -0.0715249   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.101382    | 0.00738859 | 0           | -0.115863    | -0.0868998   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.117752    | 0.00746528 | 0           | -0.132384    | -0.10312     | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.132439    | 0.007529   | 0           | -0.147196    | -0.117682    | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_len              |  0.00615946  | 0.00763843 | 0.42003     | -0.00881205  |  0.021131    | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_len              |  0.0102664   | 0.00728802 | 0.158942    | -0.00401831  |  0.0245511   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_len              | -0.0191007   | 0.00652751 | 0.00343344  | -0.0318947   | -0.0063066   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:treated_X_len               |  0.0193908   | 0.00652901 | 0.00298022  |  0.00659384  |  0.0321879   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:treated_X_len               | -0.0116736   | 0.00668907 | 0.0809613   | -0.0247844   |  0.00143711  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:treated_X_len               | -0.00358753  | 0.00680393 | 0.598007    | -0.0169234   |  0.00974833  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:treated_X_len               | -0.00673165  | 0.00723841 | 0.352381    | -0.0209191   |  0.00745579  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:disp_X_len                 | -0.0384908   | 0.00688284 | 2.25549e-08 | -0.0519814   | -0.0250003   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:disp_X_len                 | -0.0410227   | 0.00644023 | 1.91382e-10 | -0.0536457   | -0.0283997   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:disp_X_len                 | -0.0518197   | 0.00595381 | 0           | -0.0634893   | -0.04015     | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:disp_X_len                  | -0.00348391  | 0.00609425 | 0.567548    | -0.0154288   |  0.00846096  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:disp_X_len                  | -0.0235303   | 0.00632175 | 0.000197827 | -0.0359211   | -0.0111395   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:disp_X_len                  | -0.0273846   | 0.00648551 | 2.42219e-05 | -0.0400963   | -0.0146728   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:disp_X_len                  | -0.022416    | 0.00690929 | 0.00117825  | -0.0359584   | -0.00887362  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:tXdXlen                    | -0.0230121   | 0.015234   | 0.130904    | -0.0528711   |  0.00684685  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:tXdXlen                    | -0.0464595   | 0.0149435  | 0.00187844  | -0.075749    | -0.0171699   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:tXdXlen                    | -0.00934159  | 0.0138566  | 0.500212    | -0.0365008   |  0.0178176   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:tXdXlen                     | -0.0161205   | 0.0136924  | 0.239072    | -0.042958    |  0.010717    | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:tXdXlen                     | -0.0074494   | 0.0141916  | 0.599644    | -0.0352652   |  0.0203664   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:tXdXlen                     | -0.0193786   | 0.0142917  | 0.175127    | -0.0473905   |  0.0086334   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:tXdXlen                     | -0.02118     | 0.0149948  | 0.157814    | -0.0505702   |  0.0082102   | 321184 |  0.0162182  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00110688  | 0.00722392 | 0.878222    | -0.0152659   |  0.0130522   | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00589225  | 0.00702275 | 0.401461    | -0.019657    |  0.00787249  | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00434379  | 0.0065892  | 0.509752    | -0.00857119  |  0.0172588   | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0120129   | 0.0063629  | 0.0590381   | -0.000458512 |  0.0244844   | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.000744063 | 0.00656772 | 0.9098      | -0.0121288   |  0.0136169   | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0246139   | 0.00667765 | 0.000228093 |  0.0115256   |  0.0377023   | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0052434   | 0.00687479 | 0.445647    | -0.00823135  |  0.0187182   | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.000884528 | 0.020023   | 0.964765    | -0.0383609   |  0.04013     | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            | -0.0231798   | 0.0189061  | 0.220188    | -0.0602363   |  0.0138767   | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.0355538   | 0.0179936  | 0.0481713   | -0.0708216   | -0.000285937 | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.00689051  | 0.0187825  | 0.713728    | -0.0437047   |  0.0299237   | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.0336226   | 0.0196226  | 0.0866348   | -0.0720832   |  0.00483811  | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.0157705   | 0.0197009  | 0.423428    | -0.0228438   |  0.0543848   | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.00799824  | 0.0205008  | 0.696433    | -0.0321838   |  0.0481803   | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.00820322  | 0.00909199 | 0.366931    | -0.0260237   |  0.00961728  | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.0885007   | 0.00843584 | 0           |  0.0719662   |  0.105035    | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.244076    | 0.00795384 | 0           |  0.228487    |  0.259666    | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.171252    | 0.00861335 | 0           | -0.188135    | -0.15437     | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.199693    | 0.00891711 | 0           | -0.217171    | -0.182215    | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.232563    | 0.00909154 | 0           | -0.250382    | -0.214743    | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.243652    | 0.00929018 | 0           | -0.261861    | -0.225443    | 321184 |  0.0203791  |

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

## Matched-Sample Support
| treated   | match_cell                                                        |   blocked_available |   non_blocked_available |   retained_per_group |   common_support |   episodes_before |   episodes_after |   blocked_retained |   non_blocked_retained |   treated_retained |   control_retained |
|:----------|:------------------------------------------------------------------|--------------------:|------------------------:|---------------------:|-----------------:|------------------:|-----------------:|-------------------:|-----------------------:|-------------------:|-------------------:|
| 0         | 0|(20074.5, 30111.25]|(30111.25, 40148.0]|(0.999, 10037.75]|all   |                 591 |                    1349 |                  591 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(0.999, 10037.75]|(10037.75, 20074.5]|all   |                  87 |                     422 |                   87 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(30111.25, 40148.0]|(30111.25, 40148.0]|(0.999, 10037.75]|all   |                3978 |                    1024 |                 1024 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(0.999, 10037.75]|(20074.5, 30111.25]|all   |                 119 |                    1134 |                  119 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(30111.25, 40148.0]|(10037.75, 20074.5]|all |                 115 |                     271 |                  115 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(0.999, 10037.75]|(20074.5, 30111.25]|all   |                 155 |                     582 |                  155 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(0.999, 10037.75]|(10037.75, 20074.5]|all   |                 551 |                     504 |                  504 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(0.999, 10037.75]|(0.999, 10037.75]|(20074.5, 30111.25]|all     |                   1 |                     759 |                    1 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(0.999, 10037.75]|(0.999, 10037.75]|(30111.25, 40148.0]|all     |                   4 |                    3095 |                    4 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(30111.25, 40148.0]|(0.999, 10037.75]|all   |                  29 |                     353 |                   29 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(30111.25, 40148.0]|(0.999, 10037.75]|(10037.75, 20074.5]|all   |                 447 |                     235 |                  235 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(30111.25, 40148.0]|(30111.25, 40148.0]|(10037.75, 20074.5]|all |                 337 |                     124 |                  124 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(30111.25, 40148.0]|(10037.75, 20074.5]|all |                   7 |                      92 |                    7 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(30111.25, 40148.0]|(0.999, 10037.75]|(20074.5, 30111.25]|all   |                  43 |                     140 |                   43 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(30111.25, 40148.0]|(20074.5, 30111.25]|(0.999, 10037.75]|all   |                 166 |                      56 |                   56 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(20074.5, 30111.25]|(0.999, 10037.75]|all   |                 167 |                     214 |                  167 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(20074.5, 30111.25]|(10037.75, 20074.5]|all |                 451 |                     725 |                  451 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(20074.5, 30111.25]|(0.999, 10037.75]|all   |                  34 |                     191 |                   34 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(30111.25, 40148.0]|(20074.5, 30111.25]|(10037.75, 20074.5]|all |                 369 |                     227 |                  227 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(20074.5, 30111.25]|(10037.75, 20074.5]|all |                 115 |                     469 |                  115 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(0.999, 10037.75]|(30111.25, 40148.0]|all   |                   0 |                       2 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(0.999, 10037.75]|(30111.25, 40148.0]|all   |                   0 |                      27 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(0.999, 10037.75]|(10037.75, 20074.5]|(20074.5, 30111.25]|all   |                   0 |                    1655 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(0.999, 10037.75]|(10037.75, 20074.5]|(30111.25, 40148.0]|all   |                   0 |                    2664 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(10037.75, 20074.5]|(10037.75, 20074.5]|all |                 249 |                    1120 |                  249 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(30111.25, 40148.0]|(10037.75, 20074.5]|(20074.5, 30111.25]|all |                   3 |                      57 |                    3 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(10037.75, 20074.5]|(10037.75, 20074.5]|all |                  25 |                     323 |                   25 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(10037.75, 20074.5]|(20074.5, 30111.25]|all |                   6 |                     459 |                    6 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(30111.25, 40148.0]|(10037.75, 20074.5]|(10037.75, 20074.5]|all |                 446 |                     450 |                  446 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(10037.75, 20074.5]|(20074.5, 30111.25]|all |                  17 |                     418 |                   17 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(30111.25, 40148.0]|(10037.75, 20074.5]|(0.999, 10037.75]|all   |                  37 |                      11 |                   11 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(10037.75, 20074.5]|(0.999, 10037.75]|all   |                  12 |                      23 |                   12 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(10037.75, 20074.5]|(30111.25, 40148.0]|all |                   0 |                      74 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(20074.5, 30111.25]|(20074.5, 30111.25]|all |                  98 |                    1743 |                   98 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(20074.5, 30111.25]|(30111.25, 40148.0]|all |                  13 |                    2339 |                   13 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(20074.5, 30111.25]|(20074.5, 30111.25]|all |                 114 |                     507 |                  114 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(30111.25, 40148.0]|(20074.5, 30111.25]|(20074.5, 30111.25]|all |                  38 |                      95 |                   38 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(20074.5, 30111.25]|(30111.25, 40148.0]|all |                   0 |                       1 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(0.999, 10037.75]|(20074.5, 30111.25]|all   |                  41 |                     121 |                   41 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(0.999, 10037.75]|(0.999, 10037.75]|(30111.25, 40148.0]|all     |                   3 |                     728 |                    3 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(30111.25, 40148.0]|(0.999, 10037.75]|(10037.75, 20074.5]|all   |                  81 |                      30 |                   30 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(30111.25, 40148.0]|(10037.75, 20074.5]|all |                  41 |                      56 |                   41 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(30111.25, 40148.0]|(0.999, 10037.75]|all   |                 142 |                     280 |                  142 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(0.999, 10037.75]|(20074.5, 30111.25]|all   |                  45 |                     251 |                   45 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(0.999, 10037.75]|(10037.75, 20074.5]|all   |                  93 |                      88 |                   88 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(30111.25, 40148.0]|(30111.25, 40148.0]|(0.999, 10037.75]|all   |                 806 |                     203 |                  203 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(30111.25, 40148.0]|(10037.75, 20074.5]|all |                   0 |                      12 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(0.999, 10037.75]|(10037.75, 20074.5]|all   |                  24 |                      75 |                   24 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(30111.25, 40148.0]|(30111.25, 40148.0]|(10037.75, 20074.5]|all |                 111 |                      25 |                   25 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(0.999, 10037.75]|(0.999, 10037.75]|(20074.5, 30111.25]|all     |                   0 |                     114 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(30111.25, 40148.0]|(0.999, 10037.75]|all   |                  14 |                      77 |                   14 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(30111.25, 40148.0]|(0.999, 10037.75]|(20074.5, 30111.25]|all   |                   7 |                      19 |                    7 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(20074.5, 30111.25]|(10037.75, 20074.5]|all |                  36 |                     101 |                   36 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(20074.5, 30111.25]|(10037.75, 20074.5]|all |                 134 |                     186 |                  134 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(30111.25, 40148.0]|(20074.5, 30111.25]|(10037.75, 20074.5]|all |                 112 |                      47 |                   47 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(20074.5, 30111.25]|(0.999, 10037.75]|all   |                  67 |                      58 |                   58 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(30111.25, 40148.0]|(20074.5, 30111.25]|(0.999, 10037.75]|all   |                  37 |                      16 |                   16 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(20074.5, 30111.25]|(0.999, 10037.75]|all   |                  20 |                      53 |                   20 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(0.999, 10037.75]|(30111.25, 40148.0]|all   |                   0 |                       9 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(0.999, 10037.75]|(30111.25, 40148.0]|all   |                   0 |                       1 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(10037.75, 20074.5]|(10037.75, 20074.5]|all |                   0 |                      85 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(0.999, 10037.75]|(10037.75, 20074.5]|(30111.25, 40148.0]|all   |                   0 |                     543 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(0.999, 10037.75]|(10037.75, 20074.5]|(20074.5, 30111.25]|all   |                   1 |                     470 |                    1 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(10037.75, 20074.5]|(20074.5, 30111.25]|all |                   3 |                     147 |                    3 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(10037.75, 20074.5]|(10037.75, 20074.5]|all |                  48 |                     286 |                   48 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(30111.25, 40148.0]|(10037.75, 20074.5]|(10037.75, 20074.5]|all |                  85 |                     120 |                   85 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(10037.75, 20074.5]|(20074.5, 30111.25]|all |                   0 |                     120 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(30111.25, 40148.0]|(10037.75, 20074.5]|(20074.5, 30111.25]|all |                   0 |                       9 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(30111.25, 40148.0]|(10037.75, 20074.5]|(0.999, 10037.75]|all   |                   9 |                       5 |                    5 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(10037.75, 20074.5]|(0.999, 10037.75]|all   |                   4 |                      11 |                    4 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(10037.75, 20074.5]|(30111.25, 40148.0]|all |                   0 |                      42 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(20074.5, 30111.25]|(20074.5, 30111.25]|all |                  36 |                     356 |                   36 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(30111.25, 40148.0]|(20074.5, 30111.25]|(20074.5, 30111.25]|all |                  10 |                      22 |                   10 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(20074.5, 30111.25]|(20074.5, 30111.25]|all |                  29 |                      93 |                   29 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(20074.5, 30111.25]|(30111.25, 40148.0]|all |                   2 |                     490 |                    2 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| all       | __overall__                                                       |               10865 |                   29283 |                 6317 |                1 |             40148 |            12634 |               6317 |                   6317 |               2394 |              10240 |

## Matched Binary Specs
| spec                           | estimand                               | term                  |      n |    r2_within |       coef |         se |       pvalue |       ci_low |     ci_high |
|:-------------------------------|:---------------------------------------|:----------------------|-------:|-------------:|-----------:|-----------:|-------------:|-------------:|------------:|
| binary_collapsed               | low_predicted_incidence_effect_delta_b | post_X_treated        | 101072 |   0.00020264 |  0.0353467 | 0.0110883  | 0.00143734   |   0.013612   |   0.0570814 |
| binary_collapsed               | common_high_minus_low_post_shift       | post_X_disp           | 101072 |   0.00020264 |  0.0174608 | 0.00710766 | 0.0140388    |   0.00352867 |   0.0313929 |
| binary_collapsed               | high_minus_low_ddd                     | post_X_treated_X_disp | 101072 |   0.00020264 | -0.0212828 | 0.0159866  | 0.183119     |  -0.0526191  |   0.0100534 |
| binary_collapsed_group_effects | low_predicted_incidence_effect         | post_X_treated_X_low  | 101072 |   0.00020264 |  0.0353467 | 0.0110883  | 0.00143734   |   0.013612   |   0.0570814 |
| binary_collapsed_group_effects | high_predicted_incidence_effect        | post_X_treated_X_high | 101072 |   0.00020264 |  0.0140639 | 0.0115963  | 0.225232     |  -0.00866657 |   0.0367943 |
| binary_collapsed_logit         | nan                                    | post_X_treated        | 101072 | nan          |  0.0847538 | 0.045893   | 0.0647803    | nan          | nan         |
| binary_collapsed_logit         | nan                                    | post_X_disp           | 101072 | nan          |  0.640746  | 0.0280356  | 1.31155e-115 | nan          | nan         |
| binary_collapsed_logit         | nan                                    | post_X_treated_X_disp | 101072 | nan          | -0.024483  | 0.0647329  | 0.70527      | nan          | nan         |

## Matched Event-study Specs
| spec           | estimand   | term                                                              |        coef |         se |      pvalue |      ci_low |     ci_high |      n |   r2_within |
|:---------------|:-----------|:------------------------------------------------------------------|------------:|-----------:|------------:|------------:|------------:|-------:|------------:|
| event_att      |            | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0520851  | 0.0161374  | 0.00125155  | -0.0837169  | -0.0204532  | 101072 | 0.000467142 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0647059  | 0.0164591  | 8.4937e-05  | -0.0969683  | -0.0324435  | 101072 | 0.000467142 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0401166  | 0.0161684  | 0.0131081   | -0.0718092  | -0.00842404 | 101072 | 0.000467142 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00885115 | 0.0136253  | 0.515956    | -0.0355588  |  0.0178565  | 101072 | 0.000467142 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0389057  | 0.013874   | 0.00505158  | -0.0661008  | -0.0117106  | 101072 | 0.000467142 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00399688 | 0.0143993  | 0.781344    | -0.024228   |  0.0322218  | 101072 | 0.000467142 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0154833  | 0.0148886  | 0.298386    | -0.0446673  |  0.0137006  | 101072 | 0.000467142 |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0568847  | 0.0232294  | 0.0143459   | -0.102418   | -0.0113515  | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0874354  | 0.0238807  | 0.000251914 | -0.134245   | -0.0406257  | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0252965  | 0.0234513  | 0.28075     | -0.0712645  |  0.0206716  | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00669738 | 0.0196406  | 0.733111    | -0.0451959  |  0.0318011  | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.021416   | 0.0197551  | 0.278354    | -0.060139   |  0.0173071  | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00782995 | 0.0208379  | 0.707105    | -0.0330154  |  0.0486753  | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00836616 | 0.0211044  | 0.691803    | -0.0497339  |  0.0330016  | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0103143  | 0.0319556  | 0.746876    | -0.0523237  |  0.0729522  | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0451879  | 0.0323708  | 0.162756    | -0.0182638  |  0.10864    | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.0215274  | 0.0314328  | 0.493438    | -0.0831405  |  0.0400857  | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.00183602 | 0.0268803  | 0.945545    | -0.0545255  |  0.0508534  | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.0327241  | 0.0275018  | 0.234112    | -0.0866318  |  0.0211836  | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              | -0.00504017 | 0.0284665  | 0.859467    | -0.0608388  |  0.0507585  | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.0113937  | 0.0294302  | 0.698655    | -0.0690813  |  0.0462938  | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.117392   | 0.0140729  | 0           |  0.0898072  |  0.144977   | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.149366   | 0.0140133  | 0           |  0.121898   |  0.176835   | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.287801   | 0.0137012  | 0           |  0.260944   |  0.314657   | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  0.166472   | 0.0123861  | 0           |  0.142194   |  0.190751   | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.154372   | 0.0126426  | 0           |  0.129591   |  0.179153   | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.148721   | 0.0127762  | 0           |  0.123677   |  0.173764   | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.153253   | 0.0130502  | 0           |  0.127673   |  0.178834   | 101072 | 0.00763886  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0603802  | 0.0232363  | 0.00937337  | -0.105927   | -0.0148335  | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0916286  | 0.023927   | 0.000129023 | -0.138529   | -0.044728   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0291662  | 0.023488   | 0.214352    | -0.0752062  |  0.0168738  | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00814415 | 0.0196575  | 0.678659    | -0.0466758  |  0.0303875  | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0221571  | 0.0197456  | 0.26183     | -0.0608615  |  0.0165473  | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0054616  | 0.0208791  | 0.793648    | -0.0354645  |  0.0463877  | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0116891  | 0.0211456  | 0.580416    | -0.0531378  |  0.0297595  | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0454716  | 0.0345789  | 0.188531    | -0.0223083  |  0.113252   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.102323   | 0.0347592  | 0.00324847  |  0.0341893  |  0.170456   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0186399  | 0.0339654  | 0.583158    | -0.0479374  |  0.0852172  | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.00452052 | 0.028739   | 0.875014    | -0.0518123  |  0.0608533  | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.00337906 | 0.0292433  | 0.908011    | -0.0607003  |  0.0539422  | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.0423306  | 0.0304873  | 0.165019    | -0.0174291  |  0.10209    | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.0243713  | 0.0321848  | 0.448926    | -0.0387158  |  0.0874585  | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.140355   | 0.0142554  | 0           |  0.112412   |  0.168297   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.173635   | 0.0142266  | 0           |  0.145748   |  0.201521   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.329928   | 0.0138249  | 0           |  0.302829   |  0.357027   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  0.186353   | 0.0126535  | 0           |  0.16155    |  0.211155   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.182431   | 0.0128873  | 0           |  0.15717    |  0.207692   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.173492   | 0.0130068  | 0           |  0.147997   |  0.198988   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.174081   | 0.0131478  | 0           |  0.14831    |  0.199853   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_len              | -0.00330472 | 0.0206859  | 0.873075    | -0.0438523  |  0.0372428  | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_len              |  0.00513227 | 0.0205068  | 0.802381    | -0.0350641  |  0.0453286  | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_len              | -0.0420274  | 0.0193296  | 0.0297046   | -0.0799162  | -0.0041385  | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:treated_X_len               |  0.0152667  | 0.016721   | 0.361244    | -0.0175089  |  0.0480423  | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:treated_X_len               | -0.0484858  | 0.0164831  | 0.00327174  | -0.0807952  | -0.0161764  | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:treated_X_len               | -0.0246342  | 0.0176464  | 0.162741    | -0.0592238  |  0.00995536 | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:treated_X_len               | -0.0425448  | 0.0190892  | 0.025849    | -0.0799626  | -0.00512705 | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:disp_X_len                 | -0.0796435  | 0.0108265  | 2.00728e-13 | -0.100865   | -0.058422   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:disp_X_len                 | -0.0863375  | 0.00979756 | 0           | -0.105542   | -0.0671328  | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:disp_X_len                 | -0.117775   | 0.00861622 | 0           | -0.134664   | -0.100886   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:disp_X_len                  | -0.055815   | 0.0086284  | 1.02456e-10 | -0.072728   | -0.038902   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:disp_X_len                  | -0.0829039  | 0.00903163 | 0           | -0.100607   | -0.0652005  | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:disp_X_len                  | -0.0793272  | 0.00952212 | 2.22045e-16 | -0.097992   | -0.0606624  | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:disp_X_len                  | -0.0764581  | 0.0113834  | 1.93956e-11 | -0.0987713  | -0.0541449  | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:tXdXlen                    | -0.00055937 | 0.0279025  | 0.984006    | -0.0552525  |  0.0541338  | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:tXdXlen                    | -0.0331275  | 0.0275272  | 0.228826    | -0.087085   |  0.02083    | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:tXdXlen                    |  0.0422238  | 0.0260688  | 0.105321    | -0.00887505 |  0.0933226  | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:tXdXlen                     |  0.00409086 | 0.0229131  | 0.858304    | -0.0408223  |  0.0490041  | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:tXdXlen                     |  0.0519128  | 0.023185   | 0.025169    |  0.00646661 |  0.097359   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:tXdXlen                     |  0.00395836 | 0.0242426  | 0.8703      | -0.0435607  |  0.0514774  | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:tXdXlen                     |  0.0340639  | 0.0261791  | 0.193217    | -0.017251   |  0.0853789  | 101072 | 0.0110073   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0606562  | 0.0198991  | 0.00230697  | -0.0996614  | -0.021651   | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.075744   | 0.020446   | 0.000212632 | -0.115821   | -0.0356668  | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0334489  | 0.0196523  | 0.0887729   | -0.0719703  |  0.00507253 | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00451166 | 0.0166898  | 0.786915    | -0.0372262  |  0.0282029  | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0294547  | 0.0167708  | 0.07906     | -0.062328   |  0.00341861 | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00583494 | 0.017572   | 0.73985     | -0.0286089  |  0.0402788  | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00952694 | 0.0179996  | 0.596617    | -0.0448089  |  0.0257551  | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.0411482  | 0.0550518  | 0.454809    | -0.0667617  |  0.149058   | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.0480189  | 0.0548379  | 0.381236    | -0.0594716  |  0.155509   | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.0184953  | 0.0528139  | 0.726196    | -0.122019   |  0.0850279  | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.0233366  | 0.0459584  | 0.611619    | -0.113422   |  0.0667489  | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.0506608  | 0.0469098  | 0.280179    | -0.142611   |  0.0412894  | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             | -0.0104911  | 0.0487795  | 0.829715    | -0.106106   |  0.0851242  | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             | -0.0333652  | 0.0505072  | 0.508879    | -0.132367   |  0.0656366  | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered |  0.146183   | 0.0250899  | 5.80272e-09 |  0.0970031  |  0.195363   | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.206193   | 0.0244937  | 0           |  0.158181   |  0.254204   | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.498303   | 0.0236877  | 0           |  0.451872   |  0.544735   | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  |  0.241598   | 0.021903   | 0           |  0.198664   |  0.284531   | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  |  0.212908   | 0.0225065  | 0           |  0.168792   |  0.257025   | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  |  0.193246   | 0.0226273  | 0           |  0.148893   |  0.237599   | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  |  0.205475   | 0.0233059  | 0           |  0.159792   |  0.251158   | 101072 | 0.00723299  |

## Matched Pre-trend Joint Tests
| spec           | test                                    |   n_restrictions |   statistic |      pvalue |      n |
|:---------------|:----------------------------------------|-----------------:|------------:|------------:|-------:|
| event_att      | pretrend_att_joint_zero                 |                3 |    16.9717  | 0.000716282 | 101072 |
| event_binary_B | pretrend_baseline_joint_zero            |                3 |    14.8405  | 0.00195814  | 101072 |
| event_binary_B | pretrend_displacement_joint_zero        |                3 |     4.8454  | 0.183474    | 101072 |
| event_binary_D | pretrend_length_displacement_joint_zero |                3 |     8.36465 | 0.039047    | 101072 |
| event_binary_D | pretrend_length_baseline_joint_zero     |                3 |     7.0784  | 0.0694405   | 101072 |
| event_score_C  | pretrend_score_baseline_joint_zero      |                3 |    15.4985  | 0.0014366   | 101072 |
| event_score_C  | pretrend_score_slope_joint_zero         |                3 |     2.31666 | 0.509336    | 101072 |

## Blocked Gap Event Study
| spec              | estimand   | term                                                       |      coef |        se |      pvalue |    ci_low |   ci_high |      n |   r2_within |
|:------------------|:-----------|:-----------------------------------------------------------|----------:|----------:|------------:|----------:|----------:|-------:|------------:|
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[-4]:blocked_treated_gap | 0.0829461 | 0.0221797 | 0.00018503  | 0.0394706 |  0.126422 | 101072 |   0.0072589 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[-3]:blocked_treated_gap | 0.125024  | 0.0221513 | 1.6962e-08  | 0.0816043 |  0.168444 | 101072 |   0.0072589 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[-2]:blocked_treated_gap | 0.24596   | 0.0212214 | 0           | 0.204363  |  0.287557 | 101072 |   0.0072589 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[1]:blocked_treated_gap  | 0.159184  | 0.018224  | 0           | 0.123462  |  0.194906 | 101072 |   0.0072589 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[2]:blocked_treated_gap  | 0.104272  | 0.0189935 | 4.09968e-08 | 0.0670418 |  0.141502 | 101072 |   0.0072589 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[3]:blocked_treated_gap  | 0.149854  | 0.0193354 | 9.99201e-15 | 0.111954  |  0.187754 | 101072 |   0.0072589 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[4]:blocked_treated_gap  | 0.135033  | 0.0207036 | 7.19198e-11 | 0.0944509 |  0.175615 | 101072 |   0.0072589 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[-4]:blocked_control_gap | 0.128929  | 0.0133583 | 0           | 0.102744  |  0.155113 | 101072 |   0.0072589 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[-3]:blocked_control_gap | 0.166241  | 0.013273  | 0           | 0.140224  |  0.192258 | 101072 |   0.0072589 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[-2]:blocked_control_gap | 0.292608  | 0.0129431 | 0           | 0.267238  |  0.317979 | 101072 |   0.0072589 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[1]:blocked_control_gap  | 0.167721  | 0.011738  | 0           | 0.144713  |  0.190729 | 101072 |   0.0072589 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[2]:blocked_control_gap  | 0.158414  | 0.0119666 | 0           | 0.134957  |  0.18187  | 101072 |   0.0072589 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[3]:blocked_control_gap  | 0.147145  | 0.0121569 | 0           | 0.123316  |  0.170974 | 101072 |   0.0072589 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[4]:blocked_control_gap  | 0.154811  | 0.0124075 | 0           | 0.130491  |  0.179132 | 101072 |   0.0072589 |

## Pre-period Bias Equality Tests
| spec                   | test                 | term                             |        coef |         se |      pvalue |      n | sample_scope   |
|:-----------------------|:---------------------|:---------------------------------|------------:|-----------:|------------:|-------:|:---------------|
| pretrend_bias_equality | pretrend_bias_linear | non_blocked_treated_control_bias |  0.00224189 | 0.00263174 | 0.394288    | 160592 | full           |
| pretrend_bias_equality | pretrend_bias_linear | bias_equality_difference         |  0.00543156 | 0.0054317  | 0.317322    | 160592 | full           |
| pretrend_bias_equality | pretrend_bias_linear | blocked_treated_control_bias     |  0.00767346 | 0.00475155 | 0.106324    | 160592 | full           |
| pretrend_bias_equality | pretrend_bias_linear | non_blocked_treated_control_bias |  0.0288936  | 0.00753935 | 0.000126916 |  50536 | matched        |
| pretrend_bias_equality | pretrend_bias_linear | bias_equality_difference         | -0.00400458 | 0.01028    | 0.69687     |  50536 | matched        |
| pretrend_bias_equality | pretrend_bias_linear | blocked_treated_control_bias     |  0.024889   | 0.00698833 | 0.000368733 |  50536 | matched        |