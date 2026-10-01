#!/usr/bin/env python3
"""Compact reproducible cost benchmark used to set TF1 census bounds."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import networkx as nx

from treeforge.invariants.core import domination_number, maximal_independent_set_count
from treeforge.invariants.greedy_uniformity import greedy_output_bias
from treeforge.invariants.probstack import finite_stackability_probability
from treeforge.invariants.registry import default_registry
from treeforge.invariants.treestack import treestack_estimate
from treeforge.trees.canonical import generate_unlabeled_trees

CORE = [
    "order",
    "leaf_count",
    "support_vertex_count",
    "max_degree",
    "diameter",
    "radius",
    "matching_number",
    "independence_number",
    "wiener_index",
    "cherry_count",
]


def elapsed(callable_):
    start = time.perf_counter()
    value = callable_()
    return value, time.perf_counter() - start


def run() -> dict[str, object]:
    registry = default_registry()
    by_order = []
    for order in range(8, 13):
        trees, generation_seconds = elapsed(lambda order=order: generate_unlabeled_trees(order, order))
        _, core_seconds = elapsed(lambda trees=trees: [registry.compute(tree, CORE) for tree in trees])
        _, domination_seconds = elapsed(lambda trees=trees: [domination_number(tree) for tree in trees])
        _, maximal_is_seconds = elapsed(
            lambda trees=trees: [maximal_independent_set_count(tree) for tree in trees]
        )
        _, treestack_seconds = elapsed(lambda trees=trees: [treestack_estimate(tree) for tree in trees])
        by_order.append(
            {
                "order": order,
                "tree_count": len(trees),
                "generation_seconds": generation_seconds,
                "core_seconds": core_seconds,
                "domination_seconds": domination_seconds,
                "maximal_independent_set_count_seconds": maximal_is_seconds,
                "treestack_seconds": treestack_seconds,
            }
        )

    probstack = []
    for order in (4, 6, 7):
        graph = nx.path_graph(order)
        for total in (2, 4, 6):
            _, seconds = elapsed(lambda graph=graph, total=total: finite_stackability_probability(graph, total))
            probstack.append({"family": "path", "order": order, "total": total, "seconds": seconds})

    greedy = []
    for order in (6, 7, 8):
        graph = nx.path_graph(order)
        _, seconds = elapsed(lambda graph=graph: greedy_output_bias(graph))
        greedy.append({"family": "path", "order": order, "seconds": seconds})

    return {"orders": by_order, "probstack_examples": probstack, "greedy_examples": greedy}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
