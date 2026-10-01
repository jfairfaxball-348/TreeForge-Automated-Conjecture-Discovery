# Roadmap

## TF0 — infrastructure session

Status: **IN PROGRESS until the calibration/provenance commit and CI are complete.**

Scope: inspect and pin predecessor repositories; inspect and pin TxGraffiti; scaffold the package; implement canonical unlabeled-tree generation; implement a modular invariant API; establish discovery/holdout/adversarial separation; create an append-only candidate registry; add falsification machinery; run one known-result calibration; add CI; document failures and limitations.

Explicitly out of scope: broad conjecture discovery, novelty claims, Lean, Palomar, theorem-paper work, and arXiv packaging.

## TF1 — next session

Build the first serious tree-invariant corpus and perform the first controlled discovery run. Before generation, freeze the discovery/holdout order ranges, invariant set, TxGraffiti configuration, and adversarial families. Keep the holdout untouched until candidate generation has finished.
