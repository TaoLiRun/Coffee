# 2026-04-27 Mechanism Check: Excluding Treated Cross-Store Buyers

This note summarizes the robustness check where treated member-events are excluded if the member purchased at a different store during the closure window.

## 1) How many treated cross-store buyers?

Using the main-sample closure registry and the rule:

- exclude treated member-event if member made at least one purchase at `dept_id != treated_dept_id` during `[closure_start, closure_end]`.

Counts:

- Treated member-events before exclusion: **7,390**
- Treated member-events excluded: **519**
- Exclusion rate among treated member-events: **7.0230%**
- Estimation rows before/after exclusion: **321,184 -> 317,032**
- Unique members before/after exclusion: **40,148 -> 39,629**

## 2) How do DDD coefficients change after excluding them?

Below, "before" means main-sample estimates without exclusion, and "after" means estimates after excluding treated cross-store buyers.

### A. Outcome: `n_purchases` (overall collapsed DDD)

| Term | Before coef (p) | After coef (p) | Change (after - before) |
|---|---:|---:|---:|
| `post_X_treated` | 0.000892 (0.1804) | 0.000562 (0.3959) | -0.000330 |
| `post_X_disp` | -0.034349 (<0.001) | -0.034349 (<0.001) | ~0.000000 |
| `post_X_treated_X_disp` | 0.005829 (0.0207) | 0.005150 (0.0430) | -0.000679 |

Interpretation:

- Baseline treatment effect (`post_X_treated`) attenuates and becomes less significant.
- Key triple interaction (`post_X_treated_X_disp`) also attenuates and weakens in significance (still marginally significant at 5%).

### B. Outcome: `novelty-seeking` (`variety_seeking`, overall collapsed DDD)

| Term | Before coef (p) | After coef (p) | Change (after - before) |
|---|---:|---:|---:|
| `post_X_treated` | 0.031290 (0.0091) | 0.033462 (0.0071) | +0.002172 |
| `post_X_disp` | 0.038084 (<0.001) | 0.037984 (<0.001) | -0.000100 |
| `post_X_treated_X_disp` | -0.041489 (0.0042) | -0.032248 (0.0356) | +0.009241 |

Interpretation:

- The key novelty triple interaction remains negative, but becomes less negative and less significant.
- The baseline treatment novelty effect (`post_X_treated`) is slightly stronger.

## Bottom line

- Excluding treated cross-store buyers removes about **7.0%** of treated member-events.
- For `n_purchases`, the overall treatment-side effects attenuate.
- For novelty-seeking, the key negative triple effect attenuates but remains statistically significant at 5%.
