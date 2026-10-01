#!/usr/bin/env python3
"""Known-result end-to-end calibration for TreeForge infrastructure."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from treeforge.conjecturing.calibration import KnownIdentityCalibrationAdapter
from treeforge.falsification.holdout import evaluate_identity
from treeforge.pipeline import corpus_rows, dependency_versions, stable_hash
from treeforge.registry.candidate_registry import CandidateRegistry

INVARIANTS = ["order", "edge_count"]


def run(output_dir: Path, source_commit: str, timestamp: str | None = None) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    registry_dir = output_dir / "registry"
    registry_dir.mkdir(exist_ok=True)
    candidate_path = registry_dir / "candidates.jsonl"
    experiment_path = registry_dir / "experiments.jsonl"

    discovery = corpus_rows(2, 5, INVARIANTS)
    holdout = corpus_rows(6, 6, INVARIANTS)
    discovery_hash = stable_hash(discovery)
    holdout_hash = stable_hash(holdout)

    adapter = KnownIdentityCalibrationAdapter()
    statements = adapter.discover(discovery)
    if len(statements) != 1:
        raise RuntimeError("calibration engine failed to recover the known tree identity")
    evaluation = evaluate_identity(holdout)
    if not evaluation.passed:
        raise RuntimeError("known calibration identity failed holdout")

    created_at = timestamp or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    candidate_registry = CandidateRegistry(candidate_path)
    candidate_id = candidate_registry.next_id()
    candidate = {
        "candidate_id": candidate_id,
        "revision": 1,
        "statement": statements[0].statement,
        "created_at": created_at,
        "generating_engine": statements[0].engine,
        "engine_version": statements[0].engine_version,
        "dataset_hash": discovery_hash,
        "invariant_set": INVARIANTS,
        "hypotheses": ["finite", "simple", "tree"],
        "equality_or_sharp_examples": ["all discovery trees; calibration identity"],
        "discovery_evidence": {"label": "KNOWN/CALIBRATION", "orders": [2, 5], "tree_count": len(discovery)},
        "holdout_status": {"status": "PASSED", "orders": [6, 6], "tree_count": evaluation.tested, "dataset_hash": holdout_hash},
        "adversarial_status": {"status": "NOT_REQUIRED_FOR_KNOWN_CALIBRATION"},
        "counterexamples": [],
        "prior_art_status": "KNOWN_STANDARD_TREE_IDENTITY; CALIBRATION_ONLY",
        "mathematical_interpretation": "Handshake/tree-edge identity used solely to validate infrastructure.",
        "lifecycle_state": "KNOWN_RESULT",
    }
    candidate_registry.append(candidate)

    experiment = {
        "experiment_id": "CAL-0001",
        "label": "KNOWN/CALIBRATION",
        "created_at": created_at,
        "source_commit": source_commit,
        "command": "python experiments/calibration.py --output-dir data --source-commit <commit>",
        "dependencies": dependency_versions(["networkx", "txgraffiti"]),
        "random_seed": None,
        "generation_parameters": {
            "discovery_orders": [2, 5],
            "holdout_orders": [6, 6],
            "invariants": INVARIANTS,
            "holdout_visible_to_generator": False,
        },
        "discovery_data_hash": discovery_hash,
        "holdout_data_hash": holdout_hash,
        "candidate_ids": [candidate_id],
        "result": "KNOWN_RESULT",
    }
    with experiment_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(experiment, sort_keys=True, separators=(",", ":")) + "\n")

    result = {"candidate": candidate, "experiment": experiment}
    (output_dir / "calibration_result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--timestamp")
    args = parser.parse_args()
    result = run(args.output_dir, args.source_commit, args.timestamp)
    print(json.dumps(result["candidate"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
