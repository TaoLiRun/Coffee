# Reference patterns behind the empirical-paper-writing skill

## Scope

This note records transferable patterns from the local `literature` folder. It is descriptive, not a claim that every paper should imitate one journal's style. The primary empirical references are Gruber (1994), Levine and Hristakeva (2026 draft), and Schaudt (2026 draft). Bordalo et al.'s cognitive theory paper informs only the treatment of conceptual mechanisms.

## Observed architecture

The three applied papers have different vintages and fields but share a recognizable sequence:

- motivate an economically meaningful tension;
- explain a setting that produces useful comparison groups;
- state the identification logic before presenting estimates;
- report main effects in compact exhibits and interpret them in natural units;
- use heterogeneity or channels to interpret the main finding;
- move detailed construction, diagnostics, and additional results to an appendix when space permits.

Approximate main-text lengths recoverable from the Markdown sources are 12,000 words for Gruber excluding references, 14,700 for Levine--Hristakeva, and 19,600 for Schaudt. Their introductions are roughly 2,100--2,300 words in the two recent papers. Abstracts are 163 and 194 words. These observations motivate, but do not mechanically dictate, the ranges in the skill.

## What each reference contributes

### Gruber (1994)

Gruber's introduction moves from policy importance to the economic incidence question, then to the natural experiments, data, successive empirical tests, findings, and roadmap. The paper explains the triple-difference comparison first with groups and jurisdictions, then with regression notation. Its results progress from transparent group means to regression estimates and an alternative individual-cost parameterization. The durable lesson is to let the economic comparison drive the econometrics and to use a second experiment or parameterization as genuine corroboration rather than as a list of minor robustness checks.

### Levine and Hristakeva (2026 draft)

The paper makes an ideal experiment explicit: randomly displace a planned store visit for one period and compare later demand with nondisplaced consumers. It then explains how a strike, control retailers, and a prediction model approximate that experiment. The main DDD is decomposed into baseline-demand and displacement effects, so readers see both components rather than only a triple interaction. A compact main heterogeneity table reports only the mechanism-relevant rows, while the appendix reports complete specifications, classifier prediction error, matching, and parallel-trend diagnostics. This is the strongest local template for presenting a classifier-assisted DDD without hiding its assumptions.

The paper also shows a useful mechanism structure: identify competing sources of state dependence, derive a prediction based on visiting a new store, estimate a higher-order interaction, report the relevant components, and acknowledge that remaining effects can reflect other channels. The general lesson is that mechanism evidence should distinguish interpretations, not simply redescribe the main coefficient.

### Schaudt (2026 draft)

Schaudt separates setting, data, empirical strategy, main results, sensitivity analysis, channels, quantification, and conclusion. The identification section explicitly discusses rollout selection and inference at the treatment level. The results section organizes sensitivities by concrete threats, including few rollout clusters and concurrent interventions. The channels section states the proposed income and migration pathways, introduces a new specification for each, and reports coefficient plots with 95% confidence intervals. The appendix is extensive and ordered around data construction and additional results. The transferable lesson is to connect each robustness or channel test to the threat or prediction it addresses.

### Bordalo et al. (cognitive theory)

The theory paper begins with the cognitive problem, introduces a parsimonious model, derives general predictions, and then applies them across domains. Formal detail and proofs are separated into supplementary material. For applied work, the lesson is not to reproduce the full theory but to state the primitive attentional or categorization change, derive a signed observable prediction, and keep unneeded derivations outside the empirical narrative.

## Synthesis for main text versus appendix

Keep in the main text:

- the economic question and closest counterfactual experiment;
- institutional facts that generate treatment and comparison groups;
- final sample, unit, main outcomes, and consequential restrictions;
- the preferred equation and focal estimand;
- assumptions and the most important diagnostic caveat;
- decomposed main results with magnitudes and uncertainty;
- one discriminating mechanism or heterogeneity analysis;
- one or two robustness checks that materially affect interpretation.

Move to the appendix:

- intermediate sample counts and record-cleaning details;
- full variable dictionaries and classifier diagnostics;
- complete coefficient vectors behind compact main tables;
- inspectable event-study coefficients and confidence intervals;
- common-support, alternate cutoffs, and functional-form checks;
- alternative outcomes and broader sample registries;
- full heterogeneity matrices and formal derivations.

Omit or archive outside the paper:

- robustness checks with no stated threat;
- uninformative subgroup tables;
- stale specifications retained only because they once appeared in a draft;
- unsupported mechanism claims;
- operational detail that cannot change interpretation or replication.

## Important cautions from the comparison

The references are exemplars, not authorities for a paper's facts. Their clustering choices, sample rules, estimands, and terminology cannot be imported into another design without checking assignment and code. Their manuscripts also contain choices that should not be copied automatically, including long discussions and extensive appendices. Use the common principles and calibrate the execution to the paper at hand.
