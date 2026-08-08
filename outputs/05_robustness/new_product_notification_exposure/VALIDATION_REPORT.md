# Validation report: new-product notification mechanism

## Overall assessment: Ready to share with caveats

The required first-stage has the wrong sign for the alternative explanation. The high-minus-low treated-control change in unique new-product notification campaigns is **+0.0041 per consumer-day during closure** (95% CI 0.0019 to 0.0064; restricted wild-cluster p=0.0032) and **+0.0017 after reopening** (95% CI 0.0001 to 0.0032; restricted wild-cluster p=0.0469). A negative coefficient is required for differential new-product notification exposure to explain the negative novelty DDD.

## What the levels show

Low-intention treated consumers receive more new-product notifications in absolute terms in every phase, as expected from inactivity-triggered targeting. During closure, the rates are 0.0307 per day for low-intention and 0.0115 for high-intention consumers; after reopening, they are 0.0250 and 0.0113. But the pre-period rates are already 0.0247 and 0.0058. The high group therefore experiences the larger relative increase after accounting for pre-period levels and the matched controls.

## Validation checks

All 9 programmed checks pass. The analysis uses 40,148 consumers, 18 closures and 361,332 member-period observations including the closure period. The raw scan covers 56,724,521 records and maps 912,911 to the analysis windows. All 125,918 trigger-tag-3 records are unique at the member-policy-date level, so raw and deduplicated estimates coincide. The primary event-study leads do not reject a joint pretrend (p=0.500).

## Caveats

- The records establish targeting entries, not verified delivery, impression, opening or reading.
- The interpretation assumes that new-product notifications weakly increase awareness or exploration. If they reduce novelty, the sign argument reverses, but that would conflict with the proposed notification mechanism.
- The test rules out differential recorded new-product notifications as an explanation; it does not cover familiar-product messages or unobserved in-app rankings.
- With 18 closure clusters, the primary inference uses both CRV1 intervals and restricted wild-cluster p-values.
