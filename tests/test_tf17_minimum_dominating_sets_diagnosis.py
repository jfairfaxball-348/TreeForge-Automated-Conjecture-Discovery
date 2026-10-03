from experiments.tf17_minimum_dominating_sets import (
    build_diagnosis,
    validate_repository_boundary,
)


def test_tf17_burned_extrema_and_structural_matches_preserve_firewall():
    validate_repository_boundary()
    diagnosis = build_diagnosis()

    assert diagnosis["analysis_id"] == "TF17-DIAG-0001"
    assert diagnosis["classification"] == "EXACT_MACHINERY_VALIDATED_STRUCTURAL_THEORY_INSUFFICIENT"
    assert diagnosis["fresh_data_consumed"] is False
    assert diagnosis["burned_data_boundary"] == {
        "exhaustive_orders": [1, 14],
        "tree_count": 5447,
        "orders_at_least_15": "untouched",
    }

    burned = diagnosis["burned_extrema"]
    assert [row["M_n"] for row in burned] == [
        1,
        2,
        1,
        4,
        3,
        8,
        8,
        16,
        18,
        32,
        40,
        64,
        84,
        128,
    ]
    assert [row["extremizer_count"] for row in burned] == [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        2,
        1,
        3,
        1,
        6,
        1,
        11,
    ]

    for row in burned:
        order = row["order"]
        if order % 2 == 0:
            assert row["structural_match"] == "exactly all H corona K1 for burned order"
        elif order >= 3:
            assert row["structural_match"] == "unique balanced Taletskii W_(a,b) for burned order"

    decision = diagnosis["experiment_decision"]
    assert decision["new_experiment_frozen"] is False
    assert decision["order_15_prediction_frozen"] is False
    assert decision["order_15_consumed"] is False
    assert decision["candidate_ids_allocated"] == []
    assert decision["next_candidate_id"] == "TF-001158"
    assert decision["default_invariant_changed"] is False


def test_tf17_exact_helper_is_not_promoted_to_default_registry():
    diagnosis = build_diagnosis()
    assert diagnosis["exact_dp"]["default_invariant_registered"] is False
    assert diagnosis["experiment_decision"]["candidate_registry_changed"] is False
    assert diagnosis["experiment_decision"]["experiment_registry_changed"] is False
