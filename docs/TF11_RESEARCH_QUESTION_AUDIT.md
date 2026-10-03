# TF11 — research-question audit

Date: 2026-10-03

TF11 starts from the pause deliberately imposed by TF10. It is a question-selection session, not a
scientific discovery run. No TxGraffiti generation is performed, no archived TF4 coefficient is
mined, no candidate ID is allocated, and no fresh tree order is inspected.

## Verified starting state

The starting `main` HEAD is exactly
`f742c37fefe440f8213b7bafbe2ad8a798f0ebc7`, the merge commit for PR #16.

TF10 provenance is intact:

- PR #16 is merged.
- exact TF10 PR head:
  `527bffd3b6b1ed577663fcaffe71536a34d4251d`;
- exact PR-head CI: `37104972109`, successful;
- merge commit / starting main:
  `f742c37fefe440f8213b7bafbe2ad8a798f0ebc7`;
- post-merge CI: `37105100784`, successful.

The post-merge CI job passed unit tests, byte-compilation, Ruff, deterministic calibration, the live
pinned TxGraffiti compatibility test through the unit suite, historical registry/result tests, and
the explicit TF6, TF7, TF8, TF9, and TF10 deterministic checks.

The TF10 diagnosis remains present at
`docs/TF10_NEXT_QUESTION_DIAGNOSIS.md` and
`experiments/TF10-DIAG-0001/diagnosis.json`. The experiments directory contains no
`TF10-0001` scientific spec.

The deterministic TF10 validator rechecks the current candidate registry. In particular:

- TF-001028 is revision 7 `KNOWN_RESULT`;
- TF-001034 and TF-001037 are revision 6 `ARTIFACT_OF_FEATURE_SET`;
- TF-001091 and TF-001095 are revision 5 `ADVERSARIAL_PASSED`;
- the TF4 MIS fan remains 18 `ADVERSARIAL_PASSED` plus the two projection artifacts;
- TF-001157 remains the highest allocated ID, so TF-001158 remains next.

The experiment registry contains the historical calibration row and scientific rows TF1-0001 through
TF4-0001. There is exactly one TF4-0001 row and no TF5–TF10 scientific row.

Orders 1–14 remain burned. Orders at least 15 are untouched.

## TF10 pause as a hard constraint

TF11 does not ask which unused implementation might produce output. It asks which finite-tree problem
would still be worth posing if TreeForge and TxGraffiti did not exist.

Accordingly TF11 did **not**:

- run TxGraffiti;
- rerun or inspect the archived TF4 MIS fan;
- inspect order 15;
- add `wiener_index` merely because it is already implemented;
- switch target merely because domination has not graduated a theorem;
- restrict to a convenient subclass;
- add a feature bundle or widen a relation grammar to increase yield.

A question survives only if its mathematical motivation precedes any new candidate output.

## Selected question

TF11 selects the following research question:

> **For finite trees (T) of order (n) with exactly (q) segments, what are the minimum and
> maximum possible domination numbers (gamma(T)), and which trees attain each extremum?**

For this question a **segment** is a maximal path whose endpoints have degree different from 2 and
whose internal vertices, if any, have degree 2. For (K_1) set the segment count to 0. Equivalently,
for any finite tree with (n_2) degree-2 vertices,

[
q(T)=n(T)-n_2(T)-1.
]

This is the number of edges in the homeomorphic reduction obtained by suppressing all degree-2
vertices.

### Why this is independently natural

The parameter is not invented for TreeForge. Segment count and segment sequence are standard
structural parameterizations in extremal tree theory. They separate the **topological skeleton** of a
tree from the amount and placement of subdivision along its chains.

That separation has a direct reason to matter for ordinary domination. Subdividing tree edges is a
classical operation in domination theory: the domination subdivision number asks how many edge
subdivisions are required to increase the domination number. Thus a question conditioning on the
number of maximal degree-2 chains is linked to a known mathematical mechanism affecting
(gamma(T)), rather than to a desire for more conjectures.

The selected question is also meaningfully different from the closed TF7–TF9 thread. It does not use
maximal-independent-set count, support-induced forests, twin-leaf reduction, or the archived TF4 MIS
coefficients.

### Why this is a vocabulary gap rather than an implementation opportunity

TreeForge currently has `order`, leaf/support counts, degree extrema, diameter/radius, matching,
domination, MIS count, Wiener index, and cherry count. It does not have the number of degree-2
vertices or the equivalent segment count.

The missing coordinate is selected **after** the mathematical question, not before it. It has an
exact implementation independent of candidate yield:

```text
segment_count(T) = order(T) - count(v : degree(v) == 2) - 1
```

with the (K_1) convention already giving 0. This is linear-time in the tree size and needs no
heuristic or numerical approximation.

TF11 deliberately does not implement it yet. Implementation belongs to a later session only if the
question survives the deeper freeze audit below.

## Lightweight prior-art screen

This is a bounded risk screen, not a novelty audit. “Not located” below never means “open”.

### Fixed segment count and domination

Three adjacent literature strands matter.

H. Aram, S. M. Sheikholeslami and O. Favaron, **“Domination subdivision numbers of trees,”**
*Discrete Mathematics* 309 (2009), 622–628, DOI
`10.1016/j.disc.2007.12.085`, studies the minimum number of edge subdivisions required to
increase ordinary domination number and characterizes important tree cases. This establishes a
direct domination/subdivision mechanism, but it is not the fixed-((n,q)) extremal problem posed
here.

E. O. D. Andriantiana, S. Wagner and H. Wang, **“Maximum Wiener Index of Trees with Given
Segment Sequence,”** *MATCH Communications in Mathematical and in Computer Chemistry* 75
(2016), 91–104, uses the same standard notion of a segment and solves extremal Wiener questions at
fixed segment sequence and fixed number of segments. The target is distance structure, not
domination.

B. Borovićanin, **“On the Extremal Zagreb Indices of Trees with Given Number of Segments or Given
Number of Branching Vertices,”** *MATCH Communications in Mathematical and in Computer
Chemistry* 74 (2015), 57–79, likewise treats segment/branching counts as established extremal tree
parameters. Again, the target is a degree-based index rather than domination.

The bounded searches used combinations of:

- “domination number” + tree + segment / number of segments;
- “domination number” + degree-2 vertices;
- “domination number” + branch / branching vertices;
- “domination subdivision number” + trees;
- fixed-order extremal formulations.

They did **not locate** an exact theorem, stronger theorem, or equality characterization settling
the selected fixed-order/fixed-segment domination problem. This is only a bounded-search status.

### Competing question: fixed branching-vertex count

Question:

> Among (n)-vertex trees with exactly (b) branching vertices, what are the minimum and maximum
> domination numbers and extremal trees?

This is serious. Branching vertices (degree at least 3) are standard in tree extremal theory, and
the same bounded search did not locate a direct ordinary-domination extremal theorem at fixed
((n,b)).

It is not selected because branch count alone forgets the subdivision mass between branch vertices
and leaves. The segment formulation isolates the known subdivision mechanism more directly. TF11
will not launch both related axes.

### Competing question: Wiener index at fixed domination number

Question:

> Among (n)-vertex trees with fixed domination number, what are the extremal Wiener indices?

This is independently natural, but the literature risk is already too high for a clean restart.
Andriantiana–Wagner–Wang explicitly note existing extremal Wiener results for trees with fixed order
and domination number in a substantial regime, citing the distance-index literature. TF11 therefore
does not turn `wiener_index` into a target merely because it is implemented.

### Competing question: leaf concentration and domination

Question:

> How does concentration of leaves at strong support vertices constrain domination number?

This has a real local mechanism, but recent literature is already very close. A. Cabrera-Martínez,
**“An improved upper bound on the domination number of a tree,”** *Discrete Applied Mathematics*
343 (2024), 44–48, DOI `10.1016/j.dam.2023.10.013`, improves support-based domination bounds
using support vertices, support-link vertices, strong leaves, and strong support vertices and
characterizes equality.

TreeForge's existing `cherry_count` would therefore risk being a convenient but weaker proxy for
an already-developed structural vocabulary. No cherry-based experiment is selected.

### Competing question: independent domination versus domination

Question:

> Among (n)-vertex trees with fixed domination number, what are the extremal independent
> domination numbers?

This is also mathematically natural, but it enters a dense and current literature. Recent work
explicitly studies domination number, independent domination number, and (k)-independence in
trees, with sharp inequalities and extremal characterizations. TF11 rejects this direction at the
lightweight risk-screen stage rather than adding a new domination variant.

## Question-selection matrix

No numerical score or rank is used.

| option | precise objective / conditioning | independent reason | vocabulary need | literature risk | main confounder | decision |
|---|---|---|---|---|---|---|
| fixed segments / domination | extrema of (gamma) at fixed ((n,q)) | skeleton/subdivision structure; subdivision changes domination | one new exact `segment_count` | moderate; adjacent but exact cross-result not located | segment lengths and mod-3 residues may matter | **SELECT** |
| fixed branch vertices / domination | extrema of (gamma) at fixed ((n,b)) | standard ramification parameter | one new branch count | moderate; fixed-branch extremal literature exists for other indices | loses subdivision mass and branch-degree distribution | reject in favor of the more mechanism-specific segment question |
| fixed domination / Wiener | extrema of (W) at fixed ((n,gamma)) | distance versus coverage | none | high; substantial existing extremal literature | likely rediscovery | reject |
| leaf concentration / domination | sharpen (gamma) via strong-support structure | local leaf coverage | strong-support statistic or proxy | high; recent direct support-structure domination bounds | choosing `cherry_count` would be implementation-led | reject |
| independent domination interaction | extrema of (i(T)) at fixed ((n,gamma)) | compare unrestricted and independent domination | new exact independent-domination invariant | high; direct modern literature | dense parameter literature | reject |
| maintain TF10 pause | no new question | safe default | none | none | none | reject because one question survives |

## Feasibility without fresh data

No tree corpus was recomputed in TF11. That is intentional: the question was selected from
mathematics and literature, not from exposed numerical geometry.

The new quantity `segment_count` is exact and linear-time. The existing
`domination_number` implementation is exact and already exercised on the burned corpus and in
historical CI. A future diagnostic can safely use burned orders 1–14 after the invariant is
implemented.

No order-15 timing probe was run. No order-15 invariant value was produced, printed, persisted,
ranked, or inspected.

There is no computational reason visible at TF11 that makes a future order-15 validation
implausible: the additional coordinate itself is negligible compared with the already-existing exact
domination computation. A later freeze session should still make the runtime boundary explicit
before fresh execution.

## Why no experiment is frozen yet

The question selects its structural axis: introduce `segment_count` while keeping ordinary
domination and the all-tree domain.

It does **not yet** uniquely select the representation of the extremal envelope. Ordinary domination
on subdivided paths has arithmetic behavior that can make a single linear hull an unnecessarily
strong assumption. Possible exact formulations include piecewise floors/ceilings or dependence on
segment-length residues.

Therefore TF11 does not silently make a second scientific choice between:

- a single pairwise convex-hull view in ((n,q,gamma));
- a directly grouped exact extremal table by ((n,q));
- a residue-aware structural recurrence.

A later session must resolve that from the mathematics before any candidate generation. If it cannot
do so while preserving a one-axis controlled design, TreeForge should keep the experiment paused
even though the question remains worth studying.

## Scientific boundary

TF11 creates **no** scientific experiment.

- no `TF11-0001` spec;
- no TxGraffiti run;
- no candidate allocation;
- no candidate registry edit;
- no experiment registry edit;
- no order-15 inspection;
- no archived TF4 MIS mining;
- no TF7–TF9 theorem-thread reopening;
- no `i(T[S])` feature;
- no twin-leaf discovery coordinate;
- no change to raw `maximal_independent_set_count`.

TF-001158 remains the next permanent candidate.

## Decision

**One research question is selected, but TreeForge remains paused at the experiment boundary.**

The selected question is the fixed-order/fixed-segment domination extremal problem. Its motivation is
independent of TreeForge, the missing parameter is standard and exact, and the bounded prior-art
screen does not already settle the question in the sources located.

This is **not** a claim that the problem is open or novel.

## Next session

Begin from `TF11-Q-SEGMENTS-DOMINATION`, not from a generator configuration.

1. Implement `segment_count` exactly and test it against both the degree-2 formula and explicit
   suppression on small trees.
2. Deepen the prior-art search specifically around ordinary domination with fixed segment count,
   fixed degree-2 count, homeomorphic reductions, and subdivision/edge-subdivision structure.
3. Use only burned orders 1–14 for any diagnostic envelope or recurrence study.
4. Determine whether the mathematics forces one prospective representation: a fixed pairwise hull,
   a conditioned exact envelope, or a residue-aware recurrence.
5. Freeze a scientific experiment only if exactly one material axis can then be stated
   prospectively. Only after that freeze may order at least 15 be touched.

The machine-readable audit is `experiments/TF11-DIAG-0001/diagnosis.json`, validated by
`python -m experiments.tf11_research_question_audit`.
