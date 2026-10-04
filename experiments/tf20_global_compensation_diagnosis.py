#!/usr/bin/env python3
"""TF20 global-compensation diagnosis using only burned orders 1--14.

The theorem-facing definitions in this module are fixed before the burned
census.  TF20 distinguishes strong-support banks from strong-bankless trees,
records the canonical marked support-core representation of the latter, and
tests only consequences that do not require order 15.

No function in this module constructs an unlabeled tree of order 15 or larger.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import networkx as nx

from experiments.tf19_tree_context_diagnosis import context_interface
from treeforge.invariants.minimum_dominating_sets import (
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

EXPECTED_TREE_COUNTS = [1, 1, 1, 2, 3, 6, 11, 23, 47, 106, 235, 551, 1301, 3159]


def _jsonl(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def validate_repository_boundary() -> None:
    """Assert the TF19 boundary before any burned-data diagnosis."""
    assert CandidateRegistry(CANDIDATES).next_id() == "TF-001158"

    experiments = _jsonl(EXPERIMENTS)
    scientific = [
        row for row in experiments if str(row.get("experiment_id", "")).startswith("TF")
    ]
    assert scientific
    assert scientific[-1]["experiment_id"] == "TF4-0001"
    assert all(
        not str(row.get("experiment_id", "")).startswith(
            tuple(f"TF{index}" for index in range(5, 21))
        )
        for row in experiments
    )

    assert "minimum_dominating_set_count" not in set(default_registry().names())


def _leaves(graph: nx.Graph) -> set[object]:
    if graph.number_of_nodes() <= 1:
        return set()
    return {vertex for vertex, degree in graph.degree() if degree == 1}


def _supports(graph: nx.Graph) -> dict[object, tuple[object, ...]]:
    leaves = _leaves(graph)
    return {
        vertex: tuple(neighbor for neighbor in graph.neighbors(vertex) if neighbor in leaves)
        for vertex in graph.nodes()
        if any(neighbor in leaves for neighbor in graph.neighbors(vertex))
    }


def strong_supports(graph: nx.Graph) -> tuple[object, ...]:
    """Return supports with at least two private leaf neighbours."""
    return tuple(
        vertex
        for vertex, leaf_neighbours in _supports(graph).items()
        if len(leaf_neighbours) >= 2
    )


def marked_support_core(graph: nx.Graph) -> dict[str, object]:
    """Return the canonical marked-core data for a strong-bankless tree.

    For order at least three and no strong support, delete all leaves.  The
    remaining induced graph H is a tree.  Mark exactly the former support
    vertices.  Every mark had one private leaf, and every leaf of H is marked.
    Reattaching one leaf to every mark reconstructs the original tree.
    """
    if strong_supports(graph):
        raise ValueError("marked support core is defined here only for strong-bankless trees")

    order = graph.number_of_nodes()
    if order == 1:
        return {
            "kind": "K1",
            "core_order": 1,
            "mark_count": 0,
            "core_leaf_count": 0,
        }
    if order == 2:
        return {
            "kind": "P2_EXCEPTION",
            "core_order": 0,
            "mark_count": 0,
            "core_leaf_count": 0,
        }

    leaves = _leaves(graph)
    supports = _supports(graph)
    marks = set(supports)
    assert all(len(leaf_neighbours) == 1 for leaf_neighbours in supports.values())

    core = graph.subgraph(set(graph.nodes()) - leaves).copy()
    assert core.number_of_nodes() >= 2
    assert nx.is_tree(core)

    core_leaves = {vertex for vertex, degree in core.degree() if degree == 1}
    assert core_leaves <= marks
    assert marks <= set(core.nodes())

    reconstructed = core.copy()
    for mark in sorted(marks, key=repr):
        reconstructed.add_edge(mark, ("tf20-private-leaf", repr(mark)))
    assert nx.is_isomorphic(graph, reconstructed)

    return {
        "kind": "MARKED_TREE_CORE",
        "core_order": core.number_of_nodes(),
        "mark_count": len(marks),
        "core_leaf_count": len(core_leaves),
        "all_core_leaves_marked": True,
        "reconstruction_verified": True,
    }


def p2_p3_budget(deficit: int) -> tuple[int, int]:
    """Write every deficit >=2 as 2*a+3*b with a,b nonnegative."""
    if deficit < 2:
        raise ValueError("P2/P3 compensation covers exactly deficits at least two")
    if deficit % 2 == 0:
        return deficit // 2, 0
    return (deficit - 3) // 2, 1


def _p4_one_leaf_extension_counterexample() -> dict[str, object]:
    """Show that generic one-vertex leaf compensation is false."""
    base = path(4)
    base_profile = minimum_dominating_set_profile(base)
    assert base_profile == (2, 4)

    extensions = []
    for attachment in base.nodes():
        extended = base.copy()
        new_vertex = max(extended.nodes()) + 1
        extended.add_edge(attachment, new_vertex)
        profile = minimum_dominating_set_profile(extended)
        extensions.append(
            {
                "attachment_degree_in_P4": base.degree(attachment),
                "profile": profile,
            }
        )

    assert max(profile["profile"][1] for profile in extensions) == 3
    return {
        "base": {"tree": "P4", "profile": base_profile},
        "one_leaf_extensions": extensions,
        "best_extension_zeta": 3,
        "conclusion": (
            "every one-leaf extension of P4 has fewer minimum dominating sets; "
            "there is no universal one-vertex leaf bank"
        ),
    }


def _weak_banked_replacement_example() -> dict[str, object]:
    """Check exact order restoration at an untouched external strong support."""
    old_gadget = star(3)
    new_gadget = star(2)
    old_states = rooted_minimum_dominating_set_states(old_gadget, 0)
    new_states = rooted_minimum_dominating_set_states(new_gadget, 0)
    assert context_interface(old_states) == context_interface(new_states)

    old_tree = nx.Graph(
        [
            (0, 1),
            (1, 2),
            (1, 3),
            (0, 4),
            (4, 5),
            (4, 6),
            (4, 7),
        ]
    )
    new_tree = nx.Graph(
        [
            (0, 1),
            (1, 2),
            (1, 3),
            (1, 7),
            (0, 4),
            (4, 5),
            (4, 6),
        ]
    )
    assert old_tree.number_of_nodes() == new_tree.number_of_nodes() == 8
    assert 1 in strong_supports(old_tree)
    assert 1 in strong_supports(new_tree)

    old_profile = minimum_dominating_set_profile(old_tree)
    new_profile = minimum_dominating_set_profile(new_tree)
    assert old_profile == new_profile

    return {
        "old_gadget_order": 4,
        "new_gadget_order": 3,
        "vertex_deficit": 1,
        "same_context_interface": True,
        "padding_bank": "untouched external strong support",
        "old_profile": old_profile,
        "new_profile": new_profile,
        "conclusion": "weak context replacement plus one bank leaf preserves exact order and profile",
    }


def _vertex_status_counts(graph: nx.Graph) -> tuple[int, int, int]:
    universal = empty = flexible = 0
    for vertex in graph.nodes():
        selected, dominated, _ = rooted_minimum_dominating_set_states(graph, vertex)
        if dominated.cost is None or (
            selected.cost is not None and selected.cost < dominated.cost
        ):
            universal += 1
        elif selected.cost is not None and dominated.cost < selected.cost:
            empty += 1
        else:
            flexible += 1
    return universal, empty, flexible


def _burned_rows(max_order: int) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for order in range(1, max_order + 1):
        trees = generate_unlabeled_trees(order, order)
        assert len(trees) == EXPECTED_TREE_COUNTS[order - 1]

        grouped: list[tuple[nx.Graph, int]] = []
        bankless_count = 0
        banked_count = 0
        marked_core_verified = 0
        for graph in trees:
            _, zeta = minimum_dominating_set_profile(graph)
            grouped.append((graph, zeta))
            if strong_supports(graph):
                banked_count += 1
            else:
                bankless_count += 1
                marked_support_core(graph)
                marked_core_verified += 1

        maximum = max(zeta for _, zeta in grouped)
        extremizers = [graph for graph, zeta in grouped if zeta == maximum]
        extremizer_banked = [graph for graph in extremizers if strong_supports(graph)]
        extremizer_bankless = [graph for graph in extremizers if not strong_supports(graph)]
        extremizer_strong_support_counts = [
            len(strong_supports(graph)) for graph in extremizers
        ]
        extremizer_statuses = [_vertex_status_counts(graph) for graph in extremizers]

        rows.append(
            {
                "order": order,
                "tree_count": len(trees),
                "banked_tree_count": banked_count,
                "strong_bankless_tree_count": bankless_count,
                "marked_core_verified_count": marked_core_verified,
                "M_n_burned": maximum,
                "extremizer_count": len(extremizers),
                "banked_extremizer_count": len(extremizer_banked),
                "strong_bankless_extremizer_count": len(extremizer_bankless),
                "extremizer_strong_support_counts": sorted(
                    set(extremizer_strong_support_counts)
                ),
                "extremizer_vertex_status_triples": sorted(set(extremizer_statuses)),
            }
        )
    return rows


def build_diagnosis(max_order: int = MAX_BURNED_ORDER) -> dict[str, object]:
    if not 1 <= max_order <= MAX_BURNED_ORDER:
        raise ValueError("TF20 diagnosis is restricted to burned orders 1--14")

    budget_examples = {
        deficit: p2_p3_budget(deficit)
        for deficit in range(2, MAX_BURNED_ORDER + 1)
    }
    assert all(2 * a + 3 * b == deficit for deficit, (a, b) in budget_examples.items())

    return {
        "analysis_id": "TF20-DIAG-0001",
        "classification": "GLOBAL_COMPENSATION_REDUCES_OBSTRUCTION_TO_ONE_VERTEX",
        "fresh_data_consumed": False,
        "burned_data_boundary": {
            "exhaustive_orders": [1, max_order],
            "orders_at_least_15": "untouched",
        },
        "theorem_checks": {
            "p2_p3_budget_examples": budget_examples,
            "weak_banked_replacement_example": _weak_banked_replacement_example(),
            "one_vertex_padding_counterexample": _p4_one_leaf_extension_counterexample(),
            "marked_support_core": (
                "every strong-bankless burned tree is reconstructed from a tree core "
                "with a marked subset containing every core leaf"
            ),
        },
        "burned_global_rows": _burned_rows(max_order),
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
                "strong-support banking and P2/P3 forest compensation cover many exact-order "
                "replacements, but Taletskii's no-universal empty-vertex reduction has exact "
                "deficit one in a class with no strong bank; the marked support core is canonical "
                "but has arbitrary unbounded tree geometry, so no complete finite extremal grammar "
                "or prospective M_15 theorem is proved"
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
