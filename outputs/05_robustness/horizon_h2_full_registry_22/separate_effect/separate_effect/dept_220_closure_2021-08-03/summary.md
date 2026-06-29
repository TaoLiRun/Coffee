# Displacement Effect Estimation Summary

- Sample rows: 7,336
- Unique members: 1,834
- Unique closures: 1
- Event FE units: 1,834
- Relative periods: [-2, -1, 1, 2]
- Estimation mode: separate_effect=true
- Closure event: `dept_220_closure_2021-08-03`
- Closure duration filter days: False
- Recency filter days: False
- Length-heterogeneity event-study spec skipped: true


## Binary Specs
| spec             | term                  |    n |   r2_within |       coef |         se |      pvalue |
|:-----------------|:----------------------|-----:|------------:|-----------:|-----------:|------------:|
| binary_collapsed | post_X_treated        | 7336 |  0.00711563 | -0.0102199 | 0.00296511 | 0.000580235 |
| binary_collapsed | post_X_disp           | 7336 |  0.00711563 | -0.0194145 | 0.0100381  | 0.0532571   |
| binary_collapsed | post_X_treated_X_disp | 7336 |  0.00711563 | -0.0130039 | 0.0192183  | 0.498718    |

## Score Spec
| spec            | term                   |    n |   r2_within |       coef |         se |     pvalue |
|:----------------|:-----------------------|-----:|------------:|-----------:|-----------:|-----------:|
| score_collapsed | post_X_treated         | 7336 |   0.0107064 | -0.0147203 | 0.00644046 | 0.0223918  |
| score_collapsed | post_X_score           | 7336 |   0.0107064 | -0.0348894 | 0.0135177  | 0.00992792 |
| score_collapsed | post_X_treated_X_score | 7336 |   0.0107064 | -0.0214067 | 0.0285084  | 0.452814   |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0118009   | 0.00497853 | 0.0178737   | 7336 |  0.00299472 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00342553  | 0.00400785 | 0.392826    | 7336 |  0.00299472 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00737397  | 0.00484783 | 0.128411    | 7336 |  0.00299472 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0104152   | 0.00424106 | 0.0141492   | 7336 |  0.0481695  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.0037968   | 0.00308451 | 0.21851     | 7336 |  0.0481695  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0062278   | 0.00372263 | 0.0945069   | 7336 |  0.0481695  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0305811   | 0.0196372  | 0.119572    | 7336 |  0.0481695  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.002646    | 0.0200542  | 0.895044    | 7336 |  0.0481695  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.00192719  | 0.0241341  | 0.936363    | 7336 |  0.0481695  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                |  0.075588    | 0.0113058  | 3.04021e-11 | 7336 |  0.0481695  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  2.50348e-05 | 0.0113053  | 0.998233    | 7336 |  0.0481695  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.036734    | 0.0127819  | 0.00410115  | 7336 |  0.0481695  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0218972   | 0.00688902 | 0.00150474  | 7336 |  0.0566858  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00277035  | 0.00674482 | 0.681313    | 7336 |  0.0566858  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.00477296  | 0.00807194 | 0.55439     | 7336 |  0.0566858  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.0634102   | 0.0269098  | 0.0185578   | 7336 |  0.0566858  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.00791504  | 0.0295911  | 0.789129    | 7336 |  0.0566858  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.0126816   | 0.0357405  | 0.722761    | 7336 |  0.0566858  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered |  0.102097    | 0.0156047  | 7.81615e-11 | 7336 |  0.0566858  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.00922329  | 0.0151907  | 0.543815    | 7336 |  0.0566858  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  |  0.0415415   | 0.0174422  | 0.017336    | 7336 |  0.0566858  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |     pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|-----------:|-----:|
| event_att      | pretrend_att_joint_zero            |                1 |     5.61861 | 0.0177708  | 7336 |
| event_binary_B | pretrend_baseline_joint_zero       |                1 |     6.03097 | 0.014057   | 7336 |
| event_binary_B | pretrend_displacement_joint_zero   |                1 |     2.42519 | 0.119399   | 7336 |
| event_score_C  | pretrend_score_baseline_joint_zero |                1 |    10.1033  | 0.00148005 | 7336 |
| event_score_C  | pretrend_score_slope_joint_zero    |                1 |     5.55262 | 0.0184531  | 7336 |