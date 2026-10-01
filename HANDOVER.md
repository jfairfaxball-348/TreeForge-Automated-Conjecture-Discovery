# TF0 handover

TF0 is complete. TreeForge is now an infrastructure repository for finite-tree discovery, falsification, lifecycle tracking, and provenance; it is not a theorem repository.

## Frozen code checkpoint used for the calibration

`f0c42426fdabd3860837d3e3eb048a038842a655`

At that revision, GitHub Actions run `36849930237` completed successfully: the pinned `txgraffiti==0.4.1` installed, the unit suite passed (including a real adapter call through `ConjecturePlayground.discover`), byte-compilation passed, Ruff passed, and the deterministic calibration smoke test passed.

## Calibration

`TF-000001` is `KNOWN/CALIBRATION` only: `For every finite tree T, |E(T)| = |V(T)| - 1.` Discovery orders were 2–5; order 6 was held out from generation and then checked separately. The registry records the exact source commit, command, dependency state, parameters and SHA-256 hashes. This finite run is infrastructure evidence, not a proof and not a novelty claim.

## Preserved lessons

Three early CI failures are intentionally documented in `docs/FAILURE_AND_LESSON_LEDGER.md`; they exposed a clean-environment import-path assumption and lint-policy issues. They were repaired without rewriting the history.

## Precise next session

**TF1 — build the first serious tree-invariant corpus and perform the first controlled discovery run.**

The first TF1 action should be a cost benchmark and experiment freeze: select conservative order ranges from measured invariant costs, freeze the discovery/holdout split, freeze the feature set and TxGraffiti configuration, and freeze hostile parametric families before generating any research candidates.
