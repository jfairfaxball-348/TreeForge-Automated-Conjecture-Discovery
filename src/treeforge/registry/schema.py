from __future__ import annotations

ACTIVE_STATES = {
    "OBSERVED",
    "CONJECTURED",
    "HOLDOUT_PASSED",
    "ADVERSARIAL_PASSED",
    "MATHEMATICALLY_INTERESTING",
    "NOVELTY_AUDIT",
    "GRADUATION_CANDIDATE",
    "GRADUATED",
}
SIDE_STATES = {
    "FALSIFIED",
    "KNOWN_RESULT",
    "TRIVIAL",
    "DUPLICATE",
    "ARTIFACT_OF_FEATURE_SET",
    "DEFERRED",
}
ALL_STATES = ACTIVE_STATES | SIDE_STATES

REQUIRED_FIELDS = {
    "candidate_id",
    "revision",
    "statement",
    "created_at",
    "generating_engine",
    "engine_version",
    "source_commit",
    "dataset_hash",
    "invariant_set",
    "hypotheses",
    "equality_or_sharp_examples",
    "discovery_evidence",
    "holdout_status",
    "adversarial_status",
    "counterexamples",
    "prior_art_status",
    "mathematical_interpretation",
    "lifecycle_state",
}


def validate_candidate_record(record: dict[str, object]) -> None:
    missing = REQUIRED_FIELDS - set(record)
    if missing:
        raise ValueError(f"candidate record missing fields: {sorted(missing)}")
    candidate_id = record["candidate_id"]
    if not isinstance(candidate_id, str) or not candidate_id.startswith("TF-") or len(candidate_id) != 9:
        raise ValueError("candidate_id must have form TF-000001")
    if record["lifecycle_state"] not in ALL_STATES:
        raise ValueError("unknown lifecycle state")
    if not isinstance(record["revision"], int) or record["revision"] < 1:
        raise ValueError("revision must be a positive integer")
