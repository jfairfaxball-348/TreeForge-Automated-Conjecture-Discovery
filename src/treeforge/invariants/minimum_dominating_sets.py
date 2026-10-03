"""Exact counting of minimum dominating sets in finite trees.

This module is diagnostic/theorem-support machinery. It is deliberately not
registered as a default TreeForge discovery invariant.
"""

from __future__ import annotations

from dataclasses import dataclass

import networkx as nx


@dataclass(frozen=True)
class MinCount:
    """A min-plus/count state.

    cost is the minimum number of selected vertices, with None denoting an
    infeasible state. count is the exact number of choices attaining that cost.
    """

    cost: int | None
    count: int


INFEASIBLE = MinCount(None, 0)
IDENTITY = MinCount(0, 1)


def _minimum(*states: MinCount) -> MinCount:
    feasible = [state for state in states if state.cost is not None]
    if not feasible:
        return INFEASIBLE
    minimum_cost = min(state.cost for state in feasible)
    return MinCount(
        minimum_cost,
        sum(state.count for state in feasible if state.cost == minimum_cost),
    )


def _product(left: MinCount, right: MinCount) -> MinCount:
    if left.cost is None or right.cost is None:
        return INFEASIBLE
    return MinCount(left.cost + right.cost, left.count * right.count)


def rooted_minimum_dominating_set_states(
    graph: nx.Graph,
    root: object,
) -> tuple[MinCount, MinCount, MinCount]:
    """Return the exact rooted states (A, B, C) at root.

    The graph must be a nonempty tree.

    A: the root is selected.
    B: the root is not selected and is dominated by at least one child.
    C: the root is not selected, is not dominated in its rooted subtree, and
       therefore must be dominated by its parent.

    Each state stores the minimum selected-vertex cost in the rooted subtree and
    the exact number of choices attaining that cost.
    """
    if graph.number_of_nodes() < 1 or not nx.is_tree(graph):
        raise ValueError("expected a nonempty finite tree")
    if root not in graph:
        raise ValueError("root must be a vertex of the tree")

    def visit(vertex: object, parent: object | None) -> tuple[MinCount, MinCount, MinCount]:
        child_states = [
            visit(child, vertex)
            for child in graph.neighbors(vertex)
            if child != parent
        ]

        selected = MinCount(1, 1)
        for child_a, child_b, child_c in child_states:
            selected = _product(selected, _minimum(child_a, child_b, child_c))

        needs_parent = IDENTITY
        for _, child_b, _ in child_states:
            needs_parent = _product(needs_parent, child_b)

        no_selected_child = IDENTITY
        has_selected_child = INFEASIBLE
        for child_a, child_b, _ in child_states:
            next_no_selected = _product(no_selected_child, child_b)
            next_has_selected = _minimum(
                _product(has_selected_child, _minimum(child_a, child_b)),
                _product(no_selected_child, child_a),
            )
            no_selected_child = next_no_selected
            has_selected_child = next_has_selected

        return selected, has_selected_child, needs_parent

    return visit(root, None)


def minimum_dominating_set_profile(
    graph: nx.Graph,
    root: object | None = None,
) -> tuple[int, int]:
    """Return (gamma(T), zeta(T)) exactly for a nonempty finite tree.

    zeta(T) is the number of minimum dominating sets. At the root, state C is
    inadmissible because no parent exists, so the result is the min-plus/count
    choice between states A and B.
    """
    if graph.number_of_nodes() < 1 or not nx.is_tree(graph):
        raise ValueError("expected a nonempty finite tree")
    if root is None:
        root = next(iter(graph.nodes()))

    selected, dominated_by_child, _ = rooted_minimum_dominating_set_states(graph, root)
    result = _minimum(selected, dominated_by_child)
    if result.cost is None:
        raise AssertionError("a nonempty tree must have a dominating set")
    return result.cost, result.count


def minimum_dominating_set_count(graph: nx.Graph) -> int:
    """Return the exact number of minimum dominating sets of a tree."""
    return minimum_dominating_set_profile(graph)[1]
