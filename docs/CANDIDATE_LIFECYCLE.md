# Candidate lifecycle

Candidate IDs are allocated monotonically as `TF-000001`, `TF-000002`, ... and are never reused.

## Active states

`OBSERVED → CONJECTURED → HOLDOUT_PASSED → ADVERSARIAL_PASSED → MATHEMATICALLY_INTERESTING → NOVELTY_AUDIT → GRADUATION_CANDIDATE → GRADUATED`

Transitions require an append-only registry event/revision. Passing a finite gate means only that the recorded finite test found no counterexample.

- `OBSERVED`: machine pattern retained for inspection; no mathematical claim.
- `CONJECTURED`: exact statement and hypotheses have been normalised enough to test.
- `HOLDOUT_PASSED`: passed the pre-frozen holdout corpus without leakage.
- `ADVERSARIAL_PASSED`: survived documented hostile families/smallest-counterexample searches.
- `MATHEMATICALLY_INTERESTING`: human mathematical interpretation identifies a nontrivial mechanism or question.
- `NOVELTY_AUDIT`: bounded, documented prior-art search is in progress or complete; negative search is not proof of novelty.
- `GRADUATION_CANDIDATE`: statement is frozen enough to justify a separate theorem repository.
- `GRADUATED`: separate theorem repository created; TreeForge retains history/evidence/provenance/link only.

## Side/terminal states

`FALSIFIED`, `KNOWN_RESULT`, `TRIVIAL`, `DUPLICATE`, `ARTIFACT_OF_FEATURE_SET`, `DEFERRED`.

A candidate may move to a side state from any pre-graduation state with a reason and evidence. `FALSIFIED` must preserve smallest known counterexamples and the test that found them. `KNOWN_RESULT` includes calibration rediscoveries. `ARTIFACT_OF_FEATURE_SET` includes obvious algebraic consequences of supplied columns.

## Statement revisions

A changed statement does not replace history. The same candidate ID may receive a new `revision` only when the mathematical lineage is clear; materially different statements receive new IDs and a `related_candidates` link. Every revision records exact text, timestamp, engine/version, dataset hash, invariant set, hypotheses, equality/sharp examples, holdout/adversarial status, counterexamples, prior-art status, interpretation, and lifecycle state.
