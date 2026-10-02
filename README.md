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

TF4 completed `TF4-0001` with the frozen one-axis change from ratios to 21 fixed pairwise convex-hull runs. The scientific run at source `d8e0874a22dde7f226431fc4f15a36adb8254efa` (Actions `36983184665`) reproduced 259 raw outputs, 214 after Dalmatian, 205 per-run post-duplicate outputs, and 146 exact cross-run unique statements. Permanent IDs `TF-001012`–`TF-001157` were allocated before the exposed K1 gate; K1 falsified 47, leaving a 99-candidate batch frozen with SHA-256 `2bbb81b85eb6e40351f0913fafdc822c5417b2336e957e83fc08b505aedabf0f` before order 14 was constructed.

The fresh exhaustive 3,159-tree order-14 holdout falsified 66 of those 99 and left 33 survivors; all 33 survived the exact 19-tree frozen hostile set. Post-gate interpretation then found one already-exposed order-11 counterexample, classified six forms as elementary, four as feature-set artifacts, identified `TF-001013` as the known Lemańska leaf bound, and left `TF-001028`, `gamma(T) <= (2n+1-diameter(T))/3`, in bounded `NOVELTY_AUDIT` after a targeted search found no exact match. That negative search is not evidence of novelty. Twenty maximal-independent-set-count facets remain finite `ADVERSARIAL_PASSED` without promotion. No candidate reached `GRADUATION_CANDIDATE`. See `experiments/TF4-0001/RESULTS.md`, `docs/TF4_DIAGNOSTIC.md`, and `docs/TF4_EXPERIMENT_FREEZE.md`.

TF5 resolved TF-001028 structurally rather than broadening discovery. The frozen bound
gamma(T) <= (2n+1-diameter(T))/3 is a direct consequence of Ore's classical
gamma<=floor(n/2) bound in the short-diameter regime and Gu-Meng-Zhang-Wan (2013),
Lemma 2.3, in the long-diameter regime. TF-001028 is therefore append-only KNOWN_RESULT,
not a novelty or graduation candidate. Candidate-specific exact family searches found no
counterexample and exposed infinite equality families, but the lifecycle decision rests on the
published implication. TF5 also diagnosed the 20 surviving maximal-independent-set-count facets:
they form four neighboring coordinate families and their frozen coefficient planes remain
equality-supported through exposed orders 11-14. That stability is not enough to justify removing
or transforming the MIS-count feature, so TF5 freezes no new experiment. See
docs/TF5_TF001028_ANALYSIS.md.

TF6 completes the requested exposed-data diagnosis of `maximal_independent_set_count`.
A three-state independent-domination tree DP now makes the coordinate's local recurrence explicit
and replaces the value-equivalent brute-force core implementation. The 20 surviving TF4 MIS facets
remain supporting and equality-attaining through every exposed extension to order 14; the only
strict exposed dominance relations are TF-001091 over TF-001034 and TF-001095 over TF-001037.
A bounded structural literature check confirms that exponential MIS scale is intrinsic, but log,
per-vertex growth, nth-root, extremal-ratio, removal, and rooted-state replacements are not
independently canonical linear discovery coordinates. TF6 therefore retains raw MIS count, freezes
no new experiment, allocates no candidate ID, and leaves every order at least 15 untouched. See
`docs/TF6_MIS_COORDINATE_DIAGNOSIS.md` and `experiments/TF6-DIAG-0001/diagnosis.json`.

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

See `PROJECT_CHARTER.md`, `docs/RESEARCH_PROTOCOL.md`, `docs/INVARIANT_CATALOG.md`, `docs/CANDIDATE_LIFECYCLE.md`, `experiments/TF1-0001/RESULTS.md`, `experiments/TF2-0001/RESULTS.md`, `experiments/TF3-0001/RESULTS.md`, `experiments/TF4-0001/RESULTS.md`, `docs/TF4_DIAGNOSTIC.md`, `docs/TF4_EXPERIMENT_FREEZE.md`, `docs/TF5_TF001028_ANALYSIS.md`, and `docs/TF6_MIS_COORDINATE_DIAGNOSIS.md` before adding another discovery experiment.
