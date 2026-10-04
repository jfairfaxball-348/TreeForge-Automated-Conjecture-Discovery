import networkx as nx

from experiments.tf20_global_compensation_diagnosis import (
    _p4_one_leaf_extension_counterexample,
    _weak_banked_replacement_example,
    build_diagnosis,
    marked_support_core,
    p2_p3_budget,
    strong_supports,
    validate_repository_boundary,
)
from treeforge.trees.families import path, star


def test_tf20_p2_p3_budget_covers_every_deficit_at_least_two():
    for deficit in range(2, 31):
        p2_count, p3_count = p2_p3_budget(deficit)
        assert p2_count >= 0
        assert p3_count >= 0
        assert 2 * p2_count + 3 * p3_count == deficit


def test_tf20_marked_support_core_reconstructs_bankless_examples():
    p4 = path(4)
    assert strong_supports(p4) == ()
    record = marked_support_core(p4)
    assert record["kind"] == "MARKED_TREE_CORE"
    assert record["core_order"] == 2
    assert record["mark_count"] == 2
    assert record["all_core_leaves_marked"] is True
    assert record["reconstruction_verified"] is True

    corona_edge = nx.Graph([(0, 1), (0, 2), (1, 3)])
    assert strong_supports(corona_edge) == ()
    assert marked_support_core(corona_edge)["mark_count"] == 2

    assert marked_support_core(nx.empty_graph(1))["kind"] == "K1"
    assert marked_support_core(path(2))["kind"] == "P2_EXCEPTION"


def test_tf20_strong_support_is_not_bankless():
    graph = star(2)
    assert len(strong_supports(graph)) == 1
    try:
        marked_support_core(graph)
    except ValueError as error:
        assert "strong-bankless" in str(error)
    else:
        raise AssertionError("strong-support trees must not enter the bankless-core map")


def test_tf20_one_vertex_leaf_compensation_is_false():
    example = _p4_one_leaf_extension_counterexample()
    assert example["base"]["profile"] == (2, 4)
    assert example["best_extension_zeta"] == 3
    assert {tuple(row["profile"]) for row in example["one_leaf_extensions"]} == {
        (2, 2),
        (2, 3),
    }


def test_tf20_external_strong_bank_restores_one_vertex_exactly():
    example = _weak_banked_replacement_example()
    assert example["old_gadget_order"] == 4
    assert example["new_gadget_order"] == 3
    assert example["vertex_deficit"] == 1
    assert example["same_context_interface"] is True
    assert example["old_profile"] == example["new_profile"] == (2, 1)


def test_tf20_burned_diagnosis_preserves_firewall_and_registry_boundary():
    validate_repository_boundary()
    diagnosis = build_diagnosis(max_order=8)

    assert diagnosis["analysis_id"] == "TF20-DIAG-0001"
    assert diagnosis["classification"] == "GLOBAL_COMPENSATION_REDUCES_OBSTRUCTION_TO_ONE_VERTEX"
    assert diagnosis["fresh_data_consumed"] is False
    assert diagnosis["burned_data_boundary"] == {
        "exhaustive_orders": [1, 8],
        "orders_at_least_15": "untouched",
    }

    for row in diagnosis["burned_global_rows"]:
        assert row["marked_core_verified_count"] == row["strong_bankless_tree_count"]

    decision = diagnosis["experiment_decision"]
    assert decision["new_experiment_frozen"] is False
    assert decision["order_15_prediction_frozen"] is False
    assert decision["order_15_consumed"] is False
    assert decision["candidate_ids_allocated"] == []
    assert decision["next_candidate_id"] == "TF-001158"
    assert decision["default_invariant_changed"] is False


def test_tf20_diagnosis_rejects_fresh_orders():
    try:
        build_diagnosis(max_order=15)
    except ValueError as error:
        assert "burned orders 1--14" in str(error)
    else:
        raise AssertionError("TF20 diagnosis must not expose order 15")
