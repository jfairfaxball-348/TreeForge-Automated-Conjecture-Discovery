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
        self.last_stage_counts: dict[str, int] | None = None

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

    @staticmethod
    def _cached_always_true_heuristics(heuristics, target: str):
        """Return exact TF2-equivalent Morgan/Dalmatian filters with cached minima.

        With the normalized always-true hypothesis, every generated conjecture has
        the same hypothesis mask and the generators keep the target alone on the
        conclusion LHS. Upstream Morgan therefore cannot reject a conjecture: its
        only rejection requires a *strictly* more general existing hypothesis.

        Upstream Dalmatian compares each candidate RHS against the pointwise minimum
        of previously accepted upper-bound RHS values. Maintaining that minimum
        incrementally is exactly equivalent to rebuilding it with pandas.concat for
        every one of the tens of thousands of convex-hull facets.
        """

        counts = {
            "raw_generator_output": 0,
            "after_morgan": 0,
            "after_dalmatian": 0,
        }
        upper_min = None

        def morgan_equivalent(new_conj, existing, dataframe):
            del new_conj, existing, dataframe
            counts["raw_generator_output"] += 1
            counts["after_morgan"] += 1
            return True

        def dalmatian_equivalent(new_conj, existing, dataframe):
            nonlocal upper_min

            conclusion = getattr(new_conj, "conclusion", None)
            lhs = getattr(conclusion, "lhs", None)
            rhs = getattr(conclusion, "rhs", None)
            op = getattr(conclusion, "op", None)
            if (
                conclusion is None
                or getattr(lhs, "name", None) != target
                or rhs is None
            ):
                accepted = heuristics.dalmatian_accept(new_conj, existing, dataframe)
                if accepted:
                    counts["after_dalmatian"] += 1
                return accepted

            if not new_conj.is_true(dataframe):
                return False

            rhs_values = rhs(dataframe)
            accepted = upper_min is None or bool((rhs_values < upper_min).any())
            if not accepted:
                return False

            counts["after_dalmatian"] += 1
            if op in ("<=", "≤"):
                if upper_min is None:
                    upper_min = rhs_values.copy()
                else:
                    upper_min = upper_min.where(upper_min <= rhs_values, rhs_values)
            return True

        return morgan_equivalent, dalmatian_equivalent, counts

    @staticmethod
    def _select_methods(generators, methods: list[str] | None) -> list[Any]:
        names = methods or ["convex_hull", "ratios"]
        allowed = {"convex_hull", "ratios"}
        unknown = [name for name in names if name not in allowed]
        if unknown:
            raise ValueError(f"unsupported TxGraffiti method(s): {unknown}")
        return [getattr(generators, name) for name in names]

    def discover(
        self,
        dataframe: Any,
        *,
        target: str,
        features: list[str],
        object_symbol: str = "T",
        hypothesis: list[Any] | None = None,
        methods: list[str] | None = None,
    ) -> list[GeneratedStatement]:
        playground_mod, generators, heuristics, processing = self._load_surface()
        playground = playground_mod.ConjecturePlayground(dataframe, object_symbol=object_symbol)
        effective_hypothesis = self._normalize_hypothesis(hypothesis)
        active_methods = self._select_methods(generators, methods)

        if effective_hypothesis is None:
            morgan_filter, dalmatian_filter, counts = self._cached_always_true_heuristics(
                heuristics, target
            )
            active_heuristics = [morgan_filter, dalmatian_filter]
        else:
            counts = None
            active_heuristics = [heuristics.morgan_accept, heuristics.dalmatian_accept]

        playground.discover(
            methods=active_methods,
            features=features,
            target=target,
            hypothesis=effective_hypothesis,
            heuristics=active_heuristics,
            post_processors=[processing.remove_duplicates, processing.sort_by_touch_count],
        )

        if counts is not None:
            equality_count = sum(
                getattr(getattr(conjecture, "conclusion", None), "op", None) == "=="
                for conjecture in playground.conjectures
            )
            final_stage_count = len(playground.conjectures) - equality_count
            self.last_stage_counts = {
                **counts,
                "after_duplicate_removal": final_stage_count,
                "after_touch_count_sort": final_stage_count,
                "strengthened_equalities": equality_count,
                "final_discover_output": len(playground.conjectures),
            }
        else:
            self.last_stage_counts = None

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
