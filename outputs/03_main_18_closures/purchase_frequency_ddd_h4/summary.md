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
| spec                           | estimand                               | term                  |      n |   r2_within |         coef |         se |      pvalue |      ci_low |     ci_high |
|:-------------------------------|:---------------------------------------|:----------------------|-------:|------------:|-------------:|-----------:|------------:|------------:|------------:|
| binary_collapsed               | low_predicted_incidence_effect_delta_b | post_X_treated        | 321184 |   0.0130244 |  0.000891858 | 0.00236445 | 0.710696    | -0.0040967  |  0.00588041 |
| binary_collapsed               | common_high_minus_low_post_shift       | post_X_disp           | 321184 |   0.0130244 | -0.0343661   | 0.00296791 | 1.73377e-09 | -0.0406278  | -0.0281044  |
| binary_collapsed               | high_minus_low_ddd                     | post_X_treated_X_disp | 321184 |   0.0130244 |  0.00582887  | 0.0031978  | 0.0859738   | -0.00091789 |  0.0125756  |
| binary_collapsed_group_effects | low_predicted_incidence_effect         | post_X_treated_X_low  | 321184 |   0.0130244 |  0.000891858 | 0.00236445 | 0.710696    | -0.0040967  |  0.00588041 |
| binary_collapsed_group_effects | high_predicted_incidence_effect        | post_X_treated_X_high | 321184 |   0.0130244 |  0.00672073  | 0.00448572 | 0.152407    | -0.00274331 |  0.0161848  |

## Score Spec
| spec            |   estimand | term                   |      n |   r2_within |        coef |         se |      pvalue |      ci_low |     ci_high |
|:----------------|-----------:|:-----------------------|-------:|------------:|------------:|-----------:|------------:|------------:|------------:|
| score_collapsed |        nan | post_X_treated         | 321184 |   0.0182391 |  0.00227767 | 0.00284032 | 0.433674    | -0.00371488 |  0.00827023 |
| score_collapsed |        nan | post_X_score           | 321184 |   0.0182391 | -0.056816   | 0.00457788 | 6.00093e-10 | -0.0664745  | -0.0471576  |
| score_collapsed |        nan | post_X_treated_X_score | 321184 |   0.0182391 |  0.00758612 | 0.00506113 | 0.15224     | -0.00309194 |  0.0182642  |

## Event-study Specs
| spec           | estimand   | term                                                              |         coef |         se |      pvalue |       ci_low |      ci_high |      n |   r2_within |
|:---------------|:-----------|:------------------------------------------------------------------|-------------:|-----------:|------------:|-------------:|-------------:|-------:|------------:|
| event_att      |            | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.000217695 | 0.00272705 | 0.937306    | -0.00553588  |  0.00597127  | 321184 | 0.000180302 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -6.3972e-05  | 0.00371108 | 0.986447    | -0.00789367  |  0.00776573  | 321184 | 0.000180302 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.000637519 | 0.00242298 | 0.795626    | -0.00574956  |  0.00447452  | 321184 | 0.000180302 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0026216   | 0.00194851 | 0.196156    | -0.00148939  |  0.00673259  | 321184 | 0.000180302 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.000205661 | 0.00217381 | 0.925732    | -0.00438067  |  0.00479199  | 321184 | 0.000180302 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00656805  | 0.00245943 | 0.0161358   |  0.0013791   |  0.011757    | 321184 | 0.000180302 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00179919  | 0.00192973 | 0.364207    | -0.00227218  |  0.00587056  | 321184 | 0.000180302 |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00130498  | 0.00205577 | 0.534017    | -0.00564227  |  0.00303231  | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.000183354 | 0.00258005 | 0.944174    | -0.00526007  |  0.00562678  | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0016303   | 0.00148172 | 0.286549    | -0.00149586  |  0.00475646  | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.000501284 | 0.00192025 | 0.797189    | -0.00355009  |  0.00455266  | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.000447551 | 0.00166848 | 0.791744    | -0.00307264  |  0.00396774  | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00316421  | 0.00217662 | 0.164235    | -0.00142806  |  0.00775647  | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00012099  | 0.00149848 | 0.93659     | -0.00304052  |  0.0032825   | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.00500733  | 0.00553192 | 0.378025    | -0.006664    |  0.0166787   | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             | -0.00178669  | 0.00610056 | 0.773164    | -0.0146577   |  0.0110844   | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.00777542  | 0.00580651 | 0.198174    | -0.0200261   |  0.00447525  | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.00646497  | 0.00433343 | 0.154054    | -0.00267777  |  0.0156077   | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.00223429  | 0.00459606 | 0.633082    | -0.0119311   |  0.00746256  | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.0108627   | 0.00617766 | 0.0966689   | -0.00217099  |  0.0238964   | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.00391458  | 0.00528697 | 0.469149    | -0.00723995  |  0.0150691   | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.00529345  | 0.00547224 | 0.346942    | -0.0168389   |  0.00625197  | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.0044973   | 0.00471631 | 0.353667    | -0.00545324  |  0.0144478   | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0231833   | 0.00611585 | 0.00146006  |  0.01028     |  0.0360866   | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0260961   | 0.00503205 | 7.43963e-05 | -0.0367128   | -0.0154794   | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0242329   | 0.00550658 | 0.000390583 | -0.0358508   | -0.012615    | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0323743   | 0.0044072  | 1.14297e-06 | -0.0416727   | -0.0230759   | 321184 | 0.0158694   |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0324197   | 0.00396172 | 2.67788e-07 | -0.0407782   | -0.0240612   | 321184 | 0.0158694   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00122509  | 0.00191792 | 0.531494    | -0.00527155  |  0.00282138  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.000310962 | 0.00234803 | 0.896195    | -0.00464294  |  0.00526486  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00113599  | 0.00134618 | 0.410463    | -0.0017042   |  0.00397619  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.000760541 | 0.00181591 | 0.680592    | -0.0030707   |  0.00459178  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.000530503 | 0.00166993 | 0.754596    | -0.00299274  |  0.00405374  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00328463  | 0.00207101 | 0.131162    | -0.00108481  |  0.00765407  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.000441403 | 0.00148202 | 0.769435    | -0.00268539  |  0.00356819  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.00983469  | 0.00949679 | 0.314905    | -0.0102018   |  0.0298712   | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.000710328 | 0.0125032  | 0.955357    | -0.0256691   |  0.0270897   | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.000850474 | 0.0102728  | 0.934986    | -0.0225242   |  0.0208232   | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.002921    | 0.00620418 | 0.64376     | -0.0101687   |  0.0160107   | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.00340808  | 0.00553867 | 0.54649     | -0.00827749  |  0.0150936   | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.015374    | 0.00808166 | 0.0742076   | -0.00167677  |  0.0324248   | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.00747051  | 0.00610316 | 0.237631    | -0.00540603  |  0.020347    | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.00460547  | 0.00586398 | 0.443038    | -0.0169774   |  0.00776645  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.00586166  | 0.00537396 | 0.290601    | -0.0054764   |  0.0171997   | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0256676   | 0.00622253 | 0.000707514 |  0.0125392   |  0.038796    | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0275874   | 0.00579232 | 0.000180528 | -0.0398082   | -0.0153667   | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0235287   | 0.0068566  | 0.00318288  | -0.0379949   | -0.00906252  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0328725   | 0.00552301 | 1.57673e-05 | -0.044525    | -0.0212199   | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0328235   | 0.00448001 | 1.18272e-06 | -0.0422755   | -0.0233715   | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_len              |  0.00134507  | 0.00169249 | 0.437726    | -0.00222577  |  0.00491591  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_len              |  0.00218679  | 0.00302789 | 0.47998     | -0.00420151  |  0.00857508  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_len              | -0.00224227  | 0.00195322 | 0.266872    | -0.0063632   |  0.00187865  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:treated_X_len               |  0.00277313  | 0.00123915 | 0.0389014   |  0.00015876  |  0.0053875   | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:treated_X_len               | -0.00130807  | 0.00097687 | 0.198188    | -0.00336909  |  0.000752948 | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:treated_X_len               | -0.00127638  | 0.00166607 | 0.454121    | -0.00479148  |  0.00223872  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:treated_X_len               |  0.00037899  | 0.00106502 | 0.726328    | -0.001868    |  0.00262598  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:disp_X_len                 | -0.003933    | 0.00466357 | 0.410745    | -0.0137723   |  0.00590627  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:disp_X_len                 | -0.0065043   | 0.00552481 | 0.2553      | -0.0181606   |  0.00515202  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:disp_X_len                 | -0.0100241   | 0.00532307 | 0.0769067   | -0.0212548   |  0.00120658  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:disp_X_len                  |  0.00716779  | 0.00496441 | 0.166962    | -0.0033062   |  0.0176418   | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:disp_X_len                  | -0.00123114  | 0.00642058 | 0.85021     | -0.0147774   |  0.0123151   | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:disp_X_len                  |  0.00376585  | 0.00542416 | 0.49689     | -0.00767812  |  0.0152098   | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:disp_X_len                  |  0.00458769  | 0.00349131 | 0.206292    | -0.00277834  |  0.0119537   | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:tXdXlen                    | -0.00564846  | 0.00581401 | 0.344908    | -0.017915    |  0.00661804  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:tXdXlen                    | -0.00195422  | 0.00666189 | 0.77281     | -0.0160096   |  0.0121011   | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:tXdXlen                    | -0.00143781  | 0.0055998  | 0.800445    | -0.0132524   |  0.0103767   | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:tXdXlen                     | -0.00214199  | 0.00342586 | 0.540115    | -0.00936992  |  0.00508594  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:tXdXlen                     | -0.00509052  | 0.00342197 | 0.155171    | -0.0123103   |  0.00212921  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:tXdXlen                     | -0.00644897  | 0.00512522 | 0.225298    | -0.0172622   |  0.00436429  | 321184 | 0.0180207   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:tXdXlen                     | -0.00720218  | 0.00417265 | 0.102467    | -0.0160057   |  0.00160135  | 321184 | 0.0180207   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  2.29874e-05 | 0.00281789 | 0.993586    | -0.00592224  |  0.00596822  | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.000325676 | 0.00357803 | 0.92854     | -0.00787465  |  0.0072233   | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00039927  | 0.00252012 | 0.875982    | -0.00571625  |  0.00491771  | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00212335  | 0.00214488 | 0.336076    | -0.00240196  |  0.00664866  | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.000290397 | 0.00190129 | 0.880404    | -0.00430177  |  0.00372098  | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00592337  | 0.00246528 | 0.0279722   |  0.00072209  |  0.0111247   | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.000930395 | 0.00176511 | 0.604932    | -0.00279365  |  0.00465444  | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.0102337   | 0.00842376 | 0.241025    | -0.0075389   |  0.0280063   | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.00115289  | 0.00809411 | 0.888411    | -0.0159242   |  0.01823     | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.00680765  | 0.00837844 | 0.427726    | -0.0244846   |  0.0108693   | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.0099851   | 0.00570834 | 0.0982842   | -0.00205845  |  0.0220286   | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.00100651  | 0.00687186 | 0.885275    | -0.0155049   |  0.0134919   | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.0188734   | 0.00868691 | 0.044239    |  0.000545644 |  0.0372012   | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.00753387  | 0.00789128 | 0.353105    | -0.00911527  |  0.024183    | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.00942803  | 0.0091098  | 0.315199    | -0.028648    |  0.00979197  | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.00394732  | 0.00794392 | 0.625626    | -0.0128129   |  0.0207075   | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0295799   | 0.00906098 | 0.00456646  |  0.0104629   |  0.0486969   | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0448489   | 0.00827838 | 4.61823e-05 | -0.0623148   | -0.0273831   | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0443395   | 0.00891214 | 0.000115422 | -0.0631425   | -0.0255365   | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.0576474   | 0.00681939 | 1.70927e-07 | -0.0720351   | -0.0432598   | 321184 | 0.0210658   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.0564218   | 0.00617775 | 5.74983e-08 | -0.0694557   | -0.0433879   | 321184 | 0.0210658   |

## Pre-trend Joint Tests
| spec           | test                                    |   n_restrictions |   statistic |     pvalue |      n |
|:---------------|:----------------------------------------|-----------------:|------------:|-----------:|-------:|
| event_att      | pretrend_att_joint_zero                 |                3 |   0.1909    | 0.979045   | 321184 |
| event_binary_B | pretrend_baseline_joint_zero            |                3 |   1.84946   | 0.604233   | 321184 |
| event_binary_B | pretrend_displacement_joint_zero        |                3 |   8.6259    | 0.0347013  | 321184 |
| event_binary_D | pretrend_length_displacement_joint_zero |                3 |   2.05572   | 0.560923   | 321184 |
| event_binary_D | pretrend_length_baseline_joint_zero     |                3 |  14.4286    | 0.00237621 | 321184 |
| event_score_C  | pretrend_score_baseline_joint_zero      |                3 |   0.0482416 | 0.997222   | 321184 |
| event_score_C  | pretrend_score_slope_joint_zero         |                3 |   7.79702   | 0.0503983  | 321184 |

## Matched-Sample Support
| treated   | match_cell                                                    |   blocked_available |   non_blocked_available |   retained_per_group |   common_support |   episodes_before |   episodes_after |   blocked_retained |   non_blocked_retained |   treated_retained |   control_retained |
|:----------|:--------------------------------------------------------------|--------------------:|------------------------:|---------------------:|-----------------:|------------------:|-----------------:|-------------------:|-----------------------:|-------------------:|-------------------:|
| 0         | 0|(20074.5, 30111.25]|(30111.25, 40148.0]|(0.999, 10037.75]   |                 591 |                    1349 |                  591 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(0.999, 10037.75]|(10037.75, 20074.5]   |                  87 |                     422 |                   87 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(30111.25, 40148.0]|(30111.25, 40148.0]|(0.999, 10037.75]   |                3978 |                    1024 |                 1024 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(0.999, 10037.75]|(20074.5, 30111.25]   |                 119 |                    1134 |                  119 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(30111.25, 40148.0]|(10037.75, 20074.5] |                 115 |                     271 |                  115 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(0.999, 10037.75]|(20074.5, 30111.25]   |                 155 |                     582 |                  155 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(0.999, 10037.75]|(10037.75, 20074.5]   |                 551 |                     504 |                  504 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(0.999, 10037.75]|(0.999, 10037.75]|(20074.5, 30111.25]     |                   1 |                     759 |                    1 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(0.999, 10037.75]|(0.999, 10037.75]|(30111.25, 40148.0]     |                   4 |                    3095 |                    4 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(30111.25, 40148.0]|(0.999, 10037.75]   |                  29 |                     353 |                   29 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(30111.25, 40148.0]|(0.999, 10037.75]|(10037.75, 20074.5]   |                 447 |                     235 |                  235 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(30111.25, 40148.0]|(30111.25, 40148.0]|(10037.75, 20074.5] |                 337 |                     124 |                  124 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(30111.25, 40148.0]|(10037.75, 20074.5] |                   7 |                      92 |                    7 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(30111.25, 40148.0]|(0.999, 10037.75]|(20074.5, 30111.25]   |                  43 |                     140 |                   43 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(30111.25, 40148.0]|(20074.5, 30111.25]|(0.999, 10037.75]   |                 166 |                      56 |                   56 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(20074.5, 30111.25]|(0.999, 10037.75]   |                 167 |                     214 |                  167 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(20074.5, 30111.25]|(10037.75, 20074.5] |                 451 |                     725 |                  451 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(20074.5, 30111.25]|(0.999, 10037.75]   |                  34 |                     191 |                   34 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(30111.25, 40148.0]|(20074.5, 30111.25]|(10037.75, 20074.5] |                 369 |                     227 |                  227 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(20074.5, 30111.25]|(10037.75, 20074.5] |                 115 |                     469 |                  115 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(0.999, 10037.75]|(30111.25, 40148.0]   |                   0 |                       2 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(0.999, 10037.75]|(30111.25, 40148.0]   |                   0 |                      27 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(0.999, 10037.75]|(10037.75, 20074.5]|(20074.5, 30111.25]   |                   0 |                    1655 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(0.999, 10037.75]|(10037.75, 20074.5]|(30111.25, 40148.0]   |                   0 |                    2664 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(10037.75, 20074.5]|(10037.75, 20074.5] |                 249 |                    1120 |                  249 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(30111.25, 40148.0]|(10037.75, 20074.5]|(20074.5, 30111.25] |                   3 |                      57 |                    3 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(10037.75, 20074.5]|(10037.75, 20074.5] |                  25 |                     323 |                   25 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(10037.75, 20074.5]|(20074.5, 30111.25] |                   6 |                     459 |                    6 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(30111.25, 40148.0]|(10037.75, 20074.5]|(10037.75, 20074.5] |                 446 |                     450 |                  446 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(10037.75, 20074.5]|(20074.5, 30111.25] |                  17 |                     418 |                   17 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(30111.25, 40148.0]|(10037.75, 20074.5]|(0.999, 10037.75]   |                  37 |                      11 |                   11 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(10037.75, 20074.5]|(0.999, 10037.75]   |                  12 |                      23 |                   12 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(10037.75, 20074.5]|(30111.25, 40148.0] |                   0 |                      74 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(20074.5, 30111.25]|(20074.5, 30111.25] |                  98 |                    1743 |                   98 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(10037.75, 20074.5]|(20074.5, 30111.25]|(30111.25, 40148.0] |                  13 |                    2339 |                   13 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(20074.5, 30111.25]|(20074.5, 30111.25] |                 114 |                     507 |                  114 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(30111.25, 40148.0]|(20074.5, 30111.25]|(20074.5, 30111.25] |                  38 |                      95 |                   38 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 0         | 0|(20074.5, 30111.25]|(20074.5, 30111.25]|(30111.25, 40148.0] |                   0 |                       1 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(0.999, 10037.75]|(20074.5, 30111.25]   |                  41 |                     121 |                   41 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(0.999, 10037.75]|(0.999, 10037.75]|(30111.25, 40148.0]     |                   3 |                     728 |                    3 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(30111.25, 40148.0]|(0.999, 10037.75]|(10037.75, 20074.5]   |                  81 |                      30 |                   30 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(30111.25, 40148.0]|(10037.75, 20074.5] |                  41 |                      56 |                   41 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(30111.25, 40148.0]|(0.999, 10037.75]   |                 142 |                     280 |                  142 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(0.999, 10037.75]|(20074.5, 30111.25]   |                  45 |                     251 |                   45 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(0.999, 10037.75]|(10037.75, 20074.5]   |                  93 |                      88 |                   88 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(30111.25, 40148.0]|(30111.25, 40148.0]|(0.999, 10037.75]   |                 806 |                     203 |                  203 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(30111.25, 40148.0]|(10037.75, 20074.5] |                   0 |                      12 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(0.999, 10037.75]|(10037.75, 20074.5]   |                  24 |                      75 |                   24 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(30111.25, 40148.0]|(30111.25, 40148.0]|(10037.75, 20074.5] |                 111 |                      25 |                   25 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(0.999, 10037.75]|(0.999, 10037.75]|(20074.5, 30111.25]     |                   0 |                     114 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(30111.25, 40148.0]|(0.999, 10037.75]   |                  14 |                      77 |                   14 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(30111.25, 40148.0]|(0.999, 10037.75]|(20074.5, 30111.25]   |                   7 |                      19 |                    7 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(20074.5, 30111.25]|(10037.75, 20074.5] |                  36 |                     101 |                   36 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(20074.5, 30111.25]|(10037.75, 20074.5] |                 134 |                     186 |                  134 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(30111.25, 40148.0]|(20074.5, 30111.25]|(10037.75, 20074.5] |                 112 |                      47 |                   47 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(20074.5, 30111.25]|(0.999, 10037.75]   |                  67 |                      58 |                   58 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(30111.25, 40148.0]|(20074.5, 30111.25]|(0.999, 10037.75]   |                  37 |                      16 |                   16 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(20074.5, 30111.25]|(0.999, 10037.75]   |                  20 |                      53 |                   20 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(0.999, 10037.75]|(30111.25, 40148.0]   |                   0 |                       9 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(0.999, 10037.75]|(30111.25, 40148.0]   |                   0 |                       1 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(10037.75, 20074.5]|(10037.75, 20074.5] |                   0 |                      85 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(0.999, 10037.75]|(10037.75, 20074.5]|(30111.25, 40148.0]   |                   0 |                     543 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(0.999, 10037.75]|(10037.75, 20074.5]|(20074.5, 30111.25]   |                   1 |                     470 |                    1 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(10037.75, 20074.5]|(20074.5, 30111.25] |                   3 |                     147 |                    3 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(10037.75, 20074.5]|(10037.75, 20074.5] |                  48 |                     286 |                   48 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(30111.25, 40148.0]|(10037.75, 20074.5]|(10037.75, 20074.5] |                  85 |                     120 |                   85 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(10037.75, 20074.5]|(20074.5, 30111.25] |                   0 |                     120 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(30111.25, 40148.0]|(10037.75, 20074.5]|(20074.5, 30111.25] |                   0 |                       9 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(30111.25, 40148.0]|(10037.75, 20074.5]|(0.999, 10037.75]   |                   9 |                       5 |                    5 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(10037.75, 20074.5]|(0.999, 10037.75]   |                   4 |                      11 |                    4 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(10037.75, 20074.5]|(30111.25, 40148.0] |                   0 |                      42 |                    0 |                0 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(20074.5, 30111.25]|(20074.5, 30111.25] |                  36 |                     356 |                   36 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(30111.25, 40148.0]|(20074.5, 30111.25]|(20074.5, 30111.25] |                  10 |                      22 |                   10 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(20074.5, 30111.25]|(20074.5, 30111.25]|(20074.5, 30111.25] |                  29 |                      93 |                   29 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| 1         | 1|(10037.75, 20074.5]|(20074.5, 30111.25]|(30111.25, 40148.0] |                   2 |                     490 |                    2 |                1 |               nan |              nan |                nan |                    nan |                nan |                nan |
| all       | __overall__                                                   |               10865 |                   29283 |                 6317 |                1 |             40148 |            12634 |               6317 |                   6317 |               2394 |              10240 |

## Matched Binary Specs
| spec                           | estimand                               | term                  |      n |   r2_within |        coef |         se |    pvalue |      ci_low |    ci_high |
|:-------------------------------|:---------------------------------------|:----------------------|-------:|------------:|------------:|-----------:|----------:|------------:|-----------:|
| binary_collapsed               | low_predicted_incidence_effect_delta_b | post_X_treated        | 101072 | 0.000246829 |  0.00686845 | 0.00392255 | 0.0979649 | -0.00140741 | 0.0151443  |
| binary_collapsed               | common_high_minus_low_post_shift       | post_X_disp           | 101072 | 0.000246829 | -0.00177021 | 0.00203798 | 0.397158  | -0.00606998 | 0.00252956 |
| binary_collapsed               | high_minus_low_ddd                     | post_X_treated_X_disp | 101072 | 0.000246829 | -0.00405668 | 0.00273351 | 0.156099  | -0.00982388 | 0.00171052 |
| binary_collapsed_group_effects | low_predicted_incidence_effect         | post_X_treated_X_low  | 101072 | 0.000246829 |  0.00686845 | 0.00392255 | 0.097965  | -0.00140741 | 0.0151443  |
| binary_collapsed_group_effects | high_predicted_incidence_effect        | post_X_treated_X_high | 101072 | 0.000246829 |  0.00281177 | 0.00508539 | 0.587522  | -0.00791746 | 0.013541   |

## Matched Event-study Specs
| spec           | estimand   | term                                                              |         coef |         se |      pvalue |       ci_low |      ci_high |      n |   r2_within |
|:---------------|:-----------|:------------------------------------------------------------------|-------------:|-----------:|------------:|-------------:|-------------:|-------:|------------:|
| event_att      |            | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00935193  | 0.00413157 | 0.0369769   | -0.0180688   | -0.000635087 | 101072 | 0.000452776 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00644432  | 0.00627    | 0.318446    | -0.0196729   |  0.00678422  | 101072 | 0.000452776 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00648525  | 0.00496302 | 0.208711    | -0.0169563   |  0.0039858   | 101072 | 0.000452776 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00138297  | 0.00319833 | 0.670884    | -0.00536491  |  0.00813085  | 101072 | 0.000452776 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00490891  | 0.00308773 | 0.1303      | -0.0114234   |  0.00160562  | 101072 | 0.000452776 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00370095  | 0.00328347 | 0.275339    | -0.00322656  |  0.0106285   | 101072 | 0.000452776 |
| event_att      |            | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00245698  | 0.00290454 | 0.409353    | -0.00858503  |  0.00367107  | 101072 | 0.000452776 |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0127294   | 0.00367083 | 0.00294289  | -0.0204742   | -0.00498465  | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0105751   | 0.00658495 | 0.126699    | -0.0244681   |  0.00331793  | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00287266  | 0.00370355 | 0.448612    | -0.0106865   |  0.00494115  | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.000310511 | 0.0037497  | 0.93497     | -0.00822168  |  0.00760066  | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.000375204 | 0.00329256 | 0.910608    | -0.00732189  |  0.00657149  | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00284838  | 0.00428659 | 0.515292    | -0.00619554  |  0.0118923   | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.000544116 | 0.00452842 | 0.905768    | -0.0100983   |  0.00901002  | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.00611149  | 0.00477408 | 0.217689    | -0.00396094  |  0.0161839   | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0072303   | 0.0078296  | 0.368691    | -0.00928872  |  0.0237493   | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.00684784  | 0.00562582 | 0.24015     | -0.0187173   |  0.0050216   | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.00311422  | 0.00400753 | 0.447783    | -0.00534092  |  0.0115694   | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.00931672  | 0.00432067 | 0.0456738   | -0.0184325   | -0.000200897 | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.00138588  | 0.00552384 | 0.804906    | -0.0102684   |  0.0130402   | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.00429295  | 0.00579767 | 0.469124    | -0.016525    |  0.00793906  | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.00253875  | 0.00461744 | 0.589596    | -0.0122807   |  0.00720321  | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.00314328  | 0.00544986 | 0.571659    | -0.00835493  |  0.0146415   | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0271364   | 0.00760839 | 0.00237473  |  0.0110841   |  0.0431887   | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  0.0048791   | 0.0032419  | 0.150674    | -0.00196071  |  0.0117189   | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.00699755  | 0.00445037 | 0.134294    | -0.00239191  |  0.016387    | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.00397635  | 0.0037454  | 0.30324     | -0.00392576  |  0.0118784   | 101072 | 0.00323746  |
| event_binary_B |            | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.0048889   | 0.00336195 | 0.164108    | -0.00220419  |  0.011982    | 101072 | 0.00323746  |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0131939   | 0.00319099 | 0.000692707 | -0.0199263   | -0.00646148  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.011122    | 0.00644517 | 0.102543    | -0.0247201   |  0.00247616  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00375532  | 0.00377287 | 0.333524    | -0.0117154   |  0.00420474  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.000378548 | 0.00326196 | 0.908973    | -0.00726068  |  0.00650359  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.000355684 | 0.00314162 | 0.911185    | -0.00698393  |  0.00627256  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00279625  | 0.00438598 | 0.532266    | -0.00645737  |  0.0120499   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.000301044 | 0.00468456 | 0.94951     | -0.0101846   |  0.00958251  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0109602   | 0.00856781 | 0.218       | -0.00711624  |  0.0290367   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.01202     | 0.0132261  | 0.376156    | -0.0158846   |  0.0399246   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.000349801 | 0.00916263 | 0.969991    | -0.0196813   |  0.0189817   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.00125792  | 0.00492915 | 0.80163     | -0.00914166  |  0.0116575   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.0070529   | 0.00680865 | 0.314772    | -0.0214179   |  0.00731208  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.00685839  | 0.00801854 | 0.40427     | -0.0100593   |  0.023776    | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.00199036  | 0.00802266 | 0.807035    | -0.0189167   |  0.014936    | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.000452187 | 0.00388156 | 0.908625    | -0.00773719  |  0.00864157  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.00748663  | 0.00409963 | 0.0854399   | -0.00116283  |  0.0161361   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0342377   | 0.00405118 | 1.71535e-07 |  0.0256905   |  0.0427849   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  0.00655904  | 0.00334939 | 0.066815    | -0.000507562 |  0.0136256   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.0119785   | 0.00340588 | 0.00264473  |  0.00479271  |  0.0191643   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.00762086  | 0.00294343 | 0.0191053   |  0.00141077  |  0.013831    | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.00810923  | 0.0028797  | 0.0118976   |  0.0020336   |  0.0141849   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_len              |  0.00410753  | 0.00330329 | 0.230571    | -0.00286179  |  0.0110769   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_len              |  0.00607146  | 0.0073865  | 0.422475    | -0.00951269  |  0.0216556   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_len              | -0.000212649 | 0.00376999 | 0.955676    | -0.00816662  |  0.00774133  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:treated_X_len               |  0.00876033  | 0.00298792 | 0.00931039  |  0.00245637  |  0.0150643   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:treated_X_len               | -0.00300547  | 0.0025589  | 0.25638     | -0.00840427  |  0.00239334  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:treated_X_len               | -0.00178706  | 0.00315717 | 0.578769    | -0.0084481   |  0.00487399  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:treated_X_len               |  0.00139422  | 0.00348883 | 0.69441     | -0.00596657  |  0.00875501  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:disp_X_len                 | -0.0103077   | 0.00403697 | 0.0205686   | -0.018825    | -0.00179043  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:disp_X_len                 | -0.0148983   | 0.0044897  | 0.00406583  | -0.0243708   | -0.00542592  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:disp_X_len                 | -0.0200347   | 0.00488222 | 0.00074092  | -0.0303353   | -0.00973411  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:disp_X_len                  | -0.00338146  | 0.00385496 | 0.392622    | -0.0115147   |  0.0047518   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:disp_X_len                  | -0.0132145   | 0.00472629 | 0.0124106   | -0.0231861   | -0.0032429   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:disp_X_len                  | -0.00999061  | 0.00497627 | 0.0608466   | -0.0204896   |  0.000508408 | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:disp_X_len                  | -0.006224    | 0.00320416 | 0.0688334   | -0.0129842   |  0.000536187 | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-4]:tXdXlen                    | -0.00461845  | 0.00486758 | 0.356007    | -0.0148881   |  0.00565124  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-3]:tXdXlen                    | -0.00408203  | 0.00828768 | 0.628637    | -0.0215675   |  0.0134034   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[-2]:tXdXlen                    |  0.000921891 | 0.00564686 | 0.872241    | -0.0109919   |  0.0128357   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[1]:tXdXlen                     | -0.00460669  | 0.00379319 | 0.241172    | -0.0126096   |  0.00339624  | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[2]:tXdXlen                     |  0.00689127  | 0.00587231 | 0.256768    | -0.00549823  |  0.0192808   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[3]:tXdXlen                     |  0.000100967 | 0.00526598 | 0.984926    | -0.0110093   |  0.0112112   | 101072 | 0.0067064   |
| event_binary_D |            | C(rel_t, contr.treatment(base=-1))[4]:tXdXlen                     | -0.000684278 | 0.00537449 | 0.900181    | -0.0120234   |  0.0106549   | 101072 | 0.0067064   |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0129652   | 0.00384328 | 0.00360905  | -0.0210738   | -0.0048566   | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0102561   | 0.00633225 | 0.123707    | -0.023616    |  0.00310381  | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00383419  | 0.00392406 | 0.342221    | -0.0121132   |  0.00444484  | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0009169   | 0.0034292  | 0.792393    | -0.00631808  |  0.00815188  | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00171958  | 0.00263329 | 0.522481    | -0.00727533  |  0.00383618  | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00272115  | 0.0035825  | 0.457917    | -0.00483725  |  0.0102796   | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00089357  | 0.00403073 | 0.827197    | -0.00939766  |  0.00761052  | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.0163736   | 0.010679   | 0.143614    | -0.00615718  |  0.0389044   | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.0157991   | 0.0136855  | 0.264292    | -0.0130749   |  0.044673    | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.0136282   | 0.0118554  | 0.266251    | -0.0386409   |  0.0113845   | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -9.66483e-05 | 0.00822947 | 0.990766    | -0.0174593   |  0.017266    | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.0194016   | 0.00826934 | 0.0313482   | -0.0368483   | -0.00195477  | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.00215162  | 0.0106988  | 0.843       | -0.0204209   |  0.0247241   | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             | -0.0123027   | 0.0122797  | 0.330453    | -0.0382105   |  0.0136052   | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.0176961   | 0.00969209 | 0.0854946   | -0.0381446   |  0.00275248  | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered | -0.00844906  | 0.00958416 | 0.390307    | -0.0286699   |  0.0117718   | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.05106     | 0.0149867  | 0.00335642  |  0.0194408   |  0.0826793   | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.00630824  | 0.00843824 | 0.464931    | -0.0241114   |  0.0114949   | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.00577647  | 0.0103675  | 0.584674    | -0.0276501   |  0.0160971   | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.0137346   | 0.00819169 | 0.1119      | -0.0310176   |  0.0035483   | 101072 | 0.00551063  |
| event_score_C  |            | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.0112452   | 0.00928647 | 0.242493    | -0.0308379   |  0.00834759  | 101072 | 0.00551063  |

## Matched Pre-trend Joint Tests
| spec           | test                                    |   n_restrictions |   statistic |     pvalue |      n |
|:---------------|:----------------------------------------|-----------------:|------------:|-----------:|-------:|
| event_att      | pretrend_att_joint_zero                 |                3 |     5.40691 | 0.144314   | 101072 |
| event_binary_B | pretrend_baseline_joint_zero            |                3 |    12.1718  | 0.00681724 | 101072 |
| event_binary_B | pretrend_displacement_joint_zero        |                3 |     7.0896  | 0.0690961  | 101072 |
| event_binary_D | pretrend_length_displacement_joint_zero |                3 |     4.89638 | 0.179544   | 101072 |
| event_binary_D | pretrend_length_baseline_joint_zero     |                3 |    10.1068  | 0.0176796  | 101072 |
| event_score_C  | pretrend_score_baseline_joint_zero      |                3 |    12.95    | 0.00474601 | 101072 |
| event_score_C  | pretrend_score_slope_joint_zero         |                3 |    12.3     | 0.00642292 | 101072 |

## Blocked Gap Event Study
| spec              | estimand   | term                                                       |         coef |         se |     pvalue |       ci_low |    ci_high |      n |   r2_within |
|:------------------|:-----------|:-----------------------------------------------------------|-------------:|-----------:|-----------:|-------------:|-----------:|-------:|------------:|
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[-4]:blocked_treated_gap | -0.00648854  | 0.0079728  | 0.426993   | -0.0233097   | 0.0103326  | 101072 |  0.00288848 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[-3]:blocked_treated_gap |  0.00201064  | 0.00924376 | 0.830398   | -0.017492    | 0.0215133  | 101072 |  0.00288848 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[-2]:blocked_treated_gap |  0.0179889   | 0.00869769 | 0.0541816  | -0.000361591 | 0.0363395  | 101072 |  0.00288848 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[1]:blocked_treated_gap  |  0.00772338  | 0.00368281 | 0.0512424  | -4.66719e-05 | 0.0154934  | 101072 |  0.00288848 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[2]:blocked_treated_gap  | -0.00264599  | 0.00521757 | 0.618578   | -0.0136541   | 0.00836213 | 101072 |  0.00288848 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[3]:blocked_treated_gap  |  0.00762327  | 0.00573477 | 0.201312   | -0.00447604  | 0.0197226  | 101072 |  0.00288848 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[4]:blocked_treated_gap  |  0.000139009 | 0.0050177  | 0.978221   | -0.0104474   | 0.0107254  | 101072 |  0.00288848 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[-4]:blocked_control_gap |  2.57408e-07 | 0.00440405 | 0.999954   | -0.00929147  | 0.00929198 | 101072 |  0.00288848 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[-3]:blocked_control_gap |  0.00519477  | 0.00595028 | 0.394811   | -0.00735921  | 0.0177488  | 101072 |  0.00288848 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[-2]:blocked_control_gap |  0.0276831   | 0.00756182 | 0.00193533 |  0.0117291   | 0.0436372  | 101072 |  0.00288848 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[1]:blocked_control_gap  |  0.00492795  | 0.00332588 | 0.15672    | -0.00208905  | 0.0119449  | 101072 |  0.00288848 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[2]:blocked_control_gap  |  0.00705554  | 0.00445436 | 0.131627   | -0.00234234  | 0.0164534  | 101072 |  0.00288848 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[3]:blocked_control_gap  |  0.00341142  | 0.00390574 | 0.394595   | -0.00482897  | 0.0116518  | 101072 |  0.00288848 |
| event_blocked_gap |            | C(rel_t, contr.treatment(base=-1))[4]:blocked_control_gap  |  0.00498371  | 0.00327775 | 0.146775   | -0.00193175  | 0.0118992  | 101072 |  0.00288848 |

## Pre-period Bias Equality Tests
| spec                   | test                 | term                             |         coef |          se |      pvalue |      n | sample_scope   |
|:-----------------------|:---------------------|:---------------------------------|-------------:|------------:|------------:|-------:|:---------------|
| pretrend_bias_equality | pretrend_bias_linear | non_blocked_treated_control_bias |  0.00083553  | 0.000712271 | 0.240775    | 160592 | full           |
| pretrend_bias_equality | pretrend_bias_linear | bias_equality_difference         | -0.00125276  | 0.00172428  | 0.467507    | 160592 | full           |
| pretrend_bias_equality | pretrend_bias_linear | blocked_treated_control_bias     | -0.000417229 | 0.00193936  | 0.82966     | 160592 | full           |
| pretrend_bias_equality | pretrend_bias_linear | non_blocked_treated_control_bias |  0.00547976  | 0.00125077  | 1.18076e-05 |  50536 | matched        |
| pretrend_bias_equality | pretrend_bias_linear | bias_equality_difference         | -0.0021888   | 0.00174276  | 0.209138    |  50536 | matched        |
| pretrend_bias_equality | pretrend_bias_linear | blocked_treated_control_bias     |  0.00329096  | 0.00198752  | 0.0977592   |  50536 | matched        |