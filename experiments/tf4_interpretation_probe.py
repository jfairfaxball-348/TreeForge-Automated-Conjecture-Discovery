#!/usr/bin/env python3
"""Post-gate TF4 interpretation probe using only exposed/burned material."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from experiments.tf2_discovery import _adversarial_rows as tf2_adversarial_rows
from experiments.tf2_discovery import _candidate_key, _counterexample
from experiments.tf3_discovery import _adversarial_rows as tf3_adversarial_rows
from treeforge.experiments import experiment_corpus_rows, load_frozen_spec

SCIENTIFIC_SOURCE = "d8e0874a22dde7f226431fc4f15a36adb8254efa"
EXPERIMENT_ID = "TF4-0001"


def _json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _history_keys(path: Path) -> set[tuple[str, str, str]]:
    rows = _json(path)
    return {
        _candidate_key(dict(row["metadata"]))
        for row in rows
    }


def run(output: Path) -> dict[str, object]:
    spec = load_frozen_spec(Path("experiments/TF4-0001/spec.json"))
    invariants = list(spec["corpus_invariants"])
    final = _json(Path("experiments/TF4-0001/scientific_artifact/final_candidates.json"))
    survivors = [
        row for row in final if row["lifecycle_state"] == "ADVERSARIAL_PASSED"
    ]

    exposed = experiment_corpus_rows(
        11,
        13,
        invariants,
        role="interpretation_exposed",
        source_commit=SCIENTIFIC_SOURCE,
        experiment_id=EXPERIMENT_ID,
    )
    tf2_hostile = tf2_adversarial_rows(invariants, SCIENTIFIC_SOURCE, EXPERIMENT_ID)
    tf3_hostile = tf3_adversarial_rows(invariants, SCIENTIFIC_SOURCE, EXPERIMENT_ID)
    tf2_keys = _history_keys(Path("experiments/TF2-0001/raw_txgraffiti_output.json"))
    tf3_keys = _history_keys(Path("experiments/TF3-0001/raw_txgraffiti_output.json"))

    rows = []
    for record in survivors:
        relation = dict(record["discovery_evidence"]["structured_relation"])
        key = _candidate_key(relation)
        exposed_failure = _counterexample(exposed, relation)
        tf2_failure = _counterexample(tf2_hostile, relation)
        tf3_failure = _counterexample(tf3_hostile, relation)
        rows.append(
            {
                "candidate_id": record["candidate_id"],
                "statement": record["statement"],
                "relation": relation,
                "exact_tf2_duplicate": key in tf2_keys,
                "exact_tf3_duplicate": key in tf3_keys,
                "exposed_orders_11_13_first_failure": exposed_failure,
                "tf2_hostile_first_failure": tf2_failure,
                "tf3_hostile_first_failure": tf3_failure,
            }
        )

    result = {
        "scientific_source_commit": SCIENTIFIC_SOURCE,
        "finite_survivor_count": len(survivors),
        "exposed_orders": [11, 12, 13],
        "exposed_tree_count": len(exposed),
        "historical_tf2_hostile_tree_count": len(tf2_hostile),
        "historical_tf3_hostile_tree_count": len(tf3_hostile),
        "rows": rows,
        "counts": {
            "fail_exposed_orders_11_13": sum(
                row["exposed_orders_11_13_first_failure"] is not None for row in rows
            ),
            "fail_tf2_hostile": sum(row["tf2_hostile_first_failure"] is not None for row in rows),
            "fail_tf3_hostile": sum(row["tf3_hostile_first_failure"] is not None for row in rows),
            "exact_tf2_duplicates": sum(row["exact_tf2_duplicate"] for row in rows),
            "exact_tf3_duplicates": sum(row["exact_tf3_duplicate"] for row in rows),
        },
        "note": (
            "This is post-gate mathematical interpretation using only burned/exposed data. "
            "It is not fresh TF4 validation evidence and does not alter the frozen run."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.output)


if __name__ == "__main__":
    main()
