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

