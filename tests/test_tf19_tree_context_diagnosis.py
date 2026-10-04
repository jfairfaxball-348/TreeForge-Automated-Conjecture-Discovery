import networkx as nx

from experiments.tf19_tree_context_diagnosis import (
    CONTEXT_COST_PATTERNS,
    _canonical_contexts,
    _context_equivalence_examples,
    _padding_examples,
    _tree_context_coordinatewise_counterexample,
    build_diagnosis,
    compose_profile,
    context_face_profile,
    context_interface,
    context_message,
    normalized_context_cost_pattern,
    validate_repository_boundary,
)
from treeforge.invariants.minimum_dominating_sets import (
    minimum_dominating_set_profile,
    rooted_minimum_dominating_set_states,
)
from treeforge.trees.families import path, star


def _attach_at_zero(outside: nx.Graph, gadget: nx.Graph) -> nx.Graph:
    outside = nx.convert_node_labels_to_integers(outside, first_label=0)
    offset = outside.number_of_nodes()
    gadget = nx.convert_node_labels_to_integers(gadget, first_label=offset)
    graph = nx.compose(outside, gadget)
    graph.add_edge(0, offset)
    return graph


def test_tf19_reverse_context_message_has_exact_three_cost_patterns():
    rows = _canonical_contexts()
    assert {tuple(row["normalized_cost_pattern"]) for row in rows} == set(
        CONTEXT_COST_PATTERNS
    )

    for outside_order in range(1, 9):
        for outside in [path(outside_order)]:
            states = rooted_minimum_dominating_set_states(outside, 0)
            pattern = normalized_context_cost_pattern(context_message(states))
            assert pattern in CONTEXT_COST_PATTERNS


def test_tf19_context_composition_formula_matches_direct_tree_closure():
    for outside_order in range(1, 4):
        outside = path(outside_order)
        outside_states = rooted_minimum_dominating_set_states(outside, 0)
        for leaves in range(1, 4):
            gadget = star(leaves)
            gadget_states = rooted_minimum_dominating_set_states(gadget, 0)
            combined = _attach_at_zero(outside, gadget)
            assert compose_profile(outside_states, gadget_states) == (
                minimum_dominating_set_profile(combined)
            )


def test_tf19_projective_signature_is_not_context_minimal():
    examples = _context_equivalence_examples()
    overrefined = examples["projective_overrefinement"]
    assert overrefined["R_projective"] != overrefined["S_projective"]
    assert overrefined["common_context_interface"] == (
        ((0,), (0,), (0,)),
        (1, 0, 0),
    )

    r_states = rooted_minimum_dominating_set_states(star(2), 0)
    s_states = rooted_minimum_dominating_set_states(star(3), 0)
    assert context_face_profile(r_states) == context_face_profile(s_states)
    assert context_interface(r_states) == context_interface(s_states)


def test_tf19_context_quotient_remains_infinite_on_path_family_witnesses():
    witnesses = _context_equivalence_examples()["infinite_quotient_witness_family"]
    assert [row["order"] for row in witnesses] == [3, 6, 9, 12]
    assert len({repr(row["context_interface"]) for row in witnesses}) == 4


def test_tf19_naive_coordinatewise_dominance_fails_in_a_genuine_context():
    example = _tree_context_coordinatewise_counterexample()
    assert example["outside_context"] == "endpoint-rooted P2 (cost pattern E0)"
    assert example["R_filled_profile"] == (4, 4)
    assert example["S_filled_profile"] == (3, 2)


def test_tf19_strong_support_padding_and_arbitrary_padding_failure():
    examples = _padding_examples()
    assert examples["strong_support_padding"]["before"]["profile"] == (1, 1)
    assert examples["strong_support_padding"]["after"]["profile"] == (1, 1)
    assert examples["arbitrary_padding_counterexample"]["before"]["profile"] == (1, 2)
    assert examples["arbitrary_padding_counterexample"]["after"]["profile"] == (1, 1)


def test_tf19_burned_diagnosis_preserves_firewall():
    validate_repository_boundary()
    diagnosis = build_diagnosis(max_order=8)
    assert diagnosis["analysis_id"] == "TF19-DIAG-0001"
    assert diagnosis["classification"] == "TREE_CONTEXT_QUOTIENT_EXACT_BUT_INFINITE"
    assert diagnosis["fresh_data_consumed"] is False
    assert diagnosis["burned_data_boundary"] == {
        "exhaustive_orders": [1, 8],
        "orders_at_least_15": "untouched",
    }
    row8 = diagnosis["burned_context_rows"][-1]
    assert row8["order"] == 8
    assert row8["projective_interface_count"] == 70
    assert row8["context_interface_count"] == 49
    assert row8["context_face_profile_count"] == 6
    assert row8["weak_context_undominated_count"] == 11
    assert row8["strict_context_survivor_count"] == 15

    decision = diagnosis["experiment_decision"]
    assert decision["new_experiment_frozen"] is False
    assert decision["order_15_prediction_frozen"] is False
    assert decision["order_15_consumed"] is False
    assert decision["candidate_ids_allocated"] == []
    assert decision["next_candidate_id"] == "TF-001158"
    assert decision["default_invariant_changed"] is False


def test_tf19_diagnosis_rejects_fresh_orders():
    try:
        build_diagnosis(max_order=15)
    except ValueError as error:
        assert "burned orders 1--14" in str(error)
    else:
        raise AssertionError("TF19 diagnosis must not expose order 15")
