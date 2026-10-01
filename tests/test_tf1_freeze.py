import json
from pathlib import Path

from treeforge.experiments import experiment_corpus_rows, load_frozen_spec
from treeforge.pipeline import stable_hash
from treeforge.registry.candidate_registry import CandidateRegistry
from treeforge.registry.schema import validate_candidate_record


def test_frozen_tf1_corpora_reproduce_committed_hashes():
    spec_path = Path("experiments/TF1-0001/spec.json")
    manifest = json.loads(Path("experiments/TF1-0001/manifest.json").read_text(encoding="utf-8"))
    spec = load_frozen_spec(spec_path)
    source_commit = manifest["source_commit"]
    invariants = list(spec["corpus_invariants"])

    discovery = experiment_corpus_rows(
        *spec["discovery_orders"],
        invariants,
        role="discovery",
        source_commit=source_commit,
        experiment_id=spec["experiment_id"],
    )
    holdout = experiment_corpus_rows(
        *spec["holdout_orders"],
        invariants,
        role="holdout",
        source_commit=source_commit,
        experiment_id=spec["experiment_id"],
    )

    assert len(discovery) == manifest["discovery_tree_count"] == 200
    assert len(holdout) == manifest["holdout_tree_count"] == 235
    assert stable_hash(discovery) == manifest["discovery_hash"]
    assert stable_hash(holdout) == manifest["holdout_hash"]
    assert all(row["corpus_role"] == "discovery" for row in discovery)
    assert all(row["corpus_role"] == "holdout" for row in holdout)


def test_latest_committed_candidate_revisions_validate():
    records = CandidateRegistry("data/registry/candidates.jsonl").records()
    latest = {}
    for record in records:
        current = latest.get(record["candidate_id"])
        if current is None or record["revision"] > current["revision"]:
            latest[record["candidate_id"]] = record
    assert latest
    for record in latest.values():
        validate_candidate_record(record)


def test_experiment_registry_has_unique_ids_and_tf1_result():
    rows = [
        json.loads(line)
        for line in Path("data/registry/experiments.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    ids = [row["experiment_id"] for row in rows]
    assert len(ids) == len(set(ids))
    tf1 = next(row for row in rows if row["experiment_id"] == "TF1-0001")
    assert tf1["raw_candidate_count"] == 0
    assert tf1["candidate_ids"] == []
    assert tf1["result"] == "NO_CANDIDATES_GENERATED"
