# Displacement Effect Estimation Summary

- Sample rows: 321,184
- Unique members: 40,148
- Unique closures: 18
- Event FE units: 40,148
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=false
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: False
- Model type: DDD


## Binary Specs
| spec             | term                  |     n |   r2_within |        coef |         se |     pvalue |
|:-----------------|:----------------------|------:|------------:|------------:|-----------:|-----------:|
| binary_collapsed | post_X_treated        | 99644 | 0.000260742 |  0.00436141 | 0.0103815  | 0.674408   |
| binary_collapsed | post_X_disp           | 99644 | 0.000260742 | -0.0166337  | 0.00584757 | 0.00445125 |
| binary_collapsed | post_X_treated_X_disp | 99644 | 0.000260742 |  0.0198844  | 0.0131844  | 0.131523   |

## Score Spec
| spec            | term                   |     n |   r2_within |       coef |         se |    pvalue |
|:----------------|:-----------------------|------:|------------:|-----------:|-----------:|----------:|
| score_collapsed | post_X_treated         | 99644 |  0.00021008 |  0.0120841 | 0.00886144 | 0.172685  |
| score_collapsed | post_X_score           | 99644 |  0.00021008 | -0.0214261 | 0.00924422 | 0.0204697 |
| score_collapsed | post_X_treated_X_score | 99644 |  0.00021008 |  0.0156341 | 0.0202449  | 0.439975  |

## Event-study Specs
| spec           | term                                                              |         coef |         se |      pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|-----------:|------------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.00739855  | 0.0102023  | 0.468348    | 99644 | 0.00031128  |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.00149623  | 0.0104551  | 0.886204    | 99644 | 0.00031128  |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.00520672  | 0.0100894  | 0.605819    | 99644 | 0.00031128  |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.000727766 | 0.0109049  | 0.946791    | 99644 | 0.00031128  |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0166705   | 0.0116267  | 0.15164     | 99644 | 0.00031128  |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0401155   | 0.0121282  | 0.000942355 | 99644 | 0.00031128  |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0227294   | 0.0124489  | 0.067892    | 99644 | 0.00031128  |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.0281127   | 0.0180696  | 0.119769    | 99644 | 0.000960878 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.0167137   | 0.0187839  | 0.373589    | 99644 | 0.000960878 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0213423   | 0.0199514  | 0.28476     | 99644 | 0.000960878 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0182691   | 0.0195401  | 0.349823    | 99644 | 0.000960878 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0204112   | 0.0199966  | 0.307392    | 99644 | 0.000960878 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0382605   | 0.020325   | 0.0597891   | 99644 | 0.000960878 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0080523   | 0.0204617  | 0.693932    | 99644 | 0.000960878 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             | -0.0331842   | 0.0218434  | 0.128728    | 99644 | 0.000960878 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             | -0.0284293   | 0.0224982  | 0.206378    | 99644 | 0.000960878 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.0236425   | 0.0229085  | 0.302063    | 99644 | 0.000960878 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0307857   | 0.0233894  | 0.188111    | 99644 | 0.000960878 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.00532109  | 0.0244738  | 0.827883    | 99644 | 0.000960878 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.00445474  | 0.0253008  | 0.86024     | 99644 | 0.000960878 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.0277695   | 0.0257142  | 0.280185    | 99644 | 0.000960878 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.0374765   | 0.00897044 | 2.95448e-05 | 99644 | 0.000960878 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                | -0.0258454   | 0.00931112 | 0.00551176  | 99644 | 0.000960878 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                | -0.0156171   | 0.00967832 | 0.106624    | 99644 | 0.000960878 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0292863   | 0.0101947  | 0.00407367  | 99644 | 0.000960878 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0326415   | 0.0105687  | 0.0020141   | 99644 | 0.000960878 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0476139   | 0.0112076  | 2.16183e-05 | 99644 | 0.000960878 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0395578   | 0.0114425  | 0.000546985 | 99644 | 0.000960878 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.0243941   | 0.0177983  | 0.170516    | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.014013    | 0.0186623  | 0.452737    | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0203449   | 0.0196876  | 0.301433    | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0230061   | 0.0195148  | 0.238449    | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0162581   | 0.0199428  | 0.414944    | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0337108   | 0.0201652  | 0.0945899   | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0040513   | 0.0204748  | 0.84315     | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             | -0.0345038   | 0.0214903  | 0.108385    | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             | -0.0241374   | 0.0225936  | 0.285384    | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             | -0.0222575   | 0.0229468  | 0.332076    | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              | -0.0352239   | 0.0241791  | 0.145187    | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              | -0.00251917  | 0.0251883  | 0.920334    | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              | -0.0126089   | 0.0263989  | 0.632917    | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.0192449   | 0.0272467  | 0.479994    | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.0404971   | 0.00883713 | 4.61588e-06 | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                | -0.0294621   | 0.00919693 | 0.00135964  | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                | -0.0171071   | 0.00959219 | 0.0745285   | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 | -0.0233153   | 0.0101445  | 0.0215521   | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 | -0.0380196   | 0.010497   | 0.000293019 | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.051366    | 0.0111801  | 4.36202e-06 | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 | -0.0430895   | 0.0114012  | 0.000157603 | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_len              |  0.0310821   | 0.0160905  | 0.0534072   | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_len              |  0.0285149   | 0.0158516  | 0.0720538   | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_len              |  0.00322173  | 0.016741   | 0.847395    | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_len               | -0.015373    | 0.0161611  | 0.341494    | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_len               |  0.0336286   | 0.0166045  | 0.0428509   | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated_X_len               |  0.0350492   | 0.0169425  | 0.0385839   | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated_X_len               |  0.0547528   | 0.0175649  | 0.0018282   | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:disp_X_len                 |  0.0203412   | 0.00615606 | 0.000953736 | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:disp_X_len                 |  0.0175245   | 0.00563754 | 0.00188241  | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_X_len                 |  0.0040969   | 0.00483458 | 0.396772    | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_X_len                  | -0.0197112   | 0.00577951 | 0.000649469 | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_X_len                  |  0.0199309   | 0.00654625 | 0.00233233  | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:disp_X_len                  |  0.019187    | 0.00722834 | 0.00795008  | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:disp_X_len                  |  0.0313869   | 0.00948158 | 0.000933365 | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:tXdXlen                    | -0.031392    | 0.0190614  | 0.0995952   | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:tXdXlen                    | -0.0337435   | 0.0189807  | 0.0754526   | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:tXdXlen                    | -0.00356461  | 0.0192568  | 0.853145    | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:tXdXlen                     |  0.0284573   | 0.0196652  | 0.147886    | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:tXdXlen                     | -0.0423171   | 0.0205864  | 0.0398335   | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:tXdXlen                     | -0.0146647   | 0.0213426  | 0.49202     | 99644 | 0.00240651  |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:tXdXlen                     | -0.0460831   | 0.0223085  | 0.0388655   | 99644 | 0.00240651  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    |  0.0156047   | 0.0154906  | 0.31377     | 99644 | 0.00105807  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.00975469  | 0.0161354  | 0.545483    | 99644 | 0.00105807  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    |  0.0198902   | 0.0170892  | 0.244476    | 99644 | 0.00105807  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0143465   | 0.016535   | 0.385598    | 99644 | 0.00105807  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.021661    | 0.0167933  | 0.197114    | 99644 | 0.00105807  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0422282   | 0.0171212  | 0.0136542   | 99644 | 0.00105807  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     |  0.0137817   | 0.0172924  | 0.425472    | 99644 | 0.00105807  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            | -0.0253672   | 0.0331541  | 0.444203    | 99644 | 0.00105807  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            | -0.0363649   | 0.0342454  | 0.288295    | 99644 | 0.00105807  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            | -0.0429111   | 0.0346081  | 0.215019    | 99644 | 0.00105807  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             | -0.0514175   | 0.034367   | 0.134633    | 99644 | 0.00105807  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             | -0.0159316   | 0.0360453  | 0.658503    | 99644 | 0.00105807  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             | -0.00523782  | 0.0377316  | 0.889595    | 99644 | 0.00105807  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             |  0.040644    | 0.0381078  | 0.286185    | 99644 | 0.00105807  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.0773642   | 0.0139314  | 2.83473e-08 | 99644 | 0.00105807  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered | -0.0573045   | 0.014521   | 7.95969e-05 | 99644 | 0.00105807  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered | -0.0332688   | 0.0153729  | 0.0304654   | 99644 | 0.00105807  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  | -0.0548417   | 0.015561   | 0.000425421 | 99644 | 0.00105807  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.0668059   | 0.0161322  | 3.46787e-05 | 99644 | 0.00105807  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.0780758   | 0.0171208  | 5.13423e-06 | 99644 | 0.00105807  |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  | -0.0624631   | 0.017545   | 0.00037136  | 99644 | 0.00105807  |

## Pre-trend Joint Tests
| spec           | test                                    |   n_restrictions |   statistic |   pvalue |     n |
|:---------------|:----------------------------------------|-----------------:|------------:|---------:|------:|
| event_att      | pretrend_att_joint_zero                 |                3 |     1.30523 | 0.727892 | 99644 |
| event_binary_B | pretrend_baseline_joint_zero            |                3 |     2.54749 | 0.46677  | 99644 |
| event_binary_B | pretrend_displacement_joint_zero        |                3 |     2.42839 | 0.488371 | 99644 |
| event_binary_D | pretrend_length_displacement_joint_zero |                3 |     5.13271 | 0.162333 | 99644 |
| event_binary_D | pretrend_length_baseline_joint_zero     |                3 |     6.05497 | 0.108966 | 99644 |
| event_score_C  | pretrend_score_baseline_joint_zero      |                3 |     1.63851 | 0.65069  | 99644 |
| event_score_C  | pretrend_score_slope_joint_zero         |                3 |     1.75594 | 0.624569 | 99644 |