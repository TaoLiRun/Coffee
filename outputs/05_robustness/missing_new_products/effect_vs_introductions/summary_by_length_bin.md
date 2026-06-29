# Matched-Bin Comparison by Closure Length

- Bins (inclusive): 10-14, 15-19, 20-24, 25-29 days.
- Metric for product changes: `avg_n_introduced_during_control`.

## n_purchases

- Pooled within-bin correlation between introductions and key DDD effect: -0.092
- Mean within-bin high-minus-low effect gap: -0.0067

| outcome     | length_bin   |   n_closures |   mean_closure_duration_days |   mean_avg_n_introduced_during_control |   mean_effect |   corr_intro_vs_effect_within_bin |   within_bin_median_intro |   high_intro_n_closures |   low_intro_n_closures |   high_minus_low_mean_effect_within_bin |
|:------------|:-------------|-------------:|-----------------------------:|---------------------------------------:|--------------:|----------------------------------:|--------------------------:|------------------------:|-----------------------:|----------------------------------------:|
| n_purchases | 10-14        |            9 |                      12.4444 |                                7.06667 |   -0.00965496 |                       0.000465344 |                       7.4 |                       5 |                      4 |                               0.0211382 |
| n_purchases | 15-19        |            5 |                      16.8    |                               10.24    |    0.00683414 |                      -0.399691    |                       9.2 |                       3 |                      2 |                              -0.0149806 |
| n_purchases | 20-24        |            0 |                     nan      |                              nan       |  nan          |                     nan           |                     nan   |                       0 |                      0 |                             nan         |
| n_purchases | 25-29        |            4 |                      27.25   |                               13.35    |    0.0030551  |                      -0.696691    |                      13.2 |                       2 |                      2 |                              -0.0262804 |

## variety_seeking_unbalanced

- Pooled within-bin correlation between introductions and key DDD effect: -0.049
- Mean within-bin high-minus-low effect gap: -0.0115

| outcome                    | length_bin   |   n_closures |   mean_closure_duration_days |   mean_avg_n_introduced_during_control |   mean_effect |   corr_intro_vs_effect_within_bin |   within_bin_median_intro |   high_intro_n_closures |   low_intro_n_closures |   high_minus_low_mean_effect_within_bin |
|:---------------------------|:-------------|-------------:|-----------------------------:|---------------------------------------:|--------------:|----------------------------------:|--------------------------:|------------------------:|-----------------------:|----------------------------------------:|
| variety_seeking_unbalanced | 10-14        |            9 |                      12.4444 |                                7.06667 |   -0.0476172  |                         -0.11733  |                       7.4 |                       5 |                      4 |                               0.0756754 |
| variety_seeking_unbalanced | 15-19        |            5 |                      16.8    |                               10.24    |   -0.0748815  |                          0.311068 |                       9.2 |                       3 |                      2 |                               0.0077967 |
| variety_seeking_unbalanced | 20-24        |            0 |                     nan      |                              nan       |  nan          |                        nan        |                     nan   |                       0 |                      0 |                             nan         |
| variety_seeking_unbalanced | 25-29        |            4 |                      27.25   |                               13.35    |   -0.00276125 |                         -0.368225 |                      13.2 |                       2 |                      2 |                              -0.117898  |
