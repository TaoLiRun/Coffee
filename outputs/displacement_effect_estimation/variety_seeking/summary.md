# Displacement Effect Estimation Summary

- Sample rows: 13,784
- Unique members: 1,723
- Unique closures: 22
- Event FE units: 1,723
- Relative periods: [-4, -3, -2, -1, 1, 2, 3, 4]
- Estimation mode: separate_effect=false
- Closure duration filter days: False
- Recency filter days: False
- Drop period-0 purchasers: True


## Binary Specs
| spec             | term                  |     n |   r2_within |      coef |        se |    pvalue |
|:-----------------|:----------------------|------:|------------:|----------:|----------:|----------:|
| binary_collapsed | post_X_treated        | 13784 |  0.00150656 |  0.084127 | 0.0863031 | 0.329803  |
| binary_collapsed | post_X_disp           | 13784 |  0.00150656 |  0.101117 | 0.0523249 | 0.0534646 |
| binary_collapsed | post_X_treated_X_disp | 13784 |  0.00150656 | -0.042621 | 0.0873414 | 0.625625  |

## Score Spec
| spec            | term                   |     n |   r2_within |       coef |        se |     pvalue |
|:----------------|:-----------------------|------:|------------:|-----------:|----------:|-----------:|
| score_collapsed | post_X_treated         | 13784 |  0.00111451 |  0.0418937 | 0.0142785 | 0.00339004 |
| score_collapsed | post_X_score           | 13784 |  0.00111451 |  0.0854047 | 0.0496075 | 0.0853203  |
| score_collapsed | post_X_treated_X_score | 13784 |  0.00111451 | -0.0767196 | 0.0992426 | 0.439598   |

## Event-study Specs
| spec           | term                                                              |         coef |        se |      pvalue |     n |   r2_within |
|:---------------|:------------------------------------------------------------------|-------------:|----------:|------------:|------:|------------:|
| event_att      | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0283056   | 0.0277172 | 0.30729     | 13784 |  0.00158194 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.0028645   | 0.0276499 | 0.9175      | 13784 |  0.00158194 |
| event_att      | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0226342   | 0.0258438 | 0.381256    | 13784 |  0.00158194 |
| event_att      | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.0493459   | 0.0279239 | 0.0773784   | 13784 |  0.00158194 |
| event_att      | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.0505251   | 0.0280249 | 0.0715835   | 13784 |  0.00158194 |
| event_att      | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0305025   | 0.0274693 | 0.266974    | 13784 |  0.00158194 |
| event_att      | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0165649   | 0.0253603 | 0.513725    | 13784 |  0.00158194 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.283993    | 0.149049  | 0.0568996   | 13784 |  0.00309717 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0439568   | 0.180661  | 0.807793    | 13784 |  0.00309717 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.117332    | 0.153227  | 0.443937    | 13784 |  0.00309717 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00319362  | 0.164394  | 0.984503    | 13784 |  0.00309717 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0513556   | 0.151556  | 0.73476     | 13784 |  0.00309717 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0446403   | 0.186312  | 0.810669    | 13784 |  0.00309717 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.00960127  | 0.130456  | 0.941339    | 13784 |  0.00309717 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.26647     | 0.151743  | 0.0792567   | 13784 |  0.00309717 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0481201   | 0.182583  | 0.792156    | 13784 |  0.00309717 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0997042   | 0.155221  | 0.520741    | 13784 |  0.00309717 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.0580433   | 0.166907  | 0.728064    | 13784 |  0.00309717 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.109252    | 0.154401  | 0.479298    | 13784 |  0.00309717 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.0795788   | 0.188278  | 0.672591    | 13784 |  0.00309717 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              | -0.00399365  | 0.133024  | 0.976053    | 13784 |  0.00309717 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.129662    | 0.0873151 | 0.13773     | 13784 |  0.00309717 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                | -0.0418545   | 0.079702  | 0.599555    | 13784 |  0.00309717 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                | -0.016198    | 0.0919567 | 0.860198    | 13784 |  0.00309717 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  0.0757153   | 0.0904002 | 0.402396    | 13784 |  0.00309717 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.0460522   | 0.0872456 | 0.597675    | 13784 |  0.00309717 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.00345037  | 0.107532  | 0.974406    | 13784 |  0.00309717 |
| event_binary_B | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.0978303   | 0.0757381 | 0.196637    | 13784 |  0.00309717 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.298662    | 0.148191  | 0.0440191   | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated                    | -0.0428119   | 0.166355  | 0.796937    | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0723327   | 0.138652  | 0.601956    | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated                     | -0.00131795  | 0.163476  | 0.993568    | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated                     | -0.0624911   | 0.163818  | 0.702903    | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated                     | -0.0273103   | 0.191339  | 0.886518    | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0425628   | 0.142609  | 0.765389    | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_disp             |  0.264157    | 0.15108   | 0.0805621   | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_disp             |  0.0378033   | 0.168579  | 0.822592    | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_disp             |  0.0422192   | 0.141104  | 0.764818    | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_disp              |  0.0428876   | 0.166236  | 0.796444    | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_disp              |  0.12227     | 0.166209  | 0.462049    | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated_X_disp              |  0.0470849   | 0.193412  | 0.807691    | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated_X_disp              |  0.0162003   | 0.144684  | 0.91086     | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:disp_binary                | -0.128967    | 0.087745  | 0.141802    | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:disp_binary                | -0.0417722   | 0.0797585 | 0.600531    | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_binary                | -0.0156059   | 0.091817  | 0.865055    | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_binary                 |  0.0727775   | 0.0905013 | 0.421415    | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_binary                 |  0.0356931   | 0.0886307 | 0.687206    | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:disp_binary                 | -0.0126949   | 0.107983  | 0.906427    | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:disp_binary                 |  0.0619316   | 0.0812774 | 0.446177    | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_len              | -0.0530128   | 0.142102  | 0.709149    | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_len              |  0.00309421  | 0.150601  | 0.98361     | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_len              |  0.236868    | 0.0893102 | 0.00807055  | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:treated_X_len               |  0.0333678   | 0.134047  | 0.803448    | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:treated_X_len               | -0.0340411   | 0.149595  | 0.820019    | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:treated_X_len               |  0.126267    | 0.15937   | 0.428302    | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:treated_X_len               | -0.0531806   | 0.118326  | 0.65317     | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:disp_X_len                 |  0.0114563   | 0.0165949 | 0.490067    | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:disp_X_len                 |  0.00247453  | 0.0142593 | 0.862249    | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:disp_X_len                 |  0.024145    | 0.011993  | 0.0442434   | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:disp_X_len                  |  0.00263185  | 0.0122962 | 0.830544    | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:disp_X_len                  | -0.0373226   | 0.0140646 | 0.00803573  | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:disp_X_len                  | -0.00405314  | 0.0159035 | 0.798863    | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:disp_X_len                  | -0.119465    | 0.0264086 | 6.49107e-06 | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-4]:tXdXlen                    |  0.0901664   | 0.144435  | 0.532534    | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-3]:tXdXlen                    |  0.0261781   | 0.15231   | 0.863557    | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[-2]:tXdXlen                    | -0.232995    | 0.0921935 | 0.0115853   | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[1]:tXdXlen                     | -0.0262243   | 0.136283  | 0.847432    | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[2]:tXdXlen                     |  0.0452753   | 0.151697  | 0.765389    | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[3]:tXdXlen                     | -0.118251    | 0.161177  | 0.463251    | 13784 |  0.00832804 |
| event_binary_D | C(rel_t, contr.treatment(base=-1))[4]:tXdXlen                     |  0.0858465   | 0.120673  | 0.476933    | 13784 |  0.00832804 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated                    | -0.0300154   | 0.0273755 | 0.273043    | 13784 |  0.00298858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated                    |  0.000109878 | 0.0271139 | 0.996767    | 13784 |  0.00298858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated                    | -0.0221506   | 0.025661  | 0.388147    | 13784 |  0.00298858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated                     |  0.050526    | 0.027879  | 0.0701089   | 13784 |  0.00298858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated                     |  0.051421    | 0.0282409 | 0.0688108   | 13784 |  0.00298858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated                     |  0.0309456   | 0.0272088 | 0.255554    | 13784 |  0.00298858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated                     | -0.0177767   | 0.025567  | 0.486963    | 13784 |  0.00298858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:treated_X_score            |  0.232519    | 0.18415   | 0.206881    | 13784 |  0.00298858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:treated_X_score            |  0.0517145   | 0.201926  | 0.7979      | 13784 |  0.00298858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:treated_X_score            |  0.101725    | 0.185787  | 0.584081    | 13784 |  0.00298858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:treated_X_score             |  0.0513899   | 0.196217  | 0.793427    | 13784 |  0.00298858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:treated_X_score             |  0.0606384   | 0.180145  | 0.736452    | 13784 |  0.00298858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:treated_X_score             |  0.119405    | 0.207957  | 0.565919    | 13784 |  0.00298858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:treated_X_score             | -0.154897    | 0.166212  | 0.351506    | 13784 |  0.00298858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-4]:displacement_prob_centered | -0.208427    | 0.0924084 | 0.0242273   | 13784 |  0.00298858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-3]:displacement_prob_centered | -0.0823717   | 0.0829837 | 0.321032    | 13784 |  0.00298858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[-2]:displacement_prob_centered | -0.04713     | 0.0958572 | 0.623016    | 13784 |  0.00298858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[1]:displacement_prob_centered  |  0.00782224  | 0.0936365 | 0.933433    | 13784 |  0.00298858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[2]:displacement_prob_centered  | -0.013303    | 0.0923129 | 0.885432    | 13784 |  0.00298858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[3]:displacement_prob_centered  | -0.0722931   | 0.100709  | 0.472954    | 13784 |  0.00298858 |
| event_score_C  | C(rel_t, contr.treatment(base=-1))[4]:displacement_prob_centered  |  0.0804547   | 0.0852727 | 0.345558    | 13784 |  0.00298858 |

## Pre-trend Joint Tests
| spec           | test                                    |   n_restrictions |   statistic |    pvalue |     n |
|:---------------|:----------------------------------------|-----------------:|------------:|----------:|------:|
| event_att      | pretrend_att_joint_zero                 |                3 |     2.23609 | 0.524875  | 13784 |
| event_binary_B | pretrend_baseline_joint_zero            |                3 |     6.11066 | 0.106349  | 13784 |
| event_binary_B | pretrend_displacement_joint_zero        |                3 |     4.80671 | 0.18651   | 13784 |
| event_binary_D | pretrend_length_displacement_joint_zero |                3 |     9.19484 | 0.0268095 | 13784 |
| event_binary_D | pretrend_length_baseline_joint_zero     |                3 |     9.43358 | 0.0240485 | 13784 |
| event_score_C  | pretrend_score_baseline_joint_zero      |                3 |     2.17272 | 0.537343  | 13784 |
| event_score_C  | pretrend_score_slope_joint_zero         |                3 |     1.91975 | 0.589228  | 13784 |