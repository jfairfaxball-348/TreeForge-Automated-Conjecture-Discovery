import json
from pathlib import Path

from experiments.tf7_support_mis_diagnosis import build_diagnosis, fibonacci
from treeforge.registry.candidate_registry import CandidateRegistry

SUMMARY = Path("experiments/TF7-DIAG-0001/diagnosis.json")


def _jsonl(path: str):
    return [
        json.loads(line)
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def test_tf7_diagnosis_reproduces_from_exposed_data_and_registries():
    committed = json.loads(SUMMARY.read_text(encoding="utf-8"))
    reproduced = build_diagnosis()
    assert reproduced == committed

    assert committed["classification"] == "STRUCTURAL_DIAGNOSIS_NO_SCIENTIFIC_EXPERIMENT"
    assert committed["fresh_data_consumed"] is False
    assert committed["burned_data_boundary"]["orders_at_least_15"] == "untouched"
    assert committed["target_inequalities"]["m_ge_3s_minus_4"]["status"] == (
        "PROVED_FOR_ALL_FINITE_TREES"
    )
    assert committed["target_inequalities"]["m_ge_5s_minus_12"]["status"] == (
        "PROVED_FOR_ALL_FINITE_TREES"
    )
    assert committed["decision"]["new_experiment_frozen"] is False
    assert committed["decision"]["raw_mis_coordinate"] == "RETAIN_UNCHANGED"


def test_exposed_fixed_support_minima_match_the_structural_formula():
    committed = json.loads(SUMMARY.read_text(encoding="utf-8"))
    minima = committed["exposed_computational_check"]["fixed_support_minima"]

    assert minima["0"]["minimum_mis_count"] == 1
    assert minima["1"]["minimum_mis_count"] == 2
    assert minima["2"]["minimum_mis_count"] == 2
    for support_count in range(3, 8):
        assert minima[str(support_count)]["minimum_mis_count"] == fibonacci(support_count + 2)

    assert committed["exposed_computational_check"][
        "support_forest_injection_failures_excluding_P2"
    ] == 0
    assert committed["exposed_computational_check"]["fibonacci_bound_failures_excluding_P2"] == 0
    assert committed["exposed_computational_check"]["m_ge_3s_minus_4_failures"] == 0
    assert committed["exposed_computational_check"]["m_ge_5s_minus_12_failures"] == 0


def test_tf7_candidate_revisions_are_append_only_and_stronger_siblings_are_unpromoted():
    candidates = _jsonl("data/registry/candidates.jsonl")
    latest = {}
    for row in candidates:
        if row["candidate_id"] in {"TF-001034", "TF-001037", "TF-001091", "TF-001095"}:
            latest[row["candidate_id"]] = row

    assert latest["TF-001034"]["revision"] == 6
    assert latest["TF-001034"]["lifecycle_state"] == "ARTIFACT_OF_FEATURE_SET"
    assert latest["TF-001037"]["revision"] == 6
    assert latest["TF-001037"]["lifecycle_state"] == "ARTIFACT_OF_FEATURE_SET"

    assert latest["TF-001091"]["revision"] == 5
    assert latest["TF-001091"]["lifecycle_state"] == "ADVERSARIAL_PASSED"
    assert latest["TF-001095"]["revision"] == 5
    assert latest["TF-001095"]["lifecycle_state"] == "ADVERSARIAL_PASSED"

    assert CandidateRegistry("data/registry/candidates.jsonl").next_id() == "TF-001158"


def test_tf7_did_not_create_a_scientific_experiment_record():
    experiments = _jsonl("data/registry/experiments.jsonl")
    assert sum(row["experiment_id"] == "TF4-0001" for row in experiments) == 1
    assert all(not str(row["experiment_id"]).startswith("TF7") for row in experiments)
