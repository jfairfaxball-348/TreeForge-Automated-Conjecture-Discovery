# TF21 — exact one-vertex compensation obstruction

Date: 2026-10-04

For a finite tree (T), write

`zeta(T) = # {D subseteq V(T) : D is a minimum dominating set of T}`

and

`M_n = max {zeta(T) : T is a tree of order n}`.

TF21 attacks only the one-vertex deficit left by TF20.  It does not reopen the
infinite local-interface problem, fit the burned extremal sequence, or inspect
order 15.

**Decision: TF21 proves an exact two-empty-vertex pairing theorem.  Hence a
no-universal exact order-extremizer has at most one empty vertex.  The remaining
one-empty case admits a sharp component decomposition and exact
product-minus-product formula, but it is still an unbounded global class.  In
particular, the subdivided-star family has a unique empty centre and an
arbitrarily large marked-core degree, while its Taletskii deletion improves
multiplicity by only one.  The smallest member is (P_5), which is itself the
exact order-5 extremizer, proving that a strict (d=1) deletion improvement
cannot always be converted into a strict same-order improvement.  The generic
replacement programme therefore stops at a genuine one-vertex obstruction
rather than yielding a complete finite grammar.  No experiment is frozen and
order 15 remains sealed.**

This is preferred end state **B/D** from the TF21 brief: pairing eliminates all
multi-empty residuals, but the rigorously isolated one-empty class remains.

## 1. Provenance and scientific boundary

TF21 starts from exact merged `main`

`4df7f281591d9a9a1f1a97ea0f86931236dcfd7a`.

The requested TF20 provenance checks exactly:

- TF20 PR #26 exact head:
  `83d4a4283452da534751bb301863169dd97f2e6b`;
- exact-head Actions run `37188803865`: completed successfully at that head;
- TF20 merge / TF21 starting main:
  `4df7f281591d9a9a1f1a97ea0f86931236dcfd7a`;
- post-merge Actions run `37207236838`: completed successfully at the merge
  commit.

Both green runs completed installation, unit tests, byte-compilation, Ruff
static analysis, deterministic calibration, every historical deterministic
diagnosis, and the TF20 global-compensation diagnosis.

The earlier PR-head run `37188758167` passed installation, unit tests, and
compile, then stopped at Ruff because of one unused import in the TF20
diagnosis.  Commit
`83d4a4283452da534751bb301863169dd97f2e6b` removed only that import.  This was
an implementation/static-check failure and had no scientific consequence.

PR #26 changed exactly:

- `.github/workflows/ci.yml`;
- `HANDOVER.md`;
- `README.md`;
- `ROADMAP.md`;
- `docs/FAILURE_AND_LESSON_LEDGER.md`;
- `docs/TF20_GLOBAL_COMPENSATION_STRUCTURE.md`;
- `experiments/tf20_global_compensation_diagnosis.py`;
- `tests/test_tf20_global_compensation_diagnosis.py`.

Thus neither registry nor the default invariant implementation changed.

The live boundary also agrees with TF20:

- the candidate history ends at `TF-001157`; `TF-001158` remains next;
- the last scientific experiment row is `TF4-0001`;
- `minimum_dominating_set_count` remains non-default theorem/diagnostic
  machinery;
- orders 1--14 remain the burned diagnostic universe;
- no order at least 15 is generated or inspected in TF21.

No provenance discrepancy was found.

## 2. Precise Taletskii (d=1) theorem

TF21 returns to Lemma 3 of D. S. Taletskii, *On the Number of Minimum
Dominating Sets in Trees*, Mathematical Notes 113 (2023), 552--566,
DOI 10.1134/S0001434623030264 (Russian original DOI 10.4213/mzm13571).

Use Taletskii's terminology:

- a vertex is **universal** if every minimum dominating set contains it;
- a vertex is **empty** if no minimum dominating set contains it.

Assume (T) has no universal vertices and (u) is empty.

Taletskii proves the following exact facts.

1. (u) has at least two nonempty neighbours
   (u_1,ldots,u_k), with (k>=2).
2. Let (T_i) be the component of (T-u) containing (u_i).
   Let (F_0) consist of all remaining components.  If (F_0) is nonempty,
   each of its components contains exactly one neighbour of (u), and that
   neighbour is empty in (T).
3. With (F=T-u),
   (Delta(F)<=Delta(T)) and
   (gamma(F)=gamma(T)).
4. The exact counts satisfy
   [
   zeta(F)=zeta(F_0)prod_izeta(T_i)
   ]
   and
   [
   zeta(T)=zeta(F_0)
   left(
      prod_izeta(T_i)
      -
      prod_izeta^-(T_i,u_i)
   ight),
   ]
   where (zeta^-(T_i,u_i)) counts minimum dominating sets of (T_i)
   omitting (u_i).
5. Every (u_i) is non-universal in (T_i), so every factor
   (zeta^-(T_i,u_i)) is positive.  Hence
   (zeta(F)>zeta(T)).

The order deficit is exactly one.

There are two elementary consequences worth making explicit.  First, an empty
vertex in a no-universal tree cannot have a leaf neighbour: that leaf would
have to occur in every minimum dominating set and would be universal.  Second,
(u) itself cannot be a leaf, for the same reason applied to its sole
neighbour.  Therefore (T-u) has at least two components and no isolated
vertices.

So the TF21 residual deletion forest is **always disconnected**.  The
connected (T-u) branch listed in the session brief is impossible under the
actual Taletskii hypotheses.

## 3. A general empty-deletion monotonicity lemma

The following elementary observation is used in the pairing proof.

**Lemma.** Let (G) be any graph and let (v) be empty.  Then

[
gamma(G-v)=gamma(G)
]

and every minimum dominating set of (G) is a minimum dominating set of
(G-v).  Consequently

[
zeta(G-v)>=zeta(G).
]

Proof.  Every minimum dominating set of (G) omits (v), so deleting (v)
does not destroy it as a dominating set of (G-v).  Hence
(gamma(G-v)<=gamma(G)).  If the inequality were strict, adjoining (v) to
a minimum dominating set of (G-v) would give a minimum dominating set of
(G) containing (v), contradiction.  The count injection is then
immediate.

Strictness is not automatic when universal vertices are present.  The
no-universal hypothesis in Taletskii's Lemma 3 supplies the strict first
deletion needed below.

## 4. Two-empty pairing theorem

This is the principal positive theorem of TF21.

**Theorem (two-empty pairing).** Let (T) be a tree with no universal
vertices, and let (u
e v) be empty vertices.  Then

[
F=T-{u,v}
]

is an isolate-free forest satisfying

[
|V(F)|=|V(T)|-2,qquad
Delta(F)<=Delta(T),qquad
gamma(F)=gamma(T),
]

and

[
zeta(F)>zeta(T).
]

### Proof that the second empty vertex survives the first deletion

Apply Taletskii's Lemma 3 at (u), and let (C) be the component of
(T-u) containing (v).

Suppose (v) were not empty in (C).  Then (C) has a minimum dominating
set containing (v).

Taletskii gives at least two nonempty neighbours of (u), each lying in a
different component of (T-u).  Choose one such neighbour (w) in a
component different from (C).  Because (w) is nonempty in (T), some
minimum dominating set of (T) contains (w).  Since (u) is empty and
(gamma(T-u)=gamma(T)), the restriction of that set to the component of
(w) is a componentwise minimum dominating set containing (w).

Now choose the assumed component minimum set containing (v), the component
minimum set containing (w), and arbitrary minimum sets in every other
component of (T-u).  Their union is a minimum dominating set of (T-u);
it contains (w), so it also dominates (u).  It is therefore a minimum
dominating set of (T) containing (v), contradicting that (v) is empty.

Thus (v) remains empty in its component after deleting (u).

Taletskii gives

[
zeta(T-u)>zeta(T).
]

Deleting the still-empty (v) cannot decrease multiplicity by the preceding
monotonicity lemma.  Hence

[
zeta(T-{u,v})>=zeta(T-u)>zeta(T).
]

The same argument preserves (gamma).

### Proof that the double deletion is isolate-free

If a vertex (x) became isolated after deleting (u) and (v), every
neighbour of (x) in (T) would lie in ({u,v}).

If (deg_T(x)=1), then (x) is a leaf neighbour of an empty vertex, which
would make (x) universal, impossible.

If (deg_T(x)=2) with (N_T(x)={u,v}), then every minimum dominating set
omits (u) and (v), so every one must contain (x) to dominate (x).
Again (x) would be universal.

No other degree is possible.  Therefore the double deletion is isolate-free.

### Exact-order consequence

The deficit is now (d=2).  TF20's forest-budget theorem applies directly:
add one (P_2) component and use Taletskii's same-order forest-to-tree
connection.  The resulting (n)-vertex tree has strictly more minimum
dominating sets.

Therefore:

> **Every no-universal exact order-extremizer has at most one empty vertex.**

No independence assumption between two Taletskii gains is used.  The first
deletion supplies the strict gain; the second is only required not to lose it.

## 5. Why the no-universal hypothesis is essential

The pairing theorem cannot be extended verbatim to the TF20 residual
strong-banked class.

The smallest exact witness is (P_3).  Its centre is universal and its two
leaves are empty.  It has profile

[
(gamma,zeta)=(1,1).
]

Deleting either one empty leaf gives (P_2), with profile ((1,2)), so the
one-vertex deletion is a strict improvement.  But deleting **both** empty
leaves gives (K_1), again with profile ((1,1)).  The second deletion
destroys the first gain.

Thus “two original empty vertices can always be paired” is false without the
no-universal hypothesis.

## 6. Exact structure when there is one empty vertex

Now assume (T) has no universal vertices and exactly one empty vertex (u).
Let the components of (T-u) be (T_1,ldots,T_k), rooted at the neighbours
(r_1,ldots,r_k) of (u).

Because (u) is the only empty vertex, Taletskii's (F_0) is empty.  Thus

[
gamma(T)=sum_igamma(T_i),
]

[
zeta(T-u)=prod_i zeta(T_i),
]

and

[
oxed{
zeta(T)=
prod_izeta(T_i)
-
prod_izeta^-(T_i,r_i)
}.
]

Every omitted-root factor is positive.

There is a stronger component restriction.

**Component-flexibility theorem.** Every vertex of every (T_i) is flexible:
it belongs to some, but not all, minimum dominating sets of (T_i).

Indeed, every minimum dominating set of (T) restricts to a minimum
dominating set in every (T_i), because
(gamma(T)=gamma(T-u)).

If a vertex were universal in some (T_i), it would occur in every minimum
dominating set of (T), hence would be universal in (T).  If it were empty
in (T_i), it would be omitted from every minimum dominating set of (T),
hence would be a second empty vertex of (T).  Both are impossible.

At each root (r_i), write the exact TF17 states as
((A_i,B_i,C_i)) and let (gamma_i=gamma(T_i)).  Flexibility gives

[
operatorname{cost}(A_i)=operatorname{cost}(B_i)=gamma_i.
]

Furthermore

[
operatorname{cost}(C_i)>=gamma_i
]

whenever (C_i) is feasible.  If some (C_i) had cost
(gamma_i-1), selecting the parent (u) would save one vertex in that
component and offset the cost of (u), making (u) nonempty.  With two such
components (u) would even become strictly preferred.  Since (u) is empty,
no such cheaper (C)-state exists.

This is exact A/B/C accounting inside the global decomposition, not a new
local quotient.

## 7. Marked support-core translation

TF20 gives every strong-bankless tree its canonical marked support core
((H,M)).

The unique empty vertex (u) is **unmarked**.  If it were marked, it would
have one private leaf (ell).  Since every minimum dominating set omits
(u), every minimum dominating set would have to contain (ell), making
(ell) universal, contradiction.

Every leaf of (H) is marked by TF20, so (u) is not a core leaf.  Hence

[
u
otin M,qquad deg_H(u)>=2.
]

Deleting (u) from the expanded tree gives exactly the flexible rooted
components described above.

This is considerably sharper than the raw marked-core representation, but it
does **not** bound the degree or geometry around (u).

## 8. An analytic unbounded one-empty family

Let (S_k) be the tree obtained from a (k)-leaf star by subdividing every
edge once, with centre (u), for (k>=2).

Equivalently, (u) is adjacent to (k) degree-two support vertices, each
having one private leaf.

Every minimum dominating set chooses exactly one vertex from each
support/leaf pair, except that the all-leaf choice is forbidden because it
does not dominate (u).  Therefore

[
gamma(S_k)=k,qquad
zeta(S_k)=2^k-1.
]

The centre (u) is the unique empty vertex.  Every other vertex is flexible,
there is no universal vertex, and there is no strong support.

Deleting (u) gives (kP_2), so

[
zeta(S_k-u)=2^k.
]

The Taletskii gain is therefore exactly **one**, and

[
rac{zeta(S_k-u)}{zeta(S_k)}
=
rac{2^k}{2^k-1}
longrightarrow 1.
]

In the marked support core, (H=K_{1,k}), the centre is unmarked, and all
(k) core leaves are marked.  Thus the unique-empty class has unbounded core
degree even under all TF21 restrictions.

This family is a counterexample to any claim that one empty vertex forces a
bounded local marked-core neighbourhood, and it also rules out compensation
arguments that require a fixed multiplicative margin.

It is **not** proposed as an infinite extremizer family.  For (k>=3), the
balanced Taletskii (W_{a,b}) of the same order (2k+1), with
(a+b=k-1), has

[
zeta(W_{a,b})
=
3cdot2^{k-1}-2^a-2^b
>
2^k-1.
]

So (S_k) is an analytic obstruction to a generic compensation proof, not an
extremal conjecture.

## 9. (P_5): exact obstruction to every universal (d=1) compensator

The case (k=2) above is (S_2=P_5).

It has

[
(gamma,zeta)(P_5)=(2,3),
]

while deleting its unique empty centre gives (2P_2) with

[
(gamma,zeta)(2P_2)=(2,4).
]

There are only three unlabeled trees of order five, and exact enumeration gives
(M_5=3), uniquely at (P_5).  Hence **no** operation can take this strict
four-vertex forest improvement and produce a five-vertex tree strictly
beating (P_5).

This is stronger than TF20's generic leaf-padding counterexample.  It occurs
inside the exact Taletskii deletion class and starts from an exact
order-extremizer.

Therefore the statement

> every strict Taletskii (d=1) deletion can be converted into a strict
> same-order tree improvement

is false without an explicit exceptional class.

## 10. One-vertex compensators audited

### Universal-vertex leaf bank: valid but unavailable here

There is a useful strengthening of TF19's padding idea.

**Lemma.** If (v) is universal in a tree (R), attaching one new leaf at
(v) preserves (gamma) and cannot decrease (zeta).

Every old minimum dominating set contains (v), so it remains a minimum
dominating set after the leaf is added.  A smaller dominating set in the
extended tree could be converted back to one in (R) by replacing the new
leaf by (v), contradiction.

This is a weak multiplicity bank; unlike strong-support padding it need not be
neutral.

However it is structurally unavailable in the unique-empty deletion forest:
the component-flexibility theorem proves that no component of (T-u) has a
universal vertex.  In particular no component has a strong support either.

Thus TF21 does **not** assume that a forced vertex is automatically a
strong-support bank.  It proves the weaker operation and proves why even that
operation cannot occur in the residual class.

### Reconnect first, then subdivide: false

For (P_5), the deletion forest is (2P_2).  Taletskii's separable
forest-to-tree connection can reconnect it as (P_4) without losing any of
the four minimum dominating sets.

Restoring the missing vertex by subdividing an edge gives (P_5), whose
multiplicity is only three.  Therefore “connect the forest and then subdivide
one edge” is not a neutral (d=1) principle.

### Manufacture a strong support: too expensive

Adding the missing vertex as a second private leaf to one (P_2) component
turns it into (P_3).  That changes the component multiplicity from two to
one.  On the (P_5) deletion forest this gives multiplicity two, already
below the original three.

The (S_k) family makes the general obstruction quantitative: the available
strict deletion gain can be only one, so any proposed compensator that loses
even one minimum dominating set cannot be justified merely from the fact that
Taletskii's gain is strict.

## 11. Direct connector-vertex accounting

Suppose an isolate-free forest has rooted components (R_i) with exact states
((A_i,B_i,C_i)), and add a fresh vertex (x) adjacent to every component
root.

The TF17 recurrence gives exactly

[
A_x=(1,1)otimesprod_i min(A_i,B_i,C_i),
]

[
C_x=prod_i B_i,
]

while (B_x) is the min-plus/count product over choices
(X_iin{A_i,B_i}) with at least one (A_i).

For the unique-empty deletion components, write

[
A_i=(gamma_i,alpha_i),qquad
B_i=(gamma_i,eta_i),
]

with (alpha_i,eta_i>0), and (C_i) not cheaper than (gamma_i).
Then

[
operatorname{cost}(B_x)=sum_igamma_i,
qquad
operatorname{cost}(A_x)=1+sum_igamma_i.
]

So (x) is empty and

[
operatorname{count}(B_x)
=
prod_i(alpha_i+eta_i)-prod_ieta_i.
]

This is exactly the one-empty product-minus-product formula above.

Thus using the released vertex merely as a new connector across all deletion
components reconstructs the same missing “all roots omitted” constraint.  It
does not recover the strict forest gain.

For (kP_2), every component has
(A=B=(1,1)) and (C) infeasible.  A single fresh connector adjacent to one
endpoint of every component therefore yields exactly (S_k) and exactly
(2^k-1) minimum dominating sets.  The connector loses precisely the one
all-leaf choice that deletion created.

This is the cleanest exact explanation of why the fresh vertex itself does
not generically solve the budget problem.

## 12. The connected deletion case is empty

Phase H of the TF21 brief asked for a separate analysis when (T-u) is
connected.

Under the actual residual hypotheses this case does not occur.  Taletskii
gives at least two nonempty neighbours of (u), and removing a vertex from a
tree separates different neighbours into different components.  Therefore

[
c(T-u)>=2.
]

No burned diagnostic is needed for this conclusion.

## 13. Consequences for S-decomposition

The two-empty theorem is enough to conclude:

- a no-universal exact extremizer has zero or one empty vertex;
- if it has zero, the TF20 no-empty S-decomposition analysis applies globally,
  including the already-audited exclusion of S-parts of size at least four;
- if it has one, deleting that vertex yields flexible components with no empty
  vertices, so each component individually admits Taletskii's
  S-decomposition.

The last point does **not** justify importing the size-at-most-three conclusion
componentwise.  Those components have not been proved maximal for their own
orders or degree classes, and the global tree still contains the empty hub.

Therefore TF21 does not obtain global no-empty structure and does not obtain a
finite recurrence from bounded S-parts.

## 14. Residual strong-banked class

TF20 proved that an exact extremizer with a strong support has exactly one
strong support (v), that (v) is the unique universal vertex, that it has
exactly two private leaves, and that those leaves are its only empty
neighbours.

TF21 does not collapse this class into the no-universal pairing theorem.
Taletskii's universal-vertex surgery with exactly two empty neighbours again
has deficit one.

The (P_3) calculation above proves why pairing the two empty private leaves
is invalid: the first deletion increases multiplicity, while deleting both
returns to multiplicity one.

Thus (P_3) remains a genuine small exact exception and the residual
strong-banked class remains separate.  Burned diagnostics from TF20 continue
to show no other strong-banked extremizer through order 14, but that finite
fact is not promoted to an all-order exclusion.

## 15. PPV audit

TF21 rechecked Petr--Portier--Versteegen's fixed-(gamma),
strong-support-sensitive terminal reductions against the sharper residual
structure.

No transformation located there becomes an absolute statement of the form

[
zeta(F)>zeta(T)
]

with a controlled (d=1) or (d=2) vertex deficit under the unique-empty
component hypotheses.  Their decisive comparisons still run through the
fixed-(gamma) inductive functional rather than an absolute multiplicity
improvement.

Accordingly TF21 imports no PPV terminal restriction into the unrestricted
fixed-order problem.

## 16. Burned diagnostics after the theorem statements

Only after the pairing theorem, unique-empty component theorem, marked-core
translation, and analytic counterexample family were fixed did TF21 inspect
orders 1--14.

The deterministic reproducer is
`experiments/tf21_one_vertex_compensation_diagnosis.py`, and it rejects every
requested exhaustive order above 14.

For the no-universal trees containing at least one empty vertex, the burned
census is:

| n | residual trees | exactly one empty | at least two empties | empty pairs checked |
|---:|---:|---:|---:|---:|
| 1--4 | 0 | 0 | 0 | 0 |
| 5 | 1 | 1 | 0 | 0 |
| 6 | 0 | 0 | 0 | 0 |
| 7 | 2 | 2 | 0 | 0 |
| 8 | 2 | 0 | 2 | 2 |
| 9 | 5 | 5 | 0 | 0 |
| 10 | 9 | 2 | 7 | 7 |
| 11 | 16 | 11 | 5 | 15 |
| 12 | 37 | 13 | 24 | 24 |
| 13 | 68 | 33 | 35 | 85 |
| 14 | 148 | 57 | 91 | 166 |

Every burned empty pair satisfies the proved double-deletion conclusion.
These checks are regression/falsification only.

Among already-burned exact extremizers, (P_5) is the only no-universal
extremizer with an empty vertex.  TF20's separate burned census already shows
that (P_3) is the only strong-banked extremizer through order 14.  Neither
finite observation is used to infer an all-order classification.

## 17. Global grammars considered

### “At most one empty vertex” as a finite grammar

Rejected.  It is a strong extremal restriction, but one empty vertex can sit
at the centre of the unbounded (S_k) marked cores, and its deletion
components can themselves be arbitrary flexible trees satisfying the root
state restriction.

### Product-minus-product hub grammar

Exact as a representation of the one-empty case, but not finite.  The rooted
component multiplicities ((alpha_i,eta_i)) are unbounded, the number of
components is unbounded, and the component geometry is not bounded.

### One fresh connector

Rejected as a compensation theorem.  The exact connector recurrence
reconstructs the forbidden all-roots-omitted term.  The (kP_2) family makes
the loss explicit.

### Strict-gain factor compensation

Rejected.  The (S_k) gain ratio tends to one, so no fixed multiplicative
loss can be absorbed from Taletskii's strict inequality alone.

### Reconnect then subdivide

Rejected by the exact (2P_2 -> P_4 -> P_5) calculation.

### Bounded local marked-core neighbourhood

Rejected analytically by the unbounded (K_{1,k}) marked cores.

The remaining class therefore needs a genuinely new global extremal theorem,
not another local state refinement and not another generic vertex-budget
identity.

## 18. Literature checked

TF21 rechecked:

- D. S. Taletskii, *On the Number of Minimum Dominating Sets in Trees*,
  Mathematical Notes 113 (2023), 552--566;
- J. Petr, J. Portier and L. Versteegen, *On the number of minimum dominating
  sets and total dominating sets in forests*, Journal of Graph Theory 106
  (2024), 976--993;
- J. D. Alvarado, S. Dantas, E. Mohr and D. Rautenbach,
  *On the maximum number of minimum dominating sets in forests*,
  Discrete Mathematics 342 (2019), 934--942;
- the 2026 dominion-family work already recorded by TF17--TF20.

A bounded 2025--2026 update search again did not locate a publication giving
the exact unrestricted fixed-order sequence (M_n) and all extremizers.
This is only a bounded-search record and is not evidence of novelty or
openness.

## 19. Experiment and programme decision

TF21 does **not** satisfy the prospective freeze requirements.

The pairing theorem is a substantial exact advance, but it leaves one empty
vertex.  That residual class is not finite, and (P_5) proves that the
remaining (d=1) improvement cannot always be converted into a strict
same-order improvement.

Therefore:

- prospective (M_{15}): **not derived**;
- prospective order-15 extremizer family: **not derived**;
- order 15 consumed: **no**;
- new scientific experiment frozen: **no**;
- candidate allocated: **no**;
- candidate registry changed: **no**;
- experiment registry changed: **no**;
- next candidate ID: **TF-001158**;
- default invariant changed: **no**;
- `minimum_dominating_set_count` remains non-default theorem/diagnostic
  machinery.

The unrestricted minimum-dominating-set multiplicity programme has reached a
natural replacement-theoretic stopping point.  TF17--TF20 remove every larger
generic budget and TF21 removes every multi-empty (d=1) configuration, but a
single empty hub can encode arbitrarily large flexible components and can be a
true exact extremizer at small order.

## 20. Recommended next session

Do not inspect order 15.

If this programme is continued at all, the only justified target is the exact
**unique-empty hub class** proved here:

- one unmarked internal empty vertex (u);
- every component of (T-u) entirely flexible;
- each attachment root has (A=B=gamma_i) and (C>=gamma_i);
- exact multiplicity
  (prod_i(alpha_i+eta_i)-prod_ieta_i).

A future theorem session should ask whether this class, together with the
separate TF20 strong-banked class, admits an independent global extremal
comparison that excludes all but a rigorously described finite exception
family.  It should not return to finer A/B/C quotients, sequence fitting, or
burned-state mining.

If no such global comparison is available, the unrestricted multiplicity
programme should remain paused/closed at the present theorem boundary.
