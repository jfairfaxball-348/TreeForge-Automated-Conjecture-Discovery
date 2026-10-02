"""Canonical encodings and deterministic unlabeled-tree generation."""

from __future__ import annotations

from collections.abc import Iterable

import networkx as nx


def _validate_tree(graph: nx.Graph) -> None:
    if graph.number_of_nodes() < 1:
        raise ValueError("tree must be nonempty")
    if not nx.is_tree(graph):
        raise ValueError("expected a finite simple tree")


def _rooted_code(graph: nx.Graph, vertex: int, parent: int | None) -> str:
    children = [u for u in graph.neighbors(vertex) if u != parent]
    return "(" + "".join(sorted(_rooted_code(graph, u, vertex) for u in children)) + ")"


def canonical_tree_code(graph: nx.Graph) -> str:
    """Return an exact isomorphism-invariant AHU-style code for an unrooted tree."""
    _validate_tree(graph)
    graph = nx.convert_node_labels_to_integers(graph, ordering="sorted")
    centers = nx.center(graph)
    if len(centers) == 1:
        return _rooted_code(graph, centers[0], None)
    if len(centers) != 2:
        raise AssertionError("a tree has one or two centers")
    a, b = centers
    halves = sorted((_rooted_code(graph, a, b), _rooted_code(graph, b, a)))
    return "(" + "".join(halves) + ")"


def canonical_tree_identity(graph: nx.Graph) -> tuple[int, str]:\n    """Return an exact cross-order tree identity without changing legacy codes."""\n    _validate_tree(graph)\n    return graph.number_of_nodes(), canonical_tree_code(graph)\n\n\ndef generate_unlabeled_trees(min_order: int, max_order: int) -> list[nx.Graph]:
    """Generate one representative of every unlabeled tree in a closed order range.

    Results are sorted by `(order, canonical_code)` so serialization is reproducible.
    """
    if min_order < 1 or max_order < min_order:
        raise ValueError("require 1 <= min_order <= max_order")
    rows: list[tuple[int, str, nx.Graph]] = []
    for order in range(min_order, max_order + 1):
        source: Iterable[nx.Graph]
        if order == 1:
            source = [nx.empty_graph(1)]
        else:
            source = nx.generators.nonisomorphic_trees(order)
        seen: set[str] = set()
        for graph in source:
            graph = nx.convert_node_labels_to_integers(nx.Graph(graph), ordering="sorted")
            code = canonical_tree_code(graph)
            if code in seen:
                raise AssertionError(f"duplicate isomorphism class generated at order {order}")
            seen.add(code)
            rows.append((order, code, graph))
    rows.sort(key=lambda item: (item[0], item[1]))
    return [graph for _, _, graph in rows]
