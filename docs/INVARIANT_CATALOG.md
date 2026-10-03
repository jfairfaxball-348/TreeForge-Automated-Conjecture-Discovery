# Invariant catalog

Every invariant has a mathematical definition, provenance, implementation, exactness flag, and tests. Default discovery features should be small, interpretable, and nonredundant.

## Core exact invariants

| Name | Definition | Exactness | Implementation/provenance |
|---|---|---|---|
| `order` | `|V(T)|` | exact integer | definition |
| `edge_count` | `|E(T)|` | exact integer | definition; retained mainly for calibration and consistency |
| `min_degree`, `max_degree`, `degree_sum` | degree statistics | exact integer | definition |
| `leaf_count` | number of degree-one vertices (with `K1` handled separately) | exact integer | definition |
| `support_vertex_count` | vertices adjacent to at least one leaf | exact integer | standard tree terminology |
| `segment_count` | maximal paths with degree-not-2 endpoints and degree-2 interiors; equivalently `n - n2 - 1` or edges after suppressing degree-2 vertices | exact integer | standard structural tree parameter; added in TF12 for the independently selected fixed-segment question; formula implementation independently checked by explicit path decomposition |
| `diameter`, `radius`, `eccentricity_sum` | standard distance parameters | exact integer | NetworkX shortest-path routines on trees |
| `matching_number` | maximum matching size | exact integer | tree dynamic program |
| `independence_number` | maximum independent-set size | exact integer | independent tree dynamic program |
| `domination_number` | minimum dominating-set size | exact integer | exhaustive subset search; deliberately small-order use |
| `maximal_independent_set_count` | number of inclusion-maximal independent sets (equivalently independent dominating sets) | exact integer | three-state rooted tree dynamic program; TF6 replacement is value-equivalent to the earlier exhaustive implementation |
| `wiener_index` | sum of distances over unordered vertex pairs | exact integer | all-pairs tree distances |
| `cherry_count` | number of unordered leaf pairs sharing a support vertex | exact integer | definition |

`degree_sum` and `edge_count` are intentionally available for calibration/consistency but should normally be excluded from serious discovery feature sets because they encode basic identities.

## Optional TreeStack-inspired module

`treestack_estimate(T)` exactly reimplements the estimator definition inspected at TreeStack commit `e1e437b8d02552b7c7ee0c4c74041b6ac956f063`. It is exact integer arithmetic. The module is opt-in and separately names its provenance.

## Optional ProbStack-inspired module

`finite_stackability_probability(T, t)` is the exact rational fraction of weak compositions of total `t` on `V(T)` that are stackable, using the exact TreeStack branch-message decision rule. It is parameterised by `t`, can be expensive, and is not part of the default registry.

## Optional Greedy-Uniformity-inspired module

`greedy_output_bias(T)` is the exact total-variation distance between random-permutation greedy maximal-independent-set output and the uniform law on maximal independent sets. The initial implementation uses permutation enumeration and enforces a conservative order cap; it is opt-in.

## Approximate invariants

None are enabled in TF0. Future approximate invariants must include an explicit approximation method, error/uncertainty metadata, seed when stochastic, and a name that cannot be confused with an exact quantity.
