# Displacement Effect Estimation Summary

- Sample rows: 21,152
- Unique members: 2,644
- Unique closures: 1
- Event FE units: 2,644
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_62_closure_2021-08-04`
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Length-heterogeneity event-study spec skipped: true
- Model type: DDD


## Binary Specs
| spec             | term                  |    n |   r2_within |      coef |        se |      pvalue |
|:-----------------|:----------------------|-----:|------------:|----------:|----------:|------------:|
| binary_collapsed | post_X_treated        | 5800 |  0.00362277 | 0.0127204 | 0.0678166 | 0.851239    |
| binary_collapsed | post_X_disp           | 5800 |  0.00362277 | 0.0861418 | 0.0241496 | 0.000372626 |
| binary_collapsed | post_X_treated_X_disp | 5800 |  0.00362277 | 0.0058941 | 0.0857624 | 0.945217    |

## Score Spec
| spec            | term                   |    n |   r2_within |       coef |        se |      pvalue |
|:----------------|:-----------------------|-----:|------------:|-----------:|----------:|------------:|
| score_collapsed | post_X_treated         | 5800 |  0.00451019 |  0.0291809 | 0.0569356 | 0.60836     |
| score_collapsed | post_X_score           | 5800 |  0.00451019 |  0.175465  | 0.0414404 | 2.43578e-05 |
| score_collapsed | post_X_treated_X_score | 5800 |  0.00451019 | -0.0450981 | 0.152851  | 0.768001    |

## Event-study Specs
| spec           | term                                                              |         coef |        se |      pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.0510843   | 0.0740437 | 0.490352    | 5800 |  0.00198642 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.053974    | 0.0742211 | 0.467216    | 5800 |  0.00198642 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.058104    | 0.072636  | 0.423878    | 5800 |  0.00198642 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0490199   | 0.0878498 | 0.576931    | 5800 |  0.00198642 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0489215   | 0.0854917 | 0.567249    | 5800 |  0.00198642 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.106788    | 0.093384  | 0.253       | 5800 |  0.00198642 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0210632   | 0.0848865 | 0.804065    | 5800 |  0.00198642 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.0774104   | 0.106192  | 0.466138    | 5800 |  0.00763954 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0940801   | 0.0988293 | 0.341281    | 5800 |  0.00763954 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0214159   | 0.0987241 | 0.828295    | 5800 |  0.00763954 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0877966   | 0.139063  | 0.527915    | 5800 |  0.00763954 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.1035      | 0.10009   | 0.301275    | 5800 |  0.00763954 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0929509   | 0.116087  | 0.423436    | 5800 |  0.00763954 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0422717   | 0.126688  | 0.738678    | 5800 |  0.00763954 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             | -0.0547857   | 0.142877  | 0.701445    | 5800 |  0.00763954 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0674659   | 0.139626  | 0.629033    | 5800 |  0.00763954 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.0736009   | 0.137807  | 0.593361    | 5800 |  0.00763954 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0741516   | 0.176394  | 0.674273    | 5800 |  0.00763954 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.126791    | 0.165991  | 0.445081    | 5800 |  0.00763954 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              | -0.0255618   | 0.18005   | 0.887123    | 5800 |  0.00763954 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.109741    | 0.165551  | 0.507508    | 5800 |  0.00763954 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.0515615   | 0.0474448 | 0.277317    | 5800 |  0.00763954 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.0304099   | 0.0469001 | 0.516829    | 5800 |  0.00763954 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0545983   | 0.0473328 | 0.248893    | 5800 |  0.00763954 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  0.0664502   | 0.0505546 | 0.188908    | 5800 |  0.00763954 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.133236    | 0.0487892 | 0.00639215  | 5800 |  0.00763954 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.156231    | 0.0510297 | 0.00224149  | 5800 |  0.00763954 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.122889    | 0.0505512 | 0.0151768   | 5800 |  0.00763954 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.0910022   | 0.0923971 | 0.324833    | 5800 |  0.0104114  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0620859   | 0.0806892 | 0.441752    | 5800 |  0.0104114  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -3.93767e-05 | 0.0939812 | 0.999666    | 5800 |  0.0104114  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.127396    | 0.128426  | 0.321369    | 5800 |  0.0104114  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0990872   | 0.0845409 | 0.241362    | 5800 |  0.0104114  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0691703   | 0.101601  | 0.496102    | 5800 |  0.0104114  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0439812   | 0.112413  | 0.695672    | 5800 |  0.0104114  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            | -0.161737    | 0.210824  | 0.443106    | 5800 |  0.0104114  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.0701449   | 0.183184  | 0.701834    | 5800 |  0.0104114  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.23148     | 0.215727  | 0.283437    | 5800 |  0.0104114  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.29613     | 0.27619   | 0.283807    | 5800 |  0.0104114  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.213689    | 0.26151   | 0.413984    | 5800 |  0.0104114  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             | -0.0440301   | 0.279682  | 0.874928    | 5800 |  0.0104114  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             | -0.0660875   | 0.281324  | 0.814307    | 5800 |  0.0104114  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered |  0.089684    | 0.0800617 | 0.262817    | 5800 |  0.0104114  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.0228144   | 0.0774014 | 0.768223    | 5800 |  0.0104114  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0940366   | 0.0813817 | 0.248073    | 5800 |  0.0104114  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  |  0.0786638   | 0.0789836 | 0.319437    | 5800 |  0.0104114  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  |  0.266797    | 0.0824975 | 0.00124773  | 5800 |  0.0104114  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  |  0.336022    | 0.0850159 | 8.10114e-05 | 5800 |  0.0104114  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  |  0.205692    | 0.0835036 | 0.0138811   | 5800 |  0.0104114  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                3 |     4.18413 | 0.242256 | 5800 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |     3.87991 | 0.274727 | 5800 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |     1.49388 | 0.683683 | 5800 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |     4.07401 | 0.253583 | 5800 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |     2.63208 | 0.451893 | 5800 |