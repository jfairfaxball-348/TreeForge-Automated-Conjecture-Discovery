from experiments.calibration import run


def test_end_to_end_known_calibration(tmp_path):
    result = run(tmp_path, "TESTCOMMIT", "2026-10-01T00:00:00Z")
    candidate = result["candidate"]
    assert candidate["candidate_id"] == "TF-000001"
    assert candidate["lifecycle_state"] == "KNOWN_RESULT"
    assert candidate["discovery_evidence"]["label"] == "KNOWN/CALIBRATION"
    assert candidate["holdout_status"]["status"] == "PASSED"
