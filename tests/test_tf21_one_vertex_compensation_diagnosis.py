from experiments.tf21_one_vertex_compensation_diagnosis import (
    _p3_strong_banked_warning,
    _p5_compensation_obstruction,
    _subdivided_star_family,
    build_diagnosis,
    validate_repository_boundary,
)


def test_tf21_subdivided_star_family_has_exact_one_vertex_gain():
    rows = _subdivided_star_family()
    assert [row["arms"] for row in rows] == [2, 3, 4, 5, 6]
    for row in rows:
        arms = row["arms"]
        assert row["order"] == 2 * arms + 1
        assert tuple(row["profile"]) == (arms, 2**arms - 1)
        assert tuple(row["deletion_profile"]) == (arms, 2**arms)
        assert row["gain"] == 1
        assert row["core_max_degree"] == arms


def test_tf21_p5_is_an_exact_same_order_compensation_obstruction():
    record = _p5_compensation_obstruction()
    assert record["profile"] == (2, 3)
    assert record["deleted_forest_profile"] == (2, 4)
    assert record["order_5_maximum"] == 3
    assert record["unique_order_5_extremizer"] is True
    assert record["forest_reconnection"]["profile"] == (2, 4)
    assert record["one_edge_subdivision"]["profile"] == (2, 3)


def test_tf21_no_universal_hypothesis_is_essential_for_pairing():
    record = _p3_strong_banked_warning()
    assert record["profile"] == (1, 1)
    assert record["one_leaf_deleted_profile"] == (1, 2)
    assert record["both_leaves_deleted_profile"] == (1, 1)


def test_tf21_burned_pairing_and_unique_empty_checks_preserve_firewall():
    validate_repository_boundary()
    diagnosis = build_diagnosis(max_order=10)

    assert diagnosis["analysis_id"] == "TF21-DIAG-0001"
    assert (
        diagnosis["classification"]
        == "PAIRING_SOLVES_MULTI_EMPTY_UNIQUE_EMPTY_REMAINS_UNBOUNDED"
    )
    assert diagnosis["fresh_data_consumed"] is False
    assert diagnosis["burned_data_boundary"] == {
        "exhaustive_orders": [1, 10],
        "orders_at_least_15": "untouched",
    }

    rows = diagnosis["burned_residual_rows"]
    assert [row["residual_no_universal_empty_count"] for row in rows] == [
        0,
        0,
        0,
        0,
        1,
        0,
        2,
        2,
        5,
        9,
    ]
    assert [row["one_empty_count"] for row in rows] == [
        0,
        0,
        0,
        0,
        1,
        0,
        2,
        0,
        5,
        2,
    ]
    assert [row["multiple_empty_count"] for row in rows] == [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        2,
        0,
        7,
    ]
    assert [row["residual_extremizer_count"] for row in rows] == [
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
    ]
    assert [row["one_empty_extremizer_count"] for row in rows] == [
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
    ]
    assert [row["checked_empty_pairs"] for row in rows] == [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        2,
        0,
        7,
    ]

    decision = diagnosis["experiment_decision"]
    assert decision["new_experiment_frozen"] is False
    assert decision["order_15_prediction_frozen"] is False
    assert decision["order_15_consumed"] is False
    assert decision["candidate_ids_allocated"] == []
    assert decision["next_candidate_id"] == "TF-001158"
    assert decision["default_invariant_changed"] is False


def test_tf21_diagnosis_rejects_fresh_orders():
    try:
        build_diagnosis(max_order=15)
    except ValueError as error:
        assert "burned orders 1--14" in str(error)
    else:
        raise AssertionError("TF21 diagnosis must not expose order 15")
