"""Narrow adapter around the pinned TxGraffiti API."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from typing import Any

PINNED_VERSION = "0.4.1"
PINNED_SOURCE_COMMIT = "e37126da53b84150d142a5d61202b61f78521fcc"


@dataclass(frozen=True)
class GeneratedStatement:
    statement: str
    engine: str
    engine_version: str


class TxGraffitiAdapter:
    """Adapter for the `ConjecturePlayground.discover` interface in TxGraffiti 0.4.1."""

    def __init__(self, loader=import_module) -> None:
        self._loader = loader

    def discover(
        self,
        dataframe: Any,
        *,
        target: str,
        features: list[str],
        object_symbol: str = "T",
        hypothesis: list[Any] | None = None,
    ) -> list[GeneratedStatement]:
        playground_mod = self._loader("txgraffiti.playground")
        generators = self._loader("txgraffiti.generators")
        heuristics = self._loader("txgraffiti.heuristics")
        processing = self._loader("txgraffiti.processing")

        playground = playground_mod.ConjecturePlayground(dataframe, object_symbol=object_symbol)
        playground.discover(
            methods=[generators.convex_hull, generators.ratios],
            features=features,
            target=target,
            hypothesis=[] if hypothesis is None else hypothesis,
            heuristics=[heuristics.morgan_accept, heuristics.dalmatian_accept],
            post_processors=[processing.remove_duplicates, processing.sort_by_touch_count],
        )
        return [
            GeneratedStatement(
                statement=str(playground.forall(conjecture)),
                engine="TxGraffiti",
                engine_version=PINNED_VERSION,
            )
            for conjecture in playground.conjectures
        ]

    def provenance(self) -> dict[str, str]:
        return {
            "package": "txgraffiti",
            "version": PINNED_VERSION,
            "source_commit": PINNED_SOURCE_COMMIT,
        }
