#!/usr/bin/env python3
"""TF3 diagnosis using only exposed TF2 discovery data plus timing-only order-13 feasibility."""

from __future__ import annotations

import argparse
import json
import re
import time
from itertools import combinations
from pathlib import Path

import pandas as pd

from treeforge.conjecturing.txgraffiti_adapter import TxGraffitiAdapter
from treeforge.experiments import experiment_corpus_rows, load_frozen_spec
from treeforge.invariants.core import domination_number, maximal_independent_set_count
from treeforge.trees.canonical import generate_unlabeled_trees

TF2_SOURCE_COMMIT = "d091d88889fa72322bfc49a5531bc30b1f31b049"
FEATURES = [
    "order",
    "leaf_count",
    "support_vertex_count",
    "max_degree",
    "diameter",
    "matching_number",
    "maximal_independent_set_count",
]


def _rhs_support(rhs: str) -> int:
    return sum(bool(re.search(rf"\\b{re.escape(name)}\\b", rhs)) for name in FEATURES)


def _max_denominator(rhs: str) -> int:
    denominators = [int(value) for value in re.findall(r"-?\\d+\\s*/\\s*(\\d+)", rhs)]
    return max(denominators, default=1)


def _summarize(statements) -> dict[str, object]:
    rows = []
    for item in statements:
        metadata = dict(item.metadata or {})
        rhs = str(metadata.get("rhs", ""))
        rows.append(
            {
                "key": (
                    str(metadata.get("lhs")),
                    str(metadata.get("operator")),
                    rhs,
                ),
                "rhs_support": _rhs_support(rhs),
                "max_denominator": _max_denominator(rhs),
                "touch_count": int(metadata.get("discovery_touch_count", 0)),
            }
        )
    unique = {row["key"]: row for row in rows}
    values = list(unique.values())
    support_histogram: dict[str, int] = {}
    for row in values:
        key = str(row["rhs_support"])
        support_histogram[key] = support_histogram.get(key, 0) + 1
    return {
        "final_count": len(values),
        "rhs_support_histogram": support_histogram,
        "max_denominator": max((row["max_denominator"] for row in values), default=1),
        "max_touch_count": max((row["touch_count"] for row in values), default=0),
        "keys": [list(row["key"]) for row in values],
    }


def _run_variant(frame, *, methods, feature_sets) -> dict[str, object]:
    started = time.perf_counter()
    all_statements = []
    stage_totals = {
        "raw_generator_output": 0,
        "after_morgan": 0,
        "after_dalmatian": 0,
        "after_duplicate_removal": 0,
        "after_touch_count_sort": 0,
        "strengthened_equalities": 0,
        "final_discover_output": 0,
    }
    for features in feature_sets:
        adapter = TxGraffitiAdapter()
        statements = adapter.discover(
            frame,
            target="domination_number",
            features=list(features),
            object_symbol="T",
            hypothesis=[],
            methods=list(methods),
        )
        all_statements.extend(statements)
        if adapter.last_stage_counts:
            for key in stage_totals:
                stage_totals[key] += int(adapter.last_stage_counts.get(key, 0))
    summary = _summarize(all_statements)
    summary["runtime_seconds"] = time.perf_counter() - started
    summary["stage_totals_before_cross_run_exact_dedup"] = stage_totals
    summary["feature_set_count"] = len(feature_sets)
    summary.pop("keys")
    return summary


def _timing_only_order13() -> dict[str, object]:
    started = time.perf_counter()
    trees = generate_unlabeled_trees(13, 13)
    generation_seconds = time.perf_counter() - started

    started = time.perf_counter()
    for graph in trees:
        domination_number(graph)
    domination_seconds = time.perf_counter() - started

    started = time.perf_counter()
    for graph in trees:
        maximal_independent_set_count(graph)
    maximal_is_seconds = time.perf_counter() - started

    return {
        "order": 13,
        "tree_count": len(trees),
        "generation_seconds": generation_seconds,
        "domination_number_seconds": domination_seconds,
        "maximal_independent_set_count_seconds": maximal_is_seconds,
        "values_persisted_or_reported": False,
        "purpose": "runtime feasibility only; not candidate validation",
    }


def run(output: Path) -> dict[str, object]:
    spec = load_frozen_spec(Path("experiments/TF2-0001/spec.json"))
    discovery = experiment_corpus_rows(
        *spec["discovery_orders"],
        list(spec["corpus_invariants"]),
        role="discovery",
        source_commit=TF2_SOURCE_COMMIT,
        experiment_id="TF2-0001",
    )
    frame = pd.DataFrame(
        [{name: row[name] for name in [*FEATURES, "domination_number"]} for row in discovery]
    )

    ratios = _run_variant(
        frame,
        methods=["ratios"],
        feature_sets=[FEATURES],
    )
    pairwise = _run_variant(
        frame,
        methods=["convex_hull"],
        feature_sets=list(combinations(FEATURES, 2)),
    )

    raw = json.loads(
        Path("experiments/TF2-0001/raw_txgraffiti_output.json").read_text(encoding="utf-8")
    )
    support_gate = []
    for item in raw:
        metadata = item["metadata"]
        rhs = str(metadata["rhs"])
        if _rhs_support(rhs) <= 2:
            support_gate.append(item)
    if ratios["rhs_support_histogram"] != {"1": ratios["final_count"]}:
        raise RuntimeError("ratios-only diagnostic must emit one-feature RHS forms")
    if len(support_gate) != 12:
        raise RuntimeError("exposed TF2 support<=2 diagnostic count must reproduce as 12")

    support_gate_summary = {
        "final_count": len(support_gate),
        "rhs_support_histogram": {
            str(size): sum(
                _rhs_support(str(item["metadata"]["rhs"])) == size for item in support_gate
            )
            for size in [1, 2]
        },
        "generation_stage_counts_unchanged_from_tf2": {
            "raw_generator_output": 23268,
            "after_dalmatian": 10753,
            "after_duplicate_removal": 998,
        },
        "note": "Diagnostic estimate only: mechanical RHS-support <= 2 admission gate on exposed TF2 final output.",
    }

    result = {
        "diagnostic_id": "TF3-DIAG-0001",
        "data_boundary": "Only TF2 discovery rows were used for candidate-generation comparisons.",
        "tf2_dense_output_baseline": {
            "final_count": 998,
            "rhs_support_1": 8,
            "rhs_support_2": 4,
            "rhs_support_4_or_more": 979,
            "rhs_support_7": 689,
        },
        "variants": {
            "A_ratios_only": ratios,
            "C_full_generation_rhs_support_at_most_2": support_gate_summary,
            "D_pairwise_convex_hulls": pairwise,
        },
        "fresh_order13_feasibility": _timing_only_order13(),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.output)


if __name__ == "__main__":
    main()
