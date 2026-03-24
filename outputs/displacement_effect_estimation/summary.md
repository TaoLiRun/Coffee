# Displacement Effect Estimation Summary

- Sample rows: 358,864
- Unique members: 44,858
- Unique closures: 22
- Event FE units: 44,858
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]

## Binary Specs
| spec             | term                  |      n |   r2_within |        coef |          se |   pvalue |
|:-----------------|:----------------------|-------:|------------:|------------:|------------:|---------:|
| binary_collapsed | post_X_treated        | 358864 |   0.0119923 |  0.00102916 | 0.000647202 | 0.111804 |
| binary_collapsed | post_X_disp           | 358864 |   0.0119923 | -0.0330276  | 0.00106797  | 0        |
| binary_collapsed | post_X_treated_X_disp | 358864 |   0.0119923 |  0.00369003 | 0.00241001  | 0.125745 |

## Score Spec
| spec            | term                   |      n |   r2_within |        coef |          se |    pvalue |
|:----------------|:-----------------------|-------:|------------:|------------:|------------:|----------:|
| score_collapsed | post_X_treated         | 358864 |   0.0177812 |  0.00189755 | 0.000788346 | 0.0160879 |
| score_collapsed | post_X_score           | 358864 |   0.0177812 | -0.0568327  | 0.00159369  | 0         |
| score_collapsed | post_X_treated_X_score | 358864 |   0.0177812 |  0.00603146 | 0.00359012  | 0.0929611 |

## Event-study Specs
| spec           | term                                                              |         coef |          se |      pvalue |      n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|------------:|------------:|-------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00043436  | 0.00121332  | 0.72035     | 358864 | 0.000152819 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.000282038 | 0.00116449  | 0.808628    | 358864 | 0.000152819 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.000313581 | 0.00102194  | 0.75896     | 358864 | 0.000152819 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00254148  | 0.00103261  | 0.0138506   | 358864 | 0.000152819 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.000163434 | 0.00111593  | 0.883563    | 358864 | 0.000152819 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00623115  | 0.00116723  | 9.42259e-08 | 358864 | 0.000152819 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00175002  | 0.00115576  | 0.129987    | 358864 | 0.000152819 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00106328  | 0.00101879  | 0.296643    | 358864 | 0.0153194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -2.08696e-05 | 0.000942487 | 0.982334    | 358864 | 0.0153194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00186806  | 0.000811462 | 0.0213347   | 358864 | 0.0153194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.000814165 | 0.000814017 | 0.317228    | 358864 | 0.0153194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.000564685 | 0.000927161 | 0.542496    | 358864 | 0.0153194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00347091  | 0.000960723 | 0.000303223 | 358864 | 0.0153194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.000253881 | 0.000930037 | 0.78487     | 358864 | 0.0153194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.00481439  | 0.0036431   | 0.186339    | 358864 | 0.0153194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             | -0.00208811  | 0.00353974  | 0.555257    | 358864 | 0.0153194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.00687305  | 0.00311026  | 0.0271242   | 358864 | 0.0153194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.00440355  | 0.00314199  | 0.161067    | 358864 | 0.0153194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.00340774  | 0.00332302  | 0.305135    | 358864 | 0.0153194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.00759547  | 0.00349289  | 0.0296691   | 358864 | 0.0153194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.00236541  | 0.0034865   | 0.497491    | 358864 | 0.0153194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.0129576   | 0.0016821   | 1.35447e-14 | 358864 | 0.0153194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                | -0.00123829  | 0.00161622  | 0.443581    | 358864 | 0.0153194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0196485   | 0.00145189  | 0           | 358864 | 0.0153194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0283337   | 0.0014329   | 0           | 358864 | 0.0153194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0269124   | 0.00155991  | 0           | 358864 | 0.0153194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0363833   | 0.00155484  | 0           | 358864 | 0.0153194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.034914    | 0.00161758  | 0           | 358864 | 0.0153194   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.000973486 | 0.0010037   | 0.332103    | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.000229965 | 0.000930238 | 0.804746    | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00137549  | 0.000793415 | 0.0829904   | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00113205  | 0.000805225 | 0.159767    | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.000611841 | 0.000910229 | 0.50147     | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00363519  | 0.000945963 | 0.000121782 | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.000496946 | 0.00091389  | 0.586603    | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.00784042  | 0.00492392  | 0.111321    | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             | -0.000797741 | 0.0049692   | 0.872459    | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.000596989 | 0.00425501  | 0.888421    | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.00234512  | 0.0042377   | 0.579996    | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -2.44972e-05 | 0.00459863  | 0.99575     | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.00938061  | 0.00475549  | 0.0485489   | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.00376653  | 0.00462782  | 0.415713    | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.01321     | 0.00182944  | 5.24913e-13 | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                | -0.00014993  | 0.0017879   | 0.93317     | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0220626   | 0.00162711  | 0           | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0301666   | 0.00158607  | 0           | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0264337   | 0.00174249  | 0           | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0376781   | 0.00171243  | 0           | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0355693   | 0.0017533   | 0           | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_len              |  0.000333596 | 0.000860765 | 0.698346    | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_len              |  0.00171588  | 0.00079761  | 0.0314601   | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_len              | -0.00225966  | 0.000673691 | 0.000796745 | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_len               |  0.00216934  | 0.000658693 | 0.000990623 | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_len               | -0.00207201  | 0.000742747 | 0.00527873  | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated_X_len               | -0.00107058  | 0.000749304 | 0.153078    | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated_X_len               | -0.000883769 | 0.000794415 | 0.265938    | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:disp_X_len                 | -0.000219682 | 0.00154372  | 0.886838    | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:disp_X_len                 | -0.00523695  | 0.00149384  | 0.000455839 | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_X_len                 | -0.00940745  | 0.0013016   | 4.996e-13   | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_X_len                  |  0.00781161  | 0.00130943  | 2.45483e-09 | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_X_len                  | -0.00018861  | 0.00143014  | 0.895078    | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:disp_X_len                  |  0.00679771  | 0.00146811  | 3.66285e-06 | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:disp_X_len                  |  0.004764    | 0.00150433  | 0.00154204  | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:tXdXlen                    | -0.00408238  | 0.00337965  | 0.22708     | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:tXdXlen                    | -0.000347146 | 0.00336792  | 0.917904    | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:tXdXlen                    | -0.000605405 | 0.00284881  | 0.831709    | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:tXdXlen                     |  0.00243276  | 0.00290568  | 0.40246     | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:tXdXlen                     | -0.00145782  | 0.00314997  | 0.643506    | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:tXdXlen                     | -0.00436537  | 0.00329975  | 0.185862    | 358864 | 0.0175611   |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:tXdXlen                     | -0.00285677  | 0.00321657  | 0.374469    | 358864 | 0.0175611   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.000303456 | 0.00121841  | 0.803317    | 358864 | 0.0211446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.000589993 | 0.00116947  | 0.613915    | 358864 | 0.0211446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  4.03556e-05 | 0.00102072  | 0.968463    | 358864 | 0.0211446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00194703  | 0.00101981  | 0.0562418   | 358864 | 0.0211446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.000455222 | 0.00110273  | 0.679745    | 358864 | 0.0211446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00544792  | 0.00115585  | 2.44413e-06 | 358864 | 0.0211446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.000713717 | 0.00114267  | 0.532234    | 358864 | 0.0211446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.0106225   | 0.00521905  | 0.0418233   | 358864 | 0.0211446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.00124497  | 0.00496696  | 0.802086    | 358864 | 0.0211446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.00555853  | 0.00441741  | 0.208281    | 358864 | 0.0211446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.00971324  | 0.00458417  | 0.0341074   | 358864 | 0.0211446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.00179558  | 0.00486502  | 0.71207     | 358864 | 0.0211446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.0156711   | 0.00515864  | 0.00238415  | 358864 | 0.0211446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.00735132  | 0.00515485  | 0.153847    | 358864 | 0.0211446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.01899     | 0.00247196  | 1.59872e-14 | 358864 | 0.0211446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered | -0.000804731 | 0.00236565  | 0.733728    | 358864 | 0.0211446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.02622     | 0.00211525  | 0           | 358864 | 0.0211446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0489431   | 0.00212872  | 0           | 358864 | 0.0211446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0478352   | 0.00231284  | 0           | 358864 | 0.0211446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.0628055   | 0.00230442  | 0           | 358864 | 0.0211446   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.0611901   | 0.00242451  | 0           | 358864 | 0.0211446   |

## Pre-trend Joint Tests
| spec           | test                                    |   n_restrictions |   statistic |     pvalue |      n |
|:---------------|:----------------------------------------|-----------------:|------------:|-----------:|-------:|
| event_att      | pretrend_att_joint_zero                 |                3 |    0.552381 | 0.907242   | 358864 |
| event_binary_B | pretrend_baseline_joint_zero            |                3 |    8.63176  | 0.0346095  | 358864 |
| event_binary_B | pretrend_displacement_joint_zero        |                3 |   13.6844   | 0.00336771 | 358864 |
| event_binary_D | pretrend_length_displacement_joint_zero |                3 |    2.34558  | 0.503846   | 358864 |
| event_binary_D | pretrend_length_baseline_joint_zero     |                3 |   27.7288   | 4.1407e-06 | 358864 |
| event_score_C  | pretrend_score_baseline_joint_zero      |                3 |    0.781557 | 0.853873   | 358864 |
| event_score_C  | pretrend_score_slope_joint_zero         |                3 |   12.3346   | 0.00632056 | 358864 |