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
