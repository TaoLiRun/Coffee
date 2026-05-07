# Displacement Effect Estimation Summary

- Sample rows: 19,512
- Unique members: 2,439
- Unique closures: 1
- Event FE units: 2,439
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_5_closure_2021-08-18`
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Length-heterogeneity event-study spec skipped: true
- Model type: DDD


## Binary Specs
| spec             | term                  |    n |   r2_within |      coef |        se |    pvalue |
|:-----------------|:----------------------|-----:|------------:|----------:|----------:|----------:|
| binary_collapsed | post_X_treated        | 4812 |  0.00231507 | 0.0678462 | 0.0609885 | 0.266164  |
| binary_collapsed | post_X_disp           | 4812 |  0.00231507 | 0.0613743 | 0.0265333 | 0.0208807 |
| binary_collapsed | post_X_treated_X_disp | 4812 |  0.00231507 | 0.0415255 | 0.132099  | 0.753307  |

## Score Spec
| spec            | term                   |    n |   r2_within |      coef |        se |    pvalue |
|:----------------|:-----------------------|-----:|------------:|----------:|----------:|----------:|
| score_collapsed | post_X_treated         | 4812 |  0.00199699 | 0.0797813 | 0.0537876 | 0.138259  |
| score_collapsed | post_X_score           | 4812 |  0.00199699 | 0.0824847 | 0.0448552 | 0.0661687 |
| score_collapsed | post_X_treated_X_score | 4812 |  0.00199699 | 0.226371  | 0.246367  | 0.358361  |

## Event-study Specs
| spec           | term                                                              |        coef |        se |    pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|------------:|----------:|----------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.0689195  | 0.0992434 | 0.487531  | 4812 |  0.00275131 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.124993   | 0.0931226 | 0.179766  | 4812 |  0.00275131 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.101326   | 0.110649  | 0.359983  | 4812 |  0.00275131 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0701952  | 0.105008  | 0.503955  | 4812 |  0.00275131 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0819475  | 0.10987   | 0.455895  | 4812 |  0.00275131 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.191943   | 0.121237  | 0.113632  | 4812 |  0.00275131 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.141778   | 0.115427  | 0.219572  | 4812 |  0.00275131 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.111757   | 0.119042  | 0.348014  | 4812 |  0.0102339  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.112065   | 0.11359   | 0.324045  | 4812 |  0.0102339  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.10814    | 0.154472  | 0.484019  | 4812 |  0.0102339  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.106161   | 0.129894  | 0.41392   | 4812 |  0.0102339  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.126873   | 0.124545  | 0.308549  | 4812 |  0.0102339  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.266038   | 0.139192  | 0.0561974 | 4812 |  0.0102339  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0838761  | 0.132344  | 0.526347  | 4812 |  0.0102339  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             | -0.328384   | 0.204343  | 0.108305  | 4812 |  0.0102339  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0616492  | 0.18919   | 0.744587  | 4812 |  0.0102339  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.0582574  | 0.213153  | 0.784659  | 4812 |  0.0102339  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.196057   | 0.186723  | 0.293929  | 4812 |  0.0102339  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.192252   | 0.295879  | 0.515966  | 4812 |  0.0102339  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              | -0.352068   | 0.304202  | 0.247353  | 4812 |  0.0102339  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.313562   | 0.282924  | 0.267952  | 4812 |  0.0102339  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.0138033  | 0.048605  | 0.776466  | 4812 |  0.0102339  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.00440509 | 0.0472428 | 0.925725  | 4812 |  0.0102339  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                | -0.0474588  | 0.0523613 | 0.364916  | 4812 |  0.0102339  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  0.0133036  | 0.0500028 | 0.79024   | 4812 |  0.0102339  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.0648037  | 0.0500413 | 0.195562  | 4812 |  0.0102339  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.111289   | 0.051219  | 0.0299851 | 4812 |  0.0102339  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.0108654  | 0.0525486 | 0.836225  | 4812 |  0.0102339  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.0618644  | 0.102022  | 0.544372  | 4812 |  0.00955858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.132118   | 0.0978151 | 0.177044  | 4812 |  0.00955858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.158076   | 0.14007   | 0.259307  | 4812 |  0.00955858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0521544  | 0.104722  | 0.618553  | 4812 |  0.00955858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.110857   | 0.125873  | 0.37865   | 4812 |  0.00955858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.195831   | 0.129614  | 0.131078  | 4812 |  0.00955858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.177461   | 0.119082  | 0.136416  | 4812 |  0.00955858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            | -0.185116   | 0.406177  | 0.648648  | 4812 |  0.00955858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.0379601  | 0.376183  | 0.919639  | 4812 |  0.00955858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.304989   | 0.512218  | 0.551667  | 4812 |  0.00955858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.104249   | 0.417709  | 0.802959  | 4812 |  0.00955858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.156869   | 0.568118  | 0.782502  | 4812 |  0.00955858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             | -0.176276   | 0.598338  | 0.768342  | 4812 |  0.00955858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.72486    | 0.493564  | 0.14219   | 4812 |  0.00955858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered |  0.0258578  | 0.0836758 | 0.757356  | 4812 |  0.00955858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.0504368  | 0.0829408 | 0.543229  | 4812 |  0.00955858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered | -0.119081   | 0.0868513 | 0.170596  | 4812 |  0.00955858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0165167  | 0.082865  | 0.842045  | 4812 |  0.00955858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  |  0.108138   | 0.0830936 | 0.193366  | 4812 |  0.00955858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  |  0.217871   | 0.0849964 | 0.0104863 | 4812 |  0.00955858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  |  0.0263785  | 0.0830212 | 0.750742  | 4812 |  0.00955858 |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |    pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|----------:|-----:|
| event_att      | pretrend_att_joint_zero            |                3 |     7.96544 | 0.0467314 | 4812 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |     5.6991  | 0.127203  | 4812 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |     6.07835 | 0.10786   | 4812 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |     8.26748 | 0.0407954 | 4812 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |     1.28971 | 0.731579  | 4812 |