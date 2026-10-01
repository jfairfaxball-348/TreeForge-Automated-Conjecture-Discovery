"""Deterministic known-result adapter used only to validate TreeForge plumbing."""

from __future__ import annotations

from .txgraffiti_adapter import GeneratedStatement


class KnownIdentityCalibrationAdapter:
    engine = "treeforge-known-calibration"
    version = "1"

    def discover(self, rows: list[dict[str, object]]) -> list[GeneratedStatement]:
        if rows and all(row["edge_count"] == row["order"] - 1 for row in rows):
            return [
                GeneratedStatement(
                    statement="For every finite tree T, |E(T)| = |V(T)| - 1.",
                    engine=self.engine,
                    engine_version=self.version,
                )
            ]
        return []
