import json
from collections import Counter, defaultdict
from pathlib import Path

from experiments.tf3_discovery import _adversarial_rows
from treeforge.experiments import experiment_corpus_rows, load_frozen_spec
from treeforge.pipeline import stable_hash
from treeforge.registry.schema import validate_candidate_record

EXPECTED_SOURCE = "e23b44d24a7b87d6f67aa18749059540934b2767"
EXPECTED_DISCOVERY_HASH = "e1fa7090640ba0254dba399082c436cf30742d7fe19ffef1d17028e7f45ab250"
EXPECTED_BATCH_HASH = "85669d95fb7199b720bfe488c606055dd5f38a5af157c1ed2bdb5f98710344c6"
EXPECTED_HOLDOUT_HASH = "5b02d81644415adc2df55d0a2ec3694125ef328cb1a0c4a2eeb733efaecef7e9"
EXPECTED_ADVERSARIAL_HASH = "37abd291592c4e98730d4dc8fef8c1678c4835ac87a555aad19edd5b75f14a18"
EXPECTED_IDS = [f"TF-{number:06d}" for number in range(1000, 1012)]


def _json(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _jsonl(path: str):
    return [
        json.loads(line)
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def test_tf3_committed_scientific_record_and_firewall():
    manifest = _json("experiments/TF3-0001/manifest.json")
    stage = _json("experiments/TF3-0001/stage_counts.json")
    batch = _json("experiments/TF3-0001/candidate_batch.json")
    freeze = _json("experiments/TF3-0001/candidate_batch_freeze.json")
    holdout = _json("experiments/TF3-0001/holdout_summary.json")
    adversarial = _json("experiments/TF3-0001/adversarial_summary.json")
    interpretation = _json("experiments/TF3-0001/interpretation_summary.json")

    assert manifest["source_commit"] == EXPECTED_SOURCE
    assert manifest["methods"] == ["ratios"]
    assert stage == {
        "raw_generator_output": 14,
        "after_morgan": 14,
        "after_dalmatian": 12,
        "after_duplicate_removal": 12,
        "after_touch_count_sort": 12,
        "strengthened_equalities": 0,
        "final_discover_output": 12,
    }
    assert manifest["candidate_ids"] == EXPECTED_IDS
    assert stable_hash(batch) == EXPECTED_BATCH_HASH
    assert freeze["candidate_batch_hash"] == EXPECTED_BATCH_HASH
    assert freeze["holdout_constructed"] is False
    assert manifest["candidate_batch_frozen_before_holdout"] is True
    assert manifest["holdout_visible_to_generator"] is False

    assert holdout["tree_count"] == 1301
    assert holdout["tested_candidate_count"] == 12
    assert holdout["falsified_count"] == 8
    assert holdout["survivor_count"] == 4
    assert holdout["dataset_hash"] == EXPECTED_HOLDOUT_HASH
    assert adversarial["tree_count"] == 18
    assert adversarial["tested_candidate_count"] == 4
    assert adversarial["falsified_count"] == 0
    assert adversarial["survivor_count"] == 4
    assert adversarial["dataset_hash"] == EXPECTED_ADVERSARIAL_HASH
    assert interpretation["final_state_counts"] == {"FALSIFIED": 11, "TRIVIAL": 1}
    assert interpretation["mathematically_interesting_reached_count"] == 0
    assert interpretation["prior_art_search_performed"] is False
    assert interpretation["graduation_candidate_count"] == 0


def test_tf3_reproduces_discovery_holdout_and_adversarial_hashes():
    spec = load_frozen_spec(Path("experiments/TF3-0001/spec.json"))
    invariants = list(spec["corpus_invariants"])

    discovery = experiment_corpus_rows(
        min_order=2,
        max_order=10,
        invariant_names=invariants,
        role="discovery",
        source_commit=EXPECTED_SOURCE,
        experiment_id="TF3-0001",
    )
    assert len(discovery) == 200
    assert stable_hash(discovery) == EXPECTED_DISCOVERY_HASH

    holdout = experiment_corpus_rows(
        min_order=13,
        max_order=13,
        invariant_names=invariants,
        role="holdout",
        source_commit=EXPECTED_SOURCE,
        experiment_id="TF3-0001",
    )
    assert len(holdout) == 1301
    assert all(row["order"] == 13 for row in holdout)
    assert stable_hash(holdout) == EXPECTED_HOLDOUT_HASH

    adversarial = _adversarial_rows(invariants, EXPECTED_SOURCE, "TF3-0001")
    assert len(adversarial) == 18
    assert stable_hash(adversarial) == EXPECTED_ADVERSARIAL_HASH


def test_tf3_registry_is_append_only_and_interpreted():
    records = _jsonl("data/registry/candidates.jsonl")
    for record in records:
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

    by_id = defaultdict(list)
    for record in records:
        by_id[record["candidate_id"]].append(record)

    assert all(candidate_id in by_id for candidate_id in EXPECTED_IDS)
    for candidate_id in EXPECTED_IDS:
        lineage = by_id[candidate_id]
        revisions = [row["revision"] for row in lineage]
        assert revisions == sorted(revisions)
        assert len(revisions) == len(set(revisions))
        assert lineage[0]["source_commit"] == EXPECTED_SOURCE
        assert lineage[0]["lifecycle_state"] == "OBSERVED"
        assert any(row["lifecycle_state"] == "CONJECTURED" for row in lineage)

    current = {candidate_id: by_id[candidate_id][-1] for candidate_id in EXPECTED_IDS}
    assert dict(sorted(Counter(row["lifecycle_state"] for row in current.values()).items())) == {
        "FALSIFIED": 11,
        "TRIVIAL": 1,
    }
    assert current["TF-001000"]["counterexamples"][-1]["order"] == 1
    assert current["TF-001001"]["counterexamples"][-1]["order"] == 1
    assert current["TF-001006"]["lifecycle_state"] == "TRIVIAL"
    assert current["TF-001010"]["counterexamples"][-1]["order"] == 25
    assert current["TF-001010"]["counterexamples"][-1]["values"]["domination_number"] == 7
    assert current["TF-001010"]["counterexamples"][-1]["values"]["matching_number"] == 12


def test_tf3_experiment_registry_record_is_unique_and_complete():
    experiments = _jsonl("data/registry/experiments.jsonl")
    matches = [row for row in experiments if row["experiment_id"] == "TF3-0001"]
    assert len(matches) == 1
    record = matches[0]
    assert record["source_commit"] == EXPECTED_SOURCE
    assert record["scientific_actions_run"] == 36914647703
    assert record["candidate_batch_hash"] == EXPECTED_BATCH_HASH
    assert record["holdout_falsified_count"] == 8
    assert record["holdout_survivor_count"] == 4
    assert record["adversarial_falsified_count"] == 0
    assert record["adversarial_survivor_count"] == 4
    assert record["mathematically_interesting_reached_count"] == 0
    assert record["prior_art_search_performed"] is False
    assert record["graduation_candidate_count"] == 0
    assert record["final_state_counts"] == {"FALSIFIED": 11, "TRIVIAL": 1}
