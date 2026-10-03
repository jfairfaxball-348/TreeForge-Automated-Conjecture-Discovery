# Failure and lesson ledger

This file is append-only in spirit: corrections add entries rather than erasing the research path.

## 2026-10-01 — TxGraffiti runtime package unavailable in local execution environment

The current public TxGraffiti source and API were inspected at `RandyRDavila/TxGraffiti2@e37126da53b84150d142a5d61202b61f78521fcc`, package version `0.4.1`. The local execution environment used for TF0 had no network access to PyPI, so `pip install txgraffiti==0.4.1` could not be completed locally. This is an environment limitation, not evidence of a TxGraffiti defect.

Mitigation: TreeForge pins the package version, isolates it behind a narrow adapter, unit-tests the adapter contract with a stub backend, and configures GitHub Actions to install the real optional dependency and run a live import/API smoke test.

## Standing lesson

Do not silently repair away failed conjectures, counterexamples, dependency mismatches, leaked holdout data, or broken assumptions. Record the failure, the affected experiment IDs, and the corrective action.

## 2026-10-01 — CI run #1 failed before calibration

GitHub Actions run `36849349936` installed the pinned `txgraffiti==0.4.1` successfully, but pytest collection failed because `tests/test_calibration.py` imported `experiments.calibration` while `experiments/` had not been made an importable package in the clean installed environment. Local checks had used an explicit repository-root `PYTHONPATH`, which masked the packaging mistake.

Corrective action: add `experiments/__init__.py` and require the clean GitHub Actions environment to pass before TF0 is marked complete. The failed run remains part of the repository history and this ledger.

## 2026-10-01 — CI run #2 exposed pytest import-path assumptions

Run `36849570117` showed that adding `experiments/__init__.py` alone was insufficient: the clean pytest entry-point invocation still did not place the repository root on the test import path, so `experiments.calibration` remained unavailable.

Corrective action: make the test path explicit with `pythonpath = [".", "src"]` and invoke tests as `python -m pytest -q` in CI. This removes dependence on the local shell's `PYTHONPATH` and makes the intended import boundary explicit.

## 2026-10-01 — CI run #3 reached static analysis and failed style policy

Run `36849715804` passed the full unit-test suite, including the live TreeForge adapter call against installed `txgraffiti==0.4.1`, and passed byte-compilation. It then failed Ruff on a modern-stdlib import rule, one import-order rule, and line-length findings.

Corrective action: adopt `datetime.UTC`, import `Callable` from `collections.abc`, normalize the live-test import block, and explicitly exclude `E501` from the initial lint policy. Line wrapping is a formatting preference rather than a research-integrity gate; semantic/import/static errors remain enabled.

## 2026-10-01 — TF1 CI run #1 stopped at Ruff before discovery

GitHub Actions run `36852332959` passed installation, the full unit suite (including the live TxGraffiti adapter call), and byte-compilation, then failed static analysis before the benchmark or TF1 discovery steps ran. Ruff reported four B023 loop-variable closure findings in the new benchmark harness, one import-order finding, and one unused import in the TF1 leakage test.

This was a pre-discovery implementation/style failure, so no candidate output from the run is valid or retained as TF1 evidence. The frozen TF1-0001 scientific specification was not changed. Corrective action: bind the benchmark loop variable explicitly in timing lambdas and normalize the test import block, then rerun CI from a new source commit.

## 2026-10-01 — TF1 CI run #2 mistook an empty candidate batch for infrastructure failure

GitHub Actions run `36852483813` passed installation, all unit tests, the live TxGraffiti API check, byte-compilation, Ruff, the calibration smoke test, and the TF1 benchmark. The frozen TF1-0001 discovery then completed successfully with TxGraffiti `0.4.1`, 200 discovery trees, 235 untouched holdout trees, no feature-audit or standard-identity violations, and **zero generated candidates**.

The workflow nevertheless failed because it used `test -s` on `observed_candidates.jsonl`, incorrectly requiring a nonempty candidate registry artifact. This is contrary to TreeForge's research standard: an empty candidate batch is a valid controlled-discovery result and must not be converted into artificial progress. Corrective action: require the file to exist (`test -f`) but permit it to be empty. The frozen scientific specification was not changed.


## 2026-10-01 — TF2 freeze CI caught an incomplete test fixture before generation

GitHub Actions run `36863952291` failed in the unit-test step before any TF2 candidate generation was enabled or executed. The new TF2 lifecycle runner correctly required the frozen `hypotheses` field when constructing candidate records, but the synthetic test fixture omitted that field and raised `KeyError: 'hypotheses'`.

The scientific TF2-0001 specification was not changed. Corrective action: add the frozen hypothesis list to the test fixture and rerun CI. This was runner/test plumbing only and did not expose the TF2 holdout or produce research candidates.


## 2026-10-01 — TF2 freeze CI reached static analysis and caught import policy

GitHub Actions run `36864222486` passed all 19 unit tests and byte-compilation, then failed Ruff because the new exact-expression evaluator imported `Mapping` from `typing` rather than `collections.abc`.

No TF2 candidate generation had been enabled or executed. Corrective action: use the modern standard-library import and rerun the unchanged frozen TF2-0001 protocol.


## 2026-10-01 — TF2 first scientific execution exposed heuristic-scaling bottleneck before valid output

GitHub Actions run `36875119955`, using intended TF2-0001 scientific source commit `4e25b666b4c650047387d131ce5d05ff5c693521`, passed installation, the full unit suite, byte-compilation, Ruff, the deterministic calibration smoke test, and the live TF2 zero-yield diagnosis. It then remained inside the frozen TF2-0001 scientific step without producing the required scientific artifact within the expected runtime envelope. PR #5 was closed and no candidate, holdout, or adversarial result from that attempt is accepted as TF2 scientific evidence.

A discovery-only performance probe in successful run `36887027180` used only the already-burned discovery orders 2–10. The 8-dimensional SciPy/Qhull construction itself completed in approximately 0.48 seconds but returned 42,068 facets. Inspection of pinned TxGraffiti `0.4.1` showed that its streaming Morgan/Dalmatian application repeatedly scans or reconstructs state across this large facet stream. The bottleneck is therefore adapter/upstream heuristic application cost, not corpus generation, Qhull itself, the TF2 holdout, or a scientific zero/survivor result.

Corrective action: keep the frozen TF2-0001 target, features, methods, heuristics, post-processors, split, normalization, and adversarial set unchanged. For TreeForge's normalized always-true hypothesis case, cache the exact pointwise minimum used by Dalmatian and exploit the fact that Morgan cannot reject when every generated conjecture has the identical hypothesis mask. A live pinned-package equivalence test compares the complete ordered output of this optimized path with the unoptimized upstream pipeline on a nondegenerate dataset before the replacement scientific run. The replacement run must use a new exact source commit.


## 2026-10-01 — TF2 result materialization initially rejected preserved TF0 legacy revision

GitHub Actions run `36890309397` passed installation, unit tests, byte-compilation, Ruff, calibration, and the TF2 diagnostic, then failed only while materializing the already-completed TF2 scientific artifact. The finalizer applied the current candidate schema to the original `TF-000001` revision 1, which intentionally predates the later `source_commit` field and was preserved by TF1 revision 2 rather than rewritten.

No TF2 scientific computation was rerun, no holdout data were changed, and no candidate result was altered. Corrective action: the finalizer now has an explicit read-only validation exception for that single preserved TF0 legacy revision while requiring the current schema for every later record.


## 2026-10-01 — late completion of the first TF2 scientific execution was observed after replacement-run planning

GitHub Actions run `36875119955` was provisionally classified as a pre-valid-output performance failure after it remained inside the TF2-0001 scientific step far beyond the expected runtime envelope and PR #5 was closed before a scientific artifact was available for inspection. The run later completed successfully and uploaded artifact `11180206717`.

The late artifact was audited against the repaired authoritative run. Its 998 final TxGraffiti statements are identical in order and structured content to those from scientific run `36888114138`; discovery, holdout, and adversarial rows are identical after removing the source-commit provenance field; candidate lifecycle outcomes are identical. Its dataset hashes differ because TreeForge intentionally includes the exact scientific source commit in serialized corpus rows.

Corrective interpretation: preserve run `36875119955` and the contemporaneous PR #5 closure as process history, but do not describe the late artifact as a distinct scientific variant or use it as the authoritative TF2 record. Run `36888114138`, source commit `d091d88889fa72322bfc49a5531bc30b1f31b049`, remains authoritative because it uses the equivalence-tested performance repair and records the complete single-pass stage counts. The frozen TF2-0001 scientific specification was unchanged throughout.


## 2026-10-01 — TF3 diagnostic complexity parser over-escaped regexes

GitHub Actions run `36906621879` successfully exercised installation, unit tests, byte-compilation,
Ruff, calibration, the live TF2 adapter diagnostic, and the predeclared TF3 generation variants.
However, the TF3 diagnostic script over-escaped the regular expressions used only to count RHS
feature symbols and coefficient denominators. The generation-stage counts and timings themselves
were valid, but the reported RHS-support/denominator summaries and the derived support-gate count
were invalid and are not used for TF3 design.

No TF3 candidate IDs were allocated, no TF3 scientific generation was run, and the timing-only
order-13 feasibility probe persisted or reported no invariant values. Corrective action: fix the
diagnostic parser, add a focused parser unit test plus internal sanity assertions, and rerun the
same predeclared diagnostic comparison without changing its alternatives.

## 2026-10-01 — TF3 method-selection unit fixture compared unrelated object identities

GitHub Actions run `36906556561` failed in the unit-test step before the TF3 diagnostic ran.
The adapter method-selection code had correctly selected the fake `ratios` object supplied by its
loader, but the test constructed a second independent fake-module mapping and compared object
identity across the two mappings.

No TF3 diagnostic comparison, scientific generation, candidate ID allocation, or fresh validation
evaluation occurred in this run. Corrective action: retain one fake-module mapping for both loader
injection and assertion, then rerun the unchanged method-selection implementation.

## 2026-10-01 — first TF3 diagnostic-parser correction remained over-escaped

After run `36906621879` exposed the diagnostic-only regular-expression error, commit
`d46602df21f4d18e0b442b4b1b05ff2f9f6e3e76` added a focused parser unit test and internal
sanity assertions. GitHub Actions run `36907013799` then failed that unit test, proving the first
literal correction was still over-escaped. The diagnostic step did not run.

No scientific configuration changed and no TF3 candidate or holdout comparison was produced.
The regex literals were corrected without changing the predeclared diagnostic alternatives.
Run `36907058956` subsequently passed the complete suite and the unchanged diagnostic.

## 2026-10-01 — TF3 scientific workflow invoked the frozen runner in script mode

GitHub Actions runs `36914094286` and `36914294452` both passed their preflight checks but
failed immediately on `ModuleNotFoundError: No module named 'experiments'` when the workflow
used `python experiments/tf3_discovery.py`. The second run repeated the same failure because an
intended workflow text substitution had not actually changed the command.

Both failures occurred at module import before discovery generation, candidate allocation,
candidate-batch persistence, or order-13 construction, so neither produced TF3 scientific evidence.
Corrective action: replace the workflow command explicitly with
`python -m experiments.tf3_discovery` and rerun the complete unchanged preflight. Scientific
run `36914647703` then completed successfully from source commit
`e23b44d24a7b87d6f67aa18749059540934b2767`. The frozen TF3 specification was unchanged.

## 2026-10-01 — TF3 result materialization exposed an unnecessary exponential invariant computation

The first result-materialization workflow, run `36915447930`, called the full TF3 invariant set on
the already-exposed order-25 six-arm spider while preparing the post-gate interpretation of
`TF-001010`. That unnecessarily included the exact maximal-independent-set counter, whose current
implementation enumerates all vertex subsets. This was finalization overhead, not a scientific
calculation or change to any frozen evidence.

Corrective action: compute only `order`, `domination_number`, and `matching_number` for that
known counterexample. The scientific artifact, hashes, holdout outcomes, and adversarial outcomes
were not changed.

## 2026-10-01 — post-TF3 materialization invalidated pre-execution registry assumptions in tests

Materialization validation runs `36915684035` and `36915894349` correctly rejected two test
assumptions that were valid only before TF3 execution. One frozen-spec test expected
`CandidateRegistry.next_id()` to remain `TF-001000` and expected no TF3 experiment record;
one TF2 result test expected the entire candidate registry to end permanently at `TF-000999`.

The generated TF3 records themselves were valid, and the workflow committed nothing while validation
failed. Corrective action: keep the frozen spec assertion that TF3's starting ID was
`TF-001000`, move post-execution registry facts into dedicated TF3 result tests, and scope TF2
lineage assertions to TF2 candidate IDs. Materialization run `36916149651` then passed the full
suite before committing the append-only TF3 record.

## 2026-10-02 — TF4 freeze validation exposed cross-order ambiguity in the legacy bare tree code

GitHub Actions run `36974147991` failed in the unit-test step before any TF4 scientific
execution. The new TF4 hostile-set test incorrectly treated `canonical_tree_code(graph)` by itself
as an exact identity across different orders and asserted that the 19 frozen hostile instances must
produce 19 distinct bare code strings.

The failing pair was not a duplicated tree: `P18` and `P19` have different orders and therefore
cannot be isomorphic. The historical AHU-style encoding can nevertheless give the same bare string
across orders because the extra wrapper used for a two-center tree can coincide with the rooted
encoding of a one-center tree. Existing corpus rows always serialize `order` separately, and
unlabeled-tree generation deduplicates codes within each fixed order, so this discovery does not
change or invalidate the preserved TF0-TF3 dataset hashes.

Corrective action: preserve the historical code function and all prior hashes, document its
cross-order limitation, add `canonical_tree_identity(graph) = (order, canonical_tree_code)`, and
use that exact pair for TF4 cross-order hostile-set uniqueness/disjointness checks. The frozen TF4
scientific target, features, pairwise generator, order-14 holdout, and hostile-family parameters were
not changed. No TF4 candidate ID was allocated and no fresh validation value was inspected.

## 2026-10-02 — TF4 cross-order identity helper was committed with escaped newlines

After run `36974147991` exposed the need for an explicit cross-order tree identity, GitHub Actions
run `36974559986` failed during pytest collection before any diagnostic or scientific step. The
new `canonical_tree_identity` helper had been written with literal `\\n` escape text rather than
actual line breaks, causing a Python `SyntaxError` on import.

No TF4 candidate generation, order-14 evaluation, or fresh hostile-tree evaluation occurred.
Corrective action: replace the malformed helper text with valid Python while keeping its semantics
unchanged: exact cross-order identity is `(order, canonical_tree_code)`, and the historical bare
code remains unchanged for all prior hashes and records.



## 2026-10-02 — TF4 exposed-data interpretation probe used an unsupported corpus-role label

GitHub Actions run `36984250743` failed after the successful authoritative TF4 scientific run while
executing a post-gate interpretation probe on already-exposed orders. The probe passed a role label
that `experiment_corpus_rows` does not accept and raised
`ValueError: role must be discovery or holdout`.

This failure occurred after TF4's candidate batch, fresh order-14 holdout, and frozen hostile-set
evaluation were already complete. It exposed no new fresh data and changed no candidate or frozen
scientific setting.

Corrective action: use a supported role value for the exposed-data reconstruction only. Runs
`36984350503` and `36984350541` then completed successfully with the same scientific record.

## 2026-10-02 — TF4 result materialization exposed pre-materialization and terminal-registry test assumptions

After authoritative scientific run `36983184665`, CI runs `36985331317` and
`36985361656` failed because newly added TF4 result tests expected compact materialized files
(`manifest.json`, `interpretation_summary.json`) before those generated files had been committed.

One-shot materialization run `36985361788` then generated the compact TF4 record correctly but
validation caught a separate historical TF3 test asserting that
`CandidateRegistry.next_id()` must remain `TF-001012`. Once TF4 had append-only candidate IDs
through `TF-001157`, that assertion was no longer a valid TF3 invariant. It was removed without
weakening TF3's own lineage or result checks.

CI run `36985673530` still ran against the pre-materialization commit and therefore again saw the
compact TF4 result files absent, while paired materialization run `36985673542` completed the
authoritative result commit. Subsequent CI was green.

These failures were result-materialization/test-ordering issues only. They did not rerun or alter
TF4-0001 scientific generation, the 99-candidate frozen batch, the order-14 holdout, the 19-tree
hostile set, or any lifecycle outcome.

## 2026-10-02 — TF4 exact-form prior-art search did not surface a stronger fixed-diameter theorem

TF4's bounded audit of TF-001028 searched the exact normalized form and closely related
domination/diameter bounds and correctly recorded only a negative search result. TF5 broadened the
same candidate-specific audit to extremal domination at fixed order and diameter and found
Gu, Meng, Zhang and Wan (2013), Lemma 2.3. Combined with Ore's classical isolate-free bound, that
published result directly implies TF-001028.

This does not invalidate the TF4 audit because TF4 explicitly stated that negative search was not
novelty evidence and left the candidate in NOVELTY_AUDIT. The process lesson is that a bounded
audit for a simple two-parameter candidate should include fixed-parameter extremal formulations,
not only exact algebraic-string variants. TF5 records the candidate append-only as KNOWN_RESULT;
no novelty or theorem-repository claim is made.

## 2026-10-02 — TF5 reproducibility test initially compared different summary schemas

GitHub Actions run `37031645190` at commit
`5e340e069be3a9ed350bb4b8d0ffa663bdfc3630` reached the unit-test step and failed
`tests/test_tf5_analysis.py::test_tf5_summary_reproduces_from_exposed_data`. The deterministic
TF5 analysis helper emitted an extra per-candidate `stability_details` field that the committed
compact `analysis_summary.json` intentionally omitted. The substantive derived values shown in
the comparison agreed; this was a serialization-schema mismatch, not a counterexample, proof
failure, lifecycle change, or fresh-data event.

Corrective action: remove the nonessential verbose field from the generated compact summary so the
reproducer and committed artifact use one schema. Commit
`5adee4117017de3765b63f08287e78eba0d2b40f` applied that correction and CI run
`37031706953` then passed. TF-001028's statement, prior-art implication, revision-7
`KNOWN_RESULT` classification, exposed/family analyses, MIS-facet diagnosis, and decision not to
freeze a new experiment were unchanged.


## 2026-10-02 — TF6 diagnosis entry-point failure

- GitHub Actions runs `37045955391` and `37046259205` reached the new TF6 exposed-data diagnosis only after unit
  tests, compileall, Ruff, deterministic calibration, TF2 diagnosis, and TF4 diagnosis had all
  passed.
- The TF6 step then failed immediately with
  `ModuleNotFoundError: No module named 'experiments'` because the workflow invoked
  `python experiments/tf6_mis_diagnosis.py` while that script imports the existing
  `experiments.tf5_analysis` module.
- This was an entry-point/import-path mistake, not a mathematical failure, candidate event, data
  event, or TxGraffiti event. The TF6 script had not begun exposed-corpus construction and no fresh
  data existed to consume.
- Fix: invoke the diagnosis as a module,
  `python -m experiments.tf6_mis_diagnosis`, matching the repository's earlier TF3 lesson about
  package-aware scientific entry points.
- Scientific consequence: none. TF0--TF5 provenance and all frozen data boundaries remain unchanged.


## 2026-10-03 — TF12 first PR-head CI missed one removed `ceil` call

PR #18 run `37112335549` reached the unit-test step and failed only in the new TF12 deterministic
diagnosis. During cleanup, the reproducer had replaced floating `ceil(... / 3)` uses with exact
integer arithmetic and removed the `ceil` import, but one path-case branch of
`_maximum_formula` still called `ceil`. Both TF12 tests therefore stopped at (P_2) with
`NameError: ceil is not defined` before the new 80-cell extremal assertions ran.

Corrective action: replace that remaining call with exact `(order + 2) // 3` arithmetic. This was
a deterministic implementation/cleanup error only. It did not run TxGraffiti, inspect order 15,
allocate a candidate, alter either registry, or change any mathematical formula or prior-art
conclusion.

## 2026-10-03 — TF12 equality search did not surface the rounded tree classification

TF12 correctly separated Lemańska's real-valued equality theorem from the unresolved fixed-(n,q)
equality question and explicitly treated its negative bounded search as non-novelty evidence.
TF13 searched the rounded leaf-bound equality problem directly and located Hajian--Henning--Jafari
Rad's 2019 tree families and their 2022 cactus classification. Specializing their Theorem 1 to
trees closes the ceiling-slack cases G_0^0, G_0^1 and G_0^2.

Scientific consequence: the TF12 numerical formulas, data boundary, and experiment-pause decision
are unchanged. The minimum equality residue is smaller than TF12's bounded audit suggested and is
now a direct corollary of published classification. No candidate or fresh data was involved.

Process lesson: when an integer graph invariant is bounded by a nonintegral expression, an equality
audit must search both exact real equality and equality after floor/ceiling rounding, including
parameterized residual classes. A negative search for the unrounded statement alone must not be
used to infer that rounded equality is unclassified.


## 2026-10-03 — TF13 first branch CI had a YAML indentation error

GitHub Actions run 37116185772 failed before creating any job because the newly appended TF13
workflow step lost the leading indentation on its first list item, making the workflow YAML invalid.

Corrective action: restore the step's existing job-level indentation and rerun the exact unchanged
TF13 deterministic checks. This was workflow syntax only: no test, diagnosis, TxGraffiti call,
candidate allocation, fresh-order construction, or scientific computation ran, and no mathematical
claim or data boundary changed.


## 2026-10-03 — TF13 exact-head CI stopped at import ordering

PR #19 exact-head Actions run `37116302326` passed installation, all 79 unit tests, and
byte-compilation. Ruff then reported only two import-order findings in the new TF13 reproducer and
its test file, so the later deterministic workflow steps were skipped.

Corrective action: apply Ruff's import grouping/order without changing executable mathematics,
data selection, assertions, documentation conclusions, or workflow scope. The failure did not run
TxGraffiti, allocate a candidate, alter either registry, inspect order 15, or change any TF13
theorem-status conclusion.


## 2026-10-03 — TF14 entry audit found the named TF13 diagnosis JSON was not committed

The TF14 brief named `experiments/TF13-DIAG-0001/diagnosis.json` among the required starting
artifacts. At the verified TF13 main commit
`8213e511715f478f7f0e94f89902e6aa076a4a15`, that path is absent. The deterministic
reproducer `experiments/tf13_segment_domination_equality.py` is committed, and exact PR-head
Actions run `37129172222` successfully executed it and uploaded the generated diagnosis as an
artifact.

Corrective action: do not fabricate or backfill a historical TF13 commit. TF14 records the
materialization discrepancy explicitly and commits its own deterministic diagnosis artifact.
Scientific consequence: none. No candidate, experiment registry row, invariant, tree of order 15,
or theorem-status conclusion is affected.


## 2026-10-03 — TF14 first PR-head CI stopped at unused test imports

PR #20 run `37132064937` passed installation, all unit tests, and byte-compilation before Ruff
reported two unused imports in the new TF14 test module. The imported support-core helpers were no
longer referenced directly after the test was simplified to check their serialized diagnostic
values.

Corrective action: remove the two unused imports only. No mathematical statement, test expectation,
diagnostic computation, prior-art conclusion, registry, candidate allocation, experiment boundary,
or tree data changes. The failed run did not reach the deterministic TF14 workflow step and had no
scientific consequence.

## 2026-10-03 — TF15 support-refined equality is not the rounded-defect classification

TF15 combined Cabrera-Martínez's 2024 refined domination bound with the strict-rounded equality
equation and obtained the necessary condition `2delta+|SL(T)|<=epsilon`. It was tempting to hope
that residue-1/2 maximizers would have equality here, reducing the final classification to the
published 2024 equality family.

Burned orders 1--14 falsify that stronger necessity. Among residue-1 strict-rounded maximizers, 50
have `(delta,|SL|)=(0,0)`, including an order-10 example, so the inequality is strict. Among
residue-2 maximizers, 33 have `(delta,|SL|)=(0,0)`, already from order 8. Thus rules such as
“residue 1 means exactly one support-link” or “residue 2 means one extra leaf or two support-links”
are false.

Scientific consequence: the support bound remains a useful necessary restriction, but TF15 uses
the published Dorfling et al. `(gamma,i)` construction and its exact defect recurrence for the
complete iff. No fresh order, candidate, experiment, or default invariant was involved.


## 2026-10-03 — TF17 burned corona/W pattern is not a global extremizer grammar

The exact TF17 census on burned orders 1--14 exposes an unusually clean parity pattern: every
even extremizer is a corona `H corona K1`, and every odd extremizer from order 3 through 13 is
the balanced Taletskii `W_(a,b)`. That finite pattern is mathematically explained, but it is not
safe to extrapolate.

Taletskii's published degree-5 construction joins copies of `W_(4,4)` while preserving the
multiplicative number of minimum dominating sets. Since `zeta(W_(4,4))=736`, the resulting
order-38 tree has `736^2=541696` minimum dominating sets, already exceeding the
`2^19=524288` value of every 38-vertex corona. The published construction has exponential base
strictly greater than sqrt(2), so the simple burned parity grammar cannot be the unrestricted
all-order solution.

Scientific consequence: TF17 records the burned pattern as a structural diagnostic, not a
conjecture, and freezes no order-15 experiment. Process lesson: even an exact family
characterization on every burned order must be compared against asymptotically stronger published
constructions before it is allowed to generate a fresh prediction.


## 2026-10-03 — TF18 coordinatewise rooted Pareto dominance is not context-safe

TF18 tested a natural but over-strong replacement intuition: replace a pendant rooted gadget by a
same-order gadget whose A/B/C state costs are all no larger and whose optimum state counts are all
no smaller. This does **not** preserve the number of global minimum dominating sets because
selectively lowering one boundary-state cost can destroy an optimum tie.

A burned order-8 pair gives an exact same-order counterexample. One rooted spider has
`A=(3,1), B=(3,1), C=infeasible`, hence closed profile `(gamma,zeta)=(3,2)`. A second
rooted spider has `A=(2,1), B=(3,2), C=infeasible`: every finite state cost is no larger and
every state count is no smaller, yet the closed profile is `(2,1)`. The cheaper A state removes
the A/B tie and halves zeta.

Corrective action: use only **projective** cost comparison for arbitrary pendant contexts. The
replacement states must differ by one common additive cost shift, equivalently have the same
A-normalized cost shape; exact counts may then be compared coordinatewise. This preserves every
boundary-state tie, so zeta cannot decrease. Same-order strict improvement in every feasible state
is a valid extremal exclusion.

Scientific consequence: ordinary Pareto pruning is rejected. The counterexample uses only burned
order 8 and does not expose order 15.


## 2026-10-03 — TF18 published local restrictions do not transfer automatically between extremal objectives

Taletskii's local replacements and Petr--Portier--Versteegen's terminal restrictions are both
structurally useful, but their proof objectives matter. Taletskii often replaces a tree by a
smaller object with better multiplicity per vertex, which supports an exponential-rate
minimal-counterexample argument rather than an exact same-order exclusion. Petr--Portier--
Versteegen derive their terminal degree restrictions inside a minimal counterexample for a
fixed-domination-number/strong-support extremal functional.

The distinction is concrete: the degree-five branching pattern used in Taletskii's published
higher-growth construction is precisely the sort of 2-terminal configuration excluded inside the
Petr--Portier--Versteegen counterexample. Therefore those terminal restrictions cannot simply be
declared forbidden in the unrestricted fixed-order problem.

Scientific consequence: TF18 records an exact DP dictionary for both proof systems but does not
manufacture a finite gadget grammar from restrictions proved for a different extremal objective.
The projective preorder gives substantial burned-order compression, but finite observed frontiers
remain diagnostics rather than evidence for a finite automaton.
