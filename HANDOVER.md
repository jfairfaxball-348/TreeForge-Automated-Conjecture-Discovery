# TF4 handover

TF4 completed the exposed-data diagnosis of TF3's interpretable-but-zero-interest result and froze
`TF4-0001`. No TF4 scientific run has been executed. TF0-TF3 diagnostics, freezes, candidate
lineages, and scientific results remain preserved append-only.

## Verified starting state and authoritative history

Verified starting `main` HEAD for TF4:
`fe2ce0cf6a0a7a749ffe8b9425a0508646cf1ad7`.

The existing post-TF3 main validation run `36917219570` was rechecked: installation, unit tests,
compileall, Ruff, deterministic calibration, and live pinned TxGraffiti compatibility were green.

TF2 authoritative scientific source:
`d091d88889fa72322bfc49a5531bc30b1f31b049`.  
TF2 authoritative scientific run: `36888114138`.

Corrected TF3 diagnostic run: `36907058956`.

TF3 authoritative scientific source:
`e23b44d24a7b87d6f67aa18749059540934b2767`.  
TF3 authoritative scientific run: `36914647703`.

The exact final merged `main` HEAD and final post-merge CI run are reported in the session
closeout because a Git commit cannot contain its own resulting SHA without changing that SHA.

## Reproduced TF3 record

TF3 pipeline counts remain:

- raw ratios generator output: 14
- after Morgan: 14
- after Dalmatian: 12
- after duplicate removal: 12
- final: 12

TF3 permanent IDs: `TF-001000` through `TF-001011`.

Candidate-batch SHA-256:
`85669d95fb7199b720bfe488c606055dd5f38a5af157c1ed2bdb5f98710344c6`.

Fresh TF3 order-13 holdout:

- 1,301 trees
- SHA-256 `5b02d81644415adc2df55d0a2ec3694125ef328cb1a0c4a2eeb733efaecef7e9`
- 12 tested
- 8 falsified
- 4 survived

Fresh TF3 adversarial set:

- 18 trees
- SHA-256 `37abd291592c4e98730d4dc8fef8c1678c4835ac87a555aad19edd5b75f14a18`
- 4 tested
- 0 falsified
- 4 finite survivors

Final TF3 interpreted states remain 11 `FALSIFIED`, 1 `TRIVIAL`; zero reached
`MATHEMATICALLY_INTERESTING`, no TF3 prior-art search was performed, and zero reached
`GRADUATION_CANDIDATE`.

The TF2/TF3 reproducibility tests, registry lineage tests, candidate-batch firewall checks, and
experiment-record uniqueness checks were green before TF4 diagnosis. The candidate registry remains
contiguous through `TF-001011`; the next permanent ID is `TF-001012`. The experiment registry
still contains exactly one scientific `TF3-0001` record and no `TF4-0001` scientific record.

## TF4 diagnostic runs and data boundary

TF4-DIAG-0001 initial validation run: `36972524602`.  
TF4-DIAG-0001 refined validation run: `36973194898`.

All candidate-selection and stability comparisons used only already-exposed orders 1-13 and committed
TF2/TF3 outputs.

Order 14 was accessed only for timing in run `36972524602`:

- all unlabeled order-14 trees: 3,159
- generation: about 0.797 s
- all domination numbers: about 8.047 s
- all maximal-independent-set counts: about 194.600 s
- individual values persisted/printed/ranked: no
- candidate-specific comparison: no

Order 14 therefore remains fresh candidate-validation data.

## Exact diagnosis of TF3 zero-interest output

The 12 ratios-only statements were interpretable but mostly bounded-order extremal fits:

- 8/12 exactly duplicate normalized TF2 statements.
- 9/12 have discovery touch count 1.
- 8/12 have the relevant extremal coefficient drift when exposed orders through 13 are included.
- The eight order-13 holdout failures collapse to four deterministic first-counterexample trees/failure
  modes.
- K1 falsifies 5/12 statements under the literal all-finite-tree domain:
  `TF-001000`, `TF-001001`, `TF-001005`, `TF-001007`, and `TF-001009`.

The four coefficients stable through exposed order 13 do not yield interest: two are K1-invalid,
one is elementary/trivial, and the `3 matching_number/5` lower bound is the already-falsified
TF-000998/TF-001010 relation.

Conclusion: the dominant TF3 limitation is the one-feature homogeneous relation grammar. It fits
discovery-boundary extrema but cannot express the interactions required by the exposed structural
counterexamples.

## Literal-hypothesis conclusion

The candidate statement says “for every finite simple tree”, while discovery begins at order 2.
TF4 treats this as an experiment-design/lifecycle mismatch.

It is not silently repaired. TF3 statements remain unchanged.

Changing TF4 to a “nontrivial tree” hypothesis was considered and rejected as the next scientific
axis because the unchanged orders-2-10 discovery dataframe is already nontrivial; generator output
would not change. Such a hypothesis mostly changes truth status for K1-sensitive forms.

TF4 therefore keeps the literal all-tree hypothesis and freezes an exposed K1 domain-consistency
gate before fresh validation. This enforces the already-declared domain; it is not a new mathematical
hypothesis and is not fresh evidence.

## Feature-vocabulary and target conclusions

No existing feature produced a mathematically interesting one-feature ratio.

- `order`, `leaf_count`, and `max_degree` show direct bounded-order scale artifacts.
- path-like growth breaks the upper `leaf_count` and `support_vertex_count` ratios.
- diameter alone fails in both directions.
- matching number yields a familiar upper relation and a historically falsified lower ratio.
- the support-vertex lower ratio is elementary.
- `maximal_independent_set_count` is qualitatively different: its ratio coefficient is strongly
  order-dependent, while it participates heavily in the more stable two-feature relations.

No feature is removed in TF4 because that would confound feature vocabulary with relation grammar.
No new invariant is added: the exposed evidence does not independently justify one strongly enough.
The target remains `domination_number`; the evidence diagnoses relation grammar before target
exhaustion.

## Alternatives considered

The following were explicitly considered:

- keep ratios and change only to a nontrivial-tree hypothesis — rejected;
- remove one existing feature — rejected for TF4;
- add one new invariant — rejected for lack of independent justification;
- change target — rejected;
- restore full-dimensional convex hulls — rejected because TF2 already diagnosed their opacity;
- full TF2 generation plus an RHS-support gate — rejected because it recreates the opaque stream and
  adds a threshold;
- fixed pairwise convex hulls — selected for one controlled experiment.

Pairwise hulls were not selected merely because ratios produced zero interest. They were reconsidered
because completed TF3 specifically diagnosed missing feature interaction as the limiting grammar.

## Quantitative pairwise-hull evidence

Across the fixed 21 unordered feature pairs:

- raw generator outputs: 259
- after Morgan: 259
- after Dalmatian: 214
- per-run post-duplicate total: 205
- cross-run exact-deduplicated forms: 146
- RHS support 0 / 1 / 2: 2 / 17 / 127
- exact TF2 overlap: 5 / 146
- upper / lower forms: 86 / 60
- median maximum denominator: 4
- 90th-percentile maximum denominator: 11
- maximum denominator: 61
- median touch count: 5
- 90th-percentile touch count: 30

On burned data, cumulative survivors were 69 through order 11, 51 through order 12, and 48 through
order 13. K1 falsifies 47/146 independently. Requiring both K1 validity and survival of burned
orders 11-13 leaves 32 forms: 1 zero-feature, 5 one-feature, and 26 two-feature forms.

Of those 26 two-feature exposed-data survivors, 21 involve `maximal_independent_set_count`. This
concentration is preserved as a diagnostic warning for interpretation; it was not used to delete or
downweight that feature.

Conclusion: pairwise hulls reintroduce more volume than TF3, but not TF2's high-dimensional opacity.
They supply genuinely new low-dimensional interaction forms with bounded feature support and moderate
coefficient complexity.

## Frozen TF4-0001

TF4-0001 is frozen with exactly one material scientific change relative to TF3:

> `ratios` over all seven features becomes `convex_hull` run separately over each of the 21
> unordered feature pairs, followed only by exact cross-run normalized deduplication.

Unchanged:

- target: `domination_number`
- discovery corpus: all 200 unlabeled trees of orders 2-10
- seven discovery features
- TxGraffiti `0.4.1` / upstream `e37126da53b84150d142a5d61202b61f78521fcc`
- Morgan/Dalmatian
- duplicate removal / touch-count sorting
- object symbol `T`
- empty payload -> upstream `None`
- literal all-finite-tree mathematical hypothesis

The machine freeze is `experiments/TF4-0001/spec.json`; the scientific runner is
`experiments/tf4_discovery.py`.

Permanent IDs begin at `TF-001012` only when the scientific run occurs. Every cross-run unique
statement receives an ID before the exposed K1 gate. Only statements remaining `CONJECTURED` after
discovery reevaluation and K1 testing enter the frozen candidate batch.

No cap, touch threshold, denominator threshold, coefficient threshold, ranking rule, or post-hoc
support gate is permitted.

## Fresh TF4 validation design

Burned/exposed orders: 1 through 13.

Fresh holdout:

> every one of the 3,159 unlabeled trees of order 14.

The candidate batch and its SHA-256 must be persisted with `holdout_constructed=false` before the
runner constructs order 14.

The exact fresh hostile families are frozen in the machine spec and consist of 19 new
path/star/spider/caterpillar/double-star/broom instances. Regression tests require their canonical
tree codes to be disjoint from both TF2 and TF3 exact hostile sets.

Only fresh order-14 survivors see those hostile trees.

## Failures and CI

No meaningful TF4 process failure occurred before the freeze. The initial and refined diagnostic
runs both completed successfully. No new failure entry was therefore required in
`docs/FAILURE_AND_LESSON_LEDGER.md`.

Relevant validation runs at this handover stage:

- pre-TF4 main validation: `36917219570`
- initial TF4 diagnostic: `36972524602`
- refined TF4 diagnostic: `36973194898`

The final freeze/PR validation and post-merge run are reported in the session closeout.

## Next session

Do not redesign TF4-0001.

Verify the then-current `main` HEAD and CI, reproduce the frozen spec/runner checks, and execute the
already-frozen TF4-0001 runner from an exact source commit. Preserve this ordering:

pairwise discovery -> exact cross-run dedup -> permanent IDs -> discovery reevaluation -> exposed K1
domain gate -> candidate-batch hash/freeze -> fresh order-14 construction/evaluation -> exact frozen
TF4 hostile set for holdout survivors -> mathematical interpretation.

Do not treat burned orders 1-13 or old hostile trees as fresh evidence. Do not tune pairwise feature
pairs, coefficients, thresholds, candidate count, or the order-14 holdout after seeing output. Do not
perform broad prior-art search unless a candidate independently reaches `MATHEMATICALLY_INTERESTING`.

---

# TF3 handover

TF3-0001 is complete as a controlled discovery/falsification experiment. TF0, TF1, TF2, and the
TF3 diagnostic/freeze history remain preserved append-only. Finite survival was not treated as proof,
and TF3 produced no graduation candidate.

## Verified provenance

Verified starting `main` HEAD for the TF3 execution continuation:
`bd6fb3d72010514e6edf0b37ab638f57688d51c5`.

TF2 authoritative scientific source commit:
`d091d88889fa72322bfc49a5531bc30b1f31b049`.  
TF2 authoritative Actions run: `36888114138`.  
Corrected TF3 diagnostic run: `36907058956`.

TF3 scientific source commit:
`e23b44d24a7b87d6f67aa18749059540934b2767`.  
TF3 scientific Actions run: `36914647703`.

The exact final merged `main` HEAD and final post-merge CI run are reported in the session
closeout because a Git commit cannot contain its own resulting SHA without changing that SHA.

## Frozen changed axis and corpus

Exactly one material discovery axis changed relative to TF2:
TxGraffiti methods `[convex_hull, ratios]` became `[ratios]`.

Target: `domination_number`.

Discovery features:
`order`, `leaf_count`, `support_vertex_count`, `max_degree`, `diameter`,
`matching_number`, `maximal_independent_set_count`.

Discovery corpus: all 200 unlabeled finite simple trees of orders 2-10.  
Discovery SHA-256:
`e1fa7090640ba0254dba399082c436cf30742d7fe19ffef1d17028e7f45ab250`.

TxGraffiti remained `0.4.1` at upstream revision
`e37126da53b84150d142a5d61202b61f78521fcc`, with Morgan/Dalmatian,
duplicate removal, touch-count sorting, object symbol `T`, and empty-payload-to-upstream-`None`
semantics unchanged.

## Generation and candidate-batch firewall

Stage counts:

- raw ratios generator output: 14
- after Morgan: 14
- after Dalmatian: 12
- after duplicate removal: 12
- final candidate count: 12

Every final statement used exactly one RHS discovery feature. Permanent IDs were allocated as
`TF-001000` through `TF-001011` before fresh holdout construction.

Candidate-batch SHA-256:
`85669d95fb7199b720bfe488c606055dd5f38a5af157c1ed2bdb5f98710344c6`.

The persisted freeze record has `holdout_constructed=false`; the runner and regression tests
enforce candidate-batch persistence before order-13 construction.

Discovery-side triage: 12 `CONJECTURED`; 0 discovery-side `FALSIFIED`, `KNOWN_RESULT`,
`TRIVIAL`, `DUPLICATE`, or `ARTIFACT_OF_FEATURE_SET`.

## Fresh order-13 holdout

The untouched TF3 holdout was all 1,301 unlabeled trees of order 13.  
Holdout SHA-256:
`5b02d81644415adc2df55d0a2ec3694125ef328cb1a0c4a2eeb733efaecef7e9`.

All 12 frozen candidates were tested. Eight were falsified and four survived:
`TF-001000`, `TF-001001`, `TF-001006`, and `TF-001010`.
The deterministic first counterexample for every holdout failure is preserved in
`experiments/TF3-0001/holdout_summary.json`.

## Fresh pre-frozen adversarial gate

Only the four order-13 survivors were tested on the exact pre-frozen fresh hostile set.

Hostile tree count: 18.  
Adversarial SHA-256:
`37abd291592c4e98730d4dc8fef8c1678c4835ac87a555aad19edd5b75f14a18`.

Adversarial falsifications: 0.  
Adversarial finite survivors: 4.

The exact TF2 hostile set remained regression-only and was not counted as fresh TF3 evidence.

## Mathematical interpretation

No finite survivor was promoted automatically.

- `TF-001000` (`gamma <= nu`) was falsified by `K1` under the literal frozen all-tree
  hypotheses: `gamma(K1)=1`, `nu(K1)=0`.
- `TF-001001` (`gamma <= n/2`) was likewise falsified by `K1`.
- `TF-001006` (`gamma >= support_vertex_count/2`) was classified `TRIVIAL` by an
  elementary support-leaf-pair argument.
- `TF-001010` (`gamma >= 3 nu/5`) is the same normalized relation previously examined as
  `TF-000998`; the already-exposed order-25 six-arm length-4 spider again falsifies it with
  `gamma=7`, `nu=12`. This was post-gate interpretation, not fresh TF3 validation evidence.

Final TF3 states: 11 `FALSIFIED`, 1 `TRIVIAL`.

Candidates reaching `MATHEMATICALLY_INTERESTING`: none.  
TF3 prior-art search performed: none.  
Candidates reaching `GRADUATION_CANDIDATE`: none.

## Process failures and validation

Scientific execution attempts `36914094286` and `36914294452` failed immediately at Python
import before discovery because the workflow invoked the runner in script mode; neither produced
scientific evidence. The successful run used module invocation only and did not change the frozen
scientific specification.

Result materialization then exposed two non-scientific maintenance issues: an unnecessary expensive
order-25 invariant computation and tests whose assertions assumed the registry would permanently stop
at a pre-TF3 state. These were corrected without changing the scientific artifact. All meaningful
failures are recorded append-only in `docs/FAILURE_AND_LESSON_LEDGER.md`.

The compact result record is in `experiments/TF3-0001/`; append-only candidate revisions extend
the registry through `TF-001011`, so the next permanent candidate ID is `TF-001012`.
Exactly one `TF3-0001` experiment record is present.

## Recommendation for TF4

TF4 should begin as a diagnosis session, not by inventing or immediately freezing a new generator.
Use the completed TF3 evidence to ask why ratios-only improved interpretability but yielded only
elementary/false one-feature relations, including the literal-hypothesis issue exposed by `K1`.
Only after that diagnosis should TF4 freeze one justified controlled axis change and allocate fresh
validation data. Do not reopen TF3-0001 or tune its failed coefficients.

---

# TF2 handover

TF2 is complete as a controlled discovery/falsification session. TreeForge remains a discovery laboratory; finite survival is not proof, and no candidate graduated to a theorem repository.

## Diagnostic conclusion

`TF2-DIAG-0001` was live-validated in GitHub Actions run `36855637323`. TF1 remains closed with exactly zero candidates. The zero is preserved as the result of its frozen configuration. TF2 established that TreeForge's empty hypothesis payload had been passed upstream as `[]`, while pinned TxGraffiti `0.4.1` interprets `None` as the always-true base predicate and `[]` as an empty hypothesis iteration. The correction is a TreeForge adapter/configuration semantic fix, not an upstream TxGraffiti bug.

## TF2-0001 scientific run

Experiment: `TF2-0001`  
Scientific source commit: `d091d88889fa72322bfc49a5531bc30b1f31b049`  
Successful scientific GitHub Actions run: `36888114138`

Discovery: orders 2–10, 200 unlabeled trees, SHA-256 `40bc528cd8b035854de816a1fbd37f1c6d688b2b1686d006387fb16dc8f5c4a8`.

Burned order: 11. It was not used for TF2 generation, tuning, holdout testing, or adversarial selection.

Untouched holdout: order 12, 551 unlabeled trees, SHA-256 `ea9f5d200ec503090499b4744338a5e39a37b7412d21ed5f6f876e2129be9433`. It was generated only after raw generation and first-stage discovery triage; `holdout_visible_to_generator=false`.

Target: `domination_number`.

Discovery features: `order`, `leaf_count`, `support_vertex_count`, `max_degree`, `diameter`, `matching_number`, `maximal_independent_set_count`.

TxGraffiti: package `0.4.1`, upstream revision `e37126da53b84150d142a5d61202b61f78521fcc`; methods `convex_hull` and `ratios`; heuristics Morgan and Dalmatian; post-processors duplicate removal and touch-count sorting; object symbol `T`; TreeForge hypothesis payload `[]` normalized by the adapter to upstream `None` (always true).

Stage counts: 23,268 raw generator outputs; 23,268 after Morgan; 10,753 after Dalmatian; 998 after duplicate removal; 998 after touch-count sorting; 0 strengthened equalities.

## Candidate outcome

Raw final TxGraffiti statements: **998**. Permanent IDs: `TF-000002` through `TF-000999`.

First-stage exact triage: 998 `CONJECTURED`; 0 `KNOWN_RESULT`; 0 `TRIVIAL`; 0 `DUPLICATE`; 0 `ARTIFACT_OF_FEATURE_SET`; 0 discovery-side `FALSIFIED`.

Untouched order-12 holdout: 924 falsified; 74 survived.

Frozen adversarial set: 74 tested; 0 falsified there; 74 survived. The adversarial corpus contained exactly the frozen 26 path/star/spider/caterpillar/balanced-binary/double-star/broom instances, SHA-256 `dea3af9c495cc79da46b7ed3797276caae22495bc86d5000ddea3605a07bcb8a`.

Mathematical interpretation: `TF-000002` became `KNOWN_RESULT`; `TF-000010` and `TF-000996` became `TRIVIAL`; 70 finite survivors remain `ADVERSARIAL_PASSED` without promotion. `TF-000998` temporarily reached `MATHEMATICALLY_INTERESTING`, received the only bounded prior-art audit, and was then `FALSIFIED` by an exact order-25 spider with six arms of length 4, where `gamma=7` and `nu=12`.

Final TF2 states: 925 `FALSIFIED`, 1 `KNOWN_RESULT`, 2 `TRIVIAL`, 70 `ADVERSARIAL_PASSED`. One lineage reached `MATHEMATICALLY_INTERESTING` before later falsification. No candidate reached or approached `GRADUATION_CANDIDATE`.

Prior-art search performed: **yes, bounded and candidate-specific for TF-000998 only**. No novelty claim was made.

## Workflow record

Frozen TF2 implementation pre-merge CI: `36864378120`.  
Original TF2 diagnostic validation: `36855637323`.  
First scientific execution attempt: `36875119955` (provisionally closed as stalled; it later completed and produced an artifact equivalent in mathematical output to the authoritative repaired run).  
Discovery-only 42,068-facet performance probe: `36887027180`.  
Clean repaired preflight: `36887887082`.  
Successful scientific run: `36888114138`.  
Initial result-materialization schema failure: `36890309397`.

The slow first-execution path, its later completion, and the materialization failure are preserved append-only in `docs/FAILURE_AND_LESSON_LEDGER.md`. The late artifact from run `36875119955` was audited as mathematically equivalent to the repaired run after removing source-commit provenance labels; it is not the authoritative TF2 record. None of these process events changed the frozen TF2 scientific specification.

## Precise next session

TF3 should begin from the completed TF2 records, not by reopening TF2-0001. Diagnose the interpretability problem exposed by 998 final convex-hull statements using only already-consumed discovery/TF2 evidence, then freeze a new experiment with one justified change aimed at producing a smaller, structurally interpretable candidate set. Orders 11 and 12 are burned, and the specific TF2 adversarial trees are exposed; fresh validation must not be represented by any of them.

The exact final repository HEAD is reported in the session closeout after final CI and merge, because a Git commit cannot contain its own resulting SHA without changing that SHA.

---

# TF1 handover

TF1 is complete. TreeForge remains a discovery/falsification/provenance laboratory; no theorem, novelty, Lean, Palomar, paper, or arXiv claim was created.

## Scientific run

Experiment: `TF1-0001`  
Source commit used to generate the corpus and call TxGraffiti: `e5175b5f5667195adf64ccae75e3dc42f0061086`  
Successful GitHub Actions run: `36852665881`

Discovery: orders 2–10, 200 unlabeled trees, SHA-256 `3e2fc0d8a340893ae82205f7524dd7021ea46cc921126820faf77fba1679203e`.

Holdout: order 11, 235 unlabeled trees, generated only after candidate generation, SHA-256 `bf525742920c088d56162172274011fa5b44973a9ce7e89f96d6f1dcfdea7b50`.

TxGraffiti `0.4.1` at upstream revision `e37126da53b84150d142a5d61202b61f78521fcc` was live-tested through the TreeForge adapter.

## Outcome

Raw generated candidates: **0**.

Known/trivial/duplicate/artifact: 0. Falsified: 0. Holdout survivors: 0. Adversarial survivors: 0. `MATHEMATICALLY_INTERESTING`: 0.

The order-11 holdout was therefore never used to evaluate a candidate, and the reserved adversarial families were not instantiated for candidate testing. No prior-art search was warranted.

Two TF1 process failures are preserved in `docs/FAILURE_AND_LESSON_LEDGER.md`: an initial Ruff failure before discovery and a workflow assertion that incorrectly treated an empty candidate batch as failure. Neither changed the frozen scientific specification.

## Precise next session

TF2 should diagnose why the frozen TxGraffiti configuration emitted no candidates, using only discovery-side information, then freeze a new experiment ID with one justified change and a fresh holdout allocation. Do not convert the zero-yield TF1 result into a reason to relax standards or mine the holdout.

The exact final repository HEAD for this session is reported in the session handover after the final CI check, because a Git commit cannot contain its own resulting SHA without changing that SHA.
