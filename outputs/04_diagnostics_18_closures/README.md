# 18-Closure Diagnostics

These folders contain identification checks and technical backup for the 18-closure main sample. They are important for the technical report but are not main paper results unless promoted later.

| Folder | Contents | Current interpretation |
|---|---|---|
| `purchase_common_support/` | Coarsened common-support and matched blocked-gap diagnostics for purchase frequency | Purchase DDD attenuates and becomes imprecise after common-support pruning; keep as a caveat. |
| `novelty_common_support/` | Coarsened common-support and matched blocked-gap diagnostics for member-first novelty | Novelty pretrends look cleaner than purchase pretrends, but the matched estimate is smaller and imprecise. Not added to the paper yet. |
| `novelty_pre_heterogeneity_median/` | Pre-period novelty median-split heterogeneity | Descriptive heterogeneity; high pre-novelty members also differ in baseline purchase frequency. |
| `novelty_pre_heterogeneity_quartile_tails/` | Bottom/top quartile pre-period novelty heterogeneity | Sharper descriptive contrast, with the same caution about baseline differences. |
| `novelty_common_support_heterogeneity_median/` | Common-support version of median heterogeneity | Technical backup. |
| `novelty_common_support_heterogeneity_quartile_tails/` | Common-support version of quartile-tail heterogeneity | Technical backup. |
| `pre_period_novelty_distribution/` | Pre-period novelty distribution files that were previously in the flat main folder | Descriptive support for heterogeneity diagnostics. |
| `separate_effect_duration10_recency10/` | Older separate-effect run for 10-day closures and recent consumers | Legacy diagnostic, not a headline result. |

Large row-level `estimation_sample.csv` files in common-support folders are intentionally ignored when newly generated.
