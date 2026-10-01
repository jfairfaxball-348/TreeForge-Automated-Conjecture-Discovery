# TF2-0001 experiment freeze

TF2-0001 is frozen before real candidate generation. Its diagnostic basis is `TF2-DIAG-0001`, live-validated in GitHub Actions run `36855637323`.

## Scientific question

TF1's zero output was caused by a TreeForge/TxGraffiti hypothesis-semantics mismatch: an empty TreeForge hypothesis payload was passed upstream as an empty list, which caused pinned TxGraffiti `0.4.1` to iterate over no hypotheses and invoke no generators. TF2-0001 corrects that adapter boundary and otherwise keeps the intended TF1 mathematical configuration fixed.

The target remains `domination_number`. The seven discovery features remain:

- `order`
- `leaf_count`
- `support_vertex_count`
- `max_degree`
- `diameter`
- `matching_number`
- `maximal_independent_set_count`

The TxGraffiti methods remain `convex_hull` and `ratios`; Morgan and Dalmatian acceptance remain enabled; duplicate removal and touch-count sorting remain enabled. No withheld TF1 diagnostic invariant is promoted into the discovery feature set.

## Split

Discovery reuses all 200 unlabeled trees of orders 2–10. These orders have already influenced the project and are therefore not represented as fresh evidence.

TF1 order 11 is burned. It is excluded from TF2 generation, feature/method choice, holdout testing, and adversarial selection.

The new untouched TF2 holdout is all 551 unlabeled trees of order 12. The holdout is generated only after TxGraffiti finishes and first-stage discovery-side triage is complete. Its exact hash is recorded by the live run because TreeForge corpus hashes include the exact scientific source-commit label.

## Candidate policy

Every final TxGraffiti statement entering triage receives a permanent candidate ID beginning with `TF-000002`. Raw statements are preserved. Normalization uses the adapter's structured `lhs`, operator, and `rhs` metadata; there is no post-hoc coefficient tuning. Exact normalized duplicates are classified `DUPLICATE`. Obvious target-placement artifacts or tautologies are classified before holdout. Every remaining exact discovery-valid statement becomes `CONJECTURED` and must receive an order-12 holdout result.

No candidate-count cap is imposed after seeing output.

## Adversarial set

The hostile-family set is frozen in the machine specification and deliberately capped at orders 13–15 where practical so the current exact exhaustive maximal-independent-set counter remains conservative. It includes paths, stars, long-arm spiders, one balanced spider, three caterpillars, the height-3 balanced binary tree, three double-stars, and three brooms.

Only `HOLDOUT_PASSED` candidates see these families.

## Research boundary

Finite survival is not proof. The runner may move a survivor to `ADVERSARIAL_PASSED`, but it does not automatically promote anything to `MATHEMATICALLY_INTERESTING`. Any such promotion requires a separate mathematical interpretation after the finite results are visible. Prior-art search is not triggered unless that interpretation gate is actually passed.

The machine-readable freeze is `experiments/TF2-0001/spec.json`. Any material change requires a new experiment ID.
