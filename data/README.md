# Data policy

Generated corpora should normally be regenerated from code. Commit only compact outputs that are useful for provenance, review, or calibration.

`registry/candidates.jsonl` is the append-only candidate/revision record.  
`registry/experiments.jsonl` is the append-only experiment/provenance record.

Each JSONL line is a standalone object. Never delete a failed candidate from history merely because a later revision or counterexample supersedes it.
