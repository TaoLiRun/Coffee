# Displacement Effect Estimation Summary

- Sample rows: 160,592
- Unique members: 40,148
- Unique closures: 18
- Event FE units: 40,148
- Relative periods: [-2, -1, 1, 2]
- Estimation mode: separate_effect=false
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Model type: DDD


## Binary Specs
| spec             | term                  |     n |   r2_within |        coef |        se |   pvalue |
|:-----------------|:----------------------|------:|------------:|------------:|----------:|---------:|
| binary_collapsed | post_X_treated        | 42101 | 5.70148e-05 |  0.013008   | 0.0152262 | 0.392945 |
| binary_collapsed | post_X_disp           | 42101 | 5.70148e-05 | -0.00214688 | 0.0078675 | 0.78495  |
| binary_collapsed | post_X_treated_X_disp | 42101 | 5.70148e-05 | -0.0145032  | 0.0178369 | 0.416173 |

## Score Spec
| spec            | term                   |     n |   r2_within |        coef |        se |   pvalue |
|:----------------|:-----------------------|------:|------------:|------------:|----------:|---------:|
| score_collapsed | post_X_treated         | 42101 | 7.64165e-05 |  0.00987653 | 0.013102  | 0.450971 |
| score_collapsed | post_X_score           | 42101 | 7.64165e-05 | -0.00797769 | 0.0124345 | 0.521159 |
| score_collapsed | post_X_treated_X_score | 42101 | 7.64165e-05 | -0.0197831  | 0.0270906 | 0.465245 |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00965539  | 0.00899174 | 0.282926    | 42101 | 3.88792e-05 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00867764  | 0.010283   | 0.398751    | 42101 | 3.88792e-05 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00724287  | 0.0117657  | 0.538174    | 42101 | 3.88792e-05 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00910535  | 0.0190978  | 0.633529    | 42101 | 0.000563154 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0269802   | 0.0199356  | 0.175959    | 42101 | 0.000563154 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00802739  | 0.0216736  | 0.711107    | 42101 | 0.000563154 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.000186646 | 0.0214454  | 0.993056    | 42101 | 0.000563154 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0276527   | 0.0231313  | 0.231923    | 42101 | 0.000563154 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.000115799 | 0.0256917  | 0.996404    | 42101 | 0.000563154 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                | -0.0290411   | 0.00890028 | 0.00110509  | 42101 | 0.000563154 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0111864   | 0.0101918  | 0.272401    | 42101 | 0.000563154 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0218546   | 0.0110447  | 0.0478626   | 42101 | 0.000563154 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00983245  | 0.0188953  | 0.602817    | 42101 | 0.00257581  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0268568   | 0.0201436  | 0.182465    | 42101 | 0.00257581  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00524898  | 0.0215996  | 0.807999    | 42101 | 0.00257581  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.0080064   | 0.0213504  | 0.707666    | 42101 | 0.00257581  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.042448    | 0.0241871  | 0.0792824   | 42101 | 0.00257581  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.00131927  | 0.026347   | 0.960065    | 42101 | 0.00257581  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                | -0.0244456   | 0.00885368 | 0.00576843  | 42101 | 0.00257581  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.00232616  | 0.0101764  | 0.819196    | 42101 | 0.00257581  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0132784   | 0.0109901  | 0.226985    | 42101 | 0.00257581  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_len              |  0.00319106  | 0.0159977  | 0.841897    | 42101 | 0.00257581  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_len               | -0.0100574   | 0.0164064  | 0.539873    | 42101 | 0.00257581  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_len               | -0.00940429  | 0.0182391  | 0.606133    | 42101 | 0.00257581  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_X_len                 | -0.00888045  | 0.00413512 | 0.0317641   | 42101 | 0.00257581  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_X_len                  | -0.0336386   | 0.0054335  | 6.13709e-10 | 42101 | 0.00257581  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_X_len                  | -0.0418019   | 0.00674492 | 5.88687e-10 | 42101 | 0.00257581  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:tXdXlen                    |  0.0128371   | 0.0176513  | 0.467078    | 42101 | 0.00257581  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:tXdXlen                     |  0.0384627   | 0.0193087  | 0.0463905   | 42101 | 0.00257581  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:tXdXlen                     |  0.0252619   | 0.0218467  | 0.247567    | 42101 | 0.00257581  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00448369  | 0.0165598  | 0.786581    | 42101 | 0.000638727 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0171611   | 0.0168613  | 0.308798    | 42101 | 0.000638727 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00729088  | 0.0182854  | 0.690101    | 42101 | 0.000638727 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.0125143   | 0.0322889  | 0.698338    | 42101 | 0.000638727 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.0261404   | 0.0341587  | 0.444127    | 42101 | 0.000638727 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.00111887  | 0.0379369  | 0.976472    | 42101 | 0.000638727 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered | -0.0530536   | 0.0138551  | 0.000129102 | 42101 | 0.000638727 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0226708   | 0.0155926  | 0.145983    | 42101 | 0.000638727 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0425348   | 0.016869   | 0.0116969   | 42101 | 0.000638727 |

## Pre-trend Joint Tests
| spec           | test                                    |   n_restrictions |   statistic |   pvalue |     n |
|:---------------|:----------------------------------------|-----------------:|------------:|---------:|------:|
| event_att      | pretrend_att_joint_zero                 |                1 | 1.15306     | 0.282909 | 42101 |
| event_binary_B | pretrend_baseline_joint_zero            |                1 | 0.227315    | 0.633522 | 42101 |
| event_binary_B | pretrend_displacement_joint_zero        |                1 | 7.57479e-05 | 0.993056 | 42101 |
| event_binary_D | pretrend_length_displacement_joint_zero |                1 | 0.528906    | 0.467067 | 42101 |
| event_binary_D | pretrend_length_baseline_joint_zero     |                1 | 0.0397885   | 0.841895 | 42101 |
| event_score_C  | pretrend_score_baseline_joint_zero      |                1 | 0.0733096   | 0.786578 | 42101 |
| event_score_C  | pretrend_score_slope_joint_zero         |                1 | 0.150212    | 0.698333 | 42101 |