#!/usr/bin/env python3
"""Diagnose TF1 zero yield without using TF1 holdout for experiment design."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from treeforge.conjecturing.txgraffiti_adapter import TxGraffitiAdapter
from treeforge.experiments import experiment_corpus_rows, load_frozen_spec
from treeforge.feature_audit import audit_columns, known_identity_violations
from treeforge.pipeline import dependency_versions, stable_hash

TF1_SOURCE_COMMIT = "e5175b5f5667195adf64ccae75e3dc42f0061086"
WITHHELD_DIAGNOSTIC_FEATURES = [
    "radius",
    "eccentricity_sum",
    "independence_number",
    "wiener_index",
    "cherry_count",
]


def _compact_stages(stages: dict[str, dict[str, object]]) -> dict[str, object]:
    return {
        name: {
            "count": payload["count"],
            "sample_statements": list(payload["statements"])[:5],
        }
        for name, payload in stages.items()
    }


def _geometry(
    rows: list[dict[str, object]], columns: list[str], target: str
) -> dict[str, object]:
    frame = pd.DataFrame([{name: row[name] for name in columns} for row in rows])
    stats = {}
    for name in columns:
        values = frame[name]
        counts = values.value_counts().sort_index()
        stats[name] = {
            "min": int(values.min()),
            "max": int(values.max()),
            "distinct_values": int(values.nunique()),
            "repeated_rows": int(len(values) - values.nunique()),
            "zero_count": int((values == 0).sum()),
            "frequencies": {str(int(k)): int(v) for k, v in counts.items()},
        }

    corr = frame.corr(method="pearson")
    correlation = {
        row: {
            col: (
                None
                if pd.isna(corr.loc[row, col])
                else round(float(corr.loc[row, col]), 6)
            )
            for col in columns
        }
        for row in columns
    }

    target_values = frame[target]
    lo, hi = int(target_values.min()), int(target_values.max())
    extreme_examples = {
        "minimum": {
            "value": lo,
            "tree_codes": [row["tree_code"] for row in rows if row[target] == lo][:5],
        },
        "maximum": {
            "value": hi,
            "tree_codes": [row["tree_code"] for row in rows if row[target] == hi][:5],
        },
    }

    matrix = frame.to_numpy(dtype=float)
    affine_rank = int(np.linalg.matrix_rank(matrix - matrix[0])) if len(matrix) else 0
    return {
        "column_statistics": stats,
        "audit": audit_columns(rows, columns),
        "pearson_correlation_descriptive_only": correlation,
        "unique_joint_rows": int(frame.drop_duplicates().shape[0]),
        "affine_rank": affine_rank,
        "ambient_dimension": len(columns),
        "target_extreme_examples": extreme_examples,
    }


def run(output: Path) -> dict[str, object]:
    spec = load_frozen_spec(Path("experiments/TF1-0001/spec.json"))
    manifest = json.loads(
        Path("experiments/TF1-0001/manifest.json").read_text(encoding="utf-8")
    )
    committed_raw = json.loads(
        Path("experiments/TF1-0001/raw_txgraffiti_output.json").read_text(
            encoding="utf-8"
        )
    )

    invariants = list(spec["corpus_invariants"])
    features = list(spec["discovery_features"])
    target = str(spec["target"])
    dmin, dmax = spec["discovery_orders"]
    discovery = experiment_corpus_rows(
        dmin,
        dmax,
        invariants,
        role="discovery",
        source_commit=TF1_SOURCE_COMMIT,
        experiment_id="TF1-0001",
    )
    discovery_hash = stable_hash(discovery)
    if discovery_hash != manifest["discovery_hash"]:
        raise RuntimeError("TF1 discovery hash did not reproduce")
    discovery_identity_failures = known_identity_violations(discovery)
    if discovery_identity_failures:
        raise RuntimeError("TF1 discovery identity check failed")

    # Recreate TF1 holdout only to verify its frozen hash and exact identities.
    # No holdout values or descriptive statistics enter the diagnosis/design record.
    hmin, hmax = spec["holdout_orders"]
    holdout = experiment_corpus_rows(
        hmin,
        hmax,
        invariants,
        role="holdout",
        source_commit=TF1_SOURCE_COMMIT,
        experiment_id="TF1-0001",
    )
    holdout_hash = stable_hash(holdout)
    if holdout_hash != manifest["holdout_hash"]:
        raise RuntimeError("TF1 holdout hash did not reproduce")
    holdout_identity_failures = known_identity_violations(holdout)
    if holdout_identity_failures:
        raise RuntimeError("TF1 holdout identity check failed")
    del holdout

    frame = pd.DataFrame(
        [{name: row[name] for name in [*features, target]} for row in discovery]
    )
    adapter = TxGraffitiAdapter()

    frozen_stages = adapter.pipeline_diagnostics(
        frame,
        target=target,
        features=features,
        object_symbol=spec["txgraffiti"]["object_symbol"],
        hypothesis=spec["txgraffiti"]["hypothesis_payload"],
        preserve_empty_hypothesis=True,
    )
    if any(payload["count"] != 0 for payload in frozen_stages.values()):
        raise RuntimeError("frozen TF1 semantics unexpectedly generated candidates")
    if committed_raw != []:
        raise RuntimeError("committed TF1 raw output is no longer empty")

    synthetic = pd.DataFrame({"x": [1, 2, 3, 4, 5], "y": [2, 4, 6, 8, 10]})
    synthetic_frozen = adapter.pipeline_diagnostics(
        synthetic,
        target="y",
        features=["x"],
        object_symbol="n",
        hypothesis=[],
        preserve_empty_hypothesis=True,
    )
    synthetic_corrected = adapter.pipeline_diagnostics(
        synthetic,
        target="y",
        features=["x"],
        object_symbol="n",
        hypothesis=[],
    )
    if synthetic_frozen["raw_generator_output"]["count"] != 0:
        raise RuntimeError("legacy empty-payload calibration did not reproduce suppression")
    if synthetic_corrected["raw_generator_output"]["count"] < 2:
        raise RuntimeError("corrected adapter failed synthetic raw-generation calibration")
    if synthetic_corrected["after_touch_count_sort"]["count"] < 1:
        raise RuntimeError("corrected adapter failed synthetic final-stage calibration")

    diagnostic_columns = [target, *features, *WITHHELD_DIAGNOSTIC_FEATURES]
    result = {
        "diagnostic_id": "TF2-DIAG-0001",
        "tf1_reproduction": {
            "source_commit": TF1_SOURCE_COMMIT,
            "discovery_tree_count": len(discovery),
            "discovery_hash": discovery_hash,
            "expected_discovery_hash": manifest["discovery_hash"],
            "holdout_tree_count": manifest["holdout_tree_count"],
            "holdout_hash": holdout_hash,
            "expected_holdout_hash": manifest["holdout_hash"],
            "committed_raw_candidate_count": len(committed_raw),
            "dependency_versions": dependency_versions(
                ["networkx", "pandas", "txgraffiti"]
            ),
            "discovery_identity_violations": discovery_identity_failures,
            "holdout_identity_violations": holdout_identity_failures,
        },
        "root_cause": {
            "classification": "TREEFORGE_ADAPTER_CONFIGURATION_SEMANTIC_MISMATCH",
            "frozen_payload": [],
            "upstream_semantics": (
                "TxGraffiti ConjecturePlayground.generate treats hypothesis=None as "
                "the always-true base predicate, but hypothesis=[] produces an empty "
                "hypothesis iteration and invokes no generators."
            ),
            "treeforge_semantics": (
                "An empty hypothesis payload means no extra predicate beyond the tree universe."
            ),
            "fix": (
                "Normalize an empty TreeForge hypothesis payload to None inside the "
                "TxGraffiti adapter."
            ),
        },
        "tf1_frozen_pipeline": _compact_stages(frozen_stages),
        "synthetic_calibration": {
            "relation": "y = 2*x on five positive integer rows",
            "frozen_semantics": _compact_stages(synthetic_frozen),
            "corrected_semantics": _compact_stages(synthetic_corrected),
        },
        "discovery_only_geometry": _geometry(
            discovery, diagnostic_columns, target
        ),
        "holdout_use_boundary": (
            "TF1 order-11 holdout was regenerated only for frozen hash/identity "
            "verification; its values were not used for geometry analysis, feature "
            "selection, method selection, or TF2 tuning."
        ),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.output)


if __name__ == "__main__":
    main()
