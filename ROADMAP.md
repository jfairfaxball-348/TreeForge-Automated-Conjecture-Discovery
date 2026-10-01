# Roadmap

## TF0 — infrastructure session

Status: **COMPLETE (2026-10-01).**

Completed scope: predecessor and TxGraffiti provenance pins; package scaffold; exact AHU-style canonical unlabeled-tree generation; modular exact invariant registry; separate opt-in TreeStack/ProbStack/Greedy-Uniformity quantities; a narrow TxGraffiti adapter pinned to `txgraffiti==0.4.1`; append-only candidate/experiment registries; holdout machinery; parametric hostile-family constructors; tests; static checks; CI; and one tiny `KNOWN/CALIBRATION` end-to-end run.

Calibration source code checkpoint: `f0c42426fdabd3860837d3e3eb048a038842a655`. GitHub Actions run `36849930237` passed installation, unit tests (including a live TxGraffiti adapter call), byte-compilation, Ruff, and deterministic calibration smoke testing.

The calibration candidate is `TF-000001`, the standard identity `|E(T)| = |V(T)| - 1`, generated only to validate plumbing. It is permanently classified `KNOWN_RESULT` and must never be presented as new mathematics.

## TF1 — first controlled discovery

Status: **COMPLETE (2026-10-01).**

TF1 benchmarked the current exact invariant implementations, froze experiment `TF1-0001`, generated a 200-tree discovery corpus (orders 2–10) and a 235-tree holdout corpus (order 11) with strict generation-order separation, added practical duplicate/affine/known-identity checks, and exercised the pinned live TxGraffiti adapter in GitHub Actions.

Successful scientific run: source commit `e5175b5f5667195adf64ccae75e3dc42f0061086`, Actions run `36852665881`.

Result: TxGraffiti generated **zero candidates** under the frozen target/features/methods/heuristics. No standards were weakened to force a survivor. Accordingly there were no TF1 candidate IDs, holdout candidate evaluations, adversarial survivor tests, mathematical-interest promotions, or prior-art searches.

See `experiments/TF1-0001/RESULTS.md`.

## TF2 — diagnosed and controlled discovery rerun

Status: **COMPLETE (2026-10-01).**

TF2 diagnosed the TF1 zero-yield result without rewriting TF1 history. The practical cause was a TreeForge/TxGraffiti adapter-semantics mismatch: TreeForge's empty hypothesis payload was forwarded as upstream `[]`, while pinned TxGraffiti `0.4.1` uses `None` for the always-true base predicate and `[]` iterates over no hypotheses. The correction remains isolated in the adapter and is live-tested against the pinned package.

Frozen experiment `TF2-0001` kept the TF1 target, seven discovery features, `convex_hull` plus `ratios`, Morgan/Dalmatian heuristics, duplicate removal, and touch-count sorting. Discovery reused orders 2–10 (200 trees); order 11 remained burned; the untouched holdout was all 551 unlabeled trees of order 12.

Successful scientific run: source commit `d091d88889fa72322bfc49a5531bc30b1f31b049`, Actions run `36888114138`.

Pipeline counts were 23,268 raw generator outputs, 23,268 after Morgan, 10,753 after Dalmatian, and 998 after duplicate removal/touch-count sorting. Permanent IDs `TF-000002` through `TF-000999` were allocated. All 998 passed exact discovery-side reevaluation and entered `CONJECTURED`; the untouched order-12 holdout falsified 924 and left 74 survivors. All 74 survived the 26 pre-frozen adversarial trees.

Mathematical interpretation classified `TF-000002` as `KNOWN_RESULT`, `TF-000010` and `TF-000996` as `TRIVIAL`, and left 70 high-dimensional facets at finite `ADVERSARIAL_PASSED` without promotion. `TF-000998`, the simple bound `gamma(T) >= 3 nu(T)/5`, briefly reached `MATHEMATICALLY_INTERESTING` and received a bounded prior-art audit, but deeper structural interpretation produced an exact order-25 six-arm spider counterexample (`gamma=7`, `nu=12`), so it is permanently `FALSIFIED`.

No candidate reached `GRADUATION_CANDIDATE`. No theorem, novelty, Lean, Palomar, paper, or arXiv claim was created.

See `experiments/TF2-0001/RESULTS.md`.

## TF3 — recommended next session

Close TF2 rather than mining its used holdout or weakening its gates. Start with a discovery-side/recorded-evidence diagnosis of why the full-dimensional convex-hull configuration produced a large batch of mostly opaque facets, then freeze a new experiment ID with one justified interpretability-oriented change. Benchmark any proposed configuration before freeze, keep orders 11 and 12 burned, treat the specific TF2 adversarial trees as exposed, and allocate genuinely fresh validation data rather than representing previously inspected trees as untouched evidence.
