from fractions import Fraction

import networkx as nx

from treeforge.invariants.core import independence_number, matching_number
from treeforge.invariants.greedy_uniformity import greedy_output_bias
from treeforge.invariants.probstack import finite_stackability_probability
from treeforge.invariants.registry import default_registry
from treeforge.invariants.treestack import treestack_estimate


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
