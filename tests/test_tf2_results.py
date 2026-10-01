import json
from collections import Counter, defaultdict
from pathlib import Path

from experiments.tf2_discovery import _adversarial_rows
from treeforge.experiments import experiment_corpus_rows, load_frozen_spec
from treeforge.pipeline import stable_hash
from treeforge.registry.schema import validate_candidate_record

EXPECTED_SOURCE = "d091d88889fa72322bfc49a5531bc30b1f31b049"
EXPECTED_DISCOVERY_HASH = "40bc528cd8b035854de816a1fbd37f1c6d688b2b1686d006387fb16dc8f5c4a8"
EXPECTED_HOLDOUT_HASH = "ea9f5d200ec503090499b4744338a5e39a37b7412d21ed5f6f876e2129be9433"
EXPECTED_ADVERSARIAL_HASH = "dea3af9c495cc79da46b7ed3797276caae22495bc86d5000ddea3605a07bcb8a"


def _json(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _jsonl(path: str):
    return [
        json.loads(line)
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _validate_preserving_tf0_legacy(record):
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


def test_tf2_committed_manifest_and_raw_output():
    spec = load_frozen_spec(Path("experiments/TF2-0001/spec.json"))
    manifest = _json("experiments/TF2-0001/manifest.json")
    raw = _json("experiments/TF2-0001/raw_txgraffiti_output.json")

    assert spec["burned_orders_excluded"] == [11]
    assert spec["holdout_orders"] == [12, 12]
    assert manifest["source_commit"] == EXPECTED_SOURCE
    assert manifest["discovery_hash"] == EXPECTED_DISCOVERY_HASH
    assert manifest["holdout_hash"] == EXPECTED_HOLDOUT_HASH
    assert manifest["discovery_tree_count"] == 200
    assert manifest["holdout_tree_count"] == 551
    assert manifest["holdout_visible_to_generator"] is False
    assert manifest["raw_candidate_count"] == 998
    assert len(raw) == 998
    assert all({"lhs", "operator", "rhs"} <= set(item["metadata"]) for item in raw)
    assert manifest["stage_counts"] == {
        "raw_generator_output": 23268,
        "after_morgan": 23268,
        "after_dalmatian": 10753,
        "after_duplicate_removal": 998,
        "after_touch_count_sort": 998,
        "strengthened_equalities": 0,
        "final_discover_output": 998,
    }


def test_tf2_registry_lineages_and_final_states():
    records = _jsonl("data/registry/candidates.jsonl")
    for record in records:
        _validate_preserving_tf0_legacy(record)

    by_id = defaultdict(list)
    for record in records:
        by_id[record["candidate_id"]].append(record)

    assert sorted(by_id) == [f"TF-{number:06d}" for number in range(1, 1000)]
    assert by_id["TF-000001"][0]["statement"] == (
        "For every finite tree T, |E(T)| = |V(T)| - 1."
    )
    assert by_id["TF-000001"][-1]["lifecycle_state"] == "KNOWN_RESULT"

    for candidate_id, lineage in by_id.items():
        revisions = [row["revision"] for row in lineage]
        assert revisions == sorted(revisions)
        assert len(revisions) == len(set(revisions))
        if candidate_id != "TF-000001":
            assert lineage[0]["source_commit"] == EXPECTED_SOURCE
            assert lineage[0]["lifecycle_state"] == "OBSERVED"
            assert any(row["lifecycle_state"] == "CONJECTURED" for row in lineage)

    current = {candidate_id: lineage[-1] for candidate_id, lineage in by_id.items()}
    tf2_counts = Counter(
        record["lifecycle_state"]
        for candidate_id, record in current.items()
        if candidate_id != "TF-000001"
    )
    assert dict(sorted(tf2_counts.items())) == {
        "ADVERSARIAL_PASSED": 70,
        "FALSIFIED": 925,
        "KNOWN_RESULT": 1,
        "TRIVIAL": 2,
    }

    tf998_states = [row["lifecycle_state"] for row in by_id["TF-000998"]]
    assert "MATHEMATICALLY_INTERESTING" in tf998_states
    assert "NOVELTY_AUDIT" in tf998_states
    assert tf998_states[-1] == "FALSIFIED"
    counterexample = by_id["TF-000998"][-1]["counterexamples"][-1]
    assert counterexample["order"] == 25
    assert counterexample["values"]["domination_number"] == 7
    assert counterexample["values"]["matching_number"] == 12


def test_tf2_experiment_registry_record_is_unique_and_complete():
    experiments = _jsonl("data/registry/experiments.jsonl")
    ids = [row["experiment_id"] for row in experiments]
    assert ids.count("TF2-0001") == 1
    record = next(row for row in experiments if row["experiment_id"] == "TF2-0001")
    assert record["source_commit"] == EXPECTED_SOURCE
    assert record["scientific_actions_run"] == 36888114138
    assert record["raw_candidate_count"] == 998
    assert record["holdout_falsified_count"] == 924
    assert record["holdout_survivor_count"] == 74
    assert record["adversarial_falsified_count"] == 0
    assert record["adversarial_survivor_count"] == 74
    assert record["mathematically_interesting_reached_count"] == 1
    assert record["graduation_candidate_count"] == 0
    assert record["generation_parameters"]["burned_orders_excluded"] == [11]
    assert record["generation_parameters"]["holdout_visible_to_generator"] is False


def test_tf2_recorded_discovery_and_holdout_hashes_reproduce():
    spec = load_frozen_spec(Path("experiments/TF2-0001/spec.json"))
    invariants = list(spec["corpus_invariants"])

    dmin, dmax = spec["discovery_orders"]
    discovery = experiment_corpus_rows(
        dmin,
        dmax,
        invariants,
        role="discovery",
        source_commit=EXPECTED_SOURCE,
        experiment_id="TF2-0001",
    )
    assert len(discovery) == 200
    assert stable_hash(discovery) == EXPECTED_DISCOVERY_HASH

    hmin, hmax = spec["holdout_orders"]
    holdout = experiment_corpus_rows(
        hmin,
        hmax,
        invariants,
        role="holdout",
        source_commit=EXPECTED_SOURCE,
        experiment_id="TF2-0001",
    )
    assert len(holdout) == 551
    assert stable_hash(holdout) == EXPECTED_HOLDOUT_HASH


def test_tf2_recorded_adversarial_hash_reproduces_from_frozen_families():
    spec = load_frozen_spec(Path("experiments/TF2-0001/spec.json"))
    rows = _adversarial_rows(
        list(spec["corpus_invariants"]),
        EXPECTED_SOURCE,
        "TF2-0001",
    )
    assert len(rows) == 26
    assert all(int(row["order"]) != 11 for row in rows)
    assert stable_hash(rows) == EXPECTED_ADVERSARIAL_HASH
