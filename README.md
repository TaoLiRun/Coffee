# Coffee Model-Free Analysis

This repository contains the model-free analysis of temporary Luckin Coffee store closures and later customer behavior. The current project focus is the 18-closure displacement design and the DDD effect on novelty seeking.

## Main Entry Points

- Technical record: `docs/technical_report.md`
- Rendered technical report: `docs/technical_report.html`
- Current results report: `reports/main_results.qmd`
- Preliminary paper draft: `writeup/main.tex`
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
├── outputs/
│   ├── customer-store/                  # Closure registries and descriptive panels
│   ├── displacement_classification/     # Blocked-buyer model scores and diagnostics
│   ├── 03_main_18_closures/             # Paper-facing 18-closure DDD/event-study outputs
│   ├── 04_diagnostics_18_closures/      # Common-support and identification diagnostics
│   ├── 05_robustness/                   # Robustness, mechanism checks, and older 22-closure runs
│   └── README.md                        # Output folder guide
├── reports/
│   └── main_results.qmd                 # Current 18-closure result report
├── scripts/
│   ├── customer-store/
│   ├── displacement_classification/
│   ├── displacement_effect_estimation/
│   └── push_targeting_after_reopening/
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
- `outputs/05_robustness/`: 22-closure full-registry history, horizon robustness, cross-store exclusion, missing-new-product checks, push-targeting checks, and legacy runs.

The headline implementation sequence is:

1. Identify closure spells from store-level zero-demand runs.
2. Build treated/control member-closure registries.
3. Train the blocked-buyer classifier and export ex-ante scores.
4. Estimate DDD and event-study models for purchase and novelty outcomes.
5. Run robustness and mechanism checks, including matched/common-support diagnostics, missing-new-product exposure, cross-store substitution, and push targeting.

For exact commands, code paths, output files, and result interpretations, use `docs/technical_report.md`.
