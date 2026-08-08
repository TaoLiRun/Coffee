# New-Product Notification Exposure

This folder contains the paper-facing alternative-explanation test based on push records with `trigger_tag = 3`, the data definition for a new-product notification.

The primary outcome is the number of unique member-policy-date new-product notification campaigns per consumer-day. A negative high-minus-low DDD would be required for differential notification exposure to explain the negative novelty-seeking DDD. The estimated first stages are positive during closure and after reopening.

Main files:

- `new_product_push_ddd.csv`: collapsed during/pre and post/pre exposure estimates with closure-clustered and restricted wild-cluster inference.
- `new_product_push_event_study.csv`: dynamic high-minus-low exposure coefficients relative to period -1.
- `cell_phase_descriptives.csv` and `treated_high_low_means.csv`: absolute exposure levels by treatment, predicted incidence and phase.
- `purchase_timing_descriptives.csv` and `new_push_dormancy.csv`: timing and inactivity diagnostics.
- `new_product_push_panel.parquet`: reproducible member-event-period analysis panel generated in the working directory; the repository's standard `*.parquet` rule excludes it from version control.
- `audit.json`, `validation_checks.csv` and `VALIDATION_REPORT.md`: construction and validation records.

Rebuild with `scripts/writeup/estimate_new_product_notification_exposure.py`; validate the saved outputs with `scripts/writeup/validate_new_product_notification_exposure.py`.
