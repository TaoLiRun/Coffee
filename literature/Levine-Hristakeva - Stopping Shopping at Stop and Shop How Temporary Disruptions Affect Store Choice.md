# Stopping Shopping at Stop and Shop? How Temporary Disruptions Affect Store Choice $ ^{*} $

Julia Levine†

Sylvia Hristakeva $ ^{\dagger} $

Click here for the most recent version.

This draft: January 5, 2026

## Abstract

Shopping patterns in retail markets are highly persistent, with households patronizing the same stores over time. Whether this persistence reflects unobserved heterogeneity or a causal effect of past choices through state dependence remains an open question. We study an 11-day strike that effectively closed 240 Stop & Shop grocery stores, using a novel identification strategy to isolate the strike's long-term effects on consumer demand through state dependence. We find that the strike caused households to make 9.9% fewer trips to S&S after the strike's resolution, simply by displacing planned visits during the strike. The reduction is observed immediately in the period after the strike's resolution and attenuates only gradually over time. The effect of trip displacement is larger for households who, during the strike, visit a store that they had not previously visited, suggesting that state dependence in store choice is partially driven by search and learning frictions. These results support an economically meaningful role of state dependence in grocery store choice, suggesting that temporary supply disruptions, and marketing tactics that induce consumer switching, can have long-term effects on profitability.

Keywords: Store Choice, State Dependence, Retailer Loyalty, Store Closure, Employee Strikes, Social Consumerism

## 1 Introduction

Consumers exhibit strong persistence in where they shop, repeatedly choosing the same firms, even when close substitutes are readily available. This persistence may be driven by structural state dependence, whereby past choices causally affect present choices through mechanisms like loyalty, learning, or search costs, or by spurious state dependence, whereby unobserved heterogeneity, such as preferences and income, influences both past and present choices (Heckman, 1981). Understanding the role of structural state dependence, hereafter referred to as “state dependence,” in driving choices is important for understanding consumer demand and firm competition. Prior work in economics and marketing has documented state dependence in settings such as brand and health insurance plan choice (Dubé et al., 2010; Pakes et al., 2021). We study state dependence in store choice, a setting in which persistence is both pronounced and economically meaningful (Rhee and Bell, 2002). As stores differ in their prices and assortments, state dependence at this margin can have downstream consequences on what products consumers buy, shaping the competitive landscape, not only for retailers, but also for categories and brands.

An ideal, yet infeasible, experiment to quantify the role of state dependence in store choice would randomly displace trips to a given store for a single time period, allowing us to analyze how demand for that store changed among the group of displaced consumers, relative to the group of non-displaced consumers. We identify the effect of such a displacement in the context of the 2019 labor strike by employees of Stop & Shop (S&S), a large supermarket chain in the Northeastern United States. The strike sharply disrupted access to stores in a contiguous geographic region, forcing consumers to forgo grocery trips or shop elsewhere for the 11-day duration of the strike, and providing a rare opportunity to observe how consumers respond when their regular shopping patterns are interrupted and then restored. We find that the displacement of trips for the period of the strike resulted in an economically meaningful and persistent decrease in trips, suggesting that state dependence is an important driver of persistence in store choice.

The strike setting is economically important in its own right. The United States has seen a sharp uptick in labor stoppages, with 33 major strikes in 2023, setting a 20-year record (Bureau of Labor Statistics, 2024). While the immediate supply disruptions of strikes are visible and often well-documented (Krueger and Mas, 2004; Gruber and Kleiner, 2012; Mas, 2008), the post-strike effects on consumer demand for the affected firms are less understood. Do customers return once normal operations resume? Or do temporary disruptions lead to persistent re-allocations of demand? This distinction matters for firms, workers, and policymakers. If temporary supply disruptions have lasting effects on demand, then the

economic costs of strikes may extend well beyond their resolution. Understanding the long-term effects of strikes can therefore inform decisions for both workers and firms, helping to better characterize the stakes in labor negotiations.

On April 11, 2019, over 30,000 S&S employees went on a strike, asking for better pay and benefits. The strike lasted for 11 days, affecting 240 stores across Connecticut, Massachusetts, and Rhode Island. We use Numerator's household panel, which allows us to observe the store banner and location of each trip. We refer to households who visited S&S prior to the strike as "S&S households," and consider them to have been "treated" by the strike. We construct a control group from the set of households who visited one of two comparable grocery retailers prior to the strike. $ ^{1} $ Our main outcome of interest is the number of trips made by a household to its "focal retailer," either S&S for the treated households or one of the control retailers for the control households. We track these focal retailer trips for three months before and four months after the strike, analyzing how they change for S&S households, relative to control households, after the strike's resolution.

The strike may have affected post-strike demand for S&S through multiple mechanisms. By interrupting access to S&S, the strike displaced some planned visits, altering consumers' recent shopping histories and potentially their subsequent store choices through state dependence. At the same time, the strike may have affected baseline demand for S&S, through changes in perceived store quality, reliability, or reputation (Troncoso et al., 2023), as well as through firm responses to the disruption, such as adjustments in pricing, promotions, or assortments during or after the strike. We propose a novel strategy to disentangle the effect of trip displacement from that of changes in baseline demand for S&S. The key insight is that the strike did not affect all S&S households in the same way. Some households would have visited S&S during the strike, but instead skipped that visit. For such “displaced” households, the strike potentially affected their demand for S&S by changing both their baseline demand and their past choices. In contrast, households who did not plan to visit S&S during the strike did not experience an interruption to their recent store choice. For these “non-displaced” households, the strike could affect post-strike behavior only through changes in baseline demand. This distinction provides a natural source of variation to isolate the strike’s effect through displacing choices.

We implement this logic using a triple-difference framework, comparing changes in focal retailer trips across three dimensions: before versus after the strike, treated versus control, and displaced versus non-displaced households. As we cannot observe whether S&S households were displaced or not, we use a random forest model trained on pre-strike shopping

data to predict whether households would have visited their focal retailer during the strike in a counterfactual world where the strike did not occur, classifying households as displaced if they were predicted to visit, and non-displaced otherwise. Under a difference-in-differences approach, comparing non-displaced treated and control households isolates changes driven by shifts in baseline demand, while comparing displaced treated and control households captures the combined effect of those shifts and the displacement of trips. The triple-differences estimator represents the difference between these comparisons, isolating the effect of trip displacement under the assumption that baseline-demand impacts choices similarly for displaced and non-displaced households. We recognize that this assumption may be violated in practice, and therefore assess this condition empirically and characterize how departures from it would affect the estimated displacement effect.

Our results show that the strike affected post-strike demand by both shifting baseline demand and displacing choices. First, we estimate a positive baseline-demand effect for non-displaced S&S households, who make approximately 0.05 more trips per period to their focal retailer after the strike. We provide suggestive evidence that this increase may be driven by the firm's response, documenting a rise in price promotions at S&S relative to competing retailers following the strike. This finding suggests that any negative reputational effects of the strike were small in magnitude, so as to be compensated for by the firm's marketing tactics. $ ^{2} $

Second, we find a large and persistent displacement effect for households whose planned S&S visit was foregone during the strike: displaced households make about 0.20 fewer trips per period as a result of the skipped visit, corresponding to an almost 9.9% decline relative to pre-strike shopping intensity. Event-study estimates show that this effect emerges immediately after the missed visit and persists throughout the four-month post-strike window we observe, gradually attenuating over time.

We next examine how the displacement effect varies across households to shed light on the sources of state dependence. We find that the displacement effect is stronger for households that visited a new store, defined as a store that the household had not previously visited, during the strike. This suggests that state dependence is driven, in part, by search and learning frictions, as households that visited a new store during the strike no longer need to overcome those frictions after the strike. However, we still estimate a meaningful displacement effect among households that did not visit a new store during the strike, indicating that persistence in store choice may also reflect inertia or psychological switching.

costs.

This paper provides direct evidence that persistence in store choice reflects more than unobserved heterogeneity, with past choices causally affecting current choices. This result has important implications for managerial decision-making, both in the face of potential supply disruptions, as well as the day-to-day competitive environment. Firms embroiled in labor disputes should consider whether a work stoppage will displace consumer choices, and recognize that if so, those stoppages may have long-term effects on demand. State-dependent store choice also has implications for competitive strategy. When consumer choices are shaped by prior experiences, it becomes harder to compete with incumbents, but also easier to hold onto customers once they switch. State dependent store-choice suggests that temporary promotions could be effective in capturing market share that persists beyond the promotion's tenure (Dubé et al., 2010; Freimer and Horsky, 2008).

Relationship to Literature From a consumer demand perspective, our setting connects two largely separate literatures. Recent work uses detailed household level data to quantify substitution patterns across stores and to evaluate how changes in the retail environment, such as store entry, exit, or changes in access, reshape where consumers shop (e.g., Shriver and Bollinger (2022); Huang and Bronnenberg (2023); Knight (2022)). For example, Huang and Bronnenberg (2023) develop a structural model of store choice that emphasizes travel costs and shopping frictions to quantify how changes in retail access affect shopping behavior. In parallel, the state dependence literature in marketing has developed tools to distinguish state dependence from alternative sources of persistence, primarily in the context of product brand choice rather than retailer choice (e.g., Dubé et al. (2010); Simonov et al. (2020); Levine and Seiler (2023); Osborne (2011)). By documenting the role of state dependence in store choice, we bridge these two literatures, to our knowledge, providing the first empirical evidence that structural state dependence is a meaningful driver of store choice.

We are also related to other studies exploring the effects of labor strikes. Prior studies have examined the overall effects of labor strikes on firms' financial performance (Becker and Olson (1986)), productivity (Krueger and Mas (2004); Mas (2008)), or quality provided during the striking period (Gruber and Kleiner (2012)). Few papers explore the long-term impact of strikes on consumer demand after normal operations resume. Schmidt and Berri (2004) investigate labor strikes in professional sports and find no changes in league attendance post-resolution, and Kotschedoff et al. (2025) analyze the effects of a partial week-long closure by a Belgian grocery chain due to a strike, finding limited lasting effects. We believe that these results can be reconciled with ours in light of differences in the availability and quality of substitutes across the studied settings. In the context of professional sports, consumers

do not have many viable substitutes, limiting the potential for choices made during the strike to compete with the league once normal operations resumed. In the Belgian grocery market studied by Kotschedoff et al. (2025), store density is very high, suggesting that most consumers have already identified their optimal store. This is in contrast to the U.S. market, where higher search costs may result in a larger effect through forced experimentation. We are perhaps most related to Larcom et al. (2017), who study the effects of a strike by workers of the London Underground. The authors find lasting effects of the strike on network efficiency, as the strike caused commuters to explore new routes, and stick with them after the strike's resolution.

The strike’s potential to affect baseline demand connects our study to the literature on corporate scandals and, more broadly, on socially conscious consumerism (most recently evaluated in Liaukonytė et al. (2023); Conway and Boxell (2024); Wang and Lu (2022)). A substantial body of research has examined how consumers respond to negative information about a firm’s product, generally finding negative reactions from consumers and investors (e.g., Leuz and Schrand (2009); Bai et al. (2022); Bachmann et al. (2023)). However, when the information does not directly relate to product quality, the evidence is mixed (Christensen et al., 2023; Barrage et al., 2020). Though we do not separately identify the extent to which post-strike changes in trips are driven by consumer reactions to the strike, our analyses contribute to this literature stream by highlighting that it is important to account for firms’ responses when attempting to understand such effects.

## 2 Setting and Data

### 2.1 The Stop & Shop Strikes of 2019

Stop & Shop (S&S) is a large grocery chain operating in the Northeastern United States, with a market share of just over 20% in 2019 (The Shelby Report, 2019). S&S's workforce is fully unionized and is represented by local chapters of the United Food and Commercial Workers union (the UFCW). The contracts for five chapters of the UFCW, representing S&S workers in Connecticut, Massachusetts, and Rhode Island, expired on February 23rd of 2019. With ongoing negotiations over wages, healthcare, and retirement benefits, the five chapters authorized the workers to call a strike at any moment. That moment came on April 10th, when shareholders of S&S's holding company, Ahold Delhaize, voted to increase their dividends by 11.1%. The next day, approximately 31,000 workers walked off the job, affecting 240 stores in Connecticut, Massachusetts, and Rhode Island (Shay, 2019).

A strike had been anticipated since late February; hence, S&S had contingency plans

in place that included bringing in temporary workers and deploying corporate personnel (DeCosta-Klipa, 2019). However, the stores had limited hours of operation, were not receiving regular shipments, and departments that rely heavily on human labor were closed (Buell, 2019). Furthermore, customers who wanted to enter S&S locations had to walk past crowds of striking workers encouraging them to shop somewhere else (Johnston, 2019). Therefore, the striking stores were effectively closed: Our data show that the strike led to an 92% decrease in trips, with the average basket expenditure, conditional on a trip, dropping by 35%.

S&S also has stores with unionized workforces in New York and New Jersey. These employees did not join the strike, presumably because their contracts did not expire until 2020. $ ^{3} $ We hereafter refer to New York and New Jersey as the “non-striking region,” and to Connecticut, Massachusetts, and Rhode Island as the “striking region.”

The strikes made national news, with the New York Times, Newsweek, the Guardian, Vox, and USA Today covering the story. The coverage was perhaps amplified by the 2020 Democratic presidential primaries, with candidates Bernie Sanders and Elizabeth Warren tweeting their support for the striking workers on the day of the walk-out and President Biden making an in-person appearance at the picket lines (Warren, 2019; Sanders, 2019; Dwyer, 2019). It is therefore reasonable to assume that S&S customers in both the striking and non-striking regions were aware of the strike. The strike ended on April 21st when the parties reached a tentative agreement. The parent company estimated that they lost $324 million dollars during the strike, and $121 million in the subsequent recovery period (Springer, 2019).

### 2.2 Data and Descriptive Patterns

We use household shopping data from Numerator, a market research company that runs a large representative household panel in the United States. Our data track panelists' shopping trips and expenditures across retail outlets. For each shopping trip, we see the date of the trip, the name of the retailer, as well as the quantities and prices of the products purchased. We observe the store location for 45% of trips, which we use to infer whether households visit S&S in the striking or non-striking region (see Appendix A for details). In addition, Numerator collects demographic information for each panelist, including household size, income bracket, age, and zip code.

Below, we describe how S&S trips and promotions evolved over time. Hereafter, we refer to the 11-day window of the strike (April 11th to April 21st) as “period 0.” We divide the rest of the sample into 11-day periods, centered on period 0. For example, period -1 encompasses March 31st to April 10th. We construct this panel for nine periods before, and twelve periods after the strike. $ ^{4} $ Figure 1 displays the timing and our notation.

<div style="text-align: center;"><div style="text-align: center;">Figure 1: Timeline</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//396eb8b7-9fa3-476a-aeaf-350609f0d21d/markdown_2/imgs/img_in_image_box_180_476_1044_581.jpg?authorization=bce-auth-v1%2FALTAKzReLNvew3ySINYJ0fuAMN%2F2026-04-22T15%3A40%3A22Z%2F-1%2F%2Fae3896a372d2b088450fa818e05d63464058021f2b30402cc443e704271d0668" alt="Image" width="70%" /></div>


<div style="text-align: center;"><div style="text-align: center;">Notes: The graph shows a running counter of 11-day periods. Period 0 is defined as the period of the strike. We track households for 9 periods before the strike and 12 periods after the strike.</div> </div>


Shopping Trips over Time First, we describe how the number of trips made to S&S changed during and after the strike. Figure 2 plots the total number of trips reported over time to each store for which we observe, or are able to impute (see Appendix A), the store's location. Each line tracks trips reported to a unique store, which are grouped by state. Stores in the striking region, shown in the three plots on the top row, exhibit a clear drop in visits at the time of the strike. By contrast, the plots on the bottom row show that there is no visible change in trips to S&S stores in the non-striking region at t = 0.

In the striking region, S&S stores received 22.87 fewer visits during the strike, relative to a pre-strike average of 24.76, constituting a 92% decrease. Although trips do not fall completely to zero during the strike, exploratory analyses suggest that those who visited a striking S&S purchased substantially fewer items, suggesting that these were abnormal visits, potentially impacted by department closures and un-stocked shelves. $ ^{5} $ In the non-striking region, we observe a 3% increase in visits to S&S relative to the pre-strike average of 29.78 trips per period. This suggests that any potential reputational costs of the strike were small, or counteracted by the firm's strategic response, discussed below.

<div style="text-align: center;"><div style="text-align: center;">Figure 2: Number of Trips to Stop & Shop Stores Across Regions</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//396eb8b7-9fa3-476a-aeaf-350609f0d21d/markdown_3/imgs/img_in_chart_box_194_196_1035_632.jpg?authorization=bce-auth-v1%2FALTAKzReLNvew3ySINYJ0fuAMN%2F2026-04-22T15%3A40%3A22Z%2F-1%2F%2F6303a7fef2c46f3192084cbf059b682299e8898dd6ed564e650e669e7a2a8d10" alt="Image" width="68%" /></div>


<div style="text-align: center;"><div style="text-align: center;">Notes: Each line tracks the number of trips reported to a given S&S store during our sample period. The top row shows patterns for S&S stores in the striking region, with clear drops in visits at the time of the strike, t = 0; the bottom row shows patterns for S&S stores in the non-striking region, with no clear changes at t = 0. Source: Numerator household panel.</div> </div>


Changes in Promotions After the Strike The overall impact of the strike on S&S demand may have been shaped not only by the disruption itself but also by the chain's actions in the aftermath. In particular, if S&S increased promotions to draw customers back, observed changes in demand may partly reflect this response. We therefore describe how discounts evolved at S&S compared to competing chains in the same region. We focus on the difference between list prices and paid prices as a measure of promotional intensity. We interpret the patterns below as suggestive evidence of S&S's strategic response, though knowing the precise magnitude of any price changes is not necessary for our estimation approach or result interpretation.

For each purchased item, we observe both a list price and a paid price, allowing us to compute the percentage difference, which we refer to as the “discount.” We construct a balanced panel tracking discounts over time for each item-retailer-state combination, omitting items-retailer-states for which we do not observe transactions in each period. $ ^{6} $ Let discount $ _{kjm} $ denote the (quantity-weighted) average discount for item k at retailer j, state m, and time t. The average pre-strike discount is 6% for S&S and 4.2% for the other grocery chains in the region.

We summarize how S&S's discounts adjusted relative to their competitors with the fol-

<div style="text-align: center;"><div style="text-align: center;">Figure 3: S&S Discounts over Time Relative to Competing Grocery Chains</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//396eb8b7-9fa3-476a-aeaf-350609f0d21d/markdown_4/imgs/img_in_chart_box_238_197_983_581.jpg?authorization=bce-auth-v1%2FALTAKzReLNvew3ySINYJ0fuAMN%2F2026-04-22T15%3A40%3A23Z%2F-1%2F%2Fc256564ea4bf85d10041553fdaf20c3279db933f1e9441811f74d3a1ee596c43" alt="Image" width="60%" /></div>


<div style="text-align: center;"><div style="text-align: center;">Notes: This graph plots  $ \beta_{l} $ estimates from the regression specified in Equation 1, using t = -9 as the excluded period. After the strike, we see a gradual increase in discounts at S&S relative to other grocery chains in the same geographic region. Source: Numerator household panel.</div> </div>


lowing regression, applied to data from stores in the striking region:

 $$ \mathrm{d i s c o u n t}_{k j m t}=\alpha_{k j m}+\omega_{t}+\sum_{l=-8}^{12}\beta_{l}\mathbb{I}(j=\mathrm{S}\&\mathrm{S})\times\mathbb{I}(t=l)+\nu_{k j m t}, $$ 

where  $ \alpha_{kjm} $ and  $ \omega_t $ denote item-by-retailer-by-state, and time fixed effects, respectively. We capture average changes in S&S's discounts relative to its local competitors with the  $ \beta_l $ parameters. Figure 3 plots these coefficients over time. We observe an increase in the difference between listed and paid prices at S&S relative to its competitors right as the strike begins, consistent with S&S strategically adjusting its promotions in response to the disruption.

## 3 Conceptual Framework

Consider a stylized model of store choice, whereby each period consumers choose between visiting S&S and an alternative retailer. Define consumer i's indirect utility from visiting retailer r at time t as:

 $$ U_{i r t}=\alpha_{r t}+\gamma\times\mathbf{1}(r\in R_{i,t-1})+\epsilon_{i r t}. $$ 

The indirect utility depends on a firm-specific intercept,  $ \alpha_{rt} $, which represents the consumer's baseline demand for retailer r at time t. Baseline demand captures all determinants of store choice that are independent of i's previous choice, such as prices, assortment, and firm

reputation. These factors are time-varying, and may change after a strike. For example, baseline demand for S&S might be negatively affected by the strike if consumers prefer not to patronize firms with labor disputes, or if they inferred that the strike lowered the quality of S&S's stores. Conversely, baseline demand might be positively affected if S&S responded strategically by lowering prices, or if publicity generated by the strike served as advertising for the chain.

The second term in Equation 2,  $ \gamma \times \mathbf{1}(r \in R_{i,t-1}) $, represents the role of state dependence. We define  $ R_{i,t-1} $ as the set of retailers that consumer i visited in the previous period; thus,  $ \gamma $ captures the added utility the consumer gets from shopping at a retailer that they visited in the previous period. If  $ \gamma > 0 $, past visits increase the likelihood of present visits. This positive state dependence may be driven by inertia, if consumers incur psychological switching costs, or through search costs and consumer learning, as retailers have different store layouts and assortments. Regardless of mechanism, positive state dependence is consistent with persistence in store choice, which has been documented in the literature (Rhee and Bell, 2002). Nevertheless, this specification also nests cases of no state dependence, whereby consumers' decisions of where to shop are independent across time periods, and negative state dependence, whereby consumers are variety-seeking and less likely to revisit the same retailer they last visited. Lastly, let  $ \epsilon_{irt} $ be an extreme value type I distributed shock that is independent across consumers, retailers, and time periods.

Suppose that in each period t, consumer i chooses between S&S and an alternative mutually exclusive retailer, indexed by s and  $ s' $ respectively. $ ^{7} $ The consumer will visit S&S if her utility from visiting S&S,  $ U_{ist} $, is greater than her utility from choosing the alternative option,  $ U_{is't} $:

 $$ \begin{align*}U_{ist}&\geq U_{is^{\prime}t},\\\alpha_{st}+\gamma\times\mathbf{1}(s\in R_{i,t-1})+\epsilon_{ist}&\geq\alpha_{s^{\prime}t}+\gamma\times\mathbf{1}(s^{\prime}\in R_{i,t-1})+\epsilon_{is^{\prime}t}.\end{align*} $$ 

We simplify by letting  $ \alpha_{s't} = 0 $, such that  $ \alpha_{st} $ captures the difference between S&S and the alternative retailer. Rearranging yields:

 $$ \underbrace{\alpha_{s t}+\gamma\times\left(\mathbf{1}(s\in R_{i,t-1})-\mathbf{1}(s^{\prime}\in R_{i,t-1})\right)}_{V_{i t}^{*}}\geq\underbrace{\epsilon_{i s^{\prime}t}-\epsilon_{i s t}}_{\epsilon_{i t}^{*}}. $$ 

To showcase how consumer store choice may be affected by the strike, we simulate choices

using this data-generating process (DGP) under different values of state dependence and changes in baseline demand. Figure 4 plots the effect of the strike on the share of trips captured by S&S over time, with the left panel showing the effects when choices are independent across time periods, and the right panel showing the effects when choices are positively state-dependent. For each case ( $ \gamma = 0 $ and  $ \gamma > 0 $) we simulate choices with and without a shock to baseline demand that peaks in magnitude at the time of the strike and diminishes over time, denoted by  $ \Delta\alpha_0 < 0 $ and  $ \Delta\alpha_0 = 0 $, respectively. Figure 4 plots the effect of the strike on the share of trips captured by S&S over time in each of the following scenarios:

 $ \gamma = 0 $ and  $ \Delta\alpha_0 = 0 $, represented by the solid points in the left panel of Figure 4: store choices are not state-dependent and the strike does not affect baseline demand. S&S trips drop during the strike, but consumers immediately return afterwards.

Scenario 2:  $ \gamma = 0 $ and  $ \Delta\alpha_0 < 0 $, represented by the hollow points in the left panel of Figure 4: store choices are not state-dependent, but the strike coincides with a temporary negative shock to baseline demand that decays over time.

Scenario 3:  $ \gamma > 0 $ and  $ \Delta\alpha_0 = 0 $, represented by the solid points in the right panel of Figure 4: the strike does not affect baseline demand, but store choices are state-dependent, resulting in a slower return to S&S. This highlights that state-dependent store choice can lead to similar patterns as a diminishing shock to baseline demand (Scenario 2).

Scenario 4:  $ \gamma > 0 $ and  $ \Delta\alpha_0 < 0 $, represented by the hollow points in the right panel of Figure 4: store choices are state-dependent and baseline demand is affected in the same way as in Scenario 2. Here, the effect of the strike is the largest, as both the shock to baseline demand and the tendency to repeat past choices operate to keep customers away from S&S for longer.

These simulations illustrate the key identification challenge when studying shocks that simultaneously affect baseline demand and choices. Though the patterns generated by Scenarios 2 and 3 look similar, the former is driven by shifts in baseline demand, and the latter is driven by state dependence. In Scenario 4, where consumers receive a shock to both baseline demand and choices, an analysis of the average treatment effects on the treated (ATTs) obscures the extent to which each of these shocks, alone, affects choices.

<div style="text-align: center;"><div style="text-align: center;">Figure 4: Simulated Effects of the Strike on Trips to S&S</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//7a069b7c-8ea7-4f1d-8f1a-7b1d06225bac/markdown_2/imgs/img_in_chart_box_147_197_1074_552.jpg?authorization=bce-auth-v1%2FALTAKzReLNvew3ySINYJ0fuAMN%2F2026-04-22T15%3A40%3A32Z%2F-1%2F%2Ffabd4df5066f156e45ecb6ec7a6d723ec373044ca385f366e2f32e2c16adb30d" alt="Image" width="75%" /></div>


<div style="text-align: center;"><div style="text-align: center;">Notes: These simulations compare the number of trips made to S&S with and without a strike at time period  $ t = 0 $. We model the supply disruption of the strike with an infinite  $ \epsilon^* $ draw at  $ t = 0 $. These differences are simulated under different combinations of state dependence and  $ \Delta\alpha_{st} $. In the left panel we set  $ \gamma = 0 $, and in the right panel we allow for state dependence in consumer choice with  $ \gamma = 0.75 $. Without the strike, consumers are indifferent between S&S and the alternative retailer (i.e.,  $ \alpha_{st}(0) = 0 $). With the strike, baseline demand evolves as follows:  $ \alpha_{st}(1) = \frac{-2}{3^t} $.</div> </div>


Mechanisms of Interest: Our goal is to separate between two mechanisms, which we define as follows:

D: The displacement effect: the effect of forcing consumers to forgo planned trips during the strike, without changing baseline demand.

B: The baseline-demand effect: any additional change driven by shifts in baseline demand.

Suppose that both mechanisms are active, as in Scenario 4. The displacement effect is simply the effect from Scenario 3, where the strike affects choices without changing baseline demand. The baseline-demand effect is the difference between the effects from Scenarios 4 and 3, represented by the vertical space between the solid and hollow points on the right panel of Figure 4. Our goal in what follows is to isolate the displacement effect by subtracting the baseline-demand effect from the overall effect, effectively purging it of changes driven by shifts in baseline demand.

Identification Intuition To see the intuition behind our identification strategy, we consider the strike’s effect on the probability of visiting S&S in the period immediately after the strike,  $ t = 1 $. Recall that choice probabilities are driven by differences in the deterministic part of the utility function,  $ V_t^* $, and the distribution of  $ \epsilon_t^* $, dropping individual level subscripts for ease of readability. In potential outcomes notation,  $ V_1^* $, with and without the

strike, is given by:

 $$ V_{1}^{*}(1)=\alpha_{s1}(1)+\gamma\times\Big(\mathbf{1}\big(s\in R_{0}(1)\big)-\mathbf{1}\big(s^{\prime}\in R_{0}(1)\big)\Big) $$ 

 $$ V_{1}^{*}(0)=\alpha_{s1}(0)+\gamma\times\Big(\mathbf{1}\big(s\in R_{0}(0)\big)-\mathbf{1}\big(s^{\prime}\in R_{0}(0)\big)\Big), $$ 

where  $ \alpha_{s1}(1) $ and  $ \alpha_{s1}(0) $ represent baseline demand for S&S at t = 1, with and without the strike, and  $ R_{0}(1) $ and  $ R_{0}(0) $, represent the set of stores visited at t = 0, with and without the strike.

Next, consider two groups of households, who differ only in whether they planned to visit S&S during the strike (i.e., at t = 0). A displaced household would have visited S&S absent the strike but could not because of the disruption. In contrast, a non-displaced household would not have visited S&S at t = 0 regardless of the strike.

For a displaced household, we have  $ s \in R_0(0) $ but  $ s' \in R_0(1) $. Therefore, the effect of the strike on  $ V_1^* $ is given by:

 $$ \begin{aligned}\Delta V_{1}^{*}(disp)&=V_{1}^{*}(1\mid disp)-V_{1}^{*}(0\mid disp)\\&=\left[\alpha_{s1}(1)-\gamma\right]-\left[\alpha_{s1}(0)+\gamma\right]\\&=\alpha_{s1}(1)-\alpha_{s1}(0)-2\gamma.\end{aligned} $$ 

In words, the change in visit probability after the strike is driven by both changes in baseline demand and the displacement of the trip during the strike. If the strike had no effect on baseline demand (i.e., if  $ \alpha_{s1}(1) = \alpha_{s1}(0) $), then we would be left with the displacement effect of  $ -2\gamma $.

To see how we isolate the displacement effect, consider an otherwise identical, non-displaced, consumer. This consumer has the same baseline demand for S&S, but due to natural variation in the timing of shopping trips, would not have visited S&S at t = 0, even in the absence of a strike (i.e.,  $ s' \in R_0(0) $ and  $ s' \in R_0(1) $). The change in  $ V_1^* $ for such a consumer is:

 $$ \begin{align*}\Delta V_{1}^{*}(\mathrm{non})&=V_{1}^{*}(1\mid\mathrm{non})-V_{1}^{*}(0\mid\mathrm{non})\\&=\left[\alpha_{s1}(1)-\gamma\right]-\left[\alpha_{s1}(0)-\gamma\right]\\&=\alpha_{s1}(1)-\alpha_{s1}(0).\end{align*} $$ 

Here we note that the strike influences visit probability for non-displaced households only through its impact on baseline demand as, by definition, such households did not have their

choices disrupted by the strike. As these two households are identical in all other ways, the changes in baseline demand are equal. Therefore, taking the difference between Equation 4 and Equation 3 isolates the displacement effect.

## 4 Empirical Implementation

Building on the intuition above, we estimate the displacement and baseline-demand effects using variation across four sets of households, defined along two dimensions. First, we split households into treated and control groups based on whether they visited S&S or a control retailer prior to the strike. Second, we classify each household as either displaced or non-displaced based on whether the household was expected to visit their “focal retailer” during the strike. For treated households, the focal retailer is S&S; for control households, it is a comparable non-S&S retailer. This two-by-two structure generates four groups that we use for our estimation design. Below, we first present the regressions taken to the data before carefully describing how we classify households along these two dimensions in our data. The section concludes with a description of the identifying variation, threats to identification, and robustness analyses.

### 4.1 Identification Approach

Table 1 describes how trips to the focal retailer may change after the strike for each of the four household types, grouped by treatment and displacement status. For example, for displaced S&S households, the change in the number of trips to S&S before and after the strike is as follows:

 $$ \Delta\mathrm{Trips}_{d,s}=\Delta_{d,s}^{D}+\Delta_{d,s}^{B}+\Delta_{d,s}^{T}, $$ 

where we decompose the effects of the strike into the displacement effect,  $ \Delta_{d,s}^{D} $, and the baseline-demand effect,  $ \Delta_{d,s}^{B} $. The last term,  $ \Delta_{d,s}^{T} $, allows that there may be other reasons for changes in trips that are independent of the strike, such as seasonality or shifts in the set of products needed. Row 2 describes the analogous first difference for non-displaced S&S households. Rows 3 and 4 summarizes changes for control households, where the differences consist only of time trends which are independent of the strike.

We isolate the displacement effect using a triple-difference estimator. The first difference-in-differences compares the change in trips for non-displaced S&S households, described in row 2 of Table 1, to that for non-displaced control households, described in row 4:

 $$ \Delta\mathrm{Trips}_{n,s}-\Delta\mathrm{Trips}_{n,c}=\Delta_{n,s}^{B}+\Delta_{n,s}^{T}-\Delta_{n,c}^{T}. $$ 

<div style="text-align: center;"><div style="text-align: center;">Table 1: Change in Trips to Focal Retailer After the Strike</div> </div>




<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Focal Retailer</td><td style='text-align: center; word-wrap: break-word;'>Row #</td><td style='text-align: center; word-wrap: break-word;'>Household Type</td><td style='text-align: center; word-wrap: break-word;'>1st differences</td></tr><tr><td rowspan="2">S&amp;S</td><td style='text-align: center; word-wrap: break-word;'>1</td><td style='text-align: center; word-wrap: break-word;'>displaced</td><td style='text-align: center; word-wrap: break-word;'>$ \Delta_{d,s}^{D} + \Delta_{d,s}^{B} + \Delta_{d,s}^{T} $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>2</td><td style='text-align: center; word-wrap: break-word;'>non-displaced</td><td style='text-align: center; word-wrap: break-word;'>$ \Delta_{n,s}^{B} + \Delta_{n,s}^{T} $</td></tr><tr><td rowspan="2">Control</td><td style='text-align: center; word-wrap: break-word;'>3</td><td style='text-align: center; word-wrap: break-word;'>displaced</td><td style='text-align: center; word-wrap: break-word;'>$ \Delta_{d,c}^{T} $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>4</td><td style='text-align: center; word-wrap: break-word;'>non-displaced</td><td style='text-align: center; word-wrap: break-word;'>$ \Delta_{n,c}^{T} $</td></tr></table>

Notes: This table shows the difference in trips to a focal retailer before and after the strike. Households are grouped based on whether they visited S&S in the pre-strike initialization period, and whether they were expected to visit their focal retailer during the strike (displaced) or not (non-displaced).

Analogously, taking the difference-in-differences for displaced households (comparing row 1 to row 3 in Table 1) yields the following expression:

 $$ \Delta\mathrm{Trips}_{d,s}-\Delta\mathrm{Trips}_{d,c}=\Delta_{d,s}^{D}+\Delta_{d,s}^{B}+\Delta_{d,s}^{T}-\Delta_{d,c}^{T}. $$ 

Our triple-difference estimator takes the difference between Equation 7 and Equation 6, yielding the following expression:

 $$ \begin{aligned}&\left(\Delta Trips_{d,s}-\Delta Trips_{d,c}\right)-\left(\Delta Trips_{n,s}-\Delta Trips_{n,c}\right)\\&=\left(\Delta_{d,s}^{D}+\Delta_{d,s}^{B}+\Delta_{d,s}^{T}-\Delta_{d,c}^{T}\right)-\left(\Delta_{n,s}^{B}+\Delta_{n,s}^{T}-\Delta_{n,c}^{T}\right)\\&=\Delta_{d,s}^{D}+\left(\Delta_{d,s}^{B}-\Delta_{n,s}^{B}\right)+\left(\Delta_{d,s}^{T}-\Delta_{d,c}^{T}-\Delta_{n,s}^{T}+\Delta_{n,c}^{T}\right).\end{aligned} $$ 

This expression allows us to identify the displacement effect,  $ \Delta_{d,s}^{D} $, under two assumptions:

A1 (Parallel Trends): The difference in trends between treated and control households is

a) zero within each displacement group:  $ \Delta_{n,s}^{T} = \Delta_{n,c}^{T} $ and  $ \Delta_{d,s}^{T} = \Delta_{d,c}^{T} $, or

b) the same across displacement groups:  $ \Delta_{n,s}^{T} - \Delta_{n,c}^{T} = \Delta_{d,s}^{T} - \Delta_{d,c}^{T} $

A2 (Equal Baseline-Demand Effects): The baseline-demand effect is the same for displaced and non-displaced consumers:  $ \Delta_{d,s}^{B} = \Delta_{n,s}^{B} $.

We recognize that the second assumption may not hold in the empirical setting. In Section 4.5 we explain why baseline demand effects might differ across households and present checks that help gauge the size of any resulting bias.

To estimate Equation 8, we take the following regression to the data, dropping the period

of the strike from the estimation sample:

 $$ \begin{aligned}Trips_{it}=&\delta^{\mathrm{B}}\mathbb{I}(t>0)\times\mathbb{I}(\mathrm{S\&S customer}_{i}=1)+\\&\delta^{\mathrm{D}}\mathbb{I}(t>0)\times\mathbb{I}(\mathrm{S\&S customer}_{i}=1)\times\mathbb{I}(\mathrm{displaced}_{i}=1)+\\&\beta\mathbb{I}(t>0)\times\mathbb{I}(\mathrm{displaced}_{i}=1)+\\&\phi_{i}+\omega_{t}+\nu_{it}.\end{aligned} $$ 

Trips $ _{it} $ tracks the number of trips made by household i to their focal retailer at time period t;  $ \phi_i $ and  $ \omega_t $ are household and period-level fixed effects, respectively. Under assumption A1a,  $ \delta^B $ captures the average treatment effect on the treated (ATT) for non-displaced households in the 12 periods after the strike. Under assumption A1,  $ \delta^D $ measures the difference in ATTs between displaced and non-displaced households, which represents the displacement effect under assumption A2. Standard errors are clustered at the household level.

We also show an event study of the following form:

 $$ \begin{aligned}Trips_{it}&=\sum_{l=-8}^{12}\delta_{l}^{B}\mathbb{I}(t=l)\times\mathbb{I}(S\&S customer_{i}=1)+\\&\sum_{l=-8}^{12}\delta_{l}^{D}\mathbb{I}(t=l)\times\mathbb{I}(S\&S customer_{i}=1)\times\mathbb{I}(displaced_{i}=1)+\\&\sum_{l=-8}^{12}\beta\mathbb{I}(t=l)\times\mathbb{I}(displaced_{i}=1)+\\&\phi_{i}+\omega_{t}+\nu_{it},\end{aligned} $$ 

where the excluded time period is t = -9.

Before isolating the displacement effects using the strategy above, we characterize the overall post-strike effects using the following regression, applied to the full set of S&S and control households:

 $$ \mathrm{Trips}_{it}=\delta\mathbb{I}(t>0)\times\mathbb{I}(\mathrm{S\&S customer}_{i}=1)+\phi_{i}+\omega_{t}+\nu_{it}. $$ 

Here again we drop the period of the strike such that the  $ \delta $ estimate captures the ATT in the 12 periods following the strike’s resolution (spanning approximately 4 months). To track how the ATT evolves over time, we present the results from the analogous event-study:

 $$ \mathrm{Trips}_{it}=\sum_{l=-8}^{12}\delta_{l}\mathbb{I}(t=l)\times\mathbb{I}(\mathrm{S\&S customer}_{i}=1)+\phi_{i}+\omega_{t}+\nu_{it}. $$ 

### 4.2 Defining Treated and Control Groups

We select treated and control households based on shopping behavior in the nine 11-day periods prior to the strike. A household is considered to have been “treated” by the strike if they visited a S&S store located in the striking region (MA, CT, RI) in at least two distinct time periods during this window.

To construct the control group, we identify households who shop outside of S&S's market area while being close enough to provide a relevant geographic comparison. To strike this balance, we restrict our attention to households that visited either The Giant Company or Giant Food in the pre-strike periods. These sister chains are owned by the same parent company as S&S. They operate in nearby but non-overlapping regions relative to S&S (The Giant Company in Pennsylvania, Maryland, Virginia, and West Virginia, and Giant Food in Delaware, Maryland, Virginia, and D.C.). We further drop any household that shopped within 20 miles of a S&S location prior to the strike. The first criterion identifies households with comparable shopping options, while the second ensures that they are located outside S&S's effective market area, and therefore unlikely to be affected by potential changes in the competitive environment driven by S&S's post-strike response. $ ^{8} $

Our main outcome variable is the number of trips made to a household’s focal retailer: S&S for treated households, and The Giant Company or Giant Food for control households. We track each household’s focal retailer trips in the 9 periods prior to the strike and the 12 periods following its resolution. We hereafter use “trips” and “focal retailer trips” interchangeably.

Our final sample consists only of households who visited a grocery store (focal or not) during the 11-day period of the strike. $ ^{9,10} $ The final sample includes 2,697 treated households and 5,175 control households.

Table 2 shows how our treated and control households compare based on demographic

<div style="text-align: center;"><div style="text-align: center;">Table 2: Demographic Comparison of Treated and Control Households</div> </div>




<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Variable</td><td style='text-align: center; word-wrap: break-word;'>Treated</td><td style='text-align: center; word-wrap: break-word;'>Control</td><td style='text-align: center; word-wrap: break-word;'>Difference</td><td style='text-align: center; word-wrap: break-word;'>p-value</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Age</td><td style='text-align: center; word-wrap: break-word;'>47.143</td><td style='text-align: center; word-wrap: break-word;'>47.185</td><td style='text-align: center; word-wrap: break-word;'>-0.042</td><td style='text-align: center; word-wrap: break-word;'>0.865</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Car Ownership</td><td style='text-align: center; word-wrap: break-word;'>0.880</td><td style='text-align: center; word-wrap: break-word;'>0.889</td><td style='text-align: center; word-wrap: break-word;'>-0.009</td><td style='text-align: center; word-wrap: break-word;'>0.223</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Household Size</td><td style='text-align: center; word-wrap: break-word;'>2.952</td><td style='text-align: center; word-wrap: break-word;'>3.031</td><td style='text-align: center; word-wrap: break-word;'>-0.080^{**}</td><td style='text-align: center; word-wrap: break-word;'>0.022</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>$125,000+</td><td style='text-align: center; word-wrap: break-word;'>0.251</td><td style='text-align: center; word-wrap: break-word;'>0.268</td><td style='text-align: center; word-wrap: break-word;'>-0.017</td><td style='text-align: center; word-wrap: break-word;'>0.101</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>$40,000-$124,999</td><td style='text-align: center; word-wrap: break-word;'>0.525</td><td style='text-align: center; word-wrap: break-word;'>0.552</td><td style='text-align: center; word-wrap: break-word;'>-0.027^{**}</td><td style='text-align: center; word-wrap: break-word;'>0.023</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>$0-$39,999</td><td style='text-align: center; word-wrap: break-word;'>0.223</td><td style='text-align: center; word-wrap: break-word;'>0.179</td><td style='text-align: center; word-wrap: break-word;'>0.044^{***}</td><td style='text-align: center; word-wrap: break-word;'>0.000</td></tr></table>

Notes: This table reports summary statistics for demographic variables, such as age, car ownership, household size, and income separately for treated and control households. Columns 1 and 2 report group means, and columns 3 and 4 report the difference in means and the p-value from a t-test.

Source: Numerator household panel.

characteristics tracked by the data provider and pre-treatment values of our main outcome tracking trips to the focal retailer. Treated and control households are similar in age and car ownership, but have slightly smaller household sizes and a lower income mix.

### 4.3 Classifying Customers into Displaced and Non-Displaced Groups

A key step in our empirical design is to classify all treated and control households as either displaced or non-displaced, based on whether they would have visited their focal retailer at t = 0 if a strike had not happened.

We use the random forest method to predict whether each household would have visited its focal retailer at t = 0 had the strike not occurred. Using data from the pre-strike period, we train a model to predict a household's likelihood of visiting its focal retailer in a given period based on prior behavior and household demographics. The model includes measures like the share of total trips to the focal retailer in the last period and the number of days since the household last bought routine staples like milk or eggs. Table A9 reports the full list of included features, ranked in descending order of importance for the final model.

The random forest aggregates predictions across 500 decision trees, each built on a bootstrapped sample. At each node, the algorithm chooses the best split from a set of randomly selected features. $ ^{11} $ The final prediction for a given household-period observation corresponds to the most common prediction across all 500 decision trees. Based on these predictions, we classify each treated and control household as displaced if the household was predicted to visit their focal retailer during the strike (at t = 0), and non-displaced if they were not predicted to visit. Roughly 55% of households are classified as displaced.

<div style="text-align: center;"><div style="text-align: center;">Table 3: Prediction Accuracy of Random Forest Classification</div> </div>




<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Period</td><td style='text-align: center; word-wrap: break-word;'>Control</td><td style='text-align: center; word-wrap: break-word;'>S&amp;S</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>-1</td><td style='text-align: center; word-wrap: break-word;'>0.774</td><td style='text-align: center; word-wrap: break-word;'>0.767</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>0</td><td style='text-align: center; word-wrap: break-word;'>0.773</td><td style='text-align: center; word-wrap: break-word;'>0.454</td></tr></table>

Notes: The table reports prediction accuracy from the random forest model separately for treated and control households. For each period, accuracy is defined as the share of cases in which predicted visits match observed choices. For t = -1, accuracy is calculated using out-of-bag predictions, and for t = 0, predictions are based on all trees because none were trained on strike-period data.

Source: Numerator household panel.

To assess how well the model predicts household behavior, we summarize accuracy, defined as the share of observations where the prediction matches observed household choices. That is, a prediction is accurate when the model anticipates a visit to the focal retailer and the visit occurs, or the model anticipates no visit and none takes place. Table 3 reports this metric separately for treated and control groups in the period immediately before the strike, t = -1, and the period of the strike itself, t = 0. $ ^{12} $

We take the accuracy in period t = -1 as our main indicator of model performance, because behavior in that period is not affected by strike-related shocks. At t = -1 the model performs comparably across treated and control households, with an accuracy rate of about 77% for both groups. During the strike, accuracy for treated households drops to 45% because the model does not incorporate the supply disruption that altered households' actual behavior in that period. For control households, whose shopping options were unaffected, accuracy remains stable at about 77%. Prediction error raises concerns about misclassification and the potential bias it can introduce. We discuss this issue and our approach in Section 4.5.

### 4.4 Sample and Identifying Variation

Having defined treatment and displacement status empirically, we next plot the data for each group to visualize the identifying variation. Figure 5 plots the average number of focal retailer trips separately across the four groups of households we use for estimation. The left panel shows the patterns for non-displaced households. The empty dots track the average number of trips made by control households, and the solid dots track those made by the treated households. Prior to the strike, these groups follow roughly parallel trends, with S&S households making slightly more trips per period than control households. During the strike, neither group visited their focal retailers, by construction. After the strike, the gap

<div style="text-align: center;"><div style="text-align: center;">Figure 5: Average Trips to Focal Retailer Over Time</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//36b1174b-9bf8-4f30-9521-75f4d4b380a6/markdown_0/imgs/img_in_chart_box_149_200_1073_683.jpg?authorization=bce-auth-v1%2FALTAKzReLNvew3ySINYJ0fuAMN%2F2026-04-22T15%3A40%3A20Z%2F-1%2F%2Fb6586589b076d379916c49627f3d7d00f8efa3096296fc5811922327edc067b8" alt="Image" width="75%" /></div>


<div style="text-align: center;"><div style="text-align: center;">Notes: This figure reports the average number of focal retailer trips separately for treated and control households. The left panel presents patterns for non-displaced households, and the right panel presents patterns for displaced households. Source: Numerator household panel.</div> </div>


in trips between S&S and control households widens, as compared to the pre-strike period. Intuitively, under the parallel trends assumption, the difference-in-differences between these two series identifies the baseline demand effect for these non-displaced S&S households.

The right panel compares the average number of trips made by displaced S&S and control households. As before, the two groups follow roughly parallel trends prior to the strike. However, we observe a sharp divergence during the strike: displaced control households make an average of 2.45 trips to their focal retailers, while displaced S&S households make none. In the periods immediately after the strike, the gap between treated and control households widens. Under the parallel trends assumption, this post-strike difference-in-differences reflects both changes in baseline demand and the additional effect operating through trip displacement.

These graphs also highlight two meaningful differences between displaced and non-displaced households. First, we see clear level differences, as displaced households make more visits to their focal retailers. We discuss the implications of these differences and a robustness analysis in Section 4.5. Second, we see that pre-strike trends vary by displacement status. Prior to the strike, there is a slight downward trend in visits for non-displaced households, whereas the displaced households exhibit a slight upward trend. This pattern is a mechanical feature of state-dependent store choice, where past visits increase the likelihood of current

<div style="text-align: center;"><div style="text-align: center;">Figure 6: Simulated Average Trips to Focal Retailer Over Time</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//36b1174b-9bf8-4f30-9521-75f4d4b380a6/markdown_1/imgs/img_in_chart_box_150_200_1072_683.jpg?authorization=bce-auth-v1%2FALTAKzReLNvew3ySINYJ0fuAMN%2F2026-04-22T15%3A40%3A21Z%2F-1%2F%2Fad6f025d8536be4ff1696b2b508b2905c8247f5458a3d5773b76d94ab04877da" alt="Image" width="75%" /></div>


<div style="text-align: center;"><div style="text-align: center;">Notes: This figure displays simulated visit patterns for displaced and non-displaced households under the DGP described in Section 3, which incorporates positive state dependence ( $ \gamma = 0.75 $) and a negative baseline-demand shock from the strike that evolves as follows after the strike:  $ \alpha_{st}(1) = \frac{-2}{3t} $. Treated households in the simulation experience the strike shock, while control households do not.</div> </div>


visits. Under state-dependent store choice, a household that would have visited a given retailer at $t=0$ (i.e., a displaced household) would have been increasingly more likely to visit that retailer in the preceding periods, and one who would not have visited at $t=0$ (i.e., a non-displaced household) would have been increasingly less likely to visit in the preceding periods.

To see this, Figure 6 shows the patterns generated by the DGP discussed in section 3, where we simulate state-dependent choices, both with and without a strike that coincides with a negative shock to baseline demand. Displaced households exhibit an upward trend leading up to the strike, and non-displaced households exhibit a downward trend. This difference in trends precludes a direct comparison between treated displaced and non-displaced households, leading us to the triple-differences approach, which uses control displaced and non-displaced households to make the differences in trips comparable. It is worth noting that, although the random forest algorithm does not impose any structural assumptions, the final model takes focal retailer visits in the preceding periods as important predictors of current visits. Therefore, our data follow a similar pattern to the data simulated from a model of store choice with positive state dependence.

### 4.5 Threats to Identification and Robustness Analyses

The interpretation of the displacement effect as a quantification of state dependence rests on several conditions that warrant discussion. First, we consider the impact of prediction error on our results, before considering the two identifying assumptions of parallel trends and equal baseline demand effects, introduced in Section 4.1.

Misclassification of Displacement Status: The first threat to identifying the displacement effect arises from the fact that we classify households as displaced or non displaced based on predictions of whether they would have visited their focal retailer in the absence of the strike. Prediction error in the random forest model creates the possibility of misclassification. Some households labeled as displaced may not have actually planned a visit during the strike period, and some labeled as non-displaced may in fact have planned to visit. These false positives and false negatives make the difference in ATTs between displaced and non-displaced households appear smaller in magnitude than it truly is, biasing our estimated displacement effect toward zero. We discuss this issue in detail in Appendix D.

We partially mitigate this bias by applying a simple correction to the control group. As control households face no supply disruption at t = 0, we can observe their true behavior in that period and evaluate whether our model correctly predicts it. We restrict the estimation sample to control households whose predicted behavior at t = 0 matches their actual choices. Appendix D shows that this adjustment helps reduce the bias from misclassification.

Equal Baseline-Demand Effects: A key identifying assumption is that the baseline-demand effect is the same across displaced and non-displaced households. There are two ways this assumption may fail. First, the baseline-demand effect may differ because households start from different pre-strike levels of baseline demand. For example, if displaced households had very high baseline demand for S&S prior to the strike, a shift in baseline demand may have little influence on their realized choices, while the same shift may matter more for a more marginal consumer. Second, baseline-demand effects may also differ if the strike affected baseline demand differently across displaced and non-displaced households. For example, a displaced household may have been more aware of the strike or more inconvenienced by it, which could lead to a larger shift in its baseline demand for S&S.

Figure 5 shows that displaced and non-displaced households differ in their average number of pre-strike trips, which suggests different underlying levels of baseline demand. This confirms that the first concern noted above is relevant in our setting. To gauge the size of any resulting bias, we use a robustness analysis that applies our identification strategy to a

subset of displaced and non displaced households selected to have similar baseline demand for their focal retailers. Within both the treated and control group, we match each displaced household to a non-displaced household based on pre-strike values of two variables: (i) the share of trips made to the focal retailer and (ii) the probability of visiting the focal retailer conditional on having visited it in the last period. Intuitively, the first variable captures households' relative preferences for their focal retailer, while the second serves as a proxy for the state-dependence parameter from our stylized model of store choice.

We use coarsened exact one-to-one matching, which divides each variable into broad bins, matching each household to one whose values fall into the same combination of bins. Households that do not share any cell with a counterpart (i.e., no control household can be matched to the same combination of bins) are dropped, imposing common support. Appendix E discusses the details of this approach, with average trips plotted over time for the matched sample in Figure A2. Our main assumption is that the matched sample consists of displaced and non-displaced households with equal pre-strike baseline demands. Therefore, if the shifts in baseline demand are the same, then we can interpret the displacement effect estimated with the matched sample as unbiased.

While we cannot test directly whether the shifts in baseline demand are the same for displaced and non-displaced households, we use a diagnostic inspired by our stylized model to see if different shifts appear consistent with the data. The idea is the following: If the two groups have similar baseline demand for S&S, and experience a similar shift in baseline demand from the strike, they should behave similarly after the strike. In other words, if the only thing distinguishing displaced and non-displaced households was the visit at t = 0, removing that visit should leave them on comparable trajectories. Figure 6 illustrates this logic in a simulation, where after the strike, treated displaced and non-displaced follow the same trajectory, while control displaced and non-displaced households diverge. To examine whether a similar pattern appears in the data, we estimate the following event study on the matched sample:

 $$ \mathrm{Trips}_{it}=\sum_{l=-8}^{12}\delta_{l}\times\mathbb{I}(t=l)\times\mathbb{I}(\mathrm{displaced}_{i}=1)+\phi_{i}+\omega_{t}+\nu_{it}. $$ 

Here,  $ \delta_{l} $ captures the difference in focal retailer trips between displaced and non-displaced households in each period, l, relative to t = -9. If the strike shifted baseline demand differentially for displaced and non-displaced households, we would expect these estimates to be significantly different from zero. If they are not statistically significant, it suggests that the displaced and non-displaced households experienced similar shifts in baseline demand,

and that the triple-difference estimator from Equation 9 isolates the displacement effect.

Parallel Trends: Our identification strategy is subject to the common assumption that the treated and control groups follow parallel trends in the absence of treatment within displacement groups, or that the difference in trends between treated and control groups is the same across displaced and non-displaced households (Olden and Møen, 2022). Appendix C provides empirical evidence assessing the validity of this assumption. We find that for the full estimation sample, there is a slight deviation in pre-strike trends between treated and control households for each group. However, that deviation is the same for both displaced and non-displaced households, such that the triple-differences estimator is not biased. For the matched sample, we find that the treated and control households follow parallel trends within each displacement group. Therefore, the difference-in-difference estimators are unbiased for this group, as is the triple-difference estimator.

## 5 Results and Decomposition

We begin by measuring the average treatment effect of the strike on S&S customers in the striking region. This provides a benchmark for how overall shopping patterns changed. We then use the identification strategy outlined above to isolate the displacement effect, net of changes driven by shifts in baseline demand. Lastly, we explore heterogeneity in trip displacement effects.

### 5.1 Overall Changes in Shopping Trips After the Strike

Column 1 of Table 4 shows the results of running the regression specified in Equation 11, comparing S&S households in the striking region to control households, before and after the strike. The estimated coefficient of -0.0539 corresponds to a 4.38% decrease in trips per period. These estimates capture changes in shopping patterns after the strike, which may be driven by the displacement effect or changes in baseline demand, through shifts in beliefs about the retailer or S&S's strategic response.

 $ ^{10} $ track how the AI $ ^{1} $T evolves over time, we present the results from Equation 12, plotting the estimated  $ \delta_{l} $'s in the left panel of Figure 7. We see that the negative effect of the strike is concentrated in the first seven periods after its resolution (roughly two months) before gradually converging towards pre-strike levels.

Columns two and three of Table 4 show the results of Equation 11 separately for the displaced and non-displaced households, comparing the treated displaced households to the

<div style="text-align: center;"><div style="text-align: center;">Table 4: ATT Estimates on Trips to Focal Retailer</div> </div>




<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>All (1)</td><td style='text-align: center; word-wrap: break-word;'>Displaced (2)</td><td style='text-align: center; word-wrap: break-word;'>Non-displaced (3)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>S\&amp;S \times post</td><td style='text-align: center; word-wrap: break-word;'>-0.0539^{***}(0.0183)</td><td style='text-align: center; word-wrap: break-word;'>-0.1451^{***}(0.0304)</td><td style='text-align: center; word-wrap: break-word;'>0.0538^{***}(0.0152)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Observations</td><td style='text-align: center; word-wrap: break-word;'>140,595</td><td style='text-align: center; word-wrap: break-word;'>78,393</td><td style='text-align: center; word-wrap: break-word;'>62,202</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>R^{2}</td><td style='text-align: center; word-wrap: break-word;'>0.59558</td><td style='text-align: center; word-wrap: break-word;'>0.50242</td><td style='text-align: center; word-wrap: break-word;'>0.18643</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Within R^{2}</td><td style='text-align: center; word-wrap: break-word;'>0.00012</td><td style='text-align: center; word-wrap: break-word;'>0.00057</td><td style='text-align: center; word-wrap: break-word;'>0.00043</td></tr></table>

Notes: This table shows the results from Equation 11. The dependent variable is household number of trips to their focal retailer (S&S or control) during each time period. All regressions include household and period fixed effects. The post indicator captures the twelve eleven day periods after the strike's resolution. Standard errors are clustered at the household level. Source: Numerator household panel.

control displaced households, and the treated non-displaced households to the control non-displaced households. Our results from column 2 show that displaced treated households make 0.1451 fewer trips per period than their control counterparts, a much larger drop than that estimated for the full sample. In contrast, non-displaced S&S households make an average of 0.0538 more trips per period than non-displaced control households make to their focal retailer. We interpret this positive coefficient as suggestive evidence that S&S's strategic response was successful in stimulating demand and counteracting any negative shifts in baseline demand driven by the strike. $ ^{13} $ The right panel of Figure 7 plots the analogous event studies for each group, showing that the effects for each subgroup persist over time.

### 5.2 Separately Identifying Mechanisms of Interest

Our goal in what follows is to isolate the displacement effect. A non-zero displacement effect would indicate that forgone shopping trips during the strike persistently altered subsequent store choice, consistent with state-dependent store choice behavior.

Table 5 reports the estimates from the triple-difference regression described in Equation 9. The baseline-demand effect, which is captured by the S&S×post coefficient, is simply the ATT for the non-displaced households, described in the previous section. Our focus is the trip displacement effect, captured by the estimated coefficient on S&S×post×displaced. We find economically meaningful effects: displaced households make 0.20 fewer trips per period.

<div style="text-align: center;"><div style="text-align: center;">Figure 7: Event Study: ATT of the Strike on Trips to Focal Retailer</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//952d5d62-802a-4ece-a5ab-d491f87c19b8/markdown_1/imgs/img_in_chart_box_191_197_608_607.jpg?authorization=bce-auth-v1%2FALTAKzReLNvew3ySINYJ0fuAMN%2F2026-04-22T15%3A40%3A21Z%2F-1%2F%2Fb6d4dcf4401d1f904abc32348a5663a705345286dca76e8503d704e097893a31" alt="Image" width="34%" /></div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//952d5d62-802a-4ece-a5ab-d491f87c19b8/markdown_1/imgs/img_in_chart_box_614_198_1030_607.jpg?authorization=bce-auth-v1%2FALTAKzReLNvew3ySINYJ0fuAMN%2F2026-04-22T15%3A40%3A21Z%2F-1%2F%2F03b936f03dcd721217a52716415a5fea8f8da342ebbaa53c70ff97e3420c89a0" alt="Image" width="33%" /></div>


<div style="text-align: center;"><div style="text-align: center;">Notes: These graphs plot event study estimates from Equation 12. Time is indexed by eleven day periods, with 0 representing the strike window, and period -9 is the omitted category. The dependent variable is household number of trips to their focal retailer (S&S or control) during period t. All regressions include household and period fixed effects. Standard errors are clustered at the household level. Source: Numerator household panel.</div> </div>


as a result of the skipped trip, an almost 9.9% decrease. Figure 8 plots how the displacement effect evolves over time, following Equation 10. The pattern points to a clear displacement response that begins immediately after the forgone trip at period 0 and reverts gradually. The effect persists for the four months following the strike.

To better characterize the financial costs of displacement, we estimate the resulting loss in revenue per period, relative to S&S's pre-strike average. We calculate the revenue lost per displaced household per period by multiplying the displacement effect on trips (-0.20) by the average pre-strike basket total for displaced households ($41.64). We multiple this value by the number of displaced households in our sample (1,427) to estimate the total loss per period. Lastly, we divide this value by the average pre-strike period revenue generated by households in our estimation sample: $142,391.30. This back-of-the-envelope calculation suggests that displacement results in an 8.56% loss in revenue per period in the four months after the strike's resolution.

Robustness Analyses The estimates above capture the displacement effect under the following assumptions: displaced and non-displaced households (1) share comparable baseline demand for their focal retailer and (2) experienced similar shifts in baseline demand after the strike. We acknowledge that these assumptions are unlikely to hold perfectly in our setting. Even so, we do not believe the deviations are large enough to meaningfully bias our results.

<div style="text-align: center;"><div style="text-align: center;">Table 5: Identifying The Effects of Trip Displacement and Baseline Demand</div> </div>




<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>All Households (1)</td><td style='text-align: center; word-wrap: break-word;'>Matched Subsample (2)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>S\&amp;S \times post</td><td style='text-align: center; word-wrap: break-word;'>0.0538^{***} (0.0152)</td><td style='text-align: center; word-wrap: break-word;'>0.0394 (0.0406)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>displaced \times S\&amp;S \times post</td><td style='text-align: center; word-wrap: break-word;'>-0.1989^{***} (0.0340)</td><td style='text-align: center; word-wrap: break-word;'>-0.2233^{***} (0.0743)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Observations</td><td style='text-align: center; word-wrap: break-word;'>140,595</td><td style='text-align: center; word-wrap: break-word;'>26,250</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>R^{2}</td><td style='text-align: center; word-wrap: break-word;'>0.59602</td><td style='text-align: center; word-wrap: break-word;'>0.29649</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Within R^{2}</td><td style='text-align: center; word-wrap: break-word;'>0.00121</td><td style='text-align: center; word-wrap: break-word;'>0.00225</td></tr></table>

Notes: This table reports estimates from the regression in equation 9. The dependent variable is the number of trips made by a household to their focal retailer (S&S or control) during period t. All regressions include household and period fixed effects. The strike period is omitted from the estimation sample. Standard errors are clustered at the household level. S&S×post captures the baseline-demand effect for non-displaced households in the 12 periods after the strike, and S&S×post×displaced captures the displacement effect. Column 1 presents estimates from the full sample. Column 2 reports the same regression on a matched sample that pairs displaced and non-displaced households with similar baseline demand before the strike. Source: Numerator household panel.

Below, we examine how each potential source of bias could affect our estimates and assess the extent to which it matters.

Our first robustness analysis repeats the main specification in Equation 9 using the matched subsample of displaced and non-displaced households. The matching pairs each displaced household with a non-displaced household that looks similar in their pre-strike propensity to visit (and revisit) their focal retailer. Column 2 of Table 5 shows the results using the matched sample, where we assume that the displaced and non-displaced households have equal pre-strike baseline demand. Comparing the coefficients on S&S×post×displaced shows that the displacement effect is very similar in magnitude to that estimated from the full sample, with no statistically significant difference. This close alignment indicates that the potential variation in baseline demand plays only a minor role in shaping the main estimate of interest. Overall, the matched results reinforce that our findings on displacement effects are not driven by systematic differences in baseline demand between the two groups.

The second concern is that displaced households may have experienced a larger shift in baseline demand, perhaps because they were more aware of the strike or more inconvenienced by it. Our stylized model offers a clean way to evaluate how likely this is in our data. If displaced and non-displaced households start with the same baseline demand for S&S, the model predicts that their post-strike paths should look similar. To examine this, we estimate differences in trips between displaced and non-displaced households using Equation 13.

<div style="text-align: center;"><div style="text-align: center;">Figure 8: The Displacement Effect Over Time</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//952d5d62-802a-4ece-a5ab-d491f87c19b8/markdown_3/imgs/img_in_chart_box_287_195_934_620.jpg?authorization=bce-auth-v1%2FALTAKzReLNvew3ySINYJ0fuAMN%2F2026-04-22T15%3A40%3A23Z%2F-1%2F%2Fdca9b58f7155219a41776f75b786d93606fd282c4a7b805f3399819576b48de2" alt="Image" width="52%" /></div>


<div style="text-align: center;"><div style="text-align: center;">Notes: The figure reports estimates from equation 10. The dependent variable is the number of trips made by a household to their focal retailer (S&S or control) during period t. The coefficients are interpreted as the displacement effect over time. Time is measured in eleven day periods and the omitted category is period t = -9. All regressions include household and period fixed effects. Standard errors are clustered at the household level. Source: Numerator household panel.</div> </div>


applied to our matched subsample.

Figure 9 plots these differences separately for treated and control households. Among control households (the green hollow points) the displaced and non-displaced follow different trends before and after the strike. Prior to the strike, displaced control households are increasingly more likely to visit their focal retailer, which they visit at t = 0 by construction. After the strike, displaced control households are still more likely to visit their focal retailer, perhaps due to the bolstering effect of the t = 0 visit, through state dependence. In contrast, among the treated group (the orange solid points) displaced and non-displaced households converge after the strike, suggesting that the strike equalized behavior by displacing a trip for the displaced households. This pattern is consistent with the assumption that baseline demand shifted equally for displaced and non-displaced treated households. This result implies that the estimate from the matched subsample is not biased due to differences in baseline-demand effects. It is further reassuring that the magnitude of the estimate from the matched subsample is similar to that from the full sample, suggesting that if the latter is capturing differences in baseline-demand effects, they are relatively small.

<div style="text-align: center;"><div style="text-align: center;">Figure 9: Differences in Trips Between Displaced and Non-Displaced Households Over Time</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//952d5d62-802a-4ece-a5ab-d491f87c19b8/markdown_4/imgs/img_in_chart_box_288_199_933_619.jpg?authorization=bce-auth-v1%2FALTAKzReLNvew3ySINYJ0fuAMN%2F2026-04-22T15%3A40%3A23Z%2F-1%2F%2F451c069a99001c7d88dd7e0ed75f21c19a4dcae782e5fa0b716dad0dd6b95768" alt="Image" width="52%" /></div>


<div style="text-align: center;"><div style="text-align: center;">Notes: This figure reports event study estimates of the difference in focal retailer trips between displaced and non-displaced households for periods t = -8 to t = 12, relative to period t = -9, using Equation 13. The dependent variable is the number of trips made by a household to their focal retailer (S&S or control) during period t. The solid orange line compares changes in trip patterns for S&S households and the dashed green line uses data from control households. All estimates include household and period fixed effects. Confidence intervals reflect standard errors clustered at the household level. Source: Numerator household panel.</div> </div>


### 5.3 Heterogeneity in Trip Displacement Effects

We have thus far remained agnostic as to why past store choices may influence current choices, and how that effect may vary across consumers. In this section, we explore the heterogeneity in consumers' responses to the strike to: (i) add insights on the potential forces behind state dependence, and (ii) examine how the magnitude of the trip displacement effect varies based on observable characteristics and choices.

Drivers of State Dependence Dubé et al. (2010) outline three behavioral mechanisms that could drive state dependence: loyalty, search, and learning. The loyalty mechanism suggests that the mere act of visiting a store creates attachment and/or inertia, making a return visit more likely. Alternatively, consumer search and learning can also explain state dependence in store choice. If consumers have imperfect information about store quality, and if it is costly to resolve this uncertainty, consumers should be more likely to visit stores that they are familiar with.

Our first set of analyses examines whether each of these mechanisms plays a meaningful role in the displacement effect estimated in the previous section. We do so by comparing displacement effects for households that visited a new store during the strike to that for

those who relied only on stores they had previously used. We define a new store as one the household had not visited in the pre-strike window. We posit that if loyalty alone drives state dependence, then visiting a new store should not matter for the size of the displacement effect. In contrast, if search and learning are the only drivers for our results, then the displacement effect should appear only among households that visited new stores during the strike.

To evaluate the likely presence of these mechanisms, we use a quadruple-difference estimator, introducing an interaction with an indicator for whether the household visited a new store during the strike:

 $$ \begin{aligned}Trips_{it}=&\delta^{\mathrm{B}}\mathbb{I}(t>0)\times\mathbb{I}(S\&S customer_{i}=1)+\\&\delta^{\mathrm{D}}\mathbb{I}(t>0)\times\mathbb{I}(S\&S customer_{i}=1)\times\mathbb{I}(displaced_{i}=1)+\\&\beta\mathbb{I}(t>0)\times\mathbb{I}(displaced_{i}=1)+\\&\gamma_{1}\mathbb{I}(New Store_{i}=1)\times\mathbb{I}(t>0)\times\mathbb{I}(S\&S customer_{i}=1)+\\&\gamma_{2}\mathbb{I}(New Store_{i}=1)\times\mathbb{I}(t>0)\times\mathbb{I}(S\&S customer_{i}=1)\times\mathbb{I}(displaced_{i}=1)+\\&\gamma_{3}\mathbb{I}(New Store_{i}=1)\times\mathbb{I}(t>0)\times\mathbb{I}(displaced_{i}=1)+\\&\phi_{i}+\omega_{t}+\nu_{it},&\quad(1)\end{aligned} $$ 

where we are interested in the estimate of the  $ \gamma_{2} $ parameter, which captures the difference in the displacement effect for households that visited new stores during the period of the strike. We report the estimates of  $ \delta^{D} $ and  $ \gamma_{2} $ in Column 1 of Table 6 and see that the displacement effect is larger among households who visited a new store. The full set of estimates are shown in Column 1 of Table A8, for completeness. We estimate a decrease by 7% for households who did not visit a new store, and a 10% decrease for those who did. This pattern points to a meaningful role of search and learning frictions in driving state dependence. At the same time, there remains an economically meaningful displacement effect among households that shopped at familiar stores, indicating that loyalty may also contribute to state dependence. $ ^{14} $

Heterogeneity Based on Demographics and Spending Patterns We next examine how displacement varies with observable household characteristics. We segment households based on their pre-strike spending level at S&S, as well as demographics such as income and age. It is difficult to know ex ante which customers are most likely to switch and remain with competitors, yet the distinction matters for the firm. If higher value customers are

<div style="text-align: center;"><div style="text-align: center;">Table 6: Heterogeneity in Trip Displacement Effects</div> </div>




<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>(1)</td><td style='text-align: center; word-wrap: break-word;'>(2)</td><td style='text-align: center; word-wrap: break-word;'>(3)</td><td style='text-align: center; word-wrap: break-word;'>(4)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>displaced  $ \times $ S\&amp;S  $ \times $ post</td><td style='text-align: center; word-wrap: break-word;'>$ -0.1483^{***}(0.0378) $</td><td style='text-align: center; word-wrap: break-word;'>$ -0.2143^{***}(0.0443) $</td><td style='text-align: center; word-wrap: break-word;'>$ -0.1517^{**}(0.0623) $</td><td style='text-align: center; word-wrap: break-word;'>$ -0.0079(0.0822) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>new store  $ \times $ displaced  $ \times $ S\&amp;S  $ \times $ post</td><td style='text-align: center; word-wrap: break-word;'>$ -0.1980^{**}(0.0843) $</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>high spender  $ \times $ displaced  $ \times $ S\&amp;S  $ \times $ post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>$ -0.0048(0.0674) $</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>low income  $ \times $ displaced  $ \times $ S\&amp;S  $ \times $ post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>$ 0.0662(0.1033) $</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>mid income  $ \times $ displaced  $ \times $ S\&amp;S  $ \times $ post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>$ -0.1073(0.0775) $</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>age21-34  $ \times $ displaced  $ \times $ S\&amp;S  $ \times $ post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>$ -0.3816^{**}(0.1727) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>age35-44  $ \times $ displaced  $ \times $ S\&amp;S  $ \times $ post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>$ -0.1601(0.1035) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>age45-54  $ \times $ displaced  $ \times $ S\&amp;S  $ \times $ post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>$ -0.2584^{**}(0.1034) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>age55-64  $ \times $ displaced  $ \times $ S\&amp;S  $ \times $ post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>$ -0.2371^{**}(0.1115) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Observations</td><td style='text-align: center; word-wrap: break-word;'>140,595</td><td style='text-align: center; word-wrap: break-word;'>140,595</td><td style='text-align: center; word-wrap: break-word;'>140,595</td><td style='text-align: center; word-wrap: break-word;'>140,595</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>R $ ^{2} $</td><td style='text-align: center; word-wrap: break-word;'>0.59609</td><td style='text-align: center; word-wrap: break-word;'>0.59664</td><td style='text-align: center; word-wrap: break-word;'>0.59607</td><td style='text-align: center; word-wrap: break-word;'>0.59621</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Within R $ ^{2} $</td><td style='text-align: center; word-wrap: break-word;'>0.00137</td><td style='text-align: center; word-wrap: break-word;'>0.00273</td><td style='text-align: center; word-wrap: break-word;'>0.00132</td><td style='text-align: center; word-wrap: break-word;'>0.00168</td></tr></table>

Notes: Column 1 shows the results of equation 14, a quadruple-difference specification, with household and period-level fixed effects. The dependent variable is the number of trips made by a household to their focal retailer (S&S or control) during period t. Columns 2-4 show the results of analogous specifications with high spender, income, and age indicators, respectively. Standard errors are clustered at the household level.

Source: Numerator household panel.

more easily displaced, the long term cost of a strike is greater. Understanding which groups are most influenced by state dependence therefore provides useful guidance for managerial decisions.

Table 6 shows the results. Column 2 asks whether the strike had larger displacement effects for households that spent more at S&S before the strike. We use the analogous version to Equation 14 above where we now allow for an interaction with an indicator for high spenders, defined as households whose pre-strike spending was above the sample median. Here we do not find any meaningful differences in displacement effects between the two groups of shoppers.

Next, we examine how the displacement effect varies with income and age. Column 3

reports the results for income, where we find no meaningful differences across income groups. Column 4 allows for interactions with age, where the excluded category is households over age 65. Interestingly, we find no displacement effect among households over 65, while the largest effect is for the youngest households (25-34). These results could mean that older consumers behave differently during the strike (e.g., are less likely to visit a new store or switch to a worse substitute). Alternatively, these results are consistent with consumption capital theory (Stigler and Becker, 1977), whereby consumers' purchase histories causally shape their preferences, as has been seen in the context of brand (Bronnenberg et al., 2012) and category choice (Bronnenberg et al. (2022); Levine (2023)).

## 6 Discussion

We study the long-term effects of the 2019 Stop & Shop labor strike, which effectively closed 240 stores for 11 days. The strike may have directly affected consumers' preferences for the firm, while also triggering a firm response. We develop an identification strategy that exploits variation in when households visit their focal retailers. By comparing the effects of the strike across households who were, and were not, expected to visit their focal retailer during the strike, we are able to net out changes driven by shifts in baseline demand and isolate the causal effect of missing a planned visit.

We find that households whose planned visits were displaced during the strike make approximately 0.20 fewer trips per period in the months following the strike, corresponding to a 9.9% decline relative to pre-strike shopping intensity. This reduction emerges immediately after the strike and persists throughout the four-month post-strike window, attenuating gradually over time. We also document substantial heterogeneity in the displacement effect. The decline in subsequent visits is larger for households that are induced to shop at a new store during the strike, consistent with learning and search frictions representing an important source of state dependence.

Our results suggest that state dependence is an important driver of persistence in store choice. These results clarify key aspects of competition, including how incumbents benefit from state dependence in demand or how temporary promotions may attract customers, not only in the short run but also in the long run. Furthermore, we believe that the lessons learned from the S&S strike can help characterize the long-term costs of labor stoppages, and supply disruptions more generally, adding insight to how those costs may vary depending on market characteristics and the workers' position in the supply chain. If past choices causally affect present choices, then labor stoppages that force consumers to patronize another firm

ought to be more costly. Therefore, workers' leverage increases with their ability to cause a supply disruption, and the long-term effects of that supply disruption depend on the availability and viability of substitutes.

Workers can only disrupt supply if the firm's output is depleted before the workers are replaced. This means that workers involved in so-called "low-skilled" manufacturing, particularly of stockpile-able goods, have little leverage compared to workers involved in the distribution of goods. Furthermore, when workers control the means of distribution for multiple firms, such as in the case of the recent strikes by the International Longshoremen's Association, impacting 36 U.S. ports (Kaye, 2024), and that by the Teamsters union, impacting operations at Amazon warehouses (Hadero, 2024), they have the potential to depress post-strike demand for firms other than their employer.

Conditional on a supply disruption, our results suggest that strikes are more costly when consumers are forced to switch to competitors. Therefore, we would expect that supply disruptions in industries with few viable substitutes or high switching costs, such as healthcare or education, have relatively little long-term impact on consumer demand. Furthermore, the finding that trip-displacement has a larger effect for households that visited a new store suggests that the long-term costs of supply disruptions might be greater in settings with higher search and learning frictions. For example, strikes that threaten to disrupt supply for CPG products, such as the 2021 Frito-Lay and Kellogg strikes, may have lower long-term costs, as consumers likely have tried the alternatives prior to the strike, and are more likely to switch back following its resolution.

Lastly, our results show that any negative reputational effects of the strike are small enough to be counteracted by S&S's strategic response, suggesting that supply disruptions provide a necessary source of leverage for workers. This has important policy implications, as anti-union sentiment by employers has resulted in the weakening of the National Labor Relations Act over the past 50 years, eroding protections for workers trying to organize and engage in collective bargaining.

## References

Bachmann, Rüdiger, Gabriel Ehrlich, Ying Fan, Dimitrije Ruzic, and Benjamin Leard, “Firms and collective reputation: a study of the volkswagen emissions scandal,” Journal of the European Economic Association, 2023, 21 (2), 484–525.

Bai, Jie, Ludovica Gazze, and Yukun Wang, “Collective reputation in trade: Evidence from the Chinese dairy industry,” Review of Economics and Statistics, 2022, 104 (6), 1121–1137.

Barrage, Lint, Eric Chyn, and Justine Hastings, “Advertising and environmental stewardship: Evidence from the BP oil spill,” American Economic Journal: Economic Policy, 2020, 12 (1), 33–61.

Becker, Brian E and Craig A Olson, “The impact of strikes on shareholder equity,” ILR Review, 1986, 39 (3), 425–438.

Bronnenberg, Bart J, Jean-Pierre H Dubé, and Matthew Gentzkow, “The evolution of brand preferences: Evidence from consumer migration,” American Economic Review, 2012, 102 (6), 2472–2508.

Bronnenberg, Bart, Jean-Pierre Dubé, and Joonhwi Joo, “Millennials and the takeoff of craft brands: Preference formation in the us beer industry,” Marketing Science, 2022, 41 (4), 710–732.

Buell, Griffin, “Strike Empties the Shelves at Stop & Shop,” 2019.

Bureau of Labor Statistics, "Work Stoppages Summary," February 2024.

Christensen, Hans B, Emmanuel T De George, Anthony Joffre, and Daniele Macciocchi, “Consumer Responses to the Revelation of Corporate Social Irresponsibility,” in “Consumer Responses to the Revelation of Corporate Social Irresponsibility,” [Sl]: SSRN, 2023.

Conway, Jacob and Levi Boxell, “Consuming values,” Available at SSRN 4855718, 2024.

DeCosta-Klipa, Nik, “What you need to know about the Stop & Shop strike,” 2019.

Dubé, Jean-Pierre, Günter J. Hitsch, and Peter E. Rossi, “State Dependence and Alternative Explanations for Consumer Inertia,” The RAND Journal of Economics, 2010, 41 (3), 417–445.

Dwyer, Michael, “Stop & Shop traffic from loyal customers plummets 75 percent during strike,” 2019.

Freimer, Marshall and Dan Horsky, “Try it, you will like it: Does consumer learning lead to competitive price promotions?,” Marketing Science, 2008, 27 (5), 796–810.

Gruber, Jonathan and Samuel A Kleiner, “Do strikes kill? Evidence from New York state,” American Economic Journal: Economic Policy, 2012, 4 (1), 127–157.

Hadero, Haleluya, “What to know about Amazon workers strike at multiple delivery hubs,” PBS News, December 2024.

Hahsler, Michael, Matthew Piekenbrock, and Derek Doran, “dbscan: Fast Density-Based Clustering with R,” Journal of Statistical Software, 2019, 91 (1), 1–30.

Heckman, J. J., “Heterogeneity and State Dependence,” in ed. Sherwin Rose, ed., Studies in Labor Markets, University of Chicago Press, 1981.

Ho, Daniel E., Kosuke Imai, Gary King, and Elizabeth A. Stuart, “MatchIt: Nonparametric Preprocessing for Parametric Causal Inference,” Journal of Statistical Software, 2011, 42 (8), 1–28.

Huang, Yufeng and Bart J Bronnenberg, “Consumer transportation costs and the value of e-commerce: Evidence from the dutch apparel industry,” Marketing Science, 2023, 42(5), 984–1003.

Johnston, Katie, “Visits by Loyal Stop Shop customers decline 75 percent during strike,” Apr 2019.

Kaye, Danielle, "Here's What to Know About the Port Strike," The New York Times, September 2024.

Knight, Samsun, “Retail Demand Interdependence and Chain Store Closures,” Available at SSRN 4234510, 2022.

Kotschedoff, Marco JW, Liliana Kowalczyk, and Els Breugelmans, “The persistence of grocery shopping behavior and retailer choice: Evidence from a major labor strike: MJW Kotschedoff et al.,” Quantitative Marketing and Economics, 2025, pp. 1–44.

Krueger, Alan B and Alexandre Mas, “Strikes, scabs, and tread separations: labor strife and the production of defective Bridgestone/Firestone tires,” Journal of political Economy, 2004, 112 (2), 253–289.

Larcom, Shaun, Ferdinand Rauch, and Tim Willems, “The benefits of forced experimentation: Striking evidence from the London underground network,” The Quarterly Journal of Economics, 2017, 132 (4), 2019–2055.

Leuz, Christian and Catherine Schrand, “Disclosure and the cost of capital: Evidence from firms’ responses to the Enron shock,” Technical Report, National Bureau of Economic Research 2009.

Levine, Julia, “Are Menthol Cigarettes More Addictive? A Cross-Category Comparison of Habit Formation,” Working Paper, 2023.

— and Stephan Seiler, “Identifying state dependence in brand choice: Evidence from hurricanes,” Marketing Science, 2023, 42 (5), 934–957.

Liaukonyté, Jūra, Anna Tuchman, and Xinrong Zhu, “Frontiers: Spilling the beans on political consumerism: Do social media boycotts and buycotts translate to real sales impact?,” Marketing Science, 2023, 42 (1), 11–25.

Liaw, Andy and Matthew Wiener, “Classification and Regression by randomForest,” R News, 2002, 2 (3), 18–22.

Mas, Alexandre, “Labour unrest and the quality of production: Evidence from the construction equipment resale market,” The review of economic studies, 2008, 75 (1), 229–258.

Olden, Andreas and Jarle Møen, “The triple difference estimator,” The Econometrics Journal, 2022, 25 (3), 531–553.

Osborne, Matthew, “Consumer learning, switching costs, and heterogeneity: A structural examination,” Quantitative Marketing and Economics, 2011, 9 (1), 25–70.

Pakes, Ariel, Jack R Porter, Mark Shepard, and Sophie Calder-Wang, “Unobserved heterogeneity, state dependence, and health plan choices,” Technical Report, National Bureau of Economic Research 2021.

Rhee, Hongjai and David R Bell, “The inter-store mobility of supermarket shoppers,” Journal of Retailing, 2002, 78 (4), 225–237.

Sanders, Bernie (@BernieSanders), “@Stopandshop, a multibillion-dollar company, wants to drastically cut health care for 31,000 workers. I stand with @UFCW workers in their fight to protect health care and workers’ rights.” Twitter 2019. April 11, 2019, 3:08PM. https://x.com/BernieSanders/status/1116417831397199873.

Schmidt, Martin B and David J Berri, “The impact of labor strikes on consumer demand: An application to professional sports,” American Economic Review, 2004, 94(1), 344–357.

Shay, Jim, “Timeline of Stop & Shop Strike,” 2019.

Shriver, Scott K and Bryan Bollinger, “Demand expansion and cannibalization effects from retail store entry: A structural analysis of multichannel demand,” Management Science, 2022, 68 (12), 8829–8856.

Simonov, Andrey, Jean-Pierre Dubé, Günter Hitsch, and Peter Rossi, “State-Dependent Demand Estimation with Initial Conditions Correction,” Journal of Marketing Research, 2020, 57 (5), 789–809.

Springer, Jon, "Ahold Delhaize Reveals Heavy Toll of Stop & Shop Strike," 2019.

Stigler, George J and Gary S Becker, “De gustibus non est disputandum,” The american economic review, 1977, 67 (2), 76–90.

The Shelby Report, “The Griffin Report Unveils Its 2019 Northeast Market Review,” 2019.

Troncoso, Isamar, Minkyung Kim, Ishita Chakraborty, and SooHyun Kim, “The impact of unionization on consumer perceptions of service quality: Evidence from starbucks,” Available at SSRN 4657689, 2023.

Wang, Kitty and Shijie Lu, “Corporate political positioning and sales: Evidence from a natural experiment,” Available at SSRN 4084106, 2022.

Warren, Elizabeth (@SenWarren), “31k New England @StopandShop workers just went on strike for a contract that provides fair wages, good benefits, a secure retirement. I stand in solidarity with @UFCW for these hard-working families to be treated with the dignity respect they deserve.” Twitter 2019. April 11, 2019, 2:40PM. https://x.com/senwarren/status/1116410760039735297.

### A Appendix

### A Store Location Imputation

In order to separate S&S customers who shop in the striking and non-striking region, as well as to select households for the control group, we need to know where households shop. Coordinate data, reflecting panelists' location at the time of reporting the trip, is provided for 45% of trips in the Numerator panel. In this section, we detail how we impute store locations for households' trips. We begin by creating a store ID for each distinct store location, before assigning each store ID to a common set of geographic variables.

A store number, which represents how a retailer refers to a given location, is reported for 44% of trips. While these store numbers should, in theory, represent distinct locations for a given retailer, there is often variation in the geographic information provided. This variation could reflect changes in retailers' numbering systems, in which case trips should be attributed to the provided geographic location. However, this variation could also reflect differences in where panelists report their trips (e.g., in the store parking lot, or at a gas station down the road), in which case the geographic information should be ignored and the trips should be attributed to a common location for the given store number. To address this, we cluster observed coordinates within each banner using the DBSCAN algorithm, taking an  $ \epsilon $-radius of 0.25 miles (Hahsler et al., 2019). Of the resulting clusters, 1.6% contain multiple distinct store numbers for a given banner, likely reflecting changes in retailers' numbering systems. Only 0.00001% of banner/store-number combinations are assigned to different clusters, suggesting that the clustering allows us to cut down on noise driven by variation in reporting locations while grouping trips that were spuriously associated with distinct store numbers. We assume that all trips made to a given cluster for a given banner are made at the same store location, and hereafter refer to a cluster-banner combination as a "store ID." We assign each store ID to a common set of geographic variables, taking the most commonly observed values.

We deal with missingness related to S&S trips with special care, ensuring that store IDs can be matched to a known S&S location that was operating during our sample period. We compile a list of all such locations using S&S's website, which lists the presently active locations. This list is supplemented with addresses for locations that have closed since the sample period, collected from local news sources and Yelp.

For cases where a S&S trip is associated with a set of coordinates, but no store number, the trip is assigned to the nearest known S&S location. For cases where a S&S trip is reported with a store number that is never associated with geographic information, we use the locations of trips made on the same day to approximate the location, taking the time-weighted average of the coordinates for the trips made before and after the S&S visit. We then cluster all of the time-weighted averages within store number, using the DBSCAN algorithm, and assign the cluster to the nearest known S&S location.

### B Changes in Discounts between S&S and the Control Retailers

In Section 2.2, we show that S&S increased promotions relative to its local competitors following the strike. In this section, we evaluate post strike changes at The Giant Company (TGC) and

Giant Food (GF) relative to their local competitors and assess whether any adjustments differ from the promotional response observed at S&S. As households choose among locally available stores, the relevant comparison is how discounts at each focal retailer change relative to other grocery stores operating in the same local markets.

To summarize post-strike changes in discounts, we estimate the following regression on a panel tracking discounts for items sold at the set of focal retailers (S&S, TGC and GF) and their local competitors, defined as grocery stores that operate within the same zip codes:

 $$ \begin{aligned}discount_{kjmt}=&\beta_{1}\mathbb{I}(j\in\{S\&S,TGC,GF\})\times\mathbb{I}(t>0)+\\&\beta_{2}\mathbb{I}(j=S\&S)\times\mathbb{I}(t>0)+\\&\alpha_{kjm}+\omega_{t}+\nu_{kjmt},\end{aligned} $$ 

where  $ \alpha_{kjm} $ and  $ \omega_t $ denote item-by-retailer-by-state, and time fixed effects, respectively. The  $ \beta_1 $ parameter captures the average post-strike change in discounts at the set of focal retailers relative to discounts at their local competitors. The  $ \beta_2 $ parameter captures the additional change in discounts at S&S relative to the control retailers.

Table A1 reports the results. The Focal Retailer × post coefficient (i.e.,  $ \hat{\beta}_{1} $) indicates a modest increase in discounts at the control retailers relative to their local competitors. In contrast, we see a substantially larger S&S × post coefficient (i.e.,  $ \hat{\beta}_{2} $), indicating that S&S increased discounts by far more than the control retailers did in their respective local markets.

<div style="text-align: center;"><div style="text-align: center;">Table A1: Post-Strike Changes in Discounts Relative to Local Competitors</div> </div>




<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>(1)</td></tr><tr><td rowspan="2">Focal Retailer  $ \times $ post</td><td style='text-align: center; word-wrap: break-word;'>0.3096 $ ^{***} $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>(0.0476)</td></tr><tr><td rowspan="2">S\&amp;S  $ \times $ post</td><td style='text-align: center; word-wrap: break-word;'>1.678 $ ^{***} $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>(0.0828)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Observations</td><td style='text-align: center; word-wrap: break-word;'>619,863</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>R $ ^{2} $</td><td style='text-align: center; word-wrap: break-word;'>0.43576</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Within R $ ^{2} $</td><td style='text-align: center; word-wrap: break-word;'>0.00222</td></tr></table>

<div style="text-align: center;"><div style="text-align: center;">Notes: This table reports the estimates of Equation 15 with fixed effects at the item-retailer-state and period level. Standard errors are clustered at the item-retailer-state level. These results suggest that all focal retailers, including the controls, increased their discounts after the strike relative to their local competitors, through S&S did so by more than the control retailers.</div> </div>


### C Assessing the Parallel Trends Assumption

Our identification strategy is subject to the assumption that the treated and control groups follow parallel trends in the absence of treatment within displacement groups, or that the difference in trends between treated and control groups is the same across displaced and non-displaced households (Olden and Møen, 2022). To assess the validity of this assumption, we

conduct two sets of analyses using pre-strike data. First, we run the following regression, separately for the displaced and non-displaced households:

 $$ \mathrm{Trips}_{it}=\delta\times t\times\mathbb{I}(\mathrm{S\&S\ household}_{i}=1)+\phi_{i}+\omega_{t}+\nu_{it}, $$ 

where the estimated  $ \delta $ parameter captures any difference in linear time trends between the treated and control group prior to the strike, which we hereafter refer to as the “bias.” To test whether this bias is equal across displaced and non-displaced households, we run the following:

 $$ \begin{aligned}Trips_{it}=&\delta_{1}\times t\times\mathbb{I}(S\&S household_{i}=1)+\\&\beta\times t\times\mathbb{I}(displaced_{i}=1)+\\&\delta_{2}\times t\times\mathbb{I}(S\&S household_{i}=1)\times\mathbb{I}(displaced_{i}=1)+\\&\phi_{i}+\omega_{t}+\nu_{it},\end{aligned} $$ 

where  $ \delta_{1} $ captures the bias for the non-displaced households, and  $ \delta_{2} $ captures the difference in biases between the displaced and non-displaced households.

Table A2 shows the results of this analysis, applied to the full sample and the matched subsample. Columns 1 and 2 show the results of Equation 16, estimated on the sample of displaced and non-displaced households, respectively. While column 1 shows that displaced treated and control households follow the same linear time trend prior to the strike, column 2 reveals a slight bias among the non-displaced households, with treated households exhibiting a steeper decline in focal retailer trips than control households. This suggests that our estimates of the baseline-demand effects will include some bias. Column 3 presents the results of Equation 17. The estimate on displaced×S&S×t shows that the difference in biases between the displaced and non-displaced households is not significantly different from zero. This is also seen in our event study shown in Figure 7. Therefore, we interpret these results as evidence that the estimated displacement effect is unbiased.

Columns 4-6 of Table A2 show the results of the same specifications, applied to the matched subsample. Here, we find no statistically significant difference in trends, for either the displaced nor non-displaced households.

### D Prediction Error

Our identification strategy relies on classifying households as displaced or non-displaced based on whether they were expected to visit their focal retailer at t = 0. We classify households based on a prediction model trained on pre-strike behavior. The discussion below describes how prediction error can bias our estimates, provides suggestive evidence on the size of potential biases, and explains how we use observed behavior of control households to limit its impact.

To build intuition for how prediction error may bias our estimates, we first simulate state-dependent choices, following the DGF from section 3, in worlds with and without a strike that coincides with a negative shock to baseline demand at period t = 0. We refer to the households in these counterfactual scenarios, with and without the strike, as “treated” and “control,” respectively, to match the ideas in the empirical implementation.

The top panels of Figure A1 plot average focal retailer trips for treated and control house-

<div style="text-align: center;"><div style="text-align: center;">Table A2: Differences in Pre-Strike Trends between Treated and Control Households</div> </div>




<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>(1)</td><td style='text-align: center; word-wrap: break-word;'>Full(2)</td><td style='text-align: center; word-wrap: break-word;'>(3)</td><td style='text-align: center; word-wrap: break-word;'>(4)</td><td style='text-align: center; word-wrap: break-word;'>Matched(5)</td><td style='text-align: center; word-wrap: break-word;'>(6)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>S\&amp;S \times t</td><td style='text-align: center; word-wrap: break-word;'>-0.0001(0.0071)</td><td style='text-align: center; word-wrap: break-word;'>-0.0092^{**}(0.0036)</td><td style='text-align: center; word-wrap: break-word;'>-0.0092^{***}(0.0036)</td><td style='text-align: center; word-wrap: break-word;'>-0.0139(0.0153)</td><td style='text-align: center; word-wrap: break-word;'>-0.0160(0.0118)</td><td style='text-align: center; word-wrap: break-word;'>-0.0160(0.0118)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>displaced \times t</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>0.0367^{***}(0.0050)</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>0.0732^{***}(0.0134)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>displaced \times S\&amp;S \times t</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>0.0091(0.0080)</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>0.0022(0.0193)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Observations</td><td style='text-align: center; word-wrap: break-word;'>33,597</td><td style='text-align: center; word-wrap: break-word;'>26,658</td><td style='text-align: center; word-wrap: break-word;'>60,255</td><td style='text-align: center; word-wrap: break-word;'>5,625</td><td style='text-align: center; word-wrap: break-word;'>5,625</td><td style='text-align: center; word-wrap: break-word;'>11,250</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>R^{2}</td><td style='text-align: center; word-wrap: break-word;'>0.55566</td><td style='text-align: center; word-wrap: break-word;'>0.18159</td><td style='text-align: center; word-wrap: break-word;'>0.64395</td><td style='text-align: center; word-wrap: break-word;'>0.28927</td><td style='text-align: center; word-wrap: break-word;'>0.15815</td><td style='text-align: center; word-wrap: break-word;'>0.28687</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Within R^{2}</td><td style='text-align: center; word-wrap: break-word;'>1.87 \times 10^{-8}</td><td style='text-align: center; word-wrap: break-word;'>0.00037</td><td style='text-align: center; word-wrap: break-word;'>0.00224</td><td style='text-align: center; word-wrap: break-word;'>0.00019</td><td style='text-align: center; word-wrap: break-word;'>0.00056</td><td style='text-align: center; word-wrap: break-word;'>0.00769</td></tr></table>

Notes: This table shows results supporting the plausibility of the parallel trends assumptions for the full and matched sample. Columns 1 and 4 (2 and 5) show the results of equation 16 for displaced (non-displaced) households in the full and matched sample. Columns 3 and 6 show the results of equation 17 for the full and matched sample, respectively.

holds, grouped by true displacement status. True displacement status is determined based on behavior in the absence in the strike; therefore, in this baseline, households are classified as displaced if their control counterparts visited S&S at t = 0, and non-displaced otherwise. Households in these simulations are identical in all respects, therefore the difference in trends between control displaced and non-displaced households is driven by natural variation in when they visit their focal retailer. Within each group, the vertical distance between the solid and hollow markers traces the true effect of the strike over time: this reflects the baseline-demand effect for non-displaced households, and the combined baseline-demand and displacement effect for the displaced households.

The second set of panels of Figure A1 shows these same patterns when households are grouped based on inaccurate classifications of displacement status. We randomly reassign 25% of households to be classified as the wrong displacement type, so that a quarter of those labeled as displaced are in fact non-displaced, and vice versa. Comparing these outcomes to those in the top panel of the figure, we can clearly see that this misclassification changes the gap between treated and control households, creating a bias in the estimates. It widens the gap for non-displaced households and narrows it for displaced households. This would lead us to understate the displacement effect, as we would underestimate the combined effect for the displaced households, and attribute too much of that estimated effect to changes in baseline demand.

Another useful observation from these graphs is that the bias comes mainly from misclassifying control households, whose paths shift noticeably for  $ t \geq 0 $. In contrast, the solid black markers for treated households for  $ t \geq 0 $ are identical across panels. The reason for this is that none of the treated households make a visit at t = 0: for the displaced households, forgoing a visit equalizes their post-strike trajectory with that of the non-displaced households. Therefore, relabeling does not affect their outcomes, and misclassification in displacement status impacts

<div style="text-align: center;"><div style="text-align: center;">Figure A1: Simulated Focal Retailer Trips under True and Misclassified Displacement Status</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//8be22fe6-64bd-41fd-8458-70dd2f0405a1/markdown_2/imgs/img_in_chart_box_208_341_1016_1139.jpg?authorization=bce-auth-v1%2FALTAKzReLNvew3ySINYJ0fuAMN%2F2026-04-22T15%3A40%3A26Z%2F-1%2F%2F333443562c950e129fd905c7501741c34fdb52b17edba38daccbd27d22065e30" alt="Image" width="66%" /></div>


<div style="text-align: center;"><div style="text-align: center;">Notes: The figure plots average focal retailer trips over time from data simulated under the DGP described in Section 3, where choices are positively state-dependent ( $ \gamma = 0.75 $) and consumers are indifferent between the two retailers ( $ \alpha_{st} = 0 $). Panels compare treated and control households in environments with and without a strike at t = 0, after which baseline demand takes the following functional form:  $ \alpha_{st}(1) = \frac{-2}{3}t^{2} $. Solid markers correspond to outcomes in the strike environment and hollow markers correspond to outcomes in the no strike environment. Households are grouped by displacement status: left panels showing simulations for displaced and right panels showing simulations for non-displaced households. The top panels use true displacement status. The middle panels introduce classification error in displacement status. The bottom panels maintain classification error for the treated households, but remove misclassified control households.</div> </div>


<div style="text-align: center;"><div style="text-align: center;">Table A3: First Differences in Trips to Focal Retailer for Households in the Striking Region</div> </div>




<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Focal Retailer</td><td style='text-align: center; word-wrap: break-word;'>Row #</td><td style='text-align: center; word-wrap: break-word;'>Customer Type</td><td style='text-align: center; word-wrap: break-word;'>1st differences</td></tr><tr><td rowspan="2">S&amp;S</td><td style='text-align: center; word-wrap: break-word;'>1</td><td style='text-align: center; word-wrap: break-word;'>displaced</td><td style='text-align: center; word-wrap: break-word;'>$ (1-\mu_{s})[\Delta_{d,s}^{D}+\Delta_{d,s}^{B}+\Delta_{d,s}^{T}]+\mu_{s}[\Delta_{n,s}^{B}+\Delta_{n,s}^{T}] $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>2</td><td style='text-align: center; word-wrap: break-word;'>non-displaced</td><td style='text-align: center; word-wrap: break-word;'>$ \lambda_{s}[\Delta_{d,s}^{D}+\Delta_{d,s}^{B}+\Delta_{d,s}^{T}]+(1-\lambda_{s})[\Delta_{n,s}^{B}+\Delta_{n,s}^{T}] $</td></tr><tr><td rowspan="2">Control</td><td style='text-align: center; word-wrap: break-word;'>3</td><td style='text-align: center; word-wrap: break-word;'>displaced</td><td style='text-align: center; word-wrap: break-word;'>$ (1-\mu_{c})\Delta_{d,c}^{T}+\mu_{c}\Delta_{n,c}^{T} $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>4</td><td style='text-align: center; word-wrap: break-word;'>non-displaced</td><td style='text-align: center; word-wrap: break-word;'>$ \lambda_{c}\Delta_{d,c}^{T}+(1-\lambda_{c})\Delta_{n,c}^{T} $</td></tr></table>

Notes: This table shows the difference in trips to a focal retailer before and after the strike. Households are grouped based on whether they visited S&S in the pre-strike initialization period, and whether they were expected to visit their focal retailer during the strike (displaced) or not (non-displaced).

our estimates almost entirely through changes in the control group.

Recognizing this insight, our approach mitigates the problem by exploiting a key advantage of the control households: we observe their store choices in a world without a strike. This allows us to identify which control households are truly displaced and which are not, and to remove the misclassified cases. The bottom panels of Figure A1 use the same misclassified simulations as shown in the middle panels, but drops misclassified control households, such that the remaining controls follow the same path as those shown in the top panels. If we use this “corrected” control group, the post-strike differences between treated and controls reflect the true differences resulting from the strike. We acknowledge that this correction may introduce slight differences in pre-strike trends, as visible in the three periods before the strike. In our empirical analyses, we present multiple event-study plots to verify that any deviation in pre-strike trends is slight, and more thoroughly evaluate differences in trends in Section C.

The discussion above assumes positive state dependence (i.e., a negative displacement effect) and a negative baseline-demand effect. In what follows, we relax these assumptions and formally characterize how prediction error affects the estimated displacement effect. Imperfect prediction leads to two sources of misclassification error:

1. False positives: households that were predicted to visit their focal retailer at t = 0, that would not have done so in the absence of a strike.

2. False negatives: households that were not predicted to visit their focal retailer at t = 0, that would have done so in the absence of a strike.

Let the prediction error rates be denoted by  $ \mu $ and  $ \lambda $, where  $ \mu $ is the false positive rate and  $ \lambda $ is the false negative rate. Table A3 incorporates these two forms of error into the first differences from Table 1. For example, row 1 reports the difference between post-strike and pre-strike trips for treated households labeled as displaced. The first difference captures a weighted average effect from truly displaced households  $ (1 - \mu_s)[\Delta_d, s^D + \Delta_d, s^B + \Delta_d, s^T] $ and false positives  $ (\mu_s[\Delta_{n,s}^B + \Delta_{n,s}^T]) $.

Recall that we effectively identify the displacement effect by differencing two difference-in-

differences estimators. Substituting the expressions from Table A3 yields:

 $$ \begin{align*}(\Delta\mathrm{Trips}_{d,s}-\Delta\mathrm{Trips}_{d,c})-(\Delta\mathrm{Trips}_{n,s}-\Delta\mathrm{Trips}_{n,c})=&(1-\mu_{s}-\lambda_{s})\Delta_{d,s}^{D}+\\&(1-\mu_{s}-\lambda_{s})[\Delta_{d,s}^{T}-\Delta_{n,s}^{T}]-\\&(1-\mu_{c}-\lambda_{c})[\Delta_{d,c}^{T}-\Delta_{n,c}^{T}]+\\&(\Delta_{d,s}^{B}-\Delta_{n,s}^{B}).\end{align*} $$ 

In what follows, we impose two assumptions. First, parallel trends within assigned displacement groups,  $ \Delta_{n,c}^{T} = \Delta_{n,s}^{T} $ and  $ \Delta_{d,c}^{T} = \Delta_{d,s}^{T} $. Second, equal baseline-demand effects across households assigned to each group,  $ \Delta_{d,s}^{B} = \Delta_{n,s}^{B} $.

Under these assumptions, Equation 18 simplifies to

 $$ \begin{align*}(\Delta\mathrm{Trips}_{d,s}-\Delta\mathrm{Trips}_{d,c})-(\Delta\mathrm{Trips}_{n,s}-\Delta\mathrm{Trips}_{n,c})&=(1-\mu_{s}-\lambda_{s})\Delta_{d,s}^{D}+\ $ \mu_{c}+\lambda_{c}-\mu_{s}-\lambda_{s})[\Delta_{d,s}^{T}-\Delta_{n,s}^{T}].\end{align*} $$ 

Naïve Approach: Suppose control households are assigned to displacement groups using predicted behavior, in the same method as done for the treated groups. We see in Section 4.3 that accuracy rates for t = -1 are similar across treated and control households. Therefore, it is reasonable to assume that misclassification errors are the same across the two groups of households: i.e.,  $ \mu_s = \mu_c $ and  $ \lambda_s = \lambda_c $. Under that assumption, Equation 19 simplifies to:

 $$ \hat{\Delta}_{d,s}^{D1}=\Delta_{d,s}^{D}-\underbrace{(\mu_{s}+\lambda_{s})\Delta_{d,s}^{D}}_{\mathrm{b i a s}}. $$ 

The expression above shows that any misclassification error biases the estimated displacement effect toward zero. Moreover, this conceptualization provides us with a back-of-the-envelope way to bound the true displacement effect, using the realizations of  $ \mu_{s} $ and  $ \lambda_{s} $, which we do below.

Introducing the Correction: Our proposed correction eliminates misclassification among controls, implying  $ \mu_{c} = \lambda_{c} = 0 $. Under this restriction, Equation 19 becomes:

 $$ \hat{\Delta}_{d,s}^{D2}=\Delta_{d,s}^{D}-\underbrace{(\mu_{s}+\lambda_{s})\Delta_{d,s}^{D}}_{\mathrm{bias}}-\underbrace{(\mu_{s}+\lambda_{s})[\Delta_{d,s}^{T}-\Delta_{n,s}^{T}]}_{\mathrm{correction}}. $$ 

The correction term adjusts for differences in underlying trends between displaced and non-displaced treated households. This may result in an over-correction if the absolute difference in trends is greater in magnitude than the displacement effect itself.

To evaluate this concern, Columns 1 and 2 of Table A4 show the results of our main specification, run on data with and without the correction to the controls. We estimate a larger (in magnitude) displacement effect using the corrected approach. We perform a back-of-the-envelope calculation to assess whether the correction results in a lower or upper bound for the magnitude of the true effect. Using observed prediction error rates from the control group ( $ \mu_{c} = 0.21 $ and  $ \lambda_{c} = 0.24 $) and the estimated effect from the naïve approach, we solve for

<div style="text-align: center;"><div style="text-align: center;">Table A4: Identifying The Effects of Trip Displacement and Baseline Demand</div> </div>




<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td rowspan="2"></td><td colspan="2">Full</td><td colspan="2">Matched</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Naive (1)</td><td style='text-align: center; word-wrap: break-word;'>Corrected (2)</td><td style='text-align: center; word-wrap: break-word;'>Naive (3)</td><td style='text-align: center; word-wrap: break-word;'>Corrected (4)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>S\&amp;S \times post</td><td style='text-align: center; word-wrap: break-word;'>0.0101 (0.0153)</td><td style='text-align: center; word-wrap: break-word;'>0.0538^{***} (0.0152)</td><td style='text-align: center; word-wrap: break-word;'>-0.0472 (0.0367)</td><td style='text-align: center; word-wrap: break-word;'>0.0394 (0.0406)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>displaced \times S\&amp;S \times post</td><td style='text-align: center; word-wrap: break-word;'>-0.1434^{***} (0.0328)</td><td style='text-align: center; word-wrap: break-word;'>-0.1989^{***} (0.0340)</td><td style='text-align: center; word-wrap: break-word;'>-0.0698 (0.0624)</td><td style='text-align: center; word-wrap: break-word;'>-0.2233^{***} (0.0743)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Observations</td><td style='text-align: center; word-wrap: break-word;'>165,312</td><td style='text-align: center; word-wrap: break-word;'>140,595</td><td style='text-align: center; word-wrap: break-word;'>38,388</td><td style='text-align: center; word-wrap: break-word;'>26,250</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>R^{2}</td><td style='text-align: center; word-wrap: break-word;'>0.58312</td><td style='text-align: center; word-wrap: break-word;'>0.59602</td><td style='text-align: center; word-wrap: break-word;'>0.29921</td><td style='text-align: center; word-wrap: break-word;'>0.29649</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Within R^{2}</td><td style='text-align: center; word-wrap: break-word;'>0.00144</td><td style='text-align: center; word-wrap: break-word;'>0.00121</td><td style='text-align: center; word-wrap: break-word;'>0.00093</td><td style='text-align: center; word-wrap: break-word;'>0.00225</td></tr></table>

Notes: Column 1 shows the results of running the regression specified in Equation 9. Standard errors are clustered at the household-retailer level.

the displacement effect following equation 20. This yields an implied displacement effect of -0.2607, suggesting that the correction provides a lower bound on the magnitude of the true effect.

For completeness, we repeat the same analyses for the matched sample. By matching displaced to non-displaced households based on pre-strike purchase behavior, we hope to mitigate any bias generated by unobservable differences in pre-strike demand between the groups. The results are shown in columns 3 and 4 of Table A4. We again estimate a larger (in magnitude) displacement effect using the corrected approach.

### E Matching Displaced to Non-Displaced Households

To test whether our results are driven by differences in pre-strike baseline demand for the focal retailer, we apply our identification strategy to a matched subset of households. This section details how we select the sample used for this analysis.

For each household, we use their pre-strike purchase history to calculate: (i) the share of trips made to the focal retailer and (ii) the probability of visiting the focal retailer conditional on having visited it in the last period. These variables are designed to proxy for the two parameters of the conceptual model, discussed in Section 3: baseline demand and state dependence. A consumer with high baseline demand for their focal retailer relative to competing retailers should make a large share of visits to the focal retailer in the pre-period, and one whose choices are more state-dependent should be more likely to revisit their focal retailer if it was visited in the preceding period.

We use the MatchIt package in R (Ho et al., 2011) to match displaced households to similar non-displaced households within both the treated and control groups. We use one-to-one coarsened exact matching (CEM), which works by placing continuous covariates into bins and retaining only those pairs whose values fall in the same bins. For example, a non-displaced household

<div style="text-align: center;"><div style="text-align: center;">Table A5: Covariate Balance Separately for Full and Matched Sample</div> </div>




<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Variable</td><td style='text-align: center; word-wrap: break-word;'>Displaced</td><td style='text-align: center; word-wrap: break-word;'>Non-displaced</td><td style='text-align: center; word-wrap: break-word;'>Difference</td><td style='text-align: center; word-wrap: break-word;'>p-value</td></tr><tr><td colspan="5">Un-matched</td></tr><tr><td colspan="5">Treated</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Revisit Prob.</td><td style='text-align: center; word-wrap: break-word;'>0.794</td><td style='text-align: center; word-wrap: break-word;'>0.207</td><td style='text-align: center; word-wrap: break-word;'>0.587^{***}</td><td style='text-align: center; word-wrap: break-word;'>0.000</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Trip-share</td><td style='text-align: center; word-wrap: break-word;'>0.307</td><td style='text-align: center; word-wrap: break-word;'>0.077</td><td style='text-align: center; word-wrap: break-word;'>0.230^{***}</td><td style='text-align: center; word-wrap: break-word;'>0.000</td></tr><tr><td colspan="5">Control</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Revisit Prob.</td><td style='text-align: center; word-wrap: break-word;'>0.826</td><td style='text-align: center; word-wrap: break-word;'>0.157</td><td style='text-align: center; word-wrap: break-word;'>0.669^{***}</td><td style='text-align: center; word-wrap: break-word;'>0.000</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Trip-share</td><td style='text-align: center; word-wrap: break-word;'>0.333</td><td style='text-align: center; word-wrap: break-word;'>0.054</td><td style='text-align: center; word-wrap: break-word;'>0.278^{***}</td><td style='text-align: center; word-wrap: break-word;'>0.000</td></tr><tr><td colspan="5">Matched</td></tr><tr><td colspan="5">Treated</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Revisit Prob.</td><td style='text-align: center; word-wrap: break-word;'>0.514</td><td style='text-align: center; word-wrap: break-word;'>0.506</td><td style='text-align: center; word-wrap: break-word;'>0.008</td><td style='text-align: center; word-wrap: break-word;'>0.655</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Trip-share</td><td style='text-align: center; word-wrap: break-word;'>0.155</td><td style='text-align: center; word-wrap: break-word;'>0.153</td><td style='text-align: center; word-wrap: break-word;'>0.002</td><td style='text-align: center; word-wrap: break-word;'>0.808</td></tr><tr><td colspan="5">Control</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Revisit Prob.</td><td style='text-align: center; word-wrap: break-word;'>0.512</td><td style='text-align: center; word-wrap: break-word;'>0.501</td><td style='text-align: center; word-wrap: break-word;'>0.011</td><td style='text-align: center; word-wrap: break-word;'>0.599</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Trip-share</td><td style='text-align: center; word-wrap: break-word;'>0.138</td><td style='text-align: center; word-wrap: break-word;'>0.129</td><td style='text-align: center; word-wrap: break-word;'>0.008</td><td style='text-align: center; word-wrap: break-word;'>0.183</td></tr></table>

Notes: This table shows the average pre-strike revisit probability and trip-share for displaced and non-displaced households within the treated and control group. We present the comparison for the full sample and the set of households matched using CEM.

whose pre-strike S&S trip-share and conditional revisit probability fell into the  $ (0,0.1] $ and  $ (0.5, 0.75] $ bins, respectively, would only be included in the final sample if there was a displaced household whose pre-strike variables fell into the same bins. Households whose bins are only populated by displaced or non-displaced households are dropped, which restricts the analysis to the common support.

After applying CEM, the final sample includes 420 displaced and 420 non-displaced households in the treated group, and 421 displaced and 421 non-displaced households in the control group. Table A5 shows the covariate balance for the full and matched sample. In the full sample, we see significant differences between displaced and non-displaced households, consistent with the patterns plotted in Figure 5. In contrast, after matching, displaced and non-displaced households have statistically similar values for focal retailer trip share and revisit probability.

Figure A2 plots the average number of trips to the focal retailer over time for the matched sample. Similarly to Figure 5, we see that the treated and control households in each group track each other closely in the pre-strike period before diverging after the strike. However, for this matched sample, pre strike levels are also closely aligned across displacement status.

Table A6, Figure A3, and Figure A4 replicate our main analyses using the matched sample.

<div style="text-align: center;"><div style="text-align: center;">Figure A2: Average Trips to the Focal Retailer Over Time, Matched Sample</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//69ac01c2-93e7-4c0c-81bb-07339aaac3c7/markdown_2/imgs/img_in_chart_box_276_289_944_635.jpg?authorization=bce-auth-v1%2FALTAKzReLNvew3ySINYJ0fuAMN%2F2026-04-22T15%3A40%3A25Z%2F-1%2F%2F1e53ff9a4942a2f84c2040e88e167a0f0300ae33ae537e8d2149100a9ddb05f9" alt="Image" width="54%" /></div>


<div style="text-align: center;"><div style="text-align: center;">Notes: This figure reports the average number of focal retailer trips separately for treated and control households using the matched subsample. The left panel presents patterns for non displaced households, and the right panel presents patterns for displaced households.</div> </div>


<div style="text-align: center;"><div style="text-align: center;">Table A6: ATT Estimates on Trips to Focal Retailer, Matched Sample</div> </div>




<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>All (1)</td><td style='text-align: center; word-wrap: break-word;'>Displaced (2)</td><td style='text-align: center; word-wrap: break-word;'>Non-displaced (3)</td></tr><tr><td rowspan="2">S\&amp;S \times post</td><td style='text-align: center; word-wrap: break-word;'>-0.0722 $ ^{*} $</td><td style='text-align: center; word-wrap: break-word;'>-0.1839 $ ^{***} $</td><td style='text-align: center; word-wrap: break-word;'>0.0394</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>(0.0376)</td><td style='text-align: center; word-wrap: break-word;'>(0.0623)</td><td style='text-align: center; word-wrap: break-word;'>(0.0406)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Observations</td><td style='text-align: center; word-wrap: break-word;'>26,250</td><td style='text-align: center; word-wrap: break-word;'>13,125</td><td style='text-align: center; word-wrap: break-word;'>13,125</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>R $ ^{2} $</td><td style='text-align: center; word-wrap: break-word;'>0.29508</td><td style='text-align: center; word-wrap: break-word;'>0.27337</td><td style='text-align: center; word-wrap: break-word;'>0.17773</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Within R $ ^{2} $</td><td style='text-align: center; word-wrap: break-word;'>0.00026</td><td style='text-align: center; word-wrap: break-word;'>0.00117</td><td style='text-align: center; word-wrap: break-word;'>0.00013</td></tr></table>

<div style="text-align: center;"><div style="text-align: center;">Notes: This table shows the results from Equation 11, applied to the matched sample. All regressions include household and period fixed effects. The post indicator captures the twelve eleven day periods after the strike's resolution. Standard errors are clustered at the household level.</div> </div>


<div style="text-align: center;"><div style="text-align: center;">Figure A3: Event Study: ATT of the Strike on Trips to Focal Retailer, Matched Sample</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//69ac01c2-93e7-4c0c-81bb-07339aaac3c7/markdown_3/imgs/img_in_chart_box_178_205_607_628.jpg?authorization=bce-auth-v1%2FALTAKzReLNvew3ySINYJ0fuAMN%2F2026-04-22T15%3A40%3A25Z%2F-1%2F%2F6d7b2e2758b931a032b88a01ee57f3397fecf72f46d48b52f2865d2da4e3dfe4" alt="Image" width="35%" /></div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//69ac01c2-93e7-4c0c-81bb-07339aaac3c7/markdown_3/imgs/img_in_chart_box_612_208_1042_627.jpg?authorization=bce-auth-v1%2FALTAKzReLNvew3ySINYJ0fuAMN%2F2026-04-22T15%3A40%3A25Z%2F-1%2F%2Fa37379e80fb3775526f05814b0a940485c6f6ceea319a33b583e9cbbceeafbac" alt="Image" width="35%" /></div>


<div style="text-align: center;"><div style="text-align: center;">Notes: Event study estimates from Equation 12, applied to the matched sample. Time is indexed in eleven day periods with 0 representing the strike window, and period -9 is the omitted category. All regressions include household and period fixed effects. Standard errors are clustered at the household level.</div> </div>


<div style="text-align: center;"><div style="text-align: center;">Figure A4: The Displacement Effect Over Time, Matched Sample</div> </div>


<div style="text-align: center;"><img src="https://pplines-online.bj.bcebos.com/deploy/official/paddleocr/pp-ocr-vl-15//69ac01c2-93e7-4c0c-81bb-07339aaac3c7/markdown_3/imgs/img_in_chart_box_180_809_1038_1364.jpg?authorization=bce-auth-v1%2FALTAKzReLNvew3ySINYJ0fuAMN%2F2026-04-22T15%3A40%3A25Z%2F-1%2F%2Ff031ba9c24430709de03847fc97902f5690c68bede546bea62dea1115bf0fcf8" alt="Image" width="70%" /></div>


<div style="text-align: center;"><div style="text-align: center;">Notes: The figure plots estimates from equation 10. The coefficients are interpreted as the displacement effect over time. Time is measured in eleven day periods and the omitted category is period t = -9. All regressions include household and period fixed effects. Standard errors are clustered at the household level.</div> </div>


### F Additional tables and figures

<div style="text-align: center;"><div style="text-align: center;">Table A7: Number of Households Across Groups</div> </div>




<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td rowspan="2">Variable</td><td rowspan="2">Level</td><td colspan="2">Control</td><td colspan="2">Treated</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Displaced</td><td style='text-align: center; word-wrap: break-word;'>Non-displaced</td><td style='text-align: center; word-wrap: break-word;'>Displaced</td><td style='text-align: center; word-wrap: break-word;'>Non-displaced</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>New Store</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td rowspan="2">0</td><td style='text-align: center; word-wrap: break-word;'>1</td><td style='text-align: center; word-wrap: break-word;'>2,110</td><td style='text-align: center; word-wrap: break-word;'>2,280</td><td style='text-align: center; word-wrap: break-word;'>1,046</td><td style='text-align: center; word-wrap: break-word;'>1,171</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>1</td><td style='text-align: center; word-wrap: break-word;'>385</td><td style='text-align: center; word-wrap: break-word;'>400</td><td style='text-align: center; word-wrap: break-word;'>179</td><td style='text-align: center; word-wrap: break-word;'>301</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>High Spender</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>0</td><td style='text-align: center; word-wrap: break-word;'>1</td><td style='text-align: center; word-wrap: break-word;'>1,248</td><td style='text-align: center; word-wrap: break-word;'>1,340</td><td style='text-align: center; word-wrap: break-word;'>613</td><td style='text-align: center; word-wrap: break-word;'>736</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>1</td><td style='text-align: center; word-wrap: break-word;'>1</td><td style='text-align: center; word-wrap: break-word;'>1,247</td><td style='text-align: center; word-wrap: break-word;'>1,340</td><td style='text-align: center; word-wrap: break-word;'>612</td><td style='text-align: center; word-wrap: break-word;'>736</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Income</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>high</td><td style='text-align: center; word-wrap: break-word;'>650</td><td style='text-align: center; word-wrap: break-word;'>739</td><td style='text-align: center; word-wrap: break-word;'>322</td><td style='text-align: center; word-wrap: break-word;'>356</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>low</td><td style='text-align: center; word-wrap: break-word;'>475</td><td style='text-align: center; word-wrap: break-word;'>453</td><td style='text-align: center; word-wrap: break-word;'>272</td><td style='text-align: center; word-wrap: break-word;'>330</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>mid</td><td style='text-align: center; word-wrap: break-word;'>1,370</td><td style='text-align: center; word-wrap: break-word;'>1,488</td><td style='text-align: center; word-wrap: break-word;'>631</td><td style='text-align: center; word-wrap: break-word;'>786</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Age</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>65+</td><td style='text-align: center; word-wrap: break-word;'>411</td><td style='text-align: center; word-wrap: break-word;'>446</td><td style='text-align: center; word-wrap: break-word;'>199</td><td style='text-align: center; word-wrap: break-word;'>242</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>21-34</td><td style='text-align: center; word-wrap: break-word;'>212</td><td style='text-align: center; word-wrap: break-word;'>178</td><td style='text-align: center; word-wrap: break-word;'>115</td><td style='text-align: center; word-wrap: break-word;'>89</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>35-44</td><td style='text-align: center; word-wrap: break-word;'>644</td><td style='text-align: center; word-wrap: break-word;'>728</td><td style='text-align: center; word-wrap: break-word;'>326</td><td style='text-align: center; word-wrap: break-word;'>410</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>45-54</td><td style='text-align: center; word-wrap: break-word;'>656</td><td style='text-align: center; word-wrap: break-word;'>744</td><td style='text-align: center; word-wrap: break-word;'>304</td><td style='text-align: center; word-wrap: break-word;'>399</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>55-64</td><td style='text-align: center; word-wrap: break-word;'>572</td><td style='text-align: center; word-wrap: break-word;'>584</td><td style='text-align: center; word-wrap: break-word;'>281</td><td style='text-align: center; word-wrap: break-word;'>332</td><td style='text-align: center; word-wrap: break-word;'></td></tr></table>

Notes: This table shows the number of displaced and non-displaced households within the treated and control group for each variable studied in 5.3.

<div style="text-align: center;"><div style="text-align: center;">Table A9: Variables Used in Prediction Model, Ranked by Mean Decrease in Accuracy</div> </div>




<table border="1" style="margin: auto; word-wrap: break-word;"><tr><td style="text-align: center; word-wrap: break-word;">Var.Description</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Focal retailer trips per period, all past periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Focal retailer trips/Grocery trips, all past periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Focal retailer trips, all past periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Focal retailer trips per period, last three periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Focal retailer trips, last three periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Focal retailer spend/Grocery spend, all past periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Focal retailer expenditure, last three periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Focal retailer expenditure, all past periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Focal retailer trips/Grocery trips, last three periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Focal retailer expenditure, last period</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Grocery/Club/Mass store trips, all past periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Focal retailer trips, last period</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Grocery store trips, all past periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Last focal retailer trip in the last two weeks $ ^{*} $</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Grocery/Club/Mass store expenditure, all past periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Grocery store expenditure, last three periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Grocery store expenditure, all past periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Continuation of Table A9</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Var.Description</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Focal retailer trips made on Saturdays, all past periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Grocery/Club/Mass store trips, last three periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Grocery store trips, last three periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Period relative to the strike</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Periods past</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Focal retailer trips made on Fridays, all past periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Focal retailer trips made on Tuesdays, all past periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Focal retailer trips made on Thursdays, all past periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Focal retailer trips made on Mondays, all past periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Focal retailer trips made on Wednesdays, all past periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Focal retailer trips made on Sundays, all past periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Grocery/Club/Mass store expenditure, last three periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Grocery store expenditure, last period</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Last focal retailer trip in the last week*</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Mass store expenditure, all past periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Grocery/Club/Mass store expenditure, last period</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Mass store trips, all past periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Restaurant expenditure, all past periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Grocery/Club/Mass store trips, last period</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Grocery store trips, last period</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Home-state expenditure, all past periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Restaurant trips, all past periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Dollar store expenditure, all past periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Expenditure on the last focal retailer trip</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Home-state trips, all past periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Restaurant expenditure, last three periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Mass store expenditure, last three periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Dollar store trips, all past periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Club store expenditure, all past periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Club store trips, all past periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Restaurant trips, last three periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Mass store trips, last three periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Mass store expenditure, last period</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Restaurant expenditure, last period</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Home-state expenditure, last three periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Focal retailer trips made on Sundays, last three periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Focal retailer trips made on Saturdays, last three periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Focal retailer trips made on Thursdays, last three periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Dollar store expenditure, last three periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Focal retailer trips made on Fridays, last three periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Focal retailer trips made on Mondays, last three periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Club store expenditure, last three periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">January*</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Focal retailer trips made on Tuesdays, last three periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Focal retailer trips made on Wednesdays, last three periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Restaurant trips, last period</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Home-state trips, last three periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Expenditure on the last Grocery/Club/Mass trip</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Expenditure on the last home-state trip</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Mass store trips, last period</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Specialty Food store expenditure, all past periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Dollar store trips, last three periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">March</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Club store trips, last three periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Home-state expenditure, last period</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Last Grocery/Club/Mass trip in the last week*</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Last produce purchase in the last week*</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Dollar store expenditure, last period</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Club store expenditure, last period</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Specialty Food store trips, all past periods</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Last produce purchase in the last two weeks*</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Home-state trips, last period</td></tr><tr><td style="text-align: center; word-wrap: break-word;">February*</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Last milk purchase in the last two weeks*</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Focal retailer trips made on Sundays, last period</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Last meat purchase in the last two weeks*</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Dollar store trips, last period</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Last home-state trip was to a Grocery store*</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Focal retailer trips made on Saturdays, last period</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Focal retailer trips made on Tuesdays, last period</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Last home-state trip in the last week*</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Club store trips, last period</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Last Grocery/Club/Mass trip was a Grocery trip*</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Last milk purchase in the last week*</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Focal retailer trips made on Thursdays, last period</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Last yogurt purchase in the last two weeks*</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Focal retailer trips made on Mondays, last period</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Home State = PA*</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Last Grocery/Club/Mass trip was a Mass trip*</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Last home-state trip was to a Mass store*</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Focal retailer trips made on Fridays, last period</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Last meat purchase in the last week*</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Last egg purchase in the last two weeks*</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Middle Income*</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Home State = CT*</td></tr><tr><td style="text-align: center; word-wrap: break-word;">High Income*</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Low Income*</td></tr><tr><td style="text-align: center; word-wrap: break-word;">Last home-state trip in the last two weeks*</td></tr></table>








Continuation of Table A9

Var.Description

Focal retailer trips made on Wednesdays, last period
Home State = NY*

Last yogurt purchase in the last week*
Specialty Food store expenditure, last three periods
Age 65+*
Age 35-44*
Household Size = 1*

Last Grocery/Club/Mass trip in the last day*
April*
Home State = MD*
Household Size = 2*

Last focal retailer trip took place outside of the home state*
Last focal retailer trip took place in the home state*
Age 45-54*
Home State = MA*
Household Size = 4*
Household Size = 3*
Last egg purchase in the last week*
Car*
Age 55-64*
December*
Home State = NJ*
Age 25-34*
Last focal retailer trip in the last day*
Last home-state trip was to a Restaurant*
Last home-state trip in the last day*
No car*
Home State = VA*
Last produce purchase in the last day*
Household Size = 5*
Specialty Food store trips, last three periods
November
Last Grocery/Club/Mass trip was a Disount trip*
Home State = RI*
Last Grocery/Club/Mass trip in the last two weeks*
Last home-state trip was to a Dollar store*
Last home-state trip was to a Club store*
Last Grocery/Club/Mass trip was outside of the home state*
Last milk purchase in the last day*
Household Size = 6*
Household Size >= 7*
Last Grocery/Club/Mass trip was in the home state*
Specialty Food store expenditure, last period
Last meat purchase in the last day*

Continuation of Table A9

Var.Description
September
Specialty Food store trips, last period
June*
August*
Friday*
July*
October
May
Sunday
Home State = DE*
Last yogurt purchase in the last day*
Home State = WV*
Wednesday
No response to Car*
Home State = DC*
Last egg purchase in the last day*
Home State = FL*
Monday
Home State = NC*
Home State = TX*
Home State = OH*
Last home-state trip was to a Specialty Food Store store*
Home State = VT*
Home State = MO*
Home State = NV*
Home State = OR*
Home State = UT*
Home State = SD*
Home State = LA*
Home State = KS*
Home State = OK*
Home State = MN*
Home State = MT*
Home State = ME*
Home State = IA*
Home State = HI*
Home State = NE*
Home State = WA*
Home State = WI*
Home State = MI*
Home State = AZ*
Home State = AL*
Home State = KY*
Home State = CO*



<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td colspan="2">Continuation of Table A9</td></tr><tr><td colspan="2">Var.Description</td></tr><tr><td colspan="2">Home State = GA $ ^{*} $</td></tr><tr><td colspan="2">Age 21-24 $ ^{*} $</td></tr><tr><td colspan="2">Home State = MS $ ^{*} $</td></tr><tr><td colspan="2">Home State = IN $ ^{*} $</td></tr><tr><td colspan="2">Home State = TN $ ^{*} $</td></tr><tr><td colspan="2">Home State = NM $ ^{*} $</td></tr><tr><td colspan="2">Home State = IL $ ^{*} $</td></tr><tr><td colspan="2">Home State = SC $ ^{*} $</td></tr><tr><td colspan="2">Home State = CA $ ^{*} $</td></tr><tr><td colspan="2">Home State = NH $ ^{*} $</td></tr><tr><td colspan="2">Thursday</td></tr><tr><td colspan="2">Saturday</td></tr><tr><td colspan="2">Tuesday</td></tr><tr><td colspan="2">End of Table</td></tr></table>

<div style="text-align: center;"><div style="text-align: center;">Table A8: Heterogeneity in Trip Displacement Effects</div> </div>




<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>(1)</td><td style='text-align: center; word-wrap: break-word;'>(2)</td><td style='text-align: center; word-wrap: break-word;'>(3)</td><td style='text-align: center; word-wrap: break-word;'>(4)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>new store \times post</td><td style='text-align: center; word-wrap: break-word;'>0.0210(0.0189)</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>displaced \times post</td><td style='text-align: center; word-wrap: break-word;'>-0.0448*(0.0237)</td><td style='text-align: center; word-wrap: break-word;'>0.0290(0.0286)</td><td style='text-align: center; word-wrap: break-word;'>-0.0316(0.0362)</td><td style='text-align: center; word-wrap: break-word;'>-0.0865*(0.0475)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>S&amp;S \times post</td><td style='text-align: center; word-wrap: break-word;'>$ 0.0435^{***}(0.0167) $</td><td style='text-align: center; word-wrap: break-word;'>$ 0.0837^{***}(0.0189) $</td><td style='text-align: center; word-wrap: break-word;'>0.0276(0.0274)</td><td style='text-align: center; word-wrap: break-word;'>$ 0.1019^{***}(0.0355) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>new store \times displaced \times post</td><td style='text-align: center; word-wrap: break-word;'>0.0032(0.0544)</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>new store \times S&amp;S \times post</td><td style='text-align: center; word-wrap: break-word;'>0.0460(0.0386)</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>displaced \times S&amp;S \times post</td><td style='text-align: center; word-wrap: break-word;'>$ -0.1483^{***}(0.0378) $</td><td style='text-align: center; word-wrap: break-word;'>$ -0.2143^{***}(0.0443) $</td><td style='text-align: center; word-wrap: break-word;'>$ -0.1517^{**}(0.0623) $</td><td style='text-align: center; word-wrap: break-word;'>-0.0079(0.0822)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>new store \times displaced \times S&amp;S \times post</td><td style='text-align: center; word-wrap: break-word;'>$ -0.1980^{**}(0.0843) $</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>high spender \times post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>$ -0.0958^{***}(0.0162) $</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>high spender \times displaced \times post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>$ -0.1104^{***}(0.0425) $</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>high spender \times S&amp;S \times post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>-0.0442(0.0305)</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>high spender \times displaced \times S&amp;S \times post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>-0.0048(0.0674)</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>low income \times post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>0.0005(0.0224)</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>mid income \times post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>-0.0115(0.0180)</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>low income \times displaced \times post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>-0.0960(0.0638)</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>mid income \times displaced \times post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>0.0067(0.0470)</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>low income \times S&amp;S \times post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>-0.0037(0.0441)</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>mid income \times S&amp;S \times post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>0.0517(0.0346)</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>low income \times displaced \times S&amp;S \times post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>0.0662(0.1033)</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>mid income \times displaced \times S&amp;S \times post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>-0.1073(0.0775)</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>age21-34 \times post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>-0.0159(0.0315)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>age35-44 \times post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>-0.0019(0.0229)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>age45-54 \times post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>-0.0248(0.0223)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>age55-64 \times post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>-0.0077(0.0225)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>age21-34 \times displaced \times post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>0.1052(0.1112)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>age35-44 \times displaced \times post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>0.0045(0.0614)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>age45-54 \times displaced \times post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>0.0652(0.0617)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>age55-64 \times displaced \times post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>0.0760(0.0694)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>age21-34 \times S&amp;S \times post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>-0.0531(0.0642)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>age35-44 \times S&amp;S \times post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>$ -0.1072^{**}(0.0452) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>age45-54 \times S&amp;S \times post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>-0.0173(0.0482)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>age55-64 \times S&amp;S \times post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>-0.0452(0.0469)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>age21-34 \times displaced \times S&amp;S \times post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>$ -0.3816^{**}(0.1727) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>age35-44 \times displaced \times S&amp;S \times post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>-0.1601(0.1035)</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>age45-54 \times displaced \times S&amp;S \times post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>$ -0.2584^{**}(0.1034) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>age55-64 \times displaced \times S&amp;S \times post</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>$ -0.2371^{**}(0.1115) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Observations</td><td style='text-align: center; word-wrap: break-word;'>140,595</td><td style='text-align: center; word-wrap: break-word;'>140,595</td><td style='text-align: center; word-wrap: break-word;'>140,595</td><td style='text-align: center; word-wrap: break-word;'>140,595</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>$ R^{2} $</td><td style='text-align: center; word-wrap: break-word;'>0.59609</td><td style='text-align: center; word-wrap: break-word;'>0.59664</td><td style='text-align: center; word-wrap: break-word;'>0.59607</td><td style='text-align: center; word-wrap: break-word;'>0.59621</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Within  $ R^{2} $</td><td style='text-align: center; word-wrap: break-word;'>0.00137</td><td style='text-align: center; word-wrap: break-word;'>0.00273</td><td style='text-align: center; word-wrap: break-word;'>0.00132</td><td style='text-align: center; word-wrap: break-word;'>0.00168</td></tr></table>

Notes: Column 1 shows the results of equation 14, a quadruple-difference specification, with household and period-level fixed effects. Columns 2-4 show the results of analogous specifications with high spender, income, and age indicators, respectively. Standard errors are clustered at the household level.

