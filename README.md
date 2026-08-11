# Coffee Model-Free Analysis

This repository contains the model-free analysis of temporary Luckin Coffee store closures and later customer behavior. The current project focus is the 18-closure displacement design and the DDD effect on novelty seeking.

## Main Entry Points

- Technical record: `docs/technical_report.md`
- Rendered technical report: `docs/technical_report.html`
- Current results report: `reports/main_results.qmd`
- Preliminary paper draft: `writeup/main.tex`
- Dated analysis goals and execution records: `README/`
- Archived older reports: `Archive/reports/`

## Project Structure

```text
model-free/
├── Archive/
│   └── reports/                         # Superseded reports and slides kept for history
├── data/                                # Raw/processed data, ignored by git
├── docs/
│   ├── technical_report.qmd             # Quarto wrapper for the technical report
│   ├── technical_report.md              # Detailed implementation and result ledger
│   └── technical_report.html            # Rendered report
├── literature/                          # Related-paper notes
├── README/                              # Dated robustness goals, source records, and audit plans
├── outputs/
│   ├── customer-store/                  # Closure registries and descriptive panels
│   ├── displacement_classification/     # Blocked-buyer model scores and diagnostics
│   ├── 03_main_18_closures/             # Paper-facing 18-closure DDD/event-study outputs
│   ├── 04_diagnostics_18_closures/      # Common-support and identification diagnostics
│   ├── 05_robustness/                   # Robustness, mechanism checks, and older 22-closure runs
│   │   ├── noncoffee_novelty/           # Non-coffee novelty DDD and validation outputs
│   │   ├── reopening_assortment_constraints/  # Realized reopening-menu tests
│   │   ├── time_invariant_cafe_density/ # Local café-density estimates, diagnostics, and validation
│   │   └── new_product_notification_exposure/ # New-product push exposure tests
│   └── README.md                        # Output folder guide
├── reports/
│   └── main_results.qmd                 # Current 18-closure result report
├── scripts/
│   ├── customer-store/
│   ├── displacement_classification/
│   ├── displacement_effect_estimation/
│   ├── push_targeting_after_reopening/
│   └── writeup/                         # Paper-facing robustness and alternative-explanation scripts
├── src/
│   ├── customer-store/
│   ├── displacement_classification/
│   ├── displacement_effect_estimation/
│   └── store/
└── writeup/                             # Preliminary paper draft and bibliography
```

## Current Analysis Status

The main analysis uses `outputs/customer-store/closure_pair_registry.csv`, the 18-closure registry. The older 22-closure registry and related outputs are preserved as robustness/history under `outputs/05_robustness/full_registry_22/`.

The current output organization is:

- `outputs/03_main_18_closures/`: paper-facing purchase-frequency, purchase-incidence, member-first novelty, and market-new novelty results.
- `outputs/04_diagnostics_18_closures/`: matched/common-support diagnostics, blocked-gap event studies, pre-novelty heterogeneity checks, and technical backup.
- `outputs/05_robustness/`: 22-closure full-registry history, horizon robustness, cross-store exclusion, non-coffee novelty, time-invariant local café-density estimates, missing-new-product checks, reopening-assortment tests, new-product-notification exposure tests, push-targeting checks, and legacy runs.

The headline implementation sequence is:

1. Identify closure spells from store-level zero-demand runs.
2. Build treated/control member-closure registries.
3. Train the blocked-buyer classifier and export ex-ante scores.
4. Estimate DDD and event-study models for purchase and novelty outcomes.
5. Run robustness and mechanism checks, including matched/common-support diagnostics, non-coffee novelty, local café density, missing-new-product exposure, reopening assortment, cross-store substitution, and new-product-notification targeting.

For exact commands, code paths, output files, and result interpretations, use `docs/technical_report.md`.

### Non-Coffee Novelty Robustness

Run the non-coffee novelty analysis from the project root on the remote analysis machine:

```bash
python scripts/writeup/estimate_noncoffee_novelty_ddd.py \
  --project-root . \
  --output-dir outputs/05_robustness/noncoffee_novelty
python scripts/writeup/estimate_noncoffee_entry_dynamics.py \
  --estimator scripts/writeup/estimate_noncoffee_novelty_ddd.py \
  --output-dir outputs/05_robustness/noncoffee_novelty
python scripts/writeup/validate_noncoffee_novelty_ddd.py \
  --project-root . \
  --output-dir outputs/05_robustness/noncoffee_novelty
```

The output folder retains the aggregate estimates, product-classification audit, support diagnostics and validation report. Reproducible member-level Parquet intermediates are ignored by git.

### Time-Invariant Local Café-Density Robustness

Run the café-density analysis from the project root on the remote analysis machine, where the authoritative store-address and order files sit beside the repository:

```bash
python scripts/writeup/estimate_time_invariant_cafe_density_robustness.py \
  --project-root . \
  --output-dir outputs/05_robustness/time_invariant_cafe_density
python scripts/writeup/validate_time_invariant_cafe_density_robustness.py \
  --project-root . \
  --output-dir outputs/05_robustness/time_invariant_cafe_density
```

The estimator reconstructs each member-event's preferred pre-closure store, joins the fixed 500-meter and 1,500-meter café counts, and exports the collapsed, dynamic, support and leave-one-closure-out results. The output bundle includes its independent 160-check validation report. Reproducible member-level audit intermediates remain on the analysis machines and are ignored by git; the committed bundle contains the aggregate estimates and diagnostics. The authoritative source, encoding, field names, file hash and interpretation boundary are recorded in `README/2026_08_11_time_invariant_competition_robustness_goal.md`.
