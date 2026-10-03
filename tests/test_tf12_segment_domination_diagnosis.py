from experiments.tf12_segment_domination_diagnosis import (
    build_diagnosis,
    validate_repository_boundary,
)


def test_tf12_diagnosis_resolves_values_and_preserves_pause():
    validate_repository_boundary()
    diagnosis = build_diagnosis()

    assert diagnosis["analysis_id"] == "TF12-DIAG-0001"
    assert diagnosis["classification"] == "PRIOR_ART_VALUE_RESOLUTION_EXPERIMENT_PAUSED"
    assert diagnosis["fresh_data_consumed"] is False
    assert diagnosis["burned_data_boundary"]["orders_at_least_15"] == "untouched"

    prior_art = diagnosis["prior_art_status"]
    assert prior_art["overall"] == "PARTIALLY_COVERED"
    assert prior_art["minimum_value"] == "DIRECT_COROLLARY_PLUS_ELEMENTARY_ATTAINMENT"
    assert prior_art["maximum_value"] == "DIRECT_COROLLARY_PLUS_FINITE_PARAMETER_OPTIMIZATION"
    assert prior_art["negative_search_is_novelty_evidence"] is False

    burned = diagnosis["burned_diagnostics"]
    assert burned["tree_count"] == 5447
    assert burned["occupied_n_q_cells"] == 80
    assert burned["all_cells_match_minimum_formula"] is True
    assert burned["all_cells_match_maximum_formula"] is True
    assert burned["all_cells_match_maximizing_leaf_optimizer"] is True
    assert all(cell["segment_count"] != 2 for cell in burned["cells"])

    selected = [
        row["representation"]
        for row in diagnosis["representation_selection_matrix"]
        if row["decision"] == "SELECT"
    ]
    assert selected == ["maintain_experiment_pause"]

    decision = diagnosis["decision"]
    assert decision["new_experiment_frozen"] is False
    assert decision["candidate_ids_allocated"] == []
    assert decision["next_candidate_id"] == "TF-001158"
    assert decision["order_15_consumed"] is False


def test_tf12_matrix_has_required_alternatives_and_no_scores():
    matrix = {row["representation"]: row for row in build_diagnosis()["representation_selection_matrix"]}
    assert {
        "pairwise_linear_hull",
        "exact_conditioned_envelope",
        "residue_aware_envelope",
        "structural_subdivision_recurrence",
        "maintain_experiment_pause",
    } <= matrix.keys()

    required = {
        "mathematical_object",
        "target",
        "conditioning_variables",
        "feature_vocabulary",
        "segment_count_only_new_invariant",
        "hidden_choices",
        "structural_motivation",
        "fit_to_subdivision_mathematics",
        "interpretability",
        "prior_art_risk",
        "exact_computation_feasibility",
        "major_confounders",
        "single_axis_relative_to_prior",
        "decision",
        "reason",
    }
    for row in matrix.values():
        assert required <= row.keys()
        assert row["decision"] in {"SELECT", "REJECT", "DEFER"}
        assert "score" not in row
        assert "rank" not in row
