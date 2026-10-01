from treeforge.registry.candidate_registry import CandidateRegistry


def _record(candidate_id: str, revision: int):
    return {
        "candidate_id": candidate_id,
        "revision": revision,
        "statement": "x = x",
        "created_at": "2026-10-01T00:00:00Z",
        "generating_engine": "test",
        "engine_version": "1",
        "dataset_hash": "abc",
        "invariant_set": ["x"],
        "hypotheses": [],
        "equality_or_sharp_examples": [],
        "discovery_evidence": {},
        "holdout_status": {},
        "adversarial_status": {},
        "counterexamples": [],
        "prior_art_status": "test",
        "mathematical_interpretation": "test",
        "lifecycle_state": "OBSERVED",
    }


def test_registry_ids_and_revisions(tmp_path):
    registry = CandidateRegistry(tmp_path / "candidates.jsonl")
    assert registry.next_id() == "TF-000001"
    registry.append(_record("TF-000001", 1))
    assert registry.next_id() == "TF-000002"
    registry.append(_record("TF-000001", 2))
    assert len(registry.records()) == 2
