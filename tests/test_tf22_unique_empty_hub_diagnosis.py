from experiments.tf22_unique_empty_hub_diagnosis import (
    _path_formula_record,
    _path_hub_rewire_record,
    _w_balance_reversal,
    _w_formula_record,
    build_diagnosis,
    validate_repository_boundary,
)


def test_tf22_w_formula_and_context_reversal_are_exact():
    balanced = _w_formula_record(2, 2)
    unbalanced = _w_formula_record(1, 3)

    assert balanced["root_pair"] == {"zeta": 40, "alpha": 22, "beta": 18}
    assert unbalanced["root_pair"] == {"zeta": 38, "alpha": 23, "beta": 15}

    reversal = _w_balance_reversal()
    assert reversal["unbalanced_minus_balanced"] == {
        "with_p2": -1,
        "with_p7_v3": 2,
    }


def test_tf22_path_family_exposes_context_sensitive_critical_rerooting():
    p10 = _path_formula_record(3)
    assert p10["profile"] == [4, 13]
    assert p10["stable_v2_pair"] == {"zeta": 13, "alpha": 9, "beta": 4}
    assert p10["critical_v4_pair"] == {"zeta": 13, "alpha": 6, "beta": 7}
    assert p10["critical_v4_c_count"] == 1
    assert p10["critical_reroot_delta_with_p2"] == -1


def test_tf22_path_hub_defeats_every_single_edge_rewire():
    row = _path_hub_rewire_record(3)
    assert row["order"] == 13
    assert row["component_zeta"] == 13
    assert row["best_stable_beta"] == 4
    assert row["critical_margin"] == 3
    assert row["hub_zeta"] == 22
    assert row["best_single_rewire_zeta"] == 22
    assert row["strict_single_rewire_exists"] is False


def test_tf22_burned_diagnosis_preserves_firewall_and_structural_split():
    validate_repository_boundary()
    diagnosis = build_diagnosis(max_order=10)

    assert diagnosis["analysis_id"] == "TF22-DIAG-0001"
    assert diagnosis["classification"] == "GLOBAL_HUB_OBJECTIVE_REMAINS_CONTEXT_SENSITIVE"
    assert diagnosis["fresh_data_consumed"] is False
    assert diagnosis["burned_data_boundary"] == {
        "exhaustive_orders": [1, 10],
        "orders_at_least_15": "untouched",
    }

    rows = diagnosis["burned_rows"]
    assert [row["all_flexible_count"] for row in rows] == [
        0, 1, 0, 1, 0, 1, 1, 2, 2, 5,
    ]
    assert [row["unique_empty_extremizer_count"] for row in rows] == [
        0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
    ]
    assert [row["strong_banked_extremizer_count"] for row in rows] == [
        0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    ]

    decision = diagnosis["experiment_decision"]
    assert decision["new_experiment_frozen"] is False
    assert decision["order_15_prediction_frozen"] is False
    assert decision["order_15_consumed"] is False
    assert decision["candidate_ids_allocated"] == []
    assert decision["candidate_registry_changed"] is False
    assert decision["experiment_registry_changed"] is False
    assert decision["next_candidate_id"] == "TF-001158"
    assert decision["default_invariant_changed"] is False


def test_tf22_diagnosis_rejects_fresh_orders():
    try:
        build_diagnosis(max_order=15)
    except ValueError as error:
        assert "burned orders 1--14" in str(error)
    else:
        raise AssertionError("TF22 diagnosis must not expose order 15")
