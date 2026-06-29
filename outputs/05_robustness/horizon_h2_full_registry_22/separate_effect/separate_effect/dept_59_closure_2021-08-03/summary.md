# Displacement Effect Estimation Summary

- Sample rows: 12,744
- Unique members: 3,186
- Unique closures: 1
- Event FE units: 3,186
- Relative periods: [-2, -1, 1, 2]
- Estimation mode: separate_effect=true
- Closure event: `dept_59_closure_2021-08-03`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |     n |   r2_within |        coef |         se |      pvalue |
|:-----------------|:----------------------|------:|------------:|------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 12744 |    0.014489 | -0.00266989 | 0.00281047 | 0.342195    |
| binary_collapsed | post_X_disp           | 12744 |    0.014489 | -0.0287291  | 0.0038959  | 2.09832e-13 |
| binary_collapsed | post_X_treated_X_disp | 12744 |    0.014489 | -0.00546811 | 0.0117569  | 0.641892    |

## Score Spec
| spec            | term                   |     n |   r2_within |        coef |         se |   pvalue |
|:----------------|:-----------------------|------:|------------:|------------:|-----------:|---------:|
| score_collapsed | post_X_treated         | 12744 |   0.0202091 | -0.00482547 | 0.00392658 | 0.219191 |
| score_collapsed | post_X_score           | 12744 |   0.0202091 | -0.0482278  | 0.00574176 | 0        |
| score_collapsed | post_X_treated_X_score | 12744 |   0.0202091 | -0.00455782 | 0.0188179  | 0.808635 |

## Event-study Specs
| spec           | term                                                              |        coef |         se |    pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|------------:|-----------:|----------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00163419 | 0.00430452 | 0.704234  | 12744 | 4.48757e-05 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.001929   | 0.0037931  | 0.611099  | 12744 | 4.48757e-05 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00325102 | 0.00421505 | 0.440593  | 12744 | 4.48757e-05 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00397879 | 0.002844   | 0.161906  | 12744 | 0.0343111   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00261706 | 0.00325509 | 0.421462  | 12744 | 0.0343111   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00397804 | 0.00381876 | 0.297625  | 12744 | 0.0343111   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.00644673 | 0.0137797  | 0.63993   | 12744 | 0.0343111   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0191024  | 0.0111146  | 0.0857709 | 12744 | 0.0343111   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.00171945 | 0.0121783  | 0.887729  | 12744 | 0.0343111   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0486722  | 0.00440256 | 0         | 12744 | 0.0343111   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.00533315 | 0.00429563 | 0.214501  | 12744 | 0.0343111   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.00345276 | 0.00471369 | 0.463919  | 12744 | 0.0343111   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00234185 | 0.00449813 | 0.602663  | 12744 | 0.0394423   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00331953 | 0.00393242 | 0.398652  | 12744 | 0.0394423   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00398957 | 0.00436826 | 0.36115   | 12744 | 0.0394423   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.00602405 | 0.0220963  | 0.785157  | 12744 | 0.0394423   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.0200522  | 0.0179274  | 0.263427  | 12744 | 0.0394423   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.00491252 | 0.0182834  | 0.788187  | 12744 | 0.0394423   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0672836  | 0.00658913 | 0         | 12744 | 0.0394423   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0152576  | 0.00650593 | 0.0190786 | 12744 | 0.0394423   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0139143  | 0.00696762 | 0.0459104 | 12744 | 0.0394423   |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |     n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|------:|
| event_att      | pretrend_att_joint_zero            |                1 |   0.144131  | 0.704209 | 12744 |
| event_binary_B | pretrend_baseline_joint_zero       |                1 |   1.95725   | 0.161808 | 12744 |
| event_binary_B | pretrend_displacement_joint_zero   |                1 |   0.218876  | 0.639898 | 12744 |
| event_score_C  | pretrend_score_baseline_joint_zero |                1 |   0.271053  | 0.602627 | 12744 |
| event_score_C  | pretrend_score_slope_joint_zero    |                1 |   0.0743257 | 0.78514  | 12744 |