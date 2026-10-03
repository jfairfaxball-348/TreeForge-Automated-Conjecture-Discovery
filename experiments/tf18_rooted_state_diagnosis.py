#!/usr/bin/env python3
"""TF18 rooted-state diagnosis using only burned orders 1--14.

The mathematical replacement preorder used here is defined before any census:
two rooted interfaces are projectively comparable only when their finite-state
costs differ by one common additive constant.  State counts are then compared
coordinatewise.  The common cost shift preserves every boundary-state tie.

This script never constructs a tree of order 15 or larger.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import TypeAlias

import networkx as nx

from treeforge.invariants.minimum_dominating_sets import (
    MinCount,
    rooted_minimum_dominating_set_states,
)
from treeforge.invariants.registry import default_registry
from treeforge.registry.candidate_registry import CandidateRegistry
from treeforge.trees.canonical import generate_unlabeled_trees

CANDIDATES = Path("data/registry/candidates.jsonl")
EXPERIMENTS = Path("data/registry/experiments.jsonl")
MAX_BURNED_ORDER = 14

StateTriple: TypeAlias = tuple[MinCount, MinCount, MinCount]
CostShape: TypeAlias = tuple[int | None, int | None, int | None]
CountVector: TypeAlias = tuple[int, int, int]
ProjectiveInterface: TypeAlias = tuple[CostShape, CountVector]

EXPECTED_TREE_COUNTS = [1, 1, 1, 2, 3, 6, 11, 23, 47, 106, 235, 551, 1301, 3159]
EXPECTED_STATE_STATS = {
    1: (1, 1, 1, 1, 1),
    2: (1, 1, 1, 1, 1),
    3: (2, 2, 2, 2, 2),
    4: (4, 4, 4, 4, 4),
    5: (9, 9, 7, 8, 9),
    6: (18, 18, 9, 11, 16),
    7: (38, 38, 11, 18, 27),
    8: (72, 70, 14, 22, 41),
    9: (144, 139, 18, 31, 54),
    10: (278, 264, 21, 44, 83),
    11: (533, 501, 24, 52, 101),
    12: (1035, 965, 28, 74, 154),
    13: (1977, 1827, 33, 80, 174),
    14: (3782, 3474, 37, 119, 268),
}


def _jsonl(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def validate_repository_boundary() -> None:
    """Assert the TF17 scientific boundary before any burned-data diagnosis."""
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
            (
                "TF5",
                "TF6",
                "TF7",
                "TF8",
                "TF9",
                "TF10",
                "TF11",
                "TF12",
                "TF13",
                "TF14",
                "TF15",
                "TF16",
                "TF17",
                "TF18",
            )
        )
        for row in experiments
    )

    names = set(default_registry().names())
    assert "minimum_dominating_set_count" not in names


def _signature_key(states: StateTriple) -> tuple[tuple[int | None, int], ...]:
    return tuple((state.cost, state.count) for state in states)


def _projective_interface(states: StateTriple) -> ProjectiveInterface:
    """Normalize a signature by subtracting the always-finite A cost exactly."""
    selected_cost = states[0].cost
    if selected_cost is None:
        raise AssertionError("state A is always feasible")
    deltas: CostShape = tuple(
        None if state.cost is None else state.cost - selected_cost
        for state in states
    )
    counts: CountVector = tuple(state.count for state in states)
    return deltas, counts


def _weakly_dominates(left: ProjectiveInterface, right: ProjectiveInterface) -> bool:
    """Same projective costs, no smaller state count, and strict somewhere."""
    left_shape, left_counts = left
    right_shape, right_counts = right
    return (
        left_shape == right_shape
        and all(a >= b for a, b in zip(left_counts, right_counts, strict=True))
        and any(a > b for a, b in zip(left_counts, right_counts, strict=True))
    )


def _strictly_dominates_every_feasible_state(
    left: ProjectiveInterface,
    right: ProjectiveInterface,
) -> bool:
    """Return whether every feasible boundary-state count is strictly larger."""
    left_shape, left_counts = left
    right_shape, right_counts = right
    if left_shape != right_shape:
        return False
    feasible = [index for index, delta in enumerate(right_shape) if delta is not None]
    return bool(feasible) and all(left_counts[index] > right_counts[index] for index in feasible)


def _global_profile(states: StateTriple) -> tuple[int, int]:
    selected, dominated, _ = states
    feasible = [state for state in (selected, dominated) if state.cost is not None]
    minimum_cost = min(state.cost for state in feasible)
    return (
        minimum_cost,
        sum(state.count for state in feasible if state.cost == minimum_cost),
    )


def _frontier_counts(
    interfaces: set[ProjectiveInterface],
) -> tuple[int, int]:
    by_shape: dict[CostShape, list[ProjectiveInterface]] = defaultdict(list)
    for interface in interfaces:
        by_shape[interface[0]].append(interface)

    weak_undominated = 0
    strict_survivors = 0
    for peers in by_shape.values():
        for interface in peers:
            if not any(
                _weakly_dominates(other, interface)
                for other in peers
                if other != interface
            ):
                weak_undominated += 1
            if not any(
                _strictly_dominates_every_feasible_state(other, interface)
                for other in peers
                if other != interface
            ):
                strict_survivors += 1
    return weak_undominated, strict_survivors


def _coordinatewise_counterexample() -> dict[str, object]:
    """Burned order-8 counterexample to naive coordinatewise cost dominance."""
    # R is the spider with arm lengths 1, 2, 4, rooted at the internal
    # vertex on its length-2 arm.
    r_graph = nx.Graph(
        [(1, 0), (1, 2), (1, 4), (0, 5), (2, 3), (5, 6), (6, 7)]
    )
    r_root = 2

    # S is the spider with arm lengths 1, 1, 1, 4, rooted at the
    # penultimate vertex of its length-4 arm.
    s_graph = nx.Graph(
        [(1, 0), (1, 2), (0, 4), (2, 3), (4, 5), (4, 6), (4, 7)]
    )
    s_root = 2

    r_states = rooted_minimum_dominating_set_states(r_graph, r_root)
    s_states = rooted_minimum_dominating_set_states(s_graph, s_root)

    assert _signature_key(r_states) == ((3, 1), (3, 1), (None, 0))
    assert _signature_key(s_states) == ((2, 1), (3, 2), (None, 0))
    assert _global_profile(r_states) == (3, 2)
    assert _global_profile(s_states) == (2, 1)

    for r_state, s_state in zip(r_states, s_states, strict=True):
        if r_state.cost is None:
            assert s_state.cost is None
            continue
        assert s_state.cost is not None
        assert s_state.cost <= r_state.cost
        assert s_state.count >= r_state.count

    return {
        "order": 8,
        "R_description": "spider arm lengths (1,2,4), root internal on the length-2 arm",
        "S_description": "spider arm lengths (1,1,1,4), root penultimate on the length-4 arm",
        "R_signature": _signature_key(r_states),
        "S_signature": _signature_key(s_states),
        "R_root_profile": _global_profile(r_states),
        "S_root_profile": _global_profile(s_states),
        "conclusion": (
            "coordinatewise no-larger state costs and no-smaller state counts do not "
            "preserve zeta: lowering only A destroys the A/B optimum tie"
        ),
    }


def _diagnose_order(order: int) -> dict[str, object]:
    trees = generate_unlabeled_trees(order, order)
    assert len(trees) == EXPECTED_TREE_COUNTS[order - 1]
    assert all(graph.number_of_nodes() == order for graph in trees)

    exact_signatures: set[tuple[tuple[int | None, int], ...]] = set()
    interfaces: set[ProjectiveInterface] = set()
    cost_shapes: set[CostShape] = set()

    maximum_zeta = -1
    extremizer_interfaces: set[ProjectiveInterface] = set()

    for graph in trees:
        tree_interfaces: set[ProjectiveInterface] = set()
        tree_zeta: int | None = None
        for root in graph.nodes():
            states = rooted_minimum_dominating_set_states(graph, root)
            exact_signatures.add(_signature_key(states))
            interface = _projective_interface(states)
            interfaces.add(interface)
            cost_shapes.add(interface[0])
            tree_interfaces.add(interface)
            if tree_zeta is None:
                _, tree_zeta = _global_profile(states)

        if tree_zeta is None:
            raise AssertionError("a nonempty tree has a rooted evaluation")
        if tree_zeta > maximum_zeta:
            maximum_zeta = tree_zeta
            extremizer_interfaces = set(tree_interfaces)
        elif tree_zeta == maximum_zeta:
            extremizer_interfaces.update(tree_interfaces)

    weak_undominated, strict_survivors = _frontier_counts(interfaces)
    expected = EXPECTED_STATE_STATS[order]
    observed = (
        len(exact_signatures),
        len(interfaces),
        len(cost_shapes),
        weak_undominated,
        strict_survivors,
    )
    assert observed == expected

    weak_front = {
        interface
        for interface in interfaces
        if not any(
            _weakly_dominates(other, interface)
            for other in interfaces
            if other != interface
        )
    }

    finite_b_deltas = [shape[1] for shape in cost_shapes if shape[1] is not None]
    finite_c_deltas = [shape[2] for shape in cost_shapes if shape[2] is not None]

    return {
        "order": order,
        "tree_count": len(trees),
        "rooted_evaluations": order * len(trees),
        "exact_signature_count": len(exact_signatures),
        "projective_interface_count": len(interfaces),
        "normalized_cost_shape_count": len(cost_shapes),
        "weak_projective_undominated_count": weak_undominated,
        "strict_projective_survivor_count": strict_survivors,
        "extremal_zeta": maximum_zeta,
        "extremizer_root_interface_count": len(extremizer_interfaces),
        "extremizer_root_interfaces_on_weak_front": sum(
            interface in weak_front for interface in extremizer_interfaces
        ),
        "delta_B_range": (
            [min(finite_b_deltas), max(finite_b_deltas)]
            if finite_b_deltas
            else None
        ),
        "delta_C_range": (
            [min(finite_c_deltas), max(finite_c_deltas)]
            if finite_c_deltas
            else None
        ),
    }


def build_diagnosis(max_order: int = MAX_BURNED_ORDER) -> dict[str, object]:
    if not 1 <= max_order <= MAX_BURNED_ORDER:
        raise ValueError("TF18 diagnosis is restricted to burned orders 1--14")

    rows = [_diagnose_order(order) for order in range(1, max_order + 1)]
    return {
        "analysis_id": "TF18-DIAG-0001",
        "classification": "USEFUL_PROJECTIVE_DOMINANCE_NO_FINITE_GRAMMAR",
        "fresh_data_consumed": False,
        "burned_data_boundary": {
            "exhaustive_orders": [1, max_order],
            "orders_at_least_15": "untouched",
        },
        "proved_preorder": {
            "normalization": (
                "subtract the A-state cost from every finite state cost; retain "
                "infeasibility and all exact integer state counts"
            ),
            "weak_projective_dominance": (
                "same normalized cost shape and coordinatewise no-smaller state counts"
            ),
            "context_consequence": (
                "under pendant substitution every global boundary alternative receives "
                "one common cost shift, so all optimum ties are preserved and zeta cannot decrease"
            ),
            "strict_elimination": (
                "if every feasible state count is strictly larger and gadget order is unchanged, "
                "zeta strictly increases in every pendant context"
            ),
        },
        "naive_coordinatewise_dominance_counterexample": _coordinatewise_counterexample(),
        "rooted_state_rows": rows,
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
                "projective dominance is rigorous but does not reduce the exact rooted interface "
                "space to a proved finite grammar; published terminal/S-decomposition restrictions "
                "depend on different extremal objectives and do not supply the missing completeness theorem"
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
