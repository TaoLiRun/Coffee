# Displacement Effect Estimation Summary

- Sample rows: 13,784
- Unique members: 1,723
- Unique closures: 22
- Event FE units: 1,723
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=false
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: True
- Model type: DiD


## Binary Specs
| spec          | term           |     n |   r2_within |      coef |        se |    pvalue |
|:--------------|:---------------|------:|------------:|----------:|----------:|----------:|
| did_collapsed | post_X_treated | 13784 | 0.000424378 | 0.0299111 | 0.0143518 | 0.0372951 |

## Score Spec
_No rows produced._

## Event-study Specs
| spec      | term                                           |         coef |        se |   pvalue |     n |   r2_within |
|:----------|:-----------------------------------------------|-------------:|----------:|---------:|------:|------------:|
| event_att | C(rel_t, contr.treatment(base=-1))[-4]:treated | -0.0243757   | 0.0270804 | 0.368181 | 13784 |  0.00116384 |
| event_att | C(rel_t, contr.treatment(base=-1))[-3]:treated |  0.000992052 | 0.0273212 | 0.971039 | 13784 |  0.00116384 |
| event_att | C(rel_t, contr.treatment(base=-1))[-2]:treated | -0.0166945   | 0.0251267 | 0.506516 | 13784 |  0.00116384 |
| event_att | C(rel_t, contr.treatment(base=-1))[1]:treated  |  0.0410109   | 0.0274631 | 0.135539 | 13784 |  0.00116384 |
| event_att | C(rel_t, contr.treatment(base=-1))[2]:treated  |  0.0415101   | 0.0279822 | 0.138138 | 13784 |  0.00116384 |
| event_att | C(rel_t, contr.treatment(base=-1))[3]:treated  |  0.0176313   | 0.0263784 | 0.50397  | 13784 |  0.00116384 |
| event_att | C(rel_t, contr.treatment(base=-1))[4]:treated  | -0.0213173   | 0.0253747 | 0.40097  | 13784 |  0.00116384 |

## Pre-trend Joint Tests
| spec      | test                    |   n_restrictions |   statistic |   pvalue |     n |
|:----------|:------------------------|-----------------:|------------:|---------:|------:|
| event_att | pretrend_att_joint_zero |                3 |     1.48419 | 0.685924 | 13784 |