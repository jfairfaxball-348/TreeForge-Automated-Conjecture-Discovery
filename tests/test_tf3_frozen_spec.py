from pathlib import Path

from experiments.tf2_discovery import _adversarial_graphs as tf2_adversarial_graphs
from experiments.tf3_discovery import _adversarial_graphs as tf3_adversarial_graphs
from treeforge.experiments import load_frozen_spec
from treeforge.trees.canonical import canonical_tree_code


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


def test_tf3_fresh_adversarial_set_is_disjoint_from_exact_tf2_set():
    old_codes = {canonical_tree_code(graph) for _, _, graph in tf2_adversarial_graphs()}
    new_codes = {canonical_tree_code(graph) for _, _, graph in tf3_adversarial_graphs()}
    assert new_codes
    assert old_codes.isdisjoint(new_codes)
