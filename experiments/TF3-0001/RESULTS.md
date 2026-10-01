# TF3-0001 result

TF3-0001 is scientifically complete. It is a controlled discovery/falsification experiment,
not a proof of any all-tree theorem.

## Provenance and frozen change

Scientific source commit: `e23b44d24a7b87d6f67aa18749059540934b2767`  
Successful GitHub Actions run: `36914647703`  
TxGraffiti: `0.4.1`, upstream revision
`e37126da53b84150d142a5d61202b61f78521fcc`

Exactly one material discovery axis changed from TF2: methods
`[convex_hull, ratios]` became `[ratios]`. The target, seven supplied features,
Morgan/Dalmatian heuristics, duplicate removal, touch-count sorting, and empty-hypothesis-to-
upstream-`None` semantics remained frozen.

Two earlier Actions attempts, `36914094286` and `36914294452`, failed at Python import
before the runner entered discovery; they produced no candidates or validation evidence and are
recorded in the failure ledger. The successful source commit above used module invocation only;
the frozen scientific specification was unchanged.

## Discovery and candidate-batch firewall

Discovery corpus: all 200 unlabeled trees of orders 2-10.  
Discovery SHA-256: `e1fa7090640ba0254dba399082c436cf30742d7fe19ffef1d17028e7f45ab250`

Pipeline counts:

- raw ratio generator output: 14
- after Morgan: 14
- after Dalmatian: 12
- after duplicate removal: 12
- final: 12

All final statements satisfied the frozen one-RHS-feature grammar. Every statement received a
permanent ID, `TF-001000` through `TF-001011`, before fresh holdout construction.
Candidate-batch SHA-256: `85669d95fb7199b720bfe488c606055dd5f38a5af157c1ed2bdb5f98710344c6`.

The persisted batch-freeze record says `holdout_constructed: false`; the runner and its
regression test both enforce that the order-13 corpus is constructed only below that point.

## Fresh order-13 holdout

Fresh holdout: all 1301 unlabeled trees of order 13.  
Holdout SHA-256: `5b02d81644415adc2df55d0a2ec3694125ef328cb1a0c4a2eeb733efaecef7e9`

All 12 frozen candidates were tested. Eight were falsified and four survived:
`TF-001000`, `TF-001001`, `TF-001006`, and `TF-001010`.
The committed holdout summary preserves each deterministic first counterexample for the eight
failures. Finite survival is not proof.

## Fresh pre-frozen hostile set

Only the four holdout survivors were tested on the pre-frozen TF3 hostile set.
The set contains 18 trees and has SHA-256
`37abd291592c4e98730d4dc8fef8c1678c4835ac87a555aad19edd5b75f14a18`. No survivor failed this finite hostile gate, so all four
temporarily reached `ADVERSARIAL_PASSED`.

## Mathematical interpretation

Interpretation did not force a survivor.

- `TF-001000`, `gamma <= nu`, is falsified by `K1` under the literal frozen all-tree
  hypotheses: `gamma(K1)=1`, `nu(K1)=0`.
- `TF-001001`, `gamma <= n/2`, is likewise falsified by `K1`.
- `TF-001006`, `gamma >= support_vertex_count/2`, is `TRIVIAL`: for order at least 3,
  disjoint support-leaf pairs give the stronger elementary bound `gamma >= support_vertex_count`;
  `K2` supplies the exceptional factor-1/2 equality and `K1` is immediate.
- `TF-001010`, `gamma >= 3 nu/5`, is the same normalized relation already examined as
  `TF-000998`; the exposed order-25 spider with six length-4 arms again gives
  `gamma=7`, `nu=12`, and falsifies it. This is interpretation evidence, not fresh TF3
  validation evidence.

Final interpreted states are {'FALSIFIED': 11, 'TRIVIAL': 1}. No TF3 candidate reaches
`MATHEMATICALLY_INTERESTING`, no new prior-art search is performed, no candidate reaches
`GRADUATION_CANDIDATE`, and no theorem or novelty claim is made.

## Reproducibility

The compact scientific record commits the raw TxGraffiti output, stage counts, normalized
candidate batch and batch-freeze hash, holdout/adversarial summaries, interpretation summary,
and append-only candidate/experiment registry revisions. The discovery and validation row files
remain deterministic generated data; their exact counts and hashes are recorded and reproduced by
the TF3 result tests.
