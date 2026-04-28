# Stopping Shopping at Stop and Shop? How Temporary Disruptions Affect Store Choice

**Julia Levine†** | **Sylvia Hristakeva‡**

*Click here for the most recent version.*  
*This draft: January 5, 2026*

---

## Abstract

Shopping patterns in retail markets are highly persistent, with households patronizing the same stores over time. Whether this persistence reflects unobserved heterogeneity or a causal effect of past choices through state dependence remains an open question. We study an 11-day strike that effectively closed 240 Stop & Shop grocery stores, using a novel identification strategy to isolate the strike's long-term effects on consumer demand through state dependence. We find that the strike caused households to make 9.9% fewer trips to S&S after the strike's resolution, simply by displacing planned visits during the strike. The reduction is observed immediately in the period after the strike's resolution and attenuates only gradually over time. The effect of trip displacement is larger for households who, during the strike, visit a store that they had not previously visited, suggesting that state dependence in store choice is partially driven by search and learning frictions. These results support an economically meaningful role of state dependence in grocery store choice, suggesting that temporary supply disruptions, and marketing tactics that induce consumer switching, can have long-term effects on profitability.

**Keywords:** Store Choice, State Dependence, Retailer Loyalty, Store Closure, Employee Strikes, Social Consumerism

---

## 1. Introduction

Consumers exhibit strong persistence in where they shop, repeatedly choosing the same firms, even when close substitutes are readily available. This persistence may be driven by:

- **Structural state dependence**: Past choices causally affect present choices through mechanisms like loyalty, learning, or search costs
- **Spurious state dependence**: Unobserved heterogeneity, such as preferences and income, influences both past and present choices (Heckman, 1981)

Understanding the role of structural state dependence in driving choices is important for understanding consumer demand and firm competition. Prior work in economics and marketing has documented state dependence in settings such as brand and health insurance plan choice (Dubé et al., 2010; Pakes et al., 2021). We study state dependence in **store choice**, a setting in which persistence is both pronounced and economically meaningful (Rhee and Bell, 2002).

### The Strike Setting

An ideal experiment to quantify state dependence would randomly displace trips to a given store for a single time period. We identify this effect in the context of the **2019 labor strike by employees of Stop & Shop (S&S)**:

| Detail | Information |
|--------|-------------|
| **Date** | April 11, 2019 |
| **Duration** | 11 days |
| **Workers** | ~31,000 employees |
| **Stores Affected** | 240 stores |
| **Regions** | Connecticut, Massachusetts, Rhode Island |
| **Issue** | Wages, healthcare, retirement benefits |

The strike sharply disrupted access to stores, forcing consumers to forgo grocery trips or shop elsewhere, providing a rare opportunity to observe how consumers respond when regular shopping patterns are interrupted and then restored.

### Economic Importance

The United States has seen a sharp uptick in labor stoppages, with 33 major strikes in 2023, setting a 20-year record (Bureau of Labor Statistics, 2024). Key questions:

> - Do customers return once normal operations resume?
> - Do temporary disruptions lead to persistent re-allocations of demand?

This distinction matters for firms, workers, and policymakers. If temporary supply disruptions have lasting effects on demand, then the economic costs of strikes may extend well beyond their resolution.

---

## 2. Setting and Data

### 2.1 The Stop & Shop Strikes of 2019

Stop & Shop is a large grocery chain operating in the Northeastern United States, with a market share of just over 20% in 2019 (The Shelby Report, 2019).

**Strike Timeline:**
- **February 23, 2019**: UFCW contracts expire
- **April 10, 2019**: Ahold Delhaize shareholders vote to increase dividends by 11.1%
- **April 11, 2019**: ~31,000 workers walk off the job
- **April 21, 2019**: Tentative agreement reached; strike ends

**Store Operations During Strike:**
- Limited hours of operation
- Irregular shipments
- Labor-intensive departments closed
- Customers had to walk past striking workers

**Impact on Trips:**
```
• 92% decrease in trips to striking region stores
• 35% drop in average basket expenditure (conditional on trip)
• Non-striking region (NY, NJ): 3% increase in visits
```

### 2.2 Data and Descriptive Patterns

We use household shopping data from **Numerator**, a market research company that runs a large representative household panel in the United States.

**Data Features:**
- Shopping trips and expenditures across retail outlets
- Date, retailer name, quantities, and prices for each trip
- Store location for 45% of trips (used to infer region)
- Demographics: household size, income bracket, age, zip code

**Period Definition:**
- Period 0: 11-day strike window (April 11–21)
- Other periods: 11-day windows centered on period 0
- Sample: 9 periods before strike, 12 periods after

```
Timeline Notation:
-9  -2  -1   0   1   11  12
|---Pre---|During|---Post---|
```

### Changes in Promotions After the Strike

We measure promotional intensity as the percentage difference between list prices and paid prices ("discount").

**Regression Specification:**
```math
discount_{kjmt} = α_{kjm} + ω_t + \sum_{l=-8}^{12} β_l I(j=S\&S) × I(t=l) + ν_{kjmt}
```

Where:
- `α_{kjm}`: item-by-retailer-by-state fixed effects
- `ω_t`: time fixed effects
- `β_l`: captures average changes in S&S's discounts relative to local competitors

**Key Finding:** S&S increased discounts relative to competitors immediately as the strike began, consistent with strategic promotional response.

---

## 3. Conceptual Framework

### Stylized Model of Store Choice

Consumer *i*'s indirect utility from visiting retailer *r* at time *t*:

```math
U_{irt} = α_{rt} + γ × 1(r ∈ R_{i,t-1}) + ε_{irt}
```

| Component | Description |
|-----------|-------------|
| `α_{rt}` | Firm-specific intercept (baseline demand): prices, assortment, reputation |
| `γ × 1(r ∈ R_{i,t-1})` | State dependence term: added utility from visiting a previously visited retailer |
| `ε_{irt}` | Extreme value type I shock, independent across consumers, retailers, time |

**Interpretation of γ:**
- `γ > 0`: Positive state dependence (inertia, learning, search costs)
- `γ = 0`: No state dependence (choices independent across time)
- `γ < 0`: Negative state dependence (variety-seeking)

### Choice Condition

Consumer visits S&S (indexed *s*) if:
```math
U_{ist} ≥ U_{is't}
```

Rearranging:
```math
\underbrace{α_{st} + γ × [1(s ∈ R_{i,t-1}) - 1(s' ∈ R_{i,t-1})]}_{V^*_{it}} ≥ \underbrace{ε_{is't} - ε_{ist}}_{ε^*_{it}}
```

### Simulation Scenarios

| Scenario | γ | Δα₀ | Pattern |
|----------|---|-----|---------|
| 1 | 0 | 0 | Trips drop during strike, immediate return |
| 2 | 0 | < 0 | Temporary negative shock to baseline demand |
| 3 | > 0 | 0 | Slower return due to state dependence |
| 4 | > 0 | < 0 | Largest effect: both mechanisms operate |

### Mechanisms of Interest

We aim to separate two mechanisms:

1. **D: Displacement Effect**  
   Effect of forcing consumers to forgo planned trips during the strike, *without* changing baseline demand.

2. **B: Baseline-Demand Effect**  
   Additional change driven by shifts in baseline demand (reputation, firm response, etc.).

### Identification Intuition

Consider two groups of households differing only in whether they planned to visit S&S during the strike:

**Displaced Household** (would have visited S&S at t=0 absent strike):
```math
ΔV^*_1(disp) = [α_{s1}(1) - γ] - [α_{s1}(0) + γ] = α_{s1}(1) - α_{s1}(0) - 2γ
```

**Non-Displaced Household** (would not have visited S&S at t=0 regardless):
```math
ΔV^*_1(non) = [α_{s1}(1) - γ] - [α_{s1}(0) - γ] = α_{s1}(1) - α_{s1}(0)
```

**Key Insight:** Taking the difference isolates the displacement effect (-2γ) under the assumption that baseline demand changes are equal across groups.

---

## 4. Empirical Implementation

### 4.1 Identification Approach

**Four-Group Structure:**

| | Displaced | Non-Displaced |
|---|-----------|---------------|
| **Treated (S&S)** | Row 1: Δᴰ + Δᴮ + Δᵀ | Row 2: Δᴮ + Δᵀ |
| **Control** | Row 3: Δᵀ | Row 4: Δᵀ |

**Triple-Difference Estimator:**
```math
(ΔTrips_{d,s} - ΔTrips_{d,c}) - (ΔTrips_{n,s} - ΔTrips_{n,c}) = Δᴰ_{d,s} + (Δᴮ_{d,s} - Δᴮ_{n,s}) + (Δᵀ terms)
```

**Identifying Assumptions:**

1. **A1 (Parallel Trends):**  
   - a) Zero trend difference within displacement groups: Δᵀₙ,ₛ = Δᵀₙ,𝒸 and Δᵀ𝒹,ₛ = Δᵀ𝒹,𝒸  
   - OR b) Same trend difference across displacement groups

2. **A2 (Equal Baseline-Demand Effects):**  
   Δᴮ𝒹,ₛ = Δᴮₙ,ₛ

### Regression Specification

**Main Specification (Equation 9):**
```math
Trips_{it} = δᴮ I(t>0)×I(S\&S_i=1) + δᴰ I(t>0)×I(S\&S_i=1)×I(displaced_i=1) + β I(t>0)×I(displaced_i=1) + φ_i + ω_t + ν_{it}
```

| Coefficient | Interpretation |
|-------------|---------------|
| `δᴮ` | ATT for non-displaced households (baseline-demand effect) |
| `δᴰ` | Difference in ATTs between displaced/non-displaced (displacement effect) |

**Event Study Specification (Equation 10):**
```math
Trips_{it} = \sum_{l=-8}^{12} δ^B_l I(t=l)×I(S\&S_i=1) + \sum_{l=-8}^{12} δ^D_l I(t=l)×I(S\&S_i=1)×I(displaced_i=1) + \sum_{l=-8}^{12} β_l I(t=l)×I(displaced_i=1) + φ_i + ω_t + ν_{it}
```

### 4.2 Defining Treated and Control Groups

**Treated Households:**
- Visited a S&S store in the striking region (MA, CT, RI)
- In at least 2 distinct time periods during the 9 pre-strike periods

**Control Households:**
- Visited The Giant Company or Giant Food (sister chains, same parent company)
- In geographically proximate but non-overlapping regions (PA, MD, VA, WV, DE, DC)
- Did not shop within 20 miles of any S&S location pre-strike

**Final Sample:**
- 2,697 treated households
- 5,175 control households
- Only households who visited a grocery store during the strike period

### Demographic Comparison (Table 2)

| Variable | Treated | Control | Difference | p-value |
|----------|---------|---------|------------|---------|
| Age | 47.143 | 47.185 | -0.042 | 0.865 |
| Car Ownership | 0.880 | 0.889 | -0.009 | 0.223 |
| Household Size | 2.952 | 3.031 | -0.080** | 0.022 |
| Income $125,000+ | 0.251 | 0.268 | -0.017 | 0.101 |
| Income $40K-$125K | 0.525 | 0.552 | -0.027** | 0.023 |
| Income $0-$40K | 0.223 | 0.179 | 0.044*** | 0.000 |

### 4.3 Classifying Customers: Displaced vs. Non-Displaced

**Method:** Random Forest prediction model

**Training Data:** Pre-strike period behavior

**Features Include:**
- Share of total trips to focal retailer in last period
- Days since last purchase of routine staples (milk, eggs)
- Demographics, day-of-week patterns, expenditure patterns

**Model Details:**
- 500 decision trees, bootstrapped samples
- Final prediction: majority vote across trees
- ~55% of households classified as displaced

**Prediction Accuracy (Table 3):**

| Period | Control | S&S (Treated) |
|--------|---------|---------------|
| t = -1 | 0.774 | 0.767 |
| t = 0 (strike) | 0.773 | 0.454 |

*Note: Lower accuracy for treated at t=0 reflects the strike's supply disruption, not model failure.*

### 4.4 Sample and Identifying Variation

**Figure 5 Patterns:**

*Non-Displaced Households (Left Panel):*
- Parallel pre-strike trends between treated and control
- Post-strike: gap widens (S&S households make more trips)
- Identifies baseline-demand effect under parallel trends

*Displaced Households (Right Panel):*
- Parallel pre-strike trends
- During strike: displaced S&S households make zero trips vs. 2.45 for controls
- Post-strike: larger gap emerges
- Captures combined baseline-demand + displacement effects

**Key Observation:** Pre-strike trends differ by displacement status due to state dependence mechanics—households predicted to visit at t=0 show upward pre-strike trends; those predicted not to visit show downward trends.

### 4.5 Threats to Identification and Robustness Analyses

#### Misclassification of Displacement Status

**Problem:** Prediction error may misclassify households, biasing displacement effect toward zero.

**Solution:** 
- Use observed control household behavior at t=0 (no strike disruption) to identify and remove misclassified controls
- Appendix D shows this correction reduces bias

#### Equal Baseline-Demand Effects

**Potential Violations:**
1. Different pre-strike baseline demand levels across groups
2. Strike affects baseline demand differently by displacement status

**Robustness: Matched Subsample Analysis**
- Coarsened exact one-to-one matching on:
  - Pre-strike share of trips to focal retailer
  - Probability of revisiting focal retailer conditional on last-period visit
- Restricts to common support
- Assumes matched displaced/non-displaced households have equal pre-strike baseline demand

**Diagnostic Test (Equation 13):**
```math
Trips_{it} = \sum_{l=-8}^{12} δ_l × I(t=l)×I(displaced_i=1) + φ_i + ω_t + ν_{it}
```
- If δₗ not significantly different from zero → similar baseline-demand shifts → unbiased displacement estimate

#### Parallel Trends

**Assessment:**
- Full sample: slight pre-strike trend deviation, but equal across displacement groups → triple-differences unbiased
- Matched sample: parallel trends within each displacement group → all estimators unbiased

---

## 5. Results and Decomposition

### 5.1 Overall Changes in Shopping Trips After the Strike

**Table 4: ATT Estimates on Trips to Focal Retailer**

| | All | Displaced | Non-displaced |
|---|-----|-----------|---------------|
| S&S × post | -0.0539*** | -0.1451*** | 0.0538*** |
| | (0.0183) | (0.0304) | (0.0152) |
| Observations | 140,595 | 78,393 | 62,202 |
| R² | 0.59558 | 0.50242 | 0.18643 |

**Interpretation:**
- **Full sample:** 4.38% decrease in trips per period post-strike
- **Displaced:** 0.1451 fewer trips (large negative effect)
- **Non-displaced:** 0.0538 *more* trips (suggests successful firm response counteracting negative reputational effects)

**Event Study (Figure 7):**
- Negative effect concentrated in first 7 post-strike periods (~2 months)
- Gradual convergence toward pre-strike levels

### 5.2 Separately Identifying Mechanisms of Interest

**Table 5: Identifying Effects of Trip Displacement and Baseline Demand**

| | All Households | Matched Subsample |
|---|---------------|-------------------|
| S&S × post (Baseline-demand) | 0.0538*** | 0.0394 |
| | (0.0152) | (0.0406) |
| displaced × S&S × post (Displacement) | -0.1989*** | -0.2233*** |
| | (0.0340) | (0.0743) |
| Observations | 140,595 | 26,250 |

**Key Result:** 
> Displaced households make **0.20 fewer trips per period** as a result of the skipped visit—an **almost 9.9% decline** relative to pre-strike shopping intensity.

**Temporal Pattern (Figure 8):**
- Displacement effect emerges immediately after missed visit (period 0)
- Persists throughout 4-month post-strike window
- Gradually attenuates over time

**Revenue Impact Calculation:**
```
• Displacement effect: -0.20 trips/household/period
• Pre-strike basket total (displaced): $41.64
• Displaced households in sample: 1,427
• Pre-strike period revenue (estimation sample): $142,391.30

→ Estimated revenue loss: 8.56% per period in 4 months post-strike
```

### Robustness Analyses

**Matched Subsample Results:**
- Displacement effect magnitude similar to full sample (-0.2233 vs. -0.1989)
- No statistically significant difference
- Suggests baseline demand differences play minor role

**Baseline-Demand Shift Diagnostic (Figure 9):**
- Control households: displaced/non-displaced follow different trends (expected under state dependence)
- Treated households: displaced/non-displaced *converge* post-strike
- Consistent with equal baseline-demand shifts across displacement groups

### 5.3 Heterogeneity in Trip Displacement Effects

#### Drivers of State Dependence

**Mechanisms (Dubé et al., 2010):**
1. **Loyalty**: Mere act of visiting creates attachment/inertia
2. **Search**: Costly to resolve uncertainty about store quality
3. **Learning**: Familiarity with store layout/assortment reduces future search costs

**Test:** Compare displacement effects for households that visited a *new store* (never visited pre-strike) vs. those who only visited familiar stores during the strike.

**Quadruple-Difference Specification (Equation 14):**
```math
Trips_{it} = ... + γ_1 I(NewStore_i=1)×I(t>0)×I(S\&S_i=1) + γ_2 I(NewStore_i=1)×I(t>0)×I(S\&S_i=1)×I(displaced_i=1) + ...
```

**Table 6, Column 1 Results:**
| Coefficient | Estimate | Interpretation |
|-------------|----------|---------------|
| displaced × S&S × post | -0.1483*** | Displacement effect for familiar-store shoppers (~7% decline) |
| new store × displaced × S&S × post | -0.1980** | *Additional* effect for new-store shoppers |

**Interpretation:**
- Larger displacement effect for households visiting new stores → supports role of **search/learning frictions**
- Meaningful effect remains for familiar-store shoppers → **loyalty/inertia** also contributes

#### Heterogeneity by Demographics and Spending

**Table 6 Results Summary:**

| Dimension | Finding |
|-----------|---------|
| **Pre-strike spending** (high vs. low) | No meaningful difference in displacement effects |
| **Income** (low/mid/high) | No meaningful differences across groups |
| **Age** (reference: 65+) | • No displacement effect for 65+<br>• Largest effect for ages 25-34 (-0.3816**) |

**Possible Explanations for Age Pattern:**
- Older consumers less likely to visit new stores or switch to inferior substitutes during strike
- Consistent with consumption capital theory (Stigler & Becker, 1977): purchase histories shape preferences

---

## 6. Discussion

### Summary of Findings

1. **State Dependence is Economically Meaningful**:  
   Displaced households make ~0.20 fewer trips per period post-strike (9.9% decline), emerging immediately and persisting for 4 months.

2. **Mechanisms**:  
   - Search/learning frictions: Larger effects for households visiting new stores
   - Loyalty/inertia: Effects persist even for familiar-store shoppers

3. **Firm Response Matters**:  
   Positive baseline-demand effect for non-displaced households suggests S&S's promotional response successfully counteracted potential negative reputational effects.

### Implications

#### For Managerial Decision-Making
- **Supply Disruptions**: Firms should anticipate long-term demand effects if stoppages displace consumer choices
- **Competitive Strategy**: 
  - State dependence makes it harder to compete with incumbents
  - But easier to retain customers once they switch
  - Temporary promotions may capture persistent market share (Dubé et al., 2010; Freimer & Horsky, 2008)

#### For Labor Relations and Policy
- **Worker Leverage**: Increases with ability to cause supply disruptions
- **Substitute Availability**: Long-term strike costs depend on viable alternatives:
  - High switching costs (healthcare, education) → smaller long-term demand effects
  - Low search frictions (CPG products) → consumers more likely to switch back post-strike
- **Distribution Workers**: When workers control distribution for multiple firms (e.g., port strikes, Amazon warehouses), they can depress demand beyond their direct employer

#### For Consumer Behavior Research
- **Bridge Two Literatures**: 
  - Store substitution/access literature (Shriver & Bollinger, 2022; Huang & Bronnenberg, 2023)
  - State dependence literature in marketing (Dubé et al., 2010; Simonov et al., 2020)
- **First Empirical Evidence**: Structural state dependence meaningfully drives store choice

### Reconciliation with Prior Strike Literature

| Study | Setting | Finding | Reconciliation |
|-------|---------|---------|---------------|
| Schmidt & Berri (2004) | Professional sports | No post-strike attendance changes | Few viable substitutes for consumers |
| Kotschedoff et al. (2025) | Belgian grocery chain | Limited lasting effects | High store density → consumers already optimized |
| Larcom et al. (2017) | London Underground | Lasting efficiency gains from route exploration | Similar mechanism: forced experimentation → learning |
| **This Paper** | U.S. grocery (Stop & Shop) | Persistent 9.9% trip reduction | Higher search costs → larger forced experimentation effects |

---

## References

Bachmann, Rüdiger, Gabriel Ehrlich, Ying Fan, Dimitrije Ruzic, and Benjamin Leard, "Firms and collective reputation: a study of the volkswagen emissions scandal," *Journal of the European Economic Association*, 2023, 21(2), 484–525.

Bai, Jie, Ludovica Gazze, and Yukun Wang, "Collective reputation in trade: Evidence from the Chinese dairy industry," *Review of Economics and Statistics*, 2022, 104(6), 1121–1137.

Barrage, Lint, Eric Chyn, and Justine Hastings, "Advertising and environmental stewardship: Evidence from the BP oil spill," *American Economic Journal: Economic Policy*, 2020, 12(1), 33–61.

Becker, Brian E and Craig A Olson, "The impact of strikes on shareholder equity," *ILR Review*, 1986, 39(3), 425–438.

Bronnenberg, Bart J, Jean-Pierre H Dubé, and Matthew Gentzkow, "The evolution of brand preferences: Evidence from consumer migration," *American Economic Review*, 2012, 102(6), 2472–2508.

Bronnenberg, Bart, Jean-Pierre Dubé, and Joonhwi Joo, "Millennials and the takeoff of craft brands: Preference formation in the us beer industry," *Marketing Science*, 2022, 41(4), 710–732.

Buell, Griffin, "Strike Empties the Shelves at Stop & Shop," 2019.

Bureau of Labor Statistics, "Work Stoppages Summary," February 2024.

Christensen, Hans B, Emmanuel T De George, Anthony Joffre, and Daniele Macciocchi, "Consumer Responses to the Revelation of Corporate Social Irresponsibility," SSRN, 2023.

Conway, Jacob and Levi Boxell, "Consuming values," Available at SSRN 4855718, 2024.

DeCosta-Klipa, Nik, "What you need to know about the Stop & Shop strike," 2019.

Dubé, Jean-Pierre, Günter J. Hitsch, and Peter E. Rossi, "State Dependence and Alternative Explanations for Consumer Inertia," *The RAND Journal of Economics*, 2010, 41(3), 417–445.

Dwyer, Michael, "Stop & Shop traffic from loyal customers plummets 75 percent during strike," 2019.

Freimer, Marshall and Dan Horsky, "Try it, you will like it: Does consumer learning lead to competitive price promotions?," *Marketing Science*, 2008, 27(5), 796–810.

Gruber, Jonathan and Samuel A Kleiner, "Do strikes kill? Evidence from New York state," *American Economic Journal: Economic Policy*, 2012, 4(1), 127–157.

Hadero, Haleluya, "What to know about Amazon workers strike at multiple delivery hubs," PBS News, December 2024.

Hahsler, Michael, Matthew Piekenbrock, and Derek Doran, "dbscan: Fast Density-Based Clustering with R," *Journal of Statistical Software*, 2019, 91(1), 1–30.

Heckman, J. J., "Heterogeneity and State Dependence," in *Studies in Labor Markets*, University of Chicago Press, 1981.

Ho, Daniel E., Kosuke Imai, Gary King, and Elizabeth A. Stuart, "MatchIt: Non-parametric Preprocessing for Parametric Causal Inference," *Journal of Statistical Software*, 2011, 42(8), 1–28.

Huang, Yufeng and Bart J Bronnenberg, "Consumer transportation costs and the value of e-commerce: Evidence from the dutch apparel industry," *Marketing Science*, 2023, 42(5), 984–1003.

Johnston, Katie, "Visits by Loyal Stop Shop customers decline 75 percent during strike," Apr 2019.

Kaye, Danielle, "Here's What to Know About the Port Strike," *The New York Times*, September 2024.

Knight, Samsun, "Retail Demand Interdependence and Chain Store Closures," Available at SSRN 4234510, 2022.

Kotschedoff, Marco JW, Liliana Kowalczyk, and Els Breugelmans, "The persistence of grocery shopping behavior and retailer choice: Evidence from a major labor strike," *Quantitative Marketing and Economics*, 2025, pp. 1–44.

Krueger, Alan B and Alexandre Mas, "Strikes, scabs, and tread separations: labor strife and the production of defective Bridgestone/Firestone tires," *Journal of Political Economy*, 2004, 112(2), 253–289.

Larcom, Shaun, Ferdinand Rauch, and Tim Willems, "The benefits of forced experimentation: Striking evidence from the London underground network," *The Quarterly Journal of Economics*, 2017, 132(4), 2019–2055.

Leuz, Christian and Catherine Schrand, "Disclosure and the cost of capital: Evidence from firms' responses to the Enron shock," NBER Working Paper, 2009.

Levine, Julia, "Are Menthol Cigarettes More Addictive? A Cross-Category Comparison of Habit Formation," Working Paper, 2023.

Levine, Julia and Stephan Seiler, "Identifying state dependence in brand choice: Evidence from hurricanes," *Marketing Science*, 2023, 42(5), 934–957.

Liaukonytė, Jūra, Anna Tuchman, and Xinrong Zhu, "Frontiers: Spilling the beans on political consumerism: Do social media boycotts and buycotts translate to real sales impact?," *Marketing Science*, 2023, 42(1), 11–25.

Liaw, Andy and Matthew Wiener, "Classification and Regression by randomForest," *R News*, 2002, 2(3), 18–22.

Mas, Alexandre, "Labour unrest and the quality of production: Evidence from the construction equipment resale market," *The Review of Economic Studies*, 2008, 75(1), 229–258.

Olden, Andreas and Jarle Møen, "The triple difference estimator," *The Econometrics Journal*, 2022, 25(3), 531–553.

Osborne, Matthew, "Consumer learning, switching costs, and heterogeneity: A structural examination," *Quantitative Marketing and Economics*, 2011, 9(1), 25–70.

Pakes, Ariel, Jack R Porter, Mark Shepard, and Sophie Calder-Wang, "Unobserved heterogeneity, state dependence, and health plan choices," NBER Working Paper, 2021.

Rhee, Hongjai and David R Bell, "The inter-store mobility of supermarket shoppers," *Journal of Retailing*, 2002, 78(4), 225–237.

Sanders, Bernie (@BernieSanders), "I stand with @UFCW workers in their fight to protect health care and workers' rights," Twitter, April 11, 2019.

Schmidt, Martin B and David J Berri, "The impact of labor strikes on consumer demand: An application to professional sports," *American Economic Review*, 2004, 94(1), 344–357.

Shay, Jim, "Timeline of Stop & Shop Strike," 2019.

Shriver, Scott K and Bryan Bollinger, "Demand expansion and cannibalization effects from retail store entry: A structural analysis of multichannel demand," *Management Science*, 2022, 68(12), 8829–8856.

Simonov, Andrey, Jean-Pierre Dubé, Günter Hitsch, and Peter Rossi, "State-Dependent Demand Estimation with Initial Conditions Correction," *Journal of Marketing Research*, 2020, 57(5), 789–809.

Springer, Jon, "Ahold Delhaize Reveals Heavy Toll of Stop & Shop Strike," 2019.

Stigler, George J and Gary S Becker, "De gustibus non est disputandum," *The American Economic Review*, 1977, 67(2), 76–90.

The Shelby Report, "The Griffin Report Unveils Its 2019 Northeast Market Review," 2019.

Troncoso, Isamar, Minkyung Kim, Ishita Chakraborty, and SooHyun Kim, "The impact of unionization on consumer perceptions of service quality: Evidence from starbucks," Available at SSRN 4657689, 2023.

Wang, Kitty and Shijie Lu, "Corporate political positioning and sales: Evidence from a natural experiment," Available at SSRN 4084106, 2022.

Warren, Elizabeth (@SenWarren), "I stand in solidarity with @UFCW for these hard-working families," Twitter, April 11, 2019.

---

## Appendices (Summary)

### Appendix A: Store Location Imputation
- DBSCAN clustering (ε = 0.25 miles) to group coordinates into store IDs
- Special handling for S&S: matched to known operating locations
- Time-weighted averaging for trips without coordinates

### Appendix B: Discount Changes at Control Retailers
- Triple-differences regression shows control retailers (Giant Company, Giant Food) increased discounts modestly post-strike
- S&S increased discounts substantially more → consistent with strategic response

### Appendix C: Parallel Trends Assessment
- Pre-strike trend analysis supports identifying assumptions
- Matched sample shows parallel trends within displacement groups

### Appendix D: Prediction Error and Misclassification
- Formal derivation: misclassification biases displacement effect toward zero
- Correction using observed control behavior reduces bias
- Back-of-envelope bounds suggest true effect may be larger than estimated

### Appendix E: Matching Procedure Details
- Coarsened exact matching on:
  - Pre-strike focal retailer trip share
  - Conditional revisit probability
- Improves covariate balance; restricts to common support

### Appendix F: Additional Tables
- Table A7: Household counts by subgroup
- Table A8: Full heterogeneity regression results
- Table A9: Random forest feature importance ranking

---

*End of Document*