# Displacement Effect Estimation Summary

- Sample rows: 8,776
- Unique members: 2,194
- Unique closures: 1
- Event FE units: 2,194
- Relative periods: [-2, -1, 1, 2]
- Estimation mode: separate_effect=true
- Closure event: `dept_133_closure_2021-07-28`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |        coef |         se |      pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 8776 |   0.0259144 | -0.00299405 | 0.00303005 | 0.323204    |
| binary_collapsed | post_X_disp           | 8776 |   0.0259144 | -0.0331827  | 0.00357889 | 0           |
| binary_collapsed | post_X_treated_X_disp | 8776 |   0.0259144 |  0.0364665  | 0.00867147 | 2.71168e-05 |

## Score Spec
| spec            | term                   |    n |   r2_within |        coef |         se |      pvalue |
|:----------------|:-----------------------|-----:|------------:|------------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 8776 |   0.0369999 |  0.00445912 | 0.00283897 | 0.1164      |
| score_collapsed | post_X_score           | 8776 |   0.0369999 | -0.0608983  | 0.00640752 | 0           |
| score_collapsed | post_X_treated_X_score | 8776 |   0.0369999 |  0.0592642  | 0.0134366  | 1.08037e-05 |

## Event-study Specs
| spec           | term                                                              |        coef |         se |      pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|------------:|-----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00621511 | 0.00433216 | 0.151532    | 8776 |  0.00172655 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0129791  | 0.00455425 | 0.00441429  | 8776 |  0.00172655 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00370676 | 0.00407932 | 0.363624    | 8776 |  0.00172655 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00107585 | 0.00306093 | 0.725264    | 8776 |  0.0309564  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00185613 | 0.00407742 | 0.648994    | 8776 |  0.0309564  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00305612 | 0.00305857 | 0.317809    | 8776 |  0.0309564  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.0181828  | 0.0119184  | 0.127252    | 8776 |  0.0309564  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.0404259  | 0.0115812  | 0.000491361 | 8776 |  0.0309564  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.0143243  | 0.0109693  | 0.191737    | 8776 |  0.0309564  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0175927  | 0.00421347 | 3.09179e-05 | 8776 |  0.0309564  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0228791  | 0.00412577 | 3.28552e-08 | 8776 |  0.0309564  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0258937  | 0.00419936 | 8.30841e-10 | 8776 |  0.0309564  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00404546 | 0.00333743 | 0.225587    | 8776 |  0.0416346  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0062128  | 0.00386456 | 0.10806     | 8776 |  0.0416346  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00134001 | 0.00327925 | 0.68285     | 8776 |  0.0416346  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.014721   | 0.0197086  | 0.455185    | 8776 |  0.0416346  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.0726276  | 0.0170303  | 2.08753e-05 | 8776 |  0.0416346  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.0311798  | 0.0171606  | 0.0693621   | 8776 |  0.0416346  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0222478  | 0.00719886 | 0.0020236   | 8776 |  0.0416346  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0450046  | 0.00735724 | 1.12554e-09 | 8776 |  0.0416346  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0545442  | 0.00729374 | 1.08358e-13 | 8776 |  0.0416346  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                1 |    2.0582   | 0.151389 | 8776 |
| event_binary_B | pretrend_baseline_joint_zero       |                1 |    0.123536 | 0.725231 | 8776 |
| event_binary_B | pretrend_displacement_joint_zero   |                1 |    2.32748  | 0.127107 | 8776 |
| event_score_C  | pretrend_score_baseline_joint_zero |                1 |    1.4693   | 0.225456 | 8776 |
| event_score_C  | pretrend_score_slope_joint_zero    |                1 |    0.557907 | 0.455105 | 8776 |