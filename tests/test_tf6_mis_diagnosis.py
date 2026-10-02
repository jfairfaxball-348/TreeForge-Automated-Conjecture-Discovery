import json
from pathlib import Path

from experiments.tf5_analysis import MIS_IDS
from experiments.tf6_mis_diagnosis import build_diagnosis
from treeforge.registry.candidate_registry import CandidateRegistry

SUMMARY = Path("experiments/TF6-DIAG-0001/diagnosis.json")


def _jsonl(path: str):
    return [
        json.loads(line)
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def test_tf6_diagnosis_reproduces_from_exposed_data_and_registries():
    committed = json.loads(SUMMARY.read_text(encoding="utf-8"))
    reproduced = build_diagnosis()
    assert reproduced == committed

    assert committed["classification"] == "EXPOSED_DATA_DIAGNOSIS_ONLY"
    assert committed["fresh_data_consumed"] is False
    assert committed["candidate_fan"]["candidate_ids"] == MIS_IDS
    assert committed["candidate_fan"]["count"] == 20
    assert committed["geometry"]["coordinate_family_counts"] == {
        "mis_only": 3,
        "support_plus_mis": 6,
        "diameter_plus_mis": 9,
        "matching_plus_mis": 2,
    }
    assert committed["geometry"]["exposed_pointwise_dominance_relations"] == [
        ["TF-001091", "TF-001034"],
        ["TF-001095", "TF-001037"],
    ]
    assert committed["decision"]["raw_mis_coordinate"] == "RETAIN_UNCHANGED_FOR_NOW"
    assert committed["decision"]["new_experiment_frozen"] is False
    assert committed["decision"]["candidate_ids_allocated"] == []


def test_tf6_preserves_candidate_and_experiment_registries():
    candidates = _jsonl("data/registry/candidates.jsonl")
    experiments = _jsonl("data/registry/experiments.jsonl")

    tf001028 = [row for row in candidates if row["candidate_id"] == "TF-001028"]
    assert [row["revision"] for row in tf001028] == list(range(1, 8))
    assert tf001028[-1]["lifecycle_state"] == "KNOWN_RESULT"

    tf6_snapshot = {
        row["candidate_id"]: row
        for row in candidates
        if row["candidate_id"] in MIS_IDS and row["revision"] == 5
    }
    assert sorted(tf6_snapshot) == sorted(MIS_IDS)
    assert all(row["lifecycle_state"] == "ADVERSARIAL_PASSED" for row in tf6_snapshot.values())
    assert all(row["holdout_status"]["status"] == "PASSED" for row in tf6_snapshot.values())
    assert all(row["adversarial_status"]["status"] == "PASSED" for row in tf6_snapshot.values())

    assert sum(row["experiment_id"] == "TF4-0001" for row in experiments) == 1
    assert all(not str(row["experiment_id"]).startswith("TF5") for row in experiments)
    assert all(not str(row["experiment_id"]).startswith("TF6") for row in experiments)
    assert CandidateRegistry("data/registry/candidates.jsonl").next_id() == "TF-001158"
