# Displacement Effect Estimation Summary

- Sample rows: 21,704
- Unique members: 2,713
- Unique closures: 1
- Event FE units: 2,713
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_131_closure_2021-08-29`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |     n |   r2_within |        coef |         se |      pvalue |
|:-----------------|:----------------------|------:|------------:|------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 21704 |   0.0170925 |  0.0013379  | 0.00285685 | 0.639598    |
| binary_collapsed | post_X_disp           | 21704 |   0.0170925 | -0.0518594  | 0.00784431 | 4.57741e-11 |
| binary_collapsed | post_X_treated_X_disp | 21704 |   0.0170925 |  0.00456442 | 0.0145832  | 0.754311    |

## Score Spec
| spec            | term                   |     n |   r2_within |        coef |         se |      pvalue |
|:----------------|:-----------------------|------:|------------:|------------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 21704 |   0.0244311 |  0.00348415 | 0.00487333 | 0.474706    |
| score_collapsed | post_X_score           | 21704 |   0.0244311 | -0.0823249  | 0.0101896  | 8.88178e-16 |
| score_collapsed | post_X_treated_X_score | 21704 |   0.0244311 |  0.00576609 | 0.0195357  | 0.767896    |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00247778  | 0.00531965 | 0.641411    | 21704 | 0.000302016 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.00789853  | 0.00535365 | 0.140233    | 21704 | 0.000302016 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00492615  | 0.00456002 | 0.280109    | 21704 | 0.000302016 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.000392617 | 0.00524249 | 0.940307    | 21704 | 0.000302016 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00408934  | 0.00565252 | 0.469463    | 21704 | 0.000302016 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.00444881  | 0.00532103 | 0.403183    | 21704 | 0.000302016 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00515531  | 0.0056995  | 0.3658      | 21704 | 0.000302016 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00693086  | 0.00427581 | 0.105145    | 21704 | 0.0309196   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.000564636 | 0.00444297 | 0.898882    | 21704 | 0.0309196   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00249505  | 0.00413429 | 0.546226    | 21704 | 0.0309196   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00367092  | 0.00430735 | 0.394154    | 21704 | 0.0309196   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00085389  | 0.00490768 | 0.861886    | 21704 | 0.0309196   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  5.52333e-05 | 0.00425532 | 0.989645    | 21704 | 0.0309196   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00595001  | 0.00461527 | 0.197439    | 21704 | 0.0309196   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0414846   | 0.0271448  | 0.126562    | 21704 | 0.0309196   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0593351   | 0.0271205  | 0.0287672   | 21704 | 0.0309196   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0213928   | 0.0209707  | 0.30776     | 21704 | 0.0309196   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.0395572   | 0.0259572  | 0.127641    | 21704 | 0.0309196   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.0461774   | 0.0266658  | 0.0834389   | 21704 | 0.0309196   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.0479115   | 0.0256037  | 0.0614146   | 21704 | 0.0309196   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.00682401  | 0.0274265  | 0.803526    | 21704 | 0.0309196   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.0754601   | 0.0123288  | 1.06684e-09 | 21704 | 0.0309196   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                | -0.0608796   | 0.013475   | 6.51062e-06 | 21704 | 0.0309196   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                | -0.0323417   | 0.0112646  | 0.00412238  | 21704 | 0.0309196   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0808625   | 0.0114239  | 1.8503e-12  | 21704 | 0.0309196   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0846586   | 0.0130211  | 9.42386e-11 | 21704 | 0.0309196   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.1237      | 0.0124677  | 0           | 21704 | 0.0309196   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0868984   | 0.0121453  | 1.0727e-12  | 21704 | 0.0309196   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00446604  | 0.00840025 | 0.595008    | 21704 | 0.0403675   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.0184818   | 0.00904563 | 0.0411316   | 21704 | 0.0403675   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0102512   | 0.00709787 | 0.148782    | 21704 | 0.0403675   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00674893  | 0.00830448 | 0.41647     | 21704 | 0.0403675   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0147071   | 0.00893045 | 0.0997054   | 21704 | 0.0403675   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0168592   | 0.0080645  | 0.0366614   | 21704 | 0.0403675   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00882038  | 0.00870242 | 0.310886    | 21704 | 0.0403675   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.0419918   | 0.034124   | 0.218592    | 21704 | 0.0403675   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.0788287   | 0.0375336  | 0.0358017   | 21704 | 0.0403675   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.0384832   | 0.0268279  | 0.15156     | 21704 | 0.0403675   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.0337699   | 0.0348171  | 0.332172    | 21704 | 0.0403675   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.0694531   | 0.0368325  | 0.0594495   | 21704 | 0.0403675   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.0729422   | 0.0333397  | 0.0287657   | 21704 | 0.0403675   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.00620298  | 0.0362045  | 0.863975    | 21704 | 0.0403675   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.0999267   | 0.0157885  | 2.87635e-10 | 21704 | 0.0403675   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered | -0.0821827   | 0.0179163  | 4.69988e-06 | 21704 | 0.0403675   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered | -0.0469291   | 0.014655   | 0.00137936  | 21704 | 0.0403675   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.113552    | 0.0148873  | 3.28626e-14 | 21704 | 0.0403675   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.128       | 0.0164147  | 8.88178e-15 | 21704 | 0.0403675   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.188564    | 0.0157493  | 0           | 21704 | 0.0403675   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.128222    | 0.0158668  | 8.88178e-16 | 21704 | 0.0403675   |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |     n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|------:|
| event_att      | pretrend_att_joint_zero            |                3 |     5.80026 | 0.121743 | 21704 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |     5.01028 | 0.171046 | 21704 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |     4.84583 | 0.183441 | 21704 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |     6.00577 | 0.11133  | 21704 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |     4.77628 | 0.188931 | 21704 |