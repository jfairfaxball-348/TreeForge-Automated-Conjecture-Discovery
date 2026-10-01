import json

import experiments.tf2_discovery as tf2
from treeforge.conjecturing.txgraffiti_adapter import GeneratedStatement
from treeforge.registry.candidate_registry import CandidateRegistry


class FakeAdapter:
    def __init__(self, calls):
        self.calls = calls

    def discover(self, dataframe, **kwargs):
        assert self.calls == ["discovery"]
        return [
            GeneratedStatement(
                "raw",
                "TxGraffiti",
                "0.4.1",
                {
                    "hypothesis": "TRUE",
                    "conclusion": "domination_number <= order",
                    "lhs": "domination_number",
                    "operator": "<=",
                    "rhs": "order",
                    "discovery_touch_count": 0,
                    "discovery_valid": True,
                },
            )
        ]

    def provenance(self):
        return {"package": "txgraffiti", "version": "0.4.1", "source_commit": "PIN"}


def _seed_registry(path):
    registry = CandidateRegistry(path)
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


def test_tf2_holdout_after_generation_and_ids(monkeypatch, tmp_path):
    calls = []
    original = tf2.experiment_corpus_rows

    def wrapped(*args, **kwargs):
        calls.append(kwargs["role"])
        return original(*args, **kwargs)

    monkeypatch.setattr(tf2, "experiment_corpus_rows", wrapped)
    monkeypatch.setattr(
        tf2,
        "_adversarial_rows",
        lambda invariant_names, source_commit, experiment_id: [
            {
                "tree_code": "x",
                "order": 4,
                "corpus_role": "adversarial",
                "source_commit": source_commit,
                "experiment_id": experiment_id,
                "generation_parameters": {"family": "test"},
                "edge_count": 3,
                "degree_sum": 6,
                "matching_number": 2,
                "independence_number": 2,
                "domination_number": 2,
            }
        ],
    )
    spec = {
        "experiment_id": "TF2-0001",
        "status": "FROZEN",
        "frozen_at": "2026-10-01T12:00:00Z",
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
        ],
        "target": "domination_number",
        "discovery_features": ["order"],
        "hypotheses": ["finite", "simple", "unlabeled", "tree"],
        "txgraffiti": {"object_symbol": "T", "hypothesis_payload": []},
    }
    spec_path = tmp_path / "spec.json"
    spec_path.write_text(json.dumps(spec), encoding="utf-8")
    registry_path = tmp_path / "candidates.jsonl"
    _seed_registry(registry_path)

    result = tf2.run(
        spec_path,
        tmp_path / "out",
        "TESTCOMMIT",
        registry_path=registry_path,
        adapter=FakeAdapter(calls),
    )
    assert calls == ["discovery", "holdout"]
    assert result["manifest"]["holdout_visible_to_generator"] is False
    assert result["manifest"]["candidate_ids"] == ["TF-000002"]
    assert result["final_candidates"][0]["lifecycle_state"] == "ADVERSARIAL_PASSED"
