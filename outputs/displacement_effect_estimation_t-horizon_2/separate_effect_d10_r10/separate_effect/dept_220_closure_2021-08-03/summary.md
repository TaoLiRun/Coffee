# Displacement Effect Estimation Summary

- Sample rows: 1,032
- Unique members: 258
- Unique closures: 1
- Event FE units: 258
- Relative periods: [-2, -1, 1, 2]
- Estimation mode: separate_effect=true
- Closure event: `dept_220_closure_2021-08-03`
- Closure duration filter days: 10
- Recency filter days: 10
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |        coef |        se |    pvalue |
|:-----------------|:----------------------|-----:|------------:|------------:|----------:|----------:|
| binary_collapsed | post_X_treated        | 1032 |  0.00492658 |  0.00211353 | 0.0179872 | 0.906554  |
| binary_collapsed | post_X_disp           | 1032 |  0.00492658 | -0.0321457  | 0.019447  | 0.0995531 |
| binary_collapsed | post_X_treated_X_disp | 1032 |  0.00492658 |  0.026969   | 0.0629269 | 0.668591  |

## Score Spec
| spec            | term                   |    n |   r2_within |       coef |        se |    pvalue |
|:----------------|:-----------------------|-----:|------------:|-----------:|----------:|----------:|
| score_collapsed | post_X_treated         | 1032 |  0.00579775 |  0.0183057 | 0.0332283 | 0.582175  |
| score_collapsed | post_X_score           | 1032 |  0.00579775 | -0.0536577 | 0.0313837 | 0.0885228 |
| score_collapsed | post_X_treated_X_score | 1032 |  0.00579775 |  0.0586888 | 0.107928  | 0.587066  |

## Event-study Specs
| spec           | term                                                              |        coef |        se |      pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|------------:|----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0247069  | 0.0243435 | 0.311095    | 1032 |  0.00211335 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.00260345 | 0.0282155 | 0.926555    | 1032 |  0.00211335 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0077069  | 0.0336836 | 0.819204    | 1032 |  0.00211335 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.025      | 0.0194575 | 0.200001    | 1032 |  0.0550355  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00857488 | 0.0252653 | 0.73459     | 1032 |  0.0550355  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0121981  | 0.0251164 | 0.627621    | 1032 |  0.0550355  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0505892  | 0.0486286 | 0.29917     | 1032 |  0.0550355  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.0305446  | 0.0658903 | 0.64335     | 1032 |  0.0550355  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.0739826  | 0.0787796 | 0.348557    | 1032 |  0.0550355  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.117593   | 0.0227304 | 4.63341e-07 | 1032 |  0.0550355  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  0.00253623 | 0.0221295 | 0.908845    | 1032 |  0.0550355  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.0507649  | 0.0265169 | 0.0566753   | 1032 |  0.0550355  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.00377749 | 0.0251464 | 0.880709    | 1032 |  0.0578098  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0049498  | 0.0347819 | 0.886947    | 1032 |  0.0578098  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0278842  | 0.0407296 | 0.494203    | 1032 |  0.0578098  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.0842067  | 0.0787798 | 0.286123    | 1032 |  0.0578098  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.0296475  | 0.108558  | 0.784993    | 1032 |  0.0578098  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.171937   | 0.133108  | 0.197618    | 1032 |  0.0578098  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.169529   | 0.0358763 | 3.78531e-06 | 1032 |  0.0578098  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.00288894 | 0.0334516 | 0.931246    | 1032 |  0.0578098  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  |  0.0651026  | 0.0407796 | 0.111617    | 1032 |  0.0578098  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |   pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|---------:|-----:|
| event_att      | pretrend_att_joint_zero            |                1 |    1.03008  | 0.310141 | 1032 |
| event_binary_B | pretrend_baseline_joint_zero       |                1 |    1.65084  | 0.198845 | 1032 |
| event_binary_B | pretrend_displacement_joint_zero   |                1 |    1.08226  | 0.298192 | 1032 |
| event_score_C  | pretrend_score_baseline_joint_zero |                1 |    0.022566 | 0.880591 | 1032 |
| event_score_C  | pretrend_score_slope_joint_zero    |                1 |    1.14252  | 0.285121 | 1032 |