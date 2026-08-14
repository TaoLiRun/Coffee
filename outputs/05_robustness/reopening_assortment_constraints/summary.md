# Reopening Assortment

## Primary manuscript test: evolution across four weeks after reopening

The primary specification uses treated stores, requires four observed post-reopening weeks for each outcome, includes closure-event fixed effects, and clusters CRV1 standard errors by closure event. Week 1 is the reference period.

| term | coef | se_crv1 | pvalue_crv1 | ci_low | ci_high | n | n_clusters | event_store_pairs | within_r2 | outcome | sample | relative_week |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| week_2 | 0.005878625 | 0.018534751 | 0.75497843 | -0.033226282 | 0.044983532 | 72 | 18 | 18 | 0.11606059 | core_coverage | complete_4_post_weeks | 2 |
| week_3 | -0.064784725 | 0.054373387 | 0.24983514 | -0.17950254 | 0.049933094 | 72 | 18 | 18 | 0.11606059 | core_coverage | complete_4_post_weeks | 3 |
| week_4 | -0.083992668 | 0.053745819 | 0.13652812 | -0.19738644 | 0.029401099 | 72 | 18 | 18 | 0.11606059 | core_coverage | complete_4_post_weeks | 4 |
| week_2 | 0.301875 | 0.73514473 | 0.68714718 | -1.2650489 | 1.8687989 | 64 | 16 | 16 | 0.24257274 | rarefied_products_50 | complete_4_post_weeks | 2 |
| week_3 | -0.703125 | 0.60055559 | 0.25994725 | -1.9831789 | 0.57692893 | 64 | 16 | 16 | 0.24257274 | rarefied_products_50 | complete_4_post_weeks | 3 |
| week_4 | -1.66 | 0.55523511 | 0.0091624166 | -2.8434556 | -0.47654438 | 64 | 16 | 16 | 0.24257274 | rarefied_products_50 | complete_4_post_weeks | 4 |
| week_2 | -0.0099899166 | 0.01294757 | 0.45096355 | -0.037306901 | 0.017327068 | 72 | 18 | 18 | 0.24287958 | menu_jaccard_pre | complete_4_post_weeks | 2 |
| week_3 | -0.076325165 | 0.041043846 | 0.080337124 | -0.16292011 | 0.010269782 | 72 | 18 | 18 | 0.24287958 | menu_jaccard_pre | complete_4_post_weeks | 3 |
| week_4 | -0.11114353 | 0.040314067 | 0.0134705 | -0.19619877 | -0.026088279 | 72 | 18 | 18 | 0.24287958 | menu_jaccard_pre | complete_4_post_weeks | 4 |

### Joint week-equality tests

| f_statistic | df_num | df_denom | pvalue | outcome | sample | n | n_clusters | pvalue_wild_restricted | bootstrap_reps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.1864071 | 3 | 17 | 0.34446541 | core_coverage | complete_4_post_weeks | 72 | 18 | 0.3821 | 9999 |
| 6.5149279 | 3 | 15 | 0.0048799065 | rarefied_products_50 | complete_4_post_weeks | 64 | 16 | 0.0106 | 9999 |
| 4.4934271 | 3 | 17 | 0.01696677 | menu_jaccard_pre | complete_4_post_weeks | 72 | 18 | 0.0175 | 9999 |

### Primary-sample support

| outcome | sample | observations | treated_stores | week_1_mean |
| --- | --- | --- | --- | --- |
| core_coverage | complete_4_post_weeks | 72 | 18 | 0.76870301 |
| rarefied_products_50 | complete_4_post_weeks | 64 | 16 | 29.258125 |
| menu_jaccard_pre | complete_4_post_weeks | 72 | 18 | 0.61195384 |

## Return timing and realized assortment at first return

The return sample contains treated consumers whose first purchase at the reopened focal store occurs within 28 days. Exposure outcomes assign the realized assortment in that seven-day return week. High-minus-low regressions include closure-event fixed effects and cluster CRV1 standard errors by closure event.

| disp_binary | eligible_members | returned_within_28_days | share_returned_within_28_days | mean_days_after_reopening | median_days_after_reopening | share_returning_week_1 | share_returning_week_2 | share_returning_week_3 | share_returning_week_4 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 5349 | 1134 | 0.21200224 | 12.156966 | 11 | 0.36948854 | 0.24779541 | 0.21516755 | 0.1675485 |
| 1 | 2041 | 1268 | 0.62126409 | 9.033123 | 7 | 0.5362776 | 0.24921136 | 0.12302839 | 0.09148265 |

| term | coef | se_crv1 | pvalue_crv1 | ci_low | ci_high | n | n_clusters | event_store_pairs | within_r2 | outcome | estimand |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| disp_binary | -2.8723542 | 0.29360061 | 2.1328311e-08 | -3.4917973 | -2.2529111 | 2402 | 18 | 18 | 0.031828085 | days_after_reopening | high_minus_low_among_treated_first_returners |
| disp_binary | 0.0067418596 | 0.0041596711 | 0.1234669 | -0.0020342793 | 0.015517999 | 2402 | 18 | 18 | 0.0044113994 | core_coverage | high_minus_low_among_treated_first_returners |
| disp_binary | 0.17658519 | 0.089454414 | 0.064856555 | -0.012147123 | 0.36531751 | 2390 | 18 | 18 | 0.0038850216 | rarefied_products_50 | high_minus_low_among_treated_first_returners |
| disp_binary | 0.0103489 | 0.0045616465 | 0.036600839 | 0.00072466775 | 0.019973133 | 2402 | 18 | 18 | 0.0091715586 | menu_jaccard_pre | high_minus_low_among_treated_first_returners |

| outcome | disp_binary | mean | observations |
| --- | --- | --- | --- |
| days_after_reopening | 0 | 12.156966 | 1134 |
| days_after_reopening | 1 | 9.033123 | 1268 |
| core_coverage | 0 | 0.79536566 | 1134 |
| core_coverage | 1 | 0.82610236 | 1268 |
| rarefied_products_50 | 0 | 28.864391 | 1125 |
| rarefied_products_50 | 1 | 29.646711 | 1265 |
| menu_jaccard_pre | 0 | 0.63521716 | 1134 |
| menu_jaccard_pre | 1 | 0.66056735 | 1268 |

### Personal novel-product opportunity at the actual return week

For each possible return week, the product set is leave-one-customer-out: products purchased only by the focal consumer are removed, while products also purchased by somebody else remain. A product is personally novel if the consumer did not purchase it anywhere in the chain through the closure end date. The timing-deviation outcomes subtract the same consumer's equal-weighted four-week mean, so they isolate assortment exposure due to return timing. Share regressions require a nonempty leave-one-out product set in all four weeks.

| term | coef | se_crv1 | pvalue_crv1 | ci_low | ci_high | n | n_clusters | event_store_pairs | within_r2 | outcome | estimand |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| disp_binary | -0.054316998 | 0.0040348297 | 3.8247669e-10 | -0.062870454 | -0.045763541 | 2325 | 17 | 17 | 0.15935904 | novel_opportunity_share_leave_one_out | high_minus_low_among_treated_first_returners |
| disp_binary | -0.0010009213 | 0.00056024419 | 0.092965584 | -0.0021885859 | 0.00018674338 | 2325 | 17 | 17 | 0.0017452252 | timing_deviation_novel_opportunity_share_leave_one_out | high_minus_low_among_treated_first_returners |
| disp_binary | -4.0767359 | 0.58191236 | 2.1158364e-06 | -5.3044637 | -2.8490081 | 2402 | 18 | 18 | 0.086495424 | novel_products_leave_one_out | high_minus_low_among_treated_first_returners |
| disp_binary | -0.27556508 | 0.38479649 | 0.48363196 | -1.0874147 | 0.53628454 | 2402 | 18 | 18 | 0.00081295231 | timing_deviation_novel_products_leave_one_out | high_minus_low_among_treated_first_returners |

| outcome | disp_binary | mean | observations |
| --- | --- | --- | --- |
| novel_opportunity_share_leave_one_out | 0 | 0.92676596 | 1102 |
| novel_opportunity_share_leave_one_out | 1 | 0.87701365 | 1223 |
| timing_deviation_novel_opportunity_share_leave_one_out | 0 | -0.00051512502 | 1102 |
| timing_deviation_novel_opportunity_share_leave_one_out | 1 | -0.0015608175 | 1223 |
| novel_products_leave_one_out | 0 | 67.790123 | 1134 |
| novel_products_leave_one_out | 1 | 66.94795 | 1268 |
| timing_deviation_novel_products_leave_one_out | 0 | 1.5780423 | 1134 |
| timing_deviation_novel_products_leave_one_out | 1 | 1.0561909 | 1268 |

## Supplementary matched-store comparison

| term | coef | se_crv1 | pvalue_crv1 | ci_low | ci_high | n | n_clusters | event_store_pairs | within_r2 | outcome | sample | model |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| treated_store_X_post | -0.012891243 | 0.034052016 | 0.70968969 | -0.084734716 | 0.058952231 | 736 | 18 | 92 | 0.00096977984 | core_coverage | available_unbalanced | pooled_post |
| rt_p1_X_treated_store | 0.020549207 | 0.036482068 | 0.5806061 | -0.056421229 | 0.097519643 | 736 | 18 | 92 | 0.015082731 | core_coverage | available_unbalanced | immediate_post |
| treated_store_X_post | 0.30632159 | 0.51777471 | 0.56189616 | -0.78608755 | 1.3987307 | 723 | 18 | 92 | 0.0019242131 | rarefied_products_50 | available_unbalanced | pooled_post |
| rt_p1_X_treated_store | 0.19352539 | 0.87531957 | 0.82765519 | -1.6532375 | 2.0402883 | 723 | 18 | 92 | 0.01419886 | rarefied_products_50 | available_unbalanced | immediate_post |
| treated_store_X_post | 0.014620058 | 0.025006721 | 0.56646544 | -0.038139513 | 0.067379628 | 736 | 18 | 92 | 0.0019432905 | menu_jaccard_pre | available_unbalanced | pooled_post |
| rt_p1_X_treated_store | 0.049495385 | 0.029327847 | 0.10973661 | -0.012380962 | 0.11137173 | 736 | 18 | 92 | 0.011857717 | menu_jaccard_pre | available_unbalanced | immediate_post |

### Matched-store pretrend tests

| f_statistic | df_num | df_denom | pvalue | outcome | sample |
| --- | --- | --- | --- | --- | --- |
| 2.3339025 | 3 | 17 | 0.11030831 | core_coverage | available_unbalanced |
| 1.0106568 | 3 | 17 | 0.41227331 | rarefied_products_50 | available_unbalanced |
| 0.77896295 | 3 | 17 | 0.52181769 | menu_jaccard_pre | available_unbalanced |

## Validation

| check | passed | observed | expected |
| --- | --- | --- | --- |
| registry contains 18 retained closures | True | 18 | 18 |
| panel contains one treated store per closure | True | 18 | 18 |
| panel grain is unique | True | 0 | 0 |
| first-return panel is unique at member-event grain | True | 0 | 0 |
| first-return panel covers 18 closure events | True | 18 | 18 |
| novel-opportunity panel has four weeks per returner | True | 9608 | 9608 |
| novel-opportunity share lies in the unit interval | True | 1 | maximum no greater than 1 |
| leave-one-out novel-opportunity share is observed | True | 0.98397169 | reported; missing means no leave-one-customer-out sale |
| timing deviations average to zero within returner | True | 8.3266727e-17 | 0 |
| high-intention returners return earlier within closure | True | -2.8723542 | negative high-minus-low coefficient |
| core_coverage: week 2 coefficient equals mean within-event change | True | 0.005878625 | 0.0058786250029129 |
| core_coverage: week 3 coefficient equals mean within-event change | True | -0.064784725 | -0.0647847251371019 |
| core_coverage: week 4 coefficient equals mean within-event change | True | -0.083992668 | -0.08399266825190232 |
| rarefied_products_50: week 2 coefficient equals mean within-event change | True | 0.301875 | 0.3018750000000001 |
| rarefied_products_50: week 3 coefficient equals mean within-event change | True | -0.703125 | -0.7031249999999996 |
| rarefied_products_50: week 4 coefficient equals mean within-event change | True | -1.66 | -1.6599999999999997 |
| menu_jaccard_pre: week 2 coefficient equals mean within-event change | True | -0.0099899166 | -0.009989916568602727 |
| menu_jaccard_pre: week 3 coefficient equals mean within-event change | True | -0.076325165 | -0.07632516473968515 |
| menu_jaccard_pre: week 4 coefficient equals mean within-event change | True | -0.11114353 | -0.11114352616889842 |

Product sales proxy realized assortment; a product without a recorded sale may still have been displayed or available.