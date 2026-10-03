from experiments.tf15_segment_domination_rounded_defect import (
    build_diagnosis,
    dorfling_defect_increment,
    dorfling_defect_transition_table,
    validate_repository_boundary,
)


def test_dorfling_defect_transition_table_is_exact():
    assert dorfling_defect_transition_table() == {
        "T1": {"leaf_attacher": 1, "nonleaf_attacher": 2},
        "T2": {"leaf_attacher": -1, "nonleaf_attacher": 0},
        "T3": {"leaf_attacher": -1, "nonleaf_attacher": 0},
        "T4": {"leaf_attacher": 0, "nonleaf_attacher": 1},
        "T5": {"leaf_attacher": 0, "nonleaf_attacher": 1},
        "T6": {"leaf_attacher": 0, "nonleaf_attacher": 1},
    }
    assert dorfling_defect_increment("T2", attacher_is_leaf=True) == -1
    assert dorfling_defect_increment("T1", attacher_is_leaf=False) == 2


def test_tf15_diagnosis_closes_rounded_defect_without_fresh_data():
    validate_repository_boundary()
    diagnosis = build_diagnosis()

    assert diagnosis["analysis_id"] == "TF15-DIAG-0001"
    assert diagnosis["fresh_data_consumed"] is False
    assert diagnosis["burned_data_boundary"]["tree_count"] == 5447
    assert diagnosis["burned_data_boundary"]["orders_at_least_15"] == "untouched"

    assert diagnosis["strict_rounded_residue_1"]["status"] == (
        "TREEFORGE_ELEMENTARY_DERIVATION_FROM_PUBLISHED_RESULTS"
    )
    assert diagnosis["strict_rounded_residue_2"]["status"] == (
        "TREEFORGE_ELEMENTARY_DERIVATION_FROM_PUBLISHED_RESULTS"
    )

    support = diagnosis["support_refinement"]
    assert support["necessary_condition"] == "2 delta + |SL(T)| <= epsilon"
    assert support["equality_in_refined_bound_is_not_necessary"] is True

    burned = diagnosis["burned_diagnostics"]
    assert burned["refined_domination_bound_checks"] == 5445
    assert burned["strong_leaf_excess_identity_checks"] == 5445
    assert burned["strict_rounded_maximizer_residue_counts"] == {
        "0": 49,
        "1": 119,
        "2": 49,
    }
    assert burned["residue_delta_support_link_profiles"] == {
        "epsilon=0,delta=0,support_links=0": 49,
        "epsilon=1,delta=0,support_links=0": 50,
        "epsilon=1,delta=0,support_links=1": 69,
        "epsilon=2,delta=0,support_links=0": 33,
        "epsilon=2,delta=0,support_links=1": 3,
        "epsilon=2,delta=0,support_links=2": 5,
        "epsilon=2,delta=1,support_links=0": 8,
    }

    strict_residue_1 = burned["smallest_profile_examples"][
        "epsilon=1,delta=0,support_links=0"
    ]
    assert strict_residue_1["identity"][0] == 10

    strict_residue_2 = burned["smallest_profile_examples"][
        "epsilon=2,delta=0,support_links=0"
    ]
    assert strict_residue_2["identity"][0] == 8

    decision = diagnosis["decision"]
    assert decision["full_fixed_segment_maximum_equality_complete"] is True
    assert decision["fixed_segment_thread"] == "CLOSED"
    assert decision["new_experiment_frozen"] is False
    assert decision["candidate_ids_allocated"] == []
    assert decision["next_candidate_id"] == "TF-001158"
    assert decision["orders_at_least_15_untouched"] is True
