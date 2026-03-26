# Displacement Effect Estimation Summary

- Sample rows: 1,764
- Unique members: 441
- Unique closures: 1
- Event FE units: 441
- Relative periods: [-2, -1, 1, 2]
- Estimation mode: separate_effect=true
- Closure event: `dept_181_closure_2021-02-11`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |       coef |        se |      pvalue |
|:-----------------|:----------------------|-----:|------------:|-----------:|----------:|------------:|
| binary_collapsed | post_X_treated        | 1764 |   0.0377071 |  0.0142857 | 0.0144682 | 0.323994    |
| binary_collapsed | post_X_disp           | 1764 |   0.0377071 | -0.0527559 | 0.0101123 | 2.80616e-07 |
| binary_collapsed | post_X_treated_X_disp | 1764 |   0.0377071 |  0.0339247 | 0.0357743 | 0.343497    |

## Score Spec
| spec            | term                   |    n |   r2_within |       coef |        se |      pvalue |
|:----------------|:-----------------------|-----:|------------:|-----------:|----------:|------------:|
| score_collapsed | post_X_treated         | 1764 |   0.0501751 |  0.0254545 | 0.0150057 | 0.0905334   |
| score_collapsed | post_X_score           | 1764 |   0.0501751 | -0.0817856 | 0.0152434 | 1.30927e-07 |
| score_collapsed | post_X_treated_X_score | 1764 |   0.0501751 |  0.0133919 | 0.0529825 | 0.800571    |

## Event-study Specs
| spec           | term                                                              |        coef |        se |      pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|------------:|----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0314324  | 0.0199757 | 0.116314    | 1764 |  0.00870174 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0545908  | 0.0174917 | 0.00192133  | 1764 |  0.00870174 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0198122  | 0.0174178 | 0.25596     | 1764 |  0.00870174 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00507234 | 0.0113013 | 0.653778    | 1764 |  0.0477158  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0266034  | 0.0144638 | 0.0665438   | 1764 |  0.0477158  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00704036 | 0.0171366 | 0.681391    | 1764 |  0.0477158  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0500458  | 0.039769  | 0.20891     | 1764 |  0.0477158  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.0720365  | 0.0351397 | 0.0409563   | 1764 |  0.0477158  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.0458587  | 0.0356394 | 0.198861    | 1764 |  0.0477158  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.00392248 | 0.0143331 | 0.78447     | 1764 |  0.0477158  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0460625  | 0.0117245 | 9.91327e-05 | 1764 |  0.0477158  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0555268  | 0.0136429 | 5.57346e-05 | 1764 |  0.0477158  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0205418  | 0.0156128 | 0.188959    | 1764 |  0.0604676  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0516711  | 0.0151524 | 0.000709284 | 1764 |  0.0604676  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0197797  | 0.0168362 | 0.240697    | 1764 |  0.0604676  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.0936544  | 0.0492663 | 0.0579575   | 1764 |  0.0604676  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.0695301  | 0.0497873 | 0.163255    | 1764 |  0.0604676  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.0509081  | 0.0449421 | 0.257936    | 1764 |  0.0604676  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.00104818 | 0.0209494 | 0.960118    | 1764 |  0.0604676  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0758068  | 0.0169831 | 1.02496e-05 | 1764 |  0.0604676  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0867163  | 0.0200492 | 1.88742e-05 | 1764 |  0.0604676  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |    pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|----------:|-----:|
| event_att      | pretrend_att_joint_zero            |                1 |    2.47601  | 0.115596  | 1764 |
| event_binary_B | pretrend_baseline_joint_zero       |                1 |    0.201445 | 0.653557  | 1764 |
| event_binary_B | pretrend_displacement_joint_zero   |                1 |    1.5836   | 0.208243  | 1764 |
| event_score_C  | pretrend_score_baseline_joint_zero |                1 |    1.73107  | 0.188274  | 1764 |
| event_score_C  | pretrend_score_slope_joint_zero    |                1 |    3.61373  | 0.0573044 | 1764 |