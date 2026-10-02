#!/usr/bin/env python3
"""TF4 exposed-data diagnosis after the completed TF3 ratios-only experiment."""

from __future__ import annotations

import argparse
import json
import re
import time
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from statistics import median

import pandas as pd

from treeforge.conjecturing.expression import evaluate_expression, evaluate_relation
from treeforge.conjecturing.txgraffiti_adapter import TxGraffitiAdapter
from treeforge.experiments import experiment_corpus_rows
from treeforge.invariants.core import domination_number, maximal_independent_set_count
from treeforge.trees.canonical import generate_unlabeled_trees

DIAGNOSTIC_ID = "TF4-DIAG-0001"
TF2_SOURCE_COMMIT = "d091d88889fa72322bfc49a5531bc30b1f31b049"
TF3_SOURCE_COMMIT = "e23b44d24a7b87d6f67aa18749059540934b2767"
TARGET = "domination_number"
FEATURES = [
    "order",
    "leaf_count",
    "support_vertex_count",
    "max_degree",
    "diameter",
    "matching_number",
    "maximal_independent_set_count",
]


def _json(path: str) -> object:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _relation_key(metadata: dict[str, object]) -> tuple[str, str, str]:
    return (
        str(metadata["lhs"]),
        str(metadata["operator"]),
        str(metadata["rhs"]),
    )


def _rhs_features(rhs: str) -> tuple[str, ...]:
    return tuple(name for name in FEATURES if re.search(rf"\b{re.escape(name)}\b", rhs))


def _max_denominator(rhs: str) -> int:
    denominators = [int(value) for value in re.findall(r"-?\d+\s*/\s*(\d+)", rhs)]
    return max(denominators, default=1)


def _fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def _percentile(values: list[int], fraction: float) -> int:
    if not values:
        return 0
    ordered = sorted(values)
    index = min(len(ordered) - 1, int((len(ordered) - 1) * fraction + 0.999999))
    return ordered[index]


def _corpus(order: int) -> list[dict[str, object]]:
    return experiment_corpus_rows(
        order,
        order,
        [TARGET, *FEATURES],
        role="discovery",
        source_commit=TF3_SOURCE_COMMIT,
        experiment_id=DIAGNOSTIC_ID,
    )


def _extrema(rows: list[dict[str, object]], feature: str) -> dict[str, object]:
    ratios: list[tuple[Fraction, dict[str, object]]] = []
    for row in rows:
        value = int(row[feature])
        if value == 0:
            continue
        ratios.append((Fraction(int(row[TARGET]), value), row))
    lower = min(value for value, _ in ratios)
    upper = max(value for value, _ in ratios)
    lower_rows = [row for value, row in ratios if value == lower]
    upper_rows = [row for value, row in ratios if value == upper]
    return {
        "lower": _fraction_text(lower),
        "lower_touch_count": len(lower_rows),
        "lower_example_orders": sorted({int(row["order"]) for row in lower_rows}),
        "upper": _fraction_text(upper),
        "upper_touch_count": len(upper_rows),
        "upper_example_orders": sorted({int(row["order"]) for row in upper_rows}),
    }


def _ratio_coefficient(rhs: str, feature: str) -> Fraction:
    values = {name: 0 for name in FEATURES}
    if evaluate_expression(rhs, values) != 0:
        raise RuntimeError(f"ratios-only RHS unexpectedly has an intercept: {rhs}")
    values[feature] = 1
    return evaluate_expression(rhs, values)


def _first_failure(
    metadata: dict[str, object], rows: list[dict[str, object]]
) -> dict[str, object] | None:
    lhs, operator, rhs = _relation_key(metadata)
    for row in sorted(rows, key=lambda item: (int(item["order"]), str(item["tree_code"]))):
        if not evaluate_relation(lhs, operator, rhs, row):
            return {
                "order": int(row["order"]),
                "tree_code": str(row["tree_code"]),
                "values": {name: int(row[name]) for name in [TARGET, *FEATURES]},
            }
    return None


def _tf3_ratio_diagnosis(
    exposed_by_order: dict[int, list[dict[str, object]]],
    k1_row: dict[str, object],
) -> dict[str, object]:
    batch = _json("experiments/TF3-0001/candidate_batch.json")
    tf2_raw = _json("experiments/TF2-0001/raw_txgraffiti_output.json")
    holdout = _json("experiments/TF3-0001/holdout_summary.json")
    interpretation = _json("experiments/TF3-0001/interpretation_summary.json")
    assert isinstance(batch, list)
    assert isinstance(tf2_raw, list)
    assert isinstance(holdout, dict)
    assert isinstance(interpretation, dict)

    tf2_keys = {
        _relation_key(dict(item["metadata"])): f"TF-{int(item['raw_index']) + 1:06d}"
        for item in tf2_raw
    }
    cumulative: dict[int, list[dict[str, object]]] = {}
    running: list[dict[str, object]] = []
    for order in range(2, 14):
        running.extend(exposed_by_order[order])
        if order >= 10:
            cumulative[order] = list(running)

    rows = []
    drift_count = 0
    exact_overlap_count = 0
    touch_one_count = 0
    k1_failures = []
    for candidate in batch:
        metadata = dict(candidate["discovery_evidence"]["structured_relation"])
        rhs = str(metadata["rhs"])
        rhs_features = _rhs_features(rhs)
        if len(rhs_features) != 1:
            raise RuntimeError("TF3 candidate is not a one-feature ratio")
        feature = rhs_features[0]
        coefficient = _ratio_coefficient(rhs, feature)
        direction = "lower" if str(metadata["operator"]) == ">=" else "upper"
        extrema = {order: _extrema(cumulative[order], feature) for order in range(10, 14)}
        relevant = {order: extrema[order][direction] for order in range(10, 14)}
        first_drift_order = next(
            (
                order
                for order in range(11, 14)
                if relevant[order] != _fraction_text(coefficient)
            ),
            None,
        )
        if first_drift_order is not None:
            drift_count += 1

        key = _relation_key(metadata)
        tf2_match = tf2_keys.get(key)
        if tf2_match is not None:
            exact_overlap_count += 1
        touch = int(metadata["discovery_touch_count"])
        if touch == 1:
            touch_one_count += 1
        k1_valid = evaluate_relation(*key, k1_row)
        if not k1_valid:
            k1_failures.append(str(candidate["candidate_id"]))

        first_burned_failure = None
        for order in range(11, 14):
            failure = _first_failure(metadata, exposed_by_order[order])
            if failure is not None:
                first_burned_failure = failure
                break

        rows.append(
            {
                "candidate_id": candidate["candidate_id"],
                "relation": metadata["conclusion"],
                "feature": feature,
                "operator": metadata["operator"],
                "coefficient": _fraction_text(coefficient),
                "discovery_touch_count": touch,
                "sharp_example_orders": sorted(
                    {int(item["order"]) for item in candidate["equality_or_sharp_examples"]}
                ),
                "tf2_exact_match": tf2_match,
                "cumulative_extremal_coefficient_by_max_order": {
                    str(order): relevant[order] for order in range(10, 14)
                },
                "first_extremal_drift_order": first_drift_order,
                "first_burned_failure": first_burned_failure,
                "k1_valid_under_literal_all_tree_domain": k1_valid,
                "final_state": interpretation["final_records"][candidate["candidate_id"]][
                    "lifecycle_state"
                ],
            }
        )

    first_counterexamples = dict(holdout["first_counterexamples"])
    counterexample_groups: dict[str, list[str]] = defaultdict(list)
    for candidate_id, counterexample in first_counterexamples.items():
        counterexample_groups[str(counterexample["tree_code"])].append(str(candidate_id))
    grouped = []
    for code, ids in sorted(counterexample_groups.items(), key=lambda item: item[1]):
        example = first_counterexamples[ids[0]]
        grouped.append(
            {
                "candidate_ids": sorted(ids),
                "tree_code": code,
                "values": {
                    name: int(example["values"][name]) for name in [TARGET, *FEATURES]
                },
            }
        )

    feature_outcomes: dict[str, Counter[str]] = {
        name: Counter() for name in FEATURES
    }
    for row in rows:
        feature_outcomes[str(row["feature"])][str(row["final_state"])] += 1

    return {
        "candidate_count": len(rows),
        "exact_tf2_overlap_count": exact_overlap_count,
        "exact_tf2_overlap_fraction": f"{exact_overlap_count}/{len(rows)}",
        "touch_count_one_count": touch_one_count,
        "touch_count_one_fraction": f"{touch_one_count}/{len(rows)}",
        "extremal_coefficient_drift_by_order13_count": drift_count,
        "extremal_coefficient_drift_by_order13_fraction": f"{drift_count}/{len(rows)}",
        "literal_k1_failure_ids": sorted(k1_failures),
        "holdout_first_counterexample_distinct_tree_count": len(grouped),
        "holdout_first_counterexample_groups": grouped,
        "feature_final_state_counts": {
            feature: dict(sorted(counts.items()))
            for feature, counts in feature_outcomes.items()
        },
        "candidates": rows,
    }


def _pairwise_hull_diagnosis(
    discovery_rows: list[dict[str, object]],
    exposed_by_order: dict[int, list[dict[str, object]]],
    k1_row: dict[str, object],
) -> dict[str, object]:
    frame = pd.DataFrame(
        [{name: row[name] for name in [*FEATURES, TARGET]} for row in discovery_rows]
    )
    statements: dict[tuple[str, str, str], dict[str, object]] = {}
    stage_totals = Counter()
    per_input_pair_counts: dict[str, int] = {}

    started = time.perf_counter()
    for left, right in combinations(FEATURES, 2):
        adapter = TxGraffitiAdapter()
        generated = adapter.discover(
            frame,
            target=TARGET,
            features=[left, right],
            object_symbol="T",
            hypothesis=[],
            methods=["convex_hull"],
        )
        per_input_pair_counts[f"{left}+{right}"] = len(generated)
        for key, value in (adapter.last_stage_counts or {}).items():
            stage_totals[key] += int(value)
        for item in generated:
            metadata = dict(item.metadata or {})
            key = _relation_key(metadata)
            if key not in statements:
                statements[key] = {
                    "metadata": metadata,
                    "source_pairs": [],
                }
            statements[key]["source_pairs"].append([left, right])
    runtime_seconds = time.perf_counter() - started

    tf2_raw = _json("experiments/TF2-0001/raw_txgraffiti_output.json")
    assert isinstance(tf2_raw, list)
    tf2_keys = {_relation_key(dict(item["metadata"])) for item in tf2_raw}

    supports = Counter()
    operators = Counter()
    pair_distribution = Counter()
    denominators: list[int] = []
    touches: list[int] = []
    k1_fail_count = 0
    exact_tf2_overlap = 0
    unique_rows = []
    for key, item in statements.items():
        metadata = dict(item["metadata"])
        rhs = str(metadata["rhs"])
        rhs_features = _rhs_features(rhs)
        supports[len(rhs_features)] += 1
        operators[str(metadata["operator"])] += 1
        if len(rhs_features) == 2:
            pair_distribution["+".join(rhs_features)] += 1
        denominators.append(_max_denominator(rhs))
        touches.append(int(metadata.get("discovery_touch_count", 0)))
        if key in tf2_keys:
            exact_tf2_overlap += 1
        if not evaluate_relation(*key, k1_row):
            k1_fail_count += 1
        unique_rows.append(metadata)

    individual_survival: dict[str, int] = {}
    cumulative_survival: dict[str, int] = {}
    running_orders: list[dict[str, object]] = []
    for order in range(11, 14):
        order_rows = exposed_by_order[order]
        individual_survival[str(order)] = sum(
            _first_failure(metadata, order_rows) is None for metadata in unique_rows
        )
        running_orders.extend(order_rows)
        cumulative_survival[str(order)] = sum(
            _first_failure(metadata, running_orders) is None for metadata in unique_rows
        )

    burned_rows = [
        row for order in range(11, 14) for row in exposed_by_order[order]
    ]
    k1_valid_rows = [
        metadata
        for metadata in unique_rows
        if evaluate_relation(*_relation_key(metadata), k1_row)
    ]
    burned_survivors = [
        metadata
        for metadata in unique_rows
        if _first_failure(metadata, burned_rows) is None
    ]
    domain_and_burned_survivors = [
        metadata
        for metadata in burned_survivors
        if evaluate_relation(*_relation_key(metadata), k1_row)
    ]
    survivor_supports = Counter(
        len(_rhs_features(str(metadata["rhs"])))
        for metadata in domain_and_burned_survivors
    )
    survivor_pairs = Counter(
        "+".join(_rhs_features(str(metadata["rhs"])))
        for metadata in domain_and_burned_survivors
        if len(_rhs_features(str(metadata["rhs"]))) == 2
    )

    return {
        "feature_pair_run_count": 21,
        "runtime_seconds": runtime_seconds,
        "stage_totals_before_cross_run_exact_dedup": dict(stage_totals),
        "cross_run_exact_dedup_count": len(statements),
        "rhs_support_histogram": dict(sorted(supports.items())),
        "operator_histogram": dict(sorted(operators.items())),
        "two_feature_pair_distribution": dict(sorted(pair_distribution.items())),
        "per_input_pair_final_counts": dict(sorted(per_input_pair_counts.items())),
        "exact_tf2_overlap_count": exact_tf2_overlap,
        "exact_tf2_overlap_fraction": f"{exact_tf2_overlap}/{len(statements)}",
        "k1_literal_domain_failure_count": k1_fail_count,
        "k1_literal_domain_pass_count": len(k1_valid_rows),
        "burned_orders_11_to_13_survivor_count": len(burned_survivors),
        "k1_and_burned_orders_11_to_13_survivor_count": len(domain_and_burned_survivors),
        "k1_and_burned_survivor_rhs_support_histogram": dict(sorted(survivor_supports.items())),
        "k1_and_burned_survivor_two_feature_pair_distribution": dict(sorted(survivor_pairs.items())),
        "max_denominator": max(denominators, default=1),
        "median_max_denominator": int(median(denominators)) if denominators else 1,
        "p90_max_denominator": _percentile(denominators, 0.9),
        "touch_count_median": int(median(touches)) if touches else 0,
        "touch_count_p90": _percentile(touches, 0.9),
        "burned_order_individual_survivor_counts": individual_survival,
        "burned_orders_11_through_n_cumulative_survivor_counts": cumulative_survival,
        "note": (
            "All order-11/12/13 evaluations are diagnosis on burned data. "
            "They are not fresh TF4 validation evidence."
        ),
    }


def _timing_only_order14() -> dict[str, object]:
    started = time.perf_counter()
    trees = generate_unlabeled_trees(14, 14)
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
        "order": 14,
        "tree_count": len(trees),
        "generation_seconds": generation_seconds,
        "domination_number_seconds": domination_seconds,
        "maximal_independent_set_count_seconds": maximal_is_seconds,
        "values_persisted_or_reported": False,
        "candidate_specific_comparison_performed": False,
        "purpose": "runtime feasibility only; order 14 remains uninspected candidate-validation data",
    }


def run(output: Path, *, skip_order14_timing: bool = False) -> dict[str, object]:
    exposed_by_order = {order: _corpus(order) for order in range(1, 14)}
    discovery_rows = [
        row for order in range(2, 11) for row in exposed_by_order[order]
    ]
    k1_rows = exposed_by_order[1]
    if len(k1_rows) != 1:
        raise RuntimeError("expected exactly one unlabeled order-1 tree")
    k1_row = k1_rows[0]

    ratios = _tf3_ratio_diagnosis(exposed_by_order, k1_row)
    pairwise = _pairwise_hull_diagnosis(
        discovery_rows,
        exposed_by_order,
        k1_row,
    )
    result = {
        "diagnostic_id": DIAGNOSTIC_ID,
        "data_boundary": {
            "candidate_selection_data": (
                "Only already-exposed orders 1-13 and committed TF2/TF3 outputs are used."
            ),
            "burned_orders": list(range(1, 14)),
            "order14": (
                "Timing only: no invariant value is persisted, printed, ranked, or compared "
                "with any candidate."
            ),
        },
        "verified_tf3_outcome": {
            "pipeline_count": 12,
            "final_states": {"FALSIFIED": 11, "TRIVIAL": 1},
            "mathematically_interesting": 0,
        },
        "ratios_only": ratios,
        "literal_hypothesis_diagnosis": {
            "declared_domain": "every finite simple tree",
            "discovery_domain": "orders 2-10",
            "mismatch": True,
            "k1_falsified_candidate_ids": ratios["literal_k1_failure_ids"],
            "nontrivial_tree_hypothesis_would_change_generator_output": False,
            "reason": (
                "The discovery dataframe already contains only nontrivial trees, so changing "
                "the statement domain to order>=2 would not change the ratios generated from "
                "orders 2-10. It would only change downstream truth status for K1-sensitive forms."
            ),
        },
        "pairwise_convex_hulls": pairwise,
        "order14_timing_only_feasibility": (
            {
                "skipped": True,
                "reason": "Already measured without value inspection in initial TF4 diagnostic run 36972524602.",
            }
            if skip_order14_timing
            else _timing_only_order14()
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    concise = {
        "diagnostic_id": DIAGNOSTIC_ID,
        "ratios_exact_tf2_overlap": ratios["exact_tf2_overlap_fraction"],
        "ratios_touch_one": ratios["touch_count_one_fraction"],
        "ratios_drift_by_order13": ratios["extremal_coefficient_drift_by_order13_fraction"],
        "ratios_k1_failures": ratios["literal_k1_failure_ids"],
        "ratios_holdout_counterexample_tree_count": ratios[
            "holdout_first_counterexample_distinct_tree_count"
        ],
        "pairwise_final": pairwise["cross_run_exact_dedup_count"],
        "pairwise_support_histogram": pairwise["rhs_support_histogram"],
        "pairwise_exact_tf2_overlap": pairwise["exact_tf2_overlap_fraction"],
        "pairwise_cumulative_burned_survivors": pairwise[
            "burned_orders_11_through_n_cumulative_survivor_counts"
        ],
        "pairwise_k1_failures": pairwise["k1_literal_domain_failure_count"],
        "pairwise_k1_and_burned_survivors": pairwise[
            "k1_and_burned_orders_11_to_13_survivor_count"
        ],
        "pairwise_k1_and_burned_support": pairwise[
            "k1_and_burned_survivor_rhs_support_histogram"
        ],
        "pairwise_max_denominator": pairwise["max_denominator"],
        "order14_timing_only": result["order14_timing_only_feasibility"],
    }
    print(json.dumps(concise, indent=2, sort_keys=True))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--skip-order14-timing", action="store_true")
    args = parser.parse_args()
    run(args.output, skip_order14_timing=args.skip_order14_timing)


if __name__ == "__main__":
    main()
