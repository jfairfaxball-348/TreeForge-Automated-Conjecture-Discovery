import json
from pathlib import Path

from experiments.tf2_discovery import _adversarial_rows as tf2_adversarial_rows
from experiments.tf3_discovery import _adversarial_rows as tf3_adversarial_rows
from treeforge.experiments import load_frozen_spec
from treeforge.registry.candidate_registry import CandidateRegistry


def test_tf3_frozen_spec_changes_only_generator_method_axis():
    spec = load_frozen_spec(Path("experiments/TF3-0001/spec.json"))
    tf2 = load_frozen_spec(Path("experiments/TF2-0001/spec.json"))

    assert spec["experiment_id"] == "TF3-0001"
    assert spec["target"] == tf2["target"] == "domination_number"
    assert spec["discovery_orders"] == tf2["discovery_orders"] == [2, 10]
    assert spec["discovery_features"] == tf2["discovery_features"]
    assert spec["txgraffiti"]["heuristics"] == tf2["txgraffiti"]["heuristics"]
    assert spec["txgraffiti"]["post_processors"] == tf2["txgraffiti"]["post_processors"]
    assert spec["txgraffiti"]["hypothesis_payload"] == tf2["txgraffiti"]["hypothesis_payload"] == []
    assert spec["txgraffiti"]["methods"] == ["ratios"]
    assert tf2["txgraffiti"]["methods"] == ["convex_hull", "ratios"]
    assert spec["interpretability_policy"]["post_generation_filter"] is None
    assert spec["interpretability_policy"]["touch_count_threshold"] is None
    assert spec["interpretability_policy"]["coefficient_or_denominator_threshold"] is None


def test_tf3_fresh_holdout_and_candidate_id_policy_are_frozen():
    spec = load_frozen_spec(Path("experiments/TF3-0001/spec.json"))
    assert spec["burned_or_exposed_orders"] == [11, 12]
    assert spec["holdout_orders"] == [13, 13]
    assert spec["expected_holdout_tree_count"] == 1301
    assert spec["holdout_kind"] == "exhaustive_all_unlabeled_trees_of_order_13"
    assert spec["candidate_policy"]["next_permanent_candidate_id"] == "TF-001000"
    assert CandidateRegistry("data/registry/candidates.jsonl").next_id() == "TF-001000"


def test_tf3_fresh_adversarial_set_is_disjoint_from_exact_tf2_set():
    tf2 = load_frozen_spec(Path("experiments/TF2-0001/spec.json"))
    tf3 = load_frozen_spec(Path("experiments/TF3-0001/spec.json"))
    old_rows = tf2_adversarial_rows(
        list(tf2["corpus_invariants"]),
        "OLD",
        "TF2-0001",
    )
    new_rows = tf3_adversarial_rows(
        list(tf3["corpus_invariants"]),
        "NEW",
        "TF3-0001",
    )
    old_codes = {row["tree_code"] for row in old_rows}
    new_codes = {row["tree_code"] for row in new_rows}
    assert new_codes
    assert old_codes.isdisjoint(new_codes)


def test_experiment_registry_has_not_preallocated_tf3_scientific_result():
    rows = [
        json.loads(line)
        for line in Path("data/registry/experiments.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert all(row["experiment_id"] != "TF3-0001" for row in rows)
