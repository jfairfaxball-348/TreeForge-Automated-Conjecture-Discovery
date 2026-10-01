# TF1-0001 result

TF1-0001 is complete. It was a controlled, pre-frozen discovery experiment, not a proof attempt.

## Frozen run

Scientific source commit: `e5175b5f5667195adf64ccae75e3dc42f0061086`  
Successful GitHub Actions run: `36852665881`  
TxGraffiti: `0.4.1`, upstream revision `e37126da53b84150d142a5d61202b61f78521fcc`

Discovery corpus: all 200 unlabeled trees of orders 2–10.  
Discovery SHA-256: `3e2fc0d8a340893ae82205f7524dd7021ea46cc921126820faf77fba1679203e`

Untouched holdout corpus: all 235 unlabeled trees of order 11, generated only after the TxGraffiti call returned and raw output was persisted.  
Holdout SHA-256: `bf525742920c088d56162172274011fa5b44973a9ce7e89f96d6f1dcfdea7b50`

The feature audit found no constant, exact-duplicate, or pairwise exact-affine columns among the supplied target/features, and the full corpus passed the explicit tree-identity consistency checks.

## Candidate outcome

TxGraffiti generated **0 raw candidates** under the frozen configuration. Therefore:

- TF1 candidate IDs allocated: 0.
- known/trivial/duplicate/artifact classifications: 0.
- falsified candidates: 0.
- candidates tested on holdout: 0.
- holdout survivors: 0.
- adversarially tested candidates: 0.
- adversarial survivors: 0.
- candidates reaching `MATHEMATICALLY_INTERESTING`: 0.
- prior-art searches initiated: 0.

This is a valid negative discovery result. It means only that the pinned TxGraffiti methods/heuristics emitted no statements for this target and feature set on this discovery corpus. It does **not** imply that no interesting domination-number relation exists, and it does not justify changing TF1-0001 after seeing the outcome.

The discovery and holdout row files are not committed because they are deterministic, approximately 100–120 KB each, and fully reproducible from the frozen spec, source commit label, and hashes. The compact manifest, benchmark artifact, and raw output are committed.

## Next-session recommendation

TF2 should be **zero-yield diagnosis plus a new pre-frozen controlled experiment**, not deep assessment of nonexistent survivors. Diagnose the zero output using only TF1 discovery data and TxGraffiti's documented behavior, then allocate a new experiment ID and change one justified axis (for example the target invariant or a narrowly expanded conjecturing configuration). Do not tune against the TF1 holdout, and prefer a fresh holdout allocation for the new experiment.
