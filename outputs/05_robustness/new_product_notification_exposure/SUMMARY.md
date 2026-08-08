# New-product notification mechanism test

## Question

Do treated low-intention consumers experience a relative increase in recorded new-product notification exposure during closure or after reopening, compared with the corresponding high-intention and control-group changes?

## Metric

The primary outcome is unique trigger-tag-3 policy campaigns per consumer-day. Each member-policy-date combination is counted once. Raw-record counts, notification days, any exposure, total campaign volume and new-product share are secondary outcomes.

## Primary estimates

```text
        comparison               outcome                   term     coef  se_crv1  pvalue_crv1  pvalue_wild_restricted   ci_low  ci_high      n  clusters  singleton_drops  absorption_error
       post_vs_pre new_campaigns_per_day after_X_treated_X_high 0.001673 0.000727     0.034303                  0.0469 0.000139 0.003206 321184        18                0      9.417622e-11
 during_vs_all_pre new_campaigns_per_day after_X_treated_X_high 0.004112 0.001061     0.001215                  0.0032 0.001873 0.006351 200740        18                0      9.718371e-11
during_vs_last_pre new_campaigns_per_day after_X_treated_X_high 0.004328 0.001315     0.004315                  0.0111 0.001553 0.007103  80296        18                0      9.054230e-11
```

A negative triple-difference coefficient is the direction required by the alternative explanation: low-intention treated consumers receive a larger relative increase in new-product notifications than high-intention treated consumers.

## Treated-group descriptive means

```text
 disp_binary  phase  new_campaigns_per_day  new_records_per_day  any_new_push  new_push_days_per_day  campaigns_per_day  new_campaign_share  n_new_strictly_before_first_purchase  any_new_strictly_before_first_purchase
           0 during               0.030693             0.030693      0.257805               0.030693           0.210837            0.113947                              0.005795                                0.003926
           0   post               0.025023             0.025023      0.241073               0.025023           0.193476            0.113863                              0.023789                                0.018882
           0    pre               0.024746             0.024746      0.222098               0.024734           0.160609            0.111171                              0.025939                                0.018508
           1 during               0.011489             0.011489      0.138658               0.011489           0.105332            0.094335                              0.008329                                0.005390
           1   post               0.011347             0.011347      0.126041               0.011347           0.117810            0.074880                              0.043484                                0.030132
           1    pre               0.005786             0.005786      0.073738               0.005786           0.042718            0.100646                              0.048383                                0.032950
```

## Pretrend diagnostic

For the primary exposure outcome, the joint pretrend p-value is 0.5001.

## Data and interpretation limits

The raw scan read 56,724,521 records and retained 912,911 records in the analysis windows. The source identifies recorded targeting entries; it does not establish delivery, impression, opening or reading.

This test evaluates a necessary exposure pattern. Even a negative estimate would not show that notifications caused product choice. A null or positive, precisely estimated estimate would weigh against recorded new-product notifications as an explanation for the novelty DDD.