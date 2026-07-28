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
| spec                           | estimand                               | term                  |      n |   r2_within |       coef |         se |      pvalue |      ci_low |     ci_high |
|:-------------------------------|:---------------------------------------|:----------------------|-------:|------------:|-----------:|-----------:|------------:|------------:|------------:|
| binary_collapsed               | low_predicted_incidence_effect_delta_b | post_X_treated        | 321184 |   0.0106505 |  0.0110281 | 0.0142257  | 0.448856    |  -0.0189854 |   0.0410417 |
| binary_collapsed               | common_high_minus_low_post_shift       | post_X_disp           | 321184 |   0.0106505 | -0.168781  | 0.00678765 | 8.21565e-15 |  -0.183102  |  -0.154461  |
| binary_collapsed               | high_minus_low_ddd                     | post_X_treated_X_disp | 321184 |   0.0106505 |  0.003676  | 0.0105992  | 0.732984    |  -0.0186864 |   0.0260384 |
| binary_collapsed_group_effects | low_predicted_incidence_effect         | post_X_treated_X_low  | 321184 |   0.0106505 |  0.0110281 | 0.0142257  | 0.448856    |  -0.0189854 |   0.0410417 |
| binary_collapsed_group_effects | high_predicted_incidence_effect        | post_X_treated_X_high | 321184 |   0.0106505 |  0.0147041 | 0.0140262  | 0.309161    |  -0.0148885 |   0.0442968 |
| binary_collapsed_logit         | nan                                    | post_X_treated        | 321184 | nan         |  0.0551024 | 0.119508   | 0.644743    | nan         | nan         |
| binary_collapsed_logit         | nan                                    | post_X_disp           | 321184 | nan         |  1.66773   | 0.0400458  | 0           | nan         | nan         |
| binary_collapsed_logit         | nan                                    | post_X_treated_X_disp | 321184 | nan         |  0.0110643 | 0.0901233  | 0.90229     | nan         | nan         |

## Score Spec
| spec            |   estimand | term                   |      n |   r2_within |        coef |        se |      pvalue |     ci_low |    ci_high |
|:----------------|-----------:|:-----------------------|-------:|------------:|------------:|----------:|------------:|-----------:|-----------:|
| score_collapsed |        nan | post_X_treated         | 321184 |    0.016146 |  0.0109336  | 0.013926  | 0.443186    | -0.0184476 |  0.0403149 |
| score_collapsed |        nan | post_X_score           | 321184 |    0.016146 | -0.292552   | 0.0118753 | 9.54792e-15 | -0.317606  | -0.267497  |
| score_collapsed |        nan | post_X_treated_X_score | 321184 |    0.016146 |  0.00973719 | 0.0154241 | 0.536244    | -0.0228049 |  0.0422792 |

## Event-study Specs
| spec           | estimand   | term                                                              |         coef |         se |      pvalue |       ci_low |     ci_high |      n |   r2_within |
|:---------------|:-----------|:------------------------------------------------------------------|-------------:|-----------:|------------:|-------------:|------------:|-------:|------------:|
| event_att      |            | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.000177793 | 0.0162415  | 0.991393    | -0.0340887   |  0.0344443  | 321184 |  0.00011149 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00406475  | 0.0181555  | 0.825515    | -0.0423696   |  0.0342401  | 321184 |  0.00011149 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00300674  | 0.0132941  | 0.823766    | -0.0250414   |  0.0310549  | 321184 |  0.00011149 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0147617   | 0.0100568  | 0.160408    | -0.00645628  |  0.0359797  | 321184 |  0.00011149 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0034823   | 0.0128668  | 0.789925    | -0.0236644   |  0.030629   | 321184 |  0.00011149 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0280216   | 0.0127915  | 0.0427033   |  0.00103386  |  0.0550094  | 321184 |  0.00011149 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00990424  | 0.0136521  | 0.47803     | -0.0188992   |  0.0387076  | 321184 |  0.00011149 |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00292551  | 0.0161867  | 0.858712    | -0.0312254   |  0.0370764  | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00214215  | 0.0172637  | 0.902704    | -0.0385653   |  0.034281   | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0153236   | 0.0122585  | 0.228219    | -0.0105395   |  0.0411868  | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0168449   | 0.0126989  | 0.202226    | -0.0099475   |  0.0436372  | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0111083   | 0.0108106  | 0.318565    | -0.0117      |  0.0339167  | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0259752   | 0.0121142  | 0.0467675   |  0.000416397 |  0.051534   | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00743283  | 0.0114897  | 0.526329    | -0.0168084   |  0.031674   | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             | -0.0145061   | 0.0276954  | 0.607197    | -0.0729382   |  0.043926   | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             | -0.013997    | 0.0341167  | 0.686733    | -0.0859769   |  0.0579829  | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.042809    | 0.026863   | 0.129447    | -0.0994851   |  0.013867   | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0151632   | 0.0242727  | 0.540461    | -0.0663742   |  0.0360478  | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.0353912   | 0.0226878  | 0.137199    | -0.0832582   |  0.0124758  | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              | -0.00138925  | 0.029547   | 0.963047    | -0.0637279   |  0.0609494  | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.0031314   | 0.0266005  | 0.907669    | -0.0592535   |  0.0529907  | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.0122151   | 0.018796   | 0.524456    | -0.0518711   |  0.0274409  | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.0485045   | 0.0166712  | 0.00976455  |  0.0133312   |  0.0836777  | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.180528    | 0.0205076  | 9.69284e-08 |  0.137261    |  0.223795   | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0874498   | 0.0120915  | 1.40128e-06 | -0.112961    | -0.0619389  | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.108162    | 0.0133054  | 2.93274e-07 | -0.136234    | -0.0800898  | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.125292    | 0.0132412  | 3.45919e-08 | -0.153229    | -0.0973556  | 321184 |  0.0151918  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.137909    | 0.0110348  | 5.3904e-10  | -0.161191    | -0.114628   | 321184 |  0.0151918  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00302713  | 0.0152406  | 0.844914    | -0.0291277   |  0.035182   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00238941  | 0.0158121  | 0.881665    | -0.0357501   |  0.0309713  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0125968   | 0.0111861  | 0.275762    | -0.0110037   |  0.0361973  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0178179   | 0.0118953  | 0.152499    | -0.00727898  |  0.0429148  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0106858   | 0.0105425  | 0.324986    | -0.0115569   |  0.0329284  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0258209   | 0.0120537  | 0.0469538   |  0.000389738 |  0.051252   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00684079  | 0.0114446  | 0.5579      | -0.0173052   |  0.0309868  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0139385   | 0.0390212  | 0.725335    | -0.068389    |  0.0962661  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0291574   | 0.0439807  | 0.516246    | -0.0636338   |  0.121949   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -1.69568e-05 | 0.0399302  | 0.999666    | -0.0842623   |  0.0842284  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0164024   | 0.0266417  | 0.54627     | -0.0726113   |  0.0398066  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.00977853  | 0.0266699  | 0.718403    | -0.066047    |  0.0464899  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.0280873   | 0.0333122  | 0.410849    | -0.0421952   |  0.0983699  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.0275013   | 0.0287607  | 0.352367    | -0.0331785   |  0.0881811  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.00424947  | 0.0131229  | 0.750024    | -0.0319365   |  0.0234375  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.0573518   | 0.0115089  | 0.000113488 |  0.0330701   |  0.0816334  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.193645    | 0.0159445  | 8.37225e-10 |  0.160005    |  0.227285   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0856087   | 0.0135697  | 7.85302e-06 | -0.114238    | -0.0569791  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.101382    | 0.0152728  | 4.1918e-06  | -0.133604    | -0.0691588  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.117752    | 0.0121728  | 2.5133e-08  | -0.143434    | -0.0920699  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.132439    | 0.00909336 | 4.93758e-11 | -0.151625    | -0.113254   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_len              |  0.00615946  | 0.00996487 | 0.544691    | -0.0148646   |  0.0271835  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_len              |  0.0102664   | 0.0181931  | 0.579918    | -0.0281176   |  0.0486504  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_len              | -0.0191007   | 0.013363   | 0.171019    | -0.0472942   |  0.00909287 | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:treated_X_len               |  0.0193908   | 0.0104978  | 0.0822068   | -0.0027575   |  0.0415392  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:treated_X_len               | -0.0116736   | 0.00792746 | 0.159144    | -0.0283991   |  0.00505186 | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:treated_X_len               | -0.00358753  | 0.0109357  | 0.746874    | -0.0266598   |  0.0194847  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:treated_X_len               | -0.00673165  | 0.0088309  | 0.456338    | -0.0253632   |  0.0118999  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:disp_X_len                 | -0.0384908   | 0.012933   | 0.00847433  | -0.0657772   | -0.0112045  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:disp_X_len                 | -0.0410227   | 0.0139521  | 0.00914715  | -0.0704591   | -0.0115862  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:disp_X_len                 | -0.0518197   | 0.0160806  | 0.00499953  | -0.0857468   | -0.0178925  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:disp_X_len                  | -0.00348391  | 0.0152434  | 0.821943    | -0.0356446   |  0.0286768  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:disp_X_len                  | -0.0235303   | 0.0187175  | 0.225705    | -0.0630208   |  0.0159602  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:disp_X_len                  | -0.0273846   | 0.0154305  | 0.0938534   | -0.05994     |  0.00517083 | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:disp_X_len                  | -0.022416    | 0.0094764  | 0.0301574   | -0.0424094   | -0.00242255 | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:tXdXlen                    | -0.0230121   | 0.0248353  | 0.367108    | -0.07541     |  0.0293858  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:tXdXlen                    | -0.0464595   | 0.0236564  | 0.0661061   | -0.0963701   |  0.00345116 | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:tXdXlen                    | -0.00934159  | 0.020726   | 0.657888    | -0.0530697   |  0.0343865  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:tXdXlen                     | -0.0161205   | 0.0175577  | 0.371387    | -0.053164    |  0.020923   | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:tXdXlen                     | -0.0074494   | 0.0187461  | 0.696029    | -0.0470002   |  0.0321014  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:tXdXlen                     | -0.0193786   | 0.0234366  | 0.419777    | -0.0688255   |  0.0300684  | 321184 |  0.0162182  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:tXdXlen                     | -0.02118     | 0.0202757  | 0.310835    | -0.0639579   |  0.021598   | 321184 |  0.0162182  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00110688  | 0.016571   | 0.947523    | -0.0360685   |  0.0338548  | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00589225  | 0.0176221  | 0.742192    | -0.0430716   |  0.0312871  | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00434379  | 0.0148552  | 0.773513    | -0.026998    |  0.0356855  | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0120129   | 0.0107929  | 0.281183    | -0.0107581   |  0.034784   | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.000744063 | 0.0109668  | 0.946699    | -0.0223938   |  0.0238819  | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0246139   | 0.0121925  | 0.0595706   | -0.0011101   |  0.0503379  | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0052434   | 0.0120157  | 0.668053    | -0.0201075   |  0.0305943  | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.000884528 | 0.0406593  | 0.982897    | -0.0848991   |  0.0866682  | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            | -0.0231798   | 0.042778   | 0.594944    | -0.113433    |  0.0670738  | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.0355538   | 0.0408718  | 0.396479    | -0.121786    |  0.0506781  | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.00689051  | 0.026631   | 0.798943    | -0.0630771   |  0.0492961  | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.0336226   | 0.0276104  | 0.239953    | -0.0918755   |  0.0246304  | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.0157705   | 0.0337891  | 0.646616    | -0.0555182   |  0.0870592  | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.00799824  | 0.0343057  | 0.818432    | -0.0643804   |  0.0803769  | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.00820322  | 0.032278   | 0.802434    | -0.0763039   |  0.0598975  | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.0885007   | 0.0254386  | 0.00287193  |  0.0348299   |  0.142172   | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.244076    | 0.0286721  | 1.55098e-07 |  0.183584    |  0.304569   | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.171252    | 0.0205149  | 2.03531e-07 | -0.214535    | -0.12797    | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.199693    | 0.0237442  | 1.83554e-07 | -0.249789    | -0.149597   | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.232563    | 0.0211735  | 3.84822e-09 | -0.277235    | -0.18789    | 321184 |  0.0203791  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.243652    | 0.0178561  | 1.37662e-10 | -0.281325    | -0.205979   | 321184 |  0.0203791  |

## Pre-trend Joint Tests
| spec           | test                                    |   n_restrictions |   statistic |    pvalue |      n |
|:---------------|:----------------------------------------|-----------------:|------------:|----------:|-------:|
| event_att      | pretrend_att_joint_zero                 |                3 |    0.333004 | 0.953706  | 321184 |
| event_binary_B | pretrend_baseline_joint_zero            |                3 |    2.27225  | 0.517858  | 321184 |
| event_binary_B | pretrend_displacement_joint_zero        |                3 |    4.49663  | 0.212591  | 321184 |
| event_binary_D | pretrend_length_displacement_joint_zero |                3 |   11.2347   | 0.0105221 | 321184 |
| event_binary_D | pretrend_length_baseline_joint_zero     |                3 |    9.05908  | 0.0285156 | 321184 |
| event_score_C  | pretrend_score_baseline_joint_zero      |                3 |    0.577022 | 0.901672  | 321184 |
| event_score_C  | pretrend_score_slope_joint_zero         |                3 |    3.22506  | 0.358209  | 321184 |

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
| spec                           | estimand                               | term                  |      n |    r2_within |       coef |         se |      pvalue |       ci_low |     ci_high |
|:-------------------------------|:---------------------------------------|:----------------------|-------:|-------------:|-----------:|-----------:|------------:|-------------:|------------:|
| binary_collapsed               | low_predicted_incidence_effect_delta_b | post_X_treated        | 101072 |   0.00020264 |  0.0353467 | 0.0179057  | 0.0648539   |  -0.00243105 |   0.0731244 |
| binary_collapsed               | common_high_minus_low_post_shift       | post_X_disp           | 101072 |   0.00020264 |  0.0174608 | 0.00979348 | 0.0924681   |  -0.00320166 |   0.0381232 |
| binary_collapsed               | high_minus_low_ddd                     | post_X_treated_X_disp | 101072 |   0.00020264 | -0.0212828 | 0.0157956  | 0.195541    |  -0.0546087  |   0.012043  |
| binary_collapsed_group_effects | low_predicted_incidence_effect         | post_X_treated_X_low  | 101072 |   0.00020264 |  0.0353467 | 0.0179057  | 0.0648539   |  -0.00243106 |   0.0731245 |
| binary_collapsed_group_effects | high_predicted_incidence_effect        | post_X_treated_X_high | 101072 |   0.00020264 |  0.0140639 | 0.0190626  | 0.470714    |  -0.0261547  |   0.0542825 |
| binary_collapsed_logit         | nan                                    | post_X_treated        | 101072 | nan          |  0.0847538 | 0.0990786  | 0.392319    | nan          | nan         |
| binary_collapsed_logit         | nan                                    | post_X_disp           | 101072 | nan          |  0.640746  | 0.047599   | 2.64084e-41 | nan          | nan         |
| binary_collapsed_logit         | nan                                    | post_X_treated_X_disp | 101072 | nan          | -0.024483  | 0.0754123  | 0.745442    | nan          | nan         |

## Matched Event-study Specs
| spec           | estimand   | term                                                              |        coef |        se |      pvalue |      ci_low |      ci_high |      n |   r2_within |
|:---------------|:-----------|:------------------------------------------------------------------|------------:|----------:|------------:|------------:|-------------:|-------:|------------:|
| event_att      |            | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0520851  | 0.0277215 | 0.0775199   | -0.110572   |  0.00640216  | 101072 | 0.000467142 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0647059  | 0.0313032 | 0.0543043   | -0.13075    |  0.00133818  | 101072 | 0.000467142 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0401166  | 0.0316133 | 0.221548    | -0.106815   |  0.0265816   | 101072 | 0.000467142 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00885115 | 0.0158066 | 0.582808    | -0.0422003  |  0.024498    | 101072 | 0.000467142 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0389057  | 0.0196284 | 0.0638715   | -0.0803181  |  0.00250672  | 101072 | 0.000467142 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00399688 | 0.0216177 | 0.855503    | -0.0416124  |  0.0496061   | 101072 | 0.000467142 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0154833  | 0.0267768 | 0.570686    | -0.0719775  |  0.0410108   | 101072 | 0.000467142 |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0568847  | 0.0299401 | 0.0745385   | -0.120053   |  0.00628338  | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0874354  | 0.0391768 | 0.0393749   | -0.170091   | -0.00477969  | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0252965  | 0.0346411 | 0.475184    | -0.0983828  |  0.0477899   | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00669738 | 0.0185003 | 0.721802    | -0.0457296  |  0.0323348   | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.021416   | 0.023377  | 0.372421    | -0.0707371  |  0.0279052   | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00782995 | 0.0211835 | 0.716226    | -0.0368633  |  0.0525232   | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00836616 | 0.0351864 | 0.814904    | -0.082603   |  0.0658706   | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0103143  | 0.0297054 | 0.732689    | -0.0523586  |  0.0729871   | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0451879  | 0.0465041 | 0.344825    | -0.0529271  |  0.143303    | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.0215274  | 0.0307033 | 0.492701    | -0.0863058  |  0.043251    | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.00183602 | 0.0252384 | 0.942856    | -0.0550843  |  0.0514123   | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.0327241  | 0.0200273 | 0.120646    | -0.0749781  |  0.00952987  | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              | -0.00504017 | 0.0345026 | 0.885576    | -0.0778343  |  0.0677539   | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.0113937  | 0.0406894 | 0.782843    | -0.097241   |  0.0744535   | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.117392   | 0.0391281 | 0.00805127  |  0.0348391  |  0.199945    | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.149366   | 0.0383214 | 0.00115738  |  0.0685154  |  0.230218    | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.287801   | 0.0431326 | 3.92883e-06 |  0.196799   |  0.378803    | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  0.166472   | 0.024759  | 3.56874e-06 |  0.114235   |  0.218709    | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.154372   | 0.0259473 | 1.58442e-05 |  0.099628   |  0.209116    | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.148721   | 0.0290208 | 8.44979e-05 |  0.0874921  |  0.209949    | 101072 | 0.00763886  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.153253   | 0.0290993 | 6.2977e-05  |  0.0918593  |  0.214647    | 101072 | 0.00763886  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0603802  | 0.0290616 | 0.0532072   | -0.121695   |  0.000934443 | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0916286  | 0.0399149 | 0.0346904   | -0.175842   | -0.00741553  | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0291662  | 0.0321421 | 0.376871    | -0.0969801  |  0.0386477   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00814415 | 0.017592  | 0.649275    | -0.0452601  |  0.0289718   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0221571  | 0.0222264 | 0.3328      | -0.0690507  |  0.0247365   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0054616  | 0.0230798 | 0.815764    | -0.0432324  |  0.0541556   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0116891  | 0.0366847 | 0.753883    | -0.0890871  |  0.0657088   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0454716  | 0.0393649 | 0.264015    | -0.037581   |  0.128524    | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.102323   | 0.0528075 | 0.0694602   | -0.00909155 |  0.213737    | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0186399  | 0.0380048 | 0.630077    | -0.0615432  |  0.098823    | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.00452052 | 0.0259888 | 0.863966    | -0.0503111  |  0.0593521   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.00337906 | 0.0301    | 0.911931    | -0.0668844  |  0.0601263   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.0423306  | 0.0283496 | 0.153721    | -0.0174818  |  0.102143    | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.0243713  | 0.0405103 | 0.555374    | -0.0610979  |  0.109841    | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.140355   | 0.0363707 | 0.00125885  |  0.0636191  |  0.21709     | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.173635   | 0.0355711 | 0.000140561 |  0.0985862  |  0.248683    | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.329928   | 0.026079  | 4.46537e-10 |  0.274906   |  0.38495     | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  0.186353   | 0.0220874 | 1.75607e-07 |  0.139752   |  0.232953    | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.182431   | 0.0210387 | 1.19824e-07 |  0.138044   |  0.226819    | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.173492   | 0.0242805 | 1.6401e-06  |  0.122265   |  0.22472     | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.174081   | 0.0242379 | 1.53411e-06 |  0.122944   |  0.225219    | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_len              | -0.00330472 | 0.0191241 | 0.864847    | -0.0436531  |  0.0370437   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_len              |  0.00513227 | 0.0414161 | 0.902832    | -0.082248   |  0.0925125   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_len              | -0.0420274  | 0.0331554 | 0.222033    | -0.111979   |  0.0279243   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:treated_X_len               |  0.0152667  | 0.0208071 | 0.473113    | -0.0286324  |  0.0591659   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:treated_X_len               | -0.0484858  | 0.0198169 | 0.0255852   | -0.0902959  | -0.0066757   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:treated_X_len               | -0.0246342  | 0.0201189 | 0.237487    | -0.0670815  |  0.017813    | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:treated_X_len               | -0.0425448  | 0.0261572 | 0.122235    | -0.0977318  |  0.0126421   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:disp_X_len                 | -0.0796435  | 0.019726  | 0.000854902 | -0.121262   | -0.0380252   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:disp_X_len                 | -0.0863375  | 0.0188263 | 0.000262779 | -0.126057   | -0.0466175   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:disp_X_len                 | -0.117775   | 0.0230214 | 8.6043e-05  | -0.166346   | -0.0692044   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:disp_X_len                  | -0.055815   | 0.0159599 | 0.00276069  | -0.0894874  | -0.0221426   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:disp_X_len                  | -0.0829039  | 0.0194572 | 0.000527657 | -0.123955   | -0.0418528   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:disp_X_len                  | -0.0793272  | 0.0217989 | 0.0020294   | -0.125319   | -0.0333356   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:disp_X_len                  | -0.0764581  | 0.0148614 | 8.1039e-05  | -0.107813   | -0.0451032   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:tXdXlen                    | -0.00055937 | 0.0266716 | 0.983512    | -0.0568315  |  0.0557127   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:tXdXlen                    | -0.0331275  | 0.0424934 | 0.446349    | -0.122781   |  0.0565257   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:tXdXlen                    |  0.0422238  | 0.0326538 | 0.213283    | -0.0266698  |  0.111117    | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:tXdXlen                     |  0.00409086 | 0.0282005 | 0.886367    | -0.0554069  |  0.0635886   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:tXdXlen                     |  0.0519128  | 0.0303033 | 0.104869    | -0.0120216  |  0.115847    | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:tXdXlen                     |  0.00395836 | 0.0282761 | 0.890313    | -0.055699   |  0.0636157   | 101072 | 0.0110073   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:tXdXlen                     |  0.0340639  | 0.0343059 | 0.334659    | -0.0383151  |  0.106443    | 101072 | 0.0110073   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0606562  | 0.0283766 | 0.0473769   | -0.120526   | -0.000786873 | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.075744   | 0.0364815 | 0.0533541   | -0.152713   |  0.00122521  | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0334489  | 0.0324823 | 0.317553    | -0.101981   |  0.0350827   | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00451166 | 0.0175974 | 0.800733    | -0.041639   |  0.0326156   | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0294547  | 0.0218744 | 0.195808    | -0.0756055  |  0.0166962   | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00583494 | 0.0221047 | 0.794978    | -0.0408019  |  0.0524718   | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00952694 | 0.0322803 | 0.771467    | -0.0776324  |  0.0585785   | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.0411482  | 0.0544963 | 0.460544    | -0.0738289  |  0.156125    | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.0480189  | 0.0868874 | 0.587693    | -0.135298   |  0.231335    | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.0184953  | 0.0698063 | 0.794232    | -0.165774   |  0.128783    | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.0233366  | 0.0425361 | 0.590393    | -0.11308    |  0.0664067   | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.0506608  | 0.0371794 | 0.190787    | -0.129102   |  0.0277808   | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             | -0.0104911  | 0.0564678 | 0.854809    | -0.129628   |  0.108646    | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             | -0.0333652  | 0.0749887 | 0.661979    | -0.191577   |  0.124847    | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered |  0.146183   | 0.0636148 | 0.0345285   |  0.0119677  |  0.280399    | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.206193   | 0.0606609 | 0.00341441  |  0.0782093  |  0.334176    | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.498303   | 0.0790218 | 7.89723e-06 |  0.331582   |  0.665025    | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  |  0.241598   | 0.0454971 | 5.75667e-05 |  0.145607   |  0.337588    | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  |  0.212908   | 0.044995  | 0.000192751 |  0.117977   |  0.30784     | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  |  0.193246   | 0.0484306 | 0.000947185 |  0.0910663  |  0.295425    | 101072 | 0.00723299  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  |  0.205475   | 0.0521592 | 0.0010574   |  0.0954287  |  0.315521    | 101072 | 0.00723299  |

## Matched Pre-trend Joint Tests
| spec           | test                                    |   n_restrictions |   statistic |    pvalue |      n |
|:---------------|:----------------------------------------|-----------------:|------------:|----------:|-------:|
| event_att      | pretrend_att_joint_zero                 |                3 |     5.08037 | 0.166006  | 101072 |
| event_binary_B | pretrend_baseline_joint_zero            |                3 |     6.22055 | 0.101359  | 101072 |
| event_binary_B | pretrend_displacement_joint_zero        |                3 |     2.43206 | 0.487695  | 101072 |
| event_binary_D | pretrend_length_displacement_joint_zero |                3 |    12.1599  | 0.0068551 | 101072 |
| event_binary_D | pretrend_length_baseline_joint_zero     |                3 |     8.11631 | 0.0436681 | 101072 |
| event_score_C  | pretrend_score_baseline_joint_zero      |                3 |     6.24754 | 0.100169  | 101072 |
| event_score_C  | pretrend_score_slope_joint_zero         |                3 |     1.32408 | 0.723422  | 101072 |

## Blocked Gap Event Study
| spec              | estimand   | term                                                       |      coef |        se |      pvalue |     ci_low |   ci_high |      n |   r2_within |
|:------------------|:-----------|:-----------------------------------------------------------|----------:|----------:|------------:|-----------:|----------:|-------:|------------:|
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[-4]:blocked_treated_gap | 0.0829461 | 0.0444865 | 0.0796086   | -0.0109121 |  0.176804 | 101072 |   0.0072589 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[-3]:blocked_treated_gap | 0.125024  | 0.0505139 | 0.0241485   |  0.0184493 |  0.231599 | 101072 |   0.0072589 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[-2]:blocked_treated_gap | 0.24596   | 0.0465955 | 6.14316e-05 |  0.147652  |  0.344268 | 101072 |   0.0072589 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[1]:blocked_treated_gap  | 0.159184  | 0.0330903 | 0.000163165 |  0.0893697 |  0.228998 | 101072 |   0.0072589 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[2]:blocked_treated_gap  | 0.104272  | 0.0327387 | 0.00541993  |  0.0351993 |  0.173344 | 101072 |   0.0072589 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[3]:blocked_treated_gap  | 0.149854  | 0.0423671 | 0.00253222  |  0.0604675 |  0.239241 | 101072 |   0.0072589 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[4]:blocked_treated_gap  | 0.135033  | 0.0400571 | 0.00362836  |  0.0505198 |  0.219546 | 101072 |   0.0072589 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[-4]:blocked_control_gap | 0.128929  | 0.0380903 | 0.00352162  |  0.0485651 |  0.209292 | 101072 |   0.0072589 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[-3]:blocked_control_gap | 0.166241  | 0.0401108 | 0.000678167 |  0.0816144 |  0.250867 | 101072 |   0.0072589 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[-2]:blocked_control_gap | 0.292608  | 0.0426063 | 2.72897e-06 |  0.202717  |  0.382499 | 101072 |   0.0072589 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[1]:blocked_control_gap  | 0.167721  | 0.0254181 | 4.51654e-06 |  0.114094  |  0.221349 | 101072 |   0.0072589 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[2]:blocked_control_gap  | 0.158414  | 0.0247624 | 6.62366e-06 |  0.106169  |  0.210658 | 101072 |   0.0072589 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[3]:blocked_control_gap  | 0.147145  | 0.0292275 | 0.00010196  |  0.0854804 |  0.20881  | 101072 |   0.0072589 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[4]:blocked_control_gap  | 0.154811  | 0.0288576 | 5.14701e-05 |  0.093927  |  0.215695 | 101072 |   0.0072589 |

## Pre-period Bias Equality Tests
| spec                   | test                 | term                             |        coef |         se |     pvalue |      n | sample_scope   |
|:-----------------------|:---------------------|:---------------------------------|------------:|-----------:|-----------:|-------:|:---------------|
| pretrend_bias_equality | pretrend_bias_linear | non_blocked_treated_control_bias |  0.00224189 | 0.00538397 | 0.677116   | 160592 | full           |
| pretrend_bias_equality | pretrend_bias_linear | bias_equality_difference         |  0.00543156 | 0.00961401 | 0.572099   | 160592 | full           |
| pretrend_bias_equality | pretrend_bias_linear | blocked_treated_control_bias     |  0.00767346 | 0.00957374 | 0.422836   | 160592 | full           |
| pretrend_bias_equality | pretrend_bias_linear | non_blocked_treated_control_bias |  0.0288936  | 0.00942403 | 0.00216981 |  50536 | matched        |
| pretrend_bias_equality | pretrend_bias_linear | bias_equality_difference         | -0.00400458 | 0.011729   | 0.732783   |  50536 | matched        |
| pretrend_bias_equality | pretrend_bias_linear | blocked_treated_control_bias     |  0.024889   | 0.0136499  | 0.0682456  |  50536 | matched        |