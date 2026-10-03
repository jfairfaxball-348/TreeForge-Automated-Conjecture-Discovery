# TF17 — minimum-dominating-set multiplicity: exact machinery and structural diagnosis

Date: 2026-10-03

TF17 continues the independent question selected by TF16.  For a finite tree T, write

`zeta(T) = # {D subseteq V(T) : D is a minimum dominating set of T}`

and

`M_n = max { zeta(T) : T is a tree of order n }`.

The aim of TF17 is not to extend a numerical sequence.  It is to validate exact counting machinery,
identify the mechanisms behind the exposed extremizers, compare those mechanisms with the strongest
published constructions, and decide whether one structural statement is rigid enough to freeze a
prospective experiment before order 15 is exposed.

**Decision: exact machinery is validated, but the unrestricted structural theory is not yet rigid
enough to justify a fresh experiment.  The experiment pause is preserved.**

## 1. Starting-state and provenance verification

TF17 starts from merged `main`

`63a7b45858eab3d7b734fde2506c1bf8c20622d3`.

The requested TF16 provenance checks exactly:

- TF16 PR #22 exact head:
  `19c0ebf69cc99a76dba5df6cf0411341e95c0032`;
- exact-head Actions run `37147414924`: completed successfully at that exact head;
- TF16 merge / starting main:
  `63a7b45858eab3d7b734fde2506c1bf8c20622d3`;
- post-merge Actions run `37147577254`: completed successfully at the merge commit.

PR #22 changed exactly four files:

- `HANDOVER.md`;
- `README.md`;
- `ROADMAP.md`;
- `docs/TF16_RESEARCH_QUESTION_AUDIT.md`.

It therefore contained no candidate-registry, experiment-registry, invariant-registry, source
invariant, test-corpus, or scientific-data change.

The live repository boundary also agrees with the TF16 handover:

- the last scientific experiment record is still `TF4-0001`;
- its allocated candidate range ends at `TF-001157`;
- `CandidateRegistry.next_id()` remains `TF-001158`;
- no TF5--TF17 scientific experiment record exists;
- `minimum_dominating_set_count` is not in the default invariant registry;
- orders 1--14 are the burned universe;
- no tree of order 15 or larger is generated or inspected in TF17.

No provenance discrepancy was found.

## 2. Exact rooted min-plus/count dynamic program

TF17 implements the TF16 recurrence in
`src/treeforge/invariants/minimum_dominating_sets.py` as theorem/diagnostic machinery only.
It is **not** added to the default discovery registry.

Every rooted state is a pair

`(minimum selected-vertex cost, exact number of choices attaining that cost)`.

An infeasible state has no integer cost and count zero.  Product adds feasible costs and multiplies
counts.  Minimum chooses the smaller cost; if several alternatives tie at the minimum cost, their
counts are added.  Thus no floating-point sentinel or approximate arithmetic is used.

For a rooted vertex v:

- `A_v`: v is selected;
- `B_v`: v is not selected and is dominated by at least one selected child;
- `C_v`: v is not selected, is not dominated in its rooted subtree, and must be dominated by its
  parent.

For a leaf,

- `A=(1,1)`;
- `B` is infeasible;
- `C=(0,1)`.

For an internal vertex with children u:

`A_v = (1,1) product_u min(A_u,B_u,C_u)`.

A selected v may satisfy a child in state C.

`C_v = product_u B_u`.

If v is still waiting for its parent, no child may be selected (otherwise v would already be
dominated) and no child may wait for v (because v is unselected), so every child must be closed in
state B.

For B, child states are restricted to A or B and at least one child must be in A.  The
implementation accumulates two temporary exact states: no selected child seen yet and at least one
selected child seen.  This avoids subtraction and preserves exact tie counts.

At the root state C is inadmissible.  Therefore

`min(A_root,B_root) = (gamma(T), zeta(T))`.

### Why the recurrence is exact

The three states partition feasible partial solutions according to the only information the parent
needs about the root of a child subtree: whether that child root is selected, already dominated
below, or still requires the parent.  Once those boundary states are fixed, distinct child
subtrees are independent, so costs add and counts multiply.  Alternatives represented by distinct
state choices are disjoint, so tied optimum alternatives add their counts without double counting.
Induction from the leaf states proves the recurrence.

This also proves root invariance mathematically: the root only chooses which edge boundaries are
oriented for the recursion; the final A/B union is exactly the set of global minimum dominating
sets.

## 3. Independent validation

The implementation is checked in three genuinely separate ways.

### Brute-force gamma and zeta

For every one of the 48 unlabeled trees of orders 1--8, a test independently enumerates vertex
subsets by cardinality, tests domination directly, stops at the first feasible cardinality, and
counts every dominating subset of that minimum size.

The rooted DP agrees on **both** gamma and zeta for all 48 trees.

### Root invariance

For the same 48 trees, the DP is rerun at every possible root, for 326 rooted evaluations.  Every
root gives the same ordered pair `(gamma,zeta)`.

### Existing exact domination implementation

The gamma component of the new DP is compared with TreeForge's pre-existing exhaustive
`domination_number` implementation on every one of the 5,447 burned unlabeled trees of orders
1--14.

Agreement is exact on all 5,447 trees.

Named regression examples additionally cover K1, K2, paths, stars, double-stars, subdivided stars,
and arbitrary small coronas.  In particular, every corona `H corona K1` checked from a base tree
H of order at most seven has profile

`(gamma,zeta) = (|V(H)|, 2^|V(H)|)`.

## 4. Burned-order extremal data

Only after the exact implementation passed the independent checks was it applied exhaustively to
the burned orders 1--14.

| n | M_n | number of extremizers | gamma of extremizers |
|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 |
| 2 | 2 | 1 | 1 |
| 3 | 1 | 1 | 1 |
| 4 | 4 | 1 | 2 |
| 5 | 3 | 1 | 2 |
| 6 | 8 | 1 | 3 |
| 7 | 8 | 1 | 3 |
| 8 | 16 | 2 | 4 |
| 9 | 18 | 1 | 4 |
| 10 | 32 | 3 | 5 |
| 11 | 40 | 1 | 5 |
| 12 | 64 | 6 | 6 |
| 13 | 84 | 1 | 6 |
| 14 | 128 | 11 | 7 |

These values are diagnostics on burned data, not an all-order theorem and not an order-15
prediction.

Two structural patterns are exact throughout the burned range.

### Even orders: exactly the corona family

For every burned even order `n=2k`, the extremizers are **exactly**

`H corona K1`

as H ranges over all unlabeled k-vertex trees.

The number of extremizers at n = 2,4,6,8,10,12,14 is therefore

`1,1,1,2,3,6,11`,

which is exactly the number of unlabeled trees at base orders 1 through 7.

This multiplicity is elementary.  The k pendant leaves force every dominating set to meet each
host-leaf pair, so gamma is at least k.  Choosing exactly one endpoint from every pair always
dominates the corona, giving gamma = k and exactly `2^k` minimum dominating sets.

This also explains why the burned even family need not have maximum degree at most four: taking H
with larger degree gives corona extremizers of maximum degree 5, 6, or 7 already in the exposed
range.

### Odd orders: exactly the balanced W_(a,b) family

Taletskii defines `W_(a,b)` from a three-vertex path by attaching a degree-2 preleaf-with-leaf
branch a times to one end and b times to the other end.  His exact count is

`zeta(W_(a,b)) = 3*2^(a+b) - 2^a - 2^b`.

For fixed `a+b=s`, maximizing this expression is equivalent to minimizing
`2^a+2^b`, which occurs exactly when `|a-b|<=1`.

For every burned odd order `n=3,5,7,9,11,13`, the unique extremizer is exactly this balanced
`W_(a,b)` with

`a+b=(n-3)/2`.

Thus the odd exposed values 1,3,8,18,40,84 are explained by a published family and a one-line
balancing argument, not by recurrence fitting.

Except for the tiny P3 endpoint case, the burned extremizers have no strong support vertices.

## 5. Theorem-first reductions

### Strong-support forcing

TF16 proved the first reduction: if a support has at least two leaf neighbours, it belongs to every
minimum dominating set.  TF17 retains this and makes its counting consequence explicit.

No minimum dominating set containing that forced support contains one of those leaf neighbours:
such a leaf would be redundant.

### Safe twin-leaf pruning

If a support v has at least **three** leaf neighbours, deleting one of them preserves both gamma and
zeta.

Before deletion, v is forced.  After deletion at least two leaf neighbours remain, so v is still
forced.  Minimum dominating sets on both trees contain v and none of its leaf neighbours, giving a
bijection by restriction/extension.

The threshold matters.  Pruning from two leaf neighbours to one is not valid in general:
`K1,2` has one minimum dominating set, while deleting one leaf gives `K2`, which has two.

This gives a legitimate twin-leaf normalization only down to multiplicity two at a strong support.

### Exact rooted replacement signature

The DP gives a local replacement lemma.

Attach a rooted pendant tree R to the rest of a tree by one parent edge.  The rest of the tree can
interact with R only through the three exact states `(A_R,B_R,C_R)`.  Therefore replacing R by
another rooted tree R' with the same three `(cost,count)` states preserves every ancestor state
and hence preserves the global pair `(gamma,zeta)`.

This is a genuine domination-equivalence principle, but it is not yet an extremal normal-form
theorem: the space of possible state triples has unbounded integer costs and counts, and TF17 has
not proved that every extremizer can be reduced to a finite set of rooted gadgets.

## 6. Prior-art and structural audit

The bounded TF17 audit checked the literature named in TF16 and searched current 2025--2026
follow-up terminology including minimum dominating sets, gamma-sets, dominion, extremal trees,
order, rooted recurrences, and local forcing.  No exact theorem determining unrestricted M_n and
all n-vertex extremizers was located.  This remains a bounded-search status only.

### Alvarado--Dantas--Mohr--Rautenbach (2019)

J. D. Alvarado, S. Dantas, E. Mohr and D. Rautenbach,
“On the maximum number of minimum dominating sets in forests,”
Discrete Mathematics 342 (2019), 934--942,
DOI 10.1016/j.disc.2018.11.025.

They prove a forest upper bound exponential in domination number (reported as approximately
`2.4606^gamma`) and discuss lower constructions following the counterexample to the earlier
`2^gamma` question.  This is fixed-gamma theory, not an exact order-n classification, and its
upper constant has since been improved.

### Taletskii (2023)

D. S. Taletskii, “On the Number of Minimum Dominating Sets in Trees,”
Mathematical Notes 113 (2023), 552--566,
DOI 10.1134/S0001434623030264.

Three parts are especially relevant.

First, for trees of maximum degree at most four he proves the sharp
`zeta(T) <= (sqrt(2))^n` bound.  Equality at even n occurs when exactly n/2 preleaf/support
vertices each have a unique leaf.  The burned corona mechanism is the unrestricted version of the
same pairwise choice phenomenon.

Second, the paper gives the exact W_(a,b) formula used above.  In particular,
`W_(4,4)` has order 19 and 736 minimum dominating sets, which is already greater than
`(sqrt(2))^19`.

Third, Taletskii joins copies of this degree-5 module through suitable preleaves without changing
the multiplicative count, obtaining for every n a degree-at-most-five construction with more than
`(1/3)*1.415^n` minimum dominating sets.  He also proves the unrestricted upper bound
`zeta(T) < 1.4205^n`.

This directly prevents the burned even-corona grammar from being an all-order solution.  For
example, the published module-joining construction at order 38 has `736^2=541696` minimum
dominating sets, exceeding the corona value `2^19=524288`.  More generally its exponential base
is strictly above sqrt(2), so any family with only sqrt(2)-rate growth must eventually lose.

Taletskii's proof is itself replacement-oriented: it distinguishes forced/universal and excluded
vertices, uses separability and local forest replacements, and derives an S-decomposition before
the global upper bound.  These are the most relevant published ingredients for a future
normal-form theorem, but the paper does not state an exact unrestricted equality grammar.

### Petr--Portier--Versteegen (2024)

J. Petr, J. Portier and L. Versteegen,
“On the number of minimum dominating sets and total dominating sets in forests,”
Journal of Graph Theory 106 (2024), 976--993,
DOI 10.1002/jgt.23107.

They prove

`zeta(F) <= (sqrt(5))^gamma(F)`

for every forest and construct, for every positive gamma, a tree with more than

`(2/5)*(sqrt(5))^gamma`

minimum dominating sets.

Their proof organizes vertices by recursively defined k-terminal complexity.  In a forest chosen
to violate the desired extremal estimate, low-complexity branching is progressively restricted:
for example, 2-terminal vertices have tightly bounded collections of 1-terminal neighbours, and
higher terminal levels are forced toward degree two before the final decomposition.  This is much
closer to the kind of local structural reduction TreeForge needs than an arbitrary sequence fit.

However, their objective is growth in gamma, not exact order n.  Their construction therefore does
not by itself predict M_15 or classify n-vertex extremizers.

### Current dominion-family work

The bounded update search also located the 2026 work of Allagan, Gray, Sawyer and Morgan,
“Four Dominion Growth Regimes in Trees: Forcing, Fibonacci Enumeration, Periodicity, and
Stability,” arXiv:2601.03485, and the related 2026 journal article on dominion in trees.

It gives exact zeta behavior for selected pendant-path and complete-binary-tree families.  In
particular, one pendant per path vertex gives the same `2^gamma` independent-choice mechanism,
while denser pendant attachment forces uniqueness and alternating attachment produces Fibonacci
growth.  This supports the local forcing interpretation but does not state the unrestricted M_n
extremal theorem.

### Gamma-graphs / reconfiguration

Gamma-graph work is relevant for enumerating and organizing the set of minimum dominating sets,
but no result located there converts reconfiguration structure into the exact unrestricted
order-extremal classification required here.  It is therefore not promoted to a separate discovery
axis.

## 7. Rejected structural directions

The following ideas were considered and rejected as prospective experiment hypotheses.

**“Every even extremizer is a corona.”**  Exact on all burned even orders, but analytically false
globally by Taletskii's degree-5 module construction.  No fresh test is needed to reject it.

**“Every odd extremizer is balanced W_(a,b).”**  Exact on the burned odd orders and explained by
Taletskii's formula, but it has only sqrt(2)-base exponential growth.  Published constructions have
a strictly larger exponential base, so this cannot be the final unrestricted mechanism.

**“No strong supports characterizes extremizers.”**  Absence of strong supports is at most a
necessary-looking diagnostic in the exposed range.  Many nonextremal trees also have no strong
support, so it is far too weak.

**“Normalize all repeated leaves.”**  Pruning is safe only while at least two leaf neighbours remain
at a support.  The two-to-one step can change zeta, so unrestricted twin-leaf reduction is false.

**“Use the rooted triple as a finite automaton immediately.”**  The triple is an exact sufficient
boundary signature, but its costs and counts are unbounded.  TF17 has not proved a finite dominance
order or finite set of extremal rooted states.  Treating the observed small states as finite would
be a new empirical assumption.

**“Use the strongest fixed-gamma family as the n-vertex candidate.”**  The Petr--Portier--Versteegen
construction optimizes a different resource.  Without controlling vertices per gamma-state gadget,
it does not determine the order-extremal problem.

## 8. Experiment decision

TF17 ends in preferred state **A: exact counting machinery validated, but structural extremizer
theory still insufficient**.

No scientific experiment is frozen or executed.

There is no justified order-15 prediction.  In particular, TF17 does not take the burned
corona/W pattern and extrapolate it to n=15.

The exact state is:

- new scientific experiment: **no**;
- TF17 experiment-registry row: **no**;
- order-15 prediction frozen: **no**;
- order 15 consumed: **no**;
- orders 15 and above untouched: **yes**;
- new candidate allocated: **no**;
- next candidate ID: **TF-001158**;
- candidate registry changed: **no**;
- experiment registry changed: **no**;
- new default invariant: **no**;
- `minimum_dominating_set_count` helper implemented: **yes, non-default**;
- broad TxGraffiti generation: **no**;
- fixed-segment thread reopened: **no**;
- TF7--TF9 support/MIS thread reopened: **no**.

The deterministic TF17 diagnosis is
`experiments/tf17_minimum_dominating_sets.py`.  It constructs only orders 1--14 and asserts the
fresh-data firewall internally.

## 9. Recommended next session

A theorem-first TF18 should not ask for the next value of M_n.

The most promising continuation is to translate Taletskii's separability/S-decomposition
replacements and the Petr--Portier--Versteegen terminal-complexity restrictions into TreeForge's
exact three-state rooted signatures.  The specific target should be one of:

1. prove a dominance/replacement relation on rooted signatures that reduces every n-vertex
   extremizer to a bounded menu of local gadgets; or
2. derive an exact finite-state extremal recurrence with an order cost attached to each rooted
   state, and prove that it dominates all other rooted signatures.

Only if such a theorem is obtained should TreeForge freeze a fresh experiment.  A valid freeze
would include the proved state grammar, its exact n=15 consequence, allowed extremizer families,
and a one-shot failure condition before any order-15 tree is generated.

If no finite rooted-state dominance theorem emerges, keep the experiment pause rather than turning
the burned M_n values into a recurrence-fitting exercise.
