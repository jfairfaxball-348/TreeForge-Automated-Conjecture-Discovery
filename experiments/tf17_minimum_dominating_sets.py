#!/usr/bin/env python3
"""TF17 burned-data diagnosis for minimum-dominating-set multiplicity.

This script never constructs a tree of order 15 or larger.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import networkx as nx

from treeforge.invariants.minimum_dominating_sets import minimum_dominating_set_profile
from treeforge.invariants.registry import default_registry
from treeforge.registry.candidate_registry import CandidateRegistry
from treeforge.trees.canonical import canonical_tree_code, generate_unlabeled_trees

CANDIDATES = Path("data/registry/candidates.jsonl")
EXPERIMENTS = Path("data/registry/experiments.jsonl")
MAX_BURNED_ORDER = 14


def _jsonl(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _corona(base: nx.Graph) -> nx.Graph:
    base = nx.convert_node_labels_to_integers(base, ordering="sorted")
    order = base.number_of_nodes()
    graph = base.copy()
    for vertex in range(order):
        graph.add_edge(vertex, order + vertex)
    return graph


def _w_tree(a: int, b: int) -> nx.Graph:
    """Return Taletskii's W_(a,b), with only burned sizes allowed here."""
    if a < 0 or b < 0:
        raise ValueError("a and b must be nonnegative")
    graph = nx.path_graph(3)
    next_vertex = 3
    for endpoint, count in ((0, a), (2, b)):
        for _ in range(count):
            preleaf = next_vertex
            leaf = next_vertex + 1
            next_vertex += 2
            graph.add_edges_from(((endpoint, preleaf), (preleaf, leaf)))
    if graph.number_of_nodes() > MAX_BURNED_ORDER:
        raise AssertionError("TF17 fresh-data firewall forbids order >=15")
    return graph


def _structure(graph: nx.Graph) -> dict[str, object]:
    leaves = {vertex for vertex, degree in graph.degree() if degree == 1}
    supports = {
        vertex
        for vertex in graph.nodes()
        if any(neighbor in leaves for neighbor in graph.neighbors(vertex))
    }
    strong_supports = {
        vertex
        for vertex in supports
        if sum(neighbor in leaves for neighbor in graph.neighbors(vertex)) >= 2
    }
    return {
        "degree_sequence": sorted((degree for _, degree in graph.degree()), reverse=True),
        "maximum_degree": max(degree for _, degree in graph.degree()),
        "leaf_count": len(leaves),
        "support_vertex_count": len(supports),
        "strong_support_count": len(strong_supports),
    }


def validate_repository_boundary() -> None:
    assert CandidateRegistry(CANDIDATES).next_id() == "TF-001158"

    experiments = _jsonl(EXPERIMENTS)
    scientific = [
        row
        for row in experiments
        if str(row.get("experiment_id", "")).startswith("TF")
    ]
    assert scientific
    assert scientific[-1]["experiment_id"] == "TF4-0001"
    assert all(
        not str(row.get("experiment_id", "")).startswith(
            ("TF5", "TF6", "TF7", "TF8", "TF9", "TF10", "TF11", "TF12", "TF13", "TF14", "TF15", "TF16", "TF17")
        )
        for row in experiments
    )

    names = set(default_registry().names())
    assert "minimum_dominating_set_count" not in names


def _burned_extremal_data() -> list[dict[str, object]]:
    trees = generate_unlabeled_trees(1, MAX_BURNED_ORDER)
    assert len(trees) == 5447
    assert max(graph.number_of_nodes() for graph in trees) == MAX_BURNED_ORDER

    grouped: dict[int, list[tuple[nx.Graph, int, int]]] = defaultdict(list)
    for graph in trees:
        gamma, zeta = minimum_dominating_set_profile(graph)
        grouped[graph.number_of_nodes()].append((graph, gamma, zeta))

    expected_tree_counts = [1, 1, 1, 2, 3, 6, 11, 23, 47, 106, 235, 551, 1301, 3159]
    expected_maxima = [1, 2, 1, 4, 3, 8, 8, 16, 18, 32, 40, 64, 84, 128]
    expected_extremizer_counts = [1, 1, 1, 1, 1, 1, 1, 2, 1, 3, 1, 6, 1, 11]

    rows: list[dict[str, object]] = []
    for order in range(1, MAX_BURNED_ORDER + 1):
        order_rows = grouped[order]
        maximum = max(zeta for _, _, zeta in order_rows)
        extremizers = [
            (graph, gamma)
            for graph, gamma, zeta in order_rows
            if zeta == maximum
        ]
        extremizer_codes = {canonical_tree_code(graph) for graph, _ in extremizers}

        assert len(order_rows) == expected_tree_counts[order - 1]
        assert maximum == expected_maxima[order - 1]
        assert len(extremizers) == expected_extremizer_counts[order - 1]

        structures = [_structure(graph) for graph, _ in extremizers]
        row: dict[str, object] = {
            "order": order,
            "tree_count": len(order_rows),
            "M_n": maximum,
            "extremizer_count": len(extremizers),
            "extremizer_gamma_values": sorted({gamma for _, gamma in extremizers}),
            "extremizer_maximum_degrees": sorted(
                {int(structure["maximum_degree"]) for structure in structures}
            ),
            "extremizer_leaf_counts": sorted(
                {int(structure["leaf_count"]) for structure in structures}
            ),
            "extremizer_support_counts": sorted(
                {int(structure["support_vertex_count"]) for structure in structures}
            ),
            "extremizer_strong_support_counts": sorted(
                {int(structure["strong_support_count"]) for structure in structures}
            ),
        }

        if order % 2 == 0:
            base_order = order // 2
            corona_codes = {
                canonical_tree_code(_corona(base))
                for base in generate_unlabeled_trees(base_order, base_order)
            }
            assert extremizer_codes == corona_codes
            row["structural_match"] = "exactly all H corona K1 for burned order"
            row["corona_base_order"] = base_order
            row["corona_base_tree_count"] = len(corona_codes)
        elif order >= 3:
            arm_total = (order - 3) // 2
            a = arm_total // 2
            b = arm_total - a
            w = _w_tree(a, b)
            formula = 3 * 2 ** (a + b) - 2**a - 2**b
            assert minimum_dominating_set_profile(w)[1] == formula
            assert maximum == formula
            assert extremizer_codes == {canonical_tree_code(w)}
            row["structural_match"] = "unique balanced Taletskii W_(a,b) for burned order"
            row["W_parameters"] = [a, b]
            row["W_formula"] = "3*2^(a+b)-2^a-2^b"
        else:
            row["structural_match"] = "K1"

        rows.append(row)

    return rows


def build_diagnosis() -> dict[str, object]:
    burned = _burned_extremal_data()
    return {
        "analysis_id": "TF17-DIAG-0001",
        "classification": "EXACT_MACHINERY_VALIDATED_STRUCTURAL_THEORY_INSUFFICIENT",
        "fresh_data_consumed": False,
        "burned_data_boundary": {
            "exhaustive_orders": [1, MAX_BURNED_ORDER],
            "tree_count": sum(int(row["tree_count"]) for row in burned),
            "orders_at_least_15": "untouched",
        },
        "exact_dp": {
            "states": {
                "A": "root selected",
                "B": "root unselected and dominated by at least one child",
                "C": "root unselected and must be dominated by its parent",
            },
            "arithmetic": "exact integer min-plus/count",
            "root_result": "min-plus choice of A and B",
            "default_invariant_registered": False,
        },
        "burned_extrema": burned,
        "structural_diagnosis": {
            "even_burned_orders": (
                "every extremizer is exactly a corona H corona K1; "
                "gamma=n/2 and zeta=2^(n/2)"
            ),
            "odd_burned_orders_from_3": (
                "the unique extremizer is the balanced W_(a,b) with "
                "a+b=(n-3)/2 and |a-b|<=1"
            ),
            "strong_supports": (
                "apart from K1/P3 edge cases, burned extremizers have no strong supports"
            ),
            "corona_mechanism": (
                "one choice from each host-leaf pair gives 2^(n/2) minimum dominating sets"
            ),
            "W_mechanism": (
                "Taletskii's published formula 3*2^(a+b)-2^a-2^b is maximized "
                "for fixed a+b by balancing a and b"
            ),
            "global_warning": (
                "these burned parity families cannot be promoted to an all-order extremal theorem: "
                "Taletskii's published degree-5 W_(4,4) module and module-joining construction "
                "have exponential growth strictly above sqrt(2)^n"
            ),
        },
        "theorem_first_reductions": {
            "strong_support_forcing": (
                "a support with at least two leaf neighbors is selected in every minimum dominating set"
            ),
            "safe_twin_leaf_pruning": (
                "if a support has at least three leaf neighbors, deleting one leaf preserves "
                "gamma and zeta; pruning from two leaves to one is not valid in general"
            ),
            "rooted_replacement_signature": (
                "a pendant rooted subtree influences the rest of the tree only through its "
                "three exact (cost,count) states A,B,C; equal rooted signatures are substitution-equivalent"
            ),
        },
        "experiment_decision": {
            "new_experiment_frozen": False,
            "reason": (
                "the exact burned extremizers are explained by explicit families, but published "
                "higher-growth constructions rule out those families as the unrestricted global grammar; "
                "no proved finite rooted-state recurrence or local normal-form theorem yet predicts M_15"
            ),
            "order_15_prediction_frozen": False,
            "order_15_consumed": False,
            "candidate_ids_allocated": [],
            "candidate_registry_changed": False,
            "experiment_registry_changed": False,
            "next_candidate_id": "TF-001158",
            "default_invariant_changed": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    validate_repository_boundary()
    payload = build_diagnosis()
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
