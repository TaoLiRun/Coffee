# Econometric Specification for Temporary Coffee Store Closures

## 1. Setup and notation

We study temporary closures of stores in a large coffee chain. The unit of analysis is a member-closure event.

- Let $e = 1, ..., E$ index closure events.
- Let $i$ index members assigned to event $e$.
- Let $L_e$ denote the closure duration of event $e$ in days.
- Let $t \in \{-H, ..., -1, 0, 1, ..., H\}$ denote relative event time, where each period is a bin of length $L_e$ days and $t = 0$ is the closure window itself.
- In the main implementation, $H = 4$.

For each member-event pair $(i,e)$:

- $T_{ie} = 1$ if member $i$ belongs to the treatment group for event $e$, meaning the member's preferred pre-closure store is the store that closes.
- $T_{ie} = 0$ if member $i$ belongs to the matched control group, meaning the member's preferred pre-closure store remains open.
- $D_{ie} = 1$ if member $i$ is classified ex ante as a blocked buyer for event $e$, meaning the model predicts that this member would have made a purchase during the closure window if access had not been disrupted.
- $D_{ie} = 0$ otherwise.
- $Post_t = 1[t > 0]$.

The blocked-buyer classifier is trained only on pre-closure information and then applied ex ante. Its role is to separate members whose purchase routine was plausibly interrupted from those whose purchase timing would not have put them in the closure window anyway.

The panel excludes $t = 0$ from the regression sample. Identification comes from comparing pre-closure periods to post-reopening periods.

## 2. Outcomes

We analyze two post-closure behaviors.

### 2.1 Purchase frequency

Let $Y^P_{iet}$ be member $i$'s purchase frequency at event time $t$ for event $e$, measured as purchase days per calendar day within the event-length bin:

$Y^P_{iet} = purchase\_days_{iet} / L_e$.

This is the `n_purchases` outcome in the codebase.

### 2.2 Novelty-seeking

Let $Y^V_{iet}$ be member $i$'s novelty-seeking outcome in event period $t$ for event $e$. In the distinct-product version used in the main writeup,

$Y^V_{iet} = new\_products_{iet} / total\_products_{iet}$,

where:

- $total\_products_{iet}$ is the number of distinct products bought by member $i$ in that window.
- $new\_products_{iet}$ is the number of those products whose first-ever purchase by member $i$ occurs during that window.

Members with no purchases in a window have missing $Y^V_{iet}$ for that period.

## 3. Conceptual framework

### 3.1 Purchase decision

The closure can matter for future chain purchases through two conceptually distinct channels:

1. A baseline-demand channel.
2. A blocked-purchase channel operating through the interruption of a planned purchase.

Let $C_{iet} \in \{0,1\}$ indicate whether member $i$ makes at least one purchase from the coffee chain in period $t$ of event $e$. Consider the latent net utility of buying from the chain rather than using an outside option:

$U^P_{iet} = \alpha^P_{et} + \mu^P_{ie} + \gamma^P C_{ie,t-1} + \epsilon^P_{iet}$.

Here:

- $\alpha^P_{et}$ is baseline demand for the chain in event time $t$.
- $\mu^P_{ie}$ is time-invariant member-event heterogeneity.
- $\gamma^P$ captures state dependence in chain purchasing.
- $\epsilon^P_{iet}$ is an idiosyncratic shock.

The member buys from the chain when $U^P_{iet} \geq 0$.

The key object is $\gamma^P$. When $\gamma^P > 0$, recent purchasing increases the chance of purchasing again. In the coffee setting this can reflect habit, convenience, app familiarity, commute routing, stored payment credentials, coupon usage, or simply repetition of a morning routine.

### 3.2 How a closure enters the purchase model

The closure affects future purchases in two ways.

First, it may change baseline demand $\alpha^P_{et}$ after reopening. This is the baseline-demand channel. In the coffee context, this can come from:

- members discovering substitutes during the closure;
- the chain using promotions or coupons after reopening;
- updated beliefs about reliability or convenience;
- persistent changes in commute patterns or order timing.

Second, for members who would have purchased during the closure window, the closure can interrupt the observed purchase path $C_{ie0}$. This is the blocked-purchase channel. Even if the store later reopens, the member's recent purchase history is different, and with $\gamma^P \neq 0$ that difference carries forward.

For a blocked treated member, the closure creates an access shock at $t = 0$. In the stark case where the member would have bought from the chain absent closure but does not do so when the preferred store is closed, we have:

- $C_{ie0}(0) = 1$ without the closure,
- $C_{ie0}(1) = 0$ with the closure.

Then at $t = 1$, holding baseline demand fixed, the deterministic part of utility falls by $\gamma^P$. If the member substitutes to another store of the same chain during the closure, this gap is smaller. Therefore, the blocked-purchase effect in this project should be interpreted as the average post-reopening consequence of having a purchase opportunity disrupted, not necessarily as the effect of literally making zero chain purchases during the closure.

### 3.3 Novelty decision

Conditional on purchasing, the closure may also affect what the member buys. Let $N_{iet} \in \{0,1\}$ indicate whether the member chooses a new-to-them product in period $t$ of event $e$. A simple latent-index representation is:

$U^V_{iet} = \alpha^V_{et} + \mu^V_{ie} + \gamma^V H_{ie,t-1} + \xi G_{ie} + \eta M_{ie} + \epsilon^V_{iet}$,

where:

- $\alpha^V_{et}$ is the baseline tendency to explore.
- $\mu^V_{ie}$ is time-invariant heterogeneity in experimentation.
- $H_{ie,t-1}$ is a summary of recent product-choice history.
- $G_{ie}$ captures an unfulfilled blocked purchase goal created by the closure.
- $M_{ie}$ captures missed exposure to menu evolution during the closure window.

This representation highlights two coffee-specific novelty channels.

First, a blocked purchase can create a focused rebound. After reopening, some blocked buyers may return with a narrow goal of completing the specific familiar purchase they missed. This predicts lower novelty after reopening for blocked treated members.

Second, members whose preferred store was closed may miss exposure to newly introduced items during the closure window. If matched control stores remained active and displayed new products, blocked treated members return with less recent assortment exposure, which can also reduce novelty.

At the same time, closures can shift baseline exploration even for non-blocked members. A routine disruption can move some members away from autopilot and toward broader menu search after reopening.

## 4. Mechanisms of interest

For both outcomes, we separate two reduced-form mechanisms.

### 4.1 Blocked-purchase effect

$D$ is the additional post-reopening effect caused by having a purchase due during the closure window and therefore having one's purchase path disrupted.

For purchase frequency, $D$ captures whether a blocked purchase weakens later chain purchasing, leaves it unchanged, or creates a rebound.

For novelty-seeking, $D$ captures whether a blocked purchase pushes members toward familiar items or toward experimentation after reopening, potentially through focused goal completion or missed exposure to newly introduced products.

### 4.2 Baseline-demand effect

$B$ is any post-reopening effect that hits treated members regardless of whether they had a purchase due during the closure window.

In the coffee setting this can include:

- store-reopening promotions;
- updated convenience or reliability beliefs;
- alternative-store discovery during the closure;
- routine re-optimization after access is disturbed.

The empirical goal is to distinguish $D$ from $B$.

## 5. Difference-in-differences logic

There are four relevant groups:

- treated, non-blocked;
- treated, blocked;
- control, non-blocked;
- control, blocked.

Let $\Delta Y_{g}$ denote the pre/post change in an outcome for group $g$.

For non-blocked treated members:

$\Delta Y_{T,0} = B_{T,0} + Trend_{T,0}$.

For blocked treated members:

$\Delta Y_{T,1} = D_{T,1} + B_{T,1} + Trend_{T,1}$.

For the two control groups:

- $\Delta Y_{C,0} = Trend_{C,0}$,
- $\Delta Y_{C,1} = Trend_{C,1}$.

The first DiD among non-blocked members is:

$\Delta Y_{T,0} - \Delta Y_{C,0} = B_{T,0} + Trend_{T,0} - Trend_{C,0}$.

The first DiD among blocked members is:

$\Delta Y_{T,1} - \Delta Y_{C,1} = D_{T,1} + B_{T,1} + Trend_{T,1} - Trend_{C,1}$.

The DDD estimand is:

$[(\Delta Y_{T,1} - \Delta Y_{C,1}) - (\Delta Y_{T,0} - \Delta Y_{C,0})]$

$= D_{T,1} + (B_{T,1} - B_{T,0}) + [(Trend_{T,1} - Trend_{C,1}) - (Trend_{T,0} - Trend_{C,0})]$.

Under the identification assumptions below, this isolates the blocked-purchase effect $D$.

## 6. Main estimating equation

The baseline pooled DDD specification is:

```math
Y_{iet}
= \delta^B (Post_t \times T_{ie})
+ \beta (Post_t \times D_{ie})
+ \delta^D (Post_t \times T_{ie} \times D_{ie})
+ \phi_{ie} + \omega_t + \gamma_m + \varepsilon_{iet}.
```

where:

- $\phi_{ie}$ is a member-closure fixed effect;
- $\omega_t$ is a relative-period fixed effect;
- $\gamma_m$ is a calendar-month fixed effect.

Standard errors are clustered at the member level.

The role of each coefficient is:

- $\delta^B$: post-reopening treatment effect for non-blocked members.
- $\beta$: common post shift for blocked members in both treatment and control groups.
- $\delta^D$: additional post-reopening effect for blocked treated members relative to the other three groups.

This last coefficient is the main estimand.

## 7. Interpretation by outcome

### 7.1 Purchase frequency outcome

When $Y_{iet} = Y^P_{iet}$:

- $\delta^B$ measures whether treatment members without a purchase due change their post-reopening purchase rate relative to matched controls.
- $\beta$ captures the fact that blocked members are higher-intensity purchasers even without a closure effect, so they can mechanically show stronger mean reversion.
- $\delta^D < 0$ would be evidence that missing a purchase weakens later purchasing.
- $\delta^D = 0$ would mean no detectable blocked-purchase effect on later purchase frequency.
- $\delta^D > 0$ would mean blocked treated members rebound more strongly than comparable blocked controls.

### 7.2 Novelty-seeking outcome

When $Y_{iet} = Y^V_{iet}$:

- $\delta^B$ measures whether treated non-blocked members become more or less exploratory after reopening.
- $\beta$ captures level differences in experimentation for blocked members independent of treatment.
- $\delta^D < 0$ means blocked treated members shift toward familiar products after reopening.
- $\delta^D > 0$ means blocked treated members become more exploratory after reopening.

## 8. Continuous-score robustness specification

Because blocked status is predicted rather than observed, a useful robustness specification replaces the binary blocked indicator with a centered ex ante blocked probability $\tilde{p}_{ie}$:

```math
Y_{iet}
= \delta_S^B (Post_t \times T_{ie})
+ \beta_S (Post_t \times \tilde{p}_{ie})
+ \delta_S^D (Post_t \times T_{ie} \times \tilde{p}_{ie})
+ \phi_{ie} + \omega_t + \gamma_m + \varepsilon_{iet}.
```

Interpretation:

- $\delta_S^B$ is the treatment effect at average blocked propensity.
- $\delta_S^D$ is the marginal change in the treatment effect as blocked propensity rises.

If the conceptual story is correct, the binary and continuous-score specifications should point in the same qualitative direction.

## 9. Event-study specification

To trace dynamics, replace the single post indicator with relative-time interactions and omit $t = -1$ as the reference period:

```math
Y_{iet}
= \sum_{l \in \mathcal{T}, l \neq -1} \delta^B_l 1[t=l] T_{ie}
+ \sum_{l \in \mathcal{T}, l \neq -1} \beta_l 1[t=l] D_{ie}
+ \sum_{l \in \mathcal{T}, l \neq -1} \delta^D_l 1[t=l] T_{ie} D_{ie}
+ \phi_{ie} + \omega_t + \gamma_m + \varepsilon_{iet},
```

where $\mathcal{T} = \{-H, ..., -2, 1, ..., H\}$ because the closure period $t = 0$ is omitted from estimation.

The event-study serves two purposes:

- check for pre-trends through the coefficients with $l < 0$;
- show whether post-reopening effects are immediate, persistent, decaying, or reversing over time.

## 10. A simple data-generating process

The DGP below is a stylized way to rationalize the empirical model.

### 10.1 Purchase process

For each member-event pair $(i,e)$ and period $t$:

1. Draw a baseline purchase component $\alpha^P_{et}$.
2. For treated events, allow a post-reopening shock $B^P_t$ to baseline demand. This shock may be positive or negative and may decay over time.
3. Let recent chain purchasing enter utility through $\gamma^P C_{ie,t-1}$.
4. In the closure window $t = 0$, impose an access disruption for treated members.
5. For blocked treated members, the closure changes the realized purchase path in $t = 0$, which then feeds into later periods through $\gamma^P$.
6. Convert latent utility into purchase incidence, then aggregate within each event-length bin to obtain `n_purchases`.

This DGP implies that a temporary closure can create persistent post-reopening effects even when the direct closure shock lasts only one period.

### 10.2 Novelty process

Conditional on purchase:

1. Draw a baseline exploration component $\alpha^V_{et}$.
2. Allow a post-reopening exploration shock $B^V_t$ for treated members.
3. Add a blocked-goal term that is active mainly for blocked treated members immediately after reopening.
4. Add a missed-exposure term when the member was absent during a period in which the menu evolved.
5. Convert latent exploration utility into the probability of buying new products, then aggregate to the period-level novelty ratio.

This DGP can generate a pattern in which purchase frequency fully recovers while novelty remains lower for blocked treated members.

## 11. Identification assumptions

The DDD interpretation of $\delta^D$ relies on the following assumptions.

### A1. Parallel trends across treatment and control

Absent the closure, treated and matched control members would have evolved similarly within each blocked-status group, or at least the treatment-control trend gap would have been the same for blocked and non-blocked members.

Formally, the DDD only needs:

$Trend_{T,1} - Trend_{C,1} = Trend_{T,0} - Trend_{C,0}$.

This is the key parallel-trends condition.

### A2. Equal baseline effect across blocked and non-blocked treated members

Any closure-induced shift in baseline demand that is unrelated to the interruption of a due purchase affects blocked and non-blocked treated members similarly:

$B_{T,1} = B_{T,0}$.

If this fails, $\delta^D$ mixes the blocked-purchase effect with heterogeneous baseline effects.

### A3. Ex ante blocked classification

Blocked status must be determined using only pre-closure information. It should proxy for whether a purchase was due during the closure window, not encode post-treatment behavior.

### A4. Stable measurement across groups and periods

Outcome construction, event-time binning, and treatment/control assignment must be comparable across groups. This matters because closure durations vary across events and the estimand is expressed per event-length bin.

### A5. Limited interference

One member-event's treatment status should not substantially alter another member-event's counterfactual outcome after conditioning on the design. In practice, this means any spillovers from store traffic reallocation or local demand congestion should be small enough that matched controls remain a valid counterfactual.

## 12. Main threats to interpretation

Three threats are especially important in this setting.

First, blocked and non-blocked treated members may respond differently to the closure even absent purchase interruption. For example, frequent buyers may be more promotion-sensitive, more exposed to app messages, or more likely to learn about alternative stores. That would violate A2.

Second, blocked status is predicted with error. Misclassification attenuates the binary DDD coefficient toward zero and makes the score-based specification especially useful as a robustness check.

Third, treated members can substitute to another store in the same chain during the closure. This does not invalidate the design, but it means the blocked-purchase effect is an average reduced-form effect of disrupted access, not a literal no-purchase effect for every blocked treated member.

## 13. Economic interpretation

The econometric design answers two distinct questions.

First, does a temporary closure create a general post-reopening shift in chain demand or menu exploration even for members who did not have a purchase due during the closure? That is $\delta^B$.

Second, among members whose purchase timing made them exposed to the closure, does the disrupted purchase path have an additional persistent effect after reopening? That is $\delta^D$.

For purchase frequency, $\delta^D$ is the reduced-form measure of whether a blocked coffee purchase breaks the buying habit, leaves it intact, or induces a rebound.

For novelty-seeking, $\delta^D$ is the reduced-form measure of whether a blocked coffee purchase narrows members back toward familiar items or instead encourages experimentation after the store reopens.
