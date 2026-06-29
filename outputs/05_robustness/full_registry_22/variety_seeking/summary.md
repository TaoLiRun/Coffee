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
| spec          | term           |     n |   r2_within |      coef |        se |     pvalue |
|:--------------|:---------------|------:|------------:|----------:|----------:|-----------:|
| did_collapsed | post_X_treated | 13784 | 0.000743102 | 0.0406612 | 0.0141874 | 0.00420746 |

## Score Spec
_No rows produced._

## Event-study Specs
| spec      | term                                           |       coef |        se |    pvalue |     n |   r2_within |
|:----------|:-----------------------------------------------|-----------:|----------:|----------:|------:|------------:|
| event_att | C(rel_t, contr.treatment(base=-1))[-4]:treated | -0.0283056 | 0.0277172 | 0.30729   | 13784 |  0.00158194 |
| event_att | C(rel_t, contr.treatment(base=-1))[-3]:treated |  0.0028645 | 0.0276499 | 0.9175    | 13784 |  0.00158194 |
| event_att | C(rel_t, contr.treatment(base=-1))[-2]:treated | -0.0226342 | 0.0258438 | 0.381256  | 13784 |  0.00158194 |
| event_att | C(rel_t, contr.treatment(base=-1))[1]:treated  |  0.0493459 | 0.0279239 | 0.0773784 | 13784 |  0.00158194 |
| event_att | C(rel_t, contr.treatment(base=-1))[2]:treated  |  0.0505251 | 0.0280249 | 0.0715835 | 13784 |  0.00158194 |
| event_att | C(rel_t, contr.treatment(base=-1))[3]:treated  |  0.0305025 | 0.0274693 | 0.266974  | 13784 |  0.00158194 |
| event_att | C(rel_t, contr.treatment(base=-1))[4]:treated  | -0.0165649 | 0.0253603 | 0.513725  | 13784 |  0.00158194 |

## Pre-trend Joint Tests
| spec      | test                    |   n_restrictions |   statistic |   pvalue |     n |
|:----------|:------------------------|-----------------:|------------:|---------:|------:|
| event_att | pretrend_att_joint_zero |                3 |     2.23609 | 0.524875 | 13784 |