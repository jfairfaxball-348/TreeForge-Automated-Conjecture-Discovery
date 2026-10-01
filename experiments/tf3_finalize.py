#!/usr/bin/env python3
"""Materialize the audited TF3-0001 scientific artifact append-only."""

from __future__ import annotations

import argparse
import json
import shutil
from collections import Counter
from pathlib import Path

import networkx as nx

from experiments.tf2_discovery import _revision
from treeforge.conjecturing.expression import evaluate_relation
from treeforge.experiments import load_frozen_spec
from treeforge.invariants.registry import default_registry
from treeforge.pipeline import stable_hash
from treeforge.registry.schema import validate_candidate_record
from treeforge.trees.canonical import canonical_tree_code
from treeforge.trees.families import spider

EXPERIMENT_ID = "TF3-0001"
SCIENTIFIC_SOURCE_COMMIT = "e23b44d24a7b87d6f67aa18749059540934b2767"
SCIENTIFIC_RUN_ID = 36914647703
SCIENTIFIC_COMPLETED_AT = "2026-10-01T19:31:29Z"

EXPECTED_DISCOVERY_HASH = "e1fa7090640ba0254dba399082c436cf30742d7fe19ffef1d17028e7f45ab250"
EXPECTED_CANDIDATE_BATCH_HASH = "85669d95fb7199b720bfe488c606055dd5f38a5af157c1ed2bdb5f98710344c6"
EXPECTED_HOLDOUT_HASH = "5b02d81644415adc2df55d0a2ec3694125ef328cb1a0c4a2eeb733efaecef7e9"
EXPECTED_ADVERSARIAL_HASH = "37abd291592c4e98730d4dc8fef8c1678c4835ac87a555aad19edd5b75f14a18"

INTERPRETATION_AT = "2026-10-01T19:40:00Z"
EXPECTED_IDS = [f"TF-{number:06d}" for number in range(1000, 1012)]
HOLDOUT_SURVIVORS = ["TF-001000", "TF-001001", "TF-001006", "TF-001010"]


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _append_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")


def _write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _validate_preserving_tf0_legacy(record: dict[str, object]) -> None:
    if (
        record.get("candidate_id") == "TF-000001"
        and record.get("revision") == 1
        and "source_commit" not in record
    ):
        patched = dict(record)
        patched["source_commit"] = "LEGACY_TF0_REV1_SCHEMA_OMISSION"
        validate_candidate_record(patched)
    else:
        validate_candidate_record(record)


def _relation(record: dict[str, object]) -> dict[str, object]:
    return dict(record["discovery_evidence"]["structured_relation"])


def _row_for_graph(graph, invariant_names: list[str]) -> dict[str, object]:
    values = default_registry().compute(graph, invariant_names)
    return {"tree_code": canonical_tree_code(graph), **values}


def _counterexample_from_row(
    row: dict[str, object],
    relation: dict[str, object],
    *,
    source: str,
    reason: str,
    family: str | None = None,
    parameters: dict[str, object] | None = None,
) -> dict[str, object]:
    lhs = str(relation["lhs"])
    op = str(relation["operator"])
    rhs = str(relation["rhs"])
    if evaluate_relation(lhs, op, rhs, row):
        raise RuntimeError("claimed interpretation counterexample does not falsify relation")
    result: dict[str, object] = {
        "source": source,
        "tree_code": row["tree_code"],
        "order": row["order"],
        "lhs": lhs,
        "operator": op,
        "rhs": rhs,
        "values": dict(row),
        "reason": reason,
    }
    if family is not None:
        result["family"] = family
    if parameters is not None:
        result["parameters"] = parameters
    return result


def _interpret(
    final_candidates: list[dict[str, object]],
    invariant_names: list[str],
) -> tuple[list[dict[str, object]], dict[str, dict[str, object]]]:
    current = {str(row["candidate_id"]): row for row in final_candidates}
    survivors = sorted(
        cid for cid, row in current.items() if row["lifecycle_state"] == "ADVERSARIAL_PASSED"
    )
    if survivors != HOLDOUT_SURVIVORS:
        raise RuntimeError(f"unexpected TF3 finite survivors: {survivors}")

    events: list[dict[str, object]] = []

    k1 = nx.Graph()
    k1.add_node(0)
    k1_row = _row_for_graph(k1, invariant_names)
    if int(k1_row["order"]) != 1 or int(k1_row["domination_number"]) != 1:
        raise RuntimeError("K1 invariant sanity check failed")

    for candidate_id, explanation in [
        (
            "TF-001000",
            "The literal all-tree statement gamma(T) <= nu(T) is false on K1: "
            "gamma(K1)=1 and nu(K1)=0. A standard nontrivial-tree relation is nearby, "
            "and the same normalized relation appeared as TF-000002, but TF3 does not "
            "silently add an order-at-least-two hypothesis or rewrite the earlier lineage.",
        ),
        (
            "TF-001001",
            "The literal all-tree statement gamma(T) <= |V(T)|/2 is false on K1: "
            "gamma(K1)=1 > 1/2. The familiar no-isolated-vertices/nontrivial-tree bound "
            "does not rescue this frozen candidate because its recorded hypotheses do not "
            "exclude the one-vertex tree.",
        ),
    ]:
        record = current[candidate_id]
        counterexample = _counterexample_from_row(
            k1_row,
            _relation(record),
            source="post_frozen_mathematical_interpretation",
            reason=explanation,
            family="single_vertex_tree",
            parameters={"order": 1},
        )
        updated = _revision(
            record,
            created_at=INTERPRETATION_AT,
            lifecycle_state="FALSIFIED",
            counterexamples=[*record["counterexamples"], counterexample],
            prior_art_status="NOT_STARTED; ELEMENTARY_COUNTEREXAMPLE",
            mathematical_interpretation=explanation
            + " The order-13 and frozen hostile passes remain valid finite evidence only.",
        )
        validate_candidate_record(updated)
        events.append(updated)
        current[candidate_id] = updated

    record = current["TF-001006"]
    updated = _revision(
        record,
        created_at=INTERPRETATION_AT,
        lifecycle_state="TRIVIAL",
        prior_art_status="NOT_STARTED; ELEMENTARY_FEATURE_CONSEQUENCE",
        mathematical_interpretation=(
            "Elementary support-vertex consequence. For a tree of order at least 3, choose "
            "one leaf adjacent to each support vertex. The resulting support-leaf pairs are "
            "disjoint, and every dominating set must meet every pair, so gamma(T) is at least "
            "support_vertex_count(T). For K2, support_vertex_count=2 and gamma=1; for K1 the "
            "support count is 0. Therefore gamma(T) >= support_vertex_count(T)/2 for every "
            "finite tree. No prior-art search is warranted."
        ),
    )
    validate_candidate_record(updated)
    events.append(updated)
    current["TF-001006"] = updated

    record = current["TF-001010"]
    graph = spider([4, 4, 4, 4, 4, 4])
    spider_row = _row_for_graph(graph, invariant_names)
    if (
        int(spider_row["order"]) != 25
        or int(spider_row["domination_number"]) != 7
        or int(spider_row["matching_number"]) != 12
    ):
        raise RuntimeError("exposed TF-000998 counterexample no longer reproduces")
    explanation = (
        "Exact normalized duplicate of the relation investigated as TF-000998. The already-"
        "exposed TF2 interpretation counterexample applies unchanged: the six-arm spider with "
        "arms [4,4,4,4,4,4] has gamma=7 and nu=12, so 7 < 3*12/5. This exposed tree is used "
        "only for post-gate interpretation, not counted as fresh TF3 validation evidence."
    )
    counterexample = _counterexample_from_row(
        spider_row,
        _relation(record),
        source="post_frozen_mathematical_interpretation",
        reason=explanation,
        family="spider",
        parameters={"arms": [4, 4, 4, 4, 4, 4]},
    )
    updated = _revision(
        record,
        created_at=INTERPRETATION_AT,
        lifecycle_state="FALSIFIED",
        counterexamples=[*record["counterexamples"], counterexample],
        prior_art_status="NOT_STARTED; DUPLICATE_OF_FALSIFIED_TF-000998",
        mathematical_interpretation=explanation
        + " No new prior-art search is warranted because the candidate is already falsified.",
    )
    validate_candidate_record(updated)
    events.append(updated)
    current["TF-001010"] = updated

    return events, current


def _results_markdown(
    manifest: dict[str, object],
    completion: dict[str, object],
) -> str:
    stage = manifest["stage_counts"]
    return f"""# TF3-0001 result

TF3-0001 is scientifically complete. It is a controlled discovery/falsification experiment,
not a proof of any all-tree theorem.

## Provenance and frozen change

Scientific source commit: `{SCIENTIFIC_SOURCE_COMMIT}`  
Successful GitHub Actions run: `{SCIENTIFIC_RUN_ID}`  
TxGraffiti: `0.4.1`, upstream revision
`e37126da53b84150d142a5d61202b61f78521fcc`

Exactly one material discovery axis changed from TF2: methods
`[convex_hull, ratios]` became `[ratios]`. The target, seven supplied features,
Morgan/Dalmatian heuristics, duplicate removal, touch-count sorting, and empty-hypothesis-to-
upstream-`None` semantics remained frozen.

Two earlier Actions attempts, `36914094286` and `36914294452`, failed at Python import
before the runner entered discovery; they produced no candidates or validation evidence and are
recorded in the failure ledger. The successful source commit above used module invocation only;
the frozen scientific specification was unchanged.

## Discovery and candidate-batch firewall

Discovery corpus: all {manifest['discovery_tree_count']} unlabeled trees of orders 2-10.  
Discovery SHA-256: `{manifest['discovery_hash']}`

Pipeline counts:

- raw ratio generator output: {stage['raw_generator_output']}
- after Morgan: {stage['after_morgan']}
- after Dalmatian: {stage['after_dalmatian']}
- after duplicate removal: {stage['after_duplicate_removal']}
- final: {manifest['raw_candidate_count']}

All final statements satisfied the frozen one-RHS-feature grammar. Every statement received a
permanent ID, `TF-001000` through `TF-001011`, before fresh holdout construction.
Candidate-batch SHA-256: `{manifest['candidate_batch_hash']}`.

The persisted batch-freeze record says `holdout_constructed: false`; the runner and its
regression test both enforce that the order-13 corpus is constructed only below that point.

## Fresh order-13 holdout

Fresh holdout: all {manifest['holdout_tree_count']} unlabeled trees of order 13.  
Holdout SHA-256: `{manifest['holdout_hash']}`

All 12 frozen candidates were tested. Eight were falsified and four survived:
`TF-001000`, `TF-001001`, `TF-001006`, and `TF-001010`.
The committed holdout summary preserves each deterministic first counterexample for the eight
failures. Finite survival is not proof.

## Fresh pre-frozen hostile set

Only the four holdout survivors were tested on the pre-frozen TF3 hostile set.
The set contains {manifest['adversarial_tree_count']} trees and has SHA-256
`{manifest['adversarial_hash']}`. No survivor failed this finite hostile gate, so all four
temporarily reached `ADVERSARIAL_PASSED`.

## Mathematical interpretation

Interpretation did not force a survivor.

- `TF-001000`, `gamma <= nu`, is falsified by `K1` under the literal frozen all-tree
  hypotheses: `gamma(K1)=1`, `nu(K1)=0`.
- `TF-001001`, `gamma <= n/2`, is likewise falsified by `K1`.
- `TF-001006`, `gamma >= support_vertex_count/2`, is `TRIVIAL`: for order at least 3,
  disjoint support-leaf pairs give the stronger elementary bound `gamma >= support_vertex_count`;
  `K2` supplies the exceptional factor-1/2 equality and `K1` is immediate.
- `TF-001010`, `gamma >= 3 nu/5`, is the same normalized relation already examined as
  `TF-000998`; the exposed order-25 spider with six length-4 arms again gives
  `gamma=7`, `nu=12`, and falsifies it. This is interpretation evidence, not fresh TF3
  validation evidence.

Final interpreted states are {completion['final_state_counts']}. No TF3 candidate reaches
`MATHEMATICALLY_INTERESTING`, no new prior-art search is performed, no candidate reaches
`GRADUATION_CANDIDATE`, and no theorem or novelty claim is made.

## Reproducibility

The compact scientific record commits the raw TxGraffiti output, stage counts, normalized
candidate batch and batch-freeze hash, holdout/adversarial summaries, interpretation summary,
and append-only candidate/experiment registry revisions. The discovery and validation row files
remain deterministic generated data; their exact counts and hashes are recorded and reproduced by
the TF3 result tests.
"""


def run(artifact_dir: Path) -> dict[str, object]:
    manifest = _read_json(artifact_dir / "manifest.json")
    raw = _read_json(artifact_dir / "raw_txgraffiti_output.json")
    batch = _read_json(artifact_dir / "candidate_batch.json")
    freeze = _read_json(artifact_dir / "candidate_batch_freeze.json")
    events = _read_jsonl(artifact_dir / "candidate_events.jsonl")
    final_candidates = _read_json(artifact_dir / "final_candidates.json")
    discovery = _read_jsonl(artifact_dir / "discovery.jsonl")
    holdout = _read_jsonl(artifact_dir / "holdout.jsonl")
    adversarial = _read_jsonl(artifact_dir / "adversarial.jsonl")

    if manifest["experiment_id"] != EXPERIMENT_ID:
        raise RuntimeError("wrong TF3 artifact")
    if manifest["source_commit"] != SCIENTIFIC_SOURCE_COMMIT:
        raise RuntimeError("scientific source commit mismatch")
    if manifest["dependencies"] != {
        "networkx": "3.6.1",
        "pandas": "3.0.6",
        "txgraffiti": "0.4.1",
    }:
        raise RuntimeError("unexpected scientific dependency versions")
    if manifest["methods"] != ["ratios"]:
        raise RuntimeError("frozen method set changed")
    if manifest["stage_counts"] != {
        "raw_generator_output": 14,
        "after_morgan": 14,
        "after_dalmatian": 12,
        "after_duplicate_removal": 12,
        "after_touch_count_sort": 12,
        "strengthened_equalities": 0,
        "final_discover_output": 12,
    }:
        raise RuntimeError("unexpected TF3 stage counts")
    if manifest["raw_candidate_count"] != 12 or len(raw) != 12:
        raise RuntimeError("unexpected TF3 candidate count")
    if manifest["candidate_ids"] != EXPECTED_IDS or manifest["candidate_batch_ids"] != EXPECTED_IDS:
        raise RuntimeError("unexpected TF3 candidate IDs")
    if manifest["candidate_batch_frozen_before_holdout"] is not True:
        raise RuntimeError("candidate-batch firewall flag missing")
    if freeze["holdout_constructed"] is not False or freeze["candidate_ids"] != EXPECTED_IDS:
        raise RuntimeError("candidate batch freeze record invalid")
    if manifest["holdout_visible_to_generator"] is not False:
        raise RuntimeError("holdout leakage flag invalid")

    checks = [
        (stable_hash(discovery), EXPECTED_DISCOVERY_HASH, "discovery"),
        (stable_hash(batch), EXPECTED_CANDIDATE_BATCH_HASH, "candidate batch"),
        (stable_hash(holdout), EXPECTED_HOLDOUT_HASH, "holdout"),
        (stable_hash(adversarial), EXPECTED_ADVERSARIAL_HASH, "adversarial"),
    ]
    for actual, expected, label in checks:
        if actual != expected:
            raise RuntimeError(f"{label} hash mismatch")
    if (
        manifest["discovery_hash"] != EXPECTED_DISCOVERY_HASH
        or manifest["candidate_batch_hash"] != EXPECTED_CANDIDATE_BATCH_HASH
        or manifest["holdout_hash"] != EXPECTED_HOLDOUT_HASH
        or manifest["adversarial_hash"] != EXPECTED_ADVERSARIAL_HASH
    ):
        raise RuntimeError("manifest hash mismatch")
    if len(discovery) != 200 or len(holdout) != 1301 or len(adversarial) != 18:
        raise RuntimeError("unexpected corpus size")
    if manifest["first_stage_state_counts"]["CONJECTURED"] != 12:
        raise RuntimeError("unexpected discovery-side triage")
    if manifest["holdout_survivor_count"] != 4:
        raise RuntimeError("unexpected holdout survivor count")

    for record in events:
        validate_candidate_record(record)
    artifact_ids = sorted({str(row["candidate_id"]) for row in events})
    if artifact_ids != EXPECTED_IDS:
        raise RuntimeError("artifact candidate ID range mismatch")

    registry_path = Path("data/registry/candidates.jsonl")
    existing = _read_jsonl(registry_path)
    for record in existing:
        _validate_preserving_tf0_legacy(record)
    existing_ids = sorted({str(row["candidate_id"]) for row in existing})
    if existing_ids != [f"TF-{number:06d}" for number in range(1, 1000)]:
        raise RuntimeError("candidate registry advanced unexpectedly before TF3 finalization")

    _append_jsonl(registry_path, events)

    spec = load_frozen_spec(Path("experiments/TF3-0001/spec.json"))
    interpretation_events, interpreted = _interpret(final_candidates, list(spec["corpus_invariants"]))
    _append_jsonl(registry_path, interpretation_events)

    final_state_counts = dict(
        sorted(Counter(str(row["lifecycle_state"]) for row in interpreted.values()).items())
    )
    if final_state_counts != {"FALSIFIED": 11, "TRIVIAL": 1}:
        raise RuntimeError(f"unexpected final TF3 states: {final_state_counts}")

    experiment_dir = Path("experiments/TF3-0001")
    experiment_dir.mkdir(parents=True, exist_ok=True)
    for filename in [
        "manifest.json",
        "stage_counts.json",
        "raw_txgraffiti_output.json",
        "candidate_batch.json",
        "candidate_batch_freeze.json",
    ]:
        shutil.copyfile(artifact_dir / filename, experiment_dir / filename)

    holdout_falsified_ids = sorted(
        cid
        for cid, row in {str(x["candidate_id"]): x for x in final_candidates}.items()
        if row["holdout_status"].get("status") == "FAILED"
    )
    _write_json(
        experiment_dir / "holdout_summary.json",
        {
            "orders": [13, 13],
            "tree_count": 1301,
            "dataset_hash": EXPECTED_HOLDOUT_HASH,
            "candidate_batch_hash": EXPECTED_CANDIDATE_BATCH_HASH,
            "visible_to_generator": False,
            "tested_candidate_count": 12,
            "falsified_count": 8,
            "falsified_ids": holdout_falsified_ids,
            "survivor_count": 4,
            "survivor_ids": HOLDOUT_SURVIVORS,
            "first_counterexamples": {
                str(row["candidate_id"]): row["counterexamples"][0]
                for row in final_candidates
                if row["holdout_status"].get("status") == "FAILED"
            },
        },
    )
    _write_json(
        experiment_dir / "adversarial_summary.json",
        {
            "tree_count": 18,
            "dataset_hash": EXPECTED_ADVERSARIAL_HASH,
            "candidate_batch_hash": EXPECTED_CANDIDATE_BATCH_HASH,
            "tested_candidate_count": 4,
            "tested_candidate_ids": HOLDOUT_SURVIVORS,
            "falsified_count": 0,
            "survivor_count": 4,
            "survivor_ids": HOLDOUT_SURVIVORS,
            "note": "Exactly the pre-frozen TF3-0001 fresh hostile instances were used.",
        },
    )

    completion = {
        "experiment_id": EXPERIMENT_ID,
        "scientific_source_commit": SCIENTIFIC_SOURCE_COMMIT,
        "successful_scientific_actions_run": SCIENTIFIC_RUN_ID,
        "scientific_completed_at": SCIENTIFIC_COMPLETED_AT,
        "candidate_id_range": ["TF-001000", "TF-001011"],
        "raw_generator_count": 14,
        "post_morgan_count": 14,
        "post_dalmatian_count": 12,
        "post_duplicate_count": 12,
        "final_candidate_count": 12,
        "candidate_batch_hash": EXPECTED_CANDIDATE_BATCH_HASH,
        "holdout_tree_count": 1301,
        "holdout_hash": EXPECTED_HOLDOUT_HASH,
        "holdout_falsified_count": 8,
        "holdout_survivor_count": 4,
        "adversarial_tree_count": 18,
        "adversarial_hash": EXPECTED_ADVERSARIAL_HASH,
        "adversarial_falsified_count": 0,
        "adversarial_survivor_count": 4,
        "final_state_counts": final_state_counts,
        "mathematically_interesting_reached_count": 0,
        "prior_art_search_performed": False,
        "graduation_candidate_count": 0,
        "pre_execution_failure_runs": [36914094286, 36914294452],
    }
    _write_json(
        experiment_dir / "interpretation_summary.json",
        {
            **completion,
            "literal_k1_falsified_ids": ["TF-001000", "TF-001001"],
            "trivial_ids": ["TF-001006"],
            "historical_duplicate_falsified_ids": {"TF-001010": "TF-000998"},
            "final_records": {cid: interpreted[cid] for cid in EXPECTED_IDS},
        },
    )
    (experiment_dir / "RESULTS.md").write_text(
        _results_markdown(manifest, completion), encoding="utf-8"
    )

    experiments_path = Path("data/registry/experiments.jsonl")
    experiments = _read_jsonl(experiments_path)
    if any(row.get("experiment_id") == EXPERIMENT_ID for row in experiments):
        raise RuntimeError("TF3-0001 experiment registry record already exists")
    experiment_record = {
        "experiment_id": EXPERIMENT_ID,
        "label": "CONTROLLED_DISCOVERY",
        "created_at": spec["frozen_at"],
        "completed_at": SCIENTIFIC_COMPLETED_AT,
        "source_commit": SCIENTIFIC_SOURCE_COMMIT,
        "scientific_actions_run": SCIENTIFIC_RUN_ID,
        "command": (
            "python -m experiments.tf3_discovery --spec experiments/TF3-0001/spec.json "
            "--output-dir /tmp/tf3-0001 --source-commit " + SCIENTIFIC_SOURCE_COMMIT
        ),
        "dependencies": manifest["dependencies"],
        "txgraffiti_source_revision": manifest["txgraffiti_provenance"]["source_commit"],
        "generation_parameters": {
            "spec": "experiments/TF3-0001/spec.json",
            "discovery_orders": spec["discovery_orders"],
            "burned_or_exposed_orders": spec["burned_or_exposed_orders"],
            "holdout_orders": spec["holdout_orders"],
            "target": spec["target"],
            "discovery_features": spec["discovery_features"],
            "methods": spec["txgraffiti"]["methods"],
            "heuristics": spec["txgraffiti"]["heuristics"],
            "post_processors": spec["txgraffiti"]["post_processors"],
            "hypothesis_payload": spec["txgraffiti"]["hypothesis_payload"],
            "adapter_semantics": spec["txgraffiti"]["adapter_semantics"],
            "candidate_batch_frozen_before_holdout": True,
            "holdout_visible_to_generator": False,
        },
        "discovery_data_hash": EXPECTED_DISCOVERY_HASH,
        "candidate_batch_hash": EXPECTED_CANDIDATE_BATCH_HASH,
        "holdout_data_hash": EXPECTED_HOLDOUT_HASH,
        "adversarial_data_hash": EXPECTED_ADVERSARIAL_HASH,
        "stage_counts": manifest["stage_counts"],
        "raw_candidate_count": 12,
        "candidate_ids": EXPECTED_IDS,
        "first_stage_state_counts": manifest["first_stage_state_counts"],
        "holdout_falsified_count": 8,
        "holdout_survivor_count": 4,
        "adversarial_falsified_count": 0,
        "adversarial_survivor_count": 4,
        "mathematically_interesting_reached_count": 0,
        "prior_art_search_performed": False,
        "graduation_candidate_count": 0,
        "final_state_counts": final_state_counts,
        "result": (
            "12_RATIOS_ONLY_CONJECTURED;8_FRESH_ORDER13_HOLDOUT_FALSIFIED;"
            "4_FROZEN_ADVERSARIAL_SURVIVORS;POST_INTERPRETATION_11_FALSIFIED_1_TRIVIAL;"
            "NO_MATHEMATICALLY_INTERESTING;NO_GRADUATION_CANDIDATE"
        ),
    }
    _append_jsonl(experiments_path, [experiment_record])

    all_records = _read_jsonl(registry_path)
    per_id: dict[str, list[int]] = {}
    for record in all_records:
        _validate_preserving_tf0_legacy(record)
        per_id.setdefault(str(record["candidate_id"]), []).append(int(record["revision"]))
    expected_all_ids = [f"TF-{number:06d}" for number in range(1, 1012)]
    if sorted(per_id) != expected_all_ids:
        raise RuntimeError("final candidate registry ID sequence is not contiguous through TF-001011")
    for candidate_id, revisions in per_id.items():
        if revisions != sorted(revisions) or len(revisions) != len(set(revisions)):
            raise RuntimeError(f"non-monotone/duplicate revisions for {candidate_id}")

    print(json.dumps(completion, indent=2, sort_keys=True))
    return completion


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-dir", type=Path, required=True)
    args = parser.parse_args()
    run(args.artifact_dir)


if __name__ == "__main__":
    main()
