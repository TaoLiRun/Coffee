# Displacement Effect Estimation Summary

- Sample rows: 41,600
- Unique members: 5,200
- Unique closures: 22
- Event FE units: 5,200
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=false
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Model type: DiD


## Binary Specs
| spec          | term           |     n |   r2_within |       coef |         se |   pvalue |
|:--------------|:---------------|------:|------------:|-----------:|-----------:|---------:|
| did_collapsed | post_X_treated | 41600 | 8.04281e-05 | 0.00513671 | 0.00441226 |   0.2444 |

## Score Spec
_No rows produced._

## Event-study Specs
| spec      | term                                           |         coef |         se |    pvalue |     n |   r2_within |
|:----------|:-----------------------------------------------|-------------:|-----------:|----------:|------:|------------:|
| event_att | C(rel_t, contr.treatment(base=-1))[-4]:treated |  0.00246607  | 0.00564694 | 0.66234   | 41600 | 0.000305709 |
| event_att | C(rel_t, contr.treatment(base=-1))[-3]:treated | -0.000889665 | 0.00550004 | 0.871504  | 41600 | 0.000305709 |
| event_att | C(rel_t, contr.treatment(base=-1))[-2]:treated | -0.00551125  | 0.00480167 | 0.251113  | 41600 | 0.000305709 |
| event_att | C(rel_t, contr.treatment(base=-1))[1]:treated  |  0.00759587  | 0.00531791 | 0.153249  | 41600 | 0.000305709 |
| event_att | C(rel_t, contr.treatment(base=-1))[2]:treated  | -0.000278941 | 0.00581579 | 0.961748  | 41600 | 0.000305709 |
| event_att | C(rel_t, contr.treatment(base=-1))[3]:treated  |  0.0109715   | 0.0059157  | 0.0637051 | 41600 | 0.000305709 |
| event_att | C(rel_t, contr.treatment(base=-1))[4]:treated  | -0.00164371  | 0.00601729 | 0.784737  | 41600 | 0.000305709 |

## Pre-trend Joint Tests
| spec      | test                    |   n_restrictions |   statistic |   pvalue |     n |
|:----------|:------------------------|-----------------:|------------:|---------:|------:|
| event_att | pretrend_att_joint_zero |                3 |     2.59943 |  0.45759 | 41600 |