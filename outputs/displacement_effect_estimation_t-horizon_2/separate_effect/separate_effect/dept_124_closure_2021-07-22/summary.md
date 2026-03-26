# Displacement Effect Estimation Summary

- Sample rows: 12,380
- Unique members: 3,095
- Unique closures: 1
- Event FE units: 3,095
- Relative periods: [-2, -1, 1, 2]
- Estimation mode: separate_effect=true
- Closure event: `dept_124_closure_2021-07-22`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |     n |   r2_within |         coef |         se |      pvalue |
|:-----------------|:----------------------|------:|------------:|-------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 12380 |   0.0188002 |  0.000774417 | 0.00196076 | 0.692902    |
| binary_collapsed | post_X_disp           | 12380 |   0.0188002 | -0.0288373   | 0.00357821 | 1.11022e-15 |
| binary_collapsed | post_X_treated_X_disp | 12380 |   0.0188002 |  0.00197294  | 0.00539683 | 0.714708    |

## Score Spec
| spec            | term                   |     n |   r2_within |        coef |         se |   pvalue |
|:----------------|:-----------------------|------:|------------:|------------:|-----------:|---------:|
| score_collapsed | post_X_treated         | 12380 |   0.0262937 |  0.00115334 | 0.00177391 | 0.515632 |
| score_collapsed | post_X_score           | 12380 |   0.0262937 | -0.0485247  | 0.00560006 | 0        |
| score_collapsed | post_X_treated_X_score | 12380 |   0.0262937 |  0.00511669 | 0.00860569 | 0.552174 |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.000766423 | 0.00279872 | 0.78422     | 12380 | 0.000161664 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00150613  | 0.00305893 | 0.622492    | 12380 | 0.000161664 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00216722  | 0.0030083  | 0.471325    | 12380 | 0.000161664 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00115127  | 0.001872   | 0.538603    | 12380 | 0.0207505   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.000977339 | 0.00239521 | 0.683274    | 12380 | 0.0207505   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.000579777 | 0.00213609 | 0.786086    | 12380 | 0.0207505   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.000309143 | 0.00594506 | 0.958532    | 12380 | 0.0207505   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.00358523  | 0.00644181 | 0.577871    | 12380 | 0.0207505   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  5.15086e-05 | 0.00631143 | 0.993489    | 12380 | 0.0207505   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.00916869  | 0.00404734 | 0.0235594   | 12380 | 0.0207505   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0209123   | 0.00439564 | 2.04972e-06 | 12380 | 0.0207505   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0275937   | 0.00434376 | 2.42922e-10 | 12380 | 0.0207505   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00133302  | 0.00181693 | 0.463206    | 12380 | 0.0280991   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00145889  | 0.00213515 | 0.494486    | 12380 | 0.0280991   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.000485238 | 0.0020401  | 0.812013    | 12380 | 0.0280991   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.00183527  | 0.00913383 | 0.840765    | 12380 | 0.0280991   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.00975069  | 0.0102486  | 0.341468    | 12380 | 0.0280991   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.00231795  | 0.0100462  | 0.817541    | 12380 | 0.0280991   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.00626647  | 0.00612347 | 0.306221    | 12380 | 0.0280991   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0396636   | 0.00702306 | 1.77419e-08 | 12380 | 0.0280991   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0511193   | 0.00691341 | 1.82299e-13 | 12380 | 0.0280991   |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |     n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|------:|
| event_att      | pretrend_att_joint_zero            |                1 |   0.0749926 | 0.784202 | 12380 |
| event_binary_B | pretrend_baseline_joint_zero       |                1 |   0.37822   | 0.538557 | 12380 |
| event_binary_B | pretrend_displacement_joint_zero   |                1 |   0.002704  | 0.958529 | 12380 |
| event_score_C  | pretrend_score_baseline_joint_zero |                1 |   0.538271  | 0.46315  | 12380 |
| event_score_C  | pretrend_score_slope_joint_zero    |                1 |   0.0403734 | 0.840752 | 12380 |