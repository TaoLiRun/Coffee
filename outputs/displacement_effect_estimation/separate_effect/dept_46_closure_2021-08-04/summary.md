# Displacement Effect Estimation Summary

- Sample rows: 21,760
- Unique members: 2,720
- Unique closures: 1
- Event FE units: 2,720
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_46_closure_2021-08-04`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |     n |   r2_within |        coef |         se |   pvalue |
|:-----------------|:----------------------|------:|------------:|------------:|-----------:|---------:|
| binary_collapsed | post_X_treated        | 21760 |   0.0162882 |  0.00434657 | 0.00280756 | 0.121698 |
| binary_collapsed | post_X_disp           | 21760 |   0.0162882 | -0.0369421  | 0.00409236 | 0        |
| binary_collapsed | post_X_treated_X_disp | 21760 |   0.0162882 |  0.0114863  | 0.0100975  | 0.255411 |

## Score Spec
| spec            | term                   |     n |   r2_within |        coef |         se |    pvalue |
|:----------------|:-----------------------|------:|------------:|------------:|-----------:|----------:|
| score_collapsed | post_X_treated         | 21760 |   0.0215689 |  0.00641641 | 0.00358321 | 0.0734549 |
| score_collapsed | post_X_score           | 21760 |   0.0215689 | -0.0564593  | 0.0058102  | 0         |
| score_collapsed | post_X_treated_X_score | 21760 |   0.0215689 |  0.0134517  | 0.0135738  | 0.32177   |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00359446  | 0.00463156 | 0.43777     | 21760 |  0.00206491 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.00915361  | 0.00537647 | 0.0887699   | 21760 |  0.00206491 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0159463   | 0.00468489 | 0.000674237 | 21760 |  0.00206491 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00227921  | 0.00418141 | 0.585741    | 21760 |  0.00206491 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0156808   | 0.00480429 | 0.00111243  | 21760 |  0.00206491 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0287053   | 0.00493762 | 6.82753e-09 | 21760 |  0.00206491 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0187742   | 0.00424791 | 1.02741e-05 | 21760 |  0.00206491 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0037441   | 0.003667   | 0.307332    | 21760 |  0.0247945  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.000952777 | 0.00369839 | 0.79672     | 21760 |  0.0247945  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00542319  | 0.00307534 | 0.0779381   | 21760 |  0.0247945  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.0049765   | 0.00282905 | 0.0786781   | 21760 |  0.0247945  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.00795723  | 0.00421014 | 0.0588622   | 21760 |  0.0247945  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0107856   | 0.00420524 | 0.0103766   | 21760 |  0.0247945  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00625179  | 0.00339539 | 0.065693    | 21760 |  0.0247945  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.0397364   | 0.0158304  | 0.0121262   | 21760 |  0.0247945  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0462604   | 0.0197361  | 0.0191522   | 21760 |  0.0247945  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0591705   | 0.0158638  | 0.000195466 | 21760 |  0.0247945  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.0308108   | 0.0163714  | 0.0599444   | 21760 |  0.0247945  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.0322736   | 0.0163134  | 0.0479899   | 21760 |  0.0247945  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.0747551   | 0.0167115  | 8.01896e-06 | 21760 |  0.0247945  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.0532731   | 0.0148863  | 0.000351393 | 21760 |  0.0247945  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                |  0.0156673   | 0.00622084 | 0.011842    | 21760 |  0.0247945  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.0234661   | 0.00645536 | 0.000282981 | 21760 |  0.0247945  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0295014   | 0.00594018 | 7.24228e-07 | 21760 |  0.0247945  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0117352   | 0.00564647 | 0.0377726   | 21760 |  0.0247945  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0141747   | 0.00587351 | 0.0158736   | 21760 |  0.0247945  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0332837   | 0.00564366 | 4.14571e-09 | 21760 |  0.0247945  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0199398   | 0.0062097  | 0.00133783  | 21760 |  0.0247945  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.010111    | 0.00533584 | 0.0582088   | 21760 |  0.0313651  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.0164781   | 0.00633632 | 0.00935727  | 21760 |  0.0313651  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0264189   | 0.00507984 | 2.13266e-07 | 21760 |  0.0313651  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00423838  | 0.00536586 | 0.429668    | 21760 |  0.0313651  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0184908   | 0.0056373  | 0.00105089  | 21760 |  0.0313651  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0333566   | 0.00583714 | 1.21954e-08 | 21760 |  0.0313651  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0225878   | 0.00501306 | 6.89168e-06 | 21760 |  0.0313651  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.065437    | 0.019586   | 0.000846017 | 21760 |  0.0313651  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.0658167   | 0.0230907  | 0.0043999   | 21760 |  0.0313651  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.102833    | 0.0197075  | 1.94499e-07 | 21760 |  0.0313651  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.041117    | 0.0212237  | 0.052811    | 21760 |  0.0313651  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.0594127   | 0.0200953  | 0.00313778  | 21760 |  0.0313651  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.10732     | 0.0230033  | 3.22867e-06 | 21760 |  0.0313651  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.0800438   | 0.0188791  | 2.31173e-05 | 21760 |  0.0313651  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered |  0.0206491   | 0.00838039 | 0.013802    | 21760 |  0.0313651  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.0321445   | 0.00878028 | 0.000256024 | 21760 |  0.0313651  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0358749   | 0.00812025 | 1.03534e-05 | 21760 |  0.0313651  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0185698   | 0.00798108 | 0.0200527   | 21760 |  0.0313651  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.027143    | 0.00807894 | 0.000790983 | 21760 |  0.0313651  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.0552997   | 0.00797233 | 5.00533e-12 | 21760 |  0.0313651  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.036156    | 0.00874548 | 3.66892e-05 | 21760 |  0.0313651  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |      pvalue |     n |
|:---------------|:-----------------------------------|-----------------:|------------:|------------:|------:|
| event_att      | pretrend_att_joint_zero            |                3 |    12.6348  | 0.00549667  | 21760 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |     5.50367 | 0.138419    | 21760 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |    14.5282  | 0.00226767  | 21760 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |    27.2907  | 5.11643e-06 | 21760 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |    28.0563  | 3.53447e-06 | 21760 |