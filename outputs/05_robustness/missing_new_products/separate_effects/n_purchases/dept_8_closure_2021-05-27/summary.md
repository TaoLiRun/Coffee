# Displacement Effect Estimation Summary

- Sample rows: 5,392
- Unique members: 674
- Unique closures: 1
- Event FE units: 674
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_8_closure_2021-05-27`
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Length-heterogeneity event-study spec skipped: true
- Model type: DDD


## Binary Specs
| spec             | term                  |    n |   r2_within |         coef |         se |     pvalue |
|:-----------------|:----------------------|-----:|------------:|-------------:|-----------:|-----------:|
| binary_collapsed | post_X_treated        | 5392 |  0.00776449 | -0.000880802 | 0.00604256 | 0.884149   |
| binary_collapsed | post_X_disp           | 5392 |  0.00776449 | -0.0271308   | 0.00882556 | 0.00219665 |
| binary_collapsed | post_X_treated_X_disp | 5392 |  0.00776449 |  0.000105608 | 0.0211515  | 0.996018   |

## Score Spec
| spec            | term                   |    n |   r2_within |         coef |         se |      pvalue |
|:----------------|:-----------------------|-----:|------------:|-------------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 5392 |   0.0122169 | -0.000713733 | 0.00673459 | 0.91563     |
| score_collapsed | post_X_score           | 5392 |   0.0122169 | -0.043477    | 0.01255    | 0.000565332 |
| score_collapsed | post_X_treated_X_score | 5392 |   0.0122169 | -0.00599794  | 0.0308568  | 0.845937    |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00624831  | 0.011129   | 0.574682    | 5392 |  0.00126502 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.0152971   | 0.0115393  | 0.185404    | 5392 |  0.00126502 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0117018   | 0.00891342 | 0.189688    | 5392 |  0.00126502 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  2.45919e-05 | 0.00926422 | 0.997883    | 5392 |  0.00126502 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00218179  | 0.0100493  | 0.82819     | 5392 |  0.00126502 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0136869   | 0.0118329  | 0.247813    | 5392 |  0.00126502 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0111283   | 0.0109105  | 0.30811     | 5392 |  0.00126502 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00574895  | 0.00970051 | 0.553619    | 5392 |  0.0296263  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.0172996   | 0.0116552  | 0.138203    | 5392 |  0.0296263  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00405063  | 0.00740514 | 0.584558    | 5392 |  0.0296263  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.000137131 | 0.00683383 | 0.983996    | 5392 |  0.0296263  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00162447  | 0.00694454 | 0.815117    | 5392 |  0.0296263  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.015865    | 0.011418   | 0.165149    | 5392 |  0.0296263  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00919831  | 0.00733816 | 0.210462    | 5392 |  0.0296263  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0127066   | 0.0280047  | 0.650169    | 5392 |  0.0296263  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             | -0.00383307  | 0.0281391  | 0.891689    | 5392 |  0.0296263  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0219283   | 0.0232235  | 0.345392    | 5392 |  0.0296263  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.00492151  | 0.0248826  | 0.84327     | 5392 |  0.0296263  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.00304566  | 0.0271329  | 0.910659    | 5392 |  0.0296263  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.0034453   | 0.0286035  | 0.904162    | 5392 |  0.0296263  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.0198118   | 0.0286621  | 0.489666    | 5392 |  0.0296263  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.0593152   | 0.0132686  | 9.16264e-06 | 5392 |  0.0296263  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                | -0.00996538  | 0.0120805  | 0.409713    | 5392 |  0.0296263  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                | -0.000222871 | 0.0108687  | 0.983646    | 5392 |  0.0296263  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0275765   | 0.0124955  | 0.0276569   | 5392 |  0.0296263  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0244023   | 0.0116717  | 0.0369278   | 5392 |  0.0296263  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0508872   | 0.0117404  | 1.68533e-05 | 5392 |  0.0296263  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0751607   | 0.012272   | 1.54609e-09 | 5392 |  0.0296263  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00899745  | 0.00959765 | 0.348856    | 5392 |  0.0432173  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.0167391   | 0.0104956  | 0.111211    | 5392 |  0.0432173  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0108617   | 0.0078145  | 0.165007    | 5392 |  0.0432173  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00156503  | 0.00786422 | 0.842318    | 5392 |  0.0432173  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.000513307 | 0.00853145 | 0.952041    | 5392 |  0.0432173  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0170813   | 0.0107489  | 0.112501    | 5392 |  0.0432173  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0145836   | 0.00884345 | 0.0995967   | 5392 |  0.0432173  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.0134507   | 0.0389115  | 0.729696    | 5392 |  0.0432173  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            | -0.0115206   | 0.0370636  | 0.756023    | 5392 |  0.0432173  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.0174521   | 0.0335751  | 0.603379    | 5392 |  0.0432173  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.00330544  | 0.0363547  | 0.927582    | 5392 |  0.0432173  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.0222704   | 0.03684    | 0.545705    | 5392 |  0.0432173  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             | -0.00528619  | 0.0403636  | 0.895843    | 5392 |  0.0432173  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.0196415   | 0.038026   | 0.605655    | 5392 |  0.0432173  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.0949796   | 0.0179317  | 1.59861e-07 | 5392 |  0.0432173  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered | -0.0217867   | 0.0162547  | 0.180589    | 5392 |  0.0432173  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered | -0.00351188  | 0.0153364  | 0.818947    | 5392 |  0.0432173  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0468353   | 0.0179396  | 0.00923622  | 5392 |  0.0432173  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0396098   | 0.0170516  | 0.0204802   | 5392 |  0.0432173  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.0842369   | 0.0161689  | 2.51619e-07 | 5392 |  0.0432173  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.123504    | 0.0166164  | 3.24407e-13 | 5392 |  0.0432173  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                3 |    2.74209  | 0.433121 | 5392 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |    2.49807  | 0.475641 | 5392 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |    1.49882  | 0.682542 | 5392 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |    3.11032  | 0.374926 | 5392 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |    0.985797 | 0.804689 | 5392 |