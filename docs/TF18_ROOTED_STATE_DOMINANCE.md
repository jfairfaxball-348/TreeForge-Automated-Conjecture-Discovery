# TF18 — rooted-state dominance for minimum-dominating-set multiplicity

Date: 2026-10-03

For a finite tree T, let `zeta(T)` be its number of minimum dominating sets and
`M_n=max{zeta(T): |V(T)|=n}`.

TF18 asks whether the exact TF17 three-state min-plus/count DP can be compressed, by theorem rather
than sequence fitting, into a finite rooted extremal system for the unrestricted order problem.

**Decision: useful exact replacement and state-translation lemmas are obtained, but no finite
extremal grammar is proved. The experiment pause is preserved and order 15 remains sealed.**
This is preferred end state **A** from the TF18 brief.

## 1. Provenance and boundary

TF18 starts from exact merged `main`

`7f5453c6923720da12764c62f83652d8c9d2182e`.

The requested TF17 provenance checks exactly:

- PR #23 exact head: `4e8e1887b9d9ff484361038ad8f7cbbedb9ac17f`;
- exact-head Actions run `37152917160`: successful at that head;
- merge / TF18 starting main: `7f5453c6923720da12764c62f83652d8c9d2182e`;
- post-merge Actions run `37153127056`: successful at the merge commit.

PR #23 changed exactly the intended ten TF17 files: CI, README/ROADMAP/HANDOVER/failure ledger,
the TF17 note, the exact DP, deterministic diagnosis, and its two test files. Candidate,
experiment, and default-invariant registries were not changed.

The live boundary also checks:

- candidate registry still ends at `TF-001157`; `TF-001158` remains next;
- last scientific experiment row remains `TF4-0001`;
- `minimum_dominating_set_count` remains non-default theorem/diagnostic machinery;
- orders 1--14 remain the burned universe;
- no order at least 15 is generated or inspected in TF18.

No discrepancy was found.

## 2. Exact rooted signatures

For a nonempty rooted tree R with root r,

`Sigma(R)=(A_R,B_R,C_R)`,

where each state is an exact `(cost,count)` pair or infeasible. Cost counts selected vertices
inside R, including r when selected; the attachment edge has no cost.

- A: r selected.
- B: r unselected and dominated by a selected child.
- C: r unselected, undominated below, and requiring its parent.

A leaf has `A=(1,1), B=infeasible, C=(0,1)`.

A selected parent sees `min(A,B,C)`. An unselected parent that still needs its own parent forces
every child to B. An unselected parent dominated below allows child states A/B and requires at
least one A. This is exactly the TF17 `N/Y` update. Hence the three states are a complete pendant
boundary interface.

Elementary consequences:

1. A is always feasible.
2. B is feasible iff the root has a child.
3. C is feasible for a leaf; for a nonleaf it is feasible iff none of its children is a rooted
   leaf.
4. If B is feasible, `cost(A)<=cost(B)+1`.
5. If C is feasible, `cost(A)<=cost(C)+1`.
6. If C is feasible at a nonleaf, `cost(B)<=cost(C)+1`.
7. If the root has t>=2 leaf children, `cost(B)-cost(A)>=t-1`.

The last statement is the state form of strong-support forcing: a B-solution contains all t leaves;
replace them by the root.

For the whole tree rooted at v, only A/B close globally. Writing `A=(a,alpha)`,
`B=(b,beta)`: v is in every gamma-set iff `a<b`, in no gamma-set iff `b<a`, and both kinds
exist iff `a=b`, when the total count is `alpha+beta`. This is the exact translation of
Taletskii's universal/empty terminology.

## 3. Normalization and projective dominance

Because A is always feasible, normalize by subtracting its cost:

`Delta_A=0`,
`Delta_B=cost(B)-cost(A)`,
`Delta_C=cost(C)-cost(A)`,

with an explicit infeasible marker. Keep the exact integer counts and separately retain the A
baseline and order. No floating-point count ratios are needed.

### Naive coordinatewise dominance is false

It is not safe to say that S dominates R merely because every state of S has no larger cost and at
least as many completions. Selectively lowering one state can destroy an optimum tie and reduce
zeta.

A same-order burned counterexample already occurs at order 8.

- R: spider with arm lengths (1,2,4), rooted at the internal vertex on the length-2 arm:
  `A=(3,1), B=(3,1), C=infeasible`, so closed profile `(gamma,zeta)=(3,2)`.
- S: spider with arm lengths (1,1,1,4), rooted at the penultimate vertex on the length-4 arm:
  `A=(2,1), B=(3,2), C=infeasible`, so closed profile `(2,1)`.

S has no larger state cost and no smaller state count, yet zeta drops from 2 to 1 because the
cheaper A state destroys the A/B tie.

### Projective replacement theorem

Say S **weakly projectively dominates** R when:

- the feasible-state patterns agree;
- one integer q satisfies
  `cost_S(X)=cost_R(X)+q` for every feasible X in {A,B,C};
- `count_S(X)>=count_R(X)` in every feasible state.

Equivalently, the normalized cost shapes are identical and S's exact count vector dominates R's.

**Theorem.** Under pendant replacement of R by S, every global boundary alternative receives the
same cost shift q. Therefore the set of boundary states tying for the global minimum is unchanged,
and zeta cannot decrease. If every feasible state count is strictly larger, zeta strictly increases
in every pendant context.

Proof: condition on the boundary state X. Let the outside conditional optimum be
`(k_X,l_X)`. R contributes cost `k_X+cost_R(X)` and multiplicity
`l_X*count_R(X)`. With S all conditional costs acquire the same q, preserving the argmin set,
while every multiplicity on that set is no smaller. QED.

Equal exact signatures are the q=0 equality case. Equal normalized signatures with equal counts
preserve zeta in every context but may shift gamma by the common baseline.

For fixed-order extremality, same-order strict projective dominance genuinely excludes the dominated
pendant gadget. A smaller gadget cannot be used this way without a separately proved operation that
spends the released vertices; this is the fixed-order obstruction behind several published
rate-improving replacements.

## 4. Exact repeated-child formula

Suppose a root has m>=1 identical children with

`A=(a,x), B=(b,y)`.

For the parent's B state (A/B children, at least one A):

- if `a<b`: `(m*a, x^m)`;
- if `a=b`: `(m*a, (x+y)^m-y^m)`;
- if `a>b`: `(a+(m-1)*b, m*x*y^(m-1))`.

This is the exact DP source of the powers appearing in the strongest published constructions.

## 5. Taletskii (2023) in DP language

Source: D. S. Taletskii, “On the Number of Minimum Dominating Sets in Trees,”
*Mathematical Notes* 113 (2023), 552--566,
DOI `10.1134/S0001434623030264`.

**Universal/empty vertices.** Rerooting at v translates them exactly to the A/B cost comparison
above. Taletskii's Lemma 3 and Corollary 1 replace such trees by a forest and then a smaller tree
with a better per-vertex multiplicity rate. This is appropriate for an exponential minimal
counterexample, but is not a same-n replacement theorem.

**Separability.** If adjacent supports/preleaves are joined by an edge, Taletskii's Lemma 4 shows
that cutting the edge preserves the gamma-sets. In DP terms the optimum is already internally
closed on both sides, so the cross-edge C channel is unused and the count factorizes. This is an
exact edge-decoupling certificate, not a unique local normal form.

**S-decomposition.** In a tree with no empty vertices, Taletskii's Lemma 6 gives a unique partition
into closed neighborhoods, every gamma-set choosing exactly one vertex per part. “No empty
vertex” translates to: after rerooting at every v, A has global optimum cost. Thus S(T) is a global
many-reroot certificate, not the signature of one pendant branch. Lemma 8 says that an exact
order-maximal tree **with no empty vertices** has S-parts of size at most three. The hypothesis does
not disappear, and the arrangement of those blocks is not reduced to finitely many rooted states.

**W branches.** A degree-2 preleaf with its leaf, rooted at the preleaf, has

`Q2: A=(1,1), B=(1,1), C=infeasible`.

A selected parent gets two choices per Q2 branch; an unselected parent that must be dominated by at
least one of m branches gets `2^m-1`. Applying this to the three-vertex W core gives exactly

`zeta(W_(a,b))=2^a(2^b-1)+2^(a+b)+2^b(2^a-1)`.

Thus the W formula is a direct repeated-signature evaluation.

Taletskii's W_(4,4) module and separable joining operation remain crucial order-growth mechanisms,
but his upper-bound replacements mix smaller-order rate improvements, S-structure, and
case-specific exponential comparisons. They do not prove a finite exact-order grammar.

## 6. Petr--Portier--Versteegen (2024) in DP language

Source: J. Petr, J. Portier and L. Versteegen,
“On the number of minimum dominating sets and total dominating sets in forests,”
*Journal of Graph Theory* 106 (2024), 976--993,
DOI `10.1002/jgt.23107`, arXiv `2206.13182`.

Their k-terminal vertices are the layers obtained by repeatedly deleting leaves. This is geometric
pruning depth, not an A/B/C state. Along a terminal path, however, it becomes iteration of one
unary signature map. If a new root is placed above one child,

`U(A,B,C)=((1,1)*min(A,B,C), A, B)`.

The length-two terminal branch is exactly Q2. Therefore their Claim 2.2 calculation with m such
branches has local B-count `2^m-1`, exactly the repeated-child formula.

More importantly, their final five-vertex terminal chain

`y-x-w-v-u`

rooted at y has signature

`Q5: A=(2,1), B=(2,2), C=(2,2)`.

A selected parent allows all three states, all tied at cost 2, for exactly `1+2+2=5` completions.
An unselected parent already dominated externally disallows C and sees `1+2=3` completions.
This gives a state-level derivation of their construction count `5^k+3^k`.

Their terminal degree restrictions are nevertheless conditional on a minimal counterexample for

`f(gamma,s)=max zeta among forests with domination number gamma and at least s strong supports`.

They decrease gamma and track strong supports. They are not unconditional forbidden signatures for
M_n. The contrast is explicit: a W_(4,4) endpoint has four Q2 branches plus its core neighbor, so
it is a 2-terminal vertex of degree five. That local pattern is excluded in their fixed-gamma
minimal counterexample but is part of Taletskii's higher order-growth construction.

## 7. Current dominion-family work as local test cases

TF18 also checked the 2026 dominion-family work of Allagan, Gray, Sawyer and Morgan
(arXiv:2601.03485) and the related journal article on dominion in trees. Its path-pendant forcing
dichotomy exactly matches the rooted mechanisms already isolated here: one private leaf per path
vertex gives independent two-way choices, while two or more private leaves make the support
universal/forced. The alternating-pendant families give Fibonacci recurrences because local choices
cease to be independent and must be propagated along the path.

These are useful exact regression families for any future rooted replacement theorem, but they are
family-specific recurrences rather than an unrestricted completeness result. Their forcing branch is
already covered by the strong-support state gap, and their one-pendant branch is the same pairwise
choice mechanism as coronas/Q2-style local interfaces. TF18 therefore records them as mechanism
checks, not as a new extremal grammar.

## 8. Burned rooted-state diagnosis

Only after the projective preorder was defined was it applied to orders 1--14. The deterministic
reproducer is `experiments/tf18_rooted_state_diagnosis.py`.

| n | exact signatures | projective interfaces | cost shapes | weak undominated | strict survivors |
|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 | 1 | 1 |
| 2 | 1 | 1 | 1 | 1 | 1 |
| 3 | 2 | 2 | 2 | 2 | 2 |
| 4 | 4 | 4 | 4 | 4 | 4 |
| 5 | 9 | 9 | 7 | 8 | 9 |
| 6 | 18 | 18 | 9 | 11 | 16 |
| 7 | 38 | 38 | 11 | 18 | 27 |
| 8 | 72 | 70 | 14 | 22 | 41 |
| 9 | 144 | 139 | 18 | 31 | 54 |
| 10 | 278 | 264 | 21 | 44 | 83 |
| 11 | 533 | 501 | 24 | 52 | 101 |
| 12 | 1035 | 965 | 28 | 74 | 154 |
| 13 | 1977 | 1827 | 33 | 80 | 174 |
| 14 | 3782 | 3474 | 37 | 119 | 268 |

The compression is substantial: 3,474 projective interfaces at order 14 reduce to 119 weakly
undominated interfaces. But 119 is not a finite-state theorem, and the number of normalized cost
shapes itself reaches 37 with no proved stabilization. The roots of the burned order-14
extremizers use only seven projective interfaces; that concentration is diagnostic only.

No order-15 tree or signature is used.

## 9. Analytic obstructions to raw finiteness

The nonstabilization is not purely empirical.

For a star with m leaf children rooted at its center,

`A=(1,1), B=(m,1), C=infeasible`,

so `Delta_B=m-1` is unbounded.

Even maximum degree two does not make exact counts finite. For the endpoint-rooted path P_(3k),
iteration of U gives, for k>=1,

`A=(k+1, k(k+3)/2), B=(k,1), C=(k,k)`.

The normalized cost shape is always `(0,-1,-1)`, but its exact count vector is unbounded.

These examples do not rule out a finite **symbolic** extremal recurrence. They show that such a
recurrence needs an additional structural theorem or aggregation; raw normalized signatures do
not become a finite universe by themselves.

## 10. Candidate compressions and decision

Rejected or incomplete routes:

- raw exact signatures: unbounded costs/counts;
- ordinary coordinatewise Pareto pruning: false by the order-8 tie-breaking counterexample;
- projective dominance: rigorous and useful, but leaves an unproved growing frontier;
- bounded S-parts: conditional/global, not a pendant completeness theorem;
- PPV terminal degree rules: tied to a different extremal functional;
- gadget menu Q2/Q5/W_(4,4): explains major mechanisms but lacks a theorem excluding all other
  undominated interfaces.

A bounded 2025--2026 update search located no stronger publication giving exact unrestricted M_n
and all extremizers. This is only a bounded-search status, never novelty evidence.

TF18 therefore ends in preferred state **A**:

- new scientific experiment: **no**;
- order-15 prediction: **no**;
- order 15 consumed: **no**;
- candidate allocated: **no**;
- next candidate ID: **TF-001158**;
- candidate registry changed: **no**;
- experiment registry changed: **no**;
- default invariant changed: **no**;
- `minimum_dominating_set_count` remains non-default.

## 11. Recommended next session

Do not inspect order 15.

If the line continues, TF19 should attack one of two sharply isolated theorem problems:

1. characterize which boundary cost-offset vectors are actually realizable by **tree contexts**,
   potentially allowing a stronger safe dominance relation than abstract projective equality; or
2. turn Taletskii-style smaller replacements into same-order replacements by proving an exact
   compensating operation that spends the released vertices while guaranteeing multiplicity.

If neither yields a completeness theorem, pause the unrestricted rooted-state line rather than
mine larger orders.
