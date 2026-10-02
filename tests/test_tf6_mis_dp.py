import itertools

import networkx as nx

from treeforge.invariants.core import maximal_independent_set_count
from treeforge.trees.canonical import generate_unlabeled_trees


def _brute_force_maximal_independent_set_count(graph: nx.Graph) -> int:
    vertices = list(graph.nodes())
    total = 0
    for mask in range(1 << len(vertices)):
        subset = {vertices[i] for i in range(len(vertices)) if mask & (1 << i)}
        if any(u in subset and v in subset for u, v in graph.edges()):
            continue
        if all(v in subset or any(u in subset for u in graph.neighbors(v)) for v in graph.nodes()):
            total += 1
    return total


def test_tree_dp_matches_independent_bruteforce_through_order_8():
    for graph in generate_unlabeled_trees(1, 8):
        assert maximal_independent_set_count(graph) == _brute_force_maximal_independent_set_count(graph)


def test_path_counts_obey_padovan_type_recurrence():
    counts = [maximal_independent_set_count(nx.path_graph(order)) for order in range(1, 16)]
    assert counts[:5] == [1, 2, 2, 3, 4]
    for index in range(3, len(counts)):
        assert counts[index] == counts[index - 2] + counts[index - 3]


def test_duplicate_leaf_at_existing_support_does_not_change_mis_count():
    for spine_order in range(2, 7):
        base = nx.path_graph(spine_order)
        support = 0

        one_leaf = base.copy()
        one_leaf.add_edge(support, spine_order)

        two_leaves = one_leaf.copy()
        two_leaves.add_edge(support, spine_order + 1)

        assert maximal_independent_set_count(one_leaf) == maximal_independent_set_count(two_leaves)


def test_corona_mis_count_equals_base_independent_set_count():
    for order in range(1, 8):
        base = nx.path_graph(order)
        corona = base.copy()
        for vertex in range(order):
            corona.add_edge(vertex, order + vertex)

        independent_sets = 0
        vertices = list(base.nodes())
        for size in range(order + 1):
            for subset_tuple in itertools.combinations(vertices, size):
                subset = set(subset_tuple)
                if all(not (u in subset and v in subset) for u, v in base.edges()):
                    independent_sets += 1

        assert maximal_independent_set_count(corona) == independent_sets
