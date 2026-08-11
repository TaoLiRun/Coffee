# Outputs Directory

This directory is organized by role rather than by the order in which analyses were run.

| Folder | Role | Use in project |
|---|---|---|
| `store/` | Store-closure detection inputs | Feeds the customer-store registry. |
| `customer-store/` | Treatment/control registry and closure-pair files | Defines the 18-closure main sample and the older 22-closure full registry. |
| `displacement_classification/` | Ex-ante blocked-purchase classifier outputs | Provides `displacement_scores_t0_ex_ante.csv` for DDD estimation. |
| `03_main_18_closures/` | Current paper-facing 18-closure results | Main purchase-frequency, purchase-incidence, member-first novelty, and market-new novelty outputs. |
| `04_diagnostics_18_closures/` | Identification diagnostics and technical backup | Common-support checks, matched blocked-gap event studies, heterogeneity diagnostics, and separate-effect diagnostics. |
| `05_robustness/` | Robustness and mechanism checks | Full 22-closure registry, horizon checks, cross-store exclusion, non-coffee novelty, missing-new-product tests, push-targeting checks, and legacy outputs. |
| `nanjing_store_locations/` | Store-location support files | Auxiliary store-location output. |

The main paper should draw primarily from `03_main_18_closures/`. Results in `04_diagnostics_18_closures/` are for identification and technical-report backup unless explicitly promoted later.
