#!/usr/bin/env python3
"""Append the two TF7 lifecycle revisions justified by the support/MIS theorem."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from treeforge.registry.schema import validate_candidate_record

CANDIDATE_REGISTRY = Path("data/registry/candidates.jsonl")
CREATED_AT = "2026-10-02T18:45:00Z"

INTERPRETATIONS = {
    "TF-001034": (
        "ARTIFACT_OF_FEATURE_SET: TF7 proves m(T) >= 3*support_vertex_count(T)-4 for every "
        "finite tree, via the stronger fixed-support Fibonacci bound away from the explicit P2 "
        "exception. Therefore TF-001091 has upper-bound RHS (m+2s+4)/5 <= (m+4)/3, the RHS "
        "of TF-001034, on every finite tree. TF-001034 is thus universally pointwise dominated "
        "by TF-001091. This does not prove TF-001091; that stronger sibling remains only "
        "ADVERSARIAL_PASSED finite evidence."
    ),
    "TF-001037": (
        "ARTIFACT_OF_FEATURE_SET: TF7 proves m(T) >= 5*support_vertex_count(T)-12 for every "
        "finite tree, via the stronger fixed-support Fibonacci bound away from the explicit P2 "
        "exception. Therefore TF-001095 has upper-bound RHS (m+3s+12)/8 <= (m+12)/5, the RHS "
        "of TF-001037, on every finite tree. TF-001037 is thus universally pointwise dominated "
        "by TF-001095. This does not prove TF-001095; that stronger sibling remains only "
        "ADVERSARIAL_PASSED finite evidence."
    ),
}


def _records(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def materialize(path: Path = CANDIDATE_REGISTRY) -> list[dict[str, object]]:
    records = _records(path)
    latest: dict[str, dict[str, object]] = {}
    for row in records:
        candidate_id = str(row["candidate_id"])
        if candidate_id in INTERPRETATIONS:
            latest[candidate_id] = row

    additions = []
    for candidate_id in INTERPRETATIONS:
        base = latest.get(candidate_id)
        if base is None:
            raise AssertionError(f"missing candidate {candidate_id}")
        if base["revision"] == 6 and base["lifecycle_state"] == "ARTIFACT_OF_FEATURE_SET":
            continue
        if base["revision"] != 5 or base["lifecycle_state"] != "ADVERSARIAL_PASSED":
            raise AssertionError(f"unexpected starting state for {candidate_id}")

        updated = json.loads(json.dumps(base))
        updated["revision"] = 6
        updated["created_at"] = CREATED_AT
        updated["lifecycle_state"] = "ARTIFACT_OF_FEATURE_SET"
        updated["prior_art_status"] = (
            "NOT_STARTED; UNIVERSALLY_DOMINATED_BY_STRONGER_DISCOVERED_FACET_"
            "VIA_TF7_SUPPORT_MIS_THEOREM"
        )
        updated["mathematical_interpretation"] = INTERPRETATIONS[candidate_id]
        validate_candidate_record(updated)
        additions.append(updated)

    if additions:
        with path.open("a", encoding="utf-8") as handle:
            for row in additions:
                handle.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")
    return additions


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=CANDIDATE_REGISTRY)
    args = parser.parse_args()
    additions = materialize(args.registry)
    print(json.dumps({"appended": [row["candidate_id"] for row in additions]}, sort_keys=True))


if __name__ == "__main__":
    main()
