---
name: empirical-paper-writing
description: Plan, audit, draft, or revise an applied empirical paper into a credible, reader-first manuscript. Use for economics, marketing, finance, management, or policy papers that need a publication-ready title, abstract, introduction, institutional setting, data and sample section, identification strategy, result presentation, mechanism or heterogeneity analysis, robustness design, conclusion, tables, figures, or online appendix. Also use to check that prose, equations, exhibits, inference, and code outputs agree.
---

# Empirical Paper Writing

## Purpose

Turn an empirical analysis into a paper whose argument can be understood on a first read and audited on a second. Optimize jointly for economic importance, identification credibility, transparent uncertainty, and disciplined interpretation. Never improve the story by hiding an inconvenient estimate, changing a sample to obtain significance, or describing a mechanism more strongly than the design identifies it.

Read `references/reference-patterns.md` when calibrating a full manuscript, deciding what belongs in the main text, or explaining why a structural revision is recommended. It records the source basis for this skill without tying the workflow to a particular application.

## Governing Principle

Organize the paper around a short chain:

> question -> setting and variation -> estimand -> assumptions -> evidence -> interpretation -> limits

Every main-text paragraph, equation, table, and figure should advance one link. Put material that verifies, extends, or documents the chain in the appendix. Delete material that does neither.

## Establish the Evidence Ledger First

Before rewriting, create a private ledger of every headline claim. For each claim record:

- outcome and unit;
- sample and observation count;
- treatment, comparison group, and timing;
- estimating equation and fixed effects;
- focal coefficient and its scale;
- standard error, clustering level, confidence interval, and p-value;
- relevant pretrend or randomization diagnostic;
- source table, output file, and generating script;
- allowed interpretation and known limitation.

Treat the maintained code and outputs as authoritative. Reconcile discrepancies before editing prose. Do not copy estimates from an old abstract, slide deck, or prior commit. When a result is conditional on purchase, selected into the estimation sample, exploratory, one-sided, or sensitive to a diagnostic, state that wherever the result first matters.

## Choose a Result Hierarchy

Classify findings before deciding placement:

1. **Primary result:** directly answers the paper's central question under the preferred design.
2. **Secondary result:** important but addresses another margin or requires a stronger caveat.
3. **Mechanism or heterogeneity evidence:** tests a prediction that distinguishes or supports an interpretation.
4. **Robustness:** changes one credible feature of measurement, sample, inference, or specification.
5. **Diagnostic:** probes whether an identifying or measurement assumption is plausible.
6. **Exploration:** discovered after trying alternatives or not disciplined by an ex-ante prediction.

The title and abstract should feature the primary result. The introduction may mention the strongest secondary result and one mechanism result. The main results section should contain the minimum exhibits needed to establish the primary and secondary results. Put complete coefficient vectors, alternative metrics, exhaustive subgroup analyses, and mechanical construction in the appendix unless they materially change the conclusion.

## Length and Space Budget

Use length as a budget, not a target. For a conventional applied paper, aim for roughly 12,000--18,000 main-text words, or about 25--35 journal-formatted pages excluding references and online appendix. A focused field or marketing paper can be shorter if the design and evidence remain complete. A data-intensive paper can be longer only when distinct analyses answer distinct questions.

Allocate approximately:

- abstract: 130--180 words;
- introduction: 1,500--2,500 words, usually 3--5 pages;
- setting and data: 1,500--2,500 words;
- conceptual framework: 800--1,800 words in the main text, with derivations moved to an appendix when they are not needed to understand the estimand;
- empirical strategy: 1,500--2,500 words;
- main results: 2,500--4,500 words;
- mechanism, heterogeneity, or channels: 1,000--2,500 words;
- conclusion: 300--700 words.

These ranges are diagnostics. Do not pad a simple design or compress a complicated estimand until it becomes opaque. As a default, keep the main text below about 35 pages and let the appendix carry reproducibility, full specifications, additional figures, and alternative analyses.

## Title and Abstract

### Title

Prefer 8--15 informative words. Name the treatment or variation and the economic outcome. Avoid a title built around a latent construct the data only proxy. Use a question only if the paper delivers a clear answer.

### Abstract

Use five moves in one paragraph:

1. State the broad problem and why it matters.
2. Identify the setting, data, and quasi-experimental variation.
3. Name the design or estimand in plain language.
4. Report the central estimate with units and enough uncertainty to calibrate it.
5. State the interpretation and its boundary.

Do not list every robustness check. Do not claim a causal mechanism when the evidence is heterogeneity consistent with that mechanism. If a result fails a key diagnostic, either omit it from the abstract or label it descriptive.

## Introduction

Write the introduction so a reader can answer seven questions without reading further:

1. What is the economic question?
2. Why is the answer not obvious or already known?
3. What is the setting and source of variation?
4. What exactly is compared?
5. What assumptions turn that comparison into the stated estimand?
6. What are the principal findings, in magnitudes and with uncertainty?
7. What is learned beyond the closest paper?

Use this sequence:

- **Problem and tension:** open with behavior, policy, or market stakes, then state the unresolved tension.
- **Ideal experiment and actual design:** explain the comparison intuitively before naming every interaction.
- **Data and setting:** give scale only when it helps establish scope, measurement, or credibility.
- **Results:** devote one paragraph to each main result. Report effect, uncertainty, scale, and diagnostic caveat together.
- **Interpretation:** state the favored mechanism as an interpretation unless directly identified; preview the discriminating evidence.
- **Contributions:** compare to the closest papers by question, variation, outcome, or method. State the incremental value rather than inventorying literatures.
- **Roadmap:** include only when the section sequence is not already obvious.

Do not save identification caveats for the appendix. Do not use a literature review as the opening. Do not describe an insignificant component as an effect simply because a difference between components is significant.

## Conceptual Framework and Predictions

Use a conceptual section only if it organizes the estimand, signs a non-obvious prediction, or distinguishes mechanisms. Start with primitives and the decision margin, not citations.

Follow this order:

1. Define the baseline choice problem.
2. Explain what the treatment changes and what remains fixed.
3. State the behavioral channel in one causal chain.
4. Derive two or three empirically distinguishable predictions.
5. Map each prediction to a later outcome or interaction.
6. State observationally equivalent channels and what the paper cannot distinguish.

Use a formal model only when equations provide leverage that prose cannot. Keep the main-text model to the minimum notation needed for predictions. Put proofs, alternate cases, and algebra in an appendix. Never write that a psychological process “is the mechanism” when it is unobserved; write that evidence is “consistent with,” “supports,” or “is difficult to reconcile with” the proposed channel.

## Setting, Data, and Sample Construction

Tell the reader what happened before describing every variable. Include in the main text:

- institutional facts needed to understand treatment, timing, compliance, and likely confounds;
- data source, coverage dates, unit of observation, and what behavior is observed or missed;
- treatment and control construction;
- final sample size and economically meaningful restrictions;
- primary outcome definitions and whether they are conditional;
- a compact descriptive table or figure that reveals identifying variation.

For each major screen, give both the rule and the rationale. Explain what failure mode it prevents. Put record cleaning, intermediate counts, coding taxonomies, long variable dictionaries, and edge cases in the appendix. Replace a dense sample-flow table with readable prose when the sequence and reasons matter more than the arithmetic.

Distinguish carefully among store-level assignment, customer-level measurement, market-level purchase histories, and chain-wide outcomes. State geographic or platform coverage once so readers understand the estimand; do not repeatedly advertise a measurement limitation.

## Identification and Estimation

Explain the design twice:

- first as a counterfactual comparison in plain language;
- then as an equation with notation that matches the prose and tables.

For every preferred specification, state:

- unit of observation and panel structure;
- treatment, post period, omitted category, and comparison group;
- the focal coefficient and what it is not;
- fixed effects and which variation remains after absorption;
- weighting implicit in pooling or stacking;
- clustering level and why it matches treatment assignment or residual dependence;
- identifying assumptions;
- main threats and the evidence brought to bear on them.

For differences-in-differences or triple differences, separate the group-specific effects from their difference. A DDD can be significant even when neither component is individually significant; describe this correctly. State explicitly whether events overlap, whether units recur across events, whether treated units can be controls, and whether event sizes implicitly weight the pooled coefficient when those features apply.

## Presenting Main Results

Build each result subsection in four moves:

1. Restate the estimand and expected sign.
2. Point to one exhibit and identify the focal row, column, or coefficient.
3. Translate the estimate into natural units and relative magnitude.
4. Discuss uncertainty, assumptions, and economic interpretation.

The preferred main table should generally:

- fit on one page;
- show the focal coefficient prominently, using boldface sparingly;
- show economically important component effects when needed to interpret a difference;
- report standard errors in parentheses and state clustering in the notes;
- report observations, fixed effects, and the outcome mean;
- define the sample, unit, outcome, and omitted category in self-contained notes;
- use consistent decimals and significance symbols without making stars the argument.

Report the complete specification in the appendix. A reader should be able to connect the compact main table to the full coefficient vector. Lead with magnitudes and uncertainty, not “significant” or “insignificant.” If pretrends or common support weaken a result, say so in the same subsection.

Use figures when dynamics, distributions, overlap, or nonlinear patterns are the evidence. Plot coefficients with 95% confidence intervals and an explicit omitted period. Do not replace inspectable pretrend coefficients with a table of joint p-values alone.

## Mechanism, Heterogeneity, and Channels

Introduce mechanism evidence as a sequence:

> proposed channel -> discriminating prediction -> measure -> specification -> estimate -> alternative explanation

Before the regression, show the distribution and support of the heterogeneity variable, especially if it is noisy, bounded, selected, or constructed from a short history. Explain why the split, interaction, or proxy corresponds to the theory. Prefer a continuous interaction when arbitrary cutoffs discard information; use extreme groups only when theory predicts nonlinearity and support remains adequate.

Include the full lower-order interaction hierarchy. If the focal trait is mechanically related to exposure or measurement precision, control flexibly for that source and show a model-free diagnostic that motivates the adjustment. Report a version without the adjustment in the appendix when it aids interpretation.

Use one-sided inference only when the directional hypothesis was specified by the conceptual framework before inspecting the estimate, and label it prominently. Otherwise use two-sided inference. Disclose specification search and call selected heterogeneity evidence exploratory.

A mechanism result belongs in the main text when it tests a sharp, pre-motivated prediction and materially changes interpretation. A collection of weak or ex-post subgroup results belongs in the appendix or a research archive.

## Robustness and Diagnostics

Organize robustness checks by the threat they address:

- alternative outcome definition -> measurement validity;
- alternate treatment intensity or cutoff -> functional form and classification;
- sample expansion or restriction -> external validity and selection;
- event-study path -> dynamics and parallel trends;
- common support or matching -> overlap;
- alternative fixed effects -> omitted aggregate shocks;
- inference variants -> dependence and few-cluster sensitivity;
- leave-one-event-out or equal-event weighting -> event leverage.

Do not present a “robustness dump.” State the threat, the change, and whether the conclusion survives. Keep the most decision-relevant check in the main text and move the full matrix to the appendix. Archive exploratory analyses with exact sample definitions and generating code even when they are not shown in the paper.

## Appendix Architecture

Order the appendix so it can be audited:

1. data construction and variable definitions;
2. classifier, treatment, or measurement validation;
3. identification diagnostics and event studies;
4. complete preferred specifications;
5. alternative outcomes and robustness checks;
6. mechanism or heterogeneity details;
7. sample sensitivity and supplementary exhibits;
8. model derivations or proofs, if any.

Open each appendix subsection with one sentence explaining why the material is there and how it relates to the main text. Give every table and figure a self-contained note. Do not refer to an appendix result that is not actually displayed.

## Conclusion

Use three or four paragraphs:

1. Restate the question, design, and principal result without replaying the introduction.
2. State the most credible interpretation and the central limitation.
3. Explain the economic or managerial implication at the level supported by the estimand.
4. Identify one valuable next step if it follows from a real limitation.

Do not introduce new empirical results. Avoid advice that assumes away selection, equilibrium responses, generalizability, or an unmeasured mechanism. Prefer “firms may wish to monitor” to “firms should” when the design does not estimate a policy rule.

## Consistency and Publication Audit

Before compiling, run four passes.

### Evidence pass

- Match every number in the title page, abstract, introduction, results, conclusion, tables, and notes to the ledger.
- Confirm scales: proportion, percentage point, percent change, day, window, order, or customer.
- Confirm standard errors, p-values, clustering, observation counts, and sample labels.

### Language pass

- Use one term for each construct.
- Reserve causal verbs for identified estimands.
- Distinguish prediction from realized purchase, exposure from interruption, and conditional choice from unconditional demand.
- Replace “proves” and “the mechanism” with calibrated language when alternatives remain.

### Exhibit pass

- Ensure every exhibit is cited in order and discussed.
- Make notes self-contained.
- Bold only focal estimands.
- Confirm figures show uncertainty and legible labels.
- Remove tables or figures that merely repeat prose.

### Source and build pass

- Remove hidden obsolete text, stale comments, duplicate labels, and unused inputs.
- Compile from a clean build at least twice so references settle.
- Inspect warnings for undefined citations, references, duplicate labels, overfull boxes, and missing files.
- Check the PDF visually at the title, every main exhibit, the appendix transition, and the bibliography.
- Record the final page and word counts and update the research audit or changelog.

## Final Quality Test

A publication-ready draft should pass these questions:

- Can a reader state the estimand after the introduction?
- Can the main empirical claim be verified from one table or figure?
- Are the assumptions stated before the result is interpreted causally?
- Is every uncertainty measure based on the maintained inference procedure?
- Is the mechanism labeled according to what is observed?
- Does the appendix reveal rather than bury diagnostics?
- Do title, abstract, introduction, results, and conclusion tell the same quantitative story?
- Could another researcher trace each headline number to an output and script?

If any answer is no, the draft is not ready to circulate as final.
