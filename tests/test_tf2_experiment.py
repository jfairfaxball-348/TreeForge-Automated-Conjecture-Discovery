import json

import experiments.tf2_discovery as tf2
from treeforge.conjecturing.txgraffiti_adapter import GeneratedStatement
from treeforge.registry.candidate_registry import CandidateRegistry


class FakeAdapter:
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def discover(self, dataframe, **kwargs):
        assert (self.output_dir / "pre_generation_freeze.json").exists()
        freeze = json.loads(
            (self.output_dir / "pre_generation_freeze.json").read_text(encoding="utf-8")
        )
        assert freeze["holdout_visible_to_generator"] is False
        assert freeze["holdout_rows_persisted"] is False
        assert "domination_number" in dataframe.columns
        assert len(dataframe) == 2
        return [
            GeneratedStatement(
                "forall T: test",
                "TxGraffiti",
                "0.4.1",
                metadata={
                    "hypothesis": "True",
                    "lhs": "domination_number",
                    "operator": "<=",
                    "rhs": "order",
                    "discovery_touch_count": 1,
                    "discovery_valid": True,
                },
            )
        ]


def test_tf2_freezes_holdout_before_discovery_without_exposing_rows(tmp_path):
    spec = {
        "experiment_id": "TEST-TF2",
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
        "candidate_cap_policy": "NO_CAP",
        "candidate_normalization": {"raw_preservation": "test"},
        "preprocessing": {"random_seed": None},
        "txgraffiti": {
            "object_symbol": "T",
            "treeforge_hypothesis_payload": [],
        },
    }
    spec_path = tmp_path / "spec.json"
    spec_path.write_text(json.dumps(spec), encoding="utf-8")
    registry_path = tmp_path / "candidates.jsonl"
    CandidateRegistry(registry_path).append(
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

    out = tmp_path / "out"
    result = tf2.run(
        spec_path,
        out,
        "TESTCOMMIT",
        registry_path=registry_path,
        adapter=FakeAdapter(out),
    )
    assert result["observed_candidates"][0]["candidate_id"] == "TF-000002"
    assert not (out / "holdout.jsonl").exists()
    assert result["manifest"]["pre_generation_freeze_written_before_discovery"] is True
