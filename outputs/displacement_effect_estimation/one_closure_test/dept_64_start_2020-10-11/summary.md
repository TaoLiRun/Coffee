# Displacement Effect Estimation Summary

- Sample rows: 7,296
- Unique members: 912
- Unique closures: 1
- Event FE units: 912
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]

## Threshold Specs
| spec          | term                 |        coef |         se |   pvalue |    n |       r2 |
|:--------------|:---------------------|------------:|-----------:|---------:|-----:|---------:|
| threshold_0.5 | post:treated         | -0.00304243 | 0.00663632 | 0.646628 | 7296 | 0.530056 |
| threshold_0.5 | post:treated:disp_05 |  0.00733046 | 0.0218207  | 0.736916 | 7296 | 0.530056 |

## Score Spec
| spec             | term                           |        coef |        se |   pvalue |    n |      r2 |
|:-----------------|:-------------------------------|------------:|----------:|---------:|-----:|--------:|
| score_continuous | post:treated                   | -0.00694707 | 0.0111524 | 0.533335 | 7296 | 0.53108 |
| score_continuous | post:treated:displacement_prob |  0.0162591  | 0.0383631 | 0.671697 | 7296 | 0.53108 |

## Event-study Specs
| spec                   | term                                                                        |         coef |          se |      pvalue |    n |       r2 |
|:-----------------------|:----------------------------------------------------------------------------|-------------:|------------:|------------:|-----:|---------:|
| event_att              | C(rel_t, Treatment(reference=-1))[-4]:treated                               |  0.0133705   | 0.00862264  | 0.120992    | 7296 | 0.52754  |
| event_att              | C(rel_t, Treatment(reference=-1))[-3]:treated                               |  0.0117082   | 0.00762736  | 0.124777    | 7296 | 0.52754  |
| event_att              | C(rel_t, Treatment(reference=-1))[-2]:treated                               |  0.0156138   | 0.00733781  | 0.0333496   | 7296 | 0.52754  |
| event_att              | C(rel_t, Treatment(reference=-1))[-1]:treated                               |  0.0140934   | 0.00658279  | 0.0322781   | 7296 | 0.52754  |
| event_att              | C(rel_t, Treatment(reference=-1))[1]:treated                                | -0.00466425  | 0.00517349  | 0.367287    | 7296 | 0.52754  |
| event_att              | C(rel_t, Treatment(reference=-1))[2]:treated                                |  0.0172094   | 0.00636873  | 0.0068889   | 7296 | 0.52754  |
| event_att              | C(rel_t, Treatment(reference=-1))[3]:treated                                |  0.0242818   | 0.00605685  | 6.09806e-05 | 7296 | 0.52754  |
| event_att              | C(rel_t, Treatment(reference=-1))[4]:treated                                |  0.0178868   | 0.00712209  | 0.0120234   | 7296 | 0.52754  |
| event_threshold_0.5    | C(rel_t, Treatment(reference=-1))[-4]:treated:disp_05                       |  5.30434e-05 | 0.000178008 | 0.765716    | 7296 | 0.536626 |
| event_threshold_0.5    | C(rel_t, Treatment(reference=-1))[-3]:treated:disp_05                       |  0.000148    | 0.000159201 | 0.352557    | 7296 | 0.536626 |
| event_threshold_0.5    | C(rel_t, Treatment(reference=-1))[-2]:treated:disp_05                       |  0.000174188 | 0.000160167 | 0.276798    | 7296 | 0.536626 |
| event_threshold_0.5    | C(rel_t, Treatment(reference=-1))[-1]:treated:disp_05                       |  0.000272112 | 0.000155446 | 0.0800271   | 7296 | 0.536626 |
| event_threshold_0.5    | C(rel_t, Treatment(reference=-1))[1]:treated:disp_05                        |  7.38588e-06 | 0.000109196 | 0.946073    | 7296 | 0.536626 |
| event_threshold_0.5    | C(rel_t, Treatment(reference=-1))[2]:treated:disp_05                        |  0.000262006 | 0.000139205 | 0.0598143   | 7296 | 0.536626 |
| event_threshold_0.5    | C(rel_t, Treatment(reference=-1))[3]:treated:disp_05                        |  0.000478709 | 0.000143622 | 0.000858795 | 7296 | 0.536626 |
| event_threshold_0.5    | C(rel_t, Treatment(reference=-1))[4]:treated:disp_05                        |  0.000139585 | 0.000149652 | 0.350959    | 7296 | 0.536626 |
| event_threshold_0.5    | C(rel_t, Treatment(reference=-1))[-4]:treated:disp_05:closure_duration_days |  0.000583478 | 0.00195809  | 0.765716    | 7296 | 0.536626 |
| event_threshold_0.5    | C(rel_t, Treatment(reference=-1))[-3]:treated:disp_05:closure_duration_days |  0.001628    | 0.00175121  | 0.352557    | 7296 | 0.536626 |
| event_threshold_0.5    | C(rel_t, Treatment(reference=-1))[-2]:treated:disp_05:closure_duration_days |  0.00191607  | 0.00176184  | 0.276798    | 7296 | 0.536626 |
| event_threshold_0.5    | C(rel_t, Treatment(reference=-1))[-1]:treated:disp_05:closure_duration_days |  0.00299324  | 0.0017099   | 0.0800271   | 7296 | 0.536626 |
| event_threshold_0.5    | C(rel_t, Treatment(reference=-1))[1]:treated:disp_05:closure_duration_days  |  8.12447e-05 | 0.00120115  | 0.946073    | 7296 | 0.536626 |
| event_threshold_0.5    | C(rel_t, Treatment(reference=-1))[2]:treated:disp_05:closure_duration_days  |  0.00288207  | 0.00153125  | 0.0598143   | 7296 | 0.536626 |
| event_threshold_0.5    | C(rel_t, Treatment(reference=-1))[3]:treated:disp_05:closure_duration_days  |  0.0052658   | 0.00157984  | 0.000858795 | 7296 | 0.536626 |
| event_threshold_0.5    | C(rel_t, Treatment(reference=-1))[4]:treated:disp_05:closure_duration_days  |  0.00153544  | 0.00164617  | 0.350959    | 7296 | 0.536626 |
| event_threshold_0.5    | C(rel_t, Treatment(reference=-1))[-4]:treated:disp_05:closure_duration_days |  0.000583478 | 0.00195809  | 0.765716    | 7296 | 0.536626 |
| event_threshold_0.5    | C(rel_t, Treatment(reference=-1))[-3]:treated:disp_05:closure_duration_days |  0.001628    | 0.00175121  | 0.352557    | 7296 | 0.536626 |
| event_threshold_0.5    | C(rel_t, Treatment(reference=-1))[-2]:treated:disp_05:closure_duration_days |  0.00191607  | 0.00176184  | 0.276798    | 7296 | 0.536626 |
| event_threshold_0.5    | C(rel_t, Treatment(reference=-1))[-1]:treated:disp_05:closure_duration_days |  0.00299324  | 0.0017099   | 0.0800271   | 7296 | 0.536626 |
| event_threshold_0.5    | C(rel_t, Treatment(reference=-1))[1]:treated:disp_05:closure_duration_days  |  8.12447e-05 | 0.00120115  | 0.946073    | 7296 | 0.536626 |
| event_threshold_0.5    | C(rel_t, Treatment(reference=-1))[2]:treated:disp_05:closure_duration_days  |  0.00288207  | 0.00153125  | 0.0598143   | 7296 | 0.536626 |
| event_threshold_0.5    | C(rel_t, Treatment(reference=-1))[3]:treated:disp_05:closure_duration_days  |  0.0052658   | 0.00157984  | 0.000858795 | 7296 | 0.536626 |
| event_threshold_0.5    | C(rel_t, Treatment(reference=-1))[4]:treated:disp_05:closure_duration_days  |  0.00153544  | 0.00164617  | 0.350959    | 7296 | 0.536626 |
| event_score_continuous | C(rel_t, Treatment(reference=-1))[-4]:treated:displacement_prob             |  0.0325      | 0.0370589   | 0.380497    | 7296 | 0.540085 |
| event_score_continuous | C(rel_t, Treatment(reference=-1))[-3]:treated:displacement_prob             |  0.0454502   | 0.0352124   | 0.196793    | 7296 | 0.540085 |
| event_score_continuous | C(rel_t, Treatment(reference=-1))[-2]:treated:displacement_prob             |  0.0418994   | 0.0319291   | 0.189431    | 7296 | 0.540085 |
| event_score_continuous | C(rel_t, Treatment(reference=-1))[-1]:treated:displacement_prob             |  0.0500776   | 0.0339951   | 0.140728    | 7296 | 0.540085 |
| event_score_continuous | C(rel_t, Treatment(reference=-1))[1]:treated:displacement_prob              |  0.0181732   | 0.0240591   | 0.450035    | 7296 | 0.540085 |
| event_score_continuous | C(rel_t, Treatment(reference=-1))[2]:treated:displacement_prob              |  0.0650629   | 0.0304268   | 0.0324892   | 7296 | 0.540085 |
| event_score_continuous | C(rel_t, Treatment(reference=-1))[3]:treated:displacement_prob              |  0.0958745   | 0.0270029   | 0.00038446  | 7296 | 0.540085 |
| event_score_continuous | C(rel_t, Treatment(reference=-1))[4]:treated:displacement_prob              |  0.0558528   | 0.0309899   | 0.0714994   | 7296 | 0.540085 |