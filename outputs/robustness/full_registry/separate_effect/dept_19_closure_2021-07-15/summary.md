# Displacement Effect Estimation Summary

- Sample rows: 26,408
- Unique members: 3,301
- Unique closures: 1
- Event FE units: 3,301
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_19_closure_2021-07-15`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |     n |   r2_within |        coef |         se |   pvalue |
|:-----------------|:----------------------|------:|------------:|------------:|-----------:|---------:|
| binary_collapsed | post_X_treated        | 26408 |   0.0278262 |  0.0021203  | 0.00229038 | 0.354648 |
| binary_collapsed | post_X_disp           | 26408 |   0.0278262 | -0.0614673  | 0.00500645 | 0        |
| binary_collapsed | post_X_treated_X_disp | 26408 |   0.0278262 |  0.00778394 | 0.0130563  | 0.551095 |

## Score Spec
| spec            | term                   |     n |   r2_within |        coef |         se |   pvalue |
|:----------------|:-----------------------|------:|------------:|------------:|-----------:|---------:|
| score_collapsed | post_X_treated         | 26408 |   0.0389655 |  0.00265851 | 0.00436775 | 0.542786 |
| score_collapsed | post_X_score           | 26408 |   0.0389655 | -0.104092   | 0.00731486 | 0        |
| score_collapsed | post_X_treated_X_score | 26408 |   0.0389655 |  0.0122178  | 0.0193514  | 0.527846 |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  2.77962e-05 | 0.00530998 | 0.995824    | 26408 |  0.00234709 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0254036   | 0.00437082 | 6.75653e-09 | 26408 |  0.00234709 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00662455  | 0.00432466 | 0.125666    | 26408 |  0.00234709 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00969702  | 0.00452984 | 0.0323715   | 26408 |  0.00234709 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00733978  | 0.00474091 | 0.121675    | 26408 |  0.00234709 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.000733967 | 0.00481396 | 0.878828    | 26408 |  0.00234709 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0023543   | 0.00451081 | 0.601758    | 26408 |  0.00234709 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.00298256  | 0.00417845 | 0.475403    | 26408 |  0.038194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0170144   | 0.0033052  | 2.79035e-07 | 26408 |  0.038194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00080488  | 0.00380495 | 0.832483    | 26408 |  0.038194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00670773  | 0.00323603 | 0.0382661   | 26408 |  0.038194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00444481  | 0.0039435  | 0.259772    | 26408 |  0.038194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.00299708  | 0.0035507  | 0.398686    | 26408 |  0.038194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00706063  | 0.00365501 | 0.0534737   | 26408 |  0.038194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.019555    | 0.0251224  | 0.436396    | 26408 |  0.038194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             | -0.0597932   | 0.019911   | 0.00269318  | 26408 |  0.038194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.0332483   | 0.0182186  | 0.0680971   | 26408 |  0.038194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0457932   | 0.0193081  | 0.0177632   | 26408 |  0.038194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.0072054   | 0.0194924  | 0.711666    | 26408 |  0.038194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              | -0.00111802  | 0.0234383  | 0.961958    | 26408 |  0.038194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.0117659   | 0.0201823  | 0.559946    | 26408 |  0.038194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.000175931 | 0.00902601 | 0.98445     | 26408 |  0.038194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                | -0.0145429   | 0.00809027 | 0.0723359   | 26408 |  0.038194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0132682   | 0.00723717 | 0.0668411   | 26408 |  0.038194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.074672    | 0.00787681 | 0           | 26408 |  0.038194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0739823   | 0.00795115 | 0           | 26408 |  0.038194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0450231   | 0.00795127 | 1.62075e-08 | 26408 |  0.038194   |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0536423   | 0.00801495 | 2.56262e-11 | 26408 |  0.038194   |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00379961  | 0.00816382 | 0.641661    | 26408 |  0.0540377  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0380011   | 0.00645899 | 4.42018e-09 | 26408 |  0.0540377  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.010766    | 0.00634379 | 0.0897721   | 26408 |  0.0540377  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.0244688   | 0.00614178 | 6.92298e-05 | 26408 |  0.0540377  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.000899407 | 0.00663989 | 0.89226     | 26408 |  0.0540377  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.00496753  | 0.00740859 | 0.502581    | 26408 |  0.0540377  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00579651  | 0.0066344  | 0.382343    | 26408 |  0.0540377  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.0363682   | 0.0333897  | 0.276143    | 26408 |  0.0540377  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            | -0.0951213   | 0.0270997  | 0.000454021 | 26408 |  0.0540377  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.0434729   | 0.0246841  | 0.0783026   | 26408 |  0.0540377  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.0707421   | 0.026712   | 0.00812761  | 26408 |  0.0540377  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.00341437  | 0.0282332  | 0.90375     | 26408 |  0.0540377  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.00149532  | 0.0313956  | 0.962015    | 26408 |  0.0540377  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.0124776   | 0.0278264  | 0.653886    | 26408 |  0.0540377  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.00483292  | 0.0127648  | 0.705       | 26408 |  0.0540377  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered | -0.0407139   | 0.0113981  | 0.000359357 | 26408 |  0.0540377  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0129469   | 0.0103347  | 0.21038     | 26408 |  0.0540377  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.135788    | 0.0116001  | 0           | 26408 |  0.0540377  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.133135    | 0.0115797  | 0           | 26408 |  0.0540377  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.0858991   | 0.0116528  | 2.12053e-13 | 26408 |  0.0540377  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.0941473   | 0.0118644  | 2.88658e-15 | 26408 |  0.0540377  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |      pvalue |     n |
|:---------------|:-----------------------------------|-----------------:|------------:|------------:|------:|
| event_att      | pretrend_att_joint_zero            |                3 |     45.8243 | 6.18098e-10 | 26408 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |     36.8925 | 4.84881e-08 | 26408 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |     18.5718 | 0.000335187 | 26408 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |     52.6504 | 2.1766e-11  | 26408 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |     23.436  | 3.27551e-05 | 26408 |