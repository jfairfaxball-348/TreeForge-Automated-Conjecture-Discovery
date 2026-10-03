# TF12 — segment/domination diagnosis

TF12 develops the question selected in TF11 without reopening automated conjecturing:

> For finite trees (T) of order (n) with exactly (q) segments, what are the minimum and
> maximum possible domination numbers (gamma(T)), and which trees attain each extremum?

The outcome is deliberately **not** a new discovery experiment. A deeper prior-art check exposes
stronger published results that determine both numerical extremal values after an elementary
fixed-segment reduction. The complete fixed-((n,q)) equality classes are not located in the
bounded search. TreeForge therefore keeps the experiment pause rather than spending order 15 on an
already-resolved numerical surface.

## Verified starting state

TF12 starts from merged TF11 main
`ca3d12661c6c6260b7489f8b9efb94416e698452`. PR #17 is merged; its exact head is
`6d48ba673b0a06917c2f49b3098ab374e158efcd`, exact-head CI
`37109771347` passed, and post-merge CI `37109895238` passed.

The registry boundary is unchanged at entry: TF-001028 is revision-7 `KNOWN_RESULT`;
TF-001034 and TF-001037 are revision-6 `ARTIFACT_OF_FEATURE_SET`; TF-001091 and
TF-001095 are revision-5 `ADVERSARIAL_PASSED`, as are the other sixteen active TF4 MIS
survivors. TF-001157 is the highest allocated candidate and TF-001158 is next. Exactly one
`TF4-0001` experiment record exists and no TF5--TF11 scientific record exists. No
`TF10-0001` or `TF11-0001` scientific spec exists.

Orders 1--14 are burned. No order at least 15 is generated or inspected in TF12.

## Exact segment invariant

For a finite tree (T), let (n_2(T)) be the number of degree-2 vertices. TF12 adds the exact
core invariant

[
q(T)=operatorname{segment_count}(T)=|V(T)|-n_2(T)-1.
]

For (K_1) this is 0. For every nontrivial path it is 1. For a nontrivial star it is its number
of leaves. Equivalently, it is the number of edges of the tree obtained by suppressing every
degree-2 vertex.

The production implementation uses the degree-count formula. An independent checker explicitly
traverses every maximal path whose endpoints have degree different from 2 and whose internal
vertices have degree 2. The two implementations agree on all 5,447 burned unlabeled trees of orders
1--14. Named regression tests include (K_1), (K_2), paths, stars, double-stars, spiders,
subdivided spiders/stars, caterpillars, adjacent branching vertices, and unequal degree-2 chains.
Repeated subdivision of an edge is also checked to leave (q) unchanged.

No segment sequence, residue statistic, reduced-tree code, or segment-length vector is promoted to
the invariant registry.

## Fixed-(q) elementary structure

Suppressing degree-2 vertices gives a reduced tree (H) with (q) edges and (q+1) vertices.
Its vertices are exactly the leaves and branching vertices of (T). If (L) is the number of
leaves and (B) the number of branching vertices, then

[
L+B=q+1,qquad
L=2+sum_{v:deg(v)ge3}(deg(v)-2).
]

Consequently:

- (q=0) occurs only for (K_1);
- (q=1) occurs exactly for nontrivial paths;
- (q=2) is impossible;
- for (qge3), every feasible tree has
  [
  leftlceilrac{q+3}{2}ightceille Lle q,
  ]
  and every integer in that interval is realizable by a reduced tree;
- the number of degree-2 vertices is fixed by ((n,q)):
  [
  n_2=n-q-1.
  ]

This reduction is the key to the prior-art implication.

## Deeper prior-art audit

### Lemańska (2004): leaf lower bound

Magdalena Lemańska, *Lower bound on the domination number of a tree*, Discussiones
Mathematicae Graph Theory 24 (2004), 165--169, DOI
`10.7151/DMGT.1222`, proves for an (n)-vertex tree with (L) leaves

[
gamma(T)ge rac{n+2-L}{3}
]

and characterizes equality. The 2023 domination monograph records the equality family as the trees
in which every pair of distinct leaves is at distance congruent to 2 modulo 3.

For fixed (qge3), (Lle q), so integrality gives

[
gamma(T)ge
leftlceilrac{n-q+2}{3}ightceil.
]

This value is attained by taking a (q)-leaf star as the reduced tree and placing all
(n-q-1) subdivision vertices on one arm. Thus the fixed-((n,q)) **minimum value** is a
direct consequence of published prior art plus an elementary attainment construction.

### Gentner--Henning--Rautenbach (2016): fixed-degree-sequence maximum

Michael Gentner, Michael A. Henning and Dieter Rautenbach,
*Largest domination number and smallest independence number of forests with given degree
sequence*, Discrete Applied Mathematics 206 (2016), 181--187, DOI
`10.1016/j.dam.2016.01.040`, gives a closed formula for the largest domination number among
forest realizations of a fixed degree sequence.

Specializing their Theorem 3 to a tree and writing (L) for the number of degree-1 entries yields

[
gamma_{max}(n,L)
=
minleft{n-L,leftlfloorrac{n+L}{3}ightflooright}.
]

Crucially, for a tree realization this maximum depends only on (n) and (L), not on the rest of
the degree sequence. Optimizing over the fixed-(q) feasible leaf interval gives, for (qge3),

[
gamma_{max}(n,q)
=
max_{lceil(q+3)/2ceille Lle q}
minleft{n-L,leftlfloorrac{n+L}{3}ightflooright}.
]

The increasing/decreasing two-branch envelope simplifies to

[
oxed{
gamma_{max}(n,q)=
minleft{
leftlfloorrac n2ightfloor,
leftlfloorrac{n+q}{3}ightfloor,
n-leftlceilrac{q+3}{2}ightceil
ight}.
}
]

Hence the fixed-((n,q)) **maximum value** is also already implied by stronger published
fixed-degree-sequence theory plus elementary optimization.

### Other directly adjacent literature

Gentner--Henning--Rautenbach,
*Smallest domination number and largest independence number of graphs and forests with given degree
sequence*, Journal of Graph Theory 88 (2018), 131--145, DOI
`10.1002/jgt.22189`, gives a closed formula for the smallest domination number among forest
realizations of a degree sequence. This is a strictly finer parameterization than fixed segment
count and confirms that degree-sequence methods are the correct neighboring literature.

A. D. Kurnosov, *The set of all values of the domination number in trees with a given degree
sequence*, Journal of Applied and Industrial Mathematics 14 (2020), 131--147, DOI
`10.1134/S1990478920010135`, proves that the domination values realized by trees with a fixed
degree sequence form the whole integer interval between the minimum and maximum. This is highly
relevant to structural realization, but it does not by itself classify all extremizers after
coarsening from a degree sequence to ((n,q)).

H. Aram, S. M. Sheikholeslami and O. Favaron,
*Domination subdivision numbers of trees*, Discrete Mathematics 309 (2009), 622--628, DOI
`10.1016/j.disc.2007.12.085`, studies when edge subdivision first raises domination and
characterizes the trees with subdivision number 3. Dettlaff--Raczek--Topp,
*Domination subdivision and domination multisubdivision numbers of graphs* (arXiv:1310.1345),
show that the domination multisubdivision number is at most 3 and equals the ordinary subdivision
number on trees. These results explain the mod-3 subdivision mechanism but do not state the
fixed-((n,q)) extremal classification.

**Bounded-search classification:** the numerical minimum and maximum values are **SETTLED AS
DIRECT CONSEQUENCES** of stronger literature plus elementary fixed-segment reductions. A complete
published characterization of **all** trees attaining the two fixed-((n,q)) envelopes was
**NOT LOCATED IN THE BOUNDED SEARCH**. This is not an openness or novelty claim.

## Exact numerical envelopes

The complete value formulas are therefore

[
gamma_{min}(n,q)=
egin{cases}
1,&(n,q)=(1,0),\
lceil n/3ceil,&q=1,\
lceil(n-q+2)/3ceil,&qge3,
end{cases}
]

and

[
gamma_{max}(n,q)=
egin{cases}
1,&(n,q)=(1,0),\
lceil n/3ceil,&q=1,\
min{lfloor n/2floor,lfloor(n+q)/3floor,
n-lceil(q+3)/2ceil},&qge3.
end{cases}
]

There is no (q=2) case.

The floor/ceiling terms explain the apparent mod-3 behavior seen under subdivision. No independent
residue coordinate is needed to state the value theorem.

## Burned-order structural diagnostics

The deterministic reproducer
`python -m experiments.tf12_segment_domination_diagnosis` recomputes exactly the 5,447
unlabeled trees of orders 1--14 and no others. It uses an independent three-state tree DP for
domination, cross-checked against the core exhaustive definition through order 8.

There are 80 occupied ((n,q)) cells. In every one:

- the computed minimum equals the formula above;
- the computed maximum equals the formula above;
- the leaf counts among maximizers are exactly the integer optimizers of the
  Gentner--Henning--Rautenbach leaf envelope;
- the formula-based segment count equals the explicit degree-2-path decomposition.

The reproducer emits the complete exact 80-cell table. Each row contains the tree count, minimum and
maximum domination values, numbers of minimizers and maximizers, a canonical representative of each
extremal class, its leaf/branch counts, its segment-length multiset, and its reduced-tree canonical
identity. This is burned-data interpretation and implementation validation, not theorem evidence.

For orientation, the order-14 slice is:

| (q) | min (gamma) | max (gamma) |
|---:|---:|---:|
| 1 | 5 | 5 |
| 3 | 5 | 5 |
| 4 | 4 | 6 |
| 5 | 4 | 6 |
| 6 | 4 | 6 |
| 7 | 3 | 7 |
| 8 | 3 | 7 |
| 9 | 3 | 7 |
| 10 | 2 | 7 |
| 11 | 2 | 7 |
| 12 | 2 | 6 |
| 13 | 1 | 6 |

No order-15 value, canonical structure, timing probe, or extremum is inspected.

## Subdivision diagnosis

For a fixed reduced tree (H) with (q) edges, choosing segment lengths is exactly assigning
positive integer lengths summing to (n-1). Subdivision changes (n) while leaving (q)
unchanged. The adjacent subdivision literature shows that one, two, or three subdivisions can be the
threshold for raising domination. The fixed-((n,q)) envelopes encode the resulting arithmetic
with floors and ceilings.

Burned data also show that reduced topology and segment-length distribution matter greatly to
**which trees** attain an envelope even after (n) and (q) are fixed. That is a reason not to
invent a scalar segment-sequence feature: the residual question is structural equality
classification, not an unexplained numerical fit.

## Representation-selection matrix

| Representation | Object | New vocabulary | Fit to mathematics | Main confounder | Decision |
|---|---|---|---|---|---|
| pairwise linear hull | linear inequalities in (gamma,n,q) | `segment_count` only | poor: exact values are piecewise floor/ceiling envelopes | would rediscover projections of known consequences | **REJECT** |
| exact conditioned envelope | exact min/max at each ((n,q)) | `segment_count` only | strongest natural value representation | values are already analytically resolved | **DEFER** as an experiment |
| residue-aware envelope | split by derived mod-3 data | no new primitive beyond (q) | arithmetic is real but already encoded by floors/ceilings | post-hoc residue grammar | **REJECT** |
| structural subdivision recurrence | reduced tree plus integer edge lengths | would require structural state/length data | strong for equality classification | changes several scientific axes before the residual question is isolated | **DEFER** |
| maintain experiment pause | no fresh-data model | `segment_count` retained as a core exact invariant | preserves the genuinely unresolved structural residue | none | **SELECT** |

No numerical scores or rankings are used.

The exact conditioned envelope is the correct **mathematical description of the value problem**.
It is not selected as a TreeForge experiment because prior art already determines it. The
structural recurrence route may become appropriate only if a subsequent equality-classification
audit isolates a precise theorem that is not already covered.

## TF12 decision

Scientific experiment frozen: **no**.

`TF12-0001` created: **no**.

TxGraffiti run: **no**.

Candidate ID allocated: **no**; TF-001158 remains next.

Candidate registry changed: **no**.

Experiment registry changed: **no**.

TF4 MIS fan reopened: **no**.

TF7--TF9 fixed-support thread reopened: **no**.

New core invariant: **yes, `segment_count` only**.

Fresh exhaustive order consumed: **no**. Orders at least 15 remain untouched.

The correct TF12 stopping point is therefore prior-art resolution of the numerical question plus a
preserved pause. A following session should audit the **complete equality classes** against
Lemańska's leaf-equality family and the structural fixed-degree-sequence extremizer literature. Only
if a precise residual characterization survives that audit should TreeForge consider a new
experiment, and order 15 should remain sealed until then.
