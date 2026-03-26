# Displacement Effect Estimation Summary

- Sample rows: 13,204
- Unique members: 3,301
- Unique closures: 1
- Event FE units: 3,301
- Relative periods: [-2, -1, 1, 2]
- Estimation mode: separate_effect=true
- Closure event: `dept_19_closure_2021-07-15`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |     n |   r2_within |         coef |         se |   pvalue |
|:-----------------|:----------------------|------:|------------:|-------------:|-----------:|---------:|
| binary_collapsed | post_X_treated        | 13204 |   0.0680997 | -0.000729016 | 0.00272604 | 0.789157 |
| binary_collapsed | post_X_disp           | 13204 |   0.0680997 | -0.0809613   | 0.00626788 | 0        |
| binary_collapsed | post_X_treated_X_disp | 13204 |   0.0680997 | -0.00987515  | 0.0140978  | 0.48368  |

## Score Spec
| spec            | term                   |     n |   r2_within |        coef |         se |   pvalue |
|:----------------|:-----------------------|------:|------------:|------------:|-----------:|---------:|
| score_collapsed | post_X_treated         | 13204 |   0.0999138 | -0.00640168 | 0.00460689 | 0.164747 |
| score_collapsed | post_X_score           | 13204 |   0.0999138 | -0.140935   | 0.00904202 | 0        |
| score_collapsed | post_X_treated_X_score | 13204 |   0.0999138 | -0.0119274  | 0.0200087  | 0.551141 |

## Event-study Specs
| spec           | term                                                              |         coef |         se |     pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|-----------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00662455  | 0.00432466 | 0.125666   | 13204 |  0.00159837 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00969702  | 0.00452984 | 0.0323715  | 13204 |  0.00159837 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00733978  | 0.00474091 | 0.121675   | 13204 |  0.00159837 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00080488  | 0.0038048  | 0.832476   | 13204 |  0.0718402  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00670773  | 0.00323591 | 0.0382588  | 13204 |  0.0718402  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00444481  | 0.00394335 | 0.259754   | 13204 |  0.0718402  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.0332483   | 0.0182179  | 0.0680866  | 13204 |  0.0718402  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0457932   | 0.0193074  | 0.0177589  | 13204 |  0.0718402  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.0072054   | 0.0194917  | 0.711655   | 13204 |  0.0718402  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0132682   | 0.00723689 | 0.0668308  | 13204 |  0.0718402  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.074672    | 0.00787651 | 0          | 13204 |  0.0718402  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0739823   | 0.00795085 | 0          | 13204 |  0.0718402  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.010766    | 0.00634355 | 0.0897599  | 13204 |  0.104412   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.0244688   | 0.00614154 | 6.9186e-05 | 13204 |  0.104412   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.000899407 | 0.00663964 | 0.892256   | 13204 |  0.104412   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.0434729   | 0.0246832  | 0.0782913  | 13204 |  0.104412   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.0707421   | 0.026711   | 0.0081252  | 13204 |  0.104412   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.00341437  | 0.0282321  | 0.903746   | 13204 |  0.104412   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0129469   | 0.0103343  | 0.210363   | 13204 |  0.104412   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.135788    | 0.0115997  | 0          | 13204 |  0.104412   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.133135    | 0.0115792  | 0          | 13204 |  0.104412   |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |    pvalue |     n |
|:---------------|:-----------------------------------|-----------------:|------------:|----------:|------:|
| event_att      | pretrend_att_joint_zero            |                1 |   2.34644   | 0.12557   | 13204 |
| event_binary_B | pretrend_baseline_joint_zero       |                1 |   0.0447505 | 0.832463  | 13204 |
| event_binary_B | pretrend_displacement_joint_zero   |                1 |   3.33074   | 0.0679963 | 13204 |
| event_score_C  | pretrend_score_baseline_joint_zero |                1 |   2.88037   | 0.0896656 | 13204 |
| event_score_C  | pretrend_score_slope_joint_zero    |                1 |   3.10195   | 0.0781987 | 13204 |