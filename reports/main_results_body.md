# Setup

This report reruns the two headline pooled DDD results on `outputs/customer-store/closure_pair_registry.csv`, reusing the existing displacement scores and feature cache. The main registry keeps **18 closures** and excludes **4** from the original kept sample.

## Sample Composition

| Run                    |   Unique closures |   Unique members |   Rows |
|:-----------------------|------------------:|-----------------:|-------:|
| Purchase full registry |                22 |            44858 | 358864 |
| Purchase main sample   |                18 |            40148 | 321184 |
| Novelty full registry  |                22 |            44858 | 358864 |
| Novelty main sample    |                18 |            40148 | 321184 |

# Purchase Frequency

The purchase-frequency headline claim is **supported** under the main sample. The main-sample blocked-buyer triple interaction is 0.0058 (SE 0.0032, p=0.086).

| Term                     |   Full-registry coef |   Full-registry SE | Full-registry p   |   Main-sample coef |   Main-sample SE | Main-sample p   |   Main - full |
|:-------------------------|---------------------:|-------------------:|:------------------|-------------------:|-----------------:|:----------------|--------------:|
| post x treated           |               0.0008 |             0.0006 | 0.222             |             0.0009 |           0.0024 | 0.711           |        0.0001 |
| post x blocked           |              -0.0344 |             0.0011 | <0.001            |            -0.0344 |           0.003  | <0.001          |       -0      |
| post x treated x blocked |               0.0049 |             0.0024 | 0.043             |             0.0058 |           0.0032 | 0.086           |        0.0009 |

# Novelty-Seeking

The novelty-seeking headline claim is **supported** under the main sample. The main-sample baseline treatment effect is 0.0313 (SE 0.0178, p=0.098), and the main-sample blocked-buyer triple interaction is -0.0415 (SE 0.0184, p=0.038).

| Term                     |   Full-registry coef |   Full-registry SE | Full-registry p   |   Main-sample coef |   Main-sample SE | Main-sample p   |   Main - full |
|:-------------------------|---------------------:|-------------------:|:------------------|-------------------:|-----------------:|:----------------|--------------:|
| post x treated           |               0.0309 |             0.0113 | 0.006             |             0.0313 |           0.0178 | 0.098           |        0.0003 |
| post x blocked           |               0.0359 |             0.006  | <0.001            |             0.0381 |           0.0081 | <0.001          |        0.0022 |
| post x treated x blocked |              -0.0386 |             0.0137 | 0.005             |            -0.0415 |           0.0184 | 0.038           |       -0.0028 |

# Conclusion

## Headline Verdicts

- Purchase frequency: **supported** on the main 18-closure sample.
- Novelty-seeking: **supported** on the main 18-closure sample.

This report is intentionally limited to the pooled headline coefficients. It does not interpret event-study or heterogeneity outputs in this first main-results pass.
