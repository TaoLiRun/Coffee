# Displacement Effect Estimation Summary

- Sample rows: 2,160
- Unique members: 540
- Unique closures: 1
- Event FE units: 540
- Relative periods: [-2, -1, 1, 2]
- Estimation mode: separate_effect=true
- Closure event: `dept_246_closure_2021-07-27`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |        coef |         se |      pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 2160 |   0.0540681 | -0.00734202 | 0.00435554 | 0.0924375   |
| binary_collapsed | post_X_disp           | 2160 |   0.0540681 | -0.0437207  | 0.00850313 | 3.81546e-07 |
| binary_collapsed | post_X_treated_X_disp | 2160 |   0.0540681 | -0.0765202  | 0.0721407  | 0.289298    |

## Score Spec
| spec            | term                   |    n |   r2_within |       coef |        se |      pvalue |
|:----------------|:-----------------------|-----:|------------:|-----------:|----------:|------------:|
| score_collapsed | post_X_treated         | 2160 |   0.0725432 | -0.0432361 | 0.0247112 | 0.0807465   |
| score_collapsed | post_X_score           | 2160 |   0.0725432 | -0.0611264 | 0.0111801 | 6.99359e-08 |
| score_collapsed | post_X_treated_X_score | 2160 |   0.0725432 | -0.15438   | 0.103334  | 0.135761    |

## Event-study Specs
| spec           | term                                                              |        coef |         se |      pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|------------:|-----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0011249  | 0.00792697 | 0.887206    | 2160 |  0.00198528 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.0144582  | 0.00732238 | 0.0488318   | 2160 |  0.00198528 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0112159  | 0.0146137  | 0.443126    | 2160 |  0.00198528 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00422654 | 0.00575286 | 0.46285     | 2160 |  0.0832568  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00867722 | 0.00523346 | 0.0978939   | 2160 |  0.0832568  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00178027 | 0.00626392 | 0.776358    | 2160 |  0.0832568  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.00168783 | 0.0444048  | 0.969694    | 2160 |  0.0832568  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0551292  | 0.0411423  | 0.180822    | 2160 |  0.0832568  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.0995991  | 0.105242   | 0.344377    | 2160 |  0.0832568  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0529699  | 0.0133145  | 7.88789e-05 | 2160 |  0.0832568  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0085849  | 0.0116533  | 0.461629    | 2160 |  0.0832568  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0258865  | 0.0115738  | 0.0257181   | 2160 |  0.0832568  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00903961 | 0.015322   | 0.555455    | 2160 |  0.0987376  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.032619   | 0.0149516  | 0.0295678   | 2160 |  0.0987376  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0448136  | 0.0391522  | 0.252883    | 2160 |  0.0987376  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.0270759  | 0.0573868  | 0.637251    | 2160 |  0.0987376  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.100029   | 0.0608164  | 0.100601    | 2160 |  0.0987376  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.181656   | 0.165508   | 0.272886    | 2160 |  0.0987376  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0617268  | 0.0193214  | 0.00148141  | 2160 |  0.0987376  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0191322  | 0.0167306  | 0.25332     | 2160 |  0.0987376  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0413938  | 0.0158045  | 0.00906394  | 2160 |  0.0987376  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                1 |  0.0201377  | 0.887153 | 2160 |
| event_binary_B | pretrend_baseline_joint_zero       |                1 |  0.539764   | 0.462531 | 2160 |
| event_binary_B | pretrend_displacement_joint_zero   |                1 |  0.00144476 | 0.96968  | 2160 |
| event_score_C  | pretrend_score_baseline_joint_zero |                1 |  0.34807    | 0.555208 | 2160 |
| event_score_C  | pretrend_score_slope_joint_zero    |                1 |  0.222608   | 0.63706  | 2160 |