# TreeForge — Experimental Conjecture Discovery in Tree Combinatorics

TreeForge is a **discovery laboratory** for finite, simple, unlabeled trees. Its job is to generate reproducible finite-tree corpora, compute mathematically defined invariants, propose candidate relations, attack them with holdout and adversarial tests, preserve failures and provenance, and graduate only unusually strong candidates into separate theorem repositories.

TreeForge is **not** a theorem prover and finite computation is never represented as proof of an infinite statement. A failed literature search is not represented as novelty. Speculative candidates are not sent to Lean, Palomar, a paper, or arXiv from this repository.

## Research pipeline

```text
finite-tree universe
→ exact/reproducible invariant computation
→ automated conjecturing
→ append-only candidate registry
→ holdout/adversarial falsification
→ mathematical interpretation
→ bounded prior-art / novelty audit
→ graduation to a separate theorem repository
```

TF0 established the infrastructure and a `KNOWN/CALIBRATION` run for the standard identity `|E(T)| = |V(T)| - 1`.

TF1 completed the first pre-frozen controlled discovery experiment, `TF1-0001`: 200 discovery trees at orders 2–10, 235 untouched holdout trees at order 11, a disciplined core feature set targeting domination number, and the pinned live `txgraffiti==0.4.1` adapter. The frozen run generated **zero candidates**. That is recorded as a valid research result rather than a reason to weaken the gates.

TF2 diagnosed that zero as a TreeForge adapter/configuration hypothesis-semantics mismatch without rewriting TF1 history, corrected the empty-payload boundary, and completed frozen experiment `TF2-0001`. The corrected run produced 998 permanent candidate lineages; 924 were falsified on untouched order 12, 74 survived the frozen adversarial set, and mathematical interpretation produced no graduation candidate. One simple finite survivor, `gamma(T) >= 3 nu(T)/5`, was later falsified exactly by an order-25 six-arm spider. See `experiments/TF2-0001/RESULTS.md`.

TF3 diagnosed the 998-statement stream as overwhelmingly dense convex-hull output and completed
`TF3-0001` with one changed discovery axis: TxGraffiti was restricted to `ratios` only.
The frozen run produced 12 permanent candidates (`TF-001000`–`TF-001011`); the fresh exhaustive
order-13 holdout falsified 8, and all 4 holdout survivors passed the 18-tree pre-frozen fresh hostile
set. Mathematical interpretation then falsified 3 of those survivors and classified the fourth as
`TRIVIAL`, leaving no `MATHEMATICALLY_INTERESTING` or graduation candidate. See
`experiments/TF3-0001/RESULTS.md`, `docs/TF3_DIAGNOSTIC.md`, and
`docs/TF3_EXPERIMENT_FREEZE.md`.

TF4 diagnosed the completed TF3 zero-interest result using only exposed orders 1-13 and committed history. The diagnosis found that 8/12 ratios already appeared exactly in TF2, 9/12 had discovery touch count 1, and 8/12 extremal coefficients drifted by exposed order 13. It also made the literal-domain mismatch explicit: K1 falsifies 5/12 TF3 forms under the stated all-tree hypothesis. TF4 therefore froze `TF4-0001` with one scientific change: fixed pairwise convex-hull generation over all 21 unordered pairs of the same seven features, with exact cross-run deduplication. The target, feature vocabulary, orders 2-10 discovery corpus, TxGraffiti pin, heuristics, post-processors, and all-tree hypothesis remain fixed. Order 14 is reserved as the fresh exhaustive holdout and has only been used for timing without value inspection. TF4-0001 has not been scientifically executed. See `docs/TF4_DIAGNOSTIC.md` and `docs/TF4_EXPERIMENT_FREEZE.md`.

## Quick start

```bash
python -m pip install -e '.[dev]'
python -m pytest -q
python -m compileall -q src experiments
ruff check .
```

Optional live TxGraffiti compatibility requires:

```bash
python -m pip install -e '.[conjecturing]'
```

Reproduce the compact TF1 benchmark with:

```bash
python experiments/benchmark_tf1.py --output /tmp/tf1-benchmark.json
```

See `PROJECT_CHARTER.md`, `docs/RESEARCH_PROTOCOL.md`, `docs/INVARIANT_CATALOG.md`, `docs/CANDIDATE_LIFECYCLE.md`, `experiments/TF1-0001/RESULTS.md`, `experiments/TF2-0001/RESULTS.md`, and `experiments/TF3-0001/RESULTS.md`, `docs/TF4_DIAGNOSTIC.md`, and `docs/TF4_EXPERIMENT_FREEZE.md` before adding another discovery experiment.
