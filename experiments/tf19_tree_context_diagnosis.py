#!/usr/bin/env python3
"""TF19 tree-context diagnosis using only burned orders 1--14.

The theorem-facing definitions in this module come before the burned census.
A one-hole tree context is the component remaining after deleting a pendant
rooted subtree, rooted at the attachment parent.  Its exact boundary message is
computed from the same A/B/C min-plus/count algebra as TF17.

No function in this module constructs an unlabeled tree of order 15 or larger.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import TypeAlias

import networkx as nx

from treeforge.invariants.minimum_dominating_sets import (
    INFEASIBLE,
    MinCount,
    minimum_dominating_set_profile,
    rooted_minimum_dominating_set_states,
)
from treeforge.invariants.registry import default_registry
from treeforge.registry.candidate_registry import CandidateRegistry
from treeforge.trees.canonical import generate_unlabeled_trees
from treeforge.trees.families import path, star

CANDIDATES = Path("data/registry/candidates.jsonl")
EXPERIMENTS = Path("data/registry/experiments.jsonl")
MAX_BURNED_ORDER = 14
STATE_NAMES = ("A", "B", "C")

StateTriple: TypeAlias = tuple[MinCount, MinCount, MinCount]
FaceProfile: TypeAlias = tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]
ContextInterface: TypeAlias = tuple[FaceProfile, tuple[int, int, int]]

# Normalized outside cost patterns proved for genuine tree contexts.
CONTEXT_COST_PATTERNS: tuple[tuple[int, int, int], ...] = (
    (0, 0, 0),
    (0, 0, 1),
    (0, 1, 1),
)

EXPECTED_TREE_COUNTS = [1, 1, 1, 2, 3, 6, 11, 23, 47, 106, 235, 551, 1301, 3159]


def _jsonl(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def validate_repository_boundary() -> None:
    """Assert the TF18 boundary before any burned-data diagnosis."""
    assert CandidateRegistry(CANDIDATES).next_id() == "TF-001158"

    experiments = _jsonl(EXPERIMENTS)
    scientific = [
        row for row in experiments if str(row.get("experiment_id", "")).startswith("TF")
    ]
    assert scientific
    assert scientific[-1]["experiment_id"] == "TF4-0001"
    assert all(
        not str(row.get("experiment_id", "")).startswith(
            tuple(f"TF{index}" for index in range(5, 20))
        )
        for row in experiments
    )

    assert "minimum_dominating_set_count" not in set(default_registry().names())


def _minimum(*states: MinCount) -> MinCount:
    feasible = [state for state in states if state.cost is not None]
    if not feasible:
        return INFEASIBLE
    cost = min(state.cost for state in feasible)
    return MinCount(cost, sum(state.count for state in feasible if state.cost == cost))


def context_message(outside_states: StateTriple) -> StateTriple:
    """Return exact outside conditional messages (K_A,K_B,K_C).

    The outside tree is rooted at the attachment parent p before the hole is
    filled.  If the inserted gadget root is in state A, it may dominate p, so
    the outside may close as A, B, or C.  State B does not dominate p and does
    not need p, so the outside closes as A or B.  State C requires p selected,
    so the outside is forced to A.
    """
    outside_a, outside_b, outside_c = outside_states
    return (
        _minimum(outside_a, outside_b, outside_c),
        _minimum(outside_a, outside_b),
        outside_a,
    )


def normalized_context_cost_pattern(message: StateTriple) -> tuple[int, int, int]:
    costs = [state.cost for state in message]
    if any(cost is None for cost in costs):
        raise AssertionError("every one-hole tree-context boundary state is compatible")
    base = costs[0]
    assert base is not None
    return tuple(int(cost - base) for cost in costs if cost is not None)


def _normalized_state_costs(states: StateTriple) -> tuple[int | None, int | None, int | None]:
    selected_cost = states[0].cost
    if selected_cost is None:
        raise AssertionError("state A is always feasible")
    return tuple(
        None if state.cost is None else state.cost - selected_cost
        for state in states
    )


def context_face_profile(states: StateTriple) -> FaceProfile:
    """Return the three lower faces exposed by genuine tree contexts."""
    deltas = _normalized_state_costs(states)
    faces: list[tuple[int, ...]] = []
    for outside_delta in CONTEXT_COST_PATTERNS:
        scores = [
            None if delta is None else delta + outside_delta[index]
            for index, delta in enumerate(deltas)
        ]
        finite = [score for score in scores if score is not None]
        minimum = min(finite)
        faces.append(
            tuple(index for index, score in enumerate(scores) if score == minimum)
        )
    return tuple(faces)  # type: ignore[return-value]


def context_interface(states: StateTriple) -> ContextInterface:
    """Projective tree-context quotient: lower faces plus observable counts."""
    faces = context_face_profile(states)
    active = set().union(*(set(face) for face in faces))
    counts = tuple(
        state.count if index in active else 0
        for index, state in enumerate(states)
    )
    return faces, counts  # type: ignore[return-value]


def _projective_interface(
    states: StateTriple,
) -> tuple[tuple[int | None, int | None, int | None], tuple[int, int, int]]:
    return _normalized_state_costs(states), tuple(state.count for state in states)


def _context_weakly_dominates(left: ContextInterface, right: ContextInterface) -> bool:
    left_faces, left_counts = left
    right_faces, right_counts = right
    if left_faces != right_faces:
        return False
    active = set().union(*(set(face) for face in right_faces))
    return (
        all(left_counts[index] >= right_counts[index] for index in active)
        and any(left_counts[index] > right_counts[index] for index in active)
    )


def _context_strict_in_every_pattern(
    left: ContextInterface,
    right: ContextInterface,
) -> bool:
    """Strictly improve the weighted optimum for every realizable cost pattern."""
    left_faces, left_counts = left
    right_faces, right_counts = right
    if left_faces != right_faces:
        return False
    if any(left_counts[index] < right_counts[index] for index in set().union(*map(set, right_faces))):
        return False
    return all(
        any(left_counts[index] > right_counts[index] for index in face)
        for face in right_faces
    )


def compose_profile(outside_states: StateTriple, gadget_states: StateTriple) -> tuple[int, int]:
    """Close a one-hole context by the exact conditional-message formula."""
    message = context_message(outside_states)
    alternatives: list[MinCount] = []
    for outside, inside in zip(message, gadget_states, strict=True):
        if outside.cost is None or inside.cost is None:
            continue
        alternatives.append(
            MinCount(outside.cost + inside.cost, outside.count * inside.count)
        )
    result = _minimum(*alternatives)
    if result.cost is None:
        raise AssertionError("a filled tree context must have a dominating set")
    return result.cost, result.count


def _canonical_contexts() -> list[dict[str, object]]:
    expected = [
        (((0, 1), (1, 1), (1, 1)), (0, 1, 1)),
        (((1, 2), (1, 2), (1, 1)), (0, 0, 0)),
        (((1, 2), (1, 1), (2, 2)), (0, 0, 1)),
    ]
    rows = []
    for order, (expected_message, expected_pattern) in enumerate(expected, start=1):
        outside = path(order)
        states = rooted_minimum_dominating_set_states(outside, 0)
        message = context_message(states)
        serialized = tuple((state.cost, state.count) for state in message)
        pattern = normalized_context_cost_pattern(message)
        assert serialized == expected_message
        assert pattern == expected_pattern
        rows.append(
            {
                "outside_path_order": order,
                "message": serialized,
                "normalized_cost_pattern": pattern,
            }
        )
    return rows


def _context_equivalence_examples() -> dict[str, object]:
    smaller_star = star(2)
    larger_star = star(3)
    r_states = rooted_minimum_dominating_set_states(smaller_star, 0)
    s_states = rooted_minimum_dominating_set_states(larger_star, 0)
    assert _projective_interface(r_states) != _projective_interface(s_states)
    assert context_interface(r_states) == context_interface(s_states)

    path_witnesses = []
    interfaces = set()
    for k in range(1, 5):
        graph = path(3 * k)
        states = rooted_minimum_dominating_set_states(graph, 0)
        expected = (
            MinCount(k + 1, k * (k + 3) // 2),
            MinCount(k, 1),
            MinCount(k, k),
        )
        assert states == expected
        interface = context_interface(states)
        interfaces.add(interface)
        path_witnesses.append(
            {
                "k": k,
                "order": 3 * k,
                "signature": tuple((state.cost, state.count) for state in states),
                "context_interface": interface,
            }
        )
    assert len(interfaces) == 4

    return {
        "projective_overrefinement": {
            "R": "center-rooted K1,2",
            "S": "center-rooted K1,3",
            "R_projective": _projective_interface(r_states),
            "S_projective": _projective_interface(s_states),
            "common_context_interface": context_interface(r_states),
        },
        "infinite_quotient_witness_family": path_witnesses,
    }


def _padding_examples() -> dict[str, object]:
    # Existing strong support: adding more private leaves preserves gamma and zeta.
    base = star(2)
    padded = star(5)
    assert minimum_dominating_set_profile(base) == (1, 1)
    assert minimum_dominating_set_profile(padded) == (1, 1)

    # Creating forcing where none existed is not neutral.
    p2 = path(2)
    p3 = path(3)
    assert minimum_dominating_set_profile(p2) == (1, 2)
    assert minimum_dominating_set_profile(p3) == (1, 1)

    q2 = path(2)
    q2_states = rooted_minimum_dominating_set_states(q2, 0)
    forced_q2 = star(2)
    forced_states = rooted_minimum_dominating_set_states(forced_q2, 0)
    assert tuple((state.cost, state.count) for state in q2_states) == (
        (1, 1),
        (1, 1),
        (None, 0),
    )
    assert tuple((state.cost, state.count) for state in forced_states) == (
        (1, 1),
        (2, 1),
        (None, 0),
    )

    return {
        "strong_support_padding": {
            "before": {"order": 3, "profile": (1, 1)},
            "after": {"order": 6, "profile": (1, 1)},
            "conclusion": "extra leaves at an already strong support preserve gamma and zeta",
        },
        "arbitrary_padding_counterexample": {
            "before": {"tree": "P2", "profile": (1, 2)},
            "after": {"tree": "P3", "profile": (1, 1)},
            "conclusion": "adding a leaf at a nonforced endpoint can reduce zeta",
        },
        "q2_forcing_counterexample": {
            "before_signature": tuple((state.cost, state.count) for state in q2_states),
            "after_signature": tuple((state.cost, state.count) for state in forced_states),
            "conclusion": "padding Q2 with a second private leaf destroys its A/B tie",
        },
    }


def _frontier_counts(interfaces: set[ContextInterface]) -> tuple[int, int]:
    by_faces: dict[FaceProfile, list[ContextInterface]] = defaultdict(list)
    for interface in interfaces:
        by_faces[interface[0]].append(interface)

    weak_undominated = 0
    strict_survivors = 0
    for peers in by_faces.values():
        for interface in peers:
            if not any(
                _context_weakly_dominates(other, interface)
                for other in peers
                if other != interface
            ):
                weak_undominated += 1
            if not any(
                _context_strict_in_every_pattern(other, interface)
                for other in peers
                if other != interface
            ):
                strict_survivors += 1
    return weak_undominated, strict_survivors


def _diagnose_order(order: int) -> tuple[dict[str, object], dict[str, object] | None]:
    trees = generate_unlabeled_trees(order, order)
    assert len(trees) == EXPECTED_TREE_COUNTS[order - 1]
    assert all(graph.number_of_nodes() == order for graph in trees)

    projective_interfaces: set[
        tuple[tuple[int | None, int | None, int | None], tuple[int, int, int]]
    ] = set()
    context_interfaces: set[ContextInterface] = set()
    face_profiles: set[FaceProfile] = set()
    projectives_by_context: dict[ContextInterface, set[object]] = defaultdict(set)

    for graph in trees:
        for root in graph.nodes():
            states = rooted_minimum_dominating_set_states(graph, root)
            projective = _projective_interface(states)
            contextual = context_interface(states)
            projective_interfaces.add(projective)
            context_interfaces.add(contextual)
            face_profiles.add(contextual[0])
            projectives_by_context[contextual].add(projective)

    weak_undominated, strict_survivors = _frontier_counts(context_interfaces)
    collapse = next(
        (
            {
                "order": order,
                "context_interface": contextual,
                "projective_interfaces": sorted(
                    peers,
                    key=repr,
                )[:2],
            }
            for contextual, peers in projectives_by_context.items()
            if len(peers) > 1
        ),
        None,
    )

    return (
        {
            "order": order,
            "tree_count": len(trees),
            "rooted_evaluations": order * len(trees),
            "projective_interface_count": len(projective_interfaces),
            "context_interface_count": len(context_interfaces),
            "context_face_profile_count": len(face_profiles),
            "weak_context_undominated_count": weak_undominated,
            "strict_context_survivor_count": strict_survivors,
        },
        collapse,
    )


def build_diagnosis(max_order: int = MAX_BURNED_ORDER) -> dict[str, object]:
    if not 1 <= max_order <= MAX_BURNED_ORDER:
        raise ValueError("TF19 diagnosis is restricted to burned orders 1--14")

    canonical_contexts = _canonical_contexts()
    equivalence_examples = _context_equivalence_examples()
    padding_examples = _padding_examples()

    rows = []
    first_same_order_collapse = None
    for order in range(1, max_order + 1):
        row, collapse = _diagnose_order(order)
        rows.append(row)
        if first_same_order_collapse is None and collapse is not None:
            first_same_order_collapse = collapse

    return {
        "analysis_id": "TF19-DIAG-0001",
        "classification": "TREE_CONTEXT_QUOTIENT_EXACT_BUT_INFINITE",
        "fresh_data_consumed": False,
        "burned_data_boundary": {
            "exhaustive_orders": [1, max_order],
            "orders_at_least_15": "untouched",
        },
        "proved_context_message": {
            "K_A": "min(A_out,B_out,C_out)",
            "K_B": "min(A_out,B_out)",
            "K_C": "A_out",
            "normalized_cost_patterns": CONTEXT_COST_PATTERNS,
            "canonical_realizers": canonical_contexts,
        },
        "context_equivalence": {
            "description": (
                "A-normalized behavior is determined by the three realizable lower faces "
                "and exact counts only on states appearing on at least one such face."
            ),
            "examples": equivalence_examples,
            "first_same_order_burned_projective_collapse": first_same_order_collapse,
        },
        "budget_compensation": padding_examples,
        "burned_context_rows": rows,
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
                "tree contexts collapse the cost geometry to three patterns, but exact active "
                "count vectors remain infinite already on endpoint-rooted P_(3k); strong-support "
                "padding converts only replacements with an existing forcing bank and does not "
                "supply unrestricted same-order completeness"
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
