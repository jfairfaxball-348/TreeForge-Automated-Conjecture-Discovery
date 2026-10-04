# TreeForge — Experimental Conjecture Discovery in Tree Combinatorics

TreeForge is a **discovery laboratory** for finite, simple, unlabeled trees. Its job is to generate reproducible finite-tree corpora, compute mathematically defined invariants, propose candidate relations, attack them with holdout and adversarial tests, preserve failures and provenance, and graduate only unusually strong candidates into separate theorem repositories.

TreeForge is **not** a theorem prover and finite computation is never represented as proof of an infinite statement. A failed literature search is not represented as novelty. Speculative candidates are not sent to Lean, Palomar, a paper, or arXiv from this repository.

## Research pipeline

```text
finite-tree universe
→ exact/reproducible invariant computation
→ automated conjecturing
→ append-only candidate registry
→ holdout/adversarial falsification
→ mathematical interpretation
→ bounded prior-art / novelty audit
→ graduation to a separate theorem repository
```

TF0 established the infrastructure and a `KNOWN/CALIBRATION` run for the standard identity `|E(T)| = |V(T)| - 1`.

TF1 completed the first pre-frozen controlled discovery experiment, `TF1-0001`: 200 discovery trees at orders 2–10, 235 untouched holdout trees at order 11, a disciplined core feature set targeting domination number, and the pinned live `txgraffiti==0.4.1` adapter. The frozen run generated **zero candidates**. That is recorded as a valid research result rather than a reason to weaken the gates.

TF2 diagnosed that zero as a TreeForge adapter/configuration hypothesis-semantics mismatch without rewriting TF1 history, corrected the empty-payload boundary, and completed frozen experiment `TF2-0001`. The corrected run produced 998 permanent candidate lineages; 924 were falsified on untouched order 12, 74 survived the frozen adversarial set, and mathematical interpretation produced no graduation candidate. One simple finite survivor, `gamma(T) >= 3 nu(T)/5`, was later falsified exactly by an order-25 six-arm spider. See `experiments/TF2-0001/RESULTS.md`.

TF3 diagnosed the 998-statement stream as overwhelmingly dense convex-hull output and completed
`TF3-0001` with one changed discovery axis: TxGraffiti was restricted to `ratios` only.
The frozen run produced 12 permanent candidates (`TF-001000`–`TF-001011`); the fresh exhaustive
order-13 holdout falsified 8, and all 4 holdout survivors passed the 18-tree pre-frozen fresh hostile
set. Mathematical interpretation then falsified 3 of those survivors and classified the fourth as
`TRIVIAL`, leaving no `MATHEMATICALLY_INTERESTING` or graduation candidate. See
`experiments/TF3-0001/RESULTS.md`, `docs/TF3_DIAGNOSTIC.md`, and
`docs/TF3_EXPERIMENT_FREEZE.md`.

TF4 completed `TF4-0001` with the frozen one-axis change from ratios to 21 fixed pairwise convex-hull runs. The scientific run at source `d8e0874a22dde7f226431fc4f15a36adb8254efa` (Actions `36983184665`) reproduced 259 raw outputs, 214 after Dalmatian, 205 per-run post-duplicate outputs, and 146 exact cross-run unique statements. Permanent IDs `TF-001012`–`TF-001157` were allocated before the exposed K1 gate; K1 falsified 47, leaving a 99-candidate batch frozen with SHA-256 `2bbb81b85eb6e40351f0913fafdc822c5417b2336e957e83fc08b505aedabf0f` before order 14 was constructed.

The fresh exhaustive 3,159-tree order-14 holdout falsified 66 of those 99 and left 33 survivors; all 33 survived the exact 19-tree frozen hostile set. Post-gate interpretation then found one already-exposed order-11 counterexample, classified six forms as elementary, four as feature-set artifacts, identified `TF-001013` as the known Lemańska leaf bound, and left `TF-001028`, `gamma(T) <= (2n+1-diameter(T))/3`, in bounded `NOVELTY_AUDIT` after a targeted search found no exact match. That negative search is not evidence of novelty. Twenty maximal-independent-set-count facets remain finite `ADVERSARIAL_PASSED` without promotion. No candidate reached `GRADUATION_CANDIDATE`. See `experiments/TF4-0001/RESULTS.md`, `docs/TF4_DIAGNOSTIC.md`, and `docs/TF4_EXPERIMENT_FREEZE.md`.

TF5 resolved TF-001028 structurally rather than broadening discovery. The frozen bound
gamma(T) <= (2n+1-diameter(T))/3 is a direct consequence of Ore's classical
gamma<=floor(n/2) bound in the short-diameter regime and Gu-Meng-Zhang-Wan (2013),
Lemma 2.3, in the long-diameter regime. TF-001028 is therefore append-only KNOWN_RESULT,
not a novelty or graduation candidate. Candidate-specific exact family searches found no
counterexample and exposed infinite equality families, but the lifecycle decision rests on the
published implication. TF5 also diagnosed the 20 surviving maximal-independent-set-count facets:
they form four neighboring coordinate families and their frozen coefficient planes remain
equality-supported through exposed orders 11-14. That stability is not enough to justify removing
or transforming the MIS-count feature, so TF5 freezes no new experiment. See
docs/TF5_TF001028_ANALYSIS.md.

TF6 completes the requested exposed-data diagnosis of `maximal_independent_set_count`.
A three-state independent-domination tree DP now makes the coordinate's local recurrence explicit
and replaces the value-equivalent brute-force core implementation. The 20 surviving TF4 MIS facets
remain supporting and equality-attaining through every exposed extension to order 14; the only
strict exposed dominance relations are TF-001091 over TF-001034 and TF-001095 over TF-001037.
A bounded structural literature check confirms that exponential MIS scale is intrinsic, but log,
per-vertex growth, nth-root, extremal-ratio, removal, and rooted-state replacements are not
independently canonical linear discovery coordinates. TF6 therefore retains raw MIS count, freezes
no new experiment, allocates no candidate ID, and leaves every order at least 15 untouched. See
`docs/TF6_MIS_COORDINATE_DIAGNOSIS.md` and `experiments/TF6-DIAG-0001/diagnosis.json`.

TF7 resolves those two exposed dominance conditions structurally. If (S(T)) is the support-vertex
set and (s=|S(T)|), then every tree other than (P_2) satisfies
(m(T)\ge i(T[S(T)])\ge F_{s+2}), while (P_2) is the explicit support/leaf-overlap exception.
This gives the exact fixed-support minimum (1,2,2,F_{s+2}) for (s=0,1,2,s\ge3),
respectively, with path coronas attaining the Fibonacci branch. Hence both
(m\ge3s-4) and (m\ge5s-12) hold for every finite tree. TF-001034 and TF-001037 therefore
move append-only to `ARTIFACT_OF_FEATURE_SET`, universally dominated by TF-001091 and
TF-001095 respectively; the stronger siblings remain finite `ADVERSARIAL_PASSED` candidates.
TF7 retains raw MIS, freezes no experiment, allocates no candidate ID, and leaves orders at least
15 untouched. See `docs/TF7_SUPPORT_MIS_DIAGNOSIS.md` and
`experiments/TF7-DIAG-0001/diagnosis.json`.

TF8 characterizes equality in the TF7 theorem without opening fresh data. Equality in the
forest bound is unique: an s-vertex forest has exactly F_(s+2) independent sets only when it is
P_s. Equality in the support injection holds exactly when the non-support/non-leaf core is
edgeless. Combining them shows that for every s>=3 the fixed-support minimizers are exactly the
trees obtained from P_s by attaching at least one private leaf to every path vertex; after
twin-leaf reduction the unique minimizer is P_s corona K1. No remaining TF4 MIS facet receives a
lifecycle change, raw MIS is retained, no new experiment is frozen, TF-001158 remains next, and
orders at least 15 remain untouched. See docs/TF8_FIXED_SUPPORT_EQUALITY.md and
experiments/TF8-DIAG-0001/diagnosis.json.


TF9 completes a bounded prior-art and theorem-significance audit of the TF7/TF8 fixed-support
result. The forest independent-set minimum is classical via Prodinger--Tichy (1982). More
decisively, Tian--Tu (2025) prove the stronger tree bound
`m(T) >= F_(n-alpha(T)+2)`; for trees `n-alpha=nu`, and for `T != P2` one private
support--leaf edge per support gives `s(T)<=nu(T)`. Thus the TF7 fixed-support **value** theorem
is a direct corollary of published stronger prior art. Taletskii--Malyshev (2022) also explicitly
record `i(H)=mi(H corona K1)` and twin-leaf invariance. The bounded audit did not locate an exact
published counterpart of TF8's core-edgeless injection-equality criterion or the complete only-if
minimizer classification, but negative search is not novelty evidence. Because the numerical theorem
is subsumed and the remaining equality-only sharpening is short and elementary, TF9 keeps the result
inside TreeForge and does not create a separate theorem project. No candidate lifecycle event,
experiment, new coordinate, or fresh order occurs; TF-001158 remains next and orders at least 15
remain untouched. See `docs/TF9_FIXED_SUPPORT_PRIOR_ART.md` and
`experiments/TF9-AUDIT-0001/audit_summary.json`.

## Quick start

```bash
python -m pip install -e '.[dev]'
python -m pytest -q
python -m compileall -q src experiments
ruff check .
```

Optional live TxGraffiti compatibility requires:

```bash
python -m pip install -e '.[conjecturing]'
```

Reproduce the compact TF1 benchmark with:

```bash
python experiments/benchmark_tf1.py --output /tmp/tf1-benchmark.json
```

See `PROJECT_CHARTER.md`, `docs/RESEARCH_PROTOCOL.md`, `docs/INVARIANT_CATALOG.md`, `docs/CANDIDATE_LIFECYCLE.md`, `experiments/TF1-0001/RESULTS.md`, `experiments/TF2-0001/RESULTS.md`, `experiments/TF3-0001/RESULTS.md`, `experiments/TF4-0001/RESULTS.md`, `docs/TF4_DIAGNOSTIC.md`, `docs/TF4_EXPERIMENT_FREEZE.md`, `docs/TF5_TF001028_ANALYSIS.md`, `docs/TF6_MIS_COORDINATE_DIAGNOSIS.md`, and `docs/TF7_SUPPORT_MIS_DIAGNOSIS.md`, plus `docs/TF8_FIXED_SUPPORT_EQUALITY.md` and `docs/TF9_FIXED_SUPPORT_PRIOR_ART.md`, before adding another discovery experiment.


TF10 audits what TreeForge should study next rather than forcing another run. It separately
reassesses the invariant vocabulary, domination target, relation grammar, and natural subclass
options and compares concrete alternatives without numerical scoring. No alternative currently has
an independent mathematical rationale strong enough to justify fresh data. TF10 therefore freezes
no experiment, allocates no candidate ID, keeps TF-001158 next, leaves the TF4 MIS fan and TF7–TF9
thread closed, and preserves every order at least 15 untouched. See
docs/TF10_NEXT_QUESTION_DIAGNOSIS.md.

TF11 converts the TF10 pause into a question-first restart without yet restarting discovery. A
bounded mathematical and prior-art audit selects one research question: among trees of order (n)
with a fixed number (q) of segments (maximal degree-2 chains between leaves/branching vertices),
determine the minimum and maximum domination numbers and characterize the extremal trees. Segment
count is standard in extremal tree theory, and edge subdivision is independently known to affect
ordinary domination; the bounded search did not locate an exact theorem settling this cross-question,
which is not a novelty claim. TF11 does not implement the new coordinate, freeze an experiment, run
TxGraffiti, allocate TF-001158, or inspect order 15. See
`docs/TF11_RESEARCH_QUESTION_AUDIT.md` and
`experiments/TF11-DIAG-0001/diagnosis.json`.



TF12 implements `segment_count` exactly and independently validates the degree-count formula against
explicit maximal degree-2 path decomposition on every burned tree through order 14. A deeper
prior-art audit changes the scientific status of the TF11 question: Lemańska's leaf lower bound,
together with the elementary fixed-segment leaf range, determines the fixed-((n,q)) minimum
value, while Gentner--Henning--Rautenbach's exact fixed-degree-sequence maximum determines the
fixed-((n,q)) maximum after optimizing over feasible leaf counts. All 80 occupied burned
((n,q)) cells agree with those derived formulas; this is a diagnostic check, not proof.
The bounded search did not locate a complete published classification of all fixed-((n,q))
extremizers, which is not a novelty claim. TF12 therefore keeps the scientific experiment pause:
no TF12-0001, no TxGraffiti run, no candidate allocation, and orders at least 15 remain untouched.
See `docs/TF12_SEGMENT_DOMINATION_DIAGNOSIS.md`.

TF13 resolves the fixed-segment **minimum equality class completely** and narrows the maximum
equality residue without consuming fresh data. Hajian--Henning--Jafari Rad's cactus classification,
specialized to trees, captures all rounded leaf-bound equality cases; after exact ceiling arithmetic,
the fixed-(n,q) minimizers are precisely the eligible published G_0^m classes. On the maximum side,
TF13 derives the complete optimizing leaf-count interval, characterizes every degree sequence capable
of attaining the value, and proves the exact gamma=n-L support-structure branch. A burned-order
counterexample at (n,q)=(6,3) shows that one degree sequence can contain both a maximizer and a
nonmaximizer, so the full maximizing tree-isomorphism classification does not follow from the
fixed-degree-sequence theorem and remains unresolved after the bounded audit. No experiment is
frozen, no candidate is allocated, TF-001158 remains next, and orders at least 15 remain untouched.
See docs/TF13_SEGMENT_DOMINATION_EQUALITY.md.


TF14 sharpens the remaining fixed-segment **maximum realization** problem without fresh data.
The tie cases are already covered by TF13: whenever
`n-L=floor((n+L)/3)`, a maximizing realization has `gamma=n-L`, hence exactly every
nonleaf is a support. On the only genuinely residual branch,
`floor((n+L)/3)<n-L`, Favaron's independent-domination bound gives the exact reduction
`gamma=floor((n+L)/3)` iff
`gamma=i=floor((n+L)/3)`. When `n+L` is divisible by 3, this is the intersection of
Favaron's published equality family with the published `(gamma,i)`-tree class, so that subcase
is a direct corollary of published classifications. The bounded audit did not locate a complete
classification for the residue-1/2 integer-saturation cases. TF14 reduces those exactly to a
support-core partial-domination equality, falsifies over-strong Kurnosov/canonical-core iff claims
on burned orders 1--14, freezes no experiment, allocates no candidate, and leaves order 15 sealed.
See `docs/TF14_SEGMENT_DOMINATION_MAXIMUM_EQUALITY.md`.

TF15 closes the last fixed-segment **maximum realization** residue without fresh data. Dorfling--Goddard--Henning--Mynhardt's complete constructive `(gamma,i)`-tree grammar gives an exact recurrence for the Favaron numerator defect `epsilon=n+L-3i`: after the mandatory first T1 in a P1-starting construction the defect is 1, and every later T1--T6 operation changes it by a locally determined value according to the operation and whether the attacher was a leaf. Therefore the strict-rounded residue-1/2 maximizers are exactly the published `(gamma,i)` constructions whose defect walk ends at 1/2. Both statuses are **TREEFORGE_ELEMENTARY_DERIVATION_FROM_PUBLISHED_RESULTS**. A 2024 support-refined domination bound also gives the necessary restriction `2delta+|SL|<=epsilon`, but burned examples show equality there is not necessary. The full fixed-segment minimum/maximum equality programme is now complete at a recursive structural level; the thread is closed, no experiment or candidate is created, TF-001158 remains next, and order 15 remains sealed. See `docs/TF15_SEGMENT_DOMINATION_ROUNDED_DEFECT.md`.


TF16 returns TreeForge to question-first mode after closing the fixed-segment programme. A bounded
landscape and prior-art audit rejects reopening the archived MIS, predecessor greedy-bias,
fixed-segment/branch-count, independent-domination, and implementation-led distance-index directions.
One independent question survives: for each order (n), determine the maximum number of minimum
dominating sets among (n)-vertex trees and characterize all extremizers. Published work gives
strong exponential bounds in terms of domination number and order, plus sharp results for restricted
maximum degree, but the bounded TF16 search did not locate the exact unrestricted (n)-vertex
extremal theorem; this is not a novelty claim. Theorem-first analysis shows strong supports are
forced into every minimum dominating set and identifies an exact rooted-tree min-plus/count DP as
the natural future computation, but no structural extremizer hypothesis is yet frozen. TF16 therefore
ends in state A: the question is justified, the experiment pause remains, no invariant/candidate/
experiment is added, TF-001158 remains next, and orders at least 15 remain untouched. See
`docs/TF16_RESEARCH_QUESTION_AUDIT.md`.


TF17 implements the selected multiplicity question as exact theorem-support machinery without
promoting it to the discovery registry. The three-state rooted min-plus/count DP is independently
validated against brute-force minimum dominating sets on every unlabeled tree through order 8,
against all possible roots through order 8, and against the existing exact domination-number
implementation on all 5,447 burned trees through order 14. The burned extrema have an exact
structural explanation: every even-order extremizer through 14 is a corona H corona K1, while every
odd-order extremizer from 3 through 13 is the unique balanced Taletskii W_(a,b). These are not
promoted to an all-order conjecture: Taletskii's published degree-5 module construction has
exponential base strictly above sqrt(2), and already gives an order-38 construction with
736^2 > 2^19, analytically ruling out the corona grammar globally. TF17 also records safe
strong-support/twin-leaf pruning and an exact three-state rooted replacement signature, but no
finite extremal-state theorem yet predicts M_15. The experiment pause therefore remains; no
candidate or experiment is added, TF-001158 remains next, the new helper stays non-default, and
orders at least 15 remain untouched. See
`docs/TF17_MINIMUM_DOMINATING_SET_MULTIPLICITY.md`.


TF18 makes the rooted replacement question precise. Subtracting the A-state cost gives a lossless
normalized cost shape; if two pendant gadgets have the same normalized shape and the replacement
has no smaller exact count in any feasible state, then all outside boundary alternatives acquire
one common cost shift, preserving the global optimum tie set and never decreasing zeta. A same-order
order-8 counterexample shows why ordinary coordinatewise cost/count dominance is unsafe: selectively
lowering one state can destroy an optimum tie and reduce multiplicity. The literature mechanisms
also receive an exact state dictionary: Taletskii's repeated preleaf branches are copies of the
rooted P2 signature, while the Petr--Portier--Versteegen five-vertex terminal branch has signature
`A=(2,1), B=(2,2), C=(2,2)`, explaining its exact 5-versus-3 factors. Burned diagnosis through
order 14 compresses 3,474 projective interfaces to 119 weakly undominated ones at order 14, but no
theorem makes this frontier finite; stars have unbounded normalized cost gaps and paths have
unbounded exact counts even at maximum degree two. TF18 therefore preserves the experiment pause:
no candidate or experiment is added, TF-001158 remains next, the count helper remains non-default,
and order 15 remains sealed. See `docs/TF18_ROOTED_STATE_DOMINANCE.md`.


TF19 characterizes the exact information that **genuine one-hole tree contexts** can see in the
TF17 A/B/C interface.  The reverse message is
`K_A=min(A_out,B_out,C_out)`, `K_B=min(A_out,B_out)`, `K_C=A_out`; consequently every
tree context has one of only three normalized boundary-cost patterns:
`(0,0,0)`, `(0,0,1)`, or `(0,1,1)`.  This yields a strictly coarser exact quotient than
TF18 projective signatures: retain the three exposed lower faces and exact counts only on states
that occur on a face.  The quotient is minimal for exact normalized min-plus/count response, but is
still infinite, already on endpoint-rooted `P_(3k)` because their exposed count vectors are
unbounded and distinguishable by canonical path contexts.  TF19 also proves that released vertices
may be padded neutrally as extra leaves at an **already strong support**, while `P2 -> P3` and Q2
show arbitrary leaf padding can destroy multiplicity.  Burned orders 1--14 are used only after
these theorems are fixed: at order 14, 3,474 projective interfaces collapse to 2,126 context
interfaces and 44 weak context-undominated interfaces.  No finite exact-order grammar follows.
No experiment or candidate is created, `TF-001158` remains next, the helper stays non-default,
and order 15 remains sealed.  See `docs/TF19_TREE_CONTEXT_COMPLETENESS.md`.

TF20 moves the unrestricted minimum-dominating-set multiplicity programme from local rooted
interfaces to global exact-order structure. It proves an exact strong-support banked replacement
theorem using TF19's three genuine context faces, and a stronger forest-budget principle: every
strict multiplicity-improving isolate-free forest replacement with vertex deficit at least two can
be padded by disjoint P2/P3 components and converted by Taletskii's same-order forest lemma into a
strict n-vertex tree improvement. The only generic missing budget is one vertex, and this gap is
real because every one-leaf extension of P4 lowers `zeta` from 4 to at most 3. This is exactly the
deficit of Taletskii's empty-vertex reduction after universal vertices are excluded, when no strong
support bank can exist. TF20 also proves that an exact order-extremizer has at most one strong
support; if present it is the unique universal vertex with exactly two private leaves and no other
empty neighbour. Every tree with no strong support has a canonical marked support-core
representation, but its core is an arbitrary unbounded tree, so this is not a finite extremal
grammar. No order-15 prediction or experiment is frozen; `TF-001158` remains next and order 15+
remains untouched. See `docs/TF20_GLOBAL_COMPENSATION_STRUCTURE.md`.

