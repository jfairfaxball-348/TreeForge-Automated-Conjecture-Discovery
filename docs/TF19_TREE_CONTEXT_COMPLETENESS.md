# TF19 — tree-context completeness for minimum-dominating-set multiplicity

Date: 2026-10-04

For a finite tree (T), write

`zeta(T)=# {D subseteq V(T): D is a minimum dominating set of T}`

and

`M_n=max{zeta(T): |V(T)|=n}`.

TF19 attacks the precise completeness gap left by TF18.  The two questions are whether actual tree
contexts see less information than the abstract projective A/B/C interface, and whether the
smaller rate-improving replacements used in the literature can be padded to the original order by
an exact vertex-budget operation.

**Decision: actual tree contexts do admit a strictly coarser exact quotient, and there is a useful
exact strong-support padding lemma, but neither result yields finite exact-order completeness.  The
tree-context quotient is already infinite on endpoint-rooted paths.  TF19 therefore preserves the
experiment pause and does not inspect order 15.**  This is preferred end state **A** from the TF19
brief.

## 1. Provenance and scientific boundary

TF19 starts from exact merged `main`

`af679ca707abf95d1b6dfc76b11035a65e3f2250`,

the merge commit for TF18 PR #24.

The requested TF18 provenance checks exactly:

- PR #24 exact head:
  `886faac8df71811d0e4c4c9467026603a04f6ff2`;
- exact-head Actions run `37156742490`: completed successfully;
- merge / TF19 starting main:
  `af679ca707abf95d1b6dfc76b11035a65e3f2250`;
- post-merge Actions run `37156926069`: its `test` job completed successfully, including
  unit tests, byte-compilation, Ruff, all historical deterministic checks, and the TF18 rooted-state
  diagnosis.

PR #24 changed exactly eight files: CI, README, ROADMAP, HANDOVER, the failure/lesson ledger, the
TF18 theorem note, the TF18 deterministic diagnosis, and its tests.  It did not change either
registry or the default invariant implementation.

The live boundary agrees with the TF18 handover:

- the candidate history still ends at `TF-001157`, so `TF-001158` remains next;
- the last scientific experiment row remains `TF4-0001`;
- `minimum_dominating_set_count` remains theorem/diagnostic machinery and is absent from the
  default invariant registry;
- orders 1--14 remain the burned diagnostic universe;
- no tree of order at least 15 is generated or inspected in TF19.

No provenance discrepancy was found.

## 2. One-hole tree contexts and the exact reverse message

Let (R) be a pendant rooted subtree with root (r), attached by the edge (pr) to the rest of a
tree.  Delete (R) and root the remaining component at (p).  This rooted component is the
**one-hole tree context** (C[-]).

Write the ordinary TF17 rooted state of the outside component at (p) as

`(A_0,B_0,C_0)`.

Each entry is an exact `(cost,count)` min-plus/count pair.  Conditioning on the boundary state of
the inserted gadget gives a reverse or outside message

`K(C)=(K_A,K_B,K_C)`.

The compatibility rules are exact:

- if the gadget is in state A, its root is selected and may dominate (p), so the outside can be
  in A, B, or C;
- if the gadget is in state B, its root is unselected and already closed below, so it neither
  dominates (p) nor needs (p); the outside may be in A or B;
- if the gadget is in state C, its root requires (p), so (p) must be selected and the outside
  is forced to A.

Therefore

`K_A=min(A_0,B_0,C_0)`,

`K_B=min(A_0,B_0)`,

`K_C=A_0`,

with the same exact min-on-tie count addition used by TF17.

If a gadget state is `X=(x_X,m_X)` and the outside message is
`K_X=(k_X,l_X)`, that boundary alternative contributes total cost
`k_X+x_X` and exact multiplicity `l_X m_X`.  Taking the min-plus/count minimum over
A, B, C exactly recovers the closed tree profile `(gamma,zeta)`.

This is the reverse DP requested in Phase B.  It requires no sampled contexts.

## 3. Realizable context offsets: only three cost patterns

The abstract TF18 projective theorem allowed an arbitrary outside offset vector.  Genuine tree
contexts are much more rigid.

Let (k_A,k_B,k_C) be the costs of the three outside messages.  From the definitions,

`k_A <= k_B <= k_C`.

Moreover (k_C-k_A<=1).  If the minimum defining (k_A) is (A_0), the gap is zero.  If it is
(B_0), the TF18 rooted inequality
`cost(A_0)<=cost(B_0)+1` gives the claim.  If it is (C_0), the inequality
`cost(A_0)<=cost(C_0)+1` gives the claim.

The costs are integers, so after subtracting (k_A), **every genuine one-hole tree context has
exactly one of three possible normalized cost patterns**:

`E0=(0,0,0)`,

`E1=(0,0,1)`,

`E2=(0,1,1)`.

All three occur.  Endpoint-rooted outside paths give canonical realizers:

| outside context | exact ((K_A,K_B,K_C)) | normalized costs |
|---|---|---|
| (P_1) | (((0,1),(1,1),(1,1))) | (E2) |
| (P_2) | (((1,2),(1,2),(1,1))) | (E0) |
| (P_3) | (((1,2),(1,1),(2,2))) | (E1) |

Thus the abstract offset space in TF18 was genuinely too large at the cost level.

## 4. The exact tree-context quotient

Normalize a rooted gadget signature by subtracting its always-finite A-state cost, giving

`d=(0,d_B,d_C)`,

with infeasible states retained.  The TF18 elementary inequalities imply every finite
(d_B,d_C) is at least (-1).

For each realizable pattern (E_i), define the **context lower face**

`F_i(R)=argmin_X (d_X + E_i(X))`.

Only states lying in one of (F_0,F_1,F_2) can ever contribute to a global minimum after the gadget
is inserted into a tree context.  A state outside all three faces is context-dead: changing its
cost farther above the minimum or changing its count has no effect on `gamma` or `zeta` in
any one-hole tree context.

This immediately shows that the TF18 projective signature is not context-minimal.  For example,

- the center-rooted (K_{1,2}) has
  `A=(1,1), B=(2,1), C=infeasible`;
- the center-rooted (K_{1,3}) has
  `A=(1,1), B=(3,1), C=infeasible`.

Their projective cost shapes differ, but A is the unique lower-face state for all three genuine
context patterns in both gadgets.  They therefore have identical exact tree-context behavior even
though TF18 keeps them separate.

### Exact congruence theorem

Define the **tree-context interface** of a rooted gadget to consist of

1. the ordered lower-face triple ((F_0,F_1,F_2)); and
2. the exact state count of every state that appears in at least one lower face.

Then two rooted gadgets with the same tree-context interface have identical normalized
((gamma,zeta)) response in every one-hole tree context.  If their A baselines differ by (q),
every context's domination number differs by the same (q), while `zeta` is identical.

Proof: every outside context has one of (E0,E1,E2).  Its winning boundary states are precisely the
corresponding lower face.  The normalized optimum cost is determined by that face, and the exact
multiplicity is the outside count-weighted sum of the retained state counts.  Context-dead states
never enter an optimum.

Conversely, the three canonical contexts (P_2,P_3,P_1), in the order (E0,E1,E2), determine
the lower-face type and every context-active count.  Their exact outside count weights are,
respectively,

`(2,2,1)`, `(2,1,2)`, and `(1,1,1)`.

Because each finite normalized gadget cost is either (-1), (0), or at least (1) for the
purpose of these three probes, there are eight effective lower-face types.  Writing the active
state counts as ((alpha,beta,gamma)), the canonical responses are:

| (d_B) type | (d_C) type | normalized optimum costs (E0,E1,E2) | zeta on (E0,E1,E2) |
|---|---|---|---|
| (-1) | (-1) | ((-1,-1,0)) | ((2beta+gamma, beta, alpha+beta+gamma)) |
| (-1) | context-dead | ((-1,-1,0)) | ((2beta, beta, alpha+beta)) |
| (0) | (-1) | ((-1,0,0)) | ((gamma, 2alpha+beta+2gamma, alpha+gamma)) |
| (0) | (0) | ((0,0,0)) | ((2alpha+2beta+gamma, 2alpha+beta, alpha)) |
| (0) | context-dead | ((0,0,0)) | ((2alpha+2beta, 2alpha+beta, alpha)) |
| context-dead | (-1) | ((-1,0,0)) | ((gamma, 2alpha+2gamma, alpha+gamma)) |
| context-dead | (0) | ((0,0,0)) | ((2alpha+gamma, 2alpha, alpha)) |
| context-dead | context-dead | ((0,0,0)) | ((2alpha, 2alpha, alpha)) |

Here “context-dead” includes any finite value at least (1), infeasibility, and in the first row
family the (d_C=0) versus (d_C>=1) distinction when (d_B=-1), because none of those
differences changes a lower face.

The table is triangular.  In the ((-1,-1,0)) optimum-cost pattern, (beta) is read from the
(E1) response and (E0-2E1) detects and recovers (gamma).  In the ((-1,0,0)) pattern,
(gamma) is the (E0) response and the excess of (E1) over twice (E2) detects and recovers
(beta).  In the ((0,0,0)) pattern, (alpha) is the (E2) response, then the residuals in
(E1) and (E0) recover any active (beta) and (gamma).  Thus the quotient is also
Myhill--Nerode-style minimal for the exact min-plus/count response: any two distinct quotient
interfaces are separated by one of the three canonical tree contexts.

### Stronger context-safe dominance

The quotient yields a strictly stronger safe replacement preorder than TF18 projective equality.
If (R) and (S) have the same three lower faces and every count of (S) on a context-active
state is at least the corresponding count of (R), then

`zeta(C[S]) >= zeta(C[R])`

for every genuine tree context (C[-]).  If, on each of the three faces, at least one winning
state count is strictly larger and no winning count is smaller, the inequality is strict in every
tree context.

At equal gadget order this is a valid exact-order extremal exclusion.  Unlike TF18 projective
dominance, it deliberately ignores cost/count coordinates that no tree context can observe.


The TF18 coordinatewise-cost counterexample remains a counterexample even after restricting the
outside to a genuine tree context.  Insert the two order-8 rooted spiders from TF18 into the
canonical (E0) context (P_2).  The first has
`A=(3,1), B=(3,1), C=infeasible`; the second has
`A=(2,1), B=(3,2), C=infeasible`.  Although the second has no larger absolute state cost and no
smaller state count, the filled profiles are respectively `(gamma,zeta)=(4,4)` and
`(3,2)`.  The cheaper A state destroys the genuine-context A/B tie.  Thus restricting to actual
trees does not rescue naive coordinatewise Pareto dominance; the lower-face condition is essential.

## 5. The quotient is nevertheless infinite

The finite set of cost faces does **not** produce a finite exact automaton.

TF18 already proved that for endpoint-rooted (P_{3k}),

`A=(k+1, k(k+3)/2)`,

`B=(k,1)`,

`C=(k,k)`.

Hence (d_B=d_C=-1) for every (k>=1).  All three states are context-active, and the exact active
count vector is

`(k(k+3)/2, 1, k)`.

The (E0) canonical context alone gives zeta (2+k), so different (k) are separated by a
genuine tree context.  Therefore there are infinitely many exact tree-context equivalence classes
already among maximum-degree-two rooted trees.

This is an analytic obstruction, not an extrapolation from burned counts.  Actual contexts
collapse the **cost geometry** to three patterns, but they do not collapse the exact active
multiplicities to finitely many states.

## 6. Same-order vertex-budget compensation

TF19 also obtains one exact compensation principle.

### Strong-support padding lemma

Let (v) be a vertex with at least two private leaf neighbors.  Add any number (d>=0) of
additional private leaves adjacent to (v).  Then both `gamma` and `zeta` are unchanged.

Proof: every minimum dominating set contains the strong support (v); otherwise its at least two
leaf neighbors must all be selected and can be replaced by (v) to obtain a smaller dominating
set.  Consequently every old minimum dominating set already dominates every newly added leaf.
Conversely (v) remains forced after padding, and a minimum dominating set cannot contain a new
leaf in addition to (v), because that leaf could be deleted.  Restriction to the original
vertices is therefore a bijection between the minimum dominating sets before and after padding.

The same proof is context-uniform.  If a rooted replacement gadget (S) contains an internal
strong support whose private leaves remain leaves after attachment, then padding (S) at that
support by (d) leaves leaves ((gamma,zeta)) unchanged in **every** outside tree context.
Thus a smaller context-improving replacement can be converted to a same-order replacement whenever
the replacement already supplies such a forcing bank.

This is an exact answer to part of the vertex-budget problem, but it is conditional.

### Arbitrary padding is false

There is no context-free rule saying that released vertices may simply be attached as leaves.

Already

`zeta(P_2)=2`

while attaching a leaf to an endpoint gives

`zeta(P_3)=1`.

The failure is exactly visible in the TF17 interface.  The two-vertex Q2 branch rooted at its
preleaf has

`A=(1,1), B=(1,1), C=infeasible`.

Adding a second private leaf makes that root a strong support and changes the signature to

`A=(1,1), B=(2,1), C=infeasible`.

The A/B tie that generated two local choices is destroyed.

Therefore Taletskii-style smaller replacements cannot in general be padded arbitrarily.  To turn
one into an exact same-order theorem, the replacement must either carry a pre-existing
strong-support bank or be accompanied by another independently proved neutral compensation
operation.

## 7. Empty vertices and S-decomposition

The sharper context language does not remove Taletskii's no-empty hypothesis.

For the whole tree rerooted at a vertex (v), “empty/excluded” means the B-state beats A.  The
rooted inequality (A<=B+1) then forces the exact normalized gap (d_B=-1).  But (d_B=-1)
is precisely a context-active low state in the quotient above; the (E0) and (E1) contexts can
observe it.

Thus empty-vertex behavior is not an artifact of abstract contexts that disappears in the true
tree-context quotient.  TF19 has no same-order transformation eliminating every empty vertex.
Taletskii's S-decomposition and its bounded-part theorem therefore remain conditional on the
no-empty hypothesis and do not yet yield a complete exact-order rooted grammar.

The strong-support padding lemma can preserve a replacement gain when a forcing bank is already
present, but it does not manufacture such a bank without potentially changing the multiplicity
mechanism.  Q2 is the smallest explicit warning.

## 8. PPV terminal restrictions under the order objective

The exact quotient clarifies the two principal published gadgets without transferring the
Petr--Portier--Versteegen minimal-counterexample restrictions.

Q2 has

`A=(1,1), B=(1,1), C=infeasible`,

so its B coordinate is tied with A and its C coordinate is context-dead.

The five-vertex PPV terminal branch Q5 has

`A=(2,1), B=(2,2), C=(2,2)`,

so both B and C are tied and context-active.  Its five-versus-three behavior is therefore genuinely
visible in different lower faces.

The two gadgets have different exact context interfaces.  No universal replacement from one to
the other follows merely from their vertex/multiplicity ratios.  PPV's terminal-degree restrictions
are still proved for a fixed-domination-number/strong-support extremal functional, not for (M_n).
TF19 therefore does not import those restrictions unchanged.

## 9. Burned-order diagnosis

Only after the reverse-message theorem, three-pattern theorem, quotient, dominance rule, and
padding lemma were fixed did TF19 apply them to burned orders 1--14.

The deterministic reproducer is `experiments/tf19_tree_context_diagnosis.py`.  It refuses any
`max_order` above 14.  The burned census is used only to measure how much the proved quotient
compresses previously exposed interfaces and to locate exact same-order examples of that
compression.  It is not used to infer stabilization or to fit a recurrence.

The exact burned counts are recorded by the deterministic CI artifact and summarized here after
validation.

| n | projective interfaces | context interfaces | face profiles | weak context-undominated | strict context survivors |
|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 | 1 | 1 |
| 2 | 1 | 1 | 1 | 1 | 1 |
| 3 | 2 | 2 | 2 | 2 | 2 |
| 4 | 4 | 4 | 4 | 4 | 4 |
| 5 | 9 | 9 | 6 | 7 | 7 |
| 6 | 18 | 14 | 6 | 7 | 8 |
| 7 | 38 | 28 | 6 | 11 | 13 |
| 8 | 70 | 49 | 6 | 11 | 15 |
| 9 | 139 | 91 | 6 | 15 | 16 |
| 10 | 264 | 173 | 6 | 21 | 24 |
| 11 | 501 | 317 | 6 | 19 | 20 |
| 12 | 965 | 607 | 6 | 31 | 35 |
| 13 | 1827 | 1137 | 6 | 25 | 27 |
| 14 | 3474 | 2126 | 6 | 44 | 49 |

At order 14 the proved context quotient reduces 3,474 TF18 projective interfaces to 2,126 exact
context interfaces; within the six observed lower-face profiles only 44 are weakly
context-undominated under the proved face-preserving count preorder.  This is substantial
compression, but the analytic (P_{3k}) family already proves that the exact quotient is infinite.

A same-order collapse occurs already at burned order 6: two rooted projective interfaces with the
same costs `(0,1,infeasible)` but B-state counts 1 and 4 both reduce to the context interface in
which A is uniquely active with count 1.  This is a concrete same-order witness that projective
state counts can retain information no genuine tree context can use.

No tree of order 15 or larger is used.

## 10. Literature audit

TF19 rechecked the sources already central to TF16--TF18:

- D. S. Taletskii, “On the Number of Minimum Dominating Sets in Trees,” *Mathematical Notes* 113
  (2023), 552--566;
- J. Petr, J. Portier and L. Versteegen, “On the number of minimum dominating sets and total
  dominating sets in forests,” *Journal of Graph Theory* 106 (2024), 976--993;
- J. D. Alvarado, S. Dantas, E. Mohr and D. Rautenbach, “On the maximum number of minimum
  dominating sets in forests,” *Discrete Mathematics* 342 (2019), 934--942;
- the current dominion-family work cited in TF18 as local forcing/recurrence examples.

A bounded 2025--2026 update search did not locate a stronger publication giving the exact
unrestricted fixed-order sequence (M_n) together with all extremizers.  This is only a bounded
search record.  It is **not** evidence of novelty or openness.

## 11. Finite-grammar and experiment decision

TF19 resolves the TF18 question at the boundary level:

- abstract projective offsets were too general;
- genuine tree contexts have exactly three normalized cost patterns;
- projective signatures are not minimal;
- the exact tree-context quotient is the three lower faces plus counts on context-active states;
- the quotient is Myhill--Nerode-style minimal for exact normalized ((gamma,zeta)) response;
- nevertheless that quotient has infinitely many classes, already on endpoint-rooted paths;
- strong-support padding is an exact vertex-budget compensator when a forcing bank already exists;
- arbitrary padding is false;
- no-empty reduction remains unproved;
- PPV terminal restrictions still do not transfer automatically to the fixed-order objective.

There is therefore no proved complete finite rooted grammar, no exact recurrence for all (M_n),
and no exact same-order normal form covering every rooted configuration.

TF19 freezes **no** scientific experiment.  In particular:

- prospective (M_{15}): **not derived**;
- prospective order-15 extremizer family: **not derived**;
- order 15 consumed: **no**;
- new experiment: **no**;
- candidate allocated: **no**;
- candidate registry changed: **no**;
- experiment registry changed: **no**;
- next candidate ID: **TF-001158**;
- default invariant changed: **no**;
- `minimum_dominating_set_count` remains non-default theorem/diagnostic machinery.

## 12. Recommended next session

The local rooted-interface programme has now reached a natural stopping point.

TF18 showed that raw projective signatures are infinite; TF19 shows that even the **minimal exact
tree-context quotient** remains infinite.  More burned state mining cannot repair that obstruction.
Any continuation of the unrestricted fixed-order problem should therefore begin from a genuinely
global structural theorem, not another local quotient.

A justified next session could ask one sharply different question: whether exact (n)-extremizers
must contain enough globally forced structure to provide strong-support compensation banks for all
rate-improving local replacements.  Such a theorem would have to be proved independently of finite
state counts.  If no route to that global forcing theorem emerges, the unrestricted
minimum-dominating-set multiplicity programme should remain paused rather than consume order 15.
