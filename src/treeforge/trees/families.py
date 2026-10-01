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
