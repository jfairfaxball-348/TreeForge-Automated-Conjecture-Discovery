import json
from pathlib import Path

from experiments.tf5_analysis import build_summary
from treeforge.registry.candidate_registry import CandidateRegistry

SUMMARY = Path("experiments/TF5-TF001028/analysis_summary.json")


def _jsonl(path: str):
    return [
        json.loads(line)
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def test_tf5_summary_reproduces_from_exposed_data():
    committed = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert build_summary() == committed
    assert committed["exposed_exhaustive_check"]["tree_count"] == 5447
    assert committed["exposed_exhaustive_check"]["failures"] == 0
    assert committed["family_search"]["parameter_instances_tested"] == 24048
    assert committed["family_search"]["counterexamples"] == 0
    assert committed["mis_facet_diagnosis"]["count"] == 20
    assert committed["mis_facet_diagnosis"]["new_experiment_frozen"] is False


def test_tf001028_append_only_resolution_and_candidate_id_continuity():
    records = _jsonl("data/registry/candidates.jsonl")
    lineage = [row for row in records if row["candidate_id"] == "TF-001028"]
    assert [row["revision"] for row in lineage] == list(range(1, 8))
    assert lineage[-2]["lifecycle_state"] == "NOVELTY_AUDIT"
    assert lineage[-1]["lifecycle_state"] == "KNOWN_RESULT"
    assert "DIRECT_COROLLARY_OF_STRONGER_PRIOR_ART" in lineage[-1]["prior_art_status"]
    assert CandidateRegistry("data/registry/candidates.jsonl").next_id() == "TF-001158"


def test_tf5_did_not_create_a_scientific_experiment_record():
    experiments = _jsonl("data/registry/experiments.jsonl")
    assert all(row["experiment_id"] != "TF5-0001" for row in experiments)


def test_prior_art_case_split_arithmetic_covers_all_integer_diameters():
    assert 3 * 1 + 0 == 2 * 1 + 1
    for n in range(2, 401):
        for diameter in range(1, n):
            if 2 * diameter <= n + 2:
                ore_upper = n // 2
                assert 3 * ore_upper + diameter <= 2 * n + 1
            else:
                assert 2 * diameter >= n + 2
                x = 2 * diameter - n - 1
                gu_upper = n - diameter + (-(-x // 3))
                assert 3 * gu_upper + diameter <= 2 * n + 1
