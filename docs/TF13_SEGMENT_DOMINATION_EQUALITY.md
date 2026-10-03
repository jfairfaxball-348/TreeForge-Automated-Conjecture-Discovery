# TF13 — fixed-segment domination equality audit

Date: 2026-10-03

TF13 continues the fixed-order/fixed-segment domination question after TF12 resolved the numerical
extremal values. It is an equality/classification session, not a conjecture-generation experiment.
All exhaustive computation in this record is restricted to the already burned unlabeled trees of
orders 1--14.

## Verified starting state and scientific boundary

TF13 starts from exact main commit
8d0c82567282d2bd2a3a571944cdf084e149439d, the TF12 merge commit for PR #18.
The exact TF12 PR head
fa23e7437ff61c491c5697e52bc4442bd2b63be4 passed Actions run 37112447566;
post-merge main passed Actions run 37112600371. The earlier PR-head run
37112335549 failed only on the already-recorded stale ceil call and had no scientific
consequence.

The TF12 invariant boundary is unchanged. segment_count remains the exact core invariant

q(T) = n(T) - n2(T) - 1,

with the K1 convention q=0, and its degree-count implementation remains independently checked
against explicit maximal degree-2-path decomposition. The candidate registry remains at
TF-001157, so TF-001158 remains next. No TF5--TF13 scientific experiment record is
created, no TF13-0001 exists, the TF4 MIS fan stays archived, the TF7--TF9 fixed-support
thread stays closed, and no tree of order at least 15 is inspected.

## TF12 numerical theorem retained unchanged

For q>=3, let

a(q) = ceil((q+3)/2).

The reduced tree obtained by suppressing every degree-2 vertex has q edges and q+1 vertices.
If L is the number of leaves and B the number of branching vertices, then

L+B=q+1,  a(q)<=L<=q,  and  n2=n-q-1.

TF12 established, from published stronger extremal results plus these elementary reductions,

gamma_min(n,q) = ceil((n-q+2)/3)

and

gamma_max(n,q) =
min(floor(n/2), floor((n+q)/3), n-a(q)).

For q=1, T=P_n and both extrema are ceil(n/3). Segment count q=2 is impossible, and
(n,q)=(1,0) is K1. TF13 does not reinterpret these values.

## Minimum side: the rounded equality theorem is already published

### Lemańska gives only the real-equality slice

Lemańska, "Lower bound on the domination number of a tree", Discuss. Math. Graph Theory 24
(2004), 165--169, DOI 10.7151/dmgt.1222, proves for a tree of order n>=2 with L leaves

gamma(T) >= (n-L+2)/3.

The equality family is exactly the family R in which the distance between every pair of distinct
leaves is congruent to 2 modulo 3. In later notation this is G_0^0.

This does not by itself classify equality in the rounded integer bound
gamma(T)=ceil((n-L+2)/3). That distinction matters at fixed (n,q): ceiling slack can allow
L<q while still attaining the fixed-(n,q) minimum.

### Hajian--Henning--Jafari Rad close the rounding gap

Hajian, Henning and Jafari Rad, "A new lower bound on the domination number of a graph",
J. Combin. Optim. 38 (2019), 721--738, DOI 10.1007/s10878-019-00409-x, introduced the
tree families G_0^0, G_0^1 and G_0^2 in their rounded leaf-bound equality work.

Their later paper, "A Classification of Cactus Graphs According to their Domination Number",
Discuss. Math. Graph Theory 42 (2022), 613--626, DOI 10.7151/dmgt.2295, states the
classification in a form especially useful here. Theorem 1 says that if G is a cactus of order
n>=2, with k cycles and L leaves, and m>=0, then

gamma(G) = (n-L+2(1-k)+m)/3  if and only if  G is in G_k^m.

Specializing to k=0 gives an exact classification for every tree. The same paper records
G_0^0=R, so Lemańska's leaf-distance condition is exactly the m=0 member, not a description
of the m=1,2 rounded-slack classes.

### Exact fixed-(n,q) minimum class

Assume q>=3, put

M = ceil((n-q+2)/3),
r = 3M-(n-q+2), so r is in {0,1,2},

and let d=q-L be the leaf deficit from the largest fixed-q leaf count.

A tree with L=q-d can attain M only if its own rounded leaf lower bound equals M:

ceil((n-L+2)/3) = ceil((n-q+2+d)/3) = M.

This is equivalent to 0<=d<=r. Feasibility also requires L>=a(q), equivalently
d<=q-a(q). For such a tree,

m = 3M-(n-L+2) = r-d.

Applying the published tree classification gives the complete iff statement.

**Fixed-segment minimum equality theorem.** Let T be a tree with q(T)=q>=3, order n, and
M=ceil((n-q+2)/3). Put r=3M-(n-q+2) and a=ceil((q+3)/2). Then gamma(T)=M if and only
if there is an integer d with

0 <= d <= min(r,q-a)

such that L(T)=q-d and T belongs to G_0^(r-d).

Equivalently:

- if n-q+2 is 0 modulo 3, only (L,m)=(q,0) occurs;
- if n-q+2 is 2 modulo 3, the possible classes are (q,1) and (q-1,0), subject to feasibility;
- if n-q+2 is 1 modulo 3, the possible classes are (q,2), (q-1,1), and (q-2,0), subject to feasibility.

Thus a star skeleton is not necessary. TF12's subdivided star was an attainment construction,
not an equality classification. Non-star reduced trees occur among minimizers already in burned
data. Nor does the leaf-distance condition alone describe all fixed-(n,q) minimizers: it is exactly
the residual m=0 slice.

TF13 minimum status: **DIRECT_COROLLARY_OF_PUBLISHED_CLASSIFICATION**.

This is a short fixed-segment specialization of a stronger published tree classification and does
not warrant a separate theorem project.

## Maximum side: exact leaf optimizer

Gentner, Henning and Rautenbach, "Largest domination number and smallest independence number of
forests with given degree sequence", Discrete Appl. Math. 206 (2016), 181--187,
DOI 10.1016/j.dam.2016.01.040, Theorem 3, determine the maximum domination number among
all forest realizations of a fixed degree sequence. For a tree degree sequence with L leaves their
formula specializes to

F_n(L) = min(n-L, floor((n+L)/3)).

Their Lemma 2 constructs a canonical extremal realization in the L<=n-L regime, but neither that
lemma nor the proof of Theorem 3 states that every realization of an extremal degree sequence is
extremal.

Let M=gamma_max(n,q) and a=a(q). Since M is the maximum of F_n(L) over a<=L<=q,
F_n(L)=M exactly when both branches of the minimum are at least M. Therefore

L <= n-M  and  L >= 3M-n.

Hence the complete optimizing leaf-count set is

L_max(n,q) = { integer L : max(a,3M-n) <= L <= min(q,n-M) }.

This includes all ties and parity/modulo boundary cases; no single optimizer is silently chosen.

## Maximum side: exactly which degree sequences are capable

Fix q>=3 and an eligible leaf count L. Then

B=q+1-L  and  n2=n-q-1.

Write the B branch degrees as 2+e_1,...,2+e_B. The tree degree-sum identity gives

e_i>=1 and sum(e_i)=L-2.

Conversely, every multiset of B positive integers summing to L-2, together with L degree-1
entries and n-q-1 degree-2 entries, has positive total degree 2n-2 and is a tree degree
sequence. Thus the admissible fixed-(n,q,L) degree sequences are characterized exactly by the
partitions of L-2 into B=q+1-L positive branch excesses.

If L is in L_max(n,q), the Gentner--Henning--Rautenbach maximum for each such degree sequence
is M. Therefore every admissible degree sequence at every optimizing leaf count has at least one
tree realization attaining the fixed-(n,q) maximum. Segment count is automatically preserved
because the number of degree-2 entries is fixed.

This completely classifies degree sequences capable of attaining the value. It does not classify
all tree isomorphism classes with those degree sequences.

## A complete structural branch: gamma = n-L

For trees of order at least three there is a simple iff statement.

**Lemma.** If T is a tree of order n>=3 with L leaves, then gamma(T)=n-L if and only if
every nonleaf vertex is a support vertex.

**Proof.** Let X be the set of nonleaves. It is always a dominating set, so gamma(T)<=n-L.

If some v in X is not a support vertex, then X without v still dominates T: every leaf retains
its support neighbor in the set, while v, being a nonleaf with no leaf neighbor, has a nonleaf
neighbor in the set. Hence gamma(T)<=n-L-1.

Conversely, if every nonleaf is a support, choose one leaf neighbor u_v for every v in X. The
pairs {v,u_v} are disjoint, and every dominating set must meet each pair to dominate u_v.
Thus every dominating set has size at least |X|=n-L. Together with the upper bound, equality
follows.

The bounded literature audit did not locate this exact iff statement as a named theorem. TF13
records it as an elementary derivation, not as a novelty claim. In the Gentner--Henning--Rautenbach
tree case L>n-L, their proof selects an extremal realization in which every nonleaf is a support,
consistent with the lemma.

## Why the complete maximum isomorphism class is still unresolved

The fixed-degree-sequence theorem is an attainment theorem, not an all-realizations theorem.
Burned data gives a minimal obstruction.

At (n,q)=(6,3), the degree sequence

(3,2,2,1,1,1)

has two nonisomorphic tree realizations. One has segment lengths (3,1,1) and domination number 2;
another has segment lengths (2,2,1) and domination number 3. The fixed-(6,3) maximum is 3.
Thus exactly the same degree sequence and segment count can contain both a maximizer and a
nonmaximizer.

Kurnosov, "The Set of All Values of the Domination Number in Trees with a Given Degree Sequence",
J. Appl. Ind. Math. 14 (2020), 131--147, DOI 10.1134/S1990478920010135, proves that the
possible domination values across tree realizations of a fixed degree sequence form an integer
interval and gives transformations reaching the maximum. The bounded audit did not locate in that
work an iff description of every maximum realization.

Adjacent results cover special branches: the classical gamma=floor(n/2) extremal problem is
characterized for connected graphs, hence trees; Favaron-type independent-domination bounds cover
real-equality versions of the (n+L)/3 expression; and Cabrera-Martínez (2024) characterizes sharper
support-structure upper-bound equality. The inspected statements do not provide a complete iff
classification for all tree realizations attaining the rounded floor((n+L)/3) branch needed here.

Accordingly TF13 does not assemble special cases into an unsupported global iff theorem.

TF13 maximum status: **PARTIALLY_RESOLVED**.

Precisely resolved:

1. the complete optimizing leaf-count set L_max(n,q);
2. the complete set of degree sequences capable of attaining the fixed-(n,q) maximum;
3. existence of a maximizing realization for every such sequence, from the 2016 theorem;
4. the exact tree-isomorphism condition on the gamma=n-L branch.

Still unresolved after the bounded audit:

an iff structural description of every tree realization attaining the rounded
floor((n+L)/3) branch, including ties, and therefore a complete all-isomorphism fixed-(n,q)
maximum classification.

This is a theorem/classification residue, not a justification for automated conjecturing.

## Burned-order falsification and interpretation checks

The deterministic TF13 reproducer recomputes only orders 1--14 and checks:

- all 5,447 burned unlabeled trees remain inside the declared data boundary;
- every fixed-(n,q) minimizer has exactly one arithmetic residual m in {0,1,2} allowed above;
- on burned minimizers, m=0 agrees exactly with Lemańska's leaf-distance 2 modulo 3 condition;
- non-star reduced-tree minimizers exist, falsifying the over-strong "subdivided star only" claim;
- every occupied fixed-(n,q) maximum has exactly the closed leaf-count interval L_max(n,q);
- for each optimizing leaf count, the maximizing degree-sequence set agrees exactly with the
  branch-excess partition description;
- for every burned tree of order at least three, gamma(T)=n-L iff every nonleaf is a support;
- mixed maximizing/nonmaximizing realizations of one degree sequence occur, with the smallest
  recorded obstruction at (6,3).

These are deterministic interpretation checks, not proofs of the infinite statements.

## Theorem significance and experiment decision

The complete minimum equality theorem is a short specialization of a published stronger
classification and stays in TreeForge. The maximum-side reductions are useful, but the principal
all-isomorphism classification remains incomplete. No theorem-focused repository is justified and
no novelty claim is made from a bounded negative search.

New scientific experiment frozen: **no**.  
TF13-0001 created: **no**.  
Scientific experiment executed: **no**.  
TxGraffiti discovery run: **no**.  
New candidate allocated: **no**.  
Candidate registry changed: **no**.  
Experiment registry changed: **no**.  
Next permanent candidate: **TF-001158**.  
TF4 MIS fan reopened: **no**.  
TF7--TF9 fixed-support thread reopened: **no**.  
Order 15 consumed: **no**.  
Orders at least 15 remain untouched: **yes**.

The unresolved equality question does not independently select one new experimental coordinate.
A reduced-tree/segment-length recurrence may eventually be useful, but choosing one now would add
representation choices before a theorem question has forced them. The experiment pause remains in
force.

## Next session recommendation

If the fixed-segment problem continues, remain theorem-first and focus only on the unresolved
maximum-realization question. Audit whether the rounded fixed-leaf upper branch has an existing
complete structural classification under another parameterization; if not, try to derive an iff
theorem for maximizing realizations using domination structure on the nonleaf core or a canonical
subdivision-state argument.

Do not inspect order 15, allocate TF-001158, or freeze a scientific experiment merely to search
for that proof structure.
