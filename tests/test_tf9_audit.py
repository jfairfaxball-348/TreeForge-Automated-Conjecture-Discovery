import json
from collections import Counter
from pathlib import Path

from experiments.tf8_fixed_support_equality import TF4_MIS_FAN
from treeforge.registry.candidate_registry import CandidateRegistry

SUMMARY = Path("experiments/TF9-AUDIT-0001/audit_summary.json")
CANDIDATES = Path("data/registry/candidates.jsonl")
EXPERIMENTS = Path("data/registry/experiments.jsonl")


def _jsonl(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def test_tf9_audit_summary_records_bounded_nonexperimental_decision():
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))

    assert summary["analysis_id"] == "TF9-AUDIT-0001"
    assert summary["classification"] == "BOUNDED_PRIOR_ART_AUDIT_NO_SCIENTIFIC_EXPERIMENT"
    assert summary["starting_main_head"] == "2dcf6df89648dab8b050b1ebf05f332dceb90c54"
    assert summary["fresh_data_consumed"] is False
    assert summary["burned_data_boundary"]["orders_at_least_15"] == "untouched"

    components = summary["component_status"]
    assert components["forest_independent_set_minimum"]["status"] == "DIRECT_COROLLARY"
    assert components["fixed_support_value"]["status"] == "DIRECT_COROLLARY"
    assert (
        components["fixed_support_value"]["stronger_source_relationship"]
        == "STRICTLY_STRONGER_RESULT"
    )
    assert components["complete_fixed_support_equality_class"]["status"] == (
        "NOT_SHOWN_TO_BE_DIRECT_COROLLARY"
    )

    decision = summary["decision"]
    assert decision["tf4_mis_fan_reopened"] is False
    assert decision["raw_mis_coordinate"] == "RETAIN_UNCHANGED"
    assert decision["new_experiment_frozen"] is False
    assert decision["candidate_ids_allocated"] == []
    assert decision["theorem_repository_created"] is False
    assert summary["significance"]["separate_theorem_project"] is False
    assert summary["limitations"]["negative_search_is_novelty_evidence"] is False
    assert summary["limitations"]["exact_equality_novelty_claimed"] is False


def test_tf9_preserves_candidate_and_experiment_registry_boundary():
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
        assert latest[candidate_id]["revision"] == revision
        assert latest[candidate_id]["lifecycle_state"] == state

    fan_states = Counter(str(latest[candidate_id]["lifecycle_state"]) for candidate_id in TF4_MIS_FAN)
    assert fan_states == Counter({"ADVERSARIAL_PASSED": 18, "ARTIFACT_OF_FEATURE_SET": 2})
    assert CandidateRegistry(CANDIDATES).next_id() == "TF-001158"

    experiments = _jsonl(EXPERIMENTS)
    assert sum(row["experiment_id"] == "TF4-0001" for row in experiments) == 1
    assert all(
        not str(row["experiment_id"]).startswith(("TF5", "TF6", "TF7", "TF8", "TF9"))
        for row in experiments
    )


def test_tf9_relationship_labels_stay_within_the_frozen_audit_vocabulary():
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    allowed = {
        "EXACT_MATCH",
        "EQUIVALENT_REFORMULATION",
        "STRICTLY_STRONGER_RESULT",
        "DIRECT_COROLLARY",
        "SAME_INGREDIENT_DIFFERENT_PARAMETER",
        "RELATED_ONLY",
        "TERMINOLOGY_ONLY",
    }
    relationships = {row["relationship"] for row in summary["source_relationships"]}
    assert relationships <= allowed
    assert "STRICTLY_STRONGER_RESULT" in relationships
    assert "DIRECT_COROLLARY" in relationships
    assert "SAME_INGREDIENT_DIFFERENT_PARAMETER" in relationships
