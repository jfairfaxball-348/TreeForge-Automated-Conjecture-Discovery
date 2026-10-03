import json
from pathlib import Path

from experiments.tf10_next_question_diagnosis import load_and_validate
from treeforge.registry.candidate_registry import CandidateRegistry

SUMMARY = Path("experiments/TF10-DIAG-0001/diagnosis.json")
CANDIDATES = Path("data/registry/candidates.jsonl")
EXPERIMENTS = Path("data/registry/experiments.jsonl")


def _jsonl(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def test_tf10_diagnosis_validates_and_selects_only_pause():
    committed = load_and_validate()
    assert committed == json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert committed["fresh_data_consumed"] is False
    assert committed["burned_data_boundary"]["orders_at_least_15"] == "untouched"

    selected = [row for row in committed["decision_matrix"] if row["decision"] == "SELECT"]
    assert [row["alternative"] for row in selected] == ["pause_no_experiment"]

    decision = committed["decision"]
    assert decision["selected_next_scientific_question"] is None
    assert decision["new_experiment_frozen"] is False
    assert decision["candidate_ids_allocated"] == []
    assert decision["tf4_mis_fan_reopened"] is False
    assert decision["tf7_tf9_theorem_thread_reopened"] is False
    assert decision["order_15_consumed"] is False


def test_tf10_preserves_registry_and_candidate_boundaries():
    committed = json.loads(SUMMARY.read_text(encoding="utf-8"))
    provenance = committed["provenance_verification"]

    assert provenance["tf9_pr"] == 15
    assert provenance["tf9_pr_head"] == "02fcbf6dca9cf74c27890ea0df61ef5e401aeeb1"
    assert provenance["tf9_pr_head_ci"] == 37062351898
    assert provenance["tf9_post_merge_ci"] == 37062610463

    assert CandidateRegistry(CANDIDATES).next_id() == "TF-001158"
    experiments = _jsonl(EXPERIMENTS)
    assert sum(row["experiment_id"] == "TF4-0001" for row in experiments) == 1
    assert all(
        not str(row["experiment_id"]).startswith(("TF5", "TF6", "TF7", "TF8", "TF9", "TF10"))
        for row in experiments
    )
    assert not Path("experiments/TF10-0001/spec.json").exists()


def test_tf10_matrix_covers_required_alternatives_without_scores():
    committed = json.loads(SUMMARY.read_text(encoding="utf-8"))
    alternatives = {row["alternative"]: row for row in committed["decision_matrix"]}
    required = {
        "continue_domination_unchanged",
        "domination_plus_wiener_index",
        "wiener_index_target",
        "subcubic_domination",
        "pause_no_experiment",
    }
    assert required <= alternatives.keys()

    required_fields = {
        "scientific_question",
        "target",
        "changed_axis",
        "unchanged_axes",
        "independent_mathematical_motivation",
        "known_literature_risk",
        "interpretability_expectation",
        "exact_computation_feasibility",
        "confounding_risks",
        "decision",
        "reason",
    }
    for row in alternatives.values():
        assert required_fields <= row.keys()
        assert "score" not in row
        assert "rank" not in row

    assert committed["invariant_vocabulary_audit"]["selection"] == "NO_NEW_INVARIANT_SELECTED"
    assert committed["target_audit"]["target_change_selected"] is False
    assert committed["subclass_audit"]["selection"] == "NO_SUBCLASS_SELECTED"
