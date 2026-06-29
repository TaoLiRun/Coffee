# Displacement Effect Estimation Summary

- Sample rows: 6,308
- Unique members: 1,577
- Unique closures: 1
- Event FE units: 1,577
- Relative periods: [-2, -1, 1, 2]
- Estimation mode: separate_effect=true
- Closure event: `dept_182_closure_2021-08-03`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |        coef |         se |      pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 6308 |   0.0148182 |  0.00377294 | 0.00375297 | 0.314896    |
| binary_collapsed | post_X_disp           | 6308 |   0.0148182 | -0.0290862  | 0.00625026 | 3.53502e-06 |
| binary_collapsed | post_X_treated_X_disp | 6308 |   0.0148182 |  0.025999   | 0.0153032  | 0.089531    |

## Score Spec
| spec            | term                   |    n |   r2_within |       coef |         se |      pvalue |
|:----------------|:-----------------------|-----:|------------:|-----------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 6308 |   0.0197607 |  0.0110869 | 0.00499427 | 0.0265659   |
| score_collapsed | post_X_score           | 6308 |   0.0197607 | -0.0469385 | 0.00906025 | 2.49555e-07 |
| score_collapsed | post_X_treated_X_score | 6308 |   0.0197607 |  0.0462104 | 0.0264569  | 0.0808968   |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0037879   | 0.0053424  | 0.478414    | 6308 |  0.00114877 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0113426   | 0.00527869 | 0.0318056   | 6308 |  0.00114877 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00989497  | 0.00490813 | 0.0439655   | 6308 |  0.00114877 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.000176288 | 0.00384005 | 0.96339     | 6308 |  0.0206627  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00957064  | 0.00512782 | 0.0621691   | 6308 |  0.0206627  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00184847  | 0.00430066 | 0.667392    | 6308 |  0.0206627  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0118801   | 0.0191727  | 0.535587    | 6308 |  0.0206627  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.010645    | 0.0161372  | 0.509573    | 6308 |  0.0206627  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.0532332   | 0.0159123  | 0.000840907 | 6308 |  0.0206627  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0169385   | 0.00788583 | 0.0318688   | 6308 |  0.0206627  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0176351   | 0.00744524 | 0.0179735   | 6308 |  0.0206627  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0235989   | 0.00792275 | 0.00293972  | 6308 |  0.0206627  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00329345  | 0.00594611 | 0.579738    | 6308 |  0.0258672  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0128845   | 0.00575561 | 0.0253206   | 6308 |  0.0258672  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0125827   | 0.005277   | 0.017223    | 6308 |  0.0258672  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.0155246   | 0.0316197  | 0.623509    | 6308 |  0.0258672  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.0338424   | 0.0287211  | 0.238851    | 6308 |  0.0258672  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.0741029   | 0.0233628  | 0.00154399  | 6308 |  0.0258672  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0300583   | 0.0110062  | 0.00638394  | 6308 |  0.0258672  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0276892   | 0.0107259  | 0.00992585  | 6308 |  0.0258672  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0361296   | 0.0114414  | 0.00161989  | 6308 |  0.0258672  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                1 |  0.502716   | 0.478309 | 6308 |
| event_binary_B | pretrend_baseline_joint_zero       |                1 |  0.00210751 | 0.963384 | 6308 |
| event_binary_B | pretrend_displacement_joint_zero   |                1 |  0.38395    | 0.535497 | 6308 |
| event_score_C  | pretrend_score_baseline_joint_zero |                1 |  0.306786   | 0.579659 | 6308 |
| event_score_C  | pretrend_score_slope_joint_zero    |                1 |  0.241061   | 0.623441 | 6308 |