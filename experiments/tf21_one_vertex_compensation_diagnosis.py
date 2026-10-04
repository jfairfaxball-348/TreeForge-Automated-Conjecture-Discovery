#!/usr/bin/env python3
"""TF21 one-vertex compensation diagnosis using only burned orders 1--14.

The theorem-facing statements in this module are fixed before the burned
census.  TF21 proves that two empty vertices can be paired exactly in a
no-universal tree, then records the exact structure left by a unique empty
vertex.  No function constructs an unlabeled tree of order 15 or larger.
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path

import networkx as nx

from experiments.tf20_global_compensation_diagnosis import (
    marked_support_core,
    strong_supports,
)
from treeforge.invariants.minimum_dominating_sets import (
    minimum_dominating_set_profile,
    rooted_minimum_dominating_set_states,
)
from treeforge.invariants.registry import default_registry
from treeforge.registry.candidate_registry import CandidateRegistry
from treeforge.trees.canonical import generate_unlabeled_trees
from treeforge.trees.families import path

CANDIDATES = Path("data/registry/candidates.jsonl")
EXPERIMENTS = Path("data/registry/experiments.jsonl")
MAX_BURNED_ORDER = 14

EXPECTED_TREE_COUNTS = [1, 1, 1, 2, 3, 6, 11, 23, 47, 106, 235, 551, 1301, 3159]


def _jsonl(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def validate_repository_boundary() -> None:
    """Assert the TF20 scientific boundary before burned-data diagnosis."""
    assert CandidateRegistry(CANDIDATES).next_id() == "TF-001158"

    experiments = _jsonl(EXPERIMENTS)
    scientific = [
        row for row in experiments if str(row.get("experiment_id", "")).startswith("TF")
    ]
    assert scientific
    assert scientific[-1]["experiment_id"] == "TF4-0001"
    assert all(
        not str(row.get("experiment_id", "")).startswith(
            tuple(f"TF{index}" for index in range(5, 22))
        )
        for row in experiments
    )

    assert "minimum_dominating_set_count" not in set(default_registry().names())


def vertex_status(graph: nx.Graph, vertex: object) -> str:
    """Return Taletskii's universal/empty/flexible status exactly."""
    selected, dominated, _ = rooted_minimum_dominating_set_states(graph, vertex)
    if dominated.cost is None or (
        selected.cost is not None and selected.cost < dominated.cost
    ):
        return "universal"
    if selected.cost is not None and dominated.cost < selected.cost:
        return "empty"
    return "flexible"


def _statuses(graph: nx.Graph) -> dict[object, str]:
    return {vertex: vertex_status(graph, vertex) for vertex in graph.nodes()}


def _forest_profile(forest: nx.Graph) -> tuple[int, int]:
    """Return exact (gamma,zeta), multiplicatively over forest components."""
    if forest.number_of_nodes() == 0:
        return 0, 1

    gamma = 0
    zeta = 1
    for vertices in nx.connected_components(forest):
        component = forest.subgraph(vertices).copy()
        component_gamma, component_zeta = minimum_dominating_set_profile(component)
        gamma += component_gamma
        zeta *= component_zeta
    return gamma, zeta


def _subdivided_star(arms: int) -> nx.Graph:
    """Return the star with every edge subdivided once."""
    if arms < 2:
        raise ValueError("TF21 uses at least two arms")
    graph = nx.Graph()
    graph.add_node(0)
    for index in range(arms):
        support = 2 * index + 1
        leaf = support + 1
        graph.add_edges_from(((0, support), (support, leaf)))
    return graph


def _double_deletion_isolate_free(
    graph: nx.Graph,
    left: object,
    right: object,
) -> bool:
    reduced = graph.copy()
    reduced.remove_nodes_from((left, right))
    return reduced.number_of_nodes() > 0 and all(
        degree > 0 for _, degree in reduced.degree()
    )


def _check_pairing(graph: nx.Graph, left: object, right: object) -> dict[str, object]:
    """Check the TF21 two-empty conclusion on one burned tree."""
    original = minimum_dominating_set_profile(graph)
    reduced = graph.copy()
    reduced.remove_nodes_from((left, right))
    reduced_profile = _forest_profile(reduced)

    assert _double_deletion_isolate_free(graph, left, right)
    assert reduced_profile[0] == original[0]
    assert reduced_profile[1] > original[1]
    assert max(dict(reduced.degree()).values()) <= max(dict(graph.degree()).values())

    return {
        "distance": nx.shortest_path_length(graph, left, right),
        "original_profile": original,
        "double_deletion_profile": reduced_profile,
    }


def _unique_empty_record(graph: nx.Graph, empty: object) -> dict[str, object]:
    """Check the exact component restrictions after deleting a sole empty vertex."""
    original_gamma, original_zeta = minimum_dominating_set_profile(graph)
    reduced = graph.copy()
    reduced.remove_node(empty)
    reduced_gamma, reduced_zeta = _forest_profile(reduced)

    assert reduced_gamma == original_gamma
    assert reduced_zeta > original_zeta
    assert all(degree > 0 for _, degree in reduced.degree())

    component_rows = []
    product_total = 1
    product_omit_root = 1
    for vertices in nx.connected_components(reduced):
        component = reduced.subgraph(vertices).copy()
        attachment_root = next(
            vertex
            for vertex in graph.neighbors(empty)
            if vertex in component
        )
        component_gamma, component_zeta = minimum_dominating_set_profile(component)
        component_statuses = _statuses(component)
        assert set(component_statuses.values()) == {"flexible"}

        selected, dominated, needs_parent = rooted_minimum_dominating_set_states(
            component,
            attachment_root,
        )
        assert selected.cost == dominated.cost == component_gamma
        assert needs_parent.cost is None or needs_parent.cost >= component_gamma
        assert selected.count > 0
        assert dominated.count > 0

        product_total *= component_zeta
        product_omit_root *= dominated.count
        component_rows.append(
            {
                "order": component.number_of_nodes(),
                "root_signature": (
                    (selected.cost, selected.count),
                    (dominated.cost, dominated.count),
                    (needs_parent.cost, needs_parent.count),
                ),
            }
        )

    assert product_total == reduced_zeta
    assert original_zeta == product_total - product_omit_root

    core = marked_support_core(graph)
    leaves = {
        vertex for vertex, degree in graph.degree() if degree == 1
    }
    supports = {
        vertex
        for vertex in graph.nodes()
        if any(neighbor in leaves for neighbor in graph.neighbors(vertex))
    }
    assert empty not in supports

    return {
        "original_profile": (original_gamma, original_zeta),
        "deletion_profile": (reduced_gamma, reduced_zeta),
        "component_count": len(component_rows),
        "components": component_rows,
        "product_total": product_total,
        "product_omit_root": product_omit_root,
        "marked_core_kind": core["kind"],
        "empty_is_unmarked": True,
    }


def _subdivided_star_family(
    max_order: int = MAX_BURNED_ORDER,
) -> list[dict[str, object]]:
    """Finite checks of the analytic one-empty family inside the burned range."""
    rows = []
    for arms in range(2, 7):
        graph = _subdivided_star(arms)
        if graph.number_of_nodes() > max_order:
            continue
        assert graph.number_of_nodes() == 2 * arms + 1 <= MAX_BURNED_ORDER

        profile = minimum_dominating_set_profile(graph)
        statuses = _statuses(graph)
        assert profile == (arms, 2**arms - 1)
        assert statuses[0] == "empty"
        assert all(
            status == "flexible"
            for vertex, status in statuses.items()
            if vertex != 0
        )
        assert not strong_supports(graph)

        reduced = graph.copy()
        reduced.remove_node(0)
        assert _forest_profile(reduced) == (arms, 2**arms)
        assert len(list(nx.connected_components(reduced))) == arms

        core = marked_support_core(graph)
        assert core["core_order"] == arms + 1
        assert core["mark_count"] == arms
        assert core["core_leaf_count"] == arms

        rows.append(
            {
                "arms": arms,
                "order": graph.number_of_nodes(),
                "profile": profile,
                "deletion_profile": _forest_profile(reduced),
                "gain": 1,
                "gain_ratio": f"{2**arms}/{2**arms - 1}",
                "core_max_degree": arms,
            }
        )
    return rows


def _p5_compensation_obstruction() -> dict[str, object]:
    """P5 proves that no universal one-vertex compensator can exist."""
    graph = _subdivided_star(2)
    assert nx.is_isomorphic(graph, path(5))
    assert minimum_dominating_set_profile(graph) == (2, 3)

    reduced = graph.copy()
    reduced.remove_node(0)
    assert _forest_profile(reduced) == (2, 4)

    order_five = generate_unlabeled_trees(5, 5)
    values = [minimum_dominating_set_profile(tree)[1] for tree in order_five]
    assert max(values) == 3
    assert values.count(3) == 1

    reconnected = path(4)
    assert minimum_dominating_set_profile(reconnected) == (2, 4)
    subdivided = path(5)
    assert minimum_dominating_set_profile(subdivided) == (2, 3)

    return {
        "tree": "P5 = subdivided 2-arm star",
        "profile": (2, 3),
        "deleted_forest": "2 P2",
        "deleted_forest_profile": (2, 4),
        "order_5_maximum": 3,
        "unique_order_5_extremizer": True,
        "forest_reconnection": {"tree": "P4", "profile": (2, 4)},
        "one_edge_subdivision": {"tree": "P5", "profile": (2, 3)},
        "conclusion": (
            "a strict d=1 Taletskii forest improvement need not admit any "
            "strict same-order compensation"
        ),
    }


def _p3_strong_banked_warning() -> dict[str, object]:
    """The two empty leaves of P3 cannot be paired as in the no-universal case."""
    graph = path(3)
    center = 1
    leaves = (0, 2)
    statuses = _statuses(graph)
    assert statuses[center] == "universal"
    assert all(statuses[leaf] == "empty" for leaf in leaves)
    assert minimum_dominating_set_profile(graph) == (1, 1)

    one_deleted = graph.copy()
    one_deleted.remove_node(leaves[0])
    assert minimum_dominating_set_profile(one_deleted) == (1, 2)

    both_deleted = graph.copy()
    both_deleted.remove_nodes_from(leaves)
    assert minimum_dominating_set_profile(both_deleted) == (1, 1)

    return {
        "tree": "P3",
        "profile": (1, 1),
        "one_leaf_deleted_profile": (1, 2),
        "both_leaves_deleted_profile": (1, 1),
        "conclusion": (
            "the no-universal hypothesis in the two-empty pairing theorem is essential"
        ),
    }


def _burned_rows(max_order: int) -> list[dict[str, object]]:
    rows = []
    for order in range(1, max_order + 1):
        trees = generate_unlabeled_trees(order, order)
        assert len(trees) == EXPECTED_TREE_COUNTS[order - 1]

        profiles = [minimum_dominating_set_profile(graph) for graph in trees]
        maximum = max(zeta for _, zeta in profiles)
        residual_count = 0
        one_empty_count = 0
        multiple_empty_count = 0
        residual_extremizer_count = 0
        one_empty_extremizer_count = 0
        checked_pairs = 0

        for graph, graph_profile in zip(trees, profiles, strict=True):
            statuses = _statuses(graph)
            if "universal" in statuses.values():
                continue
            empties = [
                vertex
                for vertex, status in statuses.items()
                if status == "empty"
            ]
            if not empties:
                continue

            assert not strong_supports(graph)
            residual_count += 1
            if graph_profile[1] == maximum:
                residual_extremizer_count += 1

            if len(empties) == 1:
                one_empty_count += 1
                if graph_profile[1] == maximum:
                    one_empty_extremizer_count += 1
                _unique_empty_record(graph, empties[0])
            else:
                multiple_empty_count += 1
                for left, right in combinations(empties, 2):
                    _check_pairing(graph, left, right)
                    checked_pairs += 1

        rows.append(
            {
                "order": order,
                "tree_count": len(trees),
                "residual_no_universal_empty_count": residual_count,
                "one_empty_count": one_empty_count,
                "multiple_empty_count": multiple_empty_count,
                "residual_extremizer_count": residual_extremizer_count,
                "one_empty_extremizer_count": one_empty_extremizer_count,
                "checked_empty_pairs": checked_pairs,
            }
        )
    return rows


def build_diagnosis(max_order: int = MAX_BURNED_ORDER) -> dict[str, object]:
    if not 1 <= max_order <= MAX_BURNED_ORDER:
        raise ValueError("TF21 diagnosis is restricted to burned orders 1--14")

    family = _subdivided_star_family(max_order=max_order)
    p5 = _p5_compensation_obstruction()
    p3 = _p3_strong_banked_warning()
    burned = _burned_rows(max_order)

    return {
        "analysis_id": "TF21-DIAG-0001",
        "classification": "PAIRING_SOLVES_MULTI_EMPTY_UNIQUE_EMPTY_REMAINS_UNBOUNDED",
        "fresh_data_consumed": False,
        "burned_data_boundary": {
            "exhaustive_orders": [1, max_order],
            "orders_at_least_15": "untouched",
        },
        "proved_structure": {
            "two_empty_pairing": (
                "in a no-universal tree, deleting any two distinct empty vertices "
                "gives an isolate-free forest of deficit two with the same gamma "
                "and strictly larger zeta"
            ),
            "extremizer_consequence": (
                "a no-universal exact order-extremizer has at most one empty vertex"
            ),
            "unique_empty_components": (
                "after deleting the sole empty vertex, every component has only "
                "flexible vertices; at its attachment root A and B tie at the "
                "component gamma and C is not cheaper"
            ),
            "unique_empty_formula": (
                "zeta(T)=product_i zeta(T_i)-product_i zeta^-(T_i,r_i)"
            ),
            "marked_core": (
                "the unique empty vertex is unmarked and internal in the marked "
                "support core"
            ),
        },
        "analytic_obstructions": {
            "subdivided_star_family_burned_checks": family,
            "p5_exact_compensation_obstruction": p5,
            "p3_strong_banked_warning": p3,
            "connector_vertex": (
                "for k disjoint P2 components, a single fresh connector adjacent "
                "to one endpoint in every component recreates the subdivided "
                "k-arm star and loses exactly the all-leaves choice"
            ),
        },
        "burned_residual_rows": burned,
        "experiment_decision": {
            "new_experiment_frozen": False,
            "order_15_prediction_frozen": False,
            "order_15_consumed": False,
            "candidate_ids_allocated": [],
            "candidate_registry_changed": False,
            "experiment_registry_changed": False,
            "next_candidate_id": "TF-001158",
            "default_invariant_changed": False,
            "reason": (
                "pairing closes every residual configuration with at least two "
                "empty vertices, but the unique-empty class has an exact "
                "product-minus-product decomposition with unbounded marked-core "
                "degree; P5 is already an exact extremizer with a strict d=1 "
                "deletion gain, so no universal same-order d=1 compensator exists"
            ),
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
