# Non-coffee novelty-seeking robustness check

## Result

- **all_noncoffee**: novelty DDD -0.0413 (SE 0.0340, 95% CI [-0.1131, 0.0305], CRV1 p=0.2418, restricted wild p=0.2249; N=30,444). The conditional pre-period mean is 0.7457; the differential pretrend p-value is 0.0064. The any-purchase DDD is -0.0170 (SE 0.0100, p=0.1070).
- **noncoffee_consumables**: novelty DDD -0.0411 (SE 0.0339, 95% CI [-0.1126, 0.0304], CRV1 p=0.2420, restricted wild p=0.2303; N=30,418). The conditional pre-period mean is 0.7458; the differential pretrend p-value is 0.0058. The any-purchase DDD is -0.0175 (SE 0.0101, p=0.1022).
- **noncoffee_drinks**: novelty DDD -0.0626 (SE 0.0412, 95% CI [-0.1495, 0.0243], CRV1 p=0.1468, restricted wild p=0.1185; N=21,433). The conditional pre-period mean is 0.7807; the differential pretrend p-value is 0.2262. The any-purchase DDD is -0.0224 (SE 0.0090, p=0.0229).

## Benchmark

The temporary estimator reproduces the headline all-product novelty DDD: -0.0415 (SE 0.0184, p=0.0380; N=99,644).

## Construction

The raw scan covers 10,631,943 commodity rows. Every source row has exactly one populated category field. The primary definition combines non-coffee drinks, food and other non-coffee products; category and exact description jointly identify a product.

The novelty outcome is conditional on purchasing at least one product in the selected non-coffee scope. The any-purchase DDD and cell-specific entry rates diagnose the resulting sample-selection margin.
