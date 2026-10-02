# TF4 diagnosis: why interpretable one-feature ratios produced zero interest

TF4-DIAG-0001 diagnoses the completed TF3 result using only already-exposed data. It does not reopen TF3, allocate new permanent candidates, or use order 14 for candidate selection.

Initial validation run: `36972524602`.  
Refined validation run: `36973194898`.  
Verified starting `main` HEAD: `fe2ce0cf6a0a7a749ffe8b9425a0508646cf1ad7`.

## Data boundary

Candidate comparisons use only:

- the orders 2-10 discovery corpus;
- exposed orders 11, 12, and 13;
- K1 for literal-domain consistency;
- committed TF2 and TF3 candidate/output records; and
- previously exposed TF2/TF3 hostile and interpretation structures.

Thus every order from 1 through 13 is burned for TF4 validation.

Order 14 was used only for timing feasibility. Run `36972524602` generated all 3,159 order-14 unlabeled trees and timed exact computation without persisting, printing, ranking, or comparing any individual invariant value with a candidate. Generation took about 0.797 s, domination-number computation about 8.047 s, and maximal-independent-set counting about 194.600 s. Order 14 therefore remains uninspected candidate-validation data.

## What TF3 ratios actually did

The 12 TF3 ratios-only candidates were small and readable, but the batch was mostly a rediscovery/extremal-fit layer rather than a new structural regime:

- 8/12 are exact normalized statements already present in TF2.
- 9/12 have discovery touch count 1.
- 8/12 have their relevant extremal coefficient change by the time exposed orders through 13 are included.
- The eight fresh order-13 failures collapse to only four deterministic first-counterexample trees.
- Five of the twelve statements already fail on K1 under the literal all-finite-tree hypothesis.

The scale drift is concrete. For example:

- `gamma >= n/10` changes to the star-controlled extrema `1/11`, `1/12`, and `1/13` as exposed orders 11-13 are added.
- `gamma >= leaf_count/9` and `gamma >= max_degree/9` likewise drift immediately on larger stars.
- `gamma <= 2 leaf_count` and `gamma <= 2 support_vertex_count` are eventually broken by paths, where domination grows while those features remain bounded.
- The diameter lower and upper coefficients both drift on exposed larger trees.
- `gamma >= 3 maximal_independent_set_count/13` changes sharply across exposed orders, confirming that the maximal-independent-set count lives on a qualitatively different scale from the linear target.

The four ratio coefficients that do not drift through order 13 do not produce mathematical interest:

- `gamma <= matching_number` is K1-invalid under the frozen all-tree domain and is the same relation as TF-000002.
- `gamma <= n/2` is K1-invalid.
- `gamma >= support_vertex_count/2` is elementary/trivial.
- `gamma >= 3 matching_number/5` is the already-falsified TF-000998/TF-001010 relation.

So TF3's zero-interest outcome is not explained merely by bad luck on order 13. The dominant mechanism is that a one-feature homogeneous ratio grammar fits bounded-order extrema but cannot express the feature interactions that the exposed counterexamples require.

## Literal hypothesis / K1 diagnosis

The mathematical statement says “for every finite simple tree”, while discovery starts at order 2. This is an experiment-design mismatch, not a reason to rewrite TF3 statements.

It affects more than the two late TF3 survivors: K1 falsifies TF-001000, TF-001001, TF-001005, TF-001007, and TF-001009.

Changing a future experiment to the hypothesis “nontrivial tree” would not change the generator output on the unchanged orders 2-10 dataframe. It would only change downstream truth status for K1-sensitive forms, including familiar bounds. That is not a convincing scientific axis for TF4.

TF4 therefore retains the literal all-finite-tree domain. Future execution should instead enforce that declared domain before any fresh holdout by evaluating generated statements on the already-exposed K1 after permanent IDs are allocated and before the candidate batch is frozen. This is a lifecycle/domain-consistency correction, not a new mathematical hypothesis.

## Feature-vocabulary diagnosis

No supplied feature generated a mathematically interesting one-feature ratio.

- `order`, `leaf_count`, and `max_degree` produced obvious bounded-order scale artifacts.
- `leaf_count` and `support_vertex_count` upper bounds fail against path-like growth.
- `diameter` fails in both directions because domination depends on branching and placement, not diameter alone.
- `matching_number` produced one standard-style upper relation and one historically falsified lower relation.
- `support_vertex_count` produced an elementary lower consequence.
- `maximal_independent_set_count` behaves qualitatively differently: its one-feature coefficient is strongly order-dependent, and it participates heavily in the more stable two-feature pairwise relations below.

This does not justify deleting `maximal_independent_set_count` in TF4. Doing so simultaneously with changing relation grammar would confound two scientific axes. It also does not justify adding a new invariant merely to force yield. The exposed evidence points first to missing interactions among the existing features.

There is likewise insufficient evidence to abandon `domination_number` as the target. The zero-interest ratio result diagnoses the grammar more directly than the target.

## Reconsidering fixed pairwise convex hulls

TF3 had rejected pairwise hulls because ratios-only was the cleaner response to TF2 opacity. The completed TF3 result supplies a new reason to reconsider them: one-feature relations are now empirically the limiting grammar.

The fixed pairwise diagnostic runs `convex_hull` once for each of the 21 unordered pairs of the same seven features, with the same target, discovery rows, hypothesis semantics, Morgan/Dalmatian heuristics, and post-processors. Only exact cross-run duplicates are collapsed.

Measured result:

| quantity | value |
|---|---:|
| feature-pair runs | 21 |
| raw generator outputs | 259 |
| after Morgan | 259 |
| after Dalmatian | 214 |
| per-run post-duplicate total | 205 |
| cross-run exact-deduplicated forms | 146 |
| RHS support 0 / 1 / 2 | 2 / 17 / 127 |
| exact TF2 overlap | 5 / 146 |
| upper / lower bounds | 86 / 60 |
| maximum denominator | 61 |
| median denominator | 4 |
| 90th-percentile denominator | 11 |
| median touch count | 5 |
| 90th-percentile touch count | 30 |

Using burned data diagnostically, 69 of the 146 forms survive order 11, 51 survive cumulative orders 11-12, and 48 survive cumulative orders 11-13. K1 independently falsifies 47/146. Requiring both literal-domain validity on K1 and survival of burned orders 11-13 leaves 32 forms: 1 constant-RHS, 5 one-feature, and 26 two-feature forms.

Those 26 two-feature exposed-data survivors are distributed across several feature pairs, so the method is not simply reproducing TF2. However, 21/26 involve `maximal_independent_set_count`; this concentration is an explicit diagnostic flag for later interpretation, not a reason to remove that feature before the controlled grammar experiment.

Pairwise hulls therefore do reintroduce more volume than ratios-only, but not the TF2 opacity regime: every RHS uses at most two supplied features, median coefficient denominator is 4, and only 5/146 statements exactly duplicate TF2. The output is large enough to require disciplined automation but small and low-dimensional enough for candidate-by-candidate interpretation.

## Alternatives considered

**Keep ratios and change only the hypothesis domain.** Rejected for TF4. The discovery dataframe is already nontrivial, so the generator output would be unchanged; this mostly rescues K1-sensitive forms rather than opening a new discovery regime.

**Remove one feature.** Not selected. Ratios fail across several features, and removing `maximal_independent_set_count` now would confound feature vocabulary with relation grammar.

**Add one new invariant.** Not selected. No missing invariant is justified strongly enough by exposed evidence independent of a desired conjecture.

**Change target.** Not selected. The current evidence identifies a grammar limitation before it identifies target exhaustion.

**Full-dimensional convex hulls.** Rejected. TF2 already established the 998-statement high-dimensional opacity problem.

**Full TF2 generation plus an RHS-support filter.** Rejected again. It creates the opaque full stream first and then adds a threshold/filter axis.

**Fixed pairwise convex hulls.** Selected. This is the minimal controlled interaction increase supported by TF3's completed failure mode.

## TF4 decision

Freeze TF4-0001 with one material scientific change relative to TF3:

> replace ratios-only generation with fixed pairwise convex-hull generation over all 21 unordered pairs of the unchanged seven features, followed only by exact cross-run deduplication.

Target, features, discovery orders, TxGraffiti pin, heuristics, post-processors, object symbol, and literal all-tree hypothesis remain unchanged.

The fresh holdout is all 3,159 unlabeled trees of order 14. No order-14 candidate comparison has occurred.

The machine freeze is `experiments/TF4-0001/spec.json`. TF4-0001 is frozen only in this session; it is not scientifically executed.
