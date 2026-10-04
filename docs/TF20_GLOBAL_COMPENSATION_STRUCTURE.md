# TF20 — global compensation and bankless structure

Date: 2026-10-04

For a finite tree (T), write

`zeta(T) = # {D subseteq V(T) : D is a minimum dominating set of T}`

and

`M_n = max {zeta(T) : T is a tree of order n}`.

TF20 begins after TF19 proved that the **minimal exact local tree-context quotient is still
infinite**.  The purpose of TF20 is therefore global: decide whether exact order-extremizers
nevertheless fall into a finite structural system because smaller replacements can be compensated
exactly, or because the trees without such compensation banks have a finite global grammar.

**Decision: TF20 proves two exact compensation theorems and a canonical representation of every
tree with no strong support, and it sharply restricts any exact extremizer that does contain a
strong support.  These results reduce the unresolved replacement problem to an exact one-vertex
deficit in the no-universal/empty-vertex class.  That residual class still has arbitrary marked-core
geometry, so no complete finite extremal grammar or prospective value of (M_{15}) is proved.
The experiment pause is preserved.**

This is preferred end state **A**, with a sharper residual obstruction than TF19.

## 1. Provenance and scientific boundary

TF20 starts from exact merged `main`

`f493a2ca380c9876c3687bbbf4a30a81f6ce6b52`.

The requested TF19 provenance checks exactly:

- TF19 PR #25 exact head:
  `57839138093b9a6da04d7f0e9e23069cf00be079`;
- exact-head Actions run `37181108083`: completed successfully at that exact head;
- TF19 merge / TF20 starting main:
  `f493a2ca380c9876c3687bbbf4a30a81f6ce6b52`;
- post-merge Actions run `37181221379`: completed successfully at the merge commit.

PR #25 changed exactly eight files: CI, README, ROADMAP, HANDOVER, the failure/lesson ledger,
the TF19 theorem/diagnosis document, the deterministic TF19 diagnosis, and its test file.  It
therefore made no candidate-registry, experiment-registry, default-invariant, or scientific-corpus
change.

The live repository boundary also agrees with the TF19 handover:

- the candidate registry still ends at `TF-001157`, so `TF-001158` remains next;
- the last scientific experiment row remains `TF4-0001`;
- `minimum_dominating_set_count` remains non-default theorem/diagnostic machinery;
- orders 1--14 remain the burned diagnostic universe;
- no tree of order at least 15 is generated or inspected in TF20.

No provenance discrepancy was found.

## 2. Definitions: structural banks and replacement banks

A **strong support** is a vertex with at least two leaf neighbours.  TF19 proved that adding any
number of additional private leaves to an already strong support preserves both `gamma` and
`zeta`.

TF20 uses two related notions deliberately.

A tree is **strong-banked** if it contains at least one strong support.  It is
**strong-bankless** if it contains none.

For a *particular pendant replacement*, a strong support is an **untouched replacement bank** only
when it lies outside the replaced gadget and at least two of its private leaf neighbours also lie
outside the gadget.  Thus a structurally strong-banked tree need not supply a bank for every
possible local replacement.

This distinction matters when one proves exact same-order replacement rather than merely counts
strong supports.

## 3. Exact banked same-order rooted replacement theorem

Let (T=C[R]) be a tree containing a pendant rooted gadget (R).  Suppose an untouched strong
support (v) lies in the outside context (C[-]).  Let (S) be another rooted gadget with

`|S| = |R| - d`,  where `d >= 0`.

Use the exact TF19 tree-context quotient.  For each of the three realizable outside cost patterns

`E0=(0,0,0)`, `E1=(0,0,1)`, `E2=(0,1,1)`,

let (F_i(R)) and (F_i(S)) be the exposed lower faces after A-normalization.

Assume:

1. (F_i(R)=F_i(S)) for (i=0,1,2);
2. on every state appearing in at least one of these faces, the exact state count of (S) is at
   least the corresponding count of (R).

Then for every genuine outside tree context,

`zeta(C[S]) >= zeta(C[R])`.

Moreover, if for each of E0, E1 and E2 at least one state on the corresponding winning face has a
strictly larger count in (S), while no active count decreases, then the inequality is strict for
every genuine outside context.

Let

`q = cost_A(S) - cost_A(R)`.

Every context optimum cost changes by exactly this common amount (q).  Thus

`gamma(C[S]) = gamma(C[R]) + q`,

while the multiplicity comparison above is independent of whether (q) is zero.  This separation is
important: the fixed-order objective (M_n) maximizes `zeta`, not `gamma`.

Finally attach exactly (d) new private leaves at the untouched strong support (v).  TF19
strong-support padding preserves `gamma` and `zeta` from the intermediate tree and keeps (v)
strong.  The resulting tree (T') therefore satisfies

`|V(T')| = |V(T)|`

and

`zeta(T') >= zeta(T)`,

with strict inequality under the strict-face hypothesis above.

This is the **banked same-order replacement theorem**.  It uses the exact TF19 context preorder;
projective equality is not required.

A smaller replacement is called **bankable** in TF20 only when these hypotheses and the untouched
vertex budget bank are both proved.

The deterministic TF20 diagnosis contains a weak exact bookkeeping example: a center-rooted
three-leaf star may be replaced by the context-equivalent center-rooted two-leaf star, releasing
one vertex, while an external untouched strong support absorbs that vertex.  Exact order and the
whole-tree ((gamma,zeta)) profile are preserved.

## 4. A global compensation theorem beyond strong supports

Strong-support padding is not the only exact way to spend released vertices.  Taletskii's forest
replacement framework yields a stronger global operation.

### Forest-budget compensation theorem

Let (T) be an (n)-vertex tree, and let (F) be an isolate-free forest of order (n-d) such
that

`zeta(F) > zeta(T)`

and

`Delta(F) <= Delta(T)`.

If (d=0), or if (d>=2), then (T) is not an exact (n)-vertex extremizer.

For (d=0), this is Taletskii's same-order forest-to-tree Lemma 5 directly.

For (d>=2), write

`d = 2a + 3b`

with nonnegative integers (a,b).  Such a representation exists for every integer at least two:
take (b=0) when (d) is even, and (b=1) when (d) is odd.

Form the isolate-free forest

`F* = F union a P2 union b P3`.

Then (|V(F*)|=n).  Minimum dominating sets multiply over forest components, while

`zeta(P2)=2`,  `zeta(P3)=1`.

Hence

`zeta(F*) = 2^a zeta(F) > zeta(T)`.

Because (d>=2) and (F) is isolate-free, the relevant (T) has maximum degree at least two,
and therefore

`Delta(F*) <= Delta(T)`.

Taletskii's Lemma 5 now reconnects this same-order isolate-free forest into an (n)-vertex tree
without decreasing its number of minimum dominating sets.  That tree strictly beats (T).

So **every strict smaller-forest improvement with deficit at least two is already convertible to
an exact same-order contradiction without any strong-support bank**.

The generic uncovered budget is exactly

`d=1`.

This is the central global reduction of TF20.

## 5. One-vertex compensation is genuinely different

There is no universal rule saying that one released vertex can be spent by attaching a leaf.

The TF19 example already gives

`zeta(P2)=2 > zeta(P3)=1`.

TF20 records a stronger example that is not confined to order two.  The path (P_4) has

`(gamma,zeta)=(2,4)`.

There are only two attachment orbits for adding one new leaf:

- attach at an endpoint, giving (P_5), with ((gamma,zeta)=(2,3));
- attach at an internal vertex, giving the degree-three tree with arm lengths (1,1,2), with
  ((gamma,zeta)=(2,2)).

Thus **every** one-leaf extension of (P_4) has strictly fewer minimum dominating sets.

Consequently a generic one-vertex neutral extension theorem is false.  Any successful
(d=1) compensation principle must use extra structure, pair two replacements, or compare a
nontrivial compensator together with its exact multiplicity effect.

## 6. Taletskii replacements audited for exact-order use

The relevant transformations in Taletskii's 2023 paper separate cleanly once exact vertex budget is
tracked.

| Source mechanism | Old/new order bookkeeping | Exact multiplicity status | TF20 exact-order status |
|---|---:|---|---|
| Lemma 3, universal vertex with (m) empty neighbours | delete all but one empty neighbour; (d=m-1) before stripping possible isolated components | strict smaller-forest improvement | bank-free same-order contradiction whenever effective (d>=2); (d=1) needs another bank/compensator |
| Lemma 3, empty vertex after assuming no universal vertices | delete the empty vertex; (d=1) | strict smaller-forest improvement, with unchanged domination number in Taletskii's proof | **precise unresolved one-vertex case** |
| Lemma 4, adjacent supports/preleaves | cut the edge; (d=0) | equality/factorization of gamma-sets | exact separability certificate, but not itself a strict improvement |
| Lemma 7, S-part size 4 | remove two vertices and add two leaves; net (d=0) | strict same-order forest improvement | exact same-order exclusion; no bank needed |
| Lemma 7, S-part size 5 | remove one vertex and add one leaf, with the stated edge change; net (d=0) | strict same-order forest improvement | exact same-order exclusion; no bank needed |
| Lemma 8, larger S-parts | builds a same-order comparison forest from P2/P7-type pieces | strict same-order forest improvement | exact same-order exclusion once the no-empty S-decomposition hypothesis is valid |
| Corollary/rate reductions used in the exponential upper bound | often pass to smaller components/trees | per-vertex or minimal-counterexample comparison | not automatically an absolute local TF19 improvement |

Two points follow.

First, the S-part-size-at-most-three theorem is stronger for exact order than TF18/TF19 had needed
to claim: the relevant size-four-and-larger exclusions are already same-order forest arguments.
They do **not** require strong-support padding.

Second, the principal remaining Taletskii reduction is not a large untracked deficit.  It is the
single-vertex deletion at an empty vertex after universal vertices have been excluded.

## 7. Empty vertices under the strong-banked / strong-bankless split

A strong support is universal: it belongs to every minimum dominating set.  Each of its private
leaves is empty.  Therefore

> every tree with no empty vertices is automatically strong-bankless.

This makes the two mechanisms structurally orthogonal.  Strong-support banking cannot be used to
*establish* Taletskii's no-empty hypothesis, because the existence of the bank itself creates empty
vertices.

The smallest exact warning is (P_3): its center is a strong support and its two leaves are empty.

### The no-universal empty-vertex move is exactly the one-vertex gap

Taletskii treats an empty vertex (u) after first assuming that no universal vertex exists.  In
that situation (u) cannot have a leaf neighbour: if a leaf (x) were adjacent to (u), every
minimum dominating set would have to contain (x), making (x) universal.

Hence deleting (u) creates no isolated vertex.  Taletskii's Lemma 3 gives an isolate-free forest
(T-u) with strict multiplicity improvement, but its vertex deficit is exactly one.

The same no-universal hypothesis also rules out every strong support.  Thus this (d=1) move occurs
**precisely where the TF19 strong-support bank is unavailable**.

This is the cleanest remaining global obstruction after TF20.

## 8. What exact extremizers with strong supports can look like

The preceding compensation theorem sharply restricts the strong-banked side.

### At most one strong support

Suppose an exact order-extremizer (T) had two distinct strong supports.  Choose one of them,
(v).  It is universal and has at least two empty neighbours.

Taletskii's universal-vertex surgery deletes all but one empty neighbour.

- If the effective deficit is at least two, the forest-budget compensation theorem gives a
  same-order strict improvement.
- If the effective deficit is exactly one, the other strong support survives untouched: it cannot
  be an empty neighbour of (v), and its private leaves are not deleted.  Padding one leaf at that
  surviving support restores the missing vertex without changing `zeta`, after which Taletskii's
  same-order forest-to-tree lemma again yields a strict (n)-vertex improvement.

Both cases contradict extremality.

Therefore an exact order-extremizer has **at most one strong support**.

### If a strong support exists, it is extremely rigid

Let (v) be the unique strong support of an exact extremizer.

Its private leaves are empty.  If (v) had three or more empty neighbours in total, Taletskii's
universal surgery would release at least two vertices and the forest-budget theorem would contradict
extremality.

Therefore (v) has exactly two empty neighbours.  Since it already has at least two private leaf
neighbours, it follows that:

- (v) has exactly two private leaves;
- those two leaves are its only empty neighbours.

Moreover (v) must be the **unique universal vertex**.  If another universal vertex existed, apply
the universal surgery there.  A deficit at least two is handled globally; a deficit one leaves
(v) as an untouched strong-support bank, again giving a same-order contradiction.

Thus every exact extremizer lies in one of two classes:

1. **strong-bankless**; or
2. a residual strong-banked class with exactly one strong support, exactly two private leaves there,
   that support the unique universal vertex, and those leaves its only empty neighbours.

This is a genuine global structural restriction.  It still does not prove that the residual
strong-banked class is empty.  (P_3) is a small exact extremizer in it.

## 9. Canonical structure of every strong-bankless tree

The strong-bankless class has a simple exact representation, although not a finite extremal grammar.

### Marked support-core theorem

Let (T) be a strong-bankless tree of order at least three.  Let (L) be its set of leaves and
let (M) be its set of support vertices.  Delete all leaves and let

`H = T - L`.

Then:

1. (H) is a tree with at least two vertices;
2. every vertex in (M) has exactly one private leaf in (T);
3. (M subseteq V(H));
4. every leaf of (H) belongs to (M);
5. (T) is recovered uniquely from the marked tree ((H,M)) by attaching exactly one new private
   leaf to every marked vertex.

Conversely, take any tree (H) with at least two vertices and any marked set

`L(H) subseteq M subseteq V(H)`.

Attach exactly one new leaf to each marked vertex.  The resulting tree is strong-bankless, and
deleting all of its leaves recovers exactly ((H,M)).

Proof of the forward direction is elementary.  With no strong support, every support has exactly one
leaf neighbour.  A leaf of (H) was not a leaf of (T), so it must have had exactly one deleted
leaf neighbour and is therefore marked.  The reconstruction is immediate.  The converse follows
because marking every leaf of (H) prevents any unmarked core leaf from remaining a leaf of the
expanded tree, while each mark receives exactly one private leaf.

The one-vertex tree and (P_2) are recorded as the two small exceptions to this deletion
description.

### Why this is not a finite grammar

The marked alphabet is finite — marked versus unmarked — but the core (H) is an arbitrary tree.
In particular its degree and geometry are unbounded.  For example, take an arbitrarily large star
as (H), mark every leaf, and attach one private leaf at each mark; the expanded tree has no strong
support while the core center has arbitrarily large degree.

The TF17 A/B/C recurrence computes ((gamma,zeta)) exactly from the decorated core, but its exact
state counts remain unbounded.  Thus the marked support-core theorem is a complete representation of
the strong-bankless class, **not** a finite extremal recurrence.

## 10. S-decomposition: now used at the correct boundary

If an exact extremizer has no empty vertices, Taletskii's S-decomposition applies legitimately.

His unique S-decomposition gives one chosen vertex from every S-part in every minimum dominating
set.  Lemma 8 then rules out S-parts of size at least four in a maximal (n)-tree.  An unrestricted
(M_n)-extremizer is certainly maximal inside the degree class determined by its own maximum
degree, so the conclusion applies.

Thus a no-empty exact extremizer has only S-parts of size two or three (apart from the trivial
one-vertex case).  Size-two parts are support/leaf pairs; size-three parts contain neither leaves
nor supports as recorded in Taletskii's decomposition theory.

This is useful global structure, but bounded part size does not bound the interaction graph of the
parts.  TF20 proves no restriction that turns all possible S-part arrangements into a finite
extremal grammar.

## 11. Compensation mechanisms attempted beyond strong supports

### Proved: P2/P3 forest budget

The forest-budget theorem is the principal new compensator.  It absorbs every deficit (d>=2)
globally and can even increase multiplicity by a factor (2^a).

### Rejected: arbitrary one-leaf padding

(P_2 -> P_3) and the stronger (P_4) extension example above show that a one-vertex leaf bank is
not universal.

### Rejected as neutral banks: Q2 and Q5

The rooted Q2 branch has

`A=(1,1), B=(1,1), C=infeasible`.

Adding a second private leaf forces its root and destroys the A/B tie, as TF19 already records.

The PPV five-vertex terminal branch Q5 has

`A=(2,1), B=(2,2), C=(2,2)`.

Its exact factor is context-dependent: a selected parent sees five tied completions, while an
unselected externally closed parent sees three.  Q5 is therefore not a one-vertex or context-neutral
bank.

### Possible but unproved: pair two one-vertex replacements

Two independent strict (d=1) reductions would release two vertices and hence fall under the
P2/P3 theorem.  What is missing is a theorem guaranteeing that two such reductions can be performed
simultaneously without destroying each other's strict comparison.  Separability can provide that in
specific configurations, but TF20 proves no universal pairing theorem.

## 12. Petr--Portier--Versteegen under exact order bookkeeping

Petr, Portier and Versteegen prove a fixed-(gamma), strong-support-sensitive extremal bound.
Their terminal reductions repeatedly delete local branches and compare the remaining forest through
an inductive functional (f(gamma,s)).

That is not the premise of the TF20 forest-budget theorem.  TF20 needs an **absolute**
multiplicity improvement `zeta(F)>zeta(T)` before spending the order deficit.  PPV's claims instead
bound different classes after changing (gamma) and the number of strong supports.

For example, Claim 2.2 restricts 2-terminal branching inside a minimal counterexample to their
fixed-(gamma) functional; it does not supply a smaller forest with strictly larger absolute
`zeta`.  Later terminal claims have the same issue.  Their Q5 calculation is exact and useful as
state accounting, but its 5-versus-3 factors are boundary-state dependent.

Consequently neither strong-support banking nor the P2/P3 global compensation theorem imports the
PPV terminal restrictions unchanged into (M_n).

## 13. Burned-order diagnostics after theorem definitions

Only after the banked theorem, forest-budget theorem, one-vertex obstruction, and marked-core
representation were fixed did TF20 inspect burned orders 1--14.

The deterministic reproducer is
`experiments/tf20_global_compensation_diagnosis.py`.  It refuses every order above 14.

The burned census is used only to check the proved marked-core representation and to describe how
the already-known burned extremizers fall across the structural split.  In particular:

- every strong-bankless burned tree satisfies and reconstructs from the marked support-core theorem;
- among the 32 already-burned extremizers through order 14, only (P_3) is strong-banked; the
  other 31 are strong-bankless;
- the absence of larger burned strong-banked extremizers is **not** promoted to a threshold theorem;
- the P4 one-vertex-extension counterexample is checked exactly;
- all budget deficits (2,...,14) are mechanically decomposed as (2a+3b).

These are diagnostics and regression checks only.  No order-15 object is constructed.

## 14. Candidate global grammars and why they remain incomplete

**Finite marked support core.**  Rejected as a finite grammar.  The representation is exact but the
core is an arbitrary tree with unbounded degree and topology.

**S-parts of size at most three.**  Legitimate after no-empty is proved, but the interaction graph
of parts remains unbounded and no extremal recurrence over those interactions is proved.

**Strong-banked normal form.**  Greatly narrowed: at most one strong support, exactly two private
leaves if it exists, and a unique universal vertex.  The residual class is not eliminated.

**W/Q2/Q5 module menu.**  These modules explain important multiplicative mechanisms but there is no
theorem that every strong-bankless exact extremizer decomposes into them.

**PPV terminal grammar.**  Rejected for the exact-order objective because the terminal restrictions
are conditional on a different fixed-(gamma)/strong-support extremal functional.

**One-vertex extension recurrence.**  Rejected in generic form by (P_2) and (P_4).

The infinite TF19 local quotient is therefore not repaired or reopened.  TF20 instead isolates the
remaining global obstruction as a specific budget-one problem.

## 15. Literature checked

TF20 returned to the exact replacement proofs rather than relying on their asymptotic summaries.

- D. S. Taletskii, **“On the Number of Minimum Dominating Sets in Trees,”**
  *Mathematical Notes* 113 (2023), 552--566,
  DOI `10.1134/S0001434623030264`.
  TF20 audited the universal/empty reductions, separability, S-decomposition, same-order S-part
  replacements, and forest-to-tree maximality lemma.

- J. Petr, J. Portier and L. Versteegen,
  **“On the number of minimum dominating sets and total dominating sets in forests,”**
  *Journal of Graph Theory* 106 (2024), 976--993,
  DOI `10.1002/jgt.23107`.
  TF20 rechecked the terminal claims against their actual minimal-counterexample functional.

- J. D. Alvarado, S. Dantas, E. Mohr and D. Rautenbach,
  **“On the maximum number of minimum dominating sets in forests,”**
  *Discrete Mathematics* 342 (2019), 934--942,
  DOI `10.1016/j.disc.2018.11.025`, as background for the earlier fixed-(gamma) line.

A bounded current search through 2025--2026 follow-up terminology did not locate a publication
giving the exact unrestricted fixed-order sequence (M_n) and all extremizers.  As throughout
TreeForge, this is only a bounded-search status and is **not** evidence of novelty or openness.

## 16. Exact negative lessons

TF20 preserves the following failures rather than hiding them.

- Arbitrary leaf padding is false: (P_2) to (P_3) lowers `zeta`.
- The failure persists at a less exceptional size: every one-leaf extension of (P_4) lowers
  `zeta` from 4 to at most 3.
- Creating a strong support from Q2 destroys its multiplicity-generating A/B tie.
- “Banked extremizer implies no empty vertices” is directionally impossible: a strong-support bank
  itself forces empty private leaves.
- A finite marked alphabet does not make the arbitrary marked core a finite extremal grammar.
- Bounded S-part size does not imply finitely many whole-tree arrangements.
- PPV terminal restrictions do not become exact-order forbidden configurations merely because
  released vertices can sometimes be compensated.

## 17. Experiment and holdout decision

TF20 does **not** satisfy the prospective-freeze requirements.

There is no proved complete global replacement closure: the no-universal empty-vertex move produces
a strict isolate-free smaller forest with exact deficit one, precisely in a class with no strong
support bank.  The canonical strong-bankless representation does not collapse that class to a
finite grammar.

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
- `minimum_dominating_set_count` remains non-default theorem/diagnostic machinery.

## 18. Recommended next session

If the unrestricted multiplicity programme continues, the next theorem session should attack only
the **one-vertex deficit** left by TF20.

The cleanest target is the strong-bankless, no-universal class containing an empty vertex.  Possible
proof routes are:

- show that two (d=1) empty-vertex reductions can always be made independently or separated, so
  their deficits combine to two;
- prove a one-vertex compensator for the restricted marked-core configurations created by
  Taletskii's empty-vertex deletion, rather than for arbitrary trees;
- prove that an exact extremizer in the residual class cannot have exactly one usable empty
  reduction; or
- if all such routes fail under exact accounting, record the one-vertex obstruction as the natural
  stopping point and pause the unrestricted programme.

Do not return to finer local A/B/C quotient mining, do not fit (M_1,...,M_{14}), and do not
inspect order 15 without a complete prospective theorem.
