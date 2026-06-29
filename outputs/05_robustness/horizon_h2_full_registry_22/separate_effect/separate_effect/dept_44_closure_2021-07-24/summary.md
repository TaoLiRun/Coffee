# Displacement Effect Estimation Summary

- Sample rows: 6,252
- Unique members: 1,563
- Unique closures: 1
- Event FE units: 1,563
- Relative periods: [-2, -1, 1, 2]
- Estimation mode: separate_effect=true
- Closure event: `dept_44_closure_2021-07-24`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |        coef |         se |   pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|-----------:|---------:|
| binary_collapsed | post_X_treated        | 6252 |   0.0511394 |  0.00495455 | 0.0036209  | 0.171408 |
| binary_collapsed | post_X_disp           | 6252 |   0.0511394 | -0.0642115  | 0.00737466 | 0        |
| binary_collapsed | post_X_treated_X_disp | 6252 |   0.0511394 |  0.013514   | 0.0163589  | 0.408877 |

## Score Spec
| spec            | term                   |    n |   r2_within |        coef |         se |   pvalue |
|:----------------|:-----------------------|-----:|------------:|------------:|-----------:|---------:|
| score_collapsed | post_X_treated         | 6252 |   0.0699378 |  0.00819206 | 0.00529315 | 0.121904 |
| score_collapsed | post_X_score           | 6252 |   0.0699378 | -0.0982224  | 0.010064   | 0        |
| score_collapsed | post_X_treated_X_score | 6252 |   0.0699378 |  0.0149986  | 0.0215427  | 0.48639  |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00260687  | 0.00510821 | 0.609892    | 6252 |   0.0017863 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0130328   | 0.00580527 | 0.0249079   | 6252 |   0.0017863 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00683244  | 0.00582923 | 0.241335    | 6252 |   0.0017863 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0063845   | 0.00364667 | 0.0801807   | 6252 |   0.0581155 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.000686209 | 0.0043104  | 0.873533    | 6252 |   0.0581155 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0028384   | 0.0043784  | 0.516904    | 6252 |   0.0581155 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0206965   | 0.0178064  | 0.245287    | 6252 |   0.0581155 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.0397768   | 0.0199099  | 0.0459071   | 6252 |   0.0581155 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.00794772  | 0.019907   | 0.689768    | 6252 |   0.0581155 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0196355   | 0.00823744 | 0.017259    | 6252 |   0.0581155 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0649697   | 0.00930976 | 4.38871e-12 | 6252 |   0.0581155 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0438179   | 0.00950627 | 4.36771e-06 | 6252 |   0.0581155 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.000181945 | 0.00580506 | 0.975       | 6252 |   0.0770509 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0116217   | 0.00655283 | 0.0763356   | 6252 |   0.0770509 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00458052  | 0.00657183 | 0.485911    | 6252 |   0.0770509 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.0272328   | 0.0237228  | 0.251162    | 6252 |   0.0770509 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.0474085   | 0.0275079  | 0.0850054   | 6252 |   0.0770509 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.00982155  | 0.0279858  | 0.725675    | 6252 |   0.0770509 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0270502   | 0.0111526  | 0.0154018   | 6252 |   0.0770509 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0983956   | 0.01281    | 2.75335e-14 | 6252 |   0.0770509 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.070999    | 0.0129794  | 5.2292e-08  | 6252 |   0.0770509 |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |    pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|----------:|-----:|
| event_att      | pretrend_att_joint_zero            |                1 |  0.260437   | 0.60982   | 6252 |
| event_binary_B | pretrend_baseline_joint_zero       |                1 |  3.06522    | 0.0799844 | 6252 |
| event_binary_B | pretrend_displacement_joint_zero   |                1 |  1.35097    | 0.245109  | 6252 |
| event_score_C  | pretrend_score_baseline_joint_zero |                1 |  0.00098235 | 0.974996  | 6252 |
| event_score_C  | pretrend_score_slope_joint_zero    |                1 |  1.3178     | 0.250986  | 6252 |