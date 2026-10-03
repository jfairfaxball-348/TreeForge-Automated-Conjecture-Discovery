from fractions import Fraction

import networkx as nx

from treeforge.invariants.core import (
    _segment_count_by_decomposition,
    independence_number,
    matching_number,
    segment_count,
)
from treeforge.invariants.greedy_uniformity import greedy_output_bias
from treeforge.invariants.probstack import finite_stackability_probability
from treeforge.invariants.registry import default_registry
from treeforge.invariants.treestack import treestack_estimate
from treeforge.trees.canonical import generate_unlabeled_trees
from treeforge.trees.families import caterpillar, double_star, path, spider, star


def test_core_invariants_on_path4():
    graph = nx.path_graph(4)
    values = default_registry().compute(
        graph,
        ["order", "edge_count", "leaf_count", "diameter", "matching_number", "independence_number"],
    )
    assert values == {
        "order": 4,
        "edge_count": 3,
        "leaf_count": 2,
        "diameter": 3,
        "matching_number": 2,
        "independence_number": 2,
    }
    assert matching_number(graph) == 2
    assert independence_number(graph) == 2


def test_predecessor_inspired_exact_examples():
    p2 = nx.path_graph(2)
    assert treestack_estimate(p2) >= 2
    assert finite_stackability_probability(p2, 2) == Fraction(2, 3)
    assert greedy_output_bias(p2) == 0



def test_segment_count_named_structural_examples():
    examples = [
        (nx.empty_graph(1), 0),
        (path(2), 1),
        (path(7), 1),
        (star(3), 3),
        (star(7), 7),
        (double_star(2, 3), 6),
        (spider([1, 2, 4, 5]), 4),
        (caterpillar(5, [2, 0, 1, 0, 2]), 7),
    ]
    for graph, expected in examples:
        assert segment_count(graph) == expected
        assert _segment_count_by_decomposition(graph) == expected


def test_segment_count_formula_agrees_with_independent_decomposition_on_burned_orders():
    for graph in generate_unlabeled_trees(1, 14):
        expected = graph.number_of_nodes() - sum(degree == 2 for _, degree in graph.degree()) - 1
        assert segment_count(graph) == expected
        assert _segment_count_by_decomposition(graph) == expected


def test_segment_count_is_invariant_under_edge_subdivision():
    graph = spider([1, 2, 4])
    expected = segment_count(graph)

    for _ in range(3):
        u, v = next(iter(graph.edges()))
        new_vertex = max(graph.nodes()) + 1
        graph.remove_edge(u, v)
        graph.add_edges_from(((u, new_vertex), (new_vertex, v)))
        assert segment_count(graph) == expected
        assert _segment_count_by_decomposition(graph) == expected
