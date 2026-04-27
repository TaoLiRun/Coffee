# Setup

This report reruns the two headline pooled DDD results on `outputs/customer-store/closure_pair_registry_selected.csv`, reusing the existing displacement scores and feature cache. The selected registry keeps **18 closures** and excludes **4** from the original kept sample.

## Sample Composition

| Run                      |   Unique closures |   Unique members |   Rows |
|:-------------------------|------------------:|-----------------:|-------:|
| Purchase baseline        |                22 |            44858 | 358864 |
| Purchase selected subset |                18 |            40148 | 321184 |
| Novelty baseline         |                22 |            44858 | 358864 |
| Novelty selected subset  |                18 |            40148 | 321184 |

# Purchase Frequency

The purchase-frequency headline claim is **supported** under the selected subset. The subset blocked-buyer triple interaction is 0.0058 (SE 0.0025, p=0.021).

| Term                     |   Baseline coef |   Baseline SE | Baseline p   |   Subset coef |   Subset SE | Subset p   |   Subset - baseline |
|:-------------------------|----------------:|--------------:|:-------------|--------------:|------------:|:-----------|--------------------:|
| post x treated           |          0.0008 |        0.0006 | 0.222        |        0.0009 |      0.0007 | 0.180      |              0.0001 |
| post x blocked           |         -0.0344 |        0.0011 | <0.001       |       -0.0344 |      0.0011 | <0.001     |             -0      |
| post x treated x blocked |          0.0049 |        0.0024 | 0.043        |        0.0058 |      0.0025 | 0.021      |              0.0009 |

# Novelty-Seeking

The novelty-seeking headline claim is **supported** under the selected subset. The subset baseline treatment effect is 0.0313 (SE 0.0120, p=0.009), and the subset blocked-buyer triple interaction is -0.0415 (SE 0.0145, p=0.004).

| Term                     |   Baseline coef |   Baseline SE | Baseline p   |   Subset coef |   Subset SE | Subset p   |   Subset - baseline |
|:-------------------------|----------------:|--------------:|:-------------|--------------:|------------:|:-----------|--------------------:|
| post x treated           |          0.0309 |        0.0113 | 0.006        |        0.0313 |      0.012  | 0.009      |              0.0003 |
| post x blocked           |          0.0359 |        0.006  | <0.001       |        0.0381 |      0.0064 | <0.001     |              0.0022 |
| post x treated x blocked |         -0.0386 |        0.0137 | 0.005        |       -0.0415 |      0.0145 | 0.004      |             -0.0028 |

# Conclusion

## Headline Verdicts

- Purchase frequency: **supported** on the selected 18-closure subset.
- Novelty-seeking: **supported** on the selected 18-closure subset.

This report is intentionally limited to the pooled headline coefficients. It does not interpret event-study or heterogeneity outputs in this first robustness pass.
