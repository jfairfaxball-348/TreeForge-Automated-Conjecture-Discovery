import json
from pathlib import Path

from treeforge.conjecturing.txgraffiti_adapter import GeneratedStatement
from treeforge.registry.candidate_registry import CandidateRegistry

import experiments.tf1_discovery as tf1


class FakeAdapter:
    def __init__(self, calls):
        self.calls = calls

    def discover(self, dataframe, **kwargs):
        assert self.calls == ["discovery"]
        assert "domination_number" in dataframe.columns
        return [GeneratedStatement("raw candidate", "TxGraffiti", "0.4.1")]


def test_holdout_is_constructed_only_after_discovery(monkeypatch, tmp_path):
    calls = []
    original = tf1.experiment_corpus_rows

    def wrapped(*args, **kwargs):
        calls.append(kwargs["role"])
        return original(*args, **kwargs)

    monkeypatch.setattr(tf1, "experiment_corpus_rows", wrapped)
    spec = {
        "experiment_id": "TEST",
        "status": "FROZEN",
        "frozen_at": "2026-10-01T00:00:00Z",
        "discovery_orders": [2, 3],
        "holdout_orders": [4, 4],
        "expected_discovery_tree_count": 2,
        "expected_holdout_tree_count": 2,
        "corpus_invariants": [
            "order",
            "edge_count",
            "degree_sum",
            "matching_number",
            "independence_number",
            "domination_number",
            "leaf_count",
        ],
        "target": "domination_number",
        "discovery_features": ["order", "leaf_count"],
        "hypotheses": ["finite", "simple", "unlabeled", "tree"],
        "txgraffiti": {"object_symbol": "T", "hypothesis_payload": []},
    }
    spec_path = tmp_path / "spec.json"
    spec_path.write_text(json.dumps(spec), encoding="utf-8")
    registry_path = tmp_path / "candidates.jsonl"
    registry = CandidateRegistry(registry_path)
    registry.append(
        {
            "candidate_id": "TF-000001",
            "revision": 1,
            "statement": "calibration",
            "created_at": "2026-10-01T00:00:00Z",
            "generating_engine": "test",
            "engine_version": "1",
            "source_commit": "OLD",
            "dataset_hash": "abc",
            "invariant_set": ["order"],
            "hypotheses": [],
            "equality_or_sharp_examples": [],
            "discovery_evidence": {},
            "holdout_status": {},
            "adversarial_status": {},
            "counterexamples": [],
            "prior_art_status": "test",
            "mathematical_interpretation": "test",
            "lifecycle_state": "KNOWN_RESULT",
        }
    )
    result = tf1.run(
        spec_path,
        tmp_path / "out",
        "TESTCOMMIT",
        registry_path=registry_path,
        adapter=FakeAdapter(calls),
    )
    assert calls == ["discovery", "holdout"]
    assert result["observed_candidates"][0]["candidate_id"] == "TF-000002"
    assert result["manifest"]["holdout_visible_to_generator"] is False
