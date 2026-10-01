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
