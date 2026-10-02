# TF8 fixed-support MIS equality characterization

TF8 refines the TF7 fixed-support theorem. It is a structural mathematics session using only
already exposed orders 1--14 for computational falsification checks. It does not freeze or execute
a new scientific discovery experiment, does not allocate a candidate ID, and does not inspect any
exhaustive tree of order at least 15.

## Verified starting state

TF8 starts from merged TF7 main commit
cdfa0cdd86aee25498c7315dfcb083cfb1c5a7c1. PR #13 is merged. Its exact PR head is
7f1bbe426e25837f41a53672844ffae5c21d3def; PR-head CI run 37050771524 and
post-merge main CI run 37050985352 are successful.

TF-001028 remains KNOWN_RESULT revision 7. TF-001034 and TF-001037 remain
ARTIFACT_OF_FEATURE_SET revision 6. TF-001091 and TF-001095 remain revision-5
ADVERSARIAL_PASSED. The other sixteen active members of the TF4 MIS fan likewise remain
revision-5 ADVERSARIAL_PASSED, so the latest fan is eighteen finite survivors plus two projection
artifacts. TF-001157 is still the highest allocated candidate and TF-001158 remains next.

The experiment registry still contains exactly one TF4-0001 row and no TF5, TF6, TF7, or TF8
scientific experiment row. Orders 1--14 and all earlier hostile/family material remain burned;
orders at least 15 remain untouched.

## TF7 theorem being refined

Write m(T) for the number of maximal independent sets, L(T) for the leaves, S(T) for the support
vertices, s(T)=|S(T)|, and i(F) for the number of all independent sets of a forest F.

TF7 proved that every finite tree other than P2 satisfies

m(T) >= i(T[S(T)]) >= F_(s(T)+2).

It also showed that the fixed-support minimum is F_(s+2) for every s>=3, attained by the path
corona P_s corona K1, but did not characterize all equality trees.

## Equality in the forest Fibonacci bound

**Theorem.** For every forest F on s vertices,

i(F) = F_(s+2)

if and only if F=P_s, with P_0 interpreted as the empty forest.

The cases s=0,1 are immediate. Let s>=2 and suppose equality holds.

If F has an isolated vertex v, then

i(F)=2 i(F-v) >= 2 F_(s+1) > F_(s+2),

because 2F_(s+1)-F_(s+2)=F_(s-1)>0. Hence an equality forest has no isolated vertex.

Choose a leaf v with neighbor u. Splitting independent sets according to whether they contain v
gives the exact recurrence

i(F)=i(F-v)+i(F-{u,v}).

The inductive lower bounds on the two terms add to F_(s+2), so equality forces equality in both:
F-v=P_(s-1) and F-{u,v}=P_(s-2). In the path F-v, deleting u leaves one path on s-2 vertices
only when u is an endpoint. Thus adding v back extends that endpoint and F=P_s. Conversely the
standard path recurrence gives i(P_s)=F_(s+2).

So equality forces connectedness and maximum degree at most two; there are no disconnected or
isolated-vertex equality cases.

## Equality in the support-induced-forest injection

For T != P2 define the core

C(T)=V(T) - (S(T) union L(T)).

**Theorem.** For every finite tree T != P2,

m(T)=i(T[S(T)])

if and only if the induced core T[C(T)] is edgeless.

For trees of order at least three, leaves and supports are disjoint. Every maximal independent set
M determines the independent support set I=M intersect S(T). Once I is fixed, leaf membership is
forced: a leaf is absent when its support lies in I, and present when its support lies outside I.
This is the leaf choice used in the TF7 injection.

Take I empty. Then all leaves are selected and every support is excluded. A completion is exactly a
maximal independent set of the induced core T[C(T)]: core vertices have no leaf neighbors, and
their support neighbors are all excluded. If the core contains an edge xy, a maximal independent
set extending {x} and one extending {y} are distinct. Thus the empty-support seed already has at
least two completions, and m(T)>i(T[S(T)]).

Conversely suppose the core is edgeless and fix any independent I subset S(T). A core vertex is
excluded precisely when it has a neighbor in I; otherwise it must be selected, because it has no
core neighbor, no leaf neighbor, and no selected support neighbor. Hence every core choice is
forced. Together with the forced leaves this produces exactly one maximal independent set for every
I. Thus m(T)=i(T[S(T)]).

K1 satisfies the conclusion directly. P2 remains the unique support/leaf-overlap exception from
TF7: both vertices lie in both S and L, and m(P2)=2<i(P2)=3.

This also shows why requiring all non-support/non-leaf vertices to be absent is too strong for
equality in the first inequality alone. P5 has one isolated core vertex and satisfies
m=i(T[S])=4; P6 has a core edge and satisfies m=5>i(T[S])=4.

## Exact fixed-support equality class

Now let s>=3. If

m(T)=F_(s(T)+2),

then equality holds in both TF7 inequalities. The forest theorem forces T[S(T)]=P_s, while the
injection theorem forces the core to be independent.

Because T[S(T)] is connected, a nonempty independent core is impossible. A core vertex is not a
leaf, has no leaf neighbor, and has no core neighbor, so it has at least two support neighbors.
Those two support neighbors are already joined by the support path; adding their two edges through
the core vertex creates a cycle, contradicting that T is a tree. Therefore the core is empty.

It follows that T consists exactly of the support path P_s together with leaves, with every path
vertex carrying at least one private leaf. Conversely every such tree has one maximal independent
set for every independent subset of its support path, hence

m(T)=i(P_s)=F_(s+2).

Therefore, for every s>=3:

> m(T)=F_(s(T)+2) if and only if T is obtained from P_s by attaching at least one private
> leaf to every path vertex and adding no other vertices.

Equivalently, the fixed-support minimizers are exactly the arbitrary duplicate-leaf closure of the
path corona P_s corona K1. After twin-leaf reduction, the minimizer is unique: P_s corona K1.
There is no second genuinely different extremal family.

The small cases are separate. s=0 gives only K1, with m=1. For s=1, the trees are exactly stars
K_(1,k) with k>=2, all with m=2. For s=2, the global minimum is the exceptional P2, with m=2;
among trees other than P2, Fibonacci-chain equality m=3 is attained exactly by a support edge with
at least one private leaf at each endpoint.

## Exposed computational check

The deterministic TF8 reproducer uses only all 5,447 already burned unlabeled trees of orders
1--14. This is interpretation data, not proof. It verifies zero failures of:

- m=i(T[S]) if and only if the core is edgeless, excluding P2;
- i(T[S])=F_(s+2) if and only if T[S] is P_s;
- the fixed-support equality characterization for every visible s>=3;
- exact agreement between all visible extremizers and generated positive leaf-multiplicity blowups
  of the support path, modulo isomorphism.

The visible equality counts are:

| support count | orders and numbers of equality trees |
|---:|---|
| 3 | 6:1, 7:2, 8:4, 9:6, 10:9, 11:12, 12:16, 13:20, 14:25 |
| 4 | 8:1, 9:2, 10:6, 11:10, 12:19, 13:28, 14:44 |
| 5 | 10:1, 11:3, 12:9, 13:19, 14:38 |
| 6 | 12:1, 13:3, 14:12 |
| 7 | 14:1 |

No order-15 tree or other fresh exhaustive corpus is generated or inspected.

## Candidate and coordinate consequences

No candidate lifecycle revision follows from the equality theorem. It characterizes the sharp lower
envelope of MIS count at fixed support count, but neither proves nor refutes any of the eighteen
remaining domination-number/MIS facets. Their coefficients are not searched for new patterns and
the archived fan is not reopened.

Raw maximal_independent_set_count remains retained unchanged. The statistic i(T[S]) is
mathematically canonical as the lower-envelope term in the proof, but it deliberately forgets the
multiplicity contributed by the core and supplies no independent reason for domination number to be
linear in it. Twin-leaf reduction is likewise a useful structural quotient, not a replacement
coordinate: it preserves m and s while changing other discovery quantities such as order, leaf
count, and maximum degree.

Thus TF8 identifies no independently motivated new discovery feature, normalization, target change,
or grammar change.

## Decision

New scientific experiment frozen: **no**.

New permanent candidate allocated: **no**.

Candidate registry changed: **no**.

Experiment registry changed: **no**.

TF4 MIS fan reopened: **no**.

Raw MIS coordinate changed: **no**.

Fresh exhaustive order consumed: **no**.

The fixed-support extremal problem is structurally complete at the level posed by TF8. If this
result is pursued further, the next defensible session is a bounded prior-art audit of the
fixed-support theorem and its equality characterization before deciding whether it merits a
separate theorem-focused project. Until then, keep orders at least 15 untouched and the eighteen
TF4 MIS survivors archived.

The deterministic machine record is experiments/TF8-DIAG-0001/diagnosis.json, reproduced by
python -m experiments.tf8_fixed_support_equality.
