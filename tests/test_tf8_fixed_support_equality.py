import json
from pathlib import Path

import networkx as nx

from experiments.tf7_support_mis_diagnosis import independent_set_count_forest
from experiments.tf8_fixed_support_equality import (
    build_diagnosis,
    core_is_independent,
    is_path_leaf_blowup,
    support_induced_forest,
)
from treeforge.invariants.core import maximal_independent_set_count, support_vertex_count
from treeforge.trees.families import caterpillar

SUMMARY = Path("experiments/TF8-DIAG-0001/diagnosis.json")


def test_tf8_diagnosis_reproduces_from_exposed_data_and_registries():
    committed = json.loads(SUMMARY.read_text(encoding="utf-8"))
    reproduced = build_diagnosis()
    assert reproduced == committed

    assert committed["classification"] == (
        "STRUCTURAL_EQUALITY_CHARACTERIZATION_NO_SCIENTIFIC_EXPERIMENT"
    )
    assert committed["fresh_data_consumed"] is False
    assert committed["burned_data_boundary"]["orders_at_least_15"] == "untouched"
    assert committed["decision"]["new_experiment_frozen"] is False
    assert committed["decision"]["tf4_mis_fan_reopened"] is False
    assert committed["coordinate_decision"]["raw_maximal_independent_set_count"] == (
        "RETAIN_UNCHANGED"
    )


def test_core_independence_is_the_exact_injection_equality_mechanism_on_paths():
    p5 = nx.path_graph(5)
    p6 = nx.path_graph(6)

    assert core_is_independent(p5)
    assert maximal_independent_set_count(p5) == independent_set_count_forest(
        support_induced_forest(p5)
    )

    assert not core_is_independent(p6)
    assert maximal_independent_set_count(p6) > independent_set_count_forest(
        support_induced_forest(p6)
    )


def test_duplicate_leaf_blowups_of_a_support_path_are_extremal():
    graph = caterpillar(4, [1, 3, 1, 2])
    assert support_vertex_count(graph) == 4
    assert is_path_leaf_blowup(graph)
    assert maximal_independent_set_count(graph) == 8


def test_exposed_family_match_and_registry_boundary_are_unchanged():
    committed = json.loads(SUMMARY.read_text(encoding="utf-8"))
    exposed = committed["exposed_computational_check"]
    provenance = committed["provenance_verification"]

    assert exposed["tree_count"] == 5447
    assert exposed["injection_equality_equivalence_failures_excluding_P2"] == 0
    assert exposed["support_forest_path_equality_failures"] == 0
    assert exposed["fixed_support_characterization_failures_for_s_at_least_3"] == 0
    assert exposed["generated_leaf_blowup_family_match_failures"] == 0
    assert exposed["fixed_support_equality_counts_by_s_and_order"]["7"] == {"14": 1}

    assert provenance["tf4_mis_fan"]["adversarial_passed"] == 18
    assert provenance["tf4_mis_fan"]["artifact_of_feature_set"] == 2
    assert provenance["highest_allocated_candidate"] == "TF-001157"
    assert provenance["next_permanent_candidate_id"] == "TF-001158"
    assert provenance["tf4_experiment_registry_records"] == 1
    assert provenance["tf5_tf6_tf7_tf8_scientific_experiment_records"] == 0
