from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Evaluation:
    passed: bool
    tested: int
    counterexamples: tuple[dict[str, object], ...]


def evaluate_identity(rows: list[dict[str, object]]) -> Evaluation:
    counterexamples = tuple(row for row in rows if row["edge_count"] != row["order"] - 1)
    return Evaluation(not counterexamples, len(rows), counterexamples)
