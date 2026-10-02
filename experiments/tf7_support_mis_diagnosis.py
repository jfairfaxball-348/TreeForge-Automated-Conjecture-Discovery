#!/usr/bin/env python3
"""Reproduce the TF7 structural diagnosis of support vertices versus maximal independent sets."""

from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

import networkx as nx

from treeforge.invariants.core import maximal_independent_set_count, support_vertex_count
from treeforge.registry.candidate_registry import CandidateRegistry
from treeforge.trees.canonical import generate_unlabeled_trees

STARTING_MAIN = "3d4b3035301e681a7a5eed0facb2f5068051c746"
STARTING_MAIN_CI = 37047300108
OUTPUT = Path("experiments/TF7-DIAG-0001/diagnosis.json")
CANDIDATE_REGISTRY = Path("data/registry/candidates.jsonl")
EXPERIMENT_REGISTRY = Path("data/registry/experiments.jsonl")

WEAKER_TO_STRONGER = {
    "TF-001034": "TF-001091",
    "TF-001037": "TF-001095",
}


def _jsonl(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def fibonacci(index: int) -> int:
    """Return F_index for F_0=0, F_1=1."""
    if index < 0:
        raise ValueError("Fibonacci index must be nonnegative")
    a, b = 0, 1
    for _ in range(index):
        a, b = b, a + b
    return a


def independent_set_count_forest(forest: nx.Graph) -> int:
    """Count all independent sets in a forest by an exact two-state DP."""
    if not nx.is_forest(forest):
        raise ValueError("expected a forest")

    def visit(vertex: int, parent: int | None) -> tuple[int, int]:
        children = [visit(u, vertex) for u in forest.neighbors(vertex) if u != parent]
        selected = math.prod(unselected for _, unselected in children)
        unselected = math.prod(selected_child + unselected_child for selected_child, unselected_child in children)
        return selected, unselected

    total = 1
    for component in nx.connected_components(forest):
        root = min(component)
        selected, unselected = visit(root, None)
        total *= selected + unselected
    return total


def support_induced_forest(graph: nx.Graph) -> nx.Graph:
    leaves = {v for v, degree in graph.degree() if degree == 1}
    supports = [v for v in graph if any(u in leaves for u in graph.neighbors(v))]
    return graph.subgraph(supports).copy()


def _path_corona(support_count: int) -> nx.Graph:
    if support_count < 2:
        raise ValueError("path corona helper requires at least two base vertices")
    graph = nx.path_graph(support_count)
    for vertex in range(support_count):
        graph.add_edge(vertex, support_count + vertex)
    return graph


def _exposed_rows() -> list[dict[str, int]]:
    rows = []
    for graph in generate_unlabeled_trees(1, 14):
        support_forest = support_induced_forest(graph)
        rows.append(
            {
                "order": graph.number_of_nodes(),
                "support_vertex_count": support_vertex_count(graph),
                "maximal_independent_set_count": maximal_independent_set_count(graph),
                "support_forest_independent_set_count": independent_set_count_forest(support_forest),
            }
        )
    if len(rows) != 5447:
        raise AssertionError("exposed orders 1-14 corpus changed")
    return rows


def _exposed_extrema(rows: list[dict[str, int]]) -> dict[str, object]:
    by_support: defaultdict[int, list[dict[str, int]]] = defaultdict(list)
    for row in rows:
        by_support[row["support_vertex_count"]].append(row)

    minima: dict[str, dict[str, object]] = {}
    for support_count in sorted(by_support):
        group = by_support[support_count]
        minimum = min(row["maximal_independent_set_count"] for row in group)
        expected = (
            1
            if support_count == 0
            else 2
            if support_count in {1, 2}
            else fibonacci(support_count + 2)
        )
        if minimum != expected:
            raise AssertionError(f"fixed-support minimum changed at s={support_count}")
        minima[str(support_count)] = {
            "minimum_mis_count": minimum,
            "tree_count_at_minimum": sum(
                row["maximal_independent_set_count"] == minimum for row in group
            ),
            "orders_at_minimum": sorted(
                {
                    row["order"]
                    for row in group
                    if row["maximal_independent_set_count"] == minimum
                }
            ),
        }

    support_injection_failures = sum(
        row["maximal_independent_set_count"] < row["support_forest_independent_set_count"]
        for row in rows
        if row["order"] != 2
    )
    fibonacci_failures = sum(
        row["maximal_independent_set_count"] < fibonacci(row["support_vertex_count"] + 2)
        for row in rows
        if row["order"] != 2
    )
    inequality_a_failures = sum(
        row["maximal_independent_set_count"] < 3 * row["support_vertex_count"] - 4
        for row in rows
    )
    inequality_b_failures = sum(
        row["maximal_independent_set_count"] < 5 * row["support_vertex_count"] - 12
        for row in rows
    )
    if any(
        (
            support_injection_failures,
            fibonacci_failures,
            inequality_a_failures,
            inequality_b_failures,
        )
    ):
        raise AssertionError("TF7 exposed structural check failed")

    corona_checks = {}
    for support_count in range(3, 8):
        graph = _path_corona(support_count)
        actual_support = support_vertex_count(graph)
        actual_mis = maximal_independent_set_count(graph)
        expected_mis = fibonacci(support_count + 2)
        if actual_support != support_count or actual_mis != expected_mis:
            raise AssertionError("path-corona extremal family check failed")
        corona_checks[str(support_count)] = {
            "order": graph.number_of_nodes(),
            "support_vertex_count": actual_support,
            "maximal_independent_set_count": actual_mis,
        }

    return {
        "orders": [1, 14],
        "tree_count": len(rows),
        "fixed_support_minima": minima,
        "support_forest_injection_failures_excluding_P2": support_injection_failures,
        "fibonacci_bound_failures_excluding_P2": fibonacci_failures,
        "m_ge_3s_minus_4_failures": inequality_a_failures,
        "m_ge_5s_minus_12_failures": inequality_b_failures,
        "path_corona_checks": corona_checks,
        "classification": "burned/exposed interpretation data only; not proof",
    }


def _candidate_implications() -> dict[str, object]:
    records = _jsonl(CANDIDATE_REGISTRY)
    latest: dict[str, dict[str, object]] = {}
    for row in records:
        candidate_id = str(row["candidate_id"])
        if candidate_id in {*WEAKER_TO_STRONGER, *WEAKER_TO_STRONGER.values()}:
            latest[candidate_id] = row

    expected = {
        "TF-001034": (6, "ARTIFACT_OF_FEATURE_SET"),
        "TF-001037": (6, "ARTIFACT_OF_FEATURE_SET"),
        "TF-001091": (5, "ADVERSARIAL_PASSED"),
        "TF-001095": (5, "ADVERSARIAL_PASSED"),
    }
    for candidate_id, (revision, state) in expected.items():
        row = latest.get(candidate_id)
        if row is None or row["revision"] != revision or row["lifecycle_state"] != state:
            raise AssertionError(f"unexpected TF7 lifecycle state for {candidate_id}")

    return {
        "TF-001034": {
            "new_revision": 6,
            "new_state": "ARTIFACT_OF_FEATURE_SET",
            "universally_dominated_by": "TF-001091",
            "algebra": (
                "(m+2s+4)/5 <= (m+4)/3 exactly when m>=3s-4; "
                "TF7 proves that condition for every finite tree."
            ),
        },
        "TF-001037": {
            "new_revision": 6,
            "new_state": "ARTIFACT_OF_FEATURE_SET",
            "universally_dominated_by": "TF-001095",
            "algebra": (
                "(m+3s+12)/8 <= (m+12)/5 exactly when m>=5s-12; "
                "TF7 proves that condition for every finite tree."
            ),
        },
        "TF-001091": {
            "revision": 5,
            "state": "ADVERSARIAL_PASSED",
            "interpretation": (
                "TF7 proves only that this finite survivor is pointwise stronger than TF-001034; "
                "it does not prove the domination-number inequality itself."
            ),
        },
        "TF-001095": {
            "revision": 5,
            "state": "ADVERSARIAL_PASSED",
            "interpretation": (
                "TF7 proves only that this finite survivor is pointwise stronger than TF-001037; "
                "it does not prove the domination-number inequality itself."
            ),
        },
    }


def build_diagnosis() -> dict[str, object]:
    rows = _exposed_rows()
    experiments = _jsonl(EXPERIMENT_REGISTRY)
    if sum(row["experiment_id"] == "TF4-0001" for row in experiments) != 1:
        raise AssertionError("TF4-0001 registry multiplicity changed")
    if any(str(row["experiment_id"]).startswith(("TF5", "TF6", "TF7")) for row in experiments):
        raise AssertionError("unexpected TF5/TF6/TF7 scientific experiment record")

    next_id = CandidateRegistry(CANDIDATE_REGISTRY).next_id()
    if next_id != "TF-001158":
        raise AssertionError("candidate-ID continuity changed")

    return {
        "analysis_id": "TF7-DIAG-0001",
        "classification": "STRUCTURAL_DIAGNOSIS_NO_SCIENTIFIC_EXPERIMENT",
        "starting_main_head": STARTING_MAIN,
        "starting_main_ci_run": STARTING_MAIN_CI,
        "fresh_data_consumed": False,
        "burned_data_boundary": {
            "exhaustive_orders": [1, 14],
            "orders_at_least_15": "untouched",
            "tf2_tf3_tf4_hostile_sets": "burned",
            "tf5_family_instances": "burned interpretation data",
        },
        "structural_result": {
            "notation": (
                "m(T)=maximal_independent_set_count, S(T)=support-vertex set, "
                "s(T)=|S(T)|, i(F)=number of independent sets of a forest F."
            ),
            "support_forest_injection": (
                "For every tree except P2, each independent I subset S(T) seeds a nonempty, "
                "pairwise-disjoint class of maximal independent sets: include I and every leaf "
                "whose support neighbor is outside I, then extend to a maximal independent set. "
                "Hence m(T)>=i(T[S(T)]). K1 also satisfies the conclusion directly."
            ),
            "forest_fibonacci_bound": (
                "Every forest F on s vertices has i(F)>=F_(s+2), by induction using an isolated "
                "vertex or a leaf v with neighbor u: i(F)=i(F-v)+i(F-{u,v})."
            ),
            "strong_bound": (
                "For every finite tree T other than P2, m(T)>=F_(s(T)+2), with F_0=0,F_1=1. "
                "P2 has s=2 and m=2."
            ),
            "duplicate_leaf_reduction": (
                "Deleting duplicate leaves at an existing support vertex, while retaining one leaf, "
                "preserves both m(T) and s(T). Fixed-support extremal analysis may therefore reduce "
                "to one leaf per support without changing the objective."
            ),
            "adjacent_support_vertices": (
                "Adjacent supports require no exceptional recurrence: their edges simply appear in "
                "the support-induced forest T[S]. P2 is the sole exception because its support "
                "vertices are themselves leaves."
            ),
            "fixed_support_minimum": {
                "s=0": "1 (K1)",
                "s=1": "2 (nontrivial stars attain it)",
                "s=2": "2 (P2; among trees of order at least 3 the minimum is 3)",
                "s>=3": "F_(s+2)",
            },
            "extremal_family": (
                "For every s>=3, the corona P_s o K1 has support count s and "
                "m=i(P_s)=F_(s+2), so the fixed-support lower bound is exact."
            ),
        },
        "target_inequalities": {
            "m_ge_3s_minus_4": {
                "status": "PROVED_FOR_ALL_FINITE_TREES",
                "derivation": (
                    "Check s<=2 directly. For s>=3, F_(s+2)>=3s-4; equality starts at s=3 "
                    "and Fibonacci increments F_(s+1) are at least 3."
                ),
            },
            "m_ge_5s_minus_12": {
                "status": "PROVED_FOR_ALL_FINITE_TREES",
                "derivation": (
                    "Check s<=3 directly. At s=4, F_6=8=5s-12; thereafter Fibonacci increments "
                    "F_(s+1) are at least 5."
                ),
            },
        },
        "exposed_computational_check": _exposed_extrema(rows),
        "candidate_implications": _candidate_implications(),
        "provenance_verification": {
            "tf6_final_main_head": STARTING_MAIN,
            "tf6_post_merge_ci": STARTING_MAIN_CI,
            "tf6_pr": 12,
            "tf001028_state": "KNOWN_RESULT",
            "tf001028_revision": 7,
            "highest_allocated_candidate": "TF-001157",
            "next_permanent_candidate_id": next_id,
            "tf4_experiment_registry_records": 1,
            "tf7_scientific_experiment_records": 0,
        },
        "decision": {
            "raw_mis_coordinate": "RETAIN_UNCHANGED",
            "remaining_mis_fan": (
                "Archive as finite geometry after reclassifying TF-001034 and TF-001037 as "
                "universal projection artifacts; the other 18 TF4 MIS facets are not promoted."
            ),
            "new_experiment_frozen": False,
            "candidate_ids_allocated": [],
            "experiment_registry_updated": False,
            "reason": (
                "The fixed-support extremal theorem explains the two exposed dominance relations "
                "and removes two redundant projections, but it does not select an independently "
                "canonical transformation/removal of raw MIS or another single discovery-axis change."
            ),
            "next_session_recommendation": (
                "Keep orders >=15 untouched. Treat the fixed-support theorem and its equality "
                "mechanism as structural mathematics; leave the residual MIS facet fan archived "
                "unless a separately motivated question identifies a new controlled axis."
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    payload = build_diagnosis()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
