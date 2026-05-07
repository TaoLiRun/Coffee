# Displacement Effect Estimation Summary

- Sample rows: 13,512
- Unique members: 1,689
- Unique closures: 1
- Event FE units: 1,689
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_238_closure_2021-07-24`
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Length-heterogeneity event-study spec skipped: true
- Model type: DDD


## Binary Specs
| spec             | term                  |    n |   r2_within |       coef |        se |   pvalue |
|:-----------------|:----------------------|-----:|------------:|-----------:|----------:|---------:|
| binary_collapsed | post_X_treated        | 5970 | 0.000114846 | 0.00663137 | 0.0454277 | 0.883964 |
| binary_collapsed | post_X_disp           | 5970 | 0.000114846 | 0.0106954  | 0.03349   | 0.749507 |
| binary_collapsed | post_X_treated_X_disp | 5970 | 0.000114846 | 0.00451419 | 0.0514189 | 0.930056 |

## Score Spec
| spec            | term                   |    n |   r2_within |       coef |        se |   pvalue |
|:----------------|:-----------------------|-----:|------------:|-----------:|----------:|---------:|
| score_collapsed | post_X_treated         | 5970 | 0.000223451 |  0.0215621 | 0.0388641 | 0.579128 |
| score_collapsed | post_X_score           | 5970 | 0.000223451 |  0.0396913 | 0.0456661 | 0.384928 |
| score_collapsed | post_X_treated_X_score | 5970 | 0.000223451 | -0.0290526 | 0.0734253 | 0.692413 |

## Event-study Specs
| spec           | term                                                              |        coef |        se |    pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|------------:|----------:|----------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.0533842  | 0.03768   | 0.156801  | 5970 |  0.00178366 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.0344356  | 0.0390184 | 0.377653  | 5970 |  0.00178366 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00864605 | 0.0361573 | 0.81105   | 5970 |  0.00178366 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0585059  | 0.0361345 | 0.105679  | 5970 |  0.00178366 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0552648  | 0.0399084 | 0.166368  | 5970 |  0.00178366 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0131925  | 0.0406244 | 0.745431  | 5970 |  0.00178366 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.00622059 | 0.0426627 | 0.884096  | 5970 |  0.00178366 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0897884  | 0.0835626 | 0.282808  | 5970 |  0.00669751 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.116138   | 0.0868152 | 0.181224  | 5970 |  0.00669751 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0133458  | 0.0860146 | 0.876722  | 5970 |  0.00669751 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.038809   | 0.0728352 | 0.594246  | 5970 |  0.00669751 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0338141  | 0.075528  | 0.654447  | 5970 |  0.00669751 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.119705   | 0.0820756 | 0.144968  | 5970 |  0.00669751 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.017569   | 0.0881406 | 0.842038  | 5970 |  0.00669751 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.182109   | 0.0935548 | 0.0518167 | 5970 |  0.00669751 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.192127   | 0.0969413 | 0.0477141 | 5970 |  0.00669751 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.00655445 | 0.0946983 | 0.944831  | 5970 |  0.00669751 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.124755   | 0.0837376 | 0.136526  | 5970 |  0.00669751 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.111295   | 0.0888033 | 0.210346  | 5970 |  0.00669751 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.136803   | 0.0943595 | 0.147369  | 5970 |  0.00669751 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.0199705  | 0.100773  | 0.842943  | 5970 |  0.00669751 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.0419267  | 0.0624763 | 0.502295  | 5970 |  0.00669751 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                |  0.062017   | 0.0657822 | 0.345988  | 5970 |  0.00669751 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.0607809  | 0.0678787 | 0.370731  | 5970 |  0.00669751 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0127817  | 0.053179  | 0.810097  | 5970 |  0.00669751 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.0401993  | 0.0581559 | 0.489549  | 5970 |  0.00669751 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.0177153  | 0.0620361 | 0.775261  | 5970 |  0.00669751 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.0864832  | 0.0624672 | 0.16647   | 5970 |  0.00669751 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0288674  | 0.068881  | 0.675224  | 5970 |  0.00622796 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.047889   | 0.0712345 | 0.501536  | 5970 |  0.00622796 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0363527  | 0.0728243 | 0.61774   | 5970 |  0.00622796 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0340981  | 0.0635481 | 0.591661  | 5970 |  0.00622796 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0101298  | 0.0643395 | 0.874922  | 5970 |  0.00622796 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0619294  | 0.0689875 | 0.369527  | 5970 |  0.00622796 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.014094   | 0.0755175 | 0.85198   | 5970 |  0.00622796 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.192713   | 0.128189  | 0.133005  | 5970 |  0.00622796 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.184805   | 0.131923  | 0.161509  | 5970 |  0.00622796 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.0608307  | 0.133351  | 0.64835   | 5970 |  0.00622796 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.046185   | 0.118835  | 0.697603  | 5970 |  0.00622796 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.150525   | 0.12558   | 0.230899  | 5970 |  0.00622796 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.107371   | 0.129754  | 0.408116  | 5970 |  0.00622796 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.0299704  | 0.142773  | 0.833768  | 5970 |  0.00622796 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.0505776  | 0.0835604 | 0.545104  | 5970 |  0.00622796 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered |  0.143947   | 0.0860244 | 0.094518  | 5970 |  0.00622796 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.0740432  | 0.0941732 | 0.431875  | 5970 |  0.00622796 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  |  0.0628422  | 0.0742604 | 0.397583  | 5970 |  0.00622796 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  |  0.0881646  | 0.0808748 | 0.275867  | 5970 |  0.00622796 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  |  0.0707398  | 0.0848856 | 0.404807  | 5970 |  0.00622796 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  |  0.101183   | 0.0878004 | 0.249371  | 5970 |  0.00622796 |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |    pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|----------:|-----:|
| event_att      | pretrend_att_joint_zero            |                3 |    3.69606  | 0.29621   | 5970 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |    2.4793   | 0.479043  | 5970 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |    7.07972  | 0.0693999 | 5970 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |    0.486146 | 0.921924  | 5970 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |    3.13348  | 0.371499  | 5970 |