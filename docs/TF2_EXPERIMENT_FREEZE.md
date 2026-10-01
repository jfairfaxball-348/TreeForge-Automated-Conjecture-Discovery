# TF2-0001 experiment freeze

TF2-0001 is the first controlled experiment after the TF1 zero-yield diagnosis. It is frozen before candidate generation.

## Design decision

The diagnosis identified a single implementation-semantic cause for TF1's empty output: TreeForge used an empty hypothesis payload to mean no extra predicate, while pinned TxGraffiti interprets an empty list as no hypotheses to iterate. The adapter now maps an empty TreeForge payload to TxGraffiti `None`, its always-true base predicate.

TF2-0001 therefore changes **only that axis**. It retains TF1's target `domination_number`; the seven features `order`, `leaf_count`, `support_vertex_count`, `max_degree`, `diameter`, `matching_number`, and `maximal_independent_set_count`; the `convex_hull` and `ratios` generators; Morgan and Dalmatian heuristics; duplicate removal; and touch-count sorting.

The withheld invariants examined during the discovery-only diagnostic are not added.

## Split

Discovery remains all 200 unlabeled trees of orders 2–10. Reusing these already-seen orders is intentional: TF2-0001 asks what the intended TF1 configuration emits after the adapter semantic correction.

TF1 order 11 is permanently burned and is not reused.

The TF2 holdout is all 551 unlabeled trees of order 12. Order 12 was previously used in TF1 only for computation-time benchmarking. No order-12 invariant table, mathematical relation, candidate result, feature choice, method choice, or threshold choice was inspected before this freeze. Thus its mathematical values remain sealed from TF2 design.

Before the conjecturer runs, the TF2 runner computes the discovery and holdout hashes and exact consistency checks, writes a pre-generation freeze artifact containing only hashes/counts/provenance, discards the holdout rows, and only then calls TxGraffiti on the discovery dataframe.

## Candidate policy

There is no post-hoc attractiveness cap. Every statement returned by the frozen TxGraffiti adapter after the frozen heuristics and post-processors is preserved and assigned a permanent candidate ID beginning with `TF-000002`.

First-stage triage precedes all holdout evaluation. Every statement promoted to `CONJECTURED` must then receive an order-12 holdout result. Only holdout survivors may be exposed to the pre-reserved hostile families.

The machine-readable authority is `experiments/TF2-0001/spec.json`. Any material change requires a different experiment ID.
