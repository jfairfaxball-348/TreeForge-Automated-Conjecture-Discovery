# TF3-0001 experiment freeze

TF3-0001 is frozen before scientific candidate generation. Its diagnostic basis is `TF3-DIAG-0001`, corrected and validated in GitHub Actions run `36907058956`.

## Scientific question

TF2 showed that the full-dimensional convex-hull configuration produced a high-volume, low-interpretability stream. Of 998 final TF2 statements, 979 used at least four RHS features and 689 used all seven. TF3 asks whether restricting only the generator family to simple ratios yields a substantially smaller, structurally legible batch without changing the domination-number target, discovery features, heuristics, or research gates.

## Single changed axis

The only discovery-side material change from TF2-0001 is the TxGraffiti method set:

- TF2: `convex_hull`, `ratios`
- TF3: `ratios` only

The corrected exposed-data benchmark produced 14 raw ratio statements and 12 final statements, all with exactly one RHS discovery feature. Pairwise convex hulls produced 146 exact-deduplicated forms; an RHS-support gate would admit 12 only after generating the unchanged 23,268-item TF2 raw stream. Ratios-only therefore addresses the diagnosed source directly and avoids a post-hoc complexity threshold.

No order-12 survival result was used to select a coefficient, statement, or threshold.

## Fixed target, features, and TxGraffiti semantics

Target: `domination_number`.

Discovery features remain exactly:

- `order`
- `leaf_count`
- `support_vertex_count`
- `max_degree`
- `diameter`
- `matching_number`
- `maximal_independent_set_count`

TxGraffiti remains pinned to package `0.4.1` and upstream revision `e37126da53b84150d142a5d61202b61f78521fcc`. Morgan and Dalmatian remain enabled; duplicate removal and touch-count sorting remain enabled; object symbol remains `T`; the empty TreeForge hypothesis payload remains normalized to upstream `None`, the always-true base predicate.

There is no candidate cap and no post-generation interpretability filter. Ratios-only output is machine-checked to use exactly one distinct RHS discovery feature. A violation aborts the run rather than being silently removed.

## Discovery and exposed data

Discovery remains all 200 unlabeled trees of orders 2-10. These are exposed discovery data, not fresh evidence.

Orders 11 and 12 are burned. The exact 26-tree TF2 adversarial set, hash
`dea3af9c495cc79da46b7ed3797276caae22495bc86d5000ddea3605a07bcb8a`,
is exposed. The order-25 spider with arms `[4,4,4,4,4,4]` that falsified TF-000998 is exposed. None is counted as fresh TF3 validation evidence.

## Fresh holdout

The fresh TF3 holdout is **all 1,301 unlabeled trees of order 13**.

A pre-freeze feasibility probe timed order-13 computation but did not persist, print, inspect, rank, or compare individual invariant values. No candidate batch existed during that timing probe.

The scientific runner structurally enforces:

```text
discovery generation
→ raw-output persistence
→ machine grammar/normalization checks
→ exact discovery-side triage
→ candidate_batch.json written
→ candidate-batch SHA-256 written
→ only then fresh order-13 holdout construction
```

The holdout cannot influence feature choice, method choice, interpretability thresholds, coefficient selection, or candidate ranking.

## Candidate identity

The candidate registry is verified to end at `TF-000999`. The next permanent ID is
`TF-001000`.

Diagnostic outputs do not receive research candidate IDs. During the future scientific run, every final TxGraffiti statement receives a permanent ID beginning at `TF-001000`; IDs are allocated before holdout testing and never recycled.

## Fresh adversarial evidence

Only order-13 holdout survivors see the newly pre-frozen TF3 hostile instances:

- paths of orders 16 and 17;
- stars of orders 16 and 17;
- spiders with arms `[3,3,9]`, `[3,4,9]`, `[5,5,5]`, `[1,3,12]`, and `[2,4,10]`;
- three specified caterpillars;
- double-stars `[7,7]`, `[7,8]`, `[8,8]`;
- brooms `[8,8]`, `[9,8]`, `[8,9]`.

The exact machine-readable parameters are in `experiments/TF3-0001/spec.json`. Exposed TF2 hostile trees may later be used only as regression checks, never as fresh evidence.

## Mutation policy

Any material post-output change to the target, features, split, holdout, method set, heuristics,
post-processors, hypothesis semantics, interpretability policy, candidate normalization, or fresh
adversarial set closes TF3-0001 and requires a new experiment ID.

The machine-readable freeze is `experiments/TF3-0001/spec.json`.
