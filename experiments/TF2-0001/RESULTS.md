# TF2-0001 result

TF2-0001 is scientifically complete. It is a controlled discovery/falsification experiment,
not a proof of any all-tree theorem.

## Provenance and frozen split

Scientific source commit: `d091d88889fa72322bfc49a5531bc30b1f31b049`  
Successful GitHub Actions run: `36888114138`  
TxGraffiti: `0.4.1`, upstream revision `e37126da53b84150d142a5d61202b61f78521fcc`

Discovery corpus: all 200 unlabeled trees of orders 2-10.  
Discovery SHA-256: `40bc528cd8b035854de816a1fbd37f1c6d688b2b1686d006387fb16dc8f5c4a8`

Burned order: 11. It was not used for TF2 generation, tuning, holdout testing, or
adversarial selection.

Untouched holdout: all 551 unlabeled trees of order 12,
generated only after TxGraffiti generation and exact first-stage discovery triage.  
Holdout SHA-256: `ea9f5d200ec503090499b4744338a5e39a37b7412d21ed5f6f876e2129be9433`

Frozen adversarial corpus: 26 trees from exactly the
pre-frozen path, star, spider, caterpillar, balanced-binary-tree, double-star, and broom
instances.  
Adversarial SHA-256: `dea3af9c495cc79da46b7ed3797276caae22495bc86d5000ddea3605a07bcb8a`

## TxGraffiti pipeline

The corrected TreeForge adapter maps the frozen empty hypothesis payload to upstream
`None`, the always-true base predicate. The methods remained `convex_hull` and
`ratios`; the heuristics remained Morgan and Dalmatian; the post-processors remained
duplicate removal and touch-count sorting.

Single-pass stage counts:

- raw generator output: 23268
- after Morgan: 23268
- after Dalmatian: 10753
- after duplicate removal: 998
- after touch-count sort: 998
- strengthened equalities added by upstream discover: 0
- final raw statements entering TreeForge triage: 998

The first attempted live execution, Actions run `36875119955`, was provisionally treated as a
pre-valid-output performance failure after it remained inside the scientific step beyond the expected
runtime envelope and PR #5 was closed before its artifact was available. The run later completed and
uploaded an artifact whose 998 final statements and scientific outcomes match the repaired run after
removing source-commit provenance labels. It is preserved as process history rather than used as the
authoritative TF2 record. A discovery-only probe in run
`36887027180` found 42,068 convex-hull facets while Qhull itself took about 0.48 seconds.
TreeForge therefore replaced repeated always-true Morgan/Dalmatian state reconstruction by
an output-equivalent cached adapter path, verified against the pinned live upstream package.
The frozen scientific specification was not changed. Clean repaired preflight run
`36887887082` passed before the successful scientific run above.

## Candidate lifecycle

TxGraffiti produced 998 final statements, allocated permanently
as `TF-000002` through `TF-000999`. Exact discovery-side reevaluation admitted all
998 to `CONJECTURED`; none was classified
away at this first stage.

The untouched order-12 holdout falsified 924 candidates
and left 74 finite survivors. Every survivor was tested on
the frozen adversarial corpus. None failed there, so all 74
reached `ADVERSARIAL_PASSED` before mathematical interpretation.

Interpretation then classified `TF-000002` as `KNOWN_RESULT` (the standard
`gamma(T) <= nu(T)` relation), and `TF-000010` plus `TF-000996` as elementary
`TRIVIAL` consequences of leaf/support/degree structure. Seventy high-dimensional
convex-hull facets remain finite `ADVERSARIAL_PASSED` survivors with no identified
structural mechanism strong enough for promotion.

`TF-000998`, `gamma(T) >= 3 nu(T)/5`, initially reached
`MATHEMATICALLY_INTERESTING` because it is a simple two-invariant bound, was sharp on the
order-10 discovery spider with arms `[1,4,4]`, and survived every frozen finite gate. A
bounded candidate-specific prior-art search found no exact match in the searched sources,
but this was not treated as novelty. Deeper structural interpretation then produced an exact
counterexample: the six-arm spider with arms `[4,4,4,4,4,4]` has order 25,
`gamma=7`, and `nu=12`, so `7 < 3*12/5`. It is therefore permanently
`FALSIFIED`.

Final interpreted states are: {'ADVERSARIAL_PASSED': 70, 'FALSIFIED': 925, 'KNOWN_RESULT': 1, 'TRIVIAL': 2}. One candidate reached the
mathematical-interest gate during its lineage, and it was later falsified. No candidate is a
`GRADUATION_CANDIDATE`, no theorem is claimed, and no novelty claim is made.

## Prior-art boundary

A bounded prior-art search was performed only for `TF-000998` after its temporary
`MATHEMATICALLY_INTERESTING` promotion. Exact search terms, sources, close results, and
uncertainty are preserved in that candidate lineage and in
`interpretation_summary.json`. No other candidate triggered literature search.

## Reproducibility

The complete raw TxGraffiti output is committed as `raw_txgraffiti_output.json`, with
structured relation and touch-count metadata. The central append-only candidate registry
contains every generated lineage and every later interpretation revision. Discovery and
holdout row files are deterministic and are not committed; their exact counts and hashes are
recorded above and in `manifest.json`.
