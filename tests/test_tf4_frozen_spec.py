from pathlib import Path

from experiments.tf2_discovery import _adversarial_graphs as tf2_adversarial_graphs
from experiments.tf3_discovery import _adversarial_graphs as tf3_adversarial_graphs
from experiments.tf4_discovery import _adversarial_graphs as tf4_adversarial_graphs
from treeforge.experiments import load_frozen_spec
from treeforge.trees.canonical import canonical_tree_identity


def test_tf4_frozen_spec_changes_only_pairwise_relation_geometry():
    spec = load_frozen_spec(Path("experiments/TF4-0001/spec.json"))
    tf3 = load_frozen_spec(Path("experiments/TF3-0001/spec.json"))

    assert spec["experiment_id"] == "TF4-0001"
    assert spec["target"] == tf3["target"] == "domination_number"
    assert spec["discovery_orders"] == tf3["discovery_orders"] == [2, 10]
    assert spec["discovery_features"] == tf3["discovery_features"]
    assert spec["txgraffiti"]["heuristics"] == tf3["txgraffiti"]["heuristics"]
    assert spec["txgraffiti"]["post_processors"] == tf3["txgraffiti"]["post_processors"]
    assert (
        spec["txgraffiti"]["hypothesis_payload"]
        == tf3["txgraffiti"]["hypothesis_payload"]
        == []
    )
    assert spec["hypotheses"] == tf3["hypotheses"]
    assert spec["txgraffiti"]["methods"] == ["convex_hull"]
    assert tf3["txgraffiti"]["methods"] == ["ratios"]
    assert spec["txgraffiti"]["feature_set_construction"].startswith(
        "Run once for each of the 21 unordered pairs"
    )
    assert spec["interpretability_policy"]["expected_rhs_distinct_feature_symbols_maximum"] == 2
    assert spec["interpretability_policy"]["candidate_cap"] is None
    assert spec["interpretability_policy"]["touch_count_threshold"] is None
    assert spec["interpretability_policy"]["coefficient_or_denominator_threshold"] is None


def test_tf4_keeps_literal_all_tree_domain_and_adds_exposed_k1_guard():
    spec = load_frozen_spec(Path("experiments/TF4-0001/spec.json"))
    guard = spec["literal_domain_consistency_gate"]

    assert spec["hypotheses"] == ["finite", "simple", "unlabeled", "tree"]
    assert guard["mathematical_hypothesis_changed"] is False
    assert guard["exposed_guard_tree"] == "K1"
    assert "before candidate_batch.json is frozen" in guard["timing"]
    assert spec["candidate_policy"]["batch_freeze"].startswith(
        "All discovery-side machine triage plus the exposed K1"
    )


def test_tf4_fresh_holdout_and_candidate_id_policy_are_frozen():
    spec = load_frozen_spec(Path("experiments/TF4-0001/spec.json"))

    assert spec["burned_or_exposed_orders"] == list(range(1, 14))
    assert spec["holdout_orders"] == [14, 14]
    assert spec["expected_holdout_tree_count"] == 3159
    assert spec["holdout_kind"] == "exhaustive_all_unlabeled_trees_of_order_14"
    assert spec["candidate_policy"]["next_permanent_candidate_id"] == "TF-001012"


def test_tf4_fresh_adversarial_set_is_disjoint_from_tf2_and_tf3():
    old_ids = {
        canonical_tree_identity(graph)
        for builder in [tf2_adversarial_graphs, tf3_adversarial_graphs]
        for _, _, graph in builder()
    }
    new_graphs = tf4_adversarial_graphs()
    new_ids = {canonical_tree_identity(graph) for _, _, graph in new_graphs}

    assert len(new_graphs) == 19
    assert len(new_ids) == 19
    assert old_ids.isdisjoint(new_ids)
