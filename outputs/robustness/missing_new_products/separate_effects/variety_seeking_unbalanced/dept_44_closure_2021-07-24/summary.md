# Displacement Effect Estimation Summary

- Sample rows: 12,504
- Unique members: 1,563
- Unique closures: 1
- Event FE units: 1,563
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=true
- Closure event: `dept_44_closure_2021-07-24`
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Length-heterogeneity event-study spec skipped: true
- Model type: DDD


## Binary Specs
| spec             | term                  |    n |   r2_within |       coef |        se |    pvalue |
|:-----------------|:----------------------|-----:|------------:|-----------:|----------:|----------:|
| binary_collapsed | post_X_treated        | 3709 |  0.00205761 |  0.0475202 | 0.0631895 | 0.452241  |
| binary_collapsed | post_X_disp           | 3709 |  0.00205761 |  0.0772749 | 0.0325739 | 0.0178983 |
| binary_collapsed | post_X_treated_X_disp | 3709 |  0.00205761 | -0.0667247 | 0.0757525 | 0.37866   |

## Score Spec
| spec            | term                   |    n |   r2_within |      coef |        se |     pvalue |
|:----------------|:-----------------------|-----:|------------:|----------:|----------:|-----------:|
| score_collapsed | post_X_treated         | 3709 |  0.00385218 |  0.022114 | 0.0487528 | 0.650236   |
| score_collapsed | post_X_score           | 3709 |  0.00385218 |  0.144903 | 0.0465548 | 0.00191654 |
| score_collapsed | post_X_treated_X_score | 3709 |  0.00385218 | -0.030742 | 0.0983489 | 0.754675   |

## Event-study Specs
| spec           | term                                                              |        coef |        se |     pvalue |    n |   r2_within |
|:---------------|:------------------------------------------------------------------|------------:|----------:|-----------:|-----:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.082019   | 0.0599721 | 0.17179    | 3709 |  0.00276637 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.149572   | 0.0548957 | 0.00656799 | 3709 |  0.00276637 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.105271   | 0.0633111 | 0.0967279  | 3709 |  0.00276637 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.0306353  | 0.0678423 | 0.651695   | 3709 |  0.00276637 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0995835  | 0.0626299 | 0.112197   | 3709 |  0.00276637 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0787084  | 0.0635087 | 0.215562   | 3709 |  0.00276637 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.112604   | 0.0631772 | 0.0750461  | 3709 |  0.00276637 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.145151   | 0.0991733 | 0.143668   | 3709 |  0.00912432 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.173815   | 0.0845253 | 0.0400495  | 3709 |  0.00912432 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.189486   | 0.130038  | 0.14544    | 3709 |  0.00912432 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.0927445  | 0.110907  | 0.403256   | 3709 |  0.00912432 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0622193  | 0.100226  | 0.534902   | 3709 |  0.00912432 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.110998   | 0.100425  | 0.269347   | 3709 |  0.00912432 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0234036  | 0.100826  | 0.816501   | 3709 |  0.00912432 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.1112     | 0.124026  | 0.370192   | 3709 |  0.00912432 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0436336  | 0.111951  | 0.696815   | 3709 |  0.00912432 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.125212   | 0.147992  | 0.397752   | 3709 |  0.00912432 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.118393   | 0.139596  | 0.396615   | 3709 |  0.00912432 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.0815084  | 0.127287  | 0.522114   | 3709 |  0.00912432 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.0851763  | 0.128372  | 0.507181   | 3709 |  0.00912432 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.155992   | 0.129727  | 0.229517   | 3709 |  0.00912432 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.0373623  | 0.0623985 | 0.549486   | 3709 |  0.00912432 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                | -0.0229216  | 0.0594641 | 0.699985   | 3709 |  0.00912432 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                | -0.0730281  | 0.060597  | 0.228481   | 3709 |  0.00912432 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.00617362 | 0.0679682 | 0.927648   | 3709 |  0.00912432 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.00649973 | 0.0610887 | 0.915291   | 3709 |  0.00912432 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 |  0.0409989  | 0.0638713 | 0.521111   | 3709 |  0.00912432 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.124046   | 0.066392  | 0.0620502  | 3709 |  0.00912432 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.11545    | 0.0857498 | 0.178544   | 3709 |  0.0117513  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.168707   | 0.0707165 | 0.017264   | 3709 |  0.0117513  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.147167   | 0.102052  | 0.149648   | 3709 |  0.0117513  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.0913274  | 0.0889751 | 0.304976   | 3709 |  0.0117513  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0914859  | 0.0810165 | 0.259119   | 3709 |  0.0117513  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0901698  | 0.0798205 | 0.258937   | 3709 |  0.0117513  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0628593  | 0.0814449 | 0.440445   | 3709 |  0.0117513  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.13969    | 0.181371  | 0.441401   | 3709 |  0.0117513  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.0794568  | 0.156413  | 0.611588   | 3709 |  0.0117513  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.14648    | 0.201833  | 0.468191   | 3709 |  0.0117513  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.281008   | 0.183858  | 0.126784   | 3709 |  0.0117513  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.0271473  | 0.171098  | 0.87397    | 3709 |  0.0117513  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.13211    | 0.169443  | 0.4358     | 3709 |  0.0117513  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             | -0.176673   | 0.181658  | 0.331047   | 3709 |  0.0117513  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.0521746  | 0.0904042 | 0.564006   | 3709 |  0.0117513  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered | -0.0338506  | 0.0898425 | 0.706432   | 3709 |  0.0117513  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered | -0.127067   | 0.0902287 | 0.159413   | 3709 |  0.0117513  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0115847  | 0.0951454 | 0.903119   | 3709 |  0.0117513  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  |  0.0365608  | 0.0896232 | 0.68342    | 3709 |  0.0117513  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  |  0.0899128  | 0.0911702 | 0.32431    | 3709 |  0.0117513  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  |  0.236837   | 0.0953623 | 0.0131985  | 3709 |  0.0117513  |

## Pre-trend Joint Tests
| spec           | test                               |   n_restrictions |   statistic |    pvalue |    n |
|:---------------|:-----------------------------------|-----------------:|------------:|----------:|-----:|
| event_att      | pretrend_att_joint_zero            |                3 |    7.64056  | 0.0540548 | 3709 |
| event_binary_B | pretrend_baseline_joint_zero       |                3 |    4.68882  | 0.196054  | 3709 |
| event_binary_B | pretrend_displacement_joint_zero   |                3 |    1.10529  | 0.775798  | 3709 |
| event_score_C  | pretrend_score_baseline_joint_zero |                3 |    5.93874  | 0.114629  | 3709 |
| event_score_C  | pretrend_score_slope_joint_zero    |                3 |    0.813617 | 0.846207  | 3709 |