# TF14 — fixed-segment domination maximum-equality audit

Date: 2026-10-03

TF14 continues only the realization-level maximum-equality residue left by TF13. It is a structural
theorem and prior-art session, not a conjecture-generation experiment. Every finite diagnostic in
this record is restricted to the already burned unlabeled trees of orders 1--14.

## Verified starting state

TF14 starts from exact main commit
`8213e511715f478f7f0e94f89902e6aa076a4a15`, the TF13 merge commit for PR #19.

The verified TF13 provenance is:

- PR #19 merged;
- exact PR head `c48a2362ba4367278dc8b83469927edf10c5943d`;
- exact PR-head Actions run `37129172222`, successful;
- merge commit / starting main
  `8213e511715f478f7f0e94f89902e6aa076a4a15`;
- recorded post-merge Actions run `37129314891`, successful.

The append-only failure ledger retains the earlier TF13 workflow-YAML failure and exact-head Ruff
import-order failure `37116302326`; neither had scientific consequences.

At entry, `segment_count` is still the exact core invariant
`q(T)=n(T)-n_2(T)-1`, the candidate registry still ends at TF-001157,
TF-001158 is still next, and the experiment registry still contains no scientific row after
TF4-0001. There is no TF13-0001 or TF14-0001 scientific experiment. Orders at least 15 remain
untouched.

One materialization discrepancy was found during the required entry audit:
`experiments/TF13-DIAG-0001/diagnosis.json` is not committed at the verified TF13 main head,
although the deterministic TF13 reproducer is committed and exact-head CI ran it successfully and
uploaded its output as an Actions artifact. TF14 does not backfill or rewrite TF13 history. The
discrepancy has no mathematical consequence and TF14 commits its own deterministic diagnosis.

## TF13 result retained unchanged

For (qge3), put

[
a(q)=leftlceilrac{q+3}{2}ightceil
]

and

[
M=gamma_{max}(n,q)
 =minleft{leftlfloorrac n2ightfloor,
              leftlfloorrac{n+q}{3}ightfloor,
              n-a(q)ight}.
]

TF13 proved that the complete optimizing leaf-count set is

[
mathcal L_{max}(n,q)
=
left{Linmathbb Z:
max(a(q),3M-n)le Lle min(q,n-M)ight}.
]

For every such (L), the admissible fixed-((n,q,L)) degree sequences are exactly the
positive partitions of (L-2) into (B=q+1-L) branch excesses, together with
(n-q-1) degree-two entries and (L) leaves. Gentner--Henning--Rautenbach (2016),
Theorem 3, guarantees at least one realization attaining

[
F_n(L)=minleft{n-L,leftlfloorrac{n+L}{3}ightflooright}.
]

TF13 also proved for every tree of order at least three that

[
gamma(T)=n-L
quadLongleftrightarrowquad
	ext{every nonleaf vertex is a support vertex}.
]

The minimum-equality side remains completely resolved as a direct corollary of the
Hajian--Henning--Jafari Rad classification and is not reopened here.

## Realization-level audit of the fixed-degree-sequence proof

### Gentner--Henning--Rautenbach (2016)

Michael Gentner, Michael A. Henning and Dieter Rautenbach,
“Largest domination number and smallest independence number of forests with given degree
sequence”, *Discrete Applied Mathematics* 206 (2016), 181--187,
DOI `10.1016/j.dam.2016.01.040`.

The relevant statements are Theorem 3 and Lemma 2, together with the edge-switch claims in the
proof of Theorem 3.

For a tree degree sequence with (L) leaves, Theorem 3 yields the maximum value
(F_n(L)) above. Lemma 2 constructs a canonical maximum realization in the rounded regime:
each support has one leaf, the non-support nonleaves have degree two, and those vertices form a
path. The proof of Theorem 3 then chooses a maximum realization with secondary extremal choices
(number of (K_2) components and support vertices) and applies degree-preserving edge switches to
force useful structure.

This is an **existence/canonicalization proof**. Its switches do not establish that every maximum
realization has the canonical structure, and the proof contains no converse of the form “a
realization is maximum iff no switch applies”. TF13's mixed-degree-sequence example is therefore
fully consistent with the published proof.

### Kurnosov (2020)

A. D. Kurnosov, “The Set of All Values of the Domination Number in Trees with a Given Degree
Sequence”, *Journal of Applied and Industrial Mathematics* 14 (2020), 131--147,
DOI `10.1134/S1990478920010135`.

The relevant items are Theorem 3, Remark 1, Lemma 5 and Theorem 7.

Kurnosov's Theorem 3 gives the same fixed-degree-sequence maximum and records two **sufficient**
maximum-realization structures:

1. every nonleaf is a support vertex; or
2. every support has exactly one leaf neighbor, while the nonleaf non-support vertices all have
   degree two and induce a path.

Crucially, Remark 1 explicitly states that these sufficient conditions are **not necessary** and
gives an infinite maximum family outside them. In that family the non-support part may be a forest
of several paths, with an arithmetic condition
(sum_ilfloor s_i/3floor=lfloorsum_i s_i/3floor).

Lemma 5 introduces degree-sequence-preserving transformations whose effect on domination is bounded,
and Theorem 7 uses such transformations to prove that the domination values realized by a fixed
degree sequence form an integer interval. The terminal construction can be chosen to satisfy one of
Theorem 3's sufficient structures. These results do **not** characterize all maximum realizations
and do not turn “no applicable transformation” into a necessary-and-sufficient maximum criterion.

### Later fixed-degree-sequence work

S. A. Krupoderova and A. D. Kurnosov,
“On Relation between two Classes of Extremal Trees with Prescribed Degree Sequence”,
*Discrete Analysis and Operations Research* 32(2) (2025), 72--87; English version
*Journal of Applied and Industrial Mathematics* 19(2), 268--277,
DOI `10.1134/S1990478925020061`.

The located result compares support-vertex and **minimum-domination** extremizers in a prescribed
degree sequence. It does not provide the missing classification of maximum-domination realizations.

The bounded search also checked combinations of “maximum domination realization”, “fixed degree
sequence”, “prescribed leaves”, “tree transformations”, and equality in the
(lfloor(n+L)/3floor) bound. No later complete maximum-realization classification was located.
That negative result is not evidence that the problem is open or novel.

## The tie cases are already complete

TF13 described the residue as including the rounded branch “and ties”. The branch separation makes
the tie part immediate.

For an optimizing (L), write

[
A=n-L,qquad B=leftlfloorrac{n+L}{3}ightfloor.
]

If (A<B), the fixed-leaf maximum is (A=n-L). If (A=B), the same is true.
Therefore in both the strict (n-L) branch and the tie branch,

[
gamma(T)=F_n(L)
quadLongleftrightarrowquad
gamma(T)=n-L
quadLongleftrightarrowquad
	ext{every nonleaf is a support}.
]

Thus **ties are not part of the remaining TF14 obstruction**. They are covered exactly by the TF13
support lemma.

Status for the strict (n-L) and tie branches:
**TREEFORGE_ELEMENTARY_DERIVATION_FROM_PUBLISHED_RESULTS**.

## Strict rounded branch: reduction to independent domination

The only remaining leaf-level branch is

[
B=leftlfloorrac{n+L}{3}ightfloor<n-L=A.
]

Let (i(T)) be the independent domination number. Every independent dominating set is a
dominating set, so

[
gamma(T)le i(T).
]

Favaron proved for every nontrivial tree with (L) leaves that

[
i(T)lerac{n+L}{3}.
]

Since (i(T)) is integral,

[
i(T)le leftlfloorrac{n+L}{3}ightfloor=B.
]

Consequently the rounded fixed-leaf maximum has the exact realization-level reduction

[
oxed{
gamma(T)=B
quadLongleftrightarrowquad
gamma(T)=i(T)=B.
}
]

The forward implication is forced by
(gamma(T)le i(T)le B=gamma(T)); the reverse implication is immediate.

This is stronger than the canonical-construction description: it is an iff statement for **every**
realization. It does not yet give a purely local tree grammar because the right-hand side intersects
two equality problems.

### Published ((gamma,i))-tree classification

Cockayne, Favaron, Mynhardt and Puech,
“A characterization of ((gamma,i))-trees”, *Journal of Graph Theory* 34 (2000),
277--292, characterize exactly the trees satisfying (gamma(T)=i(T)).
Dorfling, Goddard, Henning and Mynhardt,
“Construction of trees and graphs with equal domination parameters”,
*Discrete Mathematics* 306 (2006), 2647--2654,
give a simpler constructive characterization of the same tree class.

Therefore the (gamma=i) half of the rounded equality problem is already published.

### Favaron equality and the residue-zero subcase

Favaron, “A bound on the independent domination number of a tree”,
*Vishwa International Journal of Graph Theory* 1 (1992), 19--27, proves

[
i(T)lerac{n+L}{3}
]

and characterizes all trees attaining **real equality**
(i(T)=(n+L)/3). The 2013 independent-domination survey and the 2023 domination monograph
explicitly record that the full equality list is contained in Favaron's proof.

Hence when

[
n+Lequiv0pmod3,
]

the strict-rounded maximum realization class is already exact:

[
oxed{
T	ext{ is a strict-rounded maximizer}
iff
T	ext{ is a Favaron equality tree and a }(gamma,i)	ext{-tree}.
}
]

This is a direct intersection of two published classifications.

Status for the strict-rounded residue-zero branch:
**DIRECT_COROLLARY_OF_PUBLISHED_CLASSIFICATIONS**.

### The actual remaining residue

If (n+Lequiv1) or (2pmod3), maximum realization requires

[
gamma(T)=i(T)=leftlfloorrac{n+L}{3}ightfloor,
]

but this is **not real equality** in Favaron's bound. The bounded audit located no theorem
classifying every tree satisfying this integer-rounded saturation condition.

The 2026 paper by Bujtás, Iršič Chenoweth, Klavžar and Zhang,
“Revisiting (d)-distance (independent) domination in trees and in bipartite graphs”,
*Discrete Mathematics* 349 (2026), article 114972,
extends Favaron's leaf bound to (d)-distance independent domination and again describes Favaron's
(d=1) predecessor in terms of trees attaining equality. It does not supply a residue-1/2
classification for integer saturation of Favaron's original (d=1) bound.

Thus the exact remaining literature-level question is:

> **Among the published ((gamma,i))-trees, characterize those with
> (i(T)=lfloor(n+L)/3floor) when (n+Lequiv1) or (2pmod3).**

Status:
**UNRESOLVED_AFTER_BOUNDED_AUDIT**.

This statement is intentionally narrower than TF13's residue.

## Exact support-core reduction

TF14 also gives an elementary structural normalization of the same residue.

Let

- (H) be the set of support vertices;
- (S) be the set of nonleaf non-support vertices;
- (h=|H|);
- (s=|S|);
- (delta=L-h), the number of leaves beyond one private leaf per support.

For a tree of order at least three, there is a minimum dominating set containing every support
vertex and no leaf: if a minimum dominating set uses leaves adjacent to a support, replacing the
necessary leaf choices by that support does not increase its size. Therefore define

[
	au_H(T)=
min{|X|:Xsubseteq S, Hcup X	ext{ dominates }T}.
]

Then

[
oxed{gamma(T)=h+	au_H(T).}
]

Because (n=L+h+s),

[
leftlfloorrac{n+L}{3}ightfloor-h
=
leftlfloorrac{s+2delta}{3}ightfloor.
]

Hence, on the strict rounded branch,

[
oxed{
T	ext{ is maximum}
iff
	au_H(T)=
leftlfloorrac{s+2delta}{3}ightfloor.
}
]

Equivalently, after support vertices are preselected, the unresolved problem is an equality
classification for a **partial domination problem on the forest (T[S])**: only core vertices not
already adjacent to (H) still require domination, and choices are restricted to (S).

This is an exact reduction, not a new discovery coordinate and not a claim that (	au_H) is a
satisfactory final classification. It explains two features that defeat overly simple candidates:

- (delta>0) creates integer slack from strong support vertices;
- (T[S]) need not be one path or even a linear forest.

Status of this reduction:
**TREEFORGE_ELEMENTARY_DERIVATION_FROM_PUBLISHED_RESULTS**.

## Burned-order falsification

The deterministic reproducer
`python -m experiments.tf14_segment_domination_maximum_equality`
uses only the 5,447 burned unlabeled trees of orders 1--14.

It independently computes (i(T)) by a rooted three-state dynamic program and checks
(gamma(T)le i(T)lelfloor(n+L)/3floor) for every nontrivial burned tree. It also
checks (gamma(T)=h+	au_H(T)) for all 5,445 burned trees of order at least three.

For (qge3), the burned fixed-cell maximizers split as:

- 39 in the strict (n-L) branch;
- 59 in the tie branch;
- 217 in the strict rounded branch.

The 217 strict-rounded maximizers split by ((n+L)mod3) as 49 / 119 / 49 for residues
0 / 1 / 2.

Kurnosov's two Theorem 3 sufficient forms cover only 56 of those 217 strict-rounded maximizers;
161 lie outside them. This is finite falsification of the over-strong “Theorem 3 forms are iff”
interpretation and is consistent with Kurnosov's own Remark 1.

Smallest burned witnesses to failed simplifications include:

1. **Kurnosov canonical form is not necessary.** At order 7, (q=3), (L=3), the tree with
   degree sequence ((3,2,2,2,1,1,1)) and segment lengths ((2,2,2)) has
   (gamma=i=3), the strict-rounded maximum. Its sole non-support nonleaf has degree 3,
   so it fails Kurnosov's degree-two core-path sufficient condition.
2. **One leaf per support is not necessary.** At order 8, (q=3), (L=3), a maximizer with
   segment lengths ((5,1,1)) has only two support vertices, hence
   (delta=L-h=1), while (gamma=i=3).
3. **The non-support core need not be a linear forest.** At order 10, (q=3), (L=3),
   the equal-arm subdivision with segment lengths ((3,3,3)) has
   (gamma=i=4); the induced non-support core contains a degree-3 vertex.

These examples are interpretation diagnostics from burned data, not evidence of novelty and not
proof of any infinite statement.

## Complete TF14 branch table

For (qge3), let (Linmathcal L_{max}(n,q)).

| leaf-level branch | realization condition | status |
|---|---|---|
| (n-L<lfloor(n+L)/3floor) | every nonleaf is a support | TREEFORGE_ELEMENTARY_DERIVATION_FROM_PUBLISHED_RESULTS |
| (n-L=lfloor(n+L)/3floor) | every nonleaf is a support | TREEFORGE_ELEMENTARY_DERIVATION_FROM_PUBLISHED_RESULTS |
| (lfloor(n+L)/3floor<n-L), (n+Lequiv0pmod3) | Favaron equality tree AND published ((gamma,i))-tree | DIRECT_COROLLARY_OF_PUBLISHED_CLASSIFICATIONS |
| (lfloor(n+L)/3floor<n-L), (n+Lequiv1,2pmod3) | equivalently (gamma=i=lfloor(n+L)/3floor), or (	au_H=lfloor(s+2delta)/3floor); no structural grammar located/proved | UNRESOLVED_AFTER_BOUNDED_AUDIT |

The full fixed-((n,q)) maximum equality theorem is therefore still **PARTIALLY_RESOLVED**, but
the unresolved portion is now only the strict-rounded residue-1/2 saturation problem.

## Theorem significance

TF14 does not justify a separate theorem repository.

The tie reduction is immediate from TF13. The residue-zero strict-rounded class is a short
intersection of published classifications. The support-core formula is useful and exact but
elementary; by itself it repackages the remaining condition as a partial-domination equality problem
rather than solving it.

A future complete residue-1/2 grammar could be mathematically interesting, especially if it is local
and constructive. Negative search alone does not support a novelty claim.

## Experiment decision and data boundary

New scientific experiment frozen: **no**.  
TF14-0001 created: **no**.  
Scientific experiment executed: **no**.  
TxGraffiti discovery run: **no**.  
New candidate allocated: **no**.  
Candidate registry changed: **no**.  
Experiment registry changed: **no**.  
Next permanent candidate: **TF-001158**.  
TF4 MIS fan reopened: **no**.  
TF7--TF9 fixed-support thread reopened: **no**.  
New invariant registered: **no**.  
Order 15 consumed: **no**.  
Orders at least 15 remain untouched: **yes**.

The support-core quantities in the reproducer are interpretation diagnostics only and are not added
to the invariant registry.

## Next-session recommendation

If this line continues, do not reopen the full fixed-segment question. Attack only the strict-rounded
residue-1/2 theorem:

> characterize ((gamma,i))-trees satisfying
> (i(T)=lfloor(n+L)/3floor) when (n+Lequiv1,2pmod3).

The most defensible proof routes are either:

- start from the published constructive grammar for ((gamma,i))-trees and track the Favaron
  integer slack through its operations; or
- prove an equality classification for the support-core partial-domination bound
  (	au_Hlelfloor(s+2delta)/3floor).

Continue to use orders 1--14 only as falsification. Do not allocate TF-001158, add a new invariant,
or inspect order 15 unless a later, independently justified experiment is first frozen.
