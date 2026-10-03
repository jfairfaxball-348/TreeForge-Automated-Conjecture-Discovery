import itertools

import networkx as nx

from treeforge.invariants.core import domination_number
from treeforge.invariants.minimum_dominating_sets import (
    INFEASIBLE,
    MinCount,
    minimum_dominating_set_profile,
    rooted_minimum_dominating_set_states,
)
from treeforge.trees.canonical import generate_unlabeled_trees
from treeforge.trees.families import double_star, path, star


def _brute_force_profile(graph: nx.Graph) -> tuple[int, int]:
    vertices = list(graph.nodes())
    for size in range(len(vertices) + 1):
        count = 0
        for choice in itertools.combinations(vertices, size):
            selected = set(choice)
            dominated = set(selected)
            for vertex in selected:
                dominated.update(graph.neighbors(vertex))
            if len(dominated) == len(vertices):
                count += 1
        if count:
            return size, count
    raise AssertionError("nonempty graph must have a dominating set")


def _corona(base: nx.Graph) -> nx.Graph:
    base = nx.convert_node_labels_to_integers(base, ordering="sorted")
    graph = base.copy()
    order = base.number_of_nodes()
    for vertex in range(order):
        graph.add_edge(vertex, order + vertex)
    return graph


def _subdivided_star(leaves: int) -> nx.Graph:
    graph = nx.Graph()
    graph.add_node(0)
    next_vertex = 1
    for _ in range(leaves):
        preleaf = next_vertex
        leaf = next_vertex + 1
        next_vertex += 2
        graph.add_edges_from(((0, preleaf), (preleaf, leaf)))
    return graph


def test_leaf_state_semantics_are_exact():
    graph = nx.empty_graph(1)
    selected, dominated_by_child, needs_parent = rooted_minimum_dominating_set_states(graph, 0)
    assert selected == MinCount(1, 1)
    assert dominated_by_child == INFEASIBLE
    assert needs_parent == MinCount(0, 1)
    assert minimum_dominating_set_profile(graph) == (1, 1)


def test_dp_matches_independent_bruteforce_through_order_8():
    for graph in generate_unlabeled_trees(1, 8):
        assert minimum_dominating_set_profile(graph) == _brute_force_profile(graph)


def test_gamma_component_matches_existing_exact_core_on_all_burned_orders():
    for graph in generate_unlabeled_trees(1, 14):
        gamma, _ = minimum_dominating_set_profile(graph)
        assert gamma == domination_number(graph)


def test_profile_is_root_invariant_through_order_8():
    for graph in generate_unlabeled_trees(1, 8):
        expected = minimum_dominating_set_profile(graph)
        for root in graph.nodes():
            assert minimum_dominating_set_profile(graph, root=root) == expected


def test_named_small_trees():
    assert minimum_dominating_set_profile(path(1)) == (1, 1)
    assert minimum_dominating_set_profile(path(2)) == (1, 2)
    assert minimum_dominating_set_profile(path(4)) == (2, 4)
    assert minimum_dominating_set_profile(path(7)) == (3, 8)

    assert minimum_dominating_set_profile(star(1)) == (1, 2)
    for leaves in range(2, 8):
        assert minimum_dominating_set_profile(star(leaves)) == (1, 1)

    assert minimum_dominating_set_profile(double_star(1, 1)) == (2, 4)
    assert minimum_dominating_set_profile(double_star(1, 3)) == (2, 2)
    assert minimum_dominating_set_profile(double_star(3, 3)) == (2, 1)

    for leaves in range(2, 7):
        assert minimum_dominating_set_profile(_subdivided_star(leaves)) == (
            leaves,
            2**leaves - 1,
        )


def test_every_tree_corona_has_two_choices_per_host_leaf_pair():
    for base_order in range(1, 8):
        for base in generate_unlabeled_trees(base_order, base_order):
            corona = _corona(base)
            assert minimum_dominating_set_profile(corona) == (
                base_order,
                2**base_order,
            )
