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

## TF3 — interpretability diagnosis and next experiment freeze

Status: **FROZEN; SCIENTIFIC EXECUTION NOT YET RUN (2026-10-01).**

TF3 quantified the TF2 interpretability problem using only exposed data. Of 998 final TF2 statements,
979 used at least four RHS features and 689 used all seven. Corrected diagnostic run
`36907058956` compared a small predeclared set of discovery-side alternatives. Ratios-only produced
14 raw and 12 final statements, all one-feature RHS forms; fixed pairwise convex hulls still produced
146 cross-run exact-deduplicated statements; a post-generation support-size gate would admit 12 only
after creating the unchanged full TF2 hull stream.

Experiment `TF3-0001` is frozen with exactly one discovery-axis change: TxGraffiti methods are
restricted from `convex_hull + ratios` to `ratios` only. The target, seven features, orders 2-10
discovery corpus, Morgan/Dalmatian heuristics, duplicate removal, touch-count sorting, and
empty-hypothesis semantics remain unchanged.

Orders 11 and 12 and all exact TF2 hostile/candidate-specific structures remain exposed. The fresh
TF3 holdout is all 1,301 unlabeled trees of order 13, constructed by the scientific runner only
after `candidate_batch.json` and its SHA-256 are frozen. A timing-only feasibility probe did not
persist or inspect individual order-13 invariant values. Fresh hostile instances are also frozen in
the TF3 machine spec.

The next session should execute the already-frozen TF3-0001 protocol without retuning it, materialize
the candidate lineages beginning at `TF-001000`, and perform the exact holdout/adversarial lifecycle.
