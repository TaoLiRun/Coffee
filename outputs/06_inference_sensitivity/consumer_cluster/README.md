# Consumer-cluster inference sensitivity

These outputs re-estimate customer-level manuscript inference with CRV1 standard errors clustered by `member_id`. The production manuscript continues to use `closure_event_id`, the level of the common treatment shock.

The results were generated on `mktserver` with Python 3.11 and PyFixest 0.50.1 using:

```text
scripts/writeup/run_consumer_cluster_sensitivity.py
```

Each subdirectory contains compact regression or confidence-interval results and a `run_metadata.json`. Production output directories were not overwritten.

Restricted wild-bootstrap p-values are intentionally not included for consumer clusters. The manuscript's restricted bootstrap is performed over the 18 common closure shocks and should remain the small-cluster robustness check.

See `docs/clustering_sensitivity_summary.md` for the closure-versus-consumer comparison and interpretation.
