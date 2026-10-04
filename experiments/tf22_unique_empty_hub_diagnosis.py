#!/usr/bin/env python3
"""TF22 diagnostics for the unique-empty hub obstruction.

This module is theorem-support machinery only.  It uses exclusively the burned
orders 1--14 and refuses every larger exhaustive order.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import NamedTuple

import networkx as nx

from experiments.tf20_global_compensation_diagnosis import strong_supports
from experiments.tf21_one_vertex_compensation_diagnosis import vertex_status
from treeforge.invariants.minimum_dominating_sets import (
    minimum_dominating_set_profile,
    rooted_minimum_dominating_set_states,
)
from treeforge.invariants.registry import default_registry
from treeforge.registry.candidate_registry import CandidateRegistry
from treeforge.trees.canonical import generate_unlabeled_trees

CANDIDATES = Path("data/registry/candidates.jsonl")
EXPERIMENTS = Path("data/registry/experiments.jsonl")
MAX_BURNED_ORDER = 14
EXPECTED_TREE_COUNTS = [1, 1, 1, 2, 3, 6, 11, 23, 47, 106, 235, 551, 1301, 3159]


class RootPair(NamedTuple):
    zeta: int
    alpha: int
    beta: int


def _jsonl(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def validate_repository_boundary() -> None:
    """Assert that TF22 begins from the frozen TF21 scientific boundary."""
    assert CandidateRegistry(CANDIDATES).next_id() == "TF-001158"

    experiments = _jsonl(EXPERIMENTS)
    scientific = [
        row for row in experiments if str(row.get("experiment_id", "")).startswith("TF")
    ]
    assert scientific
    assert scientific[-1]["experiment_id"] == "TF4-0001"
    assert all(
        not str(row.get("experiment_id", "")).startswith(
            tuple(f"TF{index}" for index in range(5, 23))
        )
        for row in experiments
    )
    assert "minimum_dominating_set_count" not in set(default_registry().names())


def _forest_profile(forest: nx.Graph) -> tuple[int, int]:
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


def _is_critical(graph: nx.Graph, vertex: object) -> bool:
    """Return whether deleting vertex lowers gamma by one."""
    gamma, _ = minimum_dominating_set_profile(graph)
    reduced = graph.copy()
    reduced.remove_node(vertex)
    reduced_gamma, _ = _forest_profile(reduced)
    return reduced_gamma == gamma - 1


def _all_flexible(graph: nx.Graph) -> bool:
    return all(vertex_status(graph, vertex) == "flexible" for vertex in graph.nodes())


def _root_pair(graph: nx.Graph, root: object) -> RootPair:
    gamma, zeta = minimum_dominating_set_profile(graph)
    selected, dominated, needs_parent = rooted_minimum_dominating_set_states(graph, root)
    assert selected.cost == dominated.cost == gamma
    assert selected.count > 0 and dominated.count > 0
    assert needs_parent.cost is None or needs_parent.cost >= gamma - 1
    return RootPair(zeta=zeta, alpha=selected.count, beta=dominated.count)


def _stable_root_pair(graph: nx.Graph, root: object) -> RootPair:
    gamma, _ = minimum_dominating_set_profile(graph)
    selected, dominated, needs_parent = rooted_minimum_dominating_set_states(graph, root)
    assert selected.cost == dominated.cost == gamma
    assert needs_parent.cost is None or needs_parent.cost >= gamma
    return _root_pair(graph, root)


def _critical_root_data(graph: nx.Graph, root: object) -> tuple[RootPair, int]:
    gamma, _ = minimum_dominating_set_profile(graph)
    selected, dominated, needs_parent = rooted_minimum_dominating_set_states(graph, root)
    assert selected.cost == dominated.cost == gamma
    assert needs_parent.cost == gamma - 1
    return _root_pair(graph, root), needs_parent.count


def _w_tree(left_arms: int, right_arms: int) -> tuple[nx.Graph, int]:
    """Return Taletskii's W_(a,b) and one support root on the left side."""
    if left_arms < 1 or right_arms < 1:
        raise ValueError("TF22 uses positive W parameters")

    graph = nx.Graph()
    left, middle, right = 0, 1, 2
    graph.add_edges_from(((left, middle), (middle, right)))
    next_vertex = 3
    left_root = -1

    for index in range(left_arms):
        support = next_vertex
        leaf = next_vertex + 1
        next_vertex += 2
        graph.add_edges_from(((left, support), (support, leaf)))
        if index == 0:
            left_root = support

    for _ in range(right_arms):
        support = next_vertex
        leaf = next_vertex + 1
        next_vertex += 2
        graph.add_edges_from(((right, support), (support, leaf)))

    return graph, left_root


def _w_formula_record(left_arms: int, right_arms: int) -> dict[str, object]:
    graph, root = _w_tree(left_arms, right_arms)
    arm_sum = left_arms + right_arms
    expected_zeta = 3 * 2**arm_sum - 2**left_arms - 2**right_arms
    expected_alpha = 3 * 2 ** (arm_sum - 1) - 2 ** (left_arms - 1)

    gamma, zeta = minimum_dominating_set_profile(graph)
    pair = _stable_root_pair(graph, root)
    assert _all_flexible(graph)
    assert gamma == arm_sum + 1
    assert zeta == expected_zeta
    assert pair.alpha == expected_alpha
    assert pair.beta == expected_zeta - expected_alpha

    return {
        "parameters": [left_arms, right_arms],
        "order": graph.number_of_nodes(),
        "gamma": gamma,
        "root_pair": pair._asdict(),
        "formula": {"zeta": expected_zeta, "alpha": expected_alpha},
    }


def _path_formula_record(m: int) -> dict[str, object]:
    """Check the P_(3m+1) formulas used in the rerooting obstruction."""
    if not 1 <= m <= 4:
        raise ValueError("burned path check is restricted to m=1..4")

    graph = nx.path_graph(3 * m + 1)
    gamma, zeta = minimum_dominating_set_profile(graph)
    expected_zeta = (m * m + 5 * m + 2) // 2
    assert gamma == m + 1
    assert zeta == expected_zeta
    assert _all_flexible(graph)

    stable_root = 1
    stable_pair = _stable_root_pair(graph, stable_root)
    assert stable_pair.beta == m + 1

    record: dict[str, object] = {
        "m": m,
        "order": graph.number_of_nodes(),
        "profile": [gamma, zeta],
        "stable_v2_pair": stable_pair._asdict(),
    }

    if m >= 2:
        critical_root = 3
        critical_pair, chi = _critical_root_data(graph, critical_root)
        expected_critical_beta = (m * m + m + 2) // 2
        assert critical_pair.beta == expected_critical_beta
        assert chi == 1

        context_root = 2
        context_pair = _stable_root_pair(graph, context_root)
        assert context_pair.alpha == 2
        assert context_pair.beta == zeta - 2

        reroot_delta_with_p2 = stable_pair.beta - critical_pair.beta + 2 * chi
        assert reroot_delta_with_p2 == (-m * m + m + 4) // 2

        record.update(
            {
                "critical_v4_pair": critical_pair._asdict(),
                "critical_v4_c_count": chi,
                "stable_v3_pair": context_pair._asdict(),
                "critical_reroot_delta_with_p2": reroot_delta_with_p2,
            }
        )

    return record


def _hub_objective(component_pairs: list[RootPair]) -> int:
    total = 1
    omitted = 1
    for pair in component_pairs:
        total *= pair.zeta
        omitted *= pair.beta
    return total - omitted


def _path_hub(m: int) -> tuple[nx.Graph, int]:
    """Build a burned member of the P_(3m+1)+P2 hub family."""
    if m < 1 or 3 * m + 4 > MAX_BURNED_ORDER:
        raise ValueError("TF22 path-hub generation is restricted to burned orders")
    component_order = 3 * m + 1
    graph = nx.disjoint_union(nx.path_graph(component_order), nx.path_graph(2))
    hub = graph.number_of_nodes()
    graph.add_node(hub)
    graph.add_edge(hub, 1)
    graph.add_edge(hub, component_order)
    return graph, hub


def _best_single_hub_rewire(graph: nx.Graph, hub: object) -> int:
    original = minimum_dominating_set_profile(graph)[1]
    best = original
    reduced = graph.copy()
    reduced.remove_node(hub)
    for old_root in list(graph.neighbors(hub)):
        component = nx.node_connected_component(reduced, old_root)
        for new_root in component:
            if new_root == old_root:
                continue
            rewired = graph.copy()
            rewired.remove_edge(hub, old_root)
            rewired.add_edge(hub, new_root)
            assert nx.is_tree(rewired)
            best = max(best, minimum_dominating_set_profile(rewired)[1])
    return best


def _path_hub_rewire_record(m: int) -> dict[str, object]:
    """Check a burned member of the analytic no-single-rewire family."""
    graph, hub = _path_hub(m)
    component_zeta = (m * m + 5 * m + 2) // 2
    stable_beta = m + 1
    best_critical_alpha = ((m + 2) ** 2) // 4
    best_critical_beta = component_zeta - best_critical_alpha
    critical_margin = best_critical_beta - stable_beta
    expected_zeta = 2 * component_zeta - stable_beta

    assert vertex_status(graph, hub) == "empty"
    assert all(
        vertex_status(graph, vertex) == "flexible"
        for vertex in graph.nodes()
        if vertex != hub
    )
    assert minimum_dominating_set_profile(graph)[1] == expected_zeta

    best_rewire = _best_single_hub_rewire(graph, hub)
    if m >= 3:
        assert critical_margin > 2
        assert best_rewire == expected_zeta

    return {
        "m": m,
        "order": graph.number_of_nodes(),
        "component_zeta": component_zeta,
        "best_stable_beta": stable_beta,
        "best_critical_alpha": best_critical_alpha,
        "best_critical_beta": best_critical_beta,
        "critical_margin": critical_margin,
        "hub_zeta": expected_zeta,
        "best_single_rewire_zeta": best_rewire,
        "strict_single_rewire_exists": best_rewire > expected_zeta,
    }


def _w_balance_reversal() -> dict[str, object]:
    """Check the exact two-coordinate reversal at the smallest burned q=2."""
    balanced_graph, balanced_root = _w_tree(2, 2)
    unbalanced_graph, unbalanced_root = _w_tree(1, 3)
    balanced = _stable_root_pair(balanced_graph, balanced_root)
    unbalanced = _stable_root_pair(unbalanced_graph, unbalanced_root)

    assert balanced == RootPair(40, 22, 18)
    assert unbalanced == RootPair(38, 23, 15)

    p2 = nx.path_graph(2)
    p2_pair = _stable_root_pair(p2, 0)
    assert p2_pair == RootPair(2, 1, 1)

    p7 = nx.path_graph(7)
    p7_pair = _stable_root_pair(p7, 2)
    assert p7_pair == RootPair(8, 2, 6)

    p2_delta = _hub_objective([unbalanced, p2_pair]) - _hub_objective(
        [balanced, p2_pair]
    )
    p7_delta = _hub_objective([unbalanced, p7_pair]) - _hub_objective(
        [balanced, p7_pair]
    )
    assert p2_delta == -1
    assert p7_delta == 2

    return {
        "balanced": balanced._asdict(),
        "unbalanced": unbalanced._asdict(),
        "p2_context": p2_pair._asdict(),
        "p7_v3_context": p7_pair._asdict(),
        "unbalanced_minus_balanced": {"with_p2": p2_delta, "with_p7_v3": p7_delta},
        "note": (
            "only component signatures are combined algebraically; no tree of "
            "order 15 or larger is generated"
        ),
    }


def _strong_banked_residual(graph: nx.Graph) -> bool:
    supports = strong_supports(graph)
    if len(supports) != 1:
        return False
    support = supports[0]
    statuses = {vertex: vertex_status(graph, vertex) for vertex in graph.nodes()}
    universals = {vertex for vertex, state in statuses.items() if state == "universal"}
    empties = {vertex for vertex, state in statuses.items() if state == "empty"}
    private_leaves = {
        neighbor
        for neighbor in graph.neighbors(support)
        if graph.degree(neighbor) == 1
    }
    return (
        universals == {support}
        and len(private_leaves) == 2
        and empties == private_leaves
    )


def _burned_rows(max_order: int) -> list[dict[str, object]]:
    rows = []
    for order in range(1, max_order + 1):
        trees = generate_unlabeled_trees(order, order)
        assert len(trees) == EXPECTED_TREE_COUNTS[order - 1]
        profiles = [minimum_dominating_set_profile(graph) for graph in trees]
        maximum = max(zeta for _, zeta in profiles)

        all_flexible_count = 0
        unique_empty_count = 0
        unique_empty_extremizer_count = 0
        strong_banked_count = 0
        strong_banked_extremizer_count = 0
        rooted_pairs: set[tuple[int, int, int, bool]] = set()

        for graph, (_, zeta) in zip(trees, profiles, strict=True):
            statuses = {
                vertex: vertex_status(graph, vertex) for vertex in graph.nodes()
            }

            if set(statuses.values()) == {"flexible"}:
                all_flexible_count += 1
                gamma, _ = minimum_dominating_set_profile(graph)
                for vertex in graph.nodes():
                    selected, dominated, needs_parent = (
                        rooted_minimum_dominating_set_states(graph, vertex)
                    )
                    critical_by_state = needs_parent.cost == gamma - 1
                    assert critical_by_state == _is_critical(graph, vertex)
                    rooted_pairs.add(
                        (zeta, selected.count, dominated.count, critical_by_state)
                    )

            if "universal" not in statuses.values():
                empties = [
                    vertex
                    for vertex, state in statuses.items()
                    if state == "empty"
                ]
                if len(empties) == 1:
                    unique_empty_count += 1
                    empty = empties[0]
                    reduced = graph.copy()
                    reduced.remove_node(empty)
                    for vertices in nx.connected_components(reduced):
                        component = reduced.subgraph(vertices).copy()
                        root = next(
                            neighbor
                            for neighbor in graph.neighbors(empty)
                            if neighbor in component
                        )
                        assert _all_flexible(component)
                        component_gamma, _ = minimum_dominating_set_profile(component)
                        _, _, needs_parent = rooted_minimum_dominating_set_states(
                            component, root
                        )
                        assert needs_parent.cost is None or needs_parent.cost >= component_gamma
                    if zeta == maximum:
                        unique_empty_extremizer_count += 1

            if _strong_banked_residual(graph):
                strong_banked_count += 1
                if zeta == maximum:
                    strong_banked_extremizer_count += 1

        rows.append(
            {
                "order": order,
                "tree_count": len(trees),
                "maximum_zeta_burned_only": maximum,
                "all_flexible_count": all_flexible_count,
                "distinct_all_flexible_root_records": len(rooted_pairs),
                "unique_empty_count": unique_empty_count,
                "unique_empty_extremizer_count": unique_empty_extremizer_count,
                "strong_banked_residual_count": strong_banked_count,
                "strong_banked_extremizer_count": strong_banked_extremizer_count,
            }
        )
    return rows


def build_diagnosis(max_order: int = MAX_BURNED_ORDER) -> dict[str, object]:
    if not 1 <= max_order <= MAX_BURNED_ORDER:
        raise ValueError("TF22 diagnosis is restricted to burned orders 1--14")

    w_checks = []
    for left_arms in range(1, 6):
        for right_arms in range(1, 6):
            order = 2 * (left_arms + right_arms) + 3
            if order <= max_order:
                w_checks.append(_w_formula_record(left_arms, right_arms))

    path_checks = [
        _path_formula_record(m)
        for m in range(1, 5)
        if 3 * m + 1 <= max_order
    ]
    path_hub_rewire_check = (
        _path_hub_rewire_record(3) if max_order >= 13 else None
    )
    burned = _burned_rows(max_order)

    return {
        "analysis_id": "TF22-DIAG-0001",
        "classification": "GLOBAL_HUB_OBJECTIVE_REMAINS_CONTEXT_SENSITIVE",
        "fresh_data_consumed": False,
        "burned_data_boundary": {
            "exhaustive_orders": [1, max_order],
            "orders_at_least_15": "untouched",
        },
        "theorem_regressions": {
            "all_flexible_criticality": (
                "on every burned all-flexible tree, root C has cost gamma-1 "
                "exactly at domination-critical vertices"
            ),
            "unique_empty_stable_roots": (
                "every burned unique-empty deletion component is all-flexible "
                "and every actual attachment root is stable"
            ),
            "w_root_pair_formula_checks": w_checks,
            "path_reroot_formula_checks": path_checks,
            "path_hub_no_single_rewire_check": path_hub_rewire_check,
            "w_balance_context_reversal": _w_balance_reversal(),
        },
        "burned_rows": burned,
        "burned_observations_not_promoted_to_theorems": {
            "unique_empty_extremizer_orders": [
                row["order"] for row in burned if row["unique_empty_extremizer_count"]
            ],
            "strong_banked_extremizer_orders": [
                row["order"] for row in burned if row["strong_banked_extremizer_count"]
            ],
            "all_flexible_counts": [row["all_flexible_count"] for row in burned],
        },
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
                "gamma-excellent structure identifies the flexible components, "
                "but exact rooted count pairs remain genuinely two-dimensional "
                "and context-sensitive; the strong-banked residue also remains "
                "unclosed, so the prospective TF22 freeze conditions fail"
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
