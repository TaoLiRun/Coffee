# Displacement Effect Estimation Summary

- Sample rows: 17,744
- Unique members: 2,218
- Unique closures: 1
- Event FE units: 2,218
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_121_closure_2021-08-03`
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Length-heterogeneity event-study spec skipped: true
- Model type: DDD


## Binary Specs
| spec             | term                  |    n |   r2_within |       coef |        se |     pvalue |
|:-----------------|:----------------------|-----:|------------:|-----------:|----------:|-----------:|
| binary_collapsed | post_X_treated        | 5249 |  0.00294284 |  0.145839  | 0.0481913 | 0.00252488 |
| binary_collapsed | post_X_disp           | 5249 |  0.00294284 |  0.0379998 | 0.0296325 | 0.199943   |
| binary_collapsed | post_X_treated_X_disp | 5249 |  0.00294284 | -0.178193  | 0.0596204 | 0.00285375 |

## Score Spec
| spec            | term                   |    n |   r2_within |       coef |        se |    pvalue |
|:----------------|:-----------------------|-----:|------------:|-----------:|----------:|----------:|
| score_collapsed | post_X_treated         | 5249 |  0.00171658 |  0.0914373 | 0.041262  | 0.0268636 |
| score_collapsed | post_X_score           | 5249 |  0.00171658 |  0.074639  | 0.0451591 | 0.0986135 |
| score_collapsed | post_X_treated_X_score | 5249 |  0.00171658 | -0.18087   | 0.0908626 | 0.0467363 |

## Event-study Specs
| spec           | term                                                              |        coef |        se |     pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|------------:|----------:|-----------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0684062  | 0.0579412 | 0.237973   | 5249 |  0.00449124 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.0689763  | 0.0576401 | 0.231654   | 5249 |  0.00449124 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0662195  | 0.0564508 | 0.240993   | 5249 |  0.00449124 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.12017    | 0.0608956 | 0.0486645  | 5249 |  0.00449124 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.077964   | 0.0614256 | 0.204583   | 5249 |  0.00449124 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0637315  | 0.0627789 | 0.310213   | 5249 |  0.00449124 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0167688  | 0.0600375 | 0.780055   | 5249 |  0.00449124 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0481244  | 0.099486  | 0.628659   | 5249 |  0.0121108  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.120582   | 0.103378  | 0.243659   | 5249 |  0.0121108  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.12419    | 0.102586  | 0.226275   | 5249 |  0.0121108  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.253893   | 0.10117   | 0.0122089  | 5249 |  0.0121108  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.265358   | 0.103855  | 0.0107296  | 5249 |  0.0121108  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.2007     | 0.105343  | 0.0569743  | 5249 |  0.0121108  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0523181  | 0.106161  | 0.622224   | 5249 |  0.0121108  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             | -0.0222166  | 0.121031  | 0.854386   | 5249 |  0.0121108  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             | -0.0835239  | 0.123384  | 0.498562   | 5249 |  0.0121108  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.0943347  | 0.121366  | 0.43714    | 5249 |  0.0121108  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.246099   | 0.124749  | 0.0487357  | 5249 |  0.0121108  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.320498   | 0.127628  | 0.0121538  | 5249 |  0.0121108  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              | -0.225561   | 0.130313  | 0.0837057  | 5249 |  0.0121108  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.106018   | 0.126529  | 0.402245   | 5249 |  0.0121108  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.0570014  | 0.0468388 | 0.223838   | 5249 |  0.0121108  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.0603648  | 0.0495762 | 0.223592   | 5249 |  0.0121108  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0352768  | 0.0497919 | 0.478771   | 5249 |  0.0121108  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0203184  | 0.0548543 | 0.71114    | 5249 |  0.0121108  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.176122   | 0.0581101 | 0.00248717 | 5249 |  0.0121108  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.125668   | 0.0601374 | 0.0368413  | 5249 |  0.0121108  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.0369156  | 0.0567349 | 0.515377   | 5249 |  0.0121108  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.115995   | 0.0860964 | 0.178128   | 5249 |  0.0110878  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.0334663  | 0.0880247 | 0.703865   | 5249 |  0.0110878  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0989405  | 0.0913274 | 0.27885    | 5249 |  0.0110878  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.155697   | 0.0846298 | 0.0660359  | 5249 |  0.0110878  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.116562   | 0.0871544 | 0.18132    | 5249 |  0.0110878  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0975049  | 0.0888269 | 0.272542   | 5249 |  0.0110878  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0218342  | 0.0903301 | 0.809039   | 5249 |  0.0110878  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.208749   | 0.189808  | 0.271628   | 5249 |  0.0110878  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.123596   | 0.185566  | 0.505499   | 5249 |  0.0110878  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.0994933  | 0.196221  | 0.612208   | 5249 |  0.0110878  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.184821   | 0.182468  | 0.3113     | 5249 |  0.0110878  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.107655   | 0.185279  | 0.561312   | 5249 |  0.0110878  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             | -0.133067   | 0.187779  | 0.478678   | 5249 |  0.0110878  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.040831   | 0.192681  | 0.83221    | 5249 |  0.0110878  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered |  0.0555489  | 0.0751262 | 0.459794   | 5249 |  0.0110878  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.10522    | 0.0789406 | 0.1828     | 5249 |  0.0110878  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.06104    | 0.0800313 | 0.445781   | 5249 |  0.0110878  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.00112439 | 0.0823423 | 0.989107   | 5249 |  0.0110878  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  |  0.255475   | 0.0887398 | 0.00405597 | 5249 |  0.0110878  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  |  0.166706   | 0.0888947 | 0.0609739  | 5249 |  0.0110878  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  |  0.113693   | 0.0884185 | 0.198724   | 5249 |  0.0110878  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |    pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|----------:|-----:|
| event_att      | pretrend_att_joint_zero            |                3 |    9.37502  | 0.0246988 | 5249 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |    5.01399  | 0.170776  | 5249 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |    0.878757 | 0.830551  | 5249 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |    8.02014  | 0.0455973 | 5249 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |    3.66347  | 0.300171  | 5249 |