# Displacement Effect Estimation Summary

- Sample rows: 10,852
- Unique members: 2,713
- Unique closures: 1
- Event FE units: 2,713
- Relative periods: [-2, -1, 1, 2]
- Estimation mode: separate_effect=true
- Closure event: `dept_131_closure_2021-08-29`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |     n |   r2_within |        coef |         se |      pvalue |
|:-----------------|:----------------------|------:|------------:|------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 10852 |   0.0300767 | -0.00350993 | 0.00382013 | 0.358283    |
| binary_collapsed | post_X_disp           | 10852 |   0.0300767 | -0.0665897  | 0.00985821 | 1.74425e-11 |
| binary_collapsed | post_X_treated_X_disp | 10852 |   0.0300767 |  0.0321709  | 0.021473   | 0.134197    |

## Score Spec
| spec            | term                   |     n |   r2_within |        coef |         se |      pvalue |
|:----------------|:-----------------------|------:|------------:|------------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 10852 |   0.0375422 |  0.00560242 | 0.00713549 | 0.432435    |
| score_collapsed | post_X_score           | 10852 |   0.0375422 | -0.0973115  | 0.0129168  | 6.68354e-14 |
| score_collapsed | post_X_treated_X_score | 10852 |   0.0375422 |  0.0323699  | 0.0301863  | 0.283664    |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00492615  | 0.00455971 | 0.280076    | 10852 | 0.000166559 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.000392617 | 0.00524213 | 0.940303    | 10852 | 0.000166559 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00408934  | 0.00565212 | 0.469433    | 10852 | 0.000166559 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00249505  | 0.00413382 | 0.546179    | 10852 | 0.0337403   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00367092  | 0.00430686 | 0.394099    | 10852 | 0.0337403   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00085389  | 0.00490711 | 0.86187     | 10852 | 0.0337403   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0213928   | 0.0209683  | 0.307705    | 10852 | 0.0337403   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.0395572   | 0.0259542  | 0.127597    | 10852 | 0.0337403   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.0461774   | 0.0266627  | 0.0834033   | 10852 | 0.0337403   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                | -0.0323417   | 0.0112633  | 0.00411808  | 10852 | 0.0337403   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0808625   | 0.0114226  | 1.83964e-12 | 10852 | 0.0337403   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0846586   | 0.0130196  | 9.37772e-11 | 10852 | 0.0337403   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0102512   | 0.00709706 | 0.148735    | 10852 | 0.0422968   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00674893  | 0.00830353 | 0.416416    | 10852 | 0.0422968   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0147071   | 0.00892942 | 0.0996664   | 10852 | 0.0422968   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.0384832   | 0.0268249  | 0.151513    | 10852 | 0.0422968   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.0337699   | 0.0348131  | 0.332116    | 10852 | 0.0422968   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.0694531   | 0.0368283  | 0.0594202   | 10852 | 0.0422968   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered | -0.0469291   | 0.0146533  | 0.0013776   | 10852 | 0.0422968   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.113552    | 0.0148856  | 3.26406e-14 | 10852 | 0.0422968   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.128       | 0.0164128  | 8.88178e-15 | 10852 | 0.0422968   |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |     n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|------:|
| event_att      | pretrend_att_joint_zero            |                1 |    1.16719  | 0.27998  | 10852 |
| event_binary_B | pretrend_baseline_joint_zero       |                1 |    0.364298 | 0.546129 | 10852 |
| event_binary_B | pretrend_displacement_joint_zero   |                1 |    1.04089  | 0.307614 | 10852 |
| event_score_C  | pretrend_score_baseline_joint_zero |                1 |    2.08636  | 0.14862  | 10852 |
| event_score_C  | pretrend_score_slope_joint_zero    |                1 |    2.05811  | 0.151398 | 10852 |