"""Append-only JSONL candidate registry."""

from __future__ import annotations

import json
from pathlib import Path

from .schema import validate_candidate_record


class CandidateRegistry:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)

    def records(self) -> list[dict[str, object]]:
        result = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                result.append(json.loads(line))
        return result

    def next_id(self) -> str:
        max_number = 0
        for record in self.records():
            max_number = max(max_number, int(str(record["candidate_id"]).split("-")[1]))
        return f"TF-{max_number + 1:06d}"

    def append(self, record: dict[str, object]) -> None:
        validate_candidate_record(record)
        existing = self.records()
        same_id = [row for row in existing if row["candidate_id"] == record["candidate_id"]]
        if same_id and record["revision"] <= max(int(row["revision"]) for row in same_id):
            raise ValueError("candidate revisions must increase monotonically")
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
