"""Small exact, interpretable tree invariants for initial discovery work."""

from __future__ import annotations

import itertools
import math

import networkx as nx

from .registry import InvariantSpec


def _degrees(graph: nx.Graph) -> list[int]:
    return [degree for _, degree in graph.degree()]


def leaf_count(graph: nx.Graph) -> int:
    if graph.number_of_nodes() == 1:
        return 0
    return sum(degree == 1 for degree in _degrees(graph))


def support_vertex_count(graph: nx.Graph) -> int:
    leaves = {v for v, degree in graph.degree() if degree == 1}
    return sum(any(u in leaves for u in graph.neighbors(v)) for v in graph.nodes())


def matching_number(graph: nx.Graph) -> int:
    root = next(iter(graph.nodes()))

    def visit(v: int, parent: int | None) -> tuple[int, int]:
        children = [u for u in graph.neighbors(v) if u != parent]
        child = {u: visit(u, v) for u in children}
        unmatched = sum(child[u][0] for u in children)
        best = unmatched
        for u in children:
            best = max(best, 1 + child[u][1] + unmatched - child[u][0])
        return best, unmatched

    return visit(root, None)[0]


def independence_number(graph: nx.Graph) -> int:
    root = next(iter(graph.nodes()))

    def visit(v: int, parent: int | None) -> tuple[int, int]:
        children = [u for u in graph.neighbors(v) if u != parent]
        vals = [visit(u, v) for u in children]
        take = 1 + sum(skip for _, skip in vals)
        skip = sum(max(take_u, skip_u) for take_u, skip_u in vals)
        return take, skip

    return max(visit(root, None))


def _is_dominating(graph: nx.Graph, subset: set[int]) -> bool:
    dominated = set(subset)
    for v in subset:
        dominated.update(graph.neighbors(v))
    return len(dominated) == graph.number_of_nodes()


def domination_number(graph: nx.Graph) -> int:
    vertices = list(graph.nodes())
    for size in range(1, len(vertices) + 1):
        for subset in itertools.combinations(vertices, size):
            if _is_dominating(graph, set(subset)):
                return size
    raise AssertionError("nonempty graph must have a dominating set")


def _is_maximal_independent(graph: nx.Graph, subset: set[int]) -> bool:
    if any(u in subset and v in subset for u, v in graph.edges()):
        return False
    return all(v in subset or any(u in subset for u in graph.neighbors(v)) for v in graph.nodes())


def maximal_independent_set_count(graph: nx.Graph) -> int:
    """Count maximal independent sets by a three-state exact tree DP.

    A maximal independent set is exactly an independent dominating set.  For a
    rooted subtree the returned states count solutions where the root is
    selected, is unselected but dominated by a selected child, or is
    unselected and still needs its parent to dominate it.
    """
    root = next(iter(graph.nodes()))

    def visit(vertex: int, parent: int | None) -> tuple[int, int, int]:
        children = [visit(u, vertex) for u in graph.neighbors(vertex) if u != parent]
        selected = math.prod(dominated + needs_parent for _, dominated, needs_parent in children)
        needs_parent = math.prod(dominated for _, dominated, _ in children)
        child_closed = math.prod(
            selected_child + dominated for selected_child, dominated, _ in children
        )
        dominated_by_child = child_closed - needs_parent
        return selected, dominated_by_child, needs_parent

    selected, dominated, _ = visit(root, None)
    return selected + dominated


def wiener_index(graph: nx.Graph) -> int:
    distances = dict(nx.all_pairs_shortest_path_length(graph))
    return sum(distances[u][v] for u, v in itertools.combinations(graph.nodes(), 2))


def cherry_count(graph: nx.Graph) -> int:
    leaves = {v for v, degree in graph.degree() if degree == 1}
    return sum(math.comb(sum(u in leaves for u in graph.neighbors(v)), 2) for v in graph.nodes())


def _eccentricity_sum(graph: nx.Graph) -> int:
    return sum(nx.eccentricity(graph).values())


CORE_INVARIANTS = (
    InvariantSpec("order", "|V(T)|", "definition", True, lambda g: g.number_of_nodes()),
    InvariantSpec("edge_count", "|E(T)|", "definition", True, lambda g: g.number_of_edges()),
    InvariantSpec("min_degree", "minimum vertex degree", "definition", True, lambda g: min(_degrees(g))),
    InvariantSpec("max_degree", "maximum vertex degree", "definition", True, lambda g: max(_degrees(g))),
    InvariantSpec("degree_sum", "sum_v deg(v)", "definition", True, lambda g: sum(_degrees(g))),
    InvariantSpec("leaf_count", "number of degree-one vertices", "standard", True, leaf_count),
    InvariantSpec(
        "support_vertex_count",
        "number of vertices adjacent to a leaf",
        "standard tree terminology",
        True,
        support_vertex_count,
    ),
    InvariantSpec("diameter", "max_{u,v} d(u,v)", "standard", True, nx.diameter),
    InvariantSpec("radius", "min_v ecc(v)", "standard", True, nx.radius),
    InvariantSpec("eccentricity_sum", "sum_v ecc(v)", "standard", True, _eccentricity_sum),
    InvariantSpec("matching_number", "maximum matching cardinality", "tree DP", True, matching_number),
    InvariantSpec(
        "independence_number",
        "maximum independent-set cardinality",
        "independent tree DP",
        True,
        independence_number,
    ),
    InvariantSpec("domination_number", "minimum dominating-set cardinality", "exact search", True, domination_number),
    InvariantSpec(
        "maximal_independent_set_count",
        "number of inclusion-maximal independent sets",
        "exact search",
        True,
        maximal_independent_set_count,
    ),
    InvariantSpec("wiener_index", "sum_{u<v} d(u,v)", "standard", True, wiener_index),
    InvariantSpec("cherry_count", "leaf pairs with common support", "definition", True, cherry_count),
)
