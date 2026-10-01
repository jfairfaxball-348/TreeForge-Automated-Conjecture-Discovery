#!/usr/bin/env python3
"""Run frozen TF3-0001 with a candidate-batch firewall before fresh holdout construction."""

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path

import pandas as pd

from experiments.tf2_discovery import (
    _candidate_key,
    _counterexample,
    _metadata,
    _normalized_statement,
    _revision,
    _tight_examples,
    _write_json,
    _write_jsonl,
)
from treeforge.conjecturing.txgraffiti_adapter import TxGraffitiAdapter
from treeforge.experiments import experiment_corpus_rows, load_frozen_spec
from treeforge.feature_audit import audit_columns, known_identity_violations
from treeforge.invariants.registry import default_registry
from treeforge.pipeline import dependency_versions, stable_hash
from treeforge.registry.candidate_registry import CandidateRegistry
from treeforge.trees.canonical import canonical_tree_code
from treeforge.trees.families import broom, caterpillar, double_star, path, spider, star


def _rhs_symbols(rhs: str) -> set[str]:
    tree = ast.parse(rhs, mode="eval")
    return {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}


def _base_record(
    *,
    candidate_id: str,
    statement: str,
    created_at: str,
    source_commit: str,
    discovery_hash: str,
    target: str,
    features: list[str],
    raw_index: int,
    raw_statement: str,
    engine: str,
    engine_version: str,
    metadata: dict[str, object],
    tight_examples: list[dict[str, object]],
    discovery_orders: list[int],
    discovery_count: int,
    hypotheses: list[str],
) -> dict[str, object]:
    return {
        "candidate_id": candidate_id,
        "revision": 1,
        "statement": statement,
        "created_at": created_at,
        "generating_engine": engine,
        "engine_version": engine_version,
        "source_commit": source_commit,
        "dataset_hash": discovery_hash,
        "invariant_set": [target, *features],
        "hypotheses": hypotheses,
        "equality_or_sharp_examples": tight_examples,
        "discovery_evidence": {
            "experiment_id": "TF3-0001",
            "orders": discovery_orders,
            "tree_count": discovery_count,
            "raw_index": raw_index,
            "raw_statement": raw_statement,
            "structured_relation": metadata,
        },
        "holdout_status": {"status": "NOT_TESTED"},
        "adversarial_status": {"status": "NOT_TESTED"},
        "counterexamples": [],
        "prior_art_status": "NOT_STARTED",
        "mathematical_interpretation": "Pending exact discovery-side triage.",
        "lifecycle_state": "OBSERVED",
    }


def _adversarial_graphs() -> list[tuple[str, dict[str, object], object]]:
    rows: list[tuple[str, dict[str, object], object]] = []
    for n in [16, 17]:
        rows.append(("path", {"order": n}, path(n)))
        rows.append(("star", {"leaves": n - 1}, star(n - 1)))

    for arms in [[3, 3, 9], [3, 4, 9], [5, 5, 5], [1, 3, 12], [2, 4, 10]]:
        rows.append(("spider", {"arms": arms}, spider(arms)))

    caterpillar_specs = [
        (6, [3, 0, 0, 3, 0, 4]),
        (7, [2, 0, 2, 0, 2, 0, 3]),
        (8, [0, 2, 0, 2, 0, 2, 0, 2]),
    ]
    for spine_order, leaves in caterpillar_specs:
        rows.append(
            (
                "caterpillar",
                {"spine_order": spine_order, "leaves": leaves},
                caterpillar(spine_order, leaves),
            )
        )

    for left, right in [(7, 7), (7, 8), (8, 8)]:
        rows.append(
            (
                "double_star",
                {"left_leaves": left, "right_leaves": right},
                double_star(left, right),
            )
        )
    for handle, brush in [(8, 8), (9, 8), (8, 9)]:
        rows.append(
            (
                "broom",
                {"handle_edges": handle, "brush_leaves": brush},
                broom(handle, brush),
            )
        )
    return rows


def _adversarial_rows(
    invariant_names: list[str], source_commit: str, experiment_id: str
) -> list[dict[str, object]]:
    registry = default_registry()
    rows = []
    for family, parameters, graph in _adversarial_graphs():
        values = registry.compute(graph, invariant_names)
        rows.append(
            {
                "tree_code": canonical_tree_code(graph),
                "order": graph.number_of_nodes(),
                "corpus_role": "adversarial",
                "source_commit": source_commit,
                "experiment_id": experiment_id,
                "generation_parameters": {"family": family, **parameters},
                **{key: value for key, value in values.items() if key != "order"},
            }
        )
    return rows


def _freeze_candidate_batch(
    output_dir: Path,
    current: dict[str, dict[str, object]],
    *,
    source_commit: str,
) -> tuple[list[dict[str, object]], str]:
    batch = [
        current[candidate_id]
        for candidate_id in sorted(current)
        if current[candidate_id]["lifecycle_state"] == "CONJECTURED"
    ]
    _write_json(output_dir / "candidate_batch.json", batch)
    batch_hash = stable_hash(batch)
    _write_json(
        output_dir / "candidate_batch_freeze.json",
        {
            "experiment_id": "TF3-0001",
            "source_commit": source_commit,
            "candidate_count": len(batch),
            "candidate_ids": [row["candidate_id"] for row in batch],
            "candidate_batch_hash": batch_hash,
            "holdout_constructed": False,
        },
    )
    return batch, batch_hash


def run(
    spec_path: Path,
    output_dir: Path,
    source_commit: str,
    *,
    registry_path: Path = Path("data/registry/candidates.jsonl"),
    adapter=None,
) -> dict[str, object]:
    spec = load_frozen_spec(spec_path)
    if spec["experiment_id"] != "TF3-0001":
        raise ValueError("this runner is frozen for TF3-0001")
    output_dir.mkdir(parents=True, exist_ok=True)

    registry = CandidateRegistry(registry_path)
    expected_next = str(spec["candidate_policy"]["next_permanent_candidate_id"])
    if registry.next_id() != expected_next:
        raise RuntimeError(
            f"candidate registry advanced: expected {expected_next}, got {registry.next_id()}"
        )

    experiment_id = str(spec["experiment_id"])
    invariants = list(spec["corpus_invariants"])
    features = list(spec["discovery_features"])
    target = str(spec["target"])
    dmin, dmax = spec["discovery_orders"]

    discovery = experiment_corpus_rows(
        dmin,
        dmax,
        invariants,
        role="discovery",
        source_commit=source_commit,
        experiment_id=experiment_id,
    )
    if len(discovery) != spec["expected_discovery_tree_count"]:
        raise RuntimeError("unexpected discovery corpus size")
    discovery_hash = stable_hash(discovery)
    audit = audit_columns(discovery, features + [target])
    identity_failures = known_identity_violations(discovery)
    if identity_failures:
        raise RuntimeError("discovery identity consistency failure")

    frame = pd.DataFrame(
        [{name: row[name] for name in [*features, target]} for row in discovery]
    )
    engine = adapter or TxGraffitiAdapter()
    statements = engine.discover(
        frame,
        target=target,
        features=features,
        object_symbol=spec["txgraffiti"]["object_symbol"],
        hypothesis=spec["txgraffiti"]["hypothesis_payload"],
        methods=list(spec["txgraffiti"]["methods"]),
    )
    stage_counts = getattr(engine, "last_stage_counts", None)
    _write_json(output_dir / "stage_counts.json", stage_counts or {})

    raw = []
    for index, item in enumerate(statements, start=1):
        metadata = _metadata(item)
        symbols = _rhs_symbols(str(metadata["rhs"]))
        if len(symbols) != 1 or not symbols <= set(features):
            raise RuntimeError(
                "ratios-only output violated frozen one-feature RHS grammar: "
                f"{metadata['rhs']}"
            )
        raw.append(
            {
                "raw_index": index,
                "statement": item.statement,
                "engine": item.engine,
                "engine_version": item.engine_version,
                "metadata": metadata,
            }
        )
    _write_json(output_dir / "raw_txgraffiti_output.json", raw)
    _write_jsonl(output_dir / "discovery.jsonl", discovery)

    next_number = int(expected_next.split("-")[1])
    events: list[dict[str, object]] = []
    current: dict[str, dict[str, object]] = {}
    seen: dict[tuple[str, str, str], str] = {}

    for offset, item in enumerate(raw):
        candidate_id = f"TF-{next_number + offset:06d}"
        metadata = dict(item["metadata"])
        record = _base_record(
            candidate_id=candidate_id,
            statement=_normalized_statement(metadata),
            created_at=str(spec["frozen_at"]),
            source_commit=source_commit,
            discovery_hash=discovery_hash,
            target=target,
            features=features,
            raw_index=int(item["raw_index"]),
            raw_statement=str(item["statement"]),
            engine=str(item["engine"]),
            engine_version=str(item["engine_version"]),
            metadata=metadata,
            tight_examples=_tight_examples(discovery, metadata),
            discovery_orders=[dmin, dmax],
            discovery_count=len(discovery),
            hypotheses=list(spec["hypotheses"]),
        )
        events.append(record)
        key = _candidate_key(metadata)

        if str(metadata["lhs"]) != target or target in str(metadata["rhs"]):
            record = _revision(
                record,
                lifecycle_state="ARTIFACT_OF_FEATURE_SET",
                mathematical_interpretation=(
                    "Rejected before holdout: target placement is not an admissible "
                    "target-vs-feature bound."
                ),
            )
        elif key in seen:
            record = _revision(
                record,
                lifecycle_state="DUPLICATE",
                mathematical_interpretation=f"Exact normalized duplicate of {seen[key]}.",
            )
        elif str(metadata["lhs"]) == str(metadata["rhs"]):
            record = _revision(
                record,
                lifecycle_state="TRIVIAL",
                mathematical_interpretation="Tautological normalized relation.",
            )
        else:
            discovery_failure = _counterexample(discovery, metadata)
            if discovery_failure is not None:
                record = _revision(
                    record,
                    lifecycle_state="FALSIFIED",
                    counterexamples=[discovery_failure],
                    mathematical_interpretation=(
                        "Generated relation failed exact discovery-side reevaluation."
                    ),
                )
            else:
                seen[key] = candidate_id
                record = _revision(
                    record,
                    lifecycle_state="CONJECTURED",
                    mathematical_interpretation=(
                        "Unique exact discovery-valid ratios-only target bound; admitted "
                        "to the frozen candidate batch."
                    ),
                )
        events.append(record)
        current[candidate_id] = record

    candidate_batch, candidate_batch_hash = _freeze_candidate_batch(
        output_dir, current, source_commit=source_commit
    )
    candidate_batch_ids = [str(row["candidate_id"]) for row in candidate_batch]

    # Fresh holdout construction is structurally below candidate-batch persistence.
    holdout: list[dict[str, object]] = []
    holdout_hash: str | None = None
    holdout_identity_failures: list[dict[str, object]] = []
    if candidate_batch_ids:
        hmin, hmax = spec["holdout_orders"]
        holdout = experiment_corpus_rows(
            hmin,
            hmax,
            invariants,
            role="holdout",
            source_commit=source_commit,
            experiment_id=experiment_id,
        )
        if len(holdout) != spec["expected_holdout_tree_count"]:
            raise RuntimeError("unexpected holdout corpus size")
        holdout_hash = stable_hash(holdout)
        holdout_identity_failures = known_identity_violations(holdout)
        if holdout_identity_failures:
            raise RuntimeError("holdout identity consistency failure")
        _write_jsonl(output_dir / "holdout.jsonl", holdout)

        for candidate_id in candidate_batch_ids:
            record = current[candidate_id]
            metadata = dict(record["discovery_evidence"]["structured_relation"])
            failure = _counterexample(holdout, metadata)
            if failure:
                updated = _revision(
                    record,
                    lifecycle_state="FALSIFIED",
                    holdout_status={
                        "status": "FAILED",
                        "dataset_hash": holdout_hash,
                        "orders": [hmin, hmax],
                        "tree_count": len(holdout),
                    },
                    counterexamples=[failure],
                    mathematical_interpretation="Falsified on the fresh TF3 order-13 holdout.",
                )
            else:
                updated = _revision(
                    record,
                    lifecycle_state="HOLDOUT_PASSED",
                    holdout_status={
                        "status": "PASSED",
                        "dataset_hash": holdout_hash,
                        "orders": [hmin, hmax],
                        "tree_count": len(holdout),
                    },
                    mathematical_interpretation=(
                        "Survived the fresh exhaustive order-13 holdout; finite evidence only."
                    ),
                )
            events.append(updated)
            current[candidate_id] = updated

    holdout_survivors = [
        candidate_id
        for candidate_id, record in current.items()
        if record["lifecycle_state"] == "HOLDOUT_PASSED"
    ]
    adversarial = (
        _adversarial_rows(invariants, source_commit, experiment_id)
        if holdout_survivors
        else []
    )
    _write_jsonl(output_dir / "adversarial.jsonl", adversarial)
    adversarial_hash = stable_hash(adversarial) if adversarial else None

    for candidate_id in holdout_survivors:
        record = current[candidate_id]
        metadata = dict(record["discovery_evidence"]["structured_relation"])
        failure = _counterexample(adversarial, metadata)
        families = sorted(
            {row["generation_parameters"]["family"] for row in adversarial}
        )
        if failure:
            updated = _revision(
                record,
                lifecycle_state="FALSIFIED",
                adversarial_status={
                    "status": "FAILED",
                    "dataset_hash": adversarial_hash,
                    "tree_count": len(adversarial),
                    "families": families,
                },
                counterexamples=[*record["counterexamples"], failure],
                mathematical_interpretation="Falsified by a pre-frozen fresh TF3 hostile tree.",
            )
        else:
            updated = _revision(
                record,
                lifecycle_state="ADVERSARIAL_PASSED",
                adversarial_status={
                    "status": "PASSED",
                    "dataset_hash": adversarial_hash,
                    "tree_count": len(adversarial),
                    "families": families,
                },
                mathematical_interpretation=(
                    "Survived the pre-frozen fresh TF3 hostile families. No automatic "
                    "MATHEMATICALLY_INTERESTING promotion is made."
                ),
            )
        events.append(updated)
        current[candidate_id] = updated

    _write_jsonl(output_dir / "candidate_events.jsonl", events)
    _write_json(output_dir / "final_candidates.json", list(current.values()))

    states = [
        "CONJECTURED",
        "KNOWN_RESULT",
        "TRIVIAL",
        "DUPLICATE",
        "ARTIFACT_OF_FEATURE_SET",
        "FALSIFIED",
        "HOLDOUT_PASSED",
        "ADVERSARIAL_PASSED",
        "MATHEMATICALLY_INTERESTING",
    ]
    first_stage_counts = {
        state: sum(
            row["lifecycle_state"] == state
            for row in candidate_batch
        )
        for state in states
    }
    final_counts = {
        state: sum(record["lifecycle_state"] == state for record in current.values())
        for state in states
    }
    manifest = {
        "experiment_id": experiment_id,
        "source_commit": source_commit,
        "spec_path": str(spec_path),
        "dependencies": dependency_versions(["networkx", "pandas", "txgraffiti"]),
        "txgraffiti_provenance": (
            engine.provenance() if hasattr(engine, "provenance") else {"engine": "test-double"}
        ),
        "methods": list(spec["txgraffiti"]["methods"]),
        "discovery_hash": discovery_hash,
        "discovery_tree_count": len(discovery),
        "raw_candidate_count": len(raw),
        "stage_counts": stage_counts,
        "candidate_ids": sorted(current),
        "candidate_batch_ids": candidate_batch_ids,
        "candidate_batch_hash": candidate_batch_hash,
        "candidate_batch_frozen_before_holdout": True,
        "first_stage_state_counts": first_stage_counts,
        "holdout_constructed": bool(holdout),
        "holdout_hash": holdout_hash,
        "holdout_tree_count": len(holdout),
        "holdout_visible_to_generator": False,
        "holdout_survivor_count": len(holdout_survivors),
        "adversarial_hash": adversarial_hash,
        "adversarial_tree_count": len(adversarial),
        "final_state_counts": final_counts,
        "feature_audit": audit,
        "known_identity_violations": identity_failures,
        "holdout_identity_violations": holdout_identity_failures,
    }
    _write_json(output_dir / "manifest.json", manifest)
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return {
        "manifest": manifest,
        "raw_candidates": raw,
        "candidate_events": events,
        "final_candidates": list(current.values()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", type=Path, default=Path("experiments/TF3-0001/spec.json"))
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    run(args.spec, args.output_dir, args.source_commit)


if __name__ == "__main__":
    main()
