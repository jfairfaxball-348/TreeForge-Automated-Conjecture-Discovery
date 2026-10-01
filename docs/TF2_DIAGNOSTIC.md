# TF2 zero-yield diagnostic

Diagnostic ID: `TF2-DIAG-0001`  
Live validation run: GitHub Actions `36855637323`  
Diagnostic source branch checkpoint: `4e830d3c8523afcb3cd9de0c952f774228f6d146`

## Reproduction

TF1-0001 reproduced exactly from its frozen specification. The discovery corpus remained 200 trees of orders 2–10 with SHA-256 `3e2fc0d8a340893ae82205f7524dd7021ea46cc921126820faf77fba1679203e`; the order-11 holdout remained 235 trees with SHA-256 `bf525742920c088d56162172274011fa5b44973a9ce7e89f96d6f1dcfdea7b50`. Both corpora passed the existing exact identity checks, and the committed raw TxGraffiti output remained empty.

The order-11 holdout was regenerated only to verify the frozen count/hash and exact consistency identities. Its invariant values were not used for geometry analysis, feature choice, method choice, threshold choice, or TF2 tuning.

## Root cause

The zero yield is explained by a TreeForge/TxGraffiti hypothesis-semantics mismatch, not by the target geometry.

TreeForge froze `hypothesis_payload: []` to mean “no additional predicate beyond the finite-tree universe.” In pinned TxGraffiti `0.4.1`, however, `ConjecturePlayground.generate` treats `hypothesis=None` as the always-true base predicate, while an empty list creates an empty hypothesis iteration. Consequently no generator is invoked at all.

Under the exact frozen TF1 payload, the live diagnostic therefore observed:

| stage | count |
|---|---:|
| raw generator output | 0 |
| after Morgan | 0 |
| after Dalmatian | 0 |
| after duplicate removal | 0 |
| after touch-count sorting | 0 |

This makes Morgan/Dalmatian filtering, duplicate removal, touch sorting, convex-hull geometry, ratio degeneracy, and domination-number structure downstream non-causes of the TF1 zero output.

The adapter fix is deliberately narrow: an empty TreeForge hypothesis payload is normalized to `None` at the TxGraffiti boundary. TF1-0001 itself is unchanged.

## Synthetic calibration

On the separate five-row table `y = 2x`, the frozen empty-list semantics again produced zero raw statements. With the corrected adapter semantics, pinned TxGraffiti produced 6 raw statements, 6 after Morgan, 3 after Dalmatian, 2 after duplicate removal, and 2 after touch-count sorting. The surviving pair was the expected lower/upper equality pair `y >= 2x` and `y <= 2x`.

This demonstrates that the pinned package and corrected TreeForge adapter can generate and filter admissible relations.

## Discovery-side geometry audit

Using only TF1 discovery rows, the target `domination_number` takes five values, 1 through 5, with frequencies 9, 37, 93, 58, and 3. The supplied TF1 feature/target table has no constant columns, exact duplicate columns, or pairwise exact affine equivalences. Extending the audit with the withheld discovery-side invariants `radius`, `eccentricity_sum`, `independence_number`, `wiener_index`, and `cherry_count` likewise found no constants, exact duplicates, or pairwise affine equivalences across the 13 audited columns. All 200 discovery rows were distinct in the joint table; its affine rank was 12 in ambient dimension 13.

Descriptive Pearson correlations were recorded only as finite-corpus diagnostics. In particular, domination number was strongly associated on this corpus with support-vertex count (about 0.908), matching number (about 0.882), and maximal-independent-set count (about 0.823), but these values are not mathematical claims and are not used to add features to TF2.

## TF2 design consequence

The diagnosis supports changing exactly one experimental axis: correct the adapter's empty-hypothesis semantics and otherwise retain the frozen TF1 domination-number target, seven discovery features, generators, heuristics, and post-processors. This cleanly tests the intended TF1 mathematical configuration rather than opportunistically expanding the feature set after seeing TF1's outcome.

TF1 order 11 remains burned. A new TF2 holdout must be frozen separately before the corrected conjecturer is run.
