"""Explicit adversarial/parametric tree families."""

from __future__ import annotations

import networkx as nx


def path(order: int) -> nx.Graph:
    if order < 1:
        raise ValueError("order must be positive")
    return nx.path_graph(order)


def star(leaves: int) -> nx.Graph:
    if leaves < 1:
        raise ValueError("a nontrivial star needs at least one leaf")
    return nx.star_graph(leaves)


def spider(arm_lengths: list[int]) -> nx.Graph:
    if not arm_lengths or any(length < 1 for length in arm_lengths):
        raise ValueError("spider arms must have positive lengths")
    graph = nx.Graph()
    graph.add_node(0)
    nxt = 1
    for length in arm_lengths:
        parent = 0
        for _ in range(length):
            graph.add_edge(parent, nxt)
            parent = nxt
            nxt += 1
    return graph


def caterpillar(spine_order: int, leaf_multiplicities: list[int]) -> nx.Graph:
    if spine_order < 1 or len(leaf_multiplicities) != spine_order:
        raise ValueError("leaf multiplicities must match a positive spine order")
    if any(value < 0 for value in leaf_multiplicities):
        raise ValueError("leaf multiplicities must be nonnegative")
    graph = nx.path_graph(spine_order)
    nxt = spine_order
    for spine_vertex, count in enumerate(leaf_multiplicities):
        for _ in range(count):
            graph.add_edge(spine_vertex, nxt)
            nxt += 1
    return graph


def balanced_binary_tree(height: int) -> nx.Graph:
    if height < 0:
        raise ValueError("height must be nonnegative")
    return nx.balanced_tree(2, height)


def double_star(left_leaves: int, right_leaves: int) -> nx.Graph:
    if left_leaves < 1 or right_leaves < 1:
        raise ValueError("double-star sides need at least one leaf")
    graph = nx.Graph()
    graph.add_edge(0, 1)
    nxt = 2
    for center, count in ((0, left_leaves), (1, right_leaves)):
        for _ in range(count):
            graph.add_edge(center, nxt)
            nxt += 1
    return graph


def broom(handle_edges: int, brush_leaves: int) -> nx.Graph:
    if handle_edges < 1 or brush_leaves < 1:
        raise ValueError("broom needs a positive handle and at least one brush leaf")
    graph = nx.path_graph(handle_edges + 1)
    hub = handle_edges
    nxt = handle_edges + 1
    for _ in range(brush_leaves):
        graph.add_edge(hub, nxt)
        nxt += 1
    return graph
