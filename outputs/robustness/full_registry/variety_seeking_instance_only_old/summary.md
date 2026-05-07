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
| spec          | term           |     n |   r2_within |      coef |        se |   pvalue |
|:--------------|:---------------|------:|------------:|----------:|----------:|---------:|
| did_collapsed | post_X_treated | 13784 | 3.57539e-06 | 0.0025555 | 0.0172478 | 0.882231 |

## Score Spec
_No rows produced._

## Event-study Specs
| spec      | term                                           |         coef |        se |   pvalue |     n |   r2_within |
|:----------|:-----------------------------------------------|-------------:|----------:|---------:|------:|------------:|
| event_att | C(rel_t, contr.treatment(base=-1))[-4]:treated |  0.00562363  | 0.0218593 | 0.797005 | 13784 | 0.000891788 |
| event_att | C(rel_t, contr.treatment(base=-1))[-3]:treated | -0.0116957   | 0.0223437 | 0.600732 | 13784 | 0.000891788 |
| event_att | C(rel_t, contr.treatment(base=-1))[-2]:treated |  0.000527442 | 0.0204841 | 0.979461 | 13784 | 0.000891788 |
| event_att | C(rel_t, contr.treatment(base=-1))[1]:treated  | -0.0145219   | 0.0222225 | 0.513536 | 13784 | 0.000891788 |
| event_att | C(rel_t, contr.treatment(base=-1))[2]:treated  | -0.0352632   | 0.0273261 | 0.197065 | 13784 | 0.000891788 |
| event_att | C(rel_t, contr.treatment(base=-1))[3]:treated  |  0.0247983   | 0.0293224 | 0.397831 | 13784 | 0.000891788 |
| event_att | C(rel_t, contr.treatment(base=-1))[4]:treated  |  0.0309968   | 0.0288023 | 0.281992 | 13784 | 0.000891788 |

## Pre-trend Joint Tests
| spec      | test                    |   n_restrictions |   statistic |   pvalue |     n |
|:----------|:------------------------|-----------------:|------------:|---------:|------:|
| event_att | pretrend_att_joint_zero |                3 |    0.882834 | 0.829568 | 13784 |