# TF16 — research-question audit

Date: 2026-10-03

TF16 returns TreeForge to question-first mode after TF15 closed the fixed-order/fixed-segment
domination programme. It does not reopen that programme for a prettier normal form, run TxGraffiti,
allocate a candidate, add an invariant, or inspect any tree of order at least 15.

**Decision: one independent question survives, but no prospective experiment is yet warranted.**
TreeForge therefore remains paused at the experiment boundary.

## Verified starting state

TF16 starts from exact merged `main`

`5652e29c5f6ed450482108b99503b11c087356e6`,

the merge commit for TF15 PR #21, **TF15: close strict-rounded defect classification**.

The verified TF15 provenance is:

- PR #21 exact head:
  `1a309f2a0c7792dc4b3f084f72ce9721e0e83080`;
- exact-head Actions run `37139422782`: successful;
- merge commit / TF16 starting main:
  `5652e29c5f6ed450482108b99503b11c087356e6`;
- post-merge Actions run `37139661763`: successful.

Both specified green runs completed installation, unit tests, byte-compilation, Ruff, calibration,
the historical deterministic diagnoses, and the TF15 rounded-defect diagnosis. Comparing the exact
PR head with the merge commit gives no file-content delta.

The TF15 merge also preserves the scientific boundaries exactly:

- `data/registry/candidates.jsonl` has the same blob SHA before and after TF15;
- `data/registry/experiments.jsonl` has the same blob SHA before and after TF15;
- `docs/INVARIANT_CATALOG.md` and `src/treeforge/invariants/core.py` likewise have unchanged
  blob SHAs across TF15;
- TF-001157 remains the highest allocated candidate and TF-001158 remains next;
- the last scientific experiment row remains TF4-0001;
- there is no TF15 scientific experiment;
- orders 1--14 are the burned diagnostic universe and every order at least 15 remains untouched.

No discrepancy was found in the requested TF15 provenance audit.

## Scientific state after TF15

The main TreeForge lines now separate cleanly.

### Closed theorem threads

The TF7--TF9 fixed-support/maximal-independent-set theorem thread is closed. Its numerical lower
bound is subsumed by stronger published work; the equality sharpening remains an elementary
TreeForge result that does not justify reopening the archived TF4 MIS facet fan.

The TF11--TF15 fixed-segment domination thread is closed. Its fixed-((n,q)) numerical extrema,
minimum equality structure, and maximum equality structure are all reduced to published
classifications plus explicit elementary reductions. TF15's residue-1/2 result is
`TREEFORGE_ELEMENTARY_DERIVATION_FROM_PUBLISHED_RESULTS`, not a reason for a separate theorem
repository.

### Archived discovery grammars

TF2's full-dimensional hulls generated too many opaque statements. TF3's ratios-only grammar was
more legible but largely exposed scale effects and elementary relations. TF4's pairwise hulls were
the best controlled general-purpose grammar, but rerunning them without a new mathematical question
would simply repeat an already diagnosed experiment. The TF4 MIS fan remains archived.

### Useful machinery without an active question

TreeForge retains exact unlabeled-tree generation, exact domination and matching machinery,
distance and degree invariants, `segment_count`, the exact maximal-independent-set DP, and the
optional predecessor-inspired modules. None is promoted merely because it is already implemented.

## Candidate questions considered

TF16 considered a deliberately small set of mathematically motivated directions before selecting
one.

### Fixed branching-vertex count versus domination — reject

This remains a legitimate extremal question, but it is not sufficiently independent of TF11--TF15.
For a nontrivial tree, suppressing degree-2 vertices gives

`q = L + B - 1`,

where (q) is segment count, (L) is leaf count, and (B) is the number of branching vertices.
A fixed-((n,B)) domination programme would therefore return immediately to the same
leaf/degree-sequence/subdivision mechanisms just closed. A bounded search did not locate an exact
fixed-((n,B)) ordinary-domination theorem, but that negative search is not novelty evidence and
does not overcome the scientific adjacency.

### Reopen the Greedy-Uniformity extremal problem — reject

The predecessor source lineage explicitly records the all-order extremal greedy-bias problem as
outside its frozen theorem package. Reopening it here merely because it remains unresolved would
violate TreeForge's rule against mining a completed predecessor project without a new independent
reason.

### Extremal maximal-independent-set count at fixed matching number — reject

This direction is now strongly covered by published work. Tian--Tu give a sharp lower bound for the
number of maximal independent sets in a tree in terms of (n-alpha), which equals the matching
number for trees. Shi--Tu--Wang determine corresponding maximum-count extremal problems for graph
classes that include connected triangle-free graphs, hence trees. This is not a clean new TreeForge
opening.

### Independent domination versus domination — reject

The interaction is mathematically natural but belongs to a dense current literature of sharp
inequalities and characterizations, and TF14--TF15 already depended centrally on the published
((gamma,i))-tree theory. A new independent-domination target would be too close to the thread
just closed unless a narrower external problem first selected it.

### Distance/topological indices conditioned by domination — reject

Wiener/eccentricity-type extremal problems with prescribed domination number have an extensive
literature, including recent exact characterizations for specific indices. Choosing
`wiener_index` or `eccentricity_sum` because TreeForge already computes them would be
implementation-led rather than question-led.

## Surviving question: extremal multiplicity of minimum dominating sets

For a tree (T), let

`zeta(T) = # { D subseteq V(T) : D is a minimum dominating set of T }`.

The selected TF16 research question is:

> **For each order (n), determine**
> [
> M_n=max{zeta(T): T 	ext{ is a tree on } n 	ext{ vertices}},
> ]
> **and characterize all trees attaining (M_n).**

This is a question about the multiplicity of optimal dominating configurations, not the value of
the domination number itself.

### Why the question is independently interesting

Minimum dominating sets ((gamma)-sets) are a standard object with their own structural and
reconfiguration theory. Trees with a unique (gamma)-set have classical structural
characterizations, while other work studies (gamma)-graphs whose vertices are all minimum
dominating sets. Extremal enumeration asks how much nonuniqueness an (n)-vertex tree can support
while every counted set remains globally minimum.

That motivation exists independently of TreeForge's earlier coefficient output. It is also
different from TF7--TF9: a maximal independent set is an independent dominating set that need not
have minimum dominating cardinality, whereas (zeta(T)) counts only dominating sets of size
(gamma(T)).

## Bounded prior-art audit

The most directly relevant sources located are:

1. J. D. Alvarado, S. Dantas, E. Mohr and D. Rautenbach,
   **“On the maximum number of minimum dominating sets in forests,”**
   *Discrete Mathematics* 342 (2019), 934--942,
   DOI `10.1016/j.disc.2018.11.025`.
   This studies the maximum number as a function of domination number and proves an exponential
   forest upper bound; it does not give the exact (n)-vertex tree extremum.

2. D. S. Taletskii,
   **“On the Number of Minimum Dominating Sets in Trees,”**
   *Mathematical Notes* 113 (2023), 552--566,
   DOI `10.1134/S0001434623030264`.
   For maximum degree at most four it proves the sharp order bound
   ((sqrt2)^n) and characterizes equality; it also gives degree-five lower constructions and a
   global bound strictly below (1.4205^n). This directly brackets the selected order-extremal
   problem but does not state its exact value or all unrestricted extremizers.

3. J. Petr, J. Portier and L. Versteegen,
   **“On the number of minimum dominating sets and total dominating sets in forests,”**
   *Journal of Graph Theory* 106 (2024), 976--993,
   DOI `10.1002/jgt.23107`.
   They prove that a forest of domination number (gamma) has at most
   ((sqrt5)^gamma) minimum dominating sets and construct, for every (gamma), a tree with
   more than ((2/5)(sqrt5)^gamma) such sets. Thus the fixed-(gamma) exponential order is
   known up to a constant factor, but this is not an exact (n)-vertex extremal theorem.

4. G. Gunther, B. L. Hartnell, L. R. Markus and D. F. Rall,
   **“Graphs with unique minimum dominating sets,”**
   *Congressus Numerantium* 101 (1994).
   This gives equivalent conditions and a constructive characterization for the opposite endpoint,
   trees with exactly one minimum dominating set.

The TF16 searches included combinations of “minimum dominating sets”, “gamma-sets”, trees,
maximum number, exact extremal, order, domination number, maximum degree, and 2024--2026 follow-up
terms. No stronger publication giving the exact unrestricted sequence (M_n) and all extremal
(n)-vertex trees was located.

That is only a **bounded-search status**. It is not an openness or novelty claim.

## Why stronger known theorems do not already settle the selected question

The fixed-(gamma) theorem controls (zeta(T)) by the optimum size, not by order, and is sharp
only up to a multiplicative constant. Taletskii's unrestricted (n)-vertex result is an exponential
upper bound, while the sharp equality theorem applies to the maximum-degree-at-most-four subclass.
Neither supplies the exact all-tree (M_n) or a complete unrestricted extremizer class.

The unique-(gamma)-set characterizations settle the minimum possible multiplicity, not the
maximum.

## Theorem-first diagnosis

Several structural facts constrain the problem before any computation.

### Strong supports are forced

If a support vertex (v) has at least two leaf neighbors and a minimum dominating set (D) omits
(v), then every leaf neighbor of (v) must lie in (D). Replacing those at least two leaves by
(v) produces a smaller dominating set, a contradiction. Hence every strong support belongs to
every minimum dominating set.

So repeatedly adding leaves to one support cannot create more choices among minimum dominating
sets; it eventually forces a vertex. High multiplicity must come from interacting local choices
rather than unbounded twin-leaf inflation.

### The known degree-four boundary is informative but not decisive

Taletskii's sharp ((sqrt2)^n) theorem for maximum degree at most four and higher-base
degree-five constructions show that restricting prospectively to subquartic trees would discard
the global mechanism. Conversely, the global (1.4205^n) bound is too coarse to identify exact
extremizers. This prevents a premature subclass experiment.

### Counting is naturally compositional on rooted trees

A rooted-tree dynamic program can associate to each boundary state both:

- the minimum number of selected vertices compatible with that state; and
- the number of ways attaining that minimum.

Combining child states uses min-plus arithmetic with counts summed over ties. Thus the natural new
quantity is exactly computable without enumerating all vertex subsets. This is a feasibility
observation, not yet a registry change or an experiment.

The theorem-first work in TF16 therefore narrows the mechanism but does not prove the exact
extremal sequence or a complete recursive extremizer grammar.

## Necessary invariant

If TreeForge later computes this question, the only new scalar invariant presently justified is

`minimum_dominating_set_count(T) = zeta(T)`.

It should be implemented by an exact rooted-tree DP that simultaneously computes
(gamma(T)) and the number of optimum solutions, then independently checked against brute-force
enumeration on conservative burned orders.

TF16 does **not** add it to the default invariant registry. The question has selected the quantity,
but an experiment has not yet selected a frozen hypothesis.

## What a finite experiment would have to test

A future experiment should not merely tabulate (M_n) and fit a recurrence. Before order 15 is
opened, burned orders 1--14 and theorem-first analysis would have to isolate one explicit structural
claim, for example a recursively defined extremizer family or a local replacement rule that predicts
both the extremal count and equality structure.

A genuinely informative fresh test would then ask whether the **pre-frozen structural
classification and its exact predicted order-15 extremal count** survive exhaustive order 15.
Failure would mean an order-15 counterexample outside the frozen family or with a larger count.
Success would be finite evidence only, not proof.

No such structural statement is justified yet, so no TF16 scientific experiment is frozen.

## What would change the mathematical belief

The direction becomes stronger if theorem-first reduction plus burned data produce one small,
construction-level family whose recurrence explains the best known exponential behavior and whose
predicted equality structure is rigid enough to falsify prospectively.

The direction should be abandoned or returned to pause if:

- the bounded literature audit later exposes an exact stronger theorem;
- the exact counting DP cannot be independently validated;
- burned orders require unrelated extremizer families with no stable structural operation;
- any proposed experiment reduces to arbitrary sequence fitting or multi-axis feature mining; or
- a useful structural hypothesis cannot be frozen before fresh data are visible.

## TF16 decision

End state: **A. New question justified, experiment not yet warranted.**

New scientific experiment frozen: **no**.  
TF16-0001 created: **no**.  
TxGraffiti run: **no**.  
New candidate allocated: **no**.  
Candidate registry changed: **no**.  
Experiment registry changed: **no**.  
Next permanent candidate: **TF-001158**.  
New default invariant added: **no**.  
TF4 MIS fan reopened: **no**.  
TF7--TF9 support/MIS thread reopened: **no**.  
TF11--TF15 fixed-segment thread reopened: **no**.  
Order 15 consumed: **no**.  
Orders at least 15 remain untouched: **yes**.

## Recommended next session

Continue theorem-first from the selected extremal (gamma)-set multiplicity question.

First derive and independently validate the exact rooted-tree min-plus/count DP on already burned
orders only. Then study the structural transformations behind the 2023/2024 extremal bounds and
the forced/alterable vertex decomposition, looking for a prospective extremizer grammar. Do not
inspect order 15, allocate TF-001158, or freeze a discovery experiment until one explicit
construction-level statement is strong enough to predict a fresh outcome in advance.
