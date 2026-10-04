# TF23 — independent research-question audit

Date: 2026-10-04

TF23 returns TreeForge to question-first mode after the TF17--TF22 unrestricted
minimum-dominating-set multiplicity replacement programme reached its natural endpoint.
The purpose of this session is not to manufacture a new conjecture or spend fresh data. It is to
ask whether the repository currently contains enough independent mathematical motivation for one
new controlled discovery cycle.

**Decision: no candidate question presently clears the restart standard. Preserve the experiment
pause.**

No order-15 tree is generated or inspected. No TxGraffiti run is performed. No candidate ID is
allocated. No scientific experiment is frozen. Candidate, experiment, and default-invariant
registries are unchanged.

## 1. TF22 provenance and repository boundary

TF23 starts from exact merged `main`

`0f16ae6a8482a7531d8e9a5dac77b8cb388f023b`.

The requested TF22 provenance checks exactly:

- TF22 PR #28 exact head:
  `49f84988ba2b2b9b2a374e3cf90594beed151dfb`;
- exact-head Actions run `37225316919`: completed successfully at that exact head;
- merge commit / TF23 starting main:
  `0f16ae6a8482a7531d8e9a5dac77b8cb388f023b`;
- post-merge Actions run `37225577808`: completed successfully at the merge commit.

Both green runs completed installation, the full unit suite, byte-compilation, Ruff, deterministic
calibration, all historical deterministic diagnoses present in the workflow, and the explicit TF20
global-compensation, TF21 one-vertex-compensation, and TF22 unique-empty-hub diagnoses.

PR #28 changed exactly:

- `.github/workflows/ci.yml`;
- `HANDOVER.md`;
- `README.md`;
- `ROADMAP.md`;
- `docs/FAILURE_AND_LESSON_LEDGER.md`;
- `docs/TF22_UNIQUE_EMPTY_HUB.md`;
- `experiments/tf22_unique_empty_hub_diagnosis.py`;
- `tests/test_tf22_unique_empty_hub_diagnosis.py`.

The live scientific boundary also checks:

- the candidate registry contains 1,157 unique permanent IDs and ends at `TF-001157`;
- `TF-001158` is absent and remains the next permanent ID;
- the experiment registry still ends with scientific experiment `TF4-0001`;
- `default_registry()` still registers only `CORE_INVARIANTS`;
- `minimum_dominating_set_count` remains explicitly documented in source as
  diagnostic/theorem-support machinery, not a default discovery invariant;
- orders 1--14 remain the burned diagnostic universe;
- no order-15-or-larger generation or inspection is performed in TF23.

No starting-state discrepancy was found.

## 2. Audit of completed TreeForge research lines

### TF1--TF5: automated grammar and domination discovery

This line is methodologically complete, not a reservoir of unspent candidate coefficients.

TF1 established that a controlled experiment may legitimately return zero candidates. TF2 showed
that a full-dimensional convex-hull grammar can produce a very large opaque candidate family.
TF3 reduced the grammar and exposed how easily bounded-order scaling can masquerade as structure.
TF4's fixed pairwise hulls gave the cleanest interpretable general-purpose grammar, but still
produced no graduation candidate. TF5 then demonstrated that a finite survivor can be mathematically
interesting yet fall under stronger prior art after structural analysis.

The lesson is not that ordinary domination is exhausted. It is that the existing TxGraffiti grammar
has already been diagnosed, and rerunning it without a separately posed mathematical question would
not constitute a new research programme.

Status: **method thread closed; no automatic restart**.

### TF6--TF9: maximal-independent-set/support structure

The fixed-support maximal-independent-set line produced genuine structural mathematics, but its
principal numerical lower bound is subsumed by stronger published work. The exact support-induced
equality criterion retained by TreeForge is a short elementary sharpening whose bounded prior-art
status did not justify a separate theorem programme.

The raw `maximal_independent_set_count` invariant remains legitimate and exact. That is not a
reason to reopen the archived TF4 MIS fan.

Status: **closed**.

### TF10--TF16: question audits and fixed-segment domination

TF10 correctly paused rather than changing target, feature set, or subclass merely to obtain output.
TF11 then selected the fixed-order/fixed-segment domination problem for an independent reason:
segments separate the topological skeleton from subdivision mass, and subdivision is a classical
domination mechanism.

TF12--TF15 developed that question theorem-first. The numerical extrema and both equality sides were
reduced to published classifications plus explicitly identified elementary derivations. TF15 closed
the programme at the recursive structural level and explicitly rejected reopening it merely for a
prettier normal form.

TF16 then selected minimum-dominating-set multiplicity as a genuinely independent question.

Status: **fixed-segment domination closed; question-audit discipline retained**.

### TF17--TF22: unrestricted minimum-dominating-set multiplicity

This line produced substantial exact machinery: a linear rooted min-plus/count DP, exact rooted
replacement semantics, the minimal genuine tree-context quotient, exact vertex-budget compensation
for every deficit at least two, the two-empty pairing theorem, and the complete unique-empty hub
shape characterization in terms of stable-rooted nontrivial gamma-excellent trees.

TF22 also proved why the replacement programme does not close the fixed-order extremum. The hub
objective exposes two rooted coordinates, not one. Taletskii's (W_{a,b}) family gives exact context
reversal, and an infinite (P_{3m+1}+P_2) hub family defeats every single hub-edge reattachment.
The residual strong-banked class remains separate.

These are theorem-level structural and negative results. They do not yield an exact all-order
recurrence, a prospective (M_{15}), or an order-15 extremizer family.

Status: **programme paused at a natural method boundary**.

The weighted gamma-excellent residue is therefore not classified as unfinished cleanup. Any future
return to it requires an independent reason beyond the fact that it survived TF22.

## 3. Invariant-vocabulary audit

The current default exact vocabulary remains:

- order and degree statistics;
- leaf and support-vertex counts;
- segment count;
- diameter, radius, eccentricity sum, and Wiener index;
- matching and independence numbers;
- domination number;
- maximal-independent-set count;
- cherry count.

Several entries are useful primarily for consistency or known identities: on nontrivial trees
`edge_count=order-1`, `degree_sum=2(order-1)`, and `min_degree=1`; for trees
`independence_number=order-matching_number`; radius is determined by diameter. These relations make
them poor novelty axes by themselves.

The optional TreeStack estimator, finite ProbStack probability, and Greedy-Uniformity bias retain
their predecessor-specific provenance. No new TreeForge question presently requires promoting any
of them.

The exact `minimum_dominating_set_count` module remains theorem/diagnostic support from
TF17--TF22 and stays outside the default registry.

Conclusion: **no invariant addition or promotion is justified in TF23**.

## 4. Candidate questions formulated before any data

TF23 considered a deliberately small set of exact questions. None was selected from an order-1--14
table.

### 4.1 Matching number at fixed order and segment count

Candidate question:

> For trees (T) of order (n) with exactly (q) segments, determine the minimum and maximum
> matching number (
u(T)), and characterize all extremizers.

Why it is independently natural: matching is a fundamental tree parameter, while segment count
measures subdivision of a fixed topological skeleton. Subdivision changes matching constraints in a
direct parity-sensitive way.

Plausible mechanism: matching DP on the suppressed core, segment-length parity, and edge-transfer
or balancing transformations.

Literature triage: Andriantiana, Wagner and Wang,
**“Extremal problems for trees with given segment sequence,”**
*Discrete Applied Mathematics* 220 (2017), 20--34,
DOI `10.1016/j.dam.2016.12.009`, proves, for every fixed segment sequence, that the corresponding
starlike tree has minimum matching number (equivalently maximum independence number) among all trees
with that segment sequence. The same paper develops the matching-generating-function transformation
behind that result.

Decision: **reject for TF23**. The exact fixed-((n,q)) envelope was not located as a named theorem
in the bounded search, and TF23 does not infer that it is settled. But the strongest structural step
is already published at the finer segment-sequence level, while the segment axis itself was the
subject of TF11--TF15. Optimizing the remaining segment-length compositions would be too close to a
just-closed structural programme to justify fresh holdout data without a sharper external reason.

### 4.2 Number of maximum matchings at fixed order

Candidate question:

> For each (n), maximize the number of maximum-cardinality matchings over all (n)-vertex trees
> and characterize all extremizers.

Why it is independently natural: it is the edge-optimization analogue of counting multiplicity of
an optimum combinatorial object, with an exact two-state tree DP and a clear extremal objective.

Literature triage: Clemens Heuberger and Stephan Wagner,
**“The number of maximum matchings in a tree,”**
*Discrete Mathematics* 311 (2011), 2512--2542,
DOI `10.1016/j.disc.2011.07.028`, determines the upper and lower bounds at fixed order and gives a
complete characterization of the extremal trees.

Decision: **reject as known**.

### 4.3 Extremal gamma-graph diameter for trees

Candidate question:

> Among (n)-vertex trees, determine the largest possible diameter of the reconfiguration graph of
> minimum dominating sets and characterize equality.

Why it is independently natural: it studies connectivity and movement between optimum dominating
configurations rather than their number. It is a reconfiguration question, not the TF17--TF22
multiplicity objective.

Plausible mechanism: local exchange paths between gamma-sets and tree decomposition.

Literature triage is direct. Edwards, MacGillivray and Nasserasr,
**“Reconfiguring Minimum Dominating Sets: The gamma-Graph of a Tree,”**
*Discussiones Mathematicae Graph Theory* 38 (2018), 703--716,
DOI `10.7151/dmgt.2044`, gives tree bounds on gamma-graph degree, diameter, and order.
Lemanska and Zylinski,
**“Reconfiguring Minimum Dominating Sets in Trees,”**
*Journal of Graph Algorithms and Applications* 24 (2020), 47--61,
DOI `10.7155/jgaa.00517`, gives tight diameter bounds in both single-vertex-replacement and slide
adjacency models and a constructive linear-time optimal-move algorithm. Finbow and van Bommel,
**“gamma-Graphs of Trees,”** *Algorithms* 12 (2019), 153,
DOI `10.3390/a12080153`, gives an algorithm for the gamma-graph of a tree and a characterization of
which trees arise as gamma-graphs of trees.

Decision: **reject as directly covered by existing theory**.

### 4.4 Number of maximum independent sets at fixed order

Candidate question:

> For each (n), maximize the number of maximum independent sets over all (n)-vertex trees and
> characterize the extremizers.

Why it is independently natural: it is an optimum-set multiplicity question using an existing core
parameter, but is different from counting inclusion-maximal independent sets.

Literature triage: Jennifer Zito,
**“The structure and maximum number of maximum independent sets in trees,”**
*Journal of Graph Theory* 15 (1991), 207--221,
DOI `10.1002/jgt.3190150208`, solves the fixed-order maximum and characterizes the extremal tree
families. Later work sharpens related fixed-independence-number versions.

Decision: **reject as known**.

### 4.5 TF22 weighted stable-root gamma-excellent extremum

Possible theorem problem:

[
E_m(lambda)=max{zeta(R)-lambdaeta(R,r):
(R,r)	ext{ is a stable-rooted gamma-excellent tree of order }m}.
]

Why it is mathematically coherent: TF22 proves that unique-empty hub contexts evaluate a rooted
component by a positive linear functional of two exact coordinates, and gamma-excellent trees have
published recursive shape characterizations.

Mechanism available: the exact rooted min-plus/count DP, Burton--Sumner/Samodivkin construction
grammars, Pareto-front analysis, and context-aware dynamic programming.

Literature triage: Burton and Sumner's 2007 gamma-excellent-tree theorem gives an exact constructive
shape characterization, and Samodivkin's later work gives a related labeled corona-block
description. The bounded TF23 update search did not locate an exact theorem for the weighted rooted
count objective. That negative search is **not** novelty evidence.

Decision: **reject for TF23 on independence grounds, not because it is known**. The objective exists
because TF22's replacement programme exposed it. TF23 has no separate external problem, theorem,
or application selecting this weighted functional. Choosing it merely because it is the surviving
residue would violate the explicit TF23 boundary.

## 5. Other vocabulary not promoted to a candidate

The Greedy-Uniformity predecessor leaves an all-order bias extremum outside its frozen theorem
package, but TF16 already rejected reopening that project simply because an open-looking extremal
problem remains. TF23 finds no new independent reason to reverse that decision.

The TreeStack and ProbStack optional invariants likewise remain specialized imports. Their
availability is not a mathematical question.

Distance indices such as Wiener and eccentricity sums have dense extremal literatures under segment,
degree, matching, domination, and related constraints. TF23 finds no TreeForge-specific structural
gap that selects one of those axes.

Independent domination remains both literature-dense and scientifically adjacent to the
TF12--TF15 domination programme.

## 6. Bounded literature-search scope

The TF23 search was targeted rather than exhaustive. It used combinations of:

- trees + segment sequence / number of segments + matching number;
- trees + number of maximum matchings + extremal / fixed order;
- minimum dominating sets + gamma-graph + tree + diameter / reconfiguration;
- trees + number of maximum independent sets + extremal;
- gamma-excellent + stable vertex + minimum dominating sets + counting / rooted counts;
- 2024--2026 follow-up terms where appropriate.

The audit distinguishes three outcomes:

- **exact known theorem** for maximum-matching multiplicity, gamma-graph diameter/reconfiguration,
  and maximum-independent-set multiplicity;
- **stronger or finer adjacent theorem** for matching number at fixed segment sequence;
- **apparently unaddressed after bounded search but independently unmotivated in TF23** for the
  weighted gamma-excellent residue.

A failed search is nowhere used as evidence of novelty or openness.

## 7. Mechanism test

Every serious candidate had at least one plausible exact mechanism before rejection:

- fixed-segment matching: suppressed-core matching DP plus segment parity and published
  edge-transfer transformations;
- maximum-matching multiplicity: rooted matching DP and local replacement, but the theorem is
  already known;
- gamma-graph diameter: exchange paths and decomposition, but tight tree theory is already known;
- maximum-independent-set multiplicity: critical-edge structure, but the theorem is already known;
- weighted gamma-excellent objective: rooted min-plus/count DP plus constructive grammar, but the
  motivation fails the independence gate.

Thus TF23 is not rejecting candidates merely because they look difficult. They fail because the
theorem already exists, a finer published theorem removes most of the proposed opening, or the only
motivation is residue from an exhausted TreeForge method.

## 8. Burned diagnostics

**None.**

No question survives formulation, literature triage, and mechanism testing. Therefore Phase G is
not triggered. TF23 does not enumerate or inspect orders 1--14 for question selection, does not fit
any burned sequence, and does not create a diagnostic script merely to generate activity.

This is stricter than merely avoiding order 15: no new tree census is needed at all.

## 9. Experiment decision and holdout status

Outcome: **B — preserve the experiment pause.**

A prospective experiment cannot be frozen because there is no surviving question. Consequently
there is no justified discovery representation, no predeclared candidate-generation rule, and no
scientific reason to allocate a fresh holdout.

Scientific state after TF23:

- new scientific experiment frozen: **no**;
- scientific experiment executed: **no**;
- TxGraffiti run: **no**;
- burned diagnostic census: **no**;
- candidate allocated: **no**;
- candidate registry changed: **no**;
- experiment registry changed: **no**;
- highest permanent candidate: **TF-001157**;
- next candidate ID: **TF-001158**;
- last scientific experiment: **TF4-0001**;
- default invariant registry changed: **no**;
- `minimum_dominating_set_count` promoted: **no**;
- order 15 consumed: **no**;
- orders at least 15 remain untouched: **yes**.

## 10. Recommended next session

Do not open order 15 merely because TF23 found no replacement question.

The next TreeForge session should begin only when a precise problem is supplied by an independent
mathematical source: for example, an explicit open problem in current tree theory, a structural
theorem whose missing equality/extremal case naturally matches TreeForge's exact machinery, or a
new application that selects one of the existing invariants for a reason independent of candidate
yield.

Until then, preserve the pause. In particular:

- do not return automatically to the TF22 weighted gamma-excellent residue;
- do not rerun TF4 pairwise hulls;
- do not reopen fixed-segment domination or support/MIS;
- do not promote optional predecessor invariants merely to create a new target;
- do not spend order 15 as a generic exploratory screen.

TF23's useful result is negative but concrete: the most immediate questions exposed by the current
vocabulary are either already solved, substantially pre-empted by finer literature, or insufficiently
independent of a completed programme. Fresh data should remain sealed until that changes.
