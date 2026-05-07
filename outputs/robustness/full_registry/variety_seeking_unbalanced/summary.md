# Displacement Effect Estimation Summary

- Sample rows: 358,864
- Unique members: 44,858
- Unique closures: 22
- Event FE units: 44,858
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=false
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Model type: DDD


## Binary Specs
| spec             | term                  |      n |   r2_within |       coef |         se |      pvalue |
|:-----------------|:----------------------|-------:|------------:|-----------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 113269 | 0.000486913 |  0.0309441 | 0.0112929  | 0.00614545  |
| binary_collapsed | post_X_disp           | 113269 | 0.000486913 |  0.0358733 | 0.00595093 | 1.67993e-09 |
| binary_collapsed | post_X_treated_X_disp | 113269 | 0.000486913 | -0.0386445 | 0.0136936  | 0.00477485  |

## Score Spec
| spec            | term                   |      n |   r2_within |       coef |         se |      pvalue |
|:----------------|:-----------------------|-------:|------------:|-----------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 113269 | 0.000409857 |  0.0206713 | 0.00951561 | 0.0298378   |
| score_collapsed | post_X_score           | 113269 | 0.000409857 |  0.0523767 | 0.00905995 | 7.50368e-09 |
| score_collapsed | post_X_treated_X_score | 113269 | 0.000409857 | -0.0469681 | 0.0207442  | 0.023573    |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |      n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|-------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0138182   | 0.0119893  | 0.249108    | 113269 | 0.000273345 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00320072  | 0.0120878  | 0.791174    | 113269 | 0.000273345 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0177001   | 0.0116539  | 0.128819    | 113269 | 0.000273345 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0295476   | 0.0123322  | 0.0165834   | 113269 | 0.000273345 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00334774  | 0.0125443  | 0.789569    | 113269 | 0.000273345 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0237943   | 0.012527   | 0.0575163   | 113269 | 0.000273345 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0125536   | 0.0125299  | 0.316407    | 113269 | 0.000273345 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0308763   | 0.021599   | 0.152865    | 113269 | 0.00138679  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0148626   | 0.0220875  | 0.501019    | 113269 | 0.00138679  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0250186   | 0.0227228  | 0.27089     | 113269 | 0.00138679  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0323125   | 0.0220748  | 0.143269    | 113269 | 0.00138679  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0187094   | 0.021636   | 0.387193    | 113269 | 0.00138679  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.00407485  | 0.0219804  | 0.852928    | 113269 | 0.00138679  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00602564  | 0.0220494  | 0.784641    | 113269 | 0.00138679  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0283862   | 0.025817   | 0.271553    | 113269 | 0.00138679  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0182821   | 0.026213   | 0.48553     | 113269 | 0.00138679  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.00997657  | 0.0262272  | 0.703659    | 113269 | 0.00138679  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.00335385  | 0.0264446  | 0.899079    | 113269 | 0.00138679  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.0364227   | 0.0264848  | 0.169072    | 113269 | 0.00138679  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              | -0.0322284   | 0.0266241  | 0.226098    | 113269 | 0.00138679  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.0300416   | 0.0266473  | 0.259593    | 113269 | 0.00138679  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.030167    | 0.010963   | 0.00593254  | 113269 | 0.00138679  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.0316024   | 0.0108988  | 0.00373935  | 113269 | 0.00138679  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.00471234  | 0.0112658  | 0.675741    | 113269 | 0.00138679  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  0.0167453   | 0.0113848  | 0.141342    | 113269 | 0.00138679  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.0587714   | 0.011324   | 2.11883e-07 | 113269 | 0.00138679  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.0674312   | 0.0117716  | 1.02543e-08 | 113269 | 0.00138679  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.0710285   | 0.0116151  | 9.78077e-10 | 113269 | 0.00138679  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0289293   | 0.0217993  | 0.184494    | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00912544  | 0.0223792  | 0.68345     | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0266485   | 0.0231266  | 0.249213    | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0272307   | 0.0226333  | 0.228938    | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.020544    | 0.0218635  | 0.347406    | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.00276821  | 0.0222105  | 0.900813    | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00785808  | 0.0222376  | 0.723814    | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0127306   | 0.027393   | 0.642122    | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             | -0.00289736  | 0.0278469  | 0.917133    | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.00366744  | 0.0276994  | 0.894668    | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0165689   | 0.0287582  | 0.564523    | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.0402418   | 0.0279206  | 0.149513    | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              | -0.0352121   | 0.0283773  | 0.214671    | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.0372344   | 0.0280407  | 0.184233    | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.0316764   | 0.0110253  | 0.00406836  | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.03504     | 0.01094    | 0.00136207  | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.00326     | 0.0113133  | 0.773229    | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  0.0161908   | 0.0114645  | 0.157885    | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.0639926   | 0.0113735  | 1.85807e-08 | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.0706276   | 0.0118604  | 2.63498e-09 | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.0753937   | 0.0116794  | 1.09899e-10 | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_len              | -0.0112299   | 0.0178712  | 0.529759    | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_len              | -0.0362674   | 0.0178299  | 0.0419533   | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_len              |  0.0150177   | 0.0173762  | 0.387449    | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_len               |  0.0135607   | 0.0174306  | 0.436585    | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_len               | -0.0310169   | 0.0173779  | 0.0742979   | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated_X_len               | -0.0230569   | 0.0174479  | 0.186355    | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated_X_len               | -0.046657    | 0.0184517  | 0.0114574   | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:disp_X_len                 | -0.00444271  | 0.00707612 | 0.53011     | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:disp_X_len                 | -0.0125259   | 0.00642568 | 0.0512644   | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_X_len                 |  0.0100086   | 0.00555057 | 0.0713739   | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_X_len                  | -0.000485783 | 0.00633982 | 0.938923    | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_X_len                  | -0.02766     | 0.00668043 | 3.47698e-05 | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:disp_X_len                  | -0.0233284   | 0.00719624 | 0.00118947  | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:disp_X_len                  | -0.040685    | 0.00874851 | 3.32716e-06 | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:tXdXlen                    |  0.0305546   | 0.0215666  | 0.156565    | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:tXdXlen                    |  0.0622535   | 0.0215426  | 0.00385814  | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:tXdXlen                    | -0.0128592   | 0.0206357  | 0.533188    | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:tXdXlen                     |  0.00411865  | 0.0215793  | 0.848635    | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:tXdXlen                     |  0.044085    | 0.0217456  | 0.0426409   | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:tXdXlen                     |  0.0303267   | 0.0216925  | 0.162117    | 113269 | 0.00241149  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:tXdXlen                     |  0.061258    | 0.0225078  | 0.00650021  | 113269 | 0.00241149  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0266432   | 0.0183839  | 0.147275    | 113269 | 0.00138388  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0106814   | 0.0186557  | 0.566951    | 113269 | 0.00138388  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0261849   | 0.01955    | 0.180458    | 113269 | 0.00138388  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0258587   | 0.0185795  | 0.163998    | 113269 | 0.00138388  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0055214   | 0.0181018  | 0.760354    | 113269 | 0.00138388  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0132452   | 0.0183955  | 0.471516    | 113269 | 0.00138388  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.000164462 | 0.0185069  | 0.99291     | 113269 | 0.00138388  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.0451569   | 0.0390008  | 0.246938    | 113269 | 0.00138388  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.0250519   | 0.0392797  | 0.523621    | 113269 | 0.00138388  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.0249102   | 0.0404107  | 0.537618    | 113269 | 0.00138388  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.0159176   | 0.0391253  | 0.684132    | 113269 | 0.00138388  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.0312505   | 0.0391329  | 0.424545    | 113269 | 0.00138388  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             | -0.037946    | 0.0390806  | 0.331574    | 113269 | 0.00138388  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             | -0.044736    | 0.0395571  | 0.258098    | 113269 | 0.00138388  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered |  0.0577486   | 0.0168834  | 0.000626168 | 113269 | 0.00138388  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.0537122   | 0.0168986  | 0.00148212  | 113269 | 0.00138388  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0196482   | 0.0176102  | 0.264547    | 113269 | 0.00138388  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  |  0.0261089   | 0.0169633  | 0.123781    | 113269 | 0.00138388  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  |  0.0937287   | 0.0170444  | 3.85254e-08 | 113269 | 0.00138388  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  |  0.110324    | 0.0175713  | 3.46797e-10 | 113269 | 0.00138388  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  |  0.117979    | 0.017316   | 9.7431e-12  | 113269 | 0.00138388  |

## Pre-trend Joint Tests
| spec           | test                                    |   n_restrictions |   statistic |    pvalue |      n |
|:---------------|:----------------------------------------|-----------------:|------------:|----------:|-------:|
| event_att      | pretrend_att_joint_zero                 |                3 |     3.23936 | 0.356173  | 113269 |
| event_binary_B | pretrend_baseline_joint_zero            |                3 |     2.36635 | 0.49993   | 113269 |
| event_binary_B | pretrend_displacement_joint_zero        |                3 |     1.2855  | 0.732578  | 113269 |
| event_binary_D | pretrend_length_displacement_joint_zero |                3 |    14.5526  | 0.0022418 | 113269 |
| event_binary_D | pretrend_length_baseline_joint_zero     |                3 |     9.0228  | 0.0289893 | 113269 |
| event_score_C  | pretrend_score_baseline_joint_zero      |                3 |     2.97323 | 0.39577   | 113269 |
| event_score_C  | pretrend_score_slope_joint_zero         |                3 |     1.34505 | 0.718465  | 113269 |