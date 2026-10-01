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

The first infrastructure session is deliberately small. It includes a canonical unlabeled-tree generator, a modular invariant registry, a TxGraffiti adapter pinned to `txgraffiti==0.4.1`, an append-only candidate registry, holdout machinery, and one **KNOWN/CALIBRATION** end-to-end run based on the standard tree identity `|E(T)| = |V(T)| - 1`.

## Quick start

```bash
python -m pip install -e '.[dev]'
pytest
python -m compileall -q src
python experiments/calibration.py --output-dir /tmp/treeforge-calibration --source-commit LOCAL
```

To exercise the live TxGraffiti adapter, install the optional dependency:

```bash
python -m pip install -e '.[conjecturing]'
```

See `PROJECT_CHARTER.md`, `docs/RESEARCH_PROTOCOL.md`, `docs/INVARIANT_CATALOG.md`, and `docs/CANDIDATE_LIFECYCLE.md` before adding a discovery experiment.
