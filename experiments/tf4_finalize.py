#!/usr/bin/env python3
"""Materialize the audited TF4-0001 scientific artifact append-only."""

from __future__ import annotations

import argparse
import json
import shutil
from collections import Counter
from pathlib import Path

from experiments.tf2_discovery import _revision
from treeforge.pipeline import stable_hash
from treeforge.registry.schema import validate_candidate_record

EXPERIMENT_ID = "TF4-0001"
SCIENTIFIC_SOURCE_COMMIT = "d8e0874a22dde7f226431fc4f15a36adb8254efa"
SCIENTIFIC_RUN_ID = 36983184665
SCIENTIFIC_COMPLETED_AT = "2026-10-02T08:26:01Z"

EXPECTED_DISCOVERY_HASH = "6871f362f6897f390a1e4819358deb0fd342c6ad88bf8cde5c4ba026acbdd377"
EXPECTED_BATCH_HASH = "2bbb81b85eb6e40351f0913fafdc822c5417b2336e957e83fc08b505aedabf0f"
EXPECTED_HOLDOUT_HASH = "84978208ee2c65e3cda8327709e662cc71f9018ef2afc1ca03ff86a19a6197c3"
EXPECTED_ADVERSARIAL_HASH = "caf97df7db6b739383e015f816e3d643352cf53f164363d171c0eb1751e955f3"
EXPECTED_GUARD_HASH = "cf2248c732cd1b5a0f5d368ecb704171308a0c06ab4a5521df014b0d11d47f3b"
EXPECTED_IDS = [f"TF-{n:06d}" for n in range(1012, 1158)]

INTERPRETATION_AT = "2026-10-02T08:35:00Z"
PRIOR_ART_AT = "2026-10-02T08:40:00Z"

KNOWN_ID = "TF-001013"
NOVELTY_AUDIT_ID = "TF-001028"
TRIVIAL_IDS = {
    "TF-001015",
    "TF-001021",
    "TF-001027",
    "TF-001032",
    "TF-001078",
    "TF-001107",
}
ARTIFACT_IDS = {
    "TF-001065": "TF-001093",
    "TF-001066": "TF-001095",
    "TF-001069": "TF-001099",
    "TF-001070": "TF-001091",
}
BURNED_FAILURE_ID = "TF-001068"
UNPROMOTED_IDS = {
    "TF-001033","TF-001034","TF-001037","TF-001090","TF-001091",
    "TF-001093","TF-001095","TF-001098","TF-001099","TF-001134",
    "TF-001135","TF-001137","TF-001139","TF-001140","TF-001141",
    "TF-001142","TF-001144","TF-001145","TF-001154","TF-001155",
}
TF2_OVERLAP_IDS = ["TF-001018","TF-001022","TF-001031","TF-001088","TF-001156"]


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _append_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")


def _write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _validate_preserving_tf0_legacy(record: dict[str, object]) -> None:
    if record.get("candidate_id") == "TF-000001" and record.get("revision") == 1 and "source_commit" not in record:
        patched = dict(record)
        patched["source_commit"] = "LEGACY_TF0_REV1_SCHEMA_OMISSION"
        validate_candidate_record(patched)
    else:
        validate_candidate_record(record)


def _interpret(final_candidates: list[dict[str, object]]) -> tuple[list[dict[str, object]], dict[str, dict[str, object]]]:
    current = {str(row["candidate_id"]): row for row in final_candidates}
    survivors = {cid for cid, row in current.items() if row["lifecycle_state"] == "ADVERSARIAL_PASSED"}
    expected = {KNOWN_ID, NOVELTY_AUDIT_ID, *TRIVIAL_IDS, *ARTIFACT_IDS.keys(), BURNED_FAILURE_ID, *UNPROMOTED_IDS}
    if survivors != expected:
        raise RuntimeError(f"unexpected TF4 finite survivor set: {sorted(survivors ^ expected)}")

    events: list[dict[str, object]] = []

    # TF-001068: exposed order-11 failure found only after all fresh gates were closed.
    record = current[BURNED_FAILURE_ID]
    counterexample = {
        "source": "post_frozen_mathematical_interpretation_burned_order_11",
        "tree_code": "((((())()))(((())())))",
        "order": 11,
        "lhs": "domination_number",
        "operator": "<=",
        "rhs": "(((5/12 * leaf_count) + 11/6) + (1/12 * maximal_independent_set_count))",
        "values": {
            "order": 11,
            "leaf_count": 4,
            "maximal_independent_set_count": 17,
            "domination_number": 5,
            "support_vertex_count": 4,
            "max_degree": 3,
            "diameter": 8,
            "matching_number": 5,
            "tree_code": "((((())()))(((())())))",
        },
        "reason": (
            "Burned/exposed order-11 tree: RHS = 5/12*4 + 11/6 + 1/12*17 = 59/12 < 5 = gamma. "
            "This is interpretation evidence only, never fresh TF4 validation."
        ),
    }
    updated = _revision(
        record,
        created_at=INTERPRETATION_AT,
        lifecycle_state="FALSIFIED",
        counterexamples=[*record["counterexamples"], counterexample],
        prior_art_status="NOT_STARTED; EXPOSED_COUNTEREXAMPLE",
        mathematical_interpretation=counterexample["reason"],
    )
    validate_candidate_record(updated)
    events.append(updated)
    current[BURNED_FAILURE_ID] = updated

    # Six direct elementary consequences.
    explanations = {
        "TF-001015": (
            "TRIVIAL: every finite tree is nonempty and therefore has domination number at least 1."
        ),
        "TF-001021": (
            "TRIVIAL direct construction: for a maximum-degree vertex v, the set {v} union "
            "(V(T) minus N[v]) dominates T and has size n-Delta."
        ),
        "TF-001027": (
            "TRIVIAL diametral-path counting: every dominator covers at most three vertices of a "
            "diametral path, hence diameter+1 <= 3 gamma."
        ),
        "TF-001032": (
            "TRIVIAL tree matching consequence. For a gamma-set D, every vertex outside D has a "
            "cross-edge to D. Since T has n-1 edges, T-D has at most gamma-1 edges. Taking D plus "
            "one endpoint of every edge of T-D gives a vertex cover of size at most 2gamma-1; "
            "Konig's theorem for the bipartite tree gives matching_number <= 2gamma-1."
        ),
        "TF-001078": (
            "TRIVIAL combination: for nontrivial trees gamma >= support_vertex_count and "
            "gamma >= (diameter+1)/3, so gamma is at least their weighted average "
            "(support_vertex_count + diameter + 1)/4; K1 and K2 are immediate."
        ),
        "TF-001107": (
            "TRIVIAL/dominated: for every nontrivial tree Delta>=2, the elementary diameter bound "
            "TF-001027 is at least as strong as (diameter-Delta+3)/3; K1 is immediate."
        ),
    }
    for cid, explanation in explanations.items():
        record = current[cid]
        updated = _revision(
            record,
            created_at=INTERPRETATION_AT,
            lifecycle_state="TRIVIAL",
            prior_art_status="NOT_STARTED; ELEMENTARY_DERIVATION",
            mathematical_interpretation=explanation + " No prior-art search is warranted.",
        )
        validate_candidate_record(updated)
        events.append(updated)
        current[cid] = updated

    # Four leaf/MIS facets are strictly weaker than same-coefficient support/MIS facets.
    for cid, stronger in ARTIFACT_IDS.items():
        record = current[cid]
        explanation = (
            f"ARTIFACT_OF_FEATURE_SET: {cid} is pointwise dominated by {stronger}. "
            "For every finite tree, support_vertex_count <= leaf_count. The two upper bounds have "
            "identical constant and maximal_independent_set_count coefficients, while the stronger "
            "candidate substitutes support_vertex_count for leaf_count with the same positive "
            "coefficient, producing a no-larger RHS."
        )
        updated = _revision(
            record,
            created_at=INTERPRETATION_AT,
            lifecycle_state="ARTIFACT_OF_FEATURE_SET",
            prior_art_status="NOT_STARTED; DOMINATED_BY_STRONGER_DISCOVERED_FACET",
            mathematical_interpretation=explanation,
        )
        validate_candidate_record(updated)
        events.append(updated)
        current[cid] = updated

    # TF-001013 independently merited interest, then a bounded exact-form audit found prior art.
    record = current[KNOWN_ID]
    interesting = _revision(
        record,
        created_at=INTERPRETATION_AT,
        lifecycle_state="MATHEMATICALLY_INTERESTING",
        prior_art_status="READY_FOR_BOUNDED_AUDIT",
        mathematical_interpretation=(
            "Simple, robust two-feature lower bound gamma(T) >= (n-l+2)/3 with clear structural "
            "tree parameters, moderate touch count, no exact TF2/TF3 duplicate, and survival of "
            "the frozen TF4 gates. This independently warrants a candidate-specific prior-art audit."
        ),
    )
    validate_candidate_record(interesting)
    events.append(interesting)
    known = _revision(
        interesting,
        created_at=PRIOR_ART_AT,
        lifecycle_state="KNOWN_RESULT",
        prior_art_status=(
            "BOUNDED_AUDIT_COMPLETED; EXACT_PRIOR_ART: LEMANSKA 2004, Discussiones Mathematicae "
            "Graph Theory 24:165-170; independently restated by Hajian-Henning-Jafari Rad 2019"
        ),
        mathematical_interpretation=(
            "Exact prior art: the bound gamma(T) >= (n-l+2)/3 for nontrivial trees was proved by "
            "Lemanska (2004), with equality characterization; K1 satisfies the frozen all-tree form "
            "directly. TF4 therefore records rediscovery, not novelty."
        ),
    )
    validate_candidate_record(known)
    events.append(known)
    current[KNOWN_ID] = known

    # TF-001028 is the sole promoted unresolved structural interaction.
    record = current[NOVELTY_AUDIT_ID]
    interesting = _revision(
        record,
        created_at=INTERPRETATION_AT,
        lifecycle_state="MATHEMATICALLY_INTERESTING",
        prior_art_status="READY_FOR_BOUNDED_AUDIT",
        mathematical_interpretation=(
            "Distinct low-dimensional interaction gamma(T) <= (2n+1-diameter)/3. It is not an "
            "exact TF2/TF3 duplicate, avoids maximal_independent_set_count scale effects, has a "
            "simple order-diameter form, and survives all frozen and exposed checks performed here."
        ),
    )
    validate_candidate_record(interesting)
    events.append(interesting)
    audited = _revision(
        interesting,
        created_at=PRIOR_ART_AT,
        lifecycle_state="NOVELTY_AUDIT",
        prior_art_status=(
            "BOUNDED_AUDIT_COMPLETED; NO_EXACT_MATCH_FOUND_IN_TARGETED_SEARCH; "
            "NEGATIVE_SEARCH_IS_NOT_NOVELTY_EVIDENCE"
        ),
        mathematical_interpretation=(
            "Targeted searches for the exact (2n+1-diameter)/3 upper bound located related general "
            "domination/diameter bounds and recent tree upper bounds, but no exact statement. This "
            "does not establish novelty. No proof is claimed, and the candidate is not a graduation "
            "candidate; TF5 should attack it structurally before any further promotion."
        ),
    )
    validate_candidate_record(audited)
    events.append(audited)
    current[NOVELTY_AUDIT_ID] = audited

    # The remaining MIS-count facet fan is left at finite evidence only.
    for cid in sorted(UNPROMOTED_IDS):
        record = current[cid]
        explanation = (
            "Finite survivor only. This statement belongs to the surviving maximal_independent_set_count "
            "facet fan. The pairwise grammar makes it syntactically interpretable, but neighboring "
            "coefficient facets, strong scale sensitivity of maximal_independent_set_count, and absence "
            "of an independent structural derivation do not justify MATHEMATICALLY_INTERESTING. "
            "No broad prior-art search is warranted."
        )
        updated = _revision(
            record,
            created_at=INTERPRETATION_AT,
            lifecycle_state="ADVERSARIAL_PASSED",
            prior_art_status="NOT_STARTED; NOT_MATHEMATICALLY_INTERESTING",
            mathematical_interpretation=explanation,
        )
        validate_candidate_record(updated)
        events.append(updated)
        current[cid] = updated

    return events, current


def _results_markdown(manifest: dict[str, object], completion: dict[str, object]) -> str:
    stage = manifest["pairwise_stage_counts"]
    return f"""# TF4-0001 result

TF4-0001 is scientifically complete. Finite computation is evidence, not proof.

## Frozen change and provenance

Scientific source commit: `{SCIENTIFIC_SOURCE_COMMIT}`  
Successful GitHub Actions run: `{SCIENTIFIC_RUN_ID}`

Exactly one material discovery axis changed from TF3: ratios-only generation became 21 fixed
pairwise `convex_hull` runs over the unchanged seven features, followed only by exact normalized
cross-run deduplication. The target, discovery orders, heuristics, post-processors, literal all-tree
hypothesis, and TxGraffiti pin remained frozen.

## Pairwise generation

- feature-pair runs: 21
- raw outputs: {stage['raw_generator_output']}
- after Morgan: {stage['after_morgan']}
- after Dalmatian: {stage['after_dalmatian']}
- per-run post-duplicate total: {stage['after_duplicate_removal']}
- cross-run exact unique statements: {manifest['cross_run_exact_dedup_count']}
- permanent IDs: `TF-001012` through `TF-001157`
- discovery-side reevaluation failures: 0
- exposed K1 failures: {manifest['literal_k1_falsified_count']}

All 146 cross-run unique statements received permanent IDs before the K1 consistency gate.

## Candidate-batch firewall

After discovery reevaluation and exposed K1 consistency, 99 candidates remained.
Candidate-batch SHA-256: `{manifest['candidate_batch_hash']}`.

The persisted freeze says `holdout_constructed: false`. Only after that file/hash existed did the
runner construct order 14.

## Fresh order-14 holdout

All {manifest['holdout_tree_count']} unlabeled order-14 trees were tested.
SHA-256: `{manifest['holdout_hash']}`.

- tested: 99
- falsified: 66
- survived: 33

## Frozen fresh hostile set

Exactly {manifest['adversarial_tree_count']} pre-frozen hostile trees were constructed.
SHA-256: `{manifest['adversarial_hash']}`.

Only the 33 order-14 survivors were tested; none failed this finite hostile gate.

## Mathematical interpretation

Post-gate interpretation used burned/exposed material freely and did not change the scientific run.

- `TF-001068` is falsified by an already-exposed order-11 tree.
- `TF-001015`, `TF-001021`, `TF-001027`, `TF-001032`, `TF-001078`, and
  `TF-001107` are elementary consequences and are `TRIVIAL`.
- `TF-001065`, `TF-001066`, `TF-001069`, and `TF-001070` are
  `ARTIFACT_OF_FEATURE_SET`: same-coefficient support/MIS facets are pointwise stronger because
  support_vertex_count <= leaf_count.
- `TF-001013` independently reached `MATHEMATICALLY_INTERESTING`, then a bounded audit found
  the exact Lemańska 2004 leaf bound; it is `KNOWN_RESULT`.
- `TF-001028` independently reached `MATHEMATICALLY_INTERESTING`; its bounded exact-form audit
  found related literature but no exact match. It remains `NOVELTY_AUDIT`; that negative search is
  explicitly not evidence of novelty.
- The remaining 20 finite survivors are all maximal-independent-set-count facets. They stay
  `ADVERSARIAL_PASSED` with interpretation notes only; no structural reason justified promotion.

Five of the 146 exact forms duplicate TF2 normalized relations:
`{', '.join(TF2_OVERLAP_IDS)}`. All five were already falsified during TF4's computational gates.

Final interpreted lifecycle counts: {completion['final_state_counts']}.

No candidate reaches `GRADUATION_CANDIDATE`; no theoremhood or novelty claim is made.

## Scientific conclusion

Pairwise hulls improved interpretability relative to TF2: every statement has at most two RHS
features, and the simple non-MIS survivors can be analyzed directly. They did not fully solve the
facet problem: maximal_independent_set_count still generated a large neighboring family of finite
survivors without a convincing structural mechanism.

TF5 should therefore not broaden the grammar immediately. It should first attack `TF-001028`
structurally (proof attempt, explicit family counterexample search, and focused prior-art completion).
Only if that resolves negatively should TreeForge freeze another discovery-axis change.
"""


def run(artifact_dir: Path) -> dict[str, object]:
    manifest = _read_json(artifact_dir / "manifest.json")
    stage = _read_json(artifact_dir / "pairwise_stage_counts.json")
    dedup = _read_json(artifact_dir / "cross_run_deduplicated_output.json")
    batch = _read_json(artifact_dir / "candidate_batch.json")
    freeze = _read_json(artifact_dir / "candidate_batch_freeze.json")
    guard = _read_json(artifact_dir / "literal_domain_guard.json")
    events = _read_jsonl(artifact_dir / "candidate_events.jsonl")
    final_candidates = _read_json(artifact_dir / "final_candidates.json")

    if manifest["experiment_id"] != EXPERIMENT_ID or manifest["source_commit"] != SCIENTIFIC_SOURCE_COMMIT:
        raise RuntimeError("wrong TF4 scientific artifact provenance")
    if manifest["dependencies"] != {"networkx": "3.6.1", "pandas": "3.0.6", "txgraffiti": "0.4.1"}:
        raise RuntimeError("unexpected scientific dependencies")
    if manifest["candidate_ids"] != EXPECTED_IDS or len(dedup) != 146:
        raise RuntimeError("unexpected TF4 permanent ID stream")
    if stage != {
        "raw_generator_output": 259,
        "after_morgan": 259,
        "after_dalmatian": 214,
        "after_duplicate_removal": 205,
        "after_touch_count_sort": 205,
        "strengthened_equalities": 0,
        "final_discover_output": 205,
    }:
        raise RuntimeError("TF4 pairwise stage-count drift")
    if manifest["cross_run_exact_dedup_count"] != 146:
        raise RuntimeError("TF4 cross-run dedup drift")
    if freeze["holdout_constructed"] is not False or freeze["candidate_count"] != 99:
        raise RuntimeError("candidate-batch firewall record invalid")
    if freeze["candidate_batch_hash"] != EXPECTED_BATCH_HASH or manifest["candidate_batch_hash"] != EXPECTED_BATCH_HASH:
        raise RuntimeError("candidate-batch hash mismatch")
    if guard["dataset_hash"] != EXPECTED_GUARD_HASH or guard["falsified_count"] != 47:
        raise RuntimeError("literal K1 guard mismatch")
    if manifest["discovery_hash"] != EXPECTED_DISCOVERY_HASH or manifest["holdout_hash"] != EXPECTED_HOLDOUT_HASH:
        raise RuntimeError("scientific corpus hash mismatch")
    if manifest["adversarial_hash"] != EXPECTED_ADVERSARIAL_HASH:
        raise RuntimeError("adversarial hash mismatch")
    if manifest["holdout_tree_count"] != 3159 or manifest["holdout_survivor_count"] != 33:
        raise RuntimeError("unexpected order-14 outcome")
    if manifest["adversarial_tree_count"] != 19 or len(manifest["adversarial_survivor_ids"]) != 33:
        raise RuntimeError("unexpected hostile-set outcome")
    if stable_hash(batch) != EXPECTED_BATCH_HASH:
        raise RuntimeError("candidate batch content hash mismatch")

    for row in events:
        validate_candidate_record(row)
    if sorted({str(row["candidate_id"]) for row in events}) != EXPECTED_IDS:
        raise RuntimeError("artifact candidate event range mismatch")

    registry = Path("data/registry/candidates.jsonl")
    existing = _read_jsonl(registry)
    for row in existing:
        _validate_preserving_tf0_legacy(row)
    existing_ids = sorted({str(row["candidate_id"]) for row in existing})
    if existing_ids != [f"TF-{n:06d}" for n in range(1, 1012)]:
        raise RuntimeError("candidate registry advanced unexpectedly before TF4 finalization")

    _append_jsonl(registry, events)
    interpretation_events, interpreted = _interpret(final_candidates)
    _append_jsonl(registry, interpretation_events)

    final_counts = dict(sorted(Counter(str(row["lifecycle_state"]) for row in interpreted.values()).items()))
    expected_counts = {
        "ADVERSARIAL_PASSED": 20,
        "ARTIFACT_OF_FEATURE_SET": 4,
        "FALSIFIED": 114,
        "KNOWN_RESULT": 1,
        "NOVELTY_AUDIT": 1,
        "TRIVIAL": 6,
    }
    if final_counts != expected_counts:
        raise RuntimeError(f"unexpected TF4 final state counts: {final_counts}")

    exp_dir = Path("experiments/TF4-0001")
    for filename in [
        "manifest.json",
        "pairwise_stage_counts.json",
        "cross_run_deduplicated_output.json",
        "candidate_batch.json",
        "candidate_batch_freeze.json",
        "literal_domain_guard.json",
    ]:
        shutil.copyfile(artifact_dir / filename, exp_dir / filename)

    holdout_failed = sorted(
        str(row["candidate_id"]) for row in final_candidates
        if row["holdout_status"].get("status") == "FAILED"
    )
    holdout_survivors = sorted(manifest["holdout_survivor_ids"])
    _write_json(exp_dir / "holdout_summary.json", {
        "order": 14,
        "tree_count": 3159,
        "dataset_hash": EXPECTED_HOLDOUT_HASH,
        "candidate_batch_hash": EXPECTED_BATCH_HASH,
        "visible_to_generator": False,
        "tested_candidate_count": 99,
        "falsified_count": 66,
        "falsified_ids": holdout_failed,
        "survivor_count": 33,
        "survivor_ids": holdout_survivors,
        "first_counterexamples": {
            str(row["candidate_id"]): row["counterexamples"][-1]
            for row in final_candidates
            if row["holdout_status"].get("status") == "FAILED"
        },
    })
    _write_json(exp_dir / "adversarial_summary.json", {
        "tree_count": 19,
        "dataset_hash": EXPECTED_ADVERSARIAL_HASH,
        "candidate_batch_hash": EXPECTED_BATCH_HASH,
        "tested_candidate_count": 33,
        "tested_candidate_ids": holdout_survivors,
        "falsified_count": 0,
        "survivor_count": 33,
        "survivor_ids": holdout_survivors,
        "note": "Exactly the pre-frozen TF4 hostile set was applied only to order-14 survivors.",
    })

    interpretation_summary = {
        "finite_survivor_count_before_interpretation": 33,
        "burned_exposed_falsified": [BURNED_FAILURE_ID],
        "trivial_ids": sorted(TRIVIAL_IDS),
        "artifact_of_feature_set_ids": sorted(ARTIFACT_IDS),
        "known_result_ids": [KNOWN_ID],
        "novelty_audit_ids": [NOVELTY_AUDIT_ID],
        "unpromoted_finite_survivor_ids": sorted(UNPROMOTED_IDS),
        "mathematically_interesting_reached_ids": [KNOWN_ID, NOVELTY_AUDIT_ID],
        "prior_art_search_performed_for": [KNOWN_ID, NOVELTY_AUDIT_ID],
        "graduation_candidate_ids": [],
        "exact_tf2_overlap_ids": TF2_OVERLAP_IDS,
        "exact_tf3_overlap_ids": [],
        "newly_constructed_counterexample_count": 0,
        "burned_order_11_counterexample": {
            "candidate_id": BURNED_FAILURE_ID,
            "order": 11,
            "tree_code": "((((())()))(((())())))",
            "domination_number": 5,
            "leaf_count": 4,
            "maximal_independent_set_count": 17,
        },
        "mis_count_interpretation": (
            "maximal_independent_set_count remained qualitatively dominant: after removing the burned "
            "failure, elementary/known/dominated forms and the order-diameter audit candidate, all 20 "
            "unpromoted finite survivors still involve maximal_independent_set_count. The pairwise "
            "grammar made these facets readable but did not supply a structural reason to promote them."
        ),
        "pairwise_interpretability_conclusion": (
            "Pairwise hulls are materially more interpretable than TF2 full-dimensional hulls, but a "
            "large neighboring MIS-count facet fan remains. TF4 therefore improved interpretability "
            "without eliminating geometric repetition."
        ),
        "tf5_recommendation": (
            "Do not broaden the discovery grammar yet. First make TF5 a structural attack on TF-001028: "
            "seek a proof or explicit family counterexample for gamma <= (2n+1-diameter)/3 and complete "
            "its focused prior-art audit. If it resolves negatively, diagnose the MIS-count facet fan "
            "before freezing any next discovery-axis change."
        ),
        "final_state_counts": final_counts,
    }
    _write_json(exp_dir / "interpretation_summary.json", interpretation_summary)

    experiment_registry = Path("data/registry/experiments.jsonl")
    experiment_rows = _read_jsonl(experiment_registry)
    if any(row["experiment_id"] == EXPERIMENT_ID for row in experiment_rows):
        raise RuntimeError("TF4 experiment record already exists")
    experiment_record = {
        "experiment_id": EXPERIMENT_ID,
        "label": "CONTROLLED_DISCOVERY",
        "created_at": "2026-10-02T06:00:00Z",
        "completed_at": SCIENTIFIC_COMPLETED_AT,
        "source_commit": SCIENTIFIC_SOURCE_COMMIT,
        "scientific_actions_run": SCIENTIFIC_RUN_ID,
        "command": (
            "python -m experiments.tf4_discovery --output-dir /tmp/tf4-scientific "
            f"--source-commit {SCIENTIFIC_SOURCE_COMMIT}"
        ),
        "dependencies": manifest["dependencies"],
        "txgraffiti_source_revision": manifest["txgraffiti_provenance"]["source_commit"],
        "generation_parameters": {
            "spec": "experiments/TF4-0001/spec.json",
            "target": "domination_number",
            "discovery_orders": [2, 10],
            "holdout_orders": [14, 14],
            "burned_or_exposed_orders": list(range(1, 14)),
            "methods": ["convex_hull"],
            "feature_pair_run_count": 21,
            "cross_run_duplicate_equivalence": "normalized (lhs, operator, rhs) equality",
            "candidate_batch_frozen_before_holdout": True,
            "holdout_visible_to_generator": False,
        },
        "stage_counts": stage,
        "raw_candidate_count": 146,
        "candidate_ids": EXPECTED_IDS,
        "discovery_data_hash": EXPECTED_DISCOVERY_HASH,
        "candidate_batch_hash": EXPECTED_BATCH_HASH,
        "holdout_data_hash": EXPECTED_HOLDOUT_HASH,
        "adversarial_data_hash": EXPECTED_ADVERSARIAL_HASH,
        "first_stage_state_counts": {"CONJECTURED": 146},
        "literal_k1_falsified_count": 47,
        "candidate_batch_count": 99,
        "holdout_falsified_count": 66,
        "holdout_survivor_count": 33,
        "adversarial_falsified_count": 0,
        "adversarial_survivor_count": 33,
        "final_state_counts": final_counts,
        "mathematically_interesting_reached_count": 2,
        "prior_art_search_performed": True,
        "graduation_candidate_count": 0,
        "result": (
            "146_PAIRWISE_UNIQUE;47_K1_FALSIFIED;99_BATCH;66_ORDER14_FALSIFIED;"
            "33_HOSTILE_SURVIVORS;POST_INTERPRETATION_114_FALSIFIED_6_TRIVIAL_4_ARTIFACT_"
            "1_KNOWN_1_NOVELTY_AUDIT_20_FINITE_UNPROMOTED;NO_GRADUATION_CANDIDATE"
        ),
    }
    _append_jsonl(experiment_registry, [experiment_record])

    completion = {
        **interpretation_summary,
        "experiment_id": EXPERIMENT_ID,
        "scientific_source_commit": SCIENTIFIC_SOURCE_COMMIT,
        "successful_scientific_actions_run": SCIENTIFIC_RUN_ID,
        "candidate_id_range": ["TF-001012", "TF-001157"],
        "next_candidate_id": "TF-001158",
        "candidate_batch_hash": EXPECTED_BATCH_HASH,
        "discovery_hash": EXPECTED_DISCOVERY_HASH,
        "holdout_hash": EXPECTED_HOLDOUT_HASH,
        "adversarial_hash": EXPECTED_ADVERSARIAL_HASH,
    }
    _write_json(exp_dir / "completion_summary.json", completion)
    (exp_dir / "RESULTS.md").write_text(_results_markdown(manifest, completion), encoding="utf-8")
    return completion


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-dir", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.artifact_dir), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
