"""Optional exact finite random-stackability observables inspired by ProbStack."""

from __future__ import annotations

from fractions import Fraction

import networkx as nx

EMPTY = None


def _transfer(value: int) -> int:
    if value <= 1:
        return 2 * value - 3
    if value == 2:
        return 1
    if value == 3:
        return 0
    if value % 2 == 0:
        return value // 2
    return (value - 3) // 2


def _scores(graph: nx.Graph, configuration: tuple[int, ...]) -> tuple[int, ...]:
    nodes = list(sorted(graph.nodes()))
    index = {node: i for i, node in enumerate(nodes)}

    def message(v: int, parent: int) -> int | None:
        children = [u for u in graph.neighbors(v) if u != parent]
        child_messages = [message(u, v) for u in children]
        if configuration[index[v]] == 0 and all(item is EMPTY for item in child_messages):
            return EMPTY
        effective = configuration[index[v]] + sum(item for item in child_messages if item is not EMPTY)
        return _transfer(effective)

    result = []
    for root in nodes:
        root_messages = [message(u, root) for u in graph.neighbors(root)]
        result.append(configuration[index[root]] + sum(x for x in root_messages if x is not EMPTY))
    return tuple(result)


def _weak_compositions(total: int, parts: int):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in _weak_compositions(total - first, parts - 1):
            yield (first,) + rest


def finite_stackability_probability(graph: nx.Graph, total: int) -> Fraction:
    """Return exact p_T(total) under the uniform weak-composition model."""
    if total < 0 or not nx.is_tree(graph) or graph.number_of_nodes() < 1:
        raise ValueError("expected a nonempty tree and nonnegative total")
    if graph.number_of_nodes() > 10 or total > 12:
        raise ValueError("TF0 conservative exact-computation cap exceeded")
    configs = list(_weak_compositions(total, graph.number_of_nodes()))
    stackable = sum(any(score > 0 for score in _scores(graph, config)) for config in configs)
    return Fraction(stackable, len(configs))
