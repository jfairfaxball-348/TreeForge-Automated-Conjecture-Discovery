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
