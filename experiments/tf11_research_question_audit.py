#!/usr/bin/env python3
"""Validate the TF11 research-question audit without consuming fresh tree data."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from experiments.tf8_fixed_support_equality import TF4_MIS_FAN
from treeforge.invariants.registry import default_registry
from treeforge.registry.candidate_registry import CandidateRegistry

SUMMARY = Path("experiments/TF11-DIAG-0001/diagnosis.json")
CANDIDATES = Path("data/registry/candidates.jsonl")
EXPERIMENTS = Path("data/registry/experiments.jsonl")
TF10_SPEC = Path("experiments/TF10-0001/spec.json")
TF11_SPEC = Path("experiments/TF11-0001/spec.json")

HISTORICAL_CORE = (
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
    assert payload["analysis_id"] == "TF11-DIAG-0001"
    assert payload["classification"] == "RESEARCH_QUESTION_SELECTED_NO_SCIENTIFIC_EXPERIMENT"
    assert payload["starting_constraint"]["tf10_pause_is_binding"] is True

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
        not str(row["experiment_id"]).startswith(
            ("TF5", "TF6", "TF7", "TF8", "TF9", "TF10", "TF11")
        )
        for row in experiments
    )

    current_core = set(default_registry().names())
    assert set(HISTORICAL_CORE) <= current_core
    assert current_core <= set(HISTORICAL_CORE) | {"segment_count"}
    assert not TF10_SPEC.exists()
    assert not TF11_SPEC.exists()

    selected = [
        row["alternative"]
        for row in payload["question_selection_matrix"]
        if row["decision"] == "SELECT"
    ]
    assert selected == ["fixed_segments_domination"]

    selected_question = payload["selected_question"]
    assert selected_question["question_id"] == "TF11-Q-SEGMENTS-DOMINATION"
    assert selected_question["new_invariant"]["name"] == "segment_count"
    assert selected_question["new_invariant"]["status"] == "not_yet_implemented"
    assert selected_question["experiment_frozen"] is False

    decision = payload["decision"]
    assert decision["question_selected"] is True
    assert decision["new_experiment_frozen"] is False
    assert decision["candidate_ids_allocated"] == []
    assert decision["next_candidate_id"] == "TF-001158"
    assert decision["candidate_registry_changed"] is False
    assert decision["experiment_registry_changed"] is False
    assert decision["tf4_mis_fan_reopened"] is False
    assert decision["tf7_tf9_theorem_thread_reopened"] is False
    assert decision["order_15_consumed"] is False
    assert decision["orders_at_least_15_untouched"] is True

    feasibility = payload["feasibility"]
    assert feasibility["burned_orders_1_14_recomputed"] is False
    assert feasibility["order_15_timing_probe_run"] is False
    assert feasibility["order_15_values_inspected"] is False
    assert feasibility["segment_count_implementation_added"] is False

    required_fields = {
        "precise_question",
        "target_objective",
        "conditioning_or_domain",
        "independent_mathematical_motivation",
        "connection_to_tf0_tf10",
        "required_invariants",
        "new_invariant_needed",
        "likely_relation_grammar",
        "known_literature_risk",
        "exact_computation_feasibility",
        "main_confounding_risk",
        "one_material_axis",
        "decision",
        "reason",
    }
    assert len(payload["question_selection_matrix"]) >= 5
    for row in payload["question_selection_matrix"]:
        assert required_fields <= row.keys()
        assert "score" not in row
        assert "rank" not in row

    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    payload = load_and_validate()
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
