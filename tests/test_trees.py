import networkx as nx

from treeforge.trees.canonical import canonical_tree_code, generate_unlabeled_trees


def test_canonical_code_is_label_invariant():
    graph = nx.path_graph(6)
    relabeled = nx.relabel_nodes(graph, {0: 5, 1: 3, 2: 1, 3: 4, 4: 0, 5: 2})
    assert canonical_tree_code(graph) == canonical_tree_code(relabeled)


def test_unlabeled_counts_through_six():
    counts = []
    for order in range(1, 7):
        counts.append(len(generate_unlabeled_trees(order, order)))
    assert counts == [1, 1, 1, 2, 3, 6]
