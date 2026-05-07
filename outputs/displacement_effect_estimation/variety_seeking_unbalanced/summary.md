# Displacement Effect Estimation Summary

- Sample rows: 321,184
- Unique members: 40,148
- Unique closures: 18
- Event FE units: 40,148
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=false
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Model type: DDD


## Binary Specs
| spec             | term                  |     n |   r2_within |       coef |         se |      pvalue |
|:-----------------|:----------------------|------:|------------:|-----------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 99644 | 0.000538359 |  0.03129   | 0.0119975  | 0.00911174  |
| binary_collapsed | post_X_disp           | 99644 | 0.000538359 |  0.0380842 | 0.00638979 | 2.55586e-09 |
| binary_collapsed | post_X_treated_X_disp | 99644 | 0.000538359 | -0.0414886 | 0.0145008  | 0.00422522  |

## Score Spec
| spec            | term                   |     n |   r2_within |       coef |         se |      pvalue |
|:----------------|:-----------------------|------:|------------:|-----------:|-----------:|------------:|
| score_collapsed | post_X_treated         | 99644 | 0.000410752 |  0.0189683 | 0.0102232  | 0.0635482   |
| score_collapsed | post_X_score           | 99644 | 0.000410752 |  0.0532797 | 0.00980858 | 5.62981e-08 |
| score_collapsed | post_X_treated_X_score | 99644 | 0.000410752 | -0.0452324 | 0.0220638  | 0.0403681   |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0126539   | 0.0126537  | 0.317311    | 99644 |  0.00031151 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0044647   | 0.012742   | 0.726047    | 99644 |  0.00031151 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.024399    | 0.012186   | 0.045273    | 99644 |  0.00031151 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0281551   | 0.0129847  | 0.0301436   | 99644 |  0.00031151 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00874969  | 0.0132084  | 0.507701    | 99644 |  0.00031151 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0254341   | 0.0131947  | 0.0539169   | 99644 |  0.00031151 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0166521   | 0.0132254  | 0.208005    | 99644 |  0.00031151 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0261337   | 0.0227892  | 0.251493    | 99644 |  0.00148018 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.021228    | 0.0232691  | 0.361629    | 99644 |  0.00148018 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0360356   | 0.0236215  | 0.127137    | 99644 |  0.00148018 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0359681   | 0.0233805  | 0.123969    | 99644 |  0.00148018 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0148887   | 0.0226734  | 0.511408    | 99644 |  0.00148018 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0123741   | 0.0231427  | 0.592873    | 99644 |  0.00148018 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0052464   | 0.0233285  | 0.822065    | 99644 |  0.00148018 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0223092   | 0.0271815  | 0.411797    | 99644 |  0.00148018 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0264193   | 0.0275981  | 0.338434    | 99644 |  0.00148018 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.016017    | 0.0273105  | 0.55756     | 99644 |  0.00148018 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0119598   | 0.0279029  | 0.668202    | 99644 |  0.00148018 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.0394052   | 0.0278301  | 0.156812    | 99644 |  0.00148018 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              | -0.020707    | 0.028024   | 0.459973    | 99644 |  0.00148018 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.0363733   | 0.0281478  | 0.196292    | 99644 |  0.00148018 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.0399467   | 0.011699   | 0.000640004 | 99644 |  0.00148018 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.0330551   | 0.0116509  | 0.00455615  | 99644 |  0.00148018 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0158715   | 0.012023   | 0.186815    | 99644 |  0.00148018 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  0.0291025   | 0.0122169  | 0.0172195   | 99644 |  0.00148018 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.0624086   | 0.0121763  | 2.99282e-07 | 99644 |  0.00148018 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.0702858   | 0.0126132  | 2.54002e-08 | 99644 |  0.00148018 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.0837106   | 0.0124958  | 2.14451e-11 | 99644 |  0.00148018 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0245447   | 0.0229722  | 0.285328    | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0148172   | 0.0236073  | 0.530236    | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0368376   | 0.0240334  | 0.125346    | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.032591    | 0.0240381  | 0.175173    | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0173265   | 0.0228783  | 0.448857    | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0111218   | 0.023395   | 0.634511    | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00705575  | 0.0235291  | 0.764276    | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.000347314 | 0.0291013  | 0.990478    | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.00107692  | 0.0295946  | 0.970972    | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.00642209  | 0.0290553  | 0.825071    | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0302667   | 0.0306939  | 0.324103    | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.0479089   | 0.0296387  | 0.106014    | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              | -0.0245586   | 0.0301819  | 0.415833    | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.0486014   | 0.0299694  | 0.104881    | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.0410108   | 0.0117754  | 0.000497168 | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.0354383   | 0.0117062  | 0.00246999  | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.014792    | 0.0120865  | 0.221025    | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  0.0299184   | 0.0123271  | 0.0152299   | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.0666827   | 0.0122507  | 5.28647e-08 | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.0728103   | 0.0127166  | 1.04334e-08 | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.0876226   | 0.0125818  | 3.38995e-12 | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_len              | -0.0059651   | 0.0188185  | 0.751261    | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_len              | -0.0356196   | 0.0188062  | 0.0582326   | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_len              |  0.0143933   | 0.0180621  | 0.42553     | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_len               |  0.00611778  | 0.0184874  | 0.740711    | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_len               | -0.0331473   | 0.0180524  | 0.0663451   | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated_X_len               | -0.0190087   | 0.0182721  | 0.298205    | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated_X_len               | -0.0423097   | 0.0195146  | 0.0301607   | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:disp_X_len                 | -5.86444e-05 | 0.00774733 | 0.99396     | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:disp_X_len                 | -0.00507167  | 0.0069547  | 0.46586     | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_X_len                 |  0.00770963  | 0.00595136 | 0.195181    | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_X_len                  | -0.0049444   | 0.00689439 | 0.473281    | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_X_len                  | -0.0216071   | 0.00738527 | 0.00344014  | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:disp_X_len                  | -0.0189054   | 0.00786812 | 0.0162787   | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:disp_X_len                  | -0.0357126   | 0.0099197  | 0.000318671 | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:tXdXlen                    |  0.0305064   | 0.0228581  | 0.182022    | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:tXdXlen                    |  0.0618842   | 0.0228632  | 0.00680015  | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:tXdXlen                    | -0.0072274   | 0.0216499  | 0.73851     | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:tXdXlen                     |  0.0173838   | 0.0230424  | 0.450602    | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:tXdXlen                     |  0.0475116   | 0.0229682  | 0.0385965   | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:tXdXlen                     |  0.0250338   | 0.0230091  | 0.276607    | 99644 |  0.00220727 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:tXdXlen                     |  0.0617345   | 0.0240988  | 0.0104215   | 99644 |  0.00220727 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0234991   | 0.0196808  | 0.232486    | 99644 |  0.00151693 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0160972   | 0.019939   | 0.41949     | 99644 |  0.00151693 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0365012   | 0.0206962  | 0.0778012   | 99644 |  0.00151693 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0251071   | 0.0198431  | 0.205781    | 99644 |  0.00151693 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.000783283 | 0.0192349  | 0.967518    | 99644 |  0.00151693 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0196627   | 0.0196059  | 0.315922    | 99644 |  0.00151693 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00382407  | 0.0198319  | 0.847098    | 99644 |  0.00151693 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.0361764   | 0.0412334  | 0.380302    | 99644 |  0.00151693 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.0378757   | 0.041573   | 0.362271    | 99644 |  0.00151693 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.0344195   | 0.0424195  | 0.417139    | 99644 |  0.00151693 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.0119583   | 0.0413822  | 0.772605    | 99644 |  0.00151693 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.0287379   | 0.0412575  | 0.486091    | 99644 |  0.00151693 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             | -0.0203105   | 0.0413398  | 0.623215    | 99644 |  0.00151693 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             | -0.0478      | 0.0418807  | 0.253741    | 99644 |  0.00151693 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered |  0.0758199   | 0.0181248  | 2.88482e-05 | 99644 |  0.00151693 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.0604875   | 0.0182     | 0.000890373 | 99644 |  0.00151693 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0343431   | 0.0189513  | 0.0699709   | 99644 |  0.00151693 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  |  0.0419253   | 0.0182568  | 0.0216608   | 99644 |  0.00151693 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  |  0.0971027   | 0.0184335  | 1.39353e-07 | 99644 |  0.00151693 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  |  0.113274    | 0.0189389  | 2.24979e-09 | 99644 |  0.00151693 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  |  0.139845    | 0.0187117  | 8.06022e-14 | 99644 |  0.00151693 |

## Pre-trend Joint Tests
| spec           | test                                    |   n_restrictions |   statistic |     pvalue |     n |
|:---------------|:----------------------------------------|-----------------:|------------:|-----------:|------:|
| event_att      | pretrend_att_joint_zero                 |                3 |     4.81892 | 0.185547   | 99644 |
| event_binary_B | pretrend_baseline_joint_zero            |                3 |     2.49069 | 0.476976   | 99644 |
| event_binary_B | pretrend_displacement_joint_zero        |                3 |     1.01653 | 0.797253   | 99644 |
| event_binary_D | pretrend_length_displacement_joint_zero |                3 |    11.5579  | 0.00906184 | 99644 |
| event_binary_D | pretrend_length_baseline_joint_zero     |                3 |     8.01332 | 0.0457373  | 99644 |
| event_score_C  | pretrend_score_baseline_joint_zero      |                3 |     3.33252 | 0.343142   | 99644 |
| event_score_C  | pretrend_score_slope_joint_zero         |                3 |     1.09579 | 0.77809    | 99644 |