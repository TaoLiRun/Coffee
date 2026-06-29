# Main 18-Closure Results

These folders contain the current headline outputs generated from `outputs/customer-store/closure_pair_registry.csv`.

| Folder | Outcome | Command convention | Paper role |
|---|---|---|---|
| `purchase_frequency_ddd_h4/` | Purchase frequency over four pre/post event windows | `python src/displacement_effect_estimation/run.py --output-dir outputs/03_main_18_closures/purchase_frequency_ddd_h4` | Supporting contrast; purchase rebound is small and less clean because displacement pretrends are weaker. |
| `purchase_incidence_ddd_h4/` | Binary purchase incidence | `python src/displacement_effect_estimation/run.py --outcome purchase_incidence_binary --output-dir outputs/03_main_18_closures/purchase_incidence_ddd_h4` | Technical backup for the extensive margin. |
| `novelty_member_first_ddd_h4/` | Member-first novelty seeking, distinct-product mode | `python src/displacement_effect_estimation/run.py --outcome variety_seeking --output-dir outputs/03_main_18_closures/novelty_member_first_ddd_h4` | Core paper result. |
| `novelty_market_new_ddd_h4/` | Market-new novelty seeking | `python src/displacement_effect_estimation/run.py --outcome variety_seeking --variety-seeking-mode distinct-only-new --output-dir outputs/03_main_18_closures/novelty_market_new_ddd_h4` | Paper robustness result. |
| `metadata/` | Main-run manifest and registry snapshot | Written by `scripts/displacement_effect_estimation/run_main_results.sh` | Reproducibility ledger. |

Each result folder contains `summary.md`, collapsed DDD tables, event-study tables, plot data, and event-study figures.
