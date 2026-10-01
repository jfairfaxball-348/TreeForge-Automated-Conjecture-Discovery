#!/usr/bin/env python3
"""Finalize the already-completed TF2-0001 scientific artifact into repository records."""

from __future__ import annotations

import argparse
import json
import shutil
from collections import Counter
from pathlib import Path

from treeforge.invariants.registry import default_registry
from treeforge.registry.schema import validate_candidate_record
from treeforge.trees.canonical import canonical_tree_code
from treeforge.trees.families import spider

EXPERIMENT_ID = "TF2-0001"
SCIENTIFIC_SOURCE_COMMIT = "d091d88889fa72322bfc49a5531bc30b1f31b049"
SCIENTIFIC_RUN_ID = 36888114138
SCIENTIFIC_COMPLETED_AT = "2026-10-01T15:59:16Z"
EXPECTED_DISCOVERY_HASH = "40bc528cd8b035854de816a1fbd37f1c6d688b2b1686d006387fb16dc8f5c4a8"
EXPECTED_HOLDOUT_HASH = "ea9f5d200ec503090499b4744338a5e39a37b7412d21ed5f6f876e2129be9433"
EXPECTED_ADVERSARIAL_HASH = "dea3af9c495cc79da46b7ed3797276caae22495bc86d5000ddea3605a07bcb8a"

INTERPRETATION_AT = "2026-10-01T16:05:00Z"
PRIOR_ART_AT = "2026-10-01T16:10:00Z"
FALSIFICATION_AT = "2026-10-01T16:20:00Z"

SPECIAL_IDS = {"TF-000002", "TF-000010", "TF-000996", "TF-000998"}


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


def _validate_registry_record(record: dict[str, object]) -> None:
    """Validate current-schema records while preserving the original TF0 rev1."""
    if (
        record.get("candidate_id") == "TF-000001"
        and record.get("revision") == 1
        and "source_commit" not in record
    ):
        patched = dict(record)
        patched["source_commit"] = "LEGACY_TF0_REV1_SCHEMA_OMISSION"
        validate_candidate_record(patched)
        return
    validate_candidate_record(record)


def _revision(
    record: dict[str, object],
    *,
    created_at: str,
    lifecycle_state: str,
    mathematical_interpretation: str,
    prior_art_status: object | None = None,
    counterexamples: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    updated = json.loads(json.dumps(record))
    updated["revision"] = int(record["revision"]) + 1
    updated["created_at"] = created_at
    updated["lifecycle_state"] = lifecycle_state
    updated["mathematical_interpretation"] = mathematical_interpretation
    if prior_art_status is not None:
        updated["prior_art_status"] = prior_art_status
    if counterexamples is not None:
        updated["counterexamples"] = counterexamples
    validate_candidate_record(updated)
    return updated


def _generic_interpretation(record: dict[str, object]) -> str:
    relation = record["discovery_evidence"]["structured_relation"]
    rhs = str(relation["rhs"])
    touch = int(relation.get("discovery_touch_count", 0))
    sharp = record.get("equality_or_sharp_examples", [])
    sharp_text = (
        ", ".join(f"order {item['order']} code {item['tree_code']}" for item in sharp[:3])
        if sharp
        else "no discovery equality example retained"
    )
    return (
        "Finite adversarial survivor after exact discovery and untouched order-12 testing. "
        f"The normalized RHS is {rhs}; it was tight on {touch} discovery rows "
        f"(examples: {sharp_text}). The statement is a high-dimensional convex-hull facet "
        "mixing several supplied invariants. No stable tree-structural mechanism or simple "
        "standard invariant consequence was identified during TF2 interpretation, so it is "
        "not promoted beyond ADVERSARIAL_PASSED. Finite survival is not proof."
    )


def _tf998_counterexample() -> dict[str, object]:
    graph = spider([4, 4, 4, 4, 4, 4])
    names = [
        "order",
        "matching_number",
        "domination_number",
        "max_degree",
        "leaf_count",
        "support_vertex_count",
        "diameter",
    ]
    values = default_registry().compute(graph, names)
    if values["order"] != 25 or values["matching_number"] != 12 or values["domination_number"] != 7:
        raise RuntimeError("TF-000998 mathematical counterexample no longer reproduces")
    return {
        "source": "mathematical_interpretation",
        "family": "spider",
        "parameters": {"arms": [4, 4, 4, 4, 4, 4]},
        "tree_code": canonical_tree_code(graph),
        "order": values["order"],
        "lhs": "domination_number",
        "operator": ">=",
        "rhs": "(3/5 * matching_number)",
        "values": values,
        "reason": (
            "For the six-arm length-4 spider, choosing the center and the six vertices "
            "at distance 3 from the center gives a dominating set of size 7. Conversely, "
            "each terminal leaf forces one selected vertex from its final edge, and with "
            "only those six selections the six vertices at distance 1 from the center "
            "cannot all be dominated, so gamma=7. Two disjoint edges can be selected on "
            "each arm, giving a matching of size 12; order 25 gives the matching upper "
            "bound floor(25/2)=12. Hence 7 < (3/5)*12."
        ),
    }


def _interpret_survivors(
    final_candidates: list[dict[str, object]],
) -> tuple[list[dict[str, object]], dict[str, dict[str, object]]]:
    current = {str(record["candidate_id"]): record for record in final_candidates}
    survivors = sorted(
        candidate_id
        for candidate_id, record in current.items()
        if record["lifecycle_state"] == "ADVERSARIAL_PASSED"
    )
    if len(survivors) != 74:
        raise RuntimeError("expected exactly 74 adversarial survivors before interpretation")

    events: list[dict[str, object]] = []

    for candidate_id in survivors:
        if candidate_id in SPECIAL_IDS:
            continue
        record = current[candidate_id]
        updated = _revision(
            record,
            created_at=INTERPRETATION_AT,
            lifecycle_state="ADVERSARIAL_PASSED",
            mathematical_interpretation=_generic_interpretation(record),
        )
        events.append(updated)
        current[candidate_id] = updated

    record = current["TF-000002"]
    updated = _revision(
        record,
        created_at=INTERPRETATION_AT,
        lifecycle_state="KNOWN_RESULT",
        mathematical_interpretation=(
            "Classified as a standard elementary relation, not a new conjecture. "
            "For a connected graph without isolated vertices, a maximum matching can be "
            "oriented by choosing one endpoint from each matched edge so that all unmatched "
            "vertices are dominated; thus gamma(G) <= nu(G). In particular this applies to "
            "every nontrivial tree. The 149 discovery equality cases are calibration-like "
            "evidence for a known relation, not novelty."
        ),
        prior_art_status="KNOWN_STANDARD_RELATION; NO NOVELTY SEARCH REQUIRED",
    )
    events.append(updated)
    current["TF-000002"] = updated

    record = current["TF-000010"]
    updated = _revision(
        record,
        created_at=INTERPRETATION_AT,
        lifecycle_state="TRIVIAL",
        mathematical_interpretation=(
            "Classified as an elementary consequence of the supplied tree features. "
            "For every tree of order at least 3, each support vertex has a private terminal "
            "leaf constraint, so gamma(T) >= support_vertex_count(T); also every branch of a "
            "maximum-degree vertex contains a distinct leaf, so leaf_count(T) >= max_degree(T). "
            "Therefore support_vertex_count + max_degree - leaf_count <= gamma. The order-2 "
            "tree satisfies the displayed TF-000010 inequality directly. No prior-art search "
            "is warranted for this elementary consequence."
        ),
        prior_art_status="NOT_STARTED; ELEMENTARY_FEATURE_CONSEQUENCE",
    )
    events.append(updated)
    current["TF-000010"] = updated

    record = current["TF-000996"]
    updated = _revision(
        record,
        created_at=INTERPRETATION_AT,
        lifecycle_state="TRIVIAL",
        mathematical_interpretation=(
            "Classified as a weak elementary support-vertex bound. For every tree of order "
            "at least 3, gamma(T) >= support_vertex_count(T) by the terminal-leaf constraints "
            "at distinct support vertices. For K2, support_vertex_count=2 and gamma=1, so the "
            "factor 1/2 is met with equality. Hence gamma >= support_vertex_count/2 follows by "
            "a direct case split and does not merit mathematical-interest promotion."
        ),
        prior_art_status="NOT_STARTED; ELEMENTARY_FEATURE_CONSEQUENCE",
    )
    events.append(updated)
    current["TF-000996"] = updated

    record = current["TF-000998"]
    interesting = _revision(
        record,
        created_at=INTERPRETATION_AT,
        lifecycle_state="MATHEMATICALLY_INTERESTING",
        mathematical_interpretation=(
            "Initial interpretation gate passed because this is a simple two-invariant bound, "
            "gamma(T) >= 3*nu(T)/5, rather than an opaque high-dimensional facet. It is sharp "
            "on the order-10 discovery spider with arms [1,4,4] (gamma=3, nu=5), and it survived "
            "the untouched order-12 holdout and all frozen TF2 adversarial instances. This "
            "promotion records a research question only; finite survival is not proof."
        ),
    )
    events.append(interesting)

    prior_art = {
        "status": "BOUNDED_SEARCH_COMPLETE",
        "performed": True,
        "date": "2026-10-01",
        "search_terms": [
            "\"domination number\" \"matching number\" tree \"3/5\"",
            "\"domination number\" \"matching number\" trees \"3/5\"",
            "\"gamma(T)\" \"3/5\" \"matching number\" tree",
            "\"lower bound\" \"domination number\" tree \"matching number\"",
        ],
        "sources": [
            {
                "citation": (
                    "E. DeLaVina, R. Pepper, B. Waller, Lower Bounds for the Domination "
                    "Number, Discussiones Mathematicae Graph Theory 30 (2010), 475-487"
                ),
                "note": (
                    "Relevant lower bound uses the minimum cardinality of a maximal matching, "
                    "not the maximum matching number in TF-000998."
                ),
            },
            {
                "citation": (
                    "Y. Caro, R. Davila, M.A. Henning, R. Pepper, Conjectures of TxGraffiti: "
                    "Independence, domination, and matchings, Australas. J. Comb. 84(2) "
                    "(2022), 258-274; arXiv:2104.01092"
                ),
                "note": (
                    "Contains a distinct 3/5 theorem for edge domination number versus maximum "
                    "matching number in connected cubic graphs; it is not ordinary domination "
                    "for trees."
                ),
            },
            {
                "citation": "A Survey on Characterizing Trees Using Domination Number (2022)",
                "note": "No matching ordinary-domination/maximum-matching 3/5 tree result located.",
            },
        ],
        "result": (
            "No matching prior result was located in the searched sources. This is not a "
            "novelty claim."
        ),
    }
    audited = _revision(
        interesting,
        created_at=PRIOR_ART_AT,
        lifecycle_state="NOVELTY_AUDIT",
        mathematical_interpretation=(
            interesting["mathematical_interpretation"]
            + " A bounded candidate-specific prior-art search found nearby but materially "
            "different matching/domination results and no exact match in the searched sources."
        ),
        prior_art_status=prior_art,
    )
    events.append(audited)

    counterexample = _tf998_counterexample()
    falsified = _revision(
        audited,
        created_at=FALSIFICATION_AT,
        lifecycle_state="FALSIFIED",
        mathematical_interpretation=(
            "Falsified during deeper mathematical interpretation after the finite gates and "
            "bounded prior-art audit. The six-arm spider with all arms of length 4 has order "
            "25, domination number 7, and matching number 12, so the claimed lower bound "
            "requires 7 >= 36/5 and fails. The finite order-12 and frozen adversarial passes "
            "remain valid historical evidence but do not support an infinite statement."
        ),
        prior_art_status=prior_art,
        counterexamples=[*audited["counterexamples"], counterexample],
    )
    events.append(falsified)
    current["TF-000998"] = falsified

    return events, current


def _results_markdown(
    manifest: dict[str, object],
    completion: dict[str, object],
) -> str:
    stage = manifest["stage_counts"]
    return f"""# TF2-0001 result

TF2-0001 is scientifically complete. It is a controlled discovery/falsification experiment,
not a proof of any all-tree theorem.

## Provenance and frozen split

Scientific source commit: `{SCIENTIFIC_SOURCE_COMMIT}`  
Successful GitHub Actions run: `{SCIENTIFIC_RUN_ID}`  
TxGraffiti: `0.4.1`, upstream revision `e37126da53b84150d142a5d61202b61f78521fcc`

Discovery corpus: all {manifest['discovery_tree_count']} unlabeled trees of orders 2-10.  
Discovery SHA-256: `{manifest['discovery_hash']}`

Burned order: 11. It was not used for TF2 generation, tuning, holdout testing, or
adversarial selection.

Untouched holdout: all {manifest['holdout_tree_count']} unlabeled trees of order 12,
generated only after TxGraffiti generation and exact first-stage discovery triage.  
Holdout SHA-256: `{manifest['holdout_hash']}`

Frozen adversarial corpus: {manifest['adversarial_tree_count']} trees from exactly the
pre-frozen path, star, spider, caterpillar, balanced-binary-tree, double-star, and broom
instances.  
Adversarial SHA-256: `{manifest['adversarial_hash']}`

## TxGraffiti pipeline

The corrected TreeForge adapter maps the frozen empty hypothesis payload to upstream
`None`, the always-true base predicate. The methods remained `convex_hull` and
`ratios`; the heuristics remained Morgan and Dalmatian; the post-processors remained
duplicate removal and touch-count sorting.

Single-pass stage counts:

- raw generator output: {stage['raw_generator_output']}
- after Morgan: {stage['after_morgan']}
- after Dalmatian: {stage['after_dalmatian']}
- after duplicate removal: {stage['after_duplicate_removal']}
- after touch-count sort: {stage['after_touch_count_sort']}
- strengthened equalities added by upstream discover: {stage['strengthened_equalities']}
- final raw statements entering TreeForge triage: {manifest['raw_candidate_count']}

The first attempted live execution, Actions run `36875119955`, did not produce a valid
scientific artifact within the expected runtime envelope. A discovery-only probe in run
`36887027180` found 42,068 convex-hull facets while Qhull itself took about 0.48 seconds.
TreeForge therefore replaced repeated always-true Morgan/Dalmatian state reconstruction by
an output-equivalent cached adapter path, verified against the pinned live upstream package.
The frozen scientific specification was not changed. Clean repaired preflight run
`36887887082` passed before the successful scientific run above.

## Candidate lifecycle

TxGraffiti produced {manifest['raw_candidate_count']} final statements, allocated permanently
as `TF-000002` through `TF-000999`. Exact discovery-side reevaluation admitted all
{manifest['first_stage_state_counts']['CONJECTURED']} to `CONJECTURED`; none was classified
away at this first stage.

The untouched order-12 holdout falsified {completion['holdout_falsified_count']} candidates
and left {manifest['holdout_survivor_count']} finite survivors. Every survivor was tested on
the frozen adversarial corpus. None failed there, so all {manifest['adversarial_survivor_count']}
reached `ADVERSARIAL_PASSED` before mathematical interpretation.

Interpretation then classified `TF-000002` as `KNOWN_RESULT` (the standard
`gamma(T) <= nu(T)` relation), and `TF-000010` plus `TF-000996` as elementary
`TRIVIAL` consequences of leaf/support/degree structure. Seventy high-dimensional
convex-hull facets remain finite `ADVERSARIAL_PASSED` survivors with no identified
structural mechanism strong enough for promotion.

`TF-000998`, `gamma(T) >= 3 nu(T)/5`, initially reached
`MATHEMATICALLY_INTERESTING` because it is a simple two-invariant bound, was sharp on the
order-10 discovery spider with arms `[1,4,4]`, and survived every frozen finite gate. A
bounded candidate-specific prior-art search found no exact match in the searched sources,
but this was not treated as novelty. Deeper structural interpretation then produced an exact
counterexample: the six-arm spider with arms `[4,4,4,4,4,4]` has order 25,
`gamma=7`, and `nu=12`, so `7 < 3*12/5`. It is therefore permanently
`FALSIFIED`.

Final interpreted states are: {completion['final_state_counts']}. One candidate reached the
mathematical-interest gate during its lineage, and it was later falsified. No candidate is a
`GRADUATION_CANDIDATE`, no theorem is claimed, and no novelty claim is made.

## Prior-art boundary

A bounded prior-art search was performed only for `TF-000998` after its temporary
`MATHEMATICALLY_INTERESTING` promotion. Exact search terms, sources, close results, and
uncertainty are preserved in that candidate lineage and in
`interpretation_summary.json`. No other candidate triggered literature search.

## Reproducibility

The complete raw TxGraffiti output is committed as `raw_txgraffiti_output.json`, with
structured relation and touch-count metadata. The central append-only candidate registry
contains every generated lineage and every later interpretation revision. Discovery and
holdout row files are deterministic and are not committed; their exact counts and hashes are
recorded above and in `manifest.json`.
"""


def run(artifact_dir: Path) -> dict[str, object]:
    manifest = _read_json(artifact_dir / "manifest.json")
    if manifest["experiment_id"] != EXPERIMENT_ID:
        raise RuntimeError("wrong experiment artifact")
    if manifest["source_commit"] != SCIENTIFIC_SOURCE_COMMIT:
        raise RuntimeError("scientific source commit mismatch")
    if manifest["discovery_hash"] != EXPECTED_DISCOVERY_HASH:
        raise RuntimeError("discovery hash mismatch")
    if manifest["holdout_hash"] != EXPECTED_HOLDOUT_HASH:
        raise RuntimeError("holdout hash mismatch")
    if manifest["adversarial_hash"] != EXPECTED_ADVERSARIAL_HASH:
        raise RuntimeError("adversarial hash mismatch")
    if manifest["raw_candidate_count"] != 998:
        raise RuntimeError("unexpected TF2 raw candidate count")
    if manifest["holdout_visible_to_generator"] is not False:
        raise RuntimeError("holdout leakage flag is not false")

    artifact_events = _read_jsonl(artifact_dir / "candidate_events.jsonl")
    final_candidates = _read_json(artifact_dir / "final_candidates.json")
    for record in artifact_events:
        validate_candidate_record(record)

    ids = sorted({str(record["candidate_id"]) for record in artifact_events})
    expected_ids = [f"TF-{number:06d}" for number in range(2, 1000)]
    if ids != expected_ids:
        raise RuntimeError("TF2 candidate IDs are not exactly TF-000002..TF-000999")

    registry_path = Path("data/registry/candidates.jsonl")
    existing = _read_jsonl(registry_path)
    for record in existing:
        _validate_registry_record(record)
    if any(str(record["candidate_id"]) != "TF-000001" for record in existing):
        raise RuntimeError("candidate registry advanced unexpectedly before TF2 finalization")

    _append_jsonl(registry_path, artifact_events)

    interpretation_events, interpreted = _interpret_survivors(final_candidates)
    _append_jsonl(registry_path, interpretation_events)

    final_state_counts = dict(
        sorted(Counter(str(record["lifecycle_state"]) for record in interpreted.values()).items())
    )
    expected_final = {
        "ADVERSARIAL_PASSED": 70,
        "FALSIFIED": 925,
        "KNOWN_RESULT": 1,
        "TRIVIAL": 2,
    }
    if final_state_counts != expected_final:
        raise RuntimeError(f"unexpected interpreted state counts: {final_state_counts}")

    completion = {
        "experiment_id": EXPERIMENT_ID,
        "scientific_source_commit": SCIENTIFIC_SOURCE_COMMIT,
        "successful_scientific_actions_run": SCIENTIFIC_RUN_ID,
        "scientific_completed_at": SCIENTIFIC_COMPLETED_AT,
        "candidate_id_range": ["TF-000002", "TF-000999"],
        "raw_candidate_count": 998,
        "first_stage_state_counts": manifest["first_stage_state_counts"],
        "holdout_falsified_count": 924,
        "holdout_survivor_count": 74,
        "adversarial_falsified_count": 0,
        "adversarial_survivor_count": 74,
        "mathematically_interesting_reached_count": 1,
        "mathematically_interesting_reached_ids": ["TF-000998"],
        "prior_art_search_performed": True,
        "prior_art_candidate_ids": ["TF-000998"],
        "graduation_candidate_count": 0,
        "final_state_counts": final_state_counts,
        "failed_pre_valid_output_actions_run": 36875119955,
        "performance_probe_actions_run": 36887027180,
        "repaired_preflight_actions_run": 36887887082,
        "diagnostic_validation_actions_run": 36855637323,
        "frozen_implementation_premerge_actions_run": 36864378120,
    }

    experiment_dir = Path("experiments/TF2-0001")
    experiment_dir.mkdir(parents=True, exist_ok=True)
    for filename in ["manifest.json", "raw_txgraffiti_output.json", "stage_counts.json"]:
        shutil.copyfile(artifact_dir / filename, experiment_dir / filename)

    _write_json(
        experiment_dir / "first_stage_triage.json",
        {
            "raw_candidate_count": 998,
            "candidate_id_range": ["TF-000002", "TF-000999"],
            "state_counts": manifest["first_stage_state_counts"],
            "all_conjectured_tested_on_holdout": True,
        },
    )
    _write_json(
        experiment_dir / "holdout_summary.json",
        {
            "orders": [12, 12],
            "tree_count": manifest["holdout_tree_count"],
            "dataset_hash": manifest["holdout_hash"],
            "visible_to_generator": False,
            "tested_candidate_count": 998,
            "falsified_count": 924,
            "survivor_count": 74,
            "survivor_ids": manifest["holdout_survivor_ids"],
        },
    )
    _write_json(
        experiment_dir / "adversarial_summary.json",
        {
            "tree_count": manifest["adversarial_tree_count"],
            "dataset_hash": manifest["adversarial_hash"],
            "tested_candidate_count": 74,
            "falsified_count": 0,
            "survivor_count": 74,
            "survivor_ids": manifest["adversarial_survivor_ids"],
            "note": "Exactly the pre-frozen TF2-0001 family instances were used.",
        },
    )
    tf998 = interpreted["TF-000998"]
    _write_json(
        experiment_dir / "interpretation_summary.json",
        {
            **completion,
            "known_result_ids": ["TF-000002"],
            "trivial_ids": ["TF-000010", "TF-000996"],
            "unpromoted_adversarial_survivor_ids": sorted(
                candidate_id
                for candidate_id, record in interpreted.items()
                if record["lifecycle_state"] == "ADVERSARIAL_PASSED"
            ),
            "tf_000998_final_record": tf998,
        },
    )
    (experiment_dir / "RESULTS.md").write_text(
        _results_markdown(manifest, completion), encoding="utf-8"
    )

    experiments_path = Path("data/registry/experiments.jsonl")
    experiments = _read_jsonl(experiments_path)
    if any(row.get("experiment_id") == EXPERIMENT_ID for row in experiments):
        raise RuntimeError("TF2-0001 experiment registry record already exists")
    spec = _read_json(Path("experiments/TF2-0001/spec.json"))
    experiment_record = {
        "experiment_id": EXPERIMENT_ID,
        "label": "CONTROLLED_DISCOVERY",
        "created_at": spec["frozen_at"],
        "completed_at": SCIENTIFIC_COMPLETED_AT,
        "source_commit": SCIENTIFIC_SOURCE_COMMIT,
        "scientific_actions_run": SCIENTIFIC_RUN_ID,
        "command": (
            "python experiments/tf2_discovery.py --spec experiments/TF2-0001/spec.json "
            "--output-dir /tmp/tf2-0001 --source-commit "
            + SCIENTIFIC_SOURCE_COMMIT
        ),
        "dependencies": manifest["dependencies"],
        "txgraffiti_source_revision": manifest["txgraffiti_provenance"]["source_commit"],
        "generation_parameters": {
            "spec": "experiments/TF2-0001/spec.json",
            "discovery_orders": spec["discovery_orders"],
            "burned_orders_excluded": spec["burned_orders_excluded"],
            "holdout_orders": spec["holdout_orders"],
            "target": spec["target"],
            "discovery_features": spec["discovery_features"],
            "methods": spec["txgraffiti"]["methods"],
            "heuristics": spec["txgraffiti"]["heuristics"],
            "post_processors": spec["txgraffiti"]["post_processors"],
            "hypothesis_payload": spec["txgraffiti"]["hypothesis_payload"],
            "adapter_semantics": spec["txgraffiti"]["adapter_semantics"],
            "holdout_visible_to_generator": False,
        },
        "discovery_data_hash": manifest["discovery_hash"],
        "holdout_data_hash": manifest["holdout_hash"],
        "adversarial_data_hash": manifest["adversarial_hash"],
        "stage_counts": manifest["stage_counts"],
        "raw_candidate_count": 998,
        "candidate_ids": expected_ids,
        "first_stage_state_counts": manifest["first_stage_state_counts"],
        "holdout_falsified_count": 924,
        "holdout_survivor_count": 74,
        "adversarial_falsified_count": 0,
        "adversarial_survivor_count": 74,
        "mathematically_interesting_reached_count": 1,
        "prior_art_search_performed": True,
        "graduation_candidate_count": 0,
        "final_state_counts": final_state_counts,
        "result": (
            "998_CONJECTURED;924_HOLDOUT_FALSIFIED;74_FROZEN_ADVERSARIAL_SURVIVORS;"
            "1_TEMPORARILY_MATHEMATICALLY_INTERESTING_THEN_FALSIFIED;"
            "NO_GRADUATION_CANDIDATE"
        ),
    }
    _append_jsonl(experiments_path, [experiment_record])

    all_records = _read_jsonl(registry_path)
    per_id: dict[str, list[int]] = {}
    for record in all_records:
        _validate_registry_record(record)
        per_id.setdefault(str(record["candidate_id"]), []).append(int(record["revision"]))
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
