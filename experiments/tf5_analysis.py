#!/usr/bin/env python3
"""Reproduce the exposed-data TF5 analysis for TF-001028 and the MIS facet fan."""

from __future__ import annotations

import argparse
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

import networkx as nx

from treeforge.invariants.core import matching_number, support_vertex_count
from treeforge.trees.canonical import generate_unlabeled_trees
from treeforge.trees.families import broom, caterpillar, double_star, path, spider, star

TF5_SUMMARY = Path("experiments/TF5-TF001028/analysis_summary.json")
MIS_IDS = [
    "TF-001033",
    "TF-001034",
    "TF-001037",
    "TF-001090",
    "TF-001091",
    "TF-001093",
    "TF-001095",
    "TF-001098",
    "TF-001099",
    "TF-001134",
    "TF-001135",
    "TF-001137",
    "TF-001139",
    "TF-001140",
    "TF-001141",
    "TF-001142",
    "TF-001144",
    "TF-001145",
    "TF-001154",
    "TF-001155",
]

RELATIONS = {
    "TF-001033": ("<=", {"maximal_independent_set_count": Fraction(1, 2)}, Fraction(1, 2)),
    "TF-001034": ("<=", {"maximal_independent_set_count": Fraction(1, 3)}, Fraction(4, 3)),
    "TF-001037": ("<=", {"maximal_independent_set_count": Fraction(1, 5)}, Fraction(12, 5)),
    "TF-001090": (
        "<=",
        {"support_vertex_count": Fraction(-1), "maximal_independent_set_count": Fraction(1)},
        Fraction(1),
    ),
    "TF-001091": (
        "<=",
        {"support_vertex_count": Fraction(2, 5), "maximal_independent_set_count": Fraction(1, 5)},
        Fraction(4, 5),
    ),
    "TF-001093": (
        "<=",
        {"support_vertex_count": Fraction(3, 7), "maximal_independent_set_count": Fraction(1, 7)},
        Fraction(8, 7),
    ),
    "TF-001095": (
        "<=",
        {"support_vertex_count": Fraction(3, 8), "maximal_independent_set_count": Fraction(1, 8)},
        Fraction(3, 2),
    ),
    "TF-001098": (
        ">=",
        {"support_vertex_count": Fraction(9, 4), "maximal_independent_set_count": Fraction(-1, 4)},
        Fraction(-3),
    ),
    "TF-001099": (
        "<=",
        {"support_vertex_count": Fraction(5, 9), "maximal_independent_set_count": Fraction(1, 9)},
        Fraction(10, 9),
    ),
    "TF-001134": (
        "<=",
        {"diameter": Fraction(-1), "maximal_independent_set_count": Fraction(1)},
        Fraction(2),
    ),
    "TF-001135": (
        "<=",
        {"diameter": Fraction(-1, 2), "maximal_independent_set_count": Fraction(1, 2)},
        Fraction(5, 2),
    ),
    "TF-001137": (
        "<=",
        {"diameter": Fraction(1, 4), "maximal_independent_set_count": Fraction(1, 4)},
        Fraction(3, 4),
    ),
    "TF-001139": (
        "<=",
        {"diameter": Fraction(1, 6), "maximal_independent_set_count": Fraction(1, 6)},
        Fraction(11, 6),
    ),
    "TF-001140": (
        ">=",
        {"diameter": Fraction(3, 2), "maximal_independent_set_count": Fraction(-1, 2)},
        Fraction(-3),
    ),
    "TF-001141": (
        "<=",
        {"diameter": Fraction(-1, 4), "maximal_independent_set_count": Fraction(1, 4)},
        Fraction(13, 4),
    ),
    "TF-001142": (
        "<=",
        {"diameter": Fraction(3, 8), "maximal_independent_set_count": Fraction(1, 8)},
        Fraction(11, 8),
    ),
    "TF-001144": (
        "<=",
        {"diameter": Fraction(-5, 4), "maximal_independent_set_count": Fraction(1, 2)},
        Fraction(29, 4),
    ),
    "TF-001145": (
        "<=",
        {"diameter": Fraction(-3), "maximal_independent_set_count": Fraction(1)},
        Fraction(15),
    ),
    "TF-001154": (
        ">=",
        {"matching_number": Fraction(2), "maximal_independent_set_count": Fraction(-1)},
        Fraction(1),
    ),
    "TF-001155": (
        ">=",
        {"matching_number": Fraction(5, 2), "maximal_independent_set_count": Fraction(-1, 2)},
        Fraction(-3),
    ),
}


def domination_number_dp(graph: nx.Graph) -> int:
    """Exact tree DP for domination number, independent of the exhaustive core routine."""
    root = next(iter(graph.nodes()))
    inf = graph.number_of_nodes() + 1

    def visit(vertex: int, parent: int | None) -> tuple[int, int, int]:
        children = [visit(u, vertex) for u in graph.neighbors(vertex) if u != parent]
        selected = 1 + sum(min(a, b, c) for a, b, c in children)
        base = sum(min(a, b) for a, b, _ in children)
        needs_parent = base
        dominated_by_child = (
            inf
            if not children
            else base + min(a - min(a, b) for a, b, _ in children)
        )
        return selected, dominated_by_child, needs_parent

    selected, dominated, _ = visit(root, None)
    return min(selected, dominated)


def maximal_independent_set_count_dp(graph: nx.Graph) -> int:
    """Exact count of independent dominating sets, hence maximal independent sets."""
    root = next(iter(graph.nodes()))

    def visit(vertex: int, parent: int | None) -> tuple[int, int, int]:
        children = [visit(u, vertex) for u in graph.neighbors(vertex) if u != parent]
        selected = math.prod(dominated + needs_parent for _, dominated, needs_parent in children)
        no_selected_child = math.prod(dominated for _, dominated, _ in children)
        child_closed = math.prod(selected_child + dominated for selected_child, dominated, _ in children)
        dominated_by_child = child_closed - no_selected_child
        needs_parent = no_selected_child
        return selected, dominated_by_child, needs_parent

    selected, dominated, _ = visit(root, None)
    return selected + dominated


def values(graph: nx.Graph) -> dict[str, int]:
    return {
        "order": graph.number_of_nodes(),
        "diameter": nx.diameter(graph),
        "support_vertex_count": support_vertex_count(graph),
        "matching_number": matching_number(graph),
        "maximal_independent_set_count": maximal_independent_set_count_dp(graph),
        "domination_number": domination_number_dp(graph),
    }


def target_slack(row: dict[str, int]) -> int:
    return 2 * row["order"] + 1 - 3 * row["domination_number"] - row["diameter"]


def relation_bound(row: dict[str, int], relation: tuple[str, dict[str, Fraction], Fraction]) -> Fraction:
    _, coefficients, constant = relation
    return constant + sum(coefficient * row[name] for name, coefficient in coefficients.items())


def relation_slack(row: dict[str, int], relation: tuple[str, dict[str, Fraction], Fraction]) -> Fraction:
    operator, _, _ = relation
    bound = relation_bound(row, relation)
    gamma = Fraction(row["domination_number"])
    return bound - gamma if operator == "<=" else gamma - bound


def exposed_rows() -> list[dict[str, int]]:
    return [values(graph) for graph in generate_unlabeled_trees(1, 14)]


def family_search() -> dict[str, object]:
    result: dict[str, dict[str, int]] = {}

    def record(name: str, graph: nx.Graph) -> None:
        slack = target_slack(values(graph))
        row = result.setdefault(name, {"count": 0, "max_order": 0, "minimum_integer_slack": 10**9})
        row["count"] += 1
        row["max_order"] = max(row["max_order"], graph.number_of_nodes())
        row["minimum_integer_slack"] = min(row["minimum_integer_slack"], slack)
        if slack < 0:
            raise AssertionError(f"TF-001028 counterexample in {name}: slack={slack}")

    for order in range(1, 81):
        record("paths", path(order))
    for leaves in range(1, 80):
        record("stars", star(leaves))
    for left in range(1, 21):
        for right in range(left, 21):
            record("double_stars", double_star(left, right))
    for arm_count in range(3, 9):
        for arm_length in range(1, 13):
            record("equal_arm_spiders", spider([arm_length] * arm_count))
    for arms in itertools.combinations_with_replacement(range(1, 16), 3):
        record("3_arm_spiders", spider(list(arms)))
    for handle in range(1, 31):
        for brush in range(1, 21):
            record("brooms", broom(handle, brush))
    for spine_order in range(2, 8):
        for multiplicities in itertools.product(range(4), repeat=spine_order):
            if any(multiplicities):
                record("caterpillars_small", caterpillar(spine_order, list(multiplicities)))
    for spine_order in range(2, 31):
        for leaves_per_spine in range(1, 5):
            record(
                "uniform_caterpillars",
                caterpillar(spine_order, [leaves_per_spine] * spine_order),
            )
        record(
            "comb_internal",
            caterpillar(spine_order, [0] + [1] * (spine_order - 2) + [0]),
        )
        for period in range(2, 6):
            for multiplicity in range(1, 4):
                pattern = [multiplicity if i % period == 0 else 0 for i in range(spine_order)]
                record("periodic_caterpillars", caterpillar(spine_order, pattern))

    return {
        "parameter_instances_tested": sum(row["count"] for row in result.values()),
        "families": result,
        "counterexamples": 0,
        "classification": (
            "candidate-specific structural/counterexample search on interpretation data; "
            "not a holdout"
        ),
    }


def mis_diagnosis(rows: list[dict[str, int]]) -> dict[str, object]:
    by_order = {
        order: [row for row in rows if row["order"] == order]
        for order in range(1, 15)
    }
    stability: dict[str, dict[str, dict[str, int]]] = {}
    for candidate_id in MIS_IDS:
        relation = RELATIONS[candidate_id]
        per_order = {}
        for order in range(11, 15):
            slacks = [relation_slack(row, relation) for row in by_order[order]]
            per_order[str(order)] = {
                "failures": sum(slack < 0 for slack in slacks),
                "equalities": sum(slack == 0 for slack in slacks),
            }
            if per_order[str(order)]["failures"] or not per_order[str(order)]["equalities"]:
                raise AssertionError(f"unexpected coefficient instability for {candidate_id}")
        stability[candidate_id] = per_order

    dominance = []
    for first, second in itertools.permutations(MIS_IDS, 2):
        first_relation = RELATIONS[first]
        second_relation = RELATIONS[second]
        if first_relation[0] != second_relation[0]:
            continue
        if first_relation[0] == "<=":
            ordered = all(
                relation_bound(row, first_relation) <= relation_bound(row, second_relation)
                for row in rows
            )
        else:
            ordered = all(
                relation_bound(row, first_relation) >= relation_bound(row, second_relation)
                for row in rows
            )
        strict = any(
            relation_bound(row, first_relation) != relation_bound(row, second_relation)
            for row in rows
        )
        if ordered and strict:
            dominance.append([first, second])

    common_vector_counts = {}
    for order in range(8, 15):
        common_vector_counts[str(order)] = sum(
            row["domination_number"] == 4
            and row["diameter"] == 5
            and row["support_vertex_count"] == 4
            and row["matching_number"] == 4
            and row["maximal_independent_set_count"] == 8
            for row in by_order[order]
        )

    return {
        "candidate_ids": MIS_IDS,
        "count": len(MIS_IDS),
        "coordinate_families": {
            "mis_only": 3,
            "support_plus_mis": 6,
            "diameter_plus_mis": 9,
            "matching_plus_mis": 2,
        },
        "coefficient_stability": (
            "All 20 remain valid and have equality examples at each exposed order "
            "11,12,13,14; no frozen coefficient plane loses support."
        ),
        "mis_count_ranges": {
            str(order): [
                min(row["maximal_independent_set_count"] for row in by_order[order]),
                max(row["maximal_independent_set_count"] for row in by_order[order]),
            ]
            for order in range(10, 15)
        },
        "common_extremal_vector": {
            "domination_number": 4,
            "diameter": 5,
            "support_vertex_count": 4,
            "matching_number": 4,
            "maximal_independent_set_count": 8,
            "tight_candidate_count": 10,
            "tree_counts_by_order": common_vector_counts,
        },
        "exposed_pointwise_dominance_only": dominance,
        "diagnosis": (
            "The 20 statements are neighboring facets concentrated around repeated "
            "low-dimensional extremal vectors. Raw MIS count has strongly order-dependent "
            "scale, but coefficient stability through order 14 means scale behavior alone "
            "does not justify deleting or transforming the feature."
        ),
        "new_experiment_frozen": False,
        "reason_no_new_experiment": (
            "No independently defensible single-axis discovery change follows yet from "
            "the exposed-data diagnosis."
        ),
    }


def build_summary() -> dict[str, object]:
    rows = exposed_rows()
    equality_counts = {
        str(order): sum(target_slack(row) == 0 for row in rows if row["order"] == order)
        for order in range(1, 15)
    }
    failures = sum(target_slack(row) < 0 for row in rows)
    if failures:
        raise AssertionError("TF-001028 failed on exposed orders 1-14")

    order14_equalities = [row for row in rows if row["order"] == 14 and target_slack(row) == 0]
    order14_types: dict[tuple[int, int], int] = {}
    for row in order14_equalities:
        key = (row["diameter"], row["domination_number"])
        order14_types[key] = order14_types.get(key, 0) + 1

    return {
        "analysis_id": "TF5-TF001028",
        "starting_main_head": "308104fee32f55dc12a110357c48f15249193be5",
        "starting_main_ci_run": 37016098699,
        "tf4": {
            "scientific_source_commit": "d8e0874a22dde7f226431fc4f15a36adb8254efa",
            "scientific_run": 36983184665,
            "candidate_batch_hash": "2bbb81b85eb6e40351f0913fafdc822c5417b2336e957e83fc08b505aedabf0f",
            "holdout_hash": "84978208ee2c65e3cda8327709e662cc71f9018ef2afc1ca03ff86a19a6197c3",
            "adversarial_hash": "caf97df7db6b739383e015f816e3d643352cf53f164363d171c0eb1751e955f3",
        },
        "candidate": {
            "candidate_id": "TF-001028",
            "statement": (
                "For every finite simple tree T, domination_number <= "
                "(((2/3 * order) + 1/3) + (-1/3 * diameter))."
            ),
            "integer_form": "3*domination_number + diameter <= 2*order + 1",
            "source_feature_pair": ["order", "diameter"],
            "discovery_touch_count": 7,
            "starting_lifecycle_state": "NOVELTY_AUDIT",
            "final_lifecycle_state": "KNOWN_RESULT",
            "final_revision": 7,
            "graduation_candidate": False,
        },
        "proof_resolution": {
            "k1": "equality",
            "short_diameter": (
                "For n>=2 and 2D<=n+2, Ore gamma<=floor(n/2) implies "
                "3gamma+D<=2n+1."
            ),
            "long_diameter": (
                "For 2D>=n+2, Gu-Meng-Zhang-Wan 2013 Lemma 2.3 gives "
                "gamma<=n-D+ceil((2D-n-1)/3); 3ceil(x/3)<=x+2 implies the candidate."
            ),
            "coverage": (
                "For integer D, the two regimes cover every nontrivial tree; "
                "the even boundary belongs to both."
            ),
            "explicit_equality_families": ["K1", "P_{3k+1}", "P_k corona K1 for k>=2"],
        },
        "exposed_exhaustive_check": {
            "orders": [1, 14],
            "tree_count": len(rows),
            "failures": failures,
            "equality_counts_by_order": equality_counts,
            "order14_equality_count": len(order14_equalities),
            "order14_equality_types": [
                {"diameter": diameter, "domination_number": gamma, "count": count}
                for (diameter, gamma), count in sorted(order14_types.items(), reverse=True)
            ],
            "classification": "exposed interpretation data; not fresh evidence and not proof",
        },
        "family_search": family_search(),
        "prior_art": [
            {
                "source": "O. Ore, Theory of Graphs, AMS Colloquium Publications 38 (1962)",
                "result": "isolate-free graph gamma<=floor(n/2)",
                "role": "proves short-diameter regime",
            },
            {
                "source": (
                    "Z. Gu, J. Meng, Z. Zhang, J. E. Wan, Some Upper Bounds Related "
                    "with Domination Number, J. Oper. Res. Soc. China 1 (2013), 217-225, "
                    "DOI 10.1007/s40305-013-0012-0"
                ),
                "result": (
                    "Lemma 2.3: exact maximum gamma for trees of fixed n,D when "
                    "D>=n/2+1"
                ),
                "role": "proves long-diameter regime and is stronger prior art",
            },
            {
                "source": (
                    "A. Cabrera Martinez, An improved upper bound on the domination "
                    "number of a tree, Discrete Appl. Math. 343 (2024), 44-48, "
                    "DOI 10.1016/j.dam.2023.10.013"
                ),
                "result": "support-structure upper bounds for gamma(T)",
                "role": "related recent tree upper bound; not needed for implication",
            },
            {
                "source": (
                    "J. Guo, J. Xue, R. Liu, Laplacian eigenvalue distribution, diameter "
                    "and domination number of trees, Linear Multilinear Algebra 73 (2025), "
                    "763-775, DOI 10.1080/03081087.2024.2385991"
                ),
                "result": "diameter/domination relation via Laplacian eigenvalue counts",
                "role": "related recent diameter work; not the candidate",
            },
        ],
        "mis_facet_diagnosis": mis_diagnosis(rows),
        "next_permanent_candidate_id": "TF-001158",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=TF5_SUMMARY)
    args = parser.parse_args()
    payload = build_summary()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
