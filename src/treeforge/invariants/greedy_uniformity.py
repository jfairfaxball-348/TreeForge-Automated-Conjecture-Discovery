"""Optional exact greedy-output-law quantities inspired by Greedy Uniformity."""

from __future__ import annotations

import itertools
import math
from collections import Counter
from fractions import Fraction

import networkx as nx


def _greedy_output(graph: nx.Graph, order: tuple[int, ...]) -> frozenset[int]:
    chosen: set[int] = set()
    for vertex in order:
        if all(neighbor not in chosen for neighbor in graph.neighbors(vertex)):
            chosen.add(vertex)
    return frozenset(chosen)


def greedy_output_bias(graph: nx.Graph, max_order: int = 8) -> Fraction:
    """Exact TV bias between random-permutation greedy law and uniform MIS law."""
    if not nx.is_tree(graph) or graph.number_of_nodes() < 1:
        raise ValueError("expected a nonempty tree")
    n = graph.number_of_nodes()
    if n > max_order:
        raise ValueError("exact permutation enumeration exceeds configured cap")
    nodes = tuple(graph.nodes())
    counts = Counter(_greedy_output(graph, order) for order in itertools.permutations(nodes))
    total = math.factorial(n)
    uniform = Fraction(1, len(counts))
    return sum(abs(Fraction(count, total) - uniform) for count in counts.values()) / 2
