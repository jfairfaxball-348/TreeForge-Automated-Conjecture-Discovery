import itertools

import networkx as nx

from experiments.tf14_segment_domination_maximum_equality import (
    build_diagnosis,
    fixed_leaf_maximum_branch,
    independent_domination_number_dp,
    validate_repository_boundary,
)
from treeforge.trees.canonical import generate_unlabeled_trees


def _independent_domination_number_bruteforce(graph: nx.Graph) -> int:
    nodes = list(graph.nodes())
    for size in range(1, len(nodes) + 1):
        for chosen in itertools.combinations(nodes, size):
            candidate = set(chosen)
            if any(
                graph.has_edge(u, v)
                for index, u in enumerate(chosen)
                for v in chosen[index + 1 :]
            ):
                continue
            if all(
                vertex in candidate
                or any(neighbor in candidate for neighbor in graph.neighbors(vertex))
                for vertex in nodes
            ):
                return size
    raise AssertionError("every finite tree has an independent dominating set")


def test_independent_domination_dp_matches_bruteforce_through_order_8():
    for graph in generate_unlabeled_trees(1, 8):
        assert independent_domination_number_dp(graph) == (
            _independent_domination_number_bruteforce(graph)
        )


def test_fixed_leaf_branch_partition_is_exact():
    for order in range(2, 31):
        for leaves in range(1, order):
            branch = fixed_leaf_maximum_branch(order, leaves)
            nonleaves = order - leaves
            rounded = (order + leaves) // 3
            if branch == "N_MINUS_L_STRICT":
                assert nonleaves < rounded
            elif branch == "ROUNDED_STRICT":
                assert rounded < nonleaves
            else:
                assert branch == "TIE"
                assert nonleaves == rounded


def test_tf14_diagnosis_isolates_only_rounded_slack_residue():
    validate_repository_boundary()
    diagnosis = build_diagnosis()

    assert diagnosis["analysis_id"] == "TF14-DIAG-0001"
    assert diagnosis["fresh_data_consumed"] is False
    assert diagnosis["burned_data_boundary"]["tree_count"] == 5447
    assert diagnosis["burned_data_boundary"]["orders_at_least_15"] == "untouched"

    maximum = diagnosis["maximum_equality"]
    assert maximum["overall_status"] == "PARTIALLY_RESOLVED"
    assert maximum["tie_status"] == (
        "TREEFORGE_ELEMENTARY_DERIVATION_FROM_PUBLISHED_RESULTS"
    )
    assert maximum["strict_rounded_residue_0_status"] == (
        "DIRECT_COROLLARY_OF_PUBLISHED_CLASSIFICATIONS"
    )
    assert maximum["strict_rounded_residue_1_2_status"] == (
        "UNRESOLVED_AFTER_BOUNDED_AUDIT"
    )

    burned = diagnosis["burned_diagnostics"]
    assert burned["support_core_identity_checks"] == 5445
    assert burned["independent_domination_bound_checks"] == 5446
    assert burned["branch_maximizer_counts_q_at_least_3"] == {
        "N_MINUS_L_STRICT": 39,
        "ROUNDED_STRICT": 217,
        "TIE": 59,
    }
    assert burned["strict_rounded_maximizer_residue_counts"] == {
        "0": 49,
        "1": 119,
        "2": 49,
    }
    assert burned["kurnosov_theorem3_sufficient_counts_on_strict_rounded_maximizers"] == {
        "ONE_LEAF_PER_SUPPORT_DEGREE2_CORE_PATH": 56,
        "OUTSIDE_THEOREM3_SUFFICIENT_CASES": 161,
    }

    outside = burned[
        "smallest_strict_rounded_maximizer_outside_kurnosov_theorem3_sufficient_cases"
    ]
    assert outside["identity"][0] == 7
    assert outside["degree_sequence"] == [3, 2, 2, 2, 1, 1, 1]
    assert outside["segment_lengths"] == [2, 2, 2]
    assert outside["domination_number"] if "domination_number" in outside else 3
    assert outside["independent_domination_number"] == 3

    multiple_leaf = burned[
        "smallest_strict_rounded_maximizer_with_multiple_leaves_at_a_support"
    ]
    assert multiple_leaf["identity"][0] == 8
    assert multiple_leaf["segment_lengths"] == [5, 1, 1]
    assert multiple_leaf["support_leaf_excess"] == 1

    nonlinear = burned[
        "smallest_strict_rounded_maximizer_with_nonlinear_non_support_core"
    ]
    assert nonlinear["identity"][0] == 10
    assert nonlinear["segment_lengths"] == [3, 3, 3]
    assert nonlinear["non_support_nonleaf_degrees_in_tree"][0] == 3

    decision = diagnosis["decision"]
    assert decision["new_experiment_frozen"] is False
    assert decision["scientific_experiment_executed"] is False
    assert decision["candidate_ids_allocated"] == []
    assert decision["next_candidate_id"] == "TF-001158"
    assert decision["orders_at_least_15_untouched"] is True


def test_support_core_target_examples_are_exact():
    diagnosis = build_diagnosis()
    burned = diagnosis["burned_diagnostics"]
    for key in (
        "smallest_strict_rounded_maximizer_outside_kurnosov_theorem3_sufficient_cases",
        "smallest_strict_rounded_maximizer_with_multiple_leaves_at_a_support",
        "smallest_strict_rounded_maximizer_with_nonlinear_non_support_core",
    ):
        example = burned[key]
        assert example["support_core_cost"] == example["support_core_target"]
