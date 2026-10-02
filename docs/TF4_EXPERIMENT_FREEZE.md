# TF4 experiment freeze

Experiment: `TF4-0001`  
Status: **FROZEN; SCIENTIFIC EXECUTION NOT YET RUN**  
Diagnostic: `TF4-DIAG-0001`  
Diagnostic validation runs: `36972524602`, `36973194898`

This freeze follows the completed TF3 ratios-only experiment. TF0-TF3 history and scientific results remain unchanged.

## Single changed scientific axis

Relative to TF3-0001, TF4-0001 changes one material scientific axis: the TxGraffiti relation geometry.

TF3 used one run with:

- methods: `ratios`
- all seven discovery features
- final RHS grammar: one discovery feature

TF4 uses:

- methods: `convex_hull`
- exactly 21 runs, one for each unordered pair of the same seven discovery features
- exact normalized cross-run deduplication only
- final RHS grammar: at most two discovery features

No candidate cap, touch-count threshold, coefficient threshold, denominator threshold, support-size threshold, or post-hoc ranking rule is introduced.

The completed TF3 failure supplies the scientific reason for this change: 8/12 one-feature coefficients drift on exposed larger orders, 8/12 exact statements already appeared in TF2, and the non-drifting forms resolve as K1-invalid, elementary, or historically falsified. Pairwise hulls are the minimal controlled increase that can express interactions while preventing the seven-feature full-dimensional opacity diagnosed in TF2.

## Fixed target, features, engine, and hypothesis

Target remains:

`domination_number`

Discovery features remain:

- `order`
- `leaf_count`
- `support_vertex_count`
- `max_degree`
- `diameter`
- `matching_number`
- `maximal_independent_set_count`

Discovery corpus remains all 200 unlabeled finite simple trees of orders 2-10.

TxGraffiti remains:

- package: `txgraffiti==0.4.1`
- upstream revision: `e37126da53b84150d142a5d61202b61f78521fcc`
- heuristic order: Morgan, then Dalmatian
- post-processors: exact duplicate removal, then touch-count sorting
- object symbol: `T`
- TreeForge hypothesis payload: `[]`
- adapter semantics: empty payload maps to upstream `None`, the always-true base predicate

The mathematical hypothesis remains literally every finite simple tree. TF4 does **not** rewrite it as “nontrivial tree”.

## Literal-domain consistency gate

TF3 exposed a lifecycle mismatch: discovery starts at order 2 although the statement includes K1.

TF4 closes this mismatch without changing the mathematical hypothesis. After permanent IDs are allocated to every final cross-run exact-deduplicated statement and after exact discovery-side reevaluation, every otherwise-`CONJECTURED` statement is evaluated on the already-exposed K1.

A K1 failure is recorded as `FALSIFIED` before the candidate batch is frozen. K1 is not fresh evidence and is not counted as a holdout or adversarial test.

This guard is required to make validation match the already-declared all-tree domain. It is not a generator-selection threshold and does not alter coefficients or statements.

## Candidate allocation and firewall

The current next permanent candidate ID is frozen as `TF-001012`.

Scientific execution order is:

1. construct only the orders 2-10 discovery corpus;
2. run the 21 pairwise convex-hull generators in the frozen feature-pair order;
3. preserve per-run raw outputs and stage counts;
4. exact-deduplicate normalized `(lhs, operator, rhs)` relations across runs while preserving source-pair provenance;
5. allocate a permanent ID to every cross-run unique final statement;
6. run exact discovery-side reevaluation and machine triage;
7. run the exposed K1 literal-domain consistency gate;
8. persist `candidate_batch.json` containing only remaining `CONJECTURED` statements plus its SHA-256 and a freeze record with `holdout_constructed=false`;
9. only then construct the fresh order-14 holdout;
10. evaluate every frozen-batch candidate on that holdout;
11. evaluate only holdout survivors on the exact pre-frozen TF4 hostile set.

The diagnostic observed 146 cross-run exact-deduplicated forms, but **146 is not a candidate cap**. Reproduction of the frozen diagnostic count is an implementation/provenance check; outputs are not selected by rank or truncated.

## Burned data

All orders 1-13 are exposed for TF4:

- order 1: K1 domain-consistency diagnosis;
- orders 2-10: discovery;
- order 11: TF1/exposed;
- order 12: TF2 holdout/exposed;
- order 13: TF3 holdout/exposed.

All TF2/TF3 candidates, counterexamples, hostile trees, and interpretation structures are exposed regression/diagnostic data only.

None may be represented as fresh TF4 evidence.

## Fresh holdout

Fresh exhaustive holdout:

> all 3,159 unlabeled trees of order 14.

Order 14 has not been inspected candidate-by-candidate.

The only pre-freeze access was the timing-only feasibility probe in Actions run `36972524602`:

- generation: about 0.797 s
- domination numbers: about 8.047 s
- maximal-independent-set counts: about 194.600 s

Individual values were not persisted, printed, ranked, or compared with candidates.

Because corpus hashing includes source-commit provenance, the exact order-14 holdout SHA-256 is recorded only by the future scientific run from its exact source commit.

## Fresh adversarial set

The following families/parameters are frozen before any order-14 survivor is known:

- paths of orders 18 and 19;
- stars of orders 18 and 19;
- spiders with arms:
  - `[2,2,13]`
  - `[3,5,10]`
  - `[2,6,10]`
  - `[4,4,5,5]`
  - `[2,2,2,2,2,2,2,2]`
  - `[1,5,12]`
- caterpillars:
  - spine 6, leaf multiplicities `[0,4,0,0,4,3]`
  - spine 7, leaf multiplicities `[3,0,0,3,0,0,4]`
  - spine 8, leaf multiplicities `[2,0,1,0,2,0,1,3]`
- double stars:
  - `[8,9]`
  - `[7,9]`
  - `[6,8]`
- brooms:
  - `[10,7]`
  - `[7,10]`
  - `[9,9]`

Regression tests must confirm that the exact `(order, canonical_tree_code)` identities are disjoint from both the TF2 and TF3 hostile sets. The order component is required because TreeForge preserves a legacy bare canonical code that is complete only within a fixed order.

Only order-14 holdout survivors see these trees during scientific execution.

## Interpretation policy

Every final generated relation must use at most two of the seven frozen RHS discovery features. A violation aborts the run rather than silently filtering it.

The exposed pairwise diagnostic measured:

- 146 cross-run exact-deduplicated forms;
- 127 two-feature forms;
- 17 one-feature forms;
- 2 constant-RHS forms;
- median maximum denominator 4;
- 90th-percentile maximum denominator 11;
- maximum denominator 61.

These numbers justify the grammar choice; they are not admission thresholds.

No broad literature search is part of TF4 execution. Prior-art work begins only if a future candidate independently reaches `MATHEMATICALLY_INTERESTING`.

Finite holdout or hostile-family survival is not proof.

## Execution status

TF4-0001 is frozen only. No TF4 permanent IDs have been allocated, no order-14 candidate evaluation has occurred, and no TF4 prior-art search has been performed.

The next session should verify the then-current `main` HEAD and CI, reproduce the frozen diagnostic/spec checks, and execute TF4-0001 without changing the target, features, feature-pair set, coefficients, candidate policy, K1 gate, holdout, or hostile set.
