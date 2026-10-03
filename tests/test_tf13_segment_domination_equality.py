from experiments.tf13_segment_domination_equality import (
    build_diagnosis,
    maximum_leaf_interval,
    minimum_equality_classes,
    validate_repository_boundary,
)
from experiments.tf12_segment_domination_diagnosis import (
    _maximum_formula,
    _minimum_formula,
    _minimum_leaf_count,
)


def test_minimum_ceiling_slack_classes_match_rounded_leaf_bound():
    for order in range(4, 31):
        for segments in range(3, order):
            minimum = _minimum_formula(order, segments)
            minimum_leaves = _minimum_leaf_count(segments)
            expected = set()
            for leaves in range(minimum_leaves, segments + 1):
                leaf_bound = (order - leaves + 4) // 3
                if leaf_bound == minimum:
                    expected.add(
                        (
                            leaves,
                            3 * minimum - (order - leaves + 2),
                        )
                    )
            observed = {
                (row["leaf_count"], row["published_class_index_m"])
                for row in minimum_equality_classes(order, segments)
            }
            assert observed == expected


def test_maximum_leaf_interval_matches_direct_integer_optimization():
    for order in range(4, 31):
        for segments in range(3, order):
            minimum_leaves = _minimum_leaf_count(segments)
            values = {
                leaves: min(order - leaves, (order + leaves) // 3)
                for leaves in range(minimum_leaves, segments + 1)
            }
            maximum = max(values.values())
            assert maximum == _maximum_formula(order, segments)
            expected = [leaves for leaves, value in values.items() if value == maximum]
            lower, upper = maximum_leaf_interval(order, segments)
            assert list(range(lower, upper + 1)) == expected


def test_tf13_diagnosis_preserves_boundary_and_finds_realization_obstruction():
    validate_repository_boundary()
    diagnosis = build_diagnosis()

    assert diagnosis["analysis_id"] == "TF13-DIAG-0001"
    assert diagnosis["fresh_data_consumed"] is False
    assert diagnosis["burned_data_boundary"]["tree_count"] == 5447
    assert diagnosis["burned_data_boundary"]["occupied_n_q_cells"] == 80
    assert diagnosis["burned_data_boundary"]["orders_at_least_15"] == "untouched"

    minimum = diagnosis["minimum_equality"]
    assert minimum["status"] == "DIRECT_COROLLARY_OF_PUBLISHED_CLASSIFICATION"
    assert minimum["nonstar_reduced_tree_minimizer_exists"] is True

    maximum = diagnosis["maximum_equality"]
    assert maximum["status"] == "PARTIALLY_RESOLVED"
    assert maximum["all_tree_isomorphism_classes_status"] == (
        "UNRESOLVED_AFTER_BOUNDED_AUDIT"
    )
    assert maximum["burned_mixed_degree_sequence_group_count"] > 0
    example = maximum["smallest_mixed_degree_sequence_example"]
    assert (example["order"], example["segment_count"]) == (6, 3)
    assert example["degree_sequence"] == [3, 2, 2, 1, 1, 1]
    assert example["nonmaximizer"]["domination_number"] == 2
    assert example["maximizer"]["domination_number"] == 3

    burned = diagnosis["burned_diagnostics"]
    assert burned["all_maximizing_leaf_intervals_match"] is True
    assert burned["all_capable_degree_sequence_sets_match"] is True
    assert burned["gamma_equals_n_minus_l_iff_all_nonleaves_support_checks"] == 5445

    decision = diagnosis["decision"]
    assert decision["new_experiment_frozen"] is False
    assert decision["scientific_experiment_executed"] is False
    assert decision["candidate_ids_allocated"] == []
    assert decision["next_candidate_id"] == "TF-001158"
    assert decision["orders_at_least_15_untouched"] is True
