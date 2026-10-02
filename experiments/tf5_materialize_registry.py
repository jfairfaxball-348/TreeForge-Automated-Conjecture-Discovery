#!/usr/bin/env python3
"""One-shot append-only TF5 materialization for TF-001028.

This script exists because the candidate registry is intentionally large and must
be updated append-only. It validates the exact expected TF4 terminal revision
before appending the TF5 KNOWN_RESULT event, and is idempotent thereafter.
"""

from __future__ import annotations

import json
from pathlib import Path

from treeforge.registry.schema import validate_candidate_record

REGISTRY = Path("data/registry/candidates.jsonl")
CANDIDATE_ID = "TF-001028"
CREATED_AT = "2026-10-02T14:06:00Z"
PRIOR_ART_STATUS = (
    "BOUNDED_AUDIT_COMPLETED; DIRECT_COROLLARY_OF_STRONGER_PRIOR_ART; "
    "GU-MENG-ZHANG-WAN 2013 LEMMA 2.3; ORE 1962; NOT_NOVEL"
)
INTERPRETATION = (
    "TF5 resolves the frozen all-tree statement as a direct corollary of prior art. "
    "K1 is equality. For n>=2 and D<=(n+2)/2, Ore's gamma<=n/2 gives "
    "3gamma+D<=2n+1. For D>=n/2+1, Gu, Meng, Zhang and Wan (2013), Lemma 2.3 "
    "gives gamma<=n-D+ceil((2D-n-1)/3); with integral x=2D-n-1, "
    "3ceil(x/3)<=x+2, yielding 3gamma+D<=2n+1. The integer ranges cover every "
    "diameter. The corona family P_k o K_1 is an infinite equality family "
    "(n=2k, gamma=k, D=k+1). This is a known-result consequence, not a TreeForge "
    "novelty claim, and it does not reach GRADUATION_CANDIDATE."
)


def _read_rows() -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in REGISTRY.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def main() -> None:
    rows = _read_rows()
    lineage = [row for row in rows if row.get("candidate_id") == CANDIDATE_ID]
    if not lineage:
        raise RuntimeError(f"{CANDIDATE_ID} missing from candidate registry")

    latest = lineage[-1]
    if latest.get("revision") == 7:
        if latest.get("lifecycle_state") != "KNOWN_RESULT":
            raise RuntimeError("TF-001028 revision 7 exists in an unexpected state")
        if latest.get("prior_art_status") != PRIOR_ART_STATUS:
            raise RuntimeError("TF-001028 revision 7 has unexpected prior-art status")
        print("TF-001028 revision 7 already materialized")
        return

    if latest.get("revision") != 6 or latest.get("lifecycle_state") != "NOVELTY_AUDIT":
        raise RuntimeError(
            "expected TF-001028 to end at revision 6 / NOVELTY_AUDIT before TF5"
        )

    event = dict(latest)
    event["revision"] = 7
    event["created_at"] = CREATED_AT
    event["lifecycle_state"] = "KNOWN_RESULT"
    event["prior_art_status"] = PRIOR_ART_STATUS
    event["mathematical_interpretation"] = INTERPRETATION
    validate_candidate_record(event)

    with REGISTRY.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n")

    print("appended TF-001028 revision 7 / KNOWN_RESULT")


if __name__ == "__main__":
    main()
