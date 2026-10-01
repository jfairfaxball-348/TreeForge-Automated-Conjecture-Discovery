import json

import experiments.tf3_discovery as tf3
from treeforge.conjecturing.txgraffiti_adapter import GeneratedStatement
from treeforge.registry.candidate_registry import CandidateRegistry


class FakeAdapter:
    def __init__(self, calls):
        self.calls = calls
        self.last_stage_counts = {
            "raw_generator_output": 1,
            "after_morgan": 1,
            "after_dalmatian": 1,
            "after_duplicate_removal": 1,
            "after_touch_count_sort": 1,
            "strengthened_equalities": 0,
            "final_discover_output": 1,
        }

    def discover(self, dataframe, **kwargs):
        assert self.calls == ["discovery"]
        assert kwargs["methods"] == ["ratios"]
        return [
            GeneratedStatement(
                "raw",
                "TxGraffiti",
                "0.4.1",
                {
                    "hypothesis": "True",
                    "conclusion": "domination_number <= order",
                    "lhs": "domination_number",
                    "operator": "<=",
                    "rhs": "order",
                    "discovery_touch_count": 2,
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
            "candidate_id": "TF-000999",
            "revision": 1,
            "statement": "seed",
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


def test_tf3_freezes_candidate_batch_before_fresh_holdout(monkeypatch, tmp_path):
    calls = []
    original = tf3.experiment_corpus_rows
    output_dir = tmp_path / "out"

    def wrapped(*args, **kwargs):
        role = kwargs["role"]
        if role == "holdout":
            assert (output_dir / "candidate_batch.json").is_file()
            assert (output_dir / "candidate_batch_freeze.json").is_file()
            freeze = json.loads(
                (output_dir / "candidate_batch_freeze.json").read_text(encoding="utf-8")
            )
            assert freeze["candidate_ids"] == ["TF-001000"]
            assert freeze["holdout_constructed"] is False
        calls.append(role)
        return original(*args, **kwargs)

    monkeypatch.setattr(tf3, "experiment_corpus_rows", wrapped)
    monkeypatch.setattr(
        tf3,
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
        "experiment_id": "TF3-0001",
        "status": "FROZEN",
        "frozen_at": "2026-10-01T18:35:00Z",
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
        "candidate_policy": {"next_permanent_candidate_id": "TF-001000"},
        "txgraffiti": {
            "object_symbol": "T",
            "hypothesis_payload": [],
            "methods": ["ratios"],
        },
    }
    spec_path = tmp_path / "spec.json"
    spec_path.write_text(json.dumps(spec), encoding="utf-8")
    registry_path = tmp_path / "candidates.jsonl"
    _seed_registry(registry_path)

    result = tf3.run(
        spec_path,
        output_dir,
        "TESTCOMMIT",
        registry_path=registry_path,
        adapter=FakeAdapter(calls),
    )

    assert calls == ["discovery", "holdout"]
    assert result["manifest"]["candidate_batch_frozen_before_holdout"] is True
    assert result["manifest"]["holdout_visible_to_generator"] is False
    assert result["manifest"]["candidate_ids"] == ["TF-001000"]
    assert result["final_candidates"][0]["lifecycle_state"] == "ADVERSARIAL_PASSED"
