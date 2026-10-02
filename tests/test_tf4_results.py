import json
from collections import Counter
from pathlib import Path

from treeforge.pipeline import stable_hash
from treeforge.registry.candidate_registry import CandidateRegistry

EXPECTED_SOURCE = "d8e0874a22dde7f226431fc4f15a36adb8254efa"
EXPECTED_RUN = 36983184665
EXPECTED_BATCH_HASH = "2bbb81b85eb6e40351f0913fafdc822c5417b2336e957e83fc08b505aedabf0f"
EXPECTED_HOLDOUT_HASH = "84978208ee2c65e3cda8327709e662cc71f9018ef2afc1ca03ff86a19a6197c3"
EXPECTED_ADVERSARIAL_HASH = "caf97df7db6b739383e015f816e3d643352cf53f164363d171c0eb1751e955f3"


def _json(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _jsonl(path: str):
    return [
        json.loads(line)
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def test_tf4_scientific_manifest_and_firewall_reproduce():
    manifest = _json("experiments/TF4-0001/manifest.json")
    freeze = _json("experiments/TF4-0001/candidate_batch_freeze.json")
    batch = _json("experiments/TF4-0001/candidate_batch.json")

    assert manifest["source_commit"] == EXPECTED_SOURCE
    assert manifest["candidate_ids"] == [f"TF-{n:06d}" for n in range(1012, 1158)]
    assert manifest["pairwise_stage_counts"] == {
        "raw_generator_output": 259,
        "after_morgan": 259,
        "after_dalmatian": 214,
        "after_duplicate_removal": 205,
        "after_touch_count_sort": 205,
        "strengthened_equalities": 0,
        "final_discover_output": 205,
    }
    assert manifest["cross_run_exact_dedup_count"] == 146
    assert manifest["literal_k1_falsified_count"] == 47
    assert freeze["holdout_constructed"] is False
    assert freeze["candidate_count"] == 99
    assert freeze["candidate_batch_hash"] == EXPECTED_BATCH_HASH
    assert stable_hash(batch) == EXPECTED_BATCH_HASH
    assert manifest["holdout_tree_count"] == 3159
    assert manifest["holdout_hash"] == EXPECTED_HOLDOUT_HASH
    assert manifest["holdout_survivor_count"] == 33
    assert manifest["adversarial_tree_count"] == 19
    assert manifest["adversarial_hash"] == EXPECTED_ADVERSARIAL_HASH
    assert len(manifest["adversarial_survivor_ids"]) == 33


def test_tf4_interpreted_results_and_registries_are_append_only():
    summary = _json("experiments/TF4-0001/interpretation_summary.json")
    assert summary["final_state_counts"] == {
        "ADVERSARIAL_PASSED": 20,
        "ARTIFACT_OF_FEATURE_SET": 4,
        "FALSIFIED": 114,
        "KNOWN_RESULT": 1,
        "NOVELTY_AUDIT": 1,
        "TRIVIAL": 6,
    }
    assert summary["mathematically_interesting_reached_ids"] == ["TF-001013", "TF-001028"]
    assert summary["graduation_candidate_ids"] == []
    assert summary["exact_tf2_overlap_ids"] == [
        "TF-001018", "TF-001022", "TF-001031", "TF-001088", "TF-001156"
    ]
    assert summary["exact_tf3_overlap_ids"] == []

    rows = _jsonl("data/registry/candidates.jsonl")
    tf4_rows = [row for row in rows if 1012 <= int(row["candidate_id"].split("-")[1]) <= 1157]
    tf4_cutoff = {}
    for row in tf4_rows:
        if row["created_at"] <= "2026-10-02T08:40:00Z":
            tf4_cutoff[row["candidate_id"]] = row
    assert sorted(tf4_cutoff) == [f"TF-{n:06d}" for n in range(1012, 1158)]
    assert Counter(row["lifecycle_state"] for row in tf4_cutoff.values()) == Counter(
        summary["final_state_counts"]
    )
    assert CandidateRegistry("data/registry/candidates.jsonl").next_id() == "TF-001158"

    experiments = _jsonl("data/registry/experiments.jsonl")
    tf4 = [row for row in experiments if row["experiment_id"] == "TF4-0001"]
    assert len(tf4) == 1
    assert tf4[0]["source_commit"] == EXPECTED_SOURCE
    assert tf4[0]["scientific_actions_run"] == EXPECTED_RUN
    assert tf4[0]["candidate_batch_hash"] == EXPECTED_BATCH_HASH
    assert tf4[0]["final_state_counts"] == summary["final_state_counts"]
    assert tf4[0]["graduation_candidate_count"] == 0
