#!/usr/bin/env python3
"""Run frozen TF2-0001 while keeping the order-12 holdout sealed."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from treeforge.conjecturing.txgraffiti_adapter import TxGraffitiAdapter
from treeforge.experiments import experiment_corpus_rows, load_frozen_spec
from treeforge.feature_audit import audit_columns, known_identity_violations
from treeforge.pipeline import dependency_versions, stable_hash
from treeforge.registry.candidate_registry import CandidateRegistry


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.write_text(
        "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in rows),
        encoding="utf-8",
    )


def run(
    spec_path: Path,
    output_dir: Path,
    source_commit: str,
    *,
    registry_path: Path = Path("data/registry/candidates.jsonl"),
    adapter=None,
) -> dict[str, object]:
    spec = load_frozen_spec(spec_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    experiment_id = str(spec["experiment_id"])
    invariants = list(spec["corpus_invariants"])
    features = list(spec["discovery_features"])
    target = str(spec["target"])

    discovery_min, discovery_max = spec["discovery_orders"]
    discovery = experiment_corpus_rows(
        discovery_min,
        discovery_max,
        invariants,
        role="discovery",
        source_commit=source_commit,
        experiment_id=experiment_id,
    )
    if len(discovery) != spec["expected_discovery_tree_count"]:
        raise RuntimeError("unexpected discovery corpus size")
    discovery_audit = audit_columns(discovery, [*features, target])
    discovery_identity_failures = known_identity_violations(discovery)
    if discovery_identity_failures:
        raise RuntimeError(
            f"discovery identity consistency failure: {discovery_identity_failures[:3]}"
        )
    discovery_hash = stable_hash(discovery)

    # Seal the fresh holdout before generation. Only count/hash/consistency status
    # are persisted here; no holdout row is serialized or passed to the engine.
    holdout_min, holdout_max = spec["holdout_orders"]
    holdout = experiment_corpus_rows(
        holdout_min,
        holdout_max,
        invariants,
        role="holdout",
        source_commit=source_commit,
        experiment_id=experiment_id,
    )
    if len(holdout) != spec["expected_holdout_tree_count"]:
        raise RuntimeError("unexpected holdout corpus size")
    holdout_identity_failures = known_identity_violations(holdout)
    if holdout_identity_failures:
        raise RuntimeError(
            f"holdout identity consistency failure: {holdout_identity_failures[:3]}"
        )
    holdout_hash = stable_hash(holdout)

    freeze = {
        "experiment_id": experiment_id,
        "source_commit": source_commit,
        "spec_path": str(spec_path),
        "discovery_orders": [discovery_min, discovery_max],
        "discovery_tree_count": len(discovery),
        "discovery_hash": discovery_hash,
        "discovery_feature_audit": discovery_audit,
        "discovery_identity_violations": discovery_identity_failures,
        "holdout_orders": [holdout_min, holdout_max],
        "holdout_tree_count": len(holdout),
        "holdout_hash": holdout_hash,
        "holdout_identity_violations": holdout_identity_failures,
        "holdout_rows_persisted": False,
        "holdout_visible_to_generator": False,
        "txgraffiti": spec["txgraffiti"],
        "target": target,
        "features": features,
        "hypotheses": spec["hypotheses"],
        "candidate_cap_policy": spec["candidate_cap_policy"],
        "candidate_normalization": spec["candidate_normalization"],
        "random_seed": spec["preprocessing"]["random_seed"],
    }
    freeze_path = output_dir / "pre_generation_freeze.json"
    freeze_path.write_text(
        json.dumps(freeze, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    # Ensure no reference to the holdout table survives into the conjecturing call.
    del holdout

    frame = pd.DataFrame(
        [{name: row[name] for name in [*features, target]} for row in discovery]
    )
    engine = adapter or TxGraffitiAdapter()
    statements = engine.discover(
        frame,
        target=target,
        features=features,
        object_symbol=spec["txgraffiti"]["object_symbol"],
        hypothesis=spec["txgraffiti"]["treeforge_hypothesis_payload"],
    )

    raw = [
        {
            "raw_index": index,
            "statement": item.statement,
            "engine": item.engine,
            "engine_version": item.engine_version,
            "metadata": item.metadata,
        }
        for index, item in enumerate(statements, start=1)
    ]
    (output_dir / "raw_txgraffiti_output.json").write_text(
        json.dumps(raw, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    _write_jsonl(output_dir / "discovery.jsonl", discovery)

    registry = CandidateRegistry(registry_path)
    next_number = int(registry.next_id().split("-")[1])
    observed = []
    for offset, item in enumerate(raw):
        observed.append(
            {
                "candidate_id": f"TF-{next_number + offset:06d}",
                "revision": 1,
                "statement": item["statement"],
                "created_at": spec["frozen_at"],
                "generating_engine": item["engine"],
                "engine_version": item["engine_version"],
                "source_commit": source_commit,
                "dataset_hash": discovery_hash,
                "invariant_set": [target, *features],
                "hypotheses": list(spec["hypotheses"]),
                "equality_or_sharp_examples": [],
                "discovery_evidence": {
                    "experiment_id": experiment_id,
                    "orders": [discovery_min, discovery_max],
                    "tree_count": len(discovery),
                    "raw_index": item["raw_index"],
                    "engine_metadata": item["metadata"],
                },
                "holdout_status": {
                    "status": "SEALED_NOT_TESTED",
                    "dataset_hash": holdout_hash,
                    "orders": [holdout_min, holdout_max],
                    "tree_count": spec["expected_holdout_tree_count"],
                },
                "adversarial_status": {"status": "NOT_TESTED"},
                "counterexamples": [],
                "prior_art_status": "NOT_STARTED",
                "mathematical_interpretation": "Pending first-stage triage.",
                "lifecycle_state": "OBSERVED",
            }
        )
    _write_jsonl(output_dir / "observed_candidates.jsonl", observed)

    manifest = {
        **freeze,
        "dependencies": dependency_versions(["networkx", "pandas", "txgraffiti"]),
        "txgraffiti_provenance": (
            engine.provenance()
            if hasattr(engine, "provenance")
            else {"engine": "test-double"}
        ),
        "raw_candidate_count": len(raw),
        "candidate_ids": [row["candidate_id"] for row in observed],
        "pre_generation_freeze_written_before_discovery": True,
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"manifest": manifest, "raw_candidates": raw}, indent=2, sort_keys=True))
    return {
        "manifest": manifest,
        "raw_candidates": raw,
        "observed_candidates": observed,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--spec", type=Path, default=Path("experiments/TF2-0001/spec.json")
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    run(args.spec, args.output_dir, args.source_commit)


if __name__ == "__main__":
    main()
