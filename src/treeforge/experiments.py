"""Helpers for frozen discovery/holdout experiments."""

from __future__ import annotations

import json
from pathlib import Path

from .invariants.registry import default_registry
from .trees.canonical import canonical_tree_code, generate_unlabeled_trees


def load_frozen_spec(path: str | Path) -> dict[str, object]:
    spec = json.loads(Path(path).read_text(encoding="utf-8"))
    if spec.get("status") != "FROZEN":
        raise ValueError("experiment specification is not frozen")
    discovery = tuple(spec["discovery_orders"])
    holdout = tuple(spec["holdout_orders"])
    if discovery[1] >= holdout[0]:
        raise ValueError("discovery and holdout order ranges must be disjoint")
    return spec


def experiment_corpus_rows(
    min_order: int,
    max_order: int,
    invariant_names: list[str],
    *,
    role: str,
    source_commit: str,
    experiment_id: str,
) -> list[dict[str, object]]:
    if role not in {"discovery", "holdout"}:
        raise ValueError("role must be discovery or holdout")
    registry = default_registry()
    rows = []
    parameters = {"min_order": min_order, "max_order": max_order}
    for graph in generate_unlabeled_trees(min_order, max_order):
        values = registry.compute(graph, invariant_names)
        rows.append(
            {
                "tree_code": canonical_tree_code(graph),
                "order": graph.number_of_nodes(),
                "corpus_role": role,
                "source_commit": source_commit,
                "experiment_id": experiment_id,
                "generation_parameters": parameters,
                **{key: value for key, value in values.items() if key != "order"},
            }
        )
    return rows
