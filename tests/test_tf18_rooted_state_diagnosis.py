from experiments.tf18_rooted_state_diagnosis import (
    _coordinatewise_counterexample,
    build_diagnosis,
    validate_repository_boundary,
)


def test_tf18_coordinatewise_dominance_counterexample_is_exact():
    example = _coordinatewise_counterexample()

    assert example["order"] == 8
    assert example["R_signature"] == ((3, 1), (3, 1), (None, 0))
    assert example["S_signature"] == ((2, 1), (3, 2), (None, 0))
    assert example["R_root_profile"] == (3, 2)
    assert example["S_root_profile"] == (2, 1)


def test_tf18_projective_frontier_diagnosis_uses_only_burned_orders():
    validate_repository_boundary()
    diagnosis = build_diagnosis(max_order=8)

    assert diagnosis["analysis_id"] == "TF18-DIAG-0001"
    assert diagnosis["classification"] == "USEFUL_PROJECTIVE_DOMINANCE_NO_FINITE_GRAMMAR"
    assert diagnosis["fresh_data_consumed"] is False
    assert diagnosis["burned_data_boundary"] == {
        "exhaustive_orders": [1, 8],
        "orders_at_least_15": "untouched",
    }

    rows = diagnosis["rooted_state_rows"]
    assert [row["exact_signature_count"] for row in rows] == [1, 1, 2, 4, 9, 18, 38, 72]
    assert [row["projective_interface_count"] for row in rows] == [1, 1, 2, 4, 9, 18, 38, 70]
    assert [row["normalized_cost_shape_count"] for row in rows] == [1, 1, 2, 4, 7, 9, 11, 14]
    assert [row["weak_projective_undominated_count"] for row in rows] == [
        1,
        1,
        2,
        4,
        8,
        11,
        18,
        22,
    ]
    assert [row["strict_projective_survivor_count"] for row in rows] == [
        1,
        1,
        2,
        4,
        9,
        16,
        27,
        41,
    ]

    decision = diagnosis["experiment_decision"]
    assert decision["new_experiment_frozen"] is False
    assert decision["order_15_prediction_frozen"] is False
    assert decision["order_15_consumed"] is False
    assert decision["candidate_ids_allocated"] == []
    assert decision["next_candidate_id"] == "TF-001158"
    assert decision["default_invariant_changed"] is False


def test_tf18_diagnosis_rejects_fresh_orders():
    try:
        build_diagnosis(max_order=15)
    except ValueError as error:
        assert "burned orders 1--14" in str(error)
    else:
        raise AssertionError("TF18 diagnosis must not expose order 15")
