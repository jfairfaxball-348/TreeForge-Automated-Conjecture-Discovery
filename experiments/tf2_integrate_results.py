#!/usr/bin/env python3
"""Integrate the completed TF2-0001 Actions artifact without rerunning science."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

from treeforge.pipeline import stable_hash
from treeforge.registry.schema import validate_candidate_record

SOURCE = "4e25b666b4c650047387d131ce5d05ff5c693521"
RUN_ID = 36875119955
ARTIFACT_ID = 11180206717
DISCOVERY_HASH = "23a9f93eeeceb75ddfa670a4b869867194e8c04dd7afe0da187fcdee6233a4d4"
HOLDOUT_HASH = "7ddb31eaa17ea53045463968c21fe40f803e152d2054bd923d33632734bb9404"
ADVERSARIAL_HASH = "92957af1524dae77995776147b958a83e3cdd3d61cddf0cd3c48504ae9c859c2"
KNOWN = {"TF-000002", "TF-000010", "TF-000996"}
INTERESTING = "TF-000998"
SEARCH_TERMS = [
    '"domination number" "matching number" tree gamma nu bound',
    '"domination number" "matching number" trees 3/5',
    '"3/5" "domination number" tree matching',
    '"γ(G)" "3/5" "μ(G)" domination matching',
    '"domination number" "matching number" "lower bound" graph γ μ',
]
FEATURES = [
    "order", "leaf_count", "support_vertex_count", "max_degree", "diameter",
    "matching_number", "maximal_independent_set_count",
]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def append_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def newest(rows: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    result: dict[str, dict[str, object]] = {}
    for row in rows:
        cid = str(row["candidate_id"])
        if cid not in result or int(row["revision"]) > int(result[cid]["revision"]):
            result[cid] = row
    return result


def revise(record: dict[str, object], **changes: object) -> dict[str, object]:
    updated = json.loads(json.dumps(record))
    updated["revision"] = int(record["revision"]) + 1
    updated.update(changes)
    validate_candidate_record(updated)
    return updated


def generic_interpretation(record: dict[str, object]) -> dict[str, object]:
    meta = dict(record["discovery_evidence"]["structured_relation"])
    rhs = str(meta["rhs"])
    used = [name for name in FEATURES if re.search(rf"\b{re.escape(name)}\b", rhs)]
    touch = int(meta.get("discovery_touch_count", 0))
    sharp = sorted({int(x["order"]) for x in record.get("equality_or_sharp_examples", [])})
    direction = "upper" if str(meta["operator"]) in {"<", "<="} else "lower"
    text = (
        f"Finite {direction}-bound survivor from the frozen high-dimensional TxGraffiti hull. "
        f"Its RHS uses {len(used)} supplied features ({', '.join(used)}) and had discovery "
        f"touch count {touch}; retained sharp-example orders are {sharp}. The mixed coefficients "
        "do not expose a clear tree-structural mechanism or a cleaner mathematical question than "
        "the simple survivors isolated separately. It remains ADVERSARIAL_PASSED as finite evidence "
        "only and is not promoted to MATHEMATICALLY_INTERESTING."
    )
    return revise(
        record,
        lifecycle_state="ADVERSARIAL_PASSED",
        mathematical_interpretation=text,
        prior_art_status="NOT_STARTED; MATHEMATICAL_INTEREST_GATE_NOT_PASSED",
    )


def interpretation_events(record: dict[str, object]) -> list[dict[str, object]]:
    cid = str(record["candidate_id"])
    if cid == "TF-000002":
        return [
            revise(
                record,
                lifecycle_state="KNOWN_RESULT",
                mathematical_interpretation=(
                    "Known structural consequence. In a graph without isolated vertices every "
                    "vertex cover is a dominating set, so gamma <= tau. Trees are bipartite and "
                    "Konig's theorem gives tau = nu; hence gamma(T) <= nu(T)."
                ),
                prior_art_status="KNOWN_STANDARD_CONSEQUENCE; NO CANDIDATE-SPECIFIC SEARCH_REQUIRED",
            )
        ]
    if cid == "TF-000996":
        return [
            revise(
                record,
                lifecycle_state="KNOWN_RESULT",
                mathematical_interpretation=(
                    "Weak support-vertex consequence. For trees of order at least 3, a dominating "
                    "set must spend at least one vertex for each distinct support vertex/leaf "
                    "neighborhood, so gamma >= support_vertex_count. K2 has gamma=1 and "
                    "support_vertex_count=2. Thus gamma >= support_vertex_count/2 is immediate on "
                    "the frozen order>=2 universe and is not mathematically substantive."
                ),
                prior_art_status="KNOWN_STANDARD_CONSEQUENCE; NO CANDIDATE-SPECIFIC SEARCH_REQUIRED",
            )
        ]
    if cid == "TF-000010":
        return [
            revise(
                record,
                lifecycle_state="KNOWN_RESULT",
                mathematical_interpretation=(
                    "Known structural consequence. For trees of order at least 3, gamma >= "
                    "support_vertex_count, while max_degree <= leaf_count because each component "
                    "created by a maximum-degree vertex contains a distinct leaf. Therefore "
                    "max_degree - leaf_count + support_vertex_count <= gamma; K2 gives equality."
                ),
                prior_art_status="KNOWN_STANDARD_CONSEQUENCE; NO CANDIDATE-SPECIFIC SEARCH_REQUIRED",
            )
        ]
    if cid == INTERESTING:
        text = (
            "Substantive simple survivor gamma(T) >= 3/5 matching_number(T). It is sharp on the "
            "order-10 discovery tree ((((())))(((())))()) with gamma=3 and matching_number=5, "
            "and on four untouched order-12 trees. The frozen hostile set also survives; its "
            "smallest observed gamma/nu ratio is 2/3. The statement poses a clear extremal question "
            "about inf gamma(T)/nu(T) over finite trees and equality structure."
        )
        r5 = revise(
            record,
            lifecycle_state="MATHEMATICALLY_INTERESTING",
            mathematical_interpretation=text + " Finite survival is not proof.",
            prior_art_status="BOUNDED_SEARCH_REQUIRED",
        )
        audit = {
            "status": "BOUNDED_SEARCH_COMPLETE_NO_MATCH_LOCATED",
            "searched_on": "2026-10-01",
            "search_terms": SEARCH_TERMS,
            "sources": [
                "arXiv (direct inspection)",
                "web-indexed scholarly pages surfaced from DMGT, ScienceDirect, ResearchGate, MDPI, and related publisher/index pages",
            ],
            "close_results": [
                {
                    "citation": "Yair Caro, Randy Davila, Michael Henning, Ryan Pepper, Conjecture(s) of TxGraffiti: Independence, domination, and matchings, arXiv:2104.01092 (2021)",
                    "url": "https://arxiv.org/abs/2104.01092",
                    "relation": "Contains a distinct 3/5 lower bound for edge domination number versus matching number in connected cubic graphs, not ordinary domination number on trees.",
                },
                {
                    "relation": "Searches also surfaced the standard upper relation gamma(G) <= matching_number(G) for graphs without isolated vertices, not a lower bound matching TF-000998.",
                },
            ],
            "conclusion": "No matching prior result was located in the searched sources. This does not establish novelty; broader expert/literature review remains necessary.",
        }
        r6 = revise(
            r5,
            lifecycle_state="NOVELTY_AUDIT",
            prior_art_status=audit,
            mathematical_interpretation=(
                text + " A bounded candidate-specific prior-art search found no matching result "
                "in the searched sources; novelty remains unresolved and no graduation is warranted."
            ),
        )
        return [r5, r6]
    return [generic_interpretation(record)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-dir", type=Path, required=True)
    args = parser.parse_args()
    a = args.artifact_dir

    manifest = load_json(a / "manifest.json")
    raw = load_json(a / "raw_txgraffiti_output.json")
    events = load_jsonl(a / "candidate_events.jsonl")
    final = load_json(a / "final_candidates.json")
    discovery = load_jsonl(a / "discovery.jsonl")
    holdout = load_jsonl(a / "holdout.jsonl")
    adversarial = load_jsonl(a / "adversarial.jsonl")

    assert manifest["source_commit"] == SOURCE
    assert manifest["raw_candidate_count"] == len(raw) == 998
    assert manifest["discovery_hash"] == stable_hash(discovery) == DISCOVERY_HASH
    assert manifest["holdout_hash"] == stable_hash(holdout) == HOLDOUT_HASH
    assert manifest["adversarial_hash"] == stable_hash(adversarial) == ADVERSARIAL_HASH
    assert (len(discovery), len(holdout), len(adversarial)) == (200, 551, 26)
    assert all(int(row["order"]) != 11 for row in discovery + holdout + adversarial)
    assert [x["candidate_id"] for x in final] == [f"TF-{n:06d}" for n in range(2, 1000)]
    for row in events:
        validate_candidate_record(row)

    registry = Path("data/registry/candidates.jsonl")
    existing = load_jsonl(registry)
    if any(row.get("candidate_id") == "TF-000002" for row in existing):
        print("TF2 registry already integrated")
        return
    assert {row["candidate_id"] for row in existing} == {"TF-000001"}
    append_jsonl(registry, events)

    latest = newest(load_jsonl(registry))
    interpretations: list[dict[str, object]] = []
    for cid in manifest["adversarial_survivor_ids"]:
        produced = interpretation_events(latest[str(cid)])
        for row in produced:
            interpretations.append(row)
            latest[str(cid)] = row
    append_jsonl(registry, interpretations)

    experiments = Path("data/registry/experiments.jsonl")
    assert not any(
        row.get("experiment_id") == "TF2-0001" for row in load_jsonl(experiments)
    )
    append_jsonl(
        experiments,
        [{
            "experiment_id": "TF2-0001",
            "label": "CONTROLLED_DISCOVERY_AFTER_ADAPTER_SEMANTIC_CORRECTION",
            "created_at": "2026-10-01T12:34:00Z",
            "artifact_created_at": "2026-10-01T17:11:29Z",
            "source_commit": SOURCE,
            "scientific_github_actions_run": RUN_ID,
            "scientific_artifact_id": ARTIFACT_ID,
            "command": f"python experiments/tf2_discovery.py --spec experiments/TF2-0001/spec.json --output-dir <output-dir> --source-commit {SOURCE}",
            "dependencies": manifest["dependencies"],
            "txgraffiti_source_revision": manifest["txgraffiti_provenance"]["source_commit"],
            "generation_parameters": {
                "discovery_orders": [2, 10],
                "burned_orders_excluded": [11],
                "holdout_orders": [12, 12],
                "target": "domination_number",
                "discovery_features": FEATURES,
                "methods": ["convex_hull", "ratios"],
                "heuristics": ["morgan_accept", "dalmatian_accept"],
                "post_processors": ["remove_duplicates", "sort_by_touch_count"],
                "hypothesis_payload": [],
                "adapter_semantics": "empty TreeForge payload normalized to upstream None",
                "holdout_visible_to_generator": False,
            },
            "discovery_tree_count": 200,
            "discovery_data_hash": DISCOVERY_HASH,
            "holdout_tree_count": 551,
            "holdout_data_hash": HOLDOUT_HASH,
            "adversarial_tree_count": 26,
            "adversarial_data_hash": ADVERSARIAL_HASH,
            "raw_candidate_count": 998,
            "candidate_id_first": "TF-000002",
            "candidate_id_last": "TF-000999",
            "first_stage_counts": manifest["first_stage_state_counts"],
            "holdout_falsified_count": 924,
            "holdout_survivor_count": 74,
            "adversarial_falsified_count": 0,
            "adversarial_survivor_count": 74,
            "post_interpretation_known_result_count": 3,
            "mathematically_interesting_reached_count": 1,
            "bounded_prior_art_search_performed": True,
            "graduation_candidate_count": 0,
            "result": "TF2_COMPLETE; TF-000998_IN_NOVELTY_AUDIT",
        }],
    )

    out = Path("experiments/TF2-0001")
    shutil.copy2(a / "manifest.json", out / "manifest.json")
    shutil.copy2(a / "raw_txgraffiti_output.json", out / "raw_txgraffiti_output.json")
    write_json(out / "run_record.json", {
        "scientific_source_commit": SOURCE,
        "successful_github_actions_run": RUN_ID,
        "scientific_artifact_id": ARTIFACT_ID,
        "diagnostic_validation_run": 36855637323,
        "pre_merge_freeze_ci_run": 36864378120,
    })
    write_json(out / "stage_summary.json", {
        "final_TxGraffiti_statements_after_frozen_heuristics_and_postprocessors": 998,
        "earlier_internal_TxGraffiti_stage_counts_recorded_by_scientific_runner": False,
        "note": "No post-hoc scientific rerun was performed solely to reconstruct unrecorded internal stages.",
    })
    write_json(out / "first_stage_triage_summary.json", {
        "raw_candidate_count": 998,
        "candidate_ids": {"first": "TF-000002", "last": "TF-000999", "count": 998},
        **manifest["first_stage_state_counts"],
    })
    write_json(out / "holdout_result_summary.json", {
        "orders": [12, 12],
        "tree_count": 551,
        "hash": HOLDOUT_HASH,
        "holdout_visible_to_generator": False,
        "candidates_tested": 998,
        "falsified": 924,
        "survived": 74,
        "survivor_ids": manifest["holdout_survivor_ids"],
    })
    write_json(out / "adversarial_result_summary.json", {
        "tree_count": 26,
        "hash": ADVERSARIAL_HASH,
        "candidates_tested": 74,
        "falsified": 0,
        "survived": 74,
        "survivor_ids": manifest["adversarial_survivor_ids"],
    })
    write_json(out / "mathematical_interpretation_summary.json", {
        "adversarial_survivors_interpreted": 74,
        "reclassified_known_result_ids": sorted(KNOWN),
        "retained_adversarial_passed_without_interest_promotion_count": 70,
        "mathematically_interesting_reached_ids": [INTERESTING],
        "novelty_audit_ids": [INTERESTING],
        "prior_art_search_performed": True,
        "prior_art_search": latest[INTERESTING]["prior_art_status"],
        "graduation_candidate_count": 0,
    })
    print("Integrated TF2-0001 scientific artifact and interpretation revisions")


if __name__ == "__main__":
    main()
