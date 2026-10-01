"""Typed invariant registry."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import networkx as nx

InvariantFn = Callable[[nx.Graph], int | float | str]


@dataclass(frozen=True)
class InvariantSpec:
    name: str
    definition: str
    provenance: str
    exact: bool
    compute: InvariantFn


class InvariantRegistry:
    def __init__(self) -> None:
        self._specs: dict[str, InvariantSpec] = {}

    def register(self, spec: InvariantSpec) -> None:
        if spec.name in self._specs:
            raise ValueError(f"duplicate invariant: {spec.name}")
        self._specs[spec.name] = spec

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._specs))

    def spec(self, name: str) -> InvariantSpec:
        return self._specs[name]

    def compute(self, graph: nx.Graph, names: list[str] | tuple[str, ...]) -> dict[str, object]:
        return {name: self._specs[name].compute(graph) for name in names}


def default_registry() -> InvariantRegistry:
    from .core import CORE_INVARIANTS

    registry = InvariantRegistry()
    for spec in CORE_INVARIANTS:
        registry.register(spec)
    return registry
