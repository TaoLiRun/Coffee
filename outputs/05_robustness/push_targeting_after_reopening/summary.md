# Push Targeting After Reopening

- Selected member-events: 40,148
- Treatment member-events: 7,390
- Control member-events: 32,758
- Member-event-window rows: 160,592
- Filtered push records: 446,602

## Member-Event Counts

|   treated |   predicted_purchase_intention |     n |
|----------:|-------------------------------:|------:|
|         0 |                              0 | 23934 |
|         0 |                              1 |  8824 |
|         1 |                              0 |  5349 |
|         1 |                              1 |  2041 |

## Welch Mean Tests

|   treated | sample    | metric               | comparison          |   n_predicted_0 |   n_predicted_1 |   mean_predicted_0 |   mean_predicted_1 |   difference |          se |    t_stat |      df |       pvalue |     ci_low |      ci_high |
|----------:|:----------|:---------------------|:--------------------|----------------:|----------------:|-------------------:|-------------------:|-------------:|------------:|----------:|--------:|-------------:|-----------:|-------------:|
|         0 | control   | n_push               | predicted_1_minus_0 |           95736 |           35296 |           2.98094  |          2.02139   |  -0.959547   | 0.0194301   | -49.3846  | 56150.6 | 0            | -0.99763   | -0.921464    |
|         0 | control   | push_per_day         | predicted_1_minus_0 |           95736 |           35296 |           0.186094 |          0.101596  |  -0.0844981  | 0.000993351 | -85.0637  | 65594.4 | 0            | -0.0864451 | -0.0825512   |
|         0 | control   | n_push_with_coupon   | predicted_1_minus_0 |           95736 |           35296 |           0.688393 |          0.330717  |  -0.357676   | 0.00647563  | -55.2341  | 67670.5 | 0            | -0.370368  | -0.344983    |
|         0 | control   | share_push_coupon    | predicted_1_minus_0 |           95736 |           35296 |           0.158701 |          0.0517825 |  -0.106918   | 0.00114674  | -93.2364  | 96774.1 | 0            | -0.109166  | -0.10467     |
|         0 | control   | mean_coupon          | predicted_1_minus_0 |           95736 |           35296 |           6.35302  |          2.09043   |  -4.26259    | 0.0465874   | -91.4966  | 95800   | 0            | -4.3539    | -4.17127     |
|         0 | control   | n_push_with_discount | predicted_1_minus_0 |           95736 |           35296 |           0.699935 |          0.729658  |   0.0297225  | 0.00853073  |   3.48417 | 53135.6 | 0.000494063  |  0.0130022 |  0.0464428   |
|         0 | control   | share_push_discount  | predicted_1_minus_0 |           95736 |           35296 |           0.174463 |          0.161971  |  -0.0124919  | 0.00174115  |  -7.17455 | 60053   | 7.33797e-13  | -0.0159046 | -0.00907929  |
|         0 | control   | mean_discount        | predicted_1_minus_0 |           95736 |           35296 |           0.68542  |          0.648914  |  -0.0365055  | 0.00701886  |  -5.20106 | 58979.2 | 1.9882e-07   | -0.0502625 | -0.0227485   |
|         1 | treatment | n_push               | predicted_1_minus_0 |           21396 |            8164 |           3.1998   |          2.62237   |  -0.577437   | 0.0453858   | -12.7229  | 12296   | 7.53323e-37  | -0.6664    | -0.488474    |
|         1 | treatment | push_per_day         | predicted_1_minus_0 |           21396 |            8164 |           0.193488 |          0.11781   |  -0.0756775  | 0.00209593  | -36.107   | 14925.1 | 8.97463e-274 | -0.0797858 | -0.0715693   |
|         1 | treatment | n_push_with_coupon   | predicted_1_minus_0 |           21396 |            8164 |           0.737428 |          0.497305  |  -0.240122   | 0.0160113   | -14.997   | 14087.7 | 1.88128e-50  | -0.271507  | -0.208738    |
|         1 | treatment | share_push_coupon    | predicted_1_minus_0 |           21396 |            8164 |           0.161578 |          0.0725967 |  -0.0889818  | 0.00257567  | -34.5471  | 19895.7 | 4.85779e-254 | -0.0940303 | -0.0839332   |
|         1 | treatment | mean_coupon          | predicted_1_minus_0 |           21396 |            8164 |           6.40221  |          2.73155   |  -3.67067    | 0.102328    | -35.8715  | 20223   | 2.96752e-273 | -3.87124   | -3.4701      |
|         1 | treatment | n_push_with_discount | predicted_1_minus_0 |           21396 |            8164 |           0.794541 |          0.898089  |   0.103548   | 0.0196374   |   5.27301 | 12231.1 | 1.36492e-07  |  0.0650558 |  0.142041    |
|         1 | treatment | share_push_discount  | predicted_1_minus_0 |           21396 |            8164 |           0.191249 |          0.183709  |  -0.00753995 | 0.00372262  |  -2.02544 | 14059.5 | 0.0428407    | -0.0148368 | -0.000243127 |
|         1 | treatment | mean_discount        | predicted_1_minus_0 |           21396 |            8164 |           0.748727 |          0.739745  |  -0.00898146 | 0.0150974   |  -0.5949  | 13685.6 | 0.55192      | -0.0385745 |  0.0206116   |

## Closure-Window Adjusted Subgroup Regressions

| sample    | metric               |       coef |         se |       pvalue |     ci_low |    ci_high |      n |        r2 |
|:----------|:---------------------|-----------:|-----------:|-------------:|-----------:|-----------:|-------:|----------:|
| control   | n_push               | -1.37031   | 0.027682   | 0            | -1.42457   | -1.31606   | 131032 | 0.126383  |
| control   | push_per_day         | -0.0845169 | 0.00152747 | 0            | -0.0875107 | -0.0815231 | 131032 | 0.0592526 |
| control   | n_push_with_coupon   | -0.483497  | 0.0094641  | 0            | -0.502046  | -0.464948  | 131032 | 0.10206   |
| control   | share_push_coupon    | -0.116968  | 0.00160551 | 0            | -0.120115  | -0.113822  | 131032 | 0.0707009 |
| control   | mean_coupon          | -4.67438   | 0.0647985  | 0            | -4.80138   | -4.54738   | 131032 | 0.0714785 |
| control   | n_push_with_discount | -0.12481   | 0.00970706 | 7.78555e-38  | -0.143836  | -0.105785  | 131032 | 0.119973  |
| control   | share_push_discount  | -0.0320899 | 0.00203374 | 4.35587e-56  | -0.0360759 | -0.0281038 | 131032 | 0.064669  |
| control   | mean_discount        | -0.117997  | 0.0081386  | 1.23908e-47  | -0.133948  | -0.102046  | 131032 | 0.0689393 |
| treatment | n_push               | -1.31371   | 0.0667862  | 3.86624e-86  | -1.44461   | -1.18281   |  29560 | 0.144324  |
| treatment | push_per_day         | -0.0716906 | 0.00335034 | 1.39534e-101 | -0.0782571 | -0.065124  |  29560 | 0.0761027 |
| treatment | n_push_with_coupon   | -0.491297  | 0.0244729  | 1.21668e-89  | -0.539263  | -0.443331  |  29560 | 0.127579  |
| treatment | share_push_coupon    | -0.107363  | 0.00369482 | 1.23223e-185 | -0.114604  | -0.100121  |  29560 | 0.0911712 |
| treatment | mean_coupon          | -4.3012    | 0.146988   | 3.14416e-188 | -4.58929   | -4.01311   |  29560 | 0.0888238 |
| treatment | n_push_with_discount | -0.169915  | 0.0237322  | 8.08769e-13  | -0.216429  | -0.1234    |  29560 | 0.151061  |
| treatment | share_push_discount  | -0.040033  | 0.00455596 | 1.53677e-18  | -0.0489625 | -0.0311035 |  29560 | 0.0851213 |
| treatment | mean_discount        | -0.146577  | 0.0182603  | 9.97854e-16  | -0.182367  | -0.110788  |  29560 | 0.0883882 |

## Treatment-Control Difference in Subgroup Gaps

| metric               | term                         | interpretation                       |        coef |         se |      pvalue |      ci_low |      ci_high |      n |        r2 |
|:---------------------|:-----------------------------|:-------------------------------------|------------:|-----------:|------------:|------------:|-------------:|-------:|----------:|
| n_push               | predicted_purchase_intention | control subgroup gap                 | -1.37525    | 0.0276952  | 0           | -1.42953    | -1.32097     | 160592 | 0.128682  |
| n_push               | predicted_X_treated          | treatment minus control subgroup gap |  0.0525689  | 0.0717924  | 0.464025    | -0.0881415  |  0.193279    | 160592 | 0.128682  |
| push_per_day         | predicted_purchase_intention | control subgroup gap                 | -0.0844108  | 0.00152526 | 0           | -0.0874003  | -0.0814214   | 160592 | 0.0591898 |
| push_per_day         | predicted_X_treated          | treatment minus control subgroup gap |  0.00926865 | 0.00358801 | 0.00978811  |  0.00223627 |  0.016301    | 160592 | 0.0591898 |
| n_push_with_coupon   | predicted_purchase_intention | control subgroup gap                 | -0.485737   | 0.00945005 | 0           | -0.504259   | -0.467215    | 160592 | 0.101924  |
| n_push_with_coupon   | predicted_X_treated          | treatment minus control subgroup gap |  0.00857305 | 0.0253768  | 0.735491    | -0.0411645  |  0.0583106   | 160592 | 0.101924  |
| share_push_coupon    | predicted_purchase_intention | control subgroup gap                 | -0.117113   | 0.00160756 | 0           | -0.120263   | -0.113962    | 160592 | 0.0678966 |
| share_push_coupon    | predicted_X_treated          | treatment minus control subgroup gap |  0.00952062 | 0.00398986 | 0.0170233   |  0.00170064 |  0.0173406   | 160592 | 0.0678966 |
| mean_coupon          | predicted_purchase_intention | control subgroup gap                 | -4.66691    | 0.0648571  | 0           | -4.79403    | -4.53979     | 160592 | 0.0684305 |
| mean_coupon          | predicted_X_treated          | treatment minus control subgroup gap |  0.268993   | 0.158758   | 0.0901967   | -0.0421665  |  0.580152    | 160592 | 0.0684305 |
| n_push_with_discount | predicted_purchase_intention | control subgroup gap                 | -0.126078   | 0.00973419 | 2.28789e-38 | -0.145156   | -0.106999    | 160592 | 0.120244  |
| n_push_with_discount | predicted_X_treated          | treatment minus control subgroup gap | -0.0530628  | 0.0254858  | 0.0373376   | -0.103014   | -0.00311153  | 160592 | 0.120244  |
| share_push_discount  | predicted_purchase_intention | control subgroup gap                 | -0.0320837  | 0.00202838 | 2.36065e-56 | -0.0360592  | -0.0281081   | 160592 | 0.0638554 |
| share_push_discount  | predicted_X_treated          | treatment minus control subgroup gap | -0.0104158  | 0.00483247 | 0.031133    | -0.0198872  | -0.000944285 | 160592 | 0.0638554 |
| mean_discount        | predicted_purchase_intention | control subgroup gap                 | -0.118036   | 0.0081168  | 6.5517e-48  | -0.133944   | -0.102127    | 160592 | 0.0683762 |
| mean_discount        | predicted_X_treated          | treatment minus control subgroup gap | -0.0375572  | 0.0193843  | 0.0526833   | -0.0755498  |  0.000435297 | 160592 | 0.0683762 |