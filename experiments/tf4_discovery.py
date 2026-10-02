#!/usr/bin/env python3
"""Run frozen TF4-0001 pairwise convex-hull discovery with strict fresh-data firewalls."""

from __future__ import annotations

import argparse
import ast
import json
from collections import Counter
from itertools import combinations
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

EXPERIMENT_ID = "TF4-0001"


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
    cross_run_index: int,
    raw_statements: list[str],
    source_feature_pairs: list[list[str]],
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
            "experiment_id": EXPERIMENT_ID,
            "orders": discovery_orders,
            "tree_count": discovery_count,
            "cross_run_index": cross_run_index,
            "source_feature_pairs": source_feature_pairs,
            "raw_statements": raw_statements,
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
    for n in [18, 19]:
        rows.append(("path", {"order": n}, path(n)))
        rows.append(("star", {"leaves": n - 1}, star(n - 1)))

    for arms in [
        [2, 2, 13],
        [3, 5, 10],
        [2, 6, 10],
        [4, 4, 5, 5],
        [2, 2, 2, 2, 2, 2, 2, 2],
        [1, 5, 12],
    ]:
        rows.append(("spider", {"arms": arms}, spider(arms)))

    for spine_order, leaves in [
        (6, [0, 4, 0, 0, 4, 3]),
        (7, [3, 0, 0, 3, 0, 0, 4]),
        (8, [2, 0, 1, 0, 2, 0, 1, 3]),
    ]:
        rows.append(
            (
                "caterpillar",
                {"spine_order": spine_order, "leaves": leaves},
                caterpillar(spine_order, leaves),
            )
        )

    for left, right in [(8, 9), (7, 9), (6, 8)]:
        rows.append(
            (
                "double_star",
                {"left_leaves": left, "right_leaves": right},
                double_star(left, right),
            )
        )

    for handle, brush in [(10, 7), (7, 10), (9, 9)]:
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


def _pairwise_discover(
    frame: pd.DataFrame,
    *,
    target: str,
    features: list[str],
    object_symbol: str,
    hypothesis: list[object],
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, int]]:
    per_run_final: list[dict[str, object]] = []
    unique: dict[tuple[str, str, str], dict[str, object]] = {}
    stage_totals: Counter[str] = Counter()

    for feature_pair in combinations(features, 2):
        adapter = TxGraffitiAdapter()
        statements = adapter.discover(
            frame,
            target=target,
            features=list(feature_pair),
            object_symbol=object_symbol,
            hypothesis=hypothesis,
            methods=["convex_hull"],
        )
        for key, value in (adapter.last_stage_counts or {}).items():
            stage_totals[key] += int(value)

        for pair_raw_index, item in enumerate(statements, start=1):
            metadata = _metadata(item)
            symbols = _rhs_symbols(str(metadata["rhs"]))
            if not symbols <= set(features) or len(symbols) > 2:
                raise RuntimeError(
                    "pairwise output violated frozen RHS grammar: "
                    f"{metadata['rhs']}"
                )
            row = {
                "feature_pair": list(feature_pair),
                "pair_raw_index": pair_raw_index,
                "statement": item.statement,
                "engine": item.engine,
                "engine_version": item.engine_version,
                "metadata": metadata,
            }
            per_run_final.append(row)

            key = _candidate_key(metadata)
            if key not in unique:
                unique[key] = {
                    "statement": item.statement,
                    "engine": item.engine,
                    "engine_version": item.engine_version,
                    "metadata": metadata,
                    "source_feature_pairs": [list(feature_pair)],
                    "raw_statements": [item.statement],
                }
            else:
                existing = unique[key]
                if existing["metadata"].get("discovery_touch_count") != metadata.get(
                    "discovery_touch_count"
                ):
                    raise RuntimeError(
                        "exact cross-run duplicate has inconsistent touch count"
                    )
                existing["source_feature_pairs"].append(list(feature_pair))
                existing["raw_statements"].append(item.statement)

    deduplicated = []
    for cross_run_index, item in enumerate(unique.values(), start=1):
        deduplicated.append({"cross_run_index": cross_run_index, **item})
    return per_run_final, deduplicated, dict(stage_totals)


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
            "experiment_id": EXPERIMENT_ID,
            "source_commit": source_commit,
            "candidate_count": len(batch),
            "candidate_ids": [row["candidate_id"] for row in batch],
            "candidate_batch_hash": batch_hash,
            "literal_domain_guard_completed": True,
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
) -> dict[str, object]:
    spec = load_frozen_spec(spec_path)
    if spec["experiment_id"] != EXPERIMENT_ID:
        raise ValueError(f"this runner is frozen for {EXPERIMENT_ID}")
    output_dir.mkdir(parents=True, exist_ok=True)

    registry = CandidateRegistry(registry_path)
    expected_next = str(spec["candidate_policy"]["next_permanent_candidate_id"])
    if registry.next_id() != expected_next:
        raise RuntimeError(
            f"candidate registry advanced: expected {expected_next}, got {registry.next_id()}"
        )

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
        experiment_id=EXPERIMENT_ID,
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
    per_run_final, deduplicated, stage_totals = _pairwise_discover(
        frame,
        target=target,
        features=features,
        object_symbol=str(spec["txgraffiti"]["object_symbol"]),
        hypothesis=list(spec["txgraffiti"]["hypothesis_payload"]),
    )
    expected_diag = spec["diagnostic_basis"]["pairwise_convex_hulls"]
    expected_stage = {
        "raw_generator_output": int(expected_diag["raw_generator_output"]),
        "after_morgan": int(expected_diag["raw_generator_output"]),
        "after_dalmatian": int(expected_diag["after_dalmatian"]),
        "after_duplicate_removal": int(expected_diag["per_run_post_duplicate_total"]),
        "after_touch_count_sort": int(expected_diag["per_run_post_duplicate_total"]),
        "strengthened_equalities": 0,
        "final_discover_output": int(expected_diag["per_run_post_duplicate_total"]),
    }
    if stage_totals != expected_stage:
        raise RuntimeError(
            f"pairwise stage counts differ from frozen diagnostic: {stage_totals}"
        )
    if len(deduplicated) != int(
        spec["interpretability_policy"][
            "expected_cross_run_exact_dedup_count_from_exposed_diagnostic"
        ]
    ):
        raise RuntimeError("cross-run exact-dedup count differs from frozen diagnostic")

    _write_json(output_dir / "pairwise_stage_counts.json", stage_totals)
    _write_json(output_dir / "raw_pairwise_final_output.json", per_run_final)
    _write_json(output_dir / "cross_run_deduplicated_output.json", deduplicated)
    _write_jsonl(output_dir / "discovery.jsonl", discovery)

    next_number = int(expected_next.split("-")[1])
    events: list[dict[str, object]] = []
    current: dict[str, dict[str, object]] = {}

    for offset, item in enumerate(deduplicated):
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
            cross_run_index=int(item["cross_run_index"]),
            raw_statements=list(item["raw_statements"]),
            source_feature_pairs=[list(pair) for pair in item["source_feature_pairs"]],
            engine=str(item["engine"]),
            engine_version=str(item["engine_version"]),
            metadata=metadata,
            tight_examples=_tight_examples(discovery, metadata),
            discovery_orders=[dmin, dmax],
            discovery_count=len(discovery),
            hypotheses=list(spec["hypotheses"]),
        )
        events.append(record)

        if str(metadata["lhs"]) != target or target in str(metadata["rhs"]):
            record = _revision(
                record,
                lifecycle_state="ARTIFACT_OF_FEATURE_SET",
                mathematical_interpretation=(
                    "Rejected before fresh validation: target placement is not an "
                    "admissible target-vs-feature bound."
                ),
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
                record = _revision(
                    record,
                    lifecycle_state="CONJECTURED",
                    mathematical_interpretation=(
                        "Unique cross-run exact-deduplicated pairwise convex-hull bound; "
                        "pending literal-domain consistency."
                    ),
                )
        events.append(record)
        current[candidate_id] = record

    # K1 is already exposed. This enforces the literal all-tree statement before
    # any fresh holdout is constructed; it is not fresh validation evidence.
    k1_rows = experiment_corpus_rows(
        1,
        1,
        invariants,
        role="discovery",
        source_commit=source_commit,
        experiment_id=EXPERIMENT_ID,
    )
    if len(k1_rows) != 1:
        raise RuntimeError("expected exactly one K1 row for literal-domain consistency")
    k1_hash = stable_hash(k1_rows)
    k1_falsified: list[str] = []
    for candidate_id, record in list(current.items()):
        if record["lifecycle_state"] != "CONJECTURED":
            continue
        metadata = dict(record["discovery_evidence"]["structured_relation"])
        failure = _counterexample(k1_rows, metadata)
        if failure is None:
            continue
        updated = _revision(
            record,
            lifecycle_state="FALSIFIED",
            counterexamples=[*record["counterexamples"], failure],
            mathematical_interpretation=(
                "Falsified by exposed K1 under the literal frozen all-finite-tree "
                "hypothesis before fresh validation."
            ),
        )
        events.append(updated)
        current[candidate_id] = updated
        k1_falsified.append(candidate_id)

    _write_json(
        output_dir / "literal_domain_guard.json",
        {
            "tree": "K1",
            "tree_count": 1,
            "dataset_hash": k1_hash,
            "fresh_validation_evidence": False,
            "falsified_count": len(k1_falsified),
            "falsified_ids": sorted(k1_falsified),
            "holdout_constructed": False,
        },
    )

    candidate_batch, candidate_batch_hash = _freeze_candidate_batch(
        output_dir, current, source_commit=source_commit
    )
    candidate_batch_ids = [str(row["candidate_id"]) for row in candidate_batch]

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
            experiment_id=EXPERIMENT_ID,
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
                    counterexamples=[*record["counterexamples"], failure],
                    mathematical_interpretation="Falsified on the fresh TF4 order-14 holdout.",
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
                        "Survived the fresh exhaustive TF4 order-14 holdout; "
                        "this is finite evidence only."
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
        _adversarial_rows(invariants, source_commit, EXPERIMENT_ID)
        if holdout_survivors
        else []
    )
    _write_jsonl(output_dir / "adversarial.jsonl", adversarial)
    adversarial_hash = stable_hash(adversarial)

    for candidate_id in holdout_survivors:
        record = current[candidate_id]
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
                mathematical_interpretation=(
                    "Falsified by a pre-frozen fresh TF4 hostile tree."
                ),
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
                    "Survived the pre-frozen finite TF4 hostile families. "
                    "No automatic MATHEMATICALLY_INTERESTING promotion is made."
                ),
            )
        events.append(updated)
        current[candidate_id] = updated

    _write_jsonl(output_dir / "candidate_events.jsonl", events)
    _write_json(output_dir / "final_candidates.json", list(current.values()))

    final_counts = dict(
        sorted(Counter(str(row["lifecycle_state"]) for row in current.values()).items())
    )
    manifest = {
        "experiment_id": EXPERIMENT_ID,
        "source_commit": source_commit,
        "spec_path": str(spec_path),
        "dependencies": dependency_versions(["networkx", "pandas", "txgraffiti"]),
        "txgraffiti_provenance": TxGraffitiAdapter().provenance(),
        "methods": ["convex_hull"],
        "feature_pair_run_count": len(list(combinations(features, 2))),
        "discovery_hash": discovery_hash,
        "literal_domain_guard_hash": k1_hash,
        "holdout_hash": holdout_hash,
        "adversarial_hash": adversarial_hash,
        "discovery_tree_count": len(discovery),
        "holdout_tree_count": len(holdout),
        "adversarial_tree_count": len(adversarial),
        "per_run_final_statement_count": len(per_run_final),
        "cross_run_exact_dedup_count": len(deduplicated),
        "candidate_ids": sorted(current),
        "literal_k1_falsified_count": len(k1_falsified),
        "literal_k1_falsified_ids": sorted(k1_falsified),
        "candidate_batch_hash": candidate_batch_hash,
        "candidate_batch_ids": candidate_batch_ids,
        "candidate_batch_frozen_before_holdout": True,
        "holdout_survivor_count": len(holdout_survivors),
        "holdout_survivor_ids": holdout_survivors,
        "adversarial_survivor_ids": [
            cid
            for cid in holdout_survivors
            if current[cid]["lifecycle_state"] == "ADVERSARIAL_PASSED"
        ],
        "final_state_counts": final_counts,
        "holdout_visible_to_generator": False,
        "feature_audit": audit,
        "known_identity_violations": identity_failures,
        "holdout_identity_violations": holdout_identity_failures,
        "pairwise_stage_counts": stage_totals,
    }
    _write_json(output_dir / "manifest.json", manifest)
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return {
        "manifest": manifest,
        "candidate_events": events,
        "final_candidates": list(current.values()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--spec", type=Path, default=Path("experiments/TF4-0001/spec.json")
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    run(args.spec, args.output_dir, args.source_commit)


if __name__ == "__main__":
    main()
