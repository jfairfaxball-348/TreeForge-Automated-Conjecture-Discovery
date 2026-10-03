import json
from pathlib import Path

from experiments.tf11_research_question_audit import load_and_validate
from treeforge.registry.candidate_registry import CandidateRegistry

SUMMARY = Path("experiments/TF11-DIAG-0001/diagnosis.json")
CANDIDATES = Path("data/registry/candidates.jsonl")
EXPERIMENTS = Path("data/registry/experiments.jsonl")


def _jsonl(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def test_tf11_selects_question_without_freezing_experiment():
    committed = load_and_validate()
    assert committed == json.loads(SUMMARY.read_text(encoding="utf-8"))

    selected = [
        row
        for row in committed["question_selection_matrix"]
        if row["decision"] == "SELECT"
    ]
    assert [row["alternative"] for row in selected] == ["fixed_segments_domination"]

    question = committed["selected_question"]
    assert question["question_id"] == "TF11-Q-SEGMENTS-DOMINATION"
    assert question["target"] == "domination_number"
    assert question["conditioning_parameters"] == ["order", "segment_count"]
    assert question["experiment_frozen"] is False


def test_tf11_preserves_fresh_data_and_registry_boundaries():
    committed = json.loads(SUMMARY.read_text(encoding="utf-8"))
    decision = committed["decision"]
    feasibility = committed["feasibility"]

    assert CandidateRegistry(CANDIDATES).next_id() == "TF-001158"
    experiments = _jsonl(EXPERIMENTS)
    assert sum(row["experiment_id"] == "TF4-0001" for row in experiments) == 1
    assert all(
        not str(row["experiment_id"]).startswith(
            ("TF5", "TF6", "TF7", "TF8", "TF9", "TF10", "TF11")
        )
        for row in experiments
    )

    assert decision["candidate_ids_allocated"] == []
    assert decision["candidate_registry_changed"] is False
    assert decision["experiment_registry_changed"] is False
    assert decision["order_15_consumed"] is False
    assert feasibility["order_15_values_inspected"] is False
    assert not Path("experiments/TF11-0001/spec.json").exists()


def test_tf11_matrix_is_question_first_and_unscored():
    committed = json.loads(SUMMARY.read_text(encoding="utf-8"))
    alternatives = {row["alternative"]: row for row in committed["question_selection_matrix"]}
    required = {
        "fixed_segments_domination",
        "fixed_branch_vertices_domination",
        "fixed_domination_wiener_extrema",
        "leaf_concentration_domination",
        "independent_domination_interaction",
        "pause_no_question",
    }
    assert required <= alternatives.keys()

    for row in alternatives.values():
        assert "score" not in row
        assert "rank" not in row

    assert alternatives["fixed_segments_domination"]["decision"] == "SELECT"
    assert alternatives["pause_no_question"]["decision"] == "REJECT"
