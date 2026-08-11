# Validation report: non-coffee novelty DDD

## Overall assessment: Ready to share with caveats

The primary all-non-coffee DDD is **-0.0413** (SE 0.0340; 95% CI [-0.1131, 0.0305]; CRV1 p=0.2418; restricted wild-cluster p=0.2249). The differential-pretrend test has p=0.0064.

## Validation checks

| check                                        | passed   | detail                                                                                                                               |
|:---------------------------------------------|:---------|:-------------------------------------------------------------------------------------------------------------------------------------|
| raw row count                                | True     | raw_rows=10,631,943                                                                                                                  |
| source category reconciliation               | True     | {'coffee': 7651380, 'food': 1010912, 'noncoffee_drink': 1947508, 'other_noncoffee': 22143}                                           |
| exactly one category field per source row    | True     | {'1': 10631943}                                                                                                                      |
| complete non-coffee classification crosswalk | True     | category-name pairs={'food': 103, 'noncoffee_drink': 168, 'other_noncoffee': 81}; unique keys=352                                    |
| headline grid retained                       | True     | rows=321,184; episodes=40,148                                                                                                        |
| novelty metric bounds and denominators       | True     | all scopes checked                                                                                                                   |
| scope nesting                                | True     | all >= consumables >= drinks                                                                                                         |
| DDD group-effect algebra                     | True     | high = low + DDD                                                                                                                     |
| headline estimator reproduction              | True     | coef diff=0; se diff=3.12e-17; N=99,644                                                                                              |
| independent DDD refits                       | True     | all_noncoffee: coef=-0.041284, N=30,444; noncoffee_consumables: coef=-0.041090, N=30,418; noncoffee_drinks: coef=-0.062625, N=21,433 |
| DDD pretrend coverage                        | True     | three leads for every novelty scope                                                                                                  |
| event-study period coverage                  | True     | reference period -1 omitted                                                                                                          |
| sample-entry support table                   | True     | rows=96; expected=96                                                                                                                 |

## Required caveat

The novelty ratio is defined only in member-periods containing at least one product in the selected non-coffee scope. The saved any-purchase DDD and cell-specific entry rates must accompany interpretation of the conditional result.

## Incomplete blockers

None.
