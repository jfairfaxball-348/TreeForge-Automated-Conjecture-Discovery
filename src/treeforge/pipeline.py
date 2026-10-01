"""Reproducible small-corpus helpers shared by experiments and tests."""

from __future__ import annotations

import hashlib
import json
from importlib.metadata import PackageNotFoundError, version

from .invariants.registry import default_registry
from .trees.canonical import canonical_tree_code, generate_unlabeled_trees


def corpus_rows(min_order: int, max_order: int, invariant_names: list[str]) -> list[dict[str, object]]:
    registry = default_registry()
    rows = []
    for graph in generate_unlabeled_trees(min_order, max_order):
        row = {
            "tree_code": canonical_tree_code(graph),
            **registry.compute(graph, invariant_names),
        }
        rows.append(row)
    return rows


def stable_hash(rows: list[dict[str, object]]) -> str:
    payload = "\n".join(json.dumps(row, sort_keys=True, separators=(",", ":")) for row in rows)
    return hashlib.sha256(payload.encode()).hexdigest()


def dependency_versions(names: list[str]) -> dict[str, str]:
    result = {}
    for name in names:
        try:
            result[name] = version(name)
        except PackageNotFoundError:
            result[name] = "not-installed"
    return result
