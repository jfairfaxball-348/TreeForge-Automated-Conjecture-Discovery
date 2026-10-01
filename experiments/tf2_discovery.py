#!/usr/bin/env python3
"""Run frozen TF2-0001 with discovery/holdout/adversarial separation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from treeforge.conjecturing.expression import evaluate_relation, is_tight
from treeforge.conjecturing.txgraffiti_adapter import TxGraffitiAdapter
from treeforge.experiments import experiment_corpus_rows, load_frozen_spec
from treeforge.feature_audit import audit_columns, known_identity_violations
from treeforge.invariants.registry import default_registry
from treeforge.pipeline import dependency_versions, stable_hash
from treeforge.registry.candidate_registry import CandidateRegistry
from treeforge.trees.canonical import canonical_tree_code
from treeforge.trees.families import (
    balanced_binary_tree,
    broom,
    caterpillar,
    double_star,
    path,
    spider,
    star,
)


def _write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.write_text(
        "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in rows),
        encoding="utf-8",
    )


def _metadata(item) -> dict[str, object]:
    if not item.metadata:
        raise RuntimeError("TxGraffiti candidate lacks structured metadata")
    required = {"lhs", "operator", "rhs"}
    if not required <= item.metadata.keys():
        raise RuntimeError("TxGraffiti candidate metadata is incomplete")
    return dict(item.metadata)


def _normalized_statement(metadata: dict[str, object]) -> str:
    return (
        "For every finite simple tree T, "
        f"{metadata['lhs']} {metadata['operator']} {metadata['rhs']}."
    )


def _candidate_key(metadata: dict[str, object]) -> tuple[str, str, str]:
    return (
        str(metadata["lhs"]),
        str(metadata["operator"]),
        str(metadata["rhs"]),
    )


def _counterexample(
    rows: list[dict[str, object]], metadata: dict[str, object]
) -> dict[str, object] | None:
    lhs, op, rhs = _candidate_key(metadata)
    for row in sorted(rows, key=lambda r: (int(r["order"]), str(r["tree_code"]))):
        if not evaluate_relation(lhs, op, rhs, row):
            return {
                "tree_code": row["tree_code"],
                "order": row["order"],
                "lhs": lhs,
                "operator": op,
                "rhs": rhs,
                "values": {
                    key: row[key]
                    for key in row
                    if key
                    not in {
                        "corpus_role",
                        "experiment_id",
                        "generation_parameters",
                        "source_commit",
                    }
                },
            }
    return None


def _tight_examples(
    rows: list[dict[str, object]], metadata: dict[str, object], limit: int = 5
) -> list[dict[str, object]]:
    lhs, _, rhs = _candidate_key(metadata)
    examples = []
    for row in rows:
        if is_tight(lhs, rhs, row):
            examples.append({"tree_code": row["tree_code"], "order": row["order"]})
            if len(examples) >= limit:
                break
    return examples


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
            "experiment_id": "TF2-0001",
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
        "mathematical_interpretation": "Pending first-stage triage.",
        "lifecycle_state": "OBSERVED",
    }


def _revision(record: dict[str, object], **changes: object) -> dict[str, object]:
    updated = json.loads(json.dumps(record))
    updated["revision"] = int(record["revision"]) + 1
    updated.update(changes)
    return updated


def _adversarial_graphs() -> list[tuple[str, dict[str, object], object]]:
    rows: list[tuple[str, dict[str, object], object]] = []
    for n in range(13, 16):
        rows.append(("path", {"order": n}, path(n)))
        rows.append(("star", {"leaves": n - 1}, star(n - 1)))

    for k in range(10, 13):
        rows.append(("spider", {"arms": [1, 1, k]}, spider([1, 1, k])))
    for k in range(9, 12):
        rows.append(("spider", {"arms": [1, 2, k]}, spider([1, 2, k])))
    for k in range(8, 11):
        rows.append(("spider", {"arms": [2, 2, k]}, spider([2, 2, k])))
    rows.append(("spider", {"arms": [4, 4, 4]}, spider([4, 4, 4])))

    rows.extend(
        [
            (
                "caterpillar",
                {"spine_order": 5, "leaves": [4, 0, 0, 0, 4]},
                caterpillar(5, [4, 0, 0, 0, 4]),
            ),
            (
                "caterpillar",
                {"spine_order": 6, "leaves": [2, 0, 2, 0, 2, 1]},
                caterpillar(6, [2, 0, 2, 0, 2, 1]),
            ),
            (
                "caterpillar",
                {"spine_order": 7, "leaves": [0, 3, 0, 3, 0, 2, 0]},
                caterpillar(7, [0, 3, 0, 3, 0, 2, 0]),
            ),
            ("balanced_binary_tree", {"height": 3}, balanced_binary_tree(3)),
        ]
    )

    for left, right in [(5, 6), (5, 7), (6, 7)]:
        rows.append(
            (
                "double_star",
                {"left_leaves": left, "right_leaves": right},
                double_star(left, right),
            )
        )
    for handle, brush in [(5, 7), (6, 7), (7, 7)]:
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


def run(
    spec_path: Path,
    output_dir: Path,
    source_commit: str,
    *,
    registry_path: Path = Path("data/registry/candidates.jsonl"),
    adapter=None,
) -> dict[str, object]:
    spec = load_frozen_spec(spec_path)
    if spec["experiment_id"] != "TF2-0001":
        raise ValueError("this runner is frozen for TF2-0001")
    output_dir.mkdir(parents=True, exist_ok=True)

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

    frame = pd.DataFrame([{name: row[name] for name in [*features, target]} for row in discovery])
    engine = adapter or TxGraffitiAdapter()
    statements = engine.discover(
        frame,
        target=target,
        features=features,
        object_symbol=spec["txgraffiti"]["object_symbol"],
        hypothesis=spec["txgraffiti"]["hypothesis_payload"],
    )
    stage_counts = getattr(engine, "last_stage_counts", None)
    _write_json(output_dir / "stage_counts.json", stage_counts or {})

    raw = []
    for index, item in enumerate(statements, start=1):
        raw.append(
            {
                "raw_index": index,
                "statement": item.statement,
                "engine": item.engine,
                "engine_version": item.engine_version,
                "metadata": _metadata(item),
            }
        )
    _write_json(output_dir / "raw_txgraffiti_output.json", raw)
    _write_jsonl(output_dir / "discovery.jsonl", discovery)

    registry = CandidateRegistry(registry_path)
    next_number = int(registry.next_id().split("-")[1])
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
                mathematical_interpretation="Rejected before holdout: target placement is not an admissible target-vs-feature bound.",
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
                    mathematical_interpretation="Generated relation failed exact discovery-side reevaluation.",
                )
            else:
                seen[key] = candidate_id
                record = _revision(
                    record,
                    lifecycle_state="CONJECTURED",
                    mathematical_interpretation="Unique exact discovery-valid target bound; admitted to pre-frozen holdout testing.",
                )
        events.append(record)
        current[candidate_id] = record

    first_stage_state_counts = {
        state: sum(1 for record in current.values() if record["lifecycle_state"] == state)
        for state in [
            "CONJECTURED",
            "KNOWN_RESULT",
            "TRIVIAL",
            "DUPLICATE",
            "ARTIFACT_OF_FEATURE_SET",
            "FALSIFIED",
        ]
    }

    # The order-12 holdout is constructed only after raw generation and first-stage triage.
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

    for candidate_id, record in list(current.items()):
        if record["lifecycle_state"] != "CONJECTURED":
            continue
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
                mathematical_interpretation="Falsified on the untouched TF2 holdout.",
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
                mathematical_interpretation="Survived the untouched finite order-12 holdout; this is finite evidence only.",
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
    adversarial_hash = stable_hash(adversarial)
    for candidate_id, record in list(current.items()):
        if record["lifecycle_state"] != "HOLDOUT_PASSED":
            continue
        metadata = dict(record["discovery_evidence"]["structured_relation"])
        failure = _counterexample(adversarial, metadata)
        if failure:
            updated = _revision(
                record,
                lifecycle_state="FALSIFIED",
                adversarial_status={
                    "status": "FAILED",
                    "dataset_hash": adversarial_hash,
                    "tree_count": len(adversarial),
                    "families": sorted(
                        {row["generation_parameters"]["family"] for row in adversarial}
                    ),
                },
                counterexamples=[*record["counterexamples"], failure],
                mathematical_interpretation="Falsified by a pre-frozen hostile tree family.",
            )
        else:
            updated = _revision(
                record,
                lifecycle_state="ADVERSARIAL_PASSED",
                adversarial_status={
                    "status": "PASSED",
                    "dataset_hash": adversarial_hash,
                    "tree_count": len(adversarial),
                    "families": sorted(
                        {row["generation_parameters"]["family"] for row in adversarial}
                    ),
                },
                mathematical_interpretation=(
                    "Survived the pre-frozen finite hostile families. No automatic "
                    "MATHEMATICALLY_INTERESTING promotion is made."
                ),
            )
        events.append(updated)
        current[candidate_id] = updated

    adversarial_survivors = [
        candidate_id
        for candidate_id, record in current.items()
        if record["lifecycle_state"] == "ADVERSARIAL_PASSED"
    ]
    _write_jsonl(output_dir / "candidate_events.jsonl", events)
    _write_json(output_dir / "final_candidates.json", list(current.values()))

    counts = {
        state: sum(1 for record in current.values() if record["lifecycle_state"] == state)
        for state in [
            "KNOWN_RESULT",
            "TRIVIAL",
            "DUPLICATE",
            "ARTIFACT_OF_FEATURE_SET",
            "FALSIFIED",
            "HOLDOUT_PASSED",
            "ADVERSARIAL_PASSED",
            "MATHEMATICALLY_INTERESTING",
        ]
    }
    manifest = {
        "experiment_id": experiment_id,
        "source_commit": source_commit,
        "spec_path": str(spec_path),
        "dependencies": dependency_versions(["networkx", "pandas", "txgraffiti"]),
        "txgraffiti_provenance": engine.provenance() if hasattr(engine, "provenance") else {"engine": "test-double"},
        "discovery_hash": discovery_hash,
        "holdout_hash": holdout_hash,
        "adversarial_hash": adversarial_hash,
        "discovery_tree_count": len(discovery),
        "holdout_tree_count": len(holdout),
        "adversarial_tree_count": len(adversarial),
        "raw_candidate_count": len(raw),
        "stage_counts": stage_counts,
        "candidate_ids": sorted(current),
        "first_stage_state_counts": first_stage_state_counts,
        "holdout_survivor_count": len(holdout_survivors),
        "holdout_survivor_ids": holdout_survivors,
        "adversarial_survivor_count": len(adversarial_survivors),
        "adversarial_survivor_ids": adversarial_survivors,
        "final_state_counts": counts,
        "holdout_visible_to_generator": False,
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
    parser.add_argument("--spec", type=Path, default=Path("experiments/TF2-0001/spec.json"))
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    run(args.spec, args.output_dir, args.source_commit)


if __name__ == "__main__":
    main()
