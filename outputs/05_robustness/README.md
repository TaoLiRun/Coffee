# Robustness And Mechanism Outputs

These folders hold robustness checks, mechanism diagnostics, and older analysis runs.

| Folder | Meaning | Paper role |
|---|---|---|
| `full_registry_22/` | Older full-registry results using 22 closures | Shows broad sign stability relative to the 18-closure main sample. |
| `horizon_h1_full_registry_22/` | Older one-window horizon robustness | Technical backup. |
| `horizon_h2_full_registry_22/` | Older two-window horizon robustness | Technical backup. |
| `excluding_cross_store_treated/` | Excludes treated member-events with same-chain purchases at another store during closure | Mechanism/robustness check for cross-store substitution. |
| `missing_new_products/` | Control-store product introduction and missed-exposure diagnostics | Mechanism diagnostic; not proof that missed exposure is ruled out. |
| `push_targeting_after_reopening/` | Push-notification targeting after reopening | Caveat/diagnostic for marketing exposure. |
| `legacy_registry_n_purchases_ddd/` | Older legacy purchase-frequency run log | Historical reference only. |

Use `03_main_18_closures/` for headline paper results. Use this folder to document sensitivity and mechanisms in the technical report or appendix.
