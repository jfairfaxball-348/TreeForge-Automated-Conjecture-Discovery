# Roadmap

## TF0 — infrastructure session

Status: **COMPLETE (2026-10-01).**

Completed scope: predecessor and TxGraffiti provenance pins; package scaffold; exact AHU-style canonical unlabeled-tree generation; modular exact invariant registry; separate opt-in TreeStack/ProbStack/Greedy-Uniformity quantities; a narrow TxGraffiti adapter pinned to `txgraffiti==0.4.1`; append-only candidate/experiment registries; holdout machinery; parametric hostile-family constructors; tests; static checks; CI; and one tiny `KNOWN/CALIBRATION` end-to-end run.

Calibration source code checkpoint: `f0c42426fdabd3860837d3e3eb048a038842a655`. GitHub Actions run `36849930237` passed installation, unit tests (including a live TxGraffiti adapter call), byte-compilation, Ruff, and deterministic calibration smoke testing.

The calibration candidate is `TF-000001`, the standard identity `|E(T)| = |V(T)| - 1`, generated only to validate plumbing. It is permanently classified `KNOWN_RESULT` and must never be presented as new mathematics.

## TF1 — first controlled discovery

Status: **COMPLETE (2026-10-01).**

TF1 benchmarked the current exact invariant implementations, froze experiment `TF1-0001`, generated a 200-tree discovery corpus (orders 2–10) and a 235-tree holdout corpus (order 11) with strict generation-order separation, added practical duplicate/affine/known-identity checks, and exercised the pinned live TxGraffiti adapter in GitHub Actions.

Successful scientific run: source commit `e5175b5f5667195adf64ccae75e3dc42f0061086`, Actions run `36852665881`.

Result: TxGraffiti generated **zero candidates** under the frozen target/features/methods/heuristics. No standards were weakened to force a survivor. Accordingly there were no TF1 candidate IDs, holdout candidate evaluations, adversarial survivor tests, mathematical-interest promotions, or prior-art searches.

See `experiments/TF1-0001/RESULTS.md`.

## TF2 — diagnosed and controlled discovery rerun

Status: **COMPLETE (2026-10-01).**

TF2 diagnosed the TF1 zero-yield result without rewriting TF1 history. The practical cause was a TreeForge/TxGraffiti adapter-semantics mismatch: TreeForge's empty hypothesis payload was forwarded as upstream `[]`, while pinned TxGraffiti `0.4.1` uses `None` for the always-true base predicate and `[]` iterates over no hypotheses. The correction remains isolated in the adapter and is live-tested against the pinned package.

Frozen experiment `TF2-0001` kept the TF1 target, seven discovery features, `convex_hull` plus `ratios`, Morgan/Dalmatian heuristics, duplicate removal, and touch-count sorting. Discovery reused orders 2–10 (200 trees); order 11 remained burned; the untouched holdout was all 551 unlabeled trees of order 12.

Successful scientific run: source commit `d091d88889fa72322bfc49a5531bc30b1f31b049`, Actions run `36888114138`.

Pipeline counts were 23,268 raw generator outputs, 23,268 after Morgan, 10,753 after Dalmatian, and 998 after duplicate removal/touch-count sorting. Permanent IDs `TF-000002` through `TF-000999` were allocated. All 998 passed exact discovery-side reevaluation and entered `CONJECTURED`; the untouched order-12 holdout falsified 924 and left 74 survivors. All 74 survived the 26 pre-frozen adversarial trees.

Mathematical interpretation classified `TF-000002` as `KNOWN_RESULT`, `TF-000010` and `TF-000996` as `TRIVIAL`, and left 70 high-dimensional facets at finite `ADVERSARIAL_PASSED` without promotion. `TF-000998`, the simple bound `gamma(T) >= 3 nu(T)/5`, briefly reached `MATHEMATICALLY_INTERESTING` and received a bounded prior-art audit, but deeper structural interpretation produced an exact order-25 six-arm spider counterexample (`gamma=7`, `nu=12`), so it is permanently `FALSIFIED`.

No candidate reached `GRADUATION_CANDIDATE`. No theorem, novelty, Lean, Palomar, paper, or arXiv claim was created.

See `experiments/TF2-0001/RESULTS.md`.

## TF3 — ratios-only controlled discovery

Status: **COMPLETE (2026-10-01).**

TF3 first diagnosed the TF2 high-volume/low-interpretability stream, then froze and executed
`TF3-0001` with exactly one discovery-axis change: TxGraffiti was restricted to `ratios`
only. The target, seven discovery features, orders 2-10 corpus, heuristics, post-processors, and
empty-hypothesis semantics remained fixed.

Successful scientific run: source commit
`e23b44d24a7b87d6f67aa18749059540934b2767`, Actions run `36914647703`.

The ratios-only pipeline produced 14 raw statements, 14 after Morgan, 12 after Dalmatian, and 12
after exact duplicate removal. Permanent IDs `TF-001000` through `TF-001011` were frozen
before constructing the fresh exhaustive order-13 holdout. Eight candidates were falsified on the
1,301-tree holdout; four survived and then all four passed the exact 18-tree pre-frozen fresh hostile
set.

Mathematical interpretation did not force a survivor: two literal all-tree upper bounds were
falsified by `K1`, one support-vertex lower bound was elementary and `TRIVIAL`, and the
`3 nu/5` lower bound duplicated the already-falsified TF2 relation and was killed by the exposed
order-25 six-arm spider. Final TF3 states are 11 `FALSIFIED` and 1 `TRIVIAL`.

No TF3 candidate reached `MATHEMATICALLY_INTERESTING`; no new prior-art search was performed;
no candidate reached `GRADUATION_CANDIDATE`.

See `experiments/TF3-0001/RESULTS.md`.

## TF4 — pairwise interaction controlled discovery

Status: **COMPLETE (2026-10-02).**

TF4 first diagnosed TF3's interpretable-but-zero-interest result, then froze and executed
`TF4-0001` with exactly one material discovery-axis change: ratios-only generation became
`convex_hull` run separately on all 21 unordered pairs of the unchanged seven discovery features,
followed only by exact normalized cross-run deduplication. The target, orders 2–10 discovery corpus,
TxGraffiti pin, heuristics, post-processors, feature vocabulary, and literal all-tree hypothesis were
unchanged.

Authoritative scientific source:
`d8e0874a22dde7f226431fc4f15a36adb8254efa`. Actions run: `36983184665`.

The pairwise pipeline produced 259 raw outputs, 259 after Morgan, 214 after Dalmatian, 205
per-run post-duplicate forms, and 146 exact cross-run unique statements. Permanent IDs
`TF-001012` through `TF-001157` were allocated before the exposed K1 domain gate. Exact
discovery reevaluation killed none; K1 killed 47. The remaining 99 candidates were frozen before
holdout construction with batch SHA-256
`2bbb81b85eb6e40351f0913fafdc822c5417b2336e957e83fc08b505aedabf0f`.

Fresh exhaustive order-14 holdout: 3,159 trees, SHA-256
`84978208ee2c65e3cda8327709e662cc71f9018ef2afc1ca03ff86a19a6197c3`.
It falsified 66 candidates and left 33. Only those 33 saw the exact pre-frozen 19-tree hostile set,
SHA-256 `caf97df7db6b739383e015f816e3d643352cf53f164363d171c0eb1751e955f3`;
none failed that finite hostile gate.

Post-gate interpretation did not force a graduation candidate. `TF-001068` is falsified by an
already-exposed order-11 tree; six candidates are `TRIVIAL`; four leaf/MIS facets are
`ARTIFACT_OF_FEATURE_SET` because same-coefficient support/MIS facets are pointwise stronger.
`TF-001013` independently reached mathematical interest but a bounded audit identified it as the
known Lemańska leaf bound. `TF-001028`, `gamma(T) <= (2n+1-diameter(T))/3`, independently
reached mathematical interest and remains in `NOVELTY_AUDIT`: a targeted exact-form search found
related literature but no exact match, which is explicitly not evidence of novelty. Twenty
maximal-independent-set-count facets remain finite `ADVERSARIAL_PASSED` without promotion.

Final TF4 states: 114 `FALSIFIED`, 6 `TRIVIAL`, 4 `ARTIFACT_OF_FEATURE_SET`,
1 `KNOWN_RESULT`, 1 `NOVELTY_AUDIT`, and 20 `ADVERSARIAL_PASSED`. No candidate reached
`GRADUATION_CANDIDATE`.

TF5 should not broaden the discovery grammar yet. First attack `TF-001028` structurally: seek a
proof or an explicit family counterexample and complete its focused prior-art audit. If it resolves
negatively, diagnose the maximal-independent-set-count facet fan before freezing another discovery
axis change.

See `experiments/TF4-0001/RESULTS.md`, `docs/TF4_DIAGNOSTIC.md`, and
`docs/TF4_EXPERIMENT_FREEZE.md`.

## TF5 — structural resolution of TF-001028

Status: **COMPLETE (2026-10-02).**

TF5 began from main 308104fee32f55dc12a110357c48f15249193be5 with successful post-TF4
CI 37016098699. It did not reopen TF4-0001 or consume new fresh holdout data.

The primary candidate TF-001028,

gamma(T) <= (2n+1-diameter(T))/3,

was attacked structurally and by candidate-specific exact family search. The mathematical resolution
is prior art rather than a new TreeForge theorem. Ore's 1962 isolate-free bound gamma<=floor(n/2)
proves the required inequality when 2D<=n+2. For the complementary long-diameter regime,
Gu, Meng, Zhang and Wan (2013), Lemma 2.3, give the exact maximum domination number for trees
with fixed order n and diameter D>=n/2+1:
gamma<=n-D+ceil((2D-n-1)/3). The elementary inequality
3 ceil(x/3)<=x+2 then gives 3gamma+D<=2n+1. K1 is equality separately.

TF-001028 therefore moves append-only from NOVELTY_AUDIT to KNOWN_RESULT. It does not reach
GRADUATION_CANDIDATE. No new candidate ID was allocated; TF-001158 remains next.

TF5 also diagnosed the 20 remaining MIS-count finite survivors. They split into 3 MIS-only,
6 support/MIS, 9 diameter/MIS, and 2 matching/MIS facets. All 20 remain valid and have equality
examples at each exposed order 11-14; a common exposed invariant vector makes 10 facets tight.
Thus the fan is genuine neighboring low-dimensional geometry, not merely TF3-style coefficient
drift. Raw MIS count is scale-sensitive, but this evidence does not independently justify deleting,
logging, normalizing, or replacing it.

No new experiment was frozen and no fresh data boundary was allocated. The next session should
remain diagnostic until a single-axis change is justified independently of desired yield.

See docs/TF5_TF001028_ANALYSIS.md and experiments/TF5-TF001028/analysis_summary.json.


## TF6 — MIS-count coordinate diagnosis

Status: **COMPLETE (2026-10-02).**

TF6 uses only exposed orders 1--14 and existing burned interpretation data to diagnose
`maximal_independent_set_count`. The exact three-state independent-domination recurrence explains
why the coordinate can be invariant under twin-leaf duplication yet grow exponentially under path,
corona, or repeated-branch composition. The production invariant now uses that exact tree DP, with
independent brute-force equivalence tests.

All 20 TF4 MIS survivors remain supporting planes after every cumulative exposed extension through
order 14. They form 3 MIS-only, 6 support/MIS, 9 diameter/MIS, and 2 matching/MIS facets; only
TF-001091 over TF-001034 and TF-001095 over TF-001037 are strictly pointwise dominated on the
exposed corpus.

A bounded structural literature check confirms an exact exponential order-wise extremal envelope
(Wilf/Sagan), leaf-conditioned extremal theory, the corona-extension identity, and path/caterpillar
recurrences. TF6 considers log, per-vertex log, nth-root, extremal-ratio, recurrence-state, removal,
and raw-coordinate choices. None of the alternatives is independently canonical for exact linear
conjecturing.

Decision: retain raw MIS count for now; freeze no TF6 scientific experiment; allocate no candidate
ID; consume no fresh order. TF-001158 remains next and orders at least 15 remain untouched.

See `docs/TF6_MIS_COORDINATE_DIAGNOSIS.md`.

## TF7 — support/MIS structural diagnosis

Status: **COMPLETE (2026-10-02).**

TF7 attacks the only two strict exposed-corpus dominance conditions isolated by TF6 without using
order 15 or any other fresh exhaustive corpus. The key structural result is stronger than either
condition. If (S(T)) is the support-vertex set, (s=|S(T)|), and (m(T)) is the number of
maximal independent sets, then every tree other than (P_2) satisfies

(m(T) \ge i(T[S(T)]) \ge F_{s+2}).

The first inequality comes from seeding disjoint classes of maximal independent sets with independent
sets of the support-induced forest. The second is the sharp minimum number of independent sets in an
(s)-vertex forest. Path coronas (P_s\circ K_1) attain the Fibonacci value for every (s\ge3);
(P_2) is the unique support/leaf-overlap exception relevant to the formula. Thus the exact
fixed-support minimum is (1,2,2,F_{s+2}) for (s=0,1,2,s\ge3).

Consequently (m\ge3s-4) and (m\ge5s-12) are proved for every finite tree. The resulting
candidate implications are append-only: TF-001034 becomes `ARTIFACT_OF_FEATURE_SET` revision 6
because TF-001091 is universally pointwise stronger, and TF-001037 receives the same state at
revision 6 because TF-001095 is universally pointwise stronger. TF-001091 and TF-001095 themselves
remain revision-5 `ADVERSARIAL_PASSED`; TF7 does not prove either domination-number statement.

Raw MIS remains retained. The residual 18 MIS facets stay archived as finite geometry. No TF7
scientific experiment is frozen, no candidate ID is allocated, the experiment registry is unchanged,
TF-001158 remains next, and orders at least 15 remain untouched.

See `docs/TF7_SUPPORT_MIS_DIAGNOSIS.md` and
`experiments/TF7-DIAG-0001/diagnosis.json`.


## TF8 — fixed-support equality characterization

Status: **COMPLETE (2026-10-02).**

TF8 refines the TF7 theorem using only burned orders 1--14. The forest lower bound has a unique
equality structure: i(F)=F_(s+2) for an s-vertex forest if and only if F=P_s. Separately, for every
tree T other than P2, equality m(T)=i(T[S(T)]) holds if and only if the induced subgraph on
vertices that are neither supports nor leaves is edgeless.

Combining the two equality mechanisms gives the exact fixed-support minimizers for every s>=3:
they are precisely the trees obtained from P_s by attaching at least one private leaf to every
support-path vertex and no other vertices. Equivalently, they are the arbitrary duplicate-leaf
closure of P_s corona K1; after twin-leaf reduction the minimizer is unique.

The deterministic exposed check recomputes all 5,447 unlabeled trees of orders 1--14 and finds zero
failures of the two equality characterizations or the final extremal family. This is interpretation
data, not proof. No order at least 15 is inspected.

No TF4 survivor receives a lifecycle revision, the archived 18-candidate MIS fan is not reopened,
raw maximal_independent_set_count remains unchanged, no new coordinate is introduced, no
scientific experiment is frozen, and no candidate ID is allocated. TF-001158 remains next.

See docs/TF8_FIXED_SUPPORT_EQUALITY.md and
experiments/TF8-DIAG-0001/diagnosis.json.


## TF9 — fixed-support prior-art and theorem-significance audit

Status: **COMPLETE (2026-10-02).**

TF9 audits the TF7/TF8 fixed-support MIS theorem without consuming fresh data or reopening the
archived TF4 MIS fan. The classical all-independent-set ingredient is already contained in
Prodinger--Tichy (1982): among n-vertex trees the path uniquely minimizes the number of independent
sets, with value F_(n+2).

The strongest prior-art implication is Tian--Tu (2025), who prove for every tree T of order n and
independence number alpha that m(T)>=F_(n-alpha+2), sharply. Since trees are bipartite,
n-alpha(T)=nu(T), and for T!=P2 one can choose pairwise disjoint private support--leaf edges, so
s(T)<=nu(T). Hence the TF7 fixed-support value theorem m(T)>=F_(s(T)+2) is a direct corollary of a
strictly stronger published bound; Tian--Tu's sharp family contains P_s corona K1 at n=2s,
alpha=s.

Taletskii--Malyshev (2022) independently record the extension identity i(H)=mi(H corona K1) and
that adding twin leaves preserves the maximal-independent-set count. Their fixed-leaf extremal
problem and the twin-free extremal literature are genuinely different parameterizations, but these
identities already cover substantial ingredients of the TF8 equality examples.

The bounded audit did not locate an exact published statement of the support-induced injection
m(T)>=i(T[S(T)]), its equality criterion T[C(T)] edgeless, or the complete only-if classification
of all fixed-support minimizers. This is explicitly not a novelty claim. The remaining
equality-only sharpening is elementary, while the main numerical extremal theorem is subsumed by
stronger literature.

Decision: keep the theorem inside TreeForge; do not create a separate theorem repository. No
candidate lifecycle revision, no experiment registry record, no new coordinate, no new candidate
ID, and no fresh exhaustive order are created. TF-001158 remains next; orders at least 15 remain
untouched.

See `docs/TF9_FIXED_SUPPORT_PRIOR_ART.md` and
`experiments/TF9-AUDIT-0001/audit_summary.json`.


## TF10 — next-question diagnosis

Status: **COMPLETE (2026-10-03).**

TF10 audited the accumulated TF1–TF9 evidence before touching fresh data. It separated the
heavily exercised domination vocabulary from withheld core invariants, optional predecessor-inspired
quantities, and plausible absent parameters; it then reassessed target, grammar, and natural
subclasses independently.

The explicit alternatives were continuation unchanged, one new feature (Wiener index), one new
target (Wiener index), one natural subclass (subcubic trees), one restricted three-feature grammar,
and pause. None of the experiment alternatives is selected by a sufficiently specific mathematical
question rather than by search-design considerations.

Decision: **pause; no TF10 scientific experiment is frozen**. No candidate ID is allocated,
TF-001158 remains next, registries are unchanged, the archived TF4 MIS fan is not reopened, the
TF7–TF9 theorem thread remains closed, and orders at least 15 remain untouched.

See docs/TF10_NEXT_QUESTION_DIAGNOSIS.md and experiments/TF10-DIAG-0001/diagnosis.json.

## TF11 — research-question audit

Status: **COMPLETE (2026-10-03).**

TF11 treats the TF10 pause as binding and asks for a mathematical question before any new discovery
configuration. It compares five serious question directions plus continued pause, with a bounded
prior-art risk screen and no numerical scoring.

Selected question:

> Among finite trees of order (n) with exactly (q) segments, what are the minimum and maximum
> domination numbers, and which trees attain each extremum?

A segment is a maximal path whose endpoints have degree different from 2 and whose internal vertices
have degree 2; equivalently `segment_count = n - n2 - 1`, where `n2` is the number of
degree-2 vertices. The parameter is independently standard in extremal tree theory, while ordinary
domination is independently known to be sensitive to edge subdivision. The bounded TF11 literature
screen did not locate an exact theorem settling the fixed-order/fixed-segment domination extremal
problem; this is recorded only as negative bounded-search evidence, not as an openness or novelty
claim.

The competing fixed-branching-vertex question remains mathematically serious but is not selected
because segment count more directly captures the subdivision mechanism. Fixed-domination Wiener
extrema, strong-support/leaf-concentration refinements, and independent-domination interactions are
rejected at this stage because the bounded search already exposes substantial directly adjacent
literature.

No scientific experiment is frozen. In particular, `segment_count` is not yet implemented, no
relation/envelope grammar is chosen, no TxGraffiti run occurs, no candidate ID is allocated, the
candidate and experiment registries remain unchanged, TF-001158 remains next, and every order at
least 15 remains untouched.

The next session should implement and independently test `segment_count`, deepen prior-art search
around ordinary domination with fixed segment/degree-2 count, and use only burned orders 1–14 to
decide whether a single prospective envelope/recurrence representation is mathematically forced.
Only then may a one-axis experiment be frozen.

See `docs/TF11_RESEARCH_QUESTION_AUDIT.md` and
`experiments/TF11-DIAG-0001/diagnosis.json`.



## TF12 — fixed-segment domination representation diagnosis

Status: **COMPLETE (2026-10-03).**

TF12 implements exact `segment_count = n - n2 - 1` and independently checks it by explicit
maximal degree-2 path decomposition on all 5,447 burned unlabeled trees through order 14. The new
coordinate is required by the TF11 question rather than by candidate yield; no additional
segment-sequence or residue coordinate is added.

A deeper prior-art audit shows that the **numeric** fixed-((n,q)) problem is already implied by
stronger results. Lemańska's 2004 leaf bound plus (L\le q) gives the exact minimum
`ceil((n-q+2)/3)` for (q\ge3), attained by a star skeleton with all subdivisions on one arm.
Gentner--Henning--Rautenbach's 2016 exact fixed-degree-sequence maximum specializes to
`min(n-L, floor((n+L)/3))`; optimizing over the feasible fixed-(q) leaf interval
`ceil((q+3)/2) <= L <= q` gives
`min(floor(n/2), floor((n+q)/3), n-ceil((q+3)/2))`.
Paths have (q=1) and domination number `ceil(n/3)`; (q=2) is impossible.

The deterministic TF12 reproducer checks all 80 occupied ((n,q)) cells through order 14 and finds
exact agreement with both formulas and with the predicted maximizing leaf counts. This is
interpretation data only. A complete published classification of every fixed-((n,q)) minimizer
and maximizer was not located in the bounded search; negative search is not novelty evidence.

Representation decision: reject pairwise linear hulls and an extra residue grammar; treat the exact
conditioned envelope as the correct nonexperimental mathematical description of the value problem;
defer reduced-tree/subdivision recurrence until an equality-classification question is isolated;
**maintain the experiment pause**. No TF12-0001 is frozen or executed, no candidate ID is
allocated, TF-001158 remains next, and orders at least 15 remain untouched.

See `docs/TF12_SEGMENT_DOMINATION_DIAGNOSIS.md`.

## TF13 — fixed-segment domination equality audit

Status: **COMPLETE (2026-10-03).**

TF13 keeps the TF12 numerical extrema unchanged and resolves the minimum equality problem by
specializing Hajian--Henning--Jafari Rad's published cactus classification to trees. If
M=ceil((n-q+2)/3), r=3M-(n-q+2), a=ceil((q+3)/2), and d=q-L, then a q>=3 tree is a
fixed-(n,q) minimizer exactly when 0<=d<=min(r,q-a), L=q-d, and the tree belongs to the
published class G_0^(r-d). Lemańska's pairwise leaf-distance condition is exactly the residual
m=0 slice, not the whole rounded equality class.

For the maximum, if M=gamma_max(n,q), the complete maximizing leaf set is the integer interval

max(a,3M-n) <= L <= min(q,n-M).

For each such L, the admissible degree sequences are exactly those obtained by partitioning L-2
into B=q+1-L positive branch excesses, together with n-q-1 degree-2 entries and L leaves.
Gentner--Henning--Rautenbach guarantee at least one maximizing realization for each such sequence.
TF13 also proves, for trees of order at least three, gamma(T)=n-L iff every nonleaf is a support.

The complete maximizing tree-isomorphism class remains unresolved: burned order 6 already contains
two nonisomorphic trees with degree sequence (3,2,2,1,1,1) and q=3 but domination numbers 2 and 3.
Thus degree-sequence attainability cannot be promoted to an all-realizations classification.

Minimum status: **DIRECT_COROLLARY_OF_PUBLISHED_CLASSIFICATION**.
Maximum status: **PARTIALLY_RESOLVED**.

No TF13 scientific experiment is frozen or executed, no candidate ID is allocated, TF-001158
remains next, and order 15 remains sealed. See docs/TF13_SEGMENT_DOMINATION_EQUALITY.md and
experiments/tf13_segment_domination_equality.py.


## TF14 — fixed-segment maximum realization equality

Status: **COMPLETE (2026-10-03).**

TF14 audits the realization-level proof machinery behind the 2016 fixed-degree-sequence maximum and
Kurnosov's 2020 interval theorem. Kurnosov's Theorem 3 gives only sufficient maximum-realization
forms; its Remark 1 explicitly says they are not necessary, and its transformations prove
reachability rather than a local maximum iff criterion.

The maximum residue splits more sharply than TF13 recorded. For every optimizing leaf count (L),
both the strict `n-L` branch and the tie branch are already completely characterized by TF13:
`gamma=n-L` iff every nonleaf is a support. The only remaining branch is
`floor((n+L)/3)<n-L`.

On that strict rounded branch, Favaron's independent-domination bound yields the exact iff reduction
`gamma=floor((n+L)/3)` iff
`gamma=i=floor((n+L)/3)`. Published characterizations of `(gamma,i)`-trees therefore
supply one half of the structure. If (n+Lequiv0pmod3), Favaron's own equality classification
supplies the other half, so the residue-zero branch is a
**DIRECT_COROLLARY_OF_PUBLISHED_CLASSIFICATIONS**. The bounded audit did not locate an exact
classification for (n+Lequiv1,2pmod3).

TF14 also proves the exact support-core reduction
`gamma=h+tau`, where all support vertices are preselected and `tau` is the minimum number
of nonleaf non-support vertices needed to finish domination. Writing (s) for the size of that
core and (delta=L-h), strict-rounded maximality is exactly
`tau=floor((s+2 delta)/3)`. This is a structural normalization, not a new registry invariant.

Overall maximum-equality status remains **PARTIALLY_RESOLVED**, with only the strict-rounded
residue-1/2 saturation problem unresolved after the bounded audit. No experiment is frozen or
executed, no candidate is allocated, TF-001158 remains next, and orders at least 15 remain
untouched.

See `docs/TF14_SEGMENT_DOMINATION_MAXIMUM_EQUALITY.md`.

## TF15 — strict-rounded defect classification and fixed-segment closure

Status: **COMPLETE (2026-10-03).**

TF15 attacks only the strict-rounded residue-1/2 realization problem left by TF14. The complete
constructive `(gamma,i)`-tree grammar of Dorfling--Goddard--Henning--Mynhardt (2006) supplies an
exact local recurrence for `epsilon(T)=n(T)+L(T)-3i(T)`. Observation 11 lets every nontrivial
`(gamma,i)`-tree use a construction starting from the D-labeled P1. Its mandatory first T1 produces
a P2 with defect 1. Thereafter the defect increments are:

- T1: +1 at a leaf attacher, +2 at a nonleaf;
- T2/T3: -1 at a leaf attacher, 0 at a nonleaf;
- T4/T5/T6: 0 at a leaf attacher, +1 at a nonleaf.

Thus the final defect is exactly the sum of published local construction changes. On TF14's strict
rounded branch, residue 1 maximizers are exactly the published `(gamma,i)` constructions ending
with defect 1, and residue 2 maximizers are exactly those ending with defect 2. Both subcases have
status **TREEFORGE_ELEMENTARY_DERIVATION_FROM_PUBLISHED_RESULTS**. The construction is not unique,
but the endpoint sum is the graph invariant `n+L-3i`.

Cabrera-Martínez's 2024 refined domination bound independently yields
`2delta+|SL(T)|<=epsilon`, where `delta=L-h`. Hence residue 1 forces `delta=0` and at most
one support-link; residue 2 allows only `delta=0, |SL|<=2` or `delta=1, |SL|=0`. Burned
orders 1--14 show that equality in this support restriction is not necessary, so it is a useful
necessary filter rather than the classification.

Together with TF13 and TF14, the fixed-(n,q) numerical extrema and both equality sides are now
complete at a recursive structural level. Decision: **close the fixed-segment thread and return to a
research-question pause**. No TF15-0001 is frozen or executed, no candidate is allocated, no
default invariant is added, TF-001158 remains next, and orders at least 15 remain untouched.

See `docs/TF15_SEGMENT_DOMINATION_ROUNDED_DEFECT.md` and
`experiments/tf15_segment_domination_rounded_defect.py`.


## TF16 — minimum-dominating-set multiplicity question audit

Status: **COMPLETE (2026-10-03).**

TF16 verifies the TF15 closeout at merged main
`5652e29c5f6ed450482108b99503b11c087356e6`, exact PR #21 head
`1a309f2a0c7792dc4b3f084f72ce9721e0e83080`, successful exact-head CI
`37139422782`, and successful post-merge CI `37139661763`. Candidate and experiment
registries plus the invariant catalog/core implementation are unchanged across TF15.

The fixed-segment programme stays closed. A bounded landscape audit also rejects reopening the
TF4/TF7--TF9 MIS thread, the completed Greedy-Uniformity predecessor programme, a branching-count
variant of the segment question, a generic independent-domination reset, and implementation-led
distance-index work.

One independent question survives: if (zeta(T)) is the number of minimum dominating sets of a
tree, determine
[
M_n=max{zeta(T): |V(T)|=n, T	ext{ a tree}}
]
and characterize all extremizers. Alvarado--Dantas--Mohr--Rautenbach (2019),
Taletskii (2023), and Petr--Portier--Versteegen (2024) give strong exponential bounds and
restricted-class structure, but the bounded TF16 search did not locate an exact unrestricted
(n)-vertex extremal theorem. Negative search is not novelty evidence.

The theorem-first audit proves the elementary forced-strong-support restriction and identifies a
rooted min-plus/count DP as the exact natural computation. It does not yet produce a sufficiently
specific extremizer grammar to test prospectively. Therefore TF16 freezes no experiment, adds no
invariant, allocates no candidate, keeps TF-001158 next, and leaves every order at least 15
untouched.

End state: **A — new question justified, experiment not yet warranted.**

See `docs/TF16_RESEARCH_QUESTION_AUDIT.md`.


## TF17 — exact minimum-dominating-set multiplicity machinery and structural diagnosis

Status: **COMPLETE (2026-10-03).**

TF17 verifies TF16 provenance, implements the exact three-state rooted min-plus/count DP for
`(gamma(T),zeta(T))` as non-default theorem-support machinery, and validates it independently:
brute-force gamma/zeta agreement on every unlabeled tree through order 8, root invariance through
order 8, and gamma agreement with the pre-existing exhaustive implementation on all 5,447 burned
trees through order 14.

The burned exact maxima are
`1,2,1,4,3,8,8,16,18,32,40,64,84,128`.
For every burned even order `n=2k`, the extremizers are exactly all coronas
`H corona K1` with H a k-vertex tree, hence zeta=2^k. For every burned odd order
`3<=n<=13`, the unique extremizer is Taletskii's balanced `W_(a,b)`, whose published
formula `3*2^(a+b)-2^a-2^b` is maximized by balancing a and b.

This exposed parity grammar is **not** frozen as a conjecture. Taletskii's published degree-5
module-joining construction grows strictly faster than sqrt(2)^n; at order 38 it already yields
`736^2 > 2^19`, so the even corona pattern is analytically non-global. TF17 proves safe
twin-leaf pruning for supports with at least three leaves and records exact equality of rooted
(A,B,C) profiles as a substitution principle, but no finite rooted-state dominance theorem has
been obtained.

End state: **A — exact machinery validated, structural extremizer theory still insufficient.**
No experiment is frozen, no candidate is allocated, the helper is not promoted to the default
invariant registry, TF-001158 remains next, and orders at least 15 remain untouched.

See `docs/TF17_MINIMUM_DOMINATING_SET_MULTIPLICITY.md`.


## TF18 — rooted-state dominance and finite-grammar audit

Status: **COMPLETE (2026-10-03).**

TF18 formalizes the TF17 A/B/C signature as an exact pendant boundary object and proves a
context-safe projective replacement theorem. After subtracting one common A-state baseline, equal
normalized cost shapes preserve every boundary-state cost tie; coordinatewise larger exact state
counts therefore cannot decrease zeta under pendant substitution, and strict improvement in every
feasible state strictly improves zeta. Ordinary coordinatewise cost dominance is not safe: a
same-order burned order-8 pair has no larger replacement costs and no smaller replacement counts
but loses an A/B optimum tie and drops closed zeta from 2 to 1.

Taletskii's and Petr--Portier--Versteegen's structural mechanisms are translated into the same
states. Repeated degree-2 preleaf branches are the rooted P2 gadget
`A=B=(1,1), C=infeasible`; the repeated-child recurrence gives the `2^m-1` factors in W-type
calculations. The five-vertex PPV terminal branch has
`A=(2,1), B=(2,2), C=(2,2)`, giving exactly five optimum completions under a selected parent and
three under an externally dominated unselected parent. Their terminal degree restrictions remain
specific to a fixed-gamma/strong-support minimal counterexample, while Taletskii's smaller
replacements are per-vertex growth arguments rather than exact same-order replacements.

Only after this preorder was proved, orders 1--14 were diagnosed. At order 14 there are 3,782 exact
rooted signatures, 3,474 projective interfaces, 37 normalized cost shapes, and 119 weakly
projectively undominated interfaces. This is useful compression but not a finite-state theorem.
Analytically, rooted stars have unbounded normalized cost gaps and endpoint-rooted paths have
unbounded exact count vectors even at maximum degree two.

Decision: preferred end state **A**. Freeze no TF18 scientific experiment, allocate no candidate,
leave `TF-001158` next, keep `minimum_dominating_set_count` non-default, and keep every order
at least 15 untouched. Any continuation should attack tree-realizable context offsets or a
same-order budgeted replacement theorem before any fresh data are exposed.

See `docs/TF18_ROOTED_STATE_DOMINANCE.md`.


## TF19 — exact tree-context quotient and budget compensation

Status: **COMPLETE (2026-10-04).**

TF19 resolves the local completeness question left by TF18.  A one-hole tree context rooted at the
attachment parent sends the exact reverse message
`(min(A,B,C), min(A,B), A)`; its normalized costs are therefore restricted to exactly three
patterns: `(0,0,0)`, `(0,0,1)`, and `(0,1,1)`.  The resulting exact boundary congruence is
strictly coarser than projective equality: only the three realizable lower faces and exact counts on
states exposed by at least one face matter.  Three canonical path contexts separate all quotient
classes.

The quotient does **not** make the unrestricted problem finite.  Endpoint-rooted `P_(3k)` have
one fixed lower-face pattern but pairwise distinguishable exposed count vectors, proving infinitely
many exact context classes even at maximum degree two.  TF19 also proves a conditional same-order
compensation lemma: any number of released vertices may be spent as extra private leaves at an
already strong support without changing `gamma` or `zeta` in any outside context.  Arbitrary
padding is false, as `P2 -> P3` and the destruction of Q2's A/B tie show.

Decision: preferred end state **A**.  The rooted-interface programme should pause unless a new
global forcing/replacement theorem is found.  No TF19 experiment is frozen, no candidate is
allocated, `TF-001158` remains next, the count helper remains non-default, and all orders at
least 15 remain untouched.  See `docs/TF19_TREE_CONTEXT_COMPLETENESS.md`.

## TF20 — global compensation and bankless structure

Status: **COMPLETE (2026-10-04), experiment pause preserved.**

TF20 leaves the now-complete local context-quotient programme and attacks exact order bookkeeping
globally. The TF19 three-face preorder yields an exact banked replacement theorem: a smaller
context-improving pendant gadget can spend its vertex deficit at an untouched strong support.

A stronger global theorem covers every strict smaller **isolate-free forest** improvement with
deficit at least two. Write the deficit as `2a+3b`, add disjoint P2/P3 components, use
`zeta(P2)=2`, `zeta(P3)=1`, and invoke Taletskii's same-order forest-to-tree lemma. The only
generic missing budget is therefore one vertex. That gap is real: every one-leaf extension of P4
has fewer minimum dominating sets than P4.

This identifies Taletskii's unresolved exact-order obstruction precisely. After universal vertices
are excluded, his empty-vertex reduction deletes exactly one vertex, strictly improves multiplicity,
creates no isolated component, and occurs in a class with no strong supports. Strong-support banking
therefore cannot repair it.

TF20 nevertheless obtains strong global structure. An exact order-extremizer has at most one strong
support; if one exists it has exactly two private leaves, is the unique universal vertex, and those
two leaves are its only empty neighbours. Every strong-bankless tree has a canonical marked
support-core representation obtained by deleting all leaves and marking the former supports, with
every core leaf marked. The representation is complete but not finite: the marked core is an
arbitrary tree.

Taletskii's S-part-size-at-most-three moves are audited as genuine same-order forest exclusions once
the no-empty hypothesis is available. Petr--Portier--Versteegen terminal restrictions remain tied
to their fixed-domination-number functional and are not imported into the fixed-order problem.

No complete global grammar or recurrence follows, so TF20 derives no M_15 value, freezes no
experiment, allocates no candidate, leaves `TF-001158` next, keeps
`minimum_dominating_set_count` non-default, and does not inspect order 15. The next theorem target
is only the residual one-vertex deficit in the strong-bankless no-universal empty-vertex class.

See `docs/TF20_GLOBAL_COMPENSATION_STRUCTURE.md`.



## TF21 — exact one-vertex obstruction

Status: **COMPLETE (2026-10-04), experiment pause preserved.**

TF21 proves the missing pairing theorem for the no-universal side. If u and v are two distinct
empty vertices, Taletskii deletion at u gives a strict smaller-forest gain; v remains empty in its
surviving component, so deleting v cannot reduce that gain. The double deletion is isolate-free,
has deficit two, preserves gamma, and has larger zeta. TF20's d=2 compensation then gives a strict
same-order contradiction. Hence a no-universal exact extremizer has at most one empty vertex.

The unique-empty residue is characterized exactly enough to expose why the programme still does not
close. Deleting the sole empty hub u gives rooted components containing no universal or empty
vertices; every component vertex is flexible, each attachment root has A=B at the component gamma,
and C is not cheaper. Thus
`zeta(T)=product zeta(T_i)-product zeta^-(T_i,r_i)`.
In the TF20 marked support core, u is unmarked and internal.

This class is not locally bounded. The subdivided k-arm star has unique empty centre, marked core
K1,k, zeta `2^k-1`, and deletion forest kP2 with zeta `2^k`, so the strict gain can be
only one and its ratio tends to one. The k=2 case is P5, the unique exact order-5 extremizer.
Therefore no universal d=1 compensator can turn every strict Taletskii deletion into a strict
same-order improvement. A direct fresh connector merely recreates the missing all-roots-omitted
constraint; reconnect-then-subdivide already fails on 2P2 -> P4 -> P5.

Decision: preferred end state **B/D**. Multi-empty configurations are closed, but the one-empty
hub class and the separate TF20 strong-banked class remain. No M_15 value or order-15 family is
derived, no experiment is frozen, no candidate is allocated, `TF-001158` remains next,
`minimum_dominating_set_count` remains non-default, and order 15 remains untouched.

See `docs/TF21_ONE_VERTEX_COMPENSATION.md`.


## TF22 — unique-empty hub global structure

Status: **COMPLETE (2026-10-04), unrestricted multiplicity programme paused.**

TF22 identifies TF21's all-flexible deletion components with the established class of nontrivial
gamma-excellent trees. Burton--Sumner's critical/stable theory and Samodivkin's corona-block
reformulation then give a complete recursive shape grammar. TF22 proves that an actual unique-empty
attachment root is stable, and conversely that joining a new hub to stable vertices of at least two
nontrivial gamma-excellent trees produces exactly a no-universal tree with one empty vertex.

The exact hub objective does not collapse with that structural grammar. For a stable-root component,
write `s=zeta(R)` and `alpha` for the number of gamma-sets containing the root. With the other
components fixed, the hub objective is `(A-B)s+B alpha` with `A>B>0`. Consequently
context-universal same-order component replacement is exactly coordinatewise dominance in
`(s,alpha)`; a two-component exchange has the analogous exact coordinates `(S,Q)`.

TF22 gives analytic counterfamilies to the remaining natural closure attempts. On
`P_(3m+1)`, rerooting from a stable vertex to a critical one can strictly lower the whole hub
objective. Within Taletskii's `W_(a,b)` family, balancing `W_(q-1,q+1)` to `W_(q,q)`
raises standalone zeta but lowers the rooted inclusion coordinate, and valid P2 versus P7 contexts
reverse which same-order component is better. Hence there is no context-independent scalar ranking
or balancing rule capable of closing the unique-empty class by the TF17--TF22 replacement methods.

The no-empty S-decomposition side still lacks a complete exact-order recurrence, and TF20's separate
strong-banked class is not excluded above the small P3 exception. Therefore TF22 derives no M_15
prediction, freezes no experiment, allocates no candidate, leaves `TF-001158` next, keeps the
minimum-dominating-set helper non-default, and leaves every order at least 15 untouched.

See `docs/TF22_UNIQUE_EMPTY_HUB.md`.
