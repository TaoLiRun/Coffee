# Displacement Effect Estimation Summary

- Sample rows: 2,064
- Unique members: 258
- Unique closures: 1
- Event FE units: 258
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_220_closure_2021-08-03`
- Closure duration filter days: 10
- Recency filter days: 10
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |        coef |        se |      pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|----------:|------------:|
| binary_collapsed | post_X_treated        | 2064 |   0.0163437 |  0.00884662 | 0.0143631 | 0.538487    |
| binary_collapsed | post_X_disp           | 2064 |   0.0163437 | -0.0624497  | 0.0156593 | 8.69096e-05 |
| binary_collapsed | post_X_treated_X_disp | 2064 |   0.0163437 |  0.0253916  | 0.0559392 | 0.650273    |

## Score Spec
| spec            | term                   |    n |   r2_within |      coef |        se |      pvalue |
|:----------------|:-----------------------|-----:|------------:|----------:|----------:|------------:|
| score_collapsed | post_X_treated         | 2064 |   0.0190664 |  0.025373 | 0.0299163 | 0.397153    |
| score_collapsed | post_X_score           | 2064 |   0.0190664 | -0.105221 | 0.0246158 | 2.70135e-05 |
| score_collapsed | post_X_treated_X_score | 2064 |   0.0190664 |  0.061006 | 0.0992166 | 0.53918     |

## Event-study Specs
| spec           | term                                                              |         coef |        se |      pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00143103  | 0.0248695 | 0.954158    | 2064 |  0.00402275 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0293276   | 0.0264542 | 0.268632    | 2064 |  0.00402275 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0247069   | 0.0243613 | 0.311448    | 2064 |  0.00402275 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00260345  | 0.0282361 | 0.926609    | 2064 |  0.00402275 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0077069   | 0.0337083 | 0.819334    | 2064 |  0.00402275 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0206724   | 0.0308235 | 0.503032    | 2064 |  0.00402275 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0276034   | 0.0280953 | 0.326781    | 2064 |  0.00402275 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.013285    | 0.0222364 | 0.550736    | 2064 |  0.0477011  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0233092   | 0.0221469 | 0.293568    | 2064 |  0.0477011  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.025       | 0.0194814 | 0.200551    | 2064 |  0.0477011  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00857488  | 0.0252963 | 0.734903    | 2064 |  0.0477011  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0121981   | 0.0251472 | 0.628042    | 2064 |  0.0477011  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.000603865 | 0.0288693 | 0.983328    | 2064 |  0.0477011  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00483092  | 0.0233974 | 0.836585    | 2064 |  0.0477011  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0597497   | 0.0514979 | 0.247029    | 2064 |  0.0477011  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.029959    | 0.0562244 | 0.5946      | 2064 |  0.0477011  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0505892   | 0.0486883 | 0.299761    | 2064 |  0.0477011  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.0305446   | 0.0659711 | 0.643757    | 2064 |  0.0477011  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.0739826   | 0.0788762 | 0.349147    | 2064 |  0.0477011  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.0652503   | 0.0698481 | 0.35109     | 2064 |  0.0477011  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.0720868   | 0.0663794 | 0.278505    | 2064 |  0.0477011  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.0672705   | 0.0248514 | 0.00724636  | 2064 |  0.0477011  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.108172    | 0.0249236 | 2.04863e-05 | 2064 |  0.0477011  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.117593    | 0.0227583 | 4.77791e-07 | 2064 |  0.0477011  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  0.00253623  | 0.0221567 | 0.908956    | 2064 |  0.0477011  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.0507649   | 0.0265495 | 0.0569768   | 2064 |  0.0477011  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.0216184   | 0.0242406 | 0.373321    | 2064 |  0.0477011  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0316828   | 0.0228684 | 0.167119    | 2064 |  0.0477011  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.0196584   | 0.0259453 | 0.449333    | 2064 |  0.0521634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0116229   | 0.0294287 | 0.693207    | 2064 |  0.0521634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00377749  | 0.0251773 | 0.880854    | 2064 |  0.0521634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0049498   | 0.0348245 | 0.887084    | 2064 |  0.0521634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0278842   | 0.0407795 | 0.494731    | 2064 |  0.0521634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0358196   | 0.0370125 | 0.334069    | 2064 |  0.0521634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0370966   | 0.0353668 | 0.295204    | 2064 |  0.0521634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.151303    | 0.0800948 | 0.0600104   | 2064 |  0.0521634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.0521346   | 0.0911502 | 0.567847    | 2064 |  0.0521634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.0842067   | 0.0788764 | 0.286713    | 2064 |  0.0521634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.0296475   | 0.108691  | 0.78525     | 2064 |  0.0521634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.171937    | 0.133271  | 0.198166    | 2064 |  0.0521634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.171273    | 0.118953  | 0.15113     | 2064 |  0.0521634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.158812    | 0.115825  | 0.17153     | 2064 |  0.0521634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered |  0.0988241   | 0.0390947 | 0.0120776   | 2064 |  0.0521634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.164101    | 0.0377391 | 1.97906e-05 | 2064 |  0.0521634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.169529    | 0.0359203 | 3.88575e-06 | 2064 |  0.0521634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.00288894  | 0.0334926 | 0.93133     | 2064 |  0.0521634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  |  0.0651026   | 0.0408296 | 0.112055    | 2064 |  0.0521634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  |  0.00315109  | 0.0379222 | 0.933842    | 2064 |  0.0521634  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.0537932   | 0.0355803 | 0.131793    | 2064 |  0.0521634  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                3 |     2.04807 | 0.562491 | 2064 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |     1.85289 | 0.603494 | 2064 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |     1.80564 | 0.613708 | 2064 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |     1.31857 | 0.724728 | 2064 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |     4.06651 | 0.254371 | 2064 |