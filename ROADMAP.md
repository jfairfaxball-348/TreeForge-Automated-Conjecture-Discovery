# Roadmap

## TF0 — infrastructure session

Status: **COMPLETE (2026-10-01).**

Completed scope: predecessor and TxGraffiti provenance pins; package scaffold; exact AHU-style canonical unlabeled-tree generation; modular exact invariant registry; separate opt-in TreeStack/ProbStack/Greedy-Uniformity quantities; a narrow TxGraffiti adapter pinned to `txgraffiti==0.4.1`; append-only candidate/experiment registries; holdout machinery; parametric hostile-family constructors; tests; static checks; CI; and one tiny `KNOWN/CALIBRATION` end-to-end run.

Calibration source code checkpoint: `f0c42426fdabd3860837d3e3eb048a038842a655`. GitHub Actions run `36849930237` passed installation, unit tests (including a live TxGraffiti adapter call), byte-compilation, Ruff, and deterministic calibration smoke testing.

The calibration candidate is `TF-000001`, the standard identity `|E(T)| = |V(T)| - 1`, generated only to validate plumbing. It is permanently classified `KNOWN_RESULT` and must never be presented as new mathematics.

Explicitly not done in TF0: broad conjecture discovery, novelty claims, Lean, Palomar, theorem-paper work, or arXiv packaging.

## TF1 — next session

**Build the first serious tree-invariant corpus and perform the first controlled discovery run.**

Before candidate generation, benchmark the default and optional invariant costs; freeze the discovery and holdout ranges; freeze the invariant set and TxGraffiti configuration; choose targeted adversarial families; record the corpus-generation command and dependency versions; then generate candidates from discovery data only. Do not expose the holdout until generation has finished.
