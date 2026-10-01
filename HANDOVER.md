# TF3 handover

TF3 completed the interpretability diagnosis and froze `TF3-0001`; the scientific experiment has
**not** been executed. TF0, TF1, and TF2 history remains unchanged.

## Verified starting state

Verified starting `main` HEAD: `b0cb414a3603bf9bd2db3367878e39ae05df01bc`.

TF2 authoritative scientific source commit:
`d091d88889fa72322bfc49a5531bc30b1f31b049`.

TF2 authoritative scientific GitHub Actions run: `36888114138`.
TF2 final pre-merge validation run: `36901734182`.

At TF3 start, the candidate registry contained exactly 999 candidate IDs,
`TF-000001` through `TF-000999`; `TF-000001` remained the calibration identity. The next
permanent ID is `TF-001000`. TF1 and TF2 experiment records remain unique and append-only.

## TF2 interpretability diagnosis

The 998 TF2 final statements have RHS feature-support counts:

- 1 feature: 8
- 2 features: 4
- 3 features: 7
- 4 features: 12
- 5 features: 61
- 6 features: 217
- 7 features: 689

Therefore 979/998 (98.1%) use at least four RHS features and 689/998 (69.0%) use all seven.
Of the already-consumed 74 order-12 survivors, 70/74 (94.6%) use at least four features.
There are 190 upper bounds and 808 lower bounds. Discovery touch count has median 10 and
90th percentile 17; per-candidate maximum rational denominator has median 10, 90th percentile 60,
and maximum 1208.

The principal diagnosis is full-dimensional convex-hull geometry interacting with seven supplied
features. TF2's earlier discovery-only probe exposed 42,068 Qhull facets. Morgan is ineffective
under the common always-true hypothesis mask; Dalmatian reduced the stream substantially, and exact
duplicate removal reduced 10,753 statements to 998, but exact syntactic equivalence does not collapse
the many mathematically related dense facet families. Low touch counts and complicated rational
coefficients add opacity but are secondary to the geometry.

## Alternatives considered

Corrected diagnostic GitHub Actions run: `36907058956`.

1. Ratios only: 14 raw, 12 after Dalmatian, 12 final; all 12 have one RHS feature; maximum
   denominator 13; about 0.342 seconds.
2. Unchanged full TF2 generation plus a machine RHS-support <= 2 gate: would admit 12 final TF2
   forms, but only after the unchanged 23,268 raw / 10,753 post-Dalmatian / 998 deduplicated stream.
3. Twenty-one fixed pairwise convex hulls: 259 raw, 214 after Dalmatian, 205 post-duplicate across
   individual runs, 146 after cross-run exact deduplication; 127 use two RHS features; maximum
   denominator 61; about 0.778 seconds.

The support gate was rejected because it adds a threshold while retaining the diagnosed opaque
generation process. Pairwise hulls were rejected for TF3 because they still create a materially
larger stream and introduce a multi-hull design. No holdout survival information selected a
coefficient, statement, or threshold.

## Frozen TF3-0001

Single changed discovery axis: TxGraffiti method set becomes `ratios` only.

Target: `domination_number`.

Discovery features remain:
`order`, `leaf_count`, `support_vertex_count`, `max_degree`, `diameter`,
`matching_number`, `maximal_independent_set_count`.

Discovery corpus: all 200 unlabeled trees of orders 2-10.

TxGraffiti remains `0.4.1` at upstream revision
`e37126da53b84150d142a5d61202b61f78521fcc`; Morgan/Dalmatian, duplicate removal,
touch-count sorting, object symbol `T`, and empty-payload-to-`None` semantics remain fixed.

Interpretability policy: no post-generation filter, candidate cap, touch threshold, or
coefficient/denominator threshold. Ratios-only output is asserted to contain exactly one distinct
RHS discovery feature; violation aborts rather than silently filters.

## Exposed data and fresh validation

Burned/exposed data include all trees of orders 2-12, the exact TF2 adversarial set, the
order-25 six-arm length-4 spider, and all other structures inspected during TF2 interpretation.

Fresh holdout: all 1,301 unlabeled trees of order 13, exhaustive rather than sampled. A pre-freeze
timing-only probe measured about 0.187 seconds for generation, 0.949 seconds for all domination
numbers, and 23.976 seconds for all maximal-independent-set counts. Individual order-13 invariant
values were not persisted, printed, inspected, ranked, or compared with candidates.

The runner enforces discovery generation → machine normalization/triage → candidate-batch file and
hash freeze → only then order-13 construction. Only holdout survivors see the newly frozen TF3
adversarial instances. Exact TF2 hostile trees remain regression-only, not fresh evidence.

## Process failures

Run `36906556561` failed a synthetic method-selection fixture before diagnostics.
Run `36906621879` completed but its diagnostic-only complexity parser was invalid because regexes
were over-escaped. Run `36907013799` failed the new parser unit test during the first correction.
All are preserved in `docs/FAILURE_AND_LESSON_LEDGER.md`. Corrected run `36907058956` passed.

## Execution status and next session

Experiment ID: `TF3-0001`.

Next permanent candidate ID: `TF-001000`.

TF3-0001 is **frozen only; not scientifically executed**. No TF3 permanent candidate IDs have been
allocated, no order-13 candidate evaluation has occurred, and no TF3 literature search has been
performed.

The next session should verify the then-current `main` HEAD and CI, read
`docs/TF3_DIAGNOSTIC.md`, `docs/TF3_EXPERIMENT_FREEZE.md`, and
`experiments/TF3-0001/spec.json`, then execute the frozen runner without retuning. It should
materialize results append-only, test every admitted candidate on the fresh holdout, apply only the
pre-frozen fresh adversarial set to holdout survivors, and stop before any prior-art work unless a
candidate independently reaches `MATHEMATICALLY_INTERESTING`.

The exact final repository HEAD and final merged CI run are reported in the session closeout because
a Git commit cannot contain its own resulting SHA without changing that SHA.

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
