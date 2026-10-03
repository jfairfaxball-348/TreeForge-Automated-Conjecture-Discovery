#!/usr/bin/env python3
"""Validate and reproduce the TF10 next-question diagnosis without fresh tree data."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from experiments.tf8_fixed_support_equality import TF4_MIS_FAN
from treeforge.invariants.registry import default_registry
from treeforge.registry.candidate_registry import CandidateRegistry

SUMMARY = Path("experiments/TF10-DIAG-0001/diagnosis.json")
CANDIDATES = Path("data/registry/candidates.jsonl")
EXPERIMENTS = Path("data/registry/experiments.jsonl")
TF10_SPEC = Path("experiments/TF10-0001/spec.json")

EXPECTED_CORE = (
    "cherry_count",
    "degree_sum",
    "diameter",
    "domination_number",
    "eccentricity_sum",
    "edge_count",
    "independence_number",
    "leaf_count",
    "matching_number",
    "max_degree",
    "maximal_independent_set_count",
    "min_degree",
    "order",
    "radius",
    "support_vertex_count",
    "wiener_index",
)


def _jsonl(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def load_and_validate() -> dict[str, object]:
    payload = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert payload["analysis_id"] == "TF10-DIAG-0001"
    assert payload["classification"] == "NEXT_QUESTION_DIAGNOSIS_NO_SCIENTIFIC_EXPERIMENT"
    assert payload["fresh_data_consumed"] is False
    assert payload["burned_data_boundary"]["orders_at_least_15"] == "untouched"

    candidates = _jsonl(CANDIDATES)
    latest: dict[str, dict[str, object]] = {}
    for row in candidates:
        latest[str(row["candidate_id"])] = row

    expected = {
        "TF-001028": (7, "KNOWN_RESULT"),
        "TF-001034": (6, "ARTIFACT_OF_FEATURE_SET"),
        "TF-001037": (6, "ARTIFACT_OF_FEATURE_SET"),
        "TF-001091": (5, "ADVERSARIAL_PASSED"),
        "TF-001095": (5, "ADVERSARIAL_PASSED"),
    }
    for candidate_id, (revision, state) in expected.items():
        row = latest[candidate_id]
        assert row["revision"] == revision
        assert row["lifecycle_state"] == state

    fan_states = Counter(str(latest[cid]["lifecycle_state"]) for cid in TF4_MIS_FAN)
    assert fan_states == Counter({"ADVERSARIAL_PASSED": 18, "ARTIFACT_OF_FEATURE_SET": 2})
    assert CandidateRegistry(CANDIDATES).next_id() == "TF-001158"

    experiments = _jsonl(EXPERIMENTS)
    assert sum(row["experiment_id"] == "TF4-0001" for row in experiments) == 1
    assert all(
        not str(row["experiment_id"]).startswith(("TF5", "TF6", "TF7", "TF8", "TF9", "TF10"))
        for row in experiments
    )

    assert default_registry().names() == EXPECTED_CORE
    assert not TF10_SPEC.exists()

    selected = [row["alternative"] for row in payload["decision_matrix"] if row["decision"] == "SELECT"]
    assert selected == ["pause_no_experiment"]
    assert payload["decision"]["new_experiment_frozen"] is False
    assert payload["decision"]["candidate_ids_allocated"] == []
    assert payload["decision"]["order_15_consumed"] is False
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    payload = load_and_validate()
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
