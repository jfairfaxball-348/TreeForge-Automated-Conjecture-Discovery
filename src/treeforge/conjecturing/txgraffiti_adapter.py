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
    metadata: dict[str, object] | None = None


class TxGraffitiAdapter:
    """Adapter for the public playground surface in TxGraffiti 0.4.1."""

    def __init__(self, loader=import_module) -> None:
        self._loader = loader

    @staticmethod
    def _normalize_hypothesis(hypothesis: list[Any] | None) -> list[Any] | None:
        # Upstream uses None for the always-true base predicate. An empty list
        # means iterate over no hypotheses, which invokes no generators.
        if hypothesis is None or len(hypothesis) == 0:
            return None
        return hypothesis

    def _load_surface(self):
        playground_mod = self._loader("txgraffiti.playground")
        generators = self._loader("txgraffiti.generators")
        heuristics = self._loader("txgraffiti.heuristics")
        processing = self._loader("txgraffiti.processing")
        return playground_mod, generators, heuristics, processing

    @staticmethod
    def _statement(playground, conjecture) -> GeneratedStatement:
        conclusion = getattr(conjecture, "conclusion", None)
        metadata = None
        if conclusion is not None:
            metadata = {
                "hypothesis": getattr(getattr(conjecture, "hypothesis", None), "name", None),
                "conclusion": getattr(conclusion, "name", str(conclusion)),
                "lhs": getattr(getattr(conclusion, "lhs", None), "name", None),
                "operator": getattr(conclusion, "op", None),
                "rhs": getattr(getattr(conclusion, "rhs", None), "name", None),
            }
            touch_count = getattr(conclusion, "touch_count", None)
            if callable(touch_count):
                metadata["discovery_touch_count"] = int(touch_count(playground.df))
            is_true = getattr(conjecture, "is_true", None)
            if callable(is_true):
                metadata["discovery_valid"] = bool(is_true(playground.df))
        return GeneratedStatement(
            statement=str(playground.forall(conjecture)),
            engine="TxGraffiti",
            engine_version=PINNED_VERSION,
            metadata=metadata,
        )

    def discover(
        self,
        dataframe: Any,
        *,
        target: str,
        features: list[str],
        object_symbol: str = "T",
        hypothesis: list[Any] | None = None,
    ) -> list[GeneratedStatement]:
        playground_mod, generators, heuristics, processing = self._load_surface()
        playground = playground_mod.ConjecturePlayground(dataframe, object_symbol=object_symbol)
        playground.discover(
            methods=[generators.convex_hull, generators.ratios],
            features=features,
            target=target,
            hypothesis=self._normalize_hypothesis(hypothesis),
            heuristics=[heuristics.morgan_accept, heuristics.dalmatian_accept],
            post_processors=[processing.remove_duplicates, processing.sort_by_touch_count],
        )
        return [self._statement(playground, conjecture) for conjecture in playground.conjectures]

    def pipeline_diagnostics(
        self,
        dataframe: Any,
        *,
        target: str,
        features: list[str],
        object_symbol: str = "T",
        hypothesis: list[Any] | None = None,
        preserve_empty_hypothesis: bool = False,
    ) -> dict[str, dict[str, object]]:
        """Inspect public pipeline stages without exposing TxGraffiti objects."""
        playground_mod, generators, heuristics, processing = self._load_surface()
        effective_hypothesis = (
            hypothesis if preserve_empty_hypothesis else self._normalize_hypothesis(hypothesis)
        )
        stages = [
            ("raw_generator_output", None, None),
            ("after_morgan", [heuristics.morgan_accept], None),
            (
                "after_dalmatian",
                [heuristics.morgan_accept, heuristics.dalmatian_accept],
                None,
            ),
            (
                "after_duplicate_removal",
                [heuristics.morgan_accept, heuristics.dalmatian_accept],
                [processing.remove_duplicates],
            ),
            (
                "after_touch_count_sort",
                [heuristics.morgan_accept, heuristics.dalmatian_accept],
                [processing.remove_duplicates, processing.sort_by_touch_count],
            ),
        ]
        result: dict[str, dict[str, object]] = {}
        for name, stage_heuristics, post_processors in stages:
            playground = playground_mod.ConjecturePlayground(
                dataframe, object_symbol=object_symbol
            )
            conjectures = list(
                playground.generate(
                    methods=[generators.convex_hull, generators.ratios],
                    features=features,
                    target=target,
                    hypothesis=effective_hypothesis,
                    heuristics=stage_heuristics,
                    post_processors=post_processors,
                )
            )
            statements = [self._statement(playground, conjecture) for conjecture in conjectures]
            result[name] = {
                "count": len(statements),
                "statements": [item.statement for item in statements],
            }
        return result

    def provenance(self) -> dict[str, str]:
        return {
            "package": "txgraffiti",
            "version": PINNED_VERSION,
            "source_commit": PINNED_SOURCE_COMMIT,
        }
